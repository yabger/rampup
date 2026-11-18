from tests.conftest import login


def test_health_and_openapi(client):
    assert client.get("/health").json()["status"] == "ok"
    assert client.get("/openapi.json").status_code == 200


def test_onboarding_and_block_resolution_flow(client):
    lucas_headers = login(client, "lucas@example.com")
    bruno_headers = login(client, "bruno@example.com")

    trail = client.get(f"/api/v1/onboarding/trilha/{client.lucas_id}", headers=lucas_headers)
    assert trail.status_code == 200
    assert trail.json()[0]["tarefa"]["titulo"] == "Clonar repositório"

    blocked = client.post(
        "/api/v1/blocks/stuck",
        headers=lucas_headers,
        json={"id_progresso": client.progress_id, "log_erro": "Permission denied (publickey)"},
    )
    assert blocked.status_code == 201
    block_id = blocked.json()["id_bloqueio"]

    dashboard = client.get(
        f"/api/v1/mentor/dashboard/{client.bruno_id}", headers=bruno_headers
    )
    assert dashboard.status_code == 200
    assert len(dashboard.json()) == 1
    assert dashboard.json()[0]["progresso_tarefa"]["usuario"]["nome"] == "Lucas Rocha"

    resolved = client.put(f"/api/v1/blocks/{block_id}/unblock", headers=bruno_headers)
    assert resolved.status_code == 200
    assert resolved.json()["status_bloqueio"] == "RESOLVIDO"
    assert resolved.json()["progresso_tarefa"]["status"] == "CONCLUIDO"


def test_novato_cannot_access_mentor_dashboard(client):
    headers = login(client, "lucas@example.com")
    response = client.get(
        f"/api/v1/mentor/dashboard/{client.bruno_id}", headers=headers
    )
    assert response.status_code == 403
