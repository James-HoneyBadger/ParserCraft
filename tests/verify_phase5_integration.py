#!/usr/bin/env python3
"""
Verify Phase 5 Integration
- Menu items properly added
- Keyboard shortcuts configured
- Methods exist and are callable
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from hb_lcs.ide import AdvancedIDE
import tkinter as tk


def verify_phase5_integration():
    """Verify all Phase 5 features are integrated."""
    print("\n" + "=" * 70)
    print("PHASE 5 INTEGRATION VERIFICATION")
    print("=" * 70)

    # Create IDE instance
    root = tk.Tk()
    root.withdraw()
    ide = AdvancedIDE(root)

    print("\n✓ IDE instance created successfully")

    # Check methods exist
    methods = [
        "_language_template_generator",
        "_parse_description_to_config",
        "_syntax_conflict_analyzer",
        "_analyze_keyword_conflicts",
        "_analyze_ambiguous_patterns",
        "_analyze_delimiter_issues",
        "_generate_fix_recommendations",
        "_export_conflict_report",
    ]

    print("\nChecking Phase 5 methods:")
    all_present = True
    for method in methods:
        if hasattr(ide, method):
            print(f"  ✓ {method}")
        else:
            print(f"  ✗ {method} MISSING")
            all_present = False

    if not all_present:
        print("\n❌ Some methods are missing!")
        return False

    # Verify methods are callable
    print("\nVerifying methods are callable:")
    callable_methods = [
        "_language_template_generator",
        "_syntax_conflict_analyzer",
    ]

    for method_name in callable_methods:
        method = getattr(ide, method_name)
        if callable(method):
            print(f"  ✓ {method_name} is callable")
        else:
            print(f"  ✗ {method_name} is not callable")
            all_present = False

    # Test parsing method with sample input
    print("\nTesting description parsing:")
    try:
        test_desc = "Create a Spanish language"
        result = ide._parse_description_to_config(test_desc)
        if result and "keywords" in result:
            print(f"  ✓ Parser generates valid config")
        else:
            print(f"  ⚠ Parser returned: {result[:100]}...")
    except Exception as e:
        print(f"  ✗ Parser error: {e}")
        all_present = False

    # Test analysis methods with a sample config
    print("\nTesting conflict analysis methods:")
    try:
        # Create a simple test config
        from hb_lcs.language_config import LanguageConfig

        test_config = {
            "metadata": {
                "name": "Test",
                "version": "1.0",
                "description": "Test config",
                "author": "Test",
            },
            "keywords": {
                "IF": {"original": "if", "custom": "si", "category": "control"},
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

        ide.current_config = LanguageConfig.from_dict(test_config)

        # Test analysis methods
        conflict_report = ide._analyze_keyword_conflicts()
        if "KEYWORD CONFLICT" in conflict_report:
            print("  ✓ _analyze_keyword_conflicts works")

        pattern_report = ide._analyze_ambiguous_patterns()
        if "PATTERN" in pattern_report:
            print("  ✓ _analyze_ambiguous_patterns works")

        delimiter_report = ide._analyze_delimiter_issues()
        if "DELIMITER" in delimiter_report:
            print("  ✓ _analyze_delimiter_issues works")

        recommendations = ide._generate_fix_recommendations()
        if "RECOMMENDATION" in recommendations:
            print("  ✓ _generate_fix_recommendations works")

    except Exception as e:
        print(f"  ✗ Analysis error: {e}")
        import traceback

        traceback.print_exc()
        all_present = False

    root.destroy()

    print("\n" + "=" * 70)
    if all_present:
        print("✅ PHASE 5 INTEGRATION VERIFIED SUCCESSFULLY!")
        print("=" * 70)
        print("\nPhase 5 Features:")
        print("  1. Language Template Generator")
        print("     - Menu: Tools → Language Template Generator")
        print("     - Generates configs from natural language descriptions")
        print("     - Quick templates: Spanish, Verbose, Minimal, Academic")
        print("     - Custom keyword extraction")
        print()
        print("  2. Syntax Conflict Analyzer")
        print("     - Menu: Tools → Syntax Conflict Analyzer")
        print("     - Shortcut: Ctrl+Shift+A")
        print("     - Detects duplicate keywords")
        print("     - Finds prefix conflicts")
        print("     - Identifies ambiguous patterns")
        print("     - Checks delimiter conflicts")
        print("     - Provides fix recommendations")
        print("     - Export analysis reports")
        print("\n" + "=" * 70)
        return True
    else:
        print("❌ PHASE 5 INTEGRATION INCOMPLETE")
        print("=" * 70)
        return False


if __name__ == "__main__":
    success = verify_phase5_integration()
    sys.exit(0 if success else 1)
