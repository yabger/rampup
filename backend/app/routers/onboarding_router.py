from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.dependencies import get_current_user
from app.models.task import ProgressoTarefa, StatusTarefa
from app.models.user import Usuario, TipoPerfil
from app.schemas.task_schema import ProgressoTarefaResponse, ProgressoTarefaUpdate, ProgressoResumo
from app.services.onboarding_service import listar_trilha, resumo_progresso

router = APIRouter(prefix="/api/v1/onboarding", tags=["Trilhas & Onboarding"])


def _check_owner_or_manager(target_user_id: int, current_user: Usuario):
    if current_user.tipo_perfil == TipoPerfil.NOVATO and current_user.id_usuario != target_user_id:
        raise HTTPException(status_code=403, detail="Você só pode consultar sua própria trilha.")


@router.get("/trilha/{usuario_id}", response_model=list[ProgressoTarefaResponse])
def obter_trilha(usuario_id: int, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    _check_owner_or_manager(usuario_id, user)
    progressos = listar_trilha(db, usuario_id)
    if not progressos:
        raise HTTPException(status_code=404, detail="Nenhuma trilha de onboarding encontrada para este usuário.")
    return progressos


@router.get("/trilha/{usuario_id}/resumo", response_model=ProgressoResumo)
def obter_resumo(usuario_id: int, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    _check_owner_or_manager(usuario_id, user)
    return resumo_progresso(db, usuario_id)


@router.put("/tasks/{progresso_id}/status", response_model=ProgressoTarefaResponse)
def atualizar_status(
    progresso_id: int,
    payload: ProgressoTarefaUpdate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
):
    progress = db.query(ProgressoTarefa).options(joinedload(ProgressoTarefa.tarefa)).filter(
        ProgressoTarefa.id_progresso == progresso_id
    ).first()
    if progress is None:
        raise HTTPException(status_code=404, detail="Registro de progresso não encontrado.")
    _check_owner_or_manager(progress.id_usuario, user)
    if user.tipo_perfil == TipoPerfil.NOVATO and payload.status == StatusTarefa.TRAVADO:
        raise HTTPException(status_code=400, detail="Use o endpoint /api/v1/blocks/stuck para sinalizar um bloqueio.")
    progress.status = payload.status
    progress.data_conclusao = datetime.now(timezone.utc) if payload.status == StatusTarefa.CONCLUIDO else None
    db.commit()
    db.refresh(progress)
    return progress
