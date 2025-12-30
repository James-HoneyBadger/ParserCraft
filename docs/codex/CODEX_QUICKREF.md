# CodeEx Quick Reference Card

**CodeEx v1.0.0** - CodeCraft Execution Environment

## Launch

```bash
python codex.py
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

## Menu Bar

### File
- New Project (Ctrl+N)
- Open Project (Ctrl+O)
- Save (Ctrl+S)
- Exit (Ctrl+Q)

### Edit
- Undo (Ctrl+Z)
- Redo (Ctrl+Shift+Z)
- Cut, Copy, Paste

### Interpreter
- Load Interpreter
- Create Language Configuration
- Interpreter Settings

### Run
- Execute Code (Ctrl+R)
- Stop Execution
- Recent Executions

### View
- Toggle Theme
- Zoom In/Out
- Show/Hide Console
- Show/Hide Project Explorer

### Help
- Getting Started
- User Guide
- API Reference
- About CodeEx

## Toolbar Buttons

| Button | Action |
|--------|--------|
| New Project | Create new CodeEx project |
| Open Project | Load existing project |
| Save | Save current file (Ctrl+S) |
| Load Interpreter | Import language configuration |
| ▶ Run | Execute code (Ctrl+R) |
| ⏹ Stop | Halt execution |
| 🌙 Theme | Toggle light/dark theme |
| ❓ Help | Show help dialog |

## Workflow

### 1. Create Project
```
File → New Project
├─ Enter: Project name
├─ Optional: Description
└─ Optional: Interpreter name
```

### 2. Load Language
```
Click: Load Interpreter
├─ Navigate: ~/configs/examples/ or custom path
└─ Select: Language configuration (JSON/YAML)
```

### 3. Write Code
```
Type code in editor
- Syntax highlighting applies automatically
- Line numbers show on left
- Use keyboard shortcuts
```

### 4. Execute
```
Click: ▶ Run (or Ctrl+R)
├─ Code executes
├─ Output shows in console
└─ Status shows: Success or Error
```

### 5. Save
```
Press: Ctrl+S
└─ File saved to project/src/
```

## Project Structure

```
MyProject/
├── project.json      # Metadata
├── src/              # Your code
├── examples/         # Examples
└── tests/            # Tests
```

## Common Tasks

### Load Python-Like Language
```
1. Click "Load Interpreter"
2. Select: configs/examples/python_like.yaml
3. Code syntax updates automatically
```

### Run Simple Program
```
1. Type: print "Hello World"
2. Press: Ctrl+R
3. See: "Hello World" in console
```

### Switch Languages
```
1. Click "Load Interpreter" 
2. Select different config
3. Syntax highlighting updates
```

### Clear Console
```
1. Click "Clear" button in console
2. Output emptied, ready for next execution
```

## Settings

**Location**: `~/.codex/settings.json`

```json
{
  "theme": "light" or "dark",
  "font_size": 11,
  "recent_projects": [...]
}
```

## Projects Location

**Directory**: `~/.codex/projects/`

All created projects stored here.

## Interpreters Location

**Directory**: `~/.codecraft/interpreters/`

Exported interpreters from CodeCraft stored here.

## Error Messages

| Error | Solution |
|-------|----------|
| "No interpreter loaded" | Click "Load Interpreter" |
| "File not found" | Check file path and permissions |
| "Execution failed" | Check code syntax |
| "No project loaded" | Create or open project first |

## Tips

1. **Save Often**: Ctrl+S after each change
2. **Test Code**: Run small snippets first
3. **Check Syntax**: Review error messages carefully
4. **Use Examples**: Load example configs first
5. **Explore Menus**: All features discoverable there

## Documentation

| Document | Purpose |
|----------|---------|
| [CODEX_QUICKSTART.md](docs/guides/CODEX_QUICKSTART.md) | 5-minute start |
| [CODEX_USER_GUIDE.md](docs/guides/CODEX_USER_GUIDE.md) | Complete manual |
| [CODEX_DEVELOPER_GUIDE.md](docs/guides/CODEX_DEVELOPER_GUIDE.md) | Development |
| [CODEX_INTEGRATION_GUIDE.md](docs/guides/CODEX_INTEGRATION_GUIDE.md) | CodeCraft integration |

## Keyboard Shortcut Categories

### Project Management
- Ctrl+N: New Project
- Ctrl+O: Open Project

### File Operations
- Ctrl+S: Save File

### Editing
- Ctrl+Z: Undo
- Ctrl+Shift+Z: Redo

### Execution
- Ctrl+R: Run Code
- F5: Run Code (alternative)

### Application
- Ctrl+Q: Quit

## File Types

| Type | Extension | Example |
|------|-----------|---------|
| CodeCraft Language | .json, .yaml | python_like.yaml |
| Code Files | .cc, .py | hello.cc |
| Project Metadata | .json | project.json |
| Settings | .json | settings.json |

## Console Output Tags

| Type | Color | Example |
|------|-------|---------|
| Output | Black | `Hello World` |
| Error | Red | `Syntax error at line 5` |
| Success | Green | `Execution successful` |

## Syntax Highlighting Colors

| Category | Color | Font |
|----------|-------|------|
| Keywords | Blue | Bold |
| Strings | Green | Regular |
| Comments | Gray | Italic |
| Numbers | Orange | Regular |
| Functions | Red | Regular |
| Operators | Dark Blue | Regular |

## Configuration Requirements

Valid language configuration needs:
- `name`: Language identifier
- `keywords`: List of keywords
- `functions`: Dictionary of functions
- `operators`: List of operators

## System Requirements

- Python 3.8 or higher
- tkinter (included with Python)
- 100MB disk space for projects
- Modern OS (Linux, macOS, Windows)

## Performance Tips

1. **Limit file size**: <1MB for best performance
2. **Clear old projects**: Remove unused projects
3. **Restart IDE**: If experiencing slowness
4. **Save frequently**: Don't lose work

## Troubleshooting

### Won't Launch
```bash
# Check Python version
python --version

# Test imports
python -c "import tkinter; print('OK')"
```

### Interpreter Won't Load
- File must be JSON or YAML
- Must have required fields
- Try example config first

### Code Won't Execute
- Verify interpreter loaded (see status bar)
- Check code syntax
- Review error message

### Slow Performance
- Close other applications
- Reduce file size
- Try simpler code

## Getting Help

1. **In-app**: Click Help menu
2. **Documentation**: Read guide files
3. **Examples**: Try example configs
4. **Code**: Review example code in demos/

## Features Summary

✅ Multi-language support  
✅ Professional editor  
✅ Real-time execution  
✅ Project management  
✅ Integrated console  
✅ Syntax highlighting  
✅ Theme support  
✅ Settings persistence  
✅ Complete menus  
✅ Keyboard shortcuts  

## Coming Soon (v1.1)

- Debugger with breakpoints
- Enhanced syntax highlighting
- Code completion
- Language templates

## Version Information

**Current**: 1.0.0  
**Release Date**: December 2024  
**Status**: Production Ready  
**Part of**: CodeCraft Project

---

**Tip**: For comprehensive information, see [CODEX_USER_GUIDE.md](docs/guides/CODEX_USER_GUIDE.md)

**Quick Start**: See [CODEX_QUICKSTART.md](docs/guides/CODEX_QUICKSTART.md)
