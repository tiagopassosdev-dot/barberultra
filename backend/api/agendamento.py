from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.models.agendamento import Agendamento
from backend.models.agendamento_servico import AgendamentoServico
from backend.models.cliente import Cliente
from backend.models.servico import Servico

from backend.schemas.agendamento import (
    AgendamentoCreate, AgendamentoResponse)

router = APIRouter(
    prefix="/agendamentos", tags=["Agendamentos"])


@router.post("", response_model=AgendamentoResponse, status_code=201)
def criar_agendamento(agendamento: AgendamentoCreate, db: Session = Depends(get_db)):
    # Verifica se o cliente existe
    cliente = db.query(Cliente).filter(
        Cliente.id == agendamento.cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=404, detail="Cliente não encontrado")

    #buscar serviços
    servicos = ( db.query(Servico).filter(Servico.id.in_(agendamento.servicos)).all() )
    if not servicos:
        raise HTTPException(
            status_code=404, detail="Serviço(s) não encontrado(s)")
    # Calcula a duração total dos serviços selecionados
    duracao_total = sum(servico.duracao_minutos for servico in servicos)
    # Calcula a data e hora de término do agendamento com base na duração total dos serviços
    data_hora_fim = (agendamento.data_hora_inicio + timedelta(minutes=duracao_total))

    # Cria o agendamento
    novo_agendamento = Agendamento(
        cliente_id=agendamento.cliente_id,
        data_hora_inicio=agendamento.data_hora_inicio,
        data_hora_fim=data_hora_fim,
        status="agendado"
    )
    db.add(novo_agendamento)
    db.commit()
    db.refresh(novo_agendamento)
    for servico in servicos:
        agendamento_servico = AgendamentoServico(
            agendamento_id=novo_agendamento.id, servico_id=servico.id)
        db.add(agendamento_servico)
    db.commit()
    return novo_agendamento

