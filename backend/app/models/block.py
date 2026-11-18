from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class StatusBloqueio(str, Enum):
    ATIVO = "ATIVO"
    RESOLVIDO = "RESOLVIDO"


class VinculoMentoria(Base):
    __tablename__ = "vinculos_mentoria"

    id_vinculo: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_novato: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"), nullable=False)
    id_mentor: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"), nullable=False)
    data_inicio: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    novato = relationship("Usuario", foreign_keys=[id_novato])
    mentor = relationship("Usuario", foreign_keys=[id_mentor])


class Bloqueio(Base):
    __tablename__ = "bloqueios"

    id_bloqueio: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_progresso: Mapped[int] = mapped_column(
        ForeignKey("progresso_tarefas.id_progresso"), nullable=False
    )
    id_mentor: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id_usuario"), nullable=True
    )
    log_erro: Mapped[str] = mapped_column(Text, nullable=False)
    status_bloqueio: Mapped[StatusBloqueio] = mapped_column(
        SAEnum(StatusBloqueio, name="status_bloqueio_enum"),
        default=StatusBloqueio.ATIVO,
        nullable=False,
    )
    data_bloqueio: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    data_resolucao: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    progresso_tarefa = relationship("ProgressoTarefa", back_populates="bloqueios")
    mentor = relationship("Usuario", foreign_keys=[id_mentor])
