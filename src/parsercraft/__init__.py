"""
ParserCraft — Custom Programming Language Construction Framework

Design, build, and deploy real programming languages through configuration.
Supports grammar definition (BNF/PEG), code generation (C, WASM, Python, LLVM IR),
LSP integration, and full runtime interpretation.

Usage:
    from parsercraft import LanguageConfig, LanguageRuntime

    config = LanguageConfig.from_preset("python_like")
    config.rename_keyword("if", "cuando")
"""

__version__ = "4.0.0"
__author__ = "James-HoneyBadger"

# Backward-compatible top-level imports
from parsercraft.config.language_config import LanguageConfig
from parsercraft.runtime.language_runtime import LanguageRuntime

__all__ = ["LanguageConfig", "LanguageRuntime"]
