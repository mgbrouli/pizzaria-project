from app.core.database import Session_m
from app.routers.auth.model import Users
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Cookie
from app.core.config import SECRET_KEY, ALGORITHM, oauth2_schema
from jose import jwt, JWTError


def sessao_banco():
    try:
        session = Session_m()
        yield session
    finally:
        session.close()
        
        
def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(sessao_banco) ):
    
    try:
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dict_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado!, verifique  a validade do token")
    
    usuario = session.query(Users).filter(Users.id == id_usuario ).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Invalido")
    return usuario

def verificar_refresh_token_cookie(refresh_token: str = Cookie(None), session : Session = Depends(sessao_banco)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token ausente nos cookies")
    
    
    try:
        dict_info = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        
        if dict_info.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Token do tipo invalido")
        
        id_usuario = int(dict_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Refresh token expirado ou invalido")
    
    usuario = session.query(Users).filter(Users.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=403, detail="Usuario não encontrado")
    
    return usuario
        