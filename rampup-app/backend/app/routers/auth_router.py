# Gerencia o cadastro de colaboradores e a rota de login
from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.orm import Session 
from app.database import get_db 
from app.models.user import Usuario
from app.schemas.user_schema import UsuarioCreate, UsuarioResponse, UsuarioLogin, TokenResponse

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticação & Usuários"])

@router.post("/cadastro", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED) 
def cadastrar_usuario(usuario_data: UsuarioCreate, db: Session = Depends(get_db)): 
    # Verifica se o e-mail já está cadastrado 
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario_data.email).first() 
    if usuario_existente: 
        raise HTTPException( 
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Este e-mail já está cadastrado no RampUp." 
        )

    # Cria o novo usuário (Em produção, aplique hash na senha ex: passlib/bcrypt) 
    novo_usuario = Usuario( 
        nome=usuario_data.nome, 
        email=usuario_data.email, 
        senha_hash=usuario_data.senha,     # Hash de senha 
        tipo_perfil=usuario_data.tipo_perfil, 
        cargo=usuario_data.cargo 
    ) 
    db.add(novo_usuario) 
    db.commit() 
    db.refresh(novo_usuario) 
    return novo_usuario

@router.post("/login", response_model=TokenResponse) 
def login(login_data: UsuarioLogin, db: Session = Depends(get_db)): 
    # Busca o usuário pelo e-mail 
    usuario = db.query(Usuario).filter(Usuario.email == login_data.email).first() 
    if not usuario or usuario.senha_hash != login_data.senha: 
        raise HTTPException( 
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="E-mail ou senha incorretos." 
        ) 
    
    # Retorna o token de acesso (Simulado para PoC; integre JWT conforme necessário) 
    return TokenResponse( 
        access_token=f"fake-jwt-token-user-{usuario.id_usuario}", 
        token_type="bearer",
        usuario=usuario 
    )
