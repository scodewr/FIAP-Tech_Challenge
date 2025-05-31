from app.application.ports.output.iam.auth.permissions_port_out import PermissionsPortOut
from app.domain.models.entities.iam.user import UserEntity
from app.domain.exceptions.iam.db.db_exceptions import UserNotFoundError, InvalidPasswordError
from app.domain.exceptions.iam.permission.permission_exceptions import PermissionDeniedException
from app.domain.services.iam.auth.permissions_service import PermissionsService
from typing import List

class PermissionsAdapterOut(PermissionsPortOut):
    
    def __init__(self, service: PermissionsService):
        """
        Initializes the LogInAdapterOut with the service.
        :param service: An instance of LogInService to handle user login.
        """
        self.service = service

    def validate_user(self, user_data: UserEntity):
        """
        Validates the user data.
        :param user_data: UserEntity containing user data to be validated.
        :raises UserNotFoundError: If the user is not found.
        :raises InvalidPasswordError: If the password is invalid.
        """
        try:
            self.service.validate_user(user_data)
        except UserNotFoundError as e:
            raise UserNotFoundError(f"User not found: {str(e)}") from e
        except InvalidPasswordError as e:
            raise InvalidPasswordError(f"Invalid password: {str(e)}") from e

    def validate_access_permissions(self, user: UserEntity, permission: str):
        """
        Validates the user data.
        :param user_data: UserEntity containing user data to be validated.
        :raises UserNotFoundError: If the user is not found.
        :raises InvalidPasswordError: If the password is invalid.
        :raises PermissionDeniedException: If the user does not have permission.
        """
        try:
            self.service.validate_access_permissions(user, permission)
        except UserNotFoundError as e:
            raise UserNotFoundError(f"User not found: {str(e)}") from e
        except InvalidPasswordError as e:
            raise InvalidPasswordError(f"Invalid password: {str(e)}") from e
        except PermissionDeniedException as e:
            raise PermissionDeniedException(f"Permission denied: {str(e)}") from e