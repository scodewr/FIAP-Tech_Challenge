from pydantic import BaseModel, model_validator

class ExportationEntity(BaseModel):

    id: int
    country: str
    year: int
    exportation: int
    