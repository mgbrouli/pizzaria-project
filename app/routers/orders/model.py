from typing import TYPE_CHECKING, List
from sqlalchemy import ForeignKey, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.routers.auth.model import Users
    

class Order(Base):
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status : Mapped[str] = mapped_column(String(20), default="PENDENTE")
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    price: Mapped[float] = mapped_column(Float, default=0.0)
    
    user_ref:  Mapped["Users"] = relationship(back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship(back_populates="order_ref", cascade="all, delete-orphan", lazy="joined")
    
    
    def calculate_total_price(self) -> None:
        if not self.items:
            self.price: float = 0.0
            return
        self.price = sum(
            float(item.price or 0.0) * int(item.quantity or 1)
            for item in self.items
        )
    
class OrderItem(Base):
    __tablename__ = "order_items"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    quantity: Mapped[int] = mapped_column(default=1)
    observations: Mapped[str] = mapped_column(String(100), default="Padrão")
    
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    order_ref: Mapped["Order"] = relationship(back_populates="items")
    