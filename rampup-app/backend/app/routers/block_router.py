# Gerencia o acionamento do alerta pelo novato e a ação de destravar pelo mentor
from datetime import datetime 
from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.orm import Session, joinedload
from app.database import get_db 
from app.models.task import ProgressoTarefa, StatusTarefa 
from app.models.block import Bloqueio, StatusBloqueio, VinculoMentoria 
from app.schemas.block_schema import BloqueioCreate, BloqueioResponse 

router = APIRouter(prefix="/api/v1/blocks", tags=["Gestão de Bloqueios ('Estou Travado')"])


@router.post(
    "/stuck",
    response_model=BloqueioResponse,
    status_code=status.HTTP_201_CREATED
)
def acionar_botao_estou_travado(
    payload: BloqueioCreate,
    db: Session = Depends(get_db)
):
    """Acionado pelo novato ao encontrar um erro."""

    # 1. Busca o progresso e carrega os relacionamentos necessários.
    progresso = (
        db.query(ProgressoTarefa)
        .options(
            joinedload(ProgressoTarefa.tarefa),
            joinedload(ProgressoTarefa.usuario)
        )
        .filter(ProgressoTarefa.id_progresso == payload.id_progresso)
        .first()
    )

    if not progresso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progresso não encontrado."
        )

    # 2. Impede o bloqueio de tarefas concluídas.
    if progresso.status == StatusTarefa.CONCLUIDO:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível bloquear uma tarefa concluída."
        )

    # 3. Impede a criação de bloqueios ativos duplicados.
    bloqueio_ativo = (
        db.query(Bloqueio)
        .filter(
            Bloqueio.id_progresso == progresso.id_progresso,
            Bloqueio.status_bloqueio == StatusBloqueio.ATIVO
        )
        .first()
    )

    if bloqueio_ativo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um bloqueio ativo para esta tarefa."
        )

    # 4. Busca o mentor vinculado ao novato.
    vinculo = (
        db.query(VinculoMentoria)
        .options(joinedload(VinculoMentoria.mentor))
        .filter(VinculoMentoria.id_novato == progresso.id_usuario)
        .first()
    )

    # 5. Atualiza o progresso e registra o bloqueio.
    try:
        progresso.status = StatusTarefa.BLOQUEADO

        novo_bloqueio = Bloqueio(
            id_progresso=progresso.id_progresso,
            id_mentor=vinculo.id_mentor if vinculo else None,
            log_erro=payload.log_erro,
            status_bloqueio=StatusBloqueio.ATIVO
        )

        db.add(novo_bloqueio)
        db.commit()
        db.refresh(novo_bloqueio)

        return novo_bloqueio

    except Exception:
        db.rollback()
        raise


@router.put(
    "/{id_bloqueio}/unblock",
    response_model=BloqueioResponse
)
def destravar_novato(
    id_bloqueio: int,
    db: Session = Depends(get_db)
):
    """Acionado pelo mentor para resolver o bloqueio do novato."""

    # 1. Busca o bloqueio e carrega seus relacionamentos.
    bloqueio = (
        db.query(Bloqueio)
        .options(
            joinedload(Bloqueio.progresso_tarefa).joinedload(
                ProgressoTarefa.tarefa
            ),
            joinedload(Bloqueio.progresso_tarefa).joinedload(
                ProgressoTarefa.usuario
            ),
            joinedload(Bloqueio.mentor)
        )
        .filter(Bloqueio.id_bloqueio == id_bloqueio)
        .first()
    )

    if not bloqueio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bloqueio não encontrado."
        )

    # 2. Impede a resolução duplicada.
    if bloqueio.status_bloqueio == StatusBloqueio.RESOLVIDO:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este bloqueio já foi resolvido."
        )

    # 3. Atualiza o bloqueio e o progresso relacionado.
    try:
        bloqueio.status_bloqueio = StatusBloqueio.RESOLVIDO
        bloqueio.data_resolucao = datetime.now()

        progresso = bloqueio.progresso_tarefa

        if progresso:
            progresso.status = StatusTarefa.PENDENTE
            progresso.data_conclusao = None

        db.commit()
        db.refresh(bloqueio)

        return bloqueio

    except Exception:
        db.rollback()
        raise
