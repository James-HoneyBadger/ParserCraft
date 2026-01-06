# ParserCraft Troubleshooting Guide

**Version 2.0** | Common Issues and Solutions | January 2026

---

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Configuration Errors](#configuration-errors)
3. [Runtime Errors](#runtime-errors)
4. [Module System Issues](#module-system-issues)
5. [IDE and GUI Problems](#ide-and-gui-problems)
6. [Performance Issues](#performance-issues)
7. [Type System Errors](#type-system-errors)
8. [LSP Integration Issues](#lsp-integration-issues)

---

## Installation Issues

### "parsercraft: command not found"

**Symptoms**:
```bash
$ parsercraft create
bash: parsercraft: command not found
```

**Solutions**:

**Option 1**: Install package
```bash
cd /home/james/CodeCraft
pip install -e .
```

**Option 2**: Use Python module
```bash
python -m parsercraft.cli create
```

**Option 3**: Set PATH
```bash
export PATH=$PATH:$HOME/.local/bin
```

**Option 4**: Use PYTHONPATH
```bash
export PYTHONPATH=/home/james/CodeCraft/src:$PYTHONPATH
python -m parsercraft.cli create
```

---

### "No module named 'parsercraft'"

**Symptoms**:
```python
ModuleNotFoundError: No module named 'parsercraft'
```

**Solutions**:

**Option 1**: Install in development mode
```bash
cd /home/james/CodeCraft
pip install -e .
```

**Option 2**: Add to PYTHONPATH
```bash
export PYTHONPATH=/home/james/CodeCraft/src:$PYTHONPATH
```

**Option 3**: Use sys.path in code
```python
import sys
sys.path.insert(0, '/home/james/CodeCraft/src')
from parsercraft.language_config import LanguageConfig
```

---

### "tkinter not found" (IDE launch fails)

**Symptoms**:
```
ModuleNotFoundError: No module named 'tkinter'
```

**Solutions**:

**Ubuntu/Debian**:
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

**Fedora/RHEL/CentOS**:
```bash
sudo dnf install python3-tkinter
```

**macOS**:
```bash
# tkinter comes with Python from python.org
# If using Homebrew Python, reinstall with:
brew reinstall python-tk
```

**Windows**:
- tkinter is included with official Python installer
- If missing, reinstall Python with "tcl/tk" option checked

**Verification**:
```python
python3 -c "import tkinter; print('tkinter is available')"
```

---

### "pyyaml not found"

**Symptoms**:
```
ModuleNotFoundError: No module named 'yaml'
```

**Solution**:
```bash
pip install pyyaml
```

**Alternative**: Use JSON instead of YAML
```bash
# Save as JSON
parsercraft create --output my_lang.json

# JSON is always available (Python stdlib)
```

---

## Configuration Errors

### "Invalid configuration format"

**Symptoms**:
```
ValueError: Invalid configuration format
```

**Solutions**:

**Check YAML syntax**:
```bash
# Validate YAML
python -c "import yaml; yaml.safe_load(open('my_lang.yaml'))"
```

**Check JSON syntax**:
```bash
# Validate JSON
python -c "import json; json.load(open('my_lang.json'))"
```

**Use validator**:
```bash
parsercraft validate my_lang.yaml
```

**Common YAML mistakes**:
```yaml
# ❌ Wrong: Inconsistent indentation
keyword_mappings:
  if: cuando
   else: sino

# ✅ Correct: Consistent 2-space indentation
keyword_mappings:
  if: cuando
  else: sino

# ❌ Wrong: Missing colon
keyword_mappings
  if: cuando

# ✅ Correct: Colon after key
keyword_mappings:
  if: cuando
```

---

### "Keyword mapping conflict"

**Symptoms**:
```
ConfigurationError: Keyword 'print' conflicts with Python builtin
```

**Solution**: Don't map to Python reserved words
```yaml
# ❌ Wrong: Conflicts with Python
keyword_mappings:
  myprint: print  # 'print' is already Python keyword

# ✅ Correct: Map FROM custom TO Python
keyword_mappings:
  imprimir: print  # 'imprimir' → 'print'
```

---

### "Missing required fields"

**Symptoms**:
```
ValidationError: Missing required field 'name'
```

**Solution**: Include all required fields
```yaml
# Minimum required configuration
name: MyLanguage
version: 1.0
description: My custom language

keyword_mappings: {}
builtin_functions: {}
```

---

## Runtime Errors

### "Translation failed"

**Symptoms**:
```
TranslationError: Could not translate code
```

**Causes & Solutions**:

**Cause 1**: Keyword not defined
```yaml
# ❌ Missing keyword mapping
keyword_mappings:
  if: cuando
  # Missing 'else' mapping

# Program uses 'sino' but it's not mapped
```

**Solution**: Add all needed keywords
```yaml
keyword_mappings:
  if: cuando
  else: sino  # Add missing mapping
```

**Cause 2**: Function not defined
```python
# Program uses 'imprimir' but not defined
imprimir("Hello")  # Error!
```

**Solution**: Add function mapping
```yaml
builtin_functions:
  imprimir:
    maps_to: print
```

---

### "Syntax error in generated Python code"

**Symptoms**:
```
SyntaxError: invalid syntax (line 42)
```

**Debug**: View translated code
```bash
parsercraft translate --config my_lang.yaml --input program.ml
```

**Common issues**:

**Issue 1**: Indentation problems
```python
# Original custom code
cuando True:
say("Hello")  # ❌ Not indented

# Fix: Proper indentation
cuando True:
    say("Hello")  # ✅ Indented
```

**Issue 2**: Missing colons
```python
# ❌ Missing colon
funcion test()
    pass

# ✅ With colon
funcion test():
    pass
```

---

### "NameError: name 'X' is not defined"

**Symptoms**:
```
NameError: name 'cuando' is not defined
```

**Cause**: Keyword not translated

**Solution**: Ensure runtime is loaded with config
```python
# ❌ Wrong: No config loaded
runtime = LanguageRuntime.get_instance()
runtime.execute(code)  # Error!

# ✅ Correct: Load config first
LanguageRuntime.load_config('my_lang.yaml')
runtime = LanguageRuntime.get_instance()
runtime.execute(code)  # Works!
```

---

## Module System Issues

### "Module not found"

**Symptoms**:
```
ModuleLoadError: Cannot find module 'mymodule'
```

**Solutions**:

**Check search paths**:
```yaml
module_options:
  search_paths:
    - "."
    - "./lib"
    - "./modules"
```

**Verify file exists**:
```bash
ls -la ./lib/mymodule.py
ls -la ./modules/mymodule.py
```

**Use absolute imports**:
```python
# Instead of relative
import mymodule  # May fail

# Use absolute
from lib import mymodule  # Better
```

---

### "Circular import detected"

**Symptoms**:
```
ModuleLoadError: Circular import: A -> B -> A
```

**Solutions**:

**Option 1**: Refactor to remove cycle
```python
# Before (circular):
# a.py
from b import func_b

# b.py
from a import func_a  # ❌ Circular!

# After (refactored):
# a.py
from c import shared_func

# b.py
from c import shared_func  # ✅ No cycle

# c.py (new)
def shared_func():
    pass
```

**Option 2**: Use lazy imports
```python
# Import inside function
def my_function():
    from b import func_b  # Import only when needed
    func_b()
```

---

## IDE and GUI Problems

### IDE won't launch

**Symptoms**:
```
$ python -m parsercraft.launch_ide
# No window appears
```

**Solutions**:

**Check tkinter**:
```python
python3 -c "import tkinter; tkinter.Tk()"
# Should open empty window
```

**Check DISPLAY (Linux)**:
```bash
echo $DISPLAY
# Should show :0 or similar

# If empty, set it:
export DISPLAY=:0
```

**Run with PYTHONPATH**:
```bash
cd /home/james/CodeCraft
PYTHONPATH=src:$PYTHONPATH python3 src/parsercraft/launch_ide.py
```

**Check for errors**:
```bash
python3 src/parsercraft/launch_ide.py 2>&1 | tee ide_error.log
```

---

### "No such file or directory: run-parsercraft.sh"

**Symptoms**:
```bash
$ ./run-parsercraft.sh
bash: ./run-parsercraft.sh: No such file or directory
```

**Solutions**:

**Option 1**: Launch directly
```bash
cd /home/james/CodeCraft
PYTHONPATH=src:$PYTHONPATH python3 src/parsercraft/launch_ide.py
```

**Option 2**: Create script
```bash
cat > run-parsercraft.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
PYTHONPATH="$(pwd)/src:$PYTHONPATH" python3 src/parsercraft/launch_ide.py
EOF

chmod +x run-parsercraft.sh
./run-parsercraft.sh
```

---

## Performance Issues

### Slow execution

**Symptoms**: Programs run slowly

**Solutions**:

**Enable optimization**:
```yaml
optimization:
  level: 2  # 0=none, 1=basic, 2=aggressive
  inline_functions: true
  constant_folding: true
```

**Compile to bytecode**:
```bash
parsercraft compile --config my_lang.yaml program.ml
parsercraft run --config my_lang.yaml program.pbc  # Faster
```

**Profile code**:
```bash
parsercraft profile --config my_lang.yaml program.ml
```

---

### High memory usage

**Symptoms**: Process uses excessive RAM

**Solutions**:

**Clear module cache**:
```python
runtime = LanguageRuntime.get_instance()
runtime._module_cache.clear()
```

**Limit recursion**:
```python
import sys
sys.setrecursionlimit(1000)  # Default, reduce if needed
```

**Process large files in chunks**:
```python
# Instead of loading entire file
with open('huge_file.txt') as f:
    for line in f:  # Process line by line
        process(line)
```

---

## Type System Errors

### "Type mismatch"

**Symptoms**:
```
TypeError: Expected 'int' but got 'str'
```

**Solutions**:

**Add type annotations**:
```python
# Before (implicit types)
funcion sumar(a, b):
    devolver a + b

# After (explicit types)
funcion sumar(a: entero, b: entero) -> entero:
    devolver a + b
```

**Use type conversion**:
```python
# Ensure correct types
resultado = sumar(entero("5"), 3)  # Convert string to int
```

---

### "Type inference failed"

**Symptoms**:
```
TypeInferenceError: Cannot infer type for variable 'x'
```

**Solution**: Add explicit annotation
```python
# ❌ Ambiguous
x = None
x = "hello"  # What type is x?

# ✅ Clear
x: texto = None
x = "hello"  # x is definitely 'texto'
```

---

## LSP Integration Issues

### LSP server won't start

**Symptoms**:
```
$ parsercraft lsp --config my_lang.yaml
Error: Address already in use
```

**Solutions**:

**Check if port is in use**:
```bash
# Linux/macOS
lsof -i :8080

# Windows
netstat -ano | findstr :8080
```

**Use different port**:
```bash
parsercraft lsp --config my_lang.yaml --port 9000
```

**Kill existing process**:
```bash
# Linux/macOS
kill $(lsof -t -i:8080)

# Windows
taskkill /PID <PID> /F
```

---

### IDE not recognizing LSP server

**Symptoms**: No autocomplete, no syntax highlighting

**Solutions**:

**VS Code**: Check settings.json
```json
{
  "mylanguage.lsp.enabled": true,
  "mylanguage.lsp.serverPath": "/path/to/parsercraft",
  "mylanguage.lsp.configFile": "/path/to/my_lang.yaml",
  "mylanguage.lsp.port": 8080
}
```

**Restart LSP server**:
1. Stop server: Ctrl+C
2. Restart: `parsercraft lsp --config my_lang.yaml`
3. Reload IDE window

---

## Getting More Help

### Enable Debug Mode

```bash
# CLI debug mode
parsercraft run --config my_lang.yaml program.ml --debug --verbose

# Python debug mode
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Generate Debug Report

```python
from parsercraft.language_runtime import LanguageRuntime
from parsercraft.language_config import LanguageConfig

config = LanguageConfig.load('my_lang.yaml')
runtime = LanguageRuntime.get_instance()

print("Config:", config.to_dict())
print("Runtime:", runtime.get_reverse_mappings())
```

### Check Version

```bash
parsercraft --version
python3 --version
pip list | grep parsercraft
```

### Report Bugs

Include:
1. ParserCraft version
2. Python version
3. Operating system
4. Configuration file
5. Code that fails
6. Complete error message
7. Steps to reproduce

**GitHub Issues**: https://github.com/James-HoneyBadger/ParserCraft/issues

---

## Quick Diagnostics

```bash
# Full system check
python3 << 'EOF'
import sys
print(f"Python: {sys.version}")

try:
    import parsercraft
    print(f"ParserCraft: Available")
except:
    print("ParserCraft: NOT FOUND")

try:
    import tkinter
    print("tkinter: Available")
except:
    print("tkinter: NOT FOUND")

try:
    import yaml
    print("PyYAML: Available")
except:
    print("PyYAML: NOT FOUND (JSON only)")

print(f"PYTHONPATH: {sys.path}")
EOF
```

---

## See Also

- [Getting Started Guide](GETTING_STARTED.md)
- [User Manual](USER_MANUAL.md)
- [FAQ](FAQ.md)
- [GitHub Issues](https://github.com/James-HoneyBadger/ParserCraft/issues)

---

**Still having issues?** Open a GitHub issue with details!
