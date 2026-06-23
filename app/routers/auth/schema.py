from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    active : bool | None = True
    admin : bool | None = False
    enterprise_id : int | None = None
    
    model_config = ConfigDict(from_attributes=True)
    
    
class LoginSchema(BaseModel):
    email: str
    password: str
    
    model_config = ConfigDict(from_attributes=True)
    
    
class EnterpriseSchema(BaseModel):
    name_est: str
    cnpj_est: str
    short_description: str
    whatsapp: str
    logradouro: str
    bairro: str
    cidade: str
    estado: str
    cep: str
    
    active: bool | None = True
    plan: str
    
    model_config = ConfigDict(from_attributes=True)
    
    
    