# Contrato de integração do backend

## Login

`POST /api/v1/auth/login`

```json
{
  "email": "lucas.rocha@empresa.com",
  "senha": "123456"
}
```

Retorna `access_token`, `token_type` e `usuario` (inclui `id_usuario` e `tipo_perfil`).

## Trilha

`GET /api/v1/onboarding/trilha/{usuario_id}`

Retorna uma lista de progressos. Cada item contém `id_progresso`, `status` e o objeto `tarefa` (`titulo`, `periodo`, `tempo_estimado_min`, `link_tutorial`). Os status usados pela interface são `PENDENTE`, `CONCLUIDO` e `TRAVADO`.

## Atualizar tarefa

`PUT /api/v1/onboarding/tasks/{progresso_id}/status`

```json
{ "status": "CONCLUIDO" }
```

## Sinalizar bloqueio

`POST /api/v1/blocks/stuck`

```json
{
  "id_progresso": 2,
  "log_erro": "Permission denied (publickey)"
}
```

## Painel Buddy

`GET /api/v1/mentor/dashboard/{mentor_id}`

Retorna bloqueios ativos com `id_bloqueio`, `log_erro`, `data_bloqueio` e `progresso_tarefa`, incluindo os dados `usuario.nome` e `tarefa.titulo` usados pelo dashboard React.

## Resolver bloqueio

`PUT /api/v1/blocks/{bloqueio_id}/unblock`

Marca o bloqueio como `RESOLVIDO` e a tarefa associada como `CONCLUIDO`.
