# Importa as classes do Pydantic
# BaseModel: classe base para criar schemas
# Field: permite adicionar validações aos campos
from pydantic import BaseModel, Field


# Schema usado para RECEBER dados ao criar um cliente
class ClienteCreate(BaseModel):

    # Campo obrigatório (...)
    nome: str = Field(
        ...,
        min_length=3,
        max_length=100
    )
    telefone: str = Field(
        ...,
        min_length=10,
        max_length=20
    )
# Schema usado para DEVOLVER dados ao usuário
class ClienteResponse(BaseModel):
    id: int
    nome: str
    telefone: str
    model_config = {
        "from_attributes": True
    } # permite que o Pydantic crie o schema a partir de um objeto ORM (SQLAlchemy)