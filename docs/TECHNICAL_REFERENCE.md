# ParserCraft — Technical Reference

> Version 4.0.0

This document is the authoritative API reference for all public classes and functions in ParserCraft. It covers the parser engine, code-generation backends, runtime, configuration, tooling, type system, and packaging modules.

---

## Table of Contents

- [Module Map](#module-map)
- [parsercraft.parser](#parsercraftparser)
  - [GrammarParser](#grammarparser)
  - [GrammarBuilder](#grammarbuilder)
  - [Grammar](#grammar)
  - [GrammarRule](#grammarrule)
  - [PEGInterpreter](#peginterpreter)
  - [SourceAST](#sourceast)
  - [IncrementalParser](#incrementalparser)
  - [PEG Grammar Text Notation](#peg-grammar-text-notation)
  - [Built-in Token Types](#built-in-token-types)
- [parsercraft.codegen](#parsercraftcodegen)
  - [transpile\_and\_exec](#transpile_and_exec)
  - [transpile\_to\_python](#transpile_to_python)
  - [PythonTranspiler](#pythontranspiler)
  - [TranspileOptions](#transpileoptions)
  - [CCodeGenerator](#ccodegenerator)
  - [WasmGenerator](#wasmgenerator)
  - [LLVMIRGenerator](#llvmirgenerator)
  - [Backend Contract](#backend-contract)
- [parsercraft.config](#parsercraftconfig)
  - [LanguageConfig](#languageconfig)
  - [LanguageValidator](#languagevalidator)
  - [IdentifierValidator](#identifiervalidator)
- [parsercraft.runtime](#parsercraftruntime)
  - [REPL](#repl)
  - [StdLib](#stdlib)
  - [FFIBridge](#ffibridge)
  - [LanguageRuntime](#languageruntime)
  - [ModuleManager](#modulemanager)
- [parsercraft.tooling](#parsercrafttooling)
  - [ErrorLocalizer](#errorlocalizer)
  - [CLI Entry Point](#cli-entry-point)
- [parsercraft.types](#parsercrafttypes)
- [parsercraft.packaging](#parsercraftpackaging)
- [SourceAST Node Types Reference](#sourceast-node-types-reference)
- [PEG Notation Quick Reference](#peg-notation-quick-reference)

---

## Module Map

```
parsercraft
├── parser          Grammar definition & parsing engine
│   ├── grammar.py          GrammarParser, GrammarBuilder, PEGInterpreter, SourceAST
│   └── incremental.py      IncrementalParser
├── codegen         Code generation backends
│   ├── python_transpiler.py  PythonTranspiler, TranspileOptions
│   ├── codegen_c.py         CCodeGenerator
│   ├── codegen_wasm.py      WasmGenerator
│   └── llvm_ir.py           LLVMIRGenerator
├── config          Language configuration
│   ├── language_config.py   LanguageConfig
│   ├── language_validator.py LanguageValidator
│   └── identifier_validator.py IdentifierValidator
├── runtime         Execution environment
│   ├── repl.py              REPL
│   ├── stdlib.py            StdLib
│   ├── ffi.py               FFIBridge
│   ├── language_runtime.py  LanguageRuntime
│   └── module_system.py     ModuleManager
├── tooling         Developer tools
│   ├── cli.py               main() entry point
│   ├── error_localization.py ErrorLocalizer
│   ├── lsp/                 Language Server Protocol
│   └── debug/               Debug Adapter Protocol
├── types           Type system
│   ├── generics.py          Generic type parameters
│   └── protocol_type_integration.py Protocols
└── packaging       Distribution tools
    ├── vscode_integration.py VS Code extension generator
    └── package_registry.py   Package registry
```

---

## parsercraft.parser

Import path: `from parsercraft.parser import ...`

---

### GrammarParser

Parse PEG text notation into a `Grammar` object.

```python
class GrammarParser:
    def parse(self, grammar_text: str, grammar_name: str = "custom") -> Grammar
```

#### `parse(grammar_text, grammar_name="custom") -> Grammar`

Parse a multi-line PEG grammar string. Rules are separated by newlines. The first rule defined becomes the start rule.

**Parameters:**
- `grammar_text` — PEG grammar string (see [PEG Notation](#peg-notation-quick-reference))
- `grammar_name` — Optional human-readable name for the grammar

**Returns:** A `Grammar` object ready for use with `PEGInterpreter`.

**Raises:** `SyntaxError` if the grammar text is malformed.

**Example:**

```python
from parsercraft.parser import GrammarParser

grammar = GrammarParser().parse("""
    program   <- statement+
    statement <- IDENT "=" expr ";"
    expr      <- term (("+" / "-") term)*
    term      <- factor (("*" / "/") factor)*
    factor    <- NUMBER / IDENT / "(" expr ")"
""")
```

---

### GrammarBuilder

Fluent API for constructing `Grammar` objects programmatically, without text notation.

```python
class GrammarBuilder:
    # Instance methods
    def rule(self, name: str, description: str = "") -> GrammarBuilder
    def set_pattern(self, pattern: PEGNode) -> GrammarBuilder
    def start(self, rule_name: str) -> GrammarBuilder
    def build(self) -> Grammar

    # Static factory methods
    @staticmethod def seq(*items: PEGNode) -> PEGNode
    @staticmethod def choice(*items: PEGNode) -> PEGNode
    @staticmethod def star(item: PEGNode) -> PEGNode
    @staticmethod def plus(item: PEGNode) -> PEGNode
    @staticmethod def opt(item: PEGNode) -> PEGNode
    @staticmethod def lit(text: str) -> PEGNode
    @staticmethod def ref(rule_name: str) -> PEGNode
```

#### Instance Methods

| Method | Description |
|---|---|
| `rule(name)` | Begin defining a rule with the given name |
| `set_pattern(pattern)` | Set the PEG pattern for the current rule |
| `start(rule_name)` | Set a specific rule as the start rule (default: first defined) |
| `build()` | Finalise and return the `Grammar` object |

#### Static Factory Methods

| Method | PEG Equivalent | Description |
|---|---|---|
| `seq(a, b, ...)` | `a b ...` | Match items in sequence |
| `choice(a, b, ...)` | `a / b / ...` | Ordered choice — try `a` first, then `b` |
| `star(p)` | `p*` | Zero or more repetitions |
| `plus(p)` | `p+` | One or more repetitions |
| `opt(p)` | `p?` | Optional (zero or one) |
| `lit("x")` | `"x"` | Match exact literal string |
| `ref("rule")` | `rule` | Reference another rule by name |

**Example:**

```python
from parsercraft.parser import GrammarBuilder

g = GrammarBuilder()
g.rule("program").set_pattern(GrammarBuilder.plus(GrammarBuilder.ref("stmt")))
g.rule("stmt").set_pattern(GrammarBuilder.seq(
    GrammarBuilder.ref("IDENT"),
    GrammarBuilder.lit("="),
    GrammarBuilder.ref("NUMBER"),
    GrammarBuilder.lit(";"),
))
grammar = g.build()
```

---

### Grammar

A compiled grammar, ready for use with `PEGInterpreter`. Not constructed directly — use `GrammarParser` or `GrammarBuilder`.

```python
@dataclass
class Grammar:
    name: str
    rules: Dict[str, GrammarRule]
    start_rule: str
```

---

### GrammarRule

A single named rule in a grammar.

```python
@dataclass
class GrammarRule:
    name: str
    pattern: PEGNode
    description: str = ""
```

---

### PEGInterpreter

Parse source text against a grammar, returning a `SourceAST`.

```python
class PEGInterpreter:
    def __init__(self, grammar: Grammar)
    def parse(self, source: str) -> SourceAST
```

#### `__init__(grammar)`

**Parameters:**
- `grammar` — A `Grammar` object from `GrammarParser` or `GrammarBuilder`

#### `parse(source) -> SourceAST`

Parse `source` against the grammar using memoised PEG matching.

**Parameters:**
- `source` — The source text to parse

**Returns:** A `SourceAST` node tree rooted at the start rule.

**Raises:** `SyntaxError` with line/column information on parse failure.

**Implementation notes:**
- Uses packat memoization — O(n) guaranteed worst-case parse.
- Skips whitespace between tokens automatically.
- Furthest-position error reporting: errors identify the deepest point reached.

---

### SourceAST

The abstract syntax tree node produced by `PEGInterpreter.parse()`.

```python
@dataclass
class SourceAST:
    node_type: str         # Rule name or token type
    value: Any = None      # Literal value for leaf nodes (str for tokens)
    children: List[SourceAST] = field(default_factory=list)
    line: int = 0          # Source line number (1-based)
    column: int = 0        # Source column number (1-based)
    source_text: str = ""  # Original source text span

    def to_dict(self) -> Dict[str, Any]
    def pretty(self, indent: int = 0) -> str
```

#### Node Types

| `node_type` | `value` | `children` | Produced by |
|---|---|---|---|
| `"program"` | `None` | statement nodes | Start rule |
| `"statement"` | `None` | rule sub-nodes | `statement` rule |
| `"expr"` | `None` | term / operator nodes | `expr` rule |
| `"term"` | `None` | factor / operator nodes | `term` rule |
| `"factor"` | `None` | child node(s) | `factor` rule |
| `"Number"` | `"42"` (str) | `[]` | `NUMBER` token |
| `"Identifier"` / `"IDENT"` | `"x"` (str) | `[]` | `IDENT` token |
| `"String"` | `"hello"` | `[]` | `STRING` token |
| `"Operator"` | `"="` / `"+"` etc. | `[]` | Matched literal |

> **Inline Assignment Pattern**: When a grammar defines `statement <- IDENT "=" expr ";"` but has no separate `assignment` rule, the statement node's children are `[IDENT, Operator("="), expr, Operator(";")]`. All backends detect this automatically.

---

### IncrementalParser

Re-parse only the changed region of source text. Suitable for real-time use in editors.

```python
class IncrementalParser:
    def __init__(self, grammar: Grammar)
    def parse(self, source: str) -> SourceAST
    def apply_edit(self, start: int, end: int, new_text: str) -> SourceAST
```

#### `apply_edit(start, end, new_text) -> SourceAST`

Apply a text edit and return an updated `SourceAST`. Only invalidates memo entries that overlap `[start, end]`, then re-parses the affected region.

**Parameters:**
- `start` — Byte offset of the edit start (inclusive)
- `end` — Byte offset of the edit end (exclusive)
- `new_text` — Replacement text

---

### PEG Grammar Text Notation

```
rule_name <- pattern

Sequences:       a b c           (all must match in order)
Ordered choice:  a / b / c       (try a; if fails, try b; etc.)
Repetition:      p*              (zero or more)
                 p+              (one or more)
                 p?              (zero or one)
Grouping:        (a b / c)
Literal:         "text"
Rule reference:  rule_name
Built-in token:  NUMBER IDENT STRING
```

**Example grammar for a simple assignment language:**

```
program   <- statement+
statement <- IDENT "=" expr ";"
expr      <- term (("+" / "-") term)*
term      <- factor (("*" / "/") factor)*
factor    <- NUMBER / IDENT / "(" expr ")"
```

---

### Built-in Token Types

| Token | Matches | `value` |
|---|---|---|
| `NUMBER` | Integer or float literal (e.g. `42`, `3.14`) | The matched string |
| `IDENT` | Identifier (letters, digits, `_`; cannot start with digit) | The identifier string |
| `STRING` | Double- or single-quoted string literal | Content without quotes |

All token matching automatically skips leading whitespace.

---

## parsercraft.codegen

Import path: `from parsercraft.codegen import ...`

---

### transpile\_and\_exec

```python
def transpile_and_exec(
    ast: SourceAST,
    options: Optional[TranspileOptions] = None,
    namespace: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

Convenience function: transpile a `SourceAST` to Python and immediately `exec()` it.

**Returns:** The execution namespace `dict` with all defined variables (dunder keys excluded).

**Example:**

```python
from parsercraft.codegen import transpile_and_exec

result = transpile_and_exec(ast)
print(result["x"])  # 14
```

---

### transpile\_to\_python

```python
def transpile_to_python(
    ast: SourceAST,
    indent: str = "    ",
    keyword_map: Optional[Dict[str, str]] = None,
    function_map: Optional[Dict[str, str]] = None,
) -> str
```

Transpile a `SourceAST` to a Python source string without executing it.

---

### PythonTranspiler

Full-featured Python transpiler with config-driven keyword and function remapping.

```python
class PythonTranspiler:
    def __init__(self, options: Optional[TranspileOptions] = None)
    def translate(self, ast: SourceAST) -> str
    def translate_source_ast(self, ast: SourceAST) -> str   # alias
```

#### `translate(ast) -> str`

Translate a `SourceAST` node tree to Python source code string.

**Example:**

```python
from parsercraft.codegen import PythonTranspiler, TranspileOptions

opts = TranspileOptions(
    keyword_map={"si": "if", "sino": "else"},
    function_map={"imprimir": "print"},
    wrap_in_main=True,
)
transpiler = PythonTranspiler(opts)
py_source = transpiler.translate(ast)
```

---

### TranspileOptions

```python
@dataclass
class TranspileOptions:
    indent_str: str = "    "
    keyword_map: Dict[str, str] = field(default_factory=dict)
    function_map: Dict[str, str] = field(default_factory=dict)
    operator_map: Dict[str, str] = field(default_factory=dict)
    inject_runtime: bool = False
    source_maps: bool = False
    wrap_in_main: bool = False
```

| Field | Default | Description |
|---|---|---|
| `indent_str` | `"    "` (4 spaces) | Indentation unit |
| `keyword_map` | `{}` | Map custom keywords to Python keywords (`{"si": "if"}`) |
| `function_map` | `{}` | Map custom function names to Python builtins |
| `operator_map` | `{}` | Map custom operators to Python operators |
| `inject_runtime` | `False` | Inject stdlib helpers at top of output |
| `source_maps` | `False` | Add `# line N` source-map comments |
| `wrap_in_main` | `False` | Wrap code in `if __name__ == "__main__":` guard |

---

### CCodeGenerator

Generate ANSI C source from a `SourceAST`.

```python
class CCodeGenerator:
    def __init__(self)
    def translate_source_ast(self, ast: SourceAST) -> str
```

Output includes:
- `#include <stdio.h>`, `<stdlib.h>`, `<string.h>` preamble
- A `main()` function containing the translated statements
- `printf` calls for any `print` / output nodes

---

### WasmGenerator

Generate WebAssembly Text Format (WAT) from a `SourceAST`.

```python
class WasmGenerator:
    def __init__(self) -> None
    def translate_source_ast(self, ast: SourceAST) -> WasmModule
```

**Returns:** A `WasmModule` object.

```python
class WasmModule:
    def to_wat(self) -> str        # Emit WAT text
    def to_bytes(self) -> bytes    # Emit binary WebAssembly (stub)
```

The WAT output is compatible with any standard WebAssembly runtime (Wasmtime, Node.js WASM API, browser `WebAssembly.compile`).

---

### LLVMIRGenerator

Generate LLVM IR in SSA form from a `SourceAST`.

```python
class LLVMIRGenerator:
    def __init__(self)
    def translate_source_ast(self, ast: SourceAST) -> str
```

Output is compatible with `llc` (compilation to native code) and `lli` (LLVM JIT interpreter).

---

### Backend Contract

All backends implement the same interface. To add a custom backend:

```python
class MyBackend:
    def translate_source_ast(self, ast: SourceAST) -> str:
        """Translate a SourceAST to target language source."""
        ...
```

Handle the following `node_type` values at minimum:
- `"program"` / `"Program"` — root; iterate `node.children`
- `"statement"` — detect inline-assignment via `Operator(value="=")` child
- `"expr"`, `"term"`, `"factor"` — recursive expression nodes
- `"Number"` — numeric literal (`node.value`)
- `"Identifier"` / `"IDENT"` — variable name (`node.value`)
- `"Operator"` — operator text (`node.value`)

---

## parsercraft.config

Import path: `from parsercraft.config import LanguageConfig`

---

### LanguageConfig

The central class for defining and manipulating language configurations.

```python
class LanguageConfig:
    name: str
    version: str
    description: str
    keywords: Dict[str, str]
    functions: Dict[str, str]
    syntax: Dict[str, Any]
    features: Dict[str, bool]
```

#### Class Methods

| Method | Description |
|---|---|
| `LanguageConfig.from_preset(name)` | Load a built-in preset |
| `LanguageConfig.load(filepath)` | Load YAML or JSON from file |
| `LanguageConfig.from_dict(data)` | Construct from a plain dict |
| `LanguageConfig.from_json(json_str)` | Construct from a JSON string |
| `LanguageConfig.load_preset(name)` | Alias for `from_preset` |

#### Instance Methods — Keywords

| Method | Description |
|---|---|
| `rename_keyword(original, new_name)` | Rename an existing keyword |
| `add_keyword(name, python_equivalent, ...)` | Add a new keyword |
| `remove_keyword(name)` | Remove a keyword |
| `set_keyword_mapping(mapping: dict)` | Replace the full keyword map |

#### Instance Methods — Functions

| Method | Description |
|---|---|
| `add_function(name, python_func, ...)` | Map a function name to a Python callable |
| `rename_function(original, new_name)` | Rename a function |
| `remove_function(name)` | Remove a function mapping |

#### Instance Methods — Syntax

| Method | Description |
|---|---|
| `set_syntax_option(key, value)` | Set a single syntax option |
| `set_array_indexing(style)` | Set array indexing style (`"0"`, `"1"`) |
| `set_comment_style(line, block_open, block_close)` | Set comment delimiters |
| `enable_feature(feature, enabled=True)` | Toggle a language feature flag |

#### Instance Methods — Serialisation

| Method | Description |
|---|---|
| `save(filepath, fmt="auto")` | Save to file (YAML or JSON auto/forced) |
| `to_dict()` | Serialise to a plain dict |
| `to_json()` | Serialise to a JSON string |
| `to_yaml()` | Serialise to a YAML string |
| `validate()` | Return list of validation error strings (empty = valid) |
| `update(updates, merge=True)` | Apply a dict of partial updates |
| `export_mapping_table()` | Return a formatted keyword/function mapping string |

---

### LanguageValidator

Validate a `LanguageConfig` object against the schema.

```python
from parsercraft.config.language_validator import LanguageValidator

errors = LanguageValidator.validate(config)   # returns List[str]
```

---

### IdentifierValidator

Validate that identifier names meet the configured rules.

```python
from parsercraft.config.identifier_validator import IdentifierValidator

validator = IdentifierValidator(config)
validator.is_valid("my_var")   # True / False
```

---

## parsercraft.runtime

Import path: `from parsercraft.runtime import ...`

---

### REPL

Interactive read-eval-print loop.

```python
class REPL:
    def __init__(self, config: Optional[LanguageConfig] = None,
                 grammar: Optional[Grammar] = None)
    def run(self) -> None
    def eval_line(self, line: str) -> Optional[str]
```

#### `run()`

Start the REPL interactive loop. Blocks until `:quit` is entered.

#### `eval_line(line) -> Optional[str]`

Evaluate a single line and return the output string (or `None` for REPL commands).

---

### StdLib

Provides six injectable standard library namespaces.

```python
class StdLib:
    def inject(self, namespace: Dict[str, Any]) -> None
    def inject_module(self, namespace: Dict[str, Any], module: str) -> None
    def list_modules(self) -> List[str]
    def list_functions(self, module: Optional[str] = None) -> List[str]
```

Available modules: `"io"`, `"math"`, `"string"`, `"collections"`, `"system"`, `"random"`.

---

### FFIBridge

Foreign function interface for calling C and Python code.

```python
class FFIBridge:
    def register_python(self, name: str, func: Callable) -> None
    def import_python_module(self, module_name: str) -> None
    def load_c_library(self, alias: str, path: str) -> None
    def register_c_function(self, lib_alias: str, func_name: str,
                            argtypes: List[Any], restype: Any) -> None
    def call(self, name: str, *args: Any) -> Any
    def list_registered(self) -> List[str]
```

---

### LanguageRuntime

Config-driven execution environment. Maps custom keywords to Python semantics at runtime.

```python
class LanguageRuntime:
    @classmethod
    def load_config(cls, config: LanguageConfig) -> None
    @classmethod
    def get_instance(cls) -> LanguageRuntime
    def execute(self, source: str) -> Dict[str, Any]
```

---

### ModuleManager

Multi-file module system with dependency tracking.

```python
class ModuleManager:
    def __init__(self)
    def add_search_path(self, path: str) -> None
    def load_module(self, name: str) -> ModuleAST
    def check_cycles(self, entry_point: str) -> None
    def get_dependency_graph(self) -> Dict[str, List[str]]
```

#### `check_cycles(entry_point)`

**Raises:** `CircularDependencyError` if any cycle is detected.

---

## parsercraft.tooling

---

### ErrorLocalizer

Produce human-readable, optionally localised error messages.

```python
class ErrorLocalizer:
    def __init__(self, locale: str = "en")
    def format_error(self, error_type: str, **context) -> str
    def format_parse_error(self, error: SyntaxError, source: str) -> str
```

Supported locales: `"en"` (English), `"es"` (Spanish), `"fr"` (French; partial). Custom locales can be registered by adding entries to the locale table.

---

### CLI Entry Point

```python
# parsercraft.tooling.cli
def main() -> None
```

Called by the `parsercraft` console script. Parses `sys.argv` and dispatches to the appropriate `cmd_*` handler.

All `cmd_*` functions follow the signature:

```python
def cmd_validate(args: argparse.Namespace) -> int:
    ...
    return 0  # exit code
```

---

## parsercraft.types

```python
from parsercraft.types import TypeChecker
from parsercraft.types.generics import GenericType, TypeVar
from parsercraft.types.protocol_type_integration import ProtocolType
```

| Class | Purpose |
|---|---|
| `TypeChecker` | Infer and check types for `SourceAST` nodes |
| `GenericType` | Parameterised type (e.g. `List[T]`) |
| `TypeVar` | Type variable for generic definitions |
| `ProtocolType` | Structural type matching (duck-typing protocol) |

---

## parsercraft.packaging

```python
from parsercraft.packaging.vscode_integration import VSCodeExtensionGenerator
from parsercraft.packaging.package_registry import PackageRegistry
```

### VSCodeExtensionGenerator

```python
class VSCodeExtensionGenerator:
    def __init__(self, config: LanguageConfig)
    def generate(self, output_dir: str) -> None
```

Generates a complete, publish-ready VS Code extension directory from a `LanguageConfig`.

Output contains:
- `package.json`
- `syntaxes/<lang>.tmLanguage.json`
- `language-configuration.json`
- `README.md`

---

## SourceAST Node Types Reference

| `node_type` | Value | Children | Notes |
|---|---|---|---|
| `program` / `Program` | — | statement list | Root node |
| `statement` | — | depends on grammar | May contain inline assignment |
| `assignment` / `Assignment` | — | `[IDENT, value_expr]` | Explicit assignment rule |
| `expr` | — | `[term, (op, term)*]` | Expression node |
| `term` | — | `[factor, (op, factor)*]` | Term node |
| `factor` | — | Varies | Parenthesised or leaf |
| `Number` | `"42"` | `[]` | Numeric literal |
| `Identifier` / `IDENT` | `"x"` | `[]` | Variable name |
| `String` / `STRING` | `"hello"` | `[]` | String literal |
| `Operator` | `"+"`, `"="`, etc. | `[]` | Structural operator |
| `if_stmt` | — | `[cond, then, (else_)?]` | Conditional |
| `while_stmt` | — | `[cond, body]` | While loop |
| `for_stmt` | — | `[var, iter, body]` | For loop |
| `function_def` | — | `[name, params, body]` | Function definition |
| `return_stmt` | — | `[expr]` | Return statement |

---

## PEG Notation Quick Reference

| Notation | Meaning |
|---|---|
| `a b` | Sequence: match `a` then `b` |
| `a / b` | Ordered choice: try `a`; if fail, try `b` |
| `p*` | Zero or more `p` |
| `p+` | One or more `p` |
| `p?` | Zero or one `p` (optional) |
| `(p)` | Grouping |
| `"text"` | Literal string match |
| `NAME` | Reference to rule `NAME` |
| `NUMBER` | Built-in integer/float token |
| `IDENT` | Built-in identifier token |
| `STRING` | Built-in string literal token |

> PEG grammars are always deterministic and unambiguous due to ordered choice. Unlike CFGs, there is no ambiguity or shift-reduce conflict.
