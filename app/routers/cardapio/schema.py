from pydantic import BaseModel, ConfigDict
from typing import Optional

class ImageSchema(BaseModel):
    
    name: str
    image: str
        
    model_config = ConfigDict(from_attributes=True)

class ProductSchema(BaseModel):
    name: str
    ingredients: str
    price: float
    
    image: Optional[ImageSchema]
    
    model_config = ConfigDict(from_attributes=True)    

