# CodeCraft

**Create Custom Programming Languages Without Writing a Compiler**

CodeCraft is a comprehensive framework for designing and deploying custom programming language variants through simple configuration files. No compiler engineering required—just define your language syntax and semantics through intuitive JSON/YAML configurations.

## 🎯 **Proof of Concept: TeachScript**

**See a complete, working custom language built with CodeCraft!**

**TeachScript** is a beginner-friendly educational programming language demonstrating CodeCraft's power:
- `when` instead of `if` for conditionals
- `teach` instead of `def` for function definitions
- `say()` instead of `print()` for output
- Intuitive, English-like syntax ideal for learning

**Try TeachScript now**:
```bash
# Quick start - launch TeachScript IDE
./run-codecraft.sh

# Or run a TeachScript program
python demos/teachscript/run_teachscript.py demos/teachscript/examples/01_hello_world.teach

# Run the full test suite
python -m pytest tests/
```

**Read the full documentation**: [docs/teachscript/README_TEACHSCRIPT.md](docs/teachscript/README_TEACHSCRIPT.md)

**All examples verified and working** ✓

---

## Overview

CodeCraft empowers you to:
- **Create custom languages** - Design any language variant without compiler knowledge
- **Rename keywords** - Change language keywords (e.g., `if` → `cuando`) for any locale or style
- **Customize functions** - Define and modify built-in function libraries
- **Configure syntax** - Adjust array indexing, comments, operators, and more
- **Use templates** - Start from Python-like, JavaScript-like, Lisp-like, or minimal presets
- **Manage with CLI** - Powerful command-line tools for configuration creation and validation
- **Visual IDE** - CodeCraft IDE for interactive language design and testing
- **Professional IDE** - CodeEx for developing applications in your custom language

## Quick Start

### Easy Launch (Recommended)

The fastest way to get started—scripts handle all setup:

```bash
# Linux/macOS - Launch CodeCraft IDE
./run-codecraft.sh

# Linux/macOS - Launch CodeEx IDE
./run-codex.sh

# Windows - Launch CodeCraft IDE
run-codecraft.bat

# Windows - Launch CodeEx IDE
run-codex.bat
```

These scripts automatically:
- Create a Python virtual environment (`.venv`)
- Install all dependencies
- Verify required components (tkinter)
- Launch the application

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/James-HoneyBadger/CodeCraft.git
cd CodeCraft

# Install the package in development mode
pip install -e .

# Or install with development dependencies
pip install -e .[dev]
```

### Project Structure

```
CodeCraft/
├── src/
│   ├── hb_lcs/              # Core language construction framework
│   │   ├── language_config.py       # Configuration system
│   │   ├── language_runtime.py      # Runtime integration
│   │   ├── parser_generator.py      # Parser generation
│   │   ├── ide.py                   # CodeCraft IDE
│   │   ├── cli.py                   # CLI tools
│   │   ├── teachscript_*.py         # TeachScript integration
│   │   └── launch_ide.py            # IDE launcher
│   └── codex/               # CodeEx IDE components
│       ├── codex.py                 # CodeEx main application
│       ├── codex_gui.py             # GUI components
│       └── codex_components.py      # UI components
├── docs/                    # Comprehensive documentation
│   ├── guides/              # User guides and tutorials
│   ├── reference/           # Technical reference
│   ├── teachscript/         # TeachScript documentation
│   ├── codex/               # CodeEx documentation
│   └── summaries/           # Project summaries
├── configs/                 # Language configurations
│   ├── examples/            # Example configurations
│   └── teachscript.*        # TeachScript configuration
├── demos/                   # Example programs
│   ├── teachscript/         # TeachScript examples
│   └── demo_*.py            # Feature demonstrations
├── tests/                   # Comprehensive test suite
│   ├── integration/         # Integration tests
│   └── test_*.py            # Unit tests
├── run-codecraft.sh         # CodeCraft launcher (Linux/macOS)
├── run-codex.sh             # CodeEx launcher (Linux/macOS)
├── run-codecraft.bat        # CodeCraft launcher (Windows)
├── run-codex.bat            # CodeEx launcher (Windows)
└── README.md                # This file
```

## Using CodeCraft IDE

Launch the CodeCraft IDE for interactive language design:

```bash
# Using the launch script
./run-codecraft.sh              # Linux/macOS
run-codecraft.bat               # Windows

# Or manually
python -m hb_lcs.ide
```

**CodeCraft IDE Features:**
- Visual configuration editor for language design
- Syntax highlighting and code editor
- Real-time language testing and validation
- Multiple language presets to customize
- Configuration export/import
- Project management
- Version control integration

Learn more: [docs/guides/CODEX_DEVELOPER_GUIDE.md](docs/guides/CODEX_DEVELOPER_GUIDE.md)

## Using CodeEx IDE

Launch CodeEx for professional application development:

```bash
# Using the launch script
./run-codex.sh                  # Linux/macOS
run-codex.bat                   # Windows

# Or manually
python src/codex/codex.py
```

**CodeEx Features:**
- Load any CodeCraft-created language
- Professional multi-panel editor
- Real-time code execution
- Project organization and management
- Integrated console and debugging
- Code templates and snippets

Learn more: [docs/guides/CODEX_USER_GUIDE.md](docs/guides/CODEX_USER_GUIDE.md)

## Command-Line Tools

CodeCraft includes powerful CLI tools for language configuration:

```bash
# Create a new language configuration
codecraft create --preset python_like --output my_lang.yaml

# Validate a configuration
codecraft validate my_lang.yaml

# Edit a configuration
codecraft edit my_lang.yaml

# View configuration info
codecraft info my_lang.yaml

# Export configuration to different formats
codecraft export my_lang.yaml --format markdown
```

Learn more: [docs/reference/CLI_REFERENCE.md](docs/reference/CLI_REFERENCE.md)

## Python API

Use CodeCraft's Python API to programmatically create language configurations:

```python
from hb_lcs.language_config import LanguageConfig
from hb_lcs.language_runtime import LanguageRuntime

# Create a custom language configuration
config = LanguageConfig()

# Rename keywords for your language
config.rename_keyword("if", "cuando")          # Spanish conditional
config.rename_keyword("function", "func")      # Function keyword
config.rename_keyword("return", "devolver")    # Spanish return

# Customize syntax and semantics
config.set_array_indexing(0)                   # 0-based indexing
config.set_comment_style("#")                  # Python-style comments
config.set_string_delimiters('"', "'")         # Quote styles

# Add custom built-in functions
config.add_function("say", "output text")

# Save your configuration
config.save("my_language.yaml")

# Use it at runtime
runtime = LanguageRuntime(config)
result = runtime.execute("say 'Hello, World!'")
```

Learn more: [docs/reference/API_REFERENCE.md](docs/reference/API_REFERENCE.md)

## Example: Creating a Spanish-Like Language

```bash
# 1. Create configuration
./run-codecraft.sh

# 2. In CodeCraft IDE:
#    - Load preset: "python_like"
#    - Rename "if" → "si"
#    - Rename "else" → "sino"
#    - Rename "def" → "define"
#    - Save as "spanish.yaml"

# 3. Test in CodeEx:
./run-codex.sh

# 4. Load "spanish.yaml" and write code:
si True:
    define greet():
        say "¡Hola!"
    greet()
```

### Using Presets

```python
# Load from preset
config = LanguageConfig.from_preset("python_like")

# Customize further
config.rename_keyword("class", "blueprint")

# Save customized version
config.save("my_custom.yaml")
```

## CLI Tool

The CLI tool provides command-line access to all features:

### Create Configurations

```bash
# If installed with pip
hblcs create --preset python_like --output my_lang.yaml

# Or run directly
python src/hb_lcs/cli.py create --preset python_like --output my_lang.yaml

# Create interactively
hblcs create --interactive

# Create default
hblcs create --output default.json
```

### Validate and Inspect

```bash
# Validate configuration
hblcs validate my_lang.yaml

# Show detailed information
hblcs info my_lang.yaml

# List available presets
hblcs list-presets
```

### Modify Configurations

```bash
# Update metadata
hblcs update my_lang.yaml \
    --set metadata.author "Your Name" \
    --set metadata.version "2.0" \
    --output my_lang_v2.yaml

# Merge configurations
hblcs update base.yaml \
    --merge additions.yaml \
    --output merged.yaml

# Delete elements
hblcs delete my_lang.yaml \
    --keyword obsolete_keyword \
    --function deprecated_func \
    --output cleaned.yaml
```

### Compare and Convert

```bash
# Compare two configurations
hblcs diff config1.yaml config2.yaml

# Convert between formats
hblcs convert my_lang.yaml --to json
hblcs convert my_lang.json --to yaml

# Export documentation
hblcs export my_lang.yaml --format markdown
```

## Core Components

### 1. language_config.py

Core configuration system with dataclasses:

- `KeywordMapping` - Maps original keywords to custom names
- `FunctionConfig` - Configuration for built-in functions
- `OperatorConfig` - Operator precedence and associativity
- `ParsingConfig` - Deep syntax customization
- `SyntaxOptions` - General syntax options
- `LanguageConfig` - Main configuration container

**Key Methods:**

```python
# Keyword management
config.rename_keyword(original, custom)
config.add_keyword(original, custom, category)
config.delete_keyword(original)

# Function management
config.add_function(name, arity, description)
config.rename_function(original, custom)
config.remove_function(name)

# Syntax options
config.set_array_indexing(start_index, allow_fractional)
config.set_comment_style(single_line, multi_start, multi_end)
config.enable_feature(feature_name, enabled)

# Serialization
config.save(filepath, format="json"|"yaml")
config = LanguageConfig.load(filepath)

# Validation
errors = config.validate()

# CRUD operations
config.update(data, merge=True)
config.merge(other_config, prefer_other=True)
backup = config.clone()
```

### 2. language_runtime.py

Runtime system for applying configurations:

```python
from language_runtime import LanguageRuntime

# Load configuration
LanguageRuntime.load_config(config)
LanguageRuntime.load_config(config_file="my_lang.yaml")

# Query runtime state
original = LanguageRuntime.translate_keyword("custom_keyword")
start_idx = LanguageRuntime.get_array_start_index()
enabled = LanguageRuntime.is_feature_enabled("satirical")

# Get runtime info
info = LanguageRuntime.get_info()

# Reset to default
LanguageRuntime.reset()
```

### 3. langconfig.py

Command-line interface for all operations (see CLI Tool section above).

## Available Presets

The system includes several built-in presets:

### python_like
Python-style syntax with familiar keywords and 0-based indexing.

### js_like
JavaScript-style syntax with semicolons and function expressions.

### serious
Professional mode with satirical features disabled.

### minimal
Teaching mode with only essential keywords (6 keywords, 5 functions).

### spanish
Spanish keywords for education (si, mientras, función, etc.).

### french
French keywords (si, tantque, fonction, etc.).

## Configuration File Format

Configurations can be saved as JSON or YAML:

### JSON Example

```json
{
  "metadata": {
    "name": "My Language",
    "version": "1.0",
    "description": "A custom variant",
    "author": "Your Name"
  },
  "keywords": {
    "if": {
      "original": "if",
      "custom": "cuando",
      "category": "control_flow"
    }
  },
  "builtin_functions": {
    "print": {
      "name": "print",
      "arity": -1,
      "enabled": true,
      "description": "Output to console"
    }
  },
  "syntax_options": {
    "array_start_index": 0,
    "allow_fractional_indexing": false,
    "single_line_comment": "#",
    "statement_terminator": "!"
  }
}
```

### YAML Example

```yaml
metadata:
  name: My Language
  version: "1.0"
  description: A custom variant
  author: Your Name

keywords:
  if:
    original: if
    custom: cuando
    category: control_flow

builtin_functions:
  print:
    name: print
    arity: -1
    enabled: true
    description: Output to console

syntax_options:
  array_start_index: 0
  allow_fractional_indexing: false
  single_line_comment: "#"
  statement_terminator: "!"
```

## Advanced Features

### CRUD Operations

```python
# Delete keyword
config.delete_keyword("obsolete")

# Merge configurations
other = LanguageConfig.load("other.yaml")
config.merge(other, prefer_other=True)

# Clone for backup
backup = config.clone()

# Compare configurations
differences = config.diff(other)
```

### Deep Customization

```python
from language_config import ParsingConfig

config = LanguageConfig()

# Customize delimiters
config.parsing_config = ParsingConfig(
    block_start="(",
    block_end=")",
    list_start="[",
    list_end="]",
    parameter_separator=","
)
```

### Validation

```python
# Validate configuration
errors = config.validate()

if errors:
    print("Validation errors:")
    for error in errors:
        print(f"  • {error}")
else:
    print("✓ Configuration is valid")
```

## Demo Script

Run the demo to see all features in action:

```bash
python demo_language_construction.py
```

This will:
- Create sample configurations
- Demonstrate preset usage
- Show runtime integration
- Perform CRUD operations
- Validate configurations
- Save/load examples

## API Reference

### LanguageConfig Class

**Constructor:**
- `LanguageConfig(name, version, description, author)` - Create new config

**Keyword Methods:**
- `rename_keyword(original, custom)` - Rename a keyword
- `add_keyword(original, custom, category)` - Add new keyword
- `delete_keyword(original)` - Remove keyword

**Function Methods:**
- `add_function(name, arity, description)` - Add function
- `rename_function(original, custom)` - Rename function
- `remove_function(name)` - Remove function

**Syntax Methods:**
- `set_array_indexing(start, fractional)` - Configure arrays
- `set_comment_style(single, multi_start, multi_end)` - Configure comments
- `enable_feature(feature, enabled)` - Toggle features

**I/O Methods:**
- `save(filepath, format)` - Save to file
- `load(filepath)` - Load from file (class method)
- `from_preset(preset_name)` - Load preset (class method)
- `validate()` - Validate configuration
- `export_mapping_table(filepath)` - Export docs

**CRUD Methods:**
- `update(data, merge)` - Update configuration
- `merge(other, prefer_other)` - Merge configurations
- `clone()` - Create copy
- `diff(other)` - Compare configurations

### LanguageRuntime Class

**Configuration:**
- `load_config(config, config_file)` - Load configuration
- `get_config()` - Get current config
- `reset()` - Reset to default

**Query Methods:**
- `translate_keyword(custom)` - Get original keyword
- `is_keyword_enabled(original)` - Check if enabled
- `get_array_start_index()` - Get array start
- `is_fractional_indexing_enabled()` - Check fractional
- `is_feature_enabled(feature)` - Check feature
- `get_comment_syntax()` - Get comment style
- `should_enforce_semicolons()` - Check semicolons
- `get_info()` - Get runtime info

## Environment Variables

### LANGUAGE_CONFIG
Path to default configuration file:

```bash
export LANGUAGE_CONFIG=/path/to/my_config.yaml
```

### Auto-Loading

The system automatically loads configuration from:
1. `LANGUAGE_CONFIG` environment variable
2. `.langconfig` in current directory
3. `~/.langconfig` in home directory

## Best Practices

### Start with a Preset

```bash
python langconfig.py create --preset python_like --output my_lang.yaml
```

Then customize from there.

### Validate Early and Often

```bash
python langconfig.py validate my_lang.yaml
```

### Use Version Control

Keep your configurations in version control to track changes.

### Clone Before Major Changes

```python
backup = config.clone()
# Make risky changes
if something_wrong:
    config = backup
```

### Use Diff to Review Changes

```bash
python langconfig.py diff original.yaml modified.yaml
```

## Examples

See the generated demo files for examples:
- `demo_basic.json` - Basic configuration
- `demo_python_custom.yaml` - Customized preset
- `demo_config.json` / `demo_config.yaml` - Serialization examples

## Project Structure

```
HB_LCS/
├── language_config.py      # Core configuration system
├── language_runtime.py     # Runtime integration
├── langconfig.py           # CLI tool
├── demo_language_construction.py  # Demo script
└── README.md              # This file
```

## License

[Specify your license here]

## Contributing

[Add contribution guidelines if applicable]

## Support

For questions or issues, please [specify contact method].
