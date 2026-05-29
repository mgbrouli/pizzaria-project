from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase,sessionmaker

#Primeiro cria a conxaõ
db = create_engine("sqlite:///banco.db")

Session_m = sessionmaker(autoflush=False, bind=db)

#Segundo base do banco de dados
class Base(DeclarativeBase):
    pass
