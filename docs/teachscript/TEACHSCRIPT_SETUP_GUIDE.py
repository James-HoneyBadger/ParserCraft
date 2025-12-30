#!/usr/bin/env python3
"""
TeachScript IDE Installation and Setup Guide

Complete setup instructions for the TeachScript + CodeCraft IDE integration.
"""

SETUP_GUIDE = """
================================================================================
  TEACHSCRIPT + CODECRAFT IDE - INSTALLATION & SETUP GUIDE
================================================================================

================================================================================
  SYSTEM REQUIREMENTS
================================================================================

Minimum:
  • Python 3.8+
  • Tkinter (usually included with Python)
  • 50 MB disk space
  • Any OS (Windows, macOS, Linux)

Recommended:
  • Python 3.10+
  • 4GB RAM
  • SSD storage
  • Fast internet connection (for examples)

================================================================================
  INSTALLATION STEPS
================================================================================

STEP 1: Clone or Extract the Repository
  
  $ git clone https://github.com/James-HoneyBadger/CodeCraft.git
  $ cd CodeCraft
  
  OR if you have it extracted:
  
  $ cd /home/james/CodeCraft

STEP 2: Install the Package

  $ pip install -e .
  
  Or with development tools:
  
  $ pip install -e .[dev]
  
  Optional: Install YAML support for config files:
  
  $ pip install pyyaml

STEP 3: Verify Installation

  $ python -c "from src.hb_lcs.teachscript_runtime import TeachScriptRuntime; print('✓ TeachScript runtime installed')"
  $ python -c "from src.hb_lcs.ide_teachscript_integration import TeachScriptIDEIntegration; print('✓ IDE integration installed')"

STEP 4: Test the Runtime (Optional)

  $ python demos/teachscript/run_teachscript.py demos/teachscript/examples/01_hello_world.teach
  
  Expected output:
    Hello, World!
    Welcome to TeachScript!

================================================================================
  LAUNCHING THE IDE
================================================================================

OPTION 1: Using the Enhanced TeachScript IDE Launcher
  
  $ cd /home/james/CodeCraft
  $ python -m src.hb_lcs.launch_ide_teachscript
  
  This launches the IDE with full TeachScript integration.

OPTION 2: Using the Original IDE Launcher
  
  $ python -m src.hb_lcs.launch_ide
  
  This launches the IDE without TeachScript-specific features
  (though TeachScript runtime is still available).

OPTION 3: Direct Python Execution
  
  $ python -m src.hb_lcs.ide
  
  Direct IDE execution without launcher.

================================================================================
  FIRST TIME SETUP IN IDE
================================================================================

1. WELCOME SCREEN
   • The IDE launches and displays the welcome screen
   • You see the main editor area, console, and configuration panels

2. CREATE YOUR FIRST PROJECT
   • Go to: File → New → TeachScript Project
   • Select "Hello World" template
   • Click "Create"
   • Choose save location (e.g., ~/projects/my_teachscript_projects/)
   • The template code appears in the editor

3. RUN YOUR CODE
   • Press Ctrl+Shift+T or go to TeachScript → Run TeachScript
   • Output appears in the console at the bottom
   • Should see:
       === TeachScript Output ===
       Hello, World!
       Welcome to TeachScript!

4. EXPLORE FEATURES
   • Try TeachScript → Preview Python Code to see transpilation
   • Try TeachScript → Check Syntax for validation
   • Try TeachScript → Interactive Tutorial for lessons
   • Try TeachScript → Language Reference for syntax help

================================================================================
  PROJECT TEMPLATES AVAILABLE
================================================================================

When creating a new TeachScript project, you can choose from:

1. Hello World
   Simple output program
   Demonstrates: say() function

2. Variables
   Working with variables
   Demonstrates: remember keyword, input(), type conversion

3. Conditionals
   If/else statements
   Demonstrates: when/otherwise, logical operators

4. Loops
   For and while loops
   Demonstrates: repeat_for, repeat_while

5. Functions
   Defining and calling functions
   Demonstrates: teach, give_back, parameter passing

6. Lists
   Working with lists/arrays
   Demonstrates: list operations, iteration

7. Interactive Game
   Number guessing game
   Demonstrates: loops, conditionals, random numbers

8. (More can be added)

================================================================================
  KEYBOARD SHORTCUTS
================================================================================

TeachScript-Specific:
  Ctrl+Shift+T       Run TeachScript
  Ctrl+Space         Code Completion
  
General IDE:
  Ctrl+N             New File
  Ctrl+O             Open File
  Ctrl+S             Save File
  Ctrl+Shift+S       Save As
  Ctrl+Z             Undo
  Ctrl+Y             Redo
  Ctrl+C             Copy
  Ctrl+V             Paste
  Ctrl+X             Cut
  Ctrl+F             Find
  Ctrl+H             Find & Replace

================================================================================
  COMMAND LINE USAGE
================================================================================

If you prefer command-line execution:

RUN A TEACHSCRIPT FILE:
  
  $ python demos/teachscript/run_teachscript.py your_file.teach
  
TRANSPILE TO PYTHON:
  
  $ python -c "
    from src.hb_lcs.teachscript_runtime import get_runtime
    runtime = get_runtime()
    with open('program.teach') as f:
        code = f.read()
    print(runtime.get_transpiled_code(code))
  "

INTERACTIVE REPL:
  
  $ python -i -c "
    from src.hb_lcs.teachscript_runtime import get_runtime
    runtime = get_runtime()
    print('TeachScript REPL - type code and press Enter')
  "

================================================================================
  CONFIGURATION FILES
================================================================================

TeachScript Configuration:
  Location: configs/teachscript.json
  Contains: Language keywords and built-in functions
  Modifiable: Yes, but changes require restart
  Purpose: Defines how TeachScript maps to Python

Language Configs:
  Location: configs/examples/
  Includes: Basic, Python-like, JavaScript-like variants
  Usage: Can create different language variants

IDE Settings:
  Stored in: System temp directory (or home directory)
  Persists: Window size, recent files, preferences
  Reset: Delete settings file to return to defaults

================================================================================
  TROUBLESHOOTING
================================================================================

ISSUE: "ModuleNotFoundError: No module named 'src.hb_lcs'"
  SOLUTION: Run from the project root directory
            cd /home/james/CodeCraft
            python -m src.hb_lcs.launch_ide_teachscript

ISSUE: "No module named 'tkinter'"
  SOLUTION: Install tkinter for your Python version
            Ubuntu/Debian: sudo apt-get install python3-tk
            Fedora: sudo dnf install python3-tkinter
            macOS: Usually included with Python

ISSUE: IDE window doesn't appear
  SOLUTION: Check if display is available (might need X11 forwarding)
            Try: python -c "import tkinter; print('Tkinter OK')"

ISSUE: Code runs but no output appears
  SOLUTION: Check console panel is visible
            Go to View → Show Console
            Verify code doesn't have syntax errors

ISSUE: Syntax highlighting not working
  SOLUTION: Restart IDE
            Check that teachscript_highlighting.py is installed
            Try: python -c "from src.hb_lcs.teachscript_highlighting import TeachScriptHighlighter; print('✓')"

ISSUE: Code completion not working
  SOLUTION: Check that code completion is enabled
            Settings → Editor → Enable Code Completion
            Restart IDE

================================================================================
  TESTING YOUR INSTALLATION
================================================================================

RUN THE TEST SUITE:
  
  $ cd /home/james/CodeCraft
  $ python -m pytest tests/
  
  Or test specific TeachScript features:
  
  $ python -m pytest tests/test_teachscript.py -v

MANUAL TESTING:
  
  1. Launch IDE: python -m src.hb_lcs.launch_ide_teachscript
  2. Create Hello World project
  3. Run with Ctrl+Shift+T
  4. Should see output in console
  5. Try Preview Python Code
  6. Try Check Syntax
  7. Try Interactive Tutorial

COMMAND-LINE TESTING:
  
  $ python -c "
    from src.hb_lcs.teachscript_runtime import get_runtime
    runtime = get_runtime()
    output, error = runtime.run('say(\"Test\")')
    print(output)
  "
  
  Expected output: Test

================================================================================
  LEARNING PATH
================================================================================

BEGINNER (Day 1):
  □ Launch IDE
  □ Create Hello World project
  □ Run code with Ctrl+Shift+T
  □ View Preview Python Code
  □ Complete Lesson 1: Say Hello

BEGINNER+ (Day 2-3):
  □ Complete Lesson 2: Variables
  □ Complete Lesson 3: Input
  □ Create and run Variables template
  □ Create and run Calculator template

INTERMEDIATE (Week 1-2):
  □ Complete Lesson 4: Conditionals
  □ Complete Lesson 5: Loops
  □ Create game using guessing_game template
  □ Write your own simple program

ADVANCED (Week 3+):
  □ Read Advanced Guide
  □ Use educational libraries (TSMath, TSGame, etc.)
  □ Create game with TSGame library
  □ Analyze data with TSMath
  □ Build multi-function programs

================================================================================
  CUSTOMIZATION
================================================================================

CHANGE THEME:
  File → Settings → Theme
  Choose: Light, Dark, Custom
  (IDE may need restart)

ADD MORE PROJECT TEMPLATES:
  Edit: src/hb_lcs/ide_teachscript_integration.py
  Find: TEMPLATES dictionary
  Add new template entries

CREATE CUSTOM KEYWORDS:
  Edit: src/hb_lcs/teachscript_runtime.py
  Find: KEYWORD_MAP dictionary
  Add mappings
  Restart IDE

EXTEND LIBRARIES:
  Edit: src/hb_lcs/teachscript_libraries.py
  Add new classes or functions
  Modify TeachScriptEnvironment._setup_libraries()

================================================================================
  NEXT STEPS AFTER INSTALLATION
================================================================================

1. READ THE DOCUMENTATION:
   • TEACHSCRIPT_IDE_INTEGRATION.md - Main guide
   • TEACHSCRIPT_ADVANCED_GUIDE.md - Advanced features
   • TEACHSCRIPT_MANUAL.md - Language manual

2. EXPLORE EXAMPLE PROGRAMS:
   • demos/teachscript/examples/ contains 12 programs
   • Start with 01_hello_world.teach
   • Progress to 10_scientific_calculator.teach

3. USE INTERACTIVE TUTORIALS:
   • Launch IDE
   • Go to TeachScript → Interactive Tutorial
   • Complete 5 lessons
   • ~30 minutes total

4. BUILD YOUR OWN PROGRAM:
   • Create new project
   • Write program step-by-step
   • Use Reference for syntax help
   • Run frequently to test

5. JOIN THE COMMUNITY:
   • Check GitHub for issues/discussions
   • Share your programs
   • Suggest improvements

================================================================================
  UNINSTALLATION
================================================================================

If you want to remove TeachScript:

  $ pip uninstall hb-lcs
  
Or if installed from source:
  
  $ pip uninstall -e .

The source files remain unchanged.

================================================================================
  SUPPORT & HELP
================================================================================

In IDE:
  • TeachScript → Interactive Tutorial
  • TeachScript → Language Reference
  • Help menu in menu bar

Online:
  • docs/teachscript/ directory
  • GitHub repository
  • README.md file

Command Line:
  $ python -m src.hb_lcs.teachscript_runtime --help

================================================================================
  QUICK START SUMMARY
================================================================================

1. Install:     pip install -e .
2. Launch:      python -m src.hb_lcs.launch_ide_teachscript
3. Create:      File → New → TeachScript Project
4. Code:        Write TeachScript in editor
5. Run:         Ctrl+Shift+T
6. Learn:       TeachScript → Interactive Tutorial
7. Explore:     Try all the templates and examples

Welcome to TeachScript! Happy coding! 🎉

================================================================================
"""

if __name__ == "__main__":
    print(SETUP_GUIDE)
    
    # Also save to file
    with open("TEACHSCRIPT_SETUP_GUIDE.txt", "w") as f:
        f.write(SETUP_GUIDE)
    print("\nGuide also saved to: TEACHSCRIPT_SETUP_GUIDE.txt")
