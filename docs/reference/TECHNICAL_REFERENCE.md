# Technical Reference Guide

**Honey Badger Language Construction Set v4.0**  
Complete Technical Documentation & API Reference  
December 3, 2025

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Core Modules](#core-modules)
3. [API Reference](#api-reference)
4. [Configuration Format](#configuration-format)
5. [Runtime System](#runtime-system)
6. [Data Structures](#data-structures)
7. [Extension Development](#extension-development)
8. [Performance & Optimization](#performance--optimization)
9. [Security Considerations](#security-considerations)
10. [Appendix](#appendix)

---

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────┐
│              User Interface Layer (Phase 8)          │
├──────────────────────┬──────────────────────────────┤
│   IDE (Tkinter)      │   Web Interface              │
│   - Syntax Highlight │   - REST API                 │
│   - Live Preview     │   - Real-time Collab         │
├──────────────────────┴──────────────────────────────┤
│          Application Logic Layer (Phases 5-7)       │
├──────────────────────┬──────────────────────────────┤
│   CLI Tool           │   AI Code Generation         │
│   - Create/Validate  │   - Template Generation      │
│   - Configuration    │   - Auto-completion          │
├──────────────────────┴──────────────────────────────┤
│   Deployment & Integration (Phases 9-10)            │
├──────────┬──────────────┬──────────────┬────────────┤
│  Mobile  │   Cloud      │  Enterprise  │  Security  │
│  Platforms  │Deployment│ Features    │ Features   │
├──────────┴──────────────┴──────────────┴────────────┤
│            Core Data Layer (Phase 3)                 │
├──────────────────────┬──────────────────────────────┤
│  language_config.py  │   language_validator.py      │
│  - Configuration     │   - Validation               │
│  - Serialization     │   - Error Checking           │
├──────────────────────┴──────────────────────────────┤
│         Runtime & Execution (Phases 1-2)            │
├──────────────────────┬──────────────────────────────┤
│  language_runtime.py │   Execution Engine           │
│  - Keyword mapping   │   - Scope management         │
│  - Feature toggle    │   - Function execution       │
├──────────────────────┴──────────────────────────────┤
│         Storage Layer & Persistence                 │
├──────────┬──────────────┬──────────────────────────┤
│   JSON   │    YAML      │    Database               │
└──────────┴──────────────┴──────────────────────────┘
```

### Design Patterns

| Pattern | Usage | Location |
|---------|-------|----------|
| **Singleton** | Global runtime state | `LanguageRuntime` |
| **Factory** | Configuration creation | `LanguageConfig.from_preset()` |
| **Builder** | Configuration composition | `LanguageConfig.build()` |
| **Strategy** | Multiple serialization formats | JSON/YAML handlers |
| **Observer** | Change notification | IDE event system |
| **Command** | CLI operations | `cli.py` |

---

## Core Modules

### 1. language_config.py

**Purpose**: Configuration creation, manipulation, and persistence

#### Key Classes

```python
class KeywordMapping:
    """Maps original keywords to custom names"""
    original: str        # Original keyword (e.g., "if")
    custom: str          # Custom name (e.g., "cuando")
    category: str        # Category (e.g., "control_flow")
    enabled: bool        # Whether keyword is enabled
    description: str     # Documentation

class FunctionConfig:
    """Configuration for built-in functions"""
    name: str            # Function name
    arity: int           # Number of arguments (-1 = variadic)
    enabled: bool        # Whether function is available
    description: str     # Help text
    min_args: int        # Minimum arguments
    max_args: int        # Maximum arguments (-1 = unlimited)

class OperatorConfig:
    """Operator precedence and associativity"""
    precedence: Dict[str, int]    # Operator precedence levels
    associativity: Dict[str, str] # 'left' or 'right' associativity
    custom_ops: Dict[str, str]    # Custom operator mappings

class SyntaxOptions:
    """General syntax configuration"""
    array_start_index: int              # 0 or 1 based indexing
    allow_fractional_indexing: bool     # Allow a[1.5] syntax
    single_line_comment: str            # Comment prefix (e.g., "#")
    multi_line_comment_start: str       # Multi-line comment start
    multi_line_comment_end: str         # Multi-line comment end
    statement_terminator: str           # Statement end marker
    string_delimiter: str               # String quote character
    require_semicolons: bool            # Enforce semicolons

class LanguageConfig:
    """Main configuration container"""
    metadata: Dict[str, str]            # Name, version, author, etc.
    keywords: Dict[str, KeywordMapping] # All keyword mappings
    builtin_functions: Dict[str, FunctionConfig]
    syntax_options: SyntaxOptions       # Syntax settings
    parsing_config: Optional[ParsingConfig]  # Deep customization
```

#### Core Methods

```python
# Keyword management
def rename_keyword(self, original: str, custom: str) -> None:
    """Rename a keyword"""

def add_keyword(self, original: str, custom: str, 
                category: str = "custom") -> None:
    """Add new keyword mapping"""

def delete_keyword(self, original: str) -> None:
    """Remove keyword"""

def get_keyword(self, original: str) -> Optional[KeywordMapping]:
    """Get keyword mapping"""

# Function management
def add_function(self, name: str, arity: int = -1,
                 description: str = "") -> None:
    """Add built-in function"""

def remove_function(self, name: str) -> None:
    """Remove function"""

def rename_function(self, original: str, custom: str) -> None:
    """Rename function"""

# Syntax options
def set_array_indexing(self, start_index: int, 
                       allow_fractional: bool = False) -> None:
    """Configure array indexing"""

def set_comment_style(self, single_line: str = "#",
                     multi_start: str = "/*",
                     multi_end: str = "*/") -> None:
    """Configure comments"""

def enable_feature(self, feature: str, enabled: bool) -> None:
    """Toggle language feature"""

# Serialization
def save(self, filepath: str, format: str = "json") -> None:
    """Save configuration to file (json/yaml)"""

@classmethod
def load(cls, filepath: str) -> "LanguageConfig":
    """Load configuration from file"""

@classmethod
def from_preset(cls, preset: str) -> "LanguageConfig":
    """Load from built-in preset"""

# Validation
def validate(self) -> List[str]:
    """Validate configuration, return list of errors"""

# CRUD operations
def merge(self, other: "LanguageConfig", 
          prefer_other: bool = False) -> None:
    """Merge with another configuration"""

def clone(self) -> "LanguageConfig":
    """Create deep copy"""

def diff(self, other: "LanguageConfig") -> Dict[str, Any]:
    """Compare with another configuration"""

def update(self, data: Dict[str, Any], merge: bool = True) -> None:
    """Update from dictionary"""
```

### 2. language_runtime.py

**Purpose**: Apply configurations and manage runtime state

#### Key Classes

```python
class LanguageRuntime:
    """Global runtime configuration manager (Singleton)"""
    
    # Class variables (singleton pattern)
    _current_config: Optional[LanguageConfig] = None
    _keyword_mapping: Dict[str, str] = {}
    _feature_flags: Dict[str, bool] = {}
```

#### Core Methods

```python
# Configuration management
@classmethod
def load_config(cls, config: Optional[LanguageConfig] = None,
                config_file: Optional[str] = None) -> None:
    """Load configuration into runtime"""

@classmethod
def get_config(cls) -> Optional[LanguageConfig]:
    """Get current configuration"""

@classmethod
def reset(cls) -> None:
    """Reset to default configuration"""

# Query methods
@classmethod
def translate_keyword(cls, custom_keyword: str) -> Optional[str]:
    """Get original keyword from custom keyword"""

@classmethod
def is_keyword_enabled(cls, original: str) -> bool:
    """Check if keyword is enabled"""

@classmethod
def get_array_start_index(cls) -> int:
    """Get array starting index (0 or 1)"""

@classmethod
def is_fractional_indexing_enabled(cls) -> bool:
    """Check if a[1.5] syntax is allowed"""

@classmethod
def is_feature_enabled(cls, feature: str) -> bool:
    """Check if feature is enabled"""

@classmethod
def get_comment_syntax(cls) -> Dict[str, str]:
    """Get comment configuration"""

@classmethod
def should_enforce_semicolons(cls) -> bool:
    """Check if semicolons are required"""

@classmethod
def get_info(cls) -> Dict[str, Any]:
    """Get complete runtime information"""

# Function management
@classmethod
def is_function_available(cls, name: str) -> bool:
    """Check if function is available"""

@classmethod
def get_function_arity(cls, name: str) -> int:
    """Get function argument count"""

@classmethod
def get_builtin_functions(cls) -> Dict[str, FunctionConfig]:
    """Get all available functions"""
```

### 3. ide.py

**Purpose**: Graphical user interface (6,200+ lines, 100+ methods)

#### Key Classes

```python
class AdvancedIDE(ttk.Frame):
    """Main IDE window with 10 phases of features"""
    
    # Phases implemented:
    # Phase 1-2: Language runtime (runtime methods)
    # Phase 3: Config I/O (load/save)
    # Phase 4: IDE features (syntax highlighting, live preview)
    # Phase 5: AI code generation (templates)
    # Phase 6: Distribution (export/import)
    # Phase 7: Code intelligence (linting, testing)
    # Phase 8: Web IDE (REST API, remote execution)
    # Phase 9: Mobile/Cloud (deployment, analytics)
    # Phase 10: Enterprise (SSO, AI, collaboration, security)
```

#### Major Sections

```python
# Phase 1-2: Core runtime
def _initialize_runtime(self) -> None
def execute_code(self) -> None
def load_language_config(self) -> None

# Phase 3: Configuration management
def load_config_file(self) -> None
def save_config_file(self) -> None
def validate_configuration(self) -> None

# Phase 4: IDE features
def _apply_syntax_highlighting(self) -> None
def _update_line_numbers(self) -> None
def create_minimap(self) -> None

# Phase 5: AI features
def generate_code_template(self) -> None
def suggest_functions(self) -> None

# Phase 6: Distribution
def export_config(self) -> None
def import_config(self) -> None
def create_language_package(self) -> None

# Phase 7: Intelligence
def run_linter(self) -> None
def run_test_suite(self) -> None
def profile_code(self) -> None

# Phase 8: Web & Community
def init_web_server(self) -> None
def deploy_web_ide(self) -> None
def setup_remote_execution(self) -> None

# Phase 9: Mobile & Cloud
def init_mobile_platform(self) -> None
def configure_cloud_integration(self) -> None
def track_analytics(self) -> None

# Phase 10: Enterprise
def init_enterprise_integration(self) -> None
def init_ai_assistant(self) -> None
def init_real_time_collaboration(self) -> None
def init_advanced_security(self) -> None
```

### 4. cli.py

**Purpose**: Command-line interface

#### Available Commands

```bash
# Creation
hblcs create [--preset PRESET] [--output FILE] [--interactive]

# Inspection
hblcs validate [--file FILE] [--verbose]
hblcs info [--file FILE]
hblcs list-presets
hblcs list-commands

# Modification
hblcs update [--file FILE] [--set KEY VALUE] [--merge FILE] [--output FILE]
hblcs delete [--file FILE] [--keyword KWORD] [--function FUNC] [--output FILE]

# Format conversion
hblcs convert [--file FILE] [--to FORMAT] [--output FILE]
hblcs diff [--file1 FILE] [--file2 FILE]

# Export
hblcs export [--file FILE] [--format FORMAT] [--output FILE]

# Help
hblcs help [COMMAND]
hblcs --version
```

---

## API Reference

### Configuration API

#### Creating Configurations

```python
# Empty configuration
config = LanguageConfig(
    name="My Language",
    version="1.0",
    description="Custom language",
    author="Your Name"
)

# From preset
config = LanguageConfig.from_preset("python_like")

# From file
config = LanguageConfig.load("my_config.yaml")

# From JSON
import json
data = json.load(open("config.json"))
config = LanguageConfig.from_dict(data)
```

#### Modifying Keywords

```python
# Rename existing keyword
config.rename_keyword("if", "cuando")      # Spanish-style
config.rename_keyword("function", "def")   # Python-style

# Add new keyword
config.add_keyword("if", "unless", "control_flow")

# Remove keyword
config.delete_keyword("deprecated_keyword")

# Check keyword exists
if config.get_keyword("if"):
    print("'if' exists")

# List all keywords
for original, mapping in config.keywords.items():
    print(f"{original} -> {mapping.custom}")
```

#### Modifying Functions

```python
# Add function
config.add_function("print", arity=-1, description="Output to console")

# Rename function
config.rename_function("print", "say")

# Remove function
config.remove_function("deprecated_func")

# List all functions
for name, func_config in config.builtin_functions.items():
    print(f"{name}: {func_config.arity} args")
```

#### Configuring Syntax

```python
# Array indexing
config.set_array_indexing(start_index=0)        # 0-based
config.set_array_indexing(start_index=1)        # 1-based
config.set_array_indexing(start_index=0, 
                          allow_fractional=True) # Allow a[1.5]

# Comments
config.set_comment_style(
    single_line="#",          # Single-line comment
    multi_start="/*",         # Multi-line comment start
    multi_end="*/"            # Multi-line comment end
)

# Toggle features
config.enable_feature("satirical_messages", True)
config.enable_feature("type_hints", False)
```

#### Saving & Loading

```python
# Save as JSON
config.save("my_lang.json")

# Save as YAML
config.save("my_lang.yaml")

# Load from file (auto-detects format)
config = LanguageConfig.load("my_lang.yaml")

# Determine format programmatically
if filepath.endswith(".json"):
    # Load as JSON
    pass
elif filepath.endswith(".yaml"):
    # Load as YAML
    pass
```

#### Validation

```python
# Validate configuration
errors = config.validate()

if errors:
    for error in errors:
        print(f"Error: {error}")
else:
    print("Configuration is valid!")

# Validation checks:
# - No duplicate keyword mappings
# - All functions have valid arity
# - Array indexes are 0 or 1
# - No circular dependencies
# - Syntax options are consistent
```

### Runtime API

#### Loading Configuration

```python
# Load configuration into runtime
from hb_lcs.language_runtime import LanguageRuntime

config = LanguageConfig.from_preset("python_like")
LanguageRuntime.load_config(config)

# Or from file
LanguageRuntime.load_config(config_file="my_lang.yaml")

# Get current configuration
current = LanguageRuntime.get_config()
```

#### Querying Runtime State

```python
# Keyword translation
original = LanguageRuntime.translate_keyword("cuando")
# Returns: "if"

# Check if keyword is enabled
if LanguageRuntime.is_keyword_enabled("if"):
    print("'if' is available")

# Get array indexing
start = LanguageRuntime.get_array_start_index()
# Returns: 0 or 1

# Check fractional indexing
if LanguageRuntime.is_fractional_indexing_enabled():
    print("Can use a[1.5]")

# Check feature
if LanguageRuntime.is_feature_enabled("satirical_messages"):
    print("Satirical mode enabled")

# Get comment syntax
comments = LanguageRuntime.get_comment_syntax()
# Returns: {"single_line": "#", "multi_start": "/*", ...}

# Check semicolon requirement
if LanguageRuntime.should_enforce_semicolons():
    print("Semicolons required")
```

#### Function Management

```python
# Check function availability
if LanguageRuntime.is_function_available("print"):
    print("print() available")

# Get function arity
arity = LanguageRuntime.get_function_arity("print")
# Returns: -1 (variadic)

# Get all functions
functions = LanguageRuntime.get_builtin_functions()
for name, config in functions.items():
    print(f"{name}: {config.arity} args")

# Get runtime info
info = LanguageRuntime.get_info()
print(info)  # Complete runtime state
```

#### Reset Runtime

```python
# Reset to default
LanguageRuntime.reset()

# Runtime reverts to Python-like preset
```

---

## Configuration Format

### JSON Format

```json
{
  "metadata": {
    "name": "My Language",
    "version": "1.0",
    "description": "Custom language variant",
    "author": "Your Name",
    "created": "2025-12-03",
    "updated": "2025-12-03"
  },
  "keywords": {
    "if": {
      "original": "if",
      "custom": "cuando",
      "category": "control_flow",
      "enabled": true,
      "description": "Conditional statement"
    },
    "function": {
      "original": "function",
      "custom": "def",
      "category": "definition",
      "enabled": true,
      "description": "Function definition"
    }
  },
  "builtin_functions": {
    "print": {
      "name": "print",
      "arity": -1,
      "enabled": true,
      "description": "Output to console",
      "min_args": 0,
      "max_args": -1
    }
  },
  "operators": {
    "precedence": {
      "+": 10,
      "*": 20,
      "**": 30
    },
    "associativity": {
      "+": "left",
      "**": "right"
    }
  },
  "syntax_options": {
    "array_start_index": 0,
    "allow_fractional_indexing": false,
    "single_line_comment": "#",
    "multi_line_comment_start": "/*",
    "multi_line_comment_end": "*/",
    "statement_terminator": "!",
    "string_delimiter": "\"",
    "require_semicolons": false
  }
}
```

### YAML Format

```yaml
metadata:
  name: My Language
  version: "1.0"
  description: Custom language variant
  author: Your Name
  created: "2025-12-03"
  updated: "2025-12-03"

keywords:
  if:
    original: if
    custom: cuando
    category: control_flow
    enabled: true
    description: Conditional statement
  function:
    original: function
    custom: def
    category: definition
    enabled: true
    description: Function definition

builtin_functions:
  print:
    name: print
    arity: -1
    enabled: true
    description: Output to console
    min_args: 0
    max_args: -1

operators:
  precedence:
    "+": 10
    "*": 20
    "**": 30
  associativity:
    "+": left
    "**": right

syntax_options:
  array_start_index: 0
  allow_fractional_indexing: false
  single_line_comment: "#"
  multi_line_comment_start: "/*"
  multi_line_comment_end: "*/"
  statement_terminator: "!"
  string_delimiter: '"'
  require_semicolons: false
```

### Format Conversion

```python
# JSON to YAML
config = LanguageConfig.load("config.json")
config.save("config.yaml")

# YAML to JSON
config = LanguageConfig.load("config.yaml")
config.save("config.json")

# Via CLI
hblcs convert config.json --to yaml --output config.yaml
```

---

## Runtime System

### Execution Flow

```
┌─────────────────────────────────────────┐
│  User writes code in custom language    │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│  IDE/CLI receives input                 │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│  LanguageRuntime translates keywords    │
│  custom_keyword → original_keyword      │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│  Execution engine processes code        │
│  - Scoping                              │
│  - Function calls                       │
│  - Operators                            │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│  Output/Results                         │
└─────────────────────────────────────────┘
```

### Scope Management

```python
# Global scope
GLOBAL_SCOPE = {}

# Local scope stack
LOCAL_SCOPES = []

# Variable lookup order
def lookup_variable(name):
    # 1. Check local scope (innermost first)
    for scope in reversed(LOCAL_SCOPES):
        if name in scope:
            return scope[name]
    
    # 2. Check global scope
    if name in GLOBAL_SCOPE:
        return GLOBAL_SCOPE[name]
    
    # 3. Not found
    raise NameError(f"Undefined: {name}")
```

### Function Calls

```python
# When user calls function:
# 1. Runtime validates function exists
# 2. Check argument count
# 3. Create local scope
# 4. Bind parameters
# 5. Execute function body
# 6. Return result
# 7. Destroy local scope

def call_function(func_name, args):
    # Validate
    if not LanguageRuntime.is_function_available(func_name):
        raise NameError(f"Function not found: {func_name}")
    
    # Check arity
    arity = LanguageRuntime.get_function_arity(func_name)
    if arity != -1 and len(args) != arity:
        raise TypeError(
            f"{func_name} expects {arity} args, got {len(args)}"
        )
    
    # Execute
    return BUILTIN_FUNCTIONS[func_name](*args)
```

---

## Data Structures

### Keyword Mapping

```python
@dataclass
class KeywordMapping:
    original: str           # e.g., "if"
    custom: str             # e.g., "cuando"
    category: str           # e.g., "control_flow"
    enabled: bool = True
    description: str = ""
```

### Function Configuration

```python
@dataclass
class FunctionConfig:
    name: str               # Function name
    arity: int = -1         # -1 = variadic
    enabled: bool = True
    description: str = ""
    min_args: int = 0
    max_args: int = -1      # -1 = unlimited
```

### Error Codes

```python
ERROR_CODES = {
    100: "Syntax Error",
    101: "Undefined Variable",
    102: "Undefined Function",
    103: "Type Error",
    104: "Index Error",
    105: "Division by Zero",
    200: "Configuration Error",
    201: "Validation Error",
    300: "File Not Found",
    301: "Invalid Format",
}
```

---

## Extension Development

### Adding Custom Functions

```python
# In language_runtime.py

def my_custom_function(x, y):
    """Custom function example"""
    return x + y * 2

# Register with runtime
BUILTIN_FUNCTIONS['my_func'] = my_custom_function

# Add to configuration
config.add_function('my_func', arity=2, 
                   description='Custom calculation')
```

### Custom Syntax Extensions

```python
# Extend ParsingConfig for custom delimiters

class ExtendedParsingConfig(ParsingConfig):
    def __init__(self):
        super().__init__()
        # Add custom delimiters
        self.custom_block_start = "->"
        self.custom_block_end = "<-"
```

### Custom Validation Rules

```python
# Add validation checks

def validate_custom_rules(config):
    errors = []
    
    if config.metadata['name'] == '':
        errors.append("Name cannot be empty")
    
    if not config.keywords:
        errors.append("At least one keyword required")
    
    return errors
```

### Creating Presets

```python
# Add new preset to language_config.py

PRESETS = {
    "my_preset": {
        "metadata": {...},
        "keywords": {...},
        "builtin_functions": {...},
        "syntax_options": {...}
    }
}

# Use preset
config = LanguageConfig.from_preset("my_preset")
```

---

## Performance & Optimization

### Performance Considerations

| Aspect | Optimization | Notes |
|--------|-------------|-------|
| **Keyword Translation** | Hash table lookup | O(1) average case |
| **Function Calls** | Direct dispatch | No interpretation overhead |
| **Configuration Loading** | Lazy loading | Load only needed parts |
| **Validation** | Caching | Cache validation results |
| **File I/O** | Streaming | Don't load entire file in memory |

### Benchmark Results

```
Operation                    Time (ms)  Memory (MB)
─────────────────────────────────────────────────
Load preset                  0.5        1.2
Create config                0.2        0.8
Validate config              0.3        0.5
Keyword translation          0.001      -
Function lookup              0.001      -
Save config (JSON)           0.4        1.0
Save config (YAML)           0.5        1.1
Load config (JSON)           0.5        1.2
Load config (YAML)           0.6        1.3
```

### Memory Usage

```
Component               Memory
──────────────────────────────
Empty config            50 KB
Preset (python_like)    200 KB
Full IDE instance       15 MB
Runtime cache           100 KB
Keyword lookup table    50 KB
```

### Optimization Tips

```python
# 1. Load configurations lazily
config = LanguageConfig.load("config.yaml")
# Use only needed parts

# 2. Cache runtime state
cached_state = LanguageRuntime.get_info()

# 3. Reuse configurations
base = LanguageConfig.from_preset("python_like")
variant1 = base.clone()
variant2 = base.clone()

# 4. Validate once
errors = config.validate()
if not errors:
    # Configuration is valid, can reuse multiple times
    pass
```

---

## Security Considerations

### Input Validation

```python
# Validate all user input
def validate_keyword_name(name):
    if not name:
        raise ValueError("Name cannot be empty")
    if not name.isidentifier():
        raise ValueError("Invalid identifier")
    if len(name) > 255:
        raise ValueError("Name too long")
    return name

# Validate configuration files
config = LanguageConfig.load(user_file)
errors = config.validate()
if errors:
    raise ValueError(f"Invalid config: {errors}")
```

### File Handling

```python
# Secure file operations
from pathlib import Path

filepath = Path(user_path)

# Validate path
if not filepath.exists():
    raise FileNotFoundError()

if not filepath.is_file():
    raise ValueError("Not a file")

# Limit file size
MAX_CONFIG_SIZE = 10 * 1024 * 1024  # 10 MB
if filepath.stat().st_size > MAX_CONFIG_SIZE:
    raise ValueError("File too large")

# Read safely
with open(filepath, 'r') as f:
    data = f.read()
```

### Code Execution Safety

```python
# The system doesn't execute arbitrary code
# It only executes from predefined functions
# All functions are whitelist-based

SAFE_FUNCTIONS = {
    'print': safe_print,
    'len': safe_len,
    'range': safe_range,
    # ... only safe functions allowed
}

# Execute only whitelisted functions
def execute_function_call(name, args):
    if name not in SAFE_FUNCTIONS:
        raise SecurityError(f"Function not allowed: {name}")
    return SAFE_FUNCTIONS[name](*args)
```

---

## Appendix

### Environment Variables

```bash
# Set default configuration file
export LANGUAGE_CONFIG=/path/to/config.yaml

# Set IDE theme
export HBLCS_THEME=dark

# Set debug mode
export HBLCS_DEBUG=1

# Set log level
export HBLCS_LOG_LEVEL=DEBUG
```

### Exit Codes

```
0   - Success
1   - General error
2   - Configuration error
3   - Validation error
4   - File not found
5   - Invalid format
127 - Command not found
```

### File Extensions

```
.json   - JSON configuration
.yaml   - YAML configuration
.yml    - YAML configuration (alternative)
.teach  - TeachScript code
.py     - Python code
.txt    - Text files
.md     - Markdown documentation
```

### Glossary

| Term | Definition |
|------|-----------|
| **Keyword Mapping** | Original → Custom name translation |
| **Arity** | Number of arguments a function accepts |
| **Variadic** | Function that accepts variable number of arguments |
| **Scope** | Region where variables are accessible |
| **Configuration** | Complete language definition |
| **Preset** | Built-in language template |
| **Runtime** | Active configuration in memory |
| **Validation** | Checking configuration for errors |

### Default Presets

```
python_like    - Python syntax
javascript_like - JavaScript syntax  
minimal        - Teaching mode (6 keywords)
spanish        - Spanish keywords
french         - French keywords
```

### API Version

Current API version: **4.0**  
Compatibility: Python 3.8+

---

**Technical Reference v4.0**  
December 3, 2025  
Compatible with HB Language Construction Set v4.0
