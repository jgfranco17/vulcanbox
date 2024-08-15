"""VulcanBox exceptions."""

from typing import Final, Optional


class ExitCode:
    """Class for VulcanBox Exit Codes."""

    SUCCESS: Final[int] = 0
    RUNTIME_ERROR: Final[int] = 1
    INPUT_ERROR: Final[int] = 2


class VulcanBoxBaseError(Exception):
    """A base VulcanBox Error class.

    Contains a message, exit_code and help text show to the user

    exit_code should be a member of ExitCode
    """

    def __init__(self, message: str, exit_code: int, help_text: Optional[str]):
        """Init an VulcanBox Error."""
        self.message = message
        self.exit_code = exit_code
        if help_text is None:
            help_text = "Help is available with --help. Use the -v flag to increase output verbosity."
        self.help_text = help_text
        super().__init__(self.message)


class VulcanBoxRuntimeError(VulcanBoxBaseError):
    """General VulcanBox CLI Error class."""

    def __init__(
        self,
        message: str,
        help_text: Optional[str] = None,
    ) -> None:
        """Init an VulcanBox CLI Error."""
        self.message = message
        super().__init__(self.message, ExitCode.RUNTIME_ERROR, help_text)


class VulcanBoxInputError(VulcanBoxBaseError):
    """VulcanBox User Input Error class."""

    def __init__(
        self,
        message: str,
        help_text: Optional[str] = None,
    ) -> None:
        """Init an VulcanBox Input Error."""
        self.message = message
        super().__init__(self.message, ExitCode.INPUT_ERROR, help_text)
