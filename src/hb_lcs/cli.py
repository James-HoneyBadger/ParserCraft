#!/usr/bin/env python3
"""
CodeCraft Configuration CLI Tool

Command-line utility for creating, editing, and managing custom programming
language configurations without a GUI.

Usage:
    codecraft create [--preset PRESET] [--output FILE]
    codecraft edit FILE
    codecraft validate FILE
    codecraft info [FILE]
    codecraft export FILE [--format markdown|json|yaml]
    codecraft import FILE [--scope runtime|project|user]
    codecraft list-presets
    codecraft convert FILE --to FORMAT
    codecraft diff FILE1 FILE2
    codecraft update FILE [--set KEY VALUE] [--merge FILE]
    codecraft delete FILE [--keyword KW] [--function FN]
    codecraft repl [FILE] [--debug]
    codecraft batch FILE [--script SCRIPT]

Presets:
    - python_like    : Python-style syntax
    - javascript_like: JavaScript-style syntax
    - lisp_like      : Lisp-style syntax
    - minimal        : Minimal functional language
    - teachscript    : Educational language (TeachScript)

Examples:
    # Create a new Python-like language
    codecraft create --preset python_like --output my_lang.yaml

    # Validate a configuration file
    codecraft validate my_lang.yaml

    # Export to markdown documentation
    codecraft export my_lang.yaml --format markdown

See Also:
    - CodeCraft IDE: Interactive GUI for language design
    - CodeEx IDE: Develop applications in your languages
    - Documentation: docs/guides/CODEX_QUICKSTART.md
"""

import argparse
import json
import os
import re
import subprocess
import sys
import traceback
from pathlib import Path
from typing import Any, Optional, Sequence

try:
    import readline  # type: ignore  # noqa: F401
except ImportError:  # pragma: no cover - platform dependent
    readline = None

from hb_lcs.language_config import (
    LanguageConfig,
    create_custom_config_interactive,
    list_presets,
)
from hb_lcs.language_runtime import LanguageRuntime

try:
    from yaml import YAMLError  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    YAMLError = None  # type: ignore[assignment]

if YAMLError is not None:
    CONFIG_LOAD_ERRORS: tuple[type[Exception], ...] = (
        OSError,
        ValueError,
        json.JSONDecodeError,
        YAMLError,  # type: ignore[arg-type]
    )
else:
    CONFIG_LOAD_ERRORS = (OSError, ValueError, json.JSONDecodeError)


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
    return translated


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
        exec(  # pylint: disable=exec-used
            translated,
            {"__builtins__": __builtins__},
            variables,
        )

        stripped_line = line.strip()
        has_assignment = "=" in line
        starts_with_keyword = stripped_line.startswith(tuple(keyword_prefixes))

        if not has_assignment and not starts_with_keyword:
            try:
                result = eval(  # pylint: disable=eval-used
                    translated,
                    {"__builtins__": __builtins__},
                    variables,
                )
                if result is not None:
                    print(result)
            except (SyntaxError, TypeError, NameError):
                pass
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
            {"__builtins__": __builtins__},
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
    try:
        target_dir.mkdir(exist_ok=True, parents=True)
    except OSError as error:
        print(f"Error creating output directory {target_dir}: {error}")
        return 1

    glob_pattern = pattern or "*.txt"
    files = list(input_dir.glob(glob_pattern))
    if not files:
        print(f"No files found matching pattern: {glob_pattern}")
        return 1

    print(f"Processing {len(files)} file(s)...")
    print("=" * 70)

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
        except ValueError as e:
            print(f"Error: {e}")
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


def cmd_edit(args):
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
        config.save(output_file, format="json")
        print(f"Exported to JSON: {output_file}")

    elif format_type == "yaml":
        output_file = f"{output}.yaml"
        config.save(output_file, format="yaml")
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

    config.save(output, format=to_format)
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


def cmd_update(args):
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
    }

    handler = commands.get(args.command)
    if handler:
        return handler(args)
    else:
        print(f"Unknown command: {args.command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
