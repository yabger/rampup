from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base 
# Importa os modelos para que o SQLAlchemy reconheça a estrutura 
from app.models import user, task, block 

#Importação dos Routers
from app.routers import auth_router, onboarding_router, block_router, mentor_router


app = FastAPI( 
	title="RampUp API REST", 
	description="API do Hub Interativo de Onboarding Técnico", 
	version="1.0.0" 
)

# Configuração de CORS para permitir requisições do Frontend em React 
app.add_middleware( 
    CORSMiddleware, 
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
	allow_credentials=True, 
	allow_methods=["*"],
	allow_headers=["*"], 
)

# Inicializa as tabelas no PostgreSQL se não existirem
Base.metadata.create_all(bind=engine) 

# Registro das rotas na aplicação
app.include_router(auth_router.router) 
app.include_router(onboarding_router.router) 
app.include_router(block_router.router) 
app.include_router(mentor_router.router)

@app.get("/") 
def root(): 
	return { 
		"status": "online", 
		"app": "RampUp API REST", 
		"docs": "Acesse /docs para visualizar a documentação interativa do Swagger" 
	}