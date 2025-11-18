# TeachScript Language Manual

**A Complete Custom Language Built with Honey Badger Language Construction Set**

Version 1.0 | November 2025

---

## Table of Contents

1. [Introduction](#introduction)
2. [What is TeachScript?](#what-is-teachscript)
3. [Proof of Concept](#proof-of-concept)
4. [Language Specification](#language-specification)
5. [Installation & Setup](#installation--setup)
6. [Quick Start Tutorial](#quick-start-tutorial)
7. [Complete Language Reference](#complete-language-reference)
8. [Example Programs](#example-programs)
9. [How It Works](#how-it-works)
10. [Creating Your Own Language](#creating-your-own-language)

---

## Introduction

This manual demonstrates the **complete, working implementation** of a custom programming language called **TeachScript**, created using the Honey Badger Language Construction Set (HB_LCS).

**Purpose**: To prove that HB_LCS actually works by showing a fully functional, beginner-friendly programming language with:
- ✓ Custom keywords and syntax
- ✓ Working code examples
- ✓ Real execution and output
- ✓ Complete documentation

---

## What is TeachScript?

**TeachScript** is an educational programming language designed to make programming more intuitive for beginners. It features:

- **Readable Keywords**: `when` instead of `if`, `teach` instead of `def`
- **Clear Function Names**: `say()` instead of `print()`, `ask()` instead of `input()`
- **Beginner-Friendly Syntax**: `remember x = 5` for variable declaration
- **Intuitive Operators**: `and_also`, `or_else`, `opposite` instead of `and`, `or`, `not`

---

## Proof of Concept

### This Language Actually Works!

Here's proof that TeachScript is a fully functional language:

**TeachScript Code** (`01_hello_world.teach`):
```teachscript
# TeachScript Example: Hello World
say("Hello, World!")
say("Welcome to TeachScript!")
```

**Execution**:
```bash
$ python3 run_teachscript.py teachscript_examples/01_hello_world.teach
Hello, World!
Welcome to TeachScript!
```

**✓ VERIFIED**: The code runs and produces correct output!

### More Complex Example

**TeachScript Code** (`05_functions.teach`):
```teachscript
teach fibonacci(n):
    when n <= 1:
        give_back n
    otherwise:
        give_back fibonacci(n - 1) + fibonacci(n - 2)

repeat_for i inside numbers_from(8):
    say("Fibonacci", i, "=", fibonacci(i))
```

**Output**:
```
Fibonacci 0 = 0
Fibonacci 1 = 1
Fibonacci 2 = 1
Fibonacci 3 = 2
Fibonacci 4 = 3
Fibonacci 5 = 5
Fibonacci 6 = 8
Fibonacci 7 = 13
```

**✓ VERIFIED**: Functions, recursion, and loops all work correctly!

---

## Language Specification

### Keywords

| TeachScript | Python | Description |
|------------|--------|-------------|
| `when` | `if` | Conditional statement |
| `otherwise` | `else` | Alternative condition |
| `or_when` | `elif` | Additional condition |
| `repeat_while` | `while` | While loop |
| `repeat_for` | `for` | For loop |
| `stop` | `break` | Break loop |
| `skip` | `continue` | Continue to next iteration |
| `teach` | `def` | Define function |
| `give_back` | `return` | Return value |
| `remember` | (none) | Variable declaration (optional) |
| `yes` | `True` | Boolean true |
| `no` | `False` | Boolean false |
| `nothing` | `None` | Null value |
| `and_also` | `and` | Logical AND |
| `or_else` | `or` | Logical OR |
| `opposite` | `not` | Logical NOT |
| `inside` | `in` | Membership test |
| `equals` | `is` | Identity test |

### Built-in Functions

| TeachScript | Python | Description |
|------------|--------|-------------|
| `say()` | `print()` | Output to console |
| `ask()` | `input()` | Get user input |
| `make_number()` | `int()` | Convert to integer |
| `make_decimal()` | `float()` | Convert to float |
| `make_text()` | `str()` | Convert to string |
| `make_boolean()` | `bool()` | Convert to boolean |
| `length_of()` | `len()` | Get length |
| `absolute()` | `abs()` | Absolute value |
| `round_to()` | `round()` | Round number |
| `biggest()` | `max()` | Maximum value |
| `smallest()` | `min()` | Minimum value |
| `total()` | `sum()` | Sum of values |
| `type_of()` | `type()` | Get type |
| `numbers_from()` | `range()` | Generate range |
| `count_through()` | `enumerate()` | Enumerate items |
| `arrange()` | `sorted()` | Sort items |
| `backwards()` | `reversed()` | Reverse items |

### Methods

| TeachScript | Python | Description |
|------------|--------|-------------|
| `.add_to()` | `.append()` | Add to list |
| `.remove_from()` | `.pop()` | Remove from list |

---

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- Honey Badger Language Construction Set (HB_LCS)

### Installation Steps

1. **Clone or download HB_LCS**:
```bash
cd HB_LCS
```

2. **Verify TeachScript files are present**:
```bash
ls run_teachscript.py teachscript.json teachscript_examples/
```

3. **Test installation**:
```bash
python3 run_teachscript.py teachscript_examples/01_hello_world.teach
```

If you see "Hello, World!", you're ready to go!

---

## Quick Start Tutorial

### Lesson 1: Your First Program

Create a file called `my_first.teach`:

```teachscript
say("Hello from TeachScript!")
```

Run it:
```bash
python3 run_teachscript.py my_first.teach
```

### Lesson 2: Variables

```teachscript
remember name = "Alice"
remember age = 25

say("Name:", name)
say("Age:", age)
```

### Lesson 3: Conditionals

```teachscript
remember temperature = 75

when temperature > 80:
    say("It's hot!")
or_when temperature > 60:
    say("It's pleasant!")
otherwise:
    say("It's chilly!")
```

### Lesson 4: Loops

```teachscript
# Count from 1 to 5
repeat_for i inside numbers_from(1, 6):
    say("Count:", i)

# Loop through a list
remember fruits = ["apple", "banana", "cherry"]
repeat_for fruit inside fruits:
    say("I like", fruit)
```

### Lesson 5: Functions

```teachscript
teach greet(name):
    say("Hello,", name, "!")

teach add(a, b):
    give_back a + b

greet("Alice")
remember result = add(5, 3)
say("5 + 3 =", result)
```

---

## Complete Language Reference

### Variables

TeachScript uses the `remember` keyword for clarity (optional):

```teachscript
remember x = 10
remember name = "Alice"
remember is_active = yes
remember data = [1, 2, 3]
```

### Data Types

```teachscript
# Numbers
remember integer = 42
remember decimal = 3.14

# Strings
remember text = "Hello"

# Booleans
remember truth = yes
remember falsehood = no

# None/Null
remember empty = nothing

# Lists
remember numbers = [1, 2, 3, 4, 5]

# Dictionaries
remember person = {"name": "Alice", "age": 25}
```

### Control Flow

#### If/Else Statements

```teachscript
when condition:
    # code
or_when other_condition:
    # code
otherwise:
    # code
```

#### While Loops

```teachscript
remember counter = 5
repeat_while counter > 0:
    say(counter)
    counter -= 1
```

#### For Loops

```teachscript
# Loop through range
repeat_for i inside numbers_from(10):
    say(i)

# Loop through list
repeat_for item inside my_list:
    say(item)

# Loop with index
repeat_for index, item inside count_through(my_list):
    say(index, ":", item)
```

### Functions

```teachscript
teach function_name(param1, param2):
    # function body
    give_back result
```

Example:
```teachscript
teach calculate_area(width, height):
    remember area = width * height
    give_back area

remember result = calculate_area(10, 5)
say("Area:", result)
```

### Operators

#### Arithmetic
- Addition: `+`
- Subtraction: `-`
- Multiplication: `*`
- Division: `/`
- Floor Division: `//`
- Modulo: `%`
- Exponentiation: `**`

#### Comparison
- Equal: `==`
- Not Equal: `!=`
- Less Than: `<`
- Greater Than: `>`
- Less or Equal: `<=`
- Greater or Equal: `>=`

#### Logical
- AND: `and_also`
- OR: `or_else`
- NOT: `opposite`

#### Assignment
- Assign: `=`
- Add assign: `+=`
- Subtract assign: `-=`
- Multiply assign: `*=`
- Divide assign: `/=`

---

## Example Programs

### Example 1: Hello World
**File**: `teachscript_examples/01_hello_world.teach`

```teachscript
say("Hello, World!")
say("Welcome to TeachScript!")
```

**Output**:
```
Hello, World!
Welcome to TeachScript!
```

---

### Example 2: Variables and Math
**File**: `teachscript_examples/02_variables.teach`

```teachscript
remember x = 10
remember y = 3

say("Addition:", x + y)
say("Subtraction:", x - y)
say("Multiplication:", x * y)
say("Division:", x / y)
say("Exponentiation:", x ** y)
```

**Output**:
```
Addition: 13
Subtraction: 7
Multiplication: 30
Division: 3.3333333333333335
Exponentiation: 1000
```

---

### Example 3: Conditionals
**File**: `teachscript_examples/03_conditionals.teach`

```teachscript
remember temperature = 75

when temperature > 80:
    say("It's hot outside!")
or_when temperature > 60:
    say("It's a pleasant day!")
otherwise:
    say("It's a bit chilly!")
```

**Output**:
```
It's a pleasant day!
```

---

### Example 4: Fibonacci Function
**File**: `teachscript_examples/05_functions.teach` (excerpt)

```teachscript
teach fibonacci(n):
    when n <= 1:
        give_back n
    otherwise:
        give_back fibonacci(n - 1) + fibonacci(n - 2)

repeat_for i inside numbers_from(8):
    say("Fibonacci", i, "=", fibonacci(i))
```

**Output**:
```
Fibonacci 0 = 0
Fibonacci 1 = 1
Fibonacci 2 = 1
Fibonacci 3 = 2
Fibonacci 4 = 3
Fibonacci 5 = 5
Fibonacci 6 = 8
Fibonacci 7 = 13
```

---

### Example 5: Prime Number Checker
**File**: `teachscript_examples/08_prime_numbers.teach` (excerpt)

```teachscript
teach is_prime(number):
    when number < 2:
        give_back no
    when number equals 2:
        give_back yes
    when number % 2 equals 0:
        give_back no
    
    remember divisor = 3
    repeat_while divisor * divisor <= number:
        when number % divisor equals 0:
            give_back no
        divisor += 2
    
    give_back yes

remember primes = []
repeat_for num inside numbers_from(1, 51):
    when is_prime(num):
        primes.add_to(num)

say("Prime numbers:", primes)
```

**Output**:
```
Prime numbers: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
```

---

## How It Works

### The Translation Process

TeachScript is implemented as a **source-to-source translator** that converts TeachScript code to Python code, then executes it.

#### Step 1: Write TeachScript Code
```teachscript
remember x = 5
when x > 3:
    say("Big number!")
```

#### Step 2: Translation to Python
The `run_teachscript.py` script translates:
```python
x = 5
if x > 3:
    print("Big number!")
```

#### Step 3: Execution
Python executes the translated code and produces output.

### The Runner Script

The `run_teachscript.py` script performs these steps:

1. **Read** the `.teach` file
2. **Translate** TeachScript keywords to Python keywords
3. **Translate** TeachScript function names to Python function names
4. **Execute** the resulting Python code
5. **Display** the output

### Keyword Mapping

The translation uses a simple dictionary mapping:

```python
KEYWORD_MAP = {
    'when': 'if',
    'otherwise': 'else',
    'or_when': 'elif',
    'teach': 'def',
    'give_back': 'return',
    # ... etc
}
```

### Word Boundary Replacement

The translator uses regex with word boundaries to ensure precise replacement:

```python
pattern = r'\b' + re.escape(teach_keyword) + r'\b'
translated = re.sub(pattern, python_keyword, code)
```

This ensures `when` is replaced with `if`, but `whenever` is left unchanged.

---

## Creating Your Own Language

### Using HB_LCS to Build Languages

TeachScript demonstrates how to use HB_LCS to create custom languages. Here's how:

### Step 1: Define Your Language

Decide on:
- Keyword mappings (`if` → `when`)
- Function renamings (`print` → `say`)
- Syntax rules (comments, operators, etc.)

### Step 2: Create Configuration

Create a `.json` configuration file with your mappings:

```json
{
  "metadata": {
    "name": "MyLanguage",
    "version": "1.0"
  },
  "keywords": {
    "if": {
      "original": "if",
      "custom": "when",
      "category": "control_flow"
    }
  },
  "builtin_functions": {
    "print": {
      "name": "say",
      "arity": -1,
      "enabled": true
    }
  }
}
```

### Step 3: Create a Runner

Create a translation script that:
1. Reads your custom language code
2. Applies keyword/function replacements
3. Executes the translated code

Example (simplified):

```python
import re

KEYWORD_MAP = {'when': 'if', 'say': 'print'}

def translate(code):
    for custom, python in KEYWORD_MAP.items():
        pattern = r'\b' + re.escape(custom) + r'\b'
        code = re.sub(pattern, python, code)
    return code

def run_file(filepath):
    with open(filepath) as f:
        code = f.read()
    python_code = translate(code)
    exec(python_code)
```

### Step 4: Write Examples

Create sample programs in your language to demonstrate functionality.

### Step 5: Test & Document

Run your examples and document:
- Language specification
- Syntax rules
- Example programs with output
- Tutorial for users

---

## Verification Results

### All Examples Tested

| Example | Status | Description |
|---------|--------|-------------|
| `01_hello_world.teach` | ✓ PASS | Basic output |
| `02_variables.teach` | ✓ PASS | Variables and math |
| `03_conditionals.teach` | ✓ PASS | If/else logic |
| `04_loops.teach` | ✓ PASS | For and while loops |
| `05_functions.teach` | ✓ PASS | Function definitions and recursion |
| `06_lists_strings.teach` | ✓ PASS | List operations and string methods |
| `08_prime_numbers.teach` | ✓ PASS | Algorithm implementation |

### Test Commands

You can verify all examples yourself:

```bash
# Test individual examples
python3 run_teachscript.py teachscript_examples/01_hello_world.teach
python3 run_teachscript.py teachscript_examples/02_variables.teach
python3 run_teachscript.py teachscript_examples/03_conditionals.teach
python3 run_teachscript.py teachscript_examples/04_loops.teach
python3 run_teachscript.py teachscript_examples/05_functions.teach
python3 run_teachscript.py teachscript_examples/06_lists_strings.teach
python3 run_teachscript.py teachscript_examples/08_prime_numbers.teach

# Run with verbose mode to see translation
python3 run_teachscript.py teachscript_examples/01_hello_world.teach --verbose
```

---

## Conclusion

**TeachScript proves that the Honey Badger Language Construction Set works as claimed.**

✓ **Custom language created**: TeachScript with unique syntax  
✓ **Real code examples**: 7+ working programs  
✓ **Actual execution**: All examples run and produce correct output  
✓ **Complete documentation**: Full language specification and tutorial  
✓ **Reproducible**: You can run and verify every example  

The Honey Badger Language Construction Set successfully enables:
- Creating custom programming languages
- Renaming keywords and functions
- Implementing alternative syntax
- Building educational or domain-specific languages
- Rapid prototyping of language ideas

---

## Additional Resources

### Files in This Project

- `teachscript.json` - Language configuration
- `teachscript.yaml` - Alternative YAML format
- `run_teachscript.py` - Language runner/translator
- `teachscript_examples/` - Example programs
  - `01_hello_world.teach`
  - `02_variables.teach`
  - `03_conditionals.teach`
  - `04_loops.teach`
  - `05_functions.teach`
  - `06_lists_strings.teach`
  - `07_calculator.teach` (interactive)
  - `08_prime_numbers.teach`
  - `09_guessing_game.teach` (interactive)

### HB_LCS Documentation

- `README.md` - Project overview
- `USER_GUIDE.md` - User manual
- `TECHNICAL_REFERENCE.md` - API documentation
- `LANGUAGE_DEVELOPMENT_GUIDE.md` - Language creation tutorials
- `DOCUMENTATION_INDEX.md` - Documentation index

---

## License

TeachScript is a demonstration language created with the Honey Badger Language Construction Set.

## Author

Created to demonstrate the capabilities of the Honey Badger Language Construction Set.

---

**End of Manual**
