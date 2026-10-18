from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from backend.database.connection import get_db

from backend.models.profissional import Profissional
from backend.models.bloqueio import Bloqueio

from backend.schemas.bloqueio import BloqueioCreate, BloqueioResponse

router = APIRouter(prefix="/bloqueios", tags=["Bloqueios"])


@router.post("", response_model=BloqueioResponse)
def criar_bloqueio(bloqueio: BloqueioCreate, db: Session = Depends(get_db)):
    if bloqueio.data_hora_fim <= bloqueio.data_hora_inicio:
        raise HTTPException(
            status_code=400, detail="Horário final deve ser maior que inicial"
        )
    novo_bloqueio = Bloqueio(
        profissional_id=bloqueio.profissional_id,
        data_hora_inicio=bloqueio.data_hora_inicio,
        data_hora_fim=bloqueio.data_hora_fim,
        motivo=bloqueio.motivo,
    )

    db.add(novo_bloqueio)

    db.commit()

    db.refresh(novo_bloqueio)

    return novo_bloqueio
