
class LogInPortIn:
    """
    Interface for the input port of the LogIn use case.
    This port defines the contract for logging in a user.
    """

    def log_in(self, login: str, password: str) -> str:
        """
        Logs in a user with the provided email and password.

        :param login: The user's username.
        :param password: The user's password.
        :return: A JWT access token if the login is successful.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")