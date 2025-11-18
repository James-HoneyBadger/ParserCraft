# Honey Badger Language Construction Set - Technical Reference Manual

**Technical Reference**  
Version 1.0 | November 2025

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Core Modules](#core-modules)
3. [API Reference](#api-reference)
4. [Data Structures](#data-structures)
5. [Configuration Format](#configuration-format)
6. [Runtime System](#runtime-system)
7. [Extension Development](#extension-development)
8. [Performance Considerations](#performance-considerations)

---

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────┐
│                 User Interface Layer                 │
├──────────────────────┬──────────────────────────────┤
│   ide.py (GUI)       │   langconfig.py (CLI)        │
├──────────────────────┴──────────────────────────────┤
│              Application Logic Layer                 │
├──────────────────────┬──────────────────────────────┤
│  language_runtime.py │   Demo Scripts               │
├──────────────────────┴──────────────────────────────┤
│                Core Data Layer                       │
├─────────────────────────────────────────────────────┤
│           language_config.py (Core Library)          │
├─────────────────────────────────────────────────────┤
│              Storage/Serialization                   │
├──────────────────────┬──────────────────────────────┤
│  JSON Files          │   YAML Files                 │
└──────────────────────┴──────────────────────────────┘
```

### Design Patterns

**Singleton Pattern**: `LanguageRuntime`
- Ensures single global runtime instance
- Thread-safe initialization
- Global configuration state

**Data Class Pattern**: Configuration objects
- Immutable-by-default structures
- Type-safe attributes
- Validation on construction

**Strategy Pattern**: Serialization
- JSON vs YAML strategies
- Format-agnostic loading
- Automatic format detection

**Builder Pattern**: Configuration creation
- Fluent API for configuration
- Method chaining support
- Preset templates

---

## Core Modules

### language_config.py

**Purpose**: Core configuration management library

**Size**: ~650 lines, 24KB

**Key Classes**:
- `KeywordMapping` - Keyword translation mappings
- `FunctionConfig` - Built-in function definitions
- `OperatorConfig` - Operator precedence and associativity
- `ParsingConfig` - Comment and string parsing rules
- `SyntaxOptions` - Syntax feature flags
- `LanguageConfig` - Main configuration container

**Dependencies**:
- `dataclasses` (stdlib)
- `json` (stdlib)
- `yaml` (optional, for YAML support)
- `typing` (stdlib)

**Thread Safety**: Read-safe, write operations not thread-safe

### language_runtime.py

**Purpose**: Runtime singleton for configuration application

**Size**: ~390 lines, 12KB

**Key Class**:
- `LanguageRuntime` - Singleton runtime manager

**Responsibilities**:
- Load and apply configurations
- Maintain runtime state
- Provide keyword translation
- Environment variable integration

**Thread Safety**: Singleton initialization is thread-safe

### langconfig.py

**Purpose**: Command-line interface

**Size**: ~650 lines, 21KB

**Commands**: 10 subcommands via argparse

**Dependencies**:
- `argparse` (stdlib)
- `language_config`
- `sys`, `os`, `pathlib` (stdlib)

**Exit Codes**:
- 0 - Success
- 1 - Error (validation failed, file not found, etc.)
- 2 - Invalid arguments

### ide.py

**Purpose**: Graphical user interface

**Size**: ~750 lines, 26KB

**Key Class**:
- `HBLCS_IDE` - Main IDE application (inherits ttk.Frame)

**Dependencies**:
- `tkinter`, `ttk` (stdlib)
- `language_config`
- `language_runtime`
- `json` (for settings persistence)

**Settings Storage**: `~/.hb_lcs/settings.json`

---

## API Reference

### LanguageConfig Class

#### Constructor

```python
LanguageConfig(
    name: str = "Custom Language",
    version: str = "1.0",
    keywords: Optional[Dict[str, str]] = None,
    builtin_functions: Optional[Dict[str, FunctionConfig]] = None,
    operators: Optional[Dict[str, OperatorConfig]] = None,
    parsing: Optional[ParsingConfig] = None,
    syntax: Optional[SyntaxOptions] = None
)
```

**Parameters**:
- `name`: Language configuration name
- `version`: Version string (semantic versioning recommended)
- `keywords`: Dictionary of keyword mappings (original → custom)
- `builtin_functions`: Dictionary of function configurations
- `operators`: Dictionary of operator configurations
- `parsing`: Parsing configuration object
- `syntax`: Syntax options object

**Returns**: New `LanguageConfig` instance

**Example**:
```python
config = LanguageConfig(
    name="My Language",
    version="1.0"
)
```

#### Class Methods

##### from_preset()

```python
@classmethod
from_preset(cls, preset_name: str) -> LanguageConfig
```

**Parameters**:
- `preset_name`: Name of preset ("python_like", "javascript_like", "minimal", "teaching_mode")

**Returns**: New `LanguageConfig` initialized from preset

**Raises**: `ValueError` if preset not found

**Example**:
```python
config = LanguageConfig.from_preset("python_like")
```

##### load()

```python
@classmethod
load(cls, filepath: str) -> LanguageConfig
```

**Parameters**:
- `filepath`: Path to JSON or YAML configuration file

**Returns**: `LanguageConfig` loaded from file

**Raises**:
- `FileNotFoundError` if file doesn't exist
- `ImportError` if YAML support needed but not available
- `ValueError` if file format invalid

**Example**:
```python
config = LanguageConfig.load("my_config.yaml")
```

##### from_dict()

```python
@classmethod
from_dict(cls, data: Dict[str, Any]) -> LanguageConfig
```

**Parameters**:
- `data`: Dictionary representation of configuration

**Returns**: `LanguageConfig` instance

**Example**:
```python
data = {
    "name": "Test",
    "version": "1.0",
    "keywords": {"if": "si"}
}
config = LanguageConfig.from_dict(data)
```

#### Instance Methods

##### rename_keyword()

```python
def rename_keyword(self, original: str, custom: str) -> None
```

**Parameters**:
- `original`: Original keyword name
- `custom`: Custom replacement name

**Raises**: `ValueError` if original keyword not found

**Mutates**: Modifies `self.keywords`

**Example**:
```python
config.rename_keyword("if", "cuando")
```

##### add_function()

```python
def add_function(
    self,
    original_name: str,
    custom_name: str,
    min_args: int = 0,
    max_args: int = -1,
    description: str = ""
) -> None
```

**Parameters**:
- `original_name`: Original function name (key)
- `custom_name`: Custom function name
- `min_args`: Minimum argument count (default: 0)
- `max_args`: Maximum argument count (-1 for unlimited, default: -1)
- `description`: Function description

**Mutates**: Adds to `self.builtin_functions`

**Example**:
```python
config.add_function("sqrt", "raiz", min_args=1, max_args=1)
```

##### remove_function()

```python
def remove_function(self, name: str) -> None
```

**Parameters**:
- `name`: Function name to remove

**Raises**: `ValueError` if function not found

**Mutates**: Removes from `self.builtin_functions`

**Example**:
```python
config.remove_function("eval")
```

##### set_comment_style()

```python
def set_comment_style(self, comment_str: str) -> None
```

**Parameters**:
- `comment_str`: Comment prefix string (e.g., "#", "//", "--")

**Mutates**: Updates `self.parsing.comment_style`

**Example**:
```python
config.set_comment_style("//")
```

##### set_array_indexing()

```python
def set_array_indexing(self, base: int, one_based: bool) -> None
```

**Parameters**:
- `base`: Array index base (0 or 1)
- `one_based`: Whether indexing is 1-based (True) or 0-based (False)

**Raises**: `ValueError` if base not 0 or 1

**Mutates**: Updates `self.syntax.array_index_base` and `array_index_one_based`

**Example**:
```python
config.set_array_indexing(0, False)  # 0-based
config.set_array_indexing(1, True)   # 1-based
```

##### validate()

```python
def validate(self) -> List[str]
```

**Returns**: List of validation error strings (empty if valid)

**Example**:
```python
errors = config.validate()
if errors:
    print("Validation errors:", errors)
```

##### save()

```python
def save(self, filepath: str) -> None
```

**Parameters**:
- `filepath`: Path to save configuration (.json or .yaml)

**Raises**:
- `ImportError` if YAML support needed but not available
- `OSError` if file cannot be written

**Example**:
```python
config.save("my_config.yaml")
```

##### to_dict()

```python
def to_dict(self) -> Dict[str, Any]
```

**Returns**: Dictionary representation of configuration

**Example**:
```python
data = config.to_dict()
```

##### clone()

```python
def clone(self) -> LanguageConfig
```

**Returns**: Deep copy of configuration

**Example**:
```python
config2 = config.clone()
```

---

### LanguageRuntime Class

#### Class Methods

##### load_config()

```python
@classmethod
def load_config(cls, config: LanguageConfig) -> None
```

**Parameters**:
- `config`: LanguageConfig to load into runtime

**Mutates**: Sets global runtime configuration

**Thread Safety**: Not thread-safe during load

**Example**:
```python
LanguageRuntime.load_config(config)
```

##### get_keyword()

```python
@classmethod
def get_keyword(cls, original: str) -> str
```

**Parameters**:
- `original`: Original keyword name

**Returns**: Custom keyword name or original if not found

**Example**:
```python
custom = LanguageRuntime.get_keyword("if")
```

##### is_feature_enabled()

```python
@classmethod
def is_feature_enabled(cls, feature: str) -> bool
```

**Parameters**:
- `feature`: Feature flag name

**Returns**: True if feature enabled, False otherwise

**Example**:
```python
if LanguageRuntime.is_feature_enabled("satirical_keywords"):
    # ...
```

##### get_info()

```python
@classmethod
def get_info(cls) -> str
```

**Returns**: Formatted string with runtime configuration information

**Example**:
```python
info = LanguageRuntime.get_info()
print(info)
```

##### reset()

```python
@classmethod
def reset(cls) -> None
```

**Mutates**: Resets runtime to default state

**Example**:
```python
LanguageRuntime.reset()
```

---

## Data Structures

### KeywordMapping

```python
@dataclass
class KeywordMapping:
    original: str
    custom: str
    category: str = "general"
```

**Fields**:
- `original`: Original keyword (immutable)
- `custom`: Custom replacement keyword
- `category`: Keyword category for grouping

**Categories**: `control_flow`, `declaration`, `operator`, `literal`, `module`, `general`

### FunctionConfig

```python
@dataclass
class FunctionConfig:
    name: str
    min_args: int = 0
    max_args: int = -1
    enabled: bool = True
    description: str = ""
```

**Fields**:
- `name`: Function name in custom language
- `min_args`: Minimum number of arguments
- `max_args`: Maximum arguments (-1 = unlimited)
- `enabled`: Whether function is enabled
- `description`: Function documentation

### OperatorConfig

```python
@dataclass
class OperatorConfig:
    symbol: str
    precedence: int
    associativity: str = "left"
```

**Fields**:
- `symbol`: Operator symbol (e.g., "+", "==")
- `precedence`: Precedence level (higher = binds tighter)
- `associativity`: "left" or "right"

**Precedence Levels** (typical):
- 1: Logical OR
- 2: Logical AND
- 3: Equality/comparison
- 4: Addition/subtraction
- 5: Multiplication/division
- 6: Exponentiation
- 7: Unary operators

### ParsingConfig

```python
@dataclass
class ParsingConfig:
    comment_style: str = "#"
    string_delimiters: List[str] = field(default_factory=lambda: ['"'])
    multiline_comment_start: Optional[str] = None
    multiline_comment_end: Optional[str] = None
```

**Fields**:
- `comment_style`: Single-line comment prefix
- `string_delimiters`: List of string delimiter characters
- `multiline_comment_start`: Start of multi-line comment
- `multiline_comment_end`: End of multi-line comment

### SyntaxOptions

```python
@dataclass
class SyntaxOptions:
    array_index_base: int = 0
    array_index_one_based: bool = False
    function_keyword_required: bool = True
    parentheses_required: bool = True
    block_end_required: bool = False
    statement_separator: Optional[str] = None
```

**Fields**:
- `array_index_base`: Starting index for arrays (0 or 1)
- `array_index_one_based`: Whether 1-based indexing
- `function_keyword_required`: Whether `function` keyword needed
- `parentheses_required`: Whether function calls need `()`
- `block_end_required`: Whether blocks need explicit end
- `statement_separator`: Statement separator (`;`, `\n`, etc.)

---

## Configuration Format

### JSON Format

```json
{
  "name": "My Language",
  "version": "1.0",
  "keywords": {
    "if": "cuando",
    "else": "sino",
    "while": "mientras"
  },
  "builtin_functions": {
    "print": {
      "name": "imprimir",
      "min_args": 0,
      "max_args": -1,
      "enabled": true,
      "description": "Print to console"
    }
  },
  "operators": {
    "plus": {
      "symbol": "+",
      "precedence": 4,
      "associativity": "left"
    }
  },
  "parsing": {
    "comment_style": "#",
    "string_delimiters": ["\"", "'"],
    "multiline_comment_start": "/*",
    "multiline_comment_end": "*/"
  },
  "syntax": {
    "array_index_base": 0,
    "array_index_one_based": false,
    "function_keyword_required": true,
    "parentheses_required": true,
    "block_end_required": false,
    "statement_separator": null
  }
}
```

### YAML Format

```yaml
name: "My Language"
version: "1.0"

keywords:
  if: "cuando"
  else: "sino"
  while: "mientras"

builtin_functions:
  print:
    name: "imprimir"
    min_args: 0
    max_args: -1
    enabled: true
    description: "Print to console"

operators:
  plus:
    symbol: "+"
    precedence: 4
    associativity: "left"

parsing:
  comment_style: "#"
  string_delimiters:
    - "\""
    - "'"
  multiline_comment_start: "/*"
  multiline_comment_end: "*/"

syntax:
  array_index_base: 0
  array_index_one_based: false
  function_keyword_required: true
  parentheses_required: true
  block_end_required: false
  statement_separator: null
```

### Schema Validation

**Required Fields**:
- `name` (string)
- `version` (string)

**Optional Fields**:
- `keywords` (dict)
- `builtin_functions` (dict)
- `operators` (dict)
- `parsing` (object)
- `syntax` (object)

**Type Constraints**:
- Keywords must be strings
- Function min_args/max_args must be integers
- Precedence must be integer
- Associativity must be "left" or "right"
- Array index base must be 0 or 1

---

## Runtime System

### Initialization Sequence

1. **Import Module**: `from language_runtime import LanguageRuntime`
2. **Load Configuration**: `LanguageRuntime.load_config(config)`
3. **Apply Settings**: Runtime applies keyword mappings
4. **Ready State**: Runtime ready for queries

### State Management

**Global State**:
```python
_instance = None  # Singleton instance
_config = None    # Current configuration
_initialized = False
```

**State Transitions**:
```
UNINITIALIZED → load_config() → CONFIGURED
CONFIGURED → reset() → UNINITIALIZED
CONFIGURED → load_config() → CONFIGURED (overwrite)
```

### Environment Variables

**Supported Variables**:
- `LANGUAGE_CONFIG`: Path to auto-load configuration
- `LANGUAGE_NAME`: Override configuration name
- `LANGUAGE_STRICT`: Enable strict mode

**Usage**:
```bash
export LANGUAGE_CONFIG=/path/to/config.yaml
python my_program.py  # Auto-loads config
```

### Thread Safety

**Thread-Safe Operations**:
- ✓ Reading configuration
- ✓ Keyword lookup
- ✓ Feature flag checks
- ✓ get_info()

**Not Thread-Safe**:
- ✗ load_config()
- ✗ reset()
- ✗ Modifying configuration

**Recommendation**: Load configuration once at startup before spawning threads.

---

## Extension Development

### Creating Custom Presets

```python
# In language_config.py, add to _get_preset_config()

def _get_preset_config(preset_name: str) -> Dict[str, Any]:
    presets = {
        # ... existing presets ...
        
        "my_custom_preset": {
            "name": "My Custom Preset",
            "version": "1.0",
            "keywords": {
                "if": "custom_if",
                "else": "custom_else",
                # ...
            },
            # ... rest of configuration
        }
    }
    
    if preset_name not in presets:
        raise ValueError(f"Unknown preset: {preset_name}")
    
    return presets[preset_name]
```

### Adding Custom Validation Rules

```python
class LanguageConfig:
    def validate(self) -> List[str]:
        errors = []
        
        # Existing validation...
        
        # Add custom validation
        if "forbidden_keyword" in self.keywords:
            errors.append("Keyword 'forbidden_keyword' is not allowed")
        
        # Custom function validation
        for fname, fconfig in self.builtin_functions.items():
            if fconfig.max_args < fconfig.min_args:
                errors.append(
                    f"Function '{fname}': max_args < min_args"
                )
        
        return errors
```

### Custom Export Formats

```python
def export_to_xml(config: LanguageConfig) -> str:
    """Export configuration to XML format"""
    xml = ['<?xml version="1.0"?>']
    xml.append('<language>')
    xml.append(f'  <name>{config.name}</name>')
    xml.append(f'  <version>{config.version}</version>')
    
    xml.append('  <keywords>')
    for orig, custom in config.keywords.items():
        xml.append(f'    <keyword original="{orig}" custom="{custom}"/>')
    xml.append('  </keywords>')
    
    xml.append('</language>')
    return '\n'.join(xml)

# Usage
xml_output = export_to_xml(config)
```

### Plugin System Design

```python
class ConfigPlugin:
    """Base class for configuration plugins"""
    
    def on_load(self, config: LanguageConfig) -> None:
        """Called when configuration is loaded"""
        pass
    
    def on_validate(self, config: LanguageConfig) -> List[str]:
        """Called during validation, returns errors"""
        return []
    
    def on_save(self, config: LanguageConfig) -> None:
        """Called before saving configuration"""
        pass

# Example plugin
class LoggingPlugin(ConfigPlugin):
    def on_load(self, config: LanguageConfig) -> None:
        print(f"Loading configuration: {config.name}")
    
    def on_validate(self, config: LanguageConfig) -> List[str]:
        errors = []
        if len(config.keywords) < 5:
            errors.append("Warning: Less than 5 keywords defined")
        return errors
```

---

## Performance Considerations

### Memory Usage

**Configuration Object Size**:
- Small config (~10 keywords): ~5-10 KB
- Medium config (~50 keywords): ~20-50 KB
- Large config (~200 keywords): ~100-200 KB

**Memory Optimization**:
```python
# Use __slots__ for memory efficiency
@dataclass
class KeywordMapping:
    __slots__ = ['original', 'custom', 'category']
    original: str
    custom: str
    category: str = "general"
```

### Load Performance

**Benchmark Results** (typical):
- JSON load: ~1-5 ms for medium config
- YAML load: ~5-20 ms for medium config
- Validation: ~1-3 ms for medium config

**Optimization Tips**:
1. **Cache loaded configurations**
   ```python
   _config_cache = {}
   
   def load_cached(filepath: str) -> LanguageConfig:
       if filepath not in _config_cache:
           _config_cache[filepath] = LanguageConfig.load(filepath)
       return _config_cache[filepath]
   ```

2. **Use JSON for performance-critical loads**
   - JSON parsing is faster than YAML
   - Consider converting YAML to JSON for production

3. **Lazy load optional features**
   - Don't load all presets at startup
   - Load on demand

### Serialization Performance

**JSON vs YAML**:
- JSON save: ~1-3 ms
- YAML save: ~5-15 ms
- JSON load: ~1-5 ms
- YAML load: ~5-20 ms

**Recommendation**: Use JSON for high-performance scenarios, YAML for human readability.

### Runtime Query Performance

**Keyword Lookup**: O(1) dictionary lookup
**Feature Check**: O(1) attribute access
**Validation**: O(n) where n = number of keywords + functions

**Optimization**:
```python
# Pre-compile validation rules
class LanguageConfig:
    def __post_init__(self):
        self._validation_cache = None
    
    def validate(self) -> List[str]:
        if self._validation_cache is not None:
            return self._validation_cache
        
        errors = self._do_validation()
        self._validation_cache = errors
        return errors
```

---

## Appendix A: Error Codes

### Validation Errors

| Code | Message | Cause |
|------|---------|-------|
| V001 | Missing required field | name or version missing |
| V002 | Invalid type | Field has wrong type |
| V003 | Invalid value | Value outside valid range |
| V004 | Duplicate key | Keyword/function defined twice |
| V005 | Circular reference | Keyword maps to itself |

### Runtime Errors

| Code | Message | Cause |
|------|---------|-------|
| R001 | Configuration not loaded | Accessing runtime before load |
| R002 | Invalid keyword | Keyword not in configuration |
| R003 | Feature not available | Feature flag disabled |

### File I/O Errors

| Code | Message | Cause |
|------|---------|-------|
| F001 | File not found | Configuration file missing |
| F002 | Parse error | Invalid JSON/YAML syntax |
| F003 | Write error | Cannot write to file |
| F004 | Format unsupported | Unknown file extension |

## Appendix B: Version History

**v1.0 (November 2025)**
- Initial release
- Core configuration system
- CLI tool with 10 commands
- GUI IDE
- 6 example configurations
- Complete documentation

**Future Roadmap**:
- v1.1: Plugin system
- v1.2: Advanced validation rules
- v1.3: Configuration inheritance
- v2.0: Visual configuration editor

## Appendix C: API Compatibility

**Backwards Compatibility Guarantee**:
- Major version (1.x → 2.x): Breaking changes allowed
- Minor version (1.1 → 1.2): No breaking changes
- Patch version (1.0.0 → 1.0.1): Bug fixes only

**Deprecated APIs**:
- None currently

---

**End of Technical Reference Manual**

For user-focused documentation, see the [User Guide](USER_GUIDE.md).  
For language development tutorials, see the [Language Development Guide](LANGUAGE_DEVELOPMENT_GUIDE.md).
