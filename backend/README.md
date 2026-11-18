# RampUp — Backend FastAPI

Backend da PoC RampUp, alinhado ao README principal do projeto: Python 3.12+, FastAPI, SQLAlchemy 2, Pydantic v2 e PostgreSQL. A API entrega JSON e documentação OpenAPI/Swagger em `/docs`.

## Requisitos

- Python 3.10+ (recomendado Python 3.12)
- PostgreSQL 14+
- `python` e `pip`

## 1. Preparar o banco PostgreSQL

Crie um usuário e um banco para desenvolvimento. Exemplo no `psql`, usando uma conta administrativa:

```sql
CREATE USER rampup WITH PASSWORD 'rampup_dev';
CREATE DATABASE rampup_db OWNER rampup;
```

Não use essa senha de exemplo em ambientes compartilhados ou de produção.

## 2. Criar ambiente Python

Na pasta `backend/`:

```bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\\Scripts\\Activate.ps1  # Windows PowerShell

python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env            # Linux/macOS
```

No Windows PowerShell, use `Copy-Item .env.example .env`.

Edite `.env` e configure `DATABASE_URL` e `JWT_SECRET`. Gere um segredo com:

```bash
openssl rand -hex 32
```

O arquivo `.env` é local e não deve ser enviado ao Git.

## 3. Criar tabelas e dados demonstrativos

A primeira inicialização da API cria as tabelas que ainda não existirem. Para inserir os usuários e tarefas de demonstração, execute:

```bash
python seed.py
```

O seed é idempotente para os registros demonstrativos: pode ser executado novamente sem duplicar os usuários, o vínculo e os progressos existentes.

### Contas da demonstração

| Perfil | E-mail | Senha local de demonstração |
|---|---|---|
| Novato — Lucas Rocha | `lucas.rocha@empresa.com` | `123456` |
| Buddy — Bruno Santos | `bruno.santos@empresa.com` | `123456` |
| Tech Lead — Mariana Costa | `mariana.costa@empresa.com` | `123456` |

As senhas são exclusivamente para a PoC local. Troque-as antes de qualquer implantação acessível externamente.

## 4. Executar a API

Com o ambiente virtual ativado e o PostgreSQL disponível:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Endereços locais:

- API: http://127.0.0.1:8000
- Health check: http://127.0.0.1:8000/health
- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

## Endpoints principais

| Método | Endpoint | Finalidade |
|---|---|---|
| POST | `/api/v1/auth/login` | Autenticar e emitir JWT |
| POST | `/api/v1/auth/cadastro` | Cadastrar usuário |
| GET | `/api/v1/auth/me` | Consultar usuário autenticado |
| GET | `/api/v1/onboarding/trilha/{usuario_id}` | Consultar trilha e progresso |
| GET | `/api/v1/onboarding/trilha/{usuario_id}/resumo` | Consultar percentual de conclusão |
| PUT | `/api/v1/onboarding/tasks/{progresso_id}/status` | Atualizar status de tarefa |
| POST | `/api/v1/blocks/stuck` | Registrar bloqueio e log de erro |
| PUT | `/api/v1/blocks/{bloqueio_id}/unblock` | Resolver bloqueio pelo Buddy/Tech Lead |
| GET | `/api/v1/mentor/dashboard/{mentor_id}` | Listar bloqueios ativos do Buddy |
| GET | `/api/v1/metrics/overview` | Consultar indicadores gerais |

As rotas protegidas exigem `Authorization: Bearer <token>`. O Swagger permite executar o fluxo após autenticar e informar o token no botão **Authorize**.

## 5. Testes

Os testes automatizados usam SQLite temporário em memória, sem exigir uma instância PostgreSQL:

```bash
pytest -q
```

Eles verificam o health check/OpenAPI e a jornada central: login do novato, consulta da trilha, criação de bloqueio, visualização no painel do Buddy e resolução.

## Integração com o frontend

O frontend Vite do projeto usa `http://localhost:8000` como URL padrão e envia o JWT no cabeçalho `Authorization`. A origem `http://localhost:5173` já está liberada por padrão em `CORS_ORIGINS`.

## Observações de escopo

- Esta é uma PoC acadêmica, não uma implantação pronta para produção.
- As tabelas são criadas por `Base.metadata.create_all`; para evolução de schema em produção, adote migrações Alembic.
- O endpoint de cadastro aceita o perfil informado no payload para facilitar a demonstração. Em produção, a atribuição de perfis privilegiados deve ser restrita a administradores.
- O “aviso” ao novato é refletido no estado persistido e pode ser consultado novamente pelo frontend; não há envio de e-mail, push ou WebSocket nesta PoC.
