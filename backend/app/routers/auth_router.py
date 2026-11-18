from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import Usuario
from app.schemas.user_schema import UsuarioCreate, UsuarioLogin, UsuarioResponse, TokenResponse
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticação & Usuários"])


@router.post("/cadastro", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(payload: UsuarioCreate, db: Session = Depends(get_db)):
    existing = db.scalar(select(Usuario).where(Usuario.email == payload.email.lower()))
    if existing:
        raise HTTPException(status_code=409, detail="Este e-mail já está cadastrado no RampUp.")
    user = Usuario(
        nome=payload.nome.strip(),
        email=payload.email.lower(),
        senha_hash=hash_password(payload.senha),
        tipo_perfil=payload.tipo_perfil,
        cargo=payload.cargo,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: UsuarioLogin, db: Session = Depends(get_db)):
    user = db.scalar(select(Usuario).where(Usuario.email == payload.email.lower()))
    if user is None or not verify_password(payload.senha, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
        )
    token = create_access_token(str(user.id_usuario), user.tipo_perfil.value)
    return TokenResponse(access_token=token, usuario=user)


@router.get("/me", response_model=UsuarioResponse)
def usuario_atual(user: Usuario = Depends(get_current_user)):
    return user
