from typing import TYPE_CHECKING
from sqlalchemy import String, Float, LargeBinary, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


if TYPE_CHECKING:
    from app.routers.auth.model import Enterprise

class Product(Base):
    __tablename__ = "products"
    
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name : Mapped[str] = mapped_column(String(100))
    ingredients : Mapped[str]
    price: Mapped[float] = mapped_column(Float, default=0.0)
    
    enterprise_id: Mapped[int] = mapped_column(ForeignKey("enterprises.id"))
    image_ref : Mapped["Image"] = relationship("Image", uselist=False , back_populates="product_ref", lazy="joined", cascade="all, delete-orphan")
    
    enterprise_ref : Mapped["Enterprise"] = relationship(back_populates="products_ref")
    
    
class Image(Base):
    __tablename__ = "images"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name : Mapped[str] = mapped_column(String(100), nullable=False)
    image : Mapped[bytes] = mapped_column(LargeBinary)
    
    product_id : Mapped[int] = mapped_column(ForeignKey("products.id"))
    enterprise_id : Mapped[int] = mapped_column(ForeignKey("enterprises.id"))
    
    product_ref : Mapped["Product"] = relationship("Product", back_populates="image_ref" )
    enterprise_ref : Mapped["Enterprise"] = relationship("Enterprise", back_populates="images_ref")