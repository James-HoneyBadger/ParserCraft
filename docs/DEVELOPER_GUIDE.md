# ParserCraft Developer Guide

**Version 2.0** | For Contributors and Extenders | January 2026

A comprehensive guide for developers who want to contribute to ParserCraft or extend its capabilities.

---

## Table of Contents

1. [Development Setup](#development-setup)
2. [Architecture Overview](#architecture-overview)
3. [Code Organization](#code-organization)
4. [Contributing Guidelines](#contributing-guidelines)
5. [Testing Strategy](#testing-strategy)
6. [Adding New Features](#adding-new-features)
7. [Performance Optimization](#performance-optimization)
8. [Security Considerations](#security-considerations)

---

## Development Setup

### Prerequisites

- Python 3.8+ (3.10+ recommended)
- Git
- Virtual environment tool (venv, conda, or virtualenv)
- Text editor or IDE (VS Code, PyCharm, etc.)

### Clone and Setup

```bash
# Clone repository
git clone https://github.com/James-HoneyBadger/ParserCraft.git
cd ParserCraft

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .[dev]

# Install development dependencies
pip install pytest black mypy pylint pre-commit

# Setup pre-commit hooks
pre-commit install
```

### Verify Installation

```bash
# Run tests
python -m pytest tests/ -v

# Check code style
black --check src/
pylint src/parsercraft/

# Type checking
mypy src/parsercraft/

# Run IDE
PYTHONPATH=src:$PYTHONPATH python3 src/parsercraft/launch_ide.py
```

---

## Architecture Overview

### Three-Layer Design

```
┌────────────────────────────────────────────┐
│  Configuration Layer                        │
│  ├─ LanguageConfig (dataclass)              │
│  ├─ YAML/JSON serialization                 │
│  └─ Validation and schema checking          │
└──────────────┬─────────────────────────────┘
               │
┌──────────────▼─────────────────────────────┐
│  Runtime Layer (Singleton)                  │
│  ├─ LanguageRuntime                         │
│  ├─ Keyword mappings (custom ↔ Python)      │
│  ├─ Hot-reloadable configs                  │
│  └─ Execution context management            │
└──────────────┬─────────────────────────────┘
               │
┌──────────────▼─────────────────────────────┐
│  Execution Layer                            │
│  ├─ ParserGenerator (lexer/parser)          │
│  ├─ ModuleManager (multi-file support)      │
│  ├─ TypeChecker (static analysis)           │
│  └─ LSPServer (IDE integration)             │
└────────────────────────────────────────────┘
```

### Key Design Patterns

1. **Singleton Pattern**: `LanguageRuntime` ensures single execution context
2. **Factory Pattern**: `ParserGenerator` creates parsers from configurations
3. **Observer Pattern**: LSP server watches file changes
4. **Strategy Pattern**: Different execution strategies (interpret, compile, JIT)

---

## Code Organization

### Directory Structure

```
ParserCraft/
├── src/
│   ├── parsercraft/           # Core framework
│   │   ├── __init__.py
│   │   ├── language_config.py       # Configuration dataclasses
│   │   ├── language_runtime.py      # Execution runtime (singleton)
│   │   ├── parser_generator.py      # Parser generation
│   │   ├── module_system.py         # Multi-file imports
│   │   ├── type_system.py           # Type checking
│   │   ├── lsp_server.py            # LSP implementation
│   │   ├── cli.py                   # Command-line interface
│   │   ├── ide.py                   # GUI IDE
│   │   ├── test_framework.py        # Testing utilities
│   │   ├── codegen_c.py             # C code generation
│   │   ├── codegen_wasm.py          # WebAssembly generation
│   │   ├── enterprise_security.py   # Enterprise features
│   │   ├── mobile_cloud_analytics.py # Mobile/cloud support
│   │   └── advanced_debugging_hardware.py # Advanced features
│   │
│   └── codex/                 # CodeEx IDE (separate app)
│       ├── codex.py
│       ├── codex_gui.py
│       └── codex_components.py
│
├── tests/                     # Test suite
│   ├── test_phase5_integration.py
│   ├── test_phase6_optimizations.py
│   ├── test_phase7_production.py
│   ├── test_phase8_web_ide.py
│   ├── test_phase9_mobile_cloud.py
│   ├── test_phase10_enterprise.py
│   └── test_phase11_advanced.py
│
├── configs/                   # Language configurations
│   ├── teachscript.yaml
│   └── examples/
│       ├── python_like.yaml
│       ├── lisp_like.yaml
│       └── ...
│
├── demos/                     # Demo scripts
│   ├── demo_language_construction.py
│   └── teachscript/
│
└── docs/                      # Documentation
    ├── GETTING_STARTED.md
    ├── USER_MANUAL.md
    ├── guides/
    ├── reference/
    └── teachscript/
```

### Module Responsibilities

| Module | Purpose | Key Classes |
|--------|---------|-------------|
| `language_config.py` | Configuration management | `LanguageConfig`, `SyntaxOptions` |
| `language_runtime.py` | Execution context | `LanguageRuntime` (singleton) |
| `parser_generator.py` | Parsing infrastructure | `ParserGenerator`, `Lexer`, `Parser` |
| `module_system.py` | Multi-file support | `ModuleManager`, `Module` |
| `type_system.py` | Type checking | `TypeChecker`, `TypeInferrer` |
| `lsp_server.py` | IDE integration | `LSPServer` |
| `cli.py` | Command-line tools | `main()`, command handlers |
| `ide.py` | GUI application | `ParserCraftIDE` |

---

## Contributing Guidelines

### Code Style

```bash
# Format code with Black
black src/ tests/

# Sort imports
isort src/ tests/

# Check style
pylint src/parsercraft/
flake8 src/

# Type checking
mypy src/parsercraft/
```

### Coding Standards

1. **Follow PEP 8**: Use Black for automatic formatting
2. **Type Hints**: Add type hints to all functions
3. **Docstrings**: Use Google-style docstrings
4. **Comments**: Explain "why", not "what"
5. **Error Handling**: Use specific exceptions

**Example:**

```python
def load_module(self, name: str, search_paths: Optional[List[str]] = None) -> Module:
    """Load a module by name.
    
    Args:
        name: Module name to load
        search_paths: Optional list of directories to search
        
    Returns:
        Loaded Module object
        
    Raises:
        ModuleLoadError: If module cannot be found or loaded
        
    Example:
        >>> manager = ModuleManager(config)
        >>> module = manager.load_module('math')
    """
    if search_paths is None:
        search_paths = self.config.module_options.search_paths
        
    # Implementation...
```

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-new-feature

# Make changes and commit
git add .
git commit -m "Add new feature: description"

# Push and create PR
git push origin feature/my-new-feature
# Then create Pull Request on GitHub
```

### Commit Messages

Follow conventional commits:

```
feat: Add support for Rust-like syntax
fix: Resolve circular import detection bug
docs: Update API reference for LanguageRuntime
test: Add tests for type inference
refactor: Simplify parser generation logic
perf: Optimize module loading performance
chore: Update dependencies
```

---

## Testing Strategy

### Test Structure

```python
# tests/test_my_feature.py
import pytest
from parsercraft.language_config import LanguageConfig
from parsercraft.language_runtime import LanguageRuntime

class TestMyFeature:
    """Test suite for my feature."""
    
    @pytest.fixture
    def config(self):
        """Create test configuration."""
        config = LanguageConfig(name="TestLang")
        config.rename_keyword("if", "cuando")
        return config
    
    @pytest.fixture
    def runtime(self, config):
        """Create test runtime."""
        LanguageRuntime.load_config(config=config)
        return LanguageRuntime.get_instance()
    
    def test_basic_functionality(self, runtime):
        """Test basic functionality."""
        code = "cuando True: imprimir('test')"
        result = runtime.execute(code)
        assert result is not None
    
    def test_error_handling(self, runtime):
        """Test error handling."""
        with pytest.raises(ExecutionError):
            runtime.execute("invalid syntax")
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_phase5_integration.py -v

# Run with coverage
python -m pytest tests/ --cov=src/parsercraft --cov-report=html

# Run only fast tests
python -m pytest tests/ -m "not slow"

# Run in parallel
python -m pytest tests/ -n auto
```

### Test Categories

1. **Unit Tests**: Test individual functions/classes
2. **Integration Tests**: Test component interactions
3. **End-to-End Tests**: Test complete workflows
4. **Performance Tests**: Measure execution time
5. **Regression Tests**: Verify bug fixes

---

## Adding New Features

### Adding a New Keyword Type

1. **Update LanguageConfig** (`language_config.py`):

```python
@dataclass
class LanguageConfig:
    # Add new keyword category
    loop_keywords: Dict[str, str] = field(default_factory=dict)
```

2. **Update LanguageRuntime** (`language_runtime.py`):

```python
class LanguageRuntime:
    def _build_reverse_mappings(self):
        # Add reverse mapping
        for custom, python in self.config.loop_keywords.items():
            self.reverse_mappings[custom] = python
```

3. **Update Parser** (`parser_generator.py`):

```python
class ParserGenerator:
    def generate_parser(self):
        # Handle new keyword type
        loop_keywords = self.config.loop_keywords
        # Generate parser rules...
```

4. **Add Tests** (`tests/test_new_keyword.py`):

```python
def test_new_keyword():
    config = LanguageConfig()
    config.loop_keywords = {"repeat": "while"}
    # Test implementation...
```

5. **Update Documentation**:
   - Add to User Manual
   - Update API Reference
   - Create examples

### Adding LSP Features

1. **Extend LSPServer** (`lsp_server.py`):

```python
class LSPServer:
    def handle_new_feature(self, params: NewFeatureParams) -> Result:
        """Handle new LSP feature."""
        # Implementation
        return result
```

2. **Register Handler**:

```python
self.handlers["textDocument/newFeature"] = self.handle_new_feature
```

3. **Update Protocol Types**:

```python
@dataclass
class NewFeatureParams:
    textDocument: TextDocumentIdentifier
    position: Position
```

4. **Test Integration**:

```python
def test_lsp_new_feature():
    server = LSPServer(config)
    result = server.handle_new_feature(params)
    assert result is not None
```

### Adding Code Generator Target

1. **Create Generator Module** (`codegen_new.py`):

```python
class NewCodeGenerator:
    """Generate code for new target."""
    
    def __init__(self, config: LanguageConfig):
        self.config = config
    
    def generate(self, code: str) -> str:
        """Generate target code."""
        # Parse source
        # Translate to target
        # Optimize
        return generated_code
```

2. **Add CLI Command** (`cli.py`):

```python
codegen_new_parser = subparsers.add_parser(
    "codegen-new",
    help="Generate code for new target"
)
```

3. **Add Tests**:

```python
def test_codegen_new():
    generator = NewCodeGenerator(config)
    code = "funcion test(): pass"
    result = generator.generate(code)
    assert "expected output" in result
```

---

## Performance Optimization

### Profiling

```python
import cProfile
import pstats

# Profile code execution
profiler = cProfile.Profile()
profiler.enable()

runtime.execute_file('large_program.py')

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)
```

### Optimization Techniques

1. **Cache Compiled Parsers**:

```python
class ParserGenerator:
    _parser_cache: Dict[str, Parser] = {}
    
    def generate_parser(self) -> Parser:
        cache_key = hash(str(self.config))
        if cache_key in self._parser_cache:
            return self._parser_cache[cache_key]
        
        parser = self._create_parser()
        self._parser_cache[cache_key] = parser
        return parser
```

2. **Lazy Module Loading**:

```python
class ModuleManager:
    def load_module(self, name: str) -> Module:
        if name in self._loaded_modules:
            return self._loaded_modules[name]
        
        # Load only when needed
        module = self._do_load(name)
        self._loaded_modules[name] = module
        return module
```

3. **Bytecode Compilation**:

```python
def execute(self, code: str) -> Any:
    # Compile to bytecode once
    bytecode = compile(translated_code, '<string>', 'exec')
    # Execute bytecode (faster than re-parsing)
    exec(bytecode, globals_dict)
```

---

## Security Considerations

### Input Validation

```python
def validate_config(config: LanguageConfig) -> None:
    """Validate configuration for security issues."""
    
    # Check for command injection
    for func in config.builtin_functions.values():
        if 'os.system' in func.maps_to or 'subprocess' in func.maps_to:
            raise SecurityError("Dangerous function mapping")
    
    # Validate keyword names
    for keyword in config.keyword_mappings.keys():
        if not keyword.isidentifier():
            raise ValidationError(f"Invalid keyword: {keyword}")
```

### Sandboxing

```python
def execute_sandboxed(self, code: str, timeout: float = 5.0) -> Any:
    """Execute code in sandboxed environment."""
    
    # Restricted builtins
    safe_builtins = {
        'print': print,
        'len': len,
        'range': range,
        # Only safe functions
    }
    
    # Execute with timeout
    import signal
    signal.alarm(int(timeout))
    try:
        result = exec(code, {"__builtins__": safe_builtins})
    finally:
        signal.alarm(0)
    
    return result
```

### Code Scanning

```python
def scan_for_vulnerabilities(code: str) -> List[Vulnerability]:
    """Scan code for security issues."""
    
    vulnerabilities = []
    
    # Check for eval/exec
    if 'eval(' in code or 'exec(' in code:
        vulnerabilities.append(Vulnerability(
            severity="HIGH",
            message="Use of eval/exec detected"
        ))
    
    # Check for file operations
    if 'open(' in code:
        vulnerabilities.append(Vulnerability(
            severity="MEDIUM",
            message="File access detected"
        ))
    
    return vulnerabilities
```

---

## Debugging Tips

### Enable Debug Mode

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('parsercraft')

logger.debug("Loading configuration...")
```

### Interactive Debugging

```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use Python 3.7+
breakpoint()
```

### Verbose Execution

```bash
# Run with verbose output
parsercraft run --config my_lang.yaml script.py --debug --verbose
```

---

## Release Process

### Version Numbering

Follow Semantic Versioning (semver):
- MAJOR.MINOR.PATCH (e.g., 2.1.0)

```python
# Update version in setup.py
version="2.1.0"

# Tag release
git tag -a v2.1.0 -m "Release version 2.1.0"
git push origin v2.1.0
```

### Release Checklist

- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped
- [ ] Create GitHub release
- [ ] Build and upload to PyPI

```bash
# Build distribution
python setup.py sdist bdist_wheel

# Upload to PyPI
twine upload dist/*
```

---

## Resources

### Documentation
- [User Manual](USER_MANUAL.md)
- [API Reference](reference/API_REFERENCE.md)
- [Architecture Documentation](ARCHITECTURE.md)

### Community
- GitHub: https://github.com/James-HoneyBadger/ParserCraft
- Issues: https://github.com/James-HoneyBadger/ParserCraft/issues
- Discussions: https://github.com/James-HoneyBadger/ParserCraft/discussions

### Tools
- Black: https://black.readthedocs.io/
- mypy: http://mypy-lang.org/
- pytest: https://pytest.org/

---

**Happy Coding!** 🚀

For questions, contact the maintainers or open an issue on GitHub.
