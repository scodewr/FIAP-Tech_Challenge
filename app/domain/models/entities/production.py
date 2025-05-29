from typing import Optional
from pydantic import BaseModel, Field, model_validator
from enum import Enum

class ProductionCategoryEnum(Enum):
    VM = "Vinho de Mesa"
    VV = "Vinho Fino de Mesa (Vinifera)"
    SU = "Suco"
    DE = "Derivados"

class ProductionEntity(BaseModel):
    id: int
    control: str
    product: str
    category: Optional[ProductionCategoryEnum] = Field(default=None)
    year: int
    production: int

    @model_validator(mode="after")
    def set_category(cls, values):
        """
        Define o campo 'category' com base no 'control'.
        """
        if not values.category and values.control:
            try:
                category_control = ProductionEntity.extract_control(values.control).upper()
                values.category = ProductionCategoryEnum[category_control].value
            except KeyError:
                raise ValueError(f"O valor '{category_control}' não é válido para a categoria.")
        return values

    @staticmethod
    def extract_control(control: str) -> str:
        """
        Extrai o prefixo do campo 'control' antes do primeiro '_'.
        """
        underscore_position: int = control.find("_")
        return control[:underscore_position]