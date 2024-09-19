from unittest.mock import MagicMock, Mock, patch

from tests.conftest import TestRunner


def __new_mock_subprocess(name: str) -> Mock:
    value = Mock()
    output = {"returncode": 0, "stdout.decode.return_value": f"{name} 1.2.3"}
    value.configure_mock(**output)
    return value


def __new_mock_subprocess_with_err(name: str, exit_code: int, output: str) -> Mock:
    value = Mock()
    output = {
        "returncode": exit_code,
        "stdout.decode.return_value": f"Some {name} error: {output}",
    }
    value.configure_mock(**output)
    return value


@patch("subprocess.run")
def test_doctor_success(
    mock_subproc_run: MagicMock,
    runner: TestRunner,
) -> None:
    """Tests stf doctor in the success case."""
    services = [
        "Docker",
        "Docker Compose",
        "Git",
    ]
    mock_subproc_run.side_effect = list(map(__new_mock_subprocess, services))

    result = runner.run_cli(["doctor"])
    assert result.exit_code == 0
    assert "All 3 dependencies ready" in result.output


@patch("subprocess.run")
def test_doctor_missing_dependencies(
    mock_subproc_run: MagicMock,
    runner: TestRunner,
) -> None:
    """Tests stf doctor in the success case."""
    services = [
        "Docker",
        "Docker Compose",
        "Git",
    ]
    mock_subproc_run.side_effect = [
        __new_mock_subprocess_with_err(
            service, exit_code=1, output=f"{service} not installed"
        )
        for service in services
    ]

    result = runner.run_cli(["doctor"])
    assert "Vulcanbox Doctor found 3 missing dependencies" in result.output
    for service in services:
        assert f"Install {service}" in result.output
