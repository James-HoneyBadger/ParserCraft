#!/usr/bin/env python3
"""
CodeEx GUI Components

Reusable UI components for the CodeEx IDE.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from pathlib import Path
from typing import Optional, List


class CodeExEditor(ttk.Frame):
    """Code editor with syntax highlighting."""
    
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        
        # Create frame with line numbers
        editor_frame = ttk.Frame(self)
        editor_frame.pack(fill="both", expand=True)
        
        # Line numbers
        self.line_numbers = tk.Text(
            editor_frame,
            width=4,
            bg="#f0f0f0",
            fg="#666",
            state="disabled",
            font=("Courier", 11)
        )
        self.line_numbers.pack(side="left", fill="y")
        
        # Editor
        self.text = scrolledtext.ScrolledText(
            editor_frame,
            wrap="none",
            font=("Courier", 11),
            undo=True,
            maxundo=-1
        )
        self.text.pack(side="left", fill="both", expand=True)
        
        # Configure tags for syntax highlighting
        self._configure_syntax_tags()
        
        # Bind events
        self.text.bind("<KeyRelease>", self._update_line_numbers)
        self.text.bind("<KeyRelease>", self._update_syntax_highlighting)
    
    def _configure_syntax_tags(self):
        """Configure syntax highlighting tags."""
        # Keywords
        self.text.tag_configure("keyword", foreground="#0066ff", font=("Courier", 11, "bold"))
        
        # Strings
        self.text.tag_configure("string", foreground="#009900")
        
        # Comments
        self.text.tag_configure("comment", foreground="#999999", font=("Courier", 11, "italic"))
        
        # Numbers
        self.text.tag_configure("number", foreground="#ff6600")
        
        # Functions
        self.text.tag_configure("function", foreground="#cc0000")
        
        # Operators
        self.text.tag_configure("operator", foreground="#0066cc")
    
    def _update_line_numbers(self, event=None):
        """Update line number display."""
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", "end")
        
        content = self.text.get("1.0", "end-1c")
        lines = content.split("\n")
        
        for i in range(1, len(lines) + 1):
            self.line_numbers.insert("end", f"{i}\n")
        
        self.line_numbers.config(state="disabled")
    
    def _update_syntax_highlighting(self, event=None):
        """Update syntax highlighting."""
        # Remove all tags
        for tag in self.text.tag_names():
            if tag not in ("sel",):
                self.text.tag_remove(tag, "1.0", "end")
        
        content = self.text.get("1.0", "end-1c")
        
        # Highlight numbers
        self._highlight_pattern(r"\b\d+\b", "number")
        
        # Highlight strings
        self._highlight_pattern(r'"[^"]*"', "string")
        self._highlight_pattern(r"'[^']*'", "string")
        
        # Highlight comments
        self._highlight_pattern(r"#.*$", "comment")
    
    def _highlight_pattern(self, pattern: str, tag: str):
        """Highlight text matching pattern."""
        import re
        content = self.text.get("1.0", "end-1c")
        for match in re.finditer(pattern, content, re.MULTILINE):
            start = self.text.index(f"1.0+{match.start()}c")
            end = self.text.index(f"1.0+{match.end()}c")
            self.text.tag_add(tag, start, end)
    
    def get_content(self) -> str:
        """Get editor content."""
        return self.text.get("1.0", "end-1c")
    
    def set_content(self, content: str):
        """Set editor content."""
        self.text.delete("1.0", "end")
        self.text.insert("1.0", content)
    
    def clear(self):
        """Clear editor."""
        self.text.delete("1.0", "end")


class CodeExConsole(ttk.Frame):
    """Output console."""
    
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        
        # Header
        header = ttk.Frame(self)
        header.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(header, text="Output Console", font=("Arial", 10, "bold")).pack(side="left")
        ttk.Button(header, text="Clear", command=self.clear).pack(side="right", padx=2)
        
        # Console text
        self.text = scrolledtext.ScrolledText(
            self,
            wrap="word",
            font=("Courier", 10),
            bg="#f5f5f5",
            fg="#000000"
        )
        self.text.pack(fill="both", expand=True, padx=5, pady=5)
        self.text.config(state="disabled")
        
        # Configure tags
        self.text.tag_configure("output", foreground="#000000")
        self.text.tag_configure("error", foreground="#ff0000", font=("Courier", 10, "bold"))
        self.text.tag_configure("success", foreground="#009900")
    
    def write(self, text: str, tag: str = "output"):
        """Write text to console."""
        self.text.config(state="normal")
        self.text.insert("end", text + "\n", tag)
        self.text.see("end")
        self.text.config(state="disabled")
    
    def clear(self):
        """Clear console."""
        self.text.config(state="normal")
        self.text.delete("1.0", "end")
        self.text.config(state="disabled")


class CodeExProjectExplorer(ttk.Frame):
    """Project file explorer."""
    
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        
        # Header
        header = ttk.Frame(self)
        header.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(header, text="Project", font=("Arial", 10, "bold")).pack(side="left")
        ttk.Button(header, text="↻", command=self.refresh).pack(side="right", padx=2)
        
        # Tree
        self.tree = ttk.Treeview(self, show="tree headings")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.config(yscrollcommand=scrollbar.set)
        
        self.current_path: Optional[Path] = None
    
    def load_project(self, path: str):
        """Load project directory."""
        self.current_path = Path(path)
        self._load_tree(self.current_path)
    
    def _load_tree(self, path: Path, parent: str = ""):
        """Recursively load directory tree."""
        self.tree.delete(*self.tree.get_children(parent))
        
        try:
            items = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name))
            for item in items:
                if item.name.startswith("."):
                    continue
                
                icon = "📁" if item.is_dir() else "📄"
                node_id = self.tree.insert(
                    parent,
                    "end",
                    text=f"{icon} {item.name}",
                    open=False
                )
                
                if item.is_dir() and item.name not in ("__pycache__", ".git"):
                    self._load_tree(item, node_id)
        except Exception as e:
            print(f"Error loading tree: {e}")
    
    def refresh(self):
        """Refresh tree."""
        if self.current_path:
            self._load_tree(self.current_path)


class CodeExMenu(tk.Menu):
    """Menu bar for CodeEx."""
    
    def __init__(self, parent, ide):
        super().__init__(parent)
        self.ide = ide
        
        # File menu
        file_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Project", command=ide.new_project)
        file_menu.add_command(label="Open Project", command=ide.open_project)
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=ide.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Exit", command=parent.quit)
        
        # Edit menu
        edit_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=ide.undo_action, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=ide.redo_action, accelerator="Ctrl+Shift+Z")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=ide.cut_text, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=ide.copy_text, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=ide.paste_text, accelerator="Ctrl+V")
        
        # Interpreter menu
        interp_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Interpreter", menu=interp_menu)
        interp_menu.add_command(label="Load Interpreter", command=ide.load_interpreter)
        interp_menu.add_command(label="Create Language Configuration", command=ide.create_language_config)
        interp_menu.add_separator()
        interp_menu.add_command(label="Interpreter Settings", command=ide.interpreter_settings)
        
        # Run menu
        run_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Execute Code", command=ide.run_code, accelerator="Ctrl+R")
        run_menu.add_command(label="Stop", command=ide.stop_execution)
        run_menu.add_separator()
        run_menu.add_command(label="Recent Executions", command=ide.recent_executions)
        
        # View menu
        view_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Theme", command=ide.toggle_theme)
        view_menu.add_command(label="Zoom In", command=ide.zoom_in, accelerator="Ctrl++")
        view_menu.add_command(label="Zoom Out", command=ide.zoom_out, accelerator="Ctrl+-")
        view_menu.add_separator()
        view_menu.add_command(label="Show/Hide Console", command=ide.toggle_console)
        view_menu.add_command(label="Show/Hide Project Explorer", command=ide.toggle_explorer)
        
        # Help menu
        help_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Getting Started", command=ide.show_getting_started)
        help_menu.add_command(label="User Guide", command=ide.show_user_guide)
        help_menu.add_command(label="API Reference", command=ide.show_api_reference)
        help_menu.add_separator()
        help_menu.add_command(label="About CodeEx", command=self._show_about)
        help_menu.add_command(label="About CodeCraft", command=ide.show_about_codecraft)
        help_menu.add_command(label="Help Contents", command=ide.show_help, accelerator="F1")
    
    def _show_about(self):
        """Show about dialog."""
        from tkinter import messagebox
        messagebox.showinfo(
            "About CodeEx",
            "CodeEx v1.0\n\n"
            "CodeCraft Execution Environment\n\n"
            "Professional IDE for developing and running\n"
            "applications created with CodeCraft.\n\n"
            "© 2024 CodeCraft Project"
        )
