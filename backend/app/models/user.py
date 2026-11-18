from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SAEnum, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class TipoPerfil(str, Enum):
    NOVATO = "NOVATO"
    BUDDY = "BUDDY"
    TECH_LEAD = "TECH_LEAD"


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo_perfil: Mapped[TipoPerfil] = mapped_column(
        SAEnum(TipoPerfil, name="tipo_perfil_enum"),
        default=TipoPerfil.NOVATO,
        nullable=False,
    )
    cargo: Mapped[str | None] = mapped_column(String(100), nullable=True)
    data_cadastro: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    progressos = relationship("ProgressoTarefa", back_populates="usuario")
