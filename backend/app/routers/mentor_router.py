from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.dependencies import require_roles
from app.models.block import Bloqueio, StatusBloqueio
from app.models.task import ProgressoTarefa
from app.models.user import Usuario, TipoPerfil
from app.schemas.block_schema import BloqueioResponse

router = APIRouter(prefix="/api/v1/mentor", tags=["Painel do Mentor / Buddy"])


@router.get("/dashboard/{mentor_id}", response_model=list[BloqueioResponse])
def dashboard_mentor(
    mentor_id: int,
    db: Session = Depends(get_db),
    user: Usuario = Depends(require_roles(TipoPerfil.BUDDY, TipoPerfil.TECH_LEAD)),
):
    if user.tipo_perfil == TipoPerfil.BUDDY and user.id_usuario != mentor_id:
        raise HTTPException(status_code=403, detail="Você só pode consultar seu próprio painel.")
    query = (
        db.query(Bloqueio)
        .options(
            joinedload(Bloqueio.progresso_tarefa).joinedload(ProgressoTarefa.tarefa),
            joinedload(Bloqueio.progresso_tarefa).joinedload(ProgressoTarefa.usuario),
            joinedload(Bloqueio.mentor),
        )
        .filter(Bloqueio.status_bloqueio == StatusBloqueio.ATIVO)
    )
    if user.tipo_perfil == TipoPerfil.BUDDY:
        query = query.filter(Bloqueio.id_mentor == mentor_id)
    else:
        query = query.filter(Bloqueio.id_mentor == mentor_id)
    return query.order_by(Bloqueio.data_bloqueio.desc()).all()
