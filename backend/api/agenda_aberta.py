from backend.models.bloqueio import Bloqueio
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from datetime import date, datetime, timedelta, time
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.models.agendamento import Agendamento
from backend.models.profissional import Profissional
from backend.models.agenda_aberta import AgendaAberta

from backend.schemas.agenda_aberta import AgendaAbertaCreate, AgendaAbertaResponse

router = APIRouter(prefix="/agenda-aberta", tags=["Agenda Aberta"])


# A rota abrir_agenda permite que o usuário abra a agenda de um profissional para uma data específica
@router.post("", response_model=AgendaAbertaResponse)
def abrir_agenda(agenda: AgendaAbertaCreate, db: Session = Depends(get_db)):
    profissional = (
        db.query(Profissional).filter(Profissional.id == agenda.profissional_id).first()
    )

    if not profissional:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    agenda_existente = (
        db.query(AgendaAberta)
        .filter(AgendaAberta.profissional_id == agenda.profissional_id)
        .filter(AgendaAberta.data == agenda.data)
        .first()
    )

    if agenda_existente:
        raise HTTPException(status_code=409, detail="Agenda já aberta para essa data")

    nova_agenda = AgendaAberta(profissional_id=agenda.profissional_id, data=agenda.data)

    db.add(nova_agenda)

    db.commit()

    db.refresh(nova_agenda)

    return nova_agenda


# rota para listar as agendas abertas e horarios disponiveis de um profissional para uma data específica
@router.get("/horarios-disponiveis/{profissional_id}/{data}")
def horarios_disponiveis(
    profissional_id: int, data: date, db: Session = Depends(get_db)
):
    agenda_aberta = (
        db.query(AgendaAberta)
        .filter(AgendaAberta.profissional_id == profissional_id)
        .filter(AgendaAberta.data == data)
        .first()
    )

    if not agenda_aberta:
        raise HTTPException(status_code=404, detail="Agenda não aberta para esta data")
    # define os horários de abertura e fechamento do profissional
    ABERTURA = 9
    FECHAMENTO = 18
    inicio = datetime.combine(data, time(hour=ABERTURA))

    fim = datetime.combine(data, time(hour=FECHAMENTO))
    # cria uma lista de horários disponíveis em intervalos de 30 minutos
    slots = []

    horario = inicio

    while horario < fim:

        slots.append(horario)

        horario += timedelta(minutes=30)
    # Busca agendamentos somente ativos do profissional para a data especificada
    agendamentos = (
        db.query(Agendamento)
        .filter(Agendamento.profissional_id == profissional_id)
        .filter(Agendamento.status == "agendado")
        .filter(Agendamento.data_hora_inicio >= inicio)
        .filter(Agendamento.data_hora_fim < fim)
        .all()
    )
    # Buscar bloqueio de horarios ou horarios indisponivel
    bloqueios = (
        db.query(Bloqueio)
        .filter(Bloqueio.profissional_id == profissional_id)
        .filter(Bloqueio.data_hora_inicio >= inicio)
        .filter(Bloqueio.data_hora_fim < fim)
        .all()
    )

    # filtra os horários disponíveis removendo os horários já agendados e bloqueados

    horarios_disponiveis = []
    for slot in slots:
        ocupado = False
        for agendamento in agendamentos:

            if (
                slot >= agendamento.data_hora_inicio
                and slot < agendamento.data_hora_fim
            ):
                ocupado = True
                break
        if not ocupado:

            for bloqueio in bloqueios:

                if slot >= bloqueio.data_hora_inicio and slot < bloqueio.data_hora_fim:
                    ocupado = True
                    break
        if not ocupado:

            horarios_disponiveis.append(slot.strftime("%H:%M"))

    return {
        "profissional_id": profissional_id,
        "data": data,
        "horarios_disponiveis": horarios_disponiveis,
    }
