#!/usr/bin/env python3
"""
CodeEx - CodeCraft Execution Environment

A specialized IDE for developing and running applications created with CodeCraft.
Provides professional development environment for CodeCraft-based languages.

Features:
- Multi-interpreter support (load any CodeCraft language)
- Project management (organize code files and resources)
- Professional editor with syntax highlighting
- Real-time code execution
- Integrated console output
- Debugging capabilities
- Project templates
- Version control integration
"""

import sys
import tkinter as tk
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Local imports must come after sys.path modification
from codex.codex_gui import \
    CodeExIDE  # noqa: E402 pylint: disable=wrong-import-position


def main():
    """Launch CodeEx IDE."""
    root = tk.Tk()
    root.title("CodeEx - CodeCraft Execution Environment")
    root.geometry("1600x900")

    CodeExIDE(root)

    root.mainloop()


if __name__ == "__main__":
    main()
