from pydantic import BaseModel, ConfigDict


class ProductSchema(BaseModel):
    name: str
    ingredients: str
    price: float
    
    
    model_config = ConfigDict(from_attributes=True)    

class ImageSchema(BaseModel):
    
    name: str
    image: str
    
    product_id: int
    enterprise_id: int
    
    model_config = ConfigDict(from_attributes=True)