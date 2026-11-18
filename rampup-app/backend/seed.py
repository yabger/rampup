
from datetime import datetime

from app.database import Base, SessionLocal, engine
from app.models.user import Usuario, TipoPerfil
from app.models.task import (
    Trilha,
    Tarefa,
    ProgressoTarefa,
    PeriodoOnboarding,
    StatusTarefa,
)
from app.models.block import (
    Bloqueio,
    StatusBloqueio,
    VinculoMentoria,
)


def obter_ou_criar_usuario(db, dados):
    usuario = (
        db.query(Usuario)
        .filter(Usuario.email == dados["email"])
        .first()
    )

    if usuario is None:
        usuario = Usuario(**dados)
        db.add(usuario)
        db.flush()

        print(f"Usuário criado: {usuario.email}")
    else:
        print(f"Usuário já existente: {usuario.email}")

    return usuario


def obter_ou_criar_trilha(db, dados):
    trilha = (
        db.query(Trilha)
        .filter(
            Trilha.titulo_trilha == dados["titulo_trilha"],
            Trilha.cargo_destino == dados["cargo_destino"],
        )
        .first()
    )

    if trilha is None:
        trilha = Trilha(**dados)
        db.add(trilha)
        db.flush()

        print(f"Trilha criada: {trilha.titulo_trilha}")
    else:
        print(f"Trilha já existente: {trilha.titulo_trilha}")

    return trilha


def obter_ou_criar_tarefa(db, id_trilha, dados):
    tarefa = (
        db.query(Tarefa)
        .filter(
            Tarefa.id_trilha == id_trilha,
            Tarefa.titulo == dados["titulo"],
        )
        .first()
    )

    if tarefa is None:
        tarefa = Tarefa(
            id_trilha=id_trilha,
            **dados,
        )
        db.add(tarefa)
        db.flush()

        print(f"Tarefa criada: {tarefa.titulo}")

    return tarefa


def obter_ou_criar_progresso(
    db,
    id_usuario,
    tarefa,
    status_inicial,
):
    progresso = (
        db.query(ProgressoTarefa)
        .filter(
            ProgressoTarefa.id_usuario == id_usuario,
            ProgressoTarefa.id_tarefa == tarefa.id_tarefa,
        )
        .first()
    )

    if progresso is None:
        progresso = ProgressoTarefa(
            id_usuario=id_usuario,
            id_tarefa=tarefa.id_tarefa,
            status=status_inicial,
            data_conclusao=(
                datetime.now()
                if status_inicial == StatusTarefa.CONCLUIDO
                else None
            ),
        )

        db.add(progresso)
        db.flush()

        print(f"Progresso criado: {tarefa.titulo}")

    return progresso


def povoar_banco():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        print("\nIniciando povoamento do banco RampUp...\n")

        # 1. Usuários de demonstração

        lucas = obter_ou_criar_usuario(
            db,
            {
                "nome": "Lucas Rocha",
                "email": "lucas.rocha@empresa.com",
                "senha_hash": "123456",
                "tipo_perfil": TipoPerfil.NOVATO,
                "cargo": "Dev Júnior",
            },
        )

        bruno = obter_ou_criar_usuario(
            db,
            {
                "nome": "Bruno Santos",
                "email": "bruno.santos@empresa.com",
                "senha_hash": "123456",
                "tipo_perfil": TipoPerfil.BUDDY,
                "cargo": "Dev Sênior",
            },
        )

        obter_ou_criar_usuario(
            db,
            {
                "nome": "Mariana Costa",
                "email": "mariana.costa@empresa.com",
                "senha_hash": "123456",
                "tipo_perfil": TipoPerfil.TECH_LEAD,
                "cargo": "Gerente de Engenharia",
            },
        )

        # 2. Vínculo de mentoria

        vinculo = (
            db.query(VinculoMentoria)
            .filter(
                VinculoMentoria.id_novato == lucas.id_usuario,
                VinculoMentoria.id_mentor == bruno.id_usuario,
            )
            .first()
        )

        if vinculo is None:
            vinculo = VinculoMentoria(
                id_novato=lucas.id_usuario,
                id_mentor=bruno.id_usuario,
            )

            db.add(vinculo)
            db.flush()

            print("Vínculo de mentoria criado: Lucas -> Bruno")

        # 3. Trilha de onboarding

        trilha = obter_ou_criar_trilha(
            db,
            {
                "titulo_trilha": "Onboarding Engenharia de Software",
                "cargo_destino": "Dev Júnior",
                "descricao": (
                    "Checklist de configuração de ambiente "
                    "e acessos para novos desenvolvedores."
                ),
            },
        )

        # 4. Tarefas

        tarefas_dados = [
            {
                "titulo": "Configurar Acessos e Credenciais (VPN, GitHub, Slack)",
                "periodo": PeriodoOnboarding.DIA_1,
                "tempo_estimado_min": 30,
                "link_tutorial": None,
                "ordem": 1,
            },
            {
                "titulo": "Instalar e Configurar Docker e Containers Locais",
                "periodo": PeriodoOnboarding.DIA_1,
                "tempo_estimado_min": 45,
                "link_tutorial": None,
                "ordem": 2,
            },
            {
                "titulo": "Clonar Repositório Principal e Instalar Dependências",
                "periodo": PeriodoOnboarding.DIA_2,
                "tempo_estimado_min": 30,
                "link_tutorial": None,
                "ordem": 3,
            },
            {
                "titulo": "Rodar Suíte de Testes Unitários Locais",
                "periodo": PeriodoOnboarding.SEMANA_1,
                "tempo_estimado_min": 60,
                "link_tutorial": None,
                "ordem": 4,
            },
            {
                "titulo": "Primeiro Push & Pull Request de Teste em Staging",
                "periodo": PeriodoOnboarding.MES_1,
                "tempo_estimado_min": 90,
                "link_tutorial": None,
                "ordem": 5,
            },
        ]

        tarefas = []

        for dados in tarefas_dados:
            tarefa = obter_ou_criar_tarefa(
                db,
                trilha.id_trilha,
                dados,
            )

            tarefas.append(tarefa)

        # 5. Progresso das tarefas do novato

        status_iniciais = [
            StatusTarefa.CONCLUIDO,
            StatusTarefa.BLOQUEADO,
            StatusTarefa.PENDENTE,
            StatusTarefa.PENDENTE,
            StatusTarefa.PENDENTE,
        ]

        progressos = []

        for tarefa, status_inicial in zip(
            tarefas,
            status_iniciais,
        ):
            progresso = obter_ou_criar_progresso(
                db,
                lucas.id_usuario,
                tarefa,
                status_inicial,
            )

            progressos.append(progresso)

        # 6. Bloqueio de demonstração

        progresso_docker = progressos[1]

        if progresso_docker.status == StatusTarefa.BLOQUEADO:
            bloqueio_ativo = (
                db.query(Bloqueio)
                .filter(
                    Bloqueio.id_progresso
                    == progresso_docker.id_progresso,
                    Bloqueio.status_bloqueio
                    == StatusBloqueio.ATIVO,
                )
                .first()
            )

            if bloqueio_ativo is None:
                bloqueio = Bloqueio(
                    id_progresso=progresso_docker.id_progresso,
                    id_mentor=bruno.id_usuario,
                    log_erro=(
                        "Error response from daemon: "
                        "dial tcp: lookup registry-1.docker.io "
                        "on 127.0.0.53:53: i/o timeout.\n"
                        "Failed to pull image 'postgres:15-alpine'."
                    ),
                    status_bloqueio=StatusBloqueio.ATIVO,
                )

                db.add(bloqueio)
                db.flush()

                print("Bloqueio de demonstração criado.")

        db.commit()

        print("\nPovoamento concluído com sucesso.")

    except Exception:
        db.rollback()
        print("\nErro durante o povoamento. Transação revertida.")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    povoar_banco()
