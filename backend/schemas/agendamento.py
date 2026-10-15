from datetime import datetime
from pydantic import BaseModel

class AgendamentoCreate(BaseModel):
    cliente_id: int
    profissional_id: int
    servicos: list[int]
    data_hora_inicio: datetime

class AgendamentoResponse(BaseModel):
    id: int
    cliente_id: int
    profissional_id: int
    servicos: list[int]
    data_hora_inicio: datetime
    data_hora_fim: datetime
    status: str
    model_config = {
        "from_attributes": True
    }  # permite que o Pydantic crie o schema a partir de um objeto
