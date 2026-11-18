import os 
from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:Minnie@localhost:5432/rampup_db"

if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg2://",
        1
    )

# 1. Cria o Motor de Conexão (Engine) 
engine = create_engine(DATABASE_URL, echo=False) 

# 2. Cria a fábrica de sessões para comunicação com o banco 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

# 3. Base declarativa herdada por todos os modelos ORM (Usuario, Tarefa, Bloqueio) 

Base = declarative_base() 

# 4. Injetor de Dependência (yield) para abrir e fechar conexões por requisição HTTP 
def get_db(): 
    db = SessionLocal() 
    try: 
        yield db 
    finally: 
        db.close() # Fecha a sessão automaticamente após a rota responder
