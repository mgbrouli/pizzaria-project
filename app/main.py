from fastapi import FastAPI
from app.core.database import db, Base


Base.metadata.create_all(bind=db)
app = FastAPI()


from app.routers.auth.auth_routes import auth_router
from app.routers.orders.order_routes import order_router
from app.routers.cardapio.cardapio_router import cardapio_router

app.include_router(auth_router)
app.include_router(order_router)
app.include_router(cardapio_router)