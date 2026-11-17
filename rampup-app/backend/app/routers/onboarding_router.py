# Gerencia o carregamento da trilha de onboarding do novato e a atualização do status das atividades
from typing import List 
from datetime import datetime 
from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.orm import Session 
from app.database import get_db 
from app.models.task import Trilha, Tarefa, ProgressoTarefa, StatusTarefa 
from app.schemas.task_schema import TrilhaResponse, ProgressoTarefaResponse, ProgressoTarefaUpdate 

router = APIRouter(prefix="/api/v1/onboarding", tags=["Trilhas & Onboarding"])

@router.get("/trilha/{id\_usuario}", response_model=List[ProgressoTarefaResponse]) 
def obter_trilha_do_novato(id_usuario: int, db: Session = Depends(get_db)): 
    """ Retorna todas as tarefas atribuídas ao novato e seus respectivos status 
    (PENDENTE, CONCLUIDO, TRAVADO). """
    progressos = db.query(ProgressoTarefa).filter(ProgressoTarefa.id_usuario == id_usuario).all() 
    if not progressos: 
        raise HTTPException( 
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Nenhuma trilha de onboarding encontrada para este usuário." 
        ) 
    return progressos

@router.put("/tasks/{id\_progresso}/status", response_model=ProgressoTarefaResponse) 
def atualizar_status_tarefa( id_progresso: int, status_update: ProgressoTarefaUpdate, db: Session = Depends(get_db) ): 
    """ Atualiza o status de uma tarefa no checklist do novato. """
    progresso = db.query(ProgressoTarefa).filter(ProgressoTarefa.id_progresso == id_progresso).first() 
    if not progresso: 
        raise HTTPException( 
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Registro de progresso não encontrado." 
        ) 
    if status_update.status == StatusTarefa.CONCLUIDA: 
        progresso.data_conclusao = datetime.now() 
    progresso.status = status_update.status 
    db.commit() 
    db.refresh(progresso) 
    return progresso