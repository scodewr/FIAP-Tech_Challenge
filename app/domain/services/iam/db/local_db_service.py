from app.domain.models.entities.iam.user import UserEntity
from app.domain.exceptions.iam.db.general_exceptions import UserAlreadyExistsError

class LocalDbService:
    """
    LocalDbService is a service that provides an interface for interacting with a local database.
    It is used to manage user data and other related operations.
    """

    db = {
        "users": {
            "admin": {
            "id": 1,
            "first_name": "Admin",
            "last_name": "Service User",
            "password": "admin123",
            "permissions": ["admin"]
            }
        }
    }


    def register_user(self, user: UserEntity):
        """
        Registers a new user in the local database.
        
        :param user: User data to be registered.
        :return: The registered user data.
        """

        login = user.login

        if login in self.db["users"]:
            raise UserAlreadyExistsError(f"Usuário '{login}' já existe.")
        
        user_dict = user.model_dump()
        user_dict["id"] = len(self.db["users"]) + 1

        self.db["users"][login] = user_dict

    def delete_user(self, user_id):
        raise NotImplementedError("Delete user operation is not implemented in LocalDbService.")