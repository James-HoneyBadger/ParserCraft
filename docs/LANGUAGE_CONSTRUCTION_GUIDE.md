# ParserCraft Language Construction Guide

**Version 2.0** | Complete Guide to Building Custom Languages | January 2026

---

## Table of Contents

1. [Introduction](#introduction)
2. [Language Design Principles](#language-design-principles)
3. [Step-by-Step Language Creation](#step-by-step-language-creation)
4. [Keyword Design](#keyword-design)
5. [Function Libraries](#function-libraries)
6. [Syntax Design](#syntax-design)
7. [Type System Integration](#type-system-integration)
8. [Module System Design](#module-system-design)
9. [Real-World Examples](#real-world-examples)
10. [Best Practices](#best-practices)

---

## Introduction

This guide teaches you how to design and implement custom programming languages using ParserCraft. Whether you're creating an educational language, a domain-specific language (DSL), or experimenting with language design, this guide provides a structured approach.

### What You'll Learn

- How to design a language from scratch
- Best practices for keyword selection
- Creating consistent syntax rules
- Building standard libraries
- Testing and validating your language

---

## Language Design Principles

### 1. Know Your Audience

Before designing, ask:
- **Who will use this language?**
  - Students, professionals, domain experts?
- **What problems does it solve?**
  - Simplification, domain-specific tasks, education?
- **What's the learning curve?**
  - Beginner-friendly vs. expert-focused

### 2. Design Goals

Choose primary goals:
- **Readability**: Easy to read and understand
- **Simplicity**: Minimal concepts to learn
- **Power**: Express complex ideas concisely
- **Safety**: Prevent common errors
- **Performance**: Fast execution

### 3. Consistency

Maintain consistency in:
- Naming conventions
- Syntax patterns
- Error messages
- Standard library design

---

## Step-by-Step Language Creation

### Phase 1: Conceptual Design

**Define Your Language's Purpose**

```yaml
# Example: Educational language for beginners
name: LearnCode
purpose: Teaching programming to children (ages 8-12)
key_features:
  - Simple English keywords
  - No complex punctuation
  - Visual feedback
  - Safe execution environment
```

**Design Philosophy**

```
Guiding Principles:
1. Use familiar words (say instead of print)
2. Natural language feel (repeat 5 times instead of for i in range(5))
3. Immediate visual feedback
4. Encourage experimentation
5. Clear, helpful error messages
```

### Phase 2: Keyword Mapping

```yaml
keyword_mappings:
  # Control flow (natural language)
  if: when
  else: otherwise
  while: repeat_while
  for: repeat_for
  
  # Functions (teaching metaphor)
  def: teach
  return: answer
  
  # Variables (clarity)
  True: yes
  False: no
  None: nothing
  
  # Logic (natural)
  and: also
  or: or_else
  not: opposite
  
  # Structures
  class: blueprint
  import: use
```

### Phase 3: Function Library

```yaml
builtin_functions:
  # Output (friendly)
  say:
    maps_to: print
    description: "Display message to user"
  
  ask:
    maps_to: input
    description: "Get input from user"
  
  # Math (intuitive)
  count:
    maps_to: len
    description: "Count items in collection"
  
  numbers_from:
    maps_to: range
    description: "Create sequence of numbers"
  
  # Conversions
  make_number:
    maps_to: int
    description: "Convert to whole number"
  
  make_text:
    maps_to: str
    description: "Convert to text"
```

### Phase 4: Syntax Rules

```yaml
syntax_options:
  # Beginner-friendly: 1-based indexing
  array_start_index: 1
  allow_fractional_indexing: false
  
  # No semicolons
  statement_terminator: ""
  
  # Indentation for blocks
  block_delimiter: "indent"
  
  # Simple comments
  comment_style: "#"
  
  # Case insensitive (for beginners)
  case_sensitive: false
```

### Phase 5: Example Programs

**Hello World**
```
teach greet(name):
    say("Hello, " + name + "!")

greet("Alice")
```

**Loop Example**
```
repeat_for number inside numbers_from(1, 11):
    say(number)
```

**Conditional Example**
```
age = make_number(ask("How old are you? "))

when age >= 13:
    say("You're a teenager!")
otherwise:
    say("You're a kid!")
```

### Phase 6: Testing

```yaml
tests:
  - name: "Test greeting"
    code: |
      teach greet(name):
          answer "Hello, " + name
      result = greet("World")
      say(result)
    expected_output: "Hello, World\n"
  
  - name: "Test loop"
    code: |
      total = 0
      repeat_for n inside numbers_from(1, 6):
          total = total + n
      say(total)
    expected_output: "15\n"
```

---

## Keyword Design

### Categories of Keywords

#### 1. Control Flow Keywords

```yaml
# Standard approach (Python-like)
if: si
elif: sino_si
else: sino

# Natural language approach
if: when
elif: when_also
else: otherwise

# Question-based approach
if: is_it_true_that
elif: or_is_it_true_that
else: if_nothing_is_true
```

#### 2. Function Keywords

```yaml
# Professional
def: function
return: return

# Educational
def: teach
return: answer

# Domain-specific (math)
def: formula
return: result
```

#### 3. Loop Keywords

```yaml
# Traditional
for: for
while: while

# Descriptive
for: repeat_for
while: repeat_while

# Action-based
for: go_through
while: keep_doing
```

### Keyword Selection Guidelines

1. **Be Consistent**: Use similar patterns across the language
2. **Avoid Ambiguity**: Don't use words with multiple meanings
3. **Consider Length**: Balance brevity and clarity
4. **Test Pronunciation**: Keywords should be easy to say
5. **Check Translations**: Ensure localized keywords make sense

---

## Function Libraries

### Standard Library Design

#### Category 1: I/O Functions

```yaml
builtin_functions:
  # Console I/O
  display:
    maps_to: print
    category: "I/O"
    examples: ['display("Hello")', 'display(x, y, z)']
  
  prompt:
    maps_to: input
    category: "I/O"
    examples: ['name = prompt("Enter name: ")']
  
  # File I/O
  read_file:
    maps_to: open
    category: "I/O"
    mode: "r"
  
  write_file:
    maps_to: open
    category: "I/O"
    mode: "w"
```

#### Category 2: Data Structures

```yaml
builtin_functions:
  # Lists
  create_list:
    maps_to: list
    category: "Data Structures"
  
  add_item:
    maps_to: list.append
    category: "Data Structures"
  
  remove_item:
    maps_to: list.remove
    category: "Data Structures"
  
  # Dictionaries
  create_dictionary:
    maps_to: dict
    category: "Data Structures"
```

#### Category 3: Math Operations

```yaml
builtin_functions:
  absolute:
    maps_to: abs
    category: "Math"
  
  power:
    maps_to: pow
    category: "Math"
  
  square_root:
    maps_to: math.sqrt
    category: "Math"
  
  round_number:
    maps_to: round
    category: "Math"
```

### Domain-Specific Libraries

**Example: Financial DSL**

```yaml
builtin_functions:
  calculate_interest:
    maps_to: "lambda principal, rate, time: principal * rate * time"
    category: "Finance"
  
  compound_growth:
    maps_to: "lambda p, r, n, t: p * (1 + r/n)**(n*t)"
    category: "Finance"
  
  present_value:
    maps_to: "lambda fv, r, n: fv / (1 + r)**n"
    category: "Finance"
```

---

## Syntax Design

### Indexing Conventions

```yaml
# Zero-based (like Python, JavaScript)
syntax_options:
  array_start_index: 0
  
# One-based (like Lua, MATLAB)
syntax_options:
  array_start_index: 1
  
# Custom (Gulf of Mexico: -1 based)
syntax_options:
  array_start_index: -1
```

### Statement Terminators

```yaml
# No terminator (Python-style)
statement_terminator: ""

# Semicolon (C-style)
statement_terminator: ";"

# Newline required
statement_terminator: "\n"
```

### Block Delimiters

```yaml
# Indentation (Python)
block_delimiter: "indent"

# Braces (C/Java/JavaScript)
block_delimiter: "braces"

# Keywords (Ruby/Pascal)
block_delimiter: "keywords"  # Uses 'end'
```

### Comment Styles

```yaml
# Hash/pound (Python, Ruby)
comment_style: "#"

# Double-slash (C, Java, JavaScript)
comment_style: "//"

# Exclamation (Fortran, VBA)
comment_style: "!"
```

---

## Type System Integration

### Basic Type Annotations

```yaml
type_system:
  enabled: true
  inference: true
  strict_mode: false
```

**Usage:**
```python
teach calculate(x: number, y: number) -> number:
    answer x + y

result: number = calculate(5, 3)
```

### Generic Types

```yaml
type_system:
  enabled: true
  generic_types: true
```

**Usage:**
```python
teach find_max(items: list[number]) -> number:
    answer max(items)
```

### Custom Type Names

```yaml
# Map Python types to custom names
type_mappings:
  int: numero
  float: decimal
  str: texto
  bool: logico
  list: lista
  dict: diccionario
```

---

## Module System Design

### Import Styles

#### Python-style

```yaml
module_options:
  import_style: "python"
```

```python
import math
from collections import Counter
```

#### JavaScript-style

```yaml
module_options:
  import_style: "javascript"
```

```javascript
require math
import { Counter } from collections
```

#### Custom Import

```yaml
keyword_mappings:
  import: use
  from: grab

module_options:
  import_style: "python"
```

```
use math
grab sin, cos via math
```

### Module Organization

```yaml
module_options:
  module_extension: ".lc"  # Custom extension
  search_paths:
    - "."
    - "./stdlib"
    - "./user_modules"
    - "~/.learncode/modules"
```

---

## Real-World Examples

### Example 1: Spanish Programming Language

**Design Goals:**
- Teach programming in Spanish
- Maintain Python's elegance
- Support Spanish-speaking students

**Configuration:**

```yaml
name: PythonEspañol
version: 1.0
description: Python con palabras clave en español

keyword_mappings:
  if: si
  elif: sino_si
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

builtin_functions:
  imprimir:
    maps_to: print
  longitud:
    maps_to: len
  rango:
    maps_to: range
  entero:
    maps_to: int
  flotante:
    maps_to: float
  texto:
    maps_to: str

syntax_options:
  array_start_index: 0
  statement_terminator: ""
  block_delimiter: "indent"
```

**Example Program:**

```python
# Calculadora de números primos
funcion es_primo(numero):
    si numero < 2:
        devolver Falso
    para i dentro rango(2, numero):
        si numero % i == 0:
            devolver Falso
    devolver Verdadero

para n dentro rango(1, 101):
    si es_primo(n):
        imprimir(f"{n} es primo")
```

### Example 2: Kids Programming Language

**Design Goals:**
- Extremely simple for children
- Natural English
- Visual and fun

**Configuration:**

```yaml
name: KidsCode
version: 1.0
description: Programming for kids ages 6-10

keyword_mappings:
  if: when
  else: otherwise
  while: repeat_while
  for: repeat_for
  def: teach
  return: give_back
  True: yes
  False: no
  and: also
  or: or_maybe
  not: opposite
  in: inside

builtin_functions:
  say:
    maps_to: print
  ask:
    maps_to: input
  count:
    maps_to: len
  numbers_from:
    maps_to: range
  make_number:
    maps_to: int
  wait:
    maps_to: time.sleep

syntax_options:
  array_start_index: 1  # Kids count from 1
  case_sensitive: false  # Forgiving
```

**Example Program:**

```
teach make_pattern():
    repeat_for i inside numbers_from(1, 6):
        say("*" * i)

make_pattern()

name = ask("What's your name? ")
say("Hi " + name + "!")
```

### Example 3: Math DSL

**Design Goals:**
- Domain-specific for mathematics
- Concise formula notation
- Built-in math functions

**Configuration:**

```yaml
name: MathLang
version: 1.0
description: Mathematical computation language

keyword_mappings:
  def: formula
  return: result
  if: when
  else: otherwise

builtin_functions:
  sqrt:
    maps_to: math.sqrt
  sin:
    maps_to: math.sin
  cos:
    maps_to: math.cos
  tan:
    maps_to: math.tan
  log:
    maps_to: math.log
  exp:
    maps_to: math.exp
  abs:
    maps_to: abs
  sum:
    maps_to: sum
  
# Special: Allow mathematical operators
operator_mappings:
  "^": "**"  # Power operator
  "×": "*"   # Multiplication
  "÷": "/"   # Division
```

**Example Program:**

```
formula quadratic(a, b, c):
    discriminant = sqrt(b^2 - 4×a×c)
    x1 = (-b + discriminant) ÷ (2×a)
    x2 = (-b - discriminant) ÷ (2×a)
    result (x1, x2)

roots = quadratic(1, -3, 2)
print(roots)
```

---

## Best Practices

### 1. Start Simple

Begin with minimal features:
```yaml
# Minimum viable language
keyword_mappings:
  if: when
  def: function
  return: return

builtin_functions:
  print:
    maps_to: print
  input:
    maps_to: input
```

Expand incrementally as needed.

### 2. Test Early and Often

```bash
# Test each feature as you add it
parsercraft validate my_lang.yaml
parsercraft test --config my_lang.yaml --tests tests.yaml
```

### 3. Document Everything

Create comprehensive documentation:
- Language reference
- Tutorial
- Standard library docs
- Code examples

### 4. Gather Feedback

- Have users try your language
- Iterate based on feedback
- Monitor common errors

### 5. Maintain Backward Compatibility

When updating:
- Don't break existing code
- Deprecate gradually
- Provide migration guides

### 6. Provide Good Error Messages

```yaml
# Configure helpful errors
error_messages:
  syntax_error: "Oops! Check your spelling and punctuation on line {line}"
  name_error: "I don't recognize '{name}'. Did you forget to define it?"
  type_error: "Expected {expected} but got {actual}"
```

### 7. Create Standard Library

Build commonly needed functions:
- String manipulation
- List operations
- Math functions
- File I/O
- Date/time handling

### 8. Consider Tooling

Provide:
- Syntax highlighter
- LSP server for IDEs
- Debugger
- Package manager
- Documentation generator

---

## Quick Reference Checklist

### Language Creation Checklist

- [ ] Define purpose and audience
- [ ] Design keyword mappings
- [ ] Create function library
- [ ] Configure syntax options
- [ ] Write example programs
- [ ] Create test suite
- [ ] Write documentation
- [ ] Generate IDE support
- [ ] Gather user feedback
- [ ] Iterate and improve

### Configuration File Checklist

- [ ] Basic metadata (name, version, description)
- [ ] Keyword mappings (complete set)
- [ ] Built-in functions (sufficient library)
- [ ] Operator mappings (if needed)
- [ ] Syntax options (consistent choices)
- [ ] Module system configuration
- [ ] Type system options
- [ ] Error message templates

### Testing Checklist

- [ ] Basic syntax tests
- [ ] Control flow tests
- [ ] Function definition tests
- [ ] Module import tests
- [ ] Error handling tests
- [ ] Integration tests
- [ ] Real-world example programs

---

## Additional Resources

- [Getting Started Guide](GETTING_STARTED.md)
- [User Manual](USER_MANUAL.md)
- [API Reference](reference/API_REFERENCE.md)
- [Example Languages](../configs/examples/)
- [TeachScript Case Study](teachscript/TEACHSCRIPT_MANUAL.md)

---

**Ready to build your language?** Start with `parsercraft create --interactive`!
