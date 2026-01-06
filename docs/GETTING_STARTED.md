# Getting Started with ParserCraft

**Version 2.0** | January 2026

ParserCraft is a custom programming language construction framework that enables you to create language variants through configuration files (YAML/JSON) without compiler engineering knowledge.

---

## 📋 Table of Contents

1. [What is ParserCraft?](#what-is-parsercraft)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [First Language](#first-language)
5. [Running Programs](#running-programs)
6. [Next Steps](#next-steps)

---

## 🎯 What is ParserCraft?

ParserCraft allows you to:

- **Create custom programming languages** through simple configuration files
- **Rename keywords** (e.g., `if` → `cuando`, `def` → `teach`)
- **Add custom functions** and operators
- **Configure syntax rules** (array indexing, statement terminators, etc.)
- **Generate IDE support** (syntax highlighting, autocomplete, LSP integration)
- **Build and distribute** language interpreters

### Core Philosophy

**Language features are configured, not coded.** You define your language in YAML/JSON, and ParserCraft handles parsing, interpretation, and tooling.

---

## 💾 Installation

### Prerequisites

- **Python 3.8+** (Python 3.10+ recommended)
- **pip** package manager
- **Git** (optional, for cloning)

### Install from Repository

```bash
# Clone the repository
git clone https://github.com/James-HoneyBadger/ParserCraft.git
cd ParserCraft

# Install in development mode
pip install -e .

# Or install with all optional dependencies
pip install -e .[dev]
```

### Verify Installation

```bash
# Check ParserCraft CLI is available
parsercraft --version

# Run test suite
python -m pytest tests/ -v

# Launch IDE (requires tkinter)
python -m parsercraft.launch_ide
```

### Install Optional Dependencies

```bash
# YAML support (recommended)
pip install pyyaml

# Development tools
pip install pytest black mypy pylint
```

---

## 🚀 Quick Start

### 1. Create Your First Language Configuration

```bash
# Interactive mode - guides you through creation
parsercraft create --interactive --output my_lang.yaml

# Or use a preset template
parsercraft create --preset python_like --output my_lang.yaml
```

### 2. Edit Configuration

```yaml
# my_lang.yaml
name: MyLanguage
version: 1.0
description: My first custom language

keyword_mappings:
  if: cuando           # Spanish "when"
  else: sino           # Spanish "else"
  def: funcion         # Spanish "function"
  return: devolver     # Spanish "return"

syntax_options:
  array_start_index: 0
  allow_fractional_indexing: false
  statement_terminator: ""
```

### 3. Validate Configuration

```bash
parsercraft validate my_lang.yaml
```

### 4. Write a Program

Create `hello.ml` (my language):

```
funcion saludar(nombre):
    devolver "Hola, " + nombre + "!"

resultado = saludar("Mundo")
print(resultado)
```

### 5. Run Your Program

```bash
# Method 1: Using CLI
parsercraft run --config my_lang.yaml hello.ml

# Method 2: Using Python API
python3 << EOF
from parsercraft.language_runtime import LanguageRuntime

LanguageRuntime.load_config('my_lang.yaml')
runtime = LanguageRuntime.get_instance()
runtime.execute_file('hello.ml')
EOF
```

---

## 🔧 First Language: Step-by-Step

### Step 1: Start with a Preset

```bash
parsercraft create --preset python_like --output spanish.yaml
```

### Step 2: Customize Keywords

Edit `spanish.yaml`:

```yaml
name: Spanish Python
description: Python with Spanish keywords

keyword_mappings:
  # Control flow
  if: si
  elif: sino_si
  else: sino
  while: mientras
  for: para
  
  # Functions
  def: funcion
  return: devolver
  
  # Boolean
  True: Verdadero
  False: Falso
  
  # Data structures
  list: lista
  dict: diccionario
```

### Step 3: Add Custom Functions

```yaml
builtin_functions:
  imprimir:
    maps_to: print
    description: "Print to console"
  
  longitud:
    maps_to: len
    description: "Get length of collection"
  
  rango:
    maps_to: range
    description: "Create range of numbers"
```

### Step 4: Test Your Language

Create `prueba.py`:

```python
# Spanish Python example
funcion fibonacci(n):
    si n <= 1:
        devolver n
    sino:
        devolver fibonacci(n-1) + fibonacci(n-2)

para i dentro rango(10):
    imprimir(fibonacci(i))
```

Run it:

```bash
parsercraft run --config spanish.yaml prueba.py
```

---

## 🎮 Running Programs

### Using the CLI

```bash
# Basic execution
parsercraft run --config my_lang.yaml script.ml

# With debug output
parsercraft run --config my_lang.yaml script.ml --debug

# Show translated Python code
parsercraft translate --config my_lang.yaml --input script.ml
```

### Using the IDE

```bash
# Launch ParserCraft IDE
python -m parsercraft.launch_ide
```

In the IDE:
1. **File → Open Configuration** → Select `my_lang.yaml`
2. **File → New** → Create new script
3. Write code in your custom language
4. Click **Run** or press **F5**

### Using Python API

```python
from parsercraft.language_runtime import LanguageRuntime
from parsercraft.language_config import LanguageConfig

# Load configuration
config = LanguageConfig.load('my_lang.yaml')
LanguageRuntime.load_config(config_file='my_lang.yaml')

# Get runtime instance
runtime = LanguageRuntime.get_instance()

# Execute code
code = """
funcion sumar(a, b):
    devolver a + b

resultado = sumar(5, 3)
imprimir(resultado)
"""

runtime.execute(code)
```

---

## 📚 Next Steps

### Learn More

1. **[User Manual](USER_MANUAL.md)** - Complete guide to all features
2. **[Language Construction Guide](LANGUAGE_CONSTRUCTION_GUIDE.md)** - Deep dive into creating languages
3. **[API Reference](reference/API_REFERENCE.md)** - Complete API documentation
4. **[Examples & Tutorials](TUTORIALS.md)** - Learn by example

### Explore Features

- **Module System**: Create multi-file projects with imports
- **Type System**: Add static typing to your language
- **LSP Integration**: Get IDE support in VS Code, PyCharm, etc.
- **Code Generation**: Compile to C, WebAssembly, or other targets
- **Testing Framework**: Write and run automated tests

### Try Examples

```bash
# Example languages
cd configs/examples/

# TeachScript (educational)
parsercraft run --config ../teachscript.yaml ../../demos/teachscript/examples/01_hello_world.teach

# Lisp-like language
parsercraft run --config lisp_like.yaml lisp_demo.lisp

# BASIC-like language
parsercraft run --config basic_like.yaml basic_demo.bas
```

### Join the Community

- **Documentation**: `/home/james/CodeCraft/docs/`
- **Examples**: `/home/james/CodeCraft/demos/`
- **Tests**: `/home/james/CodeCraft/tests/`
- **GitHub**: https://github.com/James-HoneyBadger/ParserCraft

---

## 🆘 Troubleshooting

### Common Issues

**1. "parsercraft: command not found"**

```bash
# Ensure installation completed
pip install -e .

# Or use full path
python -m parsercraft.cli create --help
```

**2. "No module named 'parsercraft'"**

```bash
# Set PYTHONPATH
export PYTHONPATH=/home/james/CodeCraft/src:$PYTHONPATH

# Or install package
cd /home/james/CodeCraft
pip install -e .
```

**3. "tkinter not found" (IDE launch fails)**

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora/RHEL
sudo dnf install python3-tkinter

# macOS
# tkinter included with Python from python.org
```

**4. Configuration validation errors**

```bash
# Check syntax
parsercraft validate my_lang.yaml

# View detailed error info
parsercraft validate my_lang.yaml --verbose
```

### Getting Help

- **[Troubleshooting Guide](TROUBLESHOOTING.md)** - Detailed solutions
- **[FAQ](FAQ.md)** - Frequently asked questions
- **GitHub Issues** - Report bugs or request features

---

## 📖 Quick Reference

### Essential Commands

```bash
# Create new language
parsercraft create --preset python_like --output lang.yaml

# Validate configuration
parsercraft validate lang.yaml

# Run program
parsercraft run --config lang.yaml script.py

# Translate to Python
parsercraft translate --config lang.yaml --input script.py

# Start LSP server (for IDE integration)
parsercraft lsp --config lang.yaml --port 8080

# Launch IDE
python -m parsercraft.launch_ide
```

### Configuration Template

```yaml
name: MyLanguage
version: 1.0
description: Brief description

keyword_mappings:
  if: when
  def: function

builtin_functions:
  show:
    maps_to: print

syntax_options:
  array_start_index: 0
  allow_fractional_indexing: false
  statement_terminator: ""
```

---

## 🎓 Learning Path

### Beginner

1. Complete this Getting Started guide
2. Try the example languages in `configs/examples/`
3. Modify existing configurations
4. Create simple keyword remappings

### Intermediate

1. Build a complete custom language
2. Add custom functions and operators
3. Use the module system
4. Write language tests

### Advanced

1. Integrate LSP for IDE support
2. Implement code generation (C, WASM)
3. Add static type checking
4. Create language extensions/plugins

---

**Ready to create your first language? Let's go!** 🚀

For detailed information, see the [User Manual](USER_MANUAL.md).
