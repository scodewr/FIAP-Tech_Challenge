from typing import Optional, ClassVar
from pydantic import BaseModel, Field, model_validator
from enum import Enum
from app.shared.util.util import Util

class ProductionCategoryEnum(Enum):
    VM = "Vinho de Mesa"
    VV = "Vinho Fino de Mesa (Vinifera)"
    SU = "Suco"
    DE = "Derivados"

class ProductionEntity(BaseModel):
    id: int
    control: str
    product: str
    category: Optional[str] = None
    year: int
    production: float

    @model_validator(mode="after")
    def set_category(self):
        """
        Define o campo 'category' com base no 'control'.
        """
        if not self.category and self.control:
            try:
                category_control = Util.extract_prefix(self.control).upper()
                self.category = ProductionCategoryEnum[category_control].value
            except KeyError:
                raise ValueError(f"O valor '{category_control}' não é válido para a categoria.")
        return self

    schema_equivalence: ClassVar[dict[str, str]] = {
            "produto": "product"
        }
        