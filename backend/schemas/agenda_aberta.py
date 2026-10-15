# backend/models/agenda_aberta.py

from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from backend.database.base import Base


class AgendaAberta(Base):
    __tablename__ = "agenda_aberta"

    id = Column(Integer, primary_key=True, index=True)

    profissional_id = Column(Integer, ForeignKey("profissionais.id"), nullable=False)

    data = Column(Date, nullable=False)
