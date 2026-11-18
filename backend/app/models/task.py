from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PeriodoOnboarding(str, Enum):
    DIA_1 = "DIA 1"
    DIA_2 = "DIA 2"
    SEMANA_1 = "SEMANA 1"
    SEMANA_2 = "SEMANA 2"
    MES_1 = "MÊS 1"


class StatusTarefa(str, Enum):
    PENDENTE = "PENDENTE"
    CONCLUIDO = "CONCLUIDO"
    TRAVADO = "TRAVADO"


class Trilha(Base):
    __tablename__ = "trilhas"

    id_trilha: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo_trilha: Mapped[str] = mapped_column(String(120), nullable=False)
    cargo_destino: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text)
    tarefas = relationship(
        "Tarefa", back_populates="trilha", cascade="all, delete-orphan",
        order_by="Tarefa.ordem",
    )


class Tarefa(Base):
    __tablename__ = "tarefas"

    id_tarefa: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_trilha: Mapped[int] = mapped_column(ForeignKey("trilhas.id_trilha"), nullable=False)
    titulo: Mapped[str] = mapped_column(String(180), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text)
    periodo: Mapped[PeriodoOnboarding] = mapped_column(
        SAEnum(PeriodoOnboarding, name="periodo_onboarding_enum"), nullable=False
    )
    tempo_estimado_min: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    link_tutorial: Mapped[str | None] = mapped_column(String(500))
    ordem: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    trilha = relationship("Trilha", back_populates="tarefas")
    progressos = relationship("ProgressoTarefa", back_populates="tarefa")


class ProgressoTarefa(Base):
    __tablename__ = "progresso_tarefas"

    id_progresso: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"), nullable=False)
    id_tarefa: Mapped[int] = mapped_column(ForeignKey("tarefas.id_tarefa"), nullable=False)
    status: Mapped[StatusTarefa] = mapped_column(
        SAEnum(StatusTarefa, name="status_tarefa_enum"),
        default=StatusTarefa.PENDENTE,
        nullable=False,
    )
    data_inicio: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    data_conclusao: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    usuario = relationship("Usuario", back_populates="progressos")
    tarefa = relationship("Tarefa", back_populates="progressos")
    bloqueios = relationship("Bloqueio", back_populates="progresso_tarefa")
