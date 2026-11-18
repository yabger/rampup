from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_roles
from app.models.user import Usuario, TipoPerfil
from app.models.task import ProgressoTarefa
from app.models.block import Bloqueio, StatusBloqueio
from sqlalchemy import func

router = APIRouter(prefix="/api/v1/metrics", tags=["Métricas"])


@router.get("/overview")
def obter_indicadores(
    db: Session = Depends(get_db),
    user: Usuario = Depends(require_roles(TipoPerfil.BUDDY, TipoPerfil.TECH_LEAD)),
):
    total_progress = db.query(func.count(ProgressoTarefa.id_progresso)).scalar() or 0
    completed = db.query(func.count(ProgressoTarefa.id_progresso)).filter(
        ProgressoTarefa.status == "CONCLUIDO"
    ).scalar() or 0
    active_blocks = db.query(func.count(Bloqueio.id_bloqueio)).filter(
        Bloqueio.status_bloqueio == StatusBloqueio.ATIVO
    ).scalar() or 0
    return {
        "total_tarefas_atribuidas": total_progress,
        "tarefas_concluidas": completed,
        "percentual_conclusao": round(completed * 100 / total_progress) if total_progress else 0,
        "bloqueios_ativos": active_blocks,
    }
