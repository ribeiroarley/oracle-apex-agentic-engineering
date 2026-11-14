# Skill: DBA Performance Tuning & Query Audit

> **Papel:** Especialista em Performance Tuning no Oracle Database 23ai para Agentes Autônomos de IA via MCP Server (`oracle-sqlcl-hr-lab`).
> **Contexto:** Governança com Menor Privilégio (`MCP_AGENT_RO`).

---

## 1. Diretrizes Obrigatórias do Harness (Guardrails Inegociáveis)

1. **Validação Prévia Mandatória:**
   - **NUNCA** sugira a criação de índices baseado unicamente no texto da query SQL.
   - É **obrigatório** consultar previamente o plano real de execução na view `V$SQL_PLAN` para identificar operações ineficientes como `TABLE ACCESS FULL`, `HASH JOIN` desbalanceado ou `SORT ORDER BY` com spill em disco.
   - É **obrigatório** consultar a cardinalidade, número de nulos e seletividade das colunas envolvidas na view `ALL_TAB_COL_STATISTICS` ou `DBA_TAB_COL_STATISTICS`.
2. **Padrão Estrito de Nomenclatura:**
   - Todo índice recomendado deve seguir impreterivelmente o padrão corporativo:
     `HR.IDX_<TABELA>_<COLUNA>`
     *(Exemplo: `HR.IDX_EMPLOYEE_ACT_LOGS_EMP_ID` ou `HR.IDX_EMP_ACT_LOGS_STATUS`)*
3. **Formato Padronizado de Saída:**
   - O diagnóstico final entregue ao usuário deve respeitar rigorosamente a seguinte estrutura em 4 blocos:
     - `SQL_ID`: Identificador alfanumérico da query na `V$SQL`.
     - `Gargalo Identificado`: Diagnóstico técnico preciso do custo de I/O, cardinalidade real vs estimada e ausência de índices em Foreign Keys.
     - `DDL Recomendado`: Instrução SQL DDL completa e formatada com tablespace `USERS` e opções adequadas.
     - `Impacto Esperado`: Estimativa de melhoria percentual em *Buffer Gets*, eliminação de contenção de locks na FK e redução de tempo de execução.

---

## 2. Procedimento Operacional Passo a Passo

### Passo 1: Localizar Queries Alvo na `V$SQL`
Execute via MCP Server a busca das instruções marcadas para diagnóstico:

```sql
SELECT sql_id,
       plan_hash_value,
       executions,
       buffer_gets,
       disk_reads,
       rows_processed,
       elapsed_time / 1000000 AS elapsed_seconds,
       SUBSTR(sql_text, 1, 100) AS sql_snippet
FROM v$sql
WHERE sql_text LIKE '%MCP_TUNING_TARGET%'
  AND sql_text NOT LIKE '%v$sql%'
ORDER BY buffer_gets DESC;
```

### Passo 2: Extrair o Plano de Execução Real na `V$SQL_PLAN`
Para cada `sql_id` identificado, inspecione a hierarquia de operações do Otimizador Baseado em Custo (CBO):

```sql
SELECT id,
       parent_id,
       LPAD(' ', 2 * depth) || operation || ' ' || options AS operation_tree,
       object_owner,
       object_name,
       cardinality,
       bytes,
       cost,
       cpu_cost,
       io_cost
FROM v$sql_plan
WHERE sql_id = '&target_sql_id'
ORDER BY id;
```

> **Pontos de Atenção no Plano:**
> - `TABLE ACCESS FULL` em tabelas volumosas (>10.000 linhas) como `EMPLOYEE_ACTIVITY_LOGS`.
> - Ausência de índice na coluna `EMPLOYEE_ID` (Foreign Key para `HR.EMPLOYEES`), o que pode induzir `HASH JOIN` em varredura completa ou locks de tabela inteira durante operações DML concorrentes.

### Passo 3: Inspecionar Cardinalidade e Estatísticas das Colunas
Valide a seletividade da coluna antes de propor qualquer índice:

```sql
SELECT column_name,
       num_distinct,
       density,
       num_nulls,
       histogram
FROM all_tab_col_statistics
WHERE owner = 'HR'
  AND table_name = 'EMPLOYEE_ACTIVITY_LOGS'
  AND column_name IN ('EMPLOYEE_ID', 'ACTIVITY_STATUS', 'LOG_DATE');
```

> **Critério de Avaliação Técnica:**
> - Se `density` for baixa (alta cardinalidade, como `EMPLOYEE_ID` com milhares de valores distintos), o índice **B-Tree** é altamente recomendado.
> - Se a coluna tiver baixa cardinalidade (ex: `ACTIVITY_STATUS` com apenas 3 valores distintos: `COMPLETED`, `FAILED`, `PENDING`), um índice simples geralmente não é benéfico, a menos que seja composto com outra coluna seletiva ou utilize particionamento/índice filtrado.

---

## 3. Template de Resposta Padronizada

```markdown
### Diagnóstico de Performance — SQL_ID: `<ID>`

- **SQL_ID:** `<ID>`
- **Gargalo Identificado:**
  Varredura completa de tabela (`TABLE ACCESS FULL`) em `HR.EMPLOYEE_ACTIVITY_LOGS` consumindo `<X>` Buffer Gets por execução. A chave estrangeira `EMPLOYEE_ID` não possui índice de suporte, forçando o CBO a realizar Full Table Scan nas 100.000 linhas durante a junção com `HR.EMPLOYEES`.
- **DDL Recomendado:**
  ```sql
  CREATE INDEX HR.IDX_EMPLOYEE_ACT_LOGS_EMP_ID
  ON HR.EMPLOYEE_ACTIVITY_LOGS (EMPLOYEE_ID)
  TABLESPACE USERS;
  ```
- **Impacto Esperado:**
  - Migração de `TABLE ACCESS FULL` para `INDEX RANGE SCAN`.
  - Redução estimada de Buffer Gets em mais de 90%.
  - Eliminação de risco de bloqueio em tabela inteira em atualizações na tabela pai `HR.EMPLOYEES`.
```
