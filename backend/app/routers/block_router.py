from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.dependencies import require_roles
from app.models.block import Bloqueio, StatusBloqueio, VinculoMentoria
from app.models.task import ProgressoTarefa, StatusTarefa
from app.models.user import Usuario, TipoPerfil
from app.schemas.block_schema import BloqueioCreate, BloqueioResponse

router = APIRouter(prefix="/api/v1/blocks", tags=["Gestão de Bloqueios"])


@router.post("/stuck", response_model=BloqueioResponse, status_code=status.HTTP_201_CREATED)
def registrar_bloqueio(
    payload: BloqueioCreate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(require_roles(TipoPerfil.NOVATO)),
):
    progress = db.query(ProgressoTarefa).filter(
        ProgressoTarefa.id_progresso == payload.id_progresso
    ).first()
    if progress is None:
        raise HTTPException(status_code=404, detail="Progresso não encontrado.")
    if progress.id_usuario != user.id_usuario:
        raise HTTPException(status_code=403, detail="Você só pode bloquear uma tarefa da sua própria trilha.")
    if progress.status == StatusTarefa.CONCLUIDO:
        raise HTTPException(status_code=409, detail="Uma tarefa concluída não pode ser bloqueada.")
    active_block = db.query(Bloqueio).filter(
        Bloqueio.id_progresso == progress.id_progresso,
        Bloqueio.status_bloqueio == StatusBloqueio.ATIVO,
    ).first()
    if active_block:
        raise HTTPException(status_code=409, detail="Esta tarefa já possui um bloqueio ativo.")

    link = db.query(VinculoMentoria).filter(
        VinculoMentoria.id_novato == user.id_usuario
    ).first()
    progress.status = StatusTarefa.TRAVADO
    block = Bloqueio(
        id_progresso=progress.id_progresso,
        id_mentor=link.id_mentor if link else None,
        log_erro=payload.log_erro.strip(),
        status_bloqueio=StatusBloqueio.ATIVO,
    )
    db.add(block)
    db.commit()
    return (
        db.query(Bloqueio)
        .options(
            joinedload(Bloqueio.progresso_tarefa).joinedload(ProgressoTarefa.tarefa),
            joinedload(Bloqueio.progresso_tarefa).joinedload(ProgressoTarefa.usuario),
            joinedload(Bloqueio.mentor),
        )
        .filter(Bloqueio.id_bloqueio == block.id_bloqueio)
        .first()
    )


@router.put("/{bloqueio_id}/unblock", response_model=BloqueioResponse)
def resolver_bloqueio(
    bloqueio_id: int,
    db: Session = Depends(get_db),
    user: Usuario = Depends(require_roles(TipoPerfil.BUDDY, TipoPerfil.TECH_LEAD)),
):
    block = (
        db.query(Bloqueio)
        .options(joinedload(Bloqueio.progresso_tarefa))
        .filter(Bloqueio.id_bloqueio == bloqueio_id)
        .first()
    )
    if block is None:
        raise HTTPException(status_code=404, detail="Bloqueio não encontrado.")
    if block.id_mentor is not None and block.id_mentor != user.id_usuario and user.tipo_perfil != TipoPerfil.TECH_LEAD:
        raise HTTPException(status_code=403, detail="Este bloqueio está atribuído a outro Buddy.")
    if block.status_bloqueio == StatusBloqueio.RESOLVIDO:
        raise HTTPException(status_code=409, detail="Este bloqueio já foi resolvido.")

    now = datetime.now(timezone.utc)
    block.status_bloqueio = StatusBloqueio.RESOLVIDO
    block.data_resolucao = now
    if block.progresso_tarefa:
        block.progresso_tarefa.status = StatusTarefa.CONCLUIDO
        block.progresso_tarefa.data_conclusao = now
    db.commit()
    return (
        db.query(Bloqueio)
        .options(
            joinedload(Bloqueio.progresso_tarefa).joinedload(ProgressoTarefa.tarefa),
            joinedload(Bloqueio.progresso_tarefa).joinedload(ProgressoTarefa.usuario),
            joinedload(Bloqueio.mentor),
        )
        .filter(Bloqueio.id_bloqueio == bloqueio_id)
        .first()
    )
