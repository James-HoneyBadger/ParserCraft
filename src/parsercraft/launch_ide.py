#!/usr/bin/env python3
"""
ParserCraft - IDE Launcher

Simple launcher script for the Honey Badger LCS IDE.
"""

import sys


def main():
    """Launch the Honey Badger LCS IDE."""
    try:
        # Prefer importing the module and constructing the IDE directly
        import tkinter as tk

        from parsercraft.ide import AdvancedIDE

        root = tk.Tk()
        AdvancedIDE(root)  # noqa: F841
        root.mainloop()
    except ImportError as e:
        print(f"Error: Failed to import IDE: {e}")
        print("\nMake sure hb_lcs is properly installed:")
        print("  pip install -e .")
        sys.exit(1)
    except Exception as e:  # noqa: BLE001  # pylint: disable=broad-except
        print(f"Error starting IDE: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
