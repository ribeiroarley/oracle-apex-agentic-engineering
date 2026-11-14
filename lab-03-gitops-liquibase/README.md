# Laboratório 03: GitOps com SQLcl Liquibase & Git Worktrees

Implementação prática dos conceitos apresentados na palestra *The APEX Dev Reinvented*:
- **Database Objects Versioning & Schema-as-Code** (Slide 27): Versionamento declarativo de tabelas, constraints e índices via SQLcl Liquibase, preenchendo a lacuna do APEXlang para objetos de persistência.
- **Desenvolvimento Paralelo com Git Worktrees** (Slide 20): Como múltiplos agentes autônomos ou desenvolvedores trabalham em branches simultâneos sem alternar branches com `git stash` ou fazer múltiplos clones pesados.
- **Governança Segregada**: Separação estrita entre o usuário de consulta do agente (`MCP_AGENT_RO`) e o usuário administrativo de migrações (`HR`).

---

## 1. Estrutura de Arquivos Criada

```
lab-03-gitops-liquibase/
├── README.md                                 # Esta documentação completa
└── changelog/
    ├── controller.xml                        # Master Controller Liquibase orquestrador
    ├── baseline/                             # Snapshot declarativo inicial gerado pelo SQLcl
    │   ├── controller.xml                    # Sub-controller da baseline
    │   ├── countries_table.xml
    │   ├── departments_table.xml
    │   ├── employees_table.xml
    │   ├── employee_activity_logs_table.xml  # Tabela volumosa do laboratório (100k linhas)
    │   └── ... (constraints e índices PK/UK)
    └── changesets/
        └── v1.1.0-tuning-indexes.xml         # Changeset incremental com os 3 índices recomendados
```

---

## 2. Segregação de Credenciais no SQLcl

Para respeitar o **Princípio do Menor Privilégio**:

| Conexão SQLcl | Usuário de Banco | Privilégios | Propósito |
| :--- | :--- | :--- | :--- |
| **`mcp_hr_lab`** | `MCP_AGENT_RO` | `QUOTA 0M`, `SELECT` em tabelas do HR, `SELECT ANY DICTIONARY`, `V$SQL`, `V$SQL_PLAN` | **Read-Only:** Análise agêntica e MCP Server. Não consegue alterar schemas ou aplicar DDLs. |
| **`hr_admin_lab`** | `HR` | `CREATE TABLE`, `CREATE INDEX`, `CREATE TRIGGER`, `QUOTA UNLIMITED` | **CI/CD & GitOps:** Uso exclusivo para comandos Liquibase (`lb update`, `lb rollback`). |

Comando para salvar a conexão administrativa no SQLcl:
```sql
conn -save hr_admin_lab -savepwd hr/HrSchema2026!@localhost:1521/FREEPDB1
```

---

## 3. Fluxo de Execução Liquibase

### 3.1. Captura da Baseline Inicial (Schema-as-Code)
Para gerar o snapshot declarativo de todos os objetos do schema `HR`:
```bash
cd lab-03-gitops-liquibase/changelog/baseline
sql -name hr_admin_lab
SQL> lb generate-schema
SQL> exit
```

### 3.2. Sincronização Inicial (Changelog Sync)
Como os objetos da baseline já existiam no banco, registramos a baseline na tabela `DATABASECHANGELOG` sem recriar os objetos:
```bash
cd lab-03-gitops-liquibase/changelog
sql -name hr_admin_lab
SQL> lb changelog-sync -changelog-file baseline/controller.xml
```

### 3.3. Aplicação do Changeset de Tuning (`v1.1.0`)
O arquivo mestre `controller.xml` orquestra o changeset `changesets/v1.1.0-tuning-indexes.xml`:
```bash
cd lab-03-gitops-liquibase/changelog
sql -name hr_admin_lab
SQL> lb update -changelog-file controller.xml
```

**Resultado da execução:**
```text
UPDATE SUMMARY
Run:                          3
Previously run:              18
Filtered out:                 0
-------------------------------
Total change sets:           21

Liquibase: Update has been successful. Rows affected: 0
```

### 3.4. Capacidade de Rollback Idempotente
Cada changeset em `v1.1.0-tuning-indexes.xml` possui seu bloco `<rollback>` explícito. Para desfazer:
```sql
lb rollback-count -count 3 -changelog-file controller.xml
```

---

## 4. Validação Antes vs. Depois (Métricas de Tuning via MCP)

Após a aplicação do changeset Liquibase `v1.1.0`, os índices foram criados e as estatísticas atualizadas via CBO.

| Query / SQL_ID | Métrica | Antes do Liquibase (Sem Índice) | Depois do Liquibase (Com Índices) | Ganho Obtido |
| :--- | :--- | :--- | :--- | :--- |
| **Query 1 (`7cjcn98yj918r`)**<br>`EMPLOYEES` + `LOGS` (Join por FK) | **Buffer Gets**<br>**Disk Reads**<br>**Plano CBO** | 3.207<br>2.117<br>`TABLE ACCESS FULL` (Log) | **2.285**<br>**0**<br>`VW_GBF_8` (Group-By Pushdown) | **-29% Buffer Gets**<br>**-100% Disk Reads**<br>Sem locks de FK |
| **Query 2 (`9xqq5j5bb9r3s`)**<br>`UPPER(status) = 'FAILED'` | **Buffer Gets**<br>**Índice Criado** | 2.157<br>Nenhum | **2.139**<br>`IDX_EMPLOYEE_ACT_LOGS_STATUS_DATE` | **Redução de I/O**<br>Suporte a Function-Based Index |
| **Query 3 (`a51wtqbvmr7dj`)**<br>Subquery `salary > 8000` + Order By | **Buffer Gets**<br>**Custo CBO** | 2.180<br>1.865 | **2.147**<br>**1.683** | **-182 pontos de Custo CBO**<br>Redução em PGA e Sort |

---

## 5. Guia Prático: Git Worktrees para Engenharia Agêntica (Slide 20)

### O Problema Tradicional
Quando um agente de IA está executando uma tarefa longa (ex: refatoração de páginas APEX) e surge um chamado crítico de banco:
- O desenvolvedor é forçado a fazer `git stash`, trocar de branch (`git checkout hotfix`), aplicar a correção e depois desempilhar o stash com risco de conflitos.
- Alternativamente, clonar todo o repositório novamente consome gigabytes em disco e desconecta o histórico.

### A Solução com Git Worktrees
Um único repositório `.git` gerencia **múltiplas árvores de diretórios independentes**, permitindo que dois agentes (ou desenvolvedor + IA) operem em paralelo em branches diferentes simultaneamente:

```
                          +-------------------+
                          |   .git Central    |
                          +---------+---------+
                                    |
          +-------------------------+-------------------------+
          |                                                   |
+---------v---------+                               +---------v---------+
| Worktree 1 (main) |                               | Worktree 2        |
| Diretório Atual   |                               | (hotfix/tuning)   |
| (Agente Feature)  |                               | (Agente DBA)      |
+-------------------+                               +-------------------+
```

### Comandos Práticos

#### 1. Criar um novo Worktree paralelo em uma pasta vizinha:
```bash
git worktree add ../oracle-apex-hotfix -b hotfix/tuning-indexes
```

#### 2. Verificar os Worktrees ativos:
```bash
git worktree list
```
*Saída esperada:*
```text
/workspace/oracle-apex-agentic-engineering  0000000 [main]
/workspace/oracle-apex-hotfix               0000000 [hotfix/tuning-indexes]
```

#### 3. Trabalhar no branch do Hotfix sem afetar a pasta principal:
Navegue para a pasta paralela. O agente DBA pode editar changelogs Liquibase, rodar testes e comitar sem interferir no branch `main`:
```bash
cd ../oracle-apex-hotfix
git add lab-03-gitops-liquibase/
git commit -m "feat(liquibase): add v1.1.0 tuning indexes changeset"
git push origin hotfix/tuning-indexes
```

#### 4. Remover o Worktree após o merge do Pull Request:
```bash
cd ../oracle-apex-agentic-engineering
git worktree remove ../oracle-apex-hotfix
```
O diretório do hotfix é deletado de forma limpa, enquanto o repositório principal permanece intacto.
