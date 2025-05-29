from pydantic import BaseModel

class ExportationEntity(BaseModel):

    id: int
    country: str
    year: int
    exportation: int