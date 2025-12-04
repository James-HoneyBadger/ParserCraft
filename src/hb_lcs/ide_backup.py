#!/usr/bin/env python3
"""
Honey Badger Language Construction Set - IDE

A tkinter-based IDE adapted from Time_Warp for editing and testing
custom language configurations.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
import json
from typing import Optional, cast

from hb_lcs.language_config import LanguageConfig
from hb_lcs.language_runtime import LanguageRuntime


class HBLCS_IDE(ttk.Frame):
    """Main IDE window with editor, console, and configuration."""

    def __init__(self, master: Optional[tk.Misc] = None):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.root = cast(tk.Tk, self.winfo_toplevel())
        self.root.title("Honey Badger Language Construction Set - IDE v1.0")
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        # Settings
        self.settings = {
            "theme": "light",
            "editor_font_size": 11,
            "console_font_size": 11,
            "geometry": None,
            "show_line_numbers": True,
            "last_config": None,
        }

        # UI State
        self.wrap_var = tk.BooleanVar(value=False)
        self.show_line_numbers_var = tk.BooleanVar(value=True)
        self.theme_var = tk.StringVar(value="light")

        self._build_ui()

        # Load and apply saved settings
        self._load_settings()
        self._apply_settings()

        self.current_file: Optional[str] = None
        self.current_config: Optional[LanguageConfig] = None

        self._load_default_example()
        self._update_status()
        self._update_title()

        # Keyboard shortcuts
        self.root.bind("<Control-n>", lambda e: self._new_file())
        self.root.bind("<Control-o>", lambda e: self._open_file())
        self.root.bind("<Control-s>", lambda e: self._save_file())
        self.root.bind("<Control-Shift-S>", lambda e: self._save_file_as())
        self.root.bind("<F5>", lambda e: self._load_config())
        self.root.bind("<Control-f>", lambda e: self._find_dialog())
        self.root.bind("<Control-h>", lambda e: self._replace_dialog())
        self.root.bind("<Control-l>", lambda e: self._goto_line())

    def _build_ui(self) -> None:
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)

        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(
            label="New", command=self._new_file, accelerator="Ctrl+N"
        )
        file_menu.add_command(
            label="Open...", command=self._open_file, accelerator="Ctrl+O"
        )
        file_menu.add_command(
            label="Save", command=self._save_file, accelerator="Ctrl+S"
        )
        file_menu.add_command(
            label="Save As...",
            command=self._save_file_as,
            accelerator="Ctrl+Shift+S",
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self._edit_undo)
        edit_menu.add_command(label="Redo", command=self._edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(
            label="Cut", command=lambda: self.editor.event_generate("<<Cut>>")
        )
        edit_menu.add_command(
            label="Copy",
            command=lambda: self.editor.event_generate("<<Copy>>"),
        )
        edit_menu.add_command(
            label="Paste",
            command=lambda: self.editor.event_generate("<<Paste>>"),
        )
        edit_menu.add_command(
            label="Select All",
            command=lambda: self.editor.event_generate("<<SelectAll>>"),
        )
        edit_menu.add_separator()
        edit_menu.add_command(
            label="Find...", command=self._find_dialog, accelerator="Ctrl+F"
        )
        edit_menu.add_command(
            label="Replace...",
            command=self._replace_dialog,
            accelerator="Ctrl+H",
        )
        edit_menu.add_command(
            label="Go to Line...",
            command=self._goto_line,
            accelerator="Ctrl+L",
        )
        edit_menu.add_separator()
        edit_menu.add_checkbutton(
            label="Word Wrap",
            command=self._toggle_wrap,
            variable=self.wrap_var,
        )
        edit_menu.add_separator()
        edit_menu.add_command(
            label="Preferences...", command=self._open_preferences
        )

        # Config menu
        config_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Config", menu=config_menu)
        config_menu.add_command(
            label="Load Config...",
            command=self._load_config,
            accelerator="F5",
        )
        config_menu.add_command(
            label="Reload Current", command=self._reload_config
        )
        config_menu.add_command(
            label="Unload Config", command=self._unload_config
        )
        config_menu.add_separator()
        config_menu.add_command(
            label="Show Config Info", command=self._show_config_info
        )
        config_menu.add_command(
            label="Validate Config", command=self._validate_config
        )

        # Examples menu
        examples_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Examples", menu=examples_menu)
        examples_menu.add_command(
            label="Python-Like",
            command=lambda: self._load_example("python_like.yaml"),
        )
        examples_menu.add_command(
            label="Minimal", command=lambda: self._load_example("minimal.json")
        )
        examples_menu.add_command(
            label="Spanish", command=lambda: self._load_example("spanish.yaml")
        )

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_checkbutton(
            label="Show Line Numbers",
            command=self._toggle_line_numbers,
            variable=self.show_line_numbers_var,
        )
        theme_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Theme", menu=theme_menu)
        theme_menu.add_radiobutton(
            label="Light",
            variable=self.theme_var,
            value="light",
            command=lambda: self._set_theme("light"),
        )
        theme_menu.add_radiobutton(
            label="Dark",
            variable=self.theme_var,
            value="dark",
            command=lambda: self._set_theme("dark"),
        )

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)

        # Toolbar
        toolbar = ttk.Frame(self)
        toolbar.pack(side="top", fill="x", padx=4, pady=2)
        ttk.Button(toolbar, text="New", command=self._new_file).pack(
            side="left"
        )
        ttk.Button(toolbar, text="Open", command=self._open_file).pack(
            side="left"
        )
        ttk.Button(toolbar, text="Save", command=self._save_file).pack(
            side="left"
        )
        ttk.Separator(toolbar, orient="vertical").pack(
            side="left", fill="y", padx=6
        )
        ttk.Button(
            toolbar, text="Load Config", command=self._load_config
        ).pack(side="left")
        ttk.Button(toolbar, text="Info", command=self._show_config_info).pack(
            side="left"
        )

        # Main panes
        panes = ttk.PanedWindow(self, orient="horizontal")
        panes.pack(fill="both", expand=True)

        # Editor on the left
        editor_frame = ttk.LabelFrame(panes, text="Code Editor")

        # Line numbers
        self.line_num_frame = ttk.Frame(editor_frame)
        self.line_num_frame.pack(side="left", fill="y")
        self.line_numbers = tk.Text(
            self.line_num_frame,
            width=4,
            padx=3,
            takefocus=0,
            border=0,
            background="#f0f0f0",
            state="disabled",
            wrap="none",
            font="TkFixedFont",
        )
        self.line_numbers.pack(side="left", fill="y")

        self.editor = tk.Text(
            editor_frame, wrap="none", undo=True, font="TkFixedFont"
        )
        self.editor.pack(side="left", fill="both", expand=True)

        # Scrollbars for editor
        editor_vscroll = ttk.Scrollbar(
            editor_frame, orient="vertical", command=self._on_editor_scroll
        )
        editor_vscroll.pack(side="right", fill="y")
        self.editor.configure(yscrollcommand=editor_vscroll.set)

        self.editor.bind("<KeyRelease>", self._on_editor_change)
        self.editor.bind("<Button-1>", self._on_editor_change)
        self._update_line_numbers()

        panes.add(editor_frame, weight=2)

        # Right side: console
        right_frame = ttk.LabelFrame(panes, text="Configuration Info")
        console_container = ttk.Frame(right_frame)
        console_container.pack(fill="both", expand=True)

        self.console = tk.Text(
            console_container,
            height=10,
            state="disabled",
            font="TkFixedFont",
            wrap="word",
        )
        vscroll = ttk.Scrollbar(
            console_container, orient="vertical", command=self.console.yview
        )
        self.console.configure(yscrollcommand=vscroll.set)
        console_container.columnconfigure(0, weight=1)
        console_container.rowconfigure(0, weight=1)
        self.console.grid(row=0, column=0, sticky="nsew")
        vscroll.grid(row=0, column=1, sticky="ns")

        panes.add(right_frame, weight=1)

        # Status bar
        self.status_bar = ttk.Frame(self)
        self.status_bar.pack(side="bottom", fill="x")

        self.status_label = ttk.Label(
            self.status_bar, text="Ready", relief="sunken", anchor="w"
        )
        self.status_label.pack(side="left", fill="x", expand=True)

        self.position_label = ttk.Label(
            self.status_bar, text="Line 1, Col 1", relief="sunken", width=15
        )
        self.position_label.pack(side="right")

    def _update_line_numbers(self) -> None:
        """Update line numbers in the gutter."""
        line_count = int(self.editor.index("end-1c").split(".")[0])
        line_numbers_str = "\n".join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.configure(state="normal")
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", line_numbers_str)
        self.line_numbers.configure(state="disabled")

    def _on_editor_scroll(self, *args) -> None:
        """Sync editor and line numbers scrolling."""
        self.editor.yview(*args)
        self.line_numbers.yview(*args)

    def _on_editor_change(self, event: Optional[tk.Event] = None) -> None:
        """Handle editor changes to update UI."""
        _ = event
        self._update_line_numbers()
        self._update_status()

    def _toggle_line_numbers(self) -> None:
        if self.show_line_numbers_var.get():
            self.line_num_frame.pack(side="left", fill="y")
            self.line_numbers.pack(side="left", fill="y")
            self._update_line_numbers()
        else:
            try:
                self.line_num_frame.pack_forget()
            except tk.TclError:
                pass
        self.settings["show_line_numbers"] = bool(
            self.show_line_numbers_var.get()
        )
        self._save_settings()

    def _set_theme(self, name: str) -> None:
        self.settings["theme"] = name
        self._save_settings()
        self._apply_settings()

    def _edit_undo(self) -> None:
        try:
            self.editor.edit_undo()
        except tk.TclError:
            pass

    def _edit_redo(self) -> None:
        try:
            self.editor.edit_redo()
        except tk.TclError:
            pass

    def _update_status(self) -> None:
        """Update cursor position in status bar."""
        cursor_pos = self.editor.index("insert")
        line, col = cursor_pos.split(".", maxsplit=1)
        self.position_label.configure(text=f"Line {line}, Col {int(col) + 1}")

    def _update_title(self) -> None:
        """Update window title with filename."""
        title = "Honey Badger LCS IDE v1.0"
        if self.current_file:
            filename = os.path.basename(self.current_file)
            title += f" - {filename}"
        if self.current_config:
            title += f" [{self.current_config.name}]"
        self.root.title(title)

    # File operations
    def _new_file(self) -> None:
        self.current_file = None
        self.editor.delete("1.0", "end")
        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        self.console.configure(state="disabled")
        self._update_title()
        self.status_label.configure(text="New file created")

    def _open_file(self) -> None:
        path = filedialog.askopenfilename(
            title="Open file",
            filetypes=[
                ("Python", "*.py"),
                ("JSON", "*.json"),
                ("YAML", "*.yaml;*.yml"),
                ("All", "*.*"),
            ],
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.editor.delete("1.0", "end")
                self.editor.insert("1.0", f.read())
                self.current_file = path
                self._update_title()
                self.status_label.configure(text=f"Opened: {path}")
        except OSError as e:
            messagebox.showerror("Open failed", str(e))

    def _save_file(self) -> None:
        if self.current_file:
            try:
                with open(self.current_file, "w", encoding="utf-8") as f:
                    f.write(self.editor.get("1.0", "end-1c"))
                self.status_label.configure(text=f"Saved: {self.current_file}")
            except OSError as e:
                messagebox.showerror("Save failed", str(e))
        else:
            self._save_file_as()

    def _save_file_as(self) -> None:
        path = filedialog.asksaveasfilename(
            title="Save file as",
            filetypes=[
                ("Python", "*.py"),
                ("JSON", "*.json"),
                ("YAML", "*.yaml"),
                ("All", "*.*"),
            ],
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.editor.get("1.0", "end-1c"))
            self.current_file = path
            self._update_title()
            self.status_label.configure(text=f"Saved: {path}")
        except OSError as e:
            messagebox.showerror("Save failed", str(e))

    # Configuration operations
    def _load_config(self) -> None:
        path = filedialog.askopenfilename(
            title="Load Language Configuration",
            filetypes=[
                ("YAML", "*.yaml;*.yml"),
                ("JSON", "*.json"),
                ("All", "*.*"),
            ],
        )
        if not path:
            return
        try:
            self.current_config = LanguageConfig.load(path)
            LanguageRuntime.load_config(self.current_config)
            self.settings["last_config"] = path
            self._save_settings()
            self._update_title()
            self._display_config_info()
            self.status_label.configure(text=f"Loaded config: {path}")
        except Exception as e:
            messagebox.showerror("Failed to load config", str(e))

    def _reload_config(self) -> None:
        if self.settings.get("last_config"):
            try:
                self.current_config = LanguageConfig.load(
                    self.settings["last_config"]
                )
                LanguageRuntime.load_config(self.current_config)
                self._display_config_info()
                self.status_label.configure(text="Config reloaded")
            except Exception as e:
                messagebox.showerror("Failed to reload config", str(e))
        else:
            messagebox.showinfo(
                "No config",
                "No configuration loaded yet. Use Load Config first.",
            )

    def _unload_config(self) -> None:
        self.current_config = None
        LanguageRuntime.reset()
        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        self.console.configure(state="disabled")
        self._update_title()
        self.status_label.configure(text="Config unloaded")

    def _show_config_info(self) -> None:
        if self.current_config:
            self._display_config_info()
        else:
            messagebox.showinfo(
                "No config", "No configuration loaded. Use Load Config first."
            )

    def _display_config_info(self) -> None:
        """Display configuration info in console."""
        if not self.current_config:
            return

        info = LanguageRuntime.get_info()
        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        self.console.insert("1.0", info)
        self.console.configure(state="disabled")

    def _validate_config(self) -> None:
        if not self.current_config:
            messagebox.showinfo(
                "No config", "No configuration loaded. Use Load Config first."
            )
            return

        errors = self.current_config.validate()
        if errors:
            error_text = "\n".join(f"  • {e}" for e in errors)
            messagebox.showwarning(
                "Validation Errors",
                f"Found {len(errors)} validation errors:\n\n{error_text}",
            )
        else:
            messagebox.showinfo(
                "Validation Success", "✓ Configuration is valid!"
            )

    def _load_example(self, filename: str) -> None:
        """Load an example configuration."""
        examples_dir = os.path.join(os.path.dirname(__file__), "examples")
        path = os.path.join(examples_dir, filename)

        if not os.path.isfile(path):
            messagebox.showerror(
                "Example not found", f"Could not find: {path}"
            )
            return

        try:
            self.current_config = LanguageConfig.load(path)
            LanguageRuntime.load_config(self.current_config)
            self._update_title()
            self._display_config_info()
            self.status_label.configure(text=f"Loaded example: {filename}")
        except Exception as e:
            messagebox.showerror("Failed to load example", str(e))

    def _load_default_example(self) -> None:
        sample = (
            "# Honey Badger Language Construction Set\n"
            "# Create custom programming language variants\n\n"
            "from language_config import LanguageConfig\n\n"
            "# Create a new configuration\n"
            "config = LanguageConfig(\n"
            '    name="My Custom Language",\n'
            '    version="1.0"\n'
            ")\n\n"
            "# Rename keywords\n"
            'config.rename_keyword("if", "when")\n'
            'config.rename_keyword("function", "def")\n\n'
            "# Save configuration\n"
            'config.save("my_language.yaml")\n'
        )
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", sample)
        self.current_file = None
        self._update_title()

    # Editor utilities
    def _find_dialog(self) -> None:
        win = tk.Toplevel(self.root)
        win.title("Find")
        ttk.Label(win, text="Find:").grid(row=0, column=0, padx=6, pady=6)
        find_var = tk.StringVar()
        ttk.Entry(win, textvariable=find_var, width=32).grid(
            row=0, column=1, padx=6, pady=6
        )

        def do_find() -> None:
            needle = find_var.get()
            if not needle:
                return
            start_pos = self.editor.search(
                needle, "insert", stopindex="end", nocase=True
            )
            if start_pos:
                end_pos = f"{start_pos}+{len(needle)}c"
                self.editor.tag_remove("sel", "1.0", "end")
                self.editor.tag_add("sel", start_pos, end_pos)
                self.editor.mark_set("insert", end_pos)
                self.editor.see(start_pos)
            else:
                messagebox.showinfo("Not found", f"'{needle}' not found.")
            win.lift()

        ttk.Button(win, text="Find Next", command=do_find).grid(
            row=1, column=1, padx=6, pady=6, sticky="e"
        )

    def _replace_dialog(self) -> None:
        win = tk.Toplevel(self.root)
        win.title("Replace")
        ttk.Label(win, text="Find:").grid(row=0, column=0, padx=6, pady=6)
        find_var = tk.StringVar()
        ttk.Entry(win, textvariable=find_var, width=32).grid(
            row=0, column=1, padx=6, pady=6
        )
        ttk.Label(win, text="Replace:").grid(row=1, column=0, padx=6, pady=6)
        repl_var = tk.StringVar()
        ttk.Entry(win, textvariable=repl_var, width=32).grid(
            row=1, column=1, padx=6, pady=6
        )

        def do_replace_all() -> None:
            needle = find_var.get()
            replacement = repl_var.get()
            if not needle:
                return
            content = self.editor.get("1.0", "end-1c")
            new_content = content.replace(needle, replacement)
            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", new_content)
            win.destroy()

        ttk.Button(win, text="Replace All", command=do_replace_all).grid(
            row=2, column=1, padx=6, pady=6, sticky="e"
        )

    def _goto_line(self) -> None:
        line_num = simpledialog.askinteger(
            "Go to Line", "Line number:", parent=self.root, minvalue=1
        )
        if line_num:
            self.editor.mark_set("insert", f"{line_num}.0")
            self.editor.see("insert")
            self._update_status()

    def _toggle_wrap(self) -> None:
        if self.wrap_var.get():
            self.editor.configure(wrap="word")
        else:
            self.editor.configure(wrap="none")

    # Settings
    def _config_path(self) -> str:
        config_dir = os.path.expanduser("~/.hb_lcs")
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, "settings.json")

    def _load_settings(self) -> None:
        path = self._config_path()
        try:
            if os.path.isfile(path):
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.settings.update(data)
        except (OSError, json.JSONDecodeError, ValueError):
            pass

    def _save_settings(self) -> None:
        data = dict(self.settings)
        data["geometry"] = self.root.geometry()
        try:
            with open(self._config_path(), "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except (OSError, TypeError):
            pass

    def _apply_settings(self) -> None:
        theme = str(self.settings.get("theme", "light"))
        ed_size = int(str(self.settings.get("editor_font_size", 11)))
        con_size = int(str(self.settings.get("console_font_size", 11)))

        if theme == "dark":
            self.editor.configure(
                bg="#2b2b2b", fg="#f8f8f2", insertbackground="white"
            )
            self.console.configure(
                bg="#2b2b2b", fg="#f8f8f2", insertbackground="white"
            )
        else:
            self.editor.configure(
                bg="white", fg="black", insertbackground="black"
            )
            self.console.configure(
                bg="white", fg="black", insertbackground="black"
            )

        self.editor.configure(font=("TkFixedFont", ed_size))
        self.console.configure(font=("TkFixedFont", con_size))

        if self.settings.get("geometry"):
            try:
                self.root.geometry(self.settings["geometry"])
            except tk.TclError:
                pass

        show_ln = self.settings.get("show_line_numbers", True)
        self.show_line_numbers_var.set(show_ln)

    def _open_preferences(self) -> None:
        win = tk.Toplevel(self.root)
        win.title("Preferences")
        win.resizable(False, False)

        ttk.Label(win, text="Theme:").grid(
            row=0, column=0, padx=8, pady=6, sticky="e"
        )
        theme_val = str(self.settings.get("theme", "light"))
        theme_var = tk.StringVar(value=theme_val)
        ttk.OptionMenu(win, theme_var, theme_var.get(), "light", "dark").grid(
            row=0, column=1, padx=8, pady=6, sticky="w"
        )

        ttk.Label(win, text="Editor font size:").grid(
            row=1, column=0, padx=8, pady=6, sticky="e"
        )
        ed_size = int(str(self.settings.get("editor_font_size", 11)))
        ed_var = tk.IntVar(value=ed_size)
        ttk.Spinbox(win, from_=8, to=32, textvariable=ed_var, width=6).grid(
            row=1, column=1, padx=8, pady=6, sticky="w"
        )

        ttk.Label(win, text="Console font size:").grid(
            row=2, column=0, padx=8, pady=6, sticky="e"
        )
        co_size = int(str(self.settings.get("console_font_size", 11)))
        co_var = tk.IntVar(value=co_size)
        ttk.Spinbox(win, from_=8, to=32, textvariable=co_var, width=6).grid(
            row=2, column=1, padx=8, pady=6, sticky="w"
        )

        def save_prefs() -> None:
            self.settings["theme"] = theme_var.get()
            self.settings["editor_font_size"] = ed_var.get()
            self.settings["console_font_size"] = co_var.get()
            self._save_settings()
            self._apply_settings()
            win.destroy()

        ttk.Button(win, text="Save", command=save_prefs).grid(
            row=3, column=1, padx=8, pady=12, sticky="e"
        )

    def _show_about(self) -> None:
        about_text = (
            "Honey Badger Language Construction Set - IDE v1.0\n\n"
            "Integrated Development Environment for Language Construction\n\n"
            "Features:\n"
            "• Load and test language configurations\n"
            "• Syntax highlighting for Python\n"
            "• Configuration validation\n"
            "• Example configurations\n\n"
            "Build custom programming languages with ease"
        )
        messagebox.showinfo("About Honey Badger LCS IDE", about_text)

    def _on_close(self) -> None:
        self._save_settings()
        self.root.destroy()


def main() -> None:
    """Start the IDE."""
    root = tk.Tk()
    app = HBLCS_IDE(root)
    app.mainloop()


if __name__ == "__main__":
    main()
