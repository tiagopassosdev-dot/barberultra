from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String

from backend.database.base import Base

# Classe que representa a tabela "servicos" no banco de dados
class Servico(Base):
    __tablename__ = "servicos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(
        String(100),
        nullable=False,
        unique=True
    )

    duracao_minutos = Column(
        Integer,
        nullable=False
    )

    preco = Column(
        Numeric(10, 2),
        nullable=False
    )
# Campo que indica se o serviço está ativo ou não
    ativo = Column(
        Boolean,
        nullable=False,
        default=True
    )