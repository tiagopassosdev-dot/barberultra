from fastapi import FastAPI

from backend.database.base import Base
from backend.database.connection import engine
from backend.api.Clientes import router as clientes_router
from backend.models.cliente import Cliente
from backend.models.servico import Servico
from backend.api.servicos import router as servicos_router
from backend.models.agendamento import Agendamento
from backend.models.agendamento_servico import AgendamentoServico

# cria tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BarberUltra API"
)

app.include_router(clientes_router)  # adiciona as rotas de clientes ao app
app.include_router(servicos_router)  # adiciona as rotas de serviços ao app

@app.get("/")
def root():
    return {
        "status": "online"
    }
