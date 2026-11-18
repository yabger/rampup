"""Cria dados demonstrativos idempotentes para a apresentação da PoC."""
from sqlalchemy import select

from app.database import Base, SessionLocal, engine
from app.models import (
    Usuario, TipoPerfil, Trilha, Tarefa, PeriodoOnboarding,
    ProgressoTarefa, StatusTarefa, VinculoMentoria,
)
from app.security import hash_password


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        demo_users = [
            ("Lucas Rocha", "lucas.rocha@empresa.com", TipoPerfil.NOVATO, "Desenvolvedor Júnior"),
            ("Bruno Santos", "bruno.santos@empresa.com", TipoPerfil.BUDDY, "Desenvolvedor Sênior"),
            ("Mariana Costa", "mariana.costa@empresa.com", TipoPerfil.TECH_LEAD, "Tech Lead"),
        ]
        users = {}
        for name, email, role, job in demo_users:
            user = db.scalar(select(Usuario).where(Usuario.email == email))
            if user is None:
                user = Usuario(
                    nome=name,
                    email=email,
                    senha_hash=hash_password("123456"),
                    tipo_perfil=role,
                    cargo=job,
                )
                db.add(user)
                db.flush()
            users[email] = user

        lucas = users["lucas.rocha@empresa.com"]
        bruno = users["bruno.santos@empresa.com"]
        link = db.scalar(select(VinculoMentoria).where(VinculoMentoria.id_novato == lucas.id_usuario))
        if link is None:
            db.add(VinculoMentoria(id_novato=lucas.id_usuario, id_mentor=bruno.id_usuario))

        trail = db.scalar(select(Trilha).where(Trilha.cargo_destino == "Desenvolvedor Júnior"))
        if trail is None:
            trail = Trilha(
                titulo_trilha="Onboarding de Desenvolvimento",
                cargo_destino="Desenvolvedor Júnior",
                descricao="Trilha demonstrativa de configuração do ambiente técnico.",
            )
            db.add(trail)
            db.flush()
            task_data = [
                ("Acessar contas e ferramentas corporativas", PeriodoOnboarding.DIA_1, 20, 1),
                ("Clonar o repositório do projeto", PeriodoOnboarding.DIA_1, 25, 2),
                ("Instalar e configurar Git", PeriodoOnboarding.DIA_2, 30, 3),
                ("Configurar Docker", PeriodoOnboarding.SEMANA_1, 45, 4),
                ("Executar a aplicação localmente", PeriodoOnboarding.SEMANA_1, 40, 5),
                ("Revisar arquitetura e documentação", PeriodoOnboarding.SEMANA_2, 60, 6),
                ("Realizar primeira contribuição", PeriodoOnboarding.MES_1, 90, 7),
            ]
            for title, period, minutes, order in task_data:
                db.add(Tarefa(
                    id_trilha=trail.id_trilha,
                    titulo=title,
                    descricao=f"Conclua a etapa: {title.lower()}.",
                    periodo=period,
                    tempo_estimado_min=minutes,
                    ordem=order,
                ))
            db.flush()

        tasks = db.scalars(select(Tarefa).where(Tarefa.id_trilha == trail.id_trilha).order_by(Tarefa.ordem)).all()
        for task in tasks:
            progress = db.scalar(select(ProgressoTarefa).where(
                ProgressoTarefa.id_usuario == lucas.id_usuario,
                ProgressoTarefa.id_tarefa == task.id_tarefa,
            ))
            if progress is None:
                db.add(ProgressoTarefa(
                    id_usuario=lucas.id_usuario,
                    id_tarefa=task.id_tarefa,
                    status=StatusTarefa.PENDENTE,
                ))
        db.commit()
        print("Seed concluído. Usuários demonstrativos: Lucas, Bruno e Mariana.")
        print("Senha dos três usuários: 123456")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
