from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload

from app.models.task import ProgressoTarefa, StatusTarefa


def listar_trilha(db: Session, usuario_id: int) -> list[ProgressoTarefa]:
    statement = (
        select(ProgressoTarefa)
        .options(joinedload(ProgressoTarefa.tarefa))
        .where(ProgressoTarefa.id_usuario == usuario_id)
        .order_by(ProgressoTarefa.id_progresso)
    )
    return list(db.scalars(statement).unique().all())


def resumo_progresso(db: Session, usuario_id: int) -> dict:
    rows = db.query(ProgressoTarefa.status).filter(
        ProgressoTarefa.id_usuario == usuario_id
    ).all()
    total = len(rows)
    completed = sum(status == StatusTarefa.CONCLUIDO for (status,) in rows)
    blocked = sum(status == StatusTarefa.TRAVADO for (status,) in rows)
    return {
        "total_tarefas": total,
        "concluidas": completed,
        "travadas": blocked,
        "percentual_conclusao": round(completed * 100 / total) if total else 0,
    }
