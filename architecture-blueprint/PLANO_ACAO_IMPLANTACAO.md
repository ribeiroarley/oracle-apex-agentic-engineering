# Plano de Acao e Roteiro de Implantacao Corporativa

Roteiro pratico de consultoria tecnica e governanca para adocao da **Esteira DevSecOps Agentica para Oracle e APEX** em ambientes corporativos criticos (indústrias, operacoes financeiras e varejo de grande escala).

Este plano detalha o cronograma de 8 semanas estruturado em 4 fases sequenciais, os entregaveis tecnicos, a matriz de responsabilidades e os pre-requisitos de infraestrutura.

---

## 1. Cronograma Executivo de 8 Semanas

```
+---------------------------------------------------------------------------------------------------------+
|                                FASES DO PROJETO DE IMPLANTACAO (8 SEMANAS)                              |
+--------------------------+--------------------------+--------------------------+------------------------+
| SEMANAS 1-2              | SEMANAS 3-4              | SEMANAS 5-6              | SEMANAS 7-8+           |
| FASE 1: SEGURANCA        | FASE 2: HARNESS          | FASE 3: GITOPS           | FASE 4: OPERACAO       |
+--------------------------+--------------------------+--------------------------+------------------------+
| - Topologia & Firewalls  | - Catalogo Master Index  | - Baseline do Schema     | - Operacao Assistida   |
| - Usuario MCP_AGENT_RO   | - Skills Corporativas    | - Master Controller XML  | - Coleta de KPIs       |
| - Trigger de Auditoria   | - Tool Call Offloading   | - Pipeline CI/CD         | - Treinamento Equipe   |
| - Homologacao do SQLcl   | - Protecao de Contexto   | - Validacao de Rollbacks | - Handover Tecnico     |
+--------------------------+--------------------------+--------------------------+------------------------+
```

---

## 2. Detalhamento das Fases

### Fase 1: Descoberta, Seguranca e Governanca (Semanas 1 e 2)

**Objetivo:** Estabelecer a conectividade segura e criar a infraestrutura de usuarios minimamente privilegiados e auditados, garantindo conformidade com a politica de seguranca do cliente (CISO).

#### Atividades da Fase 1:
1. **Mapeamento de Topologia e Conectividade:**
   - Levantamento de redes, sub-redes, rotas de VPN e portas de comunicacao (porta TCP 1521 padrao ou porta segura TCPS 2484).
   - Validacao de que o acesso direto a producao permanece estritamente bloqueado para estacoes de trabalho.
2. **Criacao do Usuario Read-Only de IA (`MCP_AGENT_RO`):**
   - Criacao do usuario dedicado nos ambientes de Desenvolvimento e Homologacao (UAT).
   - Aplicacao da restricao `QUOTA 0M ON USERS` (garantia de que a conta nunca podera criar segmentos de dados ou gravar informacoes).
   - Concessao estrita de privilegios de leitura no dicionario (`SELECT ANY DICTIONARY`) e views dinamicas de performance (`sys.v_$sql`, `sys.v_$sql_plan`, `sys.v_$session`).
   - Geracao automatica de sinônimos privados para as tabelas de negocio relevantes, eliminando a exposicao e necessidade de qualificacao por schema.
3. **Implantacao da Auditoria de Sessoes Agenticas:**
   - Criacao da tabela corporativa `SYSTEM.ADMIN_AUDIT_MCP_SESSIONS`.
   - Ativacao da trigger de banco de dados `AFTER LOGON` (`TRG_AUDIT_MCP_AGENT_LOGON`), registrando `OS_USER`, `MODULE`, `MACHINE`, `IP_ADDRESS` e timestamp de cada conexao aberta pelo agente de IA.
4. **Homologacao do Oracle SQLcl em Modo MCP:**
   - Validacao da instalacao do Java 17+/21+ e do Oracle SQLcl 24.3+ nas estacoes de trabalho dos desenvolvedores/DBAs.
   - Configuracao da conexao nomeada segura no SQLcl (`conn -save mcp_lab -savepwd ...`), eliminando credenciais em texto puro em arquivos de configuracao JSON.
   - Registro do servidor MCP nos clientes locais (VS Code, Claude Desktop, Cursor).

#### Entregaveis da Fase 1:
- Relatorio de Conformidade de Seguranca e Menor Privilegio assinado pelo DBA responsavel.
- Scripts SQL de provisionamento auditados e versionados (`01_setup_governance.sql`).
- Estacoes de trabalho dos engenheiros devidamente conectadas ao SQLcl MCP Server.

---

### Fase 2: Engenharia de Harness e Padroes Internos (Semanas 3 e 4)

**Objetivo:** Projetar o arcabouço de contencao (*harness*) da Inteligencia Artificial para garantir conformidade arquitetural, evitar alucinacoes e mitigar a saturacao de tokens (*Context Rot*).

#### Atividades da Fase 2:
1. **Estruturacao do Catalogo de Progressive Disclosure:**
   - Criacao do catalogo mestre `skills/MASTER_INDEX.md`, listando apenas o nome, gatilho de ativacao e arquivo de cada habilidade corporativa, consumindo menos de 300 tokens na inicializacao.
2. **Desenvolvimento e Calibracao das Skills Corporativas:**
   - **Skill de Nomenclatura e Padroes:** Forca o cumprimento das convencoes corporativas de nomes de tabelas, colunas, sequences, packages e indices (`IDX_<TABELA>_<COLUNA>`).
   - **Skill de Diagnostico CBO e Performance:** Instrucao declarativa instruindo o modelo a inspecionar planos reais na `V$SQL_PLAN` e cardinalidade na `ALL_TAB_COL_STATISTICS` antes de sugerir qualquer DDL.
   - **Skill de Seguranca PL/SQL:** Verificacao obrigatoria de injecao de SQL dinamico (`DBMS_ASSERT`, uso de bind variables) e respeito a privilegios definidos (`AUTHID CURRENT_USER` vs. `AUTHID DEFINER`).
3. **Implantacao do Tool Call Offloading:**
   - Configuracao do utilitário CLI em Python (`tools/offload_query.py`) integrado a biblioteca `oracledb` em modo thin.
   - Definicao da regra de interceptacao: consultas retornando mais de 1.500 tokens sao automaticamente gravadas no disco local da estacao de trabalho (`offload_cache/dump_*.json`), devolvendo ao agente de IA apenas um resumo estruturado e uma amostra de 5 linhas.
   - Validacao de reducao de ~98% no consumo de tokens da janela de contexto.

#### Entregaveis da Fase 2:
- Diretorio corporativo `skills/` contendo `MASTER_INDEX.md` e as skills homologadas pela lideranca tecnica.
- Utilitario de Tool Call Offloading homologado nas estacoes de trabalho.
- Guia pratico de operacao dos agentes de IA com Progressive Disclosure.

---

### Fase 3: Versionamento Schema-as-Code e GitOps (Semanas 5 e 6)

**Objetivo:** Eliminar scripts SQL manuais de deploy, estabelecendo um fluxo deterministico de versionamento de banco com SQLcl Liquibase integrado a esteiras de CI/CD.

#### Atividades da Fase 3:
1. **Captura da Baseline Declarativa do Schema:**
   - Execucao do comando nativo `lb generate-schema` conectado com credencial administrativa (`HR_ADMIN`) no ambiente de homologacao.
   - Geracao do snapshot inicial de tabelas, sequences, constraints e indices em XML declarativo, organizado sob o diretorio `changelog/baseline/`.
   - Execucao de `lb changelog-sync` para registrar os objetos pre-existentes na tabela de controle `DATABASECHANGELOG` sem recria-los.
2. **Estruturacao do Master Controller e Politica de Changesets:**
   - Criacao do arquivo mestre `changelog/controller.xml` orquestrando a baseline e os changesets incrementais.
   - Regra corporativa obrigatoria: **nenhum changeset e aprovado sem o bloco `<rollback>` devidamente preenchido e testado**.
3. **Fluxo de Trabalho com Git Worktrees:**
   - Capacitacao dos desenvolvedores e DBAs para utilizacao de Git Worktrees (`git worktree add ../feature-tuning`), viabilizando a criacao e teste de migrações em paralelo sem alternancia arriscada de branch no mesmo diretorio.
4. **Configuracao da Esteira Automatizada de CI/CD:**
   - Criacao de pipeline no GitLab CI, GitHub Actions ou Azure DevOps.
   - Configuracao dos estagios:
     - **Estagio 1 (Lint & Validacao):** Verificacao sintatica do XML e garantia de presenca da tag de rollback.
     - **Estagio 2 (Deploy em Homologacao):** Execucao de `lb update -changelog-file controller.xml` via runner isolado.
     - **Estagio 3 (Validacao e Teste Regressivo):** Validacao de sucesso e teste automatizado de rollback em schema de teste.
     - **Estagio 4 (Gate de Producao):** Aprovacao formal (CAB) e execucao programada em producao durante a janela autorizada.

#### Entregaveis da Fase 3:
- Repositorio Git contendo a baseline declarativa e o Master Controller Liquibase.
- Pipeline de CI/CD funcional com deploys automatizados em homologacao e portoes de qualidade.
- Politica formal de aprovacao de Pull Requests para alteracoes de banco de dados.

---

### Fase 4: Operacao Assistida, KPIs e Handover (Semanas 7 e 8+)

**Objetivo:** Acompanhar a operacao da esteira em sprints reais, validar os indicadores de sucesso (KPIs) e transferir a autonomia para a equipe interna do cliente.

#### Atividades da Fase 4:
1. **Operacao Assistida (Hypercare):**
   - Acompanhamento conjunto de 2 a 3 ciclos completos de mudanca de schema gerados pelo time de desenvolvimento APEX e validados pelo time de DBA interno.
   - Refinamento de prompts, calibracao de skills e ajustes finos de thresholds de offloading.
2. **Coleta e Consolidacao de Metricas (KPIs):**
   - Comparativo do tempo medio de analise e implementacao de melhorias antes vs. depois da adocao da esteira.
3. **Treinamento e Capacitacao da Equipe:**
   - Workshop pratico para a equipe de desenvolvimento APEX (operacao com VS Code, acionamento das skills e boas praticas de static IDs).
   - Workshop pratico para a equipe de DBAs (governanca de branches, revisao de Pull Requests de changelogs Liquibase e auditoria de sessoes MCP).
4. **Handover Tecnico Formal:**
   - Entrega da documentacao completa de arquitetura, guias de solucao de problemas (*troubleshooting*) e termo de encerramento do projeto.

#### Entregaveis da Fase 4:
- Relatorio Executivo de KPIs com comparativo antes/depois.
- Manual de Operacao e Governanca da Esteira DevSecOps Agentica.
- Termo de Handover e conclusao da consultoria.

---

## 3. Matriz de Responsabilidades (RACI)

Legenda: **R** = Responsavel pela Execucao | **A** = Aprovador Final | **C** = Consultado | **I** = Informado

| Atividade do Projeto | Consultor / Arquiteto DevSecOps | DBA Interno do Cliente | Desenvolvedor APEX / Tech Lead | Gerente de TI / CISO |
| :--- | :---: | :---: | :---: | :---: |
| Definicao da Topologia de Rede e Portas de Firewall | **R** | **C** | **I** | **A** |
| Criacao do usuario `MCP_AGENT_RO` e Trigger de Auditoria | **C** | **R** | **I** | **A** |
| Configuracao do SQLcl MCP nas Estacoes de Trabalho | **R** | **C** | **R** | **I** |
| Elaboracao do `MASTER_INDEX.md` e das Skills Declarativas | **R** | **C** | **C** | **I** |
| Implantacao do Utilitario de Tool Call Offloading | **R** | **I** | **R** | **I** |
| Extracao da Baseline Inicial do Schema (`lb generate-schema`) | **R** | **A** | **I** | **I** |
| Criacao de Changesets Incrementais e Blocos de Rollback | **C** | **C** | **R** | **I** |
| Revisao e Aprovacao de Pull Requests de Banco de Dados | **C** | **A** | **R** | **I** |
| Configuracao do Pipeline de CI/CD (GitLab / GitHub / Azure) | **R** | **C** | **C** | **A** |
| Execucao de Deploys em Homologacao e Producao via CI/CD | **C** | **A** | **I** | **I** |
| Acompanhamento de KPIs e Treinamento da Equipe | **R** | **R** | **R** | **A** |

---

## 4. Pre-requisitos Tecnicos e de Acesso

Para o inicio imediato da Fase 1, o cliente corporativo deve assegurar os seguintes requisitos:

### 4.1. Conectividade e Redes
- **Acesso das Estacoes de Engenharia aos Ambientes de Desenvolvimento/UAT:** Porta TCP 1521 (SQL*Net padrao) ou TCPS 2484 (com certificado SSL/TLS) liberada via VPN corporativa.
- **Acesso a Producao:** Estritamente bloqueado para estacoes de trabalho; permitido apenas a partir da sub-rede dos Runners de CI/CD.
- **Servidor Git Corporativo:** Acesso HTTP/HTTPS (443) ou SSH (22) aos repositorios do GitHub Enterprise, GitLab ou Azure Repos.

### 4.2. Infraestrutura de Software
- **Servidor de Banco de Dados:** Oracle Database 19c (Enterprise / Standard) ou Oracle Database 23ai (Free / Enterprise), operando on-premises, RAC ou Exadata (Cloud@Customer / OCI).
- **Runners de CI/CD:** Servidor Linux/Windows dedicado com:
  - Java Runtime Environment (JRE/JDK) versao 17 ou 21 instalada em `PATH`.
  - Oracle SQLcl versao 24.3 ou superior instalado e acessivel via comando `sql`.
  - Cliente Git versao 2.40 ou superior.
- **Estacoes de Trabalho dos Desenvolvedores/DBAs:**
  - Sistema Operacional: Windows 10/11, macOS ou Linux.
  - Visual Studio Code instalado com extensao de cliente MCP ou cliente desktop equivalente.
  - Python 3.10 ou superior com bibliotecas `oracledb` e `python-dotenv`.

### 4.3. Credenciais Administrativas do Cliente
- Acesso administrativo temporario (`SYS` ou `SYSTEM`) em ambiente de Desenvolvimento/UAT para que o DBA interno execute os scripts de governanca e crie as contas de servico.
- Concessao de privilegio `CREATE TRIGGER` e `SELECT ANY DICTIONARY` para as contas administrativas e de auditoria estabelecidas no projeto.
