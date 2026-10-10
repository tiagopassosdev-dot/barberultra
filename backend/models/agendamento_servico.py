from sqlalchemy import Column, Integer, ForeignKey

from backend.database.base import Base


class AgendamentoServico(Base):
    __tablename__ = "agendamento_servico"

    id = Column(Integer, primary_key=True, index=True)
    agendamento_id = Column(Integer, ForeignKey("agendamentos.id"), nullable=False)
    servico_id = Column(Integer, ForeignKey("servicos.id"), nullable=False)