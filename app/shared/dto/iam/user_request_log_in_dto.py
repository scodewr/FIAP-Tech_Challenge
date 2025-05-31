from pydantic import BaseModel

class UserRequestLoginDTO(BaseModel):
    login: str
    password: str
