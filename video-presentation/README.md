# Apresentacoes Tecnicas em Video: Engenharia Agentica Governada para Oracle

Diretorio responsavel pela geracao 100% automatizada de dois videos tecnicos em alta definicao (Full HD 1920x1080, MP4, taxa de 60 fps / still image otimizada, narracao neural em portugues brasileiro com normalizacao fonetica).

Os videos cobrem de ponta a ponta a esteira de engenharia agentica, os tres laboratorios praticos implementados no repositorio e a arquitetura corporativa para bancos de dados de missao critica (Oracle Database 23ai e Oracle Exadata).

---

## 1. Producoes Disponiveis

| Video | Arquivo de Saida | Roteiro Tecnico | Cenas | Foco Principal |
| :--- | :--- | :--- | :---: | :--- |
| **Video 01** | `video-presentation/output/palestra_01_visao_executiva_e_arquitetura.mp4` | [`ROTEIRO_VIDEO_01_ARQUITETURA.md`](ROTEIRO_VIDEO_01_ARQUITETURA.md) | 12 | Visao executiva, problema do LLM puro, Harness Engineering, governanca dos 3 laboratorios e topologia Exadata com zero agentes no servidor. |
| **Video 02** | `video-presentation/output/palestra_02_implementacao_passo_a_passo.mp4` | [`ROTEIRO_VIDEO_02_IMPLEMENTACAO.md`](ROTEIRO_VIDEO_02_IMPLEMENTACAO.md) | 12 | Guia hands-on passo a passo: Docker Compose, SQLcl MCP, conexao nomeada, `.vscode/mcp.json`, skills progressivas, offloading Python, Liquibase e Git Worktrees. |

---

## 2. Arquitetura da Pipeline de Renderizacao

O processo de construcao dos videos e 100% programatico e reprodutivel em Python, sem dependencia de softwares proprietarios de edicao ou servicos pagos de terceiros:

```text
+---------------------------------------------------------------------------------------------------------+
|                                  PIPELINE DE CONSTRUCAO DOS VIDEOS (PYTHON)                             |
+--------------------------+--------------------------+---------------------------------------------------+
| ETAPA 1: NARRACAO        | ETAPA 2: SLIDES FULL HD  | ETAPA 3: MONTAGEM E CONCATENACAO                  |
| (Edge-TTS Neural)        | (Playwright Headless)    | (FFmpeg H.264 / AAC)                              |
+--------------------------+--------------------------+---------------------------------------------------+
| - Voz: pt-BR-Antonio     | - Viewport: 1920x1080    | - Leitura de duracao precisa de cada audio MP3    |
| - Ritmo: +5% dinamico    | - Template Dark Tech     | - Codificacao individual de cada cena via FFmpeg  |
| - Normalizacao Fonetica  | - Renderizacao Chromium  | - Concat demuxer sem recodificacao (-c copy)      |
|   (phonetic_normalize)   | - CSS Moderno com Cards  | - Margem de 0.8s para transicao suave             |
| - Gera 24 audios MP3     | - Gera 24 frames PNG     | - Limpeza automatica de arquivos intermediarios   |
+--------------------------+--------------------------+---------------------------------------------------+
```

---

## 3. Dicionario de Normalizacao Fonetica (`normalize_for_tts`)

Para solucionar as falhas comuns de pronuncia de termos tecnicos em ingles, siglas e nomes de objetos Oracle por vozes neurais em portugues brasileiro, o script [`build_video.py`](build_video.py) aplica um mapeamento fonetico exclusivamente ao fluxo de texto enviado ao sintetizador Edge-TTS, mantendo a grafia tecnica original nos slides visuais e na documentacao:

| Termo Tecnico Original | Conversao Fonetica Enviada ao Sintetizador | Motivo / Ajuste |
| :--- | :--- | :--- |
| `Harness` | `Rárness` | Evita a pronuncia com H mudo no portugues. |
| `Schema` | `Esquima` | Garante a pronuncia correta da palavra em ingles. |
| `Context Rot` | `Context Rót` | Garante a vogal aberta no substantivo. |
| `Offloading` | `Of-lôudim` | Evita leitura aportuguesada literal de "offloading". |
| `Thin Client` | `Tin Cláient` | Fonetica fiel da conexao nativa em Python. |
| `SQL*Plus` | `És-Quê-Éli Plus` | Impede leitura literal de asteriscos. |
| `SQL*Net` | `És-Quê-Éli Nét` | Pronuncia formal do protocolo de rede Oracle. |
| `SQLcl` | `És-Quê-Éli Cê-Éli` | Impede a pronuncia aglutinada como palavra unica. |
| `V$SQL_PLAN` | `Vê Dólar És-Quê-Éli Plan` | Leitura tecnica correta da view dinamica de plano. |
| `V$SQL` | `Vê Dólar És-Quê-Éli` | Leitura tecnica correta da view de estatisticas de SQL. |
| `MCP_AGENT_RO` | `M-C-P Agent R-O` | Soletra as siglas do usuario de servico. |
| `TRG_AUDIT_MCP_AGENT_LOGON` | `trigger de auditoria de logon` | Substitui o identificador bruto por descricao fluida. |
| `Changeset` | `Tcheindj-sét` | Pronuncia do termo de mudanca do Liquibase. |
| `Rollback` | `Rôl-béqui` | Pronuncia do comando de reversao. |
| `Pull Request` | `Púl Request` | Pronuncia padrao da operacao Git. |
| `Runners` | `Râners` | Pronuncia correta dos agentes de CI/CD. |
| `Exadata` | `Exa-deita` | Fonetica internacional da plataforma Oracle Engineered System. |
| `SYS, SYSTEM` | `Sís, Sístem` | Leitura precisa das contas administrativas do banco. |
| `IDE` | `I-D-E` | Soletra o acronimo do ambiente de desenvolvimento. |
| `DevSecOps` | `Dév-Séc-Óps` | Fonetica fluida da metodologia. |
| `Reinvented` | `Reinvênted` | Pronuncia do titulo original da palestra. |
| `Google Gemini` | `Google Djêmini` | Pronuncia correta do modelo de IA. |
| `Arley Ribeiro` | `Arlei Ribeiro` | Fonetica correta do nome do autor. |

---

## 4. Detalhamento das Cenas por Video

### Video 01: Visao Executiva e Arquitetura DevSecOps
- **Cena 01:** Capa e o Dilema da IA em Bancos Criticos (`MODEL + HARNESS = AGENT`).
- **Cena 02:** O Custo Oculto do Context Rot e Alucinacoes (Degradacao de contexto e toxicidade).
- **Cena 03:** Os Tres Pilares da Engenharia de Harness (Governanca, Reducao e Trilha).
- **Cena 04:** Lab 01: Olhos e Algemas com SQLcl MCP (`MCP_AGENT_RO`, `QUOTA 0M`, Trigger de Auditoria).
- **Cena 05:** Seguranca Operacional do MCP Server (Porta 1521, SQL*Net nativo e credencial cifrada).
- **Cena 06:** Lab 02: Mitigando o Context Rot via Progressive Disclosure (`MASTER_INDEX.md`).
- **Cena 07:** Lab 02: Tool Call Offloading com Python Thin Mode (Reducao de 98% de tokens).
- **Cena 08:** Lab 03: Da Alucinacao ao GitOps Declarativo (Schema-as-Code com SQLcl Liquibase).
- **Cena 09:** Lab 03: Tuning Real e Rollback Obrigatorio (98,7% de ganho de Buffer Gets).
- **Cena 10:** Topologia Corporativa: O Paradigma Zero-Agent no Exadata (Segregacao em 4 camadas).
- **Cena 11:** O Ciclo de Vida DevSecOps Agentico (Esteira unificada do prompt ao deploy).
- **Cena 12:** Sintese Executiva e Creditos Tecnicos (Atribuicoes de autoria e encerramento).

### Video 02: Implementacao Pratica Passo a Passo
- **Cena 01:** Capa e Visao Geral do Roteiro Pratico (Objetivo: reproducibilidade local).
- **Cena 02:** Provisionando o Banco Oracle 23ai Free no Docker (`docker-compose.yml`, volume e healthcheck).
- **Cena 03:** Criando o Usuario Restrito MCP_AGENT_RO e a Trigger (Scripts `01_create_user.sql` e `02_trigger.sql`).
- **Cena 04:** Conexao Nomeada no SQLcl e Inicializacao do MCP (`conn -save mcp_hr_lab` e `mcp start`).
- **Cena 05:** Integracao do MCP no VS Code e IDEs (`.vscode/mcp.json` e inspecao de schema).
- **Cena 06:** Arquitetura de Harness: Implementando o MASTER_INDEX.md (Taxonomia de regras e catalogos).
- **Cena 07:** Executando a Skill de Tuning e Auditoria (`SKILL_DBA_TUNING_AUDIT.md` e regras de ouro).
- **Cena 08:** Executando o Script de Offloading em Python Thin Mode (`offload_query.py` com `python-oracledb`).
- **Cena 09:** Lab 03: Exportando o Schema Baseline com Liquibase (`lb generate-schema -split`).
- **Cena 10:** Criando o Changeset com Rollback Obrigatorio (`changeset_v1.1.0_index_employees.xml`).
- **Cena 11:** Aplicando a Mudanca e Validando com Git Worktrees (`lb update`, `lb status` e isolamento Git).
- **Cena 12:** Checklist Final de Implantacao e Creditos Tecnicos (Resumo dos 3 laboratorios e encerramento).

---

## 5. Como Executar a Geracao dos Videos

Para compilar ambos os videos a partir da raiz do repositorio utilizando o ambiente virtual Python:

```bash
# Executar a pipeline de construcao automatizada
.\.venv\Scripts\python.exe video-presentation/build_video.py
```

### Reproducao dos Videos Gerados (PowerShell no Windows):

```powershell
# Reproduzir Video 01: Visao Executiva & Arquitetura
Start-Process "video-presentation/output/palestra_01_visao_executiva_e_arquitetura.mp4"

# Reproduzir Video 02: Implementacao Pratica Passo a Passo
Start-Process "video-presentation/output/palestra_02_implementacao_passo_a_passo.mp4"
```

---

## 6. Creditos e Atribuicoes

- **Palestra Original:** *"The APEX Dev Reinvented"* — **Bruno Cardoso** (Oracle ACE Associate / Oracle APEX Solutions Architect)
- **Implementacao dos Laboratorios, Arquitetura de Banco e Automacao dos Videos:** **Arley Ribeiro (DBA / Infraestrutura de Dados)**
- **Revisao Tecnica e Estruturacao:** **IA (Google Gemini)**
