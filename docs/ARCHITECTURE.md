# ParserCraft Architecture Documentation

**Version 2.0** | System Design and Implementation | January 2026

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Three-Layer Architecture](#three-layer-architecture)
3. [Core Components](#core-components)
4. [Data Flow](#data-flow)
5. [Design Patterns](#design-patterns)
6. [Module Dependencies](#module-dependencies)
7. [Extension Points](#extension-points)
8. [Performance Characteristics](#performance-characteristics)

---

## System Overview

ParserCraft is a configuration-driven language construction framework built on a three-layer architecture that separates language definition, runtime management, and execution mechanics.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  CLI Tool    │  │  GUI IDE     │  │  LSP Server  │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
┌─────────▼──────────────────▼──────────────────▼─────────────┐
│               Configuration Layer                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  LanguageConfig (YAML/JSON dataclass)               │    │
│  │  • Keyword mappings                                  │    │
│  │  • Function definitions                              │    │
│  │  • Syntax options                                    │    │
│  │  • Type system config                                │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────┐
│                  Runtime Layer                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  LanguageRuntime (Singleton)                        │    │
│  │  • Configuration loading                             │    │
│  │  • Reverse mappings                                  │    │
│  │  • Execution context                                 │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────┐
│                 Execution Layer                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Parser   │  │ Module   │  │  Type    │  │ Code     │    │
│  │Generator │  │ Manager  │  │ Checker  │  │Generator │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
└───────────────────────────────────────────────────────────────┘
```

---

## Three-Layer Architecture

### Layer 1: Configuration Layer

**Purpose**: Define language features declaratively

**Components**:
- `LanguageConfig` dataclass
- YAML/JSON serialization
- Validation logic

**Responsibilities**:
```python
@dataclass
class LanguageConfig:
    """Single source of truth for language definition."""
    
    # Metadata
    name: str
    version: str
    description: str
    
    # Language features
    keyword_mappings: Dict[str, str]
    builtin_functions: Dict[str, Dict]
    operator_mappings: Dict[str, str]
    
    # Behavior
    syntax_options: SyntaxOptions
    module_options: ModuleOptions
    type_system: TypeSystemOptions
```

**Key Characteristics**:
- Immutable after loading
- Serializable to/from YAML/JSON
- Self-validating
- Independent of runtime state

### Layer 2: Runtime Layer

**Purpose**: Manage execution context and configuration application

**Components**:
- `LanguageRuntime` singleton
- Reverse mappings cache
- Execution state management

**Responsibilities**:
```python
class LanguageRuntime:
    """Singleton managing runtime execution context."""
    
    _instance: Optional['LanguageRuntime'] = None
    _config: Optional[LanguageConfig] = None
    _reverse_mappings: Dict[str, str] = {}
    
    @classmethod
    def get_instance(cls) -> 'LanguageRuntime':
        """Singleton accessor."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def translate(self, code: str) -> str:
        """Translate custom syntax → Python."""
        # Apply reverse mappings
        translated = code
        for custom, python in self._reverse_mappings.items():
            translated = translated.replace(custom, python)
        return translated
```

**Key Characteristics**:
- Single instance per process
- Hot-reloadable configuration
- Efficient mapping lookups
- Thread-safe execution

### Layer 3: Execution Layer

**Purpose**: Parse, analyze, and execute code

**Components**:

#### ParserGenerator
```python
class ParserGenerator:
    """Generate parsers from language configuration."""
    
    def __init__(self, config: LanguageConfig):
        self.config = config
        self._lexer_cache = {}
        self._parser_cache = {}
    
    def generate_lexer(self) -> Lexer:
        """Create lexer for tokenization."""
        
    def generate_parser(self) -> Parser:
        """Create parser for AST generation."""
    
    def parse(self, code: str) -> AST:
        """Parse code into abstract syntax tree."""
```

#### ModuleManager
```python
class ModuleManager:
    """Manage multi-file module imports."""
    
    def __init__(self, config: LanguageConfig):
        self.config = config
        self._loaded_modules: Dict[str, Module] = {}
        self._dependency_graph: Dict[str, Set[str]] = {}
    
    def load_module(self, name: str) -> Module:
        """Load and cache module."""
        
    def detect_circular_imports(self) -> List[List[str]]:
        """Find circular dependency chains."""
```

#### TypeChecker
```python
class TypeChecker:
    """Static type analysis."""
    
    def __init__(self, config: LanguageConfig):
        self.config = config
        self._type_cache: Dict[str, Type] = {}
    
    def check_file(self, filepath: str) -> List[TypeError]:
        """Analyze types in file."""
    
    def infer_types(self, code: str) -> Dict[str, Type]:
        """Infer variable types."""
```

---

## Core Components

### LanguageConfig

**File**: `src/parsercraft/language_config.py`

**Architecture**:
```
┌───────────────────────────────────┐
│   LanguageConfig (dataclass)      │
├───────────────────────────────────┤
│  Fields:                           │
│  • name: str                       │
│  • version: str                    │
│  • keyword_mappings: Dict          │
│  • builtin_functions: Dict         │
│  • syntax_options: SyntaxOptions   │
│  • module_options: ModuleOptions   │
│  • type_system: TypeSystemOptions  │
├───────────────────────────────────┤
│  Methods:                          │
│  • load(filepath) → LanguageConfig │
│  • save(filepath, format)          │
│  • validate() → bool               │
│  • to_dict() → Dict                │
│  • from_dict(dict) → Config        │
└───────────────────────────────────┘
```

**Dependencies**:
- `dataclasses` (Python stdlib)
- `pyyaml` (optional, for YAML support)
- `json` (Python stdlib)

### LanguageRuntime

**File**: `src/parsercraft/language_runtime.py`

**Architecture**:
```
┌────────────────────────────────────────┐
│  LanguageRuntime (Singleton)           │
├────────────────────────────────────────┤
│  Class Variables:                       │
│  • _instance: Optional[LanguageRuntime]│
│  • _config: Optional[LanguageConfig]   │
├────────────────────────────────────────┤
│  Instance Variables:                    │
│  • reverse_mappings: Dict[str, str]    │
│  • execution_context: Dict[str, Any]   │
├────────────────────────────────────────┤
│  Methods:                               │
│  • get_instance() → LanguageRuntime    │
│  • load_config(file or config)         │
│  • get_config() → LanguageConfig       │
│  • execute(code, globals, locals)      │
│  • execute_file(filepath)              │
│  • translate(code) → str               │
│  • get_reverse_mappings() → Dict       │
└────────────────────────────────────────┘
```

**State Management**:
```python
# Singleton pattern ensures single runtime per process
_instance = None

# Configuration loaded once, used many times
_config = LanguageConfig.load('lang.yaml')

# Reverse mappings cached for fast translation
reverse_mappings = {
    'cuando': 'if',
    'sino': 'else',
    'imprimir': 'print'
}
```

---

## Data Flow

### Program Execution Flow

```
User Code (custom.lang)
         │
         ▼
┌────────────────────┐
│  LanguageRuntime   │
│  .execute_file()   │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│    Read file       │
│    contents        │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Translate code    │
│  (custom→Python)   │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Python compile()  │
│  (to bytecode)     │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Python exec()     │
│  (execute)         │
└────────┬───────────┘
         │
         ▼
      Output
```

### Module Import Flow

```
import statement
         │
         ▼
┌────────────────────┐
│  ModuleManager     │
│  .load_module()    │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Search module     │
│  in paths          │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Check circular    │
│  dependencies      │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Parse module      │
│  code              │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Execute module    │
│  in context        │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Cache module      │
│  object            │
└────────────────────┘
```

### Type Checking Flow

```
Source code
         │
         ▼
┌────────────────────┐
│  ParserGenerator   │
│  .parse()          │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Build AST         │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  TypeChecker       │
│  .check_code()     │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Infer types       │
│  from AST          │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Validate          │
│  annotations       │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Report errors     │
└────────────────────┘
```

---

## Design Patterns

### 1. Singleton Pattern

**Used in**: `LanguageRuntime`

**Rationale**: Single execution context per process

```python
class LanguageRuntime:
    _instance: Optional['LanguageRuntime'] = None
    
    @classmethod
    def get_instance(cls) -> 'LanguageRuntime':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
```

**Benefits**:
- Consistent execution environment
- Shared configuration
- Efficient resource usage

### 2. Factory Pattern

**Used in**: `ParserGenerator`

**Rationale**: Create parsers from configurations

```python
class ParserGenerator:
    def create_parser(self, config: LanguageConfig) -> Parser:
        """Factory method for parser creation."""
        if config.syntax_options.block_delimiter == "indent":
            return IndentBasedParser(config)
        elif config.syntax_options.block_delimiter == "braces":
            return BraceBasedParser(config)
        else:
            return KeywordBasedParser(config)
```

### 3. Strategy Pattern

**Used in**: Code generation

**Rationale**: Different target platforms

```python
class CodeGenerator:
    def __init__(self, strategy: GenerationStrategy):
        self.strategy = strategy
    
    def generate(self, code: str) -> str:
        return self.strategy.generate(code)

# Different strategies
c_generator = CodeGenerator(CGenerationStrategy())
wasm_generator = CodeGenerator(WASMGenerationStrategy())
```

### 4. Observer Pattern

**Used in**: LSP Server

**Rationale**: Watch file changes

```python
class LSPServer:
    def __init__(self):
        self.observers: List[Observer] = []
    
    def notify_change(self, uri: str, content: str):
        for observer in self.observers:
            observer.on_file_change(uri, content)
```

### 5. Visitor Pattern

**Used in**: AST traversal

**Rationale**: Separate algorithms from data structure

```python
class ASTVisitor:
    def visit_function(self, node: FunctionNode):
        """Visit function definition."""
    
    def visit_if(self, node: IfNode):
        """Visit if statement."""

class TypeCheckVisitor(ASTVisitor):
    def visit_function(self, node: FunctionNode):
        # Check function types
        pass
```

---

## Module Dependencies

### Dependency Graph

```
┌──────────────────┐
│  language_config │
│  (no deps)       │
└────────┬─────────┘
         │
         ▼
┌────────────────────┐     ┌──────────────┐
│  language_runtime  │────▶│  cli.py      │
└────────┬───────────┘     └──────────────┘
         │
         │
    ┌────┴────┬────────────┬─────────────┐
    ▼         ▼            ▼             ▼
┌────────┐ ┌────────┐  ┌────────┐  ┌────────┐
│ parser │ │ module │  │  type  │  │  lsp   │
│  gen   │ │manager │  │checker │  │ server │
└────────┘ └────────┘  └────────┘  └────────┘
    │         │            │             │
    └─────────┴────────────┴─────────────┘
                     │
                     ▼
              ┌──────────┐
              │   ide.py │
              └──────────┘
```

### Import Chain

```python
# Core (no dependencies)
parsercraft.language_config

# Runtime layer (depends on config)
parsercraft.language_runtime

# Execution layer (depends on runtime)
parsercraft.parser_generator
parsercraft.module_system
parsercraft.type_system
parsercraft.lsp_server

# Application layer (depends on all)
parsercraft.cli
parsercraft.ide
```

---

## Extension Points

### 1. Custom Code Generators

```python
class CustomCodeGenerator(CodeGenerator):
    """Extend to add new target platform."""
    
    def generate(self, code: str) -> str:
        """Generate code for custom target."""
        # Implementation
        return generated_code
```

### 2. Custom Type Checkers

```python
class CustomTypeChecker(TypeChecker):
    """Extend to add custom type rules."""
    
    def check_custom_rule(self, node: ASTNode) -> List[Error]:
        """Implement custom type checking."""
        # Implementation
        return errors
```

### 3. Custom LSP Features

```python
class ExtendedLSPServer(LSPServer):
    """Add custom LSP features."""
    
    def handle_custom_request(self, params: Dict) -> Any:
        """Handle custom LSP request."""
        # Implementation
        return response
```

### 4. Custom Syntax Options

```yaml
# Extend SyntaxOptions dataclass
@dataclass
class ExtendedSyntaxOptions(SyntaxOptions):
    custom_feature: bool = False
    custom_delimiter: str = ""
```

---

## Performance Characteristics

### Time Complexity

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Config load | O(n) | n = config size |
| Keyword translation | O(m) | m = code size |
| Parser generation | O(k) | k = grammar size |
| Module loading | O(d*m) | d = depth, m = modules |
| Type checking | O(n*t) | n = nodes, t = type ops |

### Space Complexity

| Component | Space | Notes |
|-----------|-------|-------|
| LanguageConfig | O(k + f) | k = keywords, f = functions |
| LanguageRuntime | O(1) | Singleton |
| Module cache | O(m*s) | m = modules, s = size |
| Type cache | O(v) | v = variables |

### Optimization Strategies

1. **Parser Caching**:
```python
_parser_cache: Dict[str, Parser] = {}

def get_parser(config: LanguageConfig) -> Parser:
    key = hash(str(config))
    if key not in _parser_cache:
        _parser_cache[key] = ParserGenerator(config).generate_parser()
    return _parser_cache[key]
```

2. **Lazy Module Loading**:
```python
def load_module(self, name: str) -> Module:
    if name in self._loaded_modules:
        return self._loaded_modules[name]  # O(1) lookup
    
    # Load only when needed
    module = self._do_load(name)
    self._loaded_modules[name] = module
    return module
```

3. **Bytecode Compilation**:
```python
def execute(self, code: str) -> Any:
    # Compile once to bytecode
    bytecode = compile(translated_code, '<string>', 'exec')
    
    # Execute bytecode (faster than re-parsing)
    exec(bytecode, globals_dict)
```

---

## See Also

- [Developer Guide](DEVELOPER_GUIDE.md)
- [API Reference](reference/API_REFERENCE.md)
- [Performance Tuning](PERFORMANCE.md)

---

**End of Architecture Documentation**
