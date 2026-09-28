from fastapi import APIRouter

order_router = APIRouter (prefix="/pedidos", tags=["pedidos"])

@order_router.get("/")
async def pedidos():
    return {"Mensagem:", "você acessou a rota de pedidos"}

