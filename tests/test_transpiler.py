"""Tests for the Python transpiler."""

import pytest

from parsercraft.parser.grammar import GrammarParser, PEGInterpreter
from parsercraft.codegen.python_transpiler import (
    PythonTranspiler,
    TranspileOptions,
    transpile_to_python,
    transpile_and_exec,
)


@pytest.fixture
def grammar():
    parser = GrammarParser()
    return parser.parse(
        'program <- statement+\n'
        'statement <- assignment\n'
        'assignment <- IDENT "=" expr ";"\n'
        'expr <- term (("+" / "-") term)*\n'
        'term <- factor (("*" / "/") factor)*\n'
        'factor <- NUMBER / IDENT / "(" expr ")"'
    )


@pytest.fixture
def interpreter(grammar):
    return PEGInterpreter(grammar)


class TestPythonTranspiler:
    """Test AST to Python transpilation."""

    def test_simple_assignment(self, interpreter):
        ast = interpreter.parse("x = 10 ;")
        t = PythonTranspiler()
        code = t.transpile(ast)
        assert "x = 10" in code

    def test_arithmetic(self, interpreter):
        ast = interpreter.parse("y = 3 + 4 ;")
        t = PythonTranspiler()
        code = t.transpile(ast)
        assert "y = 3 + 4" in code or "y = (3 + 4)" in code

    def test_complex_expression(self, interpreter):
        ast = interpreter.parse("z = 2 + 3 * 4 ;")
        t = PythonTranspiler()
        code = t.transpile(ast)
        ns = {}
        exec(code, ns)
        assert ns["z"] == 14

    def test_multiple_statements(self, interpreter):
        ast = interpreter.parse("a = 10 ; b = 20 ; c = a + b ;")
        t = PythonTranspiler()
        code = t.transpile(ast)
        ns = {}
        exec(code, ns)
        assert ns["a"] == 10
        assert ns["b"] == 20
        assert ns["c"] == 30

    def test_variable_references(self, interpreter):
        ast = interpreter.parse("x = 5 ; y = x * 3 ;")
        t = PythonTranspiler()
        code = t.transpile(ast)
        ns = {}
        exec(code, ns)
        assert ns["y"] == 15

    def test_parenthesized_expression(self, interpreter):
        ast = interpreter.parse("r = ( 2 + 3 ) * 4 ;")
        t = PythonTranspiler()
        code = t.transpile(ast)
        ns = {}
        exec(code, ns)
        assert ns["r"] == 20

    def test_subtraction(self, interpreter):
        ast = interpreter.parse("d = 10 - 3 ;")
        t = PythonTranspiler()
        code = t.transpile(ast)
        ns = {}
        exec(code, ns)
        assert ns["d"] == 7

    def test_division(self, interpreter):
        ast = interpreter.parse("q = 20 / 4 ;")
        t = PythonTranspiler()
        code = t.transpile(ast)
        ns = {}
        exec(code, ns)
        assert ns["q"] == 5.0 or ns["q"] == 5


class TestTranspileHelpers:
    """Test the convenience functions."""

    def test_transpile_to_python(self, interpreter):
        ast = interpreter.parse("x = 42 ;")
        code = transpile_to_python(ast)
        assert "x = 42" in code

    def test_transpile_and_exec(self, interpreter):
        ast = interpreter.parse("a = 7 ; b = a * 6 ;")
        ns = transpile_and_exec(ast)
        assert ns["a"] == 7
        assert ns["b"] == 42


class TestTranspileOptions:
    """Test transpiler with custom options."""

    def test_default_options(self):
        opts = TranspileOptions()
        assert opts.indent_str == "    "
        assert opts.keyword_map == {}

    def test_custom_indent_str(self, interpreter):
        ast = interpreter.parse("x = 1 ;")
        opts = TranspileOptions(indent_str="\t")
        t = PythonTranspiler(opts)
        code = t.transpile(ast)
        assert "x = 1" in code
