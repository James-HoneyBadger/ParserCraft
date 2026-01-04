from pathlib import Path

import pytest

from hb_lcs.cli import _run_test_case, _translate_with_keywords
from hb_lcs.language_config import KeywordMapping, LanguageConfig, FunctionConfig
from hb_lcs.language_runtime import LanguageRuntime


@pytest.fixture(autouse=True)
def reset_runtime():
    LanguageRuntime.reset()
    yield
    LanguageRuntime.reset()


def test_translate_with_custom_keyword():
    config = LanguageConfig()
    config.keyword_mappings["if"] = KeywordMapping("if", "si")
    config.builtin_functions["print"] = FunctionConfig(
        name="IMPRIMIR",
        arity=-1,
        implementation="print",
    )
    LanguageRuntime.load_config(config=config)

    custom_keywords = tuple(LanguageRuntime.get_custom_keywords())
    result = _translate_with_keywords(
        "si True:\n    IMPRIMIR('hola')\n    pass\n",
        custom_keywords,
    )

    assert result.startswith("if True")
    assert "print('hola')" in result


def test_run_test_case_matches_stdout_and_vars():
    config = LanguageConfig()
    config.builtin_functions["print"] = FunctionConfig(
        name="PRINT",
        arity=-1,
        implementation="print",
    )
    LanguageRuntime.load_config(config=config)
    custom_keywords = tuple(LanguageRuntime.get_custom_keywords())

    case = {
        "name": "prints and sets",
        "source": 'PRINT("hello")\nx = 5',
        "expect_stdout": "hello",
        "expect_vars": {"x": 5},
    }

    passed, details = _run_test_case(
        case,
        Path("."),
        custom_keywords,
        show_translation=False,
        debug=False,
    )

    assert passed
    assert details == []
