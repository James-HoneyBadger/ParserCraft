# ParserCraft AI Coding Agent Instructions

## Project Overview

ParserCraft is a **programming language construction framework**. Users define PEG grammars (programmatically or via text notation), parse source code into ASTs, and generate output in multiple backends (Python, C, WebAssembly, LLVM IR).

**Core Pipeline**: Grammar → PEGInterpreter → SourceAST → Backend (transpile/compile)

**Version**: 4.0.0

## Architecture: Subpackage Structure

```
src/parsercraft/
├── config/       LanguageConfig, LanguageValidator, IdentifierValidator
├── parser/       GrammarParser, GrammarBuilder, PEGInterpreter, IncrementalParser
├── codegen/      PythonTranspiler, CCodeGenerator, WasmGenerator, LLVMIRGenerator
├── runtime/      REPL, StdLib, FFIBridge, LanguageRuntime, ModuleManager
├── tooling/      CLI, ErrorLocalizer, LSP (lsp/), Debug (debug/)
├── ide/          ParserCraftIDE, CodeEditor, ProjectManager
├── types/        TypeChecker, generics, protocols
└── packaging/    VS Code extension gen, package registry
```

### Key Classes & Entry Points

| Class | Module | Purpose |
|-------|--------|---------|
| `GrammarParser` | `parsercraft.parser` | Parse PEG text notation into Grammar |
| `GrammarBuilder` | `parsercraft.parser` | Fluent API for building grammars |
| `PEGInterpreter` | `parsercraft.parser` | Parse source against grammar → SourceAST |
| `IncrementalParser` | `parsercraft.parser` | Re-parse only changed regions |
| `PythonTranspiler` | `parsercraft.codegen` | AST → Python source / exec() |
| `CCodeGenerator` | `parsercraft.codegen.codegen_c` | AST → C source |
| `WasmGenerator` | `parsercraft.codegen.codegen_wasm` | AST → WAT |
| `LLVMIRGenerator` | `parsercraft.codegen` | AST → LLVM IR (SSA) |
| `REPL` | `parsercraft.runtime` | Interactive eval with persistent namespace |
| `StdLib` | `parsercraft.runtime` | Built-in modules (io, math, string, etc.) |
| `FFIBridge` | `parsercraft.runtime` | ctypes C + Python function bindings |
| `ErrorLocalizer` | `parsercraft.tooling` | Localized error messages with context |
| `LanguageConfig` | `parsercraft.config` | YAML/JSON language definitions |
| `LanguageRuntime` | `parsercraft.runtime` | Config-driven keyword remapping |

### GrammarBuilder API

Static methods for building PEG patterns:
- `GrammarBuilder.seq(...)` — sequence
- `GrammarBuilder.choice(...)` — ordered choice
- `GrammarBuilder.star(p)` — zero or more
- `GrammarBuilder.plus(p)` — one or more
- `GrammarBuilder.opt(p)` — optional
- `GrammarBuilder.lit("x")` — string literal
- `GrammarBuilder.ref("rule")` — rule reference

Instance method: `g.rule("name").set_pattern(pattern)`

### AST Node Types

`SourceAST` nodes produced by `PEGInterpreter`:
- Rule nodes: `node_type` = rule name (e.g., "program", "statement", "expr")
- Tokens: `node_type` = "Number", "Identifier", "IDENT", "String"
- Operators: `node_type` = "Operator", `value` = the operator text

### Inline Assignment Pattern

When a grammar defines `statement <- IDENT "=" expr ";"` without a separate `assignment` rule, statement nodes contain `[IDENT, Operator('='), expr, Operator(';')]` directly. All backends detect this pattern and emit assignments correctly.

## CLI Entry Points

| Command | Purpose | Module |
|---------|---------|--------|
| `parsercraft` | CLI with 30+ subcommands | `parsercraft.tooling.cli:main` |
| `parsercraft-ide` | Tkinter IDE | `parsercraft.ide.app:main` |
| `parsercraft-repl` | Interactive REPL | `parsercraft.runtime.repl:main` |

## Testing

```bash
python -m pytest tests/ -v   # 113 tests
```

Test files:
- `test_grammar.py` — PEG parsing, GrammarBuilder, grammar_from_config
- `test_transpiler.py` — Python transpilation, exec, options
- `test_codegen.py` — C, WASM, LLVM IR generation
- `test_repl.py` — REPL eval, commands, config loading
- `test_stdlib_ffi_errors.py` — StdLib inject, FFI bindings, ErrorLocalizer
- `test_incremental.py` — Incremental parsing, edits
- `test_integration.py` — Full pipeline, multi-backend

## Developer Workflows

### Typical Pipeline Usage

```python
from parsercraft.parser import GrammarParser, PEGInterpreter
from parsercraft.codegen import transpile_and_exec

parser = GrammarParser()
grammar = parser.parse('program <- statement+\nstatement <- IDENT "=" expr ";"\nexpr <- NUMBER')
interp = PEGInterpreter(grammar)
ast = interp.parse('x = 42 ;')
result = transpile_and_exec(ast)  # {'x': 42}
```

### Config-Driven Language (Legacy/Alternative)

```python
from parsercraft.config import LanguageConfig
from parsercraft.runtime.language_runtime import LanguageRuntime

config = LanguageConfig.load("my_lang.yaml")
LanguageRuntime.load_config(config)
runtime = LanguageRuntime.get_instance()
```

### Adding a New Backend

1. Create class in `src/parsercraft/codegen/`
2. Implement `translate_source_ast(ast) -> str` method
3. Handle node types: program, statement (with inline assignment detection), expr, term, factor, Number, Identifier, Operator
4. Export from `codegen/__init__.py`
5. Add tests in `tests/`

### Modifying Grammar Engine

- Core parser: `parser/grammar.py` (~955 lines)
- `GrammarParser._parse_*` methods handle PEG syntax
- `PEGInterpreter._match_rule()` does packrat-memoized parsing
- Built-in tokens (NUMBER, IDENT, STRING) are handled in `_match_builtin_token()`

## External Dependencies

- **PyYAML**: Config parsing (required)
- **pytest**: Testing (dev)
- **tkinter**: IDE GUI (bundled with Python)

## Quick Reference

| Task | Look Here |
|------|-----------|
| Define a grammar | `parser/grammar.py` → `GrammarParser` or `GrammarBuilder` |
| Parse source code | `parser/grammar.py` → `PEGInterpreter.parse()` |
| Transpile to Python | `codegen/python_transpiler.py` → `PythonTranspiler` |
| Generate C code | `codegen/codegen_c.py` → `CCodeGenerator.translate_source_ast()` |
| Generate WASM | `codegen/codegen_wasm.py` → `WasmGenerator.translate_source_ast()` |
| Generate LLVM IR | `codegen/llvm_ir.py` → `LLVMIRGenerator.translate_source_ast()` |
| REPL | `runtime/repl.py` → `REPL` class |
| StdLib | `runtime/stdlib.py` → `StdLib` class |
| FFI | `runtime/ffi.py` → `FFIBridge` class |
| Error messages | `tooling/error_localization.py` → `ErrorLocalizer` |
| CLI | `tooling/cli.py` → `main()` |
| IDE | `ide/app.py` → `ParserCraftIDE` |
| Language config | `config/language_config.py` → `LanguageConfig` |
| Module system | `runtime/module_system.py` → `ModuleManager` |
| Incremental parse | `parser/incremental.py` → `IncrementalParser` |

## Documentation Files

User-facing documentation is in `docs/`:

| File | Purpose |
|------|---------|
| `docs/INSTALL.md` | Installation, virtual environments, platform notes |
| `docs/USER_GUIDE.md` | End-user guide (CLI, REPL, configs, IDE, stdlib, FFI) |
| `docs/TECHNICAL_REFERENCE.md` | Full public API reference |
| `docs/TUTORIAL.md` | Step-by-step tutorials (5 progressive examples) |

## Key Behavioural Notes

- `:=` is a valid assignment operator (Pascal-style). `PythonTranspiler._emit_transparent` detects both `=` and `:=` as assignment operators. `_emit_assignment` filters both from the meaningful-children list.
- `transpile_and_exec(ast)` runs `exec(py_code, namespace)`. The returned dict contains user-defined variables; filter `__builtins__` with `{k: v for k, v in ns.items() if not k.startswith("__")}`.
- All backend classes implement `translate_source_ast(ast: SourceAST) -> str`.
- The test suite must stay at 113 passing: `python -m pytest tests/ -q`.
