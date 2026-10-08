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
# A rota criar_servico permite que o usuário cadastre um novo serviço no banco de dados
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

# listar_servicos retorna todos os serviços cadastrados no banco de dados
@router.get(
    "",
    response_model=list[ServicoResponse]
)
def listar_servicos(
    db: Session = Depends(get_db)
):

    return db.query(Servico).all()
# buscar_servico retorna um serviço específico pelo seu ID
@router.get(
    "/{servico_id}",
    response_model=ServicoResponse
)
def buscar_servico(
    servico_id: int,
    db: Session = Depends(get_db)
):

    servico = (
        db.query(Servico)
        .filter(Servico.id == servico_id)
        .first()
    )

    if not servico:
        raise HTTPException(
            status_code=404,
            detail="Serviço não encontrado"
        )

    return servico