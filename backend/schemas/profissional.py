from pydantic import BaseModel
from pydantic import Field


# Schema usado para RECEBER dados ao criar um profissional
class ProfissionalCreate(BaseModel):
    nome: str = Field(..., min_length=2)


class ProfissionalResponse(BaseModel):
    id: int
    nome: str
    ativo: bool

    model_config = {"from_attributes": True}
