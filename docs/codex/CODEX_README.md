# CodeEx - CodeCraft Execution Environment

**Version 1.0.0**

Professional IDE for developing and running applications created with CodeCraft.

## What is CodeEx?

CodeEx is a specialized IDE that integrates with CodeCraft to provide:

- **Multi-language support**: Load any CodeCraft-designed language
- **Professional editor**: Syntax highlighting, line numbers, code completion
- **Project management**: Organize CodeCraft applications
- **Real-time execution**: Run code instantly with loaded interpreters
- **Integrated console**: See output, errors, and variables
- **Full integration**: Export languages from CodeCraft → Load in CodeEx

## Quick Start

### Installation

CodeEx comes as part of CodeCraft. No additional installation needed.

### Launch CodeEx

```bash
python codex.py
```

### First Project in 3 Steps

1. **Create Project**: Click "New Project", name it `HelloWorld`
2. **Load Language**: Click "Load Interpreter", select `configs/examples/python_like.yaml`
3. **Write & Run**: Type code, click "▶ Run"

## Key Features

### 🎨 Professional Editor
- Syntax highlighting with dynamic color adjustment
- Line numbers with automatic updates
- Code folding and indentation
- Undo/Redo support
- Search and replace

### 📁 Project Management
- Organized project structure
- Multi-project support
- Project metadata and settings
- Recent projects tracking
- Version control ready

### 🔧 Interpreter Management
- Load any CodeCraft language configuration
- Multiple interpreters in one session
- Interpreter metadata display
- Configuration inspection

### 🎬 Execution Engine
- Real-time code execution
- Isolated execution contexts
- Error reporting with line numbers
- Variable inspection
- Execution history

### 💬 Integrated Console
- Color-coded output (success/error/info)
- Scrollable history
- Clear button
- Output preservation

## Architecture

```
CodeEx IDE
├── Editor (Code editing)
├── Console (Output display)
├── Project Explorer (File navigation)
├── Interpreter Manager (Language selection)
└── Execution Engine (Code running)
```

## Files

```
CodeEx/
├── codex.py                      # Entry point
├── codex_gui.py                  # Main IDE interface
├── codex_components.py           # UI components
├── src/hb_lcs/
│   └── interpreter_generator.py  # CodeCraft integration
└── docs/guides/
    ├── CODEX_QUICKSTART.md       # 5-minute start
    ├── CODEX_USER_GUIDE.md       # Full manual
    ├── CODEX_DEVELOPER_GUIDE.md  # Development docs
    └── CODEX_INTEGRATION_GUIDE.md # CodeCraft integration
```

## Documentation

### For Users

| Guide | Purpose | Time |
|-------|---------|------|
| [CODEX_QUICKSTART.md](docs/guides/CODEX_QUICKSTART.md) | Get running in 5 minutes | 5 min |
| [CODEX_USER_GUIDE.md](docs/guides/CODEX_USER_GUIDE.md) | Complete user manual | 30 min |
| [CODEX_INTEGRATION_GUIDE.md](docs/guides/CODEX_INTEGRATION_GUIDE.md) | Use with CodeCraft | 20 min |

### For Developers

| Guide | Purpose | Time |
|-------|---------|------|
| [CODEX_DEVELOPER_GUIDE.md](docs/guides/CODEX_DEVELOPER_GUIDE.md) | Architecture & extension | 30 min |
| [interpreter_generator.py](src/hb_lcs/interpreter_generator.py) | Integration API | Code |

## Common Tasks

### Create New Project
```
File → New Project → Enter name → Create
```

### Load Language
```
Click "Load Interpreter" → Select configuration → CodeEx loads language
```

### Run Code
```
Write code → Click "▶ Run" or Ctrl+R → See output in console
```

### Save Work
```
Ctrl+S or File → Save
```

### Switch Language
```
Click "Load Interpreter" → Select different language → Syntax updates
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+N | New Project |
| Ctrl+O | Open Project |
| Ctrl+S | Save File |
| Ctrl+R | Run Code |
| F5 | Run Code |
| Ctrl+Z | Undo |
| Ctrl+Shift+Z | Redo |
| Ctrl+Q | Quit |

## Integration with CodeCraft

### Export Language from CodeCraft

```python
from src.hb_lcs.language_config import LanguageConfig
from src.hb_lcs.interpreter_generator import InterpreterGenerator

# Load language definition
config = LanguageConfig.load("my_language.json")

# Export for CodeEx
gen = InterpreterGenerator()
gen.export_interpreter(config, format="json")
# Saved to: ~/.codecraft/interpreters/
```

### Load in CodeEx

1. Click "Load Interpreter"
2. Navigate to `~/.codecraft/interpreters/`
3. Select exported JSON file
4. Language loaded and ready to use

See [CODEX_INTEGRATION_GUIDE.md](docs/guides/CODEX_INTEGRATION_GUIDE.md) for full details.

## System Requirements

- Python 3.8+
- tkinter (usually included)
- 100MB disk space for projects
- Modern OS (Linux, macOS, Windows)

## Project Structure

Created projects follow this structure:

```
MyProject/
├── project.json          # Metadata
├── src/                  # Your source code
├── examples/             # Example programs
└── tests/                # Test files
```

## Error Handling

CodeEx provides helpful error messages:

- **"No interpreter loaded"** → Click "Load Interpreter"
- **"Syntax error"** → Check code against language rules
- **"File not found"** → Verify file path
- **"Execution failed"** → Check console for details

See troubleshooting section in [CODEX_USER_GUIDE.md](docs/guides/CODEX_USER_GUIDE.md).

## Performance

- Handles files up to 1MB
- Real-time syntax highlighting
- Instant code execution (default 30s timeout)
- Smooth project navigation with 1000+ files

## Extensibility

CodeEx is designed to be extended:

### Add Menu Item

```python
# In codex_components.py
file_menu.add_command(label="New Feature", command=ide.new_feature)
```

### Add UI Component

```python
# In codex_gui.py
self.my_component = CodeExMyComponent(some_container)
```

### Add Feature

1. Create method in CodeExIDE class
2. Wire to menu or button
3. Test integration
4. Update documentation

See [CODEX_DEVELOPER_GUIDE.md](docs/guides/CODEX_DEVELOPER_GUIDE.md) for patterns.

## Limitations

- Single active interpreter per session
- Local projects only (no cloud)
- No remote execution
- Console limited to 10,000 lines
- 30 second execution timeout

## Future Enhancements

- [ ] Debugger with breakpoints
- [ ] Multiple concurrent interpreters
- [ ] Package management
- [ ] Plugin system
- [ ] Cloud sync
- [ ] Collaborative editing
- [ ] Language templates
- [ ] Performance profiling

## Contributing

CodeEx is part of CodeCraft. See main project for contribution guidelines.

## License

CodeEx is part of the CodeCraft project. See LICENSE file.

## Support

### Documentation
- [CODEX_USER_GUIDE.md](docs/guides/CODEX_USER_GUIDE.md) - Complete manual
- [CODEX_QUICKSTART.md](docs/guides/CODEX_QUICKSTART.md) - Quick start
- [CODEX_DEVELOPER_GUIDE.md](docs/guides/CODEX_DEVELOPER_GUIDE.md) - Developer docs
- [CODEX_INTEGRATION_GUIDE.md](docs/guides/CODEX_INTEGRATION_GUIDE.md) - CodeCraft integration

### Examples
- `configs/examples/` - Language configurations
- `demos/` - Demo programs
- Project templates (created when you make new project)

## Roadmap

### Version 1.0 (Current)
- ✅ Core IDE interface
- ✅ Project management
- ✅ Interpreter loading
- ✅ Code execution
- ✅ Integrated console

### Version 1.1
- [ ] Debugger
- [ ] Enhanced syntax highlighting
- [ ] Code completion
- [ ] Package templates

### Version 2.0
- [ ] Multiple interpreters
- [ ] Collaborative features
- [ ] Cloud storage
- [ ] Plugin system

## Getting Started

1. **Read**: [CODEX_QUICKSTART.md](docs/guides/CODEX_QUICKSTART.md) (5 minutes)
2. **Launch**: `python codex.py`
3. **Create**: New project
4. **Load**: Language configuration
5. **Write**: Your first program
6. **Run**: And see results

## Contact & Community

For questions, issues, or contributions, see the main CodeCraft project.

---

**CodeEx: Professional IDE for Custom Languages**

*Version 1.0.0 - 2024*
