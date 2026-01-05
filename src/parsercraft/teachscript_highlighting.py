#!/usr/bin/env python3
"""
TeachScript Syntax Highlighting

Provides syntax highlighting for TeachScript code in the IDE with:
- Custom keyword highlighting
- Function name highlighting
- String and number highlighting
- Comment highlighting
- Smart indentation
"""

import re
import tkinter as tk
from typing import Dict, List, Optional, Tuple


class TeachScriptHighlighter:
    """Provides syntax highlighting for TeachScript code."""

    # Color theme for syntax highlighting
    DEFAULT_THEME = {
        "keyword": "#569cd6",  # Blue for keywords
        "function": "#dcdcaa",  # Yellow for functions
        "string": "#ce9178",  # Orange for strings
        "number": "#b5cea8",  # Green for numbers
        "comment": "#6a9955",  # Dark green for comments
        "operator": "#d4d4d4",  # White for operators
        "normal": "#d4d4d4",  # Default text color
    }

    # TeachScript keywords
    KEYWORDS = {
        # Control flow
        "when",
        "otherwise",
        "or_when",
        "repeat_while",
        "repeat_for",
        "stop",
        "skip",
        "teach",
        "give_back",
        # Values
        "yes",
        "no",
        "nothing",
        # Operators
        "and_also",
        "or_else",
        "opposite",
        "inside",
        "equals",
        # Special
        "remember",
        "forever",
    }

    # Built-in functions
    BUILTINS = {
        "say",
        "ask",
        "make_number",
        "make_decimal",
        "make_text",
        "make_boolean",
        "length_of",
        "absolute",
        "round_to",
        "biggest",
        "smallest",
        "total",
        "type_of",
        "numbers_from",
        "count_through",
        "arrange",
        "backwards",
        "is_whole",
        "join_text",
        "split_text",
        "lowercase",
        "uppercase",
        "replace_in",
        # Library namespaces
        "TSMath",
        "TSRandom",
        "TSGraphics",
        "TSGame",
    }

    def __init__(self, text_widget: tk.Text, theme: Optional[Dict[str, str]] = None):
        """
        Initialize the highlighter.

        Args:
            text_widget: The Text widget to highlight
            theme: Optional color theme (uses DEFAULT_THEME if None)
        """
        self.text = text_widget
        self.theme = theme or self.DEFAULT_THEME.copy()

        # Configure text tags
        self._setup_tags()

        # Bind events
        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Return>", self._on_return)

    def _setup_tags(self):
        """Setup text tags for different token types."""
        for token_type, color in self.theme.items():
            self.text.tag_config(token_type, foreground=color)

        # Additional styling
        self.text.tag_config(
            "keyword", foreground=self.theme["keyword"], font=("Courier", 10, "bold")
        )
        self.text.tag_config(
            "function", foreground=self.theme["function"], font=("Courier", 10, "bold")
        )

    def highlight_all(self):
        """Highlight all text in the editor."""
        self.text.tag_remove("keyword", "1.0", tk.END)
        self.text.tag_remove("function", "1.0", tk.END)
        self.text.tag_remove("string", "1.0", tk.END)
        self.text.tag_remove("number", "1.0", tk.END)
        self.text.tag_remove("comment", "1.0", tk.END)

        content = self.text.get("1.0", tk.END)
        self._highlight_content(content)

    def _highlight_content(self, content: str):
        """Highlight content."""
        lines = content.split("\n")

        for line_num, line in enumerate(lines, 1):
            self._highlight_line(line, line_num)

    def _highlight_line(self, line: str, line_num: int):
        """Highlight a single line."""
        # Skip empty lines and comments
        if not line.strip() or line.strip().startswith("#"):
            if line.strip().startswith("#"):
                start = f"{line_num}.{len(line) - len(line.lstrip())}"
                end = f"{line_num}.end"
                self.text.tag_add("comment", start, end)
            return

        # Highlight strings
        for match in re.finditer(r'["\'](?:\\.|[^\\\"])*["\']', line):
            start = f"{line_num}.{match.start()}"
            end = f"{line_num}.{match.end()}"
            self.text.tag_add("string", start, end)

        # Highlight numbers
        for match in re.finditer(r"\b\d+\.?\d*\b", line):
            start = f"{line_num}.{match.start()}"
            end = f"{line_num}.{match.end()}"
            self.text.tag_add("number", start, end)

        # Highlight keywords
        for keyword in self.KEYWORDS:
            pattern = r"\b" + re.escape(keyword) + r"\b"
            for match in re.finditer(pattern, line):
                start = f"{line_num}.{match.start()}"
                end = f"{line_num}.{match.end()}"
                self.text.tag_add("keyword", start, end)

        # Highlight functions
        for builtin in self.BUILTINS:
            pattern = r"\b" + re.escape(builtin) + r"\b"
            for match in re.finditer(pattern, line):
                start = f"{line_num}.{match.start()}"
                end = f"{line_num}.{match.end()}"
                self.text.tag_add("function", start, end)

        # Highlight comments (remaining after strings)
        if "#" in line:
            # Check if # is not in a string
            in_string = False
            string_char = None
            for i, char in enumerate(line):
                if char in ('"', "'") and (i == 0 or line[i - 1] != "\\"):
                    if not in_string:
                        in_string = True
                        string_char = char
                    elif char == string_char:
                        in_string = False

                if char == "#" and not in_string:
                    start = f"{line_num}.{i}"
                    end = f"{line_num}.end"
                    self.text.tag_add("comment", start, end)
                    break

    def _on_change(self, _event):
        """Called when text changes."""
        self.highlight_all()

    def _on_return(self, _event):
        """Called when return key is pressed."""
        # Auto-indent based on previous line
        self.text.after(10, self._auto_indent)
        return "break"

    def _auto_indent(self):
        """Automatically indent the new line."""
        # Get current line
        current_line = self.text.index(tk.INSERT).split(".")[0]
        prev_line_num = int(current_line) - 1

        if prev_line_num < 1:
            return

        prev_line = self.text.get(f"{prev_line_num}.0", f"{prev_line_num}.end")

        # Get indentation from previous line
        indent = len(prev_line) - len(prev_line.lstrip())

        # Check if previous line ends with ':'
        if prev_line.rstrip().endswith(":"):
            indent += 4

        # Insert indentation
        if indent > 0:
            self.text.insert(tk.INSERT, " " * indent)

    def change_theme(self, new_theme: Dict[str, str]):
        """Change the color theme."""
        self.theme.update(new_theme)
        self._setup_tags()
        self.highlight_all()


class TeachScriptCodeCompletion:
    """Provides code completion for TeachScript."""

    def __init__(self, text_widget: tk.Text):
        """Initialize code completion."""
        self.text = text_widget
        self.suggestions: list[str] = []
        self.popup: Optional[tk.Toplevel] = None

        self.text.bind("<Control-space>", self._show_completions)

    def _show_completions(self, _event):
        """Show code completion suggestions."""
        # Get word at cursor
        line = self.text.get("insert linestart", "insert")
        word = re.split(r"[\s\(\)\[\]\{\}.,;:\-+*/=]", line)[-1]

        if not word:
            return "break"

        # Get all possible completions
        completions = self._get_completions(word)

        if not completions:
            return "break"

        # Show popup
        self._show_popup(completions, word)
        return "break"

    def _get_completions(self, prefix: str) -> List[str]:
        """Get completions for a given prefix."""
        all_items = TeachScriptHighlighter.KEYWORDS | TeachScriptHighlighter.BUILTINS

        # Filter by prefix
        completions = [
            item for item in sorted(all_items) if item.startswith(prefix.lower())
        ]

        return completions[:10]  # Limit to 10 suggestions

    def _show_popup(self, completions: List[str], prefix: str):
        """Show completion popup."""
        if self.popup:
            self.popup.destroy()

        self.popup = tk.Toplevel(self.text)
        self.popup.wm_overrideredirect(True)

        # Position popup near cursor
        x = self.text.winfo_rootx()
        y = self.text.winfo_rooty()
        self.popup.wm_geometry(f"+{x+200}+{y+300}")

        # Create listbox
        listbox = tk.Listbox(self.popup, height=min(10, len(completions)))
        listbox.pack()

        for completion in completions:
            listbox.insert(tk.END, completion)

        def select(_event):
            selection = listbox.curselection()
            if selection:
                completion = completions[selection[0]]
                # Replace word with completion
                word_start = self.text.search(
                    prefix, "insert", backwards=True, regexp=True
                )
                if word_start:
                    self.text.delete(word_start, "insert")
                    self.text.insert(word_start, completion)
                    if self.popup:
                        self.popup.destroy()

        listbox.bind("<Return>", select)
        listbox.bind("<Escape>", lambda e: self.popup.destroy() if self.popup else None)


class TeachScriptLinter:
    """Lints TeachScript code for common errors."""

    @staticmethod
    def check_syntax(code: str) -> List[Tuple[int, str]]:
        """
        Check TeachScript syntax.

        Returns:
            List of (line_number, error_message) tuples
        """
        errors: list[tuple[int, str]] = []
        lines = code.split("\n")

        for _line_num, line in enumerate(lines, 1):
            # Check indentation
            if line and not line[0].isspace() and not line.startswith("#"):
                _ = line.lstrip()
                # Check for hanging colons
                if ":" in line and not line.rstrip().endswith(":"):
                    # Colon in middle - might be okay (e.g., inside strings)
                    pass

            # Check for unmatched parentheses
            open_parens = line.count("(") - line.count(")")
            if open_parens > 0 and not line.rstrip().endswith("\\"):
                # Might be continued on next line
                pass

        return errors
