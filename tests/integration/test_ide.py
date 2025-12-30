#!/usr/bin/env python3
"""
Test script for the Advanced IDE
"""

import tkinter as tk
from src.hb_lcs.ide import AdvancedIDE


def main():
    """Launch the Advanced IDE."""
    root = tk.Tk()
    root.title("Honey Badger Language Construction Set - Advanced IDE")
    root.geometry("1200x800")

    # Create the IDE
    ide = AdvancedIDE(root)

    # Start the main event loop
    root.mainloop()


if __name__ == "__main__":
    main()
