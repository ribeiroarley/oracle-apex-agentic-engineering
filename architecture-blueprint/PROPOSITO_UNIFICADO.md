# Arquitetura de Referencia: Proposito Unificado da Esteira DevSecOps Agentica para Oracle

Documento executivo e tecnico consolidando a visao estrategica, a topologia de implantacao corporativa e o valor de negocio gerado pela integracao dos tres pilares de engenharia deste repositorio:
- [Laboratorio 01: Governanca e Seguranca com Oracle SQLcl MCP Server](../lab-01-sqlcl-mcp/README.md)
- [Laboratorio 02: Harness Engineering, Progressive Disclosure e Tool Call Offloading](../lab-02-harness-engineering/README.md)
- [Laboratorio 03: GitOps Declarativo com SQLcl Liquibase e Git Worktrees](../lab-03-gitops-liquibase/README.md)

---

## 1. Visao Estrategica: A Esteira DevSecOps Agentica

O desenvolvimento e manutencao de sistemas corporativos criticos sobre Oracle Database, Oracle Exadata e Oracle APEX historicamente enfrentam tres gargalos estruturais:

1. **Vulnerabilidade de Acesso e Falta de Governanca:** O uso de contas com privilegios elevados (`SYS`, `SYSTEM` ou o proprio dono do schema da aplicacao) para consultas exploratorias e intervencoes de suporte, sem rastreabilidade de quem ou qual processo executou a acao.
2. **Degradacao de Contexto e Alucinacao de IA (Context Rot):** A tentativa de utilizar assistentes de inteligencia artificial sem mecanismos de contencao (*harness*), expondo modelos a volumes massivos de dados brutos que saturam a janela de contexto, elevam custos de tokens e induzem a diagnosticos errôneos.
3. **Deploy Manual e Falta de Rastreabilidade de Schema:** A promocao de alteracoes de banco de dados via scripts SQL soltos executados manualmente na madrugada via SQL*Plus, sem controle deterministico de versao, sem esteira automatizada e sem mecanismo de reversao (*rollback*) testado previamente.

A solucao arquitetural implementada neste repositorio unifica esses tres pilares em uma unica **Esteira DevSecOps Agentica para Oracle**:

```
+---------------------------------------------------------------------------------------------------------+
|                                  ESTEIRA DEVSECOPS AGENTICA PARA ORACLE                                 |
+------------------------------------+-----------------------------------+--------------------------------+
|       PILAR 1: GOVERNANCA          |        PILAR 2: HARNESS           |       PILAR 3: GITOPS          |
|    (Seguranca & Protocolo)         |   (Eficiencia & Contencao)        |     (Entrega & Reversao)       |
+------------------------------------+-----------------------------------+--------------------------------+
| - Oracle SQLcl em modo MCP         | - Progressive Disclosure          | - Schema-as-Code Declarativo   |
| - Usuario Read-Only (QUOTA 0M)     | - Catalogo Master Index           | - SQLcl Liquibase Nativo       |
| - Dicionario restrito              | - Skills especializadas por papel | - Master Controller Versionado |
| - Trigger de Auditoria AFTER LOGON | - Tool Call Offloading em disco   | - Changesets com Rollback      |
| - Rastreamento de sessao de IA     | - Reducao de ~98% de tokens       | - Git Worktrees paralelos      |
+------------------------------------+-----------------------------------+--------------------------------+
```

---

## 2. Topologia de Implantacao Corporativa Real

Um dos principios mais criticos para a aprovacao deste modelo em auditorias de Seguranca da Informacao (CISO) e equipes corporativas de Administracao de Banco de Dados (DBA) e a **segregacao fisica e logica dos componentes de automacao**:

### Premissa Mandatoria: Zero Agentes no Servidor de Banco de Dados

**Nenhum componente de Inteligencia Artificial, interpretador Python, runtime Node.js ou binario do Git e instalado ou executado dentro do servidor de banco de dados do cliente (seja Oracle Database em Linux, Oracle RAC on-premises ou Oracle Exadata Cloud@Customer / OCI).**

O servidor de banco de dados corporativo permanece 100% isolado, operando exclusivamente com sua pilha nativa de servicos Oracle. Toda a interacao com o banco de dados ocorre estritamente por meio de conexoes de rede padrao **SQL*Net (porta TCP 1521 ou porta segura TCPS 2484)**, utilizando contas de servico minimamente privilegiadas e chanceladas pela governanca interna.

### Camadas da Topologia Corporativa

A esteira e distribuida em quatro camadas de isolamento rigoroso:

1. **Camada 1: Estacao de Trabalho do Engenheiro / DBA (Client-Side):**
   - Ambiente local do desenvolvedor ou Workstation corporativa em nuvem.
   - Ferramentas: Visual Studio Code, Oracle SQLcl configurado em modo MCP (`sql -mcp -name mcp_hr_lab`), catalogo declarativo de habilidades (`MASTER_INDEX.md`) e scripts de apoio (como o CLI de Tool Call Offloading).
   - O agente de IA opera como assistente na estacao do profissional, emitindo comandos via MCP stdio para o SQLcl local, que por sua vez se conecta ao banco de homologacao/desenvolvimento via SQL*Net com usuario read-only.

2. **Camada 2: Repositorio Central de Codigo (Versionamento & Colaboracao):**
   - Servidor Git corporativo (GitLab, GitHub Enterprise ou Azure DevOps).
   - Armazena a definicao declarativa da aplicacao APEX e o historico completo de migracao de schema do banco de dados (`changelog/controller.xml`, baselines e changesets Liquibase).
   - Politicas obrigatorias de protecao de branch (`main` protegida, exigencia de Pull Request, revisao por pares e aprovacao formal de DBA).

3. **Camada 3: Servidor de CI/CD (Pipeline Automatizado):**
   - Runners ou agentes de integracao continua (GitLab Runner, GitHub Actions Self-Hosted Runner, Jenkins ou OCI DevOps).
   - Equipados exclusivamente com Java 17+, Oracle SQLcl headless e cliente Git.
   - Responsavel por executar a validacao sintatica, testes unitarios, verificacao de integridade e o comando `lb update` para aplicacao dos changesets nos ambientes alvo.

4. **Camada 4: Infraestrutura de Banco de Dados (Ambientes Segregados):**
   - Instancias Oracle Database 23ai / 19c ou Oracle Exadata.
   - **Ambiente de Desenvolvimento / Homologacao:** Conexao read-only aberta para a estacao de engenharia via usuario `MCP_AGENT_RO` (com trigger de auditoria ativo) e conexao administrativa restrita ao runner de CI/CD para deploy via Liquibase.
   - **Ambiente de Producao:** Acesso de rede bloqueado para estacoes de trabalho. Conexoes DDL/migracao permitidas exclusivamente a partir do IP fixo do Runner de CI/CD durante janelas de manutencao automatizadas.

---

## 3. Diagrama de Fluxo e Topologia End-to-End

```
+----------------------------------------------------------------------------------------------------------------+
| ESTACAO DO ENGENHEIRO / DBA (Client-Side / VPN)                                                                |
|                                                                                                                |
|  +--------------------+       MCP (stdio)       +----------------------+                                       |
|  | VS Code / AI Agent | <---------------------> | Oracle SQLcl (v24.3) |                                       |
|  | + Harness Skills   |                         | -mcp -name mcp_ro    |                                       |
|  +---------+----------+                         +----------+-----------+                                       |
|            |                                               |                                                   |
|            | 1. Git Commit & Push (Branch / Worktree)      | 0. Inspecao Read-Only (SQL*Net TCP 1521)          |
|            v                                               |    Usuario: MCP_AGENT_RO (QUOTA 0M)               |
+------------|-----------------------------------------------|---------------------------------------------------+
             |                                               |
             |                                               |  (Acesso direto permitido apenas
             |                                               |   em Desenvolvimento / Homologacao)
             v                                               v
+----------------------------+             +---------------------------------------------------------------------+
| SERVIDOR GIT CORPORATIVO   |             | AMBIENTE DE HOMOLOGACAO / UAT (Oracle Database / Exadata)           |
| (GitHub / GitLab / Azure)  |             |                                                                     |
|                            |             |  - Schema da Aplicacao (Tabelas, Views, Packages)                   |
|  - Branch de Feature       |             |  - Usuario MCP_AGENT_RO (Auditado via TRG_AUDIT_MCP_AGENT_LOGON)   |
|  - Pull Request aberto     |             |  - Tabelas de Controle: DATABASECHANGELOG / DATABASECHANGELOGLOCK  |
|  - Code Review Aprovado    |             +----------------------------------^----------------------------------+
+------------+---------------+                                                |
             |                                                                |
             | 2. Webhook / Disparo de Pipeline                               | 3. Deploy de Teste
             v                                                                |    (lb update -changelog-file)
+------------------------------------------------------------+                |    Usuario CI/CD: HR_ADMIN
| RUNNER DE CI/CD (Servidor de Automacao Isolado)            |                |
|                                                            |                |
|  - Java 17+ / 21+ instalado                                |----------------+
|  - Oracle SQLcl Headless em PATH                           |
|  - Valida changesets e blocos de rollback                  |----------------+
|  - Executa testes de migracao automatizados                |                |
+------------------------------------------------------------+                |
                                                                              | 4. Promocao para Producao
                                                                              |    (Apos Aprovacao Formal CAB)
                                                                              |    (lb update -changelog-file)
                                                                              |    Usuario CI/CD: HR_ADMIN
                                                                              v
                                           +---------------------------------------------------------------------+
                                           | AMBIENTE DE PRODUCAO (Oracle Database / Exadata Cluster)            |
                                           |                                                                     |
                                           |  - Schema de Producao Atualizado Deterministicamente                |
                                           |  - Auditoria Corporativa Gravada em DATABASECHANGELOG               |
                                           |  - ZERO componentes externos instalados no SO ou no Oracle          |
                                           |  - Acesso de rede restrito ao IP do Runner de CI/CD                 |
                                           +---------------------------------------------------------------------+
```

---

## 4. Estudo de Caso Pratico: Industria de Manufatura de Calcados de Alto Volume

Para tangibilizar o impacto de negocio e a viabilidade operacional da esteira, consideramos o caso de uma **grande industria calçadista brasileira**, cuja operacao fabril depende criticamente de um cluster **Oracle Database / Exadata** com aplicacoes operadas via **Oracle APEX**:
- **Volume:** Mais de 120.000 pares de calcados produzidos/dia, 8 plantas fabris interligadas.
- **Sistemas em APEX:** Gestao de Ordens de Producao (OPs), Apontamento de Materiais no Chao de Fabrica, Controle de Expedicao/Estoque e Faturamento Fiscal em tempo real.
- **Criticidade:** Qualquer indisponibilidade ou travamento de queries no apontamento de esteiras paralisa linhas de montagem, gerando perdas estimadas em milhares de reais por hora parada.

### O Contraste de Paradigmas: Tradicional vs. Esteira DevSecOps Agentica

| Dimensao de Analise | Fluxo Tradicional (Legado / Manual) | Fluxo Moderno (Esteira DevSecOps Agentica) |
| :--- | :--- | :--- |
| **Diagnostico de Gargalos** | Reativo: O chão de fábrica trava; o operador abre chamado; o DBA entra via terminal de producao usando `SYSTEM`, busca queries no cursor cache e tenta entender o problema sob pressao. | Proativo e Governado: O agente de IA aciona a skill declarativa (`SKILL_DBA_TUNING_AUDIT.md`), conecta via MCP em homologacao ou replica read-only, inspeciona `V$SQL_PLAN` e cardinalidade sem risco de alteracao. |
| **Consumo de Contexto de IA** | Descontrolado: Consultas de analise retornam 50.000 linhas de logs para a janela do LLM, causando estouro de tokens, respostas lentas e alucinacoes tecnicas (*Context Rot*). | Otimizado via Offloading: Consultas volumosas sao desviadas para disco local via `tools/offload_query.py`. O agente consome apenas o sumario (~300 tokens), economizando mais de 95% da janela. |
| **Proposta de Solucao (DDL)** | Empirica: O DBA cria indices diretamente em producao durante o expediente sem testar impacto em escrita (`INSERT`/`UPDATE`), gerando locks de tabela e lentidao paralela. | Padronizada e Declarativa: O agente gera o DDL seguindo regras rigidas de nomenclatura (`IDX_<TABELA>_<COLUNA>`) e obrigatoriamente gera o script de reversao (`DROP INDEX`). |
| **Versionamento no Git** | Nulo ou Fragmentado: Scripts `.sql` salvos em pastas compartilhadas de rede ou tickets do Jira. Nao ha rastreabilidade de versao nem histórico de mudancas do schema. | Determinismo Schema-as-Code: O DDL e versionado em XML Liquibase (`v1.1.0-tuning-indexes.xml`) e registrado no Master Controller (`controller.xml`) via Pull Request. |
| **Ambiente de Trabalho** | Conflitante: Desenvolvedores APEX e DBAs alteram o mesmo ambiente de desenvolvimento compartilhado, gerando sobrescritas acidentais de pacotes e triggers. | Paralelo via Git Worktrees: Desenvolvedores trabalham em worktrees isoladas (`git worktree add ../feature-tuning`), validando alteracoes sem interferir na branch principal. |
| **Promocao para Producao** | Manual e Arriscada: Execucao manual de scripts SQL na madrugada via SQL*Plus por um operador de plantao. Em caso de erro, nao ha script de rollback testado. | Automatizada via CI/CD: Pipeline de CI/CD executa `lb update`. O Liquibase verifica hashes MD5 de cada changeset; se houver falha, aciona automaticamente o bloco `<rollback>`. |
| **Auditoria e Compliance** | Fragil: Dificuldade em comprovar para auditorias externas (SOX, ISO 27001, LGPD) quem solicitou, quem aprovou e quando uma alteracao de schema foi aplicada. | Total e Rastreavel: Registro imutavel na tabela corporativa `DATABASECHANGELOG` contendo autor, data/hora, identificador da mudanca e hash MD5 de execucao. |

---

## 5. Sintese de Valor para Liderancas de TI e Negocio

1. **Reducao Drastica de Downtime e Incidentes:** Eliminacao de paradas fabris decorrentes de scripts de migracao incompletos ou aplicados em ordem incorreta.
2. **Conformidade e Seguranca Chanceladas:** Aprovacao imediata em comites de seguranca corporativa, pois a IA nunca toca dados produtivos diretamente e o banco nao hospeda nenhum runtime externo.
3. **Produtividade com Governanca:** O time de banco e aplicacoes multiplica sua capacidade de diagnostico e tuning sem abrir mao de revisoes de codigo rigorosas (*Pull Requests* com presenca do DBA).
4. **Independencia de Ferramental Proprietario:** Construido sobre padroes abertos e ferramentas oficiais da Oracle (SQLcl e Liquibase), garantindo longevidade e suporte oficial.
