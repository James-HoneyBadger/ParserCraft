# ParserCraft

A programming language construction framework. Define grammars, parse source code, and generate executables — all from Python.

## What It Does

ParserCraft takes a PEG grammar definition and produces a working language pipeline:

```
Grammar (PEG)  →  Parser  →  AST  →  Backend (Python / C / WASM / LLVM IR)
```

## Quick Start

```bash
pip install -e .
```

### 1. Define a Grammar

```python
from parsercraft.parser import GrammarBuilder

g = GrammarBuilder()
g.rule("program").set_pattern(GrammarBuilder.plus(GrammarBuilder.ref("statement")))
g.rule("statement").set_pattern(GrammarBuilder.seq(
    GrammarBuilder.ref("IDENT"), GrammarBuilder.lit("="),
    GrammarBuilder.ref("expr"), GrammarBuilder.lit(";")
))
g.rule("expr").set_pattern(GrammarBuilder.seq(
    GrammarBuilder.ref("term"),
    GrammarBuilder.star(GrammarBuilder.seq(
        GrammarBuilder.choice(GrammarBuilder.lit("+"), GrammarBuilder.lit("-")),
        GrammarBuilder.ref("term")
    ))
))
g.rule("term").set_pattern(GrammarBuilder.seq(
    GrammarBuilder.ref("factor"),
    GrammarBuilder.star(GrammarBuilder.seq(
        GrammarBuilder.choice(GrammarBuilder.lit("*"), GrammarBuilder.lit("/")),
        GrammarBuilder.ref("factor")
    ))
))
g.rule("factor").set_pattern(GrammarBuilder.choice(
    GrammarBuilder.ref("NUMBER"), GrammarBuilder.ref("IDENT"),
    GrammarBuilder.seq(GrammarBuilder.lit("("), GrammarBuilder.ref("expr"), GrammarBuilder.lit(")"))
))
grammar = g.build()
```

Or use PEG text notation:

```python
from parsercraft.parser import GrammarParser, PEGInterpreter

parser = GrammarParser()
grammar = parser.parse("""
program    <- statement+
statement  <- IDENT "=" expr ";"
expr       <- term (("+" / "-") term)*
term       <- factor (("*" / "/") factor)*
factor     <- NUMBER / IDENT / "(" expr ")"
""")
```

### 2. Parse Source Code

```python
interp = PEGInterpreter(grammar)
ast = interp.parse('x = 2 + 3 * 4 ; y = ( x - 1 ) * 2 ;')
print(ast)  # SourceAST tree
```

### 3. Generate Output

**Python (transpile & execute):**
```python
from parsercraft.codegen import transpile_and_exec
result = transpile_and_exec(ast)
print(result['x'])  # 14
print(result['y'])  # 26
```

**C:**
```python
from parsercraft.codegen.codegen_c import CCodeGenerator
gen = CCodeGenerator()
print(gen.translate_source_ast(ast))
```

**WebAssembly:**
```python
from parsercraft.codegen.codegen_wasm import WasmGenerator
gen = WasmGenerator()
module = gen.translate_source_ast(ast)
print(module.to_wat())
```

**LLVM IR:**
```python
from parsercraft.codegen import LLVMIRGenerator
gen = LLVMIRGenerator()
print(gen.translate_source_ast(ast))
```

## Components

### Parser Engine (`parsercraft.parser`)

PEG parser with packrat memoization. Built-in token types: `NUMBER`, `IDENT`, `STRING`.

| Class | Purpose |
|-------|---------|
| `GrammarParser` | Parse PEG text notation into Grammar objects |
| `GrammarBuilder` | Fluent API for building grammars programmatically |
| `PEGInterpreter` | Parse source text against a grammar, producing a `SourceAST` |
| `IncrementalParser` | Re-parse only changed regions after edits |

### Code Generation (`parsercraft.codegen`)

| Backend | Output | Status |
|---------|--------|--------|
| `PythonTranspiler` | Python source / direct `exec()` | Full |
| `CCodeGenerator` | C source with `main()` | Full |
| `WasmGenerator` | WebAssembly text format (WAT) | Full |
| `LLVMIRGenerator` | LLVM IR with SSA form | Full |

### Runtime (`parsercraft.runtime`)

| Module | Purpose |
|--------|---------|
| `REPL` | Interactive read-eval-print loop with AST inspection |
| `StdLib` | Built-in modules: io, math, string, collections, system, random |
| `FFIBridge` | Call C libraries (ctypes) and Python functions from custom languages |
| `LanguageRuntime` | Config-driven keyword remapping and execution |
| `ModuleManager` | Multi-file imports with circular dependency detection |

### Tooling (`parsercraft.tooling`)

| Module | Purpose |
|--------|---------|
| `ErrorLocalizer` | Localized error messages with source context display |
| `CLI` | 30+ subcommands for language creation, validation, and execution |
| `LSP Server` | Language Server Protocol for IDE integration |
| `Debug Adapter` | DAP-compatible debugger |

### IDE (`parsercraft.ide`)

Tkinter-based development environment with grammar editor, source editor, and console output.

```bash
parsercraft-ide
```

### Configuration (`parsercraft.config`)

YAML/JSON language definitions with keyword remapping, custom functions, and syntax options.

```python
from parsercraft.config import LanguageConfig
config = LanguageConfig.load("my_language.yaml")
```

## CLI

```bash
parsercraft create          # Interactive language creation
parsercraft validate X.yaml # Validate a language config
parsercraft run program.src # Execute a program
parsercraft lsp --port 8080 # Start LSP server
parsercraft extension       # Generate VS Code extension
parsercraft-repl            # Launch REPL
parsercraft-ide             # Launch IDE
```

## REPL

```bash
parsercraft-repl
```

Special commands: `:help`, `:ast`, `:py`, `:vars`, `:reset`, `:load <file>`, `:grammar`, `:quit`

## Standard Library

Inject built-in functions into your language runtime:

```python
from parsercraft.runtime import StdLib
stdlib = StdLib()
namespace = {}
stdlib.inject(namespace)
# namespace now has: print_val, sqrt, abs, len, concat, ...
```

Six built-in modules: `io`, `math`, `string`, `collections`, `system`, `random`.

## FFI

Call external code from custom languages:

```python
from parsercraft.runtime import FFIBridge
ffi = FFIBridge()

# Python functions
ffi.register_python("my_func", lambda x: x * 2)

# Python modules
ffi.import_python_module("json")

# C libraries
ffi.load_c_library("libm", "/usr/lib/libm.so.6")
ffi.register_c_function("libm", "sqrt", [ctypes.c_double], ctypes.c_double)
```

## Project Structure

```
src/parsercraft/
├── config/         Language configuration (YAML/JSON schemas)
├── parser/         PEG grammar engine, incremental parser
├── codegen/        Python, C, WASM, LLVM IR backends
├── runtime/        REPL, stdlib, FFI, module system
├── tooling/        CLI, error localization, LSP, debug adapter
├── ide/            Tkinter IDE (editor, projects)
├── types/          Type system, generics, protocols
└── packaging/      VS Code extension generation, package registry
```

## Testing

```bash
python -m pytest tests/ -v
```

113 tests covering grammar parsing, transpilation, code generation, REPL, stdlib, FFI, error localization, incremental parsing, and full pipeline integration.

## Requirements

- Python 3.10+
- PyYAML

## License

See [LICENSE](LICENSE).
