# Turing-Complete Programming Languages - Configuration Guide

This document explains how the Language Construction Set can be used to create Turing-complete programming languages across different paradigms.

## What Makes a Language Turing-Complete?

A programming language is **Turing-complete** if it can compute any function that a Turing machine can compute. The minimum requirements are:

1. **Conditional Branching** - ability to make decisions (if/then/else)
2. **Loops or Recursion** - ability to repeat operations
3. **Memory/Variables** - ability to store and retrieve data
4. **Arithmetic** - basic computation operations

## Six Programming Paradigms

### 1. Imperative/Procedural (BASIC-style)

**Configuration**: `examples/basic_like.yaml`

**Key Features:**
- Sequential statement execution
- Explicit state modification
- Procedures and functions
- Variables and arrays

**Turing-Complete Elements:**
```
✓ Branching: IF...THEN...ELSE
✓ Iteration: FOR...NEXT, WHILE...WEND
✓ Memory: LET (variables), DIM (arrays)
✓ Computation: +, -, *, /, MOD, ^
```

**Example Pseudocode:**
```basic
LET x = 10
IF x > 5 THEN
    PRINT "Large"
ELSE
    PRINT "Small"
END IF

FOR i = 1 TO 10
    LET sum = sum + i
NEXT i
```

### 2. Functional (LISP/Scheme-style)

**Configuration**: `examples/lisp_like.yaml`

**Key Features:**
- First-class functions
- Recursion instead of loops
- Immutable data structures
- Expression evaluation

**Turing-Complete Elements:**
```
✓ Branching: (if condition then else)
✓ Recursion: (define (func ...) (func ...))
✓ Memory: let bindings, lists
✓ Computation: Mathematical operators in prefix
```

**Example Pseudocode:**
```lisp
(define factorial
  (lambda (n)
    (if (= n 0)
        1
        (* n (factorial (- n 1))))))

(map (lambda (x) (* x 2)) '(1 2 3 4 5))
```

### 3. Stack-Based (Forth-style)

**Configuration**: `examples/forth_like.yaml`

**Key Features:**
- Postfix notation (Reverse Polish)
- Stack-based operations
- Direct memory access
- Minimal syntax

**Turing-Complete Elements:**
```
✓ Branching: IF...THEN...ELSE
✓ Iteration: BEGIN...UNTIL, DO...LOOP
✓ Memory: Stack + variables + heap
✓ Computation: Postfix operators
```

**Example Pseudocode:**
```forth
: square  ( n -- n² )
  DUP * ;

: factorial  ( n -- n! )
  DUP 1 > IF
    DUP 1 - factorial *
  THEN ;

5 factorial .  \ prints 120
```

### 4. Object-Oriented (Ruby-style)

**Configuration**: `examples/ruby_like.yaml`

**Key Features:**
- Objects and classes
- Methods and message passing
- Encapsulation
- Iterators and blocks

**Turing-Complete Elements:**
```
✓ Branching: if/elsif/else, unless
✓ Iteration: while, for, .each, .map
✓ Memory: Instance variables, objects
✓ Computation: Operators as methods
```

**Example Pseudocode:**
```ruby
class Counter
  def initialize
    @count = 0
  end
  
  def increment
    @count += 1
  end
end

[1, 2, 3, 4].map { |x| x * 2 }
```

### 5. Structured (Pascal-style)

**Configuration**: `examples/pascal_like.yaml`

**Key Features:**
- Strong typing
- Block structure (BEGIN...END)
- Records and arrays
- Procedures and functions

**Turing-Complete Elements:**
```
✓ Branching: IF...THEN...ELSE, CASE
✓ Iteration: WHILE, FOR, REPEAT...UNTIL
✓ Memory: VAR declarations, ARRAY OF
✓ Computation: Infix operators
```

**Example Pseudocode:**
```pascal
PROGRAM Factorial;
VAR
  n, result: INTEGER;

FUNCTION Fact(x: INTEGER): INTEGER;
BEGIN
  IF x <= 1 THEN
    Fact := 1
  ELSE
    Fact := x * Fact(x - 1);
END;

BEGIN
  WriteLn(Fact(5));
END.
```

### 6. Functional ML-style (OCaml-style)

**Configuration**: `examples/functional_ml.yaml`

**Key Features:**
- Pattern matching
- Algebraic data types
- Type inference
- Immutability by default

**Turing-Complete Elements:**
```
✓ Branching: if...then...else, match...with
✓ Recursion: let rec function definitions
✓ Memory: let bindings, lists, records
✓ Computation: Operators with precedence
```

**Example Pseudocode:**
```ocaml
let rec length lst =
  match lst with
  | [] -> 0
  | h :: t -> 1 + length t

let rec map f lst =
  match lst with
  | [] -> []
  | h :: t -> (f h) :: (map f t)
```

## Computational Equivalence

All six paradigms are **computationally equivalent** due to the Church-Turing thesis:

| Paradigm | Primary Model | Execution | Control Flow |
|----------|--------------|-----------|--------------|
| Imperative | State machine | Sequential | IF, WHILE, FOR |
| Functional | Lambda calculus | Expression eval | Recursion |
| Stack-based | Stack machine | Postfix | Stack + jumps |
| OOP | Objects/messages | Method dispatch | Methods + loops |
| Structured | Blocks | Nested scopes | Structured jumps |
| ML-style | Pattern match | Expression eval | Match + recursion |

**Key Insight**: They all can:
- Simulate a Turing machine
- Compute the same set of functions
- Simulate each other

## Creating Your Own Turing-Complete Language

### Minimum Requirements Checklist

To create a Turing-complete language configuration:

- [ ] **Conditional execution**
  - Add: `if`, `then`, `else` keywords
  - Or: pattern matching
  - Or: conditional jumps

- [ ] **Iteration/Recursion**
  - Add: `while`, `for`, or `do...while` keywords
  - Or: recursive function support
  - Or: jump/goto capabilities

- [ ] **Memory**
  - Add: variable declarations (`let`, `var`, `const`)
  - Or: stack operations
  - Or: direct memory access

- [ ] **Arithmetic**
  - Add operators: `+`, `-`, `*`, `/`
  - Add: comparison operators: `=`, `<`, `>`
  - Add: logical operators: `and`, `or`, `not`

### Example: Minimal Turing-Complete Config

```python
from language_config import LanguageConfig

config = LanguageConfig(name="Minimal Turing Complete", version="1.0")

# Conditionals
config.rename_keyword("if", "if")
config.rename_keyword("else", "else")

# Loops
config.rename_keyword("while", "while")

# Functions (enables recursion)
config.rename_keyword("function", "function")
config.rename_keyword("return", "return")

# Save it
config.save("minimal_turing.json")
```

## Testing Turing Completeness

A simple test is to implement these algorithms:

1. **Factorial** - Tests recursion/loops + arithmetic
2. **Fibonacci** - Tests multiple recursion paths
3. **Prime Test** - Tests conditionals + loops + modulo
4. **List Operations** - Tests data structures
5. **Higher-Order Functions** - Tests function abstraction

If your language can implement all five, it's Turing-complete.

## Advanced Features (Beyond Turing-Completeness)

These make languages more practical but don't affect Turing-completeness:

- Exception handling (try/catch)
- Module systems (import/export)
- Type systems (static/dynamic)
- Concurrency primitives
- I/O operations
- Standard libraries

## Theoretical Foundations

### Church-Turing Thesis
"Every effectively calculable function is computable by a Turing machine"

**Implications:**
- All Turing-complete languages have equal computational power
- Differences are in expressiveness, not capability
- No language can compute more than another Turing-complete language

### Halting Problem
Even Turing-complete languages cannot:
- Determine if arbitrary programs will halt
- Solve undecidable problems
- Compute non-computable functions

## Using the Configurations

### Load and Validate
```bash
# Validate a configuration
python langconfig.py validate examples/lisp_like.yaml

# View configuration details
python langconfig.py info examples/forth_like.yaml

# Load in IDE
python ide.py
# Then: Config → Load Config → Select file
```

### Programmatic Use
```python
from language_config import LanguageConfig
from language_runtime import LanguageRuntime

# Load configuration
config = LanguageConfig.load("examples/basic_like.yaml")

# Apply to runtime
LanguageRuntime.load_config(config)

# Get information
print(LanguageRuntime.get_info())
```

## References

1. **Turing, A.M. (1936)** - "On Computable Numbers, with an Application to the Entscheidungsproblem"

2. **Church, A. (1936)** - "An Unsolvable Problem of Elementary Number Theory"

3. **Böhm & Jacopini (1966)** - "Flow Diagrams, Turing Machines and Languages with Only Two Formation Rules" (Proves structured programming is Turing-complete)

4. **Kleene (1943)** - "Recursive Predicates and Quantifiers" (μ-recursive functions)

## Summary

The Language Construction Set allows you to:

✓ Define languages across multiple paradigms  
✓ Ensure Turing-completeness with minimal features  
✓ Experiment with syntax and semantics  
✓ Study computational equivalence  
✓ Create domain-specific languages  

All six example configurations demonstrate different approaches to achieving the same computational power.
