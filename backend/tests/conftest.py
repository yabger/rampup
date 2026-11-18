import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

os.environ.setdefault("JWT_SECRET", "test-secret-for-rampup-only")
os.environ.setdefault("DATABASE_URL", "sqlite://")

from app.database import Base, get_db
from app.models import Usuario, TipoPerfil, Trilha, Tarefa, PeriodoOnboarding, ProgressoTarefa, StatusTarefa, VinculoMentoria
from app.security import hash_password
from main import app
import main as main_module


@pytest.fixture()
def client():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSession = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=test_engine)

    db = TestingSession()
    lucas = Usuario(nome="Lucas Rocha", email="lucas@example.com", senha_hash=hash_password("123456"), tipo_perfil=TipoPerfil.NOVATO)
    bruno = Usuario(nome="Bruno Santos", email="bruno@example.com", senha_hash=hash_password("123456"), tipo_perfil=TipoPerfil.BUDDY)
    db.add_all([lucas, bruno])
    db.flush()
    trail = Trilha(titulo_trilha="Trilha Dev", cargo_destino="Dev Jr")
    db.add(trail)
    db.flush()
    task = Tarefa(id_trilha=trail.id_trilha, titulo="Clonar repositório", periodo=PeriodoOnboarding.DIA_1, tempo_estimado_min=20, ordem=1)
    db.add(task)
    db.flush()
    progress = ProgressoTarefa(id_usuario=lucas.id_usuario, id_tarefa=task.id_tarefa, status=StatusTarefa.PENDENTE)
    db.add(progress)
    db.add(VinculoMentoria(id_novato=lucas.id_usuario, id_mentor=bruno.id_usuario))
    db.commit()
    lucas_id, bruno_id, progress_id = lucas.id_usuario, bruno.id_usuario, progress.id_progresso
    db.close()

    def override_get_db():
        session = TestingSession()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    original_engine = main_module.engine
    main_module.engine = test_engine
    with TestClient(app) as test_client:
        test_client.lucas_id = lucas_id
        test_client.bruno_id = bruno_id
        test_client.progress_id = progress_id
        yield test_client
    app.dependency_overrides.clear()
    main_module.engine = original_engine
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


def login(client, email):
    response = client.post("/api/v1/auth/login", json={"email": email, "senha": "123456"})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}
