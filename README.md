# ProjetoIntegrador_RampupApp

O \*\*RampUp\*\* é uma plataforma web interativa desenvolvida para resolver os principais gargalos enfrentados por novos colaboradores técnicos em seu primeiro mês de trabalho. O sistema substitui processos manuais e dispersos por um workflow estruturado que combina checklists cronológicos, sinalização de bloqueios operacionais e mentoria em tempo real. 
Este repositório contém a \*\*Proof of Concept (PoC)\*\* completa desenvolvida para o \*\*Projeto Integrador - 4º Semestre\*\* do Centro Universitário Senac EAD 2026.

## Autores
* Erika Cunha
* Gerson Yabiku
* Jessica Garcia
* Manuele Xavier

## O RampUp
Trata-se de uma aplicação web responsiva (compatível com desktops, notebooks e dispositivos móveis), desenvolvida sob a arquitetura de software em camadas e orientada a microsserviços. A solução integra um frontend dinâmico em React/HTML5/CSS3 com um backend modularizado em Python/Node.js, comunicando-se via API REST e persistindo dados em banco relacional SQL.

## Funcionalidades

- Dashboard do Novato (Lucas Rocha): Visualização do progresso percentual da rampa de entrada em tempo real.
- Checklist interativo agrupado por períodos (Dia 1, Dia 2, Semana 1, Mês 1). 
- Acesso direto a tutoriais, repositórios e documentações da empresa. 
- Botão "Estou Travado": Mecanismo para sinalização imediata de impedimentos técnicos. 
- Permite ao novato colar o log de erro/stacktrace do terminal para análise do mentor. Altera automaticamente o status da tarefa para TRAVADO (destaque visual em vermelho). 
- Painel do Mentor / Buddy (Bruno Santos): Central de monitoramento com a fila de bloqueios ativos dos novatos supervisionados.
- Exibição do terminal com o erro exato e identificação do colaborador. 
- Ação em um clique: "Destravar / Resolver Pendência", que atualiza o progresso no banco e notifica o novato. 
- Documentação Swagger Automática: Interface interativa para teste e validação de todas as rotas da API REST (/docs).
- Acesso demonstrativo por três perfis: novato, Buddy e Tech Lead.


## Tecnologias
### Backend & Banco de Dados 
* Linguagem: Python 3.12+ , 
* Framework Web:FastAPI 
* ORM: SQLAlchemy 
* Validação de Dados: Pydantic v2 
* Driver do Banco: psycopg2-binary 
* Servidor ASGI: Uvicorn 
* Banco de Dados: PostgreSQL 

### Frontend 
* Biblioteca: React 18
* Ferramenta de Build: Vite 
* Cliente HTTP:Axios 
* Arquitetura: Componentização baseada em Hooks e consumo de API REST

## Pré-Requisitos
* **Python 3.10+** instalado.
* **Node.js 18+** e `npm` instalados.
* **PostgreSQL** instalado e em execução na sua máquina.

## Instalação

## Para rodar a aplicação
* No terminal acesse o backend e popule o banco de dados: python seed.py
* Inicie o servidor API REST: uvicorn main:app --reload
* Abra outro terminal e acesse o frontend, inicie o servidor da interface web: npm run dev
* Interface ativa em* *http://localhost:5173*


## Usuários demonstrativos

## Testes

## Endpoints principais

## Estrutura do projeto
```text
rampup-app/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt (Lista as dependências Python, como FastAPI, Uvicorn, SQLAlchemy, PostgreSQL e Pydantic.)
│   ├── main.py (Ponto de entrada da API)
│   ├── seed.py (usado para popular o banco com dados iniciais de teste)
│   └── app/
│        ├── __init__.py
│        ├── config.py
│        ├── database.py (configura a conexão com o PostgreSQL usando SQLAlchemy)
│        │ 
│        └── models/ (tabelas do banco de dados)
│        │   ├── __init__.py
│        │   ├── user.py
│        │   ├── task.py
│        │   └── block.py
│        │
│        └── schemas/ (define o formato dos dados recebidos e enviados pela API usando Pydantic)
│        │   ├── __init__.py
│        │   ├── user_schema.py
│        │   ├── task_schema.py
│        │   └── block_schema.py
│        │
│        └── routers/ (contém as rotas HTTP da aplicação)
│        │   ├── __init__.py
│        │   ├── auth_router.py
│        │   ├── onboarding_router.py
│        │   ├── block_router.py
│        │   └── mentor_router.py
│        │
│        └── services/
│            ├── __init__.py
│            └── onboarding_service.py
│            
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── public
│   ├── index.html
│   ├── vite.config.js
│   ├── .env
│   └── src/
│        ├── main.jsx
│        ├── App.jsx
│        ├── api/
│        │   └── axios_config.js
│        │ 
│        ├── components/
│        │   ├── Header.jsx
│        │   ├── TaskCard.jsx
│        │   ├── StuckModal.jsx
│        │   └── MentorAlert.jsx
│        │
│        ├── pages/
│        │   ├── NovatoDashboard.jsx
│        │   ├── MentorDashboard.jsx
│        │   └── Login.jsx
│        │ 
│        └── styles/
│            └── main.css
├── docs/
├── README.md
├── docker-compose.yml
└── .gitignore
```
