from pydantic import BaseModel
from typing import ClassVar

class ExportationEntity(BaseModel):

    id: int
    country: str
    year: int
    exportation: int

    schema_equivalence: ClassVar[dict[str, str]] = {
        "Id": "id",
        "país": "country"
    }