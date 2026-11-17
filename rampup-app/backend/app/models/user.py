import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum 
from sqlalchemy.sql import func 
from app.database import Base

# Enumeração para os perfis de acesso do RampUp
class TipoPerfil(str, enum.Enum):
    NOVATO = "NOVATO"
    BUDDY = "BUDDY"
    TECH_LEAD = "TECH_LEAD"

class Usuario(Base):
    """ Modelo ORM para a tabela 'usuários'.
    Mapeia credenciais, dados cadastrais e perfil de acesso no sistema.
    """

    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    tipo_perfil = Column(Enum(TipoPerfil, name="tipo_perfil_enum"), default=TipoPerfil.NOVATO, nullable=False)
    cargo = Column(String(50), nullable=True) #ex: Dev Júnior, Data analyst, Dev Sênior
    data_cadastro = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<Usuario(id={self.id_usuario}, nome='{self.nome}', perfil='{self.tipo_perfil}')>"