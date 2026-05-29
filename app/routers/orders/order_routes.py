from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.core.dependencies import sessao_banco, verificar_token
from app.routers.orders.schema import OrderSchema, OrderItemSchema, ResponseOrderSchema
from app.routers.orders.model import Order, OrderItem
from app.routers.auth.model import Users
from typing import List


order_router = APIRouter(prefix="/pedidos", tags=["Pedidos"], dependencies=[Depends(verificar_token)])

@order_router.get("/")
async def order():
    """
    Todas as rotas dos pedidos precisam de autenticação
    """
    return {"Message": "Order routa"}


@order_router.post("/pedido")
async def criar_pedidos(pedido_schema: OrderSchema, session: Session = Depends(sessao_banco)):
    novo_pedido = Order(usuario_id=pedido_schema.user_id)
    session.add(novo_pedido)
    session.commit()
    
    return {"message": f"Pedidio criaco com sucesso. ID do Pedido {novo_pedido.id}"}

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(sessao_banco), usuario : Users = Depends(verificar_token)):
    pedido = session.query(Order).filter(Order.id == id_pedido).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.user_id:
        raise HTTPException(status_code=401, detail="Você não tem autorização de realizar esta ação")
    pedido.status = "CANCELADO"
    session.commit()
    return {
        "message": f"Pedido nº {pedido.id} cancelado com sucesso!!!",
        "pedido" : pedido
    }
    
@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(sessao_banco), usuario : Users = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para acessar")
    else:
        pedidos = session.query(Order).options(joinedload(Order.items)).all()
        return {
            "pedidos": pedidos
        }
        
@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int,
                                item_pedido_schema: OrderItemSchema, 
                                session:Session = Depends(sessao_banco), 
                                usuario : Users = Depends(verificar_token)):
    pedido = session.query(Order).options(joinedload(Order.items)).filter(Order.id == id_pedido).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não existente")
    elif not usuario.admin and usuario.id != pedido.user_id:
        raise HTTPException(status_code=401, detail="Você não tem autorização para esta ação")
    
    item_pedido = OrderItem(
        quantidade=item_pedido_schema.quantity,
        sabor=item_pedido_schema.sabor,
        tamanho=item_pedido_schema.size,
        preco_unitario=item_pedido_schema.unit_price,
        
    )
    
    pedido.items.append(item_pedido)
    pedido.calculate_total_price()
    session.commit()
    
    session.refresh(item_pedido)
    session.refresh(pedido)
    
    return {
        "message" : "Item criado com sucesso",
        "item_id" : item_pedido.id,
        "preco_pedido" : pedido.price
    }
    
@order_router.delete("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido: int,
                                session:Session = Depends(sessao_banco), 
                                usuario : Users = Depends(verificar_token)):
    item_pedido = session.query(OrderItem).filter(OrderItem.id == id_item_pedido).first()
    
    if not item_pedido:
        raise HTTPException(status_code=404, detail="item do pedido não existente")
    
    pedido = session.query(Order).options(joinedload(Order.items)).filter(Order.id ==item_pedido.order_id).first()
    
    if not usuario.admin and usuario.id != pedido.user_id:
        raise HTTPException(status_code=401, detail="Você não tem autorização para esta ação")
    
            
    pedido.items.remove(item_pedido)
    session.delete(item_pedido)
    pedido.calculate_total_price()
    session.commit()
    
    return {
        "message" : "Item removido com sucesso",
        "itens_pedido": pedido.items,
        "pedido": pedido
        
    }
    
    
@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session :Session = Depends(sessao_banco), usuario: Users = Depends(verificar_token)):

    pedido = session.query(Order).filter(Order.id == id_pedido).first()
    
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido inexistente")
    if not usuario.admin and usuario.id != pedido.user_id:
        raise HTTPException(status_code=401, detail="Usuario não tem permissão para modificar")
    pedido.status = "FINALIZADO"
    session.commit()
    
    return {
        "message": f"Pedido número {pedido.id} foi finalizado com sucesso",
        "pedido": pedido
        
    }
    
@order_router.get("/pedido/{id_pedido}")
async def vizualizar_pedido(id_pedido: int, session: Session = Depends(sessao_banco), usuario: Users = Depends(verificar_token)):
    
    pedido = session.query(Order).filter(Order.id == id_pedido).first()
    
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido inexistente")
    if not usuario.admin and usuario.id != pedido.user_id:
        raise HTTPException(status_code=401, ddetail="Usuario não tem permissão para esta ação")
    
    return {
        "quantidade_itens_pedido": len(pedido.items),
        "pedido": pedido
    }
    
    
@order_router.get("/listar/pedidos-usuario", response_model=List[ResponseOrderSchema])
async def listar_pedidos_por_usuario(session: Session = Depends(sessao_banco), usuario : Users = Depends(verificar_token)):
    
    pedido = session.query(Order).filter(Order.user_id==usuario.id).all()
    return pedido