from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from backend.database.connection import get_db

from backend.models.profissional import Profissional

from backend.schemas.profissional import ProfissionalCreate, ProfissionalResponse

# Cria um grupo de rotas relacionadas a profissionais
router = APIRouter(prefix="/profissionais", tags=["Profissionais"])


# A rota criar_profissional permite que o usuário cadastre um novo profissional no banco de dados
@router.post("", response_model=ProfissionalResponse, status_code=201)
def criar_profissional(profissional: ProfissionalCreate, db: Session = Depends(get_db)):

    existe = (
        db.query(Profissional).filter(Profissional.nome == profissional.nome).first()
    )

    if existe:
        raise HTTPException(status_code=409, detail="Profissional já cadastrado")

    novo_profissional = Profissional(nome=profissional.nome)

    db.add(novo_profissional)

    db.commit()

    db.refresh(novo_profissional)

    return novo_profissional


@router.get("", response_model=list[ProfissionalResponse])
def listar_profissionais(db: Session = Depends(get_db)):

    return db.query(Profissional).filter(Profissional.ativo == True).all()
