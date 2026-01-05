#!/usr/bin/env python3
"""
WebAssembly (WASM) Backend for Custom Languages

Compiles custom language code to WebAssembly for web deployment.

Features:
    - WAT (WebAssembly Text) generation
    - Memory management
    - Function imports/exports
    - Type system mapping to WASM types
    - Optimized instruction selection
    - WASM module builder

Usage:
    from parsercraft.codegen_wasm import WasmGenerator, WasmModule
    
    gen = WasmGenerator()
    module = gen.generate_from_ast(ast, config)
    wat_text = module.to_wat()
    module.save("output.wasm")

WASM Types:
    - i32: 32-bit integer
    - i64: 64-bit integer
    - f32: 32-bit float
    - f64: 64-bit float
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class WasmType(Enum):
    """WebAssembly primitive types."""

    I32 = "i32"  # 32-bit integer
    I64 = "i64"  # 64-bit integer
    F32 = "f32"  # 32-bit float
    F64 = "f64"  # 64-bit float


class WasmOp(Enum):
    """Common WebAssembly operations."""

    # Arithmetic
    ADD = "add"
    SUB = "sub"
    MUL = "mul"
    DIV = "div_s"  # signed division
    REM = "rem_s"  # signed remainder

    # Logic
    AND = "and"
    OR = "or"
    XOR = "xor"
    SHL = "shl"
    SHR_U = "shr_u"  # unsigned shift right

    # Comparison
    EQ = "eq"
    NE = "ne"
    LT_S = "lt_s"  # signed less than
    GT_S = "gt_s"  # signed greater than
    LE_S = "le_s"  # signed less than or equal
    GE_S = "ge_s"  # signed greater than or equal

    # Memory
    LOAD = "load"
    STORE = "store"

    # Control flow
    BR = "br"  # branch
    BR_IF = "br_if"  # branch if
    IF = "if"
    ELSE = "else"
    END = "end"
    LOOP = "loop"
    BLOCK = "block"
    RETURN = "return"
    CALL = "call"


@dataclass
class WasmLocal:
    """Local variable in WASM function."""

    name: str
    wasm_type: WasmType
    mutable: bool = True

    def to_wat(self) -> str:
        """Convert to WAT format."""
        return f"(local ${self.name} {self.wasm_type.value})"


@dataclass
class WasmFunction:
    """WebAssembly function."""

    name: str
    params: List[Tuple[str, WasmType]] = field(default_factory=list)
    return_type: Optional[WasmType] = None
    locals: List[WasmLocal] = field(default_factory=list)
    body: List[str] = field(default_factory=list)  # WAT instructions
    is_export: bool = False

    def to_wat(self) -> str:
        """Convert to WAT format."""
        lines = []

        # Function signature
        func_sig = f"(func ${self.name}"

        # Parameters
        for param_name, param_type in self.params:
            func_sig += f" (param ${param_name} {param_type.value})"

        # Return type
        if self.return_type:
            func_sig += f" (result {self.return_type.value})"

        # Export if needed
        if self.is_export:
            lines.append(f"(export \"{self.name}\" (func ${self.name}))")

        lines.append(func_sig)

        # Locals
        for local in self.locals:
            lines.append(f"  {local.to_wat()}")

        # Body
        for instruction in self.body:
            lines.append(f"  {instruction}")

        lines.append(")")

        return "\n".join(lines)


@dataclass
class WasmImport:
    """Imported function from JavaScript."""

    module: str
    name: str
    params: List[Tuple[str, WasmType]] = field(default_factory=list)
    return_type: Optional[WasmType] = None

    def to_wat(self) -> str:
        """Convert to WAT format."""
        sig = f"(func ${self.name}"

        for param_name, param_type in self.params:
            sig += f" (param ${param_name} {param_type.value})"

        if self.return_type:
            sig += f" (result {self.return_type.value})"

        sig += ")"

        return f'(import "{self.module}" "{self.name}" {sig})'


class WasmModule:
    """WebAssembly module builder."""

    def __init__(self, name: str = "module"):
        self.name = name
        self.functions: Dict[str, WasmFunction] = {}
        self.imports: Dict[str, WasmImport] = {}
        self.memory_size = 256  # Pages (256 * 64KB = 16MB)
        self.data_segment: Dict[int, bytes] = {}  # address -> data

    def add_function(self, func: WasmFunction) -> None:
        """Add function to module."""
        self.functions[func.name] = func

    def add_import(self, imp: WasmImport) -> None:
        """Add imported function."""
        self.imports[imp.name] = imp

    def add_data(self, address: int, data: bytes) -> None:
        """Add data segment."""
        self.data_segment[address] = data

    def set_memory_size(self, pages: int) -> None:
        """Set memory size in pages (64KB each)."""
        self.memory_size = pages

    def to_wat(self) -> str:
        """Convert module to WAT format."""
        lines = [f"(module ${self.name}"]

        # Memory
        lines.append(f"  (memory {self.memory_size})")

        # Imports
        for imp in self.imports.values():
            lines.append(f"  {imp.to_wat()}")

        # Functions
        for func in self.functions.values():
            for line in func.to_wat().split("\n"):
                lines.append(f"  {line}" if line and not line.startswith("(export") else line)

        # Data segments
        for address, data in self.data_segment.items():
            lines.append(f'  (data (i32.const {address}) "{data.decode()}")')

        lines.append(")")

        return "\n".join(lines)

    def save(self, filename: str) -> None:
        """Save module as WAT file."""
        with open(filename, "w") as f:
            f.write(self.to_wat())


class WasmGenerator:
    """Generates WebAssembly from custom language AST."""

    def __init__(self):
        self.module = WasmModule()
        self.type_mapping = {
            "int": WasmType.I32,
            "float": WasmType.F32,
            "bool": WasmType.I32,
        }
        self.var_count = 0

    def translate_type(self, lang_type: str) -> WasmType:
        """Translate language type to WASM type."""
        return self.type_mapping.get(lang_type, WasmType.I32)

    def gen_temp_var(self) -> str:
        """Generate unique temporary variable name."""
        self.var_count += 1
        return f"$temp{self.var_count}"

    def generate_from_ast(self, ast: Any, config: Any = None) -> WasmModule:
        """Generate WASM module from AST."""
        # This is a framework - actual AST traversal depends on language definition
        # For now, show structure of how it would work

        # Add memory
        self.module.set_memory_size(256)

        # Process function definitions from AST
        if hasattr(ast, "functions"):
            for func_def in ast.functions:
                wasm_func = self._generate_function(func_def)
                if wasm_func:
                    self.module.add_function(wasm_func)

        # Add standard library imports
        self._add_stdlib_imports()

        return self.module

    def _generate_function(self, func_def: Any) -> Optional[WasmFunction]:
        """Generate WASM function from function definition."""
        if not hasattr(func_def, "name"):
            return None

        # Map parameters
        params = []
        if hasattr(func_def, "params"):
            for param in func_def.params:
                param_type = self.translate_type(getattr(param, "type", "int"))
                params.append((getattr(param, "name", "arg"), param_type))

        # Map return type
        return_type = None
        if hasattr(func_def, "return_type"):
            return_type = self.translate_type(func_def.return_type)

        # Generate body
        body = []
        if hasattr(func_def, "body"):
            body = self._generate_body(func_def.body)

        func = WasmFunction(
            name=func_def.name,
            params=params,
            return_type=return_type,
            body=body,
            is_export=getattr(func_def, "is_export", False),
        )

        return func

    def _generate_body(self, statements: List[Any]) -> List[str]:
        """Generate WASM instructions from statements."""
        instructions = []

        for stmt in statements:
            if hasattr(stmt, "type"):
                if stmt.type == "return":
                    # Return statement
                    instructions.append("return")
                elif stmt.type == "assignment":
                    # Variable assignment
                    instructions.append(f"(local.set ${stmt.target} ...)") 
                elif stmt.type == "call":
                    # Function call
                    instructions.append(f"(call ${stmt.name})")

        return instructions

    def _add_stdlib_imports(self) -> None:
        """Add standard library imports for console output, math, etc."""
        # Console.log for debugging
        self.module.add_import(
            WasmImport(
                module="console",
                name="log",
                params=[("value", WasmType.I32)],
            )
        )

        # Math operations (if not using native WASM instructions)
        self.module.add_import(
            WasmImport(
                module="math",
                name="sqrt",
                params=[("value", WasmType.F64)],
                return_type=WasmType.F64,
            )
        )

    def generate_binary_op(self, op: str, left_type: WasmType, right_type: WasmType) -> str:
        """Generate WASM for binary operation."""
        # Map operator to WASM instruction
        op_map = {
            "+": WasmOp.ADD,
            "-": WasmOp.SUB,
            "*": WasmOp.MUL,
            "/": WasmOp.DIV,
            "==": WasmOp.EQ,
            "<": WasmOp.LT_S,
            ">": WasmOp.GT_S,
        }

        if op not in op_map:
            return f"(unreachable) ;; unknown op: {op}"

        wasm_op = op_map[op]
        type_suffix = ".i32" if left_type == WasmType.I32 else ".f32"

        return f"({wasm_op.value}{type_suffix})"

    def generate_memory_load(
        self, address: int, wasm_type: WasmType, offset: int = 0
    ) -> str:
        """Generate memory load instruction."""
        size_map = {WasmType.I32: 32, WasmType.I64: 64, WasmType.F32: 32, WasmType.F64: 64}
        size = size_map.get(wasm_type, 32)

        return f"({wasm_type.value}.load offset={offset} (i32.const {address}))"

    def generate_memory_store(
        self, address: int, wasm_type: WasmType, offset: int = 0
    ) -> str:
        """Generate memory store instruction."""
        return f"({wasm_type.value}.store offset={offset} (i32.const {address}))"

    def generate_loop(self, condition: str, body: List[str]) -> List[str]:
        """Generate WASM loop."""
        instructions = ["(block $break", "(loop $continue"]

        # Add condition check
        instructions.append(condition)
        instructions.append("(br_if $break)")

        # Add body
        instructions.extend(body)

        # Continue loop
        instructions.append("(br $continue)")
        instructions.append(")")
        instructions.append(")")

        return instructions

    def generate_if(
        self, condition: str, then_body: List[str], else_body: List[str] = None
    ) -> List[str]:
        """Generate WASM if statement."""
        instructions = ["(if", condition]

        instructions.append("(then")
        instructions.extend(then_body)
        instructions.append(")")

        if else_body:
            instructions.append("(else")
            instructions.extend(else_body)
            instructions.append(")")

        instructions.append(")")

        return instructions
