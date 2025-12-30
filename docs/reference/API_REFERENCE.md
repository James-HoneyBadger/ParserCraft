# CodeCraft Python API Reference

Complete API documentation for using CodeCraft programmatically in Python.

## Core Classes

### LanguageConfig

Main class for creating and managing language configurations.

```python
from hb_lcs.language_config import LanguageConfig
```

#### Constructor

```python
config = LanguageConfig()                          # Create empty config
config = LanguageConfig.from_file("lang.yaml")    # Load from file
config = LanguageConfig.from_preset("python_like")# Load from preset
```

#### Preset Names

- `python_like` - Python-style syntax
- `javascript_like` - JavaScript-style syntax
- `lisp_like` - Lisp-style syntax
- `minimal` - Minimal functional language
- `teachscript` - Educational language
- `pascal_like` - Pascal-style syntax
- `ruby_like` - Ruby-style syntax
- `forth_like` - Forth-style syntax
- `spanish` - Spanish-language keywords

#### Keyword Management

```python
# Rename a keyword
config.rename_keyword("if", "cuando")          # Old keyword → new keyword
config.rename_keyword("def", "funcion")
config.rename_keyword("return", "devolver")

# Get all keyword mappings
mappings = config.get_keyword_mappings()

# Clear all keywords
config.clear_keywords()
```

#### Syntax Configuration

```python
# Array indexing
config.set_array_indexing(0)      # 0-based indexing
config.set_array_indexing(1)      # 1-based indexing

# Comments
config.set_comment_style("#")     # Python-style
config.set_comment_style("//")    # C-style
config.set_comment_style(";")     # Lisp-style

# String delimiters
config.set_string_delimiters('"', "'")

# Operators
config.add_operator("+", "add")
config.add_operator("-", "subtract")
```

#### Functions

```python
# Add built-in function
config.add_function("say", "print to output")
config.add_function("input", "read from input")

# Remove function
config.remove_function("say")

# List functions
functions = config.get_functions()
```

#### File Operations

```python
# Save configuration
config.save("my_language.yaml")          # YAML format
config.save("my_language.json")          # JSON format

# Export as documentation
config.export_as_markdown("docs.md")
config.export_as_html("reference.html")

# Validate configuration
is_valid = config.validate()
if not is_valid:
    errors = config.get_validation_errors()
```

### LanguageRuntime

Execute code using a language configuration.

```python
from hb_lcs.language_runtime import LanguageRuntime
```

#### Execution

```python
# Create runtime from config
runtime = LanguageRuntime(config)

# Execute code
result = runtime.execute("say 'Hello, World!'")

# Execute with variables
result = runtime.execute(
    "x = 10\nprint(x)",
    variables={"initial_value": 5}
)

# Get execution output
output = runtime.get_output()
errors = runtime.get_errors()
```

#### REPL Mode

```python
# Interactive mode
runtime.repl()  # Launches interactive prompt
```

## Utility Classes

### InterpreterGenerator

Generate complete interpreter packages.

```python
from hb_lcs.interpreter_generator import InterpreterGenerator
```

```python
# Generate interpreter from config
generator = InterpreterGenerator(config)
package = generator.generate()

# Export as Python module
generator.export_to_module("output_dir/", "my_interpreter")
```

### LanguageValidator

Validate language configurations.

```python
from hb_lcs.language_validator import LanguageValidator
```

```python
validator = LanguageValidator(config)

if not validator.validate():
    for error in validator.get_errors():
        print(f"Error: {error}")
    
    for warning in validator.get_warnings():
        print(f"Warning: {warning}")
```

### ParserGenerator

Generate parsers from language definitions.

```python
from hb_lcs.parser_generator import ParserGenerator
```

```python
generator = ParserGenerator(config)
parser = generator.generate()

# Parse code
tokens = parser.tokenize(source_code)
ast = parser.parse(tokens)
```

## TeachScript Integration

### TeachScript Runtime

Specialized runtime for TeachScript language.

```python
from hb_lcs.teachscript_runtime import get_teachscript_runtime
```

```python
runtime = get_teachscript_runtime()

# Execute TeachScript code
result = runtime.execute("""
when x > 5:
    say "Greater than 5"
""")
```

### TeachScript Console

Interactive TeachScript environment.

```python
from hb_lcs.teachscript_console import TeachScriptConsole
```

```python
console = TeachScriptConsole()
console.run()  # Interactive REPL
```

## Complete Example

Create a Spanish-like language and test it:

```python
from hb_lcs.language_config import LanguageConfig
from hb_lcs.language_runtime import LanguageRuntime

# Create language configuration
config = LanguageConfig.from_preset("python_like")

# Customize for Spanish
config.rename_keyword("if", "si")
config.rename_keyword("else", "sino")
config.rename_keyword("def", "define")
config.rename_keyword("return", "devolver")
config.rename_keyword("while", "mientras")
config.rename_keyword("for", "para")

# Add Spanish built-ins
config.add_function("imprimir", "print output")
config.add_function("entrada", "read input")

# Save configuration
config.save("spanish.yaml")

# Test it
runtime = LanguageRuntime(config)
result = runtime.execute("""
define greet(name):
    imprimir "Hola, " + name

greet("Mundo")
""")

print(runtime.get_output())
```

## Error Handling

```python
from hb_lcs.language_config import LanguageConfigError
from hb_lcs.language_runtime import RuntimeError as LanguageRuntimeError

try:
    runtime.execute(code)
except LanguageRuntimeError as e:
    print(f"Runtime error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Advanced Topics

### Custom Operators

```python
config.add_operator("=>", "lambda_operator")
config.set_operator_precedence("=>", 1)
config.set_operator_associativity("=>", "right")
```

### Built-in Libraries

```python
# Access standard library
stdlib = config.get_standard_library()
math_module = stdlib.get_module("math")
string_module = stdlib.get_module("string")
```

### Configuration Validation

```python
# Detailed validation
validator = LanguageValidator(config)

errors = validator.validate_keywords()
errors += validator.validate_syntax()
errors += validator.validate_functions()

for error in errors:
    print(f"{error.level}: {error.message}")
```

## See Also

- [CLI Reference](CLI_REFERENCE.md) - Command-line tools
- [Configuration Reference](CONFIG_REFERENCE.md) - YAML/JSON schema
- [TeachScript Guide](../teachscript/README_TEACHSCRIPT.md) - Example language
