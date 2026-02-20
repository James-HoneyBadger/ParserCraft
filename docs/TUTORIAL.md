# ParserCraft — Tutorials

> Version 4.0.0

---

## Contents

- [Tutorial 1: Your First Language in 15 Minutes](#tutorial-1-your-first-language-in-15-minutes)
- [Tutorial 2: Config-Driven Language Design](#tutorial-2-config-driven-language-design)
- [Tutorial 3: Multi-Backend Code Generation](#tutorial-3-multi-backend-code-generation)
- [Tutorial 4: Building a Pascal-Like Language](#tutorial-4-building-a-pascal-like-language)
- [Tutorial 5: Adding a Custom Backend](#tutorial-5-adding-a-custom-backend)

---

## Tutorial 1: Your First Language in 15 Minutes

This tutorial walks you through creating a minimal arithmetic language, parsing a program, and executing it — all in about 30 lines of Python.

### Step 1 — Install ParserCraft

```bash
git clone https://github.com/James-HoneyBadger/ParserCraft.git
cd ParserCraft
pip install -e .
```

Verify with:

```bash
parsercraft --version
# ParserCraft 4.0.0
```

### Step 2 — Write the Grammar

A grammar defines what programs in your language look like. ParserCraft uses PEG (Parsing Expression Grammars), which are clean and unambiguous.

Create `my_lang.py`:

```python
from parsercraft.parser import GrammarParser, PEGInterpreter
from parsercraft.codegen import transpile_and_exec

# Define the grammar using PEG text notation
grammar_text = """
    program   <- statement+
    statement <- IDENT "=" expr ";"
    expr      <- term (("+" / "-") term)*
    term      <- factor (("*" / "/") factor)*
    factor    <- NUMBER / IDENT / "(" expr ")"
"""

grammar = GrammarParser().parse(grammar_text)
print("Grammar compiled successfully.")
```

**What this grammar says:**
- A `program` is one or more `statement`s.
- A `statement` is an identifier, then `=`, then an expression, then `;`.
- An `expr` is a `term` optionally followed by `+` or `-` and more terms.
- A `term` is a `factor` optionally followed by `*` or `/` and more factors.
- A `factor` is a number, or an identifier, or a parenthesised expression.

### Step 3 — Parse Source Code

Add this to `my_lang.py`:

```python
# Source code in our new language
source = """
    x = 2 + 3 * 4 ;
    y = ( x - 1 ) * 2 ;
    area = 10 * 5 ;
"""

interp = PEGInterpreter(grammar)
ast = interp.parse(source)
print("Parsed successfully!")
print(ast.pretty())
```

Run it:

```bash
python my_lang.py
```

You should see the AST tree printed — each node shows the rule name and any values.

### Step 4 — Execute the Program

Add one more block:

```python
result = transpile_and_exec(ast)
print("\nResults:")
for name, value in sorted(result.items()):
    print(f"  {name} = {value}")
```

Expected output:

```
Results:
  area = 50
  x = 14
  y = 26
```

That is all it takes: grammar → parser → AST → execution.

### Step 5 — Run from the CLI

Save the grammar as a text file `my_lang.peg`:

```
program   <- statement+
statement <- IDENT "=" expr ";"
expr      <- term (("+" / "-") term)*
term      <- factor (("*" / "/") factor)*
factor    <- NUMBER / IDENT / "(" expr ")"
```

Then launch the REPL with it:

```bash
parsercraft repl --grammar my_lang.peg
```

Type expressions interactively:

```
> x = 10 + 5 ;
> y = x * 2 ;
> :vars
  x = 15
  y = 30
> :ast
> :quit
```

---

## Tutorial 2: Config-Driven Language Design

This tutorial shows how to use a YAML config file to define a language without writing PEG grammar rules manually. This approach is ideal for keyword-remapping, localisation, and rapid prototyping.

### Step 1 — Start from a Preset

```python
from parsercraft.config import LanguageConfig

# Start with the Python-like preset
config = LanguageConfig.from_preset("python_like")
print(config.name)          # "Python-Like"
print(config.keywords)      # {'if': 'if', 'else': 'else', ...}
```

### Step 2 — Customise Keywords

Let us build a Spanish-language Python variant:

```python
config.name = "PythonEspanol"
config.description = "Python with Spanish keywords"

mappings = {
    "if":       "si",
    "else":     "sino",
    "elif":     "si_no",
    "while":    "mientras",
    "for":      "para",
    "def":      "definir",
    "return":   "retornar",
    "True":     "Verdadero",
    "False":    "Falso",
    "and":      "y",
    "or":       "o",
    "not":      "no",
    "import":   "importar",
    "class":    "clase",
    "pass":     "pasar",
}

for english, spanish in mappings.items():
    config.rename_keyword(english, spanish)
```

### Step 3 — Add Custom Functions

```python
config.add_function("imprimir", "print")
config.add_function("longitud", "len")
config.add_function("tipo",     "type")
config.add_function("rango",    "range")
```

### Step 4 — Save the Config

```python
config.save("espanol.yaml")
```

Open `espanol.yaml` to inspect the output. It is a complete, human-readable YAML file you can edit directly.

### Step 5 — Validate

```bash
parsercraft validate espanol.yaml
# ✓ espanol.yaml is valid
```

### Step 6 — Use in the REPL

```bash
parsercraft repl espanol.yaml
```

```
> si 1 > 0 : imprimir("hola")
hola
> definir doble(x) : retornar x * 2
> doble(7)
14
> :quit
```

### Step 7 — Inspect the Config

```bash
parsercraft info espanol.yaml
```

This displays all keywords, functions, and syntax options in a formatted table.

---

## Tutorial 3: Multi-Backend Code Generation

One AST, four output formats. This tutorial demonstrates how to use all four ParserCraft backends on the same program.

### Setup

```python
from parsercraft.parser import GrammarParser, PEGInterpreter

grammar = GrammarParser().parse("""
    program   <- statement+
    statement <- IDENT "=" expr ";"
    expr      <- term (("+" / "-") term)*
    term      <- factor (("*" / "/") factor)*
    factor    <- NUMBER / IDENT / "(" expr ")"
""")

source = "a = 3 ; b = 4 ; c = a * a + b * b ;"
ast = PEGInterpreter(grammar).parse(source)
```

### Backend 1 — Python

```python
from parsercraft.codegen import PythonTranspiler, TranspileOptions

opts = TranspileOptions(wrap_in_main=True)
py_code = PythonTranspiler(opts).translate(ast)
print("=== Python ===")
print(py_code)
```

```python
# Output:
if __name__ == "__main__":
    a = 3
    b = 4
    c = a * a + b * b
```

### Backend 2 — C

```python
from parsercraft.codegen.codegen_c import CCodeGenerator

c_code = CCodeGenerator().translate_source_ast(ast)
print("=== C ===")
print(c_code)
```

```c
// Output:
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    int a = 3;
    int b = 4;
    int c = a * a + b * b;
    return 0;
}
```

### Backend 3 — WebAssembly

```python
from parsercraft.codegen.codegen_wasm import WasmGenerator

module = WasmGenerator().translate_source_ast(ast)
wat = module.to_wat()
print("=== WAT ===")
print(wat)
```

```wat
;; Output:
(module $module
  (memory 256)
  ...
  (func $main
    (local $a i32)
    (local $b i32)
    (local $c i32)
    ...
  )
)
```

### Backend 4 — LLVM IR

```python
from parsercraft.codegen import LLVMIRGenerator

ir = LLVMIRGenerator().translate_source_ast(ast)
print("=== LLVM IR ===")
print(ir)
```

```llvm
; Output:
define i32 @main() {
entry:
  %a = alloca i32
  store i32 3, i32* %a
  ...
  ret i32 0
}
```

### Execute Immediately

```python
from parsercraft.codegen import transpile_and_exec

result = transpile_and_exec(ast)
print(f"a={result['a']}, b={result['b']}, c={result['c']}")
# a=3, b=4, c=25
```

---

## Tutorial 4: Building a Pascal-Like Language

This tutorial builds a complete Pascal-like language using ParserCraft's`pascal_like` preset and demonstrates the full pipeline with realistic programs.

### The Pascal Config

```bash
parsercraft info configs/examples/pascal_like.yaml
```

Key differences from Python-like syntax:
- Assignment: `:=` instead of `=`
- Blocks: `BEGIN` … `END` instead of indentation
- Declarations: `VAR x : INTEGER ;` syntax
- Functions: `FUNCTION name(args) : ReturnType ;`

### Step 1 — Load and Inspect

```python
from parsercraft.config import LanguageConfig

config = LanguageConfig.load("configs/examples/pascal_like.yaml")
print(config.name)          # pascal_like or similar
print(config.keywords)
```

### Step 2 — Define a Simple PEG Grammar for Pascal Assignments

```python
from parsercraft.parser import GrammarParser, PEGInterpreter
from parsercraft.codegen import transpile_and_exec

grammar = GrammarParser().parse("""
    program   <- statement+
    statement <- IDENT ":=" expr ";"
    expr      <- term (("+" / "-") term)*
    term      <- factor (("*" / "/") factor)*
    factor    <- NUMBER / IDENT / "(" expr ")"
""")
```

### Step 3 — Write and Parse Pascal-Like Code

```python
source = """
    x := 10 ;
    y := x * 2 + 5 ;
    area := x * y ;
"""

interp = PEGInterpreter(grammar)
ast = interp.parse(source)
```

### Step 4 — Execute

```python
result = transpile_and_exec(ast)
print(f"x={result['x']}, y={result['y']}, area={result['area']}")
# x=10, y=25, area=250
```

> **Note:** ParserCraft's `PythonTranspiler` fully handles `:=` as an assignment operator. The `:=` is treated structurally (filtered out like `;`) and the variable name with its value are emitted as a Python assignment.

### Step 5 — Try the Demo

A complete Pascal-like demo is included in `demos/pascal_like/`:

```bash
python demos/pascal_like/run_pascal.py
```

This runs four programs through the full pipeline:
1. Basic arithmetic
2. Fibonacci sequence
3. Statistical calculations
4. Unit conversions

Each program is shown in Pascal-like syntax, transpiled to Python, executed, then also shown in C, WAT, and LLVM IR.

---

## Tutorial 5: Adding a Custom Backend

This tutorial shows how to add a fifth backend — a simple JavaScript emitter — to ParserCraft.

### Step 1 — Create the Backend File

Create `src/parsercraft/codegen/codegen_js.py`:

```python
"""JavaScript code generator for ParserCraft."""

from __future__ import annotations
from parsercraft.parser.grammar import SourceAST


class JSCodeGenerator:
    """Translate a SourceAST to JavaScript source code."""

    def translate_source_ast(self, ast: SourceAST) -> str:
        lines = []
        self._emit_node(ast, lines)
        return "\n".join(lines)

    def _emit_node(self, node: SourceAST, lines: list[str]) -> None:
        if node.node_type in ("program", "Program"):
            for child in node.children:
                self._emit_node(child, lines)

        elif node.node_type == "statement":
            # Detect inline assignment: [IDENT, Operator('='), expr, ...]
            idents = [c for c in node.children if c.node_type in ("IDENT", "Identifier")]
            ops    = [c for c in node.children if c.node_type == "Operator" and c.value in ("=", ":=")]
            exprs  = [c for c in node.children if c.node_type not in ("Operator", "IDENT", "Identifier")]
            if idents and ops and exprs:
                lhs = idents[0].value
                rhs = self._emit_expr(exprs[0])
                lines.append(f"let {lhs} = {rhs};")
            else:
                for child in node.children:
                    self._emit_node(child, lines)

        else:
            # Fallback — emit all children
            for child in node.children:
                self._emit_node(child, lines)

    def _emit_expr(self, node: SourceAST) -> str:
        if node.node_type == "Number":
            return node.value or "0"
        if node.node_type in ("IDENT", "Identifier"):
            return node.value or ""
        if node.node_type == "Operator":
            return node.value or ""
        # Compound expression: interleave children
        return " ".join(self._emit_expr(c) for c in node.children)
```

### Step 2 — Export from `__init__.py`

Add to `src/parsercraft/codegen/__init__.py`:

```python
from parsercraft.codegen.codegen_js import JSCodeGenerator
__all__ = [..., "JSCodeGenerator"]
```

### Step 3 — Use the Backend

```python
from parsercraft.parser import GrammarParser, PEGInterpreter
from parsercraft.codegen.codegen_js import JSCodeGenerator

grammar = GrammarParser().parse("""
    program   <- statement+
    statement <- IDENT "=" expr ";"
    expr      <- term (("+" / "-") term)*
    term      <- factor (("*" / "/") factor)*
    factor    <- NUMBER / IDENT / "(" expr ")"
""")

ast = PEGInterpreter(grammar).parse("x = 3 + 4 ; y = x * 2 ;")
js = JSCodeGenerator().translate_source_ast(ast)
print(js)
```

Expected output:

```javascript
let x = 3 + 4;
let y = x * 2;
```

### Step 4 — Add Tests

Create `tests/test_codegen_js.py`:

```python
from parsercraft.parser import GrammarParser, PEGInterpreter
from parsercraft.codegen.codegen_js import JSCodeGenerator


GRAMMAR = GrammarParser().parse("""
    program   <- statement+
    statement <- IDENT "=" expr ";"
    expr      <- term (("+" / "-") term)*
    term      <- factor (("*" / "/") factor)*
    factor    <- NUMBER / IDENT / "(" expr ")"
""")


def parse(src: str):
    return PEGInterpreter(GRAMMAR).parse(src)


def test_simple_assignment():
    ast = parse("x = 42 ;")
    js = JSCodeGenerator().translate_source_ast(ast)
    assert "let x = 42" in js


def test_expression():
    ast = parse("result = 3 + 4 * 2 ;")
    js = JSCodeGenerator().translate_source_ast(ast)
    assert "let result" in js
```

Run:

```bash
python -m pytest tests/test_codegen_js.py -v
```

---

*Happy building. If you get stuck, open an issue at [github.com/James-HoneyBadger/ParserCraft](https://github.com/James-HoneyBadger/ParserCraft/issues).*
