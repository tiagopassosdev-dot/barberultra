# backend/schemas/agenda_aberta.py

from datetime import date

from pydantic import BaseModel


class AgendaAbertaCreate(BaseModel):
    profissional_id: int
    data: date


class AgendaAbertaResponse(BaseModel):
    id: int
    profissional_id: int
    data: date

    model_config = {"from_attributes": True}
