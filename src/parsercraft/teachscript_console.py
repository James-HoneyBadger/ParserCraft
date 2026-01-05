#!/usr/bin/env python3
"""
TeachScript Interactive Console Executor

A console-based REPL (Read-Eval-Print Loop) for TeachScript that allows
interactive program development and testing within the IDE.
"""

import tkinter as tk
from tkinter import scrolledtext, ttk
from typing import List, Optional

from . import teachscript_runtime
from .teachscript_runtime import TeachScriptError, get_runtime


class TeachScriptConsole(ttk.Frame):
    """Interactive TeachScript console with REPL functionality."""

    def __init__(self, parent, **kwargs):
        """Initialize the TeachScript console."""
        super().__init__(parent, **kwargs)

        self.runtime = get_runtime()
        self.history: List[str] = []
        self.history_index = -1
        self.current_input = ""

        # Create UI
        self._create_ui()

    def _create_ui(self):
        """Create the console UI."""
        # Top frame with buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(
            button_frame, text="Clear Console", command=self._clear_console
        ).pack(side="left", padx=2)

        ttk.Button(
            button_frame, text="Reset Environment", command=self._reset_environment
        ).pack(side="left", padx=2)

        ttk.Button(button_frame, text="Show Globals", command=self._show_globals).pack(
            side="left", padx=2
        )

        # Console output area
        self.output = scrolledtext.ScrolledText(
            self,
            height=20,
            font=("Courier", 10),
            wrap="word",
            bg="#1e1e1e",
            fg="#d4d4d4",
        )
        self.output.pack(fill="both", expand=True, padx=5, pady=5)

        # Configure tags
        self.output.tag_config(
            "prompt", foreground="#569cd6", font=("Courier", 10, "bold")
        )
        self.output.tag_config("output", foreground="#ce9178")
        self.output.tag_config(
            "error", foreground="#f48771", font=("Courier", 10, "bold")
        )
        self.output.tag_config("success", foreground="#6a9955")

        # Input area
        input_frame = ttk.Frame(self)
        input_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(input_frame, text=">>> ", font=("Courier", 10)).pack(side="left")

        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(
            input_frame, textvariable=self.input_var, font=("Courier", 10)
        )
        self.input_entry.pack(side="left", fill="x", expand=True)
        self.input_entry.bind("<Return>", self._on_input)
        self.input_entry.bind("<Up>", self._show_previous_history)
        self.input_entry.bind("<Down>", self._show_next_history)

        # Welcome message
        self.output.insert(tk.END, "TeachScript Interactive Console\n", "prompt")
        self.output.insert(
            tk.END, "Type TeachScript code and press Enter to execute.\n", "success"
        )
        self.output.insert(tk.END, "Type 'help' for commands.\n\n", "success")
        self.output.config(state="disabled")

        # Focus input
        self.input_entry.focus()

    def _on_input(self, _event: Optional[tk.Event] = None) -> str:
        """Process input when Enter is pressed."""
        code = self.input_var.get()
        self.input_var.set("")

        if not code.strip():
            return "break"

        # Add to history
        self.history.append(code)
        self.history_index = -1

        # Handle built-in commands
        if code.lower() == "help":
            self._show_help()
            return "break"
        elif code.lower() == "clear":
            self._clear_console()
            return "break"
        elif code.lower() == "reset":
            self._reset_environment()
            return "break"
        elif code.lower() == "globals":
            self._show_globals()
            return "break"
        elif code.lower() == "exit" or code.lower() == "quit":
            # In a real implementation, this would close the console
            pass

        # Execute code
        self._execute(code)

        return "break"

    def _execute(self, code: str):
        """Execute TeachScript code."""
        self.output.config(state="normal")
        self.output.insert(tk.END, f">>> {code}\n", "prompt")
        self.output.config(state="disabled")

        try:
            # Try to execute as single statement first
            output, error = self.runtime.run(code)

            if error:
                self.output.config(state="normal")
                self.output.insert(tk.END, f"Error: {error}\n", "error")
                self.output.config(state="disabled")
            elif output:
                self.output.config(state="normal")
                self.output.insert(tk.END, output, "output")
                self.output.config(state="disabled")
            else:
                # No output
                self.output.config(state="normal")
                self.output.insert(tk.END, "ok\n", "success")
                self.output.config(state="disabled")

        except TeachScriptError as e:
            self.output.config(state="normal")
            self.output.insert(tk.END, f"TeachScript Error: {str(e)}\n", "error")
            self.output.config(state="disabled")

        self.output.config(state="normal")
        self.output.see(tk.END)
        self.output.config(state="disabled")

    def _show_previous_history(self, _event: Optional[tk.Event] = None) -> str:
        """Show previous command from history."""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.input_var.set(self.history[-(self.history_index + 1)])
        return "break"

    def _show_next_history(self, _event: Optional[tk.Event] = None) -> str:
        """Show next command from history."""
        if self.history_index > 0:
            self.history_index -= 1
            self.input_var.set(self.history[-(self.history_index + 1)])
        elif self.history_index == 0:
            self.history_index = -1
            self.input_var.set("")
        return "break"

    def _clear_console(self):
        """Clear the console output."""
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.config(state="disabled")

    def _reset_environment(self):
        """Reset the runtime environment."""
        teachscript_runtime.reset_runtime()
        self.runtime = get_runtime()

        self.output.config(state="normal")
        self.output.insert(tk.END, "Environment reset.\n", "success")
        self.output.config(state="disabled")

    def _show_globals(self):
        """Show global variables in the environment."""
        self.output.config(state="normal")
        self.output.insert(tk.END, "\n--- Global Variables ---\n", "prompt")

        if self.runtime.environment.namespace:
            for name, value in sorted(self.runtime.environment.namespace.items()):
                if not name.startswith("__"):
                    self.output.insert(
                        tk.END, f"  {name}: {type(value).__name__}\n", "output"
                    )
        else:
            self.output.insert(tk.END, "  (none)\n", "output")

        self.output.config(state="disabled")
        self.output.see(tk.END)

    def _show_help(self):
        """Show help message."""
        self.output.config(state="normal")
        self.output.insert(tk.END, "\n--- TeachScript Console Help ---\n", "prompt")
        self.output.insert(
            tk.END,
            """
Commands:
  help      - Show this help message
  clear     - Clear console output
  reset     - Reset the environment
  globals   - Show global variables
  exit      - Exit the console

TeachScript Features:
  - Use 'when' instead of 'if'
  - Use 'say()' instead of 'print()'
  - Use 'ask()' to get user input
  - Use 'teach' to define functions
  - Use 'repeat_for' and 'repeat_while' for loops

Examples:
  say("Hello, World!")
  remember name = ask("Your name: ")
  remember numbers = [1, 2, 3, 4, 5]
""",
            "output",
        )
        self.output.config(state="disabled")
        self.output.see(tk.END)

    def execute_teachscript_code(self, code: str) -> tuple[str, str]:
        """Execute code from external source (like the editor)."""
        return self.runtime.run(code)
