# backend/models/bloqueio.py

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from backend.database.base import Base


class Bloqueio(Base):
    __tablename__ = "bloqueios"

    id = Column(Integer, primary_key=True, index=True)

    profissional_id = Column(Integer, ForeignKey("profissionais.id"), nullable=False)

    data_hora_inicio = Column(DateTime, nullable=False)

    data_hora_fim = Column(DateTime, nullable=False)

    motivo = Column(String(255), nullable=True)
