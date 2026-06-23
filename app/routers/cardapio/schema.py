from pydantic import BaseModel, ConfigDict
from typing import Optional


class EnterpriseCardapioSchema(BaseModel):
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)


class ImageSchema(BaseModel):
    
    name: str
    image: str
        
    model_config = ConfigDict(from_attributes=True)

class ProductSchema(BaseModel):
    name: str
    ingredients: str
    price: float
    
    image: Optional[ImageSchema]
    empresa: Optional[EnterpriseCardapioSchema]
    
    model_config = ConfigDict(from_attributes=True)    

