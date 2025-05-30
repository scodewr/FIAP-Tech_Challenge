from pydantic import BaseModel
from typing import List

class UserRequestDTO(BaseModel):
    login: str
    first_name: str
    last_name: str
    password: str
    permissions: List[str]