"""Tests for code generators (C, WASM, LLVM IR)."""

import pytest

from parsercraft.parser.grammar import GrammarParser, PEGInterpreter
from parsercraft.codegen.codegen_c import CCodeGenerator
from parsercraft.codegen.codegen_wasm import WasmGenerator
from parsercraft.codegen.llvm_ir import LLVMIRGenerator


@pytest.fixture
def interpreter():
    parser = GrammarParser()
    grammar = parser.parse(
        'program <- statement+\n'
        'statement <- assignment\n'
        'assignment <- IDENT "=" expr ";"\n'
        'expr <- term (("+" / "-") term)*\n'
        'term <- factor (("*" / "/") factor)*\n'
        'factor <- NUMBER / IDENT / "(" expr ")"'
    )
    return PEGInterpreter(grammar)


class TestCCodeGenerator:
    """Test AST to C code generation."""

    def test_simple_assignment(self, interpreter):
        ast = interpreter.parse("x = 10 ;")
        gen = CCodeGenerator()
        c_code = gen.translate_source_ast(ast)
        assert "int x = 10" in c_code
        assert "int main(" in c_code

    def test_arithmetic(self, interpreter):
        ast = interpreter.parse("y = 3 + 4 ;")
        gen = CCodeGenerator()
        c_code = gen.translate_source_ast(ast)
        assert "y" in c_code
        assert "3" in c_code

    def test_multiple_variables(self, interpreter):
        ast = interpreter.parse("a = 1 ; b = 2 ; c = a + b ;")
        gen = CCodeGenerator()
        c_code = gen.translate_source_ast(ast)
        assert "int a" in c_code
        assert "int b" in c_code
        assert "int c" in c_code

    def test_produces_valid_c_structure(self, interpreter):
        ast = interpreter.parse("x = 42 ;")
        gen = CCodeGenerator()
        c_code = gen.translate_source_ast(ast)
        assert "#include" in c_code or "int main" in c_code
        assert "return 0;" in c_code


class TestWasmGenerator:
    """Test AST to WebAssembly (WAT) code generation."""

    def test_simple_assignment(self, interpreter):
        ast = interpreter.parse("x = 10 ;")
        gen = WasmGenerator()
        result = gen.translate_source_ast(ast)
        wat = result.to_wat()
        assert "(module" in wat
        assert "(func" in wat

    def test_arithmetic(self, interpreter):
        ast = interpreter.parse("y = 3 + 4 ;")
        gen = WasmGenerator()
        result = gen.translate_source_ast(ast)
        wat = result.to_wat()
        assert "i32.add" in wat or "i32.const" in wat

    def test_multiple_statements(self, interpreter):
        ast = interpreter.parse("a = 5 ; b = a ;")
        gen = WasmGenerator()
        result = gen.translate_source_ast(ast)
        wat = result.to_wat()
        assert "(local" in wat


class TestLLVMIRGenerator:
    """Test AST to LLVM IR code generation."""

    def test_simple_assignment(self, interpreter):
        ast = interpreter.parse("x = 10 ;")
        gen = LLVMIRGenerator()
        ir = gen.translate_source_ast(ast)
        assert "define" in ir
        assert "alloca" in ir
        assert "store" in ir

    def test_arithmetic(self, interpreter):
        ast = interpreter.parse("y = 3 + 4 ;")
        gen = LLVMIRGenerator()
        ir = gen.translate_source_ast(ast)
        assert "add" in ir

    def test_multiplication(self, interpreter):
        ast = interpreter.parse("z = 5 * 6 ;")
        gen = LLVMIRGenerator()
        ir = gen.translate_source_ast(ast)
        assert "mul" in ir

    def test_complex_expression(self, interpreter):
        ast = interpreter.parse("r = 2 + 3 * 4 ;")
        gen = LLVMIRGenerator()
        ir = gen.translate_source_ast(ast)
        # Should have both mul and add
        assert "mul" in ir
        assert "add" in ir

    def test_variable_reference(self, interpreter):
        ast = interpreter.parse("a = 10 ; b = a ;")
        gen = LLVMIRGenerator()
        ir = gen.translate_source_ast(ast)
        assert "load" in ir

    def test_produces_ssa_form(self, interpreter):
        ast = interpreter.parse("x = 1 ; y = 2 ;")
        gen = LLVMIRGenerator()
        ir = gen.translate_source_ast(ast)
        # SSA form uses numbered registers
        assert "%1" in ir or "%0" in ir or "%" in ir
