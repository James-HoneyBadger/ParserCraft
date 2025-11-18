# TeachScript Quick Reference

**Honey Badger Language Construction Set - TeachScript Language**

## Quick Start

```bash
# Run a TeachScript program
python3 run_teachscript.py myprogram.teach

# Run with verbose output (see translation)
python3 run_teachscript.py myprogram.teach --verbose

# Test all examples
python3 test_teachscript.py
```

## Syntax at a Glance

```teachscript
# Variables
remember name = "Alice"
remember age = 25

# Output
say("Hello, World!")
say("Name:", name, "Age:", age)

# Input
remember user_input = ask("Enter your name: ")

# Conditionals
when age >= 18:
    say("Adult")
or_when age >= 13:
    say("Teenager")
otherwise:
    say("Child")

# Loops
repeat_for i inside numbers_from(5):
    say(i)

repeat_while age > 0:
    say(age)
    age -= 1

# Functions
teach greet(name):
    say("Hello,", name)
    give_back nothing

teach add(a, b):
    give_back a + b

# Lists
remember items = [1, 2, 3]
items.add_to(4)
remember last = items.remove_from()

# Booleans
remember is_valid = yes
remember is_empty = no
```

## Keyword Reference

| TeachScript | Python |
|------------|--------|
| `when` | `if` |
| `otherwise` | `else` |
| `or_when` | `elif` |
| `repeat_while` | `while` |
| `repeat_for` | `for` |
| `teach` | `def` |
| `give_back` | `return` |
| `yes` / `no` | `True` / `False` |
| `nothing` | `None` |
| `and_also` | `and` |
| `or_else` | `or` |
| `opposite` | `not` |
| `inside` | `in` |
| `equals` | `is` |

## Function Reference

| TeachScript | Python |
|------------|--------|
| `say()` | `print()` |
| `ask()` | `input()` |
| `make_number()` | `int()` |
| `make_decimal()` | `float()` |
| `length_of()` | `len()` |
| `biggest()` | `max()` |
| `smallest()` | `min()` |
| `total()` | `sum()` |
| `numbers_from()` | `range()` |
| `count_through()` | `enumerate()` |
| `arrange()` | `sorted()` |

## Examples

### Hello World
```teachscript
say("Hello, World!")
```

### Fibonacci
```teachscript
teach fibonacci(n):
    when n <= 1:
        give_back n
    otherwise:
        give_back fibonacci(n - 1) + fibonacci(n - 2)

repeat_for i inside numbers_from(10):
    say("F(", i, ") =", fibonacci(i))
```

### Prime Checker
```teachscript
teach is_prime(n):
    when n < 2:
        give_back no
    repeat_for i inside numbers_from(2, n):
        when n % i equals 0:
            give_back no
    give_back yes
```

## More Information

- **Complete Manual**: [TEACHSCRIPT_MANUAL.md](TEACHSCRIPT_MANUAL.md)
- **Example Programs**: `teachscript_examples/` directory
- **HB_LCS Documentation**: [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
