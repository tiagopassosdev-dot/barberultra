from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from backend.database.base import Base

# Classe que representa a tabela "clientes" no banco de dados
class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String(100), nullable=False)

    telefone = Column(
        String(20),
        unique=True,
        nullable=False
    )