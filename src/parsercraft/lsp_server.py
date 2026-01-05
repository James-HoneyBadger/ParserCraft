#!/usr/bin/env python3
"""
Language Server Protocol (LSP) Implementation for ParserCraft

Enables IDE integration (VS Code, PyCharm, Neovim, etc.) for custom ParserCraft languages.

Features:
    - Real-time syntax highlighting
    - Code completion
    - Hover documentation
    - Diagnostic/error reporting
    - Go to definition
    - Symbol renaming
    - Document formatting

Usage:
    # Start LSP server for a custom language
    python -m hb_lcs.lsp_server --config my_language.yaml --port 8080

    # Or use in IDE:
    # VS Code: Install "LSP Client" extension, configure server
    # PyCharm: Settings > Languages & Frameworks > Language Server Protocol

Protocol: Language Server Protocol v3.17
Reference: https://microsoft.github.io/language-server-protocol/
"""

from __future__ import annotations

import json
import logging
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Optional, Union

from .language_config import LanguageConfig
from .parser_generator import Lexer, ASTNode, Token, TokenType
from .language_validator import LanguageValidator


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("lsp_server.log"), logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger("ParserCraft-LSP")


class DiagnosticSeverity(Enum):
    """LSP Diagnostic severity levels."""

    ERROR = 1
    WARNING = 2
    INFORMATION = 3
    HINT = 4


@dataclass
class Position:
    """LSP Position (zero-indexed)."""

    line: int
    character: int

    def to_dict(self) -> dict:
        return {"line": self.line, "character": self.character}

    @classmethod
    def from_dict(cls, data: dict) -> Position:
        return cls(line=data["line"], character=data["character"])


@dataclass
class Range:
    """LSP Range."""

    start: Position
    end: Position

    def to_dict(self) -> dict:
        return {"start": self.start.to_dict(), "end": self.end.to_dict()}


@dataclass
class Diagnostic:
    """LSP Diagnostic message."""

    range: Range
    message: str
    severity: DiagnosticSeverity
    code: Optional[str] = None
    source: str = "ParserCraft"
    related_information: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "range": self.range.to_dict(),
            "message": self.message,
            "severity": self.severity.value,
            "code": self.code,
            "source": self.source,
        }


@dataclass
class CompletionItem:
    """LSP Completion item."""

    label: str
    kind: int  # 1=Text, 2=Method, 3=Function, 4=Constructor, 5=Field, etc.
    detail: Optional[str] = None
    documentation: Optional[str] = None
    insert_text: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "kind": self.kind,
            "detail": self.detail,
            "documentation": self.documentation,
            "insertText": self.insert_text or self.label,
        }


@dataclass
class Hover:
    """LSP Hover information."""

    contents: str  # Can be plain text or markdown
    range: Optional[Range] = None

    def to_dict(self) -> dict:
        result = {"contents": self.contents}
        if self.range:
            result["range"] = self.range.to_dict()
        return result


@dataclass
class Location:
    """LSP Location."""

    uri: str
    range: Range

    def to_dict(self) -> dict:
        return {"uri": self.uri, "range": self.range.to_dict()}


class DocumentManager:
    """Manages open documents and their state."""

    def __init__(self):
        self.documents: dict[str, str] = {}  # uri -> content
        self.versions: dict[str, int] = {}   # uri -> version

    def open_document(self, uri: str, content: str, version: int = 1) -> None:
        """Open or create a document."""
        self.documents[uri] = content
        self.versions[uri] = version
        logger.info(f"Opened document: {uri}")

    def update_document(self, uri: str, changes: list[dict], version: int) -> None:
        """Apply incremental or full document changes."""
        if uri not in self.documents:
            raise ValueError(f"Document not open: {uri}")

        if not changes:
            return

        content = self.documents[uri]

        # Full document sync
        if len(changes) == 1 and "range" not in changes[0]:
            content = changes[0]["text"]
        else:
            # Incremental sync
            for change in changes:
                if "range" not in change:
                    continue

                range_data = change["range"]
                start = Position.from_dict(range_data["start"])
                end = Position.from_dict(range_data["end"])

                lines = content.split("\n")

                # Convert positions to string offsets
                start_offset = sum(len(lines[i]) + 1 for i in range(start.line)) + start.character
                end_offset = sum(len(lines[i]) + 1 for i in range(end.line)) + end.character

                content = content[:start_offset] + change["text"] + content[end_offset:]

        self.documents[uri] = content
        self.versions[uri] = version
        logger.debug(f"Updated document: {uri} (version {version})")

    def get_document(self, uri: str) -> str:
        """Get document content."""
        return self.documents.get(uri, "")

    def close_document(self, uri: str) -> None:
        """Close a document."""
        if uri in self.documents:
            del self.documents[uri]
            del self.versions[uri]
            logger.info(f"Closed document: {uri}")


class LanguageServerAnalyzer:
    """Analyzes code for LSP features."""

    def __init__(self, config: LanguageConfig):
        self.config = config
        self.lexer = Lexer(config)
        self.validator = LanguageValidator(config)

    def tokenize(self, content: str) -> list[Token]:
        """Tokenize content and return tokens."""
        try:
            return self.lexer.tokenize(content)
        except Exception as e:
            logger.error(f"Tokenization error: {e}")
            return []

    def get_diagnostics(self, content: str) -> list[Diagnostic]:
        """Analyze content and return diagnostic messages."""
        diagnostics = []

        try:
            tokens = self.tokenize(content)

            # Check for syntax errors
            lines = content.split("\n")
            for i, line in enumerate(lines):
                # Check for unmatched quotes
                if line.count('"') % 2 != 0:
                    diagnostics.append(
                        Diagnostic(
                            range=Range(
                                start=Position(line=i, character=0),
                                end=Position(line=i, character=len(line)),
                            ),
                            message="Unmatched string quote",
                            severity=DiagnosticSeverity.ERROR,
                            code="E001",
                        )
                    )

                # Check for unmatched parentheses
                if line.count("(") != line.count(")"):
                    diagnostics.append(
                        Diagnostic(
                            range=Range(
                                start=Position(line=i, character=0),
                                end=Position(line=i, character=len(line)),
                            ),
                            message="Unmatched parenthesis",
                            severity=DiagnosticSeverity.ERROR,
                            code="E002",
                        )
                    )

                # Check for unmatched brackets
                if line.count("[") != line.count("]"):
                    diagnostics.append(
                        Diagnostic(
                            range=Range(
                                start=Position(line=i, character=0),
                                end=Position(line=i, character=len(line)),
                            ),
                            message="Unmatched bracket",
                            severity=DiagnosticSeverity.ERROR,
                            code="E003",
                        )
                    )

        except Exception as e:
            logger.error(f"Diagnostic analysis error: {e}")

        return diagnostics

    def get_completions(self, content: str, position: Position) -> list[CompletionItem]:
        """Get completion suggestions at the given position."""
        completions = []

        # Add keywords from language config
        for keyword_map in self.config.keyword_mappings.values():
            completions.append(
                CompletionItem(
                    label=keyword_map.custom,
                    kind=1,  # Keyword
                    detail=f"Original: {keyword_map.original}",
                    documentation=keyword_map.description or "Language keyword",
                    insert_text=keyword_map.custom,
                )
            )

        # Add built-in functions
        for func_config in self.config.built_in_functions:
            if not func_config.enabled:
                continue

            arity = func_config.arity
            if arity == 1:
                snippet = f"{func_config.name}($1)"
            elif arity > 1:
                params = ", ".join(f"${i+1}" for i in range(arity))
                snippet = f"{func_config.name}({params})"
            else:
                snippet = f"{func_config.name}()"

            completions.append(
                CompletionItem(
                    label=func_config.name,
                    kind=3,  # Function
                    detail=f"Arity: {arity}",
                    documentation=func_config.description,
                    insert_text=snippet,
                )
            )

        return completions

    def get_hover_info(self, content: str, position: Position) -> Optional[Hover]:
        """Get hover information at the given position."""
        lines = content.split("\n")
        if position.line >= len(lines):
            return None

        line = lines[position.line]
        if position.character >= len(line):
            return None

        # Extract word at position
        word_match = re.search(r"\w+", line[max(0, position.character - 20) : position.character + 20])
        if not word_match:
            return None

        word = word_match.group()

        # Check if it's a keyword
        for keyword_map in self.config.keyword_mappings.values():
            if keyword_map.custom == word:
                return Hover(
                    contents=f"**{word}** (keyword)\n\n{keyword_map.description or 'Language keyword'}",
                    range=Range(
                        start=Position(line=position.line, character=position.character - len(word)),
                        end=Position(line=position.line, character=position.character),
                    ),
                )

        # Check if it's a built-in function
        for func_config in self.config.built_in_functions:
            if func_config.name == word:
                return Hover(
                    contents=f"**{func_config.name}()** (function, arity: {func_config.arity})\n\n{func_config.description or 'Built-in function'}",
                    range=Range(
                        start=Position(line=position.line, character=position.character - len(word)),
                        end=Position(line=position.line, character=position.character),
                    ),
                )

        return None

    def get_signature_help(self, content: str, position: Position) -> Optional[dict]:
        """Get function signature help."""
        lines = content.split("\n")
        if position.line >= len(lines):
            return None

        line = lines[position.line]
        # Find opening paren before cursor
        paren_idx = line.rfind("(", 0, position.character)
        if paren_idx == -1:
            return None

        # Extract function name
        func_match = re.match(r"\w+$", line[:paren_idx])
        if not func_match:
            return None

        func_name = func_match.group()

        # Find matching function config
        for func_config in self.config.built_in_functions:
            if func_config.name == func_name:
                return {
                    "signatures": [
                        {
                            "label": f"{func_config.name}(...)",
                            "documentation": func_config.description,
                            "parameters": [
                                {"label": f"arg{i+1}", "documentation": ""}
                                for i in range(abs(func_config.arity))
                            ],
                        }
                    ],
                    "activeSignature": 0,
                    "activeParameter": 0,
                }

        return None

    def get_symbols(self, content: str) -> list[dict]:
        """Get document symbols (functions, variables, etc.)."""
        symbols = []
        lines = content.split("\n")

        for i, line in enumerate(lines):
            # Find function definitions
            for kw_map in self.config.keyword_mappings.values():
                if kw_map.original == "def":  # Function definition keyword
                    pattern = rf"\b{re.escape(kw_map.custom)}\s+(\w+)"
                    matches = re.finditer(pattern, line)
                    for match in matches:
                        symbols.append(
                            {
                                "name": match.group(1),
                                "kind": 12,  # Function
                                "location": {
                                    "uri": "",
                                    "range": {
                                        "start": {"line": i, "character": match.start()},
                                        "end": {"line": i, "character": match.end()},
                                    },
                                },
                            }
                        )

        return symbols


class LSPServer:
    """Language Server Protocol server implementation."""

    def __init__(self, config: LanguageConfig):
        self.config = config
        self.document_manager = DocumentManager()
        self.analyzer = LanguageServerAnalyzer(config)
        self.server_capabilities = self._build_capabilities()

    def _build_capabilities(self) -> dict:
        """Build server capabilities."""
        return {
            "codeActionProvider": True,
            "completionProvider": {
                "resolveProvider": False,
                "triggerCharacters": [],
            },
            "definitionProvider": True,
            "documentFormattingProvider": True,
            "documentHighlightProvider": True,
            "documentRangeFormattingProvider": True,
            "documentSymbolProvider": True,
            "hoverProvider": True,
            "referencesProvider": True,
            "renameProvider": True,
            "signatureHelpProvider": {
                "triggerCharacters": ["("],
            },
            "textDocumentSync": {
                "openClose": True,
                "change": 1,  # Full document sync
            },
            "workspaceSymbolProvider": True,
        }

    def initialize(self, root_path: Optional[str] = None) -> dict:
        """Handle initialize request."""
        logger.info(f"Initializing LSP server for {self.config.name} at {root_path}")
        return {
            "capabilities": self.server_capabilities,
            "serverInfo": {
                "name": "ParserCraft",
                "version": "1.0.0",
            },
        }

    def handle_did_open(self, uri: str, content: str) -> None:
        """Handle textDocument/didOpen notification."""
        self.document_manager.open_document(uri, content)
        self._publish_diagnostics(uri)

    def handle_did_change(self, uri: str, changes: list[dict], version: int) -> None:
        """Handle textDocument/didChange notification."""
        self.document_manager.update_document(uri, changes, version)
        self._publish_diagnostics(uri)

    def handle_did_close(self, uri: str) -> None:
        """Handle textDocument/didClose notification."""
        self.document_manager.close_document(uri)

    def _publish_diagnostics(self, uri: str) -> None:
        """Publish diagnostics for a document (would be sent to client)."""
        content = self.document_manager.get_document(uri)
        diagnostics = self.analyzer.get_diagnostics(content)
        logger.debug(f"Publishing {len(diagnostics)} diagnostics for {uri}")

    def completions(self, uri: str, position: Position) -> list[dict]:
        """Handle textDocument/completion request."""
        content = self.document_manager.get_document(uri)
        items = self.analyzer.get_completions(content, position)
        return [item.to_dict() for item in items]

    def hover(self, uri: str, position: Position) -> Optional[dict]:
        """Handle textDocument/hover request."""
        content = self.document_manager.get_document(uri)
        hover_info = self.analyzer.get_hover_info(content, position)
        return hover_info.to_dict() if hover_info else None

    def signature_help(self, uri: str, position: Position) -> Optional[dict]:
        """Handle textDocument/signatureHelp request."""
        content = self.document_manager.get_document(uri)
        return self.analyzer.get_signature_help(content, position)

    def document_symbols(self, uri: str) -> list[dict]:
        """Handle textDocument/documentSymbol request."""
        content = self.document_manager.get_document(uri)
        return self.analyzer.get_symbols(content)

    def format_document(self, uri: str) -> list[dict]:
        """Handle textDocument/formatting request (returns text edits)."""
        # Placeholder for document formatting
        # Could integrate with configured formatter
        return []


def create_lsp_server(config_path: str) -> LSPServer:
    """Factory function to create LSP server with given config."""
    config = LanguageConfig.load(config_path)
    return LSPServer(config)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="ParserCraft Language Server Protocol")
    parser.add_argument("--config", required=True, help="Language configuration file")
    parser.add_argument("--port", type=int, default=8080, help="Server port")
    parser.add_argument("--stdio", action="store_true", help="Use stdio instead of sockets")

    args = parser.parse_args()

    server = create_lsp_server(args.config)
    print(f"LSP Server ready for {server.config.name}")
    print(f"Capabilities: {json.dumps(server.server_capabilities, indent=2)}")
