"""
ParserCraft — Custom Programming Language Construction Framework

Core pipeline: PEG grammar → PEGInterpreter → SourceAST → backend

Supports:
    - PEG grammar definition (text notation or fluent GrammarBuilder API)
    - Multiple code-generation backends: Python transpiler, C,
      WebAssembly, LLVM IR
    - Config-driven keyword remapping via YAML/JSON language definitions
    - Interactive REPL, standard library injection, and FFI (ctypes + Python)
    - Tkinter IDE and 40+ CLI subcommands

Primary usage (grammar engine):
    from parsercraft.parser import GrammarParser, PEGInterpreter
    from parsercraft.codegen import transpile_and_exec

    grammar = GrammarParser().parse(
        'program <- statement+\n'
        'statement <- IDENT "=" expr ";"\n'
        'expr <- NUMBER'
    )
    ast = PEGInterpreter(grammar).parse('x = 42 ;')
    result = transpile_and_exec(ast)  # {'x': 42}

Config-driven usage:
    from parsercraft import LanguageConfig, LanguageRuntime

    config = LanguageConfig.from_preset("python_like")
    config.rename_keyword("if", "cuando")
    config.save("spanish.yaml")
"""

__version__ = "4.0.0"
__author__ = "James-HoneyBadger"

# Backward-compatible top-level imports
from parsercraft.config.language_config import LanguageConfig
from parsercraft.runtime.language_runtime import LanguageRuntime

__all__ = ["LanguageConfig", "LanguageRuntime"]
