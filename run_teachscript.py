#!/usr/bin/env python3
"""
TeachScript Runner

Executes TeachScript programs (.teach files) by translating them to Python.
"""

import sys
import re


# TeachScript to Python keyword mapping
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

# Function name mapping
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
}

# Method mappings (for string/list methods)
METHOD_MAP = {
    "add_to": "append",
    "remove_from": "pop",
}


def translate_teachscript(code: str) -> str:
    """Translate TeachScript code to Python code."""
    lines = code.split("\n")
    translated_lines = []

    for line in lines:
        translated = line

        # Replace keywords (use word boundaries)
        for teach_kw, python_kw in KEYWORD_MAP.items():
            pattern = r"\b" + re.escape(teach_kw) + r"\b"
            translated = re.sub(pattern, python_kw, translated)

        # Replace function names
        for teach_func, python_func in FUNCTION_MAP.items():
            pattern = r"\b" + re.escape(teach_func) + r"\b"
            translated = re.sub(pattern, python_func, translated)

        # Replace method names (for list.add_to() -> list.append())
        for teach_method, python_method in METHOD_MAP.items():
            pattern = r"\b" + re.escape(teach_method) + r"\b"
            translated = re.sub(pattern, python_method, translated)

        # Handle "remember" keyword (variable declaration)
        translated = re.sub(r"\bremember\s+", "", translated)
        translated = re.sub(r"\bforever\s+", "", translated)

        translated_lines.append(translated)

    return "\n".join(translated_lines)


def run_teachscript_file(filepath: str, verbose: bool = False):
    """Load and execute a TeachScript file."""

    # Read the TeachScript file
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            teachscript_code = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    if verbose:
        print(f"Read file: {filepath}")
        print(f"{'='*60}")
        print("TeachScript Code:")
        print(f"{'='*60}")
        print(teachscript_code)
        print(f"{'='*60}\n")

    # Translate to Python
    try:
        python_code = translate_teachscript(teachscript_code)

        if verbose:
            print("Translated Python Code:")
            print(f"{'='*60}")
            print(python_code)
            print(f"{'='*60}\n")
            print("Execution Output:")
            print(f"{'='*60}")
    except Exception as e:
        print(f"Error translating code: {e}")
        sys.exit(1)

    # Execute the translated Python code
    try:
        exec(python_code, {"__name__": "__main__"})
        if verbose:
            print(f"{'='*60}")
    except Exception as e:
        print(f"\nExecution error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("TeachScript Runner")
        print("=" * 60)
        print("Usage: python run_teachscript.py <file.teach> [--verbose]")
        print("\nExamples:")
        ex1 = "teachscript_examples/01_hello_world.teach"
        print(f"  python run_teachscript.py {ex1}")
        print("  python run_teachscript.py myprogram.teach --verbose")
        sys.exit(1)

    filepath = sys.argv[1]
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    run_teachscript_file(filepath, verbose)


if __name__ == "__main__":
    main()
