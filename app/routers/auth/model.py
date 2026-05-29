from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

if TYPE_CHECKING:
    from app.routers.orders.model import Order
    from app.routers.cardapio.model import Product, Image
    

class Users(Base):
    __tablename__ = "users"
    
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name : Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String)
    active: Mapped[bool] = mapped_column(default=True)
    admin : Mapped[bool] = mapped_column(default=False)
    enterprise_id: Mapped[Optional[int]] = mapped_column(ForeignKey("enterprises.id"), nullable=True)
    
    orders: Mapped[List["Order"]] = relationship(back_populates="user_ref")
    enterprise_ref : Mapped[Optional["Enterprise"]] = relationship(back_populates="user_ref")
    
    
    
class Enterprise(Base):
    __tablename__ = "enterprises"
    
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    #Dados gerais
    name_est : Mapped[str] = mapped_column(String(20), nullable=False)
    cnpj_est : Mapped[str] = mapped_column(String(20), nullable=False)
    short_description : Mapped[str] = mapped_column(String(255), nullable=False)
    whastapp : Mapped[str] = mapped_column(String(20), nullable=False)
    
    #Endereço
    
    logradouro : Mapped[str] = mapped_column(String(150), nullable=False)
    bairro : Mapped[str] = mapped_column(String(100), nullable=False)
    cidade : Mapped[str] = mapped_column(String(100), nullable=False)
    estado : Mapped[str] = mapped_column(String(2), nullable=False)
    cep: Mapped[str] = mapped_column(String(10), nullable=False)
    
    #Aparencia
    
    primary_color: Mapped[str] = mapped_column(String(7), default="#0d6efd")
    bg_color: Mapped[str] = mapped_column(String(7), default="#ffffff")
    text_color: Mapped[str] = mapped_column(String(7), default="#212529")
    
    logo_path: Mapped[str] = mapped_column(String(255), nullable=False)
    banner_path: Mapped[str] = mapped_column(String(255), nullable=False)
    
    products_ref : Mapped[List["Product"]] = relationship("Product",back_populates="enterprise_ref", cascade="all, delete-orphan")
    image_ref : Mapped[List["Image"]] = relationship("Image", back_populates="enterprise_ref", cascade="all, delete-orphan")
    user_ref : Mapped[List["Users"]]= relationship("Users", back_populates="enterprise_ref", cascade="all, delete-orphan")
    
    plan : Mapped[str] = mapped_column(String(20), default="GRATIS")
    active: Mapped[bool] = mapped_column(default=True)
    