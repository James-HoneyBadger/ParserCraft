# ParserCraft User Manual

**Version 2.0** | Complete Reference Guide | January 2026

The comprehensive guide to using ParserCraft for custom programming language creation.

---

## 📚 Table of Contents

### Part I: Introduction
1. [Overview](#overview)
2. [Core Concepts](#core-concepts)
3. [System Architecture](#system-architecture)

### Part II: Configuration
4. [Language Configuration](#language-configuration)
5. [Keyword Mappings](#keyword-mappings)
6. [Custom Functions](#custom-functions)
7. [Operators and Syntax](#operators-and-syntax)

### Part III: Development
8. [Writing Programs](#writing-programs)
9. [Module System](#module-system)
10. [Type System](#type-system)
11. [Testing](#testing)

### Part IV: Tooling
12. [CLI Reference](#cli-reference)
13. [IDE Usage](#ide-usage)
14. [LSP Integration](#lsp-integration)
15. [Code Generation](#code-generation)

### Part V: Advanced Topics
16. [Performance Optimization](#performance-optimization)
17. [Debugging](#debugging)
18. [Production Deployment](#production-deployment)
19. [Security](#security)

---

## Overview

### What is ParserCraft?

ParserCraft is a **configuration-driven language construction framework** that allows you to create custom programming languages by defining their features in YAML or JSON configuration files.

**Key Benefits:**
- ✅ No compiler engineering knowledge required
- ✅ Rapid prototyping of language ideas
- ✅ Full IDE support (syntax highlighting, autocomplete, LSP)
- ✅ Production-ready runtime execution
- ✅ Multi-platform support (Windows, macOS, Linux)

### Use Cases

1. **Education**: Create simplified languages for teaching programming
2. **Domain-Specific Languages (DSLs)**: Build languages for specific industries
3. **Research**: Experiment with language design ideas
4. **Localization**: Create programming languages in different human languages
5. **Legacy Migration**: Create transitional languages for code modernization

---

## Core Concepts

### Three-Layer Architecture

```
┌─────────────────────────────────────┐
│   Configuration Layer                │
│   (YAML/JSON language definitions)   │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│   Runtime Layer                      │
│   (LanguageRuntime singleton)        │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│   Execution Layer                    │
│   (Parser, Interpreter, Modules)     │
└─────────────────────────────────────┘
```

### Key Components

1. **LanguageConfig**: Dataclass defining language features
2. **LanguageRuntime**: Singleton managing execution context
3. **ParserGenerator**: Creates lexers/parsers from config
4. **ModuleManager**: Handles multi-file imports
5. **LSPServer**: Provides IDE integration

---

## Language Configuration

### Configuration File Structure

```yaml
# Basic metadata
name: MyLanguage
version: 1.0.0
description: Description of your language
author: Your Name
license: MIT

# Keyword mappings (custom → Python)
keyword_mappings:
  if: cuando
  else: sino
  while: mientras
  for: para
  def: funcion
  return: devolver
  class: clase
  import: importar
  from: desde
  True: Verdadero
  False: Falso
  None: Nulo
  and: y
  or: o
  not: no
  in: dentro
  is: es
  lambda: lambda
  pass: pasar
  break: romper
  continue: continuar
  try: intentar
  except: excepto
  finally: finalmente
  raise: lanzar
  with: con
  as: como
  assert: afirmar
  yield: ceder
  global: global
  nonlocal: no_local

# Built-in function mappings
builtin_functions:
  imprimir:
    maps_to: print
    description: "Output to console"
  
  longitud:
    maps_to: len
    description: "Get length of collection"
  
  rango:
    maps_to: range
    description: "Create numeric range"
  
  tipo:
    maps_to: type
    description: "Get type of object"
  
  entero:
    maps_to: int
    description: "Convert to integer"
  
  flotante:
    maps_to: float
    description: "Convert to float"
  
  texto:
    maps_to: str
    description: "Convert to string"

# Operator mappings
operator_mappings:
  "+": "+"
  "-": "-"
  "*": "*"
  "/": "/"
  "%": "%"
  "**": "**"
  "==": "=="
  "!=": "!="
  "<": "<"
  ">": ">"
  "<=": "<="
  ">=": ">="

# Syntax configuration
syntax_options:
  array_start_index: 0
  allow_fractional_indexing: false
  statement_terminator: ""
  block_delimiter: "indent"
  comment_style: "#"
  multiline_comment_start: '"""'
  multiline_comment_end: '"""'
  string_quote_chars: ['"', "'"]
  case_sensitive: true
  require_explicit_types: false

# Module system
module_options:
  import_style: "python"
  module_extension: ".py"
  search_paths:
    - "."
    - "./lib"
    - "./modules"

# Type system
type_system:
  enabled: true
  inference: true
  strict_mode: false
  generic_types: true
  protocol_types: true
```

### Creating Configurations

#### Method 1: Interactive CLI

```bash
parsercraft create --interactive --output my_lang.yaml
```

You'll be prompted for:
- Language name and metadata
- Preset to start from (optional)
- Keywords to rename
- Custom functions to add
- Syntax preferences

#### Method 2: From Preset

```bash
# Available presets:
# - python_like: Python-style syntax
# - javascript_like: JavaScript-style syntax  
# - lisp_like: Lisp/Scheme-style syntax
# - forth_like: Forth/stack-based syntax
# - minimal: Minimal functional language
# - teachscript: Educational language

parsercraft create --preset python_like --output my_lang.yaml
```

#### Method 3: From Scratch

```bash
# Create empty configuration
cat > my_lang.yaml << 'EOF'
name: MyLanguage
version: 1.0
description: My custom language
keyword_mappings: {}
builtin_functions: {}
EOF

# Edit with your preferred editor
parsercraft edit my_lang.yaml
```

#### Method 4: Using Python API

```python
from parsercraft.language_config import LanguageConfig

config = LanguageConfig(
    name="MyLanguage",
    version="1.0",
    description="Custom language"
)

# Rename keywords
config.rename_keyword("if", "cuando")
config.rename_keyword("else", "sino")

# Add custom function
config.add_builtin_function("imprimir", "print", "Print to console")

# Configure syntax
config.set_array_indexing(start=0, allow_fractional=False)

# Save
config.save("my_lang.yaml", format="yaml")
```

---

## Keyword Mappings

### Standard Keyword Categories

#### Control Flow
```yaml
keyword_mappings:
  if: si
  elif: sino_si
  else: sino
  while: mientras
  for: para
  break: romper
  continue: continuar
  pass: pasar
```

#### Functions and Classes
```yaml
keyword_mappings:
  def: funcion
  class: clase
  return: devolver
  yield: ceder
  lambda: lambda
```

#### Boolean and Logic
```yaml
keyword_mappings:
  True: Verdadero
  False: Falso
  None: Nulo
  and: y
  or: o
  not: no
```

#### Import System
```yaml
keyword_mappings:
  import: importar
  from: desde
  as: como
```

#### Exception Handling
```yaml
keyword_mappings:
  try: intentar
  except: excepto
  finally: finalmente
  raise: lanzar
```

### Best Practices

1. **Be Consistent**: Use a consistent naming scheme (all Spanish, all French, etc.)
2. **Avoid Conflicts**: Don't use Python builtin names as custom keywords
3. **Document Changes**: Add descriptions for custom keywords
4. **Test Thoroughly**: Validate all keyword changes

```bash
# Validate configuration
parsercraft validate my_lang.yaml

# Test keyword translation
parsercraft translate --config my_lang.yaml --input test.ml
```

---

## Custom Functions

### Adding Built-in Functions

```yaml
builtin_functions:
  # Basic mapping
  imprimir:
    maps_to: print
    description: "Output text to console"
  
  # With type hints
  sumar:
    maps_to: sum
    description: "Sum a collection of numbers"
    signature: "sumar(iterable) -> number"
  
  # Custom implementation
  saludar:
    maps_to: "lambda name: f'Hello, {name}!'"
    description: "Greet someone by name"
```

### Function Categories

#### I/O Functions
```yaml
builtin_functions:
  imprimir:
    maps_to: print
  leer:
    maps_to: input
  abrir:
    maps_to: open
```

#### Type Conversion
```yaml
builtin_functions:
  entero:
    maps_to: int
  flotante:
    maps_to: float
  texto:
    maps_to: str
  booleano:
    maps_to: bool
  lista:
    maps_to: list
  tupla:
    maps_to: tuple
  diccionario:
    maps_to: dict
  conjunto:
    maps_to: set
```

#### Collection Operations
```yaml
builtin_functions:
  longitud:
    maps_to: len
  ordenar:
    maps_to: sorted
  filtrar:
    maps_to: filter
  mapear:
    maps_to: map
  reducir:
    maps_to: functools.reduce
  sumar:
    maps_to: sum
  maximo:
    maps_to: max
  minimo:
    maps_to: min
```

#### Math Functions
```yaml
builtin_functions:
  abs:
    maps_to: abs
  potencia:
    maps_to: pow
  redondear:
    maps_to: round
  piso:
    maps_to: math.floor
  techo:
    maps_to: math.ceil
```

### Adding Custom Libraries

```python
# custom_lib.py
def custom_function(arg1, arg2):
    """Your custom implementation."""
    return arg1 + arg2

# In configuration
builtin_functions:
  mi_funcion:
    maps_to: custom_lib.custom_function
    description: "My custom function"
```

---

## Operators and Syntax

### Operator Mappings

```yaml
operator_mappings:
  # Arithmetic
  "+": "+"
  "-": "-"
  "*": "*"
  "/": "/"
  "//": "//"    # Integer division
  "%": "%"      # Modulo
  "**": "**"    # Exponentiation
  
  # Comparison
  "==": "=="
  "!=": "!="
  "<": "<"
  ">": ">"
  "<=": "<="
  ">=": ">="
  
  # Logical
  "&&": "and"
  "||": "or"
  "!": "not"
  
  # Bitwise
  "&": "&"
  "|": "|"
  "^": "^"
  "~": "~"
  "<<": "<<"
  ">>": ">>"
  
  # Assignment
  "=": "="
  "+=": "+="
  "-=": "-="
  "*=": "*="
  "/=": "/="
```

### Syntax Options

#### Array Indexing

```yaml
syntax_options:
  # Standard: 0-based indexing
  array_start_index: 0
  allow_fractional_indexing: false
  
  # Alternative: 1-based indexing (like Lua, MATLAB)
  # array_start_index: 1
  
  # Satirical: -1 based (Gulf of Mexico indexing)
  # array_start_index: -1
```

#### Statement Terminators

```yaml
syntax_options:
  # Python-style (no terminator)
  statement_terminator: ""
  
  # C-style (semicolon)
  # statement_terminator: ";"
  
  # Pascal-style (period)
  # statement_terminator: "."
```

#### Block Delimiters

```yaml
syntax_options:
  # Python-style (indentation)
  block_delimiter: "indent"
  
  # C-style (braces)
  # block_delimiter: "braces"
  
  # Ruby-style (keywords)
  # block_delimiter: "keywords"  # e.g., end
```

#### Comments

```yaml
syntax_options:
  # Python-style
  comment_style: "#"
  multiline_comment_start: '"""'
  multiline_comment_end: '"""'
  
  # C-style
  # comment_style: "//"
  # multiline_comment_start: "/*"
  # multiline_comment_end: "*/"
  
  # Pascal-style
  # comment_style: "//"
  # multiline_comment_start: "(*"
  # multiline_comment_end: "*)"
```

---

## Writing Programs

### Basic Program Structure

```python
# Spanish Python example
# Archivo: calculadora.py

importar math

funcion factorial(n):
    """Calculate factorial recursively."""
    si n <= 1:
        devolver 1
    sino:
        devolver n * factorial(n - 1)

funcion main():
    imprimir("Calculadora de Factorial")
    numero = entero(leer("Ingrese un número: "))
    
    si numero < 0:
        imprimir("Error: número debe ser positivo")
        devolver
    
    resultado = factorial(numero)
    imprimir(f"{numero}! = {resultado}")

si __name__ == "__main__":
    main()
```

### Running Programs

```bash
# Method 1: CLI
parsercraft run --config spanish.yaml calculadora.py

# Method 2: REPL
parsercraft repl spanish.yaml
>>> imprimir("Hola mundo")
Hola mundo

# Method 3: Python API
python3 << EOF
from parsercraft.language_runtime import LanguageRuntime

LanguageRuntime.load_config('spanish.yaml')
runtime = LanguageRuntime.get_instance()
runtime.execute_file('calculadora.py')
EOF
```

---

## Module System

### Import Syntax

```python
# Import entire module
importar math
importar os

# Import specific items
desde math importar sin, cos, pi
desde os importar path, environ

# Import with alias
importar numpy como np
desde collections importar Counter como Contador
```

### Creating Modules

**Module: matematicas.py**
```python
# matematicas.py
desde math importar sqrt, pi

funcion distancia(x1, y1, x2, y2):
    """Calculate Euclidean distance."""
    devolver sqrt((x2-x1)**2 + (y2-y1)**2)

funcion area_circulo(radio):
    """Calculate circle area."""
    devolver pi * radio ** 2

constante = 42
```

**Using the module:**
```python
# main.py
importar matematicas

d = matematicas.distancia(0, 0, 3, 4)
a = matematicas.area_circulo(5)

imprimir(f"Distancia: {d}")
imprimir(f"Área: {a}")
```

### Module Search Paths

```yaml
module_options:
  search_paths:
    - "."              # Current directory
    - "./lib"          # Local library folder
    - "./modules"      # Modules folder
    - "~/.parsercraft/modules"  # User modules
```

### Package Structure

```
mi_proyecto/
├── main.py
├── lib/
│   ├── __init__.py
│   ├── utilidades.py
│   └── constantes.py
└── modules/
    ├── matematicas.py
    └── graficos.py
```

---

## Type System

### Type Annotations

```python
funcion saludar(nombre: texto) -> texto:
    devolver f"Hola, {nombre}!"

funcion sumar(a: entero, b: entero) -> entero:
    devolver a + b

clase Punto:
    x: flotante
    y: flotante
    
    funcion __init__(self, x: flotante, y: flotante):
        self.x = x
        self.y = y
```

### Generic Types

```python
desde typing importar List, Dict, Optional, Union

funcion procesar(items: List[entero]) -> Dict[texto, entero]:
    resultado: Dict[texto, entero] = {}
    para item dentro items:
        resultado[texto(item)] = item * 2
    devolver resultado

funcion buscar(nombre: texto) -> Optional[Punto]:
    si nombre dentro cache:
        devolver cache[nombre]
    devolver Nulo
```

### Type Checking

```bash
# Enable type checking in configuration
type_system:
  enabled: true
  inference: true
  strict_mode: true

# Check types via CLI
parsercraft check-types --config my_lang.yaml script.py

# Type inference
parsercraft infer-types --config my_lang.yaml script.py
```

---

## Testing

### Writing Tests

**test_matematicas.yaml**
```yaml
tests:
  - name: "Test factorial"
    code: |
      desde matematicas importar factorial
      assert factorial(5) == 120
      assert factorial(0) == 1
    expected_output: ""
    should_pass: true
  
  - name: "Test negative factorial"
    code: |
      desde matematicas importar factorial
      factorial(-1)
    should_fail: true
    expected_error: "ValueError"
```

### Running Tests

```bash
# Run test suite
parsercraft test --config my_lang.yaml --tests test_suite.yaml

# Show translation for failed tests
parsercraft test --config my_lang.yaml --tests test_suite.yaml --show-translation

# Stop on first failure
parsercraft test --config my_lang.yaml --tests test_suite.yaml --stop-on-fail

# Debug mode
parsercraft test --config my_lang.yaml --tests test_suite.yaml --debug
```

### Test Framework API

```python
from parsercraft.test_framework import LanguageTestRunner, TestCase

# Create test runner
runner = LanguageTestRunner(config)

# Add tests
runner.add_test(TestCase(
    name="test_addition",
    code="resultado = 2 + 2",
    expected_vars={"resultado": 4}
))

# Run tests
results = runner.run_all_tests()

# Generate report
report = runner.generate_report()
print(report)
```

---

## CLI Reference

### Core Commands

```bash
# Configuration Management
parsercraft create [--preset PRESET] [--output FILE]
parsercraft edit FILE
parsercraft validate FILE
parsercraft info [FILE]
parsercraft convert FILE --to FORMAT

# Execution
parsercraft run --config CONFIG FILE
parsercraft repl [CONFIG]
parsercraft batch CONFIG --script SCRIPT

# Translation
parsercraft translate --config CONFIG --input FILE [--output FILE]

# Testing
parsercraft test --config CONFIG --tests TESTS

# Code Analysis
parsercraft check-types --config CONFIG FILE
parsercraft infer-types --config CONFIG FILE
parsercraft lint --config CONFIG FILE

# LSP Server
parsercraft lsp --config CONFIG [--port PORT]

# Code Generation
parsercraft codegen-c --config CONFIG FILE
parsercraft codegen-wasm --config CONFIG FILE

# Project Management
parsercraft init PROJECT_NAME
parsercraft package --config CONFIG --output ZIP
```

### Command Options

See [CLI_REFERENCE.md](reference/CLI_REFERENCE.md) for complete documentation.

---

## IDE Usage

### Launching the IDE

```bash
# Launch ParserCraft IDE
python -m parsercraft.launch_ide

# Or use convenience script
cd /home/james/CodeCraft
PYTHONPATH=src:$PYTHONPATH python3 src/parsercraft/launch_ide.py
```

### IDE Features

1. **Configuration Editor**: Visual editor for language configs
2. **Code Editor**: Syntax highlighting and autocomplete
3. **Console**: Real-time output and REPL
4. **Project Explorer**: File tree navigation
5. **Debugger**: Step-through debugging
6. **Version Control**: Git integration

### Keyboard Shortcuts

- **F5**: Run program
- **F9**: Toggle breakpoint
- **F10**: Step over
- **F11**: Step into
- **Ctrl+S**: Save file
- **Ctrl+O**: Open file
- **Ctrl+N**: New file
- **Ctrl+F**: Find
- **Ctrl+H**: Find and replace

---

## LSP Integration

### Starting LSP Server

```bash
# Start server on default port (8080)
parsercraft lsp --config my_lang.yaml

# Specify port
parsercraft lsp --config my_lang.yaml --port 9000

# With debug logging
parsercraft lsp --config my_lang.yaml --debug
```

### VS Code Integration

1. Generate extension:
```bash
parsercraft extension --config my_lang.yaml --output my-lang-extension/
```

2. Install extension:
```bash
cd my-lang-extension
npm install
npm run compile
code --install-extension my-lang-extension.vsix
```

3. Configure in VS Code `settings.json`:
```json
{
  "mylanguage.lsp.enabled": true,
  "mylanguage.lsp.port": 8080
}
```

### LSP Features

- ✅ Syntax highlighting
- ✅ Autocomplete
- ✅ Go to definition
- ✅ Find references
- ✅ Hover information
- ✅ Diagnostics (errors/warnings)
- ✅ Code formatting
- ✅ Refactoring

---

## Code Generation

### C Code Generation

```bash
# Generate C code
parsercraft codegen-c --config my_lang.yaml program.ml --output program.c

# With optimizations
parsercraft codegen-c --config my_lang.yaml program.ml --output program.c --optimize

# Compile generated C
gcc -O2 program.c -o program
./program
```

### WebAssembly Generation

```bash
# Generate WASM
parsercraft codegen-wasm --config my_lang.yaml program.ml --output program.wasm

# With optimizations
parsercraft codegen-wasm --config my_lang.yaml program.ml --optimize

# Run in browser
# (embed program.wasm in HTML)
```

---

## Performance Optimization

### Configuration Optimization

```yaml
# Enable optimizations
optimization:
  level: 2  # 0=none, 1=basic, 2=aggressive
  inline_functions: true
  constant_folding: true
  dead_code_elimination: true
```

### Runtime Options

```bash
# Compile to bytecode
parsercraft compile --config my_lang.yaml program.ml --output program.pbc

# Run bytecode
parsercraft run --config my_lang.yaml program.pbc
```

### Profiling

```bash
# Profile execution
parsercraft profile --config my_lang.yaml program.ml

# Generate flame graph
parsercraft profile --config my_lang.yaml program.ml --flamegraph
```

---

## Debugging

### Debug Mode

```bash
# Run with debugger
parsercraft run --config my_lang.yaml program.ml --debug

# Set breakpoints
parsercraft debug --config my_lang.yaml program.ml --breakpoint 10,25,42
```

### Debug Commands

```
(pdb) help          # Show commands
(pdb) break 10      # Set breakpoint at line 10
(pdb) continue      # Continue execution
(pdb) step          # Step into function
(pdb) next          # Step over
(pdb) print var     # Print variable
(pdb) list          # Show source code
(pdb) where         # Show call stack
(pdb) quit          # Exit debugger
```

---

## Production Deployment

### Packaging

```bash
# Create distributable package
parsercraft package --config my_lang.yaml --output my_lang.zip

# Include dependencies
parsercraft package --config my_lang.yaml --output my_lang.zip --include-deps

# Create standalone executable
parsercraft build-exe --config my_lang.yaml --output my_lang_runtime
```

### Distribution

```bash
# Upload to package registry
parsercraft publish --config my_lang.yaml --registry https://registry.example.com

# Install from registry
parsercraft install my-language
```

---

## Security

### Safe Execution

```yaml
security:
  sandbox_enabled: true
  max_execution_time: 30  # seconds
  max_memory: 512  # MB
  allow_file_access: false
  allow_network: false
  allowed_modules:
    - math
    - random
```

### Input Validation

```bash
# Validate untrusted code
parsercraft validate-code --config my_lang.yaml untrusted.ml

# Run in sandbox
parsercraft run --config my_lang.yaml untrusted.ml --sandbox
```

---

## Appendices

### Appendix A: Configuration Schema

See [reference/CONFIG_SCHEMA.md](reference/CONFIG_SCHEMA.md)

### Appendix B: Example Languages

See [configs/examples/](../configs/examples/)

### Appendix C: API Documentation

See [reference/API_REFERENCE.md](reference/API_REFERENCE.md)

### Appendix D: Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## Index

[Full index of terms and concepts]

---

**End of User Manual**

For quick reference, see [QUICK_REFERENCE.md](QUICK_REFERENCE.md).

For developer information, see [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md).
