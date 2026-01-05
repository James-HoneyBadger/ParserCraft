#!/usr/bin/env python3
"""
Demo: ParserCraft Language Construction Framework

This demo shows how to use ParserCraft
to create custom language configurations.
"""

from parsercraft.language_config import LanguageConfig
from parsercraft.language_runtime import LanguageRuntime, print_language_info


def demo_basic_usage():
    """Demo 1: Basic configuration usage."""
    print("\n" + "=" * 70)
    print("DEMO 1: Basic Configuration Usage")
    print("=" * 70)

    # Create a new configuration
    config = LanguageConfig(
        name="My Custom Language",
        version="2.0",
        description="A custom language variant",
    )

    # Rename some keywords
    config.rename_keyword("if", "when")
    config.rename_keyword("function", "def")
    config.rename_keyword("return", "give")

    # Customize syntax
    config.set_array_indexing(0, False)  # 0-based, no fractional

    print("\nCreated configuration:")
    print(f"  Name: {config.name}")
    print(f"  Keywords: {len(config.keyword_mappings)}")
    print(f"  Syntax: array starts at " f"{config.syntax_options.array_start_index}")

    # Save
    config.save("demo_basic.json")
    print("\n✓ Saved to demo_basic.json")


def demo_presets():
    """Demo 2: Using presets."""
    print("\n" + "=" * 70)
    print("DEMO 2: Using Presets")
    print("=" * 70)

    # Load from preset
    python_like = LanguageConfig.from_preset("python_like")
    print(f"\nLoaded preset: {python_like.name}")
    print(f"  Description: {python_like.description}")
    print(f"  Keywords: {len(python_like.keyword_mappings)}")

    # Customize further
    python_like.name = "Python-Like Custom"
    python_like.rename_keyword("class", "blueprint")

    # Save customized version
    python_like.save("demo_python_custom.yaml")
    print("\n✓ Saved customized preset to demo_python_custom.yaml")


def demo_runtime():
    """Demo 3: Runtime integration."""
    print("\n" + "=" * 70)
    print("DEMO 3: Runtime Integration")
    print("=" * 70)

    # Create and load configuration
    config = LanguageConfig()
    config.rename_keyword("if", "si")
    config.rename_keyword("while", "mientras")

    LanguageRuntime.load_config(config)
    print("\nLoaded configuration into runtime")

    # Test keyword translation
    print("\nKeyword translation:")
    print(f"  'si' translates to: {LanguageRuntime.translate_keyword('si')}")
    print(
        f"  'mientras' translates to: "
        f"{LanguageRuntime.translate_keyword('mientras')}"
    )

    # Check features
    print("\nFeature status:")
    print(f"  Array start index: {LanguageRuntime.get_array_start_index()}")
    print(f"  Satirical enabled: " f"{LanguageRuntime.is_feature_enabled('satirical')}")

    # Show runtime info
    print_language_info()


def demo_crud_operations():
    """Demo 4: CRUD operations."""
    print("\n" + "=" * 70)
    print("DEMO 4: CRUD Operations")
    print("=" * 70)

    config = LanguageConfig()

    # Create
    config.add_keyword("test_keyword", category="testing", description="Test keyword")
    print("\n✓ Added keyword: test_keyword -> test_keyword")

    # Read
    mapping = config.keyword_mappings.get("test_keyword")
    if mapping:
        print(f"  Read: {mapping.original} -> {mapping.custom}")

    # Update
    config.rename_keyword("test_keyword", "examen")
    print("✓ Updated: test_keyword -> examen")

    # Delete
    config.remove_keyword("test_keyword")
    print("✓ Deleted: test_keyword")


def demo_validation():
    """Demo 5: Configuration validation."""
    print("\n" + "=" * 70)
    print("DEMO 5: Configuration Validation")
    print("=" * 70)

    # Valid configuration
    config = LanguageConfig()
    errors = config.validate()
    print(f"\nValid config? {len(errors) == 0}")

    # Create invalid configuration
    bad_config = LanguageConfig()
    bad_config.rename_keyword("if", "test")
    bad_config.rename_keyword("while", "test")  # Duplicate!

    errors = bad_config.validate()
    if errors:
        print(f"\nInvalid config found {len(errors)} errors:")
        for error in errors:
            print(f"  • {error}")


def demo_serialization():
    """Demo 6: Serialization."""
    print("\n" + "=" * 70)
    print("DEMO 6: Serialization (JSON/YAML)")
    print("=" * 70)

    config = LanguageConfig()
    config.rename_keyword("if", "cuando")

    # Save as JSON
    config.save("demo_config.json", format="json")
    print("\n✓ Saved as JSON: demo_config.json")

    # Save as YAML
    config.save("demo_config.yaml", format="yaml")
    print("✓ Saved as YAML: demo_config.yaml")

    # Load back
    loaded = LanguageConfig.load("demo_config.json")
    print(f"\n✓ Loaded from file: {loaded.name}")


def main():
    """Run all demos."""
    print("=" * 70)
    print("HONEY BADGER LANGUAGE CONSTRUCTION SET - DEMO")
    print("=" * 70)

    demos = [
        demo_basic_usage,
        demo_presets,
        demo_runtime,
        demo_crud_operations,
        demo_validation,
        demo_serialization,
    ]

    for demo in demos:
        try:
            demo()
        except Exception as e:
            print(f"\nError in {demo.__name__}: {e}")

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
    print("\nGenerated files:")
    print("  ✓ demo_basic.json")
    print("  ✓ demo_python_custom.yaml")
    print("  ✓ demo_config.json")
    print("  ✓ demo_config.yaml")
    print("\nNext steps:")
    print("  1. Try: python langconfig.py info demo_basic.json")
    print("  2. Try: python langconfig.py validate demo_config.json")
    print("  3. Try: python langconfig.py list-presets")
    print("  4. Read the README.md for full documentation")
    print()


if __name__ == "__main__":
    main()
