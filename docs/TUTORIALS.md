# ParserCraft Examples and Tutorials

**Version 2.0** | Learn by Doing | January 2026

---

## Table of Contents

1. [Tutorial 1: Your First Custom Language](#tutorial-1-your-first-custom-language)
2. [Tutorial 2: Spanish Python](#tutorial-2-spanish-python)
3. [Tutorial 3: Kids Programming Language](#tutorial-3-kids-programming-language)
4. [Tutorial 4: Mathematical DSL](#tutorial-4-mathematical-dsl)
5. [Tutorial 5: Module System](#tutorial-5-module-system)
6. [Tutorial 6: Type-Safe Language](#tutorial-6-type-safe-language)
7. [Tutorial 7: IDE Integration](#tutorial-7-ide-integration)
8. [Tutorial 8: Code Generation](#tutorial-8-code-generation)

---

## Tutorial 1: Your First Custom Language

**Goal**: Create a simple language with custom keywords in 10 minutes

### Step 1: Create Configuration

```bash
cd ~/projects
mkdir my-first-lang
cd my-first-lang

# Create config file
cat > simple.yaml << 'EOF'
name: SimpleLang
version: 1.0
description: My first custom language

keyword_mappings:
  if: when
  else: otherwise
  def: function
  return: give

builtin_functions:
  show:
    maps_to: print
    description: "Display output"

syntax_options:
  array_start_index: 0
  statement_terminator: ""
EOF
```

### Step 2: Validate Configuration

```bash
parsercraft validate simple.yaml
```

Expected output:
```
✓ Configuration is valid
✓ All keywords mapped correctly
✓ No conflicts detected
```

### Step 3: Write a Program

```bash
cat > hello.sl << 'EOF'
function greet(name):
    give "Hello, " + name + "!"

result = greet("World")
show(result)

when result:
    show("Success!")
otherwise:
    show("Failed!")
EOF
```

### Step 4: Run the Program

```bash
parsercraft run --config simple.yaml hello.sl
```

Expected output:
```
Hello, World!
Success!
```

### Step 5: View Translated Code

```bash
parsercraft translate --config simple.yaml --input hello.sl
```

See Python equivalent:
```python
def greet(name):
    return "Hello, " + name + "!"

result = greet("World")
print(result)

if result:
    print("Success!")
else:
    print("Failed!")
```

**🎉 Congratulations!** You've created your first custom language!

---

## Tutorial 2: Spanish Python

**Goal**: Create a full-featured Spanish programming language

### Step 1: Configuration

```bash
cat > espanol.yaml << 'EOF'
name: PythonEspañol
version: 1.0
description: Python programming in Spanish

keyword_mappings:
  # Control flow
  if: si
  elif: sino_si
  else: sino
  while: mientras
  for: para
  break: romper
  continue: continuar
  
  # Functions
  def: funcion
  return: devolver
  lambda: lambda
  
  # Boolean
  True: Verdadero
  False: Falso
  None: Nulo
  and: y
  or: o
  not: no
  
  # Context
  in: dentro
  is: es
  
  # Import
  import: importar
  from: desde
  as: como
  
  # Exception handling
  try: intentar
  except: excepto
  finally: finalmente
  raise: lanzar
  
  # Classes
  class: clase
  pass: pasar

builtin_functions:
  # I/O
  imprimir:
    maps_to: print
  leer:
    maps_to: input
  
  # Type conversions
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
  
  # Collections
  longitud:
    maps_to: len
  rango:
    maps_to: range
  ordenar:
    maps_to: sorted
  sumar:
    maps_to: sum
  maximo:
    maps_to: max
  minimo:
    maps_to: min

syntax_options:
  array_start_index: 0
  statement_terminator: ""
  block_delimiter: "indent"
EOF
```

### Step 2: Example Programs

**Fibonacci Sequence:**
```python
# fibonacci.py
funcion fibonacci(n):
    si n <= 1:
        devolver n
    sino:
        devolver fibonacci(n-1) + fibonacci(n-2)

imprimir("Secuencia de Fibonacci:")
para i dentro rango(10):
    imprimir(f"fib({i}) = {fibonacci(i)}")
```

**Prime Numbers:**
```python
# primos.py
funcion es_primo(numero):
    si numero < 2:
        devolver Falso
    para i dentro rango(2, entero(numero ** 0.5) + 1):
        si numero % i == 0:
            devolver Falso
    devolver Verdadero

imprimir("Números primos hasta 100:")
primos = [n para n dentro rango(2, 101) si es_primo(n)]
imprimir(primos)
```

**Class Example:**
```python
# persona.py
clase Persona:
    funcion __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
    
    funcion saludar(self):
        imprimir(f"Hola, soy {self.nombre} y tengo {self.edad} años")

persona1 = Persona("María", 25)
persona2 = Persona("Juan", 30)

persona1.saludar()
persona2.saludar()
```

### Step 3: Run Programs

```bash
parsercraft run --config espanol.yaml fibonacci.py
parsercraft run --config espanol.yaml primos.py
parsercraft run --config espanol.yaml persona.py
```

---

## Tutorial 3: Kids Programming Language

**Goal**: Create ultra-simple language for children

### Step 1: Kid-Friendly Configuration

```yaml
name: KidsCode
version: 1.0
description: Programming for kids ages 6-10

keyword_mappings:
  if: when
  else: otherwise
  while: keep_doing
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
  make_text:
    maps_to: str

syntax_options:
  array_start_index: 1  # Kids count from 1
  case_sensitive: false
  statement_terminator: ""
```

### Step 2: Fun Examples

**Pattern Maker:**
```
teach make_pattern(rows):
    repeat_for i inside numbers_from(1, rows + 1):
        say("*" * i)

make_pattern(5)
```

**Guessing Game:**
```
teach guessing_game():
    secret = 7
    say("I'm thinking of a number between 1 and 10!")
    
    guess = make_number(ask("What's your guess? "))
    
    when guess == secret:
        say("You got it! Amazing!")
    otherwise:
        say("Not quite! The number was " + make_text(secret))

guessing_game()
```

**Story Generator:**
```
teach tell_story(name, animal):
    say("Once upon a time, there was a kid named " + name)
    say(name + " had a pet " + animal)
    say("They went on amazing adventures together!")
    say("The end!")

my_name = ask("What's your name? ")
my_pet = ask("What's your favorite animal? ")

tell_story(my_name, my_pet)
```

---

## Tutorial 4: Mathematical DSL

**Goal**: Create domain-specific language for math

### Configuration with Math Symbols

```yaml
name: MathLang
version: 1.0

keyword_mappings:
  def: formula
  return: result

builtin_functions:
  sqrt: { maps_to: "math.sqrt" }
  sin: { maps_to: "math.sin" }
  cos: { maps_to: "math.cos" }
  tan: { maps_to: "math.tan" }
  log: { maps_to: "math.log" }
  exp: { maps_to: "math.exp" }
  abs: { maps_to: "abs" }
  pi: { maps_to: "math.pi" }
  e: { maps_to: "math.e" }

operator_mappings:
  "^": "**"  # Power
  "×": "*"   # Times
  "÷": "/"   # Divide
```

### Mathematical Examples

**Quadratic Formula:**
```python
formula quadratic(a, b, c):
    discriminant = sqrt(b^2 - 4×a×c)
    x1 = (-b + discriminant) ÷ (2×a)
    x2 = (-b - discriminant) ÷ (2×a)
    result (x1, x2)

roots = quadratic(1, -5, 6)
print(f"Roots: {roots}")
```

**Distance Formula:**
```python
formula distance(x1, y1, x2, y2):
    result sqrt((x2-x1)^2 + (y2-y1)^2)

d = distance(0, 0, 3, 4)
print(f"Distance: {d}")
```

---

## Tutorial 5: Module System

**Goal**: Create multi-file project

### Project Structure

```
my_project/
├── main.py
├── lib/
│   ├── math_utils.py
│   └── string_utils.py
└── config.yaml
```

### Configuration

```yaml
name: MyProject
version: 1.0

module_options:
  search_paths:
    - "."
    - "./lib"

keyword_mappings:
  import: use
  from: grab
  def: function
  return: give

builtin_functions:
  show: { maps_to: "print" }
```

### Module Files

**lib/math_utils.py:**
```python
function factorial(n):
    when n <= 1:
        give 1
    otherwise:
        give n * factorial(n - 1)

function fibonacci(n):
    when n <= 1:
        give n
    otherwise:
        give fibonacci(n-1) + fibonacci(n-2)
```

**lib/string_utils.py:**
```python
function reverse(text):
    give text[::-1]

function capitalize_words(text):
    words = text.split()
    give " ".join(word.capitalize() for word in words)
```

**main.py:**
```python
use lib.math_utils
grab reverse, capitalize_words from lib.string_utils

show("Factorial of 5:", math_utils.factorial(5))
show("Fibonacci of 10:", math_utils.fibonacci(10))

text = "hello world"
show("Reversed:", reverse(text))
show("Capitalized:", capitalize_words(text))
```

### Run

```bash
parsercraft run --config config.yaml main.py
```

---

## Tutorial 6: Type-Safe Language

**Goal**: Add static type checking

### Configuration with Types

```yaml
name: SafeLang
version: 1.0

type_system:
  enabled: true
  inference: true
  strict_mode: true

type_mappings:
  int: number
  str: text
  bool: logic
  list: collection

keyword_mappings:
  def: function
  return: give

builtin_functions:
  show: { maps_to: "print" }
```

### Type-Annotated Programs

```python
function calculate(x: number, y: number) -> number:
    result: number = x + y
    give result

function greet(name: text) -> text:
    message: text = "Hello, " + name
    give message

# Type checking catches errors
value: number = calculate(5, 3)  # ✓ OK
name: text = greet("World")      # ✓ OK

# This would fail type check:
# wrong: number = greet("World")  # ✗ Type error!
```

### Check Types

```bash
parsercraft check-types --config config.yaml program.py
```

---

## Tutorial 7: IDE Integration

**Goal**: Set up IDE support with LSP

### Step 1: Start LSP Server

```bash
parsercraft lsp --config my_lang.yaml --port 8080
```

### Step 2: Generate VS Code Extension

```bash
parsercraft extension --config my_lang.yaml --output my-lang-ext/
cd my-lang-ext/
npm install
npm run compile
```

### Step 3: Install Extension

```bash
code --install-extension my-lang-ext/my-language-1.0.0.vsix
```

### Step 4: Configure VS Code

Add to `.vscode/settings.json`:
```json
{
  "mylanguage.lsp.enabled": true,
  "mylanguage.lsp.port": 8080,
  "files.associations": {
    "*.ml": "mylanguage"
  }
}
```

### Features

- ✅ Syntax highlighting
- ✅ Autocomplete
- ✅ Go to definition
- ✅ Error highlighting
- ✅ Hover documentation

---

## Tutorial 8: Code Generation

**Goal**: Compile to C and WebAssembly

### C Code Generation

```bash
# Generate C code
parsercraft codegen-c --config my_lang.yaml program.ml --output program.c

# Compile with GCC
gcc -O2 program.c -o program

# Run executable
./program
```

### WebAssembly Generation

```bash
# Generate WASM
parsercraft codegen-wasm --config my_lang.yaml program.ml --output program.wasm

# Use in HTML
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head><title>My Language WASM</title></head>
<body>
    <script>
        fetch('program.wasm')
            .then(response => response.arrayBuffer())
            .then(bytes => WebAssembly.instantiate(bytes))
            .then(results => {
                results.instance.exports.main();
            });
    </script>
</body>
</html>
EOF

# Open in browser
python3 -m http.server 8000
```

---

## Practice Exercises

### Exercise 1: Color Language

Create a language where keywords are color names:
- `red` = if
- `blue` = else
- `green` = def
- etc.

### Exercise 2: Emoji Language

Use emojis as keywords:
- 🤔 = if
- 🔄 = while
- 📝 = print
- etc.

### Exercise 3: Musical Language

Music-themed keywords:
- `play` = def
- `sing` = print
- `repeat` = while
- etc.

### Exercise 4: RPG Language

Game-themed keywords:
- `quest` = def
- `when_encountered` = if
- `cast` = print
- etc.

---

## Additional Resources

### Example Languages

See `configs/examples/` for:
- `python_like.yaml` - Python-style syntax
- `lisp_like.yaml` - Lisp/Scheme syntax
- `basic_like.yaml` - BASIC-style syntax
- `forth_like.yaml` - Stack-based syntax
- `ruby_like.yaml` - Ruby-style syntax

### TeachScript

Complete educational language example in `demos/teachscript/`:
- Full configuration
- 12+ example programs
- Comprehensive documentation
- IDE integration

### More Tutorials

- [Getting Started Guide](GETTING_STARTED.md)
- [User Manual](USER_MANUAL.md)
- [Language Construction Guide](LANGUAGE_CONSTRUCTION_GUIDE.md)

---

**Keep Learning!** Create your own unique language! 🚀
