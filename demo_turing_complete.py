#!/usr/bin/env python3
"""
Turing-Complete Language Configuration Examples
Demonstrates six different programming paradigms using LCS
"""

from language_config import LanguageConfig


def create_basic_like():
    """BASIC-Like: Imperative procedural language"""
    print("=" * 60)
    print("1. BASIC-Like Language - Imperative Procedural")
    print("=" * 60)

    config = LanguageConfig(name="BASIC-Like Language", version="1.0")

    # Rename keywords to BASIC style
    config.rename_keyword("if", "IF")
    config.rename_keyword("then", "THEN")
    config.rename_keyword("else", "ELSE")
    config.rename_keyword("while", "WHILE")
    config.rename_keyword("for", "FOR")
    config.rename_keyword("function", "DEF")
    config.rename_keyword("return", "RETURN")
    config.rename_keyword("let", "LET")

    # Configure functions
    config.add_function("print", "PRINT", max_args=-1)
    config.add_function("input", "INPUT", max_args=1)
    config.add_function("len", "LEN", min_args=1, max_args=1)
    config.add_function("int", "INT", min_args=1, max_args=1)
    config.add_function("str", "STR$", min_args=1, max_args=1)
    config.add_function("abs", "ABS", min_args=1, max_args=1)

    # Configure syntax
    config.set_comment_style("REM")
    config.set_array_indexing(1, True)  # 1-based indexing

    print(f"Name: {config.name}")
    print(f"Keywords: {len(config.keywords)} configured")
    print(f"Functions: {len(config.builtin_functions)} configured")
    print("\nTuring-complete elements:")
    print("  ✓ Conditional: IF...THEN...ELSE")
    print("  ✓ Loops: WHILE, FOR")
    print("  ✓ Variables: LET")
    print("  ✓ Functions: DEF...RETURN")
    print("\nExample code:")
    print("  10 LET x = 5")
    print("  20 IF x > 0 THEN PRINT x")
    print("  30 FOR i = 1 TO 10")
    print("  40   PRINT i")
    print("  50 NEXT i")

    config.save("examples/demo_basic.json")
    print(f"\n✓ Saved to examples/demo_basic.json")
    return config


def create_functional():
    """Functional: Lambda calculus based"""
    print("\n" + "=" * 60)
    print("2. Functional Language - Lambda Calculus")
    print("=" * 60)

    config = LanguageConfig(name="Functional Lambda Language", version="1.0")

    # Functional keywords
    config.rename_keyword("function", "lambda")
    config.rename_keyword("let", "let")
    config.rename_keyword("if", "if")
    config.rename_keyword("return", "return")

    # Functional operations
    config.add_function("map", "map", min_args=2, max_args=2)
    config.add_function("filter", "filter", min_args=2, max_args=2)
    config.add_function("reduce", "fold", min_args=3, max_args=3)
    config.add_function("head", "car", min_args=1, max_args=1)
    config.add_function("tail", "cdr", min_args=1, max_args=1)
    config.add_function("cons", "cons", min_args=2, max_args=2)

    # 0-based indexing for lists
    config.set_array_indexing(0, False)
    config.set_comment_style(";")

    print(f"Name: {config.name}")
    print(f"Keywords: {len(config.keywords)} configured")
    print(f"Functions: {len(config.builtin_functions)} configured")
    print("\nTuring-complete elements:")
    print("  ✓ Conditional: if...then...else")
    print("  ✓ Recursion: lambda + recursive calls")
    print("  ✓ Variables: let bindings")
    print("  ✓ Data structures: cons, car, cdr")
    print("\nExample code:")
    print("  (let factorial")
    print("    (lambda (n)")
    print("      (if (= n 0)")
    print("          1")
    print("          (* n (factorial (- n 1))))))")

    config.save("examples/demo_functional.json")
    print(f"\n✓ Saved to examples/demo_functional.json")
    return config


def create_stack_based():
    """Stack-based: Postfix notation like Forth"""
    print("\n" + "=" * 60)
    print("3. Stack-Based Language - Postfix/RPN")
    print("=" * 60)

    config = LanguageConfig(name="Stack-Based Forth-Like", version="1.0")

    # Forth-style keywords
    config.rename_keyword("function", ":")
    config.rename_keyword("return", ";")
    config.rename_keyword("if", "IF")
    config.rename_keyword("then", "THEN")
    config.rename_keyword("else", "ELSE")
    config.rename_keyword("while", "BEGIN")

    # Stack operations
    config.add_function("dup", "DUP", min_args=0, max_args=0)
    config.add_function("drop", "DROP", min_args=0, max_args=0)
    config.add_function("swap", "SWAP", min_args=0, max_args=0)
    config.add_function("over", "OVER", min_args=0, max_args=0)
    config.add_function("print", ".", min_args=1, max_args=1)

    config.set_comment_style("\\")

    print(f"Name: {config.name}")
    print(f"Keywords: {len(config.keywords)} configured")
    print(f"Functions: {len(config.builtin_functions)} configured")
    print("\nTuring-complete elements:")
    print("  ✓ Conditional: IF...THEN...ELSE")
    print("  ✓ Loops: BEGIN...UNTIL")
    print("  ✓ Memory: Stack + variables")
    print("  ✓ Functions: : ... ;")
    print("\nExample code:")
    print("  \\ Square a number")
    print("  : square DUP * ;")
    print("  5 square .  \\ prints 25")
    print("  ")
    print("  \\ Factorial")
    print("  : factorial")
    print("    DUP 1 > IF")
    print("      DUP 1 - factorial *")
    print("    THEN ;")

    config.save("examples/demo_stack.json")
    print(f"\n✓ Saved to examples/demo_stack.json")
    return config


def create_object_oriented():
    """Object-oriented like Ruby/Smalltalk"""
    print("\n" + "=" * 60)
    print("4. Object-Oriented Language - Message Passing")
    print("=" * 60)

    config = LanguageConfig(name="Object-Oriented Language", version="1.0")

    # OO keywords
    config.rename_keyword("class", "class")
    config.rename_keyword("function", "def")
    config.rename_keyword("if", "if")
    config.rename_keyword("while", "while")
    config.rename_keyword("for", "for")

    # OO operations
    config.add_function("print", "puts", max_args=-1)
    config.add_function("len", "length", min_args=1, max_args=1)
    config.add_function("map", "map", min_args=1, max_args=2)
    config.add_function("each", "each", min_args=1, max_args=2)

    config.set_comment_style("#")
    config.set_array_indexing(0, False)

    print(f"Name: {config.name}")
    print(f"Keywords: {len(config.keywords)} configured")
    print(f"Functions: {len(config.builtin_functions)} configured")
    print("\nTuring-complete elements:")
    print("  ✓ Conditional: if...elsif...else")
    print("  ✓ Loops: while, for, iterators")
    print("  ✓ Variables: instance, class, local")
    print("  ✓ Methods: def...end")
    print("\nExample code:")
    print("  class Counter")
    print("    def initialize(start)")
    print("      @count = start")
    print("    end")
    print("    ")
    print("    def increment")
    print("      @count += 1")
    print("    end")
    print("  end")

    config.save("examples/demo_oop.json")
    print(f"\n✓ Saved to examples/demo_oop.json")
    return config


def create_logic_based():
    """Logic programming like Prolog"""
    print("\n" + "=" * 60)
    print("5. Logic Programming Language - Declarative")
    print("=" * 60)

    config = LanguageConfig(name="Logic Programming Language", version="1.0")

    # Logic keywords
    config.rename_keyword("if", ":-")
    config.rename_keyword("and", ",")
    config.rename_keyword("or", ";")
    config.rename_keyword("not", "\\+")

    # Logic operations
    config.add_function("assert", "assert", min_args=1, max_args=1)
    config.add_function("retract", "retract", min_args=1, max_args=1)
    config.add_function("findall", "findall", min_args=3, max_args=3)
    config.add_function("member", "member", min_args=2, max_args=2)

    config.set_comment_style("%")

    print(f"Name: {config.name}")
    print(f"Keywords: {len(config.keywords)} configured")
    print(f"Functions: {len(config.builtin_functions)} configured")
    print("\nTuring-complete elements:")
    print("  ✓ Conditional: Rules with :-")
    print("  ✓ Recursion: Recursive rules")
    print("  ✓ Variables: Logic variables")
    print("  ✓ Unification: Pattern matching")
    print("\nExample code:")
    print("  % Facts")
    print("  parent(tom, bob).")
    print("  parent(tom, liz).")
    print("  ")
    print("  % Rules")
    print("  grandparent(X, Z) :- parent(X, Y), parent(Y, Z).")
    print("  ")
    print("  % Query")
    print("  ?- grandparent(tom, Who).")

    config.save("examples/demo_logic.json")
    print(f"\n✓ Saved to examples/demo_logic.json")
    return config


def create_assembly_like():
    """Assembly-like low-level language"""
    print("\n" + "=" * 60)
    print("6. Assembly-Like Language - Register Machine")
    print("=" * 60)

    config = LanguageConfig(name="Assembly-Like Language", version="1.0")

    # Assembly keywords
    config.rename_keyword("let", "MOV")
    config.rename_keyword("if", "CMP")
    config.rename_keyword("function", "PROC")
    config.rename_keyword("return", "RET")

    # Assembly operations
    config.add_function("add", "ADD", min_args=2, max_args=2)
    config.add_function("sub", "SUB", min_args=2, max_args=2)
    config.add_function("mul", "MUL", min_args=2, max_args=2)
    config.add_function("jmp", "JMP", min_args=1, max_args=1)
    config.add_function("jz", "JZ", min_args=1, max_args=1)
    config.add_function("print", "OUT", min_args=1, max_args=1)
    config.add_function("input", "IN", min_args=0, max_args=1)

    config.set_comment_style(";")

    print(f"Name: {config.name}")
    print(f"Keywords: {len(config.keywords)} configured")
    print(f"Functions: {len(config.builtin_functions)} configured")
    print("\nTuring-complete elements:")
    print("  ✓ Conditional: CMP + conditional jumps")
    print("  ✓ Loops: JMP (goto) + labels")
    print("  ✓ Memory: Registers + memory addresses")
    print("  ✓ Functions: PROC...RET")
    print("\nExample code:")
    print("  ; Compute factorial")
    print("  PROC factorial")
    print("    MOV R2, 1        ; result")
    print("  loop:")
    print("    CMP R1, 0")
    print("    JZ  done")
    print("    MUL R2, R1")
    print("    SUB R1, 1")
    print("    JMP loop")
    print("  done:")
    print("    RET R2")

    config.save("examples/demo_assembly.json")
    print(f"\n✓ Saved to examples/demo_assembly.json")
    return config


def demonstrate_turing_completeness():
    """Show why these languages are Turing-complete"""
    print("\n" + "=" * 60)
    print("Turing Completeness Analysis")
    print("=" * 60)

    print("\nA language is Turing-complete if it can:")
    print("1. Store and retrieve data (memory)")
    print("2. Perform conditional execution (branching)")
    print("3. Perform arbitrary iteration (loops/recursion)")
    print("4. Perform arbitrary computation (arithmetic)")

    print("\nAll six language paradigms demonstrated:")
    print("✓ BASIC-Like: Variables + IF/WHILE + arithmetic")
    print("✓ Functional: Bindings + conditionals + recursion")
    print("✓ Stack-Based: Stack + IF + loops + arithmetic")
    print("✓ Object-Oriented: Objects + methods + loops")
    print("✓ Logic: Facts + rules + recursion + unification")
    print("✓ Assembly: Registers + jumps + arithmetic")

    print("\n" + "=" * 60)
    print("Church-Turing Thesis")
    print("=" * 60)
    print("Any effectively calculable function can be computed by")
    print("all of these languages, as they are all Turing-complete.")
    print("\nThis means:")
    print("• They can all simulate each other")
    print("• They can all simulate a Turing machine")
    print("• They have equivalent computational power")
    print("• They differ only in syntax and paradigm, not power")


def main():
    """Create all example configurations"""
    print("\n" + "=" * 70)
    print(" " * 15 + "TURING-COMPLETE LANGUAGE EXAMPLES")
    print(" " * 12 + "Honey Badger Language Construction Set")
    print("=" * 70)

    configs = []

    try:
        configs.append(create_basic_like())
        configs.append(create_functional())
        configs.append(create_stack_based())
        configs.append(create_object_oriented())
        configs.append(create_logic_based())
        configs.append(create_assembly_like())

        demonstrate_turing_completeness()

        print("\n" + "=" * 70)
        print(
            f"✓ Successfully created {len(configs)} Turing-complete language configurations"
        )
        print("=" * 70)
        print("\nConfigurations saved to examples/ directory:")
        for cfg in configs:
            print(f"  • {cfg.name}")

        print("\nTo use these configurations:")
        print("  1. Load in IDE: python3 ide.py")
        print("  2. Validate: python langconfig.py validate examples/demo_*.json")
        print("  3. View info: python langconfig.py info examples/demo_basic.json")

        print("\nThese demonstrate six major programming paradigms:")
        print("  • Imperative (BASIC-like)")
        print("  • Functional (Lambda calculus)")
        print("  • Stack-based (Forth-like)")
        print("  • Object-oriented (Ruby-like)")
        print("  • Logic programming (Prolog-like)")
        print("  • Assembly-like (Register machine)")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
