import os
from pathlib import Path

from pytest import LogCaptureFixture, MonkeyPatch

from tests.conftest import TestRunner
from tests.helpers import assert_files_created, assert_lines_in_file


def test_template_new_compose_file_sane(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    runner: TestRunner,
    caplog: LogCaptureFixture,
) -> None:
    monkeypatch.chdir(tmp_path)
    dockerfile_mock = Path(os.path.join(str(tmp_path), "mock.Dockerfile"))
    generated_compose = Path(os.path.join(str(tmp_path), "docker-compose.yml"))
    generated_files = [str(dockerfile_mock), str(generated_compose)]
    dockerfile_mock.touch()

    result = runner.run_cli(
        [
            "-vv",
            "new",
            "compose",
            "--image",
            "mock.Dockerfile",
            "--count",
            "1",
        ]
    )

    assert result.exit_code == 0
    assert_files_created(str(tmp_path), generated_files)
    assert_lines_in_file(str(generated_compose), ["app-1", "context: .", "- 5050:22"])
    assert (
        f"Created new Docker Compose suite: {generated_compose}" in result.output
    ), "Did not find success log message for compose templating"


def test_template_new_compose_invalid_image(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    runner: TestRunner,
    caplog: LogCaptureFixture,
) -> None:
    monkeypatch.chdir(tmp_path)

    result = runner.run_cli(
        [
            "-vv",
            "new",
            "compose",
            "--image",
            "non-existent.Dockerfile",
        ]
    )

    assert result.exit_code == 2
    assert "Specified Dockerfile does not exist" in caplog.text


def test_template_new_compose_invalid_replicas(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    runner: TestRunner,
    caplog: LogCaptureFixture,
) -> None:
    monkeypatch.chdir(tmp_path)
    dockerfile_mock = Path(os.path.join(str(tmp_path), "mock.Dockerfile"))
    generated_compose = Path(os.path.join(str(tmp_path), "docker-compose.yml"))
    generated_files = [str(dockerfile_mock), str(generated_compose)]
    dockerfile_mock.touch()

    result = runner.run_cli(
        [
            "-vv",
            "new",
            "compose",
            "--image",
            "mock.Dockerfile",
            "--count",
            "0",
        ]
    )

    assert result.exit_code == 2
    assert "Replica count must at least 1 but got 0" in caplog.text


def test_template_new_compose_priviledged_port(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    runner: TestRunner,
    caplog: LogCaptureFixture,
) -> None:
    monkeypatch.chdir(tmp_path)
    dockerfile_mock = Path(os.path.join(str(tmp_path), "mock.Dockerfile"))
    generated_compose = Path(os.path.join(str(tmp_path), "docker-compose.yml"))
    generated_files = [str(dockerfile_mock), str(generated_compose)]
    dockerfile_mock.touch()

    result = runner.run_cli(
        [
            "-vv",
            "new",
            "compose",
            "--image",
            "mock.Dockerfile",
            "--count",
            "1",
            "--expose",
            "100",
        ]
    )

    assert result.exit_code == 2
    assert "Cannot expose port 100 (privileged)" in caplog.text
