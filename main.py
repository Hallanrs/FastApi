from fastapi import FastAPI
#como executar a api: uvicorn main:app --reload

app = FastAPI()

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)