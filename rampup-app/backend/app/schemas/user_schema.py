from datetime import datetime 
from typing import Optional 
from pydantic import BaseModel, EmailStr, ConfigDict 
from app.models.user import TipoPerfil

# Schema Base de Usuário (campos comuns)
class UsuarioBase(BaseModel): 
    nome: str 
    email: EmailStr 
    cargo: Optional[str] = None 
    tipo_perfil: TipoPerfil = TipoPerfil.NOVATO

# Schema para criação de novo usuário (Recebe a senha em texto puro)
class UsuarioCreate(UsuarioBase): 
    senha: str

# Schema de Resposta de Usuário (Retorna para o Frontend sem a senha!)
class UsuarioResponse(UsuarioBase): 
    id_usuario: int
    data_cadastro: datetime

    # Permite a conversão automática dos objetos ORM do SQLAlchemy para Pydantic
    model_config = ConfigDict(from_attributes=True)

# Schema para autenticação / Login
class UsuarioLogin(BaseModel): 
    email: EmailStr 
    senha: str

# Schema do Token JWT retornado no Login
class TokenResponse(BaseModel):
    access_token: str 
    token_type: str = "bearer"
    usuario: UsuarioResponse