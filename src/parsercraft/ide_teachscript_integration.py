#!/usr/bin/env python3
"""
IDE TeachScript Integration

Integrates TeachScript support directly into the ParserCraft IDE, providing:
- TeachScript file detection and handling
- Integrated transpiler preview
- Educational project templates
- TeachScript-specific menus and workflows
- Interactive tutorials and learning paths
"""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Optional

from .teachscript_runtime import get_runtime


class TeachScriptIDEIntegration:
    """Integrates TeachScript into the ParserCraft IDE."""

    # TeachScript file extension
    EXTENSION = ".teach"

    # Project templates
    TEMPLATES = {
        "hello_world": {
            "name": "Hello World",
            "description": "Simple output program",
            "code": """# TeachScript: Hello World
say("Hello, World!")
say("Welcome to TeachScript!")
""",
        },
        "variables": {
            "name": "Variables",
            "description": "Working with variables",
            "code": """# TeachScript: Variables
remember name = ask("What is your name? ")
remember age = make_number(ask("How old are you? "))

say("Hello, " + name)
say("You are " + make_text(age) + " years old")
""",
        },
        "conditionals": {
            "name": "Conditionals",
            "description": "If/else statements",
            "code": """# TeachScript: Conditionals
remember score = make_number(ask("Enter your score: "))

when score >= 90:
    say("Excellent!")
or_when score >= 80:
    say("Good job!")
or_when score >= 70:
    say("Passing")
otherwise:
    say("Try again next time")
""",
        },
        "loops": {
            "name": "Loops",
            "description": "For and while loops",
            "code": """# TeachScript: Loops
# For loop
say("Counting from 1 to 10:")
repeat_for i inside numbers_from(1, 11):
    say(i)

# While loop
remember count = 0
say("While loop:")
repeat_while count < 5:
    say("Count:", count)
    count = count + 1
""",
        },
        "functions": {
            "name": "Functions",
            "description": "Defining and calling functions",
            "code": """# TeachScript: Functions
teach greet(name):
    say("Hello, " + name + "!")

teach add(a, b):
    give_back a + b

greet("World")
remember result = add(5, 3)
say("5 + 3 =", result)
""",
        },
        "lists": {
            "name": "Lists",
            "description": "Working with lists",
            "code": """# TeachScript: Lists
remember fruits = ["apple", "banana", "orange"]

say("Fruits:")
repeat_for fruit inside fruits:
    say(fruit)

say("Number of fruits:", length_of(fruits))

# Add a fruit
fruits.add_to("grape")
say("Added grape:", fruits)
""",
        },
        "interactive_game": {
            "name": "Number Guessing Game",
            "description": "Interactive guessing game",
            "code": """# TeachScript: Number Guessing Game
remember secret = TSRandom.randint(1, 100)
remember guess = nothing
remember tries = 0

say("Guess the number between 1 and 100!")

repeat_while guess opposite equals secret:
    remember guess = make_number(ask("Your guess: "))
    remember tries = tries + 1

    when guess < secret:
        say("Too low!")
    or_when guess > secret:
        say("Too high!")
    otherwise:
        say("Correct! You won in", tries, "tries!")
""",
        },
    }

    def __init__(self, ide_instance):
        """
        Initialize TeachScript IDE integration.

        Args:
            ide_instance: Reference to the main IDE instance
        """
        self.ide = ide_instance
        self.runtime = get_runtime()
        self.current_teachscript_file: Optional[str] = None
        self.transpiler_preview_var: Optional[tk.StringVar] = None

    def is_teachscript_file(self, filepath: str) -> bool:
        """Check if a file is a TeachScript file."""
        return filepath.endswith(self.EXTENSION)

    def add_teachscript_menus(self, menubar: tk.Menu):
        """Add TeachScript-specific menus to the IDE."""
        teachscript_menu = tk.Menu(menubar, name="teachscript")
        menubar.add_cascade(label="TeachScript", menu=teachscript_menu)

        # New TeachScript Project
        teachscript_menu.add_command(
            label="New TeachScript Project", command=self._show_project_templates
        )

        teachscript_menu.add_separator()

        # Run TeachScript
        teachscript_menu.add_command(
            label="Run TeachScript (Ctrl+Shift+T)", command=self._run_teachscript
        )

        # Preview Transpiled Code
        teachscript_menu.add_command(
            label="Preview Python Code", command=self._show_transpiled_code
        )

        # Check Syntax
        teachscript_menu.add_command(label="Check Syntax", command=self._check_syntax)

        teachscript_menu.add_separator()

        # TeachScript Tutorial
        teachscript_menu.add_command(
            label="Interactive Tutorial", command=self._show_tutorial
        )

        # TeachScript Reference
        teachscript_menu.add_command(
            label="Language Reference", command=self._show_reference
        )

    def add_teachscript_keyboard_shortcuts(self, root: tk.Tk):
        """Add keyboard shortcuts for TeachScript commands."""
        root.bind("<Control-Shift-T>", lambda e: self._run_teachscript())

    def _show_project_templates(self):
        """Show dialog to create a new TeachScript project."""
        dialog = tk.Toplevel(self.ide.root)
        dialog.title("New TeachScript Project")
        dialog.geometry("500x400")

        # Instructions
        ttk.Label(
            dialog,
            text="Select a template to start a new TeachScript project:",
            wraplength=480,
        ).pack(pady=10, padx=10)

        # Template list
        frame = ttk.Frame(dialog)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(
            frame, yscrollcommand=scrollbar.set, height=12, font=("Courier", 10)
        )
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        # Add templates to listbox
        template_names = list(self.TEMPLATES.keys())
        for i, name in enumerate(template_names):
            template = self.TEMPLATES[name]
            listbox.insert(i, f"📚 {template['name']}: {template['description']}")

        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        def create_project():
            selection = listbox.curselection()
            if selection:
                template_key = template_names[selection[0]]
                self._create_project_from_template(template_key, dialog)

        ttk.Button(button_frame, text="Create", command=create_project).pack(
            side="left", padx=5
        )
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(
            side="left", padx=5
        )

    def _create_project_from_template(self, template_key: str, dialog: tk.Toplevel):
        """Create a new project from a template."""
        template = self.TEMPLATES[template_key]

        # Ask for file location
        filepath = filedialog.asksaveasfilename(
            defaultextension=self.EXTENSION,
            filetypes=[("TeachScript files", "*.teach"), ("All files", "*.*")],
            initialfile=f"{template_key}{self.EXTENSION}",
        )

        if filepath:
            # Write template code to file
            Path(filepath).write_text(template["code"], encoding="utf-8")
            self.current_teachscript_file = filepath

            # Load in IDE
            if self.ide.editor:
                self.ide.editor.delete("1.0", tk.END)
                self.ide.editor.insert("1.0", template["code"])
                self.ide.current_file = filepath

            messagebox.showinfo(
                "Success", f"Created {template['name']} project at:\n{filepath}"
            )
            dialog.destroy()

    def _run_teachscript(self):
        """Run the current TeachScript code."""
        if not self.ide.editor:
            messagebox.showerror("Error", "No editor available")
            return

        code = self.ide.editor.get("1.0", tk.END)

        if not code.strip():
            messagebox.showwarning("Warning", "No code to run")
            return

        try:
            output, error = self.runtime.run(code)

            # Display output in console
            if self.ide.console:
                self.ide.console.config(state="normal")
                self.ide.console.insert(tk.END, "=== TeachScript Output ===\n")
                if output:
                    self.ide.console.insert(tk.END, output)
                if error:
                    self.ide.console.insert(
                        tk.END, f"\n=== Errors ===\n{error}", "error"
                    )
                self.ide.console.insert(tk.END, "\n" + "=" * 40 + "\n")
                self.ide.console.config(state="disabled")
                self.ide.console.see(tk.END)

        except (ValueError, SyntaxError, RuntimeError) as e:
            messagebox.showerror("Execution Error", str(e))

    def _show_transpiled_code(self):
        """Show the transpiled Python code."""
        if not self.ide.editor:
            messagebox.showerror("Error", "No editor available")
            return

        code = self.ide.editor.get("1.0", tk.END)

        try:
            python_code = self.runtime.get_transpiled_code(code)

            # Create preview window
            preview = tk.Toplevel(self.ide.root)
            preview.title("Transpiled Python Code")
            preview.geometry("700x500")

            text = tk.Text(preview, font=("Courier", 10), wrap="word")
            text.pack(fill="both", expand=True, padx=10, pady=10)

            text.insert("1.0", python_code)
            text.config(state="disabled")

            ttk.Button(
                preview,
                text="Copy to Clipboard",
                command=lambda: self.ide.root.clipboard_clear()
                or self.ide.root.clipboard_append(python_code)
                or messagebox.showinfo("Copied", "Code copied to clipboard"),
            ).pack(pady=5)

        except (ValueError, SyntaxError, AttributeError) as e:
            messagebox.showerror("Transpilation Error", str(e))

    def _check_syntax(self):
        """Check TeachScript syntax."""
        if not self.ide.editor:
            messagebox.showerror("Error", "No editor available")
            return

        code = self.ide.editor.get("1.0", tk.END)

        try:
            errors = self.runtime.get_syntax_errors(code)

            if errors:
                message = "Found " + str(len(errors)) + " error(s):\n\n"
                for error in errors:
                    message += f"• {error}\n"
                messagebox.showerror("Syntax Errors", message)
            else:
                messagebox.showinfo("Success", "No syntax errors found!")

        except Exception as e:  # pylint: disable=broad-exception-caught
            messagebox.showerror("Error", str(e))

    def _show_tutorial(self):
        """Show interactive TeachScript tutorial."""
        tutorial = tk.Toplevel(self.ide.root)
        tutorial.title("TeachScript Tutorial")
        tutorial.geometry("700x600")

        # Create notebook for lessons
        notebook = ttk.Notebook(tutorial)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        lessons = [
            {
                "title": "Lesson 1: Say Hello",
                "content": """Welcome to TeachScript!

TeachScript is a beginner-friendly programming language.
Instead of 'print()', you use 'say()':

say("Hello, World!")

Try it: Click the button below to create a new Hello World project!
""",
            },
            {
                "title": "Lesson 2: Variables",
                "content": """Variables store information.

In TeachScript, you declare variables with 'remember':

remember name = "Alice"
remember age = 10

You can change them:
name = "Bob"
age = age + 1

Display them:
say("Name:", name)
say("Age:", age)
""",
            },
            {
                "title": "Lesson 3: Input",
                "content": """Get input from the user with 'ask':

remember name = ask("What is your name? ")

You might need to convert the input:

remember age = make_number(ask("How old are you? "))

say("You are", age, "years old")
""",
            },
            {
                "title": "Lesson 4: Conditionals",
                "content": """Make decisions with 'when' and 'otherwise':

remember score = 85

when score >= 90:
    say("Excellent!")
or_when score >= 80:
    say("Good job!")
otherwise:
    say("Try again")

Note:
- 'and_also' instead of 'and'
- 'or_else' instead of 'or'
- 'opposite' instead of 'not'
""",
            },
            {
                "title": "Lesson 5: Loops",
                "content": """Repeat code with loops.

For loop (repeat a specific number of times):
repeat_for i inside numbers_from(5):
    say(i)

While loop (repeat while condition is true):
remember count = 0
repeat_while count < 10:
    say(count)
    count = count + 1
""",
            },
        ]

        for lesson in lessons:
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=lesson["title"])

            text = tk.Text(frame, wrap="word", font=("Courier", 11), height=20)
            text.pack(fill="both", expand=True, padx=10, pady=10)
            text.insert("1.0", lesson["content"])
            text.config(state="disabled")

    def _show_reference(self):
        """Show TeachScript language reference."""
        reference = tk.Toplevel(self.ide.root)
        reference.title("TeachScript Language Reference")
        reference.geometry("800x600")

        notebook = ttk.Notebook(reference)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Keywords tab
        keywords_frame = ttk.Frame(notebook)
        notebook.add(keywords_frame, text="Keywords")

        keywords_text = tk.Text(
            keywords_frame, font=("Courier", 10), wrap="word", height=25
        )
        keywords_text.pack(fill="both", expand=True, padx=10, pady=10)

        keywords_content = """TeachScript Keywords and Their Meanings:

Control Flow:
  when → if
  otherwise → else
  or_when → elif
  repeat_while → while
  repeat_for → for
  stop → break
  skip → continue

Functions:
  teach → def
  give_back → return

Values:
  yes → True
  no → False
  nothing → None

Operators:
  and_also → and
  or_else → or
  opposite → not
  inside → in
  equals → is

Variables:
  remember → declare variable (optional)
  forever → constant (optional)
"""
        keywords_text.insert("1.0", keywords_content)
        keywords_text.config(state="disabled")

        # Functions tab
        functions_frame = ttk.Frame(notebook)
        notebook.add(functions_frame, text="Built-in Functions")

        functions_text = tk.Text(
            functions_frame, font=("Courier", 10), wrap="word", height=25
        )
        functions_text.pack(fill="both", expand=True, padx=10, pady=10)

        functions_content = """TeachScript Built-in Functions:

I/O:
  say(...) → print output
  ask(prompt) → get user input

Type Conversion:
  make_number(x) → convert to integer
  make_decimal(x) → convert to float
  make_text(x) → convert to string
  make_boolean(x) → convert to boolean

Sequences:
  length_of(seq) → get length
  numbers_from(n) → create range
  count_through(seq) → enumerate items
  arrange(seq) → sort items
  backwards(seq) → reverse items

Math:
  absolute(x) → absolute value
  round_to(x, d) → round to decimals
  biggest(...) → maximum value
  smallest(...) → minimum value
  total(seq) → sum of values

Type:
  type_of(x) → get type of value
"""
        functions_text.insert("1.0", functions_content)
        functions_text.config(state="disabled")
