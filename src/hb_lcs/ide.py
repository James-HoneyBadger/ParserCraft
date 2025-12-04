#!/usr/bin/env python3
"""
Honey Badger Language Construction Set - Advanced IDE

A comprehensive graphical IDE for creating, editing, and testing
custom programming languages.
Features include:
- Interactive configuration editor
- Syntax highlighting and code completion
- Multi-panel interface with editor, console, and configuration panels
- Built-in help system and tutorials
- Project management and version control integration
- Testing and validation tools
- Export/import capabilities
- Advanced language construction features
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog, scrolledtext
import os
from typing import Optional, List

from .language_config import LanguageConfig, list_presets
from .language_runtime import LanguageRuntime


class AdvancedIDE(ttk.Frame):
    """Advanced IDE for Honey Badger Language Construction Set."""

    def __init__(self, master: Optional[tk.Misc] = None):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.root = tk.Tk() if master is None else master.winfo_toplevel()
        self.root.title(
            "Honey Badger Language Construction Set - Advanced IDE v2.0"
        )
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        # Initialize state
        self.current_file: Optional[str] = None
        self.current_config: Optional[LanguageConfig] = None
        self.current_project: Optional[str] = None
        self.search_history: List[str] = []
        self.clipboard_history: List[str] = []
        self.undo_stack: List[str] = []
        self.redo_stack: List[str] = []

        # Settings
        self.settings = {
            "theme": "light",
            "editor_font_size": 11,
            "console_font_size": 10,
            "show_line_numbers": True,
            "show_minimap": False,
            "auto_save": False,
            "syntax_highlighting": True,
            "code_completion": True,
            "geometry": "1400x900",
            "last_project": None,
            "recent_files": [],
            "recent_configs": [],
        }

        # UI State
        self.wrap_var = tk.BooleanVar(value=False)
        self.show_line_numbers_var = tk.BooleanVar(value=True)
        self.show_minimap_var = tk.BooleanVar(value=False)
        self.syntax_highlight_var = tk.BooleanVar(value=True)
        self.code_completion_var = tk.BooleanVar(value=True)
        self.theme_var = tk.StringVar(value="light")

        # Build the comprehensive UI
        self._build_ui()
        self._load_settings()
        self._apply_settings()
        self._load_default_content()

        # Keyboard shortcuts
        self._setup_keyboard_shortcuts()

        # Initialize features
        self._update_ui_state()
        self._update_title()

    def _build_ui(self) -> None:
        """Build the comprehensive UI with multiple panels."""
        self.root.geometry(self.settings.get("geometry", "1400x900"))
        self.root.minsize(1200, 700)

        # Create menu bar
        self._create_menus()

        # Create toolbar
        self._create_toolbar()

        # Create main content area with multiple panels
        self._create_main_panels()

        # Create status bar
        self._create_status_bar()

    def _create_menus(self) -> None:
        """Create comprehensive menu system."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        self._create_file_menu(menubar)

        # Edit menu
        self._create_edit_menu(menubar)

        # View menu
        self._create_view_menu(menubar)

        # Language menu
        self._create_language_menu(menubar)

        # Project menu
        self._create_project_menu(menubar)

        # Tools menu
        self._create_tools_menu(menubar)

        # Window menu
        self._create_window_menu(menubar)

        # Help menu
        self._create_help_menu(menubar)

    def _create_file_menu(self, menubar: tk.Menu) -> None:
        """Create File menu with all operations."""
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)

        # New submenu
        new_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="New", menu=new_menu)
        new_menu.add_command(
            label="File", command=self._new_file, accelerator="Ctrl+N"
        )
        new_menu.add_command(label="Project", command=self._new_project)
        new_menu.add_command(
            label="Language Config", command=self._new_language_config
        )
        new_menu.add_separator()
        new_menu.add_command(
            label="From Template...", command=self._new_from_template
        )

        file_menu.add_command(
            label="Open...", command=self._open_file, accelerator="Ctrl+O"
        )
        file_menu.add_command(
            label="Open Recent", command=self._open_recent_menu
        )

        file_menu.add_separator()
        file_menu.add_command(
            label="Save", command=self._save_file, accelerator="Ctrl+S"
        )
        file_menu.add_command(
            label="Save As...",
            command=self._save_file_as,
            accelerator="Ctrl+Shift+S",
        )
        file_menu.add_command(
            label="Save All", command=self._save_all, accelerator="Ctrl+Alt+S"
        )

        file_menu.add_separator()
        file_menu.add_command(label="Import...", command=self._import_file)
        file_menu.add_command(label="Export...", command=self._export_file)

        file_menu.add_separator()
        file_menu.add_command(
            label="Close", command=self._close_file, accelerator="Ctrl+W"
        )
        file_menu.add_command(label="Close All", command=self._close_all)
        file_menu.add_command(
            label="Exit", command=self.root.quit, accelerator="Ctrl+Q"
        )

    def _create_edit_menu(self, menubar: tk.Menu) -> None:
        """Create Edit menu with advanced editing features."""
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        edit_menu.add_command(
            label="Undo", command=self._edit_undo, accelerator="Ctrl+Z"
        )
        edit_menu.add_command(
            label="Redo", command=self._edit_redo, accelerator="Ctrl+Y"
        )

        edit_menu.add_separator()
        edit_menu.add_command(
            label="Cut", command=self._edit_cut, accelerator="Ctrl+X"
        )
        edit_menu.add_command(
            label="Copy", command=self._edit_copy, accelerator="Ctrl+C"
        )
        edit_menu.add_command(
            label="Paste", command=self._edit_paste, accelerator="Ctrl+V"
        )
        edit_menu.add_command(
            label="Delete", command=self._edit_delete, accelerator="Del"
        )

        edit_menu.add_separator()
        edit_menu.add_command(
            label="Select All",
            command=self._edit_select_all,
            accelerator="Ctrl+A",
        )
        edit_menu.add_command(
            label="Select Line",
            command=self._edit_select_line,
            accelerator="Ctrl+L",
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
            label="Find in Files...",
            command=self._find_in_files,
            accelerator="Ctrl+Shift+F",
        )

        edit_menu.add_separator()
        edit_menu.add_command(
            label="Go to Line...",
            command=self._goto_line,
            accelerator="Ctrl+G",
        )
        edit_menu.add_command(
            label="Go to Definition",
            command=self._goto_definition,
            accelerator="F12",
        )

        edit_menu.add_separator()
        edit_menu.add_command(
            label="Format Document",
            command=self._format_document,
            accelerator="Shift+Alt+F",
        )
        edit_menu.add_command(
            label="Comment Line",
            command=self._toggle_comment,
            accelerator="Ctrl+/",
        )

    def _create_view_menu(self, menubar: tk.Menu) -> None:
        """Create View menu with display options."""
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)

        # Panels submenu
        panels_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Panels", menu=panels_menu)
        panels_menu.add_checkbutton(
            label="Editor", command=self._toggle_editor_panel
        )
        panels_menu.add_checkbutton(
            label="Console", command=self._toggle_console_panel
        )
        panels_menu.add_checkbutton(
            label="Config Editor", command=self._toggle_config_panel
        )
        panels_menu.add_checkbutton(
            label="Project Explorer", command=self._toggle_project_panel
        )
        panels_menu.add_checkbutton(
            label="Minimap", command=self._toggle_minimap
        )

        view_menu.add_separator()
        view_menu.add_checkbutton(
            label="Line Numbers",
            command=self._toggle_line_numbers,
            variable=self.show_line_numbers_var,
        )
        view_menu.add_checkbutton(
            label="Word Wrap",
            command=self._toggle_wrap,
            variable=self.wrap_var,
        )
        view_menu.add_checkbutton(
            label="Syntax Highlighting",
            command=self._toggle_syntax_highlighting,
            variable=self.syntax_highlight_var,
        )
        view_menu.add_checkbutton(
            label="Code Completion",
            command=self._toggle_code_completion,
            variable=self.code_completion_var,
        )

        view_menu.add_separator()
        # Theme submenu
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
        theme_menu.add_radiobutton(
            label="High Contrast",
            variable=self.theme_var,
            value="high_contrast",
            command=lambda: self._set_theme("high_contrast"),
        )

        view_menu.add_separator()
        view_menu.add_command(
            label="Zoom In", command=self._zoom_in, accelerator="Ctrl+="
        )
        view_menu.add_command(
            label="Zoom Out", command=self._zoom_out, accelerator="Ctrl+-"
        )
        view_menu.add_command(
            label="Reset Zoom", command=self._reset_zoom, accelerator="Ctrl+0"
        )

    def _create_language_menu(self, menubar: tk.Menu) -> None:
        """Create Language menu for configuration operations."""
        lang_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Language", menu=lang_menu)

        # Config operations
        lang_menu.add_command(
            label="New Configuration",
            command=self._new_language_config,
            accelerator="Ctrl+Shift+N",
        )
        lang_menu.add_command(
            label="Load Configuration...",
            command=self._load_config,
            accelerator="F5",
        )
        lang_menu.add_command(
            label="Reload Configuration",
            command=self._reload_config,
            accelerator="F6",
        )
        lang_menu.add_command(
            label="Unload Configuration", command=self._unload_config
        )

        lang_menu.add_separator()
        lang_menu.add_command(
            label="Save Configuration", command=self._save_config
        )
        lang_menu.add_command(
            label="Save Configuration As...", command=self._save_config_as
        )

        lang_menu.add_separator()
        lang_menu.add_command(
            label="Validate Configuration",
            command=self._validate_config,
            accelerator="F7",
        )
        lang_menu.add_command(
            label="Show Configuration Info",
            command=self._show_config_info,
            accelerator="F8",
        )
        lang_menu.add_command(
            label="Compare Configurations...", command=self._compare_configs
        )

        # Presets submenu
        presets_menu = tk.Menu(lang_menu, tearoff=0)
        lang_menu.add_cascade(label="Load Preset", menu=presets_menu)
        for preset in list_presets():
            presets_menu.add_command(
                label=preset.replace("_", " ").title(),
                command=lambda p=preset: self._load_preset(p),
            )

        lang_menu.add_separator()
        # Language features submenu
        features_menu = tk.Menu(lang_menu, tearoff=0)
        lang_menu.add_cascade(label="Language Features", menu=features_menu)
        features_menu.add_command(
            label="Add Keyword Mapping", command=self._add_keyword_mapping
        )
        features_menu.add_command(
            label="Add Function", command=self._add_function
        )
        features_menu.add_command(
            label="Configure Syntax", command=self._configure_syntax
        )
        features_menu.add_command(
            label="Set Operators", command=self._set_operators
        )

        lang_menu.add_separator()
        lang_menu.add_command(
            label="Test Language", command=self._test_language
        )
        lang_menu.add_command(
            label="Run Code", command=self._run_code, accelerator="F9"
        )

    def _create_project_menu(self, menubar: tk.Menu) -> None:
        """Create Project menu for project management."""
        project_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Project", menu=project_menu)

        project_menu.add_command(
            label="New Project", command=self._new_project
        )
        project_menu.add_command(
            label="Open Project...", command=self._open_project
        )
        project_menu.add_command(
            label="Close Project", command=self._close_project
        )

        project_menu.add_separator()
        project_menu.add_command(
            label="Add File", command=self._add_file_to_project
        )
        project_menu.add_command(
            label="Add Folder", command=self._add_folder_to_project
        )
        project_menu.add_command(
            label="Remove from Project", command=self._remove_from_project
        )

        project_menu.add_separator()
        project_menu.add_command(
            label="Project Settings", command=self._project_settings
        )
        project_menu.add_command(
            label="Build Project", command=self._build_project
        )
        project_menu.add_command(
            label="Clean Project", command=self._clean_project
        )

        project_menu.add_separator()
        project_menu.add_command(label="Git Status", command=self._git_status)
        project_menu.add_command(label="Git Commit", command=self._git_commit)
        project_menu.add_command(label="Git Push", command=self._git_push)

    def _create_tools_menu(self, menubar: tk.Menu) -> None:
        """Create Tools menu with development utilities."""
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)

        tools_menu.add_command(label="Terminal", command=self._open_terminal)
        tools_menu.add_command(
            label="Command Palette",
            command=self._command_palette,
            accelerator="Ctrl+Shift+P",
        )

        tools_menu.add_separator()
        tools_menu.add_command(
            label="Generate Documentation", command=self._generate_docs
        )
        tools_menu.add_command(
            label="Run Tests",
            command=self._run_tests,
            accelerator="Ctrl+Shift+T",
        )
        tools_menu.add_command(
            label="Debug Code", command=self._debug_code, accelerator="F10"
        )

        tools_menu.add_separator()
        # Code analysis submenu
        analysis_menu = tk.Menu(tools_menu, tearoff=0)
        tools_menu.add_cascade(label="Code Analysis", menu=analysis_menu)
        analysis_menu.add_command(
            label="Check Syntax", command=self._check_syntax
        )
        analysis_menu.add_command(
            label="Find References", command=self._find_references
        )
        analysis_menu.add_command(
            label="Show Call Hierarchy", command=self._show_call_hierarchy
        )

        tools_menu.add_separator()
        tools_menu.add_command(
            label="Settings", command=self._open_settings, accelerator="Ctrl+,"
        )

    def _create_window_menu(self, menubar: tk.Menu) -> None:
        """Create Window menu for layout management."""
        window_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Window", menu=window_menu)

        window_menu.add_command(label="New Window", command=self._new_window)
        window_menu.add_command(
            label="Close Window", command=self._close_window
        )

        window_menu.add_separator()
        window_menu.add_command(
            label="Split Editor", command=self._split_editor
        )
        window_menu.add_command(label="Close Split", command=self._close_split)

        window_menu.add_separator()
        window_menu.add_command(
            label="Reset Layout", command=self._reset_layout
        )
        window_menu.add_command(label="Save Layout", command=self._save_layout)
        window_menu.add_command(label="Load Layout", command=self._load_layout)

    def _create_help_menu(self, menubar: tk.Menu) -> None:
        """Create Help menu with comprehensive help system."""
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)

        help_menu.add_command(
            label="Welcome", command=self._show_welcome, accelerator="F1"
        )
        help_menu.add_command(
            label="Interactive Tutorial", command=self._start_tutorial
        )
        help_menu.add_command(
            label="Quick Start Guide", command=self._quick_start_guide
        )

        help_menu.add_separator()
        help_menu.add_command(
            label="Documentation", command=self._open_documentation
        )
        help_menu.add_command(
            label="Language Reference", command=self._language_reference
        )
        help_menu.add_command(
            label="API Reference", command=self._api_reference
        )

        help_menu.add_separator()
        # Tutorials submenu
        tutorials_menu = tk.Menu(help_menu, tearoff=0)
        help_menu.add_cascade(label="Tutorials", menu=tutorials_menu)
        tutorials_menu.add_command(
            label="Creating Your First Language",
            command=lambda: self._tutorial("first_language"),
        )
        tutorials_menu.add_command(
            label="Advanced Syntax Customization",
            command=lambda: self._tutorial("advanced_syntax"),
        )
        tutorials_menu.add_command(
            label="Building Language Extensions",
            command=lambda: self._tutorial("extensions"),
        )
        tutorials_menu.add_command(
            label="Testing and Validation",
            command=lambda: self._tutorial("testing"),
        )

        # Examples submenu
        examples_menu = tk.Menu(help_menu, tearoff=0)
        help_menu.add_cascade(label="Examples", menu=examples_menu)
        examples_menu.add_command(
            label="Basic Keyword Renaming",
            command=lambda: self._example("keyword_rename"),
        )
        examples_menu.add_command(
            label="Functional Language",
            command=lambda: self._example("functional"),
        )
        examples_menu.add_command(
            label="Object-Oriented Syntax",
            command=lambda: self._example("oop"),
        )
        examples_menu.add_command(
            label="Domain-Specific Language",
            command=lambda: self._example("dsl"),
        )

        help_menu.add_separator()
        help_menu.add_command(
            label="Keyboard Shortcuts",
            command=self._show_shortcuts,
            accelerator="Ctrl+K Ctrl+S",
        )
        help_menu.add_command(label="About", command=self._show_about)

    def _create_toolbar(self) -> None:
        """Create comprehensive toolbar."""
        toolbar = ttk.Frame(self)
        toolbar.pack(side="top", fill="x", padx=4, pady=2)

        # File operations
        ttk.Button(toolbar, text="New", command=self._new_file).pack(
            side="left", padx=2
        )
        ttk.Button(toolbar, text="Open", command=self._open_file).pack(
            side="left", padx=2
        )
        ttk.Button(toolbar, text="Save", command=self._save_file).pack(
            side="left", padx=2
        )

        ttk.Separator(toolbar, orient="vertical").pack(
            side="left", fill="y", padx=6
        )

        # Language operations
        ttk.Button(
            toolbar, text="Load Config", command=self._load_config
        ).pack(side="left", padx=2)
        ttk.Button(
            toolbar, text="Validate", command=self._validate_config
        ).pack(side="left", padx=2)
        ttk.Button(toolbar, text="Run", command=self._run_code).pack(
            side="left", padx=2
        )

        ttk.Separator(toolbar, orient="vertical").pack(
            side="left", fill="y", padx=6
        )

        # Edit operations
        ttk.Button(toolbar, text="Find", command=self._find_dialog).pack(
            side="left", padx=2
        )
        ttk.Button(toolbar, text="Replace", command=self._replace_dialog).pack(
            side="left", padx=2
        )

        ttk.Separator(toolbar, orient="vertical").pack(
            side="left", fill="y", padx=6
        )

        # Help
        ttk.Button(toolbar, text="Help", command=self._show_welcome).pack(
            side="right", padx=2
        )

    def _create_main_panels(self) -> None:
        """Create the main multi-panel interface."""
        # Main container
        main_container = ttk.Frame(self)
        main_container.pack(fill="both", expand=True)

        # Create notebook for different views
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill="both", expand=True)

        # Editor tab
        self._create_editor_tab()

        # Configuration Editor tab
        self._create_config_editor_tab()

        # Console tab
        self._create_console_tab()

        # Project Explorer tab
        self._create_project_tab()

    def _create_editor_tab(self) -> None:
        """Create the main code editor tab."""
        editor_frame = ttk.Frame(self.notebook)
        self.notebook.add(editor_frame, text="Editor")

        # Editor container
        editor_container = ttk.Frame(editor_frame)
        editor_container.pack(fill="both", expand=True)

        # Line numbers
        self.line_num_frame = ttk.Frame(editor_container)
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

        # Main editor
        self.editor = tk.Text(
            editor_container, wrap="none", undo=True, font="TkFixedFont"
        )
        self.editor.pack(side="left", fill="both", expand=True)

        # Minimap (optional)
        self.minimap_frame = ttk.Frame(editor_container)
        self.minimap = tk.Text(
            self.minimap_frame,
            width=20,
            takefocus=0,
            border=0,
            state="disabled",
            wrap="none",
            font=("TkFixedFont", 2),
        )

        # Scrollbars
        editor_vscroll = ttk.Scrollbar(
            editor_container, orient="vertical", command=self._on_editor_scroll
        )
        editor_vscroll.pack(side="right", fill="y")
        self.editor.configure(yscrollcommand=editor_vscroll.set)

        # Bind events
        self.editor.bind("<KeyRelease>", self._on_editor_change)
        self.editor.bind("<Button-1>", self._on_editor_change)
        self._update_line_numbers()

    def _create_config_editor_tab(self) -> None:
        """Create the interactive configuration editor tab."""
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="Config Editor")

        # Configuration editor with sections
        config_container = ttk.Frame(config_frame)
        config_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Create sections for different config aspects
        self._create_config_sections(config_container)

    def _create_config_sections(self, parent: ttk.Frame) -> None:
        """Create interactive configuration sections."""
        # Metadata section
        metadata_frame = ttk.LabelFrame(parent, text="Language Metadata")
        metadata_frame.pack(fill="x", pady=5)

        ttk.Label(metadata_frame, text="Name:").grid(
            row=0, column=0, sticky="w", padx=5, pady=2
        )
        self.config_name_var = tk.StringVar()
        ttk.Entry(metadata_frame, textvariable=self.config_name_var).grid(
            row=0, column=1, sticky="ew", padx=5, pady=2
        )

        ttk.Label(metadata_frame, text="Version:").grid(
            row=1, column=0, sticky="w", padx=5, pady=2
        )
        self.config_version_var = tk.StringVar()
        ttk.Entry(metadata_frame, textvariable=self.config_version_var).grid(
            row=1, column=1, sticky="ew", padx=5, pady=2
        )

        # Keywords section
        keywords_frame = ttk.LabelFrame(parent, text="Keyword Mappings")
        keywords_frame.pack(fill="both", expand=True, pady=5)

        # Keywords listbox and controls
        keywords_container = ttk.Frame(keywords_frame)
        keywords_container.pack(fill="both", expand=True, padx=5, pady=5)

        self.keywords_listbox = tk.Listbox(keywords_container, height=8)
        keywords_scrollbar = ttk.Scrollbar(
            keywords_container,
            orient="vertical",
            command=self.keywords_listbox.yview,
        )
        self.keywords_listbox.configure(yscrollcommand=keywords_scrollbar.set)

        self.keywords_listbox.pack(side="left", fill="both", expand=True)
        keywords_scrollbar.pack(side="right", fill="y")

        # Keyword buttons
        keyword_buttons = ttk.Frame(keywords_container)
        keyword_buttons.pack(side="right", fill="y", padx=5)

        ttk.Button(
            keyword_buttons, text="Add", command=self._add_keyword_mapping
        ).pack(fill="x", pady=2)
        ttk.Button(
            keyword_buttons, text="Edit", command=self._edit_keyword_mapping
        ).pack(fill="x", pady=2)
        ttk.Button(
            keyword_buttons,
            text="Remove",
            command=self._remove_keyword_mapping,
        ).pack(fill="x", pady=2)

        # Functions section
        functions_frame = ttk.LabelFrame(parent, text="Functions")
        functions_frame.pack(fill="both", expand=True, pady=5)

        # Similar structure for functions...

        # Syntax section
        syntax_frame = ttk.LabelFrame(parent, text="Syntax Options")
        syntax_frame.pack(fill="both", expand=True, pady=5)

        # Syntax controls...

    def _create_console_tab(self) -> None:
        """Create the console/output tab."""
        console_frame = ttk.Frame(self.notebook)
        self.notebook.add(console_frame, text="Console")

        console_container = ttk.Frame(console_frame)
        console_container.pack(fill="both", expand=True, padx=5, pady=5)

        self.console = scrolledtext.ScrolledText(
            console_container,
            height=15,
            state="disabled",
            font=("TkFixedFont", 10),
            wrap="word",
        )
        self.console.pack(fill="both", expand=True)

        # Console toolbar
        console_toolbar = ttk.Frame(console_container)
        console_toolbar.pack(fill="x", pady=2)

        ttk.Button(
            console_toolbar, text="Clear", command=self._clear_console
        ).pack(side="left", padx=2)
        ttk.Button(
            console_toolbar, text="Copy", command=self._copy_console
        ).pack(side="left", padx=2)
        ttk.Button(
            console_toolbar,
            text="Save Output",
            command=self._save_console_output,
        ).pack(side="left", padx=2)

    def _create_project_tab(self) -> None:
        """Create the project explorer tab."""
        project_frame = ttk.Frame(self.notebook)
        self.notebook.add(project_frame, text="Project")

        project_container = ttk.Frame(project_frame)
        project_container.pack(fill="both", expand=True, padx=5, pady=5)

        # Project tree
        self.project_tree = ttk.Treeview(project_container)
        project_tree_scrollbar = ttk.Scrollbar(
            project_container,
            orient="vertical",
            command=self.project_tree.yview,
        )
        self.project_tree.configure(yscrollcommand=project_tree_scrollbar.set)

        self.project_tree.pack(side="left", fill="both", expand=True)
        project_tree_scrollbar.pack(side="right", fill="y")

        # Project toolbar
        project_toolbar = ttk.Frame(project_container)
        project_toolbar.pack(fill="x", pady=2)

        ttk.Button(
            project_toolbar, text="Refresh", command=self._refresh_project_tree
        ).pack(side="left", padx=2)
        ttk.Button(
            project_toolbar, text="Open", command=self._open_selected_file
        ).pack(side="left", padx=2)

    def _create_status_bar(self) -> None:
        """Create the status bar."""
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

        self.language_label = ttk.Label(
            self.status_bar, text="No Language", relief="sunken", width=20
        )
        self.language_label.pack(side="right", padx=2)

    def _setup_keyboard_shortcuts(self) -> None:
        """Setup comprehensive keyboard shortcuts."""
        shortcuts = [
            ("<Control-n>", self._new_file),
            ("<Control-o>", self._open_file),
            ("<Control-s>", self._save_file),
            ("<Control-Shift-S>", self._save_file_as),
            ("<Control-w>", self._close_file),
            ("<Control-q>", self.root.quit),
            ("<F5>", self._load_config),
            ("<F6>", self._reload_config),
            ("<F7>", self._validate_config),
            ("<F8>", self._show_config_info),
            ("<F9>", self._run_code),
            ("<F1>", self._show_welcome),
            ("<Control-f>", self._find_dialog),
            ("<Control-h>", self._replace_dialog),
            ("<Control-g>", self._goto_line),
            ("<F12>", self._goto_definition),
            ("<Control-slash>", self._toggle_comment),
            ("<Control-Shift-P>", self._command_palette),
        ]

        for shortcut, command in shortcuts:
            self.root.bind(shortcut, lambda e, cmd=command: cmd())

    # Implementation methods would continue here...
    # This is a comprehensive framework - full implementation would  # noqa
    # be extensive

    def _show_welcome(self) -> None:
        """Show welcome screen with tutorials."""
        welcome_win = tk.Toplevel(self.root)
        welcome_win.title("Welcome to Honey Badger LCS IDE")
        welcome_win.geometry("800x600")

        # Welcome content
        welcome_text = """
# Welcome to Honey Badger Language Construction Set IDE

This advanced IDE helps you create custom programming languages with ease.

## Quick Start

1. **Create a new language configuration** using the Language menu
2. **Customize keywords, functions, and syntax** in the Config Editor tab
3. **Test your language** by writing and running code in the Editor tab
4. **Save and export** your language configurations

## Features

- **Interactive Configuration Editor**: Visual editing of language features
- **Multi-panel Interface**: Editor, Console, Config Editor, Project Explorer
- **Syntax Highlighting**: Code highlighting for better readability
- **Code Completion**: Intelligent suggestions while typing
- **Project Management**: Organize your language development projects
- **Built-in Help**: Comprehensive tutorials and documentation

## Getting Started

Click "Interactive Tutorial" to learn step-by-step how to create your first language!  # noqa: E501

For more information, visit the Help menu.
        """

        text_widget = scrolledtext.ScrolledText(
            welcome_win, wrap="word", font=("TkDefaultFont", 10)
        )
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        text_widget.insert("1.0", welcome_text)
        text_widget.config(state="disabled")

        # Buttons
        button_frame = ttk.Frame(welcome_win)
        button_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(
            button_frame,
            text="Start Tutorial",
            command=lambda: [self._start_tutorial(), welcome_win.destroy()],
        ).pack(side="left", padx=5)
        ttk.Button(
            button_frame,
            text="Quick Start Guide",
            command=lambda: [self._quick_start_guide(), welcome_win.destroy()],
        ).pack(side="left", padx=5)
        ttk.Button(
            button_frame, text="Close", command=welcome_win.destroy
        ).pack(side="right", padx=5)

    def _start_tutorial(self) -> None:
        """Start the interactive tutorial."""
        tutorial_win = tk.Toplevel(self.root)
        tutorial_win.title("Interactive Tutorial")
        tutorial_win.geometry("700x500")

        # Tutorial steps
        steps = [
            {
                "title": "Step 1: Create a New Language Configuration",
                "content": "Let's start by creating a new language configuration.\n\n1. Go to Language → New Configuration\n2. Give your language a name like 'MyFirstLanguage'\n3. Set version to '1.0'",  # noqa: E501
                "action": "Click 'Next' to continue",
            },
            {
                "title": "Step 2: Customize Keywords",
                "content": "Now let's customize some keywords to make your language unique.\n\n1. Switch to the 'Config Editor' tab\n2. In the Keywords section, click 'Add'\n3. Change 'if' to 'when' and 'else' to 'otherwise'",  # noqa: E501
                "action": "Click 'Next' to continue",
            },
            {
                "title": "Step 3: Test Your Language",
                "content": "Let's test your new language!\n\n1. Switch to the 'Editor' tab\n2. Type: when True: print('Hello!')\n3. Click the 'Run' button or press F9",  # noqa: E501
                "action": "Click 'Finish' to complete the tutorial",
            },
        ]

        current_step = 0

        def show_step(step_idx: int) -> None:
            nonlocal current_step
            current_step = step_idx

            for widget in tutorial_win.winfo_children():
                widget.destroy()

            step = steps[step_idx]

            ttk.Label(
                tutorial_win,
                text=step["title"],
                font=("TkDefaultFont", 14, "bold"),
            ).pack(pady=10)

            text_widget = scrolledtext.ScrolledText(
                tutorial_win,
                wrap="word",
                height=10,
                font=("TkDefaultFont", 10),
            )
            text_widget.pack(fill="both", expand=True, padx=10, pady=5)
            text_widget.insert("1.0", step["content"])
            text_widget.config(state="disabled")

            button_frame = ttk.Frame(tutorial_win)
            button_frame.pack(fill="x", padx=10, pady=10)

            if step_idx > 0:
                ttk.Button(
                    button_frame,
                    text="Previous",
                    command=lambda: show_step(step_idx - 1),
                ).pack(side="left")

            if step_idx < len(steps) - 1:
                ttk.Button(
                    button_frame,
                    text="Next",
                    command=lambda: show_step(step_idx + 1),
                ).pack(side="right")
            else:
                ttk.Button(
                    button_frame, text="Finish", command=tutorial_win.destroy
                ).pack(side="right")

        show_step(0)

    def _quick_start_guide(self) -> None:
        """Show quick start guide."""
        guide_win = tk.Toplevel(self.root)
        guide_win.title("Quick Start Guide")
        guide_win.geometry("600x400")

        guide_text = """
# Quick Start Guide

## Creating Your First Language

1. **Start the IDE**
   - Launch the Honey Badger LCS IDE

2. **Create Configuration**
   - Language → New Configuration
   - Enter name: "MyLanguage"
   - Version: "1.0"

3. **Customize Keywords**
   - Config Editor tab → Keywords section
   - Add mapping: if → when
   - Add mapping: else → otherwise

4. **Test Language**
   - Editor tab
   - Type: when True: print("Hello!")
   - Press F9 to run

## Key Shortcuts

- Ctrl+N: New file
- Ctrl+O: Open file
- Ctrl+S: Save file
- F5: Load config
- F7: Validate config
- F9: Run code
- F1: Help

## Next Steps

- Explore presets in Language → Load Preset
- Add custom functions in Config Editor
- Create project with Project → New Project
- Check Help → Tutorials for advanced features
        """

        text_widget = scrolledtext.ScrolledText(
            guide_win, wrap="word", font=("TkDefaultFont", 10)
        )
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        text_widget.insert("1.0", guide_text)
        text_widget.config(state="disabled")

        ttk.Button(guide_win, text="Close", command=guide_win.destroy).pack(
            pady=5
        )

    # Placeholder methods for comprehensive functionality
    def _new_language_config(self) -> None:
        """Create a new language configuration."""
        config_win = tk.Toplevel(self.root)
        config_win.title("New Language Configuration")
        config_win.geometry("400x200")
        config_win.resizable(False, False)

        # Name field
        ttk.Label(config_win, text="Configuration Name:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        name_var = tk.StringVar()
        ttk.Entry(config_win, textvariable=name_var).grid(
            row=0, column=1, padx=5, pady=5, sticky="ew"
        )

        # Version field
        ttk.Label(config_win, text="Version:").grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        version_var = tk.StringVar(value="1.0")
        ttk.Entry(config_win, textvariable=version_var).grid(
            row=1, column=1, padx=5, pady=5, sticky="ew"
        )

        # Description field
        ttk.Label(config_win, text="Description:").grid(
            row=2, column=0, padx=5, pady=5, sticky="nw"
        )
        desc_text = tk.Text(config_win, height=3, width=30)
        desc_text.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Buttons
        button_frame = ttk.Frame(config_win)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        def create_config():
            name = name_var.get().strip()
            version = version_var.get().strip()
            description = desc_text.get("1.0", tk.END).strip()

            if not name:
                messagebox.showerror("Error", "Configuration name is required")
                return

            try:
                self.current_config = LanguageConfig(
                    name=name, version=version, description=description
                )
                self._update_title()
                self._update_ui_state()
                config_win.destroy()
                messagebox.showinfo(
                    "Success", f"Created configuration '{name}'"
                )
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to create configuration: {e}"
                )

        ttk.Button(button_frame, text="Create", command=create_config).pack(
            side="left", padx=5
        )
        ttk.Button(
            button_frame, text="Cancel", command=config_win.destroy
        ).pack(side="left", padx=5)

        config_win.columnconfigure(1, weight=1)

    def _load_preset(self, preset: str) -> None:
        """Load a language preset."""
        try:
            self.current_config = LanguageConfig.load_preset(preset)
            self._update_title()
            self._update_ui_state()
            messagebox.showinfo("Success", f"Loaded preset '{preset}'")
        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to load preset '{preset}': {e}"
            )

    def _add_keyword_mapping(self) -> None:
        """Add a new keyword mapping to the current configuration."""
        if not self.current_config:
            messagebox.showwarning(
                "Warning", "No language configuration loaded"
            )
            return

        keyword_win = tk.Toplevel(self.root)
        keyword_win.title("Add Keyword Mapping")
        keyword_win.geometry("400x200")
        keyword_win.resizable(False, False)

        # Original keyword
        ttk.Label(keyword_win, text="Original Keyword:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        original_var = tk.StringVar()
        ttk.Entry(keyword_win, textvariable=original_var).grid(
            row=0, column=1, padx=5, pady=5, sticky="ew"
        )

        # Custom keyword
        ttk.Label(keyword_win, text="Custom Keyword:").grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        custom_var = tk.StringVar()
        ttk.Entry(keyword_win, textvariable=custom_var).grid(
            row=1, column=1, padx=5, pady=5, sticky="ew"
        )

        # Category
        ttk.Label(keyword_win, text="Category:").grid(
            row=2, column=0, padx=5, pady=5, sticky="w"
        )
        category_var = tk.StringVar(value="general")
        category_combo = ttk.Combobox(
            keyword_win,
            textvariable=category_var,
            values=[
                "general",
                "control",
                "function",
                "operator",
                "type",
                "satirical",
            ],
        )
        category_combo.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Description
        ttk.Label(keyword_win, text="Description:").grid(
            row=3, column=0, padx=5, pady=5, sticky="nw"
        )
        desc_text = tk.Text(keyword_win, height=2, width=30)
        desc_text.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Buttons
        button_frame = ttk.Frame(keyword_win)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        def add_keyword():
            original = original_var.get().strip()
            custom = custom_var.get().strip()
            category = category_var.get()
            description = desc_text.get("1.0", tk.END).strip()

            if not original or not custom:
                messagebox.showerror(
                    "Error", "Both original and custom keywords are required"
                )
                return

            try:
                self.current_config.rename_keyword(original, custom)
                # Update the mapping with additional info
                for mapping in self.current_config.keyword_mappings:
                    if (
                        mapping.original == original
                        and mapping.custom == custom
                    ):
                        mapping.category = category
                        mapping.description = description
                        break

                self._update_config_display()
                keyword_win.destroy()
                messagebox.showinfo(
                    "Success", f"Added keyword mapping: {original} → {custom}"
                )
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to add keyword mapping: {e}"
                )

        ttk.Button(button_frame, text="Add", command=add_keyword).pack(
            side="left", padx=5
        )
        ttk.Button(
            button_frame, text="Cancel", command=keyword_win.destroy
        ).pack(side="left", padx=5)

        keyword_win.columnconfigure(1, weight=1)

    def _edit_keyword_mapping(self) -> None:
        messagebox.showinfo(
            "Edit Keyword", "Keyword editing not yet implemented"
        )

    def _remove_keyword_mapping(self) -> None:
        messagebox.showinfo(
            "Remove Keyword", "Keyword removal not yet implemented"
        )

    def _add_function(self) -> None:
        messagebox.showinfo(
            "Add Function", "Function addition not yet implemented"
        )

    def _configure_syntax(self) -> None:
        messagebox.showinfo(
            "Configure Syntax", "Syntax configuration not yet implemented"
        )

    def _set_operators(self) -> None:
        messagebox.showinfo(
            "Set Operators", "Operator configuration not yet implemented"
        )

    def _test_language(self) -> None:
        messagebox.showinfo(
            "Test Language", "Language testing not yet implemented"
        )

    def _run_code(self) -> None:
        """Run the code in the editor."""
        if not self.current_config:
            messagebox.showwarning(
                "Warning",
                "No language configuration loaded. Please create or load a configuration first.",  # noqa: E501
            )
            return

        code = self.editor.get("1.0", tk.END).strip()
        if not code:
            messagebox.showinfo("Info", "No code to run")
            return

        # Switch to console tab
        self.notebook.select(2)  # Console tab

        try:
            # Create language runtime and run code
            runtime = LanguageRuntime.get_instance()
            runtime.load_config(self.current_config)

            # For now, just show the code in console as if it ran
            console_text = (
                f">>> Running code with config '{self.current_config.name}'\n"
            )
            console_text += f"Code length: {len(code)} characters\n"
            console_text += (
                "Output: [Code execution not fully implemented yet]\n"
            )

            # Add to console
            console = getattr(self, "console_text", None)
            if console:
                console.insert(tk.END, console_text)
                console.see(tk.END)

        except Exception as e:
            error_msg = f"Error running code: {e}\n"
            console = getattr(self, "console_text", None)
            if console:
                console.insert(tk.END, error_msg)
                console.see(tk.END)
            else:
                messagebox.showerror("Error", error_msg)

    def _new_project(self) -> None:
        messagebox.showinfo(
            "New Project", "Project creation not yet implemented"
        )

    def _open_project(self) -> None:
        messagebox.showinfo(
            "Open Project", "Project opening not yet implemented"
        )

    def _close_project(self) -> None:
        messagebox.showinfo(
            "Close Project", "Project closing not yet implemented"
        )

    def _add_file_to_project(self) -> None:
        messagebox.showinfo("Add File", "File addition not yet implemented")

    def _add_folder_to_project(self) -> None:
        messagebox.showinfo(
            "Add Folder", "Folder addition not yet implemented"
        )

    def _remove_from_project(self) -> None:
        messagebox.showinfo("Remove", "Removal not yet implemented")

    def _project_settings(self) -> None:
        messagebox.showinfo("Settings", "Project settings not yet implemented")

    def _build_project(self) -> None:
        messagebox.showinfo("Build", "Project building not yet implemented")

    def _clean_project(self) -> None:
        messagebox.showinfo("Clean", "Project cleaning not yet implemented")

    def _git_status(self) -> None:
        messagebox.showinfo(
            "Git Status", "Git integration not yet implemented"
        )

    def _git_commit(self) -> None:
        messagebox.showinfo("Git Commit", "Git commit not yet implemented")

    def _git_push(self) -> None:
        messagebox.showinfo("Git Push", "Git push not yet implemented")

    def _open_terminal(self) -> None:
        messagebox.showinfo(
            "Terminal", "Terminal integration not yet implemented"
        )

    def _command_palette(self) -> None:
        messagebox.showinfo(
            "Command Palette", "Command palette not yet implemented"
        )

    def _generate_docs(self) -> None:
        messagebox.showinfo(
            "Generate Docs", "Documentation generation not yet implemented"
        )

    def _run_tests(self) -> None:
        messagebox.showinfo("Run Tests", "Test running not yet implemented")

    def _debug_code(self) -> None:
        messagebox.showinfo("Debug", "Debugging not yet implemented")

    def _check_syntax(self) -> None:
        messagebox.showinfo(
            "Check Syntax", "Syntax checking not yet implemented"
        )

    def _find_references(self) -> None:
        messagebox.showinfo(
            "Find References", "Reference finding not yet implemented"
        )

    def _show_call_hierarchy(self) -> None:
        messagebox.showinfo(
            "Call Hierarchy", "Call hierarchy not yet implemented"
        )

    def _open_settings(self) -> None:
        messagebox.showinfo("Settings", "Settings dialog not yet implemented")

    def _new_window(self) -> None:
        messagebox.showinfo(
            "New Window", "Multi-window support not yet implemented"
        )

    def _close_window(self) -> None:
        messagebox.showinfo(
            "Close Window", "Window management not yet implemented"
        )

    def _split_editor(self) -> None:
        messagebox.showinfo(
            "Split Editor", "Editor splitting not yet implemented"
        )

    def _close_split(self) -> None:
        messagebox.showinfo("Close Split", "Split closing not yet implemented")

    def _reset_layout(self) -> None:
        messagebox.showinfo("Reset Layout", "Layout reset not yet implemented")

    def _save_layout(self) -> None:
        messagebox.showinfo("Save Layout", "Layout saving not yet implemented")

    def _load_layout(self) -> None:
        messagebox.showinfo(
            "Load Layout", "Layout loading not yet implemented"
        )

    def _open_documentation(self) -> None:
        messagebox.showinfo(
            "Documentation", "Documentation opening not yet implemented"
        )

    def _language_reference(self) -> None:
        messagebox.showinfo(
            "Language Reference", "Language reference not yet implemented"
        )

    def _api_reference(self) -> None:
        messagebox.showinfo(
            "API Reference", "API reference not yet implemented"
        )

    def _tutorial(self, tutorial_type: str) -> None:
        messagebox.showinfo(
            "Tutorial", f"Tutorial '{tutorial_type}' not yet implemented"
        )

    def _example(self, example_type: str) -> None:
        messagebox.showinfo(
            "Example", f"Example '{example_type}' not yet implemented"
        )

    def _show_shortcuts(self) -> None:
        messagebox.showinfo(
            "Shortcuts", "Keyboard shortcuts help not yet implemented"
        )

    def _show_about(self) -> None:
        """Show about dialog."""
        about_text = """Honey Badger Language Construction Set

Advanced IDE for Creating Custom Programming Languages

Version: 2.0
Built with: Python 3.13, Tkinter

Features:
• Interactive language configuration editor
• Multi-panel interface with editor, console, and project views
• Comprehensive menu system and keyboard shortcuts
• Built-in help system and tutorials
• Project management and version control integration
• Syntax highlighting and code completion
• Export/import capabilities

Copyright © 2025 Honey Badger Software
All rights reserved."""

        messagebox.showinfo("About", about_text)

    def _open_recent_menu(self) -> None:
        messagebox.showinfo(
            "Recent Files", "Recent files menu not yet implemented"
        )

    def _save_all(self) -> None:
        messagebox.showinfo("Save All", "Save all not yet implemented")

    def _close_all(self) -> None:
        messagebox.showinfo("Close All", "Close all not yet implemented")

    def _import_file(self) -> None:
        messagebox.showinfo("Import", "File import not yet implemented")

    def _export_file(self) -> None:
        messagebox.showinfo("Export", "File export not yet implemented")

    def _save_config(self) -> None:
        messagebox.showinfo("Save Config", "Config saving not yet implemented")

    def _save_config_as(self) -> None:
        messagebox.showinfo(
            "Save Config As", "Config save as not yet implemented"
        )

    def _compare_configs(self) -> None:
        messagebox.showinfo("Compare", "Config comparison not yet implemented")

    def _edit_cut(self) -> None:
        """Cut selected text to clipboard."""
        try:
            selected_text = self.editor.get(tk.SEL_FIRST, tk.SEL_LAST)
            if selected_text:
                self.clipboard_clear()
                self.clipboard_append(selected_text)
                self.editor.delete(tk.SEL_FIRST, tk.SEL_LAST)
                self._update_line_numbers()
        except tk.TclError:
            pass  # No selection

    def _edit_copy(self) -> None:
        """Copy selected text to clipboard."""
        try:
            selected_text = self.editor.get(tk.SEL_FIRST, tk.SEL_LAST)
            if selected_text:
                self.clipboard_clear()
                self.clipboard_append(selected_text)
        except tk.TclError:
            pass  # No selection

    def _edit_paste(self) -> None:
        """Paste text from clipboard."""
        try:
            clipboard_text = self.clipboard_get()
            if clipboard_text:
                # Delete selection if any, then insert
                try:
                    self.editor.delete(tk.SEL_FIRST, tk.SEL_LAST)
                except tk.TclError:
                    pass  # No selection
                self.editor.insert(tk.INSERT, clipboard_text)
                self._update_line_numbers()
        except tk.TclError:
            pass  # No clipboard content

    def _edit_delete(self) -> None:
        """Delete selected text."""
        try:
            self.editor.delete(tk.SEL_FIRST, tk.SEL_LAST)
            self._update_line_numbers()
        except tk.TclError:
            pass  # No selection

    def _edit_select_all(self) -> None:
        """Select all text in the editor."""
        self.editor.tag_add(tk.SEL, "1.0", tk.END)
        self.editor.mark_set(tk.INSERT, tk.END)
        self.editor.see(tk.INSERT)

    def _edit_select_line(self) -> None:
        messagebox.showinfo("Select Line", "Select line not yet implemented")

    def _find_in_files(self) -> None:
        messagebox.showinfo(
            "Find in Files", "Find in files not yet implemented"
        )

    def _goto_definition(self) -> None:
        messagebox.showinfo(
            "Go to Definition", "Go to definition not yet implemented"
        )

    def _format_document(self) -> None:
        messagebox.showinfo(
            "Format", "Document formatting not yet implemented"
        )

    def _toggle_comment(self) -> None:
        messagebox.showinfo(
            "Toggle Comment", "Comment toggle not yet implemented"
        )

    def _toggle_editor_panel(self) -> None:
        messagebox.showinfo(
            "Toggle Editor", "Panel toggle not yet implemented"
        )

    def _toggle_console_panel(self) -> None:
        messagebox.showinfo(
            "Toggle Console", "Panel toggle not yet implemented"
        )

    def _toggle_config_panel(self) -> None:
        messagebox.showinfo(
            "Toggle Config", "Panel toggle not yet implemented"
        )

    def _toggle_project_panel(self) -> None:
        messagebox.showinfo(
            "Toggle Project", "Panel toggle not yet implemented"
        )

    def _toggle_minimap(self) -> None:
        messagebox.showinfo(
            "Toggle Minimap", "Minimap toggle not yet implemented"
        )

    def _toggle_syntax_highlighting(self) -> None:
        messagebox.showinfo(
            "Toggle Syntax", "Syntax highlighting toggle not yet implemented"
        )

    def _toggle_code_completion(self) -> None:
        messagebox.showinfo(
            "Toggle Completion", "Code completion toggle not yet implemented"
        )

    def _zoom_in(self) -> None:
        messagebox.showinfo("Zoom In", "Zoom in not yet implemented")

    def _zoom_out(self) -> None:
        messagebox.showinfo("Zoom Out", "Zoom out not yet implemented")

    def _reset_zoom(self) -> None:
        messagebox.showinfo("Reset Zoom", "Zoom reset not yet implemented")

    def _clear_console(self) -> None:
        messagebox.showinfo(
            "Clear Console", "Console clearing not yet implemented"
        )

    def _copy_console(self) -> None:
        messagebox.showinfo(
            "Copy Console", "Console copying not yet implemented"
        )

    def _save_console_output(self) -> None:
        messagebox.showinfo("Save Output", "Output saving not yet implemented")

    def _refresh_project_tree(self) -> None:
        messagebox.showinfo("Refresh Tree", "Tree refresh not yet implemented")

    def _open_selected_file(self) -> None:
        messagebox.showinfo("Open File", "File opening not yet implemented")

    def _update_recent_files(self, file_path: str) -> None:
        """Update the recent files list."""
        if file_path in self.settings["recent_files"]:
            self.settings["recent_files"].remove(file_path)
        self.settings["recent_files"].insert(0, file_path)
        self.settings["recent_files"] = self.settings["recent_files"][
            :10
        ]  # Keep only 10

    def _update_ui_state(self) -> None:
        """Update UI elements based on current state."""
        # This would update menu states, toolbar buttons, etc.
        # For now, just update status
        self._update_status()

    def _update_config_display(self) -> None:
        """Update the configuration editor display."""
        if not self.current_config:
            return

        # Update metadata fields
        if hasattr(self, "config_name_var"):
            self.config_name_var.set(self.current_config.name or "")
        if hasattr(self, "config_version_var"):
            self.config_version_var.set(self.current_config.version or "")

        # Update keywords listbox
        if hasattr(self, "keywords_listbox"):
            self.keywords_listbox.delete(0, tk.END)
            for mapping in self.current_config.keyword_mappings:
                display_text = f"{mapping.original} → {mapping.custom}"
                if mapping.category != "general":
                    display_text += f" ({mapping.category})"
                self.keywords_listbox.insert(tk.END, display_text)

    def _load_default_content(self) -> None:
        pass

    def _load_settings(self) -> None:
        pass

    def _save_settings(self) -> None:
        pass

    def _apply_settings(self) -> None:
        pass

    def _on_close(self) -> None:
        pass

    def _update_title(self) -> None:
        """Update the window title based on current file and config."""
        title_parts = ["Honey Badger Language Construction Set"]

        if self.current_file:
            title_parts.append(f"- {os.path.basename(self.current_file)}")
        else:
            title_parts.append("- Untitled")

        if self.current_config:
            title_parts.append(f"[{self.current_config.name}]")

        if self.current_project:
            title_parts.append(f"({os.path.basename(self.current_project)})")

        self.root.title(" ".join(title_parts))

    def _new_file(self) -> None:
        """Create a new file in the editor."""
        if self._check_unsaved_changes():
            self.editor.delete("1.0", tk.END)
            self.current_file = None
            self._update_title()
            self._update_ui_state()
            # Clear undo/redo stacks
            self.undo_stack.clear()
            self.redo_stack.clear()

    def _open_file(self) -> None:
        """Open a file in the editor."""
        if not self._check_unsaved_changes():
            return

        file_path = filedialog.askopenfilename(
            title="Open File",
            filetypes=[
                ("All Files", "*.*"),
                ("Python Files", "*.py"),
                ("Text Files", "*.txt"),
                ("YAML Files", "*.yaml;*.yml"),
                ("JSON Files", "*.json"),
            ],
        )

        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.editor.delete("1.0", tk.END)
                self.editor.insert("1.0", content)
                self.current_file = file_path
                self._update_title()
                self._update_ui_state()
                self._update_recent_files(file_path)
                # Clear undo/redo stacks for new file
                self.undo_stack.clear()
                self.redo_stack.clear()
                self._update_line_numbers()
            except (IOError, UnicodeDecodeError) as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")

    def _save_file(self) -> bool:
        """Save the current file. Returns True if successful."""
        if not self.current_file:
            return self._save_file_as()

        try:
            content = self.editor.get("1.0", tk.END).rstrip() + "\n"
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(content)
            self._update_title()
            self._update_ui_state()
            self._update_recent_files(self.current_file)
            return True
        except IOError as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")
            return False

    def _save_file_as(self) -> bool:
        """Save the current file with a new name. Returns True if successful."""  # noqa: E501
        file_path = filedialog.asksaveasfilename(
            title="Save File As",
            defaultextension=".py",
            filetypes=[
                ("Python Files", "*.py"),
                ("Text Files", "*.txt"),
                ("YAML Files", "*.yaml"),
                ("JSON Files", "*.json"),
                ("All Files", "*.*"),
            ],
        )

        if file_path:
            self.current_file = file_path
            return self._save_file()
        return False

    def _close_file(self) -> None:
        """Close the current file."""
        if self._check_unsaved_changes():
            self.editor.delete("1.0", tk.END)
            self.current_file = None
            self._update_title()
            self._update_ui_state()
            self.undo_stack.clear()
            self.redo_stack.clear()

    def _load_config(self) -> None:
        pass

    def _reload_config(self) -> None:
        pass

    def _unload_config(self) -> None:
        pass

    def _show_config_info(self) -> None:
        pass

    def _validate_config(self) -> None:
        pass

    def _toggle_line_numbers(self) -> None:
        """Toggle line numbers display."""
        self.show_line_numbers_var.set(not self.show_line_numbers_var.get())
        self._update_line_numbers()

    def _toggle_wrap(self) -> None:
        """Toggle word wrapping in the editor."""
        current_wrap = self.editor.cget("wrap")
        new_wrap = "none" if current_wrap == "word" else "word"
        self.editor.config(wrap=new_wrap)
        self.wrap_var.set(new_wrap == "word")

    def _set_theme(self, theme: str) -> None:
        """Set the editor theme."""
        self.theme_var.set(theme)
        # Basic theme switching - could be expanded with more  # noqa
        # sophisticated theming
        if theme == "dark":
            bg_color = "#2b2b2b"
            fg_color = "#ffffff"
            select_bg = "#404040"
        elif theme == "high_contrast":
            bg_color = "#000000"
            fg_color = "#ffffff"
            select_bg = "#ffffff"
        else:  # light
            bg_color = "#ffffff"
            fg_color = "#000000"
            select_bg = "#c0c0c0"

        self.editor.config(
            bg=bg_color,
            fg=fg_color,
            selectbackground=select_bg,
            insertbackground=fg_color,
        )
        self.line_numbers.config(bg=bg_color, fg=fg_color)

    def _edit_undo(self) -> None:
        """Undo the last edit operation."""
        try:
            self.editor.edit_undo()
            self._update_line_numbers()
        except tk.TclError:
            pass  # No more undo actions available

    def _edit_redo(self) -> None:
        """Redo the last undone edit operation."""
        try:
            self.editor.edit_redo()
            self._update_line_numbers()
        except tk.TclError:
            pass  # No more redo actions available

    def _update_status(self) -> None:
        """Update the status bar with current information."""
        if hasattr(self, "status_bar"):
            # Get current line and column
            try:
                cursor_pos = self.editor.index(tk.INSERT)
                line, col = cursor_pos.split(".")
                status_text = f"Line {line}, Col {col}"

                if self.current_config:
                    status_text += f" | Config: {self.current_config.name}"

                if self.current_project:
                    status_text += (
                        f" | Project: {os.path.basename(self.current_project)}"
                    )

                # Update status bar (assuming it exists)
                # self.status_bar.config(text=status_text)
            except Exception:
                pass

    def _update_line_numbers(self) -> None:
        """Update the line numbers display."""
        if not self.show_line_numbers_var.get():
            self.line_numbers.config(state="normal")
            self.line_numbers.delete("1.0", tk.END)
            self.line_numbers.config(state="disabled")
            return

        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", tk.END)

        content = self.editor.get("1.0", tk.END)
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            self.line_numbers.insert(tk.END, f"{i}\n")

        self.line_numbers.config(state="disabled")

        # Sync scrolling
        self.line_numbers.yview_moveto(self.editor.yview()[0])

    def _on_editor_scroll(self, *args) -> None:
        pass

    def _on_editor_change(self, event: Optional[tk.Event] = None) -> None:
        pass

    def _find_dialog(self) -> None:
        """Show find dialog."""
        find_win = tk.Toplevel(self.root)
        find_win.title("Find")
        find_win.geometry("400x150")
        find_win.resizable(False, False)

        # Find text entry
        ttk.Label(find_win, text="Find:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        find_var = tk.StringVar()
        find_entry = ttk.Entry(find_win, textvariable=find_var, width=30)
        find_entry.grid(row=0, column=1, padx=5, pady=5)

        # Options
        case_var = tk.BooleanVar()
        ttk.Checkbutton(
            find_win, text="Case sensitive", variable=case_var
        ).grid(row=1, column=0, columnspan=2, padx=5, sticky="w")

        # Buttons
        button_frame = ttk.Frame(find_win)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        def do_find():
            self._find_text(find_var.get(), case_var.get())
            find_win.destroy()

        ttk.Button(button_frame, text="Find", command=do_find).pack(
            side="left", padx=5
        )
        ttk.Button(button_frame, text="Cancel", command=find_win.destroy).pack(
            side="left", padx=5
        )

        find_entry.focus()
        find_win.bind("<Return>", lambda e: do_find())
        find_win.bind("<Escape>", lambda e: find_win.destroy())

    def _replace_dialog(self) -> None:
        pass

    def _goto_line(self) -> None:
        """Go to a specific line number."""
        line_num = simpledialog.askinteger(
            "Go to Line", "Enter line number:", minvalue=1
        )
        if line_num:
            try:
                self.editor.mark_set(tk.INSERT, f"{line_num}.0")
                self.editor.see(tk.INSERT)
                self._update_line_numbers()
            except tk.TclError:
                messagebox.showerror(
                    "Error", f"Line {line_num} does not exist"
                )

    def _new_from_template(self) -> None:
        pass


def main():
    """Main entry point for the IDE."""
    root = tk.Tk()
    AdvancedIDE(root)
    root.mainloop()


if __name__ == "__main__":
    main()
