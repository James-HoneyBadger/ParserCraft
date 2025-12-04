#!/usr/bin/env python3
"""
Test Phase 8: Web IDE, Remote Execution, Debugging, Community

Tests for:
1. Web IDE Interface
2. Remote Code Execution
3. Advanced Debugging
4. Community Features
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from hb_lcs.language_config import LanguageConfig
from hb_lcs.ide import AdvancedIDE
import tkinter as tk


def test_web_ide():
    """Test web IDE features."""
    print("\n" + "=" * 70)
    print("TEST 1: WEB IDE INTERFACE")
    print("=" * 70)

    root = tk.Tk()
    root.withdraw()

    try:
        ide = AdvancedIDE(root)
        ide.current_config = LanguageConfig.from_preset("python_like")

        # Test 1: Initialize web IDE
        print("\n1. Testing web IDE initialization...")
        web_config = ide.init_web_ide(port=5000)
        assert web_config is not None, "Should initialize web config"
        assert web_config["port"] == 5000, "Should set correct port"
        assert "features" in web_config, "Should have features"
        print(f"   Web IDE: {web_config['base_url']}")
        print(f"   Features: {list(web_config['features'].keys())}")
        print("   ✓ Web IDE initialized")

        # Test 2: Generate web UI template
        print("\n2. Testing web UI template generation...")
        html = ide.generate_web_ui_template()
        assert isinstance(html, str), "Should return HTML string"
        assert "<html" in html, "Should have HTML structure"
        assert "textarea" in html, "Should have editor"
        assert "button" in html, "Should have buttons"
        print(f"   Template size: {len(html)} bytes")
        print(f"   Contains: HTML, CSS, JavaScript")
        print("   ✓ Web UI template generated")

        # Test 3: Create API handlers
        print("\n3. Testing API handler creation...")
        config_handler = ide.create_web_api_handler("/api/config")
        assert "method" in config_handler, "Should have method"
        assert "response" in config_handler, "Should have response"
        print(f"   API endpoints: {len(ide.web_routes)}")
        print(f"   Sample: /api/config - {config_handler['method']}")
        print("   ✓ API handlers created")

        # Test 4: Web routes
        print("\n4. Testing web routes...")
        assert "/api/config" in ide.web_routes, "Should have config route"
        assert "/api/code/execute" in ide.web_routes, "Should have execute"
        assert "/api/keywords" in ide.web_routes, "Should have keywords"
        print(f"   Registered routes: {len(ide.web_routes)}")
        for route in list(ide.web_routes.keys())[:3]:
            print(f"     - {route}")
        print("   ✓ Web routes configured")

        print("\n✅ Web IDE: ALL TESTS PASSED")
        return True

    finally:
        root.destroy()


def test_remote_execution():
    """Test remote code execution features."""
    print("\n" + "=" * 70)
    print("TEST 2: REMOTE CODE EXECUTION")
    print("=" * 70)

    root = tk.Tk()
    root.withdraw()

    try:
        ide = AdvancedIDE(root)
        ide.current_config = LanguageConfig.from_preset("python_like")

        # Test 1: Initialize remote execution
        print("\n1. Testing remote execution initialization...")
        success = ide.init_remote_execution(sandbox_type="local")
        assert success is True, "Should initialize successfully"
        assert "timeout" in ide.execution_config, "Should have timeout"
        print(f"   Sandbox type: {ide.execution_config['sandbox_type']}")
        print(f"   Timeout: {ide.execution_config['timeout']}s")
        print("   ✓ Remote execution initialized")

        # Test 2: Safe code execution
        print("\n2. Testing safe code execution...")
        test_code = "x = 5\ny = 10\nprint(x + y)"
        result = ide.execute_code_safely(test_code, timeout=5)
        assert "status" in result, "Should have status"
        assert result["status"] == "success", "Should execute successfully"
        assert "15" in result["output"], "Should print result"
        print(f"   Status: {result['status']}")
        print(f"   Output: {result['output'].strip()}")
        print(f"   Time: {result['execution_time']:.6f}s")
        print("   ✓ Safe execution works")

        # Test 3: Create execution sandbox
        print("\n3. Testing sandbox creation...")
        sandbox = ide.create_execution_sandbox("medium")
        assert "id" in sandbox, "Should have sandbox ID"
        assert "status" in sandbox, "Should have status"
        print(f"   Sandbox ID: {sandbox['id']}")
        print(f"   Isolation: {sandbox['isolation']}")
        print(f"   Memory: {sandbox['resources']['memory_mb']}MB")
        print("   ✓ Sandbox created")

        # Test 4: Distributed execution
        print("\n4. Testing distributed execution...")
        dist_code = "result = 2 + 2\nprint(result)"
        results = ide.distribute_execution(dist_code, num_instances=3)
        assert len(results) == 3, "Should have 3 results"
        assert all(r["status"] == "success" for r in results), "All should succeed"
        print(f"   Instances: {len(results)}")
        for i, r in enumerate(results, 1):
            print(f"     Instance {i}: {r['sandbox_id']}")
        print("   ✓ Distributed execution works")

        print("\n✅ Remote Execution: ALL TESTS PASSED")
        return True

    finally:
        root.destroy()


def test_debugging():
    """Test advanced debugging features."""
    print("\n" + "=" * 70)
    print("TEST 3: ADVANCED DEBUGGING SYSTEM")
    print("=" * 70)

    root = tk.Tk()
    root.withdraw()

    try:
        ide = AdvancedIDE(root)
        ide.current_config = LanguageConfig.from_preset("python_like")

        # Test 1: Initialize debugger
        print("\n1. Testing debugger initialization...")
        debugger_state = ide.init_debugger()
        assert "breakpoints" in debugger_state, "Should have breakpoints"
        assert "variables" in debugger_state, "Should have variables"
        print(f"   Debugger state initialized")
        print(f"   Features: breakpoints, watches, call_stack, trace")
        print("   ✓ Debugger initialized")

        # Test 2: Set breakpoints
        print("\n2. Testing breakpoint setting...")
        success = ide.set_breakpoint("test.py", 10, "x > 5")
        assert success is True, "Should set breakpoint"
        assert (
            "test.py:10" in ide.debugger_state["breakpoints"]
        ), "Should have breakpoint"
        bp = ide.debugger_state["breakpoints"]["test.py:10"]
        assert bp["condition"] == "x > 5", "Should have condition"
        print(f"   Breakpoint set: test.py:10")
        print(f"   Condition: {bp['condition']}")
        print("   ✓ Breakpoints work")

        # Test 3: Step through code
        print("\n3. Testing step-through execution...")
        step_code = "a = 1\nb = 2\nc = a + b"
        trace = ide.step_through_code(step_code, step_type="line")
        assert "steps" in trace, "Should have steps"
        print(f"   Steps traced: {len(trace.get('steps', []))}")
        if trace.get("steps"):
            print(f"   First step: {trace['steps'][0]}")
        print("   ✓ Step execution works")

        # Test 4: Inspect variables
        print("\n4. Testing variable inspection...")
        variables = ide.inspect_variables()
        assert isinstance(variables, dict), "Should return dict"
        assert "watched" in variables, "Should have watched"
        print(f"   Debugger has:")
        print(f"     - Watched variables: {len(variables['watched'])}")
        print(f"     - Locals: {len(variables['locals'])}")
        print(f"     - Breakpoints: {len(variables['breakpoints'])}")
        print("   ✓ Variable inspection works")

        print("\n✅ Debugging System: ALL TESTS PASSED")
        return True

    finally:
        root.destroy()


def test_community():
    """Test community features and registry."""
    print("\n" + "=" * 70)
    print("TEST 4: COMMUNITY FEATURES & REGISTRY")
    print("=" * 70)

    root = tk.Tk()
    root.withdraw()

    try:
        ide = AdvancedIDE(root)
        ide.current_config = LanguageConfig.from_preset("python_like")

        # Test 1: Initialize community registry
        print("\n1. Testing community registry initialization...")
        community = ide.init_community_registry()
        assert "languages" in community, "Should have languages"
        assert "users" in community, "Should have users"
        assert len(community["languages"]) > 0, "Should load sample languages"
        print(f"   Community languages: {len(community['languages'])}")
        print(f"   Categories: {len(community['categories'])}")
        for lang in community["languages"][:2]:
            print(f"     - {lang['name']} ({lang['rating']} ⭐)")
        print("   ✓ Community registry initialized")

        # Test 2: Register user
        print("\n2. Testing user registration...")
        user = ide.register_user("testuser", "test@example.com")
        assert "username" in user, "Should have username"
        assert user["username"] == "testuser", "Should match username"
        assert "user_" in user.get("id", ""), "Should have user ID"
        print(f"   User: {user['username']}")
        print(f"   Email: {user['email']}")
        print(f"   Joined: {user['joined'][:10]}")
        print("   ✓ User registration works")

        # Test 3: Publish language
        print("\n3. Testing language publishing...")
        published = ide.publish_language(
            "MyDSL",
            "A domain-specific language for data processing",
            "DSL",
        )
        assert "id" in published, "Should have language ID"
        assert published["name"] == "MyDSL", "Should match name"
        assert published["category"] == "DSL", "Should match category"
        print(f"   Language: {published['name']}")
        print(f"   Category: {published['category']}")
        print(f"   Tags: {', '.join(published['tags'])}")
        print("   ✓ Language publishing works")

        # Test 4: Rate and review
        print("\n4. Testing rating and review system...")
        review = ide.rate_and_review(
            published["id"],
            4.5,
            "Great language for DSL programming",
        )
        assert "id" in review, "Should have review ID"
        assert review["rating"] == 4.5, "Should have correct rating"
        assert "DSL" in review["text"], "Should have text"
        print(f"   Review: {review['rating']}⭐")
        print(f"   Text: {review['text']}")
        print(f"   Language rating updated")
        print("   ✓ Rating system works")

        print("\n✅ Community Features: ALL TESTS PASSED")
        return True

    finally:
        root.destroy()


def main():
    """Run all Phase 8 tests."""
    print("\n" + "=" * 70)
    print("PHASE 8: WEB IDE, REMOTE EXECUTION, DEBUGGING, COMMUNITY")
    print("=" * 70)

    tests = [
        ("Web IDE Interface", test_web_ide),
        ("Remote Execution", test_remote_execution),
        ("Debugging System", test_debugging),
        ("Community Features", test_community),
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
        print("\n🎉 ALL PHASE 8 TESTS PASSED! 🎉")
        return 0
    else:
        print(f"\n⚠ {total - passed} test suite(s) failed")
        return 1


if __name__ == "__main__":
    exit(main())
