# CodeCraft IDE Developer Guide

Technical documentation for the CodeCraft IDE - the language design interface.

## Overview

The CodeCraft IDE (`src/hb_lcs/ide.py`) is a comprehensive graphical interface
for creating and testing custom programming languages. It provides visual editors
for language configuration with real-time validation and testing capabilities.

## Architecture Overview

### System Design

CodeCraft IDE implements a multi-panel architecture:

```
┌─────────────────────────────────────┐
│     Presentation Tier               │
│  (codex_gui.py, codex_components)   │
│  - UI Layout & Menus                │
│  - Event Handling                   │
│  - User Interaction                 │
└─────────────────────────────────────┘
              ↓↑
┌─────────────────────────────────────┐
│     Business Logic Tier             │
│      (CodeExIDE in codex_gui)       │
│  - Project Management               │
│  - State Management                 │
│  - Execution Orchestration          │
└─────────────────────────────────────┘
              ↓↑
┌─────────────────────────────────────┐
│     Data Tier                       │
│  (interpreter_generator.py)         │
│  - Interpreter Generation           │
│  - Code Execution                   │
│  - Serialization                    │
└─────────────────────────────────────┘
```

### Key Classes

#### CodeExIDE (codex_gui.py)
Main controller class managing application state.

**Responsibilities**:
- Application lifecycle
- UI coordination
- Project management
- Interpreter management
- Code execution

**Key Attributes**:
- `current_project`: Active project path
- `current_interpreter`: Active InterpreterPackage
- `current_file`: Currently edited file
- `interpreter_generator`: Factory for interpreters
- `settings`: User configuration

**Key Methods**:
- `new_project()`: Create new project
- `open_project()`: Load existing project
- `load_interpreter()`: Import language configuration
- `run_code()`: Execute code with active interpreter
- `save_file()`: Persist file to disk

#### CodeExEditor (codex_components.py)
Editor component with syntax highlighting.

**Responsibilities**:
- Code display and editing
- Line number tracking
- Syntax highlighting
- Content management

**Key Methods**:
- `get_content()`: Retrieve editor text
- `set_content(content)`: Set editor text
- `clear()`: Empty editor
- `_update_syntax_highlighting()`: Apply highlighting

#### CodeExConsole (codex_components.py)
Output display component.

**Responsibilities**:
- Execution output display
- Error reporting
- Output formatting and coloring

**Key Methods**:
- `write(text, tag)`: Add output line
- `clear()`: Clear console history

#### CodeExProjectExplorer (codex_components.py)
File/folder navigation component.

**Responsibilities**:
- Project structure visualization
- File browsing
- Tree navigation

**Key Methods**:
- `load_project(path)`: Load project tree
- `refresh()`: Update tree view

### Data Structures

#### Project Structure
```json
{
  "name": "my_language",
  "created": "2024-01-15T10:30:45.123456",
  "interpreter": "my_language_config",
  "description": "My CodeCraft-based language"
}
```

#### Settings Structure
```json
{
  "theme": "light",
  "font_size": 11,
  "recent_projects": ["/path/to/project1", "/path/to/project2"]
}
```

#### Interpreter Package (from interpreter_generator.py)
```python
{
    "name": str,
    "config": LanguageConfig,
    "runtime": LanguageRuntime,
    "metadata": {
        "created": str (ISO format),
        "version": str,
        "keywords_count": int,
        "functions_count": int,
        "operators_count": int
    }
}
```

## Module Dependencies

### Import Graph

```
codex.py
  └─ codex_gui.py
      ├─ codex_components.py
      ├─ src.hb_lcs.language_config
      └─ src.hb_lcs.interpreter_generator
          ├─ src.hb_lcs.language_config
          └─ src.hb_lcs.language_runtime
```

### External Dependencies

**Required**:
- tkinter (Python standard library)
- pathlib (Python standard library)

**Optional**:
- pyyaml (for YAML config support)

## Code Patterns

### Event Handling Pattern

```python
def _on_event(self, event=None):
    """Handle UI event."""
    # Get current state
    state = self._get_state()
    
    # Validate
    if not self._validate():
        messagebox.showwarning("Warning", "Invalid state")
        return
    
    # Process
    result = self._process(state)
    
    # Update UI
    self._update_ui(result)
    
    # Update status
    self.status_label.config(text="Operation complete")
```

### Error Handling Pattern

```python
try:
    result = self.current_interpreter.execute(code)
    
    if result["status"] == "success":
        self.console.write(result["output"], "output")
        self.status_label.config(text="Success")
    else:
        self.console.write("\n".join(result["errors"]), "error")
        self.status_label.config(text="Error")

except Exception as e:
    self.console.write(f"Error: {e}", "error")
    messagebox.showerror("Error", str(e))
```

### File I/O Pattern

```python
def _save_to_file(self, path: str, content: Any):
    """Save content to file with error handling."""
    try:
        path_obj = Path(path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "w") as f:
            f.write(json.dumps(content, indent=2))
        
        self.status_label.config(text=f"Saved: {path_obj.name}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save: {e}")
```

## Extension Points

### Adding New Menu Items

1. **Add to CodeExMenu** (codex_components.py):
```python
def __init__(self, parent, ide):
    # ... existing code ...
    
    # Create menu
    custom_menu = tk.Menu(self, tearoff=False)
    self.add_cascade(label="Custom", menu=custom_menu)
    custom_menu.add_command(label="My Feature", command=ide.my_feature)
```

2. **Add to CodeExIDE** (codex_gui.py):
```python
def my_feature(self):
    """Implement feature."""
    if self._validate():
        result = self._do_something()
        self.status_label.config(text="Feature complete")
    else:
        messagebox.showwarning("Warning", "Cannot execute")
```

### Adding New Components

1. **Create component in codex_components.py**:
```python
class CodeExMyComponent(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        # Build UI
```

2. **Integrate into CodeExIDE._build_ui()**:
```python
self.my_component = CodeExMyComponent(some_paned_window)
some_paned_window.add(self.my_component, weight=1)
```

### Adding New Features

1. **Identify responsibility** (UI, logic, data)
2. **Choose appropriate tier** (presentation, business, data)
3. **Create class/method** with single responsibility
4. **Hook into existing events** or create new event handlers
5. **Add UI** (menu item, button, dialog)
6. **Test integration** with other components

## Testing Strategy

### Unit Testing

Test individual components:
```python
def test_editor_content():
    editor = CodeExEditor(None)
    editor.set_content("test")
    assert editor.get_content() == "test"
```

### Integration Testing

Test component interactions:
```python
def test_project_creation_flow():
    ide = CodeExIDE(root)
    ide.new_project()
    # ... verify project structure ...
```

### Manual Testing Checklist

- [ ] Application launches without errors
- [ ] New project creation works
- [ ] Project opening loads files correctly
- [ ] Interpreter loading accepts valid configs
- [ ] Syntax highlighting updates dynamically
- [ ] Code execution with valid code
- [ ] Error handling with invalid code
- [ ] Console output display
- [ ] File save/load operations
- [ ] Theme toggle works
- [ ] All menu items functional
- [ ] Keyboard shortcuts work
- [ ] Settings persistence
- [ ] Recent projects tracking

## Performance Considerations

### Optimization Tips

1. **Editor Performance**
   - Limit syntax highlighting to visible text
   - Cache highlight patterns
   - Use batch updates for large content

2. **Project Loading**
   - Load directory tree asynchronously
   - Cache file metadata
   - Lazy-load file contents

3. **Execution**
   - Timeout long-running code (30s)
   - Isolate execution context
   - Clean up resources after execution

4. **Memory Management**
   - Limit console history (10,000 lines)
   - Close large files cleanly
   - Cache interpreter instances

## Security Considerations

### Code Execution Isolation

```python
# Each execution gets isolated context
result = interpreter.execute(code, context={})
# Variables don't leak between executions
```

### File Access

- Projects limited to `~/.codex/projects/`
- Interpreters limited to `~/.codecraft/interpreters/`
- No direct file system access from code

### Configuration Validation

- Validate JSON/YAML before loading
- Check interpreter metadata
- Verify language config structure

## Debugging

### Enable Debug Output

```python
# In CodeExIDE.__init__()
self.debug = True

# In methods
if self.debug:
    print(f"DEBUG: {message}")
```

### Common Issues

**Import Errors**
- Verify Python path includes project root
- Check sys.path.insert() in codex.py

**UI Not Responding**
- Long-running operations block UI thread
- Use threading for heavy operations

**File Not Found**
- Verify paths are absolute
- Check directory permissions
- Use pathlib.Path for cross-platform paths

## Version Management

### Semantic Versioning

CodeEx follows semantic versioning: MAJOR.MINOR.PATCH

- **MAJOR**: Breaking changes to architecture
- **MINOR**: New features added
- **PATCH**: Bug fixes

Current Version: 1.0.0

## Documentation Standards

### Code Comments

```python
def method_name(self, param: Type) -> ReturnType:
    """One-line description.
    
    Longer description if needed.
    
    Args:
        param: Description of parameter
    
    Returns:
        Description of return value
    
    Raises:
        ExceptionType: When this occurs
    """
```

### Docstring Format

Use Google-style docstrings for consistency.

## Contributing

### Code Style

- Follow PEP 8
- Max line length: 100 characters
- Use type hints where possible
- Document public methods

### Commit Messages

```
<type>: <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore

### Pull Request Process

1. Create feature branch
2. Make changes with tests
3. Update documentation
4. Submit PR with description
5. Address review feedback
6. Merge when approved

## Troubleshooting Guide

### Module Not Found

```python
# Solution: Check sys.path
import sys
print(sys.path)
# Add project root if needed
sys.path.insert(0, '/path/to/CodeCraft')
```

### Tkinter Not Available

```bash
# Install tkinter
# Ubuntu/Debian:
sudo apt-get install python3-tk

# macOS (with Homebrew):
brew install python-tk

# Windows: Already included with Python
```

### Interpreter Generation Fails

```python
# Verify config file
config = LanguageConfig.load("path/to/config.json")
# Check for required fields
print(config.name)
print(config.keywords)
```

## Related Documentation

- [CODEX_USER_GUIDE.md](./CODEX_USER_GUIDE.md) - User documentation
- [LANGUAGE_DEVELOPMENT_GUIDE.md](./LANGUAGE_DEVELOPMENT_GUIDE.md) - CodeCraft language creation
- [TECHNICAL_REFERENCE.md](../reference/TECHNICAL_REFERENCE.md) - CodeCraft API reference
