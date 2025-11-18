#!/usr/bin/env python3
"""
Honey Badger Language Construction Set - IDE Launcher

Simple launcher script for the Honey Badger LCS IDE.
"""

import sys
import os

# Ensure we can import from the current directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from ide import main

    main()
except ImportError as e:
    print(f"Error: Failed to import IDE: {e}")
    print("\nMake sure you're running this from the Honey Badger LCS directory")
    print("and that all required files are present:")
    print("  - ide.py")
    print("  - language_config.py")
    print("  - language_runtime.py")
    sys.exit(1)
except Exception as e:
    print(f"Error starting IDE: {e}")
    sys.exit(1)
