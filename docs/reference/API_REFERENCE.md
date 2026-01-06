# ParserCraft API Reference

**Version 2.0** | Complete API Documentation | January 2026

---

## Table of Contents

1. [Core API](#core-api)
2. [Configuration API](#configuration-api)
3. [Runtime API](#runtime-api)
4. [Module System API](#module-system-api)
5. [Type System API](#type-system-api)
6. [Testing API](#testing-api)
7. [LSP API](#lsp-api)
8. [Code Generation API](#code-generation-api)
9. [Enterprise Features API](#enterprise-features-api)

---

## Core API

### parsercraft.language_config

#### LanguageConfig

```python
@dataclass
class LanguageConfig:
    """Language configuration dataclass."""
    
    name: str
    version: str = "1.0"
    description: str = ""
    author: str = ""
    license: str = "MIT"
    
    keyword_mappings: Dict[str, str] = field(default_factory=dict)
    builtin_functions: Dict[str, Dict[str, str]] = field(default_factory=dict)
    operator_mappings: Dict[str, str] = field(default_factory=dict)
    syntax_options: SyntaxOptions = field(default_factory=SyntaxOptions)
    module_options: ModuleOptions = field(default_factory=ModuleOptions)
    type_system: TypeSystemOptions = field(default_factory=TypeSystemOptions)
```

**Methods:**

```python
def load(filepath: str) -> LanguageConfig:
    """Load configuration from YAML/JSON file."""
    
def save(filepath: str, format: str = "yaml") -> None:
    """Save configuration to file."""
    
def rename_keyword(old: str, new: str) -> None:
    """Rename a keyword."""
    
def add_builtin_function(
    name: str, 
    maps_to: str, 
    description: str = ""
) -> None:
    """Add a built-in function mapping."""
    
def set_array_indexing(
    start: int = 0, 
    allow_fractional: bool = False
) -> None:
    """Configure array indexing behavior."""
    
def validate() -> bool:
    """Validate configuration consistency."""
    
def to_dict() -> Dict[str, Any]:
    """Convert to dictionary."""
    
def from_dict(data: Dict[str, Any]) -> LanguageConfig:
    """Create from dictionary."""
```

**Example:**

```python
from parsercraft.language_config import LanguageConfig

# Create new configuration
config = LanguageConfig(
    name="MyLanguage",
    version="1.0",
    description="My custom language"
)

# Rename keywords
config.rename_keyword("if", "cuando")
config.rename_keyword("else", "sino")

# Add function
config.add_builtin_function("imprimir", "print", "Output to console")

# Save
config.save("my_lang.yaml", format="yaml")

# Load
loaded = LanguageConfig.load("my_lang.yaml")
```

---

### parsercraft.language_runtime

#### LanguageRuntime

```python
class LanguageRuntime:
    """Singleton runtime for language execution."""
    
    @classmethod
    def get_instance(cls) -> 'LanguageRuntime':
        """Get singleton instance."""
        
    @classmethod
    def load_config(cls, config_file: str = None, 
                    config: LanguageConfig = None) -> None:
        """Load configuration into runtime."""
        
    def get_config(self) -> LanguageConfig:
        """Get current configuration."""
        
    def execute(self, code: str, 
                globals_dict: Dict = None,
                locals_dict: Dict = None) -> Any:
        """Execute code string."""
        
    def execute_file(self, filepath: str) -> Any:
        """Execute file."""
        
    def translate(self, code: str) -> str:
        """Translate custom syntax to Python."""
        
    def get_reverse_mappings(self) -> Dict[str, str]:
        """Get reverse keyword mappings."""
```

**Example:**

```python
from parsercraft.language_runtime import LanguageRuntime

# Load configuration
LanguageRuntime.load_config('spanish.yaml')
runtime = LanguageRuntime.get_instance()

# Execute code
code = """
funcion saludar(nombre):
    devolver f"Hola, {nombre}!"

resultado = saludar("Mundo")
imprimir(resultado)
"""

runtime.execute(code)

# Execute file
runtime.execute_file('program.py')

# Translate to Python
python_code = runtime.translate(code)
print(python_code)
```

---

## Configuration API

### SyntaxOptions

```python
@dataclass
class SyntaxOptions:
    array_start_index: int = 0
    allow_fractional_indexing: bool = False
    statement_terminator: str = ""
    block_delimiter: str = "indent"
    comment_style: str = "#"
    multiline_comment_start: str = '"""'
    multiline_comment_end: str = '"""'
    string_quote_chars: List[str] = field(default_factory=lambda: ['"', "'"])
    case_sensitive: bool = True
    require_explicit_types: bool = False
```

### ModuleOptions

```python
@dataclass
class ModuleOptions:
    import_style: str = "python"
    module_extension: str = ".py"
    search_paths: List[str] = field(default_factory=lambda: ["."])
    allow_circular_imports: bool = False
```

### TypeSystemOptions

```python
@dataclass
class TypeSystemOptions:
    enabled: bool = True
    inference: bool = True
    strict_mode: bool = False
    generic_types: bool = True
    protocol_types: bool = True
```

---

## Runtime API

### parsercraft.parser_generator

#### ParserGenerator

```python
class ParserGenerator:
    """Generate parsers from language configuration."""
    
    def __init__(self, config: LanguageConfig):
        """Initialize with configuration."""
        
    def generate_lexer(self) -> Lexer:
        """Generate lexer for tokenization."""
        
    def generate_parser(self) -> Parser:
        """Generate parser for syntax analysis."""
        
    def parse(self, code: str) -> AST:
        """Parse code into AST."""
        
    def tokenize(self, code: str) -> List[Token]:
        """Tokenize code."""
```

**Example:**

```python
from parsercraft.parser_generator import ParserGenerator
from parsercraft.language_config import LanguageConfig

config = LanguageConfig.load('my_lang.yaml')
parser_gen = ParserGenerator(config)

# Tokenize
tokens = parser_gen.tokenize("funcion saludar(nombre): ...")
print(tokens)

# Parse to AST
ast = parser_gen.parse("funcion saludar(nombre): ...")
print(ast)
```

---

## Module System API

### parsercraft.module_system

#### ModuleManager

```python
class ModuleManager:
    """Manage multi-file module imports."""
    
    def __init__(self, config: LanguageConfig):
        """Initialize module manager."""
        
    def load_module(self, name: str, 
                    search_paths: List[str] = None) -> Module:
        """Load a module by name."""
        
    def execute_module(self, name: str) -> Any:
        """Execute a module."""
        
    def get_module_exports(self, name: str) -> List[str]:
        """Get exported symbols from module."""
        
    def detect_circular_imports(self) -> List[List[str]]:
        """Detect circular dependency chains."""
        
    def run_program(self, entry_point: str) -> Any:
        """Run program starting from entry point."""
```

#### Module

```python
@dataclass
class Module:
    name: str
    filepath: Path
    exports: List[ModuleExport]
    imports: List[ModuleImport]
    source_code: str
    compiled_code: Any
    is_loaded: bool = False
```

**Example:**

```python
from parsercraft.module_system import ModuleManager
from parsercraft.language_config import LanguageConfig

config = LanguageConfig.load('my_lang.yaml')
manager = ModuleManager(config)

# Load and execute module
manager.run_program('main.py')

# Check for circular dependencies
circular = manager.detect_circular_imports()
if circular:
    print(f"Circular imports detected: {circular}")

# Get module exports
exports = manager.get_module_exports('utils')
print(f"Available exports: {exports}")
```

---

## Type System API

### parsercraft.type_system

#### TypeChecker

```python
class TypeChecker:
    """Static type checking for custom languages."""
    
    def __init__(self, config: LanguageConfig):
        """Initialize type checker."""
        
    def check_file(self, filepath: str) -> List[TypeError]:
        """Check types in file."""
        
    def check_code(self, code: str) -> List[TypeError]:
        """Check types in code string."""
        
    def infer_types(self, code: str) -> Dict[str, Type]:
        """Infer types from code."""
        
    def validate_annotations(self, code: str) -> bool:
        """Validate type annotations."""
```

**Example:**

```python
from parsercraft.type_system import TypeChecker
from parsercraft.language_config import LanguageConfig

config = LanguageConfig.load('my_lang.yaml')
checker = TypeChecker(config)

code = """
funcion sumar(a: entero, b: entero) -> entero:
    devolver a + b

resultado: texto = sumar(1, 2)  # Type error!
"""

# Check for type errors
errors = checker.check_code(code)
for error in errors:
    print(f"Line {error.line}: {error.message}")

# Infer types
types = checker.infer_types(code)
print(f"Inferred types: {types}")
```

---

## Testing API

### parsercraft.test_framework

#### LanguageTestRunner

```python
class LanguageTestRunner:
    """Test runner for custom languages."""
    
    def __init__(self, config: LanguageConfig):
        """Initialize test runner."""
        
    def add_test(self, test: TestCase) -> None:
        """Add a test case."""
        
    def add_tests(self, tests: List[TestCase]) -> None:
        """Add multiple test cases."""
        
    def run_all_tests(self) -> List[TestResult]:
        """Run all tests and return results."""
        
    def run_test(self, test: TestCase) -> TestResult:
        """Run single test."""
        
    def generate_report(self) -> str:
        """Generate test report."""
```

#### TestCase

```python
@dataclass
class TestCase:
    name: str
    code: str
    expected_output: str = ""
    expected_vars: Dict[str, Any] = field(default_factory=dict)
    should_fail: bool = False
    expected_error: str = ""
    timeout: float = 5.0
```

**Example:**

```python
from parsercraft.test_framework import LanguageTestRunner, TestCase
from parsercraft.language_config import LanguageConfig

config = LanguageConfig.load('my_lang.yaml')
runner = LanguageTestRunner(config)

# Add tests
runner.add_test(TestCase(
    name="test_addition",
    code="resultado = 2 + 2",
    expected_vars={"resultado": 4}
))

runner.add_test(TestCase(
    name="test_function",
    code="""
    funcion doble(x):
        devolver x * 2
    resultado = doble(21)
    """,
    expected_vars={"resultado": 42}
))

# Run tests
results = runner.run_all_tests()

# Generate report
report = runner.generate_report()
print(report)
```

---

## LSP API

### parsercraft.lsp_server

#### LSPServer

```python
class LSPServer:
    """Language Server Protocol implementation."""
    
    def __init__(self, config: LanguageConfig, port: int = 8080):
        """Initialize LSP server."""
        
    def start(self) -> None:
        """Start the server."""
        
    def stop(self) -> None:
        """Stop the server."""
        
    def handle_completion(self, params: CompletionParams) -> List[CompletionItem]:
        """Handle autocomplete requests."""
        
    def handle_hover(self, params: HoverParams) -> Hover:
        """Handle hover information requests."""
        
    def handle_diagnostics(self, params: DiagnosticParams) -> List[Diagnostic]:
        """Handle diagnostic requests."""
```

**Example:**

```python
from parsercraft.lsp_server import LSPServer
from parsercraft.language_config import LanguageConfig

config = LanguageConfig.load('my_lang.yaml')
server = LSPServer(config, port=8080)

# Start server
server.start()

# Server now accepts LSP requests on port 8080
# Use with VS Code, PyCharm, etc.
```

---

## Code Generation API

### parsercraft.codegen_c

#### CCodeGenerator

```python
class CCodeGenerator:
    """Generate C code from custom language."""
    
    def __init__(self, config: LanguageConfig):
        """Initialize C code generator."""
        
    def generate(self, code: str, optimize: bool = False) -> str:
        """Generate C code."""
        
    def compile(self, code: str, output: str = "a.out") -> Path:
        """Generate and compile C code."""
```

### parsercraft.codegen_wasm

#### WASMCodeGenerator

```python
class WASMCodeGenerator:
    """Generate WebAssembly from custom language."""
    
    def __init__(self, config: LanguageConfig):
        """Initialize WASM generator."""
        
    def generate(self, code: str, optimize: bool = False) -> bytes:
        """Generate WASM binary."""
```

**Example:**

```python
from parsercraft.codegen_c import CCodeGenerator
from parsercraft.language_config import LanguageConfig

config = LanguageConfig.load('my_lang.yaml')
codegen = CCodeGenerator(config)

code = """
funcion factorial(n):
    si n <= 1:
        devolver 1
    sino:
        devolver n * factorial(n - 1)
"""

# Generate C code
c_code = codegen.generate(code, optimize=True)
print(c_code)

# Generate and compile
exe_path = codegen.compile(code, output="factorial")
```

---

## Enterprise Features API

### parsercraft.enterprise_security

#### EnterpriseSecurityManager

```python
class EnterpriseSecurityManager:
    """Enterprise-grade security features."""
    
    def __init__(self):
        """Initialize security manager."""
        
    def authenticate_sso(self, provider: str, token: str) -> User:
        """Authenticate via SSO."""
        
    def check_permissions(self, user: User, action: str) -> bool:
        """Check RBAC permissions."""
        
    def enable_mfa(self, user: User, method: str = "totp") -> MFASetup:
        """Enable multi-factor authentication."""
        
    def scan_vulnerabilities(self, code: str) -> List[Vulnerability]:
        """Scan code for security vulnerabilities."""
```

### parsercraft.mobile_cloud_analytics

#### MobilePlatformGenerator

```python
class MobilePlatformGenerator:
    """Generate mobile platform code."""
    
    def generate_ios(self, config: LanguageConfig) -> Path:
        """Generate iOS app."""
        
    def generate_android(self, config: LanguageConfig) -> Path:
        """Generate Android app."""
        
    def generate_pwa(self, config: LanguageConfig) -> Path:
        """Generate Progressive Web App."""
```

#### CloudDeploymentManager

```python
class CloudDeploymentManager:
    """Manage cloud deployments."""
    
    def deploy_aws(self, config: Dict, region: str = "us-east-1") -> Deployment:
        """Deploy to AWS."""
        
    def deploy_azure(self, config: Dict, region: str = "eastus") -> Deployment:
        """Deploy to Azure."""
        
    def deploy_gcp(self, config: Dict, region: str = "us-central1") -> Deployment:
        """Deploy to Google Cloud."""
```

### parsercraft.advanced_debugging_hardware

#### TimeTravelDebugger

```python
class TimeTravelDebugger:
    """Time-travel debugging capabilities."""
    
    def record_execution(self, code: str) -> Recording:
        """Record program execution."""
        
    def replay(self, recording: Recording, 
               to_timestamp: float = None) -> ExecutionState:
        """Replay execution to specific point."""
        
    def get_snapshot(self, recording: Recording, 
                     timestamp: float) -> Snapshot:
        """Get execution state snapshot."""
```

#### HardwareIntegrationManager

```python
class HardwareIntegrationManager:
    """Hardware platform integration."""
    
    def deploy_to_arduino(self, code: str, board: str = "uno") -> bool:
        """Deploy to Arduino."""
        
    def deploy_to_esp32(self, code: str, config: Dict = None) -> bool:
        """Deploy to ESP32."""
        
    def deploy_to_raspberry_pi(self, code: str, 
                                 model: str = "4b") -> bool:
        """Deploy to Raspberry Pi."""
        
    def synthesize_fpga(self, code: str, 
                        target: str = "verilog") -> str:
        """Generate FPGA code."""
```

**Example:**

```python
from parsercraft.advanced_debugging_hardware import (
    TimeTravelDebugger, 
    HardwareIntegrationManager
)

# Time-travel debugging
debugger = TimeTravelDebugger()
recording = debugger.record_execution(code)
snapshot = debugger.get_snapshot(recording, timestamp=5.0)
print(f"Variables at t=5.0: {snapshot.variables}")

# Hardware deployment
hw_manager = HardwareIntegrationManager()
hw_manager.deploy_to_arduino(code, board="mega")
```

---

## Utility Functions

### parsercraft.language_config

```python
def print_language_info(config: LanguageConfig) -> None:
    """Print formatted language information."""

def validate_config(config: LanguageConfig) -> Tuple[bool, List[str]]:
    """Validate configuration and return errors."""
    
def merge_configs(base: LanguageConfig, 
                  override: LanguageConfig) -> LanguageConfig:
    """Merge two configurations."""
```

### parsercraft.documentation_generator

```python
class DocumentationGenerator:
    """Generate documentation for custom languages."""
    
    def generate_markdown(self, config: LanguageConfig) -> str:
        """Generate Markdown documentation."""
        
    def generate_html(self, config: LanguageConfig) -> str:
        """Generate HTML documentation."""
        
    def generate_api_docs(self, modules: List[Module]) -> str:
        """Generate API documentation."""
```

---

## Constants and Enumerations

### SecurityLevel

```python
class SecurityLevel(Enum):
    NONE = 0
    BASIC = 1
    STANDARD = 2
    ENHANCED = 3
    MAXIMUM = 4
```

### OptimizationLevel

```python
class OptimizationLevel(Enum):
    NONE = 0
    BASIC = 1
    AGGRESSIVE = 2
```

### ErrorSeverity

```python
class ErrorSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
```

---

## Error Handling

### Custom Exceptions

```python
class LanguageConfigError(Exception):
    """Configuration error."""

class TranslationError(Exception):
    """Code translation error."""

class ExecutionError(Exception):
    """Runtime execution error."""

class ModuleLoadError(Exception):
    """Module loading error."""

class TypeCheckError(Exception):
    """Type checking error."""
```

---

## Complete Example

```python
from parsercraft.language_config import LanguageConfig
from parsercraft.language_runtime import LanguageRuntime
from parsercraft.module_system import ModuleManager
from parsercraft.type_system import TypeChecker
from parsercraft.test_framework import LanguageTestRunner, TestCase

# 1. Create configuration
config = LanguageConfig(name="MiLenguaje", version="1.0")
config.rename_keyword("if", "si")
config.rename_keyword("else", "sino")
config.add_builtin_function("imprimir", "print")
config.save("mi_lenguaje.yaml")

# 2. Load into runtime
LanguageRuntime.load_config('mi_lenguaje.yaml')
runtime = LanguageRuntime.get_instance()

# 3. Execute code
code = """
si True:
    imprimir("Hola Mundo")
sino:
    imprimir("Adiós")
"""
runtime.execute(code)

# 4. Check types
checker = TypeChecker(config)
errors = checker.check_code(code)

# 5. Run tests
runner = LanguageTestRunner(config)
runner.add_test(TestCase(
    name="test_hello",
    code='imprimir("Hola")',
    expected_output="Hola\n"
))
results = runner.run_all_tests()

# 6. Module management
manager = ModuleManager(config)
manager.run_program('main.py')
```

---

## API Versioning

ParserCraft follows semantic versioning:
- **Major version**: Breaking API changes
- **Minor version**: New features, backwards compatible
- **Patch version**: Bug fixes

Current version: **2.0.0**

---

## See Also

- [User Manual](../USER_MANUAL.md)
- [Developer Guide](../DEVELOPER_GUIDE.md)
- [Language Construction Guide](../LANGUAGE_CONSTRUCTION_GUIDE.md)
- [Examples](../../demos/)

---

**End of API Reference**
