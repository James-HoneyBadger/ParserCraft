#!/usr/bin/env python3
"""
Test Phase 7: Advanced Intelligence & Collaboration

Tests for:
1. Code Intelligence System
2. Collaboration Tools
3. Plugin System
4. Performance Analytics
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from hb_lcs.language_config import LanguageConfig
from hb_lcs.ide import AdvancedIDE
import tkinter as tk


def test_code_intelligence():
    """Test code intelligence features."""
    print("\n" + "=" * 70)
    print("TEST 1: CODE INTELLIGENCE SYSTEM")
    print("=" * 70)

    root = tk.Tk()
    root.withdraw()

    try:
        ide = AdvancedIDE(root)
        ide.current_config = LanguageConfig.from_preset("python_like")

        # Test 1: Initialize code intelligence
        print("\n1. Testing code intelligence initialization...")
        ide.init_code_intelligence()
        assert hasattr(ide, "intelligence_data"), "Should create data"
        assert "symbol_table" in ide.intelligence_data, "Should have table"
        print("   ✓ Code intelligence initialized")

        # Test 2: Analyze code complexity
        print("\n2. Testing complexity analysis...")
        test_code = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

for i in range(10):
    print(fibonacci(i))
"""
        metrics = ide.analyze_code_complexity(test_code)
        assert "cyclomatic_complexity" in metrics, "Should have complexity"
        assert "nesting_depth" in metrics, "Should have nesting depth"
        assert metrics["lines"] > 0, "Should count lines"
        print(f"   Lines: {metrics['lines']}")
        print(f"   Complexity: {metrics['cyclomatic_complexity']}")
        print(f"   Nesting: {metrics['nesting_depth']}")
        print("   ✓ Complexity analysis works")

        # Test 3: Refactoring suggestions
        print("\n3. Testing refactoring suggestions...")
        duplicate_code = """
x = 10
print(x)
y = 20
print(y)
print(x)
print(y)
print(x)
"""
        suggestions = ide.suggest_refactoring(duplicate_code)
        assert isinstance(suggestions, list), "Should return list"
        print(f"   Generated {len(suggestions)} suggestions")
        if suggestions:
            print(f"   Sample: {suggestions[0]['type']}")
        print("   ✓ Refactoring suggestions work")

        # Test 4: Auto-completion
        print("\n4. Testing auto-completion...")
        partial = "if x > 5:\n    pr"
        completions = ide.auto_complete_code(partial, len(partial))
        assert isinstance(completions, list), "Should return completions"
        print(f"   Generated {len(completions)} completions")
        if completions:
            print(f"   Sample: {completions[0]}")
        print("   ✓ Auto-completion works")

        print("\n✅ Code Intelligence: ALL TESTS PASSED")
        return True

    finally:
        root.destroy()


def test_collaboration_tools():
    """Test collaboration and sharing features."""
    print("\n" + "=" * 70)
    print("TEST 2: COLLABORATION TOOLS")
    print("=" * 70)

    root = tk.Tk()
    root.withdraw()

    try:
        ide = AdvancedIDE(root)
        ide.current_config = LanguageConfig.from_preset("python_like")

        # Test 1: Export for sharing
        print("\n1. Testing export for sharing...")
        package = ide.export_for_sharing(format_type="package")
        assert isinstance(package, str), "Should return string"
        assert len(package) > 0, "Should have content"
        assert "keywords" in package, "Should contain keywords"
        print(f"   Package size: {len(package)} bytes")
        print("   ✓ Export works")

        # Test 2: Generate shareable link
        print("\n2. Testing shareable link generation...")
        link = ide.generate_shareable_link()
        assert link.startswith("hblcs://"), "Should be valid link format"
        assert "import?data=" in link, "Should have data parameter"
        print(f"   Link: {link[:50]}...")
        print("   ✓ Link generation works")

        # Test 3: Import shared config
        print("\n3. Testing config import...")
        imported = ide.import_shared_config(package)
        assert isinstance(imported, LanguageConfig), "Should return config"
        assert imported.name == ide.current_config.name, "Names match"
        assert len(imported.keyword_mappings) > 0, "Should have keywords"
        print(f"   Imported: {imported.name}")
        print(f"   Keywords: {len(imported.keyword_mappings)}")
        print("   ✓ Import works")

        # Test 4: Cloud sync simulation
        print("\n4. Testing cloud sync...")
        sync_info = ide.sync_to_cloud(provider="github")
        assert "status" in sync_info, "Should have status"
        assert "sync_id" in sync_info, "Should have ID"
        print(f"   Provider: {sync_info['provider']}")
        print(f"   Sync ID: {sync_info['sync_id']}")
        print("   ✓ Cloud sync works")

        print("\n✅ Collaboration Tools: ALL TESTS PASSED")
        return True

    finally:
        root.destroy()


def test_plugin_system():
    """Test plugin system features."""
    print("\n" + "=" * 70)
    print("TEST 3: PLUGIN SYSTEM")
    print("=" * 70)

    root = tk.Tk()
    root.withdraw()

    try:
        ide = AdvancedIDE(root)
        ide.current_config = LanguageConfig.from_preset("python_like")

        # Test 1: Initialize plugin system
        print("\n1. Testing plugin system initialization...")
        ide.init_plugin_system()
        assert hasattr(ide, "plugins"), "Should have plugins dict"
        assert "loaded" in ide.plugins, "Should have loaded plugins"
        assert "hooks" in ide.plugins, "Should have hooks"
        print(f"   Available: {len(ide.plugins['available'])}")
        print("   ✓ Plugin system initialized")

        # Test 2: Register a plugin
        print("\n2. Testing plugin registration...")

        class TestPlugin:
            def on_validation(self, config):
                return "Validation hook executed"

        success = ide.register_plugin("test_plugin", TestPlugin, ["on_validation"])
        assert success is True, "Should register successfully"
        assert "test_plugin" in ide.plugins["loaded"], "Should be loaded"
        print("   ✓ Plugin registered")

        # Test 3: Execute plugin hooks
        print("\n3. Testing hook execution...")
        results = ide.execute_plugin_hooks("on_validation", ide.current_config)
        assert isinstance(results, list), "Should return results list"
        assert len(results) > 0, "Should have results"
        print(f"   Executed {len(results)} hooks")
        if results:
            print(f"   Result: {results[0]}")
        print("   ✓ Hooks execute correctly")

        # Test 4: List plugins
        print("\n4. Testing plugin listing...")
        plugin_list = ide.list_plugins()
        assert "available" in plugin_list, "Should list available"
        assert "loaded" in plugin_list, "Should list loaded"
        assert len(plugin_list["loaded"]) > 0, "Should have loaded plugins"
        print(f"   Available: {len(plugin_list['available'])}")
        print(f"   Loaded: {len(plugin_list['loaded'])}")
        print("   ✓ Plugin listing works")

        print("\n✅ Plugin System: ALL TESTS PASSED")
        return True

    finally:
        root.destroy()


def test_performance_analytics():
    """Test performance analytics features."""
    print("\n" + "=" * 70)
    print("TEST 4: PERFORMANCE ANALYTICS")
    print("=" * 70)

    root = tk.Tk()
    root.withdraw()

    try:
        ide = AdvancedIDE(root)
        ide.current_config = LanguageConfig.from_preset("python_like")

        # Test 1: Profile language performance
        print("\n1. Testing performance profiling...")
        test_code = """
x = 10
if x > 5:
    print("Large")
for i in range(10):
    print(i)
"""
        profile = ide.profile_language_performance(test_code)
        assert "translation_time" in profile, "Should have translation time"
        assert "memory_estimate" in profile, "Should estimate memory"
        assert "optimization_score" in profile, "Should have score"
        print(f"   Translation time: {profile['translation_time']:.6f}s")
        print(f"   Memory: {profile['memory_estimate']} bytes")
        print(f"   Score: {profile['optimization_score']}/100")
        print("   ✓ Profiling works")

        # Test 2: Benchmark translation
        print("\n2. Testing translation benchmark...")
        benchmark = ide.benchmark_translation(iterations=50)
        assert "avg_time" in benchmark, "Should have average time"
        assert "iterations" in benchmark, "Should have iterations"
        assert benchmark["iterations"] == 50, "Should run 50 iterations"
        print(f"   Iterations: {benchmark['iterations']}")
        print(f"   Avg time: {benchmark['avg_time']*1000:.4f} ms")
        print("   ✓ Benchmarking works")

        # Test 3: Generate performance report
        print("\n3. Testing performance report...")
        report = ide.generate_performance_report()
        assert isinstance(report, str), "Should return string"
        assert len(report) > 0, "Should have content"
        assert "PERFORMANCE ANALYSIS" in report, "Should have header"
        print(f"   Report length: {len(report)} chars")
        print("   ✓ Report generation works")

        # Test 4: Optimization suggestions
        print("\n4. Testing optimization suggestions...")
        large_code = "\n".join([f"x{i} = {i}" for i in range(150)])
        suggestions = ide.suggest_optimizations(large_code)
        assert isinstance(suggestions, list), "Should return list"
        print(f"   Generated {len(suggestions)} suggestions")
        if suggestions:
            print(f"   Sample: {suggestions[0]['type']}")
        print("   ✓ Optimization suggestions work")

        print("\n✅ Performance Analytics: ALL TESTS PASSED")
        return True

    finally:
        root.destroy()


def main():
    """Run all Phase 7 tests."""
    print("\n" + "=" * 70)
    print("PHASE 7: ADVANCED INTELLIGENCE & COLLABORATION TEST SUITE")
    print("=" * 70)

    tests = [
        ("Code Intelligence", test_code_intelligence),
        ("Collaboration Tools", test_collaboration_tools),
        ("Plugin System", test_plugin_system),
        ("Performance Analytics", test_performance_analytics),
    ]

    results = {}
    for name, test_func in tests:
        try:
            result = test_func()
            results[name] = "PASS" if result else "FAIL"
        except Exception as e:
            print(f"\n❌ {name} FAILED: {e}")
            import traceback

            traceback.print_exc()
            results[name] = "FAIL"

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    for name, status in results.items():
        symbol = "✅" if status == "PASS" else "❌"
        print(f"{symbol} {name}: {status}")

    passed = sum(1 for s in results.values() if s == "PASS")
    total = len(results)
    print(f"\nResults: {passed}/{total} test suites passed")

    if passed == total:
        print("\n🎉 ALL PHASE 7 TESTS PASSED! 🎉")
        return 0
    else:
        print(f"\n⚠ {total - passed} test suite(s) failed")
        return 1


if __name__ == "__main__":
    exit(main())
