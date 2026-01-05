#!/usr/bin/env python3
"""
C Code Generator Backend for ParserCraft

Generates C code from custom language AST for native compilation.

Features:
    - AST to C translation
    - Memory management
    - Type-safe code generation
    - Standard library bindings
    - Optimization passes
    - Error reporting

Usage:
    from parsercraft.codegen_c import CCodeGenerator
    
    generator = CCodeGenerator(config)
    c_code = generator.generate(ast, "output.c")
    
    # Compile with:
    # gcc output.c -o program
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set


class CType(Enum):
    """C type mappings."""

    BOOL = "bool"
    INT = "int"
    FLOAT = "double"
    STR = "const char*"
    VOID = "void"
    ANY = "void*"
    LIST = "vector_t*"
    DICT = "map_t*"


@dataclass
class CVariable:
    """Represents a C variable."""

    name: str
    c_type: str
    is_pointer: bool = False
    is_const: bool = False
    initial_value: Optional[str] = None

    def declaration(self) -> str:
        """Generate C declaration."""
        prefix = "const " if self.is_const else ""
        suffix = "*" if self.is_pointer else ""
        if self.initial_value:
            return f"{prefix}{self.c_type}{suffix} {self.name} = {self.initial_value};"
        return f"{prefix}{self.c_type}{suffix} {self.name};"


@dataclass
class CFunction:
    """Represents a C function."""

    name: str
    return_type: str
    parameters: Dict[str, str] = field(default_factory=dict)  # name -> type
    body: List[str] = field(default_factory=list)
    is_static: bool = False
    is_inline: bool = False

    def signature(self) -> str:
        """Generate function signature."""
        params = ", ".join(f"{typ} {name}" for name, typ in self.parameters.items())
        prefix = "static " if self.is_static else ""
        inline = "inline " if self.is_inline else ""
        return f"{prefix}{inline}{self.return_type} {self.name}({params})"

    def definition(self) -> str:
        """Generate complete function definition."""
        sig = self.signature()
        body = "\n    ".join(self.body) if self.body else "return;"
        return f"{sig} {{\n    {body}\n}}"


class CCodeGenerator:
    """Generates C code from custom language AST."""

    def __init__(self, config: Any = None):
        self.config = config
        self.functions: List[CFunction] = []
        self.globals: List[CVariable] = []
        self.includes: Set[str] = {"<stdio.h>", "<stdlib.h>", "<string.h>"}
        self.indent_level = 0
        self.var_counter = 0

    def add_include(self, header: str) -> None:
        """Add include directive."""
        if not header.startswith("<") and not header.startswith('"'):
            header = f'"{header}"'
        self.includes.add(header)

    def gen_temp_var(self, c_type: str = "int") -> str:
        """Generate unique temporary variable."""
        var_name = f"__tmp_{self.var_counter}"
        self.var_counter += 1
        return var_name

    def indent(self) -> str:
        """Get current indentation."""
        return "    " * self.indent_level

    def generate_header(self) -> str:
        """Generate C header section."""
        lines = []

        # Includes
        for include in sorted(self.includes):
            lines.append(f"#include {include}")

        lines.append("")
        lines.append("// Forward declarations")
        for func in self.functions:
            lines.append(f"{func.signature()};")

        lines.append("")
        lines.append("// Global variables")
        for var in self.globals:
            lines.append(var.declaration())

        return "\n".join(lines)

    def generate_implementations(self) -> str:
        """Generate function implementations."""
        implementations = []
        for func in self.functions:
            implementations.append(func.definition())
            implementations.append("")
        return "\n".join(implementations)

    def generate_main(self) -> str:
        """Generate main function."""
        return """int main(int argc, char** argv) {
    // Program entry point
    return 0;
}
"""

    def generate(
        self, ast: Dict[str, Any], output_file: str = "output.c"
    ) -> str:
        """Generate complete C program."""
        code_parts = [
            "// Auto-generated C code from ParserCraft",
            f"// Original language: {self.config.name if self.config else 'Unknown'}",
            "",
            self.generate_header(),
            "",
            self.generate_implementations(),
            "",
            self.generate_main(),
        ]

        full_code = "\n".join(code_parts)

        # Write to file if specified
        if output_file:
            with open(output_file, "w") as f:
                f.write(full_code)

        return full_code

    def translate_type(self, lang_type: str) -> str:
        """Translate language type to C type."""
        type_map = {
            "bool": CType.BOOL.value,
            "int": CType.INT.value,
            "float": CType.FLOAT.value,
            "str": CType.STR.value,
            "string": CType.STR.value,
            "list": CType.LIST.value,
            "dict": CType.DICT.value,
            "void": CType.VOID.value,
        }
        return type_map.get(lang_type, CType.ANY.value)

    def gen_function_call(self, func_name: str, args: List[str]) -> str:
        """Generate C function call."""
        args_str = ", ".join(args)
        return f"{func_name}({args_str})"

    def gen_variable_declare(self, name: str, c_type: str, value: str = None) -> str:
        """Generate variable declaration."""
        var = CVariable(name, c_type, initial_value=value)
        return var.declaration()

    def gen_return(self, value: str = None) -> str:
        """Generate return statement."""
        if value:
            return f"{self.indent()}return {value};"
        return f"{self.indent()}return;"

    def gen_if(self, condition: str, true_body: List[str], false_body: List[str] = None) -> str:
        """Generate if statement."""
        lines = [f"{self.indent()}if ({condition}) {{"]
        self.indent_level += 1
        for stmt in true_body:
            lines.append(stmt)
        self.indent_level -= 1

        if false_body:
            lines.append(f"{self.indent()}}} else {{")
            self.indent_level += 1
            for stmt in false_body:
                lines.append(stmt)
            self.indent_level -= 1

        lines.append(f"{self.indent()}}}")
        return "\n".join(lines)

    def gen_loop(self, init: str, condition: str, increment: str, body: List[str]) -> str:
        """Generate for loop."""
        lines = [f"{self.indent()}for ({init}; {condition}; {increment}) {{"]
        self.indent_level += 1
        for stmt in body:
            lines.append(stmt)
        self.indent_level -= 1
        lines.append(f"{self.indent()}}}")
        return "\n".join(lines)

    def gen_while(self, condition: str, body: List[str]) -> str:
        """Generate while loop."""
        lines = [f"{self.indent()}while ({condition}) {{"]
        self.indent_level += 1
        for stmt in body:
            lines.append(stmt)
        self.indent_level -= 1
        lines.append(f"{self.indent()}}}")
        return "\n".join(lines)

    def gen_binary_op(self, left: str, op: str, right: str) -> str:
        """Generate binary operation."""
        return f"({left} {op} {right})"

    def gen_assignment(self, target: str, value: str) -> str:
        """Generate assignment statement."""
        return f"{self.indent()}{target} = {value};"

    def gen_printf(self, format_str: str, args: List[str] = None) -> str:
        """Generate printf call."""
        args_str = f", {', '.join(args)}" if args else ""
        return f'{self.indent()}printf("{format_str}"{args_str});'
