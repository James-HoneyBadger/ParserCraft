# Honey Badger Language Construction Set - User Guide

**Complete User Guide**  
Version 1.0 | November 2025

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Using the IDE](#using-the-ide)
4. [Command-Line Tools](#command-line-tools)
5. [Creating Configurations](#creating-configurations)
6. [Working with Presets](#working-with-presets)
7. [Common Tasks](#common-tasks)
8. [Troubleshooting](#troubleshooting)

---

## Introduction

### What is the Honey Badger Language Construction Set?

The Honey Badger Language Construction Set is a powerful toolkit for creating custom programming language variants. It allows you to:

- **Rename keywords** to match your preferred terminology
- **Customize syntax** for comments, operators, and indexing
- **Manage built-in functions** by adding, removing, or modifying them
- **Use presets** to start from familiar language templates
- **Create domain-specific languages** for education or specialized applications

### Who Should Use This?

- **Educators** creating simplified programming languages for teaching
- **Language designers** prototyping new language ideas
- **Developers** building domain-specific languages (DSLs)
- **Students** learning about programming language design
- **Researchers** studying language syntax and semantics

### System Requirements

- **Python 3.7+** (Python 3.8 or higher recommended)
- **Operating System**: Linux, macOS, or Windows
- **Optional**: PyYAML for YAML configuration support
- **GUI**: tkinter (usually included with Python)

---

## Getting Started

### Installation

1. **Extract or clone the project:**
   ```bash
   cd /path/to/HB_LCS
   ```

2. **Verify Python installation:**
   ```bash
   python3 --version
   ```

3. **Optional - Install YAML support:**
   ```bash
   pip install pyyaml
   # Or using system package manager:
   # Ubuntu/Debian: sudo apt install python3-yaml
   # Arch: sudo pacman -S python-yaml
   # macOS: brew install pyyaml
   ```

4. **Test the installation:**
   ```bash
   python3 demo_language_construction.py
   ```

### Quick Start (5 Minutes)

**Option 1: Using the IDE (Recommended for beginners)**

```bash
# Launch the graphical IDE
python3 ide.py
```

Then:
1. Click **Examples** → **Python-Like** to load a preset
2. View the configuration in the right panel
3. Edit code in the left panel
4. Explore the menus

**Option 2: Using the Command Line**

```bash
# Create a new configuration from a preset
python3 langconfig.py create --preset python_like my_language.yaml

# View the configuration
python3 langconfig.py info my_language.yaml

# Customize it
python3 langconfig.py edit my_language.yaml rename-keyword if cuando
```

**Option 3: Using Python API**

```python
from language_config import LanguageConfig

# Create a configuration
config = LanguageConfig.from_preset("python_like")

# Customize it
config.rename_keyword("if", "cuando")  # Spanish for "when"
config.rename_keyword("while", "mientras")  # Spanish for "while"

# Save it
config.save("spanish_python.yaml")
```

---

## Using the IDE

### Launching the IDE

```bash
# Method 1: Direct launch
python3 ide.py

# Method 2: Using launcher
python3 launch_ide.py

# Method 3: Make executable (Linux/macOS)
chmod +x ide.py
./ide.py
```

### IDE Interface Overview

```
┌─────────────────────────────────────────────────────────┐
│ File  Edit  Config  Examples  View  Help                │ Menu Bar
├─────────────────────────────────────────────────────────┤
│ [New] [Open] [Save] │ [Load Config] [Info]              │ Toolbar
├──────────────────────────────┬──────────────────────────┤
│                              │                          │
│  Code Editor                 │  Configuration Info      │
│  (with line numbers)         │  (read-only display)     │
│                              │                          │
│                              │                          │
│                              │                          │
├──────────────────────────────┴──────────────────────────┤
│ Ready                        │ Line 1, Col 1            │ Status Bar
└─────────────────────────────────────────────────────────┘
```

### Working with Files

**Create a New File:**
- Menu: `File` → `New`
- Keyboard: `Ctrl+N`
- Toolbar: Click **New**

**Open an Existing File:**
- Menu: `File` → `Open...`
- Keyboard: `Ctrl+O`
- Toolbar: Click **Open**

**Save Your Work:**
- Menu: `File` → `Save` (or `Save As...`)
- Keyboard: `Ctrl+S` (or `Ctrl+Shift+S` for Save As)
- Toolbar: Click **Save**

### Loading Language Configurations

**Method 1: Load from File**
1. Menu: `Config` → `Load Config...`
2. Keyboard: Press `F5`
3. Select a `.yaml` or `.json` file
4. View details in the right panel

**Method 2: Load from Examples**
- Menu: `Examples` → Select a preset
- Available: Python-Like, Minimal, Spanish

**Method 3: Toolbar**
- Click the **Load Config** button
- Navigate to configuration file

### Validating Configurations

To check if a configuration is valid:

1. Load the configuration (`F5`)
2. Menu: `Config` → `Validate Config`
3. See results in a popup dialog

✓ Valid configurations show "Configuration is valid!"  
✗ Invalid configurations list specific errors

### Using Editor Features

**Find Text:**
- `Ctrl+F` - Opens Find dialog
- Enter search text
- Click "Find Next"

**Replace Text:**
- `Ctrl+H` - Opens Replace dialog
- Enter find and replace text
- Click "Replace All"

**Go to Specific Line:**
- `Ctrl+L` - Opens Go to Line dialog
- Enter line number
- Jumps to that line

**Toggle Word Wrap:**
- Menu: `Edit` → Check/uncheck `Word Wrap`
- Wraps long lines for easier reading

**Toggle Line Numbers:**
- Menu: `View` → Check/uncheck `Show Line Numbers`
- Shows/hides line number gutter

### Customizing the IDE

**Change Theme:**
1. Menu: `View` → `Theme` → Select `Light` or `Dark`
2. Or use Preferences dialog

**Adjust Font Sizes:**
1. Menu: `Edit` → `Preferences...`
2. Adjust "Editor font size" (8-32)
3. Adjust "Console font size" (8-32)
4. Click "Save"

**Preferences Dialog Options:**
- **Theme**: Light or Dark
- **Editor font size**: Size of code editor text
- **Console font size**: Size of configuration display

### Keyboard Shortcuts Reference

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New file |
| `Ctrl+O` | Open file |
| `Ctrl+S` | Save file |
| `Ctrl+Shift+S` | Save As |
| `F5` | Load configuration |
| `Ctrl+F` | Find |
| `Ctrl+H` | Replace |
| `Ctrl+L` | Go to Line |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |
| `Ctrl+X` | Cut |
| `Ctrl+C` | Copy |
| `Ctrl+V` | Paste |
| `Ctrl+A` | Select All |

---

## Command-Line Tools

### Overview of langconfig.py

The `langconfig.py` tool provides 10 commands for managing language configurations:

```bash
python3 langconfig.py <command> [options] <config-file>
```

### Available Commands

1. `create` - Create new configuration
2. `edit` - Modify existing configuration
3. `validate` - Check configuration validity
4. `info` - Display configuration details
5. `export` - Export to different format
6. `list-presets` - Show available presets
7. `convert` - Convert between JSON/YAML
8. `diff` - Compare two configurations
9. `update` - Batch update configurations
10. `delete` - Remove configuration files

### Creating Configurations

**From Scratch:**
```bash
python3 langconfig.py create my_language.yaml
```

**From Preset:**
```bash
python3 langconfig.py create --preset python_like my_language.yaml
python3 langconfig.py create --preset minimal teaching_mode.json
python3 langconfig.py create --preset javascript_like web_lang.yaml
```

**Available Presets:**
- `python_like` - Python-style syntax
- `javascript_like` - JavaScript-style syntax
- `minimal` - Bare minimum features
- `teaching_mode` - Simplified for education

### Editing Configurations

**Rename a Keyword:**
```bash
python3 langconfig.py edit my_language.yaml rename-keyword if cuando
python3 langconfig.py edit my_language.yaml rename-keyword while mientras
```

**Add a Function:**
```bash
# Syntax: add-function <original> <custom> <min_args> <max_args>
python3 langconfig.py edit my_language.yaml add-function sqrt raiz 1 1
python3 langconfig.py edit my_language.yaml add-function print imprimir 0 -1
```

**Remove a Function:**
```bash
python3 langconfig.py edit my_language.yaml remove-function eval
```

**Set Array Indexing:**
```bash
# 0-based indexing
python3 langconfig.py edit my_language.yaml set-indexing 0

# 1-based indexing
python3 langconfig.py edit my_language.yaml set-indexing 1
```

**Set Comment Style:**
```bash
python3 langconfig.py edit my_language.yaml set-comment "#"
python3 langconfig.py edit my_language.yaml set-comment "//"
python3 langconfig.py edit my_language.yaml set-comment "--"
```

### Viewing Information

**Display Full Configuration:**
```bash
python3 langconfig.py info my_language.yaml
```

**Validate Configuration:**
```bash
python3 langconfig.py validate my_language.yaml
```

**List Available Presets:**
```bash
python3 langconfig.py list-presets
```

### Converting Formats

**Convert YAML to JSON:**
```bash
python3 langconfig.py convert my_language.yaml my_language.json
```

**Convert JSON to YAML:**
```bash
python3 langconfig.py convert my_language.json my_language.yaml
```

### Comparing Configurations

**Show Differences:**
```bash
python3 langconfig.py diff config1.yaml config2.yaml
```

Output shows:
- Keywords only in first config
- Keywords only in second config
- Keywords with different mappings
- Function differences

### Batch Operations

**Update Multiple Configurations:**
```bash
python3 langconfig.py update '*.yaml' rename-keyword if cuando
```

**Delete Configurations:**
```bash
python3 langconfig.py delete old_config.yaml
```

---

## Creating Configurations

### Understanding Configuration Structure

A language configuration consists of:

1. **Metadata**: Name, version, description
2. **Keywords**: Original → Custom mappings
3. **Functions**: Built-in function definitions
4. **Operators**: Operator symbols and precedence
5. **Parsing**: Comment styles, string delimiters
6. **Syntax**: Array indexing, statement separators

### Step-by-Step: Create a Spanish Language Variant

**Step 1: Start from a preset**
```python
from language_config import LanguageConfig

config = LanguageConfig.from_preset("python_like")
config.name = "Spanish Python"
config.version = "1.0"
```

**Step 2: Rename control flow keywords**
```python
config.rename_keyword("if", "si")
config.rename_keyword("else", "sino")
config.rename_keyword("elif", "sinoSi")
config.rename_keyword("while", "mientras")
config.rename_keyword("for", "para")
```

**Step 3: Rename function keywords**
```python
config.rename_keyword("function", "funcion")
config.rename_keyword("return", "retornar")
config.rename_keyword("class", "clase")
```

**Step 4: Rename built-in functions**
```python
config.add_function("print", "imprimir", max_args=-1)
config.add_function("input", "entrada", max_args=1)
config.add_function("len", "longitud", min_args=1, max_args=1)
```

**Step 5: Validate and save**
```python
errors = config.validate()
if not errors:
    config.save("spanish_python.yaml")
    print("✓ Configuration created successfully!")
else:
    print("Errors:", errors)
```

### Configuration Best Practices

**DO:**
- ✓ Use descriptive names for your language
- ✓ Keep keyword names consistent with your theme
- ✓ Validate before saving
- ✓ Document your configuration choices
- ✓ Test with example code

**DON'T:**
- ✗ Mix different language styles inconsistently
- ✗ Use special characters in keyword names
- ✗ Forget to specify min/max args for functions
- ✗ Create circular keyword mappings

---

## Working with Presets

### Available Presets

**python_like** - Python-style syntax
- Keywords: `def`, `class`, `if`, `elif`, `else`, `while`, `for`
- Functions: `print`, `len`, `range`, `input`, `int`, `str`, `float`
- Comment: `#`
- Indexing: 0-based

**javascript_like** - JavaScript-style syntax
- Keywords: `function`, `class`, `if`, `else`, `while`, `for`
- Functions: `console.log`, `parseInt`, `parseFloat`
- Comment: `//`
- Indexing: 0-based

**minimal** - Bare minimum
- Essential keywords only
- Basic functions
- Simplified syntax

**teaching_mode** - Educational
- Clear, verbose keyword names
- Limited feature set
- Beginner-friendly

### Loading Presets

**In Python:**
```python
from language_config import LanguageConfig

config = LanguageConfig.from_preset("python_like")
```

**Via CLI:**
```bash
python3 langconfig.py create --preset python_like my_config.yaml
```

**In IDE:**
- Menu: `Examples` → Select preset

### Customizing Presets

Start from a preset and modify:

```python
# Load preset
config = LanguageConfig.from_preset("python_like")

# Customize
config.name = "My Custom Language"
config.rename_keyword("function", "procedure")
config.set_comment_style("//")

# Save as new configuration
config.save("my_custom.yaml")
```

---

## Common Tasks

### Task 1: Create a Teaching Language for Kids

```python
from language_config import LanguageConfig

# Start with teaching mode preset
config = LanguageConfig.from_preset("teaching_mode")

# Use very clear English keywords
config.rename_keyword("if", "when")
config.rename_keyword("while", "repeat_while")
config.rename_keyword("function", "make_function")
config.rename_keyword("return", "give_back")

# Simple, clear function names
config.add_function("print", "say", max_args=-1)
config.add_function("input", "ask", max_args=1)
config.add_function("len", "count", min_args=1, max_args=1)

# Save
config.save("kids_language.yaml")
```

### Task 2: Create a Non-English Language

```python
# German language variant
config = LanguageConfig.from_preset("python_like")

config.rename_keyword("if", "wenn")
config.rename_keyword("else", "sonst")
config.rename_keyword("while", "während")
config.rename_keyword("for", "für")
config.rename_keyword("function", "funktion")

config.save("german_python.yaml")
```

### Task 3: Validate Multiple Configurations

```bash
# Validate all YAML files
for file in examples/*.yaml; do
    echo "Validating $file..."
    python3 langconfig.py validate "$file"
done
```

### Task 4: Convert All Configs to JSON

```bash
# Convert all YAML to JSON
for file in *.yaml; do
    json_file="${file%.yaml}.json"
    python3 langconfig.py convert "$file" "$json_file"
done
```

### Task 5: Compare Your Config with Python

```bash
python3 langconfig.py diff my_language.yaml examples/python_like.yaml
```

---

## Troubleshooting

### Common Issues and Solutions

**Issue: "YAML support not available"**
```
Solution: Install PyYAML
  pip install pyyaml
  # Or use system package manager
```

**Issue: "Keyword 'xyz' not found"**
```
Solution: Check the original keyword exists
  python3 langconfig.py info your_config.yaml
  # View all available keywords
```

**Issue: IDE won't start**
```
Solution: Verify tkinter is installed
  python3 -m tkinter
  # Should open a test window
  
  If missing on Ubuntu/Debian:
    sudo apt install python3-tk
```

**Issue: Configuration won't load**
```
Solution: Validate the configuration
  python3 langconfig.py validate your_config.yaml
  # Shows specific errors
```

**Issue: Changes not saving**
```
Solution: Check file permissions
  ls -l your_config.yaml
  chmod 644 your_config.yaml
```

### Getting Help

**View Command Help:**
```bash
python3 langconfig.py --help
python3 langconfig.py create --help
python3 langconfig.py edit --help
```

**Check Version:**
```bash
python3 langconfig.py --version
```

**IDE Help:**
- Menu: `Help` → `About`
- Shows version and feature information

### Error Messages

**"Configuration validation failed"**
- Run `validate` command to see specific errors
- Common causes: Missing required fields, invalid values

**"Function 'xyz' already exists"**
- Use different name or remove existing function first
- Use `remove-function` before `add-function`

**"Invalid array index base"**
- Must be 0 or 1
- Use `set-indexing 0` or `set-indexing 1`

### Best Practices for Stability

1. **Always validate** before using a configuration
2. **Keep backups** of working configurations
3. **Use version control** (git) for configuration files
4. **Test incrementally** - make small changes and test
5. **Document changes** in configuration descriptions

---

## Appendix A: File Locations

**Configuration Storage:**
- User configs: Anywhere you choose
- Examples: `examples/` directory
- IDE settings: `~/.hb_lcs/settings.json`

**Project Structure:**
```
HB_LCS/
├── language_config.py      # Core library
├── language_runtime.py     # Runtime system
├── langconfig.py          # CLI tool
├── ide.py                 # GUI application
├── launch_ide.py          # IDE launcher
├── examples/              # Sample configurations
│   ├── python_like.yaml
│   ├── minimal.json
│   └── spanish.yaml
└── docs/                  # Documentation
```

## Appendix B: Keyboard Shortcuts Quick Reference

**File Operations:**
- `Ctrl+N` - New
- `Ctrl+O` - Open
- `Ctrl+S` - Save
- `Ctrl+Shift+S` - Save As

**Editing:**
- `Ctrl+Z` - Undo
- `Ctrl+Y` - Redo
- `Ctrl+X/C/V` - Cut/Copy/Paste
- `Ctrl+A` - Select All

**Search:**
- `Ctrl+F` - Find
- `Ctrl+H` - Replace
- `Ctrl+L` - Go to Line

**Configuration:**
- `F5` - Load Config

## Appendix C: Example Workflows

**Workflow 1: Quick Language Variant**
1. Launch IDE (`python3 ide.py`)
2. Load preset (`Examples` → `Python-Like`)
3. Note desired changes
4. Use CLI to customize
5. Reload in IDE to verify

**Workflow 2: Iterative Development**
1. Create from preset
2. Make small change
3. Validate
4. Test with example code
5. Repeat steps 2-4

**Workflow 3: Team Collaboration**
1. Share configuration files via git
2. Each team member validates locally
3. Use `diff` to review changes
4. Merge approved configurations

---

## Quick Reference Card

**Most Used Commands:**
```bash
# Create new config from preset
python3 langconfig.py create --preset python_like myconfig.yaml

# Rename a keyword
python3 langconfig.py edit myconfig.yaml rename-keyword if cuando

# Validate configuration
python3 langconfig.py validate myconfig.yaml

# View configuration
python3 langconfig.py info myconfig.yaml

# Launch IDE
python3 ide.py
```

**Most Used Python API:**
```python
from language_config import LanguageConfig

# Load/Create
config = LanguageConfig.from_preset("python_like")

# Modify
config.rename_keyword("if", "cuando")
config.add_function("sqrt", "raiz", 1, 1)

# Save
config.save("myconfig.yaml")
```

---

**End of User Guide**

For technical details, see the [Technical Reference Manual](TECHNICAL_REFERENCE.md).  
For language development, see the [Programming Language Development Guide](LANGUAGE_DEVELOPMENT_GUIDE.md).
