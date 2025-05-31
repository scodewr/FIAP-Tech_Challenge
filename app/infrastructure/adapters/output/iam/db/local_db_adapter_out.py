from app.domain.models.entities.iam.user import UserEntity
from app.domain.services.iam.db.local_db_service import LocalDbService
from app.application.ports.output.iam.db.local_db_port_out import LocalDBPortOut

class LocalDbAdapterOut(LocalDBPortOut):
    
    def __init__(self, service: LocalDbService):
        self.service = service

    def get_user(self, user: UserEntity) -> UserEntity:
        """
        Retrieve a user from the local database by user ID.
        :param user: UserEntity containing user data to be retrieved.
        :return: UserEntity instance containing user data.
        """
        return self.service.get_user(user)

    def get_user_by_login(self, user: UserEntity) -> UserEntity:
        """
        Retrieve a user from the local database by user login.
        :param user: UserEntity containing user data to be retrieved.
        :return: UserEntity instance containing user data.
        """
        return self.service.get_user_by_login(user)