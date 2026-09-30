from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.models.servico import Servico
from backend.schemas.servico import (
    ServicoCreate,
    ServicoResponse
)
# Cria um grupo de rotas relacionadas a serviços
# Todas as rotas começarão com /servicos
router = APIRouter(
    prefix="/servicos",
    tags=["Serviços"]
)

@router.post(
    "",
    response_model=ServicoResponse,
    status_code=201
)
def criar_servico(
    servico: ServicoCreate,
    db: Session = Depends(get_db)
):

    existente = (
        db.query(Servico)
        .filter(
            Servico.nome == servico.nome
        )
        .first()
    )

    if existente:
        raise HTTPException(
            status_code=409,
            detail="Serviço já cadastrado"
        )

    novo_servico = Servico(
        nome=servico.nome,
        duracao_minutos=servico.duracao_minutos,
        preco=servico.preco
    )

    db.add(novo_servico)

    db.commit()

    db.refresh(novo_servico)

    return novo_servico

@router.get(
    "",
    response_model=list[ServicoResponse]
)
def listar_servicos(
    db: Session = Depends(get_db)
):

    return db.query(Servico).all()