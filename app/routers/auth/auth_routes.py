from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.routers.auth.model import Users, Enterprise
from app.core.dependencies import sessao_banco, verificar_token, verificar_refresh_token_cookie
from app.routers.auth.schema import UserSchema, LoginSchema, EnterpriseSchema
from app.core.config import senha_criptografada, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone





auth_router = APIRouter(prefix="/auth", tags=["Auth"])


def criar_token(id_usuario: int, tipo_token: str = "access",duracao_token : timedelta = None):
    if not duracao_token:
        duracao_token = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dict_info = {"sub": str(id_usuario),"type": tipo_token,"exp": data_expiracao}
    
    token = jwt.encode(dict_info,SECRET_KEY, ALGORITHM)
    
    return token


def autenticar_usuario(email: str, senha: str, session: Session):
    usuario = session.query(Users).filter(Users.email==email).first()
    if not usuario:
        return False
    elif not senha_criptografada.verify(senha, usuario.password):
        return False
    
        
    return usuario


@auth_router.get("/")
async def auth():
    return {"Message": "ROta auth"}

@auth_router.post("/create_user")
async def create_user(usuario_schema: UserSchema, session:Session = Depends(sessao_banco) ):

    usuario_existente = session.query(Users).filter(Users.email == usuario_schema.email).first()

    if usuario_existente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail do usuario já existe")
    else:
        novo_usuario = Users(
            name=usuario_schema.name, 
            email=usuario_schema.email, 
            password=senha_criptografada.hash(usuario_schema.password),
            active=usuario_schema.active,
            admin=usuario_schema.admin,
            enterprise_id = usuario_schema.enterprise_id
            )

        session.add(novo_usuario)
        session.commit()

        return {"message": f"Usuario cadastrado com sucesso {usuario_schema.email}"}
    
@auth_router.post("/create_enterprise")
async def criar_enterprise(enterprise_schema: EnterpriseSchema, session:Session = Depends(sessao_banco)):
    empresa_existente = session.query(Enterprise).filter(Enterprise.cnpj_est == enterprise_schema.cnpj_est).first()
    
    if empresa_existente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empresa já cadastrada, por favor tente fazer login")
    else:
        nova_empresa = Enterprise(
            name_est = enterprise_schema.name_est,
            cnpj_est = enterprise_schema.cnpj_est,
            short_description = enterprise_schema.short_description,
            whatsapp = enterprise_schema.whatsapp,
            logradouro = enterprise_schema.logradouro,
            bairro = enterprise_schema.bairro,
            cidade = enterprise_schema.cidade,
            estado = enterprise_schema.estado,
            cep=enterprise_schema.cep,
            plan=enterprise_schema.plan
        )
        
        session.add(nova_empresa)
        session.commit()
        
        return {"message": f"{status.HTTP_201_CREATED} Empresa criada com sucesso!"}
        
    
@auth_router.post("/login")
async def login(login_schema : LoginSchema ,response: Response ,session: Session = Depends(sessao_banco)):
    usuario = autenticar_usuario(login_schema.email, login_schema.password, session=session)
    
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario não encontrado")
    else:
        access_token = criar_token(usuario.id, tipo_token="access")
        refresh_token = criar_token(usuario.id, tipo_token="refresh", duracao_token=timedelta(days=7))

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=604800
            
        )
    
        return {"access_token": access_token,
                "token_type": "Bearer"
                }

@auth_router.post("/logout")
async def logout(response: Response):
    # Deleta o cookie do navegador do usuário
    response.delete_cookie(key="refresh_token")
    return {"message": "Sessão encerrada com sucesso"}

@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends() ,session: Session = Depends(sessao_banco)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session=session)
    
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario não encontrado")
    else:
        access_token = criar_token(usuario.id, tipo_token="access")
        return {"access_token": access_token,
                "token_type": "Bearer"
                }
    
@auth_router.post("/refresh")
async def use_refresh_toke( usuario : Users = Depends(verificar_refresh_token_cookie)):
    
    novo_access_token = criar_token(usuario.id, tipo_token="access")
    
    return{
        "access_token": novo_access_token,
        "token_type": "Bearer"
    }