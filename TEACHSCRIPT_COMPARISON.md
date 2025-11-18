# TeachScript Side-by-Side Comparison

This document shows TeachScript code alongside the equivalent Python code to demonstrate the translation.

---

## Example 1: Hello World

### TeachScript
```teachscript
say("Hello, World!")
say("Welcome to TeachScript!")
```

### Python (Translated)
```python
print("Hello, World!")
print("Welcome to TeachScript!")
```

### Output
```
Hello, World!
Welcome to TeachScript!
```

---

## Example 2: Variables and Conditionals

### TeachScript
```teachscript
remember temperature = 75

when temperature > 80:
    say("It's hot!")
or_when temperature > 60:
    say("It's pleasant!")
otherwise:
    say("It's chilly!")
```

### Python (Translated)
```python
temperature = 75

if temperature > 80:
    print("It's hot!")
elif temperature > 60:
    print("It's pleasant!")
else:
    print("It's chilly!")
```

### Output
```
It's pleasant!
```

---

## Example 3: Loops

### TeachScript
```teachscript
remember fruits = ["apple", "banana", "cherry"]

repeat_for fruit inside fruits:
    say("I like", fruit)
```

### Python (Translated)
```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print("I like", fruit)
```

### Output
```
I like apple
I like banana
I like cherry
```

---

## Example 4: Functions with Recursion

### TeachScript
```teachscript
teach fibonacci(n):
    when n <= 1:
        give_back n
    otherwise:
        give_back fibonacci(n - 1) + fibonacci(n - 2)

repeat_for i inside numbers_from(8):
    say("Fib", i, "=", fibonacci(i))
```

### Python (Translated)
```python
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

for i in range(8):
    print("Fib", i, "=", fibonacci(i))
```

### Output
```
Fib 0 = 0
Fib 1 = 1
Fib 2 = 1
Fib 3 = 2
Fib 4 = 3
Fib 5 = 5
Fib 6 = 8
Fib 7 = 13
```

---

## Example 5: Algorithm (Prime Number Checker)

### TeachScript
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

remember test_nums = [17, 18, 29, 30]
repeat_for num inside test_nums:
    when is_prime(num):
        say(num, "is prime")
    otherwise:
        say(num, "is not prime")
```

### Python (Translated)
```python
def is_prime(number):
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    
    divisor = 3
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 2
    
    return True

test_nums = [17, 18, 29, 30]
for num in test_nums:
    if is_prime(num):
        print(num, "is prime")
    else:
        print(num, "is not prime")
```

### Output
```
17 is prime
18 is not prime
29 is prime
30 is not prime
```

---

## Complete Keyword Mapping

| TeachScript | → | Python |
|------------|---|--------|
| `when` | → | `if` |
| `otherwise` | → | `else` |
| `or_when` | → | `elif` |
| `repeat_while` | → | `while` |
| `repeat_for` | → | `for` |
| `stop` | → | `break` |
| `skip` | → | `continue` |
| `teach` | → | `def` |
| `give_back` | → | `return` |
| `remember` | → | *(removed)* |
| `yes` | → | `True` |
| `no` | → | `False` |
| `nothing` | → | `None` |
| `and_also` | → | `and` |
| `or_else` | → | `or` |
| `opposite` | → | `not` |
| `inside` | → | `in` |
| `equals` | → | `is` |

## Complete Function Mapping

| TeachScript | → | Python |
|------------|---|--------|
| `say()` | → | `print()` |
| `ask()` | → | `input()` |
| `make_number()` | → | `int()` |
| `make_decimal()` | → | `float()` |
| `make_text()` | → | `str()` |
| `make_boolean()` | → | `bool()` |
| `length_of()` | → | `len()` |
| `absolute()` | → | `abs()` |
| `round_to()` | → | `round()` |
| `biggest()` | → | `max()` |
| `smallest()` | → | `min()` |
| `total()` | → | `sum()` |
| `type_of()` | → | `type()` |
| `numbers_from()` | → | `range()` |
| `count_through()` | → | `enumerate()` |
| `arrange()` | → | `sorted()` |
| `backwards()` | → | `reversed()` |

---

## How to See Translations

Run any TeachScript program with `--verbose` to see the translation:

```bash
python3 run_teachscript.py teachscript_examples/01_hello_world.teach --verbose
```

This shows:
1. Original TeachScript code
2. Translated Python code
3. Execution output

---

**See [TEACHSCRIPT_MANUAL.md](TEACHSCRIPT_MANUAL.md) for complete documentation**
