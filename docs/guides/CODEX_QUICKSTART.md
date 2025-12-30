# CodeCraft Quick Start Guide

Get CodeCraft and CodeEx running in 5 minutes!

## Quick Launch (Easiest)

```bash
# Linux/macOS
./run-codecraft.sh    # Launch CodeCraft IDE (language design)
./run-codex.sh        # Launch CodeEx IDE (application development)

# Windows
run-codecraft.bat     # Launch CodeCraft IDE
run-codex.bat         # Launch CodeEx IDE
```

These scripts automatically set up the Python environment and install dependencies.

## Prerequisites

- Python 3.9+
- Basic understanding of programming concepts

## What You'll Get

### CodeCraft IDE
- Visual language configuration editor
- Language presets (Python-like, JavaScript-like, Lisp-like, etc.)
- Real-time configuration validation
- Testing and preview panels
- Export/import configurations

### CodeEx IDE
- Professional application development environment
- Load any CodeCraft-created language
- Multi-file project support
- Syntax highlighting
- Real-time code execution

## First Steps

### 1. Launch CodeCraft IDE

```bash
./run-codecraft.sh    # (Linux/macOS)
run-codecraft.bat     # (Windows)
```

### 2. Design Your Language

In CodeCraft IDE:
- Click "New Configuration"
- Select preset: "python_like"
- Rename keywords:
  - `if` → `cuando` (Spanish "when")
  - `def` → `funcion` (Spanish "function")
- Save as "spanish.yaml"

### 3. Launch CodeEx IDE

```bash
./run-codex.sh        # (Linux/macOS)
run-codex.bat         # (Windows)
```

### 4. Develop in Your Language

In CodeEx IDE:
- Load "spanish.yaml"
- Create a new file: "hello.when"
- Write code using your custom syntax:
```
cuando True:
    funcion greet():
        say "¡Hola!"
    greet()
```
- Click "Run" to execute

## Manual Installation

### Prerequisites

- Python 3.8+
- tkinter (usually included with Python)

### Verify Installation

```bash
# Check Python version
python3 --version  # Should be 3.8 or higher

# Test tkinter
python3 -c "import tkinter; print('tkinter OK')"
```

## Launching Manually

### CodeCraft IDE from Command Line

```bash
cd /path/to/CodeCraft
python codex.py
```

### From Python

```python
from codex import main
main()
```

### Expected Output

CodeEx window opens with:
- Menu bar (File, Edit, Interpreter, Run, View, Help)
- Toolbar with project, interpreter, and execution buttons
- Empty editor pane
- Output console (bottom)
- Project explorer (left sidebar)

## First Steps

### Step 1: Create a Project (1 minute)

1. Click **"New Project"** button in toolbar
2. Enter project name: `HelloWorld`
3. Add description: `My first CodeEx project`
4. Click **"Create"**

You should see:
- Status bar shows: "Project: HelloWorld"
- Project explorer shows directory structure

### Step 2: Load a Language (2 minutes)

1. Click **"Load Interpreter"** button
2. Navigate to `/home/james/CodeCraft/configs/examples/`
3. Select a configuration, e.g., `python_like.yaml`
4. CodeEx loads the interpreter

You should see:
- Status bar shows: "Loaded: python_like"
- Syntax highlighting colors updated in editor
- Interpreter dropdown shows language name

### Step 3: Write Code (1 minute)

Click in the editor and type:

```
print "Hello from CodeEx!"
x = 10
y = 20
print x + y
```

You should see:
- Code appears in editor
- Line numbers on left
- Color syntax highlighting applied

### Step 4: Run Code (1 minute)

1. Click **"▶ Run"** button (or press Ctrl+R)
2. Watch console output appear

You should see:
- "Execution successful" in status bar
- Output in console pane
- No error messages

## Common Tasks

### Open an Existing Project

1. Click **"Open Project"** button
2. Navigate to `~/.codex/projects/`
3. Select project folder
4. Click **"Select Folder"**

Project loads with all files visible in explorer.

### Save Your Work

- Click **"Save"** button (or press Ctrl+S)
- File saved to project directory
- Status shows: "Saved: filename.cc"

### Switch Languages

1. Click **"Load Interpreter"** again
2. Select different language configuration
3. Code syntax highlighting updates automatically

### Clear Output

1. Click **"Clear"** button in console
2. Console empties, ready for next execution

## Project File Structure

When you create a project, CodeEx creates:

```
HelloWorld/
├── project.json          # Project metadata
├── src/                  # Your source code goes here
├── examples/             # Example programs
└── tests/                # Test files
```

**project.json** contains:
- Project name
- Creation date
- Associated interpreter
- Description

## Tips & Tricks

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+N | New Project |
| Ctrl+O | Open Project |
| Ctrl+S | Save File |
| Ctrl+R | Run Code |
| Ctrl+Z | Undo |
| Ctrl+Shift+Z | Redo |

### Workflow

1. **Create Project** → **Load Interpreter** → **Write Code** → **Run** → **Save**

2. **Repeat**: Edit code → Run → Test

3. **Switch Languages**: Load different interpreter → Same workflow

### Best Practices

- Create separate project per language
- Save frequently (Ctrl+S)
- Use meaningful project names
- Organize files in `src/` subdirectory
- Keep examples in `examples/` folder

## Troubleshooting

### CodeEx Won't Start

**Problem**: Application doesn't open
```bash
# Check Python version
python --version
# Should be 3.8 or higher

# Check imports work
python -c "import tkinter, sys; sys.path.insert(0, '.'); from codex import main"
```

### Interpreter Won't Load

**Problem**: Configuration file not found
- Ensure file exists and is readable
- Use JSON or YAML format
- Check file path is correct

**Problem**: Invalid configuration
- Open file and verify structure
- Check for required fields: name, keywords
- Try example file first: `configs/examples/python_like.yaml`

### Code Won't Execute

**Problem**: "No interpreter loaded"
- Click "Load Interpreter" button
- Select valid configuration file
- Try example configuration first

**Problem**: "Execution failed"
- Check code syntax
- Verify it follows loaded language rules
- Review error message in console

### Slow Performance

**Problem**: Editor lags while typing
- Close other applications
- Reduce file size
- Restart CodeEx

**Problem**: Slow execution
- Check code for infinite loops
- Simplify code
- Try shorter test case

## Next Steps

1. **Explore Examples**
   - Load different language configs
   - Try example code patterns
   - Study syntax for each language

2. **Create Projects**
   - Build simple programs
   - Test language features
   - Experiment with variables and logic

3. **Study Documentation**
   - Read [CODEX_USER_GUIDE.md](./CODEX_USER_GUIDE.md) for full features
   - See [LANGUAGE_DEVELOPMENT_GUIDE.md](./LANGUAGE_DEVELOPMENT_GUIDE.md) for creating languages
   - Check [TECHNICAL_REFERENCE.md](../reference/TECHNICAL_REFERENCE.md) for API details

## Getting Help

### Built-in Help

Click **Help** menu for:
- Getting Started
- User Guide
- API Reference
- About CodeEx

### Documentation

Browse docs folder:
- `docs/guides/` - How-to guides
- `docs/reference/` - API reference
- `docs/teachscript/` - TeachScript manual

### Examples

Browse example configurations:
- `configs/examples/` - Language configurations
- `demos/` - Demo programs
- Project `examples/` folder - Your examples

## Quick Reference

### Launch
```bash
python codex.py
```

### Create Project
File → New Project

### Load Language
Click "Load Interpreter" → Select config

### Run Code
Click "▶ Run" or Ctrl+R

### Save
Ctrl+S

### Exit
File → Exit or Ctrl+Q

## Common Errors

| Error | Solution |
|-------|----------|
| "No module named tkinter" | Install tkinter: `pip install tk` |
| "No interpreter loaded" | Click "Load Interpreter" button |
| "File not found" | Use full path to file |
| "Execution failed" | Check code syntax against language rules |
| "ImportError: codex_gui" | Run from CodeCraft root directory |

---

**Ready to create?** Open CodeEx and start coding! 🚀
