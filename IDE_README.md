# Honey Badger Language Construction Set - IDE

A graphical IDE for the Honey Badger Language Construction Set, adapted from the Time_Warp project.

## Features

- **Code Editor**
  - Syntax highlighting
  - Line numbers
  - Undo/Redo
  - Find & Replace
  - Go to Line
  - Word wrap toggle

- **Configuration Management**
  - Load language configurations (JSON/YAML)
  - Validate configurations
  - View configuration info in console
  - Reload/Unload configs
  - Example configurations included

- **Themes**
  - Light theme
  - Dark theme
  - Customizable font sizes

- **File Operations**
  - New/Open/Save/Save As
  - Support for Python, JSON, YAML files

## Usage

### Starting the IDE

```bash
python3 ide.py
```

Or make it executable:
```bash
chmod +x ide.py
./ide.py
```

### Loading a Configuration

1. **Via Menu**: `Config` → `Load Config...`
2. **Via Keyboard**: Press `F5`
3. **Via Toolbar**: Click "Load Config" button
4. **Via Examples Menu**: `Examples` → Select an example

### Working with Configurations

Once a configuration is loaded:
- View info in the right panel
- Configuration name appears in window title
- Use `Config` → `Validate Config` to check for errors
- Use `Config` → `Reload Current` to reload after external changes

### Keyboard Shortcuts

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

### Settings

Settings are automatically saved in `~/.hb_lcs/settings.json` and include:
- Theme preference
- Font sizes
- Window geometry
- Last loaded configuration
- Show line numbers preference

To change settings: `Edit` → `Preferences...`

## Example Workflow

1. Start the IDE
2. Load a language configuration (e.g., `Examples` → `Python-Like`)
3. View the configuration details in the right panel
4. Edit your code in the left panel
5. Save your work with `Ctrl+S`

## Architecture

The IDE consists of:
- **HBLCS_IDE**: Main application class
  - Editor pane (left): tk.Text with line numbers
  - Console pane (right): Read-only display for config info
  - Menu bar with File/Edit/Config/Examples/View/Help
  - Toolbar for quick access
  - Status bar showing cursor position

## Integration with Language Construction Set

The IDE integrates with:
- `language_config.py`: Loads and validates configurations
- `language_runtime.py`: Displays runtime information
- Example configurations in `examples/` directory

## Customization

### Adding More Examples

Place configuration files in the `examples/` directory and add menu items in the `_build_ui()` method:

```python
examples_menu.add_command(
    label="My Config",
    command=lambda: self._load_example("my_config.yaml")
)
```

### Changing Theme Colors

Edit the `_apply_settings()` method to customize dark/light theme colors.

### Adding Syntax Highlighting

Currently the IDE has basic support. To add language-specific highlighting, extend the `_on_editor_change()` method with pattern matching.

## Troubleshooting

**IDE won't start**
- Ensure Python 3.7+ is installed
- Check that tkinter is available: `python3 -m tkinter`

**Configuration won't load**
- Verify the file exists and is valid JSON/YAML
- Check the error message in the popup dialog
- Use `langconfig.py validate` to validate from command line

**Settings not saving**
- Check write permissions for `~/.hb_lcs/`
- Settings save automatically on exit

## Credits

Adapted from the Time_Warp project's tkinter IDE implementation.
