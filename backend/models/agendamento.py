from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy import DateTime 
from backend.database.base import Base



class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    data_hora_inicio = Column(DateTime, nullable=False)
    data_hora_fim = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False, default="agendado")
