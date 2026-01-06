# Contributing to ParserCraft

**Version 2.0** | Join the Community | January 2026

---

## Welcome Contributors! 🎉

Thank you for your interest in contributing to ParserCraft! This guide will help you get started.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [How to Contribute](#how-to-contribute)
4. [Development Workflow](#development-workflow)
5. [Coding Standards](#coding-standards)
6. [Testing Guidelines](#testing-guidelines)
7. [Documentation](#documentation)
8. [Pull Request Process](#pull-request-process)

---

## Code of Conduct

### Our Pledge

We pledge to make participation in ParserCraft a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- Trolling, insulting comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Report violations to: [maintainer-email]

---

## Getting Started

### Prerequisites

- Python 3.8+ (3.10+ recommended)
- Git
- GitHub account
- Familiarity with Python

### Fork and Clone

```bash
# Fork on GitHub (click Fork button)

# Clone your fork
git clone https://github.com/YOUR-USERNAME/ParserCraft.git
cd ParserCraft

# Add upstream remote
git remote add upstream https://github.com/James-HoneyBadger/ParserCraft.git
```

### Setup Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .[dev]

# Install development tools
pip install pytest black mypy pylint pre-commit

# Setup pre-commit hooks
pre-commit install
```

### Verify Setup

```bash
# Run tests
python -m pytest tests/ -v

# Check code style
black --check src/
pylint src/parsercraft/

# Type checking
mypy src/parsercraft/
```

---

## How to Contribute

### Types of Contributions

1. **Bug Reports** 🐛
   - Found a bug? Open an issue!
   - Include steps to reproduce
   - Provide error messages and logs

2. **Feature Requests** ✨
   - Have an idea? We'd love to hear it!
   - Explain the use case
   - Discuss implementation approach

3. **Code Contributions** 💻
   - Bug fixes
   - New features
   - Performance improvements
   - Documentation improvements

4. **Documentation** 📚
   - Fix typos
   - Improve clarity
   - Add examples
   - Write tutorials

5. **Testing** 🧪
   - Add test cases
   - Improve test coverage
   - Report test failures

---

## Development Workflow

### 1. Pick an Issue

- Check [GitHub Issues](https://github.com/James-HoneyBadger/ParserCraft/issues)
- Look for `good first issue` or `help wanted` labels
- Comment that you're working on it

### 2. Create a Branch

```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/my-new-feature

# Or for bug fix
git checkout -b fix/bug-description
```

### 3. Make Changes

```bash
# Edit files
# Write tests
# Update documentation

# Check your changes
black src/ tests/
pylint src/parsercraft/
mypy src/parsercraft/
python -m pytest tests/ -v
```

### 4. Commit Changes

```bash
# Stage changes
git add .

# Commit with meaningful message
git commit -m "feat: Add support for custom operators

- Implement operator mapping in LanguageConfig
- Add operator translation in LanguageRuntime
- Include tests for arithmetic and logical operators
- Update documentation

Closes #123"
```

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(parser): Add support for multi-line strings
fix(runtime): Resolve circular import detection bug
docs(api): Update LanguageConfig documentation
test(modules): Add tests for module loading
```

### 5. Push Changes

```bash
# Push to your fork
git push origin feature/my-new-feature
```

### 6. Create Pull Request

1. Go to your fork on GitHub
2. Click "Pull Request"
3. Fill out the template
4. Link related issues
5. Request review

---

## Coding Standards

### Python Style Guide

Follow [PEP 8](https://pep8.org/) with these tools:

```bash
# Format code
black src/ tests/

# Check style
pylint src/parsercraft/
flake8 src/

# Sort imports
isort src/ tests/
```

### Code Examples

**Good:**
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
    
    for path in search_paths:
        module_path = Path(path) / f"{name}.py"
        if module_path.exists():
            return self._load_from_file(module_path)
    
    raise ModuleLoadError(f"Module '{name}' not found")
```

**Bad:**
```python
def loadmod(n,p=None):
    # load module
    if not p:
        p=self.config.module_options.search_paths
    for path in p:
        mp=Path(path)/f"{n}.py"
        if mp.exists():
            return self._load_from_file(mp)
    raise ModuleLoadError(f"Module '{n}' not found")
```

### Type Hints

Always use type hints:

```python
# ✅ Good
def process_data(items: List[str], limit: int = 10) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for item in items[:limit]:
        result[item] = len(item)
    return result

# ❌ Bad
def process_data(items, limit=10):
    result = {}
    for item in items[:limit]:
        result[item] = len(item)
    return result
```

### Docstrings

Use Google-style docstrings:

```python
def my_function(param1: str, param2: int) -> bool:
    """Brief description of function.
    
    Longer description explaining what the function does,
    how it works, and any important notes.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param2 is negative
        TypeError: When param1 is not a string
        
    Example:
        >>> result = my_function("hello", 42)
        >>> print(result)
        True
    """
    if param2 < 0:
        raise ValueError("param2 must be positive")
    
    return len(param1) > param2
```

---

## Testing Guidelines

### Writing Tests

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
        config.rename_keyword("if", "when")
        return config
    
    @pytest.fixture
    def runtime(self, config):
        """Create test runtime."""
        LanguageRuntime.load_config(config=config)
        return LanguageRuntime.get_instance()
    
    def test_basic_functionality(self, runtime):
        """Test basic functionality."""
        code = "when True: print('test')"
        result = runtime.execute(code)
        assert result is not None
    
    def test_error_handling(self, runtime):
        """Test error handling."""
        with pytest.raises(SyntaxError):
            runtime.execute("invalid syntax")
    
    @pytest.mark.parametrize("input,expected", [
        ("when True: pass", None),
        ("when False: pass", None),
    ])
    def test_parametrized(self, runtime, input, expected):
        """Test with multiple inputs."""
        result = runtime.execute(input)
        assert result == expected
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_my_feature.py -v

# Run specific test
python -m pytest tests/test_my_feature.py::TestMyFeature::test_basic_functionality -v

# Run with coverage
python -m pytest tests/ --cov=src/parsercraft --cov-report=html

# Run only fast tests
python -m pytest tests/ -m "not slow"
```

### Test Coverage

Aim for >80% code coverage:

```bash
# Generate coverage report
python -m pytest tests/ --cov=src/parsercraft --cov-report=term-missing

# View HTML report
python -m pytest tests/ --cov=src/parsercraft --cov-report=html
open htmlcov/index.html
```

---

## Documentation

### Documentation Standards

1. **Clear and Concise**: Be direct, avoid jargon
2. **Examples**: Include code examples
3. **Complete**: Cover all parameters and return values
4. **Accurate**: Keep docs in sync with code

### Documentation Structure

```
docs/
├── GETTING_STARTED.md      # Quick start guide
├── USER_MANUAL.md           # Complete user documentation
├── DEVELOPER_GUIDE.md       # For contributors
├── LANGUAGE_CONSTRUCTION_GUIDE.md
├── ARCHITECTURE.md          # System design
├── TROUBLESHOOTING.md       # Common issues
├── TUTORIALS.md             # Step-by-step tutorials
├── CONTRIBUTING.md          # This file
├── reference/
│   ├── API_REFERENCE.md     # Complete API docs
│   └── CLI_REFERENCE.md     # CLI documentation
└── guides/
    ├── LSP_INTEGRATION_GUIDE.md
    ├── MODULE_SYSTEM_GUIDE.md
    └── TYPE_SYSTEM_GUIDE.md
```

### Updating Documentation

When adding features:
1. Update relevant documentation files
2. Add examples
3. Update API reference
4. Add to changelog

---

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Added tests for new features
- [ ] Updated documentation
- [ ] Commits follow conventional format
- [ ] No merge conflicts with main

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #123

## How Has This Been Tested?
Describe testing approach

## Checklist
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Review Process

1. **Automated Checks**: CI/CD runs tests
2. **Code Review**: Maintainer reviews code
3. **Feedback**: Address review comments
4. **Approval**: PR approved by maintainer
5. **Merge**: Maintainer merges PR

### After Merge

- Your changes appear in `main` branch
- Included in next release
- Added to changelog
- You're credited in contributors!

---

## Recognition

Contributors are recognized in:
- `CONTRIBUTORS.md` file
- Release notes
- Project README
- Git history

---

## Questions?

- **General Questions**: Open a [Discussion](https://github.com/James-HoneyBadger/ParserCraft/discussions)
- **Bug Reports**: Open an [Issue](https://github.com/James-HoneyBadger/ParserCraft/issues)
- **Feature Requests**: Open an [Issue](https://github.com/James-HoneyBadger/ParserCraft/issues)
- **Chat**: Join our community (link TBD)

---

## Thank You! 🙏

Every contribution, no matter how small, makes ParserCraft better!

**Happy Contributing!** 🚀
