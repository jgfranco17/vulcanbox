import json
import os
from pathlib import Path
from unittest.mock import MagicMock

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
        [
            "-vv",
            "new",
            "image",
            "--name",
            dockerfile_name,
            "--base",
            "ubuntu:20.04",
        ]
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
            "new",
            "image",
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
            "new",
            "image",
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
            "new",
            "image",
            "--name",
            unoriginal_file_name,
        ]
    )

    assert result.exit_code == 2
    assert f"Dockerfile already exists: {str(existing_file)}" in caplog.text


def test_template_new_image_with_build(
    mock_datetime: MagicMock,
    mock_docker: MagicMock,
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    runner: TestRunner,
) -> None:
    monkeypatch.chdir(tmp_path)
    dockerfile_name = "test.Dockerfile"

    # Mock datetime
    fixed_timestamp = "20240801-123456"
    mock_datetime_instance = MagicMock()
    mock_datetime_instance.strftime.return_value = fixed_timestamp
    mock_datetime.now.return_value = mock_datetime_instance

    # Mock Docker client
    mock_docker_client = MagicMock()
    mock_image = MagicMock()
    mock_docker_client.images.build.return_value = (mock_image, ["some logs"])
    mock_docker.from_env.return_value = mock_docker_client

    result = runner.run_cli(
        [
            "-vv",
            "new",
            "image",
            "--name",
            dockerfile_name,
            "--base",
            "ubuntu:20.04",
            "--expose",
            "5050",
            "--build",
            "testing",
        ]
    )

    assert result.exit_code == 0


def test_template_new_image_json_exported(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    runner: TestRunner,
) -> None:
    monkeypatch.chdir(tmp_path)
    dockerfile_name = "test.Dockerfile"
    exported_json_file = "vulcanbox-test-ubuntu-20.04.json"
    expected_files = [dockerfile_name, exported_json_file]

    result = runner.run_cli(
        [
            "-vv",
            "new",
            "image",
            "--name",
            dockerfile_name,
            "--base",
            "ubuntu:20.04",
            "--expose",
            "5050",
            "--export-config",
        ]
    )

    assert result.exit_code == 0
    assert_files_created(str(tmp_path), expected_files)
    test_json_file = os.path.join(str(tmp_path), exported_json_file)
    with open(test_json_file, "r") as config_file:
        expected_json = {
            "name": "test.Dockerfile",
            "tag": None,
            "context": {"base_image": "ubuntu:20.04", "ports": [5050]},
        }
        json_data = json.load(config_file)
        assert json_data == expected_json
