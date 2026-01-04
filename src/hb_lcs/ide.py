#!/usr/bin/env python3

"""
ParserCraft IDE - Language Construction Interface

A comprehensive graphical IDE for designing and testing custom programming languages
through configuration-driven development.

Features:
- Interactive visual configuration editor
- Multi-language preset templates (Python-like, JavaScript-like, Lisp-like, etc.)
- Syntax highlighting and code editor with line numbers
- Real-time configuration validation
- Multi-panel interface: editor, console, preview, and configuration panels
- Built-in help system and language design tutorials
- Project management for language configurations
- Configuration import/export (JSON, YAML)
- TeachScript integration and testing
- Live language testing environment
- Version control integration support
- Advanced language construction features

Usage:
    python -m hb_lcs.ide              # Launch the IDE
    python src/hb_lcs/ide.py          # Direct execution

See Also:
    - CodeEx IDE: For developing applications in custom languages
    - CLI Tools: parsercraft create, parsercraft edit, parsercraft validate
    - Documentation: docs/guides/CODEX_DEVELOPER_GUIDE.md
"""

import base64
import datetime as dt
import io
import json
import math
import os
import re
import textwrap
import time
import tkinter as tk
import uuid
import zipfile
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, simpledialog, ttk
from typing import Any, Callable, Dict, List, Optional

from .language_config import LanguageConfig, list_presets
from .language_runtime import LanguageRuntime


class AdvancedIDE(ttk.Frame):
    """Advanced IDE for Honey Badger Language Construction Set."""

    def __init__(self, master: Optional[tk.Misc] = None):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.root = tk.Tk() if master is None else master.winfo_toplevel()
        self.root.title("Honey Badger Language Construction Set - Advanced IDE v2.0")
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        # Initialize state
        self.current_file: Optional[str] = None
        self.current_config: Optional[LanguageConfig] = None
        self.current_project: Optional[str] = None
        self.search_history: List[str] = []
        self.clipboard_history: List[str] = []
        self.undo_stack: List[str] = []
        self.redo_stack: List[str] = []
        self.version_history: List[dict] = []
        self._version_lookup: Dict[str, dict] = {}
        self.intelligence_data: Dict[str, Any] = {}
        self.performance_history: List[dict] = []
        self.plugins: Dict[str, Any] = {"available": {}, "loaded": {}, "hooks": {}}
        self.web_routes: Dict[str, dict] = {}
        self.web_app_config: Dict[str, Any] = {}
        self.execution_config: Dict[str, Any] = {}
        self.debugger_state: Dict[str, Any] = {}
        self.community_registry: Optional[Dict[str, Any]] = None
        self._recent_share_payloads: List[str] = []
        self._recent_files: List[str] = []
        self._default_theme = {
            "Keywords": "#569cd6",
            "Strings": "#ce9178",
            "Comments": "#6a9955",
            "Numbers": "#b5cea8",
            "Functions": "#dcdcaa",
            "Operators": "#d4d4d4",
        }
        self.syntax_theme = dict(self._default_theme)
        self._color_history: List[str] = []

        # UI components initialised later in the build pipeline
        self.notebook: Optional[ttk.Notebook] = None
        self.line_num_frame: Optional[ttk.Frame] = None
        self.line_numbers: Optional[tk.Text] = None
        self.editor: Optional[tk.Text] = None
        self.minimap_frame: Optional[ttk.Frame] = None
        self.minimap: Optional[tk.Text] = None
        self.config_name_var: Optional[tk.StringVar] = None
        self.config_version_var: Optional[tk.StringVar] = None
        self.keywords_listbox: Optional[tk.Listbox] = None
        self.console: Optional[scrolledtext.ScrolledText] = None
        self.project_tree: Optional[ttk.Treeview] = None
        self.status_bar: Optional[ttk.Frame] = None
        self.status_label: Optional[ttk.Label] = None
        self.position_label: Optional[ttk.Label] = None
        self.language_label: Optional[ttk.Label] = None

        # Settings
        self.settings: dict[str, Any] = {
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
        new_menu.add_command(label="File", command=self._new_file, accelerator="Ctrl+N")
        new_menu.add_command(label="Project", command=self._new_project)
        new_menu.add_command(label="Language Config", command=self._new_language_config)
        new_menu.add_separator()
        new_menu.add_command(label="From Template...", command=self._new_from_template)

        file_menu.add_command(
            label="Open...", command=self._open_file, accelerator="Ctrl+O"
        )
        file_menu.add_command(label="Open Recent", command=self._open_recent_menu)

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
        edit_menu.add_command(label="Cut", command=self._edit_cut, accelerator="Ctrl+X")
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
        panels_menu.add_checkbutton(label="Editor", command=self._toggle_editor_panel)
        panels_menu.add_checkbutton(label="Console", command=self._toggle_console_panel)
        panels_menu.add_checkbutton(
            label="Config Editor", command=self._toggle_config_panel
        )
        panels_menu.add_checkbutton(
            label="Project Explorer", command=self._toggle_project_panel
        )
        panels_menu.add_checkbutton(label="Minimap", command=self._toggle_minimap)

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
        lang_menu.add_command(label="Unload Configuration", command=self._unload_config)

        lang_menu.add_separator()
        lang_menu.add_command(label="Save Configuration", command=self._save_config)
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
        features_menu.add_command(label="Add Function", command=self._add_function)
        features_menu.add_command(
            label="Configure Syntax", command=self._configure_syntax
        )
        features_menu.add_command(label="Set Operators", command=self._set_operators)

        lang_menu.add_separator()
        lang_menu.add_command(label="Test Language", command=self._test_language)
        lang_menu.add_command(
            label="Run Code", command=self._run_code, accelerator="F9"
        )

    def _create_project_menu(self, menubar: tk.Menu) -> None:
        """Create Project menu for project management."""
        project_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Project", menu=project_menu)

        project_menu.add_command(label="New Project", command=self._new_project)
        project_menu.add_command(label="Open Project...", command=self._open_project)
        project_menu.add_command(label="Close Project", command=self._close_project)

        project_menu.add_separator()
        project_menu.add_command(label="Add File", command=self._add_file_to_project)
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
        project_menu.add_command(label="Build Project", command=self._build_project)
        project_menu.add_command(label="Clean Project", command=self._clean_project)

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
        analysis_menu.add_command(label="Check Syntax", command=self._check_syntax)
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
        window_menu.add_command(label="Close Window", command=self._close_window)

        window_menu.add_separator()
        window_menu.add_command(label="Split Editor", command=self._split_editor)
        window_menu.add_command(label="Close Split", command=self._close_split)

        window_menu.add_separator()
        window_menu.add_command(label="Reset Layout", command=self._reset_layout)
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
        help_menu.add_command(label="Documentation", command=self._open_documentation)
        help_menu.add_command(
            label="Language Reference", command=self._language_reference
        )
        help_menu.add_command(label="API Reference", command=self._api_reference)

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

        ttk.Separator(toolbar, orient="vertical").pack(side="left", fill="y", padx=6)

        # Language operations
        ttk.Button(toolbar, text="Load Config", command=self._load_config).pack(
            side="left", padx=2
        )
        ttk.Button(toolbar, text="Validate", command=self._validate_config).pack(
            side="left", padx=2
        )
        ttk.Button(toolbar, text="Run", command=self._run_code).pack(
            side="left", padx=2
        )

        ttk.Separator(toolbar, orient="vertical").pack(side="left", fill="y", padx=6)

        # Edit operations
        ttk.Button(toolbar, text="Find", command=self._find_dialog).pack(
            side="left", padx=2
        )
        ttk.Button(toolbar, text="Replace", command=self._replace_dialog).pack(
            side="left", padx=2
        )

        ttk.Separator(toolbar, orient="vertical").pack(side="left", fill="y", padx=6)

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

        ttk.Button(keyword_buttons, text="Add", command=self._add_keyword_mapping).pack(
            fill="x", pady=2
        )
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

        ttk.Button(console_toolbar, text="Clear", command=self._clear_console).pack(
            side="left", padx=2
        )
        ttk.Button(console_toolbar, text="Copy", command=self._copy_console).pack(
            side="left", padx=2
        )
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
        ttk.Button(project_toolbar, text="Open", command=self._open_selected_file).pack(
            side="left", padx=2
        )

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
        ttk.Button(button_frame, text="Close", command=welcome_win.destroy).pack(
            side="right", padx=5
        )

    def _start_tutorial(self) -> None:
        """Start the interactive tutorial."""
        tutorial_win = tk.Toplevel(self.root)
        tutorial_win.title("Interactive Tutorial")
        tutorial_win.geometry("700x500")

        # Tutorial steps
        steps = [
            {
                "title": "Step 1: Create a New Language Configuration",
                "content": (
                    "Let's start by creating a new language configuration."
                    "\n\n1. Go to Language → New Configuration"
                    "\n2. Give your language a name like 'MyFirstLanguage'"
                    "\n3. Set version to '1.0'"
                ),
                "action": "Click 'Next' to continue",
            },
            {
                "title": "Step 2: Customize Keywords",
                "content": (
                    "Now let's customize some keywords to make your language unique."
                    "\n\n1. Switch to the 'Config Editor' tab"
                    "\n2. In the Keywords section, click 'Add'"
                    "\n3. Change 'if' to 'when' and 'else' to 'otherwise'"
                ),
                "action": "Click 'Next' to continue",
            },
            {
                "title": "Step 3: Test Your Language",
                "content": (
                    "Let's test your new language!"
                    "\n\n1. Switch to the 'Editor' tab"
                    "\n2. Type: when True: print('Hello!')"
                    "\n3. Click the 'Run' button or press F9"
                ),
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

        ttk.Button(guide_win, text="Close", command=guide_win.destroy).pack(pady=5)

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
                messagebox.showinfo("Success", f"Created configuration '{name}'")
            except Exception as e:  # noqa: BLE001  # pylint: disable=broad-except
                messagebox.showerror("Error", f"Failed to create configuration: {e}")

        ttk.Button(button_frame, text="Create", command=create_config).pack(
            side="left", padx=5
        )
        ttk.Button(button_frame, text="Cancel", command=config_win.destroy).pack(
            side="left", padx=5
        )

        config_win.columnconfigure(1, weight=1)

    def _load_preset(self, preset: str) -> None:
        """Load a language preset."""
        try:
            self.current_config = LanguageConfig.load_preset(preset)
            self._update_title()
            self._update_ui_state()
            messagebox.showinfo("Success", f"Loaded preset '{preset}'")
        except Exception as e:  # noqa: BLE001  # pylint: disable=broad-except
            messagebox.showerror("Error", f"Failed to load preset '{preset}': {e}")

    def _add_keyword_mapping(self) -> None:
        """Add a new keyword mapping to the current configuration."""
        if not self.current_config:
            messagebox.showwarning("Warning", "No language configuration loaded")
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
                    if mapping.original == original and mapping.custom == custom:
                        mapping.category = category
                        mapping.description = description
                        break

                self._update_config_display()
                keyword_win.destroy()
                messagebox.showinfo(
                    "Success", f"Added keyword mapping: {original} → {custom}"
                )
            except Exception as e:  # noqa: BLE001  # pylint: disable=broad-except
                messagebox.showerror("Error", f"Failed to add keyword mapping: {e}")

        ttk.Button(button_frame, text="Add", command=add_keyword).pack(
            side="left", padx=5
        )
        ttk.Button(button_frame, text="Cancel", command=keyword_win.destroy).pack(
            side="left", padx=5
        )

        keyword_win.columnconfigure(1, weight=1)

    def _edit_keyword_mapping(self) -> None:
        messagebox.showinfo("Edit Keyword", "Keyword editing not yet implemented")

    def _remove_keyword_mapping(self) -> None:
        messagebox.showinfo("Remove Keyword", "Keyword removal not yet implemented")

    def _add_function(self) -> None:
        messagebox.showinfo("Add Function", "Function addition not yet implemented")

    def _configure_syntax(self) -> None:
        messagebox.showinfo(
            "Configure Syntax", "Syntax configuration not yet implemented"
        )

    def _set_operators(self) -> None:
        messagebox.showinfo(
            "Set Operators", "Operator configuration not yet implemented"
        )

    def _test_language(self) -> None:
        messagebox.showinfo("Test Language", "Language testing not yet implemented")

    def _run_code(self) -> None:
        """Run the code in the editor."""
        if not self.current_config:
            messagebox.showwarning(
                "Warning",
                "No language configuration loaded. Please create or load a configuration first.",  # noqa: E501 pylint: disable=line-too-long
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
            console_text += "Output: [Code execution not fully implemented yet]\n"

            # Add to console
            console = getattr(self, "console_text", None)
            if console:
                console.insert(tk.END, console_text)
                console.see(tk.END)

        except Exception as e:  # noqa: BLE001  # pylint: disable=broad-except
            error_msg = f"Error running code: {e}\n"
            console = getattr(self, "console_text", None)
            if console:
                console.insert(tk.END, error_msg)
                console.see(tk.END)
            else:
                messagebox.showerror("Error", error_msg)

    def _new_project(self) -> None:
        messagebox.showinfo("New Project", "Project creation not yet implemented")

    def _open_project(self) -> None:
        messagebox.showinfo("Open Project", "Project opening not yet implemented")

    def _close_project(self) -> None:
        messagebox.showinfo("Close Project", "Project closing not yet implemented")

    def _add_file_to_project(self) -> None:
        messagebox.showinfo("Add File", "File addition not yet implemented")

    def _add_folder_to_project(self) -> None:
        messagebox.showinfo("Add Folder", "Folder addition not yet implemented")

    def _remove_from_project(self) -> None:
        messagebox.showinfo("Remove", "Removal not yet implemented")

    def _project_settings(self) -> None:
        messagebox.showinfo("Settings", "Project settings not yet implemented")

    def _build_project(self) -> None:
        messagebox.showinfo("Build", "Project building not yet implemented")

    def _clean_project(self) -> None:
        messagebox.showinfo("Clean", "Project cleaning not yet implemented")

    def _git_status(self) -> None:
        messagebox.showinfo("Git Status", "Git integration not yet implemented")

    def _git_commit(self) -> None:
        messagebox.showinfo("Git Commit", "Git commit not yet implemented")

    def _git_push(self) -> None:
        messagebox.showinfo("Git Push", "Git push not yet implemented")

    def _open_terminal(self) -> None:
        messagebox.showinfo("Terminal", "Terminal integration not yet implemented")

    def _command_palette(self) -> None:
        messagebox.showinfo("Command Palette", "Command palette not yet implemented")

    def _generate_docs(self) -> None:
        messagebox.showinfo(
            "Generate Docs", "Documentation generation not yet implemented"
        )

    def _run_tests(self) -> None:
        messagebox.showinfo("Run Tests", "Test running not yet implemented")

    def _debug_code(self) -> None:
        messagebox.showinfo("Debug", "Debugging not yet implemented")

    def _check_syntax(self) -> None:
        messagebox.showinfo("Check Syntax", "Syntax checking not yet implemented")

    def _find_references(self) -> None:
        messagebox.showinfo("Find References", "Reference finding not yet implemented")

    def _show_call_hierarchy(self) -> None:
        messagebox.showinfo("Call Hierarchy", "Call hierarchy not yet implemented")

    def _open_settings(self) -> None:
        messagebox.showinfo("Settings", "Settings dialog not yet implemented")

    def _new_window(self) -> None:
        messagebox.showinfo("New Window", "Multi-window support not yet implemented")

    def _close_window(self) -> None:
        messagebox.showinfo("Close Window", "Window management not yet implemented")

    def _split_editor(self) -> None:
        messagebox.showinfo("Split Editor", "Editor splitting not yet implemented")

    def _close_split(self) -> None:
        messagebox.showinfo("Close Split", "Split closing not yet implemented")

    def _reset_layout(self) -> None:
        messagebox.showinfo("Reset Layout", "Layout reset not yet implemented")

    def _save_layout(self) -> None:
        messagebox.showinfo("Save Layout", "Layout saving not yet implemented")

    def _load_layout(self) -> None:
        messagebox.showinfo("Load Layout", "Layout loading not yet implemented")

    def _open_documentation(self) -> None:
        messagebox.showinfo(
            "Documentation", "Documentation opening not yet implemented"
        )

    def _language_reference(self) -> None:
        messagebox.showinfo(
            "Language Reference", "Language reference not yet implemented"
        )

    def _api_reference(self) -> None:
        """Show comprehensive API reference documentation."""
        api_text = """HONEY BADGER LANGUAGE CONSTRUCTION SET - API REFERENCE

=== LANGUAGE CONFIGURATION ===

LanguageConfig class:
  • from_preset(preset_name) -> Create from template
  • add_keyword(name, replacement) -> Add keyword mapping
  • add_function(name, arity) -> Add function definition
  • add_operator(symbol, precedence) -> Add operator
  • rename_keyword(old, new) -> Rename keyword
  • to_dict() -> Export as dictionary
  • to_json() -> Export as JSON string
  • to_yaml() -> Export as YAML string
  • save(path) -> Save to file
  • load(path) -> Load from file

=== LANGUAGE RUNTIME ===

LanguageRuntime class:
  • execute(code, config) -> Execute code with config
  • translate_keyword(keyword) -> Translate to target lang
  • validate_syntax(code) -> Check syntax errors
  • get_globals() -> Get runtime globals
  • reset() -> Clear runtime state

=== IDE FEATURES ===

Menu Commands:
  • File: New, Open, Save, Export, Import
  • Edit: Cut, Copy, Paste, Select All, Undo, Redo
  • Language: Create, Edit, Validate, Export
  • Tools: Run Code, Check Syntax, Analyze, Profile
  • View: Dark/Light Theme, Reset Layout
  • Help: API Reference, Tutorials, Examples, Shortcuts

Keyboard Shortcuts:
  • Ctrl+N: New file
  • Ctrl+O: Open file
  • Ctrl+S: Save file
  • Ctrl+R: Run code
  • Ctrl+B: Check syntax
  • Ctrl+H: Show help
  • Ctrl+/: Toggle comment
  • Tab: Indent
  • Shift+Tab: Unindent

=== CODE EXECUTION ===

Functions:
  • print(message) -> Output text
  • input(prompt) -> Read user input
  • len(collection) -> Get length
  • range(start, end) -> Create sequence
  • enumerate(collection) -> Get indexed items
  • zip(*collections) -> Combine sequences
  • map(function, sequence) -> Apply function
  • filter(predicate, sequence) -> Filter items
  • sorted(sequence, [key]) -> Sort items
  • max/min(sequence) -> Find extrema
  • sum(sequence) -> Sum items
  • abs(number) -> Absolute value
  • round(number, [digits]) -> Round number
  • type(value) -> Get type name
  • isinstance(value, type) -> Check type
  • str(value) -> Convert to string
  • int(value) -> Convert to integer
  • float(value) -> Convert to float
  • list(sequence) -> Convert to list
  • dict(**kwargs) -> Create dictionary
  • tuple(sequence) -> Convert to tuple
  • set(sequence) -> Create set
"""

        # Create a scrolled text window for better readability
        top = tk.Toplevel(self.root)
        top.title("API Reference")
        top.geometry("800x600")

        text_widget = scrolledtext.ScrolledText(top, wrap="word", font=("Courier", 10))
        text_widget.pack(fill="both", expand=True, padx=5, pady=5)
        text_widget.insert("1.0", api_text)
        text_widget.config(state="disabled")

        # Add close button
        btn_frame = ttk.Frame(top)
        btn_frame.pack(fill="x", padx=5, pady=5)
        ttk.Button(btn_frame, text="Close", command=top.destroy).pack(side="right")

    def _tutorial(self, tutorial_type: str) -> None:
        """Show interactive tutorials."""
        tutorials = {
            "basics": self._tutorial_basics,
            "keywords": self._tutorial_keywords,
            "functions": self._tutorial_functions,
            "operators": self._tutorial_operators,
            "advanced": self._tutorial_advanced,
        }

        if tutorial_type in tutorials:
            tutorials[tutorial_type]()
        else:
            messagebox.showwarning(
                "Tutorial",
                f"Tutorial '{tutorial_type}' not found. "
                f"Available: {', '.join(tutorials.keys())}",
            )

    def _tutorial_basics(self) -> None:
        """Basics tutorial."""
        content = """TUTORIAL: LANGUAGE BASICS

1. CREATING A LANGUAGE
   Step 1: Go to Language → Create Language
   Step 2: Choose a preset (Python-like, JavaScript-like, etc.)
   Step 3: Configure keywords and operators
   Step 4: Save your language

2. UNDERSTANDING KEYWORDS
   Keywords are reserved words that have special meaning.
   Examples: if, while, for, function, return, etc.

   You can customize keywords to create a unique language!

3. UNDERSTANDING FUNCTIONS
   Functions are reusable blocks of code.
   Syntax: function_name(arg1, arg2) { ... }

   Built-in functions are always available.
   Custom functions are user-defined.

4. VARIABLES AND TYPES
   Variables store data values.
   Types: numbers, strings, lists, dictionaries

   Example: name = "Alice", age = 25

5. CONTROL FLOW
   Use if/else for conditions: if (x > 5) { ... }
   Use loops to repeat: for i in range(10) { ... }
   Use while for conditions: while (x < 10) { ... }

TRY IT: Create a language and write your first program!
"""
        self._show_tutorial_window("Basics Tutorial", content)

    def _tutorial_keywords(self) -> None:
        """Keywords tutorial."""
        content = """TUTORIAL: CUSTOMIZING KEYWORDS

Keywords are the syntax of your language. Customize them!

COMMON KEYWORDS:
  • if/else/elif - Conditional branching
  • while/for - Looping constructs
  • function/def/teach - Function definition
  • return/give_back - Return value
  • break/continue - Loop control
  • import/include - Import modules
  • try/catch - Error handling
  • class/type - Type definition
  • switch/case - Multi-branch selection
  • default/else - Default case

EXAMPLE CUSTOMIZATIONS:
  1. Programming languages:
     • Python: if, while, for, def, return
     • JavaScript: if, while, for, function, return
     • Ruby: if, while, for, def, return

  2. Domain-specific languages:
     • When instead of if
     • Teach instead of def
     • Give_back instead of return

  3. Natural language style:
     • Si instead of if
     • Mientras instead of while
     • Función instead of function

TO CUSTOMIZE:
  1. Open Language Editor
  2. Scroll to Keywords section
  3. Click Edit next to a keyword
  4. Enter your custom keyword
  5. Save language

TRY IT: Create a Spanish-like language!
"""
        self._show_tutorial_window("Keywords Tutorial", content)

    def _tutorial_functions(self) -> None:
        """Functions tutorial."""
        content = """TUTORIAL: WORKING WITH FUNCTIONS

Functions let you write reusable code blocks.

DEFINING FUNCTIONS:
  Syntax: function greet(name) {
            print("Hello, " + name)
          }

  Call: greet("Alice")
  Output: Hello, Alice

FUNCTION COMPONENTS:
  1. Name: greet
  2. Parameters: name
  3. Body: print("Hello, " + name)
  4. Return: (optional)

PARAMETERS vs ARGUMENTS:
  • Parameters: variables in function definition
    function add(a, b) { ... }

  • Arguments: values passed when calling
    add(5, 3)  <- 5 and 3 are arguments

RETURN VALUES:
  function add(a, b) {
    return a + b
  }

  result = add(5, 3)  # result = 8

SCOPE:
  • Local scope: variables inside function
  • Global scope: variables outside function
  • Functions can access global variables
  • Global variables can be modified with global keyword

RECURSION:
  Functions can call themselves!

  function factorial(n) {
    if (n <= 1) return 1
    return n * factorial(n - 1)
  }

ARROW FUNCTIONS:
  Modern syntax: square = (x) => x * x
  Traditional: function square(x) { return x * x }

TRY IT: Write a function that calculates Fibonacci numbers!
"""
        self._show_tutorial_window("Functions Tutorial", content)

    def _tutorial_operators(self) -> None:
        """Operators tutorial."""
        content = """TUTORIAL: OPERATORS AND EXPRESSIONS

Operators combine values into meaningful expressions.

ARITHMETIC OPERATORS:
  + : Addition       (5 + 3 = 8)
  - : Subtraction    (5 - 3 = 2)
  * : Multiplication (5 * 3 = 15)
  / : Division       (15 / 3 = 5)
  % : Modulo         (17 % 5 = 2)
  ** : Power         (2 ** 3 = 8)

COMPARISON OPERATORS:
  == : Equal         (5 == 5 = true)
  != : Not equal     (5 != 3 = true)
  > : Greater than   (5 > 3 = true)
  < : Less than      (5 < 3 = false)
  >= : Gte           (5 >= 5 = true)
  <= : Lte           (3 <= 5 = true)

LOGICAL OPERATORS:
  && : And           (true && true = true)
  || : Or            (true || false = true)
  ! : Not            (!true = false)

ASSIGNMENT OPERATORS:
  = : Assign         (x = 5)
  += : Add assign    (x += 3 means x = x + 3)
  -= : Sub assign    (x -= 3)
  *= : Mul assign    (x *= 3)
  /= : Div assign    (x /= 3)

STRING OPERATORS:
  + : Concatenate    ("Hello" + " " + "World")
  * : Repeat         ("Ha" * 3 = "HaHaHa")
  [] : Index         ("Hello"[0] = "H")
  [a:b] : Slice      ("Hello"[1:4] = "ell")

OPERATOR PRECEDENCE:
  1. ()              Parentheses
  2. **              Exponentiation
  3. *, /, %         Multiplication, Division, Modulo
  4. +, -            Addition, Subtraction
  5. <, >, <=, >=    Comparison
  6. ==, !=          Equality
  7. &&              Logical AND
  8. ||              Logical OR
  9. =               Assignment

TRY IT: Create expressions combining multiple operators!
"""
        self._show_tutorial_window("Operators Tutorial", content)

    def _tutorial_advanced(self) -> None:
        """Advanced tutorial."""
        content = """TUTORIAL: ADVANCED TECHNIQUES

Master advanced programming concepts!

DATA STRUCTURES:
  Lists (arrays):
    nums = [1, 2, 3, 4, 5]
    nums[0]      # First element = 1
    nums.append(6)  # Add element
    nums.pop()   # Remove last element

  Dictionaries (maps):
    person = {"name": "Alice", "age": 30}
    person["name"]  # Get value
    person["city"] = "NYC"  # Add field

OBJECT-ORIENTED:
  Classes define blueprints for objects:
    class Animal {
      constructor(name) { this.name = name }
      speak() { print(this.name + " makes sound") }
    }
    dog = new Animal("Dog")
    dog.speak()

FUNCTIONAL PROGRAMMING:
  Higher-order functions:
    map(square, [1, 2, 3, 4, 5])
    filter(isEven, [1, 2, 3, 4, 5])
    reduce(add, [1, 2, 3, 4, 5])

ERROR HANDLING:
  try {
    risky_operation()
  } catch (error) {
    print("Error: " + error)
  } finally {
    cleanup()
  }

MODULES & IMPORTS:
  import math from "stdlib"
  import { sqrt, sin } from "math"

  x = sqrt(16)  # = 4
  y = sin(0)    # = 0

ASYNC/AWAIT:
  async function fetchData() {
    data = await getFromAPI()
    return data
  }

LAMBDAS/ARROW FUNCTIONS:
  square = (x) => x * x
  add = (a, b) => a + b

  map((x) => x * 2, [1, 2, 3, 4, 5])

TRY IT: Build a small project using multiple concepts!
"""
        self._show_tutorial_window("Advanced Tutorial", content)

    def _show_tutorial_window(self, title: str, content: str) -> None:
        """Display tutorial in a new window."""
        top = tk.Toplevel(self.root)
        top.title(title)
        top.geometry("900x700")

        text_widget = scrolledtext.ScrolledText(top, wrap="word", font=("Courier", 11))
        text_widget.pack(fill="both", expand=True, padx=5, pady=5)
        text_widget.insert("1.0", content)
        text_widget.config(state="disabled")

        # Add close button
        btn_frame = ttk.Frame(top)
        btn_frame.pack(fill="x", padx=5, pady=5)
        ttk.Button(btn_frame, text="Close", command=top.destroy).pack(side="right")

    def _example(self, example_type: str) -> None:
        """Show practical code examples."""
        examples = {
            "hello_world": ("Hello World", 'print("Hello, World!")'),
            "variables": (
                "Variables & Types",
                """name = "Alice"
age = 30
height = 5.7
is_student = true

print(name)
print(age)
print(height)
print(is_student)""",
            ),
            "conditionals": (
                "Conditionals (If/Else)",
                """x = 15

if (x > 20) {
  print("x is greater than 20")
} else if (x > 10) {
  print("x is between 10 and 20")
} else {
  print("x is 10 or less")
}""",
            ),
            "loops": (
                "Loops (For/While)",
                """# For loop
for i in range(5) {
  print(i)
}

# While loop
x = 0
while (x < 5) {
  print(x)
  x = x + 1
}""",
            ),
            "functions": (
                "Functions",
                """function greet(name) {
  return "Hello, " + name
}

function add(a, b) {
  return a + b
}

print(greet("Alice"))
print(add(5, 3))""",
            ),
            "lists": (
                "Lists/Arrays",
                """numbers = [1, 2, 3, 4, 5]
names = ["Alice", "Bob", "Charlie"]

# Access elements
print(numbers[0])  # 1

# List operations
numbers.append(6)
numbers.pop()
length = len(numbers)

# Loop through
for num in numbers {
  print(num)
}""",
            ),
            "dictionaries": (
                "Dictionaries/Objects",
                """person = {
  "name": "Alice",
  "age": 30,
  "city": "NYC"
}

# Access values
print(person["name"])

# Modify
person["job"] = "Engineer"

# Loop through
for key in person.keys() {
  print(key + ": " + person[key])
}""",
            ),
            "recursion": (
                "Recursion",
                """function factorial(n) {
  if (n <= 1) {
    return 1
  }
  return n * factorial(n - 1)
}

print(factorial(5))  # 120""",
            ),
        }

        if example_type in examples:
            title, code = examples[example_type]
            self._show_example_window(title, code)
        else:
            available = ", ".join(examples.keys())
            messagebox.showwarning(
                "Example",
                f"Example '{example_type}' not found.\n" f"Available: {available}",
            )

    def _show_example_window(self, title: str, code: str) -> None:
        """Display example code in a new window."""
        top = tk.Toplevel(self.root)
        top.title(f"Example: {title}")
        top.geometry("700x500")

        # Code area
        text_widget = scrolledtext.ScrolledText(
            top, wrap="word", font=("Courier", 10), height=15
        )
        text_widget.pack(fill="both", expand=True, padx=5, pady=5)
        text_widget.insert("1.0", code)
        text_widget.config(state="disabled")

        # Buttons
        btn_frame = ttk.Frame(top)
        btn_frame.pack(fill="x", padx=5, pady=5)

        def copy_code():
            self.root.clipboard_clear()
            self.root.clipboard_append(code)
            messagebox.showinfo("Success", "Code copied to clipboard!")

        ttk.Button(btn_frame, text="Copy", command=copy_code).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Close", command=top.destroy).pack(
            side="right", padx=2
        )

    def _show_shortcuts(self) -> None:
        """Show comprehensive keyboard shortcuts help."""
        shortcuts_text = """KEYBOARD SHORTCUTS - HONEY BADGER IDE

=== FILE OPERATIONS ===
Ctrl+N    : New file
Ctrl+O    : Open file
Ctrl+S    : Save file
Ctrl+Shift+S : Save as
Ctrl+W    : Close file
Ctrl+Q    : Quit application

=== EDITING ===
Ctrl+X    : Cut
Ctrl+C    : Copy
Ctrl+V    : Paste
Ctrl+A    : Select all
Ctrl+Z    : Undo
Ctrl+Y    : Redo
Ctrl+/    : Toggle comment
Tab       : Indent
Shift+Tab : Unindent
Ctrl+L    : Select line

=== CODE EXECUTION ===
Ctrl+R    : Run code
Ctrl+Shift+R : Run with arguments
Ctrl+B    : Check syntax
Ctrl+E    : Export code
Ctrl+I    : Import code

=== VIEW & INTERFACE ===
Ctrl+H    : Toggle highlight
Ctrl+T    : Toggle theme (light/dark)
Ctrl+F    : Find
Ctrl+G    : Go to line
Alt+1     : Focus editor
Alt+2     : Focus console
Alt+3     : Focus config

=== LANGUAGE OPERATIONS ===
Ctrl+Alt+N : Create new language
Ctrl+Alt+E : Edit language
Ctrl+Alt+V : Validate language
Ctrl+Alt+S : Export language
Ctrl+Alt+L : Load language

=== HELP & DOCUMENTATION ===
F1        : Show API reference
F2        : Show tutorials
F3        : Show examples
F4        : Show this shortcuts list
F5        : Show about dialog

=== NAVIGATION ===
Ctrl+Home : Go to start of file
Ctrl+End  : Go to end of file
Ctrl+↑    : Move to previous error
Ctrl+↓    : Move to next error
Ctrl+F    : Find text
Ctrl+H    : Find and replace

=== DEBUG MODE ===
F6        : Start debugger
F7        : Step into
F8        : Step over
F9        : Continue
F10       : Stop debugger
Shift+F9  : Set breakpoint

=== TIPS ===
• Press Alt to access menu items
• Use Ctrl combinations for quick access
• Customize shortcuts in Settings menu
• Mouse wheel to zoom in/out
• Drag panels to resize layout
"""

        top = tk.Toplevel(self.root)
        top.title("Keyboard Shortcuts")
        top.geometry("800x700")

        text_widget = scrolledtext.ScrolledText(top, wrap="word", font=("Courier", 10))
        text_widget.pack(fill="both", expand=True, padx=5, pady=5)
        text_widget.insert("1.0", shortcuts_text)
        text_widget.config(state="disabled")

        # Add buttons
        btn_frame = ttk.Frame(top)
        btn_frame.pack(fill="x", padx=5, pady=5)
        ttk.Button(btn_frame, text="Close", command=top.destroy).pack(side="right")

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
        """Open recent files menu."""
        # Get recent files from config if available
        recent_files = getattr(self, "_recent_files", [])

        if not recent_files:
            messagebox.showinfo(
                "Recent Files", "No recent files found.\n\nOpen some files first!"
            )
            return

        # Create popup menu
        popup = tk.Menu(self.root, tearoff=0)

        for filepath in recent_files[-5:]:  # Last 5 files
            popup.add_command(
                label=Path(filepath).name,
                command=lambda f=filepath: self._open_file_direct(f),
            )

        popup.add_separator()
        popup.add_command(label="Clear Recent", command=self._clear_recent_files)

        # Display popup at mouse position
        popup.post(self.root.winfo_pointerx(), self.root.winfo_pointery())

    def _open_file_direct(self, filepath: str) -> None:
        """Open a file directly by path."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            self.input_text.config(state="normal")
            self.input_text.delete("1.0", "end")
            self.input_text.insert("1.0", content)
            self.input_text.config(state="normal")
            messagebox.showinfo("Success", f"Opened: {Path(filepath).name}")
        except (OSError, IOError, UnicodeDecodeError) as e:
            messagebox.showerror("Error", f"Failed to open file:\n{e}")

    def _clear_recent_files(self) -> None:
        """Clear recent files list."""
        self._recent_files = []
        messagebox.showinfo("Success", "Recent files cleared!")

    def _save_all(self) -> None:
        """Save all open files and configurations."""
        saved_count = 0

        try:
            # Save current code if it exists
            if hasattr(self, "input_text"):
                code_content = self.input_text.get("1.0", "end-1c")
                if code_content:
                    default_path = "current_code.txt"
                    filepath = filedialog.asksaveasfilename(
                        initialfile=default_path,
                        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                    )
                    if filepath:
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(code_content)
                        saved_count += 1

            # Save current language configuration if it exists
            if hasattr(self, "current_config") and self.current_config:
                config_path = filedialog.asksaveasfilename(
                    initialfile="language_config.json",
                    filetypes=[
                        ("JSON files", "*.json"),
                        ("YAML files", "*.yaml"),
                        ("All files", "*.*"),
                    ],
                )
                if config_path:
                    self.current_config.save(config_path)
                    saved_count += 1

            if saved_count > 0:
                messagebox.showinfo(
                    "Success", f"Saved {saved_count} item(s) successfully!"
                )
            else:
                messagebox.showinfo("Info", "Nothing to save")

        except (OSError, IOError, ValueError) as e:
            messagebox.showerror("Error", f"Failed to save:\n{e}")

    def _close_all(self) -> None:
        """Close all open files and reset the IDE."""
        if messagebox.askyesno("Confirm", "Close all files and reset IDE?"):
            try:
                # Clear editor
                if hasattr(self, "input_text"):
                    self.input_text.config(state="normal")
                    self.input_text.delete("1.0", "end")
                    self.input_text.config(state="normal")

                # Clear console
                if hasattr(self, "console_output"):
                    self.console_output.config(state="normal")
                    self.console_output.delete("1.0", "end")
                    self.console_output.config(state="disabled")

                # Reset configuration
                self.current_config = None

                # Clear recent files
                self._recent_files = []

                messagebox.showinfo("Success", "All files closed and IDE reset!")

            except (OSError, IOError, AttributeError) as e:
                messagebox.showerror("Error", f"Failed to close all:\n{e}")

    def _import_file(self) -> None:
        messagebox.showinfo("Import", "File import not yet implemented")

    def _export_file(self) -> None:
        messagebox.showinfo("Export", "File export not yet implemented")

    def _save_config(self) -> None:
        messagebox.showinfo("Save Config", "Config saving not yet implemented")

    def _save_config_as(self) -> None:
        messagebox.showinfo("Save Config As", "Config save as not yet implemented")

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
        messagebox.showinfo("Find in Files", "Find in files not yet implemented")

    def _goto_definition(self) -> None:
        messagebox.showinfo("Go to Definition", "Go to definition not yet implemented")

    def _format_document(self) -> None:
        messagebox.showinfo("Format", "Document formatting not yet implemented")

    def _toggle_comment(self) -> None:
        messagebox.showinfo("Toggle Comment", "Comment toggle not yet implemented")

    def _toggle_editor_panel(self) -> None:
        messagebox.showinfo("Toggle Editor", "Panel toggle not yet implemented")

    def _toggle_console_panel(self) -> None:
        messagebox.showinfo("Toggle Console", "Panel toggle not yet implemented")

    def _toggle_config_panel(self) -> None:
        messagebox.showinfo("Toggle Config", "Panel toggle not yet implemented")

    def _toggle_project_panel(self) -> None:
        messagebox.showinfo("Toggle Project", "Panel toggle not yet implemented")

    def _toggle_minimap(self) -> None:
        messagebox.showinfo("Toggle Minimap", "Minimap toggle not yet implemented")

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
        messagebox.showinfo("Clear Console", "Console clearing not yet implemented")

    def _copy_console(self) -> None:
        messagebox.showinfo("Copy Console", "Console copying not yet implemented")

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

    def _check_unsaved_changes(self) -> bool:
        """Prompt the user if unsaved editor content exists."""
        editor = getattr(self, "editor", None)
        if editor is None:
            return True

        try:
            modified = bool(editor.edit_modified())
        except tk.TclError:
            return True

        if not modified:
            return True

        if self.settings.get("auto_save"):
            if self._save_file():
                editor.edit_modified(False)
                return True
            return False

        response = messagebox.askyesnocancel(
            "Unsaved Changes",
            "You have unsaved changes. Save before continuing?",
        )
        if response is None:
            return False
        if response:
            saved = self._save_file()
            if saved:
                editor.edit_modified(False)
            return saved

        editor.edit_modified(False)
        return True

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
            except Exception:  # noqa: BLE001  # pylint: disable=broad-except
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

        for line_number in range(1, len(lines) + 1):
            self.line_numbers.insert(tk.END, f"{line_number}\n")

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
        ttk.Checkbutton(find_win, text="Case sensitive", variable=case_var).grid(
            row=1, column=0, columnspan=2, padx=5, sticky="w"
        )

        # Buttons
        button_frame = ttk.Frame(find_win)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        def do_find():
            self._find_text(find_var.get(), case_var.get())
            find_win.destroy()

        ttk.Button(button_frame, text="Find", command=do_find).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=find_win.destroy).pack(
            side="left", padx=5
        )

        find_entry.focus()
        find_win.bind("<Return>", lambda e: do_find())
        find_win.bind("<Escape>", lambda e: find_win.destroy())

    def _find_text(self, query: str, case_sensitive: bool) -> None:
        """Highlight matches of *query* in the editor."""
        editor = getattr(self, "editor", None)
        if editor is None or not query:
            return

        editor.tag_remove("find_match", "1.0", tk.END)
        search_kwargs = {"nocase": not case_sensitive}
        start_index = "1.0"
        first_match = None

        while True:
            match_index = editor.search(
                query, start_index, stopindex=tk.END, **search_kwargs
            )
            if not match_index:
                break

            end_index = f"{match_index}+{len(query)}c"
            editor.tag_add("find_match", match_index, end_index)
            if first_match is None:
                first_match = match_index
            start_index = end_index

        editor.tag_configure(
            "find_match",
            background="#ffd54f",
            foreground="#000000",
        )

        if first_match:
            editor.tag_remove(tk.SEL, "1.0", tk.END)
            selection_end = f"{first_match}+{len(query)}c"
            editor.tag_add(tk.SEL, first_match, selection_end)
            editor.mark_set(tk.INSERT, selection_end)
            editor.see(first_match)

        if query and query not in self.search_history:
            self.search_history.insert(0, query)
            self.search_history = self.search_history[:25]

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
                messagebox.showerror("Error", f"Line {line_num} does not exist")

    def _new_from_template(self) -> None:
        pass

    def _parse_description_to_config(self, description: str) -> str:
        """Create a configuration JSON from a natural language description."""
        normalized = (description or "").lower()

        keywords = {
            "IF": {
                "original": "if",
                "custom": "if",
                "category": "control",
            },
            "ELSE": {
                "original": "else",
                "custom": "else",
                "category": "control",
            },
            "WHILE": {
                "original": "while",
                "custom": "while",
                "category": "control",
            },
            "FOR": {
                "original": "for",
                "custom": "for",
                "category": "control",
            },
            "PRINT": {
                "original": "print",
                "custom": "print",
                "category": "io",
            },
            "FUNCTION": {
                "original": "function",
                "custom": "function",
                "category": "declaration",
            },
        }

        if "spanish" in normalized:
            keywords["IF"]["custom"] = "si"
            keywords["ELSE"]["custom"] = "sino"
            keywords["WHILE"]["custom"] = "mientras"
            keywords["FOR"]["custom"] = "para"
            keywords["PRINT"]["custom"] = "imprimir"

        if "verbose" in normalized:
            keywords["IF"]["custom"] = "if_condition"
            keywords["ELSE"]["custom"] = "otherwise"
            keywords["WHILE"]["custom"] = "while_loop"
            keywords["PRINT"]["custom"] = "display_value"

        if "minimal" in normalized:
            keywords["IF"]["custom"] = "i"
            keywords["ELSE"]["custom"] = "e"
            keywords["WHILE"]["custom"] = "w"
            keywords["FOR"]["custom"] = "f"
            keywords["PRINT"]["custom"] = "p"

        array_start = 0
        if "1-based" in normalized or "one-based" in normalized:
            array_start = 1
        if "0-based" in normalized or "zero-based" in normalized:
            array_start = 0

        canonical = {
            "if": "IF",
            "else": "ELSE",
            "while": "WHILE",
            "loop": "WHILE",
            "for": "FOR",
            "print": "PRINT",
            "display": "PRINT",
            "function": "FUNCTION",
        }

        pattern = re.compile(
            r"(?:use|set)\s*['\"]([^'\"]+)['\"]\s*for\s*([a-z_ ]+)",
            re.IGNORECASE,
        )
        for match in pattern.finditer(description or ""):
            custom_value = match.group(1).strip()
            target = match.group(2).strip().lower()
            target_key = canonical.get(target)
            if target_key and custom_value:
                keywords[target_key]["custom"] = custom_value

        metadata_name = "Generated Language"
        if "spanish" in normalized:
            metadata_name = "Spanish Variant"
        elif "minimal" in normalized:
            metadata_name = "Minimal Variant"
        elif "verbose" in normalized:
            metadata_name = "Verbose Variant"

        builtin_functions = {
            "print": {
                "name": "print",
                "arity": -1,
                "implementation": "builtin.print",
                "description": "Display output",
                "enabled": True,
            },
            "input": {
                "name": "input",
                "arity": 1,
                "implementation": "builtin.input",
                "description": "Read user input",
                "enabled": True,
            },
        }

        syntax_options = {
            "array_start_index": array_start,
            "single_line_comment": "#",
            "statement_terminator": "",
        }

        operators = {
            "+": {
                "symbol": "+",
                "precedence": 10,
                "associativity": "left",
                "enabled": True,
            },
            "-": {
                "symbol": "-",
                "precedence": 10,
                "associativity": "left",
                "enabled": True,
            },
            "*": {
                "symbol": "*",
                "precedence": 20,
                "associativity": "left",
                "enabled": True,
            },
            "/": {
                "symbol": "/",
                "precedence": 20,
                "associativity": "left",
                "enabled": True,
            },
            "==": {
                "symbol": "==",
                "precedence": 5,
                "associativity": "none",
                "enabled": True,
            },
        }

        config_dict = {
            "metadata": {
                "name": metadata_name,
                "version": "1.0.0",
                "description": (description.strip() if description else metadata_name),
                "author": "Auto Generator",
            },
            "keywords": keywords,
            "builtin_functions": builtin_functions,
            "functions": builtin_functions,
            "syntax_options": syntax_options,
            "operators": operators,
            "runtime": {"debug_mode": False, "strict_mode": True},
        }

        return json.dumps(config_dict, indent=2)

    def _normalize_config_snapshot(self, value: Any) -> dict:
        """Return a configuration dictionary from various inputs."""
        if isinstance(value, LanguageConfig):
            return value.to_dict()
        if isinstance(value, dict):
            if "config" in value and isinstance(value["config"], dict):
                return value["config"]
            return value
        return {}

    def _language_version_manager(self) -> dict:
        """Summarize current version history information."""
        if not self.current_config:
            return {"status": "no-config", "history_size": len(self.version_history)}
        if not self.version_history:
            self._save_version("Initial snapshot")
        recent = [
            {
                "id": entry["id"],
                "version": entry["version"],
                "timestamp": entry["timestamp"],
                "note": entry.get("note", ""),
            }
            for entry in self.version_history[-5:]
        ]
        return {
            "status": "ready",
            "current_version": self.current_config.version,
            "history_size": len(self.version_history),
            "recent_versions": recent,
        }

    def _save_version(self, note: str = "", extra: Optional[dict] = None) -> dict:
        """Persist the active configuration into the version history."""
        if not self.current_config:
            return {"status": "error", "reason": "No configuration loaded"}
        snapshot = self.current_config.to_dict()
        entry_id = f"ver-{uuid.uuid4().hex[:8]}"
        record = {
            "id": entry_id,
            "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "version": self.current_config.version,
            "note": note,
            "config": snapshot,
        }
        if extra:
            record["extra"] = dict(extra)
        self.version_history.append(record)
        self._version_lookup[entry_id] = record
        return record

    def _compare_versions(self, base: Any, other: Any) -> dict:
        """Compute a shallow diff between two configuration snapshots."""
        base_dict = self._normalize_config_snapshot(base)
        other_dict = self._normalize_config_snapshot(other)
        if not base_dict or not other_dict:
            return {"status": "error", "reason": "invalid-input"}

        base_meta = base_dict.get("metadata", {})
        other_meta = other_dict.get("metadata", {})
        metadata_diff = {}
        for key in ("name", "version", "description", "author"):
            if base_meta.get(key) != other_meta.get(key):
                metadata_diff[key] = {
                    "from": base_meta.get(key),
                    "to": other_meta.get(key),
                }

        base_keywords = base_dict.get("keywords", {})
        other_keywords = other_dict.get("keywords", {})
        added = sorted(set(other_keywords) - set(base_keywords))
        removed = sorted(set(base_keywords) - set(other_keywords))
        modified = sorted(
            key
            for key in set(base_keywords).intersection(other_keywords)
            if base_keywords[key] != other_keywords[key]
        )

        return {
            "status": "ok",
            "metadata_changes": metadata_diff,
            "added_keywords": added,
            "removed_keywords": removed,
            "modified_keywords": modified,
        }

    def _perform_version_merge(
        self, base: Optional[Any], incoming: Any, prefer_incoming: bool = True
    ) -> LanguageConfig:
        """Merge two configuration inputs and apply the result."""

        base_dict = self._normalize_config_snapshot(base) if base else {}
        incoming_dict = self._normalize_config_snapshot(incoming)

        if base_dict:
            target = LanguageConfig.from_dict(base_dict)
        elif self.current_config:
            target = self.current_config.clone()
        else:
            target = LanguageConfig()

        if incoming_dict:
            incoming_config = LanguageConfig.from_dict(incoming_dict)
            target.merge(incoming_config, prefer_other=prefer_incoming)

        self.current_config = target
        return target

    def _bulk_keyword_editor(
        self,
        operation: str = "prefix",
        value: str = "",
        keywords: Optional[List[str]] = None,
    ) -> dict:
        """Apply a bulk keyword modification operation."""

        if not self.current_config:
            return {"status": "no-config", "updated": 0, "changes": []}

        changes = self._apply_bulk_operation(operation, value, keywords)
        return {"status": "ok", "updated": len(changes), "changes": changes}

    def _invert_listbox_selection(self, listbox: tk.Listbox) -> int:
        """Invert the selection inside a Tk listbox widget."""

        if not listbox:
            return 0

        selected = 0
        for index in range(listbox.size()):
            if listbox.selection_includes(index):
                listbox.selection_clear(index)
            else:
                listbox.selection_set(index)
                selected += 1
        return selected

    def _apply_bulk_operation(
        self, operation: str, value: str = "", keywords: Optional[List[str]] = None
    ) -> List[dict]:
        """Execute a single bulk operation and return change details."""

        if not self.current_config:
            return []

        mappings = self.current_config.keyword_mappings
        targets = keywords or list(mappings.keys())
        results: List[dict] = []
        replacement: tuple[str, str] = tuple()
        if operation == "replace" and isinstance(value, str):
            parts = value.split("->", 1)
            if len(parts) == 2:
                replacement = (parts[0].strip(), parts[1].strip())

        for key in targets:
            if key not in mappings:
                continue

            mapping = mappings[key]
            original_value = mapping.custom

            if operation == "prefix":
                mapping.custom = f"{value}{original_value}"
            elif operation == "suffix":
                mapping.custom = f"{original_value}{value}"
            elif operation == "upper":
                mapping.custom = original_value.upper()
            elif operation == "lower":
                mapping.custom = original_value.lower()
            elif operation == "title":
                mapping.custom = original_value.title()
            elif operation == "replace" and replacement:
                mapping.custom = original_value.replace(*replacement)
            elif operation == "reset":
                mapping.custom = mapping.original

            results.append(
                {"keyword": key, "before": original_value, "after": mapping.custom}
            )

        return results

    def _export_language_package(
        self,
        output_dir: str,
        include_examples: bool = True,
        package_name: Optional[str] = None,
    ) -> str:
        """Create a distributable language package and return the archive path."""

        if not self.current_config:
            raise ValueError("No configuration loaded.")

        base_path = Path(output_dir).expanduser().resolve()
        base_path.mkdir(parents=True, exist_ok=True)

        package_name = (
            package_name or self.current_config.name.replace(" ", "_") or "Language"
        )
        version = self.current_config.version or "1.0.0"
        package_dir = base_path / f"{package_name}-{version}"
        package_dir.mkdir(parents=True, exist_ok=True)

        config_path = package_dir / "language.json"
        config_path.write_text(
            json.dumps(self.current_config.to_dict(), indent=2),
            encoding="utf-8",
        )

        readme_path = package_dir / "README.md"
        if not readme_path.exists():
            readme_text = textwrap.dedent(
                f"""
                # {self.current_config.name}

                Version: {version}

                Generated by the Honey Badger Language Construction Set.
                """
            ).strip()
            readme_path.write_text(readme_text + "\n", encoding="utf-8")

        if include_examples:
            examples_dir = package_dir / "examples"
            examples_dir.mkdir(exist_ok=True)
            examples_dir.joinpath("hello.txt").write_text(
                "print('Hello, World!')\n",
                encoding="utf-8",
            )

        zip_path = base_path / f"{package_name}-{version}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
            for path in package_dir.rglob("*"):
                if path.is_file():
                    archive.write(path, path.relative_to(base_path))

        return str(zip_path)

    def _browse_output_dir(self, initial_dir: Optional[str] = None) -> Optional[str]:
        """Prompt the user for an export directory."""

        return filedialog.askdirectory(initialdir=initial_dir or os.getcwd())

    def _perform_package_export(
        self, output_dir: str, package_name: Optional[str] = None
    ) -> dict:
        """Create a package and return a summary of the export."""

        try:
            archive = self._export_language_package(
                output_dir,
                package_name=package_name,
            )
        except Exception as exc:  # noqa: BLE001  # pylint: disable=broad-except
            return {"status": "error", "reason": str(exc)}

        summary = {
            "status": "ok",
            "archive": archive,
            "size": os.path.getsize(archive) if os.path.exists(archive) else 0,
        }
        self._recent_share_payloads.append(archive)
        return summary

    def _live_syntax_highlighter(self) -> dict:
        """Return syntax highlighting settings with sample content."""

        sample = self._generate_sample_code()
        return {"status": "ready", "colors": dict(self.syntax_theme), "sample": sample}

    def _generate_sample_code(self) -> str:
        """Produce sample code showcasing current keyword mappings."""

        config = self.current_config or LanguageConfig()
        canonical = {
            mapping.original.lower(): mapping.custom
            for mapping in config.keyword_mappings.values()
        }

        def kw(name: str, fallback: str) -> str:
            return canonical.get(name, fallback)

        func_kw = kw("function", "function")
        if_kw = kw("if", "if")
        else_kw = kw("else", "else")
        while_kw = kw("while", "while")
        loop_kw = kw("for", "for")
        print_kw = kw("print", "print")

        sample = textwrap.dedent(
            f"""
            {func_kw} greet(name):
                {print_kw}("Hello, " + name)

            {loop_kw} counter in range(3):
                {print_kw}(counter)

            {if_kw} counter == 3:
                {print_kw}("Done")
            {else_kw}:
                {print_kw}("Still running")

            {while_kw} counter < 5:
                counter = counter + 1
                {print_kw}(counter)
            """
        ).strip()
        return sample

    def _highlight_pattern(
        self, text_widget: tk.Text, pattern: str, tag: str, start: str = "1.0"
    ) -> int:
        """Apply a highlighting tag for each regex match."""

        if not hasattr(text_widget, "get"):
            return 0

        content = text_widget.get(start, tk.END)
        try:
            matches = list(re.finditer(pattern, content, re.MULTILINE))
        except re.error:
            return 0

        text_widget.tag_remove(tag, "1.0", tk.END)
        for match in matches:
            begin = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            text_widget.tag_add(tag, begin, end)

        return len(matches)

    def _pick_color(self, category: str, suggested: Optional[str] = None) -> str:
        """Assign a color to a syntax category."""

        color = suggested or self.syntax_theme.get(category, "#ffffff")
        self.syntax_theme[category] = color
        self._color_history.append(color)
        return color

    def _reset_colors(self) -> dict:
        """Reset syntax theme to defaults."""

        self.syntax_theme = dict(self._default_theme)
        return dict(self.syntax_theme)

    def _export_color_theme(self) -> str:
        """Return the current color theme as JSON."""

        return json.dumps(self.syntax_theme, indent=2)

    def init_code_intelligence(self) -> dict:
        """Initialise data required for code intelligence helpers."""

        self.intelligence_data = {
            "symbol_table": {},
            "usage_stats": Counter(),
            "last_analysis": None,
            "completions_cache": {},
        }
        return self.intelligence_data

    def analyze_code_complexity(self, code: str) -> dict:
        """Return lightweight complexity metrics for the supplied code."""

        if code is None:
            code = ""

        lines = [line for line in textwrap.dedent(code).splitlines() if line.strip()]
        keyword_usage: Counter = Counter()
        cyclomatic = 1
        max_nesting = 0

        for line in lines:
            stripped = line.strip()
            tokens = re.findall(r"[A-Za-z_]+", stripped)
            keyword_usage.update(token.lower() for token in tokens)
            cyclomatic += sum(
                token.lower() in {"if", "elif", "for", "while", "case", "except"}
                for token in tokens
            )
            indent = len(line) - len(line.lstrip(" "))
            current_level = indent // 4
            max_nesting = max(max_nesting, current_level)

        metrics = {
            "lines": len(lines),
            "statements": len(lines),
            "cyclomatic_complexity": max(1, cyclomatic),
            "nesting_depth": max_nesting,
            "keyword_usage": dict(keyword_usage),
        }

        if self.intelligence_data.get("usage_stats"):
            self.intelligence_data["usage_stats"].update(keyword_usage)
        else:
            self.intelligence_data["usage_stats"] = keyword_usage
        self.intelligence_data["last_analysis"] = metrics
        return metrics

    def suggest_refactoring(self, code: str) -> List[dict]:
        """Provide heuristic refactoring suggestions."""

        if code is None:
            code = ""

        lines = [
            line.rstrip() for line in textwrap.dedent(code).splitlines() if line.strip()
        ]
        suggestions: List[dict] = []

        counts = Counter(lines)
        duplicates = [
            line for line, count in counts.items() if count > 1 and len(line) > 3
        ]
        if duplicates:
            suggestions.append(
                {
                    "type": "deduplicate",
                    "message": "Duplicate lines detected",
                    "instances": duplicates[:5],
                }
            )

        long_lines = [line for line in lines if len(line) > 80]
        if long_lines:
            suggestions.append(
                {
                    "type": "long-line",
                    "message": "Consider wrapping long lines",
                    "count": len(long_lines),
                }
            )

        if len(lines) > 100:
            suggestions.append(
                {
                    "type": "large-file",
                    "message": "Split large modules into smaller units",
                    "lines": len(lines),
                }
            )

        if not suggestions:
            suggestions.append(
                {"type": "clean", "message": "No obvious refactors detected"}
            )

        return suggestions

    def auto_complete_code(self, source: str, cursor_index: int) -> List[str]:
        """Return completion candidates based on current context."""

        if source is None:
            source = ""

        cursor_index = max(0, min(cursor_index, len(source)))
        start = cursor_index
        while start > 0 and (source[start - 1].isalnum() or source[start - 1] == "_"):
            start -= 1
        prefix = source[start:cursor_index]

        candidates = set()
        if self.current_config:
            for mapping in self.current_config.keyword_mappings.values():
                candidates.add(mapping.custom)
            for func in self.current_config.builtin_functions.values():
                candidates.add(func.name)

        candidates.update({"print", "range", "return", "import"})
        candidates.update({"if", "else", "for", "while", "def", "class", "with", "try"})

        filtered = sorted(value for value in candidates if value.startswith(prefix))
        self.intelligence_data.setdefault("completions_cache", {})[prefix] = filtered
        return filtered

    def export_for_sharing(self, format_type: str = "package") -> str:
        """Serialize the active configuration for sharing."""

        config = self.current_config or LanguageConfig()
        payload = {
            "format": format_type,
            "generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "config": config.to_dict(),
            "metadata": {
                "name": config.name,
                "version": config.version,
                "description": config.description,
            },
        }
        serialized = json.dumps(payload, indent=2)
        self._recent_share_payloads.append(serialized)
        return serialized

    def generate_shareable_link(self) -> str:
        """Create a pseudo-link embedding the serialized configuration."""

        payload = self.export_for_sharing()
        encoded = (
            base64.urlsafe_b64encode(payload.encode("utf-8"))
            .decode("ascii")
            .rstrip("=")
        )
        link = f"hblcs://import?data={encoded}"
        self._recent_share_payloads.append(link)
        return link

    def import_shared_config(self, data: str) -> LanguageConfig:
        """Reconstruct a configuration from shared data."""

        raw = data
        try:
            padded = data + "=" * (-len(data) % 4)
            decoded = base64.urlsafe_b64decode(padded.encode("ascii"))
            if decoded.strip().startswith(b"{"):
                raw = decoded.decode("utf-8")
        except Exception:  # noqa: BLE001  # pylint: disable=broad-except
            pass

        config_payload = json.loads(raw)
        config_dict = config_payload.get("config", config_payload)
        config = LanguageConfig.from_dict(config_dict)
        self.current_config = config
        return config

    def sync_to_cloud(self, provider: str = "github") -> dict:
        """Simulate synchronising the configuration with a cloud provider."""

        sync_id = uuid.uuid4().hex[:10]
        return {
            "status": "success",
            "provider": provider,
            "sync_id": sync_id,
            "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        }

    def init_plugin_system(self) -> dict:
        """Initialise plugin registry structures."""

        self.plugins = {
            "available": {
                "linter": {
                    "description": "Static analysis helpers",
                    "hooks": ["on_save", "on_validation"],
                },
                "doc_gen": {
                    "description": "Generates documentation",
                    "hooks": ["on_export"],
                },
            },
            "loaded": {},
            "hooks": {},
        }
        return self.plugins

    def register_plugin(
        self, name: str, plugin_cls: Callable, hooks: List[str]
    ) -> bool:
        """Register a plugin and map its hooks."""

        if not getattr(self, "plugins", None):
            self.init_plugin_system()

        if name in self.plugins["loaded"]:
            return False

        instance = plugin_cls()
        registered_hooks = []
        for hook in hooks:
            if hasattr(instance, hook):
                self.plugins["hooks"].setdefault(hook, []).append(
                    (name, getattr(instance, hook))
                )
                registered_hooks.append(hook)

        self.plugins["loaded"][name] = {"instance": instance, "hooks": registered_hooks}
        return True

    def execute_plugin_hooks(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """Execute all registered hooks for a given event."""

        results: List[Any] = []
        for name, handler in self.plugins.get("hooks", {}).get(hook_name, []):
            try:
                results.append(handler(*args, **kwargs))
            except Exception as exc:  # noqa: BLE001  # pylint: disable=broad-except
                results.append({"plugin": name, "error": str(exc)})
        return results

    def list_plugins(self) -> dict:
        """Return summaries of available and loaded plugins."""

        available = list(self.plugins.get("available", {}).keys())
        loaded = list(self.plugins.get("loaded", {}).keys())
        return {"available": available, "loaded": loaded}

    def profile_language_performance(self, code: str) -> dict:
        """Estimate language translation performance metrics."""

        if code is None:
            code = ""

        lines = [line for line in textwrap.dedent(code).splitlines() if line.strip()]
        branches = sum(
            1 for line in lines if re.search(r"\b(if|for|while|match|case|try)\b", line)
        )
        translation_time = 0.0005 + len(lines) * 0.0001 + branches * 0.0002
        memory_estimate = 2048 + len(code) * 64
        optimization_score = max(
            10,
            min(100, int(100 - math.log(len(code) + 1, 2) * 5 - branches * 2)),
        )

        metrics = {
            "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "lines": len(lines),
            "branch_points": branches,
            "translation_time": translation_time,
            "memory_estimate": memory_estimate,
            "optimization_score": optimization_score,
        }
        self.performance_history.append(metrics)
        return metrics

    def benchmark_translation(self, iterations: int = 10, code: str = "") -> dict:
        """Run a synthetic translation benchmark."""

        iterations = max(1, int(iterations))
        payload = textwrap.dedent(code or self._generate_sample_code())
        start = time.perf_counter()
        checksum = 0
        for i in range(iterations):
            checksum ^= hash((i, len(payload), payload[:10]))
        elapsed = time.perf_counter() - start
        avg_time = elapsed / iterations
        return {
            "iterations": iterations,
            "avg_time": avg_time,
            "checksum": checksum & 0xFFFFFFFF,
        }

    def generate_performance_report(self) -> str:
        """Produce a textual performance summary."""

        if not self.performance_history:
            self.performance_history.append(self.profile_language_performance(""))

        lines = ["PERFORMANCE ANALYSIS", "=" * 80]
        for entry in self.performance_history[-5:]:
            lines.append(
                (
                    f"{entry['timestamp']} | lines={entry['lines']} | "
                    f"branches={entry['branch_points']} | time={entry['translation_time']:.6f}s | "
                    f"score={entry['optimization_score']}"
                )
            )

        avg_time = sum(
            item["translation_time"] for item in self.performance_history
        ) / len(self.performance_history)
        lines.append("-" * 80)
        lines.append(f"Average translation time: {avg_time:.6f}s")
        return "\n".join(lines)

    def suggest_optimizations(self, code: str) -> List[dict]:
        """Generate performance-oriented optimisation suggestions."""

        if code is None:
            code = ""

        lines = textwrap.dedent(code).splitlines()
        suggestions: List[dict] = []

        if len(lines) > 120:
            suggestions.append(
                {
                    "type": "split-modules",
                    "message": "Large script detected",
                    "lines": len(lines),
                }
            )

        loops = sum(1 for line in lines if re.search(r"\bfor\b|\bwhile\b", line))
        if loops > 20:
            suggestions.append(
                {
                    "type": "loop-optimization",
                    "message": "Consider vectorising or batching loops",
                    "loops": loops,
                }
            )

        literal_counts = Counter(line.strip() for line in lines if line.strip())
        hotspots = [line for line, count in literal_counts.items() if count > 10]
        if hotspots:
            suggestions.append(
                {
                    "type": "cache-results",
                    "message": "Repeated statements detected",
                    "examples": hotspots[:3],
                }
            )

        if not suggestions:
            suggestions.append(
                {"type": "info", "message": "Code already appears optimised"}
            )

        return suggestions

    def init_web_ide(self, port: int = 8080, host: str = "127.0.0.1") -> dict:
        """Prepare configuration for the lightweight web IDE."""

        base_url = f"http://{host}:{port}"
        features = {
            "live_reload": True,
            "syntax_highlighting": True,
            "collaboration": True,
            "api_endpoints": [
                "/api/config",
                "/api/code/execute",
                "/api/keywords",
            ],
        }
        self.web_app_config = {
            "host": host,
            "port": port,
            "base_url": base_url,
            "features": features,
        }
        self.web_routes = {
            "/": {"method": "GET", "handler": "serve_ui"},
            "/api/config": {"method": "GET", "handler": "get_config"},
            "/api/code/execute": {"method": "POST", "handler": "execute_code"},
            "/api/keywords": {"method": "GET", "handler": "list_keywords"},
        }
        return self.web_app_config

    def generate_web_ui_template(self) -> str:
        """Return a static HTML template representing the web IDE."""

        colors = self.syntax_theme
        html = textwrap.dedent(
            f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="utf-8" />
                <title>Honey Badger Web IDE</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        background: #1e1e1e;
                        color: #f0f0f0;
                    }}
                    header {{ padding: 1rem; background: #0f4c81; }}
                    textarea {{
                        width: 100%;
                        height: 300px;
                        padding: 1rem;
                        background: #252526;
                        color: {colors.get('Keywords', '#ffffff')};
                        border: none;
                    }}
                    button {{ margin-right: 0.5rem; padding: 0.6rem 1rem; }}  # noqa: E501 pylint: disable=line-too-long
                    #console {{ background: #111; padding: 1rem; min-height: 150px; white-space: pre-wrap; }}  # noqa: E501 pylint: disable=line-too-long
                </style>
            </head>
            <body>
                <header>
                    <h1>Honey Badger Language Construction Set</h1>
                    <p>Web IDE Preview</p>
                </header>
                <main style="padding: 1rem;">
                    <textarea id="editor" placeholder="Write code here..."></textarea>
                    <div style="margin-top: 1rem;">
                        <button onclick="runCode()">Run</button>
                        <button onclick="highlight()">Highlight</button>
                        <button onclick="downloadConfig()">Download Config</button>
                    </div>
                    <section id="console"></section>
                </main>
                <script>
                    async function runCode() {{
                        const response = await fetch('/api/code/execute', {{  # noqa: E501 pylint: disable=line-too-long
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},  # pylint: disable=line-too-long
                            body: JSON.stringify({{ code: document.getElementById('editor').value }})  # noqa: E501 pylint: disable=line-too-long
                        }});
                        const data = await response.json();
                        document.getElementById('console').textContent = data.output || data.error || '';  # noqa: E501 pylint: disable=line-too-long
                    }}
                    async function downloadConfig() {{
                        const response = await fetch('/api/config');
                        const data = await response.json();
                        const blob = new Blob([JSON.stringify(data, null, 2)], {{ type: 'application/json' }});  # pylint: disable=line-too-long  # noqa: E501
                        const link = document.createElement('a');
                        link.href = URL.createObjectURL(blob);
                        link.download = 'language-config.json';
                        link.click();
                    }}
                    function highlight() {{
                        document.getElementById('console').textContent = 'Syntax highlighting simulated.';  # noqa: E501 pylint: disable=line-too-long
                    }}
                </script>
            </body>
            </html>
            """
        ).strip()
        return html

    def create_web_api_handler(
        self,
        route: str,
        method: str = "GET",
        handler: Optional[Callable[[], Any]] = None,
    ) -> dict:
        """Register a callable for a simulated web API endpoint."""

        if handler is None:

            def handler() -> dict:
                config = self.current_config.to_dict() if self.current_config else {}
                return {"status": "ok", "config": config}

        self.web_routes[route] = {"method": method, "handler": handler}
        try:
            response = handler()
        except Exception as exc:  # noqa: BLE001  # pylint: disable=broad-except
            response = {"status": "error", "reason": str(exc)}

        return {"route": route, "method": method, "response": response}

    def init_remote_execution(self, sandbox_type: str = "local") -> bool:
        """Initialise remote execution configuration."""

        self.execution_config = {
            "sandbox_type": sandbox_type,
            "timeout": 10,
            "max_memory_mb": 256,
            "sandboxes": {},
            "last_run": None,
        }
        return True

    def execute_code_safely(self, code: str, timeout: int = 5) -> dict:
        """Execute code within a restricted namespace and capture output."""

        if not self.execution_config:
            self.init_remote_execution()

        safe_builtins = {
            "print": print,
            "range": range,
            "len": len,
            "int": int,
            "float": float,
            "str": str,
            "bool": bool,
            "enumerate": enumerate,
            "list": list,
            "dict": dict,
            "sum": sum,
            "min": min,
            "max": max,
        }

        globals_dict = {"__builtins__": safe_builtins}
        locals_dict: Dict[str, Any] = {}
        start = time.perf_counter()
        buffer = io.StringIO()
        status = "success"
        error = None

        try:
            with redirect_stdout(buffer):
                exec(  # noqa: S102  # pylint: disable=exec-used
                    textwrap.dedent(code or ""), globals_dict, locals_dict
                )
        except Exception as exc:  # noqa: BLE001  # pylint: disable=broad-except
            status = "error"
            error = str(exc)

        elapsed = time.perf_counter() - start
        timeout_limit = float(timeout) if timeout else 0.0
        self.execution_config["timeout"] = timeout_limit
        if timeout_limit and elapsed > timeout_limit and status == "success":
            status = "timeout"
            error = f"Execution exceeded timeout of {timeout_limit:.2f} seconds"

        result = {
            "status": status,
            "output": buffer.getvalue(),
            "error": error,
            "execution_time": elapsed,
        }
        self.execution_config["last_run"] = result
        return result

    def create_execution_sandbox(self, profile: str = "light") -> dict:
        """Simulate provisioning an execution sandbox."""

        if not self.execution_config:
            self.init_remote_execution()

        sandbox_id = f"sandbox-{uuid.uuid4().hex[:6]}"
        limits = {
            "light": {"memory_mb": 128, "cpu_shares": 1},
            "medium": {"memory_mb": 256, "cpu_shares": 2},
            "heavy": {"memory_mb": 512, "cpu_shares": 4},
        }
        resources = limits.get(profile, limits["light"])
        sandbox = {
            "id": sandbox_id,
            "profile": profile,
            "status": "ready",
            "isolation": "process",
            "resources": resources,
        }
        self.execution_config.setdefault("sandboxes", {})[sandbox_id] = sandbox
        return sandbox

    def distribute_execution(self, code: str, num_instances: int = 1) -> List[dict]:
        """Execute code across multiple simulated sandboxes."""

        results: List[dict] = []
        for _ in range(max(1, num_instances)):
            sandbox = self.create_execution_sandbox("distributed")
            result = self.execute_code_safely(code)
            result["sandbox_id"] = sandbox["id"]
            results.append(result)
        return results

    def init_debugger(self) -> dict:
        """Initialise the debugger state."""

        self.debugger_state = {
            "breakpoints": {},
            "watch_expressions": [],
            "variables": {},
            "call_stack": [],
            "trace": [],
        }
        return self.debugger_state

    def set_breakpoint(
        self, filename: str, line: int, condition: Optional[str] = None
    ) -> bool:
        """Register a breakpoint in the debugger state."""

        if not self.debugger_state:
            self.init_debugger()

        key = f"{filename}:{line}"
        self.debugger_state["breakpoints"][key] = {
            "condition": condition or "",
            "enabled": True,
        }
        return True

    def step_through_code(self, code: str, step_type: str = "line") -> dict:
        """Generate a synthetic execution trace for the supplied code."""

        if not self.debugger_state:
            self.init_debugger()

        trace_steps = []
        for index, raw in enumerate(textwrap.dedent(code or "").splitlines(), 1):
            stripped = raw.strip()
            if not stripped:
                continue
            trace_steps.append(
                {"line": index, "code": stripped, "step_type": step_type}
            )

        trace = {"steps": trace_steps, "count": len(trace_steps)}
        self.debugger_state["trace"].append(trace)
        return trace

    def inspect_variables(self) -> dict:
        """Expose a snapshot of debugger variables and breakpoints."""

        if not self.debugger_state:
            self.init_debugger()

        watched = list(self.debugger_state.get("watch_expressions", []))
        locals_view = dict(self.debugger_state.get("variables", {}))
        breakpoints = list(self.debugger_state.get("breakpoints", {}).keys())
        return {
            "watched": watched,
            "locals": locals_view,
            "breakpoints": breakpoints,
        }

    def init_community_registry(self) -> dict:
        """Initialise community registry data structures."""

        languages = [
            {
                "id": f"lang_{uuid.uuid4().hex[:6]}",
                "name": "Pythonic DSL",
                "category": "General",
                "rating": 4.6,
                "downloads": 1520,
                "tags": ["general", "educational"],
                "ratings": [],
            },
            {
                "id": f"lang_{uuid.uuid4().hex[:6]}",
                "name": "DataFlow Script",
                "category": "DSL",
                "rating": 4.2,
                "downloads": 980,
                "tags": ["dsl", "data"],
                "ratings": [],
            },
        ]

        self.community_registry = {
            "languages": languages,
            "categories": ["General", "DSL", "Education", "Experimental"],
            "users": [],
            "reviews": [],
        }
        return self.community_registry

    def register_user(self, username: str, email: str) -> dict:
        """Register a new community user."""

        if not self.community_registry:
            self.init_community_registry()

        user = {
            "id": f"user_{uuid.uuid4().hex[:8]}",
            "username": username,
            "email": email,
            "joined": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        }
        self.community_registry["users"].append(user)
        return user

    def publish_language(
        self,
        name: str,
        description: str,
        category: str,
        tags: Optional[List[str]] = None,
    ) -> dict:
        """Publish a language entry to the community registry."""

        if not self.community_registry:
            self.init_community_registry()

        tags = tags or [category.lower(), "community"]
        language = {
            "id": f"lang_{uuid.uuid4().hex[:6]}",
            "name": name,
            "description": description,
            "category": category,
            "tags": tags,
            "rating": 5.0,
            "ratings": [],
            "downloads": 0,
        }
        self.community_registry["languages"].append(language)
        return language

    def rate_and_review(self, language_id: str, rating: float, text: str) -> dict:
        """Store a language review and update aggregate rating."""

        if not self.community_registry:
            self.init_community_registry()

        language = next(
            (
                item
                for item in self.community_registry["languages"]
                if item["id"] == language_id
            ),
            None,
        )
        if language is None:
            raise ValueError("Language not found")

        language.setdefault("ratings", []).append(float(rating))
        language["rating"] = round(
            sum(language["ratings"]) / len(language["ratings"]),
            2,
        )

        review = {
            "id": f"review_{uuid.uuid4().hex[:8]}",
            "language_id": language_id,
            "rating": float(rating),
            "text": text,
            "created": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        }
        self.community_registry.setdefault("reviews", []).append(review)
        return review

    def _analyze_keyword_conflicts(self) -> str:
        """Analyze the active configuration for keyword conflicts."""
        if not self.current_config:
            return "No configuration loaded. Load a configuration first."

        mappings = list(self.current_config.keyword_mappings.values())
        lines = [
            "KEYWORD CONFLICT ANALYSIS",
            "-" * 32,
        ]

        counter = Counter(m.custom.lower() for m in mappings)
        duplicates = {name: count for name, count in counter.items() if count > 1}
        if duplicates:
            lines.append("CRITICAL: Duplicate keyword names detected.")
            for custom_name in sorted(duplicates):
                owners = [
                    m.original for m in mappings if m.custom.lower() == custom_name
                ]
                owner_list = ", ".join(sorted(owners))
                lines.append(f"  - '{custom_name}' used by {owner_list}")
        else:
            lines.append("No duplicate keyword names detected.")

        prefix_conflicts = []
        customs = [m.custom for m in mappings]
        for name in customs:
            for other in customs:
                if name != other and other.startswith(name):
                    prefix_conflicts.append((name, other))

        if prefix_conflicts:
            lines.append("WARNING: Prefix conflicts detected between keywords:")
            for shorter, longer in sorted(set(prefix_conflicts)):
                lines.append(f"  - '{shorter}' overlaps with '{longer}'")
        else:
            lines.append("No prefix conflicts detected.")

        return "\n".join(lines)

    def _analyze_ambiguous_patterns(self) -> str:
        """Highlight ambiguous keyword patterns in the configuration."""
        if not self.current_config:
            return "No configuration loaded."

        mappings = list(self.current_config.keyword_mappings.values())
        singles = [m.custom for m in mappings if len(m.custom) == 1]
        digits = [m.custom for m in mappings if any(ch.isdigit() for ch in m.custom)]

        overlaps = []
        customs = [m.custom for m in mappings]
        for candidate in customs:
            for other in customs:
                if candidate != other and other.lower().startswith(candidate.lower()):
                    overlaps.append((candidate, other))

        lines = [
            "AMBIGUOUS PATTERN ANALYSIS",
            "-" * 34,
            "SINGLE-CHARACTER KEYWORDS",
        ]
        if singles:
            for value in sorted(set(singles)):
                lines.append(f"  - {value}")
        else:
            lines.append("  - None detected")

        lines.append("\nKEYWORDS WITH DIGITS")
        if digits:
            for value in sorted(set(digits)):
                lines.append(f"  - {value}")
        else:
            lines.append("  - None detected")

        lines.append("\nPREFIX OVERLAPS")
        if overlaps:
            for shorter, longer in sorted(set(overlaps)):
                lines.append(f"  - '{shorter}' appears inside '{longer}'")
        else:
            lines.append("  - No ambiguous prefixes found")

        return "\n".join(lines)

    def _analyze_delimiter_issues(self) -> str:
        """Report potential delimiter issues for the active configuration."""
        if not self.current_config:
            return "No configuration loaded."

        options = self.current_config.syntax_options
        lines = [
            "DELIMITER ANALYSIS",
            "-" * 20,
            (
                "Single-line comment delimiter: "
                f"{options.single_line_comment or 'None'}"
            ),
        ]

        if not options.single_line_comment:
            lines.append("WARNING: No single-line comment delimiter is configured.")

        terminator = options.statement_terminator or "newline"
        lines.append(f"Statement terminator: {terminator}")

        if options.multi_line_comment_start and not options.multi_line_comment_end:
            warning = " ".join(
                [
                    "WARNING: Multi-line comment start defined without",
                    "an end delimiter.",
                ]
            )
            lines.append(warning)

        if options.multi_line_comment_start and options.multi_line_comment_end:
            confirmation = " ".join(
                [
                    "Multi-line comment delimiters appear to be",
                    "configured correctly.",
                ]
            )
            lines.append(confirmation)

        return "\n".join(lines)

    def _generate_fix_recommendations(self) -> str:
        """Create actionable recommendations based on analysis results."""
        if not self.current_config:
            return "No configuration loaded."

        mappings = list(self.current_config.keyword_mappings.values())
        counter = Counter(m.custom.lower() for m in mappings)
        duplicates = [name for name, count in counter.items() if count > 1]
        singles = [m.custom for m in mappings if len(m.custom) == 1]
        digits = [m.custom for m in mappings if any(ch.isdigit() for ch in m.custom)]

        lines = [
            "FIX RECOMMENDATIONS",
            "-" * 24,
        ]

        if duplicates:
            message = " ".join(
                [
                    "RECOMMEND: Rename duplicate keywords",
                    "to ensure unique mappings.",
                ]
            )
            lines.append(message)
            for name in sorted(set(duplicates)):
                lines.append(f"  - {name}")
        else:
            message = " ".join(
                [
                    "RECOMMEND: Keep keyword names;",
                    "no duplicates detected.",
                ]
            )
            lines.append(message)

        if singles:
            message = "RECOMMEND: Expand very short keywords to improve readability."
            lines.append(message)
            for value in sorted(set(singles)):
                lines.append(f"  - {value}")

        if digits:
            message = " ".join(
                [
                    "RECOMMEND: Remove digits from keyword names",
                    "for clarity when possible.",
                ]
            )
            lines.append(message)

        summary = " ".join(
            [
                "RECOMMEND: Review delimiter settings",
                "to confirm they match language goals.",
            ]
        )
        lines.append(summary)

        return "\n".join(lines)


def main():
    """Main entry point for the IDE."""
    root = tk.Tk()
    AdvancedIDE(root)
    root.mainloop()


if __name__ == "__main__":
    main()
