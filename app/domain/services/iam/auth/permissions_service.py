from app.application.ports.output.iam.db.local_db_port_out import LocalDBPortOut
from app.domain.models.entities.iam.user import UserEntity
from app.domain.exceptions.iam.permission.permission_exceptions import PermissionDeniedException
from app.domain.exceptions.iam.db.db_exceptions import UserNotFoundError, InvalidPasswordError

class PermissionsService(LocalDBPortOut):

    def __init__(self, local_db_port: LocalDBPortOut):
        self.local_db_port = local_db_port

    def validate_user(self, user: UserEntity):
        """
        Validates the user and returns a list of permissions.
        :param user: UserEntity containing user data to be validated.
        :raises UserNotFoundError: If the user is not found.
        :raises InvalidPasswordError: If the password is invalid.
        """
        user_entity = self.local_db_port.get_user(user)
        if not user_entity:
            raise UserNotFoundError(f"User '{user.login}' not found.")
        
        if user.password != user_entity.password:
            raise InvalidPasswordError("Invalid password provided.")
        
        return user_entity

    
    def validate_access_permissions(self, login: str, permission: str):
        """
        Validates the user and returns a list of permissions.
        :param user: UserEntity containing user data to be validated.
        :raises UserNotFoundError: If the user is not found.
        :raises InvalidPasswordError: If the password is invalid.
        :raises PermissionDeniedException: If the user does not have permission.
        """
        user_entity = self.local_db_port.get_user_by_login(login)        
        permissions = user_entity.permissions
        if not permissions or permission not in user_entity.permissions:
            raise PermissionDeniedException(f"User '{login}' has no permissions.")
        