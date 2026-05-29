from pydantic import BaseModel, ConfigDict
from typing import List


class OrderSchema(BaseModel):
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)
    

class OrderItemSchema(BaseModel):
    quantity: int
    sabor: str
    size: str
    unit_price: float
    
    model_config = ConfigDict(from_attributes=True)
    

class ResponseOrderSchema(BaseModel):
    id: int
    status: str
    price: float
    items: List[OrderItemSchema]
    
    model_config = ConfigDict(from_attributes=True)