# Importa os recursos do FastAPI para criar rotas
# e injetar dependências
from fastapi import APIRouter
from fastapi import Depends
# Importa a Session do SQLAlchemy,
# usada para acessar o banco de dados
from sqlalchemy.orm import Session

# Função que cria e fecha a conexão com o banco
from backend.database.connection import get_db

# Model (tabela) Cliente do SQLAlchemy
from backend.models.cliente import Cliente

# Schemas do Pydantic
from backend.schemas.cliente import (
    ClienteCreate,
    ClienteResponse
)
from fastapi import HTTPException

# Cria um grupo de rotas relacionadas a clientes
# Todas as rotas começarão com /clientes
router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)

@router.post(
    "",
    response_model=ClienteResponse,  # resposta segue esse schema
    status_code=201                  # HTTP 201 = criado com sucesso
)
def criar_cliente(
    # Dados enviados pelo usuário no body da requisição
    cliente: ClienteCreate,

    # FastAPI injeta automaticamente a conexão com o banco
    db: Session = Depends(get_db)
):
    # Verifica se já existe um cliente com o mesmo telefone
    cliente_existente = db.query(Cliente).filter(
        Cliente.telefone == cliente.telefone
    ).first()

    if cliente_existente:
        raise HTTPException(
            status_code=400,
            detail="Telefone já cadastrado"
        )

    # Cria um objeto Cliente usando os dados recebidos
    novo_cliente = Cliente(
        nome=cliente.nome,
        telefone=cliente.telefone
    )

    # Adiciona o objeto à sessão
    db.add(novo_cliente)

    # Salva no banco de dados
    db.commit()

    # Atualiza o objeto com os dados gerados pelo banco
    # (id, timestamps, etc.)
    db.refresh(novo_cliente)

    # Retorna o cliente criado
    return novo_cliente

@router.get(
    "",
    response_model=list[ClienteResponse]
)
def listar_clientes(

    # Conexão com o banco fornecida pelo FastAPI
    db: Session = Depends(get_db)
):

    # Busca todos os registros da tabela clientes
    clientes = db.query(Cliente).all()

    # Retorna a lista de clientes
    return clientes

@router.get(
    "/{cliente_id}",
    response_model=ClienteResponse
)
# busca um cliente pelo ID fornecido na URL
def buscar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):

    cliente = (
        db.query(Cliente)
        .filter(Cliente.id == cliente_id)
        .first()
    )

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )

    return cliente

# rota para buscar um cliente pelo telefone
@router.get("/telefone/{telefone}")
def buscar_por_telefone(
    telefone: str,
    db: Session = Depends(get_db)
):
    cliente = (
        db.query(Cliente)
        .filter(Cliente.telefone == telefone)
        .first()
    )

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )

    return cliente