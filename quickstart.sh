#!/bin/bash
# TeachScript + ParserCraft IDE Quick Start Script

echo "================================================"
echo "TeachScript + ParserCraft IDE Quick Start"
echo "================================================"
echo ""

# Check Python
echo "Checking Python installation..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python 3 not found!"
    exit 1
fi

echo "✓ Python is installed"
echo ""

# Check current directory
if [ ! -f "setup.py" ]; then
    echo "ERROR: Please run this from the ParserCraft project root directory"
    echo "Expected: /home/james/ParserCraft"
    exit 1
fi

echo "✓ Running from correct directory"
echo ""

# Install if needed
echo "Checking installation..."
python3 -c "from src.parsercraft.teachscript_runtime import get_runtime" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing ParserCraft..."
    pip install -e . > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "✓ Installation successful"
    else
        echo "ERROR: Installation failed"
        exit 1
    fi
else
    echo "✓ Already installed"
fi
echo ""

# Test TeachScript
echo "Testing TeachScript runtime..."
python3 << 'EOF'
from src.parsercraft.teachscript_runtime import get_runtime
runtime = get_runtime()
output, error = runtime.run('say("TeachScript is working!")')
if not error:
    print("✓ TeachScript runtime functional")
else:
    print("ERROR:", error)
EOF

if [ $? -ne 0 ]; then
    echo "ERROR: Runtime test failed"
    exit 1
fi

echo ""
echo "================================================"
echo "✓ All checks passed!"
echo "================================================"
echo ""
echo "To launch the IDE, run:"
echo ""
echo "  python -m src.parsercraft.launch_ide_teachscript"
echo ""
echo "Or:"
echo ""
echo "  cd /home/james/ParserCraft"
echo "  python -m src.parsercraft.launch_ide_teachscript"
echo ""
echo "To run a TeachScript file directly:"
echo ""
echo "  python demos/teachscript/run_teachscript.py demos/teachscript/examples/01_hello_world.teach"
echo ""
echo "To run tests:"
echo ""
echo "  python -m pytest tests/test_teachscript.py -v"
echo ""
echo "================================================"
echo "Documentation Files:"
echo "================================================"
echo ""
echo "Main Integration Guide:"
echo "  docs/teachscript/TEACHSCRIPT_IDE_INTEGRATION.md"
echo ""
echo "Advanced Features:"
echo "  docs/teachscript/TEACHSCRIPT_ADVANCED_GUIDE.md"
echo ""
echo "Module Reference:"
echo "  TEACHSCRIPT_MODULES_REFERENCE.md"
echo ""
echo "Setup Guide:"
echo "  TEACHSCRIPT_SETUP_GUIDE.py"
echo ""
echo "Example Programs:"
echo "  demos/teachscript/examples/ (12 programs)"
echo ""
echo "================================================"
echo "Happy TeachScripting! 🎉"
echo "================================================"
