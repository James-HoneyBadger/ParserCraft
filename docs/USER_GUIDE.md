# ParserCraft — User Guide

> Version 4.0.0

---

## Table of Contents

- [Introduction](#introduction)
- [Core Concepts](#core-concepts)
- [Language Configuration (YAML/JSON)](#language-configuration-yamljson)
  - [Config File Format](#config-file-format)
  - [Keyword Remapping](#keyword-remapping)
  - [Custom Functions](#custom-functions)
  - [Syntax Options](#syntax-options)
  - [Loading and Saving Configs](#loading-and-saving-configs)
- [Language Presets](#language-presets)
- [The CLI](#the-cli)
  - [Language Management Commands](#language-management-commands)
  - [Execution Commands](#execution-commands)
  - [Code Generation Commands](#code-generation-commands)
  - [Module & Type Commands](#module--type-commands)
  - [Tooling Commands](#tooling-commands)
- [The REPL](#the-repl)
  - [Starting the REPL](#starting-the-repl)
  - [REPL Commands](#repl-commands)
  - [Working with the AST](#working-with-the-ast)
  - [Variables and Namespaces](#variables-and-namespaces)
- [The Tkinter IDE](#the-tkinter-ide)
- [Standard Library Injection](#standard-library-injection)
  - [Built-in Modules](#built-in-modules)
- [FFI Bridge](#ffi-bridge)
  - [Calling Python Functions](#calling-python-functions)
  - [Calling C Libraries](#calling-c-libraries)
- [Module System](#module-system)
- [Error Messages and Localization](#error-messages-and-localization)
- [VS Code Extension Generation](#vs-code-extension-generation)
- [Config File Examples Gallery](#config-file-examples-gallery)

---

## Introduction

ParserCraft lets you design, implement, and run your own programming languages from Python. The typical workflow is:

1. **Define** the language — either via a YAML/JSON config or by writing PEG grammar rules directly.
2. **Parse** source programs into an abstract syntax tree (AST).
3. **Execute or compile** the AST to Python, C, WebAssembly, or LLVM IR.

This guide covers the practical day-to-day use of ParserCraft's tools and APIs. For a step-by-step beginner introduction, see [TUTORIAL.md](TUTORIAL.md). For the complete API reference, see [TECHNICAL_REFERENCE.md](TECHNICAL_REFERENCE.md).

---

## Core Concepts

| Term | Meaning |
|---|---|
| **PEG grammar** | Parsing Expression Grammar — a deterministic, unambiguous formalism for describing syntax. |
| **SourceAST** | The tree produced by `PEGInterpreter.parse()`. Each node has a `node_type`, optional `value`, and `children`. |
| **Language config** | A YAML or JSON file describing keywords, functions, syntax options, and other properties of a custom language. |
| **Preset** | A built-in template (e.g. `pascal_like`) used as a starting point. |
| **Backend** | A code generator that translates a `SourceAST` to Python, C, WAT, or LLVM IR. |
| **Transpile** | Translate source-to-source; ParserCraft's Python backend transpiles AST nodes to runnable Python text. |

---

## Language Configuration (YAML/JSON)

Language configs are the primary way non-programmers describe a language without writing grammar rules manually.

### Config File Format

A minimal YAML config:

```yaml
name: MyLang
version: "1.0"
description: A simple expression language

keywords:
  if: if
  else: else
  while: while
  for: for
  function: function
  return: return

functions:
  print: print_val
  sqrt: sqrt_func

syntax:
  statement_separator: ";"
  assignment_operator: "="
  block_begin: "{"
  block_end: "}"
  line_comment: "//"
  string_delimiters: ["\"", "'"]
  case_sensitive: true
```

All keys are optional — missing keys inherit from the `minimal` preset defaults.

### Keyword Remapping

Use keyword remapping to localise a language or change syntax style:

```python
from parsercraft.config import LanguageConfig

config = LanguageConfig.from_preset("python_like")

# Translate Python keywords to Spanish
config.rename_keyword("if", "si")
config.rename_keyword("else", "sino")
config.rename_keyword("while", "mientras")
config.rename_keyword("for", "para")
config.rename_keyword("def", "definir")
config.rename_keyword("return", "retornar")

config.save("espanol.yaml")
```

Or set the full mapping at once:

```python
config.set_keyword_mapping({
    "if": "si",
    "else": "sino",
    "while": "mientras",
})
```

### Custom Functions

Map language function names to Python runtime callables:

```python
config.add_function("escribir", "print")    # escribir(x) → print(x)
config.add_function("raiz", "math.sqrt")    # raiz(x) → sqrt(x)
```

### Syntax Options

Control fundamental syntax properties:

```python
config.set_syntax_option("statement_separator", ";")
config.set_syntax_option("assignment_operator", ":=")   # Pascal style
config.set_syntax_option("block_begin", "BEGIN")
config.set_syntax_option("block_end", "END")
config.set_syntax_option("line_comment", "--")          # SQL/Lua style
config.set_syntax_option("case_sensitive", False)
```

### Loading and Saving Configs

```python
from parsercraft.config import LanguageConfig

# Load from file (YAML or JSON auto-detected)
config = LanguageConfig.load("my_lang.yaml")

# Load from a built-in preset
config = LanguageConfig.from_preset("pascal_like")

# Save as YAML (default)
config.save("output.yaml")

# Save as JSON
config.save("output.json", fmt="json")

# Export keyword mapping as a human-readable table
table = config.export_mapping_table()
print(table)
```

---

## Language Presets

Presets are fully configured starting points. Use `list-presets` to see all available ones:

```bash
parsercraft list-presets
```

| Preset | Assignment | Blocks | Comments | Notable |
|---|---|---|---|---|
| `python_like` | `=` | indentation | `#` | `def`, `class`, `import` |
| `js_like` | `=` | `{}` | `//` | `function`, `let`, `const` |
| `ruby_like` | `=` | `do`…`end` | `#` | `def`, `puts`, method-style |
| `golang_like` | `:=` / `=` | `{}` | `//` | `func`, `var`, `go` |
| `rust_like` | `=` | `{}` | `//` | `fn`, `let mut`, `match` |
| `clike` | `=` | `{}` | `//` | typed declarations |
| `functional` | `=` | `let…in` | `(*…*)` | lambdas, `where`, `match` |
| `lisp_like` | `setq` | `()` S-exps | `;` | `defun`, `lambda`, `cond` |
| `basic_like` | `=` | line numbers | `REM` | `PRINT`, `GOTO`, `INPUT` |
| `pascal_like` | `:=` | `BEGIN`…`END` | `{…}` | `PROCEDURE`, `FUNCTION`, `VAR` |

Load and customise:

```python
config = LanguageConfig.from_preset("ruby_like")
config.rename_keyword("def", "método")
config.rename_keyword("puts", "imprimir")
config.save("ruby_espanol.yaml")
```

---

## The CLI

All CLI commands follow the pattern:

```
parsercraft <command> [options] [arguments]
```

Run `parsercraft --help` for the full command list, or `parsercraft <command> --help` for per-command help.

### Language Management Commands

#### `create`

Interactive wizard for creating a new language config:

```bash
parsercraft create
```

Prompts for language name, base preset, keywords, and syntax options, then saves a YAML file.

#### `edit`

Open a config in the visual editor:

```bash
parsercraft edit my_lang.yaml
```

#### `validate`

Check a config for structural errors:

```bash
parsercraft validate my_lang.yaml
# ✓ my_lang.yaml is valid
```

#### `info`

Display a formatted summary of a config:

```bash
parsercraft info my_lang.yaml
```

Shows keywords, functions, syntax options, and identifier rules.

#### `export` / `import`

Convert between YAML and JSON:

```bash
parsercraft export my_lang.yaml --format json   # → my_lang.json
parsercraft import foreign.json                 # normalise and save as YAML
```

#### `convert`

Convert format in-place:

```bash
parsercraft convert my_lang.yaml   # saves as my_lang.json
```

#### `diff`

Compare two language configs:

```bash
parsercraft diff base.yaml custom.yaml
```

#### `update`

Apply a JSON patch to a config:

```bash
parsercraft update my_lang.yaml '{"keywords": {"if": "cuando"}}'
```

#### `list-presets`

```bash
parsercraft list-presets
```

#### `delete`

Safely remove a config (with confirmation):

```bash
parsercraft delete my_lang.yaml
```

### Execution Commands

#### `repl`

Launch the interactive REPL with a language config:

```bash
parsercraft repl my_lang.yaml
```

#### `batch`

Process a directory of source files:

```bash
parsercraft batch ./programs/ --config my_lang.yaml --output ./out/
```

#### `test`

Run the built-in test harness against a language config:

```bash
parsercraft test my_lang.yaml
```

#### `translate`

Translate a source file using keyword remapping:

```bash
parsercraft translate program.src --from english.yaml --to espanol.yaml
```

### Code Generation Commands

#### `codegen-c`

Generate ANSI C from a source file:

```bash
parsercraft codegen-c program.src --config my_lang.yaml
```

#### `codegen-wasm`

Generate WebAssembly Text Format:

```bash
parsercraft codegen-wasm program.src --config my_lang.yaml
```

#### `codegen-llvm`

Generate LLVM IR:

```bash
parsercraft codegen-llvm program.src --config my_lang.yaml
```

### Module & Type Commands

#### `module-info`

Display module information for a source file:

```bash
parsercraft module-info main.src
```

#### `module-deps`

List all transitive dependencies:

```bash
parsercraft module-deps main.src
```

#### `module-cycles`

Detect circular imports:

```bash
parsercraft module-cycles main.src
```

#### `type-check`

Run the type checker:

```bash
parsercraft type-check program.src --config my_lang.yaml
```

### Tooling Commands

#### `lsp`

Start the Language Server Protocol server:

```bash
parsercraft lsp --port 8080
parsercraft lsp --stdio     # stdin/stdout transport
```

#### `extension`

Generate a VS Code extension package:

```bash
parsercraft extension my_lang.yaml --out ./vscode-my-lang/
```

#### `refactor-rename`

Rename a symbol across source files:

```bash
parsercraft refactor-rename --old "foo" --new "bar" --dir ./src/
```

#### `format`

Format a source file:

```bash
parsercraft format program.src --config my_lang.yaml
```

#### `debug-launch`

Launch the DAP debug adapter:

```bash
parsercraft debug-launch program.src --config my_lang.yaml
```

---

## The REPL

### Starting the REPL

**Standalone** (uses a default minimal grammar):

```bash
parsercraft-repl
```

**With a language config:**

```bash
parsercraft repl my_lang.yaml
```

**With a PEG grammar file:**

```bash
parsercraft repl --grammar my_grammar.peg
```

### REPL Commands

All REPL meta-commands begin with `:`.

| Command | Effect |
|---|---|
| `:help` | Show all available REPL commands |
| `:ast` | Print the AST of the last evaluated expression |
| `:py` | Print the Python source generated from the last input |
| `:vars` | List all variables and their values in the current namespace |
| `:reset` | Clear the namespace and start fresh |
| `:load <file>` | Execute a source file and import its bindings into the session |
| `:grammar` | Print the current grammar rules |
| `:quit` or `:exit` | Exit the REPL |

### Working with the AST

```
> x = 2 + 3 * 4 ;
Result: x = 14

> :ast
program
  statement
    IDENT 'x'
    Operator '='
    expr
      term
        Number '2'
      ...
```

### Variables and Namespaces

```
> a = 10 ;
> b = a * 2 ;
> :vars
  a = 10
  b = 20

> :reset
Namespace cleared.

> :vars
(empty)
```

---

## The Tkinter IDE

Launch the integrated development environment:

```bash
parsercraft-ide
```

The IDE provides:

- **Grammar Editor** — Write or load a PEG grammar; syntax is highlighted.
- **Source Editor** — Write programs in your custom language; errors are underlined.
- **Console Output** — See parse results, generated code, and execution output.
- **Project Manager** — Create, open, and save language projects.

The IDE is self-contained and requires no network access. It uses `tkinter` from the standard library.

---

## Standard Library Injection

The `StdLib` class provides six injectable module namespaces that can be added to any runtime:

```python
from parsercraft.runtime import StdLib

stdlib = StdLib()
namespace = {}
stdlib.inject(namespace)
```

### Built-in Modules

| Module | Injected Names | Purpose |
|---|---|---|
| `io` | `print_val`, `read_line`, `write_file`, `read_file` | Console and file I/O |
| `math` | `sqrt`, `abs_val`, `floor`, `ceil`, `pow_val`, `log`, `sin`, `cos`, `pi`, `e` | Mathematical functions |
| `string` | `concat`, `len_val`, `to_upper`, `to_lower`, `trim`, `split`, `replace`, `starts_with`, `ends_with` | String manipulation |
| `collections` | `make_list`, `append`, `pop`, `len_list`, `make_dict`, `dict_get`, `dict_set` | Data structures |
| `system` | `exit_prog`, `get_env`, `sleep_ms`, `current_time` | System interaction |
| `random` | `rand_int`, `rand_float`, `rand_choice`, `shuffle` | Random number generation |

Inject a single module:

```python
stdlib.inject_module(namespace, "math")
stdlib.inject_module(namespace, "string")
```

---

## FFI Bridge

The `FFIBridge` allows custom languages to call external code at runtime, with no changes to the grammar or transpiler.

### Calling Python Functions

```python
from parsercraft.runtime import FFIBridge

ffi = FFIBridge()

# Register an arbitrary Python callable
ffi.register_python("double", lambda x: x * 2)
ffi.register_python("greet", lambda name: f"Hello, {name}!")

# Import an entire Python module
ffi.import_python_module("json")   # json.dumps, json.loads, etc.
ffi.import_python_module("os.path")
```

### Calling C Libraries

```python
import ctypes

ffi.load_c_library("libm", "/usr/lib/libm.so.6")
ffi.register_c_function(
    "libm", "sqrt",
    argtypes=[ctypes.c_double],
    restype=ctypes.c_double
)

# Now call in source: sqrt(2.0) → 1.4142...
result = ffi.call("sqrt", 2.0)
print(result)  # 1.4142135623730951
```

---

## Module System

The `ModuleManager` handles multi-file languages with `import` / `use` statements.

```python
from parsercraft.runtime.module_system import ModuleManager

manager = ModuleManager()
manager.add_search_path("./lib")

# Load a module by name
module = manager.load_module("utils")

# Check for circular dependencies before loading
manager.check_cycles("main")
```

Circular dependency detection raises `CircularDependencyError` before execution begins.

---

## Error Messages and Localization

ParserCraft produces structured, human-readable error messages with source context:

```
SyntaxError at line 3, column 7: Expected ";" but found "END"

  3 │   x := 42
                ^
```

`ErrorLocalizer` supports multiple locales. To use a non-English locale:

```python
from parsercraft.tooling import ErrorLocalizer

loc = ErrorLocalizer(locale="es")
msg = loc.format_error("unexpected_token", token="END", expected=";")
print(msg)
# Error de sintaxis en línea 3: Se esperaba ";" pero se encontró "END"
```

---

## VS Code Extension Generation

ParserCraft can generate a complete, publishable VS Code extension from any language config:

```bash
parsercraft extension my_lang.yaml --out ./my-lang-extension/
```

The generated extension includes:

- Syntax highlighting grammar (TextMate `.tmLanguage`)
- Language configuration (comment toggling, bracket matching)
- `package.json` with correct activation events
- A README and icon placeholder

Publish with:

```bash
cd my-lang-extension
npm install -g @vscode/vsce
vsce package
vsce publish
```

---

## Config File Examples Gallery

Ready-made configs are in `configs/examples/`:

| File | Language Style |
|---|---|
| `python_like.yaml` | Python-inspired |
| `pascal_like.yaml` | Pascal / Delphi style |
| `basic_like.yaml` | Classic BASIC |
| `functional_ml.yaml` | ML / Haskell functional style |
| `lisp_like.yaml` | Lisp / Scheme s-expressions |
| `ruby_like.yaml` | Ruby method-style |
| `forth_like.yaml` | Forth stack-based |
| `spanish.yaml` | Spanish-keyword Python variant |
| `gw_basic.yaml` | GW-BASIC / QBasic style |
| `minimal.json` | Bare minimum config |
| `demo_config.yaml` | Annotated full-feature example |

See [configs/examples/README.md](../configs/examples/README.md) for descriptions of each.
