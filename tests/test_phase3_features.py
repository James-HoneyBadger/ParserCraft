from pathlib import Path
import tempfile

from hb_lcs.language_config import LanguageConfig, KeywordMapping
from hb_lcs.language_runtime import LanguageRuntime
from hb_lcs.language_validator import LanguageValidator


def test_config_load_save_reload(tmp_path):
    # Create a simple config programmatically to avoid YAML issues
    config = LanguageConfig(
        name="Test Language", version="1.0", description="Test config for Phase 3"
    )
    config.keyword_mappings["IF"] = KeywordMapping(
        original="if", custom="si", category="control"
    )

    assert config.name == "Test Language"
    assert len(config.keyword_mappings) > 0

    # Save to temp
    out_path = tmp_path / "modified.yaml"
    config.save(out_path)
    assert out_path.exists(), "Saved config should exist"

    # Reload and verify roundtrip
    reloaded = LanguageConfig.load(out_path)
    assert "IF" in reloaded.keyword_mappings
    assert reloaded.keyword_mappings["IF"].custom == "si"
    print("✓ test_config_load_save_reload passed")


def test_validator_report_contains_sections():
    config = LanguageConfig(
        name="Test Language", version="1.0", description="Test config for validation"
    )
    config.keyword_mappings["IF"] = KeywordMapping(
        original="if", custom="if", category="control"
    )

    validator = LanguageValidator(config)
    validator.validate_all()
    report = validator.generate_report()

    # Basic structure checks
    assert "LANGUAGE CONFIGURATION VALIDATION REPORT" in report
    assert "Total Issues:" in report
    assert "ERRORS" in report or "No issues" in report or "WARNINGS" in report
    print("✓ test_validator_report_contains_sections passed")


def test_runtime_load_and_keyword_translation():
    config = LanguageConfig(
        name="Test Language", version="1.0", description="Test config for runtime"
    )

    LanguageRuntime.load_config(config)

    # Add custom mapping then rebuild runtime mappings via reload
    config.keyword_mappings["WHILE"] = KeywordMapping(
        original="while", custom="mientras", category="control"
    )
    LanguageRuntime.load_config(config)

    # Translate custom -> original
    assert LanguageRuntime.translate_keyword("mientras") == "while"

    # Environment pointer persistence check (project scope)
    # Save config to temp file for pointer test
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        temp_config_path = Path(f.name)

    try:
        config.save(temp_config_path)
        pointer_file = Path(".langconfig")
        try:
            pointer_file.write_text(str(temp_config_path.resolve()), encoding="utf-8")
            assert pointer_file.exists()
            # Ensure runtime can auto-load via environment helper
            LanguageRuntime.load_config(config_file=str(temp_config_path))
        finally:
            if pointer_file.exists():
                pointer_file.unlink()
    finally:
        if temp_config_path.exists():
            temp_config_path.unlink()

    print("✓ test_runtime_load_and_keyword_translation passed")


if __name__ == "__main__":
    print("\n=== Running Phase 3 Integration Tests ===\n")

    # Test 1: Config load/save/reload
    with tempfile.TemporaryDirectory() as tmpdir:
        test_config_load_save_reload(Path(tmpdir))

    # Test 2: Validator report
    test_validator_report_contains_sections()

    # Test 3: Runtime and keyword translation
    test_runtime_load_and_keyword_translation()

    print("\n=== All Phase 3 Tests Passed ===\n")
