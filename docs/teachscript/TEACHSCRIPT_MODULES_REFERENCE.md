# TeachScript Integration - Complete Module Reference

## Overview

This document provides a complete reference for all TeachScript modules integrated into the CodeCraft IDE.

---

## New Modules Created

### 1. **teachscript_runtime.py** (Main Runtime Engine)

```python
from src.hb_lcs.teachscript_runtime import (
    TeachScriptTranspiler,
    TeachScriptEnvironment,
    TeachScriptRuntime,
    get_runtime,
    reset_runtime
)
```

**Key Classes:**

- `TeachScriptTranspiler`: Converts TeachScript code to Python
  - `transpile(code: str) -> str`: Main transpilation method
  - `_translate_line(line: str) -> str`: Line-by-line translation
  - **Supports**: 17 keywords, 25+ functions, methods

- `TeachScriptEnvironment`: Execution environment
  - `execute(python_code: str) -> Tuple[str, str]`: Runs Python code
  - Built-in functions auto-registered
  - Educational libraries available

- `TeachScriptRuntime`: Main orchestrator
  - `run(teachscript_code: str) -> Tuple[str, str]`: Executes TeachScript
  - `run_file(filepath: str) -> Tuple[str, str]`: Runs from file
  - `get_transpiled_code(code: str) -> str`: View Python output
  - `get_syntax_errors(code: str) -> List[str]`: Validates syntax
  - `register_callback(event: str, callback: Callable)`: IDE hooks

**Example:**

```python
from src.hb_lcs.teachscript_runtime import get_runtime

runtime = get_runtime()
code = """
say("Hello, World!")
remember x = 5
say("x =", x)
"""

output, error = runtime.run(code)
print(output)  # Hello, World! \n x = 5
```

---

### 2. **ide_teachscript_integration.py** (IDE Integration)

```python
from src.hb_lcs.ide_teachscript_integration import TeachScriptIDEIntegration
```

**Key Class:**

- `TeachScriptIDEIntegration`: Integrates TeachScript into IDE
  - `add_teachscript_menus(menubar)`: Adds menu items
  - `add_teachscript_keyboard_shortcuts(root)`: Registers shortcuts
  - `is_teachscript_file(filepath: str) -> bool`: File detection
  - **Templates**: 8 built-in project templates

**Available Templates:**

1. `hello_world` - Simple output
2. `variables` - Variable operations
3. `conditionals` - If/else statements
4. `loops` - For/while loops
5. `functions` - Function definition
6. `lists` - List operations
7. `interactive_game` - Game example
8. (Extensible with custom templates)

**Example:**

```python
from src.hb_lcs.ide_teachscript_integration import TeachScriptIDEIntegration

integration = TeachScriptIDEIntegration(ide_instance)

# Add menus to IDE
integration.add_teachscript_menus(menubar)

# Register shortcuts
integration.add_teachscript_keyboard_shortcuts(root)
```

---

### 3. **teachscript_highlighting.py** (Syntax Features)

```python
from src.hb_lcs.teachscript_highlighting import (
    TeachScriptHighlighter,
    TeachScriptCodeCompletion,
    TeachScriptLinter
)
```

**Key Classes:**

- `TeachScriptHighlighter`: Color-coded syntax
  - `highlight_all()`: Highlight entire editor
  - `change_theme(new_theme: Dict[str, str])`: Custom colors
  - Auto-indentation on Enter
  - Comment and string detection

- `TeachScriptCodeCompletion`: Code auto-complete
  - `_show_completions(event)`: Triggered by Ctrl+Space
  - Completes keywords and functions
  - Shows popup with suggestions

- `TeachScriptLinter`: Syntax validation
  - `check_syntax(code: str) -> List[Tuple[int, str]]`: Error checking

**Example:**

```python
from src.hb_lcs.teachscript_highlighting import TeachScriptHighlighter

highlighter = TeachScriptHighlighter(text_widget)
highlighter.highlight_all()

# Change theme
custom_theme = {"keyword": "#FF0000", "function": "#00FF00"}
highlighter.change_theme(custom_theme)
```

---

### 4. **teachscript_console.py** (Interactive REPL)

```python
from src.hb_lcs.teachscript_console import TeachScriptConsole
```

**Key Class:**

- `TeachScriptConsole`: Interactive execution environment
  - `execute_teachscript_code(code: str) -> Tuple[str, str]`: Run code
  - Command history (Up/Down arrows)
  - Built-in commands: help, clear, reset, globals
  - Color-coded output

**Built-in Commands:**

```
help       - Show help message
clear      - Clear console
reset      - Reset environment
globals    - List global variables
exit/quit  - Exit console
```

**Example:**

```python
from src.hb_lcs.teachscript_console import TeachScriptConsole

console = TeachScriptConsole(parent_frame)
console.pack(fill="both", expand=True)

# Users can now type TeachScript code interactively
```

---

### 5. **teachscript_libraries.py** (Educational Libraries)

```python
from src.hb_lcs.teachscript_libraries import (
    TeachScriptGraphics,
    TeachScriptGame,
    TeachScriptMath,
    TeachScriptAnimation,
    TeachScriptRandom,
    Point, Rectangle, Circle, GameObject
)
```

**Available Libraries:**

**TSGraphics** - Shapes and Geometry
```python
point = TSGraphics.create_point(100, 100)
rect = TSGraphics.create_rectangle(50, 50, 200, 100)
circle = TSGraphics.create_circle(150, 150, 50)

dist = TSGraphics.point_distance(p1, p2)
area = TSGraphics.rectangle_area(rect)
circ = TSGraphics.circle_circumference(circle)
color = TSGraphics.color("red")
```

**TSGame** - Game Development
```python
player = TSGame.create_object("player", 100, 100)
enemy = TSGame.create_object("enemy", 300, 100)

player.velocity = TSGraphics.create_point(5, 0)
TSGame.update_all(0.016)

collisions = TSGame.check_collisions()
TSGame.add_score(10)
```

**TSMath** - Advanced Mathematics
```python
x = TSMath.sqrt(16)
y = TSMath.sin(TSMath.PI / 2)
result = TSMath.power(2, 10)

is_prime = TSMath.is_prime(17)
fib = TSMath.fibonacci(10)
```

**TSAnimation** - Animation Framework
```python
anim = TSAnimation.create_linear_animation(0, 100, 2.0)
anim.update(0.016)
value = anim.get_value()

TSAnimation.delay(1.0)
```

**TSRandom** - Enhanced Randomization
```python
rand = TSRandom.random()
dice = TSRandom.randint(1, 6)
choice = TSRandom.choice([1, 2, 3, 4, 5])
shuffled = TSRandom.shuffle(list)
```

---

### 6. **launch_ide_teachscript.py** (IDE Launcher)

```python
from src.hb_lcs.launch_ide_teachscript import launch_ide_with_teachscript
```

**Usage:**

```bash
python -m src.hb_lcs.launch_ide_teachscript
```

**Features:**
- Launches IDE with TeachScript pre-integrated
- Automatically adds menus and shortcuts
- Initializes syntax highlighting
- Sets up code completion

---

## Keyword Mappings

| TeachScript | Python |
|------------|--------|
| when | if |
| otherwise | else |
| or_when | elif |
| repeat_while | while |
| repeat_for | for |
| stop | break |
| skip | continue |
| teach | def |
| give_back | return |
| yes | True |
| no | False |
| nothing | None |
| and_also | and |
| or_else | or |
| opposite | not |
| inside | in |
| equals | is |
| remember | (variable) |
| forever | (constant) |

---

## Function Mappings

| TeachScript | Python |
|------------|--------|
| say() | print() |
| ask() | input() |
| make_number() | int() |
| make_decimal() | float() |
| make_text() | str() |
| make_boolean() | bool() |
| length_of() | len() |
| absolute() | abs() |
| round_to() | round() |
| biggest() | max() |
| smallest() | min() |
| total() | sum() |
| type_of() | type() |
| numbers_from() | range() |
| count_through() | enumerate() |
| arrange() | sorted() |
| backwards() | reversed() |

---

## Example Usage Patterns

### Pattern 1: Basic Program Execution

```python
from src.hb_lcs.teachscript_runtime import get_runtime

code = """
remember x = 5
when x > 3:
    say("x is greater than 3")
"""

runtime = get_runtime()
output, error = runtime.run(code)
print(output)
```

### Pattern 2: Syntax Validation

```python
from src.hb_lcs.teachscript_runtime import get_runtime

code = "remember x = 5\nsay(x"  # Missing closing paren

runtime = get_runtime()
errors = runtime.get_syntax_errors(code)
for error in errors:
    print(error)
```

### Pattern 3: Transpilation Inspection

```python
from src.hb_lcs.teachscript_runtime import get_runtime

teachscript_code = """
remember x = 10
teach add(a, b):
    give_back a + b
"""

runtime = get_runtime()
python_code = runtime.get_transpiled_code(teachscript_code)
print(python_code)
```

### Pattern 4: IDE Integration

```python
from src.hb_lcs.ide_teachscript_integration import TeachScriptIDEIntegration

# In your IDE initialization
integration = TeachScriptIDEIntegration(ide_instance)

# Add TeachScript menus
menubar = root.nametowidget(root.cget("menu"))
integration.add_teachscript_menus(menubar)

# Add keyboard shortcuts
integration.add_teachscript_keyboard_shortcuts(root)
```

### Pattern 5: Using Educational Libraries

```python
# In TeachScript code:
remember point1 = TSGraphics.create_point(0, 0)
remember point2 = TSGraphics.create_point(3, 4)
remember distance = TSGraphics.point_distance(point1, point2)
say("Distance:", distance)

# Or in Python after transpilation:
from src.hb_lcs.teachscript_libraries import TeachScriptGraphics as TSGraphics
point1 = TSGraphics.create_point(0, 0)
point2 = TSGraphics.create_point(3, 4)
distance = TSGraphics.point_distance(point1, point2)
print("Distance:", distance)
```

---

## Integration Points

### IDE Menu Items

- **File → New → TeachScript Project**: Create new TeachScript file
- **TeachScript → New Project**: Show template selection
- **TeachScript → Run (Ctrl+Shift+T)**: Execute current file
- **TeachScript → Preview Python Code**: Show transpiled code
- **TeachScript → Check Syntax**: Validate syntax
- **TeachScript → Interactive Tutorial**: Show lessons
- **TeachScript → Language Reference**: Show reference

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+Shift+T | Run TeachScript |
| Ctrl+Space | Code Completion |

### Editor Features

- Syntax highlighting for keywords, functions, strings, numbers
- Auto-indentation
- Comment detection
- Code completion popup
- Real-time error checking

### Console Integration

- Interactive REPL
- Code history (Up/Down arrows)
- Built-in commands
- Color-coded output

---

## Error Handling

**TeachScriptError**: Base exception
**TeachScriptSyntaxError**: Syntax validation errors
**TeachScriptRuntimeError**: Execution errors

Example:

```python
from src.hb_lcs.teachscript_runtime import TeachScriptError, get_runtime

try:
    runtime = get_runtime()
    output, error = runtime.run(bad_code)
    if error:
        print("Error:", error)
except TeachScriptError as e:
    print("TeachScript error:", e)
```

---

## Extension Guide

### Add a Custom Keyword

Edit `teachscript_runtime.py`:

```python
KEYWORD_MAP = {
    # ... existing mappings ...
    "my_keyword": "python_keyword",
}
```

### Add a Custom Library

Edit `teachscript_libraries.py`:

```python
class MyLibrary:
    @staticmethod
    def my_function():
        return "result"

# Add to __all__
__all__ = [..., "MyLibrary"]
```

Then in `TeachScriptEnvironment._setup_libraries()`:

```python
self.namespace["TSMyLib"] = MyLibrary
```

### Add a Project Template

Edit `ide_teachscript_integration.py`:

```python
TEMPLATES = {
    "my_template": {
        "name": "My Template",
        "description": "Description here",
        "code": """# Template code here"""
    }
}
```

---

## Testing

Run tests:

```bash
cd /home/james/CodeCraft
python -m pytest tests/test_teachscript.py -v
```

Test specific features:

```bash
# Test runtime
python -c "from src.hb_lcs.teachscript_runtime import get_runtime; print(get_runtime().run('say(\"Test\")'))"

# Test highlighting
python -c "from src.hb_lcs.teachscript_highlighting import TeachScriptHighlighter; print('✓')"

# Test libraries
python -c "from src.hb_lcs.teachscript_libraries import TeachScriptMath; print(TeachScriptMath.PI)"
```

---

## Complete Example Program

Create file `hello_game.teach`:

```teachscript
# Interactive guessing game with TeachScript

say("=== Number Guessing Game ===")
remember secret = TSRandom.randint(1, 100)
remember guess = nothing
remember tries = 0

teach check_guess(g, s):
    when g < s:
        give_back "too low"
    or_when g > s:
        give_back "too high"
    otherwise:
        give_back "correct"

repeat_while guess opposite equals secret:
    remember guess = make_number(ask("Guess (1-100): "))
    remember result = check_guess(guess, secret)
    remember tries = tries + 1
    
    when result equals "correct":
        say("You won in", tries, "tries!")
    otherwise:
        say(result.uppercase())

say("Thanks for playing!")
```

Run with:

```bash
python -m src.hb_lcs.launch_ide_teachscript
# Then load and run the file
```

---

## Documentation Reference

- **TEACHSCRIPT_IDE_INTEGRATION.md** - Main integration guide
- **TEACHSCRIPT_ADVANCED_GUIDE.md** - Advanced features
- **TEACHSCRIPT_MANUAL.md** - Language manual
- **TEACHSCRIPT_QUICKREF.md** - Quick reference
- **TEACHSCRIPT_SETUP_GUIDE.py** - Installation guide
- **TEACHSCRIPT_INTEGRATION_SUMMARY.py** - This integration

---

## Version Info

- **Integration Version**: 3.0
- **TeachScript Version**: 1.0
- **Python Compatibility**: 3.8+
- **Release Date**: December 30, 2025

---

## License

Same as CodeCraft - See LICENSE file

---

*End of Module Reference*
