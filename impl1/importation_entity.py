from pydantic import BaseModel

class ImportationEntity(BaseModel):

    id: int
    country: str
    year: int
    importation: int
    