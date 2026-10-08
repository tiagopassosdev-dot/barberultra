from pydantic import BaseModel
from pydantic import Field


class ServicoCreate(BaseModel):
    nome: str = Field(..., min_length=2)
    duracao_minutos: int = Field(..., gt=0)
    preco: float = Field(..., gt=0)


class ServicoResponse(BaseModel):
    id: int
    nome: str
    duracao_minutos: int
    preco: float
    ativo: bool

    model_config = {
        "from_attributes": True
    }