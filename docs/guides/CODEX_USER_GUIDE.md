# CodeEx - CodeCraft Execution Environment

**Version 2.0**

CodeEx is a professional IDE designed specifically for developing and running applications created with CodeCraft. It provides a complete development environment for creating custom programming languages and executing code written in those languages.

## Overview

CodeEx bridges CodeCraft (language creation framework) and application development by providing:

1. **Interpreter Management**: Load any CodeCraft-generated language/interpreter
2. **Professional Editor**: Syntax-highlighted code editor with project structure
3. **Real-time Execution**: Execute code instantly with the loaded interpreter
4. **Project Management**: Organize CodeCraft applications into projects
5. **Developer Tools**: Console, debugging, and output tracking

## Architecture

### Core Components

#### 1. **codex.py** (Entry Point)
- Application launcher
- Tkinter root window initialization
- 1600x900 default resolution
- Module imports and path setup

#### 2. **codex_gui.py** (Main IDE)
- `CodeExIDE` class: Main IDE interface
- Implements multi-panel layout:
  - Project Explorer (left)
  - Code Editor (center)
  - Output Console (bottom)
- Menu bar with File, Edit, Interpreter, Run, View, Help
- Toolbar with quick actions
- Project and interpreter management

#### 3. **codex_components.py** (UI Components)
- `CodeExEditor`: Code editor with line numbers and syntax highlighting
- `CodeExConsole`: Output console for execution results
- `CodeExProjectExplorer`: File/project browser
- `CodeExMenu`: Menu bar implementation

#### 4. **src/hb_lcs/interpreter_generator.py** (Integration)
- `InterpreterPackage`: Encapsulates interpreter instances
- `InterpreterGenerator`: Creates and manages interpreters
- Serialization support (JSON, Pickle, File)
- Execution isolation and context management

### Data Flow

```
CodeCraft Language Config
        ↓
    (JSON/YAML)
        ↓
CodeEx: Load Interpreter
        ↓
    InterpreterGenerator
        ↓
    InterpreterPackage
        ↓
CodeEx: Editor
        ↓
    Write/Load Code
        ↓
Execute Button
        ↓
interpreter.execute(code)
        ↓
Result → Console Output
```

## Features

### Project Management

**Create New Project**
- Organized folder structure
- Metadata tracking (creation date, description, interpreter)
- Project file: `project.json`
- Auto-generated directories: `src/`, `examples/`, `tests/`

**Open Existing Project**
- Browse projects directory
- Load project metadata
- Auto-select configured interpreter

**Project Structure**
```
my_project/
├── project.json          # Metadata
├── src/                  # Source code
├── examples/             # Example programs
└── tests/                # Test files
```

### Interpreter Management

**Load Interpreter**
- From CodeCraft language configuration (JSON/YAML)
- Automatic syntax highlighting update
- Metadata display (keywords, functions, operators)
- Multiple interpreters supported

**Available Features**
- View interpreter configuration
- Check syntax rules
- List available keywords
- Browse function definitions

### Code Editor

**Features**
- Line numbers
- Syntax highlighting (keywords, strings, comments, numbers)
- Auto-indentation
- Undo/Redo support
- Code folding
- Find/Replace

**Syntax Categories**
- Keywords: Blue, bold
- Strings: Green
- Comments: Gray, italic
- Numbers: Orange
- Functions: Red
- Operators: Dark blue

### Execution Engine

**Run Code**
- Execute selected or full code
- Isolated execution context
- Real-time output to console
- Error reporting with line numbers

**Console Output**
- Color-coded messages (success=green, error=red, output=black)
- Scrollable history
- Clear button
- Variable display

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+N | New Project |
| Ctrl+O | Open Project |
| Ctrl+S | Save File |
| Ctrl+R | Run Code |
| F5 | Run Code |
| Ctrl+Q | Quit |
| Ctrl+Z | Undo |
| Ctrl+Shift+Z | Redo |

## Usage

### Starting CodeEx

```bash
python codex.py
```

Or from Python:
```python
from codex import main
main()
```

### Creating a Language Project

1. **Click "New Project"**
   - Enter project name
   - Add description (optional)
   - Specify interpreter (will set later if needed)

2. **Load Interpreter**
   - Click "Load Interpreter" button
   - Select CodeCraft language configuration file (JSON/YAML)
   - Interpreter loaded and ready

3. **Write Code**
   - Editor syntax highlighting updates automatically
   - Follows loaded language rules

4. **Execute Code**
   - Click "▶ Run" button
   - Output appears in console
   - Variables available in inspector

### Integration with CodeCraft

#### Export Interpreter from CodeCraft

```python
from src.hb_lcs.language_config import LanguageConfig
from src.hb_lcs.interpreter_generator import InterpreterGenerator

# Load configuration
config = LanguageConfig.load("my_language.json")

# Create generator
gen = InterpreterGenerator()

# Generate interpreter
interpreter = gen.generate(config)

# Export for CodeEx
gen.export_interpreter(config, format="json")
# Saved to: ~/.codecraft/interpreters/
```

#### Use in CodeEx

1. Click "Load Interpreter"
2. Navigate to `~/.codecraft/interpreters/`
3. Select exported JSON file
4. CodeEx loads the interpreter

## Configuration

### Settings File
Location: `~/.codex/settings.json`

```json
{
  "theme": "light",
  "font_size": 11,
  "recent_projects": [
    "/home/user/.codex/projects/project1",
    "/home/user/.codex/projects/project2"
  ]
}
```

### Projects Directory
Location: `~/.codex/projects/`

All created projects stored here with metadata.

### Interpreters Directory
Location: `~/.codecraft/interpreters/`

Exported interpreters from CodeCraft stored here.

## Menu Reference

### File Menu
- **New Project**: Create new CodeCraft project
- **Open Project**: Open existing project
- **Save**: Save current file (Ctrl+S)
- **Exit**: Close application

### Edit Menu
- **Undo**: Undo last action (Ctrl+Z)
- **Redo**: Redo last action (Ctrl+Shift+Z)
- **Cut/Copy/Paste**: Clipboard operations

### Interpreter Menu
- **Load Interpreter**: Import language configuration
- **Create Language Configuration**: New language builder
- **Interpreter Settings**: Configure behavior

### Run Menu
- **Execute Code**: Run code (Ctrl+R, F5)
- **Stop**: Halt execution
- **Recent Executions**: View history

### View Menu
- **Toggle Theme**: Switch light/dark theme
- **Zoom In/Out**: Adjust font size
- **Show/Hide Console**: Toggle console visibility
- **Show/Hide Project Explorer**: Toggle sidebar

### Help Menu
- **Getting Started**: Quick start guide
- **User Guide**: Full documentation
- **API Reference**: CodeCraft API docs
- **About CodeEx**: Version information

## Error Handling

### Common Issues

**"No interpreter loaded"**
- Click "Load Interpreter" and select configuration
- Ensure file is valid JSON/YAML

**"Execution failed"**
- Check code syntax against loaded language rules
- Review error message in console
- Look up keyword definitions in interpreter

**"Project not found"**
- Verify project path exists
- Check ~/.codex/projects/ directory
- Recreate project if necessary

### Debugging

Enable verbose output:
1. Run with debug flag: `python codex.py --debug`
2. Check console for detailed error messages
3. Review error messages include line numbers

## Development Guide

### Adding New Components

1. Add UI element to `codex_components.py`
2. Integrate into `CodeExIDE` in `codex_gui.py`
3. Connect to menu system

### Extending Features

**Add Menu Item**
```python
# In codex_components.py, CodeExMenu.__init__()
file_menu.add_command(label="New Feature", command=self.ide.new_feature)
```

**Add IDE Method**
```python
# In codex_gui.py, CodeExIDE class
def new_feature(self):
    """Implement feature."""
    pass
```

### Testing Components

```bash
# Test module imports
python -m py_compile codex.py codex_gui.py codex_components.py

# Launch IDE
python codex.py

# Test with sample project
# 1. Create new project
# 2. Load interpreter
# 3. Execute test code
```

## Performance

- Editor handles files up to 1MB
- Syntax highlighting updates in real-time
- Project navigation supports 1000+ files
- Execution timeout: 30 seconds (configurable)

## Limitations

- Single active interpreter per session
- No remote execution
- Local project storage only
- No collaborative features
- Console output limited to 10,000 lines

## Future Enhancements

- [ ] Multiple interpreter instances
- [ ] Remote execution support
- [ ] Debugger with breakpoints
- [ ] Package management system
- [ ] Cloud project sync
- [ ] Collaborative editing
- [ ] Plugin system
- [ ] Language templates

## Support

### Documentation
- See [LANGUAGE_DEVELOPMENT_GUIDE.md](../docs/guides/LANGUAGE_DEVELOPMENT_GUIDE.md)
- See [TEACHSCRIPT_MANUAL.md](../docs/teachscript/TEACHSCRIPT_MANUAL.md)

### CodeCraft Integration
- See [interpreter_generator.py](./src/hb_lcs/interpreter_generator.py) for API
- See [language_config.py](./src/hb_lcs/language_config.py) for configuration format

### Troubleshooting
Check workspace for:
- `/home/james/CodeCraft/docs/guides/` for guides
- `/home/james/CodeCraft/configs/examples/` for example configurations
- `/home/james/CodeCraft/tests/` for test examples

## License

CodeEx is part of the CodeCraft project. See LICENSE file for details.
