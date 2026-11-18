from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.models.user import TipoPerfil


class UsuarioCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=120)
    email: EmailStr
    senha: str = Field(min_length=6, max_length=128)
    tipo_perfil: TipoPerfil = TipoPerfil.NOVATO
    cargo: str | None = Field(default=None, max_length=100)


class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str


class UsuarioResponse(BaseModel):
    id_usuario: int
    nome: str
    email: EmailStr
    tipo_perfil: TipoPerfil
    cargo: str | None = None
    data_cadastro: datetime
    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse
