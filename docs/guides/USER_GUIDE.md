# User Guide

**Honey Badger Language Construction Set v4.0**  
Complete User Manual & How-To Guide  
December 3, 2025

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Using the Graphical IDE](#using-the-graphical-ide)
4. [Using the Command-Line Tool](#using-the-command-line-tool)
5. [Creating Custom Languages](#creating-custom-languages)
6. [Working with Presets](#working-with-presets)
7. [Common Tasks](#common-tasks)
8. [Advanced Features](#advanced-features)
9. [Troubleshooting](#troubleshooting)
10. [Tips & Tricks](#tips--tricks)

---

## Introduction

### What is HB Language Construction Set?

The **Honey Badger Language Construction Set** is a toolkit for creating custom programming language variants. It lets you:

- **Rename keywords** (`if` → `cuando`, `function` → `def`)
- **Customize syntax** (comment style, operators, indexing)
- **Add/remove functions** (enable/disable built-ins)
- **Use presets** (Python-like, JavaScript-like, minimal)
- **Edit visually** (graphical IDE)
- **Use command-line** (batch operations)
- **Deploy** (web, mobile, cloud)

### Who Should Use This?

✅ **Educators** - Teach programming in native language  
✅ **Language designers** - Prototype language ideas  
✅ **Researchers** - Study language syntax  
✅ **Developers** - Create domain-specific languages  
✅ **Students** - Learn language design  

### System Requirements

- **Python 3.8+** (3.10+ recommended)
- **Operating System**: Windows, macOS, or Linux
- **GUI library**: Tkinter (usually included)
- **Optional**: PyYAML for YAML support

---

## Getting Started

### Installation (2 minutes)

```bash
# 1. Get the code
git clone https://github.com/James-HoneyBadger/HB_Language_Construction.git
cd HB_Language_Construction

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# 3. Install
pip install -e .

# 4. Verify
hblcs --help

# 5. Launch IDE
hblcs-ide
```

See [INSTALL_GUIDE.md](INSTALL_GUIDE.md) for detailed installation help.

### Your First Language (5 minutes)

```bash
# Create a Spanish-style language
hblcs create --preset python_like --output spanish.yaml

# Edit it (opens in your editor)
hblcs update spanish.yaml \
    --set keywords.if.custom=si \
    --set keywords.while.custom=mientras \
    --output spanish.yaml

# Validate it
hblcs validate spanish.yaml

# View it
hblcs info spanish.yaml
```

### Your First IDE Session (10 minutes)

1. **Launch IDE**: `hblcs-ide`
2. **Menu → File → Load Configuration** → Select preset
3. **Menu → Edit → Editor Font Size** → Adjust as needed
4. **Type code** in the editor using custom keywords
5. **Menu → Tools → Syntax Check** → Verify code
6. **Menu → File → Save Configuration** → Save your changes

---

## Using the Graphical IDE

### Starting the IDE

```bash
# Standard launch
hblcs-ide

# Or from source
python src/hb_lcs/launch_ide.py
```

The IDE window shows:

```
┌─────────────────────────────────────────────────────┐
│ Menu Bar (File, Edit, Language, Tools, Help)        │
├─────────────────────────────────────────────────────┤
│ Toolbar (Quick buttons)                             │
├──────────────────┬──────────────────────────────────┤
│  Config Panel    │     Editor Panel                 │
│  (Keywords,      │     (Code editor)                │
│   Functions)     │     (Line numbers)               │
├──────────────────┼──────────────────────────────────┤
│  Configuration   │     Console/Output               │
│  Details         │     (Execution results)          │
├──────────────────┴──────────────────────────────────┤
│ Status Bar (File info, language, line count)        │
└─────────────────────────────────────────────────────┘
```

### Main Menu Options

#### File Menu

| Option | Keyboard | Action |
|--------|----------|--------|
| New | Ctrl+N | Create new file |
| Open | Ctrl+O | Open code file |
| Save | Ctrl+S | Save current file |
| Save As | Ctrl+Shift+S | Save with new name |
| Load Language Config | Ctrl+L | Load language definition |
| Save Language Config | Ctrl+Alt+S | Save language definition |
| Import Config | - | Import configuration |
| Export Config | - | Export as JSON/YAML |
| Recent Files | - | Open recently used file |
| Exit | Alt+F4 | Close IDE |

#### Edit Menu

| Option | Keyboard | Action |
|--------|----------|--------|
| Undo | Ctrl+Z | Undo last change |
| Redo | Ctrl+Y | Redo last change |
| Cut | Ctrl+X | Cut selection |
| Copy | Ctrl+C | Copy selection |
| Paste | Ctrl+V | Paste clipboard |
| Select All | Ctrl+A | Select all text |
| Find | Ctrl+F | Find in text |
| Replace | Ctrl+H | Find and replace |
| Preferences | - | IDE settings |

#### Language Menu

| Option | Action |
|--------|--------|
| Python-Like | Load Python preset |
| JavaScript-Like | Load JavaScript preset |
| Minimal | Load minimal preset |
| Spanish | Load Spanish preset |
| Custom... | Load custom config |

#### Tools Menu

| Option | Action |
|--------|--------|
| Run Code | Execute code in editor |
| Syntax Check | Validate code syntax |
| Validate Config | Validate language definition |
| Generate Template | AI code template suggestion |
| Lint Code | Check code style |
| Test Code | Run code tests |

#### Help Menu

| Option | Action |
|--------|--------|
| User Guide | Open this guide |
| Keyboard Shortcuts | Show keyboard shortcuts |
| About | About dialog |

### Editor Features

#### Syntax Highlighting

Different colors for:
- **Keywords** (orange)
- **Strings** (green)
- **Numbers** (blue)
- **Comments** (gray)
- **Functions** (purple)

Toggle: **Edit → Preferences → Syntax Highlighting**

#### Line Numbers

Shows line numbers on left side.

Toggle: **Edit → Preferences → Show Line Numbers**

#### Text Wrapping

Wrap long lines.

Toggle: **View → Word Wrap**

#### Code Completion

Auto-complete keywords and function names.

Toggle: **Edit → Preferences → Code Completion**

### Configuration Panel

Left side shows language configuration:

**Keywords Section**
- Lists all available keywords
- Shows original → custom mapping
- Click to edit mapping

**Functions Section**
- Lists all available functions
- Shows function arity (argument count)
- Click to enable/disable

**Syntax Options Section**
- Array indexing (0-based or 1-based)
- Comment style
- Operator precedence

### Running Code

1. **Write code** in the editor using custom keywords
2. **Click "Run"** button or press Ctrl+Enter
3. **See output** in the console panel
4. **Check errors** in the error panel

Example:

```python
# Using Python-like preset
x = 10
if x > 5:
    print("x is big!")
```

Example with Spanish preset:

```python
# Using Spanish preset
x = 10
si x > 5:
    print("¡x es grande!")
```

### Saving Your Work

#### Save Code

```
File → Save (Ctrl+S)
```

Saves the code file (`.py` by default).

#### Save Configuration

```
File → Save Language Config (Ctrl+Alt+S)
```

Saves the language definition (`.json` or `.yaml`).

### IDE Preferences

**Access**: Edit → Preferences

Options include:

| Setting | Options | Default |
|---------|---------|---------|
| Theme | Light/Dark | Light |
| Editor Font Size | 8-20 | 11 |
| Console Font Size | 8-16 | 10 |
| Show Line Numbers | On/Off | On |
| Show Minimap | On/Off | Off |
| Auto-Save | On/Off | Off |
| Syntax Highlighting | On/Off | On |
| Code Completion | On/Off | On |

---

## Using the Command-Line Tool

### Basic Commands

#### Get Help

```bash
# Show general help
hblcs --help

# Show specific command help
hblcs create --help

# Show version
hblcs --version

# List commands
hblcs list-commands
```

#### List Available Presets

```bash
hblcs list-presets

# Output:
# Available presets:
# - python_like (Python-style syntax)
# - javascript_like (JavaScript-style syntax)
# - minimal (Teaching mode with 6 keywords)
# - spanish (Spanish keywords)
# - french (French keywords)
```

### Creating Configurations

#### From Preset

```bash
# Create from preset
hblcs create --preset python_like --output my_lang.yaml

# Available presets:
# - python_like
# - javascript_like
# - minimal
# - spanish
# - french
```

#### Interactive Mode

```bash
# Step-by-step guided creation
hblcs create --interactive

# Prompts you for:
# 1. Language name
# 2. Version
# 3. Author
# 4. Base preset
# 5. Keywords to customize
# 6. Functions to include
```

#### Default

```bash
# Create minimal configuration
hblcs create --output basic.json
```

### Validating Configurations

```bash
# Check for errors
hblcs validate my_lang.yaml

# Output (if valid):
# ✓ Configuration is valid

# Output (if invalid):
# ✗ Configuration has errors:
#   - Error 1
#   - Error 2
```

### Inspecting Configurations

```bash
# Show detailed information
hblcs info my_lang.yaml

# Output example:
# Language: My Language v1.0
# Author: Your Name
# Keywords: 30
# Functions: 15
# Array indexing: 0-based
# Comment style: #
```

### Modifying Configurations

#### Set Values

```bash
# Change single value
hblcs update my_lang.yaml \
    --set metadata.author "New Author" \
    --output my_lang_updated.yaml

# Set multiple values
hblcs update my_lang.yaml \
    --set metadata.version "2.0" \
    --set metadata.author "Author Name" \
    --output my_lang_updated.yaml

# Change keyword mapping
hblcs update my_lang.yaml \
    --set keywords.if.custom "cuando" \
    --output my_lang_updated.yaml
```

#### Merge Configurations

```bash
# Combine two configurations
hblcs update base.yaml \
    --merge additions.yaml \
    --output merged.yaml
```

#### Delete Elements

```bash
# Remove keyword
hblcs delete my_lang.yaml \
    --keyword deprecated_kw \
    --output cleaned.yaml

# Remove function
hblcs delete my_lang.yaml \
    --function unused_func \
    --output cleaned.yaml

# Remove multiple items
hblcs delete my_lang.yaml \
    --keyword kw1 \
    --keyword kw2 \
    --function func1 \
    --output cleaned.yaml
```

### Converting Formats

#### JSON ↔ YAML

```bash
# Convert JSON to YAML
hblcs convert config.json --to yaml --output config.yaml

# Convert YAML to JSON
hblcs convert config.yaml --to json --output config.json
```

#### Comparing Configurations

```bash
# Show differences between two configs
hblcs diff config1.yaml config2.yaml

# Output:
# Differences between config1.yaml and config2.yaml:
# Keywords:
#   - if: cuando → si
# Functions:
#   - print added
#   - deprecated_func removed
```

#### Exporting Documentation

```bash
# Export as markdown
hblcs export config.yaml --format markdown --output config.md

# Export as HTML
hblcs export config.yaml --format html --output config.html
```

---

## Creating Custom Languages

### Basic Workflow

```
1. Create base from preset
2. Customize keywords
3. Customize functions
4. Adjust syntax options
5. Test & validate
6. Save & use
```

### Example 1: Educational Language

**Goal**: Create a simplified language for beginners

```bash
# 1. Start with minimal preset
hblcs create --preset minimal --output beginner.yaml

# 2. Customize keywords (make them simpler)
hblcs update beginner.yaml \
    --set keywords.if.custom=check \
    --set keywords.while.custom=repeat \
    --output beginner.yaml

# 3. Validate
hblcs validate beginner.yaml

# 4. Use in IDE
hblcs-ide
# File → Load Configuration → beginner.yaml
```

Result:
```python
# Simplified beginner syntax
x = 5
check x > 0:
    print("x is positive")

repeat i in range(3):
    print("Count:", i)
```

### Example 2: Spanish Language

**Goal**: Create Spanish keyword language

```bash
# 1. Start with Python preset
hblcs create --preset python_like --output spanish.yaml

# 2. Rename keywords to Spanish
hblcs update spanish.yaml \
    --set keywords.if.custom=si \
    --set keywords.while.custom=mientras \
    --set keywords.for.custom=para \
    --set keywords.function.custom=función \
    --set keywords.return.custom=regresa \
    --set keywords.class.custom=clase \
    --output spanish.yaml

# 3. Rename functions to Spanish
hblcs update spanish.yaml \
    --set builtin_functions.print.name=escribir \
    --output spanish.yaml

# 4. Validate
hblcs validate spanish.yaml

# 5. Use
hblcs-ide
```

Result:
```python
# Spanish syntax
x = 10
si x > 5:
    escribir("x es grande")

para i en rango(3):
    escribir(i)

función saludar(nombre):
    escribir("Hola, " + nombre)

saludar("mundo")
```

### Example 3: Domain-Specific Language

**Goal**: Create a language for data processing

```bash
# 1. Start minimal
hblcs create --preset minimal --output data_lang.yaml

# 2. Customize for data processing
hblcs update data_lang.yaml \
    --set keywords.if.custom=filter \
    --set keywords.for.custom=transform \
    --set keywords.function.custom=operation \
    --output data_lang.yaml

# 3. Add data-specific functions
# (Manual edit needed for full customization)
nano data_lang.yaml

# Add to builtin_functions:
# "sum": { "name": "sum", "arity": -1 }
# "avg": { "name": "avg", "arity": -1 }
# "max": { "name": "max", "arity": -1 }
# "min": { "name": "min", "arity": -1 }

# 4. Validate & use
hblcs validate data_lang.yaml
hblcs-ide
```

Result:
```python
# Data processing syntax
data = [1, 2, 3, 4, 5]

total = sum(data)
average = avg(data)
maximum = max(data)

transform value in data:
    if value > 2:
        print(value)
```

---

## Working with Presets

### Available Presets

#### python_like
Python-style syntax, familiar to Python developers.

```python
# Keywords
if, while, for, def, return, class, import, from, import

# Comment style: #
# Statement end: newline
# Array indexing: 0-based

x = 5
if x > 0:
    print("positive")
```

#### javascript_like
JavaScript-style syntax, familiar to JavaScript developers.

```python
# Keywords
if, while, for, function, return, class, const, let, var

# Comment style: //
# Statement end: semicolon (optional)
# Array indexing: 0-based

let x = 5;
if (x > 0) {
    console.log("positive");
}
```

#### minimal
Teaching mode with only 6 essential keywords.

```python
# Keywords: if, while, function, return, and, or

# Perfect for beginners
x = 5
if x > 0:
    print("positive")
```

#### spanish
Spanish language keywords.

```python
# Keywords in Spanish
si, mientras, para, función, regresa, clase

x = 5
si x > 0:
    print("positivo")
```

#### french
French language keywords.

```python
# Keywords in French
si, tandis, pour, fonction, retour, classe

x = 5
si x > 0:
    afficher("positif")
```

### Loading a Preset

#### In CLI

```bash
hblcs create --preset python_like --output my_lang.yaml
```

#### In IDE

1. **File → Load Configuration**
2. **Select preset** from list
3. Or **Browse** for custom config file

#### In Python

```python
from hb_lcs.language_config import LanguageConfig

config = LanguageConfig.from_preset("python_like")
```

### Customizing a Preset

```bash
# 1. Load preset
hblcs create --preset python_like --output custom.yaml

# 2. Customize it
hblcs update custom.yaml \
    --set keywords.if.custom=cuando \
    --output custom.yaml

# 3. Use it
hblcs-ide
# File → Load Configuration → custom.yaml
```

---

## Common Tasks

### Task 1: Rename a Single Keyword

**Goal**: Change `if` to `when`

```bash
hblcs update my_lang.yaml \
    --set keywords.if.custom=when \
    --output my_lang.yaml
```

### Task 2: Add Comments to Your Language

**Goal**: Use `//` for comments

```bash
hblcs update my_lang.yaml \
    --set syntax_options.single_line_comment="//" \
    --output my_lang.yaml
```

### Task 3: Make Language Use 1-Based Indexing

**Goal**: Make arrays start at 1 instead of 0

```bash
hblcs update my_lang.yaml \
    --set syntax_options.array_start_index=1 \
    --output my_lang.yaml
```

In code:
```python
arr = [10, 20, 30]
print(arr[1])  # Prints 10 (first element)
```

### Task 4: Disable Semicolons

**Goal**: Make semicolons optional

```bash
hblcs update my_lang.yaml \
    --set syntax_options.require_semicolons=false \
    --output my_lang.yaml
```

### Task 5: Compare Two Languages

**Goal**: See what's different between two configs

```bash
hblcs diff language1.yaml language2.yaml
```

### Task 6: Backup Your Language

**Goal**: Create a copy before major changes

```bash
# Backup
cp my_lang.yaml my_lang.backup.yaml

# Make changes
hblcs update my_lang.yaml --set ...

# If something goes wrong, restore
cp my_lang.backup.yaml my_lang.yaml
```

### Task 7: Export Language Documentation

**Goal**: Create user documentation for your language

```bash
# Export as markdown
hblcs export my_lang.yaml --format markdown --output my_lang.md

# Export as HTML
hblcs export my_lang.yaml --format html --output my_lang.html
```

### Task 8: Share Your Language

**Goal**: Share config with others

```bash
# Convert to JSON for better compatibility
hblcs convert my_lang.yaml --to json --output my_lang.json

# Share the file
# Recipients can use it with:
hblcs validate my_lang.json
hblcs info my_lang.json

# Or in IDE
hblcs-ide
# File → Load Configuration → my_lang.json
```

---

## Advanced Features

### Feature: Code Completion

Auto-complete suggestions for keywords and functions.

Toggle: **Edit → Preferences → Code Completion**

Usage:
1. Start typing keyword
2. See suggestions
3. Press Tab to complete
4. Or press Escape to cancel

### Feature: Real-Time Validation

Check code syntax as you type.

Toggle: **Tools → Real-time Validation**

Shows:
- ✓ Green line = valid
- ✗ Red line = error
- ⚠ Yellow line = warning

### Feature: Live Preview

See code output in real-time.

Toggle: **View → Live Preview**

Updates output every time you run code.

### Feature: Search & Replace

Find and replace text in editor.

```
Keyboard: Ctrl+H
Or: Edit → Find and Replace
```

Features:
- Regular expression support
- Case-sensitive/insensitive
- Whole word matching
- Replace one/all

### Feature: Syntax Themes

Change editor appearance.

Options:
- **Light** - Light background (default)
- **Dark** - Dark background

Toggle: **Edit → Preferences → Theme**

### Feature: Configuration Merging

Combine multiple configurations.

```bash
hblcs update base.yaml \
    --merge additions.yaml \
    --output merged.yaml
```

Useful for:
- Extending existing languages
- Combining features from multiple configs
- Iterative language development

### Feature: Batch Operations

Modify multiple items at once.

```bash
# Multiple keyword changes
hblcs update my_lang.yaml \
    --set keywords.if.custom=cuando \
    --set keywords.while.custom=mientras \
    --set keywords.for.custom=para \
    --output my_lang.yaml
```

---

## Troubleshooting

### IDE Won't Start

**Problem**: `hblcs-ide` command not found

**Solution**:
```bash
# Check if installed
pip show hb_lcs

# If not installed
pip install -e .

# Or launch from source
python src/hb_lcs/launch_ide.py
```

### Can't Load Configuration

**Problem**: "Configuration error: Invalid file"

**Solution**:
```bash
# Validate configuration
hblcs validate my_config.yaml

# Check error details
hblcs validate my_config.yaml --verbose

# Fix issues
hblcs info my_config.yaml
```

### Code Won't Run

**Problem**: "Syntax error" when running code

**Solution**:
1. Check you're using correct custom keywords
2. Run `Tools → Syntax Check` to find errors
3. Verify configuration is loaded correctly
4. Look at example code for syntax

### Configuration File Corrupted

**Problem**: "Error parsing configuration file"

**Solution**:
```bash
# Convert to JSON (often more forgiving)
hblcs convert my_lang.yaml --to json --output my_lang.json

# Validate JSON version
hblcs validate my_lang.json

# If it works, use JSON version
# If not, check file manually
cat my_lang.json | grep -i error
```

### Performance Issues

**Problem**: IDE is slow

**Solution**:
1. **Disable minimap**: Edit → Preferences → Show Minimap = Off
2. **Disable syntax highlighting**: Edit → Preferences → Syntax Highlighting = Off
3. **Disable code completion**: Edit → Preferences → Code Completion = Off
4. **Use simpler config**: Load minimal preset instead of large config
5. **Restart IDE**: Close and reopen

### File Permission Issues

**Problem**: "Permission denied" on Windows

**Solution**:
```powershell
# Run as Administrator
# Open PowerShell as admin, then:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or use Command Prompt instead
```

---

## Tips & Tricks

### Tip 1: Use Presets as Base

Don't create from scratch. Start with a preset and customize:

```bash
hblcs create --preset python_like --output my_lang.yaml
# Then modify my_lang.yaml
```

### Tip 2: Version Your Configs

Track version numbers:

```bash
# Version 1.0
hblcs create --output mylang_v1.0.yaml

# Version 2.0 (with new features)
hblcs create --output mylang_v2.0.yaml

# Keep both for backward compatibility
```

### Tip 3: Use Meaningful Names

Choose keywords that clearly indicate their purpose:

❌ Bad:
```python
x = abc()  # What does x do?
```

✅ Good:
```python
count = get_total_items()  # Clear purpose
```

### Tip 4: Document Your Language

Add descriptions to keywords:

```bash
hblcs update my_lang.yaml \
    --set keywords.if.description="Execute code if condition is true" \
    --output my_lang.yaml

# Export documentation
hblcs export my_lang.yaml --format markdown --output README.md
```

### Tip 5: Use IDE Keyboard Shortcuts

Learn common shortcuts for faster workflow:

- **Ctrl+S** - Save
- **Ctrl+O** - Open
- **Ctrl+N** - New
- **Ctrl+Z** - Undo
- **Ctrl+Y** - Redo
- **Ctrl+F** - Find
- **Ctrl+H** - Replace

### Tip 6: Backup Before Major Changes

Always backup before big modifications:

```bash
cp my_lang.yaml my_lang.backup.yaml
# Make changes
# If problem: cp my_lang.backup.yaml my_lang.yaml
```

### Tip 7: Test Incrementally

Test changes step by step:

```bash
# 1. Change one keyword
hblcs update my_lang.yaml --set keywords.if.custom=cuando --output my_lang.yaml
hblcs validate my_lang.yaml

# 2. Load in IDE and test
hblcs-ide

# 3. If it works, change next keyword
# 4. Repeat
```

### Tip 8: Share Language Configs

Share your languages as JSON (wider compatibility):

```bash
# Convert to JSON
hblcs convert my_lang.yaml --to json --output my_lang.json

# Share my_lang.json
# Recipients can use it immediately
```

### Tip 9: Use IDE for Learning

Explore built-in examples:

1. Launch IDE: `hblcs-ide`
2. Load different presets
3. Try their example code
4. See how they work
5. Create your own based on what you learn

### Tip 10: Combine CLI and IDE

Use them together effectively:

```bash
# Use CLI for bulk operations
hblcs update my_lang.yaml --set keywords.if.custom=cuando --output my_lang.yaml

# Use IDE for fine-tuning
hblcs-ide
# File → Load Configuration → my_lang.yaml
# Make final adjustments in GUI
# File → Save Configuration
```

---

## Keyboard Shortcuts Reference

| Action | Linux/Windows | macOS |
|--------|---------------|-------|
| New | Ctrl+N | Cmd+N |
| Open | Ctrl+O | Cmd+O |
| Save | Ctrl+S | Cmd+S |
| Load Config | Ctrl+L | Cmd+L |
| Undo | Ctrl+Z | Cmd+Z |
| Redo | Ctrl+Y | Cmd+Shift+Z |
| Cut | Ctrl+X | Cmd+X |
| Copy | Ctrl+C | Cmd+C |
| Paste | Ctrl+V | Cmd+V |
| Select All | Ctrl+A | Cmd+A |
| Find | Ctrl+F | Cmd+F |
| Replace | Ctrl+H | Cmd+Option+F |
| Run Code | Ctrl+Enter | Cmd+Enter |
| Exit | Alt+F4 | Cmd+Q |

---

## Getting Help

### Documentation
- **[Installation Guide](INSTALL_GUIDE.md)** - Setup instructions
- **[Technical Reference](TECHNICAL_REFERENCE.md)** - API docs
- **[Language Development Guide](LANGUAGE_DEVELOPMENT_GUIDE.md)** - Creating languages
- **[IDE Guide](IDE_README.md)** - IDE features

### Online Resources
- **GitHub**: https://github.com/James-HoneyBadger/HB_Language_Construction
- **Issues**: GitHub Issues for bug reports
- **Discussions**: GitHub Discussions for Q&A

### Running Examples

```bash
# Run demo script
python demos/demo_language_construction.py

# Run TeachScript examples
python demos/teachscript/run_teachscript.py demos/teachscript/examples/01_hello_world.teach

# Run tests
python -m pytest tests/ -v
```

---

**User Guide v4.0**  
December 3, 2025  
Compatible with HB Language Construction Set v4.0
