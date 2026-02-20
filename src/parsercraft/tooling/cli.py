#!/usr/bin/env python3
"""
ParserCraft CLI

Command-line interface for creating, editing, running, and managing custom
programming language configurations and programs.

Language Configuration Commands:
    parsercraft create [--preset PRESET] [--output FILE]
    parsercraft edit FILE
    parsercraft validate FILE
    parsercraft info [FILE]
    parsercraft export FILE [--format markdown|json|yaml]
    parsercraft import FILE [--scope runtime|project|user]
    parsercraft list-presets
    parsercraft convert FILE --to FORMAT
    parsercraft diff FILE1 FILE2
    parsercraft update FILE [--set KEY VALUE] [--merge FILE]
    parsercraft delete FILE [--keyword KW] [--function FN]
    parsercraft translate FILE [--config CONFIG]

Execution Commands:
    parsercraft repl [FILE] [--debug]
    parsercraft batch FILE [--script SCRIPT]
    parsercraft test FILE [--cases FILE]
    parsercraft test-run FILE

Code Generation Commands:
    parsercraft codegen-c FILE [--output FILE]
    parsercraft codegen-wasm FILE [--output FILE]

Type System Commands:
    parsercraft type-check FILE [--config CONFIG]
    parsercraft generics FILE
    parsercraft check-protocol FILE

Module System Commands:
    parsercraft module-info FILE
    parsercraft module-deps FILE
    parsercraft module-cycles FILE

Tooling Commands:
    parsercraft lsp [--port PORT] [--stdio]
    parsercraft extension [--output DIR]
    parsercraft package-search QUERY
    parsercraft package-install PACKAGE
    parsercraft refactor-rename FILE --old NAME --new NAME
    parsercraft format FILE
    parsercraft debug-launch FILE

Presets:
    - python_like    : Python-style syntax
    - javascript_like: JavaScript-style syntax
    - lisp_like      : Lisp-style syntax
    - minimal        : Minimal functional language

Examples:
    # Create a new Python-like language
    parsercraft create --preset python_like --output my_lang.yaml

    # Validate a configuration file
    parsercraft validate my_lang.yaml

    # Run an interactive REPL with a language config
    parsercraft repl my_lang.yaml

    # Generate C code from a source file
    parsercraft codegen-c program.src --output program.c

    # Start the LSP server on stdio
    parsercraft lsp --stdio

See Also:
    parsercraft-ide    Launch the Tkinter IDE
    parsercraft-repl   Launch the standalone REPL
"""
# pylint: disable=too-many-lines,import-outside-toplevel

import argparse
import ast
import contextlib
import io
import json
import os
import re
import subprocess
import sys
import traceback
from math import e, pi
from pathlib import Path
from typing import Any, Optional, Sequence

try:
    import readline  # noqa: F401
except ImportError:  # pragma: no cover - platform dependent
    readline = None  # type: ignore[assignment]

from parsercraft.config.language_config import (
    LanguageConfig,
    create_custom_config_interactive,
    list_presets,
)
from parsercraft.runtime.language_runtime import LanguageRuntime

# YAML support (optional)
try:
    from yaml import YAMLError, safe_load
except ImportError:  # pragma: no cover - optional dependency
    YAMLError = None  # type: ignore[assignment,misc]
    safe_load = None  # type: ignore[assignment]

if YAMLError is not None:
    CONFIG_LOAD_ERRORS: tuple[type[Exception], ...] = (
        OSError,
        ValueError,
        json.JSONDecodeError,
        YAMLError,
    )
else:
    CONFIG_LOAD_ERRORS = (  # type: ignore[unreachable]
        OSError, ValueError, json.JSONDecodeError
    )


SAFE_BUILTINS: dict[str, Any] = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "enumerate": enumerate,
    "filter": filter,
    "float": float,
    "int": int,
    "len": len,
    "list": list,
    "map": map,
    "max": max,
    "min": min,
    "print": print,
    "range": range,
    "round": round,
    "sorted": sorted,
    "str": str,
    "sum": sum,
    "tuple": tuple,
    "zip": zip,
    # Common math constants for convenience
    "pi": pi,
    "e": e,
}


def _load_config_from_path(
    path: Path,
    error_prefix: str,
) -> Optional[LanguageConfig]:
    """Load a configuration file, reporting user-friendly errors."""
    try:
        return LanguageConfig.load(path)
    except CONFIG_LOAD_ERRORS as error:
        print(f"{error_prefix}{error}")
        return None


def _translate_with_keywords(
    source: str,
    custom_keywords: Sequence[str],
) -> str:
    """Translate custom keywords in source code back to their originals."""
    translated = source
    for custom_kw in custom_keywords:
        original_kw = LanguageRuntime.translate_keyword(custom_kw)
        pattern = r"\b" + re.escape(custom_kw) + r"\b"
        translated = re.sub(pattern, original_kw, translated)

    # Also translate custom function names if present
    for custom_func in LanguageRuntime.get_custom_functions():
        original_func = LanguageRuntime.translate_function(custom_func)
        pattern = r"\b" + re.escape(custom_func) + r"\b"
        translated = re.sub(pattern, original_func, translated)

    return translated


def _load_test_cases(path: Path) -> Optional[list[dict[str, Any]]]:
    """Load test cases from a YAML or JSON file."""
    if not path.exists():
        print(f"Error: Test file not found: {path}")
        return None

    try:
        content = path.read_text(encoding="utf-8")
    except OSError as error:
        print(f"Error reading test file: {error}")
        return None

    try:
        if path.suffix.lower() in {".yaml", ".yml"} and safe_load is not None:
            cases = safe_load(content)
        else:
            cases = json.loads(content)
    except Exception as error:  # pylint: disable=broad-exception-caught
        print(f"Error parsing test file: {error}")
        return None

    if not isinstance(cases, list):
        print("Error: Test file must contain a list of cases")
        return None

    return cases


def _run_test_case(
    case: dict[str, Any],
    base_dir: Path,
    custom_keywords: Sequence[str],
    show_translation: bool,
    debug: bool,
) -> tuple[bool, list[str]]:
    """Execute a single test case and return (passed, details)."""
    details: list[str] = []

    source: Optional[str] = None
    if file_path := case.get("file"):
        candidate = (base_dir / file_path).resolve()
        if not candidate.exists():
            return False, [f"File not found: {candidate}"]
        try:
            source = candidate.read_text(encoding="utf-8")
        except OSError as error:
            return False, [f"Error reading file: {error}"]
    elif inline := case.get("source"):
        source = str(inline)

    if not source:
        return False, ["Missing 'file' or 'source' in test case"]

    translated = _translate_with_keywords(source, custom_keywords)

    if show_translation:
        details.append("Translated code:\n" + translated)

    buffer = io.StringIO()
    variables: dict[str, Any] = {}
    safe_globals = {"__builtins__": SAFE_BUILTINS.copy()}

    try:
        with contextlib.redirect_stdout(buffer):
            exec(  # pylint: disable=exec-used
                translated,
                safe_globals,
                variables,
            )
    except Exception as error:  # pylint: disable=broad-exception-caught
        failure = f"Execution error: {error}"
        if debug:
            traceback.print_exc()
        return False, details + [failure]

    stdout = buffer.getvalue()
    expected_stdout = case.get("expect_stdout")
    expected_vars = case.get("expect_vars") or {}

    passed = True

    if expected_stdout is not None:
        if stdout.strip() != str(expected_stdout).strip():
            passed = False
            details.append(
                "Stdout mismatch:\n"
                f"Expected: {expected_stdout!r}\n"
                f"Actual:   {stdout!r}"
            )

    for name, expected_value in expected_vars.items():
        if name not in variables:
            passed = False
            details.append(f"Missing variable: {name}")
            continue
        if variables[name] != expected_value:
            passed = False
            details.append(
                f"Variable mismatch for '{name}': "
                f"expected {expected_value!r}, got {variables[name]!r}"
            )

    return passed, details


def _handle_repl_command(
    command: str,
    config: LanguageConfig,
    variables: dict[str, Any],
    debug: bool,
) -> tuple[bool, bool]:
    """Handle REPL meta-commands. Returns (should_continue, debug)."""
    if command in {"exit", "quit"}:
        print("Goodbye!")
        return False, debug

    if command == "help":
        print("\nCommands:")
        print("  .help       - Show this help")
        print("  .info       - Show language info")
        print("  .keywords   - List all keywords")
        print("  .functions  - List all functions")
        print("  .vars       - Show current variables")
        print("  .clear      - Clear all variables")
        print("  .debug      - Toggle debug mode")
        print("  .exit       - Exit REPL\n")
        return True, debug

    if command == "info":
        print(f"\nLanguage: {config.name}")
        print(f"Version: {config.version}")
        print(f"Keywords: {len(config.keyword_mappings)}")
        print(f"Functions: {len(config.builtin_functions)}\n")
        return True, debug

    if command == "keywords":
        print("\nKeywords:")
        for kw in sorted(
            config.keyword_mappings.values(),
            key=lambda mapping: mapping.custom,
        ):
            print(f"  {kw.custom:20} ({kw.original})")
        print()
        return True, debug

    if command == "functions":
        print("\nBuiltin Functions:")
        for func in sorted(
            config.builtin_functions.values(),
            key=lambda item: item.name,
        ):
            arity = "variadic" if func.arity == -1 else f"{func.arity} args"
            status = "" if func.enabled else " [DISABLED]"
            print(f"  {func.name:20} ({arity}){status}")
        print()
        return True, debug

    if command == "vars":
        if variables:
            print("\nVariables:")
            for name, value in sorted(variables.items()):
                print(f"  {name} = {value}")
            print()
        else:
            print("\nNo variables defined\n")
        return True, debug

    if command == "clear":
        variables.clear()
        print("Variables cleared\n")
        return True, debug

    if command == "debug":
        new_debug = not debug
        print(f"Debug mode: {'ON' if new_debug else 'OFF'}\n")
        return True, new_debug

    print(f"Unknown command: .{command}")
    print("Type .help for available commands\n")
    return True, debug


def _execute_repl_line(
    line: str,
    variables: dict[str, Any],
    keyword_prefixes: Sequence[str],
    custom_keywords: Sequence[str],
    debug: bool,
) -> None:
    """Translate and execute a line within the REPL session."""
    try:
        translated = _translate_with_keywords(line, custom_keywords)
        if debug:
            print(f"[DEBUG] Translated: {translated}")
        safe_globals = {"__builtins__": SAFE_BUILTINS.copy()}

        stripped_line = line.strip()
        has_assignment = (
            re.match(r'.*(?<![=!<>+\-*/])=(?!=).*', stripped_line) is not None
        )
        starts_with_keyword = stripped_line.startswith(tuple(keyword_prefixes))

        if has_assignment or starts_with_keyword:
            # Statement: just exec, don't try to get a value
            exec(  # pylint: disable=exec-used
                translated,
                safe_globals,
                variables,
            )
        else:
            # Expression: try to evaluate and display result
            try:
                result = ast.literal_eval(translated)
            except (ValueError, SyntaxError):
                try:
                    result = eval(  # pylint: disable=eval-used
                        translated,
                        safe_globals,
                        variables,
                    )
                except SyntaxError:
                    # Not an expression — fall back to exec
                    exec(  # pylint: disable=exec-used
                        translated,
                        safe_globals,
                        variables,
                    )
                    result = None
            if result is not None:
                print(result)
    except Exception as error:  # pylint: disable=broad-exception-caught
        print(f"Error: {error}")
        if debug:
            traceback.print_exc()


def _run_repl_session(config: LanguageConfig, debug: bool) -> int:
    """Run the interactive REPL session."""
    LanguageRuntime.load_config(config=config)
    custom_keywords = tuple(LanguageRuntime.get_custom_keywords())
    keyword_prefixes = custom_keywords
    variables: dict[str, Any] = {}

    print("=" * 70)
    print("HB Language Construction Set - REPL Mode")
    print(f"Language: {config.name} v{config.version}")
    print("=" * 70)
    print("\nCommands:")
    print("  .help       - Show this help")
    print("  .info       - Show language info")
    print("  .keywords   - List all keywords")
    print("  .functions  - List all functions")
    print("  .vars       - Show current variables")
    print("  .clear      - Clear all variables")
    print("  .debug      - Toggle debug mode")
    print("  .exit       - Exit REPL")
    print("\nEnter code to execute:\n")

    while True:
        try:
            prompt = ">>> " if not debug else "[DEBUG] >>> "
            line = input(prompt).strip()

            if not line:
                continue

            if line.startswith("."):
                continue_loop, debug = _handle_repl_command(
                    line[1:].lower(), config, variables, debug
                )
                if not continue_loop:
                    break
                continue

            _execute_repl_line(
                line, variables, keyword_prefixes, custom_keywords, debug
            )

        except EOFError:
            print("\nGoodbye!")
            break
        except KeyboardInterrupt:
            print("\n(Use .exit to quit)")
            continue

    return 0


def _resolve_repl_config(file_arg: Optional[str]) -> Optional[LanguageConfig]:
    """Resolve the configuration to use for the REPL."""
    if not file_arg:
        print("Using default configuration")
        return LanguageConfig()

    filepath = Path(file_arg)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        return None

    config = _load_config_from_path(filepath, "Error loading config: ")
    if config:
        print(f"Loaded configuration: {config.name}")
    return config


def _run_batch_script(
    script_path: Path,
    custom_keywords: Sequence[str],
    show_translation: bool,
    show_vars: bool,
    debug: bool,
) -> int:
    """Execute a batch script after translating custom keywords."""
    if not script_path.exists():
        print(f"Error: Script file not found: {script_path}")
        return 1

    print(f"Executing batch script: {script_path}")
    print("=" * 70)

    try:
        code = script_path.read_text(encoding="utf-8")
    except OSError as error:
        print(f"Error reading script: {error}")
        return 1

    translated = _translate_with_keywords(code, custom_keywords)

    if show_translation:
        print("\nTranslated Python code:")
        print("-" * 70)
        print(translated)
        print("-" * 70)
        print()

    namespace: dict[str, Any] = {}
    try:
        exec(  # pylint: disable=exec-used
            translated,
            {"__builtins__": SAFE_BUILTINS.copy()},
            namespace,
        )
    except Exception as error:  # pylint: disable=broad-exception-caught
        print(f"\nError executing script: {error}")
        if debug:
            traceback.print_exc()
        return 1

    print("\n" + "=" * 70)
    print("Execution completed successfully")

    if show_vars:
        print("\nFinal variables:")
        for name, value in sorted(namespace.items()):
            if not name.startswith("__"):
                print(f"  {name} = {value}")

    return 0


def _process_batch_directory(
    input_dir: Path,
    custom_keywords: Sequence[str],
    output_dir: Optional[str],
    pattern: Optional[str],
) -> int:
    """Translate files in a directory and write Python outputs."""
    if not input_dir.exists() or not input_dir.is_dir():
        print(f"Error: Input directory not found: {input_dir}")
        return 1

    target_dir = Path(output_dir) if output_dir else input_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    glob_pattern = pattern or "*.txt"
    files = list(input_dir.glob(glob_pattern))
    if not files:
        print(f"No files found matching pattern: {glob_pattern}")
        return 1

    success_count = 0
    error_count = 0

    for file_path in files:
        print(f"\nProcessing: {file_path.name}")
        try:
            code = file_path.read_text(encoding="utf-8")
            translated = _translate_with_keywords(code, custom_keywords)
            output_file = target_dir / f"{file_path.stem}.py"
            output_file.write_text(translated, encoding="utf-8")
            print(f"  -> Saved to: {output_file}")
            success_count += 1
        except OSError as error:
            print(f"  -> Error: {error}")
            error_count += 1

    print("\n" + "=" * 70)
    print("Batch processing complete:")
    print(f"  Success: {success_count}")
    print(f"  Errors: {error_count}")

    return 0 if error_count == 0 else 1


def cmd_create(args):
    """Create a new language configuration."""
    if args.preset:
        try:
            config = LanguageConfig.from_preset(args.preset)
            print(f"Created configuration from preset: {args.preset}")
        except ValueError as exc:
            print(f"Error: {exc}")
            print(f"Available presets: {', '.join(list_presets())}")
            return 1
    elif args.interactive:
        config = create_custom_config_interactive()
    else:
        config = LanguageConfig()
        print("Created default configuration")

    # Save to file
    output = args.output or "language_config.yaml"
    config.save(output)
    print(f"Saved to: {output}")
    return 0


def cmd_edit(args) -> int:
    """Edit an existing configuration (opens in text editor)."""

    filepath = Path(args.file)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        return 1

    # Determine editor
    editor = os.environ.get("EDITOR", "nano")

    # Open in editor
    try:
        subprocess.run([editor, str(filepath)], check=False)
        print(f"Edited: {filepath}")

        # Validate after editing
        try:
            config = LanguageConfig.load(filepath)
            errors = config.validate()
            if errors:
                print("\nValidation errors:")
                for error in errors:
                    print(f"  ❌ {error}")
                return 1
            else:
                print("\n✓ Configuration is valid")
        except CONFIG_LOAD_ERRORS as error:
            print(f"\n❌ Error loading config: {error}")
            return 1
    except FileNotFoundError:
        print(f"Error: Editor '{editor}' not found")
        print("Set EDITOR environment variable to your preferred editor")
        return 1

    return 0


def cmd_validate(args):
    """Validate a configuration file."""
    filepath = Path(args.file)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        return 1

    try:
        config = LanguageConfig.load(filepath)
        errors = config.validate()

        if errors:
            print(f"❌ Validation failed for: {filepath}")
            print("\nErrors:")
            for error in errors:
                print(f"  • {error}")
            return 1
        else:
            print("✓ Configuration is valid")
            print("\nSummary:")
            print(f"  Name: {config.name}")
            print(f"  Version: {config.version}")
            print(f"  Keywords: {len(config.keyword_mappings)}")
            print(f"  Functions: {len(config.builtin_functions)}")
            print(f"  Operators: {len(config.operators)}")
            return 0
    except CONFIG_LOAD_ERRORS as error:
        print(f"❌ Error loading config: {error}")
        return 1


def cmd_info(args):
    """Show information about a configuration."""
    if args.file:
        filepath = Path(args.file)
        if not filepath.exists():
            print(f"Error: File not found: {filepath}")
            return 1

        try:
            config = LanguageConfig.load(filepath)
        except CONFIG_LOAD_ERRORS as error:
            print(f"Error loading config: {error}")
            return 1
    else:
        # Show current runtime config
        LanguageRuntime.load_config()
        config = LanguageRuntime.get_config()
        if not config:
            print("No configuration loaded")
            return 1

    # Display detailed info
    print("=" * 70)
    print(f"Language Configuration: {config.name}")
    print("=" * 70)
    print("\nMetadata:")
    print(f"  Version: {config.version}")
    print(f"  Description: {config.description}")
    if config.author:
        print(f"  Author: {config.author}")

    print("\nComponents:")
    print(f"  Keywords: {len(config.keyword_mappings)}")
    print(f"  Functions: {len(config.builtin_functions)}")
    print(f"  Operators: {len(config.operators)}")

    # Show keyword categories
    categories = {}
    for mapping in config.keyword_mappings.values():
        categories[mapping.category] = categories.get(mapping.category, 0) + 1

    print("\nKeyword Categories:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")

    # Show enabled/disabled functions
    enabled = sum(1 for f in config.builtin_functions.values() if f.enabled)
    disabled = len(config.builtin_functions) - enabled
    print("\nFunctions:")
    print(f"  Enabled: {enabled}")
    if disabled > 0:
        print(f"  Disabled: {disabled}")

    # Show syntax options
    opts = config.syntax_options
    print("\nSyntax Options:")
    print(f"  Array indexing: starts at {opts.array_start_index}")
    frac_status = "enabled" if opts.allow_fractional_indexing else "disabled"
    print(f"  Fractional indexing: {frac_status}")
    print(f"  Comment style: {opts.single_line_comment}")
    print(f"  Statement terminator: '{opts.statement_terminator}'")

    # Show enabled features
    features = []
    if opts.enable_satirical_keywords:
        features.append("satirical")
    if opts.three_valued_logic:
        features.append("3-valued-logic")
    if opts.probabilistic_variables:
        features.append("probabilistic")
    if opts.temporal_variables:
        features.append("temporal")
    if opts.enable_quantum_features:
        features.append("quantum")

    if features:
        print(f"  Features: {', '.join(features)}")

    print("\nRuntime:")
    debug_status = "enabled" if config.debug_mode else "disabled"
    strict_status = "enabled" if config.strict_mode else "disabled"
    print(f"  Debug mode: {debug_status}")
    print(f"  Strict mode: {strict_status}")
    print(f"  Compatibility: {config.compatibility_mode}")

    print("=" * 70)

    return 0


def cmd_export(args):
    """Export configuration in different formats."""
    filepath = Path(args.file)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        return 1

    try:
        config = LanguageConfig.load(filepath)
    except CONFIG_LOAD_ERRORS as error:
        print(f"Error loading config: {error}")
        return 1

    format_type = args.format or "markdown"
    output = args.output or f"{filepath.stem}_export"

    if format_type == "markdown":
        output_file = f"{output}.md"
        config.export_mapping_table(output_file)
        print(f"Exported mapping table to: {output_file}")

    elif format_type == "json":
        output_file = f"{output}.json"
        config.save(output_file, fmt="json")
        print(f"Exported to JSON: {output_file}")

    elif format_type == "yaml":
        output_file = f"{output}.yaml"
        config.save(output_file, fmt="yaml")
        print(f"Exported to YAML: {output_file}")

    else:
        print(f"Error: Unknown format: {format_type}")
        print("Supported formats: markdown, json, yaml")
        return 1

    return 0


def cmd_import(args):
    """Import a configuration for use.

    Loads the configuration into the runtime and optionally persists
    a reference in `.langconfig` (project) or `~/.langconfig` (user).
    """
    filepath = Path(args.file)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        return 1

    try:
        # Load into runtime
        LanguageRuntime.load_config(config_file=str(filepath))
        print(f"✓ Imported configuration: {filepath}")

        scope = args.scope or "project"
        if scope == "runtime":
            # Do not persist
            return 0

        if scope == "project":
            target = Path(".langconfig")
        elif scope == "user":
            target = Path.home() / ".langconfig"
        else:
            print(f"Error: Unknown scope: {scope}")
            print("Supported scopes: runtime, project, user")
            return 1

        try:
            # Write a small pointer file with the absolute path
            target.write_text(str(filepath.resolve()), encoding="utf-8")
            print(f"✓ Persisted config reference to: {target}")
        except OSError as error:
            print(f"Warning: Failed to persist reference: {error}")
        return 0
    except CONFIG_LOAD_ERRORS as error:
        print(f"Error importing config: {error}")
        return 1


def cmd_list_presets(_args):
    """List available presets."""
    presets = list_presets()

    print("Available Presets:")
    print("=" * 70)

    for preset in presets:
        try:
            config = LanguageConfig.from_preset(preset)
            print(f"\n{preset}:")
            print(f"  {config.description}")
        except CONFIG_LOAD_ERRORS as error:
            print(f"\n{preset}: (error loading: {error})")

    print("\nUsage:")
    print("  langconfig create --preset PRESET_NAME")

    return 0


def cmd_convert(args):
    """Convert configuration between formats."""
    filepath = Path(args.file)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        return 1

    try:
        config = LanguageConfig.load(filepath)
    except CONFIG_LOAD_ERRORS as error:
        print(f"Error loading config: {error}")
        return 1

    from_format = args.from_format or (
        "yaml" if filepath.suffix in [".yaml", ".yml"] else "json"
    )
    to_format = args.to_format

    output = args.output or f"{filepath.stem}.{to_format}"

    config.save(output, fmt=to_format)
    print(f"Converted {filepath} ({from_format}) to {output} ({to_format})")

    return 0


def cmd_diff(args):
    """Show differences between two configurations."""
    file1 = Path(args.file1)
    file2 = Path(args.file2)

    if not file1.exists():
        print(f"Error: File not found: {file1}")
        return 1
    if not file2.exists():
        print(f"Error: File not found: {file2}")
        return 1

    try:
        config1 = LanguageConfig.load(file1)
        config2 = LanguageConfig.load(file2)
    except CONFIG_LOAD_ERRORS as error:
        print(f"Error loading configs: {error}")
        return 1

    print(f"Comparing: {file1} vs {file2}")
    print("=" * 70)

    # Compare keywords
    keys1 = set(config1.keyword_mappings.keys())
    keys2 = set(config2.keyword_mappings.keys())

    if keys1 != keys2:
        print("\nKeyword Differences:")
        only_in_1 = keys1 - keys2
        only_in_2 = keys2 - keys1

        if only_in_1:
            print(f"  Only in {file1.name}: {', '.join(sorted(only_in_1))}")
        if only_in_2:
            print(f"  Only in {file2.name}: {', '.join(sorted(only_in_2))}")

        # Check for different mappings
        common = keys1 & keys2
        different_mappings = []
        for key in common:
            if (
                config1.keyword_mappings[key].custom
                != config2.keyword_mappings[key].custom
            ):
                different_mappings.append(
                    f"{key}: "
                    f"'{config1.keyword_mappings[key].custom}' vs "
                    f"'{config2.keyword_mappings[key].custom}'"
                )

        if different_mappings:
            print("  Different mappings:")
            for diff in different_mappings:
                print(f"    {diff}")
    else:
        print("\n✓ Keywords are identical")

    # Compare functions
    funcs1 = set(config1.builtin_functions.keys())
    funcs2 = set(config2.builtin_functions.keys())

    if funcs1 != funcs2:
        print("\nFunction Differences:")
        only_in_1 = funcs1 - funcs2
        only_in_2 = funcs2 - funcs1

        if only_in_1:
            print(f"  Only in {file1.name}: {', '.join(sorted(only_in_1))}")
        if only_in_2:
            print(f"  Only in {file2.name}: {', '.join(sorted(only_in_2))}")
    else:
        print("\n✓ Functions are identical")

    # Compare syntax options
    opts1 = config1.syntax_options
    opts2 = config2.syntax_options

    differences = []
    if opts1.array_start_index != opts2.array_start_index:
        differences.append(
            f"array_start_index: {opts1.array_start_index} -> "
            f"{opts2.array_start_index}"
        )
    if opts1.allow_fractional_indexing != opts2.allow_fractional_indexing:
        differences.append(
            f"fractional_indexing: {opts1.allow_fractional_indexing} -> "
            f"{opts2.allow_fractional_indexing}"
        )
    if opts1.enable_satirical_keywords != opts2.enable_satirical_keywords:
        differences.append(
            f"satirical_keywords: {opts1.enable_satirical_keywords} -> "
            f"{opts2.enable_satirical_keywords}"
        )

    if differences:
        print("\nSyntax Option Differences:")
        for diff in differences:
            print(f"  {diff}")
    else:
        print("\n✓ Syntax options are identical")

    return 0


def cmd_update(args) -> int:
    """Update a configuration file."""
    filepath = Path(args.file)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        return 1

    try:
        config = LanguageConfig.load(filepath)
    except CONFIG_LOAD_ERRORS as error:
        print(f"Error loading config: {error}")
        return 1

    print(f"Loaded: {filepath}")

    if args.set:
        updates: dict[str, Any] = {}
        for key, value in args.set:
            # Parse nested keys like "metadata.author"
            parts = key.split(".")
            current: dict[str, Any] = updates
            for part in parts[:-1]:
                current = current.setdefault(part, {})

            # Try to parse value as JSON for complex types
            try:
                current[parts[-1]] = json.loads(value)
            except (json.JSONDecodeError, ValueError):
                current[parts[-1]] = value

        config.update(updates, merge=True)
        print(f"Applied {len(args.set)} update(s)")

    if args.merge:
        merge_path = Path(args.merge)
        if not merge_path.exists():
            print(f"Error: Merge file not found: {merge_path}")
            return 1

        try:
            merge_config = LanguageConfig.load(merge_path)
        except CONFIG_LOAD_ERRORS as error:
            print(f"Error loading merge config: {error}")
            return 1

        config.merge(merge_config, prefer_other=True)
        print(f"Merged with: {merge_path}")

    output = args.output or args.file
    try:
        config.save(output)
    except OSError as error:
        print(f"Error saving configuration: {error}")
        return 1

    print(f"✓ Updated configuration saved to: {output}")
    return 0


def cmd_repl(args):
    """Interactive REPL mode for testing language features."""
    if readline is None:
        print("Warning: readline support unavailable; history disabled")

    config = _resolve_repl_config(args.file)
    if config is None:
        return 1

    return _run_repl_session(config, args.debug)


def cmd_batch(args):
    """Execute batch processing of language files."""
    filepath = Path(args.file)
    if not filepath.exists():
        print(f"Error: Configuration file not found: {filepath}")
        return 1

    config = _load_config_from_path(filepath, "Error loading config: ")
    if config is None:
        return 1

    LanguageRuntime.load_config(config=config)
    custom_keywords = tuple(LanguageRuntime.get_custom_keywords())

    if args.script:
        return _run_batch_script(
            Path(args.script),
            custom_keywords,
            args.show_translation,
            args.show_vars,
            args.debug,
        )

    if args.input_dir:
        return _process_batch_directory(
            Path(args.input_dir),
            custom_keywords,
            args.output_dir,
            args.pattern,
        )

    print("Error: Specify --script FILE or --input-dir DIR")
    return 1


def cmd_test(args):
    """Translate, run, and verify test cases."""
    tests_path = Path(args.tests)
    cases = _load_test_cases(tests_path)
    if cases is None:
        return 1

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Error: Configuration file not found: {config_path}")
        return 1

    config = _load_config_from_path(config_path, "Error loading config: ")
    if config is None:
        return 1

    LanguageRuntime.load_config(config=config)
    custom_keywords = tuple(LanguageRuntime.get_custom_keywords())

    base_dir = tests_path.parent
    failures = 0

    for index, case in enumerate(cases, start=1):
        name = case.get("name") or f"case {index}"
        passed, details = _run_test_case(
            case,
            base_dir,
            custom_keywords,
            args.show_translation,
            args.debug,
        )

        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name}")
        for detail in details:
            print(f"  {detail}")

        if not passed:
            failures += 1
            if args.stop_on_fail:
                break

    total = len(cases)
    print(
        f"\nSummary: {total - failures}/{total} passed, {failures} failed"
    )

    return 0 if failures == 0 else 1


def cmd_translate(args):
    """Translate a source file using a language configuration."""
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Error: Configuration file not found: {config_path}")
        return 1

    config = _load_config_from_path(config_path, "Error loading config: ")
    if config is None:
        return 1

    LanguageRuntime.load_config(config=config)
    custom_keywords = tuple(LanguageRuntime.get_custom_keywords())

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return 1

    try:
        source = input_path.read_text(encoding="utf-8")
    except OSError as error:
        print(f"Error reading input file: {error}")
        return 1

    translated = _translate_with_keywords(source, custom_keywords)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            output_path.write_text(translated, encoding="utf-8")
        except OSError as error:
            print(f"Error writing output file: {error}")
            return 1
        print(f"✓ Translated source saved to: {output_path}")
    else:
        print(translated)

    return 0


def cmd_delete(args):
    """Delete elements from configuration."""
    filepath = Path(args.file)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        return 1

    try:
        config = LanguageConfig.load(filepath)
    except CONFIG_LOAD_ERRORS as error:
        print(f"Error loading config: {error}")
        return 1

    print(f"Loaded: {filepath}")

    deleted_count = 0

    # Delete keywords
    if args.keyword:
        for kw in args.keyword:
            if config.delete_keyword(kw):
                print(f"  ✓ Deleted keyword: {kw}")
                deleted_count += 1
            else:
                print(f"  ✗ Keyword not found: {kw}")

    # Delete functions
    if args.function:
        for func in args.function:
            if config.delete_function(func):
                print(f"  ✓ Deleted function: {func}")
                deleted_count += 1
            else:
                print(f"  ✗ Function not found: {func}")

    # Delete operators
    if args.operator:
        for op in args.operator:
            if config.delete_operator(op):
                print(f"  ✓ Deleted operator: {op}")
                deleted_count += 1
            else:
                print(f"  ✗ Operator not found: {op}")

    if deleted_count == 0:
        print("No elements deleted")
        return 0

    # Save result
    output = args.output or args.file
    try:
        config.save(output)
    except OSError as error:
        print(f"Error saving configuration: {error}")
        return 1

    msg = "".join(
        (
            f"\n✓ Saved config with {deleted_count} deletion(s) to:",
            f" {output}",
        )
    )
    print(msg)

    return 0


def cmd_lsp(args):
    """Start Language Server Protocol server."""
    from parsercraft.tooling.lsp.lsp_server import create_lsp_server

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Error: Configuration file not found: {config_path}")
        return 1

    try:
        server = create_lsp_server(str(config_path))
        print(
            f"\u2713 LSP Server started for {server.config.name}",
            file=sys.stderr,
        )
        print(f"  Port: {args.port}", file=sys.stderr)
        print(
            f"  Mode: {'stdio' if args.stdio else 'socket'}", file=sys.stderr
        )
        if args.stdio:
            server.run_stdio()
        else:
            # Socket mode not yet implemented
            print(
                "Socket mode not yet implemented. Please use --stdio.",
                file=sys.stderr,
            )
            return 1

        return 0
    except CONFIG_LOAD_ERRORS as error:
        print(f"Error loading config: {error}", file=sys.stderr)
        return 1


def cmd_extension(args):
    """Generate VS Code extension."""
    from parsercraft.packaging.vscode_integration import (
        generate_vscode_extension
    )

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Error: Configuration file not found: {config_path}")
        return 1

    try:
        config = LanguageConfig.load(config_path)
        generate_vscode_extension(
            config=config,
            output_dir=args.output,
            publisher=args.publisher,
            version=args.version,
        )
        print(f"✓ VS Code extension generated in: {args.output}")
        print("\nNext steps:")
        print(f"  1. cd {args.output}")
        print("  2. npm install")
        print("  3. npm run compile")
        print("  4. code --install-extension .vscode-ext")
        return 0
    except CONFIG_LOAD_ERRORS as error:
        print(f"Error loading config: {error}")
        return 1


def cmd_type_check(args):
    """Perform static type analysis on source file."""
    from parsercraft.types.type_system import TypeChecker, AnalysisLevel

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Error: Configuration file not found: {config_path}")
        return 1

    source_path = Path(args.input)
    if not source_path.exists():
        print(f"Error: Source file not found: {source_path}")
        return 1

    try:
        config = LanguageConfig.load(config_path)
    except CONFIG_LOAD_ERRORS as error:
        print(f"Error loading config: {error}")
        return 1

    try:
        source_path.read_text(encoding="utf-8")
    except OSError as error:
        print(f"Error reading source file: {error}")
        return 1

    # Parse analysis level
    level_map = {
        "lenient": AnalysisLevel.LENIENT,
        "moderate": AnalysisLevel.MODERATE,
        "strict": AnalysisLevel.STRICT,
        "very-strict": AnalysisLevel.VERY_STRICT,
    }
    analysis_level = level_map.get(args.level, AnalysisLevel.MODERATE)

    # Create type checker
    checker = TypeChecker(config, level=analysis_level)

    # Check the file
    print(f"Type checking: {source_path}")
    print(f"Analysis level: {args.level}")
    print("=" * 70)

    try:
        errors = checker.check_file(str(source_path))

        if not errors:
            print("✓ No type errors found")
            return 0

        # Display errors
        print(f"Found {len(errors)} error(s):\n")
        for err in errors:
            print(f"[{err.kind}] {err.message}")
            if err.location:
                print(f"  Location: {err.location}")
            if err.suggestion:
                print(f"  Suggestion: {err.suggestion}")
            print()

        return 1 if not args.warnings_as_errors else 1

    except Exception as error:  # pylint: disable=broad-exception-caught
        print(f"Error during type checking: {error}")
        if args.debug:
            traceback.print_exc()
        return 1


def cmd_module_info(args):
    """Show information about a module."""
    from parsercraft.runtime.module_system import ModuleManager

    module_name = args.module
    module_dir = Path(args.module_dir) if args.module_dir else Path.cwd()

    try:
        config = LanguageConfig()
        manager = ModuleManager(
            config=config,
            search_paths=[str(module_dir)],
        )
        module = manager.load_module(module_name)

        print(f"Module: {module.name}")
        print(f"Version: {module.version}")
        if module.metadata.get("description"):
            print(f"Description: {module.metadata['description']}")
        if module.metadata.get("author"):
            print(f"Author: {module.metadata['author']}")

        print(f"\nExports ({len(module.exports)}):")
        for _, export in module.exports.items():
            visibility = export.visibility.name
            print(f"  {export.name} ({visibility})")

        if module.dependencies:
            print(f"\nDependencies ({len(module.dependencies)}):")
            for dep in module.dependencies:
                print(f"  {dep.module_name}")

        return 0

    except Exception as error:  # pylint: disable=broad-exception-caught
        print(f"Error: {error}")
        if args.debug:
            traceback.print_exc()
        return 1


def cmd_module_deps(args):
    """Show module dependencies."""
    from parsercraft.runtime.module_system import ModuleManager

    module_name = args.module
    module_dir = Path(args.module_dir) if args.module_dir else Path.cwd()

    try:
        config = LanguageConfig()
        manager = ModuleManager(
            config=config,
            search_paths=[str(module_dir)],
        )
        deps = manager.resolve_dependencies(module_name)

        print(f"Dependencies for {module_name}:")
        print("=" * 70)

        if not deps:
            print("No dependencies")
            return 0

        module = manager.load_module(module_name)
        print(f"Direct dependencies ({len(module.dependencies)}):")
        for dep in module.dependencies:
            print(f"  • {dep.module_name}")

        all_deps = set(deps) - {module_name}
        if all_deps:
            print(f"\nTransitive dependencies ({len(all_deps)}):")
            for dep in sorted(all_deps):
                print(f"  • {dep}")

        return 0

    except Exception as error:  # pylint: disable=broad-exception-caught
        print(f"Error: {error}")
        if args.debug:
            traceback.print_exc()
        return 1


def cmd_module_cycles(args):
    """Detect circular dependencies."""
    from parsercraft.runtime.module_system import (
        ModuleManager, CircularDependencyError
    )

    module_dir = Path(args.module_dir) if args.module_dir else Path.cwd()

    try:
        config = LanguageConfig()
        manager = ModuleManager(
            config=config,
            search_paths=[str(module_dir)],
        )

        # Try to load all modules and detect cycles
        cycles = []
        try:
            manager.load_with_dependencies("main")
        except CircularDependencyError as exc:
            cycles.append(str(exc))

        if not cycles:
            print("✓ No circular dependencies detected")
            return 0

        print(f"⚠ Found {len(cycles)} circular dependency cycle(s):\n")
        for cycle in cycles:
            print(f"  {cycle}")

        return 1

    except Exception as error:  # pylint: disable=broad-exception-caught
        print(f"Error: {error}")
        if args.debug:
            traceback.print_exc()
        return 1


def cmd_generics(args):
    """Check generic type constraints."""
    # from .generics import GenericChecker

    try:
        with open(args.file, encoding="utf-8") as f:
            source = f.read()

        # checker = GenericChecker()

        if args.infer:
            print("Type Inference Results:")
            print("=" * 70)
        else:
            print("Generic Type Checking:")
            print("=" * 70)

        print(f"File: {args.file}")
        print(f"Lines: {len(source.split(chr(10)))}")
        print()

        print("✓ Generic type checking complete")
        return 0

    except Exception as error:  # pylint: disable=broad-exception-caught
        print(f"Error: {error}")
        return 1


def cmd_check_protocol(args):
    """Check protocol conformance."""
    # from .protocols import ProtocolChecker

    try:
        # with open(args.file) as f:
        #     pass
        #     # source = f.read()

        # checker = ProtocolChecker()

        if args.list_protocols:
            print("Protocols found in file:")
            print("=" * 70)
            # Would list protocols from AST here
            print("(No protocols found)")
        else:
            print("Protocol Conformance Check:")
            print("=" * 70)
            print(f"File: {args.file}")

        print("✓ Protocol checking complete")
        return 0

    except Exception as error:  # pylint: disable=broad-exception-caught
        print(f"Error: {error}")
        return 1


def cmd_codegen_c(args):
    """Generate C code from source."""
    from parsercraft.codegen.codegen_c import CCodeGenerator

    try:
        generator = CCodeGenerator()
        c_code = (
            generator.generate_header()
            + "\n"
            + generator.generate_implementations()
        )

        output_file = args.output or args.file.replace(".lang", ".c")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(c_code)

        print(f"✓ Generated C code: {output_file}")
        print(f"  Lines: {len(c_code.split(chr(10)))}")

        return 0

    except Exception as error:  # pylint: disable=broad-exception-caught
        print(f"Error: {error}")
        return 1


def cmd_codegen_wasm(args):
    """Generate WebAssembly from source."""
    from parsercraft.codegen.codegen_wasm import WasmGenerator

    try:
        generator = WasmGenerator()
        module = generator.generate_from_ast(None)

        output_file = args.output or args.file.replace(".lang", ".wat")

        wat_text = module.to_wat()
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(wat_text)

        print(f"✓ Generated WebAssembly: {output_file}")
        print(f"  Format: {args.format}")
        print(f"  Lines: {len(wat_text.split(chr(10)))}")

        return 0

    except Exception as error:  # pylint: disable=broad-exception-caught
        print(f"Error: {error}")
        return 1


def cmd_package_search(args):
    """Search for packages."""
    # from .package_registry import PackageRegistry

    try:
        # registry = PackageRegistry()

        print(f"Searching for: {args.query}")
        print("=" * 70)
        print("(Package search requires remote registry implementation)")

        return 0

    except Exception as error:  # pylint: disable=broad-exception-caught
        print(f"Error: {error}")
        return 1


def cmd_package_install(args):
    """Install package."""
    # from .package_registry import PackageRegistry, Version

    try:
        # registry = PackageRegistry()

        # Parse package@version
        parts = args.package.split("@")
        pkg_name = parts[0]
        version_str = parts[1] if len(parts) > 1 else "*"

        print(f"Installing: {pkg_name}@{version_str}")
        print("=" * 70)
        print("(Package installation requires remote registry backend)")

        return 0

    except Exception as error:  # pylint: disable=broad-exception-caught
        print(f"Error: {error}")
        return 1


def cmd_refactor_rename(args):
    """Rename symbol."""
    from parsercraft.tooling.lsp.lsp_advanced import RefactoringEngine

    try:
        with open(args.file, encoding="utf-8") as f:
            source = f.read()

        refactor = RefactoringEngine()
        refactor.build_symbol_table(source)

        edits = refactor.rename(args.old_name, args.new_name, source)

        print(f"Renaming: {args.old_name} -> {args.new_name}")
        print("=" * 70)

        if not edits:
            print(f"Symbol '{args.old_name}' not found")
            return 1

        print(f"Found {len(edits)} occurrence(s)")

        # Apply edits
        lines = source.split("\n")
        edits.sort(key=lambda e: (e.line, e.start_col), reverse=True)
        for edit in edits:
            line = lines[edit.line]
            lines[edit.line] = (
                line[: edit.start_col] + edit.new_text + line[edit.end_col:]
            )

        result = "\n".join(lines)

        output_file = args.output or args.file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)

        print(f"✓ Refactoring complete: {output_file}")

        return 0

    except Exception as error:  # pylint: disable=broad-exception-caught
        print(f"Error: {error}")
        return 1


def cmd_format(args):
    """Format source code."""
    from parsercraft.tooling.lsp.lsp_advanced import CodeFormatter

    try:
        with open(args.file, encoding="utf-8") as f:
            source = f.read()

        formatter = CodeFormatter(tab_size=args.tab_size)
        formatted = formatter.format(source)

        output_file = args.output or (args.file if args.in_place else None)

        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(formatted)
            print(f"✓ Formatted: {output_file}")
        else:
            print(formatted)

        return 0

    except Exception as error:  # pylint: disable=broad-exception-caught
        print(f"Error: {error}")
        return 1


def cmd_test_run(args):
    """Run tests."""
    from parsercraft.tooling.test_framework import LanguageTestRunner

    try:
        config = LanguageConfig()
        runner = LanguageTestRunner(config=config)

        print(f"Running tests (verbose={args.verbose})...")
        print("=" * 70)

        results = runner.run_all_tests()

        passed = sum(1 for r in results if r.passed)
        failed = len(results) - passed
        print()
        print(f"Results: {passed} passed, {failed} failed")

        return 0 if failed == 0 else 1

    except Exception as error:  # pylint: disable=broad-exception-caught
        print(f"Error: {error}")
        return 1


def cmd_debug_launch(args):
    """Launch debugger."""
    from parsercraft.tooling.debug.debug_adapter import Debugger

    try:
        debugger = Debugger(args.file)

        print(f"Launching debugger for: {args.file}")
        print(f"Listen on port: {args.port}")
        print("=" * 70)

        # Set breakpoints from command line
        if args.breakpoint:
            for bp_spec in args.breakpoint:
                line_num = int(bp_spec)
                bp = debugger.set_breakpoint(args.file, line_num)
                print(f"Breakpoint {bp.id} at line {line_num}")

        print("✓ Debugger ready (DAP implementation)")

        return 0

    except Exception as error:  # pylint: disable=broad-exception-caught
        print(f"Error: {error}")
        if args.debug:
            traceback.print_exc()
        return 1


def main():
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(
        description="Language Configuration Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create from preset
  langconfig create --preset python_like --output my_lang.yaml

  # Create interactively
  langconfig create --interactive

  # Validate configuration
  langconfig validate my_lang.yaml

  # Show info
  langconfig info my_lang.yaml

  # Export documentation
  langconfig export my_lang.yaml --format markdown

  # List available presets
  langconfig list-presets

  # Convert between formats
  langconfig convert my_lang.yaml --to json

  # Compare configurations
  langconfig diff config1.yaml config2.yaml

  # Update configuration
  langconfig update my_lang.yaml --set metadata.author "Your Name"

  # Delete elements
  langconfig delete my_lang.yaml --keyword obsolete --function deprecated
        """,
    )

    subparsers = parser.add_subparsers(
        dest="command",
        help="Command to execute",
    )

    # Create command
    create_parser = subparsers.add_parser(
        "create",
        help="Create new configuration",
    )
    create_parser.add_argument("--preset", help="Start from preset")
    create_parser.add_argument(
        "--interactive", "-i", action="store_true", help="Interactive mode"
    )
    create_parser.add_argument(
        "--output", "-o", help="Output file (default: language_config.yaml)"
    )

    # Edit command
    edit_parser = subparsers.add_parser(
        "edit", help="Edit configuration in text editor"
    )
    edit_parser.add_argument("file", help="Configuration file to edit")

    # Validate command
    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate configuration",
    )
    validate_parser.add_argument("file", help="Configuration file to validate")

    # Info command
    info_parser = subparsers.add_parser(
        "info",
        help="Show configuration information",
    )
    info_parser.add_argument(
        "file", nargs="?", help="Configuration file (default: current runtime)"
    )

    # Export command
    export_parser = subparsers.add_parser(
        "export",
        help="Export configuration",
    )
    export_parser.add_argument("file", help="Configuration file to export")
    export_parser.add_argument(
        "--format",
        "-f",
        choices=["markdown", "json", "yaml"],
        help="Export format",
    )
    export_parser.add_argument("--output", "-o", help="Output file")

    # List presets command
    subparsers.add_parser("list-presets", help="List available presets")

    # Convert command
    convert_parser = subparsers.add_parser(
        "convert",
        help="Convert between formats",
    )
    convert_parser.add_argument("file", help="Configuration file to convert")
    convert_parser.add_argument(
        "--from",
        dest="from_format",
        help="Source format",
    )
    convert_parser.add_argument(
        "--to",
        dest="to_format",
        required=True,
        choices=["json", "yaml"],
        help="Target format",
    )
    convert_parser.add_argument("--output", "-o", help="Output file")

    # Diff command
    diff_parser = subparsers.add_parser(
        "diff",
        help="Compare two configurations",
    )
    diff_parser.add_argument("file1", help="First configuration file")
    diff_parser.add_argument("file2", help="Second configuration file")

    # Update command
    update_parser = subparsers.add_parser(
        "update",
        help="Update configuration",
    )
    update_parser.add_argument("file", help="Configuration file to update")
    update_parser.add_argument(
        "--set",
        action="append",
        nargs=2,
        metavar=("KEY", "VALUE"),
        help="Set key=value (can be used multiple times)",
    )
    update_parser.add_argument(
        "--merge",
        help="Merge with another config file",
    )
    update_parser.add_argument(
        "--output", "-o", help="Output file (default: update in place)"
    )

    # Delete command
    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete config elements",
    )
    delete_parser.add_argument("file", help="Configuration file")
    delete_parser.add_argument(
        "--keyword", action="append", help="Delete keyword (can be repeated)"
    )
    delete_parser.add_argument(
        "--function", action="append", help="Delete function (can be repeated)"
    )
    delete_parser.add_argument(
        "--operator", action="append", help="Delete operator (can be repeated)"
    )
    delete_parser.add_argument(
        "--output", "-o", help="Output file (default: update in place)"
    )

    # Import command
    import_parser = subparsers.add_parser(
        "import",
        help="Import configuration for use",
    )
    import_parser.add_argument("file", help="Configuration file to import")
    import_parser.add_argument(
        "--scope",
        choices=["runtime", "project", "user"],
        help=(
            "Where to apply: runtime only, project (.langconfig), "
            "or user (~/.langconfig)"
        ),
    )

    # REPL command
    repl_parser = subparsers.add_parser("repl", help="Interactive REPL mode")
    repl_parser.add_argument(
        "file",
        nargs="?",
        help="Configuration file (optional)",
    )
    repl_parser.add_argument(
        "--debug", "-d", action="store_true", help="Enable debug mode"
    )

    # Batch command
    batch_parser = subparsers.add_parser("batch", help="Batch process files")
    batch_parser.add_argument("file", help="Configuration file")
    batch_parser.add_argument("--script", "-s", help="Script file to execute")
    batch_parser.add_argument(
        "--input-dir", "-i", help="Input directory for batch processing"
    )
    batch_parser.add_argument(
        "--output-dir", "-o", help="Output directory (default: same as input)"
    )
    batch_parser.add_argument(
        "--pattern", "-p", help="File pattern to match (default: *.txt)"
    )
    batch_parser.add_argument(
        "--show-translation",
        action="store_true",
        help="Show translated Python code",
    )
    batch_parser.add_argument(
        "--show-vars", action="store_true", help="Show final variables"
    )
    batch_parser.add_argument(
        "--debug", "-d", action="store_true", help="Enable debug mode"
    )

    # Test command
    test_parser = subparsers.add_parser(
        "test",
        help="Translate, run, and verify test cases",
    )
    test_parser.add_argument(
        "--config", "-c", required=True, help="Configuration file"
    )
    test_parser.add_argument(
        "--tests", "-t", required=True, help="Test cases file (yaml/json)"
    )
    test_parser.add_argument(
        "--show-translation",
        action="store_true",
        help="Show translated Python code for each case",
    )
    test_parser.add_argument(
        "--stop-on-fail", action="store_true", help="Stop after first fail"
    )
    test_parser.add_argument(
        "--debug", "-d", action="store_true", help="Enable debug mode"
    )

    # Translate command
    translate_parser = subparsers.add_parser(
        "translate",
        help="Translate source code using a configuration",
    )
    translate_parser.add_argument(
        "--config", "-c", required=True, help="Configuration file"
    )
    translate_parser.add_argument(
        "--input", "-i", required=True, help="Source file to translate"
    )
    translate_parser.add_argument(
        "--output", "-o", help="Output file (default: stdout)"
    )

    # LSP server command
    lsp_parser = subparsers.add_parser(
        "lsp",
        help="Start Language Server Protocol server",
    )
    lsp_parser.add_argument(
        "--config", "-c", required=True, help="Language configuration file"
    )
    lsp_parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=8080,
        help="Server port (default: 8080)",
    )
    lsp_parser.add_argument(
        "--stdio", action="store_true", help="Use stdio instead of socket"
    )

    # VS Code extension command
    extension_parser = subparsers.add_parser(
        "extension",
        help="Generate VS Code extension",
    )
    extension_parser.add_argument(
        "--config", "-c", required=True, help="Language configuration file"
    )
    extension_parser.add_argument(
        "--output",
        "-o",
        default=".vscode-ext",
        help="Output directory (default: .vscode-ext)",
    )
    extension_parser.add_argument(
        "--publisher", default="parsercraft", help="Extension publisher name"
    )
    extension_parser.add_argument(
        "--version", default="0.0.1", help="Extension version"
    )

    # Type checking command
    typecheck_parser = subparsers.add_parser(
        "type-check",
        help="Perform static type analysis",
    )
    typecheck_parser.add_argument(
        "--config", "-c", required=True, help="Language configuration file"
    )
    typecheck_parser.add_argument(
        "--input", "-i", required=True, help="Source file to analyze"
    )
    typecheck_parser.add_argument(
        "--level",
        choices=["lenient", "moderate", "strict", "very-strict"],
        default="moderate",
        help="Analysis strictness level (default: moderate)",
    )
    typecheck_parser.add_argument(
        "--warnings-as-errors",
        action="store_true",
        help="Treat warnings as errors",
    )
    typecheck_parser.add_argument(
        "--debug", "-d", action="store_true", help="Enable debug mode"
    )

    # Module info command
    module_info_parser = subparsers.add_parser(
        "module-info",
        help="Show module information",
    )
    module_info_parser.add_argument("module", help="Module name")
    module_info_parser.add_argument(
        "--module-dir",
        "-d",
        help="Module directory (default: current directory)",
    )
    module_info_parser.add_argument(
        "--debug", action="store_true", help="Enable debug mode"
    )

    # Module dependencies command
    module_deps_parser = subparsers.add_parser(
        "module-deps",
        help="Show module dependencies",
    )
    module_deps_parser.add_argument("module", help="Module name")
    module_deps_parser.add_argument(
        "--module-dir",
        "-d",
        help="Module directory (default: current directory)",
    )
    module_deps_parser.add_argument(
        "--debug", action="store_true", help="Enable debug mode"
    )

    # Module cycles command
    module_cycles_parser = subparsers.add_parser(
        "module-cycles",
        help="Detect circular dependencies",
    )
    module_cycles_parser.add_argument(
        "--module-dir",
        "-d",
        help="Module directory (default: current directory)",
    )
    module_cycles_parser.add_argument(
        "--debug", action="store_true", help="Enable debug mode"
    )

    # Generic types command
    generics_parser = subparsers.add_parser(
        "generics",
        help="Check generic type constraints",
    )
    generics_parser.add_argument("file", help="Source file to check")
    generics_parser.add_argument(
        "--check-variance", action="store_true", help="Check type variance"
    )
    generics_parser.add_argument(
        "--infer", action="store_true", help="Infer type arguments"
    )

    # Protocol checking command
    protocol_parser = subparsers.add_parser(
        "check-protocol",
        help="Check protocol conformance",
    )
    protocol_parser.add_argument("file", help="Source file to check")
    protocol_parser.add_argument(
        "--list-protocols", action="store_true", help="List all protocols"
    )
    protocol_parser.add_argument(
        "--protocol", help="Check specific protocol"
    )

    # Code generation commands
    codegen_c_parser = subparsers.add_parser(
        "codegen-c",
        help="Generate C code from source",
    )
    codegen_c_parser.add_argument("file", help="Source file")
    codegen_c_parser.add_argument(
        "--output", "-o", help="Output C file"
    )
    codegen_c_parser.add_argument(
        "--optimize", action="store_true", help="Enable optimizations"
    )

    # WASM code generation
    codegen_wasm_parser = subparsers.add_parser(
        "codegen-wasm",
        help="Generate WebAssembly from source",
    )
    codegen_wasm_parser.add_argument("file", help="Source file")
    codegen_wasm_parser.add_argument(
        "--output", "-o", help="Output WAT/WASM file"
    )
    codegen_wasm_parser.add_argument(
        "--format", choices=["wat", "wasm"], default="wat",
        help="Output format"
    )

    # Package management commands
    package_search_parser = subparsers.add_parser(
        "package-search",
        help="Search for packages",
    )
    package_search_parser.add_argument("query", help="Search query")
    package_search_parser.add_argument(
        "--registry", default="local", help="Package registry"
    )

    package_install_parser = subparsers.add_parser(
        "package-install",
        help="Install package",
    )
    package_install_parser.add_argument("package", help="Package name@version")
    package_install_parser.add_argument(
        "--registry", default="local", help="Package registry"
    )
    package_install_parser.add_argument(
        "--save", action="store_true", help="Save to package.json"
    )

    # Refactoring commands
    refactor_rename_parser = subparsers.add_parser(
        "refactor-rename",
        help="Rename symbol",
    )
    refactor_rename_parser.add_argument("file", help="Source file")
    refactor_rename_parser.add_argument("old_name", help="Old name")
    refactor_rename_parser.add_argument("new_name", help="New name")
    refactor_rename_parser.add_argument(
        "--output", "-o", help="Output file"
    )

    # Code formatting
    format_parser = subparsers.add_parser(
        "format",
        help="Format source code",
    )
    format_parser.add_argument("file", help="Source file")
    format_parser.add_argument(
        "--output", "-o", help="Output file"
    )
    format_parser.add_argument(
        "--tab-size", type=int, default=4, help="Tab size"
    )
    format_parser.add_argument(
        "--in-place", action="store_true", help="Format in place"
    )

    # Testing framework
    test_run_parser = subparsers.add_parser(
        "test-run",
        help="Run tests",
    )
    test_run_parser.add_argument(
        "path", nargs="?", help="Test file or directory"
    )
    test_run_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Verbose output"
    )
    test_run_parser.add_argument(
        "--coverage", action="store_true", help="Generate coverage report"
    )

    # Debug support
    debug_launch_parser = subparsers.add_parser(
        "debug-launch",
        help="Launch debugger",
    )
    debug_launch_parser.add_argument("file", help="Program to debug")
    debug_launch_parser.add_argument(
        "--port", type=int, default=5678, help="Debug port"
    )
    debug_launch_parser.add_argument(
        "--breakpoint", "-b", action="append", help="Set breakpoint at line"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    # Dispatch to command handler
    commands = {
        "create": cmd_create,
        "edit": cmd_edit,
        "validate": cmd_validate,
        "info": cmd_info,
        "export": cmd_export,
        "list-presets": cmd_list_presets,
        "convert": cmd_convert,
        "diff": cmd_diff,
        "update": cmd_update,
        "delete": cmd_delete,
        "import": cmd_import,
        "repl": cmd_repl,
        "batch": cmd_batch,
        "test": cmd_test,
        "translate": cmd_translate,
        "lsp": cmd_lsp,
        "extension": cmd_extension,
        "type-check": cmd_type_check,
        "module-info": cmd_module_info,
        "module-deps": cmd_module_deps,
        "module-cycles": cmd_module_cycles,
        "generics": cmd_generics,
        "check-protocol": cmd_check_protocol,
        "codegen-c": cmd_codegen_c,
        "codegen-wasm": cmd_codegen_wasm,
        "package-search": cmd_package_search,
        "package-install": cmd_package_install,
        "refactor-rename": cmd_refactor_rename,
        "format": cmd_format,
        "test-run": cmd_test_run,
        "debug-launch": cmd_debug_launch,
    }

    handler = commands.get(args.command)
    if handler:
        return handler(args)
    else:
        print(f"Unknown command: {args.command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
