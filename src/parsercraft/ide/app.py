"""
ParserCraft IDE — Main Application

Combines editor, project management, and runtime execution 
into a cohesive Tkinter GUI application.

Launch: python -m parsercraft.ide.app
"""

from __future__ import annotations

import io
import sys
import traceback
import tkinter as tk
from contextlib import redirect_stdout, redirect_stderr
from tkinter import ttk, filedialog, messagebox
from typing import Any, Optional

from parsercraft.ide.editor import CodeEditor
from parsercraft.ide.project import Project, ProjectManager
from parsercraft.parser.grammar import GrammarParser, PEGInterpreter, grammar_from_config
from parsercraft.codegen.python_transpiler import PythonTranspiler, TranspileOptions


class ParserCraftIDE(tk.Tk):
    """Main ParserCraft IDE application."""

    def __init__(self):
        super().__init__()
        self.title("ParserCraft IDE — Language Construction Studio")
        self.geometry("1200x800")
        self.configure(bg="#1e1e1e")

        self.project: Optional[Project] = None
        self.project_manager = ProjectManager()
        self._grammar = None
        self._interpreter = None

        self._build_menu()
        self._build_toolbar()
        self._build_main_area()
        self._build_status_bar()

        # Start with welcome message
        self._console_print("ParserCraft IDE v4.0.0\n")
        self._console_print("Create or open a language project to begin.\n")
        self._console_print("Use File > New Project or File > Open Config.\n")

    # -------------------------------------------------------------------
    # UI Construction
    # -------------------------------------------------------------------

    def _build_menu(self) -> None:
        menubar = tk.Menu(self, bg="#2b2b2b", fg="#d4d4d4")

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Project...", command=self._new_project, accelerator="Ctrl+N")
        file_menu.add_command(label="Open Config...", command=self._open_config, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self._save, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self._save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Run menu
        run_menu = tk.Menu(menubar, tearoff=0)
        run_menu.add_command(label="Parse", command=self._run_parse, accelerator="F5")
        run_menu.add_command(label="Transpile to Python", command=self._run_transpile, accelerator="F6")
        run_menu.add_command(label="Execute", command=self._run_execute, accelerator="F7")
        run_menu.add_separator()
        run_menu.add_command(label="Show AST", command=self._show_ast)
        run_menu.add_command(label="Generate C", command=self._gen_c)
        run_menu.add_command(label="Generate LLVM IR", command=self._gen_llvm)
        menubar.add_cascade(label="Run", menu=run_menu)

        # Grammar menu
        grammar_menu = tk.Menu(menubar, tearoff=0)
        grammar_menu.add_command(label="Validate Grammar", command=self._validate_grammar)
        grammar_menu.add_command(label="Reload Grammar", command=self._reload_grammar)
        menubar.add_cascade(label="Grammar", menu=grammar_menu)

        self.config(menu=menubar)

        # Keyboard shortcuts
        self.bind("<Control-n>", lambda e: self._new_project())
        self.bind("<Control-o>", lambda e: self._open_config())
        self.bind("<Control-s>", lambda e: self._save())
        self.bind("<F5>", lambda e: self._run_parse())
        self.bind("<F6>", lambda e: self._run_transpile())
        self.bind("<F7>", lambda e: self._run_execute())

    def _build_toolbar(self) -> None:
        toolbar = tk.Frame(self, bg="#333333", height=32)
        toolbar.pack(fill="x")

        btn_style = {"bg": "#3c3c3c", "fg": "#d4d4d4", "relief": "flat",
                      "padx": 8, "pady": 2, "cursor": "hand2"}

        tk.Button(toolbar, text="▶ Parse", command=self._run_parse, **btn_style).pack(side="left", padx=2, pady=2)
        tk.Button(toolbar, text="⟳ Transpile", command=self._run_transpile, **btn_style).pack(side="left", padx=2, pady=2)
        tk.Button(toolbar, text="⚡ Execute", command=self._run_execute, **btn_style).pack(side="left", padx=2, pady=2)

        tk.Label(toolbar, text="  |  ", bg="#333333", fg="#555555").pack(side="left")

        tk.Button(toolbar, text="AST", command=self._show_ast, **btn_style).pack(side="left", padx=2, pady=2)
        tk.Button(toolbar, text="C", command=self._gen_c, **btn_style).pack(side="left", padx=2, pady=2)
        tk.Button(toolbar, text="LLVM", command=self._gen_llvm, **btn_style).pack(side="left", padx=2, pady=2)

    def _build_main_area(self) -> None:
        # Paned window for resizable panels
        paned = tk.PanedWindow(self, orient="horizontal", bg="#1e1e1e",
                                sashwidth=4, sashrelief="flat")
        paned.pack(fill="both", expand=True)

        # Left: Grammar editor
        left_frame = tk.Frame(paned, bg="#1e1e1e")
        tk.Label(left_frame, text="Grammar (PEG)", bg="#2b2b2b", fg="#d4d4d4",
                 anchor="w", padx=8, pady=4).pack(fill="x")
        self.grammar_editor = CodeEditor(left_frame, keywords=[
            "IDENT", "NUMBER", "STRING", "NEWLINE", "EOF",
        ])
        self.grammar_editor.pack(fill="both", expand=True)
        paned.add(left_frame, width=350)

        # Center: Source code editor
        center_frame = tk.Frame(paned, bg="#1e1e1e")
        tk.Label(center_frame, text="Source Code", bg="#2b2b2b", fg="#d4d4d4",
                 anchor="w", padx=8, pady=4).pack(fill="x")
        self.source_editor = CodeEditor(center_frame)
        self.source_editor.pack(fill="both", expand=True)
        paned.add(center_frame, width=450)

        # Right: Output / Console
        right_frame = tk.Frame(paned, bg="#1e1e1e")

        # Output notebook (tabs for different outputs)
        self._output_notebook = ttk.Notebook(right_frame)
        self._output_notebook.pack(fill="both", expand=True)

        # Console tab
        console_frame = tk.Frame(self._output_notebook, bg="#1e1e1e")
        self.console = tk.Text(
            console_frame, wrap="word",
            bg="#1e1e1e", fg="#d4d4d4",
            insertbackground="#ffffff",
            font=("Courier New", 10),
            state="disabled",
        )
        self.console.pack(fill="both", expand=True)
        self._output_notebook.add(console_frame, text="Console")

        # Output tab (transpiled code, AST, etc.)
        output_frame = tk.Frame(self._output_notebook, bg="#1e1e1e")
        self.output_text = tk.Text(
            output_frame, wrap="word",
            bg="#1e1e1e", fg="#d4d4d4",
            font=("Courier New", 10),
            state="disabled",
        )
        self.output_text.pack(fill="both", expand=True)
        self._output_notebook.add(output_frame, text="Output")

        paned.add(right_frame, width=400)

    def _build_status_bar(self) -> None:
        self.status_bar = tk.Label(
            self, text="Ready", bg="#007acc", fg="white",
            anchor="w", padx=8, pady=2,
        )
        self.status_bar.pack(fill="x", side="bottom")

    # -------------------------------------------------------------------
    # File operations
    # -------------------------------------------------------------------

    def _new_project(self) -> None:
        """Create a new language project."""
        directory = filedialog.askdirectory(title="Select Project Directory")
        if not directory:
            return

        name = tk.simpledialog.askstring("Project Name", "Language name:") if hasattr(tk, 'simpledialog') else "MyLanguage"
        if not name:
            name = "MyLanguage"

        self.project = self.project_manager.create_project(name, directory)
        self._load_project_into_ui()
        self._status(f"Created project: {name}")

    def _open_config(self) -> None:
        """Open an existing language configuration."""
        path = filedialog.askopenfilename(
            title="Open Language Configuration",
            filetypes=[
                ("YAML files", "*.yaml *.yml"),
                ("JSON files", "*.json"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return

        try:
            self.project = self.project_manager.open_project(path)
            self._load_project_into_ui()
            self._status(f"Opened: {path}")
        except Exception as e:
            self._console_print(f"Error loading config: {e}\n", error=True)

    def _save(self) -> None:
        if self.project and self.project.config_path:
            self._save_grammar_to_config()
            self.project.save()
            self._status(f"Saved: {self.project.config_path}")
        else:
            self._save_as()

    def _save_as(self) -> None:
        path = filedialog.asksaveasfilename(
            title="Save Configuration As",
            defaultextension=".yaml",
            filetypes=[("YAML files", "*.yaml"), ("JSON files", "*.json")],
        )
        if path:
            if not self.project:
                self.project = Project(name="Untitled")
            self._save_grammar_to_config()
            self.project.save(path)
            self._status(f"Saved: {path}")

    def _load_project_into_ui(self) -> None:
        """Load project data into the editor panels."""
        if not self.project:
            return

        # Load grammar
        if self.project.grammar_text:
            self.grammar_editor.set_text(self.project.grammar_text)
        elif self.project.config.get("grammar", {}).get("rules"):
            lines = []
            for name, pattern in self.project.config["grammar"]["rules"].items():
                lines.append(f"{name} <- {pattern}")
            self.grammar_editor.set_text("\n".join(lines))

        # Update source editor keywords
        keywords = self.project.get_keywords()
        self.source_editor.set_keywords(keywords)

        # Set example source if present
        example = self.project.config.get("example", "")
        if example:
            self.source_editor.set_text(example)

        # Reload grammar
        self._reload_grammar()

    def _save_grammar_to_config(self) -> None:
        """Save the grammar editor content back to the project config."""
        if not self.project:
            return

        grammar_text = self.grammar_editor.get_text().strip()
        if grammar_text:
            rules = {}
            for line in grammar_text.split("\n"):
                line = line.strip()
                if "<-" in line:
                    parts = line.split("<-", 1)
                    rules[parts[0].strip()] = parts[1].strip()

            if "grammar" not in self.project.config:
                self.project.config["grammar"] = {}
            self.project.config["grammar"]["rules"] = rules

    # -------------------------------------------------------------------
    # Grammar / Parse / Execute
    # -------------------------------------------------------------------

    def _reload_grammar(self) -> None:
        """Parse the grammar editor content into a Grammar object."""
        grammar_text = self.grammar_editor.get_text().strip()
        if not grammar_text:
            self._console_print("No grammar defined.\n")
            return

        try:
            parser = GrammarParser()
            self._grammar = parser.parse(grammar_text)

            # Apply grammar settings from config (comments, whitespace, start rule)
            if self.project and self.project.config:
                grammar_cfg = self.project.config.get("grammar", {})
                if grammar_cfg.get("comments"):
                    self._grammar.comment_patterns = grammar_cfg["comments"]
                if grammar_cfg.get("start"):
                    self._grammar.start_rule = grammar_cfg["start"]
                if "skip_whitespace" in grammar_cfg:
                    self._grammar.skip_whitespace = grammar_cfg["skip_whitespace"]

            errors = self._grammar.validate()
            if errors:
                self._console_print(f"Grammar warnings:\n", error=True)
                for err in errors:
                    self._console_print(f"  - {err}\n", error=True)
            else:
                self._interpreter = PEGInterpreter(self._grammar)
                self._console_print(f"Grammar loaded: {len(self._grammar.rules)} rules\n")
                self._status("Grammar OK")
        except Exception as e:
            self._console_print(f"Grammar error: {e}\n", error=True)
            self._status("Grammar error")

    def _run_parse(self) -> None:
        """Parse the source code using the current grammar."""
        if not self._interpreter:
            self._reload_grammar()
        if not self._interpreter:
            return

        source = self.source_editor.get_text().strip()
        if not source:
            self._console_print("No source code to parse.\n")
            return

        try:
            ast = self._interpreter.parse(source)
            self._output_set(ast.pretty())
            self._console_print(f"Parse OK — {len(ast.children)} top-level nodes\n")
            self._output_notebook.select(1)  # Show output tab
            self._status("Parse OK")
        except SyntaxError as e:
            self._console_print(f"Parse error: {e}\n", error=True)
            self._status("Parse error")

    def _run_transpile(self) -> None:
        """Transpile source code to Python via the grammar engine."""
        if not self._interpreter:
            self._reload_grammar()
        if not self._interpreter:
            return

        source = self.source_editor.get_text().strip()
        if not source:
            return

        try:
            ast = self._interpreter.parse(source)
            transpiler = PythonTranspiler()
            python_code = transpiler.transpile(ast)
            self._output_set(python_code)
            self._console_print(f"Transpiled to Python ({len(python_code)} chars)\n")
            self._output_notebook.select(1)
            self._status("Transpile OK")
        except Exception as e:
            self._console_print(f"Transpile error: {e}\n", error=True)

    def _run_execute(self) -> None:
        """Parse, transpile, and execute the source code."""
        if not self._interpreter:
            self._reload_grammar()
        if not self._interpreter:
            return

        source = self.source_editor.get_text().strip()
        if not source:
            return

        try:
            ast = self._interpreter.parse(source)
            transpiler = PythonTranspiler()
            python_code = transpiler.transpile(ast)

            # Capture output
            stdout = io.StringIO()
            stderr = io.StringIO()
            ns: dict = {}

            with redirect_stdout(stdout), redirect_stderr(stderr):
                exec(python_code, ns)  # noqa: S102

            output = stdout.getvalue()
            errors = stderr.getvalue()

            if output:
                self._console_print(output)
            if errors:
                self._console_print(errors, error=True)

            if not output and not errors:
                # Show variables
                user_vars = {k: v for k, v in ns.items()
                             if not k.startswith("_") and k != "__builtins__"}
                if user_vars:
                    self._console_print("Variables:\n")
                    for k, v in user_vars.items():
                        self._console_print(f"  {k} = {v!r}\n")

            self._status("Execute OK")
        except SyntaxError as e:
            self._console_print(f"Parse error: {e}\n", error=True)
        except Exception as e:
            self._console_print(f"Runtime error: {e}\n", error=True)
            self._console_print(traceback.format_exc() + "\n", error=True)

    def _show_ast(self) -> None:
        """Show the AST tree for the current source."""
        self._run_parse()

    def _gen_c(self) -> None:
        """Generate C code from the source."""
        if not self._interpreter:
            self._reload_grammar()
        if not self._interpreter:
            return

        source = self.source_editor.get_text().strip()
        if not source:
            return

        try:
            from parsercraft.codegen.codegen_c import CCodeGenerator
            ast = self._interpreter.parse(source)
            gen = CCodeGenerator()
            c_code = gen.translate_source_ast(ast)
            self._output_set(c_code)
            self._console_print(f"Generated C code ({len(c_code)} chars)\n")
            self._output_notebook.select(1)
        except Exception as e:
            self._console_print(f"C codegen error: {e}\n", error=True)

    def _gen_llvm(self) -> None:
        """Generate LLVM IR from the source."""
        if not self._interpreter:
            self._reload_grammar()
        if not self._interpreter:
            return

        source = self.source_editor.get_text().strip()
        if not source:
            return

        try:
            from parsercraft.codegen.llvm_ir import LLVMIRGenerator
            ast = self._interpreter.parse(source)
            gen = LLVMIRGenerator()
            ir = gen.translate_source_ast(ast)
            self._output_set(ir)
            self._console_print(f"Generated LLVM IR ({len(ir)} chars)\n")
            self._output_notebook.select(1)
        except Exception as e:
            self._console_print(f"LLVM IR error: {e}\n", error=True)

    def _validate_grammar(self) -> None:
        """Validate the current grammar."""
        grammar_text = self.grammar_editor.get_text().strip()
        if not grammar_text:
            self._console_print("No grammar to validate.\n")
            return

        try:
            parser = GrammarParser()
            grammar = parser.parse(grammar_text)
            errors = grammar.validate()
            if errors:
                self._console_print("Grammar validation errors:\n", error=True)
                for err in errors:
                    self._console_print(f"  - {err}\n", error=True)
            else:
                self._console_print(f"Grammar OK: {len(grammar.rules)} rules defined\n")
        except Exception as e:
            self._console_print(f"Grammar parse error: {e}\n", error=True)

    # -------------------------------------------------------------------
    # UI Helpers
    # -------------------------------------------------------------------

    def _console_print(self, text: str, error: bool = False) -> None:
        """Print to the console panel."""
        self.console.config(state="normal")
        if error:
            self.console.tag_configure("error", foreground="#f44747")
            self.console.insert("end", text, "error")
        else:
            self.console.insert("end", text)
        self.console.see("end")
        self.console.config(state="disabled")

    def _output_set(self, text: str) -> None:
        """Set the output panel content."""
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", text)
        self.output_text.config(state="disabled")

    def _status(self, text: str) -> None:
        """Update status bar."""
        self.status_bar.config(text=text)


def main():
    """Launch the ParserCraft IDE.

    Usage:
        parsercraft-ide [config.yaml] [source_file]
    """
    import argparse
    parser = argparse.ArgumentParser(description="ParserCraft IDE")
    parser.add_argument("config", nargs="?", default=None, help="Language config file (.yaml/.json)")
    parser.add_argument("source", nargs="?", default=None, help="Source file to open")
    args = parser.parse_args()

    app = ParserCraftIDE()

    if args.config:
        try:
            app.project = app.project_manager.open_project(args.config)
            app._load_project_into_ui()
            app._status(f"Opened: {args.config}")
        except Exception as e:
            app._console_print(f"Error loading config: {e}\n", error=True)

    if args.source:
        try:
            with open(args.source) as f:
                app.source_editor.set_text(f.read())
            app._status(f"Source: {args.source}")
        except Exception as e:
            app._console_print(f"Error loading source: {e}\n", error=True)

    app.mainloop()


if __name__ == "__main__":
    main()
