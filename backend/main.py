from fastapi import FastAPI

from backend.database.base import Base
from backend.database.connection import engine
from backend.api.Clientes import router as clientes_router
from backend.models.cliente import Cliente

# cria tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BarberUltra API"
)

app.include_router(clientes_router)  # adiciona as rotas de clientes ao app

@app.get("/")
def root():
    return {
        "status": "online"
    }
