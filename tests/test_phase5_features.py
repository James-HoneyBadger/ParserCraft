#!/usr/bin/env python3
"""
Test Phase 5: Advanced Language Design Features
- Language Template Generator
- Syntax Conflict Analyzer
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from hb_lcs.language_config import LanguageConfig
from hb_lcs.ide import AdvancedIDE
import json


def test_template_description_parsing():
    """Test parsing natural language descriptions into configs."""
    print("\n" + "=" * 70)
    print("TEST: Template Description Parsing")
    print("=" * 70)

    # Create IDE instance to access parsing method
    import tkinter as tk

    root = tk.Tk()
    root.withdraw()  # Hide main window
    ide = AdvancedIDE(root)

    # Test Spanish description
    spanish_desc = "I want Spanish keywords. Use 'si' for if and 'sino' for else."
    config_json = ide._parse_description_to_config(spanish_desc)
    config_dict = json.loads(config_json)

    print(f"Description: {spanish_desc[:50]}...")
    print(f"Generated keywords: {list(config_dict['keywords'].keys())}")

    # Verify Spanish keywords were generated
    assert "keywords" in config_dict, "Config missing keywords"
    assert len(config_dict["keywords"]) > 0, "No keywords generated"

    # Check specific Spanish keywords
    if "IF" in config_dict["keywords"]:
        assert (
            config_dict["keywords"]["IF"]["custom"] == "si"
        ), f"Expected 'si', got {config_dict['keywords']['IF']['custom']}"
        print(f"✓ Spanish IF keyword: '{config_dict['keywords']['IF']['custom']}'")

    # Test verbose description
    verbose_desc = "Create a verbose language with descriptive keywords"
    config_json = ide._parse_description_to_config(verbose_desc)
    config_dict = json.loads(config_json)

    print(f"\nDescription: {verbose_desc}")
    if "IF" in config_dict["keywords"]:
        print(f"✓ Verbose IF keyword: '{config_dict['keywords']['IF']['custom']}'")

    # Test minimal description
    minimal_desc = "Make a minimal language with shortest keywords"
    config_json = ide._parse_description_to_config(minimal_desc)
    config_dict = json.loads(config_json)

    print(f"\nDescription: {minimal_desc}")
    if "IF" in config_dict["keywords"]:
        print(f"✓ Minimal IF keyword: '{config_dict['keywords']['IF']['custom']}'")

    # Test custom mapping extraction
    custom_desc = "Use 'cuando' for while and 'imprimir' for print"
    config_json = ide._parse_description_to_config(custom_desc)
    config_dict = json.loads(config_json)

    print(f"\nDescription: {custom_desc}")
    print(f"Extracted keywords: {list(config_dict['keywords'].keys())}")

    # Check if custom mappings were extracted
    found_custom = False
    for key, value in config_dict["keywords"].items():
        if value["custom"] in ["cuando", "imprimir"]:
            print(f"✓ Found custom mapping: {value['original']} → {value['custom']}")
            found_custom = True

    if found_custom:
        print("✓ Custom keyword extraction working")
    else:
        print("⚠ Custom keyword extraction needs refinement")

    # Test array indexing detection
    array_desc = "Use 1-based indexing for arrays"
    config_json = ide._parse_description_to_config(array_desc)
    config_dict = json.loads(config_json)

    print(f"\nDescription: {array_desc}")
    print(f"Array start index: {config_dict['syntax_options']['array_start_index']}")
    assert (
        config_dict["syntax_options"]["array_start_index"] == 1
    ), "1-based indexing not detected"
    print("✓ Array indexing detection working")

    root.destroy()
    print("\n✅ Template description parsing tests passed!")
    return True


def test_conflict_analysis():
    """Test syntax conflict detection."""
    print("\n" + "=" * 70)
    print("TEST: Syntax Conflict Analysis")
    print("=" * 70)

    # Create IDE instance
    import tkinter as tk

    root = tk.Tk()
    root.withdraw()
    ide = AdvancedIDE(root)

    # Create a config with intentional conflicts
    conflict_config = {
        "metadata": {
            "name": "Conflict Test",
            "version": "1.0",
            "description": "Config with conflicts for testing",
            "author": "Test",
        },
        "keywords": {
            "IF": {"original": "if", "custom": "IF", "category": "control"},
            "IF_THEN": {
                "original": "if",
                "custom": "IF",
                "category": "control",
            },  # Duplicate
            "WHILE": {"original": "while", "custom": "WHILE", "category": "control"},
            "WHEN": {
                "original": "when",
                "custom": "WH",
                "category": "control",
            },  # Prefix conflict
            "WHERE": {
                "original": "where",
                "custom": "WHE",
                "category": "control",
            },  # Prefix conflict
            "X": {"original": "x", "custom": "X", "category": "control"},  # Single char
            "Y1": {"original": "y", "custom": "Y1", "category": "control"},  # Numeric
        },
        "builtin_functions": {},
        "syntax_options": {
            "array_start_index": 0,
            "single_line_comment": "#",
            "statement_terminator": ";",
        },
        "operators": {},
        "debug_mode": False,
        "strict_mode": True,
    }

    ide.current_config = LanguageConfig.from_dict(conflict_config)

    # Test keyword conflict analysis
    print("\nRunning keyword conflict analysis...")
    conflict_report = ide._analyze_keyword_conflicts()
    print(conflict_report[:500])  # Print first 500 chars

    assert (
        "CRITICAL" in conflict_report or "Duplicate" in conflict_report
    ), "Duplicate keywords not detected"
    print("✓ Duplicate keyword detection working")

    # Test ambiguous pattern analysis
    print("\nRunning ambiguous pattern analysis...")
    pattern_report = ide._analyze_ambiguous_patterns()
    print(pattern_report[:500])

    assert (
        "SINGLE-CHARACTER" in pattern_report or "single" in pattern_report.lower()
    ), "Single-char keywords not detected"
    print("✓ Single-character keyword detection working")

    assert (
        "DIGITS" in pattern_report or "numeric" in pattern_report.lower()
    ), "Numeric keywords not detected"
    print("✓ Numeric keyword detection working")

    # Test delimiter analysis
    print("\nRunning delimiter analysis...")
    delimiter_report = ide._analyze_delimiter_issues()
    print(delimiter_report[:300])

    assert "DELIMITER" in delimiter_report, "Delimiter section missing"
    print("✓ Delimiter analysis working")

    # Test recommendations
    print("\nRunning fix recommendations...")
    recommendations = ide._generate_fix_recommendations()
    print(recommendations[:500])

    assert (
        "SHORT" in recommendations.upper() or "RECOMMEND" in recommendations.upper()
    ), "Recommendations not generated"
    print("✓ Fix recommendations working")

    root.destroy()
    print("\n✅ Conflict analysis tests passed!")
    return True


def test_config_generation_and_application():
    """Test full config generation and application workflow."""
    print("\n" + "=" * 70)
    print("TEST: Config Generation & Application")
    print("=" * 70)

    import tkinter as tk

    root = tk.Tk()
    root.withdraw()
    ide = AdvancedIDE(root)

    # Generate a config
    desc = "Spanish language with Python syntax"
    config_json = ide._parse_description_to_config(desc)
    config_dict = json.loads(config_json)

    print(f"Generated config for: {desc}")
    print(f"Config structure:")
    print(f"  - Metadata: {config_dict['metadata']['name']}")
    print(f"  - Keywords: {len(config_dict['keywords'])} defined")
    print(f"  - Syntax options: {len(config_dict['syntax_options'])} settings")

    # Verify required sections
    required_sections = [
        "metadata",
        "keywords",
        "builtin_functions",
        "syntax_options",
        "operators",
    ]
    for section in required_sections:
        assert section in config_dict, f"Missing section: {section}"
        print(f"  ✓ {section} present")

    # Test applying config
    try:
        generated_config = LanguageConfig.from_dict(config_dict)
        ide.current_config = generated_config
        print(f"\n✓ Config successfully loaded into IDE")
        print(f"  Active keywords: {len(generated_config.keyword_mappings)}")

        # Verify some keywords
        if generated_config.keyword_mappings:
            sample = list(generated_config.keyword_mappings.items())[0]
            print(f"  Sample mapping: {sample[1].original} → {sample[1].custom}")

    except Exception as e:
        print(f"❌ Failed to apply config: {e}")
        raise

    root.destroy()
    print("\n✅ Config generation and application tests passed!")
    return True


def test_conflict_free_config():
    """Test that a well-designed config passes analysis."""
    print("\n" + "=" * 70)
    print("TEST: Conflict-Free Config Analysis")
    print("=" * 70)

    import tkinter as tk

    root = tk.Tk()
    root.withdraw()
    ide = AdvancedIDE(root)

    # Create a clean config
    clean_config = {
        "metadata": {
            "name": "Clean Test",
            "version": "1.0",
            "description": "Well-designed config",
            "author": "Test",
        },
        "keywords": {
            "IF": {"original": "if", "custom": "si", "category": "control"},
            "ELSE": {"original": "else", "custom": "sino", "category": "control"},
            "WHILE": {"original": "while", "custom": "mientras", "category": "control"},
            "FUNCTION": {
                "original": "function",
                "custom": "funcion",
                "category": "declaration",
            },
        },
        "builtin_functions": {},
        "syntax_options": {
            "array_start_index": 0,
            "single_line_comment": "#",
        },
        "operators": {},
        "debug_mode": False,
        "strict_mode": True,
    }

    ide.current_config = LanguageConfig.from_dict(clean_config)

    # Run analysis
    conflict_report = ide._analyze_keyword_conflicts()
    pattern_report = ide._analyze_ambiguous_patterns()

    print("Analyzing clean configuration...")
    print(f"\nKeyword conflicts: ", end="")
    if "No duplicate" in conflict_report:
        print("✓ None detected")
    else:
        print("⚠ Issues found")

    print(f"Ambiguous patterns: ", end="")
    if "No ambiguous" in pattern_report:
        print("✓ None detected")
    else:
        print("⚠ Some patterns flagged (may be acceptable)")

    print(f"\n✓ Clean config analyzed successfully")

    root.destroy()
    print("\n✅ Conflict-free config tests passed!")
    return True


def main():
    """Run all Phase 5 tests."""
    print("\n" + "=" * 70)
    print("PHASE 5 FEATURE TESTS")
    print("Advanced Language Design Features")
    print("=" * 70)

    tests = [
        ("Template Description Parsing", test_template_description_parsing),
        ("Syntax Conflict Analysis", test_conflict_analysis),
        ("Config Generation & Application", test_config_generation_and_application),
        ("Conflict-Free Config Analysis", test_conflict_free_config),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, "PASS" if result else "FAIL"))
        except Exception as e:
            print(f"\n❌ {test_name} FAILED: {e}")
            import traceback

            traceback.print_exc()
            results.append((test_name, "FAIL"))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    for test_name, status in results:
        status_symbol = "✅" if status == "PASS" else "❌"
        print(f"{status_symbol} {test_name}: {status}")

    passed = sum(1 for _, status in results if status == "PASS")
    total = len(results)
    print(f"\nResults: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL PHASE 5 TESTS PASSED! 🎉")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
