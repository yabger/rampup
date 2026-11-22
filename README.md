# RampUp — Hub Interativo de Onboarding Técnico

O **RampUp** é uma aplicação web desenvolvida como Proof of Concept (PoC) para o Projeto Integrador do 4º semestre do Centro Universitário Senac EAD (2026).

A proposta é organizar o processo de integração de novos colaboradores técnicos por meio de uma trilha de onboarding, acompanhamento de tarefas e registro de impedimentos que podem ser tratados por um mentor (Buddy).

> **Estado atual:** o fluxo principal está implementado e foi validado manualmente entre frontend, API e PostgreSQL. Esta versão é uma PoC acadêmica, não uma solução pronta para produção.

## Autores

- Erika Cunha
- Gerson Yabiku
- Manuele Xavier

## Funcionalidades implementadas

### Novato

- Autenticação demonstrativa pela tela de login.
- Visualização da trilha de onboarding e do progresso das tarefas.
- Consulta das tarefas organizadas por período.
- Marcação de tarefas como concluídas.
- Registro de impedimentos por meio da ação **Estou travado**, com descrição ou log do erro.
- Atualização do status da tarefa para `BLOQUEADO` quando um impedimento é registrado.

### Mentor (Buddy)

- Visualização dos bloqueios ativos associados ao mentor.
- Consulta do novato, da tarefa e da descrição do impedimento.
- Resolução de um bloqueio.
- Ao resolver, o bloqueio passa para `RESOLVIDO` e a tarefa correspondente retorna para `PENDENTE`.

A atualização do dashboard ocorre por novas consultas à API. **Não há implementação de atualização em tempo real** por WebSocket, Server-Sent Events ou polling automático.

### API

- API REST desenvolvida com FastAPI.
- Documentação interativa gerada pelo FastAPI em `/docs`.
- Persistência relacional com PostgreSQL e SQLAlchemy.

## Tecnologias

| Camada | Tecnologias |
|---|---|
| Frontend | React, Vite, JavaScript, Axios |
| Backend | Python, FastAPI, Pydantic, SQLAlchemy |
| Servidor da API | Uvicorn |
| Banco de dados | PostgreSQL |
| Driver PostgreSQL | psycopg2-binary |

O backend está organizado em módulos (modelos, schemas, rotas e serviços) dentro de uma aplicação FastAPI. O projeto **não é composto por microsserviços**.

## Requisitos

- Python 3.10 ou superior.
- Node.js e npm (Node.js 18 ou superior recomendado).
- PostgreSQL em execução.
- Git.

## Estrutura do projeto

```text
rampup/
├── rampup-app/
│   ├── backend/
│   │   ├── app/
│   │   │   ├── models/
│   │   │   │   ├── user.py
│   │   │   │   ├── task.py
│   │   │   │   └── block.py
│   │   │   ├── schemas/
│   │   │   │   ├── user_schema.py
│   │   │   │   ├── task_schema.py
│   │   │   │   └── block_schema.py
│   │   │   ├── routers/
│   │   │   │   ├── auth_router.py
│   │   │   │   ├── onboarding_router.py
│   │   │   │   ├── block_router.py
│   │   │   │   └── mentor_router.py
│   │   │   ├── services/
│   │   │   │   └── onboarding_service.py
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   ├── main.py
│   │   ├── main-Lenovo.py
│   │   ├── seed.py
│   │   └── requirements.txt
│   └── frontend/
│       ├── package.json
│       └── src/
│           ├── api/
│           │   └── axios_config.js
│           ├── components/
│           │   ├── Header.jsx
│           │   ├── MentorAlert.jsx
│           │   ├── StuckModel.jsx
│           │   └── TaskCard.jsx
│           ├── pages/
│           │   ├── LoginScreen.jsx
│           │   ├── MentorDashboard.jsx
│           │   └── NovatoDashboard.jsx
│           ├── App.jsx
│           └── main.jsx
└── README.md
```

## Configuração e execução

Os comandos abaixo consideram que o terminal está na raiz do repositório.

### 1. Configurar o banco PostgreSQL

Crie um banco de dados e um usuário para a aplicação. Exemplo, executado como administrador do PostgreSQL:

```sql
CREATE USER rampup WITH PASSWORD 'SUA_SENHA';
CREATE DATABASE rampup_db OWNER rampup;
```

Se o banco e o usuário já existirem, não é necessário criá-los novamente.

### 2. Configurar o backend

Entre no diretório do backend:

```bash
cd rampup-app/backend
```

Crie e ative um ambiente virtual:

**Bash:**
```bash
python -m venv .venv
source .venv/bin/activate
```

**fish:**
```fish
python -m venv .venv
source .venv/bin/activate.fish
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure a variável de ambiente `DATABASE_URL` em um arquivo local chamado `.env`, dentro de `rampup-app/backend/`:

```dotenv
DATABASE_URL=postgresql://rampup:SUA_SENHA@localhost:5432/rampup_db
```

Substitua `SUA_SENHA` pela senha definida para o usuário PostgreSQL. Não versione o arquivo `.env` nem credenciais reais.

### 3. Popular o banco com dados demonstrativos

Ainda no diretório `rampup-app/backend/`, execute:

```bash
python seed.py
```

O script cria os dados demonstrativos que ainda não existirem. Ele não redefine automaticamente registros já existentes; portanto, executá-lo novamente não restaura necessariamente o estado inicial da demonstração.

### 4. Iniciar a API

No mesmo diretório do backend:

```bash
uvicorn main:app --reload
```

A API ficará disponível em:

- API: http://localhost:8000/
- Documentação Swagger: http://localhost:8000/docs
- OpenAPI: http://localhost:8000/openapi.json

Mantenha esse terminal aberto.

### 5. Instalar e iniciar o frontend

Abra outro terminal e execute:

```bash
cd ~/rampup/rampup-app/frontend
npm install
npm run dev
```

O Vite disponibilizará a interface, normalmente, em http://localhost:5173/.

O frontend utiliza `VITE_API_URL` como URL opcional da API. Se não estiver definida, utiliza `http://localhost:8000`.

## Usuários demonstrativos

Os dados abaixo são criados pelo script `seed.py`, caso ainda não existam:

| Perfil | Nome | E-mail | Senha demonstrativa |
|---|---|---|---|
| Novato | Lucas Rocha | `lucas.rocha@empresa.com` | `123456` |
| Buddy | Bruno Santos | `bruno.santos@empresa.com` | `123456` |
| Tech Lead | Mariana Costa | `mariana.costa@empresa.com` | `123456` |

As credenciais são exclusivamente para demonstração local. Não as utilize em ambientes reais.

## Endpoints principais

| Método | Endpoint | Finalidade |
|---|---|---|
| GET | `/` | Verificar se a API está online |
| POST | `/api/v1/auth/cadastro` | Cadastrar usuário |
| POST | `/api/v1/auth/login` | Realizar login |
| GET | `/api/v1/onboarding/trilha/{id_usuario}` | Consultar trilha e progresso do usuário |
| PUT | `/api/v1/onboarding/tasks/{id_progresso}/status` | Atualizar status de uma tarefa |
| POST | `/api/v1/blocks/stuck` | Registrar impedimento |
| PUT | `/api/v1/blocks/{id_bloqueio}/unblock` | Resolver impedimento |
| GET | `/api/v1/mentor/dashboard/{id_mentor}` | Consultar bloqueios ativos do mentor |

Os schemas completos de entrada e saída podem ser consultados em `/docs`.

## Testes realizados

Foi realizada validação manual do fluxo principal:

1. Login do novato.
2. Consulta da trilha de onboarding.
3. Conclusão de uma tarefa e atualização do progresso.
4. Registro de um impedimento.
5. Associação do impedimento ao mentor vinculado.
6. Exibição do impedimento no dashboard do mentor.
7. Resolução do impedimento pelo mentor.
8. Retorno da tarefa para o status `PENDENTE` e remoção do bloqueio da lista de ativos.

Essas verificações foram feitas manualmente pela interface e por chamadas à API. **Uma suíte de testes automatizados ainda não está documentada como concluída.**

## Limitações conhecidas da PoC

- O login ainda utiliza comparação de senha em texto puro e retorna um token demonstrativo, não um JWT validável.
- As rotas ainda não implementam autenticação e autorização efetivas por token.
- A atualização do dashboard não é em tempo real.
- O fluxo de cadastro existe na API, mas não há confirmação de uma tela de cadastro integrada no frontend.
- Não há, nesta versão, implementação funcional completa para todos os modelos auxiliares, como vínculos de mentoria e documentação obsoleta.
- O tratamento de erros e a cobertura de testes automatizados ainda precisam ser ampliados.

Essas limitações devem ser consideradas antes de qualquer uso fora do ambiente acadêmico de demonstração.
