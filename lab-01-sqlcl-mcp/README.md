# Laboratório 01: Oracle Database 23ai Free + Oracle SQLcl MCP Server

Laboratório prático de Engenharia Agêntica para provisionar o **Oracle Database 23ai Free** em container Docker e configurar a governança de acesso com **Princípio do Menor Privilégio** para o **Oracle SQLcl MCP Server** (Model Context Protocol).

---

## 1. Arquitetura e Governança de Segurança

```
+-----------------------------------------------------------------------------------+
| Host (Developer Machine / AI Agent Client)                                        |
|                                                                                   |
|  +------------------+         MCP (stdio)         +----------------------------+  |
|  |  Claude Desktop  | <-------------------------> |  Oracle SQLcl (v24.3+)     |  |
|  |  Cursor / IDE    |                             |  sql -mcp -name mcp_hr_lab |  |
|  +------------------+                             +--------------+-------------+  |
+------------------------------------------------------------------|----------------+
                                                                   | SQL Net (Port 1521)
                                                                   | User: MCP_AGENT_RO
+------------------------------------------------------------------v----------------+
| Docker Engine                                                                     |
| Container: ora23ai-mcp-lab-db (Hostname: ora23ai-lab-host)                       |
| Rede: ora23ai-lab-bridge-net | Volume: ora23ai-lab-oradata-vol                    |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | Oracle Database 23ai Free (PDB: FREEPDB1)                                  |  |
|  |                                                                             |  |
|  |  [Schema HR]                     [Schema SYSTEM]                           |  |
|  |   - EMPLOYEES                     - ADMIN_AUDIT_MCP_SESSIONS                |  |
|  |   - DEPARTMENTS                   - Trigger AFTER LOGON (trg_audit_mcp)     |  |
|  |   - EMPLOYEE_ACTIVITY_LOGS                                                  |  |
|  |     (100k linhas / Tuning Lab)   [Governança: MCP_AGENT_RO]                 |  |
|  |                                   - QUOTA 0M (Sem escrita de dados)         |  |
|  |                                   - SELECT explícito nas tabelas HR         |  |
|  |                                   - Sinônimos Privados transparentes        |  |
|  |                                   - SELECT ANY DICTIONARY                   |  |
|  |                                   - V_$SQL, V_$SQL_PLAN, V_$SESSION         |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

### Regras de Governança Aplicadas:
1. **Isolamento de Contas Administrativas:** O agente de IA **nunca** conecta como `SYS`, `SYSTEM` ou dono do schema (`HR`).
2. **Menor Privilégio:** Usuário dedicado `MCP_AGENT_RO` criado com `QUOTA 0M ON users`, sem privilégios de `INSERT`, `UPDATE`, `DELETE`, `DROP` ou `ALTER`.
3. **Visibilidade Controlada do Dicionário:** Acesso a `SELECT ANY DICTIONARY` e concessão explícita em views dinâmicas de performance (`sys.v_$sql`, `sys.v_$sql_plan`, `sys.v_$sql_plan_statistics_all`, `sys.v_$session`) para permitir ao agente investigar gargalos de banco e planos de execução.
4. **Sinônimos Privados:** Criados automaticamente para todas as tabelas do schema `HR`, permitindo consultas diretas (`SELECT * FROM employees`) sem expor ou exigir qualificação por schema.
5. **Auditoria de Sessões Agênticas:** Tabela `SYSTEM.ADMIN_AUDIT_MCP_SESSIONS` e trigger `AFTER LOGON ON DATABASE` registram data/hora, `OS_USER`, `MODULE`, `MACHINE` e `IP_ADDRESS` de cada sessão do agente.

---

## 2. Estrutura do Laboratório

```
lab-01-sqlcl-mcp/
├── .env.lab                    # Configurações e senhas locais (ignorado no git)
├── .env.lab.example            # Modelo versionável de variáveis de ambiente
├── docker-compose.yml          # Definição do container Oracle 23ai Free com nomes fixos
├── mcp_config.example.json     # Exemplo de configuração do MCP Server para clientes de IA
├── README.md                   # Esta documentação completa
└── init-scripts/
    ├── 01_setup_hr_and_mcp_governance.sql  # Criação do HR, usuário MCP_AGENT_RO e auditoria
    └── 02_seed_tuning_scenario.sql         # Carga de 100k linhas e queries não otimizadas
```

---

## 3. Passo a Passo de Execução

### Passo 1: Configurar Variáveis de Ambiente
Caso ainda não exista o arquivo `.env.lab`, copie o modelo:
```bash
cd lab-01-sqlcl-mcp
cp .env.lab.example .env.lab
```

### Passo 2: Subir o Container Oracle 23ai Free
Execute o Docker Compose informando explicitamente o arquivo de ambiente:
```bash
# Executando de dentro da pasta lab-01-sqlcl-mcp:
docker compose --env-file .env.lab up -d
```

> **Dica:** Se estiver na raiz do repositório, utilize:
> ```bash
> docker compose --env-file lab-01-sqlcl-mcp/.env.lab -f lab-01-sqlcl-mcp/docker-compose.yml up -d
> ```

### Passo 3: Acompanhar a Inicialização do Banco
Na primeira inicialização, o Oracle Database 23ai criará a base e executará automaticamente os scripts de `init-scripts/`:
```bash
docker compose --env-file .env.lab logs -f ora23ai-mcp-lab-db
```
Aguarde até visualizar a mensagem de inicialização completa:
```
DATABASE IS READY TO USE!
```

---

## 4. Configurar a Conexão no Oracle SQLcl Local

Com o banco ativo e saudável (`healthy`), abra o seu terminal local com o SQLcl instalado:

```bash
sql /nolog
```

Dentro da console do SQLcl, salve a conexão segura com a credencial do agente de IA:

```sql
conn -save mcp_hr_lab -savepwd mcp_agent_ro/McpReadOnly2026!@localhost:1521/FREEPDB1
```

Teste a conexão salva:

```sql
conn mcp_hr_lab
show user
-- Saída esperada: USER is "MCP_AGENT_RO"
exit
```

---

## 5. Configurar o MCP Server no seu Cliente de IA

Copie a configuração de `mcp_config.example.json` para o seu cliente MCP (por exemplo, `%APPDATA%\Claude\claude_desktop_config.json` ou nas configurações de MCP do Cursor / Antigravity):

```json
{
  "mcpServers": {
    "oracle-sqlcl-mcp": {
      "command": "sql",
      "args": [
        "-mcp",
        "-name",
        "mcp_hr_lab"
      ],
      "env": {
        "NLS_LANG": "AMERICAN_AMERICA.AL32UTF8"
      }
    }
  }
}
```

> **Nota:** Certifique-se de que o executável `sql` (SQLcl) esteja no `PATH` do sistema.

---

## 6. Prompts de Teste para o Agente de IA

Utilize estes 3 prompts no seu assistente de IA conectado via SQLcl MCP Server para validar todas as capacidades do laboratório:

### Prompt 1: Introspecção do Schema e Menor Privilégio
> *"Conecte-se via MCP Server ao banco de dados e faça uma introspecção do catálogo disponível para o seu usuário. Liste todas as tabelas acessíveis no schema HR, informe a quantidade de linhas de cada uma e apresente a estrutura detalhada das tabelas `EMPLOYEES` e `DEPARTMENTS` (colunas, tipos de dados e chaves). Confirme se você possui permissão de escrita ou se está operando sob Menor Privilégio (Read-Only). Integre a resposta em formato markdown estruturado."*

### Prompt 2: Auditoria e Rastreabilidade de Sessões
> *"Consulte a tabela de auditoria `ADMIN_AUDIT_MCP_SESSIONS` para verificar o registro das sessões estabelecidas pelo usuário `MCP_AGENT_RO`. Exiba em uma tabela markdown: ID da auditoria, data/hora do logon, `OS_USER`, `MODULE`, `MACHINE` e `IP_ADDRESS`. Verifique se a sua conexão atual via SQLcl MCP Server foi devidamente capturada pelo trigger de banco `TRG_AUDIT_MCP_AGENT_LOGON`."*

### Prompt 3: Diagnóstico de Performance e Recomendação de Tuning
> *"Consulte a view de performance `V$SQL` buscando por instruções que contenham o comentário `/* MCP_TUNING_TARGET */`. Para a consulta que realiza junção entre `EMPLOYEES` e `EMPLOYEE_ACTIVITY_LOGS`:
> 1. Inspecione o plano de execução na `V$SQL_PLAN`.
> 2. Identifique se está ocorrendo Full Table Scan (TABLE ACCESS FULL) e operações de ordenação pesadas.
> 3. Avalie se a Foreign Key `EMPLOYEE_ID` da tabela `EMPLOYEE_ACTIVITY_LOGS` possui índice criado.
> 4. Apresente um relatório técnico explicando o gargalo de I/O encontrado e forneça o script DDL com o `CREATE INDEX` recomendado para otimizar a consulta."*

---

## 7. Comandos de Manutenção do Laboratório

- **Parar o laboratório mantendo dados persistidos:**
  ```bash
  docker compose --env-file .env.lab stop
  ```

- **Reiniciar o laboratório:**
  ```bash
  docker compose --env-file .env.lab start
  ```

- **Destruir o laboratório e os volumes persistentes:**
  ```bash
  docker compose --env-file .env.lab down -v
  ```
