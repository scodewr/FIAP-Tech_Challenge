from app.domain.models.entities.iam.user import UserEntity
from typing import List

class PermissionsPortOut:
    """
    Interface for handling user permissions validation in the IAM module.
    This port is used to validate user permissions during the login process.
    """
    def validate_user(self, user_data: UserEntity):
        """
        Method to validate user data.

        :param user_data: UserEntity containing user data to be validated.
        :raises UserNotFoundError: If the user is not found.
        :raises InvalidPasswordError: If the password is invalid.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def validate_access_permissions(self, login: str, permission: str):
        """
        Method to handle successful login.

        :param login: UserEntity containing user data to be validated.
        :param permission: The permission to validate for the user.
        :return: A string representing the access token for the user.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")