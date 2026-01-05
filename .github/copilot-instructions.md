# ParserCraft AI Coding Agent Instructions

## Project Overview

ParserCraft is a **custom programming language construction framework** that enables users to create language variants through configuration files (YAML/JSON) without compiler engineering knowledge. The system includes runtime interpretation, IDE integration via Language Server Protocol (LSP), and multi-file module support.

**Core Philosophy**: Language features are configured, not coded. The framework translates config-driven language definitions into executable runtimes.

## Architecture: Three-Layer Design

### 1. Configuration Layer (`src/parsercraft/language_config.py`)
- **`LanguageConfig`** dataclass: Single source of truth for language definitions
- Supports keyword remapping (e.g., `if` → `cuando`), custom functions, operators, syntax options
- Serializes to YAML/JSON for portability
- Example config: `configs/teachscript.yaml` (educational language with `teach` instead of `def`)

### 2. Runtime Layer (`src/parsercraft/language_runtime.py`)
- **`LanguageRuntime`** singleton: Applies config at interpretation time
- Maintains reverse mappings (custom keyword → Python keyword) for translation
- Hot-reloadable configurations
- **Critical pattern**: All language execution flows through `LanguageRuntime.get_instance()`

### 3. Parsing & Execution Layer
- **`ParserGenerator`** (`parser_generator.py`): Generates lexers/parsers from config
- **`ModuleManager`** (`module_system.py`): Multi-file imports, circular dependency detection
- **`LSPServer`** (`lsp_server.py`): IDE integration (VS Code, PyCharm, Neovim)

## Key Components

### Module System (`module_system.py`)
- Supports `import math`, `import {sin, cos} from math` syntax
- Tracks module visibility (public/private/protected)
- Detects circular dependencies via graph traversal
- **Entry point**: `ModuleManager.load_module(name, search_paths)`

### LSP Integration (`lsp_server.py`, `lsp_integration.py`)
- Full Language Server Protocol implementation for IDE features
- Provides: diagnostics, completion, hover, signature help
- **Usage pattern**: Start with `python -m parsercraft.lsp_server --config X.yaml --port 8080`
- VSCode extensions auto-generated via `parsercraft extension` CLI command

### Testing Patterns
- Tests use `pytest` framework (run: `python -m pytest tests/`)
- Fixtures in `tests/test_phase5_integration.py` show typical config mocking
- **Pattern**: Mock `LanguageConfig` using `SimpleNamespace` with minimal required fields

## Developer Workflows

### Creating a Custom Language
```bash
# Interactive config creation
parsercraft create --preset python_like --output my_lang.yaml

# Validate config
parsercraft validate my_lang.yaml

# Launch IDE for testing
./run-parsercraft.sh  # Auto-creates venv, installs deps
```

### Running Programs in Custom Languages
```python
from parsercraft.language_runtime import LanguageRuntime
from parsercraft.module_system import ModuleManager

# Load language config
LanguageRuntime.load_config(config_file="teachscript.yaml")

# Run with module support
manager = ModuleManager(config=LanguageRuntime.get_config())
manager.run_program("main.teach")
```

### Adding New Features
1. **New keyword/operator**: Update `LanguageConfig` dataclasses, add to mappings in `language_runtime.py`
2. **New LSP feature**: Extend `LSPServer.handle_<feature>()` methods in `lsp_server.py`
3. **New module capability**: Modify `ModuleManager` and update `Module` dataclass

## Project-Specific Conventions

### File Organization
- `src/parsercraft/`: Core framework (avoid "parsercraft" in code, use "parsercraft" imports)
- `src/codex/`: Separate IDE (CodeEx) - different codebase, shares framework
- `configs/examples/`: Reference language configs (Python-like, LISP-like, etc.)
- `docs/guides/`: User/developer documentation (e.g., `LSP_INTEGRATION_GUIDE.md`)

### Naming Patterns
- **TeachScript**: Educational proof-of-concept language (uses `teach` keyword for functions)
- **Gulf of Mexico indexing**: Arrays start at -1 (configurable via `array_start_index`)
- **Satirical keywords**: Optional humorous aliases (disabled by default)

### Configuration Access Pattern
```python
# ALWAYS use singleton pattern for runtime
runtime = LanguageRuntime.get_instance()
config = runtime.get_config()

# DON'T create new LanguageConfig() instances for runtime
# DO use LanguageConfig.load(file) then pass to LanguageRuntime.load_config()
```

### Error Handling Strategy (`production_error_handling.py`)
- Production code uses **circuit breakers**, **retry with backoff**, **rate limiters**
- Wrap external calls with `@retry_with_backoff(config)` decorator
- Use `ProductionErrorHandler` for centralized error management with audit logging

## CLI Entry Points

| Command | Purpose | Implementation |
|---------|---------|----------------|
| `parsercraft create` | Interactive language creation | `cli.py:main()` |
| `parsercraft lsp` | Start LSP server | `lsp_server.py:main()` |
| `parsercraft extension` | Generate VS Code extension | `vscode_integration.py` |
| `parsercraft run` | Execute program in custom language | `cli.py` + `language_runtime.py` |
| `./run-parsercraft.sh` | Launch ParserCraft IDE (GUI) | `launch_ide.py` via bash wrapper |

## IDE Integration

### ParserCraft IDE (`ide.py`, `launch_ide.py`)
- Tkinter-based visual language designer
- Real-time config editing and program execution
- **Launch pattern**: Shell scripts (`run-parsercraft.sh`) handle venv setup + dependency installation

### CodeEx IDE (`src/codex/codex.py`)
- Separate application for developing programs in custom languages
- Launched via `./run-codex.sh` or `codex` CLI command
- Integrates with `LanguageRuntime` for execution

## Testing Commands
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_phase5_integration.py

# Run with verbose output
python -m pytest tests/ -v
```

## Common Patterns to Follow

### When Adding Type System Features
- Extend `TypeChecker` in `type_system.py`
- Update `type_system_generics.py` for generic types
- Protocol types use structural typing (see `protocols.py`)

### When Modifying Parser Behavior
- Update `ParserGenerator` token/AST generation
- Ensure `LanguageValidator` checks new syntax rules
- Add tests to `tests/test_cli_translation.py` for keyword translation

### When Extending Module System
- Modify `ModuleExport`/`ModuleImport` dataclasses
- Update dependency graph tracking in `ModuleManager`
- Test circular dependency detection

## External Dependencies
- **PyYAML**: Config file parsing (required)
- **pytest**: Testing framework (dev dependency)
- **tkinter**: IDE GUI (bundled with Python, but verify availability)

## Documentation Structure
- `docs/guides/`: End-user guides (LSP, modules, type system)
- `docs/teachscript/`: TeachScript language documentation
- `docs/archives/`: Historical completion reports (phases 1-10)
- `README.md`: Primary user-facing entry point

## Quick Reference: Finding Code

| Task | Start Here |
|------|-----------|
| Language config schema | `language_config.py` → `LanguageConfig` dataclass |
| Runtime execution | `language_runtime.py` → `LanguageRuntime` class |
| Module imports | `module_system.py` → `ModuleManager.load_module()` |
| LSP server logic | `lsp_server.py` → `LSPServer.handle_*()` methods |
| Parser generation | `parser_generator.py` → `ParserGenerator.generate()` |
| CLI commands | `cli.py` → `main()` with argparse subcommands |
| Test examples | `tests/test_phase5_integration.py` for integration patterns |
