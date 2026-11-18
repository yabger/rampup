from datetime import datetime 
from app.database import SessionLocal, engine, Base 
from app.models.user import Usuario, TipoPerfil 
from app.models.task import Trilha, Tarefa, ProgressoTarefa, PeriodoOnboarding, StatusTarefa 
from app.models.block import Bloqueio, StatusBloqueio, VinculoMentoria

def povoar_banco(): 
    # 1\. Garante a criação das tabelas no PostgreSQL se ainda não existirem 
    Base.metadata.create_all(bind=engine) 
    db = SessionLocal()

    try: 
        print("🌱 Iniciando povoamento do banco de dados PostgreSQL (RampUp)...")

        # Limpa dados anteriores para evitar duplicação em execuções repetidas 
        db.query(Bloqueio).delete() 
        db.query(VinculoMentoria).delete() 
        db.query(ProgressoTarefa).delete() 
        db.query(Tarefa).delete() 
        db.query(Trilha).delete() 
        db.query(Usuario).delete() 
        db.commit()

        # ------------------------------------------------------------- 
        # 2. POPULAR USUÁRIOS (PERSONAS DO ESBOÇO 2)
        # ------------------------------------------------------------- 

        lucas = Usuario( 
            nome="Lucas Rocha", 
            email="lucas.rocha@empresa.com", 
            senha_hash="123456", 
            tipo_perfil=TipoPerfil.NOVATO, 
            cargo="Dev Júnior" 
            )

        bruno = Usuario( 
            nome="Bruno Santos", 
            email="bruno.santos@empresa.com", 
            senha_hash="123456", 
            tipo_perfil=TipoPerfil.BUDDY, 
            cargo="Dev Sênior" 
            )
        
        mariana = Usuario(
            nome="Mariana Costa", 
            email="mariana.costa@empresa.com", 
            senha_hash="123456", 
            tipo_perfil=TipoPerfil.TECH_LEAD, 
            cargo="Gerente de Engenharia" 
            ) 
        
        db.add_all([lucas, bruno, mariana]) 
        db.commit() 
        db.refresh(lucas) 
        db.refresh(bruno) 
        print("✅ Usuários criados (Lucas Rocha, Bruno Santos, Mariana Costa).")

        # ------------------------------------------------------------- 
        # 3. POPULAR VÍNCULO DE MENTORIA 
        # ------------------------------------------------------------- 
        vinculo = VinculoMentoria( 
            id_novato=lucas.id_usuario, 
            id_mentor=bruno.id_usuario 
            ) 
        
        db.add(vinculo) 
        db.commit() 
        print("✅ Vínculo de mentoria estabelecido (Lucas -&gt; Bruno).") 
        
        # ------------------------------------------------------------- 
        # 4. POPULAR TRILHA E TAREFAS DE ONBOARDING 
        # ------------------------------------------------------------- 
        trilha_dev = Trilha( 
            titulo_trilha="Onboarding Engenharia de Software", 
            cargo_destino="Dev Júnior", 
            descricao="Checklist de configuração de ambiente e acessos para novos desenvolvedores." 
            ) 
        
        db.add(trilha_dev) 
        db.commit() 
        db.refresh(trilha_dev) 
        t1 = Tarefa( 
            id_trilha=trilha_dev.id_trilha, 
            titulo="Configurar Acessos e Credenciais (VPN, GitHub, Slack)", 
            periodo=PeriodoOnboarding.DIA_1, 
            tempo_estimado_min=30, 
            link_tutorial="[suspicious link removed]", 
            ordem=1 
            ) 
        t2 = Tarefa( 
            id_trilha=trilha_dev.id_trilha, 
            titulo="Instalar e Configurar Docker e Containers Locais", 
            periodo=PeriodoOnboarding.DIA_1, 
            tempo_estimado_min=45, 
            link_tutorial="[suspicious link removed]", 
            ordem=2 
            ) 
        t3 = Tarefa( 
            id_trilha=trilha_dev.id_trilha, 
            titulo="Clonar Repositório Principal e Instalar Dependências", 
            periodo=PeriodoOnboarding.DIA_2, 
            tempo_estimado_min=30, 
            link_tutorial="[suspicious link removed]", 
            ordem=3 
            ) 
        t4 = Tarefa( 
            id_trilha=trilha_dev.id_trilha, 
            titulo="Rodar Suíte de Testes Unitários Locais", 
            periodo=PeriodoOnboarding.SEMANA_1, 
            tempo_estimado_min=60, 
            link_tutorial="[suspicious link removed]", 
            ordem=4 ) 
        t5 = Tarefa( 
            id_trilha=trilha_dev.id_trilha, 
            titulo="Primeiro Push &amp; Pull Request de Teste em Staging", 
            periodo=PeriodoOnboarding.MÊS_1, 
            tempo_estimado_min=90, 
            link_tutorial="[suspicious link removed]", 
            ordem=5 ) 
        
        db.add_all([t1, t2, t3, t4, t5]) 
        db.commit() 
        db.refresh(t1) 
        db.refresh(t2) 
        db.refresh(t3) 
        db.refresh(t4) 
        db.refresh(t5) 
        print("✅ Trilha e 5 tarefas de onboarding criadas.") 

        # ------------------------------------------------------------- 
        # 5\. POPULAR PROGRESSO DAS TAREFAS DO NOVATO (LUCAS) 
        # ------------------------------------------------------------- 
        prog1 = ProgressoTarefa( 
            id_usuario=lucas.id_usuario, 
            id_tarefa=t1.id_tarefa, 
            status=StatusTarefa.CONCLUIDA, 
            data_conclusao=datetime.now() 
            ) 
        prog2 = ProgressoTarefa( 
            id_usuario=lucas.id_usuario, 
            id_tarefa=t2.id_tarefa, 
            status=StatusTarefa.TRAVADO # Tarefa travada com erro de Docker 
            ) 
        prog3 = ProgressoTarefa( 
            id_usuario=lucas.id_usuario, 
            id_tarefa=t3.id_tarefa, 
            status=StatusTarefa.PENDENTE 
            ) 
        prog4 = ProgressoTarefa( 
            id_usuario=lucas.id_usuario, 
            id_tarefa=t4.id_tarefa, 
            status=StatusTarefa.PENDENTE 
            ) 
        prog5 = ProgressoTarefa( 
            id_usuario=lucas.id_usuario, 
            id_tarefa=t5.id_tarefa, 
            status=StatusTarefa.PENDENTE 
            ) 
        db.add_all([prog1, prog2, prog3, prog4, prog5]) 
        db.commit() 
        db.refresh(prog2) 
        print("✅ Registros de progresso associados a Lucas Rocha.") 

        # ------------------------------------------------------------- 
        # 6\. POPULAR REGISTRO DE BLOQUEIO ("ESTOU TRAVADO") 
        # ------------------------------------------------------------- 
        bloqueio_docker = Bloqueio( 
            id_progresso=prog2.id_progresso, 
            id_mentor=bruno.id_usuario, 
            log_erro=( 
                "Error response from daemon: Get [suspicious link removed]" 
                "dial tcp: lookup registry-1.docker.io on 127.0.0.53:53: i/o timeout.\n" 
                "Failed to pull image 'postgres:15-alpine'." 
                ), 
                status_bloqueio=StatusBloqueio.ATIVO 
            ) 
        db.add(bloqueio_docker) 
        db.commit() 
        print("✅ Alerta de bloqueio ativo inserido para a fila do mentor Bruno Santos.") 

        print("\n🚀 Povoamento concluído com sucesso!") 

    except Exception as e: 
        db.rollback() 
        print(f"❌ Erro ao povoar banco de dados: {e}") 

    finally: 
        db.close() 

    if __name__ == "__main__": 
        povoar_banco()