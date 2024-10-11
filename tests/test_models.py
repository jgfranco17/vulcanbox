import datetime as dt
from unittest.mock import MagicMock, patch

from vulcanbox.core.models import DockerImage


def test_docker_object_properties():
    test_image = DockerImage(name="test.Dockerfile", context={"foo": "bar"})
    assert not test_image.whitespace
    assert test_image.image_tag is None
    assert not test_image.is_built()


def test_docker_object_json() -> None:
    expected_json = {
        "name": "test.Dockerfile",
        "tag": None,
        "context": {"foo": "bar"},
    }
    test_image = DockerImage(name="test.Dockerfile", context={"foo": "bar"})
    assert test_image.json() == expected_json


@patch("vulcanbox.core.models.dt.datetime")
def test_docker_object_container_naming(mock_datetime: MagicMock):
    # Mock datetime for control
    fixed_timestamp = "20240801-123456"
    mock_datetime_instance = MagicMock()
    mock_datetime_instance.strftime.return_value = fixed_timestamp
    mock_datetime.now.return_value = mock_datetime_instance

    result = DockerImage._DockerImage__get_image_name("base:latest")
    assert result == f"vulcanbox-base-latest-{fixed_timestamp}"
