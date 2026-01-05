"""
ParserCraft

A comprehensive system for creating custom programming language variants.
"""

__version__ = "1.0.0"
__author__ = "James-HoneyBadger"

from .language_config import LanguageConfig
from .language_runtime import LanguageRuntime

__all__ = ["LanguageConfig", "LanguageRuntime"]
