#!/usr/bin/env python3
"""
TeachScript Runtime

An advanced runtime environment for TeachScript - an educational programming
language integrated with the ParserCraft IDE. This module provides:

- Transpilation from TeachScript to Python
- Enhanced educational libraries (graphics, math, games)
- Interactive debugging and testing
- Syntax error reporting with helpful messages
- Package management and module loading
- IDE integration via hooks and callbacks
"""

import ast
import io
import math
import random
import re
from contextlib import redirect_stderr, redirect_stdout
from typing import Callable, List, Optional, Tuple


class TeachScriptError(Exception):
    """Base exception for TeachScript runtime errors."""


class TeachScriptSyntaxError(TeachScriptError):
    """Raised when there's a syntax error in TeachScript code."""


class TeachScriptRuntimeError(TeachScriptError):
    """Raised when there's a runtime error during execution."""


class TeachScriptTranspiler:
    """Transpiles TeachScript code to Python."""

    # Core keyword mappings
    KEYWORD_MAP = {
        "when": "if",
        "otherwise": "else",
        "or_when": "elif",
        "repeat_while": "while",
        "repeat_for": "for",
        "stop": "break",
        "skip": "continue",
        "teach": "def",
        "give_back": "return",
        "yes": "True",
        "no": "False",
        "nothing": "None",
        "and_also": "and",
        "or_else": "or",
        "opposite": "not",
        "inside": "in",
        "equals": "is",
    }

    # Built-in function mappings
    FUNCTION_MAP = {
        "say": "print",
        "ask": "input",
        "make_number": "int",
        "make_decimal": "float",
        "make_text": "str",
        "make_boolean": "bool",
        "length_of": "len",
        "absolute": "abs",
        "round_to": "round",
        "biggest": "max",
        "smallest": "min",
        "total": "sum",
        "type_of": "type",
        "numbers_from": "range",
        "count_through": "enumerate",
        "arrange": "sorted",
        "backwards": "reversed",
        "is_whole": "isinstance",
        "join_text": "str.join",
        "split_text": "str.split",
        "lowercase": "str.lower",
        "uppercase": "str.upper",
        "replace_in": "str.replace",
    }

    # Method mappings
    METHOD_MAP = {
        "add_to": "append",
        "remove_from": "pop",
        "find_in": "index",
        "clear": "clear",
        "copy": "copy",
    }

    def __init__(self):
        """Initialize the transpiler."""
        self.line_number = 0
        self.source_lines = []

    def transpile(self, code: str) -> str:
        """
        Transpile TeachScript code to Python.

        Args:
            code: TeachScript source code

        Returns:
            Python source code

        Raises:
            TeachScriptSyntaxError: If transpilation fails
        """
        self.source_lines = code.split("\n")
        translated_lines = []

        for line_num, line in enumerate(self.source_lines, 1):
            self.line_number = line_num
            try:
                translated = self._translate_line(line)
                translated_lines.append(translated)
            except Exception as e:
                raise TeachScriptSyntaxError(
                    f"Error on line {line_num}: {line}\n{str(e)}"
                ) from e

        return "\n".join(translated_lines)

    def _translate_line(self, line: str) -> str:
        """Translate a single line of TeachScript to Python."""
        # Preserve indentation
        indent = len(line) - len(line.lstrip())
        content = line.lstrip()

        # Skip empty lines and comments
        if not content or content.startswith("#"):
            return line

        # Remove 'remember' keyword (variable declaration)
        content = re.sub(r"\bremember\s+", "", content)
        content = re.sub(r"\bforever\s+", "", content)

        # Replace keywords (use word boundaries to avoid partial matches)
        for teach_kw, python_kw in self.KEYWORD_MAP.items():
            pattern = r"\b" + re.escape(teach_kw) + r"\b"
            content = re.sub(pattern, python_kw, content)

        # Replace function names
        for teach_func, python_func in self.FUNCTION_MAP.items():
            pattern = r"\b" + re.escape(teach_func) + r"\b"
            content = re.sub(pattern, python_func, content)

        # Replace method names
        for teach_method, python_method in self.METHOD_MAP.items():
            pattern = r"\b" + re.escape(teach_method) + r"\b"
            content = re.sub(pattern, python_method, content)

        # Handle string literals with newlines (for multi-line strings)
        # content = re.sub(r'say\("""(.+?)"""\)', r'print("""\1""")', content, flags=re.DOTALL)

        return " " * indent + content


class TeachScriptEnvironment:
    """Provides the execution environment for TeachScript code."""

    def __init__(self):
        """Initialize the environment with educational libraries."""
        self.namespace = {}
        self._setup_builtins()
        self._setup_libraries()

    def _setup_builtins(self):
        """Set up built-in functions."""
        self.namespace.update(
            {
                "print": print,
                "input": input,
                "int": int,
                "float": float,
                "str": str,
                "bool": bool,
                "len": len,
                "abs": abs,
                "round": round,
                "max": max,
                "min": min,
                "sum": sum,
                "type": type,
                "range": range,
                "enumerate": enumerate,
                "sorted": sorted,
                "reversed": reversed,
                "list": list,
                "dict": dict,
                "set": set,
                "tuple": tuple,
                "isinstance": isinstance,
                "str_join": str.join,
                "str_split": str.split,
                "str_lower": str.lower,
                "str_upper": str.upper,
                "str_replace": str.replace,
            }
        )

    def _setup_libraries(self):
        """Set up educational libraries."""
        # Math library
        self.namespace["TSMath"] = {
            "pi": math.pi,
            "e": math.e,
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "exp": math.exp,
            "factorial": math.factorial,
            "gcd": math.gcd,
            "floor": math.floor,
            "ceil": math.ceil,
        }

        # Random library
        self.namespace["TSRandom"] = {
            "random": random.random,
            "randint": random.randint,
            "choice": random.choice,
            "shuffle": random.shuffle,
        }

        # Graphics library (stub for future implementation)
        self.namespace["TSGraphics"] = {
            "create_window": lambda w, h, title: print(f"Window: {title} ({w}x{h})"),
            "draw_circle": lambda x, y, r: print(f"Circle at ({x},{y}) r={r}"),
            "draw_rectangle": lambda x, y, w, h: print(
                f"Rectangle at ({x},{y}) {w}x{h}"
            ),
            "draw_line": lambda x1, y1, x2, y2: print(f"Line ({x1},{y1})->({x2},{y2})"),
        }

        # Game library (stub for future implementation)
        self.namespace["TSGame"] = {
            "create_game": lambda title: print(f"Game: {title}"),
            "handle_input": lambda: None,
            "update": lambda: None,
            "render": lambda: None,
        }

    def execute(
        self, python_code: str, _timeout: Optional[float] = None
    ) -> Tuple[str, str]:
        """
        Execute Python code in the environment.

        Args:
            python_code: Python code to execute
            timeout: Optional timeout in seconds

        Returns:
            Tuple of (stdout, stderr)

        Raises:
            TeachScriptRuntimeError: If execution fails
        """
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        try:
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(python_code, self.namespace)
        except Exception as e:
            raise TeachScriptRuntimeError(f"Execution error: {str(e)}") from e

        return stdout_capture.getvalue(), stderr_capture.getvalue()


class TeachScriptRuntime:
    """Main runtime for executing TeachScript programs."""

    def __init__(self):
        """Initialize the TeachScript runtime."""
        self.transpiler = TeachScriptTranspiler()
        self.environment = TeachScriptEnvironment()
        self.last_output = ""
        self.last_error = ""
        self.callbacks = {}

    def register_callback(self, event: str, callback: Callable):
        """Register a callback for an event."""
        if event not in self.callbacks:
            self.callbacks[event] = []
        self.callbacks[event].append(callback)

    def _fire_event(self, event: str, **kwargs):
        """Fire an event."""
        if event in self.callbacks:
            for callback in self.callbacks[event]:
                callback(**kwargs)

    def run(self, teachscript_code: str) -> Tuple[str, str]:
        """
        Run TeachScript code.

        Args:
            teachscript_code: TeachScript source code

        Returns:
            Tuple of (output, error)
        """
        try:
            # Transpile
            self._fire_event("transpiling", code=teachscript_code)
            python_code = self.transpiler.transpile(teachscript_code)
            self._fire_event("transpiled", python_code=python_code)

            # Execute
            self._fire_event("executing", python_code=python_code)
            stdout, stderr = self.environment.execute(python_code)
            self._fire_event("executed", output=stdout, error=stderr)

            self.last_output = stdout
            self.last_error = stderr
            return stdout, stderr

        except TeachScriptError as e:
            self._fire_event("error", error=str(e))
            self.last_error = str(e)
            return "", str(e)
        except Exception as e:  # pylint: disable=broad-exception-caught
            error_msg = f"Unexpected error: {str(e)}"
            self._fire_event("error", error=error_msg)
            self.last_error = error_msg
            return "", error_msg

    def run_file(self, filepath: str) -> Tuple[str, str]:
        """Run a TeachScript file."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                code = f.read()
            return self.run(code)
        except FileNotFoundError:
            error = f"File not found: {filepath}"
            self.last_error = error
            return "", error

    def get_transpiled_code(self, teachscript_code: str) -> str:
        """Get the transpiled Python code (for debugging)."""
        return self.transpiler.transpile(teachscript_code)

    def get_syntax_errors(self, teachscript_code: str) -> List[str]:
        """Check for syntax errors."""
        errors = []
        try:
            python_code = self.transpiler.transpile(teachscript_code)
            ast.parse(python_code)
        except TeachScriptSyntaxError as e:
            errors.append(str(e))
        except SyntaxError as e:
            errors.append(f"Syntax error: {e.msg} at line {e.lineno}")
        return errors


# Global runtime instance
_global_runtime: Optional[TeachScriptRuntime] = None


def get_runtime() -> TeachScriptRuntime:
    """Get or create the global TeachScript runtime."""
    global _global_runtime
    if _global_runtime is None:
        _global_runtime = TeachScriptRuntime()
    return _global_runtime


def reset_runtime():
    """Reset the global runtime."""
    global _global_runtime
    _global_runtime = TeachScriptRuntime()
