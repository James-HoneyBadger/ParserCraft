#!/usr/bin/env python3
"""
Feature Enhancement Demo

Demonstrates new features added to ParserCraft:
1. Type validation for identifiers
2. Additional language presets
3. Enhanced error messages
4. Documentation generation
5. Advanced validation
"""

import sys
import traceback
from pathlib import Path

from parsercraft.language_config import LanguageConfig
from parsercraft.identifier_validator import IdentifierValidator, ConflictDetector
from parsercraft.documentation_generator import DocumentationGenerator


def demo_identifier_validation():
    """Demo 1: Identifier Validation"""
    print("\n" + "=" * 70)
    print("FEATURE 1: IDENTIFIER VALIDATION")
    print("=" * 70)

    validator = IdentifierValidator()

    # Test valid identifiers
    test_names = [
        "valid_name",
        "CamelCase",
        "PascalCase",
        "valid123",
        "x",  # Short
        "if",  # Reserved
        "123invalid",  # Invalid start
        "invalid-name",  # Invalid characters
    ]

    print("\nValidating identifiers:")
    for name in test_names:
        is_valid, warnings = validator.validate_identifier(name)
        status = "✓" if is_valid else "✗"
        print(f"\n  {status} '{name}'")
        if not is_valid:
            print(f"     Error: {warnings[0]}")
        elif warnings:
            for warning in warnings:
                print(f"     Warning: {warning}")

    # Test naming style detection
    print("\n\nDetecting naming styles:")
    test_styles = ["snake_case", "camelCase", "PascalCase", "SCREAMING_SNAKE", "invalid_123"]
    for name in test_styles:
        style = validator.detect_naming_style(name)
        print(f"  '{name}' -> {style}")

    # Test name suggestions
    print("\n\nSuggesting corrections:")
    invalid_names = ["123var", "my-var", "if", "var$"]
    for name in invalid_names:
        suggestion = validator.suggest_name(name)
        print(f"  '{name}' -> '{suggestion}'")


def demo_new_presets():
    """Demo 2: New Language Presets"""
    print("\n" + "=" * 70)
    print("FEATURE 2: EXPANDED LANGUAGE PRESETS")
    print("=" * 70)

    presets = [
        "python_like",
        "js_like",
        "minimal",
        "ruby_like",
        "golang_like",
        "rust_like",
        "clike",
    ]

    print(f"\nAvailable presets ({len(presets)} total):\n")

    for preset in presets:
        try:
            config = LanguageConfig.from_preset(preset)
            print(f"  ✓ {preset:15} - {config.name:20} ({len(config.keyword_mappings)} keywords)")
        except ValueError as e:
            print(f"  ✗ {preset}: {e}")

    # Show details of a new preset
    print("\n\nRuby-like preset details:")
    ruby_config = LanguageConfig.from_preset("ruby_like")
    print(f"  Name: {ruby_config.name}")
    print(f"  Keywords: {len(ruby_config.keyword_mappings)}")
    print(f"  Functions: {len(ruby_config.builtin_functions)}")

    print("\n  Key mappings:")
    key_mappings = [
        ("if", "when"),
        ("def", "define"),
        ("class", "blueprint"),
    ]
    for orig, expected in key_mappings:
        if orig in ruby_config.keyword_mappings:
            actual = ruby_config.keyword_mappings[orig].custom
            match = "✓" if actual == expected else "✗"
            print(f"    {match} {orig} -> {actual}")


def demo_advanced_validation():
    """Demo 3: Advanced Configuration Validation"""
    print("\n" + "=" * 70)
    print("FEATURE 3: ADVANCED VALIDATION")
    print("=" * 70)

    # Test 1: Conflict detection
    print("\nTest 1: Namespace collision detection")
    config = LanguageConfig()

    # Create a deliberate conflict
    config.builtin_functions["if"] = config.builtin_functions.get(
        "print"
    )  # Same name as keyword
    config.builtin_functions["if"].name = "if"

    detector = ConflictDetector()
    conflicts = detector.find_namespace_collisions(
        config.keyword_mappings,
        config.builtin_functions,
        config.operators,
    )

    if conflicts:
        print(f"  Found {len(conflicts)} namespace collision(s):")
        for name, collision_type, issue_type in conflicts[:3]:
            print(f"    - '{name}': {collision_type} {issue_type}")
    else:
        print("  ✓ No namespace collisions detected")

    # Test 2: Operator precedence validation
    print("\nTest 2: Operator precedence validation")
    config = LanguageConfig()
    issues = detector.check_operator_precedence_consistency(config.operators)

    if issues:
        print(f"  Found {len(issues)} precedence issue(s):")
        for issue in issues:
            print(f"    - {issue}")
    else:
        print("  ✓ All operator precedences valid")


def demo_documentation_generation():
    """Demo 4: Auto-generate Documentation"""
    print("\n" + "=" * 70)
    print("FEATURE 4: DOCUMENTATION GENERATION")
    print("=" * 70)

    # Generate docs for a custom config
    config = LanguageConfig()
    config.name = "Educational Language"
    config.version = "2.0.0"
    config.description = "A language for teaching programming concepts"
    config.author = "ParserCraft Team"

    # Customize some keywords
    config.rename_keyword("if", "cuando")
    config.rename_keyword("while", "mientras")

    print("\nGenerating Markdown documentation...")
    markdown_doc = DocumentationGenerator.generate_markdown(config)

    # Save it
    output_md = Path("language_reference.md")
    DocumentationGenerator.save_markdown(config, str(output_md))
    print(f"  ✓ Saved to: {output_md}")
    print(f"  ✓ Document size: {len(markdown_doc)} characters")

    # Show snippet
    print("\n  Markdown preview (first 300 chars):")
    print(f"  {markdown_doc[:300]}...")

    print("\nGenerating HTML documentation...")
    output_html = Path("language_reference.html")
    DocumentationGenerator.save_html(config, str(output_html))
    print(f"  ✓ Saved to: {output_html}")

    # Cleanup
    output_md.unlink(missing_ok=True)
    output_html.unlink(missing_ok=True)


def demo_enhanced_validation():
    """Demo 5: Enhanced Configuration Validation"""
    print("\n" + "=" * 70)
    print("FEATURE 5: ENHANCED ERROR MESSAGES")
    print("=" * 70)

    config = LanguageConfig()

    print("\nValidating custom keyword names:")

    test_names = [
        ("valid_keyword", True),
        ("if", False),  # Reserved
        ("123_invalid", False),  # Invalid start
        ("short_kw", True),
    ]

    for name, _expected in test_names:
        try:
            if name not in config.keyword_mappings:
                config.add_keyword(name, category="test")
            else:
                config.rename_keyword(name, name + "_custom")
            print(f"  ✓ '{name}' - Added successfully")
        except ValueError as e:
            print(f"  ✗ '{name}' - {e}")


def main():
    """Run all demos."""
    print("=" * 70)
    print("PARSERCRAFT - FEATURE ENHANCEMENTS DEMONSTRATION")
    print("=" * 70)

    demos = [
        demo_identifier_validation,
        demo_new_presets,
        demo_advanced_validation,
        demo_documentation_generation,
        demo_enhanced_validation,
    ]

    for demo in demos:
        try:
            demo()
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"\n✗ Error in {demo.__name__}: {e}")
            traceback.print_exc()

    print("\n" + "=" * 70)
    print("✅ FEATURE DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\nNew features implemented:")
    print("  ✓ Type validation for identifiers")
    print("  ✓ 4 additional language presets (Ruby, Go, Rust, C)")
    print("  ✓ Advanced namespace collision detection")
    print("  ✓ Auto-generated documentation (Markdown + HTML)")
    print("  ✓ Enhanced validation with helpful error messages")
    print("\nNext steps:")
    print("  - Use presets: LanguageConfig.from_preset('ruby_like')")
    print("  - Generate docs: DocumentationGenerator.save_markdown(config, 'docs.md')")
    print("  - Validate identifiers: IdentifierValidator.validate_identifier(name)")


if __name__ == "__main__":
    sys.exit(main() or 0)
