# Honey Badger Language Construction Set

A comprehensive system for creating custom programming language variants through configuration files, with a graphical IDE for editing and testing.

## 🎯 **PROOF OF CONCEPT: TeachScript**

**See a complete, working custom language built with HB_LCS!**

**TeachScript** is a beginner-friendly educational programming language with custom syntax:
- `when` instead of `if`
- `teach` instead of `def`
- `say()` instead of `print()`
- And much more!

**Try it now**:
```bash
python3 run_teachscript.py teachscript_examples/01_hello_world.teach
python3 test_teachscript.py  # Run all tests
```

**Read the complete manual**: [TEACHSCRIPT_MANUAL.md](TEACHSCRIPT_MANUAL.md)

**All 7 example programs verified working** ✓

---

## Overview

The Language Construction Set allows you to:
- **Rename keywords** - Change language keywords (e.g., `if` → `cuando`)
- **Customize functions** - Add, remove, or modify built-in functions
- **Configure syntax** - Adjust array indexing, comments, operators
- **Use presets** - Start from Python-like, JavaScript-like, or minimal templates
- **Manage configurations** - CLI tools for creating and validating configs
- **Graphical IDE** - Edit code and load configurations visually

## Quick Start

### Installation

```bash
# Clone or extract this project
cd HB_LCS

# Optional: Install YAML support
pip install pyyaml
```

### Using the IDE

Launch the graphical IDE:

```bash
python3 ide.py
```

Features:
- Load and test language configurations
- Syntax highlighting and line numbers
- Configuration validation
- Light/Dark themes
- Built-in examples

See [IDE_README.md](IDE_README.md) for detailed IDE documentation.

### Basic Usage (Python API)

```python
from language_config import LanguageConfig

# Create a custom configuration
config = LanguageConfig()

# Rename keywords
config.rename_keyword("if", "cuando")  # Spanish-style
config.rename_keyword("function", "def")  # Python-style

# Customize syntax
config.set_array_indexing(0, False)  # 0-based indexing
config.set_comment_style("#")  # Python-style comments

# Save configuration
config.save("my_language.yaml")
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

The `langconfig.py` tool provides command-line access to all features:

### Create Configurations

```bash
# Create from preset
python langconfig.py create --preset python_like --output my_lang.yaml

# Create interactively
python langconfig.py create --interactive

# Create default
python langconfig.py create --output default.json
```

### Validate and Inspect

```bash
# Validate configuration
python langconfig.py validate my_lang.yaml

# Show detailed information
python langconfig.py info my_lang.yaml

# List available presets
python langconfig.py list-presets
```

### Modify Configurations

```bash
# Update metadata
python langconfig.py update my_lang.yaml \
    --set metadata.author "Your Name" \
    --set metadata.version "2.0" \
    --output my_lang_v2.yaml

# Merge configurations
python langconfig.py update base.yaml \
    --merge additions.yaml \
    --output merged.yaml

# Delete elements
python langconfig.py delete my_lang.yaml \
    --keyword obsolete_keyword \
    --function deprecated_func \
    --output cleaned.yaml
```

### Compare and Convert

```bash
# Compare two configurations
python langconfig.py diff config1.yaml config2.yaml

# Convert between formats
python langconfig.py convert my_lang.yaml --to json
python langconfig.py convert my_lang.json --to yaml

# Export documentation
python langconfig.py export my_lang.yaml --format markdown
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
