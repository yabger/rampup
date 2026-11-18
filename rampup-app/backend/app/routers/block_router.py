# Gerencia o acionamento do alerta pelo novato e a ação de destravar pelo mentor
from datetime import datetime 
from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.orm import Session 
from app.database import get_db 
from app.models.task import ProgressoTarefa, StatusTarefa 
from app.models.block import Bloqueio, StatusBloqueio, VinculoMentoria 
from app.schemas.block_schema import BloqueioCreate, BloqueioResponse 

router = APIRouter(prefix="/api/v1/blocks", tags=["Gestão de Bloqueios ('Estou Travado')"])

@router.post("/stuck", response_model=BloqueioResponse, status_code=status.HTTP_201_CREATED) 
def acionar_botao_estou_travado(
    payload: BloqueioCreate, 
    db: Session = Depends(get_db)): 
    """ Acionado pelo novato ao encontrar um erro. 
    Altera o status da tarefa para 'TRAVADO' e envia o log de erro para a fila do mentor. """
    progresso = db.query(ProgressoTarefa).filter(ProgressoTarefa.id_progresso == payload.id_progresso).first() 
    if not progresso: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Progresso não encontrado."
        )
    
# 1. Altera o status da tarefa do novato para TRAVADO
    progresso.status = StatusTarefa.TRAVADO 

# 2. Busca o mentor vinculado a este novato
    vinculo = db.query(VinculoMentoria).filter(VinculoMentoria.id_novato == progresso.id_usuario).first() 
    id_mentor = vinculo.id_mentor if vinculo else None

# 3. Cria o registro de bloqueio com o log do erro
    novo_bloqueio = Bloqueio( 
        id_progresso=payload.id_progresso, 
        id_mentor=id_mentor, 
        log_erro=payload.log_erro, 
        status_bloqueio=StatusBloqueio.ATIVO )

    db.add(novo_bloqueio) 
    db.commit() 
    db.refresh(novo_bloqueio) 
    return novo_bloqueio

@router.put("/{id_bloqueio}/unblock", response_model=BloqueioResponse) 
def destravar_novato(id_bloqueio: int, db: Session = Depends(get_db)): 
    """ Acionado pelo Mentor (Buddy) para destravar o novato. 
    Marca o bloqueio como RESOLVIDO e altera a tarefa para CONCLUIDO. """ 
    bloqueio = db.query(Bloqueio).filter(Bloqueio.id_bloqueio == id_bloqueio).first() 
    if not bloqueio: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Bloqueio não encontrado."
        )

    # 1. Atualiza o status do bloqueio
    bloqueio.status_bloqueio = StatusBloqueio.RESOLVIDO
    bloqueio.data_resolucao = datetime.now()

    # 2. Atualiza a tarefa do novato para CONCLUIDO
    progresso = db.query(ProgressoTarefa).filter(ProgressoTarefa.id_progresso == bloqueio.id_progresso).first() 
    if progresso: 
        progresso.status = StatusTarefa.CONCLUIDA
        progresso.data_conclusao = datetime.now()
        db.commit()
        db.refresh(bloqueio)
    return bloqueio