"""
Language Construction Set

This module provides a comprehensive configuration system that allows users to:
    - Rename commands and keywords
    - Add/remove/modify built-in functions
    - Customize syntax options and operators
    - Create language variants and dialects
    - Export/import language configurations

Features:
    - YAML/JSON configuration files for easy editing
    - Hot-reloading of language definitions
    - Validation of configuration consistency
    - Backwards compatibility mode
    - Language preset library (Python-like, JavaScript-like, etc.)

Usage:
    # Create a custom language variant
    config = LanguageConfig()
    config.rename_keyword("if", "si")  # Spanish-like
    config.rename_keyword("when", "cuando")
    config.save("spanish_config.yaml")
"""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional, Union

# Optional YAML support
try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    yaml = None  # type: ignore[assignment]


@dataclass
class KeywordMapping:
    """Maps original keyword to custom name."""

    original: str
    custom: str
    category: str = "general"  # general, control, function, satirical, etc.
    description: str = ""


@dataclass
class FunctionConfig:
    """Configuration for a built-in function."""

    name: str
    arity: int  # Number of arguments (-1 for variadic)
    implementation: Optional[str] = None  # Python code as string, or reference
    description: str = ""
    enabled: bool = True
    min_args: int = -1
    max_args: int = -1
    alias: Optional[str] = None


@dataclass
class OperatorConfig:
    """Configuration for operators."""

    symbol: str
    precedence: int
    associativity: str = "left"  # left, right, none
    enabled: bool = True


@dataclass
class ParsingConfig:
    """Deep parsing and syntax customization.

    This allows creating entirely new language syntaxes.
    """

    # Delimiters
    block_start: str = "{"
    block_end: str = "}"
    list_start: str = "["
    list_end: str = "]"
    tuple_start: str = "("
    tuple_end: str = ")"
    dict_start: str = "{"
    dict_end: str = "}"

    # Separators
    statement_separator: str = ";"
    parameter_separator: str = ","
    key_value_separator: str = ":"

    # String literals
    string_delimiters: list[str] = field(default_factory=lambda: ['"', "'", '"""'])
    escape_character: str = "\\"
    allow_raw_strings: bool = True
    raw_string_prefix: str = "r"

    # Expression syntax
    member_access: str = "."
    index_access_start: str = "["
    index_access_end: str = "]"
    function_call_start: str = "("
    function_call_end: str = ")"

    # Control flow syntax
    if_then_separator: Optional[str] = None
    else_keyword: str = "else"
    elif_keyword: str = "elif"

    # Function definition syntax
    function_param_start: str = "("
    function_param_end: str = ")"
    function_arrow: Optional[str] = None
    return_type_separator: Optional[str] = None

    # Class definition syntax
    class_inheritance_separator: str = ":"
    class_body_start: str = "{"
    class_body_end: str = "}"

    # Import/Export syntax
    import_separator: str = "."
    from_keyword: str = "from"
    as_keyword: str = "as"

    # Custom parse transforms
    allow_custom_operators: bool = True
    allow_operator_overloading: bool = True


@dataclass
class SyntaxOptions:
    """General syntax configuration options."""

    # Array indexing
    array_start_index: int = -1  # -1 for Gulf of Mexico style, 0 for traditional
    allow_fractional_indexing: bool = True

    # String quoting
    flexible_quoting: bool = True
    string_interpolation: bool = True
    interpolation_symbol: str = "$"

    # Comments
    single_line_comment: str = "//"
    multi_line_comment_start: Optional[str] = None
    multi_line_comment_end: Optional[str] = None

    # Statement terminators
    require_semicolons: bool = False
    statement_terminator: str = "!"  # Gulf of Mexico uses ! or newline

    # Type system
    three_valued_logic: bool = True  # true/false/maybe
    probabilistic_variables: bool = True
    temporal_variables: bool = True

    # Special features
    enable_satirical_keywords: bool = True
    enable_quantum_features: bool = True
    enable_time_travel: bool = True
    enable_gaslighting: bool = True


@dataclass
class LanguageConfig:
    """Complete language configuration.

    This class provides a comprehensive way to customize a language's
    syntax, keywords, functions, and behavior.
    """

    # Metadata
    name: str = "Custom Language"
    version: str = "3.0.0"
    description: str = "A customizable programming language"
    author: str = ""
    target_interpreter: str = "python"

    # Configuration sections
    keyword_mappings: dict[str, KeywordMapping] = field(default_factory=dict)
    builtin_functions: dict[str, FunctionConfig] = field(default_factory=dict)
    operators: dict[str, OperatorConfig] = field(default_factory=dict)
    syntax_options: SyntaxOptions = field(default_factory=SyntaxOptions)
    parsing_config: ParsingConfig = field(default_factory=ParsingConfig)

    # Runtime options
    debug_mode: bool = False
    strict_mode: bool = False
    compatibility_mode: str = "standard"

    def __post_init__(self):
        """Initialize with default configuration if empty."""
        if not self.keyword_mappings:
            self._load_default_keywords()
        if not self.builtin_functions:
            self._load_default_functions()
        if not self.operators:
            self._load_default_operators()

    def _load_default_keywords(self):
        """Load default keywords."""
        default_keywords = {
            # Control flow
            "if": KeywordMapping("if", "if", "control", "Conditional statement"),
            "else": KeywordMapping("else", "else", "control", "Else clause"),
            "elif": KeywordMapping("elif", "elif", "control", "Else-if clause"),
            "while": KeywordMapping("while", "while", "control", "While loop"),
            "for": KeywordMapping("for", "for", "control", "For loop"),
            "break": KeywordMapping("break", "break", "control", "Break statement"),
            "continue": KeywordMapping(
                "continue", "continue", "control", "Continue statement"
            ),
            "pass": KeywordMapping("pass", "pass", "control", "Pass statement"),
            "when": KeywordMapping("when", "when", "control", "Reactive programming"),
            # Functions and definitions
            "def": KeywordMapping("def", "def", "function", "Function definition"),
            "function": KeywordMapping(
                "function", "function", "function", "Function definition"
            ),
            "return": KeywordMapping("return", "return", "function", "Return value"),
            "lambda": KeywordMapping(
                "lambda", "lambda", "function", "Lambda expression"
            ),
            "yield": KeywordMapping("yield", "yield", "function", "Yield statement"),
            # Exception handling
            "try": KeywordMapping("try", "try", "exception", "Try block"),
            "except": KeywordMapping(
                "except", "except", "exception", "Exception handler"
            ),
            "finally": KeywordMapping(
                "finally", "finally", "exception", "Finally block"
            ),
            # Imports and modules
            "import": KeywordMapping("import", "import", "import", "Import module"),
            "from": KeywordMapping("from", "from", "import", "From import"),
            "as": KeywordMapping("as", "as", "import", "Import alias"),
            # Context management
            "with": KeywordMapping("with", "with", "context", "Context manager"),
            # Variables and constants
            "const": KeywordMapping(
                "const", "const", "variable", "Constant declaration"
            ),
            "var": KeywordMapping("var", "var", "variable", "Variable declaration"),
            # Object-oriented
            "class": KeywordMapping("class", "class", "oop", "Class definition"),
            # Logical operators (often used as keywords)
            "and": KeywordMapping("and", "and", "logic", "Logical AND"),
            "or": KeywordMapping("or", "or", "logic", "Logical OR"),
            "not": KeywordMapping("not", "not", "logic", "Logical NOT"),
            # Common keywords in other languages
            "let": KeywordMapping("let", "let", "variable", "Variable declaration"),
            "then": KeywordMapping("then", "then", "control", "Then clause"),
        }
        self.keyword_mappings = default_keywords

    def _load_default_functions(self):
        """Load default built-in functions."""
        default_functions = {
            "print": FunctionConfig("print", -1, "builtin.print", "Print to stdout"),
            "Number": FunctionConfig(
                "Number", 1, "builtin.to_number", "Convert to number"
            ),
            "String": FunctionConfig(
                "String", 1, "builtin.to_string", "Convert to string"
            ),
            "Boolean": FunctionConfig(
                "Boolean", 1, "builtin.to_boolean", "Convert to boolean"
            ),
            "List": FunctionConfig("List", -1, "builtin.list", "Create list"),
        }
        self.builtin_functions = default_functions

    def _load_default_operators(self):
        """Load default operators with precedence."""
        default_operators = {
            "+": OperatorConfig("+", 10, "left"),
            "-": OperatorConfig("-", 10, "left"),
            "*": OperatorConfig("*", 20, "left"),
            "/": OperatorConfig("/", 20, "left"),
            "==": OperatorConfig("==", 5, "none"),
            "!=": OperatorConfig("!=", 5, "none"),
            ">": OperatorConfig(">", 5, "none"),
            "<": OperatorConfig("<", 5, "none"),
            ">=": OperatorConfig(">=", 5, "none"),
            "<=": OperatorConfig("<=", 5, "none"),
            "=": OperatorConfig("=", 1, "right"),
        }
        self.operators = default_operators

    # === Keyword Management ===

    def rename_keyword(self, original: str, new_name: str) -> None:
        """Rename a keyword with validation."""
        if original not in self.keyword_mappings:
            raise ValueError(f"Keyword '{original}' not found")

        # Validate new name
        from .identifier_validator import IdentifierValidator

        is_valid, warnings = IdentifierValidator.validate_identifier(
            new_name, allow_reserved=True, allow_symbols=True
        )
        if not is_valid:
            raise ValueError(f"Invalid keyword name '{new_name}': {warnings[0]}")

        self.keyword_mappings[original].custom = new_name

    def add_keyword(
        self, name: str, category: str = "custom", description: str = ""
    ) -> None:
        """Add a new custom keyword with validation."""
        from .identifier_validator import IdentifierValidator

        # Validate name
        is_valid, warnings = IdentifierValidator.validate_identifier(
            name, allow_reserved=True, allow_symbols=True
        )
        if not is_valid:
            raise ValueError(f"Invalid keyword name '{name}': {warnings[0]}")

        self.keyword_mappings[name] = KeywordMapping(name, name, category, description)

    def remove_keyword(self, name: str) -> None:
        """Remove a keyword."""
        if name not in self.keyword_mappings:
            raise ValueError(f"Keyword '{name}' not found")
        del self.keyword_mappings[name]

    def disable_satirical_keywords(self) -> None:
        """Disable all satirical keywords (for serious mode)."""
        satirical_keywords = [
            keyword
            for keyword, mapping in self.keyword_mappings.items()
            if mapping.category == "satirical"
        ]
        for keyword in satirical_keywords:
            self.remove_keyword(keyword)
        self.syntax_options.enable_satirical_keywords = False

    # === Function Management ===

    def add_function(
        self,
        name: str,
        alias_or_arity: Union[str, int, None] = None,
        implementation: Optional[str] = None,
        description: str = "",
        min_args: int = -1,
        max_args: int = -1,
    ) -> None:
        """Add a custom built-in function.

        Arguments:
            name: Internal name or implementation reference (e.g., 'print')
            alias_or_arity: Function arity (int) OR exposed name (str)
            implementation: Python implementation path (optional)
            description: Function help text
            min_args: Minimum arguments
            max_args: Maximum arguments
        """
        exposed_name = name
        arity = -1

        if alias_or_arity is not None:
            if isinstance(alias_or_arity, str):
                exposed_name = alias_or_arity
                # If implementation missing, assume internal name maps to builtin.{name}
                if implementation is None:
                    implementation = f"builtin.{name}"
            else:
                arity = alias_or_arity

        # Use max_args as arity if not specified
        if arity == -1 and max_args != -1:
            arity = max_args

        self.builtin_functions[exposed_name] = FunctionConfig(
            name=exposed_name,
            arity=arity,
            implementation=implementation,
            description=description,
            enabled=True,
            min_args=min_args,
            max_args=max_args,
            alias=name if exposed_name != name else None
        )

    def rename_function(self, original: str, new_name: str) -> None:
        """Rename a built-in function."""
        if original not in self.builtin_functions:
            raise ValueError(f"Function '{original}' not found")
        func_config = self.builtin_functions[original]
        del self.builtin_functions[original]
        func_config.name = new_name
        self.builtin_functions[new_name] = func_config

    def remove_function(self, name: str) -> None:
        """Remove a built-in function."""
        if name not in self.builtin_functions:
            raise ValueError(f"Function '{name}' not found")
        del self.builtin_functions[name]

    # === Syntax Options ===

    def set_array_indexing(
        self, start_index: int, allow_fractional: bool = True
    ) -> None:
        """Configure array indexing behavior."""
        self.syntax_options.array_start_index = start_index
        self.syntax_options.allow_fractional_indexing = allow_fractional

    def set_comment_style(
        self,
        single_line: str = "//",
        multi_start: Optional[str] = None,
        multi_end: Optional[str] = None,
    ) -> None:
        """Configure comment syntax."""
        self.syntax_options.single_line_comment = single_line
        self.syntax_options.multi_line_comment_start = multi_start
        self.syntax_options.multi_line_comment_end = multi_end

    def enable_feature(self, feature: str, enabled: bool = True) -> None:
        """Enable or disable special language features."""
        feature_map = {
            "satirical": "enable_satirical_keywords",
            "quantum": "enable_quantum_features",
            "time_travel": "enable_time_travel",
            "gaslighting": "enable_gaslighting",
            "three_valued_logic": "three_valued_logic",
            "probabilistic": "probabilistic_variables",
            "temporal": "temporal_variables",
        }
        if feature in feature_map:
            setattr(self.syntax_options, feature_map[feature], enabled)
        else:
            raise ValueError(f"Unknown feature: {feature}")

    # === Presets ===

    @classmethod
    def from_preset(cls, preset_name: str) -> LanguageConfig:
        """Load a preset language configuration."""
        config = cls()

        if preset_name == "python_like":
            config.name = "Python-like"
            # Remove 'function' since 'def' is the Python standard
            config.remove_keyword("function")
            config.set_array_indexing(0, False)
            config.syntax_options.statement_terminator = ""
            config.syntax_options.require_semicolons = False
            config.disable_satirical_keywords()

        elif preset_name == "js_like":
            config.name = "JavaScript-like"
            config.set_array_indexing(0, False)
            config.syntax_options.statement_terminator = ";"
            config.syntax_options.require_semicolons = True
            config.disable_satirical_keywords()

        elif preset_name == "minimal":
            config.name = "Minimal"
            config.description = "Minimal feature set"
            config.disable_satirical_keywords()
            essential = {"print", "Number", "String", "Boolean", "List"}
            for func_name in list(config.builtin_functions.keys()):
                if func_name not in essential:
                    config.remove_function(func_name)

        elif preset_name == "ruby_like":
            config.name = "Ruby-like"
            config.description = "Ruby-inspired syntax for educational purposes"
            config.remove_keyword("function")
            config.rename_keyword("def", "define")
            config.rename_keyword("class", "blueprint")
            config.rename_keyword("if", "when")
            config.rename_keyword("else", "otherwise")
            config.rename_keyword("while", "loop_while")
            config.set_array_indexing(0, False)
            config.disable_satirical_keywords()

        elif preset_name == "golang_like":
            config.name = "Go-like"
            config.description = "Go/Golang-inspired syntax"
            config.remove_keyword("function")
            config.rename_keyword("def", "func")
            config.rename_keyword("class", "type")
            config.rename_keyword("return", "return")
            config.set_array_indexing(0, False)
            config.syntax_options.statement_terminator = ""
            config.disable_satirical_keywords()

        elif preset_name == "rust_like":
            config.name = "Rust-like"
            config.description = "Rust-inspired syntax for systems programming"
            config.remove_keyword("function")
            config.rename_keyword("def", "fn")
            config.rename_keyword("const", "const")
            config.rename_keyword("var", "let")
            config.rename_keyword("class", "struct")
            config.set_array_indexing(0, False)
            config.disable_satirical_keywords()

        elif preset_name == "clike":
            config.name = "C-like"
            config.description = "C/C++-inspired syntax"
            config.remove_keyword("function")
            config.rename_keyword("def", "void")
            config.rename_keyword("class", "struct")
            config.rename_keyword("if", "if")
            config.set_array_indexing(0, False)
            config.syntax_options.statement_terminator = ";"
            config.syntax_options.require_semicolons = True
            config.disable_satirical_keywords()

        elif preset_name == "functional":
            config.name = "Functional Lambda"
            config.description = "A functional language based on lambda calculus"
            config.rename_keyword("if", "cond")
            config.rename_keyword("def", "define")
            config.rename_keyword("lambda", "lambda")
            config.rename_keyword("let", "let")
            config.set_array_indexing(0, False)
            config.syntax_options.statement_terminator = ""
            config.disable_satirical_keywords()
            # Add functional-specific operators if needed, or rely on functions

        elif preset_name == "lisp_like":
            config.name = "Lisp-like"
            config.description = "Lisp-inspired parenthesized syntax"
            config.rename_keyword("if", "if")
            config.rename_keyword("def", "def")
            config.rename_keyword("lambda", "lambda")
            config.set_array_indexing(0, False)
            config.syntax_options.statement_terminator = ""
            config.syntax_options.function_call_start = "("
            config.syntax_options.function_call_end = ")"
            config.syntax_options.block_start = "("
            config.syntax_options.block_end = ")"
            config.disable_satirical_keywords()

        elif preset_name == "basic_like":
            config.name = "BASIC-like"
            config.description = "BASIC-inspired syntax"
            config.rename_keyword("if", "IF")
            config.rename_keyword("else", "ELSE")
            config.rename_keyword("for", "FOR")
            config.rename_keyword("while", "WHILE")
            # print is a function, not a keyword
            config.rename_function("print", "PRINT")
            config.rename_keyword("def", "DEF")
            config.rename_keyword("return", "RETURN")
            config.set_array_indexing(1, False)
            config.syntax_options.statement_terminator = ""
            config.disable_satirical_keywords()

        else:
            raise ValueError(f"Unknown preset: {preset_name}")

        return config

    # === Validation ===

    def validate(self) -> list[str]:
        """Validate configuration for consistency."""
        errors = []

        # Check for duplicate custom names
        custom_names = [m.custom for m in self.keyword_mappings.values()]
        duplicates = [name for name in custom_names if custom_names.count(name) > 1]
        if duplicates:
            errors.append(f"Duplicate keyword names: {set(duplicates)}")

        # Check function arities
        for name, func in self.builtin_functions.items():
            if func.arity < -1:
                errors.append(f"Function '{name}' has invalid arity: {func.arity}")

        # Check operator precedences
        for symbol, op in self.operators.items():
            if op.precedence < 0:
                errors.append(
                    f"Operator '{symbol}' has invalid precedence: {op.precedence}"  # noqa: E501
                )
            if op.associativity not in ["left", "right", "none"]:
                errors.append(
                    f"Operator '{symbol}' has invalid associativity: {op.associativity}"  # noqa: E501 pylint: disable=line-too-long
                )

        return errors

    # === Serialization ===

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "metadata": {
                "name": self.name,
                "version": self.version,
                "description": self.description,
                "author": self.author,
                "target_interpreter": self.target_interpreter,
            },
            "keywords": {k: asdict(v) for k, v in self.keyword_mappings.items()},
            "functions": {k: asdict(v) for k, v in self.builtin_functions.items()},
            "operators": {k: asdict(v) for k, v in self.operators.items()},
            "syntax_options": asdict(self.syntax_options),
            "parsing_config": asdict(self.parsing_config),
            "runtime": {
                "debug_mode": self.debug_mode,
                "strict_mode": self.strict_mode,
                "compatibility_mode": self.compatibility_mode,
            },
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LanguageConfig:
        """Create configuration from dictionary."""
        config = cls()

        if "metadata" in data:
            config.name = data["metadata"].get("name", config.name)
            config.version = data["metadata"].get("version", config.version)
            config.description = data["metadata"].get("description", config.description)
            config.author = data["metadata"].get("author", config.author)

        if "keywords" in data:
            config.keyword_mappings = {
                k: KeywordMapping(**v) for k, v in data["keywords"].items()
            }

        if "functions" in data:
            config.builtin_functions = {
                k: FunctionConfig(**v) for k, v in data["functions"].items()
            }

        if "operators" in data:
            config.operators = {
                k: OperatorConfig(**v) for k, v in data["operators"].items()
            }

        if "syntax_options" in data:
            config.syntax_options = SyntaxOptions(**data["syntax_options"])

        if "parsing_config" in data:
            config.parsing_config = ParsingConfig(**data["parsing_config"])

        if "runtime" in data:
            config.debug_mode = data["runtime"].get("debug_mode", False)
            config.strict_mode = data["runtime"].get("strict_mode", False)
            config.compatibility_mode = data["runtime"].get(
                "compatibility_mode", "standard"
            )

        return config

    def save(self, filepath: Union[str, Path], format: str = "auto") -> None:
        """Save configuration to file."""
        filepath = Path(filepath)

        if format == "auto":
            format = "yaml" if filepath.suffix in [".yaml", ".yml"] else "json"

        if format == "yaml" and not YAML_AVAILABLE:
            print("Warning: YAML not available, falling back to JSON")
            format = "json"
            filepath = filepath.with_suffix(".json")

        data = self.to_dict()

        with open(filepath, "w") as f:
            if format == "yaml":
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)
            else:
                json.dump(data, f, indent=2)

        print(f"Configuration saved to {filepath}")

    @classmethod
    def load(cls, filepath: Union[str, Path]) -> "LanguageConfig":
        """Load configuration from file."""
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"Config file not found: {filepath}")

        with open(filepath, "r") as f:
            if filepath.suffix in [".yaml", ".yml"] and YAML_AVAILABLE:
                data = yaml.safe_load(f)
            else:
                data = json.load(f)

        return cls.from_dict(data)
    
    @classmethod
    def from_json(cls, json_str: str) -> "LanguageConfig":
        """Create configuration from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)

    def to_json(self) -> str:
        """Export configuration as JSON string."""
        return json.dumps(self.to_dict(), indent=2)

    def to_yaml(self) -> str:
        """Export configuration as YAML string."""
        if YAML_AVAILABLE:
            return yaml.dump(self.to_dict(), default_flow_style=False, sort_keys=False)
        raise ImportError("PyYAML is not installed")

    @classmethod
    def load(cls, filepath: Union[str, Path]) -> LanguageConfig:
        """Load configuration from file."""
        filepath = Path(filepath)

        is_yaml = filepath.suffix in [".yaml", ".yml"]
        if is_yaml and not YAML_AVAILABLE:
            raise ImportError(
                "YAML support not available. Install with: pip install pyyaml"
            )

        with open(filepath, "r") as f:
            if is_yaml:
                data = yaml.safe_load(f)
            else:
                data = json.load(f)

        return cls.from_dict(data)

    @classmethod
    def load_preset(cls, preset_name: str) -> "LanguageConfig":
        """Compatibility helper that proxies to ``from_preset``.

        The IDE historically expected a ``load_preset`` classmethod.  Pylint
        flagged its absence, so we delegate to :meth:`from_preset` to keep the
        public surface area intuitive while avoiding duplicated logic.
        """

        return cls.from_preset(preset_name)

    # === CRUD Operations ===

    def update(self, updates: dict[str, Any], merge: bool = True) -> None:
        """Update configuration with new values."""
        if "metadata" in updates:
            meta = updates["metadata"]
            if "name" in meta:
                self.name = meta["name"]
            if "version" in meta:
                self.version = meta["version"]
            if "description" in meta:
                self.description = meta["description"]
            if "author" in meta:
                self.author = meta["author"]

        if "keywords" in updates:
            if merge:
                for key, value in updates["keywords"].items():
                    if isinstance(value, dict):
                        self.keyword_mappings[key] = KeywordMapping(**value)
            else:
                self.keyword_mappings = {
                    k: KeywordMapping(**v) for k, v in updates["keywords"].items()
                }

        if "syntax_options" in updates:
            if merge:
                for key, value in updates["syntax_options"].items():
                    if hasattr(self.syntax_options, key):
                        setattr(self.syntax_options, key, value)
            else:
                self.syntax_options = SyntaxOptions(**updates["syntax_options"])

    def delete_keyword(self, keyword: str) -> bool:
        """Delete a keyword mapping."""
        if keyword in self.keyword_mappings:
            del self.keyword_mappings[keyword]
            return True
        return False

    def delete_function(self, function_name: str) -> bool:
        """Delete a function configuration."""
        if function_name in self.builtin_functions:
            del self.builtin_functions[function_name]
            return True
        return False

    def clone(self) -> "LanguageConfig":
        """Create a deep copy of this configuration."""
        return deepcopy(self)

    @property
    def keywords(self) -> dict[str, KeywordMapping]:
        """Backward-compatible access to keyword mappings."""
        return self.keyword_mappings

    @keywords.setter
    def keywords(self, value: dict[str, KeywordMapping]) -> None:
        """Allow legacy code to assign keyword mappings."""
        self.keyword_mappings = value

    def delete_operator(self, operator_symbol: str) -> bool:
        """Delete an operator configuration if it exists."""
        if operator_symbol in self.operators:
            del self.operators[operator_symbol]
            return True
        return False

    def merge(self, other: "LanguageConfig", prefer_other: bool = True) -> None:
        """Merge another configuration into this one."""
        if prefer_other or not self.name:
            self.name = other.name
        if prefer_other or not self.version:
            self.version = other.version

        for key, mapping in other.keyword_mappings.items():
            if prefer_other or key not in self.keyword_mappings:
                self.keyword_mappings[key] = deepcopy(mapping)

        for key, func in other.builtin_functions.items():
            if prefer_other or key not in self.builtin_functions:
                self.builtin_functions[key] = deepcopy(func)

    def export_mapping_table(self, filepath: Optional[Union[str, Path]] = None) -> str:
        """Export keyword/function mapping table for documentation."""
        lines = ["# Language Configuration Mapping\n"]
        lines.append(f"**Language:** {self.name}\n")
        lines.append(f"**Version:** {self.version}\n\n")

        lines.append("## Keywords\n")
        lines.append("| Original | Custom | Category | Description |")
        lines.append("|----------|--------|----------|-------------|")
        for original, mapping in sorted(self.keyword_mappings.items()):
            lines.append(
                f"| `{mapping.original}` | `{mapping.custom}` | {mapping.category} | {mapping.description} |"  # noqa: E501 pylint: disable=line-too-long
            )

        lines.append("\n## Built-in Functions\n")
        lines.append("| Name | Arity | Description | Enabled |")
        lines.append("|------|-------|-------------|---------|")
        for name, func in sorted(self.builtin_functions.items()):
            arity_str = "variadic" if func.arity == -1 else str(func.arity)
            enabled_str = "✓" if func.enabled else "✗"
            lines.append(
                f"| `{func.name}` | {arity_str} | {func.description} | {enabled_str} |"  # noqa: E501 pylint: disable=line-too-long
            )

        result = "\n".join(lines)

        if filepath:
            with open(filepath, "w") as f:
                f.write(result)
            print(f"Mapping table exported to {filepath}")

        return result

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"LanguageConfig(name='{self.name}', "
            f"keywords={len(self.keyword_mappings)}, "
            f"functions={len(self.builtin_functions)}, "
            f"operators={len(self.operators)})"
        )


# === Helper Functions ===


def list_presets() -> list[str]:
    """Get list of available presets."""
    return [
        "python_like",
        "js_like",
        "minimal",
        "ruby_like",
        "golang_like",
        "rust_like",
        "clike",
    ]


def create_custom_config_interactive() -> LanguageConfig:
    """Interactive configuration builder (CLI)."""
    print("=== Language Configuration Builder ===\n")

    config = LanguageConfig()

    print("Start from a preset? (y/n): ", end="")
    if input().lower() == "y":
        print(f"Available presets: {', '.join(list_presets())}")
        print("Preset name: ", end="")
        preset = input().strip()
        try:
            config = LanguageConfig.from_preset(preset)
            print(f"Loaded preset: {preset}\n")
        except ValueError:
            print("Invalid preset, starting from default\n")

    print(f"Language name [{config.name}]: ", end="")
    name = input().strip()
    if name:
        config.name = name

    print("\nConfiguration complete!")
    print(config)

    return config


if __name__ == "__main__":
    # Demo usage
    print("=== Language Configuration Demo ===\n")

    config = LanguageConfig()
    print(f"Default: {config}\n")

    # Customizations
    config.rename_keyword("if", "when_condition")
    config.rename_function("print", "output")
    config.set_array_indexing(0, False)

    # Save to file
    config.save("custom_language.json")

    # Load preset
    python_like = LanguageConfig.from_preset("python_like")
    print(f"Python-like preset: {python_like}\n")

    # Validate
    errors = config.validate()
    print(f"Validation: {'OK' if not errors else errors}\n")
