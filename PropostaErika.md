O **RampUp** é projetado em uma arquitetura desacoplada em camadas, combinando um frontend reativo com um backend orientado a serviços que consome e fornece dados via **API REST em formato JSON**  (isso está na primeira entrega)

## **Módulos:**
1. Módulo 1: Gestão de Perfis e Autenticação
2. Módulo 2: Trilha Interativa de Onboarding
3. Módulo 3: Motor de Gestão de Bloqueios ("Estou Travado")
4. Módulo 4: Painel do Mentor (Visão do Buddy)
5. Módulo 5: Módulo Analítico e de Qualidade (BI / Métricas)

# PROPOSTA PARA DESENVOLVIMENTO DO PROJETO  
* **Jornada Selecionada:** **"Do Ponto de Bloqueio à Resolução com o Mentor"** (Cruzamento entre a visão do novato **Lucas Rocha** e a do mentor **Bruno Santos**).
* **Justificativa:** Esta é a jornada central e de maior valor técnico do RampUp, onde ocorre a sinalização ativa via botão **"Estou Travado"** e a destravação pelo mentor.
* **Fluxo UX Passo a Passo para a PoC:**
1. **Início e Consulta da Trilha:** Lucas acessa o sistema e visualiza a lista de cards de configuração (ex: *"1\. Configurar Docker"*, *"2\. Clonar Repositório"*).
2. **Acionamento do Bloqueio:** Ao encontrar uma falha de permissão na tarefa 2, Lucas clica em **"Estou Travado"**, cola o log/stacktrace do erro em um pop-up e envia.
3. **Mudança Visual de Estado:** O card da tarefa altera seu status e ganha destaque visual amarelo/vermelho no painel.
4. **Atuação do Mentor (Buddy):** Bruno acessa o **Painel do Mentor**, identifica o alerta em destaque com o log exato do erro e auxilia Lucas a resolver a pendência.
5. **Resolução e Avanço:** Bruno clica em **"Destravar/Resolver"**. A barra de progresso de Lucas atualiza (ex: de 20% para 40%) e libera a próxima etapa.

### Preparação do Ambiente: Stack Tecnológica e Infraestrutura
Para atender ao requisito de **Sistema Web Modularizável baseado em camadas e APIs REST**, a stack tecnológica proposta é:

* **Frontend (Interface Web Responsiva):**
  * **Tecnologia:** React.js (ou HTML5/CSS3/JavaScript ES6+ com Bootstrap).
  * **Função:** Criar uma Single Page Application (SPA) responsiva para desktop e dispositivos móveis.
* **Backend (API REST & Regras de Negócio):**
  * **Tecnologia:** Node.js com Express.
  * **Função:** Fornecer rotas REST em formato JSON e documentação Swagger/OpenAPI automatizada (`/docs`).
* **Banco de Dados (Persistência):**
  * **Tecnologia:** PostgreSQL (para desenvolvimento e execução rápida da PoC).
* **Repositório & Versionamento (Exigência do PI IV):**
  * **Repositório GitHub** estruturado com as pastas `/frontend`, `/backend`, arquivo `docker-compose.yml` e `README.md` com instruções de instalação.
* **Infraestrutura e Hospedagem (PoC):**
  * **Frontend:** Netlify.
  * **Backend:** execução em ambiente local via Docker

### Construção da Interface do Usuário (UI) e Implementação do UX
A PoC focará no desenvolvimento de **três telas essenciais**:

1. **Tela 1 – Dashboard do Novato (Visão de Lucas):**
  * Cabeçalho contendo a barra de progresso geral em porcentagem (%).
  * Lista de cards de tarefas organizados cronologicamente com marcadores de status (`PENDENTE`, `CONCLUIDO`, `TRAVADO`).
  * Ações por card: Botões **"Concluir"** e \*\*"Estou Travado"\*\*.
2. **Tela 2 – Modal Pop-up "Estou Travado":**
  * Formulário simples com campo de texto (`textarea`) para inserção do log de erro.
  * Botão de confirmação de envio que dispara uma requisição `POST` para o backend.
3. **Tela 3 – Painel do Mentor / Buddy (Visão de Bruno):**
  * Grid com novatos acompanhados e suas porcentagens de conclusão.
  * Alertas em vermelho exibindo o log do erro colado pelo novato.
  * Botão **"Destravar/Resolver"** que dispara uma requisição `PUT` para a API REST

### Desenvolvimento Backend: Lógica, Dados, APIs e Repositório
  * Modelagem de Dados (Esquema Relacional)
Para sustentar a modularidade do *RampUp*, o modelo relacional proposto mapeia as entidades principais, chaves primárias (PK), chaves estrangeiras (FK) e os relacionamentos do sistema:  
**USUARIOS** *(Cadastro de colaboradores e perfis)* --> **TRILHAS** *(Conjunto de checklists de integração por cargo)* <-- **TAREFAS** *(Passos individuais da configuração técnica)* --> **PROGRESSO\_TAREFA** *(Status de cada tarefa por novato)* --> **BLOQUEIOS** *(Registros do botão "Estou Travado")* --> **VINCULO\_MENTORIA** *(Associação entre Novato e Mentor/Buddy)* --> **USUARIOS**  
