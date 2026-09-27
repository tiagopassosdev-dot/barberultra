from fastapi import FastAPI

from backend.database.base import Base
from backend.database.connection import engine

# cria tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BarberUltra API"
)


@app.get("/")
def root():
    return {
        "status": "online"
    }