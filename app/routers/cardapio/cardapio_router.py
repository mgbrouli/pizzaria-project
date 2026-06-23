from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import Dict
from app.core.dependencies import sessao_banco, verificar_token
from app.routers.cardapio.model import Product, Image
from app.routers.cardapio.schema import ProductSchema, ImageSchema
from app.routers.auth.model import Enterprise, Users



cardapio_router = APIRouter(prefix="/cardapio", tags=["Cardapio"])

   

@cardapio_router.get("/", response_model=Dict[str, ProductSchema])
async def pegar_produtos( session: Session = Depends(sessao_banco)):
    
    """
        Rota dedidcada a criação e vizualização de produtos do cardapio,
        somente empresas podem editar e clientes podem comprar
    """
    
    
    produtos = session.query(Product).options(joinedload(Product.image), joinedload(Product.enterprise_ref)).all()
    
    
    resultado = {}
    
    for produto in produtos:
        image_convertida = None
        
        
        if produto.image:
            conteudo_image= produto.image.image
            if isinstance(conteudo_image, bytes):
                conteudo_image = conteudo_image.decode('utf-8')
                
            image_convertida = {
                "name": produto.image.name,
                "image": conteudo_image
            }
        empresa_dados = None
        if produto.enterprise_id:
            empresa_dados = {
                "id": produto.enterprise_ref.id,
                "name": produto.enterprise_ref.name_est
            }
            
        resultado[str(produto.id)] = {
            "name": produto.name,
            "ingredients": produto.ingredients,
            "price": produto.price,
            "image": image_convertida,
            "empresa": empresa_dados
        }
        
    return resultado
    



        
    
@cardapio_router.post("/adiciona_produto")
async def criar_produto(produto_schema : ProductSchema, user : Users = Depends(verificar_token), session: Session = Depends(sessao_banco)):
    
    
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
        
        imagem_em_bytes =  produto_schema.image.image.encode('utf-8')
        
        new_image = Image(
            name = produto_schema.image.name,
            image = imagem_em_bytes,
            product_id = new_product.id,
            enterprise_id = user.enterprise_id
        )
        session.add(new_image)    
        session.commit()
    except Exception as e:
        session.rollback()
        
        print("\n" + "="*50)
        print(f"ERRO REAL DETECTADO: {type(e).__name__} - {e}")
        print("="*50 + "\n")
        
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail="Erro interno ao salvar o produto e a imagem."
    )
    return {"detail": "Produto e imagem criados com sucesso!"}


#Todo - Fazer a criação dos produtos e imagens e associar.

            
@cardapio_router.put("/editar_produto/{produto_id}")
async def editar_produto(produto_id: int, produto_schema: ProductSchema, user: Users = Depends(verificar_token), session: Session = Depends(sessao_banco)):
    # 1. Busca o produto
    produto = session.query(Product).filter(Product.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
        
    # 2. Trava de Segurança: O produto pertence à empresa do usuário logado?
    if produto.enterprise_id != user.enterprise_id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para alterar produtos de outra empresa")
        
    # 3. Atualiza os dados
    produto.name = produto_schema.name
    produto.ingredients = produto_schema.ingredients
    produto.price = produto_schema.price
    
    # Se vier imagem nova no schema, atualiza a tabela Image aqui também...
    
    session.commit()
    return {"detail": "Produto atualizado com sucesso!"}


@cardapio_router.delete("/deletar_produto/{produto_id}")
async def deletar_produto(produto_id: int, user: Users = Depends(verificar_token), session: Session = Depends(sessao_banco)):
    produto = session.query(Product).filter(Product.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
        
    if produto.enterprise_id != user.enterprise_id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para deletar este produto")
        
    session.delete(produto)
    session.commit()
    return {"detail": "Produto removido com sucesso!"}