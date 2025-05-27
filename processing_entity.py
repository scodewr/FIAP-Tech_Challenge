from pc_categories_enum import ProcessingCategoryEnum
from pydantic import BaseModel, field_validator
from typing import Optional

class ProcessingEntity(BaseModel):
    id: int
    control: str
    cultivate: str
    category: Optional[ProcessingCategoryEnum] = None
    year: int
    processing: int

    @field_validator("control", mode="before")
    def validate_control(cls, value):
        # Aplica a lógica de extração do control
        return ProcessingEntity.getControl(value)

    @field_validator("category", mode="before")
    def validate_category(cls, values):
        # Usa o campo 'control' já validado para determinar a categoria
        control = values.get("control")
        if control:
            return ProcessingEntity(control).value
        raise ValueError("O campo 'control' é necessário para determinar a 'category'")
    
    @staticmethod
    def getControl(control: str) -> str:
        underscore_position: int = control.find("_")
        return control[:underscore_position]