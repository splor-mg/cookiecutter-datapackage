import log


class Error(Exception):
    """base class for errors"""


class MissingPackageError(Error):
    """
    Exception raised when one or more required packages from project dependencies are missing.

    Attributes:
    key_attribute -- environment variable
    """

    def __init__(self, vars):
        self.environment_variable, logger = vars
        self.message = f"Cannot continue with missing packages installations: {', '.join(self.environment_variable)}"
        self.log = logger.error(f"Required packages are missing: {', '.join(self.environment_variable)}")
        super().__init__(self.message)


class WrongVersionPackageError(Error):
    """
    Exception raised when one or more versions of the required packages from project dependencies are wrong.

    Attributes:
    key_attribute -- environment variable
    """

    def __init__(self, vars):
        self.environment_variable, logger = vars
        self.message = f"{', '.join([f'{pac} (Installed: {ins}, Expected: {exp})' for pac, ins, exp in self.environment_variable])}"
        self.log = logger.error(f"Required packages with wrong versions: {self.message}")
        super().__init__(f"Cannot continue with wrong version packages: {self.message}")
