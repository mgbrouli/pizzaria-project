from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import Dict
from app.core.dependencies import sessao_banco, verificar_token
from app.routers.cardapio.model import Product, Image
from app.routers.cardapio.schema import ProductSchema, ImageSchema
from app.routers.auth.model import Enterprise, Users



cardapio_router = APIRouter(prefix="/cardapio", tags=["Cardapio"])

@cardapio_router.get("/")
async def cardapio():
    """
        Rota dedidcada a criação e vizualização de produtos do cardapio,
        somente empresas podem editar e clientes podem comprar
    """
    
    
@cardapio_router.post("/adiciona_produto")
async def criar_produto(produto_schema : ProductSchema, image_schema : ImageSchema ,user : Users = Depends(verificar_token), session: Session = Depends(sessao_banco)):
    
    
    if not user.enterprise_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Este usuario não esta vinculado a nenhuma empresa")
    
    enterprise_verificado = session.query(Enterprise.id).filter(user.enterprise_id == Enterprise.id).first()
    
    if not enterprise_verificado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não existe no banco de dados")
    

    try:
        new_product = Product(
            name= produto_schema.name,
            ingredients=produto_schema.ingredients,
            price=produto_schema.price,
            enterprise_id=user.enterprise_id
            
        )
        
        session.add(new_product)
        session.flush()
        
        new_image = Image(
            name=image_schema.name,
            image= image_schema.image,
            product_id = new_product.id,
            enterprise_id=user.enterprise_id
                        
        )
        
        session.add(new_image)
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail="Erro interno ao salvar o produto e a imagem."
    )
    return {"detail": "Produto e imagem criados com sucesso!"}


#Todo - Fazer a criação dos produtos e imagens e associar.

@cardapio_router.get("/", response_model=Dict[str, ProductSchema])
async def pegar_produtos( session: Session = Depends(sessao_banco)):
    produtos = session.query(Product).all()
    
    return {str(produto.id) : produto for produto in produtos}
        
    