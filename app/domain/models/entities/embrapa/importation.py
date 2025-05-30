from pydantic import BaseModel
from typing import ClassVar

class ImportationEntity(BaseModel):

    id: int
    country: str
    year: int
    importation: int

    schema_equivalence: ClassVar[dict[str, str]] = {
        "país": "country",
    }