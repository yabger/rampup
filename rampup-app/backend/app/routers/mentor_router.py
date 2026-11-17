# Gerencia o dashboard exclusivo do mentor (Buddy)
from typing import List 
from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session 
from app.database import get_db 
from app.models.block import Bloqueio, StatusBloqueio 
from app.schemas.block_schema import BloqueioResponse 

router = APIRouter(prefix="/api/v1/mentor", tags=["Painel do Mentor (Buddy)"])

@router.get("/dashboard/{id_mentor}", response_model=List[BloqueioResponse]) 
def obter_bloqueios_do_mentor(id_mentor: int, db: Session = Depends(get_db)): 
    """ Retorna todos os alertas ativos ('Estou Travado') direcionados a um mentor específico. """ 
    bloqueios_ativos = db.query(Bloqueio).filter( 
        Bloqueio.id_mentor == id_mentor, 
        Bloqueio.status_bloqueio == StatusBloqueio.ATIVO 
    ).all() 
    return bloqueios_ativos