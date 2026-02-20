# ParserCraft

> **Build real programming languages in Python — PEG grammars, packrat parsing, four production code-generation backends.**

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-113%20passing-brightgreen.svg)](tests/)
[![Version](https://img.shields.io/badge/version-4.0.0-informational.svg)](pyproject.toml)

ParserCraft is a full-stack programming language construction framework. Define a PEG grammar — either in text notation or via a fluent Python API — and immediately get a working parser, an abstract syntax tree, and code generators targeting Python, C, WebAssembly, and LLVM IR. Add a config-driven REPL, a Language Server Protocol implementation, a DAP debugger, and a Tkinter IDE, and you have everything needed to design, implement, and ship a custom language from a single Python package.

---

## Table of Contents

- [Pipeline Overview](#pipeline-overview)
- [Feature Highlights](#feature-highlights)
- [Quick Start](#quick-start)
- [Language Presets](#language-presets)
- [Code Generation Backends](#code-generation-backends)
- [CLI Reference](#cli-reference)
- [REPL](#repl)
- [Standard Library &amp; FFI](#standard-library--ffi)
- [Architecture](#architecture)
- [Documentation](#documentation)
- [Testing](#testing)
- [Requirements](#requirements)
- [License](#license)

---

## Pipeline Overview

```
PEG Grammar
    │
    ▼
GrammarParser / GrammarBuilder
    │
    ▼  packrat memoization
PEGInterpreter  ──►  SourceAST
    │
    ├──► PythonTranspiler   →  Python source / exec()
    ├──► CCodeGenerator     →  ANSI C with main()
    ├──► WasmGenerator      →  WebAssembly Text (WAT)
    └──► LLVMIRGenerator    →  LLVM IR (SSA form)
```

Start with a grammar. Get a working language. Ship it anywhere.

---

## Feature Highlights

| Category | Capability |
|---|---|
| **Grammar** | PEG with ordered choice, sequences, quantifiers (`*`,`+`,`?`), and predicate operators |
| **Parsing** | Packrat memoization for O(n) guaranteed parse time; built-in `NUMBER`, `IDENT`, `STRING` tokens |
| **Incremental** | `IncrementalParser` re-parses only changed regions — suitable for real-time IDE use |
| **Backends** | Python transpiler, ANSI C (with `main()`), WebAssembly Text (WAT), LLVM IR (SSA) |
| **Config** | YAML/JSON language definitions with keyword remapping, custom functions, syntax toggles |
| **Presets** | 10 built-in language archetypes (Python-like, JS-like, Pascal-like, Lisp-like, and more) |
| **REPL** | Config-driven interactive loop with AST inspection, variable table, and history |
| **StdLib** | Six injectable modules: `io`, `math`, `string`, `collections`, `system`, `random` |
| **FFI** | ctypes C bridge + Python module imports — call native code from custom languages |
| **Modules** | Multi-file imports with circular dependency detection |
| **Types** | Generic type parameters, protocol-based structural typing |
| **LSP** | Language Server Protocol server for IDE syntax highlighting and completion |
| **DAP** | Debug Adapter Protocol for step-through debugging |
| **IDE** | Tkinter IDE with grammar editor, source pane, and console |
| **VS Code** | Generates a publishable VS Code extension for any language config |
| **CLI** | 30+ subcommands covering the full language lifecycle |

---

## Quick Start

### Installation

```bash
git clone https://github.com/James-HoneyBadger/ParserCraft.git
cd ParserCraft
pip install -e .
```

See [docs/INSTALL.md](docs/INSTALL.md) for virtual-environment setup and production install options.

### Step 1 — Define a Grammar

Use PEG text notation (recommended for readability):

```python
from parsercraft.parser import GrammarParser, PEGInterpreter

grammar = GrammarParser().parse("""
    program   <- statement+
    statement <- IDENT "=" expr ";"
    expr      <- term (("+" / "-") term)*
    term      <- factor (("*" / "/") factor)*
    factor    <- NUMBER / IDENT / "(" expr ")"
""")
```

Or build grammars programmatically with `GrammarBuilder`:

```python
from parsercraft.parser import GrammarBuilder

g = GrammarBuilder()
g.rule("program").set_pattern(GrammarBuilder.plus(GrammarBuilder.ref("statement")))
g.rule("statement").set_pattern(GrammarBuilder.seq(
    GrammarBuilder.ref("IDENT"),
    GrammarBuilder.lit("="),
    GrammarBuilder.ref("expr"),
    GrammarBuilder.lit(";"),
))
# ... add expr, term, factor rules ...
grammar = g.build()
```

### Step 2 — Parse Source Code

```python
interp = PEGInterpreter(grammar)
ast = interp.parse("x = 2 + 3 * 4 ; y = ( x - 1 ) * 2 ;")
print(ast)  # SourceAST tree
```

### Step 3 — Generate Output

**Execute as Python:**
```python
from parsercraft.codegen import transpile_and_exec

result = transpile_and_exec(ast)
print(result["x"])  # 14
print(result["y"])  # 26
```

**Emit ANSI C:**
```python
from parsercraft.codegen.codegen_c import CCodeGenerator
print(CCodeGenerator().translate_source_ast(ast))
```

**Emit WebAssembly (WAT):**
```python
from parsercraft.codegen.codegen_wasm import WasmGenerator
module = WasmGenerator().translate_source_ast(ast)
print(module.to_wat())
```

**Emit LLVM IR:**
```python
from parsercraft.codegen import LLVMIRGenerator
print(LLVMIRGenerator().translate_source_ast(ast))
```

---

## Language Presets

Load a ready-made language archetype with a single call:

```python
from parsercraft.config import LanguageConfig

config = LanguageConfig.from_preset("pascal_like")
config.rename_keyword("begin", "inicio")   # localise a keyword
config.save("my_lang.yaml")               # persist
```

| Preset | Style |
|---|---|
| `python_like` | Indentation-sensitive, `def`/`if`/`for` |
| `js_like` | Brace-block, `function`/`let`/`const` |
| `ruby_like` | `do`…`end` blocks, `def`/`while` |
| `golang_like` | Brace-block, short variable declarations |
| `rust_like` | `fn`/`let mut`/`match` |
| `clike` | `int`/`float` declarations, C-style control |
| `functional` | Lambda/`let-in`/`where` functional style |
| `lisp_like` | S-expression syntax |
| `basic_like` | Line-numbered BASIC style |
| `pascal_like` | `:=` assignment, `BEGIN`…`END` blocks |

---

## Code Generation Backends

| Backend | Class | Output |
|---|---|---|
| Python | `PythonTranspiler` | Runnable Python source; `transpile_and_exec()` for immediate execution |
| C | `CCodeGenerator` | ANSI C with `#include` preamble and `main()` |
| WebAssembly | `WasmGenerator` | WAT text format, importable into any WASM runtime |
| LLVM IR | `LLVMIRGenerator` | SSA-form IR compatible with `llc` / `lli` |

All backends share the same `translate_source_ast(ast) -> str` contract. Adding a fifth backend requires only implementing that one method.

---

## CLI Reference

```
parsercraft <command> [options]
```

| Command | Purpose |
|---|---|
| `create` | Interactive language creation wizard |
| `edit <file>` | Open a language config in the visual editor |
| `validate <file>` | Validate a YAML/JSON language config |
| `info <file>` | Display full language config summary |
| `export <file>` | Export config in alternate format (YAML ↔ JSON) |
| `import <file>` | Import and normalise a foreign config |
| `convert <file>` | Convert config format in-place |
| `diff <a> <b>` | Diff two language configs |
| `update <file>` | Apply structured updates to a config |
| `list-presets` | List all built-in language presets |
| `repl [config]` | Launch an interactive REPL |
| `batch <dir>` | Batch-process a directory of source files |
| `test <file>` | Run the built-in test harness |
| `translate <src>` | Translate source between configs |
| `delete <file>` | Remove a language config safely |
| `lsp` | Start the Language Server Protocol server |
| `extension` | Generate a VS Code extension |
| `type-check <src>` | Run the type checker on source |
| `module-info` | Display module dependency information |
| `module-deps` | List all module dependencies |
| `module-cycles` | Detect circular dependencies |
| `codegen-c <src>` | Emit C code from source |
| `codegen-wasm <src>` | Emit WAT from source |
| `codegen-llvm <src>` | Emit LLVM IR from source |
| `refactor-rename` | Rename a symbol across source files |
| `format <src>` | Auto-format a source file |
| `debug-launch` | Launch the DAP debug adapter |
| `test-run` | Execute a language test suite |

```bash
parsercraft-ide    # Open the Tkinter IDE
parsercraft-repl   # Launch the standalone REPL
```

---

## REPL

```bash
parsercraft-repl
# or with a language config
parsercraft repl my_lang.yaml
```

| Command | Effect |
|---|---|
| `:help` | Show all REPL commands |
| `:ast` | Print the AST of the last expression |
| `:py` | Show the generated Python for the last input |
| `:vars` | List all variables in the current namespace |
| `:reset` | Clear the namespace |
| `:load <file>` | Load a source file into the session |
| `:grammar` | Print the current grammar rules |
| `:quit` | Exit the REPL |

---

## Standard Library & FFI

### Standard Library

```python
from parsercraft.runtime import StdLib

stdlib = StdLib()
ns = {}
stdlib.inject(ns)
# ns now contains: print_val, sqrt, abs_val, len_val,
#                  concat, to_upper, to_lower, range_list, ...
```

Six injectable modules: `io`, `math`, `string`, `collections`, `system`, `random`.

### FFI Bridge

```python
import ctypes
from parsercraft.runtime import FFIBridge

ffi = FFIBridge()

# Register a Python callable
ffi.register_python("double_it", lambda x: x * 2)

# Import a full Python module
ffi.import_python_module("json")

# Load and bind a C shared library
ffi.load_c_library("libm", "/usr/lib/libm.so.6")
ffi.register_c_function("libm", "sqrt", [ctypes.c_double], ctypes.c_double)
```

---

## Architecture

```
src/parsercraft/
├── config/       LanguageConfig, LanguageValidator, IdentifierValidator
├── parser/       GrammarParser, GrammarBuilder, PEGInterpreter, IncrementalParser
├── codegen/      PythonTranspiler, CCodeGenerator, WasmGenerator, LLVMIRGenerator
├── runtime/      REPL, StdLib, FFIBridge, LanguageRuntime, ModuleManager
├── tooling/      CLI, ErrorLocalizer, LSP server, DAP debug adapter
├── ide/          ParserCraftIDE, CodeEditor, ProjectManager
├── types/        TypeChecker, generics, protocols
└── packaging/    VS Code extension generator, package registry
```

See [docs/TECHNICAL_REFERENCE.md](docs/TECHNICAL_REFERENCE.md) for the full API reference.

---

## Documentation

| Document | Description |
|---|---|
| [docs/INSTALL.md](docs/INSTALL.md) | Installation, virtual environments, platform notes |
| [docs/USER_GUIDE.md](docs/USER_GUIDE.md) | End-user guide — CLI, REPL, configs, IDE |
| [docs/TECHNICAL_REFERENCE.md](docs/TECHNICAL_REFERENCE.md) | Full API reference for all public classes |
| [docs/TUTORIAL.md](docs/TUTORIAL.md) | Step-by-step: build your first language in 15 minutes |
| [configs/examples/README.md](configs/examples/README.md) | Config file gallery and format reference |

---

## Testing

```bash
python -m pytest tests/ -v
```

113 tests covering grammar parsing, all four code-generation backends, REPL, stdlib, FFI, error localization, incremental parsing, and full end-to-end pipeline integration.

---

## Requirements

- **Python 3.10+**
- **PyYAML 6.0+** (runtime dependency)
- `tkinter` — bundled with most Python distributions (required for the IDE)
- `pytest` — development only

---

## License

MIT — see [LICENSE](LICENSE).
