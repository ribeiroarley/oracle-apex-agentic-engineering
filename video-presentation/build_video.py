import asyncio
import os
import re
import shutil
import subprocess
import time
from pathlib import Path
import edge_tts
import imageio_ffmpeg
from moviepy import AudioFileClip
from playwright.async_api import async_playwright

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / "temp"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_VIDEO_1 = OUTPUT_DIR / "palestra_01_visao_executiva_e_arquitetura.mp4"
OUTPUT_VIDEO_2 = OUTPUT_DIR / "palestra_02_implementacao_passo_a_passo.mp4"

PHONETIC_REPLACEMENTS = [
    # Termos compostos e especificos primeiro
    (r"\bTRG_AUDIT_MCP_AGENT_LOGON\b", "trigger de auditoria de logon"),
    (r"\bMCP_AGENT_RO\b", "M-C-P Agent R-O"),
    (r"\bV\$SQL_PLAN\b", "Vê Dólar És-Quê-Éli Plan"),
    (r"\bV\$SQL\b", "Vê Dólar És-Quê-Éli"),
    (r"\bSQL\*Plus\b", "És-Quê-Éli Plus"),
    (r"\bSQL\*Net\b", "És-Quê-Éli Nét"),
    (r"\bContext Rot\b", "Context Rót"),
    (r"\bcontext rot\b", "context rót"),
    (r"\bThin Client\b", "Tin Cláient"),
    (r"\bthin client\b", "tin cláient"),
    (r"\bPull Requests?\b", "Púl Request"),
    (r"\bpull requests?\b", "púl request"),
    (r"\bGoogle Gemini\b", "Google Djêmini"),
    (r"\bArley Ribeiro\b", "Arlei Ribeiro"),
    (r"\bBruno Cardoso\b", "Bruno Cardoso"),
    (r"\bThe APEX Dev Reinvented\b", "The APEX Dev Reinvênted"),
    (r"\bReinvented\b", "Reinvênted"),
    (r"\breinvented\b", "reinvênted"),
    (r"\bDevSecOps\b", "Dév-Séc-Óps"),
    (r"\bChangesets?\b", "Tcheindj-séts"),
    (r"\bchangesets?\b", "tcheindj-séts"),
    (r"\bRollbacks?\b", "Rôl-béqui"),
    (r"\brollbacks?\b", "rôl-béqui"),
    (r"\bRunners?\b", "Râners"),
    (r"\brunners?\b", "râners"),
    (r"\bExadata\b", "Exa-deita"),
    (r"\bexadata\b", "exa-deita"),
    (r"\bHarness\b", "Rárness"),
    (r"\bharness\b", "rárness"),
    (r"\bSchemas?\b", "Esquima"),
    (r"\bschemas?\b", "esquima"),
    (r"\bOffloading\b", "Of-lôudim"),
    (r"\boffloading\b", "of-lôudim"),
    (r"\bSQLcl\b", "És-Quê-Éli Cê-Éli"),
    (r"\bSYS, SYSTEM\b", "Sís, Sístem"),
    (r"\bSYS\b", "Sís"),
    (r"\bSYSTEM\b", "Sístem"),
    (r"\bIDE\b", "I-D-E"),
    (r"\bCBO\b", "C-B-O"),
    (r"\bLLMs?\b", "L-L-M"),
    (r"\bAPIs?\b", "A-P-I"),
    (r"\bCLI\b", "C-L-I"),
    (r"\bUAT\b", "U-A-T"),
    (r"\bPR\b", "P-R"),
    (r"\bPRs\b", "P-Rs"),
    (r"\bDocker\b", "Dóquer"),
    (r"\bdocker\b", "dóquer"),
    (r"\bPlaywright\b", "Pleirráiti"),
    (r"\bGitOps\b", "Git-Óps"),
    (r"\bWorktrees?\b", "Uôrc-trís"),
    (r"\bworktrees?\b", "uôrc-trís"),
    (r"\btoken offloading\b", "tôquen of-lôudim"),
    (r"\btokens?\b", "tôquens"),
    (r"\bTokens?\b", "Tôquens"),
]


def normalize_for_tts(text: str) -> str:
    """Aplica normalizacao fonetica exclusivamente ao texto enviado ao edge-tts."""
    normalized = text
    for pattern, replacement in PHONETIC_REPLACEMENTS:
        normalized = re.sub(pattern, replacement, normalized)
    return normalized


# ---------------------------------------------------------------------------
# CENAS DO VIDEO 01 (Visao Executiva e Arquitetura DevSecOps - 12 Cenas)
# ---------------------------------------------------------------------------
VIDEO_1_SCENES = [
    {
        "id": 1,
        "title": "Engenharia Agentica Governada para Oracle e APEX",
        "subtitle": "A Transicao de Desenvolvedor Low-Code para Engenheiro de Harness e Sistemas Autonomos",
        "phase": "ABERTURA & CONCEITO",
        "narration": (
            "Sejam muito bem-vindos. Nos ultimos anos, a Inteligencia Artificial transformou a engenharia de software, "
            "mas a sua adocao em bancos de dados corporativos criticos como Oracle e Oracle Exadata ainda enfrenta forte "
            "resistencia. A palestra The APEX Dev Reinvented, apresentada por Bruno Cardoso, expos com maestria essa ruptura: "
            "o desenvolvedor tradicional precisa se reinventar como um Engenheiro de Harness."
        ),
        "html_body": """
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><span class="badge badge-orange">PARADIGMA LEGADO</span> O Modelo Visual Tradicional</div>
                <ul class="styled-list">
                    <li>Desenvolvimento centrado em wizards visuais pontuais (click-and-run).</li>
                    <li>Exports monolíticos gigantescos com IDs internos volateis.</li>
                    <li>Dificuldade crônica em testes automatizados e code reviews no Git.</li>
                    <li>Dependencia de intervencoes manuais e empíricas na madrugada.</li>
                </ul>
            </div>
            <div class="card">
                <div class="card-header"><span class="badge badge-cyan">NOVO PARADIGMA</span> Engenheiro de Harness</div>
                <div class="formula-box">MODEL + HARNESS = AGENT CONFIAVEL</div>
                <p style="margin-top: 18px; color: #c9d1d9; font-size: 17px; line-height: 1.5;">
                    O desenvolvedor deixa de executar tarefas manuais e passa a projetar restricoes deterministicas, ferramentas locais e esteiras CI/CD para governar agentes de IA autônomos.
                </p>
            </div>
        </div>
        """,
    },
    {
        "id": 2,
        "title": "O Dilema da IA em Ambientes de Producao",
        "subtitle": "Alucinacao, Amnesia e Riscos Operacionais em Bancos de Dados de Missao Critica",
        "phase": "DIAGNOSTICO DO PROBLEMA",
        "narration": (
            "Modelos de linguagem isolados nao possuem memoria persistente confiavel e desconhecem regras de negocio. "
            "Sem amarras tecnicas, um agente de IA pode alucinar, executar comandos destrutivos acidentais, vazar dados "
            "sensiveis ou saturar sua propria janela de contexto. Em bancos corporativos de missao critica, a confianca cega "
            "em prompts e inaceitavel."
        ),
        "html_body": """
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><span class="badge badge-orange">RISCOS CRITICOS</span> Por que o LLM Puro Falha</div>
                <div class="rule-box"><span class="rule-tag">RISCO 1</span> <strong>Alucinacao de DDL:</strong> Sugestoes de DROP ou ALTER sem validacao de impacto.</div>
                <div class="rule-box"><span class="rule-tag">RISCO 2</span> <strong>Amnesia de Sessao:</strong> Esquecimento de regras ao longo de conversas longas.</div>
                <div class="rule-box"><span class="rule-tag">RISCO 3</span> <strong>Vazamento de Dados:</strong> Envio de dados confidenciais para nuvens externas.</div>
                <div class="rule-box"><span class="rule-tag">RISCO 4</span> <strong>Context Rot:</strong> Degradacao do modelo sob alto volume de informacao.</div>
            </div>
            <div class="card">
                <div class="card-header"><span class="badge badge-green">PRINCIPIO DA GOVERNANCA</span> Seguranca em Primeiro Lugar</div>
                <div class="highlight-banner" style="background: rgba(255, 87, 34, 0.12); border-color: rgba(255, 87, 34, 0.4);">
                    PROMPTS NAO SAO CONTRATOS DE SEGURANCA
                </div>
                <p style="margin-top: 20px; font-size: 17px; color: #8b949e; line-height: 1.5;">
                    A protecao de dados corporativos exige controles fisicos e logicos no proprio banco de dados: menor privilegio, auditoria nativa e esteiras deterministas.
                </p>
            </div>
        </div>
        """,
    },
    {
        "id": 3,
        "title": "A Equacao da Confiabilidade: Model + Harness = Agent",
        "subtitle": "Como Envolver o Modelo em Restricoes Deterministicas, Ferramentas Locais e CI/CD",
        "phase": "HARNESS ENGINEERING",
        "narration": (
            "Para tornar a IA confiavel, e mandatorio envolve-la em um harness rigoroso. O harness e o arcabouco composto por "
            "ferramentas locais, controle de acesso, gestao de memoria e esteiras de integracao continua. Neste repositorio, "
            "implementamos uma esteira DevSecOps completa construida sobre o Oracle Database 23ai e ferramentas oficiais da Oracle."
        ),
        "html_body": """
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><span class="badge badge-cyan">ESTRUTURA DO HARNESS</span> Componentes Essenciais</div>
                <ul class="styled-list">
                    <li><strong>Protocolo MCP:</strong> Oracle SQLcl atuando como servidor de contexto padronizado.</li>
                    <li><strong>Progressive Disclosure:</strong> Catalogo leve que expõe skills apenas sob demanda.</li>
                    <li><strong>Tool Call Offloading:</strong> Interceptacao de queries volumosas em disco local.</li>
                    <li><strong>Schema-as-Code:</strong> Versionamento determinista via SQLcl Liquibase com rollback.</li>
                </ul>
            </div>
            <div class="card">
                <div class="card-header"><span class="badge badge-orange">OS 3 PILARES DO REPOSITORIO</span></div>
                <div class="pillar-grid">
                    <div class="pillar-item"><div class="pillar-title">LAB 01</div><div class="pillar-desc">Governanca & SQLcl MCP Server (Menor Privilegio)</div></div>
                    <div class="pillar-item"><div class="pillar-title">LAB 02</div><div class="pillar-desc">Harness Engineering, Progressive Disclosure & Offloading</div></div>
                    <div class="pillar-item"><div class="pillar-title">LAB 03</div><div class="pillar-desc">GitOps Declarativo, Liquibase & Git Worktrees</div></div>
                </div>
            </div>
        </div>
        """,
    },
    {
        "id": 4,
        "title": "Lab 01: Olhos e Algemas com SQLcl MCP Server",
        "subtitle": "Integracao Nativa da IDE com o Banco de Dados via Model Context Protocol",
        "phase": "LAB 01: SEGURANCA & PROTOCOLO",
        "narration": (
            "No Laboratorio 01, atacamos o primeiro pilar: a seguranca. O agente de IA jamais conecta como SYS, SYSTEM ou dono do schema. "
            "Criamos um container Docker com Oracle 23ai Free e configuramos o Oracle SQLcl atuando como servidor de Model Context Protocol, "
            "permitindo que a IDE inspecione metadados de forma governada."
        ),
        "html_body": """
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><span class="badge badge-cyan">CONECTIVIDADE CONTROLADA</span> Arquitetura MCP stdio</div>
                <div class="step-flow">
                    <div class="step-box">1. IDE (VS Code / Claude Desktop) inicia o processo <code>sql -mcp</code></div>
                    <div class="step-box">2. Conexao autentica usando credencial nomeada segura <code>mcp_hr_lab</code></div>
                    <div class="step-box">3. Comunicacao via canal seguro JSON-RPC sobre stdio (sem portas HTTP abertas)</div>
                    <div class="step-box">4. Conexao com Oracle 23ai restrita a porta 1521 via usuario read-only</div>
                </div>
            </div>
            <div class="card">
                <div class="card-header"><span class="badge badge-orange">BENEFICIOS IMEDIATOS</span></div>
                <ul class="styled-list">
                    <li>Elimina credenciais em texto puro em arquivos de configuracao.</li>
                    <li>Sem instalacao de daemons externos no servidor do banco.</li>
                    <li>Inspecao de dicionario de dados governada pelo proprio SQLcl oficial.</li>
                </ul>
            </div>
        </div>
        """,
    },
    {
        "id": 5,
        "title": "Lab 01: Menor Privilegio e Auditoria em Tempo Real",
        "subtitle": "Restricao QUOTA 0M e Rastreamento de Sessoes via Trigger AFTER LOGON",
        "phase": "LAB 01: SEGURANCA & PROTOCOLO",
        "narration": (
            "Criamos o usuario dedicado MCP_AGENT_RO com QUOTA ZERO na tablespace USERS, impedindo fisicamente qualquer criacao "
            "de tabela ou gravacao de dados. Concedemos apenas leitura no dicionario e views dinamicas como V$SQL e V$SQL_PLAN. "
            "Toda conexao do agente e registrada automaticamente pela trigger AFTER LOGON em tabela de auditoria."
        ),
        "html_body": """
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><span class="badge badge-cyan">USUARIO MCP_AGENT_RO</span> Travas no Banco</div>
                <div class="rule-box"><span class="rule-tag">QUOTA 0M</span> Impossibilita alocacao de espaco ou insercoes.</div>
                <div class="rule-box"><span class="rule-tag">SELECT ONLY</span> Somente leitura nas tabelas de negocio do schema HR.</div>
                <div class="rule-box"><span class="rule-tag">VIEWS CBO</span> Acesso restrito a V$SQL e V$SQL_PLAN para tuning.</div>
                <div class="rule-box"><span class="rule-tag">SINONIMOS</span> Sinonimos privados evitam exposicao de schemas.</div>
            </div>
            <div class="card">
                <div class="card-header"><span class="badge badge-orange">TRIGGER DE AUDITORIA</span> TRG_AUDIT_MCP_AGENT_LOGON</div>
                <pre class="code-block"><code><span class="kw">CREATE OR REPLACE TRIGGER</span> trg_audit_mcp_agent_logon
<span class="kw">AFTER LOGON ON DATABASE</span>
<span class="kw">BEGIN</span>
  <span class="kw">IF</span> SYS_CONTEXT(<span class="str">'USERENV'</span>, <span class="str">'SESSION_USER'</span>) = <span class="str">'MCP_AGENT_RO'</span> <span class="kw">THEN</span>
    <span class="kw">INSERT INTO</span> system.admin_audit_mcp_sessions (...)
    <span class="kw">VALUES</span> (SYSTIMESTAMP, OS_USER, MODULE, IP_ADDRESS);
  <span class="kw">END IF</span>;
<span class="kw">END</span>;</code></pre>
            </div>
        </div>
        """,
    },
    {
        "id": 6,
        "title": "Lab 02: O Fenomeno do Context Rot e Progressive Disclosure",
        "subtitle": "Carregando Conhecimento Especializado sob Demanda para Proteger a Memoria do Modelo",
        "phase": "LAB 02: EFICIENCIA DE CONTEXTO",
        "narration": (
            "No Laboratorio 02, enfrentamos o Context Rot: quando a janela de contexto e inundada por dados massivos, o modelo perde "
            "atencao e comete erros. Aplicamos o Progressive Disclosure: o agente inicia lendo apenas o catalogo leve MASTER_INDEX "
            "com trezentos tokens, ativando skills especializadas de tuning CBO apenas sob demanda."
        ),
        "html_body": """
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><span class="badge badge-orange">O PROBLEMA</span> Saturacao da Janela de Contexto</div>
                <p style="font-size: 16px; color: #8b949e; line-height: 1.5; margin-bottom: 16px;">
                    Injetar manuais completos, DDLs inteiros e regras corporativas no prompt inicial consome 50% da janela antes de a primeira query ser analisada.
                </p>
                <div class="formula-box">CONTEXT OVERFLOW = RESPOSTAS LENTAS + ALUCINACOES</div>
            </div>
            <div class="card">
                <div class="card-header"><span class="badge badge-cyan">A SOLUCAO</span> Progressive Disclosure</div>
                <div class="step-flow">
                    <div class="step-box"><strong>Nivel 1:</strong> MASTER_INDEX.md (~300 tokens com gatilhos de ativacao).</div>
                    <div class="step-box"><strong>Nivel 2:</strong> Deteccao de gatilho: <code>/* MCP_TUNING_TARGET */</code>.</div>
                    <div class="step-box"><strong>Nivel 3:</strong> Carga isolada da <code>SKILL_DBA_TUNING_AUDIT.md</code>.</div>
                </div>
            </div>
        </div>
        """,
    },
    {
        "id": 7,
        "title": "Lab 02: Tool Call Offloading e Reducao de 98% de Tokens",
        "subtitle": "Desvio Automatico de Payloads Volumosos para Disco Local com Retorno Estruturado",
        "phase": "LAB 02: EFICIENCIA DE CONTEXTO",
        "narration": (
            "Para consultas volumosas, criamos um utilitario em Python com driver oracledb em modo thin. Se o retorno ultrapassar "
            "mil e quinhentos tokens, o payload completo e salvo em disco local e o agente recebe apenas um resumo estruturado e "
            "uma amostra de cinco linhas. Reduzimos de trinta e cinco mil para quatrocentos e cinquenta tokens: economia de noventa e oito por cento."
        ),
        "html_body": """
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><span class="badge badge-cyan">CLI OFFLOAD_QUERY.PY</span> Regra de Interceptacao</div>
                <div class="formula-box" style="border-color: #00e5ff; background: rgba(0, 229, 255, 0.05);">
                    Tokens Estimados = len(JSON) / 4
                </div>
                <div class="step-flow" style="margin-top: 16px;">
                    <div class="step-box">&lt; 1.500 tokens &rarr; Saida direta no stdout.</div>
                    <div class="step-box">&ge; 1.500 tokens &rarr; Grava em <code>offload_cache/dump_*.json</code>.</div>
                    <div class="step-box">Retorna apenas resumo, contagem de linhas e amostra de 5 registros.</div>
                </div>
            </div>
            <div class="card">
                <div class="card-header"><span class="badge badge-green">ECONOMIA REAL COMPROVADA</span> 500 Linhas de Logs</div>
                <div class="metrics-grid">
                    <div class="metric-card danger">
                        <div class="metric-val">35.385</div>
                        <div class="metric-label">Tokens Brutos</div>
                    </div>
                    <div class="metric-card success">
                        <div class="metric-val">~450</div>
                        <div class="metric-label">Tokens Offloaded</div>
                    </div>
                </div>
                <div class="highlight-banner">-98,7% DE CONSUMO DE CONTEXTO</div>
            </div>
        </div>
        """,
    },
    {
        "id": 8,
        "title": "Lab 03: Schema-as-Code Declarativo com SQLcl Liquibase",
        "subtitle": "Eliminacao de Scripts Manuais com Controle de Versao e Rastreabilidade Total",
        "phase": "LAB 03: SCHEMA-AS-CODE & GITOPS",
        "narration": (
            "No Laboratorio 03, conectamos o diagnostico da IA a entrega continua. Abolimos a execucao manual de scripts soltos "
            "via SQL*Plus. Empregamos o Oracle SQLcl integrado ao Liquibase, capturando a baseline declarativa com o comando generate-schema "
            "e versionando os indices recomendados em changesets XML rastreaveis."
        ),
        "html_body": """
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><span class="badge badge-cyan">SQLCL LIQUIBASE NATIVO</span> Da Baseline ao Changeset</div>
                <div class="step-flow">
                    <div class="step-box">1. <code>lb generate-schema</code> extrai snapshot inicial em XML declarativo.</div>
                    <div class="step-box">2. Registro dos objetos pre-existentes via <code>lb changelog-sync</code>.</div>
                    <div class="step-box">3. Criacao do changeset incremental <code>v1.1.0-tuning-indexes.xml</code>.</div>
                    <div class="step-box">4. Orquestracao via Master Controller <code>changelog/controller.xml</code>.</div>
                </div>
            </div>
            <div class="card">
                <div class="card-header"><span class="badge badge-orange">RASTREABILIDADE IMUTAVEL</span> Tabela DATABASECHANGELOG</div>
                <ul class="styled-list">
                    <li>Cada mudanca possui ID semantico, autor e hash MD5 de integridade.</li>
                    <li>Bloqueio de execucao concorrente via DATABASECHANGELOGLOCK.</li>
                    <li>Historico auditavel compativel com requisitos SOX, ISO e LGPD.</li>
                </ul>
            </div>
        </div>
        """,
    },
    {
        "id": 9,
        "title": "Lab 03: Rollback Obrigatorio e Ganho de 98,7% de I/O",
        "subtitle": "Queda Drastica no Custo do Otimizador e Buffer Gets Reduzidos de 317 para 4",
        "phase": "LAB 03: SCHEMA-AS-CODE & GITOPS",
        "narration": (
            "Uma regra inegociavel e aplicada: nenhum changeset e comitado sem o bloco de rollback testado previamente. Apos a aplicacao "
            "automatizada pelo Liquibase contra cem mil registros, validamos na view V$SQL: o custo do otimizador CBO despencou de "
            "oitenta e oito para tres, e os Buffer Gets cairam de trezentos e dezessete para quatro: economia de noventa e oito virgula sete por cento de I/O."
        ),
        "html_body": """
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><span class="badge badge-cyan">XML COM ROLLBACK OBRIGATORIO</span></div>
                <pre class="code-block"><code><span class="kw">&lt;changeSet</span> <span class="str">id="v1.1.0-idx-emp-id"</span> <span class="str">author="mcp_dba"</span><span class="kw">&gt;</span>
  <span class="kw">&lt;createIndex</span> <span class="str">tableName="EMPLOYEE_ACTIVITY_LOGS"</span>
               <span class="str">indexName="IDX_EMPLOYEE_ACT_LOGS_EMP_ID"</span><span class="kw">&gt;</span>
    <span class="kw">&lt;column</span> <span class="str">name="EMPLOYEE_ID"</span><span class="kw">/&gt;</span>
  <span class="kw">&lt;/createIndex&gt;</span>
  <span class="kw">&lt;rollback&gt;</span>
    <span class="kw">&lt;dropIndex</span> <span class="str">tableName="EMPLOYEE_ACTIVITY_LOGS"</span>
               <span class="str">indexName="IDX_EMPLOYEE_ACT_LOGS_EMP_ID"</span><span class="kw">/&gt;</span>
  <span class="kw">&lt;/rollback&gt;</span>
<span class="kw">&lt;/changeSet&gt;</span></code></pre>
            </div>
            <div class="card">
                <div class="card-header"><span class="badge badge-green">VALIDACAO ANTES VS. DEPOIS</span> (100k Linhas)</div>
                <table class="data-table">
                    <thead><tr><th>Query</th><th>Custo CBO</th><th>Buffer Gets</th><th>Ganho</th></tr></thead>
                    <tbody>
                        <tr><td><code>q1_emp_lookup</code></td><td><span class="old-val">88</span> &rarr; <span class="new-val">3</span></td><td><span class="old-val">317</span> &rarr; <span class="new-val">4</span></td><td><span class="badge-success">-98,7%</span></td></tr>
                        <tr><td><code>q2_status_range</code></td><td><span class="old-val">88</span> &rarr; <span class="new-val">3</span></td><td><span class="old-val">317</span> &rarr; <span class="new-val">4</span></td><td><span class="badge-success">-98,7%</span></td></tr>
                        <tr><td><code>q3_emp_severity</code></td><td><span class="old-val">88</span> &rarr; <span class="new-val">3</span></td><td><span class="old-val">317</span> &rarr; <span class="new-val">4</span></td><td><span class="badge-success">-98,7%</span></td></tr>
                    </tbody>
                </table>
                <div class="highlight-banner" style="margin-top: 18px;">INDEX RANGE SCAN HOMOLOGADO</div>
            </div>
        </div>
        """,
    },
    {
        "id": 10,
        "title": "Arquitetura Corporativa: Zero Agentes no Servidor Exadata",
        "subtitle": "Acesso Restrito a Rede SQL*Net e Segregacao Fisica entre Estacoes, Git e Producao",
        "phase": "TOPOLOGIA CORPORATIVA",
        "narration": (
            "No documento Proposito Unificado, consolidamos a premissa de seguranca para comites corporativos: nenhum componente de "
            "IA, Python ou Git e instalado dentro do servidor de banco de dados ou cluster Exadata. A comunicacao ocorre exclusivamente "
            "via rede SQL*Net padrao, nas portas quinze vinte e um ou vinte e quatro oitenta e quatro."
        ),
        "html_body": """
        <div class="banner-alert">
            PREMISSA MANDATORIA: ZERO AGENTES DENTRO DO SERVIDOR DE BANCO OU CLUSTER EXADATA
        </div>
        <div class="grid-4" style="margin-top: 20px;">
            <div class="tier-card">
                <div class="tier-num">CAMADA 1</div>
                <div class="tier-title">Estacao Engenheiro</div>
                <p>VS Code + SQLcl MCP + Skills locais. Conexao Read-Only via VPN.</p>
            </div>
            <div class="tier-card">
                <div class="tier-num">CAMADA 2</div>
                <div class="tier-title">Repositorio Git</div>
                <p>GitHub / GitLab. Pull Requests obrigatorios com revisao de DBA.</p>
            </div>
            <div class="tier-card">
                <div class="tier-num">CAMADA 3</div>
                <div class="tier-title">Runner CI/CD</div>
                <p>Java + SQLcl Headless. Executa <code>lb update</code> e testes de rollback.</p>
            </div>
            <div class="tier-card highlight">
                <div class="tier-num">CAMADA 4</div>
                <div class="tier-title">Exadata Cluster</div>
                <p>Producao e UAT isolados. Apenas rede SQL*Net TCP 1521 / TCPS 2484.</p>
            </div>
        </div>
        """,
    },
    {
        "id": 11,
        "title": "Estudo de Caso: Manufatura de Calcados de Alto Volume",
        "subtitle": "Como a Esteira DevSecOps Elimina Paradas de Linha de Montagem e Locks de Producao",
        "phase": "ESTUDO DE CASO REAL",
        "narration": (
            "Aplicamos este modelo no cenario de uma grande industria calçadista com cento e vinte mil pares por dia em APEX. No modelo "
            "tradicional, paradas fabris ocorriam por criacao manual de indices e migrações falhas na madrugada. Com a esteira, alteracoes "
            "nascem como Pull Requests versionados, sao testadas em homologacao e aplicadas sem locks de producao."
        ),
        "html_body": """
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><span class="badge badge-orange">FLUXO TRADICIONAL (LEGADO)</span></div>
                <ul class="styled-list">
                    <li>O chão de fábrica trava por query lenta em ordens de producao.</li>
                    <li>DBA cria indices empiricos em producao durante o expediente.</li>
                    <li>Locks de tabela paralisam esteiras de montagem e faturamento.</li>
                    <li>Deploys manuais na madrugada sem script de rollback testado.</li>
                </ul>
            </div>
            <div class="card">
                <div class="card-header"><span class="badge badge-green">ESTEIRA DEVSECOPS AGENTICA</span></div>
                <ul class="styled-list">
                    <li>Diagnostico de CBO via MCP em ambiente espelho read-only.</li>
                    <li>Mudanca encapsulada em changeset Liquibase com rollback obrigatorio.</li>
                    <li>Validacao em esteira CI/CD em UAT antes de tocar producao.</li>
                    <li>Deploy automatizado e rastreavel sem paradas fabris ou incidentes.</li>
                </ul>
            </div>
        </div>
        """,
    },
    {
        "id": 12,
        "title": "Conclusao, Reprodutibilidade e Creditos Tecnicos",
        "subtitle": "Codigo Aberto, Documentacao Completa e Atribuicoes Técnicas do Repositorio",
        "phase": "FECHAMENTO & CREDITOS",
        "narration": (
            "Esta esteira comprova que e perfeitamente viavel unir a velocidade da IA com a seguranca corporativa que a administracao de dados exige. "
            "O projeto conta com implementacao e arquitetura de dados desenvolvidas por Arley Ribeiro, DBA de infraestrutura, inspirado na palestra "
            "de Bruno Cardoso, com revisao tecnica pela IA Google Gemini. Clone o repositorio e transforme seu fluxo de engenharia. Muito obrigado."
        ),
        "html_body": """
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><span class="badge badge-cyan">SINTESE EXECUTIVA</span></div>
                <ul class="styled-list">
                    <li>Governanca de acesso inviolavel com menor privilegio (QUOTA 0M).</li>
                    <li>Protecao de contexto de IA com economia comprovada de 98% de tokens.</li>
                    <li>Versionamento declarativo com SQLcl Liquibase e rollback testado.</li>
                    <li>Homologado para operacoes de missao critica e Oracle Exadata.</li>
                </ul>
            </div>
            <div class="card">
                <div class="card-header"><span class="badge badge-orange">CREDITOS FORMAIS DO PROJETO</span></div>
                <div class="credits-box">
                    <div class="credit-item">
                        <div class="credit-role">Implementacao dos Laboratorios, Arquitetura de Banco e Governanca:</div>
                        <div class="credit-name">Arley Ribeiro</div>
                        <div class="credit-title">DBA / Infraestrutura de Dados</div>
                    </div>
                    <div class="credit-item">
                        <div class="credit-role">Palestra Original de Referencia:</div>
                        <div class="credit-name">Bruno Cardoso</div>
                        <div class="credit-title">Oracle ACE Associate / Oracle APEX Solutions Architect</div>
                    </div>
                    <div class="credit-item">
                        <div class="credit-role">Revisao e Estruturacao da Escrita:</div>
                        <div class="credit-name">IA (Google Gemini)</div>
                    </div>
                </div>
            </div>
        </div>
        """,
    },
]

# ---------------------------------------------------------------------------
# CENAS DO VIDEO 02 (Implementacao Pratica Passo a Passo - 12 Cenas)
# ---------------------------------------------------------------------------
VIDEO_2_SCENES = [
    {
        "id": 1,
        "title": "Implementacao Pratica da Esteira DevSecOps para Oracle",
        "subtitle": "Guia Hands-On Passo a Passo: Docker, SQLcl MCP, Harness Engineering e Liquibase do Zero",
        "phase": "ABERTURA HANDS-ON",
        "narration": (
            "Ola a todos. Neste segundo video, vamos colocar as maos na massa e reproduzir passo a passo toda a esteira "
            "DevSecOps implementada neste repositorio. Voce vai aprender como subir o Oracle Database 23ai em Docker, "
            "salvar conexoes seguras no SQLcl, registrar o servidor MCP no VS Code, criar skills de IA e versionar esquemas com Liquibase."
        ),
        "html_body": """
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><span class="badge badge-cyan">O QUE VAMOS CONSTRUIR</span> Roteiro Pratico</div>
                <ul class="styled-list">
                    <li><strong>Etapa 1:</strong> Banco Oracle 23ai Free em Docker com governanca de menor privilegio.</li>
                    <li><strong>Etapa 2:</strong> Oracle SQLcl 26.2 configurado e salvo como servidor MCP nativo.</li>
                    <li><strong>Etapa 3:</strong> Harness Engineering com Progressive Disclosure e Tool Call Offloading.</li>
                    <li><strong>Etapa 4:</strong> GitOps declarativo com SQLcl Liquibase e trabalho paralelo com Git Worktrees.</li>
                </ul>
            </div>
            <div class="card">
                <div class="card-header"><span class="badge badge-orange">PRE-REQUISITOS LOCAIS</span></div>
                <div class="rule-box"><span class="rule-tag">DOCKER</span> Docker Desktop com suporte a WSL2 no Windows ou Linux.</div>
                <div class="rule-box"><span class="rule-tag">JAVA</span> Java 17 ou 21 em PATH (para execucao do SQLcl).</div>
                <div class="rule-box"><span class="rule-tag">SQLCL</span> Oracle SQLcl 24.3 ou 26.2 instalado.</div>
                <div class="rule-box"><span class="rule-tag">PYTHON</span> Python 3.10+ com oracledb em modo thin.</div>
            </div>
        </div>
        """,
    },
    {
        "id": 2,
        "title": "Etapa 1.1: Variaveis de Ambiente e Seguranca no Git",
        "subtitle": "Isolamento de Credenciais Locais com .env.lab e Protecao Rigorosa no .gitignore",
        "phase": "ETAPA 1: BANCO & DOCKER",
        "narration": (
            "O primeiro passo de seguranca e clonar o repositorio e copiar o modelo de variaveis de ambiente: ponto env ponto lab ponto example "
            "para ponto env ponto lab. No arquivo ponto gitignore, garantimos que credenciais locais, wallets e arquivos de cache jamais "
            "sejam comitados no GitHub, mantendo o repositorio cem por cento seguro contra vazamentos."
        ),
        "html_body": """
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><span class="badge badge-cyan">COMANDO DE PREPARACAO</span></div>
                <pre class="code-block"><code><span class="kw"># 1. Clonar o repositorio</span>
git clone https://github.com/.../oracle-apex-agentic-engineering.git
cd oracle-apex-agentic-engineering

<span class="kw"># 2. Copiar modelo de credenciais</span>
cp lab-01-sqlcl-mcp/.env.lab.example lab-01-sqlcl-mcp/.env.lab</code></pre>
            </div>
            <div class="card">
                <div class="card-header"><span class="badge badge-orange">REGRAS DE GITIGNORE</span> Protecao de Segredos</div>
                <div class="rule-box"><span class="rule-tag">BLOQUEIO</span> <code>.env.lab</code> e <code>*.wallet</code> rigorosamente ignorados.</div>
                <div class="rule-box"><span class="rule-tag">CACHE</span> Pastas <code>offload_cache/</code> e <code>temp/</code> bloqueadas.</div>
                <div class="rule-box"><span class="rule-tag">TEMPLATES</span> Somente arquivos <code>.example</code> versionados publicamente.</div>
            </div>
        </div>
        """,
    },
    {
        "id": 3,
        "title": "Etapa 1.2: Inicializacao do Container Oracle 23ai Free",
        "subtitle": "Provisionamento Declarativo com Nomes Fixos, Volume Persistente e Rede Bridge",
        "phase": "ETAPA 1: BANCO & DOCKER",
        "narration": (
            "Para iniciar o banco de dados, executamos o comando docker compose apontando para o arquivo de ambiente do laboratorio um. "
            "Definimos nomes deterministas para o container, volume persistente e rede bridge. Acompanhamos os logs com docker logs "
            "ate visualizar a mensagem de confirmacao: Database is ready to use."
        ),
        "html_body": """
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><span class="badge badge-cyan">INICIALIZACAO VIA COMPOSE</span></div>
                <pre class="code-block"><code><span class="kw"># Subir o container Oracle 23ai Free</span>
docker compose --env-file lab-01-sqlcl-mcp/.env.lab up -d

<span class="kw"># Acompanhar logs de inicializacao</span>
docker logs -f ora23ai-mcp-lab-db</code></pre>
            </div>
            <div class="card">
                <div class="card-header"><span class="badge badge-green">RECURSOS DETERMINISTAS</span> Nomes sem Hash Aleatorio</div>
                <div class="step-flow">
                    <div class="step-box"><strong>Container:</strong> <code>ora23ai-mcp-lab-db</code> (Oracle Linux)</div>
                    <div class="step-box"><strong>Rede Bridge:</strong> <code>ora23ai-lab-bridge-net</code></div>
                    <div class="step-box"><strong>Volume Persistente:</strong> <code>ora23ai-lab-oradata-vol</code></div>
                    <div class="step-box"><strong>Porta SQL*Net:</strong> <code>1521</code> (PDB: FREEPDB1)</div>
                </div>
            </div>
        </div>
        """,
    },
    {
        "id": 4,
        "title": "Etapa 1.3: Scripts de Inicializacao e Governanca",
        "subtitle": "Provisionamento do Schema HR, Usuario MCP_AGENT_RO com QUOTA 0M e Trigger AFTER LOGON",
        "phase": "ETAPA 1: BANCO & DOCKER",
        "narration": (
            "Durante o boot do container, o script zero um cria o schema HR e o usuario dedicado MCP_AGENT_RO com cota zero na tablespace "
            "USERS e sinonimos privados. Em seguida, a trigger de banco intercepta o logon do agente gravando metadados na tabela de auditoria. "
            "O script zero dois popula cem mil linhas na tabela de logs para testes de tuning."
        ),
        "html_body": """
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><span class="badge badge-cyan">01_SETUP_GOVERNANCE.SQL</span></div>
                <pre class="code-block"><code><span class="kw">-- Cria conta minimamente privilegiada</span>
CREATE USER mcp_agent_ro IDENTIFIED BY McpReadOnly2026!;
ALTER USER mcp_agent_ro QUOTA 0M ON users;

<span class="kw">-- Privilegios de leitura restritos</span>
GRANT CREATE SESSION TO mcp_agent_ro;
GRANT SELECT ANY DICTIONARY TO mcp_agent_ro;
GRANT SELECT ON sys.v_$sql TO mcp_agent_ro;
GRANT SELECT ON sys.v_$sql_plan TO mcp_agent_ro;</code></pre>
            </div>
            <div class="card">
                <div class="card-header"><span class="badge badge-orange">02_SEED_TUNING_SCENARIO.SQL</span></div>
                <ul class="styled-list">
                    <li>Cria tabela volumosa <code>EMPLOYEE_ACTIVITY_LOGS</code>.</li>
                    <li>Gera <strong>100.000 registros</strong> com datas, status e severidades.</li>
                    <li>Simula gargalo tipico de Full Table Scan para demonstracao de tuning CBO.</li>
                </ul>
            </div>
        </div>
        """,
    },
    {
        "id": 5,
        "title": "Etapa 2.1: Salvando a Conexao Segura no Oracle SQLcl",
        "subtitle": "Eliminacao de Senhas em Arquivos JSON com Conexoes Nomeadas Salvas no Host",
        "phase": "ETAPA 2: SQLCL & MCP SERVER",
        "narration": (
            "Com o banco operacional, configuramos o Oracle SQLcl local. Para nao expor senhas em texto puro nos arquivos de configuracao "
            "do agente de IA, executamos o comando conn menos save mcp underline hr underline lab com o parametro savepwd. A conexao "
            "fica gravada de forma criptografada e segura no perfil do desenvolvedor."
        ),
        "html_body": """
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><span class="badge badge-cyan">COMANDO CONN -SAVE</span> No Terminal SQLcl</div>
                <pre class="code-block"><code><span class="kw"># Iniciar SQLcl em modo silencioso</span>
sql -s /nolog

<span class="kw"># Salvar conexao nomeada criptografada</span>
SQL> conn -save mcp_hr_lab -savepwd \\
     mcp_agent_ro/McpReadOnly2026!@localhost:1521/FREEPDB1

SQL> exit</code></pre>
            </div>
            <div class="card">
                <div class="card-header"><span class="badge badge-green">POR QUE ISSO E ESSENCIAL</span></div>
                <ul class="styled-list">
                    <li>Elimina o risco de subir senhas acidentalmente para o Git em arquivos JSON de configuracao de IA.</li>
                    <li>A conexao pode ser chamada em scripts com apenas <code>sql -name mcp_hr_lab</code>.</li>
                    <li>Separamos conexao read-only do agente da conexao administrativa de CI/CD.</li>
                </ul>
            </div>
        </div>
        """,
    },
    {
        "id": 6,
        "title": "Etapa 2.2: Registrando o Servidor MCP no VS Code",
        "subtitle": "Integracao do SQLcl em Modo Servidor via stdio com Ferramentas Nativas de IA",
        "phase": "ETAPA 2: SQLCL & MCP SERVER",
        "narration": (
            "No arquivo de configuracao MCP da sua IDE, como o mcp ponto json do VS Code, registramos o servidor chamando o comando "
            "sql com os argumentos menos mcp e menos name apontando para a conexao mcp underline hr underline lab. A partir deste "
            "instante, o assistente de IA ganha ferramentas nativas para inspecionar tabelas e planos de execucao."
        ),
        "html_body": """
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><span class="badge badge-cyan">.VSCODE/MCP.JSON</span> Registro do Servidor</div>
                <pre class="code-block"><code>{
  <span class="str">"mcpServers"</span>: {
    <span class="str">"oracle-sqlcl-hr-lab"</span>: {
      <span class="str">"command"</span>: <span class="str">"sql"</span>,
      <span class="str">"args"</span>: [
        <span class="str">"-mcp"</span>,
        <span class="str">"-name"</span>,
        <span class="str">"mcp_hr_lab"</span>
      ],
      <span class="str">"env"</span>: {
        <span class="str">"NLS_LANG"</span>: <span class="str">"AMERICAN_AMERICA.AL32UTF8"</span>
      }
    }
  }
}</code></pre>
            </div>
            <div class="card">
                <div class="card-header"><span class="badge badge-orange">FERRAMENTAS MCP DISPONIVEIS</span></div>
                <div class="step-flow">
                    <div class="step-box"><code>sql_run</code>: Executa queries SELECT no banco com seguranca.</div>
                    <div class="step-box"><code>schema_information</code>: Descreve colunas, tipos e constraints.</div>
                    <div class="step-box"><code>sqlcl_run</code>: Roda comandos administrativos suportados pelo SQLcl.</div>
                </div>
            </div>
        </div>
        """,
    },
    {
        "id": 7,
        "title": "Etapa 3.1: Progressive Disclosure na Pratica",
        "subtitle": "Catalogo Leve MASTER_INDEX.md e Ativacao sob Demanda da SKILL_DBA_TUNING_AUDIT.md",
        "phase": "ETAPA 3: HARNESS & OFFLOADING",
        "narration": (
            "No Laboratorio zero dois, estruturamos o catalogo MASTER_INDEX ponto md dentro da pasta skills. Ele consome apenas "
            "trezentos tokens e orienta o agente a carregar a skill de auditoria CBO somente quando o usuario solicita a analise "
            "de uma query com a tag MCP TUNING TARGET, preservando a memoria do modelo contra saturacao."
        ),
        "html_body": """
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><span class="badge badge-cyan">SKILLS/MASTER_INDEX.MD</span></div>
                <table class="data-table">
                    <thead><tr><th>Skill</th><th>Gatilho (Trigger)</th><th>Arquivo</th></tr></thead>
                    <tbody>
                        <tr><td><code>DBA_TUNING_AUDIT</code></td><td>Queries com <code>/* MCP_TUNING_TARGET */</code></td><td><code>SKILL_DBA_...md</code></td></tr>
                        <tr><td><code>TOOL_OFFLOADING</code></td><td>Queries com mais de 50 linhas</td><td><code>offload_query.py</code></td></tr>
                        <tr><td><code>SECURITY_GOV</code></td><td>Auditoria de sessoes de IA</td><td><code>lab-01/README.md</code></td></tr>
                    </tbody>
                </table>
            </div>
            <div class="card">
                <div class="card-header"><span class="badge badge-orange">FLUXO DO AGENTE</span></div>
                <ul class="styled-list">
                    <li>1. Agente le o indice leve (~300 tokens).</li>
                    <li>2. Identifica que a tarefa e de tuning de query.</li>
                    <li>3. Carrega apenas as instrucoes de diagnostico CBO.</li>
                    <li>4. Apresenta o diagnostico com o template padronizado.</li>
                </ul>
            </div>
        </div>
        """,
    },
    {
        "id": 8,
        "title": "Etapa 3.2: Executando Tool Call Offloading em Python",
        "subtitle": "Interceptacao de Consultas Volumosas com oracledb Thin Mode e Cache em Disco",
        "phase": "ETAPA 3: HARNESS & OFFLOADING",
        "narration": (
            "Criamos o utilitario offload underline query ponto py utilizando o driver oracledb em modo thin. Quando executamos "
            "uma consulta que retorna quinhentas linhas da tabela de logs, o script detecta que o volume ultrapassa mil e quinhentos "
            "tokens, salva o json completo na pasta de cache e imprime no terminal apenas o resumo com amostra de cinco linhas."
        ),
        "html_body": """
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><span class="badge badge-cyan">EXECUCAO NO TERMINAL</span></div>
                <pre class="code-block"><code><span class="kw"># Executar consulta volumosa (500 linhas)</span>
python lab-02-harness-engineering/tools/offload_query.py \\
  "SELECT * FROM employee_activity_logs FETCH FIRST 500 ROWS ONLY"

<span class="kw"># Saida Retornada (Payload Estruturado):</span>
{
  "status": "OFFLOADED_TO_DISK",
  "total_rows": 500,
  "dump_file": "offload_cache/dump_20261113.json",
  "token_savings_pct": 98.7,
  "sample": [ ... 5 primeiras linhas ... ]
}</code></pre>
            </div>
            <div class="card">
                <div class="card-header"><span class="badge badge-green">ECONOMIA GARANTIDA</span></div>
                <div class="metrics-grid">
                    <div class="metric-card danger"><div class="metric-val">35.385</div><div class="metric-label">Tokens Brutos</div></div>
                    <div class="metric-card success"><div class="metric-val">~450</div><div class="metric-label">Tokens Retornados</div></div>
                </div>
                <div class="highlight-banner">-98,7% DE TOKENS ECONOMIZADOS</div>
            </div>
        </div>
        """,
    },
    {
        "id": 9,
        "title": "Etapa 4.1: Captura de Baseline com SQLcl Liquibase",
        "subtitle": "Extracao Automatizada do Schema HR via lb generate-schema em XML Declarativo",
        "phase": "ETAPA 4: GITOPS & LIQUIBASE",
        "narration": (
            "No Laboratorio zero tres, iniciamos o versionamento do banco de dados. Conectamos no SQLcl com a conta administrativa "
            "do schema HR e executamos o comando lb generate underline schema dentro da pasta baseline. O SQLcl extrai automaticamente "
            "todas as tabelas, sequences e constraints em arquivos XML declarativos e versionaveis."
        ),
        "html_body": """
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><span class="badge badge-cyan">EXTRACAO DA BASELINE INICIAL</span></div>
                <pre class="code-block"><code><span class="kw"># 1. Navegar ate a pasta da baseline</span>
cd lab-03-gitops-liquibase/changelog/baseline

<span class="kw"># 2. Conectar como administrador do schema HR</span>
sql -name hr_admin_lab

<span class="kw"># 3. Gerar o snapshot declarativo completo</span>
SQL> lb generate-schema
SQL> exit</code></pre>
            </div>
            <div class="card">
                <div class="card-header"><span class="badge badge-orange">OBJETOS GERADOS NO DISCO</span></div>
                <div class="step-flow">
                    <div class="step-box"><code>controller.xml</code>: Sub-controller da baseline.</div>
                    <div class="step-box"><code>countries_table.xml</code>, <code>departments_table.xml</code>.</div>
                    <div class="step-box"><code>employees_table.xml</code>, <code>employee_activity_logs_table.xml</code>.</div>
                    <div class="step-box">XMLs declarativos de foreign keys, indices e sequences.</div>
                </div>
            </div>
        </div>
        """,
    },
    {
        "id": 10,
        "title": "Etapa 4.2: Changeset dos Indices e Master Controller",
        "subtitle": "Codificacao do XML de Migracao com Bloco de Reversao Obrigatorio e Rastreabilidade",
        "phase": "ETAPA 4: GITOPS & LIQUIBASE",
        "narration": (
            "Com base no diagnostico da IA, criamos o arquivo v um ponto um ponto zero tuning indexes ponto xml contendo os tres "
            "indices recomendados. Cada alteracao possui obrigatoriamente a tag rollback para caso de falha. No controller mestre "
            "em XML, registramos a baseline e o changeset incremental, garantindo ordem de execucao deterministica."
        ),
        "html_body": """
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><span class="badge badge-cyan">V1.1.0-TUNING-INDEXES.XML</span></div>
                <pre class="code-block"><code><span class="kw">&lt;changeSet</span> <span class="str">id="v1.1.0-tuning-idx-01"</span> <span class="str">author="mcp_dba"</span><span class="kw">&gt;</span>
  <span class="kw">&lt;createIndex</span> <span class="str">tableName="EMPLOYEE_ACTIVITY_LOGS"</span>
               <span class="str">indexName="IDX_EMPLOYEE_ACT_LOGS_EMP_ID"</span><span class="kw">&gt;</span>
    <span class="kw">&lt;column</span> <span class="str">name="EMPLOYEE_ID"</span><span class="kw">/&gt;</span>
  <span class="kw">&lt;/createIndex&gt;</span>
  <span class="kw">&lt;rollback&gt;</span>
    <span class="kw">&lt;dropIndex</span> <span class="str">tableName="EMPLOYEE_ACTIVITY_LOGS"</span>
               <span class="str">indexName="IDX_EMPLOYEE_ACT_LOGS_EMP_ID"</span><span class="kw">/&gt;</span>
  <span class="kw">&lt;/rollback&gt;</span>
<span class="kw">&lt;/changeSet&gt;</span></code></pre>
            </div>
            <div class="card">
                <div class="card-header"><span class="badge badge-orange">CHANGELOG/CONTROLLER.XML</span></div>
                <pre class="code-block"><code><span class="kw">&lt;databaseChangeLog ...&gt;</span>
  <span class="kw">&lt;include</span> <span class="str">file="baseline/controller.xml"</span>
           <span class="str">relativeToChangelogFile="true"</span><span class="kw">/&gt;</span>
  <span class="kw">&lt;include</span> <span class="str">file="changesets/v1.1.0-tuning-indexes.xml"</span>
           <span class="str">relativeToChangelogFile="true"</span><span class="kw">/&gt;</span>
<span class="kw">&lt;/databaseChangeLog&gt;</span></code></pre>
            </div>
        </div>
        """,
    },
    {
        "id": 11,
        "title": "Etapa 4.3: Deploy com lb update e Git Worktrees",
        "subtitle": "Execucao Transacional de Migracao e Trabalho Paralelo sem Conflitos de Branch",
        "phase": "ETAPA 4: GITOPS & LIQUIBASE",
        "narration": (
            "Para aplicar os indices no banco, executamos o comando lb update apontando para o arquivo controller ponto xml. "
            "O Liquibase aplica as alteracoes e registra os hashes na tabela DATABASECHANGELOG. Com o comando git worktree add, "
            "demonstramos como equipes e agentes trabalham em branches paralelos sem interferir na branch principal."
        ),
        "html_body": """
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><span class="badge badge-cyan">APLICACAO DA MIGRACAO</span></div>
                <pre class="code-block"><code><span class="kw"># 1. Navegar para a pasta do controller</span>
cd lab-03-gitops-liquibase/changelog

<span class="kw"># 2. Conectar e executar lb update</span>
sql -name hr_admin_lab
SQL> lb update -changelog-file controller.xml
SQL> exit</code></pre>
            </div>
            <div class="card">
                <div class="card-header"><span class="badge badge-green">TRABALHO PARALELO COM WORKTREES</span></div>
                <pre class="code-block"><code><span class="kw"># Criar worktree isolada em outra pasta</span>
git worktree add ../oracle-apex-hotfix feature/tuning

<span class="kw"># Trabalhar no branch sem mexer na branch main</span>
cd ../oracle-apex-hotfix
git commit -m "fix: tuning indexes"</code></pre>
                <div class="status-bar" style="margin-top: 10px;">
                    Zero necessidade de git stash ou clones pesados do repositorio!
                </div>
            </div>
        </div>
        """,
    },
    {
        "id": 12,
        "title": "Conclusao da Implementacao & Checklist de Sucesso",
        "subtitle": "Reprodutibilidade Garantida, Governanca CISO e Atribuicoes Técnicas do Projeto",
        "phase": "FECHAMENTO HANDS-ON",
        "narration": (
            "Completamos o ciclo completo de engenharia agentica: banco seguro, protocolo MCP ativo, economia de noventa e oito por cento "
            "de tokens e deploys auditados com Liquibase. O projeto conta com implementacao e arquitetura de dados por Arley Ribeiro, "
            "inspirado na palestra de Bruno Cardoso, com revisao tecnica pela IA Google Gemini. Todos os codigos estao prontos para execucao. Bons estudos."
        ),
        "html_body": """
        <div class="grid-2">
            <div class="card">
                <div class="card-header"><span class="badge badge-cyan">CHECKLIST DE PRODUCAO</span></div>
                <div class="rule-box"><span class="rule-tag">CHECK 1</span> Conexao MCP configurada com usuario read-only (QUOTA 0M).</div>
                <div class="rule-box"><span class="rule-tag">CHECK 2</span> Auditoria de logon ativada em SYSTEM.ADMIN_AUDIT_MCP_SESSIONS.</div>
                <div class="rule-box"><span class="rule-tag">CHECK 3</span> Tool call offloading ativo para queries &gt; 1.500 tokens.</div>
                <div class="rule-box"><span class="rule-tag">CHECK 4</span> Changesets com bloco de rollback obrigatorio e testado.</div>
            </div>
            <div class="card">
                <div class="card-header"><span class="badge badge-orange">CREDITOS DO PROJETO</span></div>
                <div class="credits-box">
                    <div class="credit-item">
                        <div class="credit-role">Implementacao dos Laboratorios e Arquitetura de Dados:</div>
                        <div class="credit-name">Arley Ribeiro</div>
                        <div class="credit-title">DBA / Infraestrutura de Dados</div>
                    </div>
                    <div class="credit-item">
                        <div class="credit-role">Palestra Original de Referencia:</div>
                        <div class="credit-name">Bruno Cardoso</div>
                        <div class="credit-title">Oracle ACE Associate / APEX Solutions Architect</div>
                    </div>
                    <div class="credit-item">
                        <div class="credit-role">Revisao e Estruturacao da Escrita:</div>
                        <div class="credit-name">IA (Google Gemini)</div>
                    </div>
                </div>
            </div>
        </div>
        """,
    },
]


def generate_slide_html(scene: dict, total_scenes: int, category_title: str) -> str:
    """Generate modern Full HD Dark Tech HTML slide."""
    scene_id = scene["id"]
    title = scene["title"]
    subtitle = scene["subtitle"]
    phase = scene["phase"]
    body = scene["html_body"]
    pct = (scene_id / total_scenes) * 100

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }}
    body {{
        width: 1920px;
        height: 1080px;
        overflow: hidden;
        background-color: #080c14;
        background-image:
            radial-gradient(circle at 10% 15%, rgba(0, 229, 255, 0.08) 0%, transparent 35%),
            radial-gradient(circle at 90% 85%, rgba(255, 87, 34, 0.07) 0%, transparent 40%),
            linear-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.015) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 40px 40px, 40px 40px;
        color: #f0f6fc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 44px 60px 32px 60px;
    }}
    .top-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 16px;
    }}
    .repo-tag {{
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 16px;
        font-weight: 700;
        letter-spacing: 2px;
        color: #00e5ff;
        text-transform: uppercase;
    }}
    .phase-badge {{
        background: rgba(0, 229, 255, 0.1);
        border: 1px solid rgba(0, 229, 255, 0.3);
        color: #00e5ff;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 1px;
    }}
    .slide-counter {{
        font-size: 16px;
        font-weight: 700;
        color: #8b949e;
        letter-spacing: 1px;
    }}
    .progress-bar-container {{
        width: 100%;
        height: 3px;
        background: rgba(255, 255, 255, 0.06);
        margin-top: 14px;
        position: relative;
    }}
    .progress-bar {{
        height: 100%;
        width: {pct}%;
        background: linear-gradient(90deg, #00e5ff, #ff6d00);
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.5);
    }}
    .header-section {{
        margin-top: 18px;
        margin-bottom: 18px;
    }}
    .slide-title {{
        font-size: 40px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #ffffff;
        line-height: 1.15;
    }}
    .slide-subtitle {{
        font-size: 19px;
        color: #8b949e;
        margin-top: 8px;
        font-weight: 400;
    }}
    .main-content {{
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}
    .grid-2 {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 32px;
    }}
    .grid-4 {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
    }}
    .card {{
        background: rgba(18, 24, 38, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}
    .card-header {{
        font-size: 20px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    .badge {{
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0.5px;
    }}
    .badge-cyan {{ background: rgba(0, 229, 255, 0.15); color: #00e5ff; border: 1px solid rgba(0, 229, 255, 0.3); }}
    .badge-orange {{ background: rgba(255, 87, 34, 0.15); color: #ff6d00; border: 1px solid rgba(255, 87, 34, 0.3); }}
    .badge-green {{ background: rgba(0, 230, 118, 0.15); color: #00e676; border: 1px solid rgba(0, 230, 118, 0.3); }}
    .styled-list {{
        list-style: none;
    }}
    .styled-list li {{
        position: relative;
        padding-left: 24px;
        margin-bottom: 12px;
        font-size: 16px;
        color: #c9d1d9;
        line-height: 1.4;
    }}
    .styled-list li::before {{
        content: ">";
        position: absolute;
        left: 0;
        top: 0;
        color: #00e5ff;
        font-weight: 800;
        font-family: monospace;
    }}
    .formula-box {{
        background: rgba(255, 87, 34, 0.08);
        border: 1px dashed rgba(255, 87, 34, 0.4);
        padding: 14px;
        border-radius: 8px;
        text-align: center;
        font-size: 18px;
        font-weight: 800;
        letter-spacing: 1px;
        color: #ffffff;
        margin-top: 12px;
    }}
    .pillar-grid {{
        display: grid;
        grid-template-columns: 1fr;
        gap: 10px;
        margin-top: 14px;
    }}
    .pillar-item {{
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 12px 16px;
        border-radius: 6px;
        display: flex;
        align-items: center;
        gap: 14px;
    }}
    .pillar-title {{
        font-weight: 800;
        font-size: 14px;
        color: #00e5ff;
        background: rgba(0, 229, 255, 0.1);
        padding: 3px 8px;
        border-radius: 4px;
    }}
    .pillar-desc {{
        font-size: 15px;
        color: #e6edf3;
        font-weight: 500;
    }}
    .rule-box {{
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-left: 4px solid #00e5ff;
        padding: 11px 14px;
        border-radius: 6px;
        margin-bottom: 10px;
        font-size: 15px;
        color: #c9d1d9;
    }}
    .rule-tag {{
        color: #00e5ff;
        font-weight: 800;
        font-size: 12px;
        margin-right: 6px;
    }}
    .code-block {{
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 16px;
        font-family: "Cascadia Code", "Fira Code", Consolas, monospace;
        font-size: 14px;
        line-height: 1.45;
        color: #c9d1d9;
        overflow: hidden;
    }}
    .code-block .kw {{ color: #ff7b72; font-weight: bold; }}
    .code-block .str {{ color: #a5d6ff; }}
    .status-bar {{
        margin-top: 14px;
        font-size: 14px;
        color: #8b949e;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    .step-flow {{
        display: flex;
        flex-direction: column;
        gap: 8px;
    }}
    .step-box {{
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 10px 14px;
        border-radius: 6px;
        font-size: 15px;
        color: #c9d1d9;
    }}
    .metrics-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-bottom: 14px;
    }}
    .metric-card {{
        padding: 16px;
        border-radius: 8px;
        text-align: center;
    }}
    .metric-card.danger {{ background: rgba(248, 81, 73, 0.1); border: 1px solid rgba(248, 81, 73, 0.3); }}
    .metric-card.success {{ background: rgba(0, 230, 118, 0.1); border: 1px solid rgba(0, 230, 118, 0.3); }}
    .metric-val {{ font-size: 38px; font-weight: 800; color: #ffffff; }}
    .metric-label {{ font-size: 15px; font-weight: 700; margin-top: 4px; color: #e6edf3; }}
    .highlight-banner {{
        background: linear-gradient(90deg, rgba(0, 229, 255, 0.15), rgba(0, 230, 118, 0.15));
        border: 1px solid rgba(0, 229, 255, 0.4);
        padding: 14px;
        border-radius: 6px;
        text-align: center;
        font-size: 18px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 1px;
    }}
    .data-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 15px;
    }}
    .data-table th {{
        background: rgba(255, 255, 255, 0.05);
        color: #8b949e;
        font-weight: 700;
        text-align: left;
        padding: 10px 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }}
    .data-table td {{
        padding: 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        color: #e6edf3;
    }}
    .old-val {{ color: #f85149; text-decoration: line-through; font-size: 13px; margin-right: 4px; }}
    .new-val {{ color: #00e676; font-weight: 700; }}
    .badge-success {{
        background: rgba(0, 230, 118, 0.2);
        color: #00e676;
        padding: 3px 6px;
        border-radius: 4px;
        font-weight: 800;
        font-size: 12px;
    }}
    .banner-alert {{
        background: rgba(255, 87, 34, 0.12);
        border: 2px solid rgba(255, 87, 34, 0.5);
        border-radius: 8px;
        padding: 14px 20px;
        font-size: 17px;
        font-weight: 800;
        color: #ffccbc;
        text-align: center;
        letter-spacing: 0.5px;
    }}
    .tier-card {{
        background: rgba(18, 24, 38, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 18px 16px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 230px;
    }}
    .tier-card.highlight {{ border-color: #00e5ff; background: rgba(0, 229, 255, 0.05); }}
    .tier-num {{ font-size: 12px; font-weight: 800; color: #00e5ff; letter-spacing: 1px; }}
    .tier-title {{ font-size: 17px; font-weight: 700; color: #ffffff; margin: 6px 0; }}
    .tier-card p {{ font-size: 13px; color: #8b949e; line-height: 1.35; }}
    .credits-box {{ display: flex; flex-direction: column; gap: 12px; }}
    .credit-item {{
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-left: 4px solid #ff6d00;
        padding: 10px 14px;
        border-radius: 6px;
    }}
    .credit-role {{ font-size: 12px; font-weight: 700; color: #8b949e; text-transform: uppercase; }}
    .credit-name {{ font-size: 18px; font-weight: 800; color: #ffffff; margin: 2px 0; }}
    .credit-title {{ font-size: 14px; color: #00e5ff; }}
    .footer-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        padding-top: 14px;
        font-size: 13px;
        color: #8b949e;
    }}
    .tech-stack {{ display: flex; gap: 16px; }}
    .tech-item {{ color: #c9d1d9; font-weight: 600; }}
    .tech-item span {{ color: #00e5ff; }}
</style>
</head>
<body>
    <div>
        <div class="top-bar">
            <div class="repo-tag"><span>{category_title}</span></div>
            <div class="phase-badge">{phase}</div>
            <div class="slide-counter">SLIDE {scene_id:02d} / {total_scenes:02d}</div>
        </div>
        <div class="progress-bar-container"><div class="progress-bar"></div></div>
        <div class="header-section">
            <div class="slide-title">{title}</div>
            <div class="slide-subtitle">{subtitle}</div>
        </div>
    </div>
    <div class="main-content">
        {body}
    </div>
    <div class="footer-bar">
        <div class="tech-stack">
            <div class="tech-item"><span>BANCO:</span> Oracle Database 23ai / Exadata</div>
            <div class="tech-item"><span>PROTOCOLO:</span> Oracle SQLcl MCP Server</div>
            <div class="tech-item"><span>HARNESS:</span> Progressive Disclosure & Offloading</div>
            <div class="tech-item"><span>GITOPS:</span> SQLcl Liquibase Declarativo</div>
        </div>
        <div>oracle-apex-agentic-engineering</div>
    </div>
</body>
</html>"""


async def generate_audios(scenes: list, temp_dir: Path):
    """Sintetiza audios MP3 aplicando normalizacao fonetica com edge-tts."""
    tasks = []
    for scene in scenes:
        scene_id = scene["id"]
        audio_path = temp_dir / f"audio_{scene_id}.mp3"
        spoken_text = normalize_for_tts(scene["narration"])
        comm = edge_tts.Communicate(spoken_text, voice="pt-BR-AntonioNeural", rate="+5%")
        tasks.append(comm.save(str(audio_path)))
    await asyncio.gather(*tasks)


async def render_slides(scenes: list, temp_dir: Path, category_title: str):
    """Renderiza slides Full HD 1920x1080 em PNG usando Playwright."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        total_scenes = len(scenes)

        for scene in scenes:
            scene_id = scene["id"]
            html_content = generate_slide_html(scene, total_scenes, category_title)
            png_path = temp_dir / f"slide_{scene_id}.png"
            await page.set_content(html_content, wait_until="networkidle")
            await page.screenshot(path=str(png_path), full_page=False)

        await browser.close()


def assemble_video(scenes: list, temp_dir: Path, output_filepath: Path):
    """Codifica e concatena as cenas em MP4 usando FFmpeg."""
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    concat_lines = []
    total_audio_duration = 0.0

    for scene in scenes:
        scene_id = scene["id"]
        png_path = temp_dir / f"slide_{scene_id}.png"
        audio_path = temp_dir / f"audio_{scene_id}.mp3"
        scene_mp4 = temp_dir / f"scene_{scene_id}.mp4"

        audio_clip = AudioFileClip(str(audio_path))
        duration = audio_clip.duration
        audio_clip.close()
        total_audio_duration += duration

        # Adiciona 0.8s de margem entre cenas
        clip_duration = duration + 0.8

        cmd = [
            ffmpeg_exe,
            "-y",
            "-loop",
            "1",
            "-i",
            str(png_path),
            "-i",
            str(audio_path),
            "-c:v",
            "libx264",
            "-tune",
            "stillimage",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-pix_fmt",
            "yuv420p",
            "-t",
            f"{clip_duration:.3f}",
            str(scene_mp4),
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            raise RuntimeError(f"Erro ao codificar cena {scene_id}: {res.stderr.decode('utf-8', errors='ignore')}")

        concat_lines.append(f"file '{scene_mp4.name}'")

    concat_file = temp_dir / "concat_list.txt"
    concat_file.write_text("\n".join(concat_lines), encoding="utf-8")

    cmd_concat = [
        ffmpeg_exe,
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
        "-c",
        "copy",
        str(output_filepath),
    ]
    res_concat = subprocess.run(cmd_concat, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res_concat.returncode != 0:
        raise RuntimeError(f"Erro na concatenacao final: {res_concat.stderr.decode('utf-8', errors='ignore')}")

    final_duration = total_audio_duration + (len(scenes) * 0.8)
    return final_duration


async def build_production(scenes: list, subfolder_name: str, output_filepath: Path, category_title: str):
    """Executa a esteira completa de um video (audio, slides, montagem)."""
    t0 = time.time()
    sub_temp = TEMP_DIR / subfolder_name
    sub_temp.mkdir(parents=True, exist_ok=True)

    print(f"\n================================================================================")
    print(f"  INICIANDO CONSTRUCAO: {output_filepath.name}")
    print(f"  Total de Cenas: {len(scenes)} | Titulo: {category_title}")
    print(f"================================================================================")

    print(f"  [1/3] Sintetizando {len(scenes)} narracoes com Edge-TTS e normalizacao fonetica...")
    await generate_audios(scenes, sub_temp)

    print(f"  [2/3] Renderizando {len(scenes)} slides Full HD 1080p via Playwright...")
    await render_slides(scenes, sub_temp, category_title)

    print(f"  [3/3] Codificando cenas e concatenando MP4 via FFmpeg...")
    final_duration = assemble_video(scenes, sub_temp, output_filepath)

    elapsed = time.time() - t0
    file_size_mb = output_filepath.stat().st_size / (1024 * 1024)

    print(f"  CONCLUIDO: {output_filepath.name}")
    print(f"  Duracao: {final_duration:.2f}s ({final_duration / 60:.2f} min) | Tamanho: {file_size_mb:.2f} MB")
    print(f"  Tempo de Processamento: {elapsed:.2f}s")
    print(f"================================================================================\n")


async def main():
    start_total = time.time()

    # Video 1: Visao Executiva e Arquitetura DevSecOps
    await build_production(
        scenes=VIDEO_1_SCENES,
        subfolder_name="video_01",
        output_filepath=OUTPUT_VIDEO_1,
        category_title="ORACLE DEVSECOPS: VISAO EXECUTIVA & ARQUITETURA",
    )

    # Video 2: Implementacao Pratica Passo a Passo
    await build_production(
        scenes=VIDEO_2_SCENES,
        subfolder_name="video_02",
        output_filepath=OUTPUT_VIDEO_2,
        category_title="ORACLE DEVSECOPS: GUIA HANDS-ON PASSO A PASSO",
    )

    # Limpeza dos arquivos temporarios de frames e audios
    print("--- Limpando diretorios temporarios de renderizacao ---")
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    print("  Diretorios temporarios removidos. Repositorio limpo!\n")

    total_elapsed = time.time() - start_total
    print("================================================================================")
    print(f"  TODAS AS PRODUCOES FORAM CONCLUIDAS COM SUCESSO!")
    print(f"  Video 1: {OUTPUT_VIDEO_1.name} ({OUTPUT_VIDEO_1.stat().st_size / (1024 * 1024):.2f} MB)")
    print(f"  Video 2: {OUTPUT_VIDEO_2.name} ({OUTPUT_VIDEO_2.stat().st_size / (1024 * 1024):.2f} MB)")
    print(f"  Tempo Total: {total_elapsed:.2f}s")
    print("================================================================================")


if __name__ == "__main__":
    asyncio.run(main())
