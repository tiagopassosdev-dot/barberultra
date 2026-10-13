from pydantic import BaseModel
from pydantic import Field


class ServicoCreate(BaseModel):
    nome: str = Field(..., min_length=2)
    preco: float = Field(..., gt=0)


class ServicoResponse(BaseModel):
    id: int
    nome: str
    preco: float
    ativo: bool

    model_config = {"from_attributes": True}
