from datetime import timedelta, datetime, date, time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.models.agendamento import Agendamento
from backend.models.agendamento_servico import AgendamentoServico
from backend.models.cliente import Cliente
from backend.models.servico import Servico
from backend.models.profissional import Profissional

from backend.schemas.agendamento import AgendamentoCreate, AgendamentoResponse

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])


@router.post("", response_model=AgendamentoResponse, status_code=201)
def criar_agendamento(agendamento: AgendamentoCreate, db: Session = Depends(get_db)):

    # validar profissional
    profissional = (
        db.query(Profissional)
        .filter(Profissional.id == agendamento.profissional_id)
        .first()
    )
    if not profissional:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    # Verifica se o cliente existe
    cliente = db.query(Cliente).filter(Cliente.id == agendamento.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    # verifica se o usuario selecionou algum serviço
    if len(agendamento.servicos) == 0:
        raise HTTPException(status_code=400, detail="Nenhum serviço selecionado")

    # buscar serviços
    servicos = db.query(Servico).filter(Servico.id.in_(agendamento.servicos)).all()
    # verifica se todos os serviços selecionados existem
    if len(servicos) != len(agendamento.servicos):
        raise HTTPException(
            status_code=404, detail="Um ou mais serviços não encontrados"
        )
    if not servicos:
        raise HTTPException(status_code=404, detail="Serviço(s) não encontrado(s)")
    # Variavel que define a duração de cada serviço em minutos
    SLOT_MINUTOS = 30
    # Calcula a duração total dos serviços selecionados
    duracao_total = len(servicos) * SLOT_MINUTOS
    # Calcula a data e hora de término do agendamento com base na duração total dos serviços
    data_hora_fim = agendamento.data_hora_inicio + timedelta(minutes=duracao_total)

    # Verifica se o profissional já possui um agendamento nesse horário
    conflito = (
        db.query(Agendamento)
        .filter(
            Agendamento.profissional_id == agendamento.profissional_id,
            Agendamento.data_hora_inicio < data_hora_fim,
            Agendamento.data_hora_fim > agendamento.data_hora_inicio,
        )
        .first()
    )
    if conflito:
        raise HTTPException(
            status_code=409,
            detail="O profissional já possui um agendamento nesse horário",
        )

    # Cria o agendamento
    novo_agendamento = Agendamento(
        cliente_id=agendamento.cliente_id,
        profissional_id=agendamento.profissional_id,
        data_hora_inicio=agendamento.data_hora_inicio,
        data_hora_fim=data_hora_fim,
        status="agendado",
    )
    db.add(novo_agendamento)
    db.commit()
    db.refresh(novo_agendamento)
    for servico in servicos:
        agendamento_servico = AgendamentoServico(
            agendamento_id=novo_agendamento.id, servico_id=servico.id
        )
        db.add(agendamento_servico)
    db.commit()
    return {
        "id": novo_agendamento.id,
        "cliente_id": novo_agendamento.cliente_id,
        "profissional_id": novo_agendamento.profissional_id,
        "servicos": [servico.id for servico in servicos],
        "data_hora_inicio": novo_agendamento.data_hora_inicio,
        "data_hora_fim": novo_agendamento.data_hora_fim,
        "status": novo_agendamento.status,
    }


# Rota para lista agendamentos de um profissional específico
@router.get("/profissional/{profissional_id}")
def agenda_profissional(profissional_id: int, db: Session = Depends(get_db)):
    # Verifica se o profissional existe
    profissional = (
        db.query(Profissional).filter(Profissional.id == profissional_id).first()
    )
    if not profissional:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")

    agendamentos = (
        db.query(Agendamento)
        .filter(Agendamento.profissional_id == profissional_id)
        .all()
    )
    resultado = []
    # Itera sobre os agendamentos encontrados para o profissional
    for agendamento in agendamentos:

        cliente = db.query(Cliente).filter(Cliente.id == agendamento.cliente_id).first()

        servicos_relacao = (
            db.query(AgendamentoServico)
            .filter(AgendamentoServico.agendamento_id == agendamento.id)
            .all()
        )

        servicos = []
        for item in servicos_relacao:
            servico = db.query(Servico).filter(Servico.id == item.servico_id).first()
            if servico:
                servicos.append(servico.nome)
        profissional = (
            db.query(Profissional)
            .filter(Profissional.id == agendamento.profissional_id)
            .first()
        )
        # Monta o resultado final com as informações do agendamento, cliente, profissional e serviços
        resultado.append(
            {
                "id": agendamento.id,
                "profissional": profissional.nome,
                "horario": agendamento.data_hora_inicio,
                "cliente": cliente.nome,
                "telefone": cliente.telefone,
                "servicos": servicos,
                "status": agendamento.status,
            }
        )

    return resultado


@router.get("/profissional/{profissional_id}/dia/{data}")
def agenda_profissional_dia(
    profissional_id: int, data: date, db: Session = Depends(get_db)
):
    inicio_dia = datetime.combine(data, time.min)
    fim_dia = datetime.combine(data, time.max)
    agendamentos = (
        db.query(Agendamento)
        .filter(
            Agendamento.profissional_id == profissional_id,
            Agendamento.data_hora_inicio >= inicio_dia,
            Agendamento.data_hora_inicio <= fim_dia,
        )
        .order_by(Agendamento.data_hora_inicio)
        .all()
    )

    resultado = []

    for agendamento in agendamentos:

        cliente = db.query(Cliente).filter(Cliente.id == agendamento.cliente_id).first()

        profissional = (
            db.query(Profissional)
            .filter(Profissional.id == agendamento.profissional_id)
            .first()
        )

        servicos_relacao = (
            db.query(AgendamentoServico)
            .filter(AgendamentoServico.agendamento_id == agendamento.id)
            .all()
        )

        servicos = []

        for item in servicos_relacao:

            servico = db.query(Servico).filter(Servico.id == item.servico_id).first()

            servicos.append(servico.nome)

        resultado.append(
            {
                "id": agendamento.id,
                "profissional": profissional.nome,
                "horario": agendamento.data_hora_inicio,
                "cliente": cliente.nome,
                "telefone": cliente.telefone,
                "servicos": servicos,
                "status": agendamento.status,
            }
        )

    return resultado
