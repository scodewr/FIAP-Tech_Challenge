from pydantic import BaseModel, model_validator

class ImportationEntity(BaseModel):

    id: int
    country: str
    year: int
    importation: int
    