import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# Enumeração para os períodos do Onboarding
class PeriodoOnboarding(str, enum.Enum):
    DIA_1 = "DIA_1"
    DIA_2 = "DIA_2"
    SEMANA_1 = "SEMANA_1"
    SEMANA_2 = "SEMANA_2"
    MES_1 = "MES_1"

# Enumeração para o status da tarefa no onboarding do novato
class StatusTarefa(str, enum.Enum):
    PENDENTE = "PENDENTE"
    CONCLUIDO = "CONCLUIDO"
    BLOQUEADO = "BLOQUEADO"
    ATRASADA = "ATRASADA"

class Trilha(Base):

    """ Modelo ORM para a tabela 'trilhas'. Agrupa o conjunto de checklists por cargo técnico (ex: Dev Júnior, Engenharia de Dados). """

    __tablename__ = "trilhas"

    id_trilha = Column(Integer, primary_key=True, index=True, autoincrement=True)
    titulo_trilha = Column(String(100), nullable=False)
    cargo_destino = Column(String(50), nullable=False)
    descricao = Column(Text, nullable=True)

    # Relacionamento com Tarefas

    tarefas = relationship("Tarefa", back_populates="trilha", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Trilha(id={self.id_trilha}, titulo='{self.titulo_trilha}', cargo='{self.cargo_destino}')>"

class Tarefa(Base):

    """ Modelo ORM para a tabela 'tarefas'. Representa uma tarefa específica dentro de uma trilha de onboarding.
     Passos individuais de configuração técnica (ex: 'Instalar Docker', 'Clonar Repositório'). """

    __tablename__ = "tarefas"

    id_tarefa = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_trilha = Column(Integer, ForeignKey("trilhas.id_trilha"), nullable=False)
    titulo = Column(String(150), nullable=False)
    descricao = Column(Text, nullable=True)
    periodo = Column( 
        Enum(PeriodoOnboarding, name="periodo_onboarding_enum"), 
        nullable=False, 
        default=PeriodoOnboarding.DIA_1 
    )

    tempo_estimado_min = Column(Integer, nullable=True, default=30)
    link_tutorial = Column(String(255), nullable=True)
    ordem = Column(Integer, nullable=False, default=1)

    # Relacionamento com Trilha e Progresso
    trilha = relationship("Trilha", back_populates="tarefas")
    progressos = relationship("ProgressoTarefa", back_populates="tarefa", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Tarefa(id={self.id_tarefa}, titulo='{self.titulo}', periodo='{self.periodo}')>"

class ProgressoTarefa(Base):

    """ Modelo ORM para a tabela 'progresso_tarefas'. Representa o progresso de um novato em relação a uma tarefa específica.
    Registra a execução individual de cada tarefa para um novato específico"""

    __tablename__ = "progresso_tarefas"

    id_progresso = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_tarefa = Column(Integer, ForeignKey("tarefas.id_tarefa"), nullable=False)
    status = Column(
        Enum(StatusTarefa, name="status_tarefa_enum"),
        nullable=False,
        default=StatusTarefa.PENDENTE
    )
    data_inicio = Column(DateTime(timezone=True), server_default=func.now())
    data_conclusao = Column(DateTime(timezone=True), nullable=True)

    # Relacionamento com Tarefa
    usuario = relationship("Usuario")
    tarefa = relationship("Tarefa", back_populates="progressos")
    bloqueios = relationship("Bloqueio", back_populates="progresso_tarefa", cascade="all, delete-orphan")


    def __repr__(self):
        return f"<ProgressoTarefa(id={self.id_progresso}, usuario={self.id_usuario}, status='{self.status}')>"
