from pathlib import Path
import subprocess

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PYTHON = PROJECT_ROOT / ".venv" / "bin" / "python"
CLI = PROJECT_ROOT / "src" / "hb_lcs" / "cli.py"
CONFIG = PROJECT_ROOT / "configs" / "examples" / "gw_basic.yaml"
CASES = PROJECT_ROOT / "tests" / "data" / "gw_basic_cases.yaml"
DEMO_BAS = (
    PROJECT_ROOT
    / "demos"
    / "teachscript"
    / "examples"
    / "gw_basic_demo.bas"
)


def run_cli(args: list[str]) -> subprocess.CompletedProcess[str]:
    cmd = [str(PYTHON), str(CLI)] + args
    return subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )


def test_cli_test_passes_all_cases():
    result = run_cli([
        "test",
        "--config",
        str(CONFIG),
        "--tests",
        str(CASES),
    ])

    assert result.returncode == 0, result.stderr
    assert "Summary: 2/2 passed, 0 failed" in result.stdout


def test_cli_translate_prints_to_stdout_when_no_output():
    result = run_cli([
        "translate",
        "--config",
        str(CONFIG),
        "--input",
        str(DEMO_BAS),
    ])

    assert result.returncode == 0, result.stderr
    assert "print" in result.stdout.lower()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(pytest.main([__file__]))
