import enum
from logging import log 
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey 
from sqlalchemy.orm import relationship 
from sqlalchemy.sql import func 
from app.database import Base

# Enumeração para o estado do bloqueio
class StatusBloqueio(str, enum.Enum):
    ATIVO = "ATIVO"
    RESOLVIDO = "RESOLVIDO"

class Bloqueio(Base):
    """ Modelo ORM para a tabela 'bloqueios'. Registra os alertas disparados pelo botão 'Estou Travado', guardando o log de erro. """

    __tablename__ = "bloqueios"

    id_bloqueio = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_progresso = Column(Integer, ForeignKey("progresso_tarefas.id_progresso"), nullable=False)
    id_mentor = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True) # Buddy responsável
    log_erro = Column(Text, nullable=False) # Linha de erro/stacktrace colada pelo novato
    status_bloqueio = Column(
        Enum(StatusBloqueio, name="status_bloqueio_enum"),
        nullable=False,
        default=StatusBloqueio.ATIVO
    )
    data_bloqueio = Column(DateTime(timezone=True), server_default=func.now(), nullable=False) 
    data_resolucao = Column(DateTime(timezone=True), nullable=True)

    # Relacionamento
    progresso_tarefa = relationship("ProgressoTarefa", back_populates="bloqueios") 
    mentor = relationship("Usuario", foreign_keys=[id_mentor])

    def __repr__(self):
        return f"<Bloqueio(id={self.id_bloqueio}, status='{self.status_bloqueio}')>"

class VinculoMentoria(Base):
    """Modelo ORM para o vínculo entre um novato e seu mentor."""

    __tablename__ = "vinculo_mentoria"

    id_vinculo = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_novato = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_mentor = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    data_inicio = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    novato = relationship("Usuario", foreign_keys=[id_novato])
    mentor = relationship("Usuario", foreign_keys=[id_mentor])

    def __repr__(self):
        return f"<VinculoMentoria(novato_id={self.id_vinculo}, mentor_id={self.id_mentor})>"


class DocumentacaoObsoleta(Base):
    """Modelo ORM para registros de documentação desatualizada."""

    __tablename__ = "documentacoes_obsoletas"

    id_report = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_tarefa = Column(Integer, ForeignKey("tarefas.id_tarefa"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    trecho_desatualizado = Column(Text, nullable=False)
    sugestao_correcao = Column(Text, nullable=True)
    data_registro = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    tarefa = relationship("Tarefa")
    usuario = relationship("Usuario")

    def __repr__(self):
        return f"<DocumentacaoObsoleta(id={self.id_report}, tarefa_id={self.id_tarefa})>"