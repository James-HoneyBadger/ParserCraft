#!/usr/bin/env python3
"""
Enhanced IDE Launcher with TeachScript Integration

Launches the CodeCraft IDE with full TeachScript support integrated.
"""

import sys
import tkinter as tk
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from ide import (  # noqa: E402 pylint: disable=wrong-import-position
    AdvancedIDE,
)
from ide_teachscript_integration import (  # noqa: E402 pylint: disable=wrong-import-position
    TeachScriptIDEIntegration,
)
from teachscript_highlighting import (  # noqa: E402 pylint: disable=wrong-import-position
    TeachScriptCodeCompletion,
    TeachScriptHighlighter,
)


def launch_ide_with_teachscript():
    """Launch the IDE with TeachScript integration."""
    root = tk.Tk()

    # Create the main IDE
    ide = AdvancedIDE(root)

    # Add TeachScript integration
    teachscript_integration = TeachScriptIDEIntegration(ide)

    # Add TeachScript menus
    teachscript_integration.add_teachscript_menus(root.nametowidget(root.cget("menu")))

    # Add keyboard shortcuts
    teachscript_integration.add_teachscript_keyboard_shortcuts(root)

    # Add syntax highlighting if editor is available
    if ide.editor:
        _ = TeachScriptHighlighter(ide.editor)

        # Add code completion
        _ = TeachScriptCodeCompletion(ide.editor)

    # Customize title
    root.title("CodeCraft IDE with TeachScript - v3.0")

    # Start the IDE
    root.mainloop()


if __name__ == "__main__":
    launch_ide_with_teachscript()
