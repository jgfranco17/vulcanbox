from vulcanbox.errors import (
    ExitCode,
    VulcanBoxBaseError,
    VulcanBoxInputError,
    VulcanBoxRuntimeError,
)


def test_vulcanbox_base_error():
    message = "Base error occurred"
    exit_code = ExitCode.RUNTIME_ERROR
    help_text = "This is a help text"
    error = VulcanBoxBaseError(message, exit_code, help_text)
    assert error.message == message
    assert error.exit_code == exit_code
    assert error.help_text == help_text


def test_vulcanbox_runtime_error_default_help_text():
    message = "Runtime error occurred"
    error = VulcanBoxRuntimeError(message)
    assert error.message == message
    assert error.exit_code == ExitCode.RUNTIME_ERROR
    assert error.help_text is not None
    assert "Help is available" in error.help_text


def test_vulcanbox_input_error_default_help_text():
    message = "Input error occurred"
    error = VulcanBoxInputError(message)
    assert error.message == message
    assert error.exit_code == ExitCode.INPUT_ERROR
    assert error.help_text is not None
    assert "Help is available" in error.help_text


def test_vulcanbox_runtime_error_custom_help_text():
    message = "Runtime error occurred"
    help_text = "Custom help text"
    error = VulcanBoxRuntimeError(message, help_text)
    assert error.message == message
    assert error.exit_code == ExitCode.RUNTIME_ERROR
    assert error.help_text == help_text


def test_vulcanbox_input_error_custom_help_text():
    message = "Input error occurred"
    help_text = "Custom help text"
    error = VulcanBoxInputError(message, help_text)
    assert error.message == message
    assert error.exit_code == ExitCode.INPUT_ERROR
    assert error.help_text == help_text
