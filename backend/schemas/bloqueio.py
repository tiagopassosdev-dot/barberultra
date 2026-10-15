from datetime import datetime

from pydantic import BaseModel


class BloqueioCreate(BaseModel):
    profissional_id: int

    data_hora_inicio: datetime

    data_hora_fim: datetime

    motivo: str


class BloqueioResponse(BaseModel):
    id: int
    profissional_id: int

    data_hora_inicio: datetime

    data_hora_fim: datetime

    motivo: str | None

    model_config = {"from_attributes": True}
