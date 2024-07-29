from tests.conftest import TestRunner


def test_help_message_sane(runner: TestRunner) -> None:
    """Test a sane basic help call."""
    result = runner.run_cli(["--help"])
    assert result.exit_code == 0
    assert (
        "VulcanBox: CLI tool for managing Github repositories from local"
        in result.output
    )
