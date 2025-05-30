from pydantic import BaseModel
from typing import List

class UserEntity(BaseModel):
    id: int = None
    login: str
    first_name: str
    last_name: str
    password: str
    permissions: List[str]