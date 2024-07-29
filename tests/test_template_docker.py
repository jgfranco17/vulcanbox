import os
from pathlib import Path

from pytest import LogCaptureFixture, MonkeyPatch

from tests.conftest import TestRunner
from tests.helpers import assert_files_created, assert_lines_in_file


def test_template_new_image_sane(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    runner: TestRunner,
    caplog: LogCaptureFixture,
) -> None:
    monkeypatch.chdir(tmp_path)
    dockerfile_name = "test.Dockerfile"
    expected_files = [dockerfile_name]

    result = runner.run_cli(
        ["-vv", "docker", "new", "--name", dockerfile_name, "--base", "ubuntu:20.04"]
    )

    assert result.exit_code == 0
    assert_files_created(str(tmp_path), expected_files)
    expected_file_path = os.path.join(str(tmp_path), dockerfile_name)
    assert_lines_in_file(expected_file_path, ["FROM ubuntu:20.04 AS build-stage"])
    assert (
        f"Wrote to file: {expected_file_path}" in caplog.text
    ), f"Did not find success log message for image templating"


def test_template_new_image_with_exposed_ports(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    runner: TestRunner,
    caplog: LogCaptureFixture,
) -> None:
    monkeypatch.chdir(tmp_path)
    dockerfile_name = "test.Dockerfile"
    expected_files = [dockerfile_name]

    result = runner.run_cli(
        [
            "-vv",
            "docker",
            "new",
            "--name",
            dockerfile_name,
            "--base",
            "ubuntu:20.04",
            "--expose",
            "5050",
            "--expose",
            "8080",
        ]
    )

    assert result.exit_code == 0
    assert_files_created(str(tmp_path), expected_files)
    expected_file_path = os.path.join(str(tmp_path), dockerfile_name)
    assert_lines_in_file(expected_file_path, ["EXPOSE 5050", "EXPOSE 8080"])
    assert (
        f"Wrote to file: {expected_file_path}" in caplog.text
    ), f"Did not find success log message for image templating"


def test_template_new_image_invalid_name(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    runner: TestRunner,
    caplog: LogCaptureFixture,
) -> None:
    monkeypatch.chdir(tmp_path)

    result = runner.run_cli(
        [
            "-vv",
            "docker",
            "new",
            "--name",
            "not-valid.txt",
        ]
    )

    assert result.exit_code == 2
    assert "Name is invalid" in caplog.text


def test_template_new_image_file_already_exists(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    runner: TestRunner,
    caplog: LogCaptureFixture,
) -> None:
    monkeypatch.chdir(tmp_path)
    unoriginal_file_name = "exists.Dockerfile"
    existing_file = Path(os.path.join(str(tmp_path), unoriginal_file_name))
    existing_file.touch()
    result = runner.run_cli(
        [
            "-vv",
            "docker",
            "new",
            "--name",
            unoriginal_file_name,
        ]
    )

    assert result.exit_code == 2
    assert f"Dockerfile already exists: {str(existing_file)}" in caplog.text
