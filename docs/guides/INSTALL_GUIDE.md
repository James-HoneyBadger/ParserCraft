# Installation & Setup Guide

**Honey Badger Language Construction Set v4.0**  
Complete Installation & Configuration Instructions  
December 3, 2025

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Install](#quick-install)
3. [Detailed Installation](#detailed-installation)
4. [Virtual Environment Setup](#virtual-environment-setup)
5. [Package Installation Methods](#package-installation-methods)
6. [Verification & Testing](#verification--testing)
7. [IDE Setup & Configuration](#ide-setup--configuration)
8. [Troubleshooting](#troubleshooting)
9. [Uninstalling](#uninstalling)

---

## System Requirements

### Minimum Requirements

| Component | Requirement | Notes |
|-----------|-------------|-------|
| **Python** | 3.8+ | 3.10+ recommended for best compatibility |
| **OS** | Linux, macOS, Windows | Tested on all major platforms |
| **RAM** | 512 MB | 2 GB+ recommended for development |
| **Disk** | 100 MB | For installation + dependencies |
| **GUI** | Tkinter | Usually included with Python |

### Python Installation

#### Linux (Debian/Ubuntu)
```bash
# Check Python version
python3 --version

# If not installed
sudo apt-get update
sudo apt-get install python3.10 python3-pip python3-tk
sudo apt-get install python3.10-dev  # For development
```

#### macOS
```bash
# Using Homebrew
brew install python@3.10
brew install python-tk@3.10

# Or use official Python installer from python.org
```

#### Windows
```bash
# Download from python.org and run installer
# Or use Windows Package Manager
winget install Python.Python.3.10

# Verify Tkinter is included
python -m tkinter
```

### Optional Dependencies

| Package | Purpose | Install |
|---------|---------|---------|
| **PyYAML** | YAML config support | `pip install pyyaml` |
| **pytest** | Testing framework | `pip install pytest` |
| **black** | Code formatting | `pip install black` |
| **mypy** | Type checking | `pip install mypy` |

---

## Quick Install

### For End Users (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/James-HoneyBadger/HB_Language_Construction.git
cd HB_Language_Construction

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install package
pip install -e .

# 5. Verify installation
hblcs --help

# 6. Launch IDE
hblcs-ide
```

### For Developers (10 minutes)

```bash
# 1. Clone repository
git clone https://github.com/James-HoneyBadger/HB_Language_Construction.git
cd HB_Language_Construction

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# 3. Install with development tools
pip install -e .[dev]

# 4. Verify installation
python -m pytest tests/

# 5. Launch IDE
hblcs-ide
```

---

## Detailed Installation

### Step 1: Clone or Download Repository

#### Using Git
```bash
# Clone repository
git clone https://github.com/James-HoneyBadger/HB_Language_Construction.git
cd HB_Language_Construction

# Or if you have fork
git clone https://github.com/YOUR_USERNAME/HB_Language_Construction.git
cd HB_Language_Construction
```

#### Manual Download
```bash
# Download ZIP from GitHub
# Extract to desired location
cd HB_Language_Construction
```

### Step 2: Verify Python Installation

```bash
# Check Python version (must be 3.8+)
python3 --version

# Check pip is installed
pip3 --version

# Verify Tkinter is available
python3 -m tkinter
```

### Step 3: Create Virtual Environment

**What is a Virtual Environment?**
A virtual environment is an isolated Python environment where you can install packages without affecting your system Python.

```bash
# Create virtual environment
python3 -m venv venv

# Verify directory structure
ls venv/  # Linux/macOS
dir venv  # Windows
```

### Step 4: Activate Virtual Environment

```bash
# Linux/macOS
source venv/bin/activate

# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

You should see `(venv)` prefix in your terminal prompt.

### Step 5: Upgrade pip

```bash
# Ensure pip is up to date
pip install --upgrade pip

# Verify
pip --version
```

### Step 6: Install the Package

```bash
# Standard installation (user mode)
pip install -e .

# Or installation with development tools
pip install -e .[dev]

# Or installation with all optional features
pip install -e .[dev,docs]
```

**Installation Options:**

| Command | Purpose | Best For |
|---------|---------|----------|
| `pip install -e .` | Basic installation | Users |
| `pip install -e .[dev]` | Development tools | Developers |
| `pip install -e .[docs]` | Documentation tools | Documentation |
| `pip install -e .[dev,docs]` | Everything | Full development |

---

## Virtual Environment Setup

### Creating Virtual Environment

```bash
# Create virtual environment with specific Python version
python3.10 -m venv venv

# Or with custom name
python3 -m venv my_project_env
source my_project_env/bin/activate
```

### Managing Virtual Environment

```bash
# Activate
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate      # Windows

# Deactivate
deactivate

# Delete (after deactivating)
rm -rf venv  # Linux/macOS
rmdir venv   # Windows (if empty)
```

### Virtual Environment Files

After creation, your venv directory contains:

```
venv/
├── bin/           # Linux/macOS executables
│   ├── python
│   ├── pip
│   ├── activate
│   ├── hblcs       # CLI tool
│   └── hblcs-ide   # IDE launcher
├── lib/           # Python packages
├── include/       # Header files
└── pyvenv.cfg     # Configuration
```

### Troubleshooting Virtual Environment

**Issue: `python: command not found`**
```bash
# Use python3 instead
python3 -m venv venv
source venv/bin/activate
```

**Issue: `Permission denied` on Windows**
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

**Issue: `venv` activation doesn't work**
```bash
# Reinstall venv
python3 -m venv venv --clear
source venv/bin/activate
```

---

## Package Installation Methods

### Method 1: From Source (Recommended)

```bash
# Install from local source
cd /path/to/HB_Language_Construction
pip install -e .

# Verify
hblcs --version
```

### Method 2: From GitHub

```bash
# Install directly from GitHub
pip install git+https://github.com/James-HoneyBadger/HB_Language_Construction.git

# Or from specific branch
pip install git+https://github.com/James-HoneyBadger/HB_Language_Construction.git@main
```

### Method 3: Wheel Installation

```bash
# Build wheel
python setup.py bdist_wheel

# Install wheel
pip install dist/hb_lcs-*.whl
```

### Method 4: Development Installation

```bash
# Install in editable mode (best for development)
pip install -e .

# Changes to source code are immediately available
# No need to reinstall after edits
```

### Verifying Installation

```bash
# Check package is installed
pip show hb_lcs

# Run CLI help
hblcs --help

# List available commands
hblcs list-commands

# Launch IDE
hblcs-ide
```

---

## Verification & Testing

### Basic Verification

```bash
# 1. Verify Python installation
python3 --version

# 2. Verify venv activation
which python  # Should point to venv/bin/python

# 3. Verify package installation
pip show hb_lcs

# 4. Test CLI tool
hblcs --version
hblcs --help

# 5. Test IDE launch
hblcs-ide  # Should open GUI window
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_phase9_10_features.py -v

# Run with coverage
pip install pytest-cov
python -m pytest tests/ --cov=src/hb_lcs

# Run tests in parallel (faster)
pip install pytest-xdist
python -m pytest tests/ -n auto
```

### Test Results

```
tests/test_phase9_10_features.py::test_phase_ix_mobile_native_apps PASSED
tests/test_phase9_10_features.py::test_phase_ix_cloud_integration PASSED
tests/test_phase9_10_features.py::test_phase_ix_advanced_analytics PASSED
tests/test_phase9_10_features.py::test_phase_x_enterprise_integration PASSED
tests/test_phase9_10_features.py::test_phase_x_ai_assistance PASSED
tests/test_phase9_10_features.py::test_phase_x_real_time_collaboration PASSED
tests/test_phase9_10_features.py::test_phase_x_advanced_security PASSED

======================== 31 passed in 2.34s ========================
```

### Manual Testing

```bash
# Test IDE launches
hblcs-ide

# Test CLI
hblcs list-presets
hblcs create --preset python_like --output test_lang.yaml
hblcs validate test_lang.yaml
hblcs info test_lang.yaml

# Test language creation
python demos/demo_language_construction.py
```

---

## IDE Setup & Configuration

### Launching the IDE

```bash
# Standard launch
hblcs-ide

# Or from source
python src/hb_lcs/launch_ide.py

# Or as Python module
python -m hb_lcs.launch_ide
```

### IDE Configuration

IDE settings are stored in `~/.hb_lcs/settings.json`:

```json
{
  "theme": "light",
  "editor_font_size": 11,
  "console_font_size": 10,
  "show_line_numbers": true,
  "show_minimap": false,
  "auto_save": false,
  "syntax_highlighting": true,
  "code_completion": true,
  "geometry": "1400x900",
  "last_project": null,
  "recent_files": [],
  "recent_configs": []
}
```

### Customizing IDE Settings

Inside IDE:
1. Menu: **Edit → Preferences**
2. Adjust font size, theme, features
3. Click **Save Preferences**

Or manually edit `~/.hb_lcs/settings.json`:

```bash
# Open settings file
nano ~/.hb_lcs/settings.json
# Edit and save
```

### IDE First Launch

```bash
# First launch creates default config
hblcs-ide

# Automatically creates:
# - ~/.hb_lcs/settings.json
# - ~/.hb_lcs/recent_files.json
# - ~/.hb_lcs/projects/
```

---

## Troubleshooting

### Installation Issues

#### Issue: `pip: command not found`
```bash
# Use pip3
pip3 --version
pip3 install -e .

# Or use python module
python3 -m pip install -e .
```

#### Issue: `ModuleNotFoundError: No module named 'tkinter'`
```bash
# Install tkinter
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS
brew install python-tk@3.10

# Windows
# Re-run Python installer and check "tcl/tk and IDLE"
```

#### Issue: `Permission denied` when installing
```bash
# Use --user flag
pip install --user -e .

# Or activate virtual environment
source venv/bin/activate
pip install -e .
```

### Runtime Issues

#### IDE Won't Launch

```bash
# Check if tkinter works
python3 -m tkinter

# If GUI appears, tkinter is fine
# Check if hb_lcs is installed
pip show hb_lcs

# Try launching from source
python src/hb_lcs/launch_ide.py

# Check Python version
python3 --version  # Should be 3.8+
```

#### CLI Command Not Found

```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate      # Windows

# Verify installation
pip show hb_lcs

# Try running from source
python src/hb_lcs/cli.py --help
```

#### Test Failures

```bash
# Check Python version
python --version  # Need 3.8+

# Check dependencies
pip list

# Reinstall with dev tools
pip install -e .[dev]

# Run tests with verbose output
python -m pytest tests/ -vv

# Check specific test
python -m pytest tests/test_phase9_10_features.py::test_phase_ix_mobile_native_apps -vv
```

### Performance Issues

#### IDE Is Slow

```bash
# Disable minimap
In IDE: Edit → Preferences → show_minimap = false

# Disable syntax highlighting
In IDE: Edit → Preferences → syntax_highlighting = false

# Disable code completion
In IDE: Edit → Preferences → code_completion = false

# Use light theme
In IDE: Edit → Preferences → theme = light
```

#### Memory Usage

```bash
# Close other applications
# Disable features in settings
# Use minimal config files
# Restart IDE if needed
```

### File Permission Issues

#### Linux/macOS

```bash
# Fix file permissions
chmod +x venv/bin/python
chmod +x venv/bin/hblcs
chmod +x venv/bin/hblcs-ide

# Or reset venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

#### Windows

```bash
# Run Command Prompt as Administrator
# Then activate venv
venv\Scripts\activate

# Install package
pip install -e .
```

---

## Uninstalling

### Removing Virtual Environment

```bash
# Deactivate first
deactivate

# Remove directory
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows
```

### Uninstalling Package

```bash
# While in virtual environment
pip uninstall hb_lcs

# Or with confirmation
pip uninstall -y hb_lcs
```

### Removing Configuration

```bash
# Remove IDE settings
rm -rf ~/.hb_lcs  # Linux/macOS
rmdir %APPDATA%\.hb_lcs  # Windows

# This removes:
# - settings.json
# - recent files
# - project cache
```

### Clean Complete Removal

```bash
# Remove virtual environment
rm -rf venv

# Remove IDE config
rm -rf ~/.hb_lcs

# Remove source code (optional)
cd ..
rm -rf HB_Language_Construction
```

---

## Post-Installation

### Initial Configuration

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Verify installation
hblcs --version

# 3. Create first language
hblcs create --preset python_like --output my_language.yaml

# 4. Validate configuration
hblcs validate my_language.yaml

# 5. Launch IDE
hblcs-ide
```

### Learning Resources

- **Quick Start**: See [USER_GUIDE.md](guides/USER_GUIDE.md)
- **Language Development**: See [LANGUAGE_DEVELOPMENT_GUIDE.md](guides/LANGUAGE_DEVELOPMENT_GUIDE.md)
- **API Reference**: See [TECHNICAL_REFERENCE.md](reference/TECHNICAL_REFERENCE.md)
- **Examples**: Check `configs/examples/` and `demos/`

### Next Steps

1. **Read User Guide** for basic usage
2. **Try IDE** - Launch with `hblcs-ide`
3. **Create First Language** - Use `hblcs create --interactive`
4. **Explore Examples** - Check `configs/examples/`
5. **Read Development Guide** for advanced features

---

## Getting Help

### Documentation
- **[User Guide](guides/USER_GUIDE.md)** - How to use the system
- **[Language Development Guide](guides/LANGUAGE_DEVELOPMENT_GUIDE.md)** - Creating languages
- **[Technical Reference](reference/TECHNICAL_REFERENCE.md)** - API documentation
- **[IDE Guide](guides/IDE_README.md)** - IDE features

### Support
```bash
# Get help from CLI
hblcs --help
hblcs create --help

# Check troubleshooting
grep -r "Troubleshooting" docs/

# Run tests to verify installation
python -m pytest tests/ -v
```

### Examples
- **Presets**: `hblcs list-presets`
- **Demo Script**: `python demos/demo_language_construction.py`
- **Language Configs**: See `configs/examples/`
- **TeachScript**: See `demos/teachscript/examples/`

---

## Appendix: Common Commands

### Virtual Environment
```bash
source venv/bin/activate           # Activate (Linux/macOS)
venv\Scripts\activate              # Activate (Windows)
deactivate                         # Deactivate
```

### Package Management
```bash
pip install -e .                   # Install editable
pip show hb_lcs                    # Show package info
pip list                           # List installed
pip uninstall hb_lcs               # Uninstall
```

### CLI Tools
```bash
hblcs --help                       # Show help
hblcs create --preset python_like  # Create config
hblcs validate my.yaml             # Validate
hblcs info my.yaml                 # Show info
hblcs list-presets                 # List presets
```

### IDE
```bash
hblcs-ide                          # Launch IDE
python src/hb_lcs/launch_ide.py   # Launch from source
```

### Testing
```bash
python -m pytest tests/ -v         # Run all tests
python -m pytest tests/ --cov      # With coverage
pytest tests/test_*.py -v          # Run specific tests
```

---

**Installation Guide v1.0**  
December 3, 2025  
Compatible with HB Language Construction Set v4.0
