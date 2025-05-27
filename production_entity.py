from typing import Optional
from pd_categories_enum import ProductionCategoryEnum
from pydantic import BaseModel, model_validator

class ProductionEntity(BaseModel):
    id: int
    control: str
    product: str 
    category: Optional[ProductionCategoryEnum] = None 
    year: int
    production: int

    @model_validator(mode="after")
    def set_category(cls, values):
        # Calcula o campo 'category' com base no 'control'
        if not values.category and values.control:
            try:
                categoryControl = ProductionEntity.getControl(values.control).upper()
                values.category = ProductionCategoryEnum[categoryControl]
            except ValueError:
                raise ValueError(f"O valor '{categoryControl}' não é válido para a categoria.")
        return values
    
    @staticmethod
    def getControl(control: str) -> str:
        underscore_position: int = control.find("_")
        return control[:underscore_position]
    
    