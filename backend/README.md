# Backend RampUp

API REST modular em Node.js, Express e PostgreSQL, conforme a PropostaErika.md.

## Requisitos
- Node.js 20 ou superior
- PostgreSQL 14 ou superior

## Configuração
```bash
cp .env.example .env
# Edite DATABASE_URL e JWT_SECRET
npm install
npm run db:init
npm run db:seed
npm start
```

No PowerShell: `Copy-Item .env.example .env`. Edite o arquivo `.env`.

API: `http://localhost:3000`; saúde: `/health`; Swagger: `/docs`.

## Usuários demonstrativos
Lucas, Bruno e Mariana: `lucas@rampup.local`, `bruno@rampup.local` e `mariana@rampup.local`. Senha comum: `RampUpDemo!2026`. Use exclusivamente em ambiente local de demonstração; nunca reutilize em produção.
