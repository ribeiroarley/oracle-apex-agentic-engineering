-- ==============================================================================
-- 02_seed_tuning_scenario.sql
-- Laboratório: Oracle Database 23ai Free + Oracle SQLcl MCP Server
-- Objetivo: Criar cenário de Performance Tuning com 100.000 registros,
--           ausência intencional de índice na Foreign Key (EMPLOYEE_ID)
--           e coluna de baixa seletividade (ACTIVITY_STATUS).
--           Executa 3 consultas com tag /* MCP_TUNING_TARGET */ para análise na V$SQL.
-- ==============================================================================

SET ECHO ON;
SET SERVEROUTPUT ON;

-- 1. Alternar sessão para a Pluggable Database (FREEPDB1)
ALTER SESSION SET CONTAINER = FREEPDB1;

PROMPT [01] Sessão alternada com sucesso para FREEPDB1.

-- ==============================================================================
-- 2. Criação da Tabela HR.EMPLOYEE_ACTIVITY_LOGS (sem índice na FK)
-- ==============================================================================
PROMPT [02] Recriando tabela HR.EMPLOYEE_ACTIVITY_LOGS para cenário de tuning...

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE hr.employee_activity_logs CASCADE CONSTRAINTS PURGE';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

CREATE TABLE hr.employee_activity_logs (
    log_id           NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_id      NUMBER(6) NOT NULL,
    activity_type    VARCHAR2(30) NOT NULL,
    activity_status  VARCHAR2(20) NOT NULL,
    log_date         TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    payload_details  VARCHAR2(400),
    severity_level   NUMBER(1) NOT NULL,
    CONSTRAINT fk_act_logs_emp FOREIGN KEY (employee_id) REFERENCES hr.employees(employee_id)
);

PROMPT [02] Tabela HR.EMPLOYEE_ACTIVITY_LOGS criada com Foreign Key sem índice.

-- ==============================================================================
-- 3. Carga de 100.000 Registros (CONNECT BY LEVEL)
-- ==============================================================================
PROMPT [03] Inserindo 100.000 registros sintéticos para simulação de carga...

INSERT /*+ APPEND */ INTO hr.employee_activity_logs (
    employee_id,
    activity_type,
    activity_status,
    log_date,
    payload_details,
    severity_level
)
WITH emp_pool AS (
    SELECT employee_id, ROW_NUMBER() OVER (ORDER BY employee_id) AS rn, COUNT(*) OVER () AS total_emps
    FROM hr.employees
)
SELECT
    e.employee_id,
    CASE MOD(l.lvl, 6)
        WHEN 0 THEN 'AUTH_LOGIN'
        WHEN 1 THEN 'QUERY_REPORT'
        WHEN 2 THEN 'EXPORT_DATA'
        WHEN 3 THEN 'UPDATE_RECORD'
        WHEN 4 THEN 'BATCH_JOB'
        ELSE 'API_REQUEST'
    END AS activity_type,
    -- Baixa seletividade: COMPLETED (~90%), FAILED (~7%), PENDING (~3%)
    CASE
        WHEN MOD(l.lvl, 100) < 90 THEN 'COMPLETED'
        WHEN MOD(l.lvl, 100) < 97 THEN 'FAILED'
        ELSE 'PENDING'
    END AS activity_status,
    SYSTIMESTAMP - NUMTODSINTERVAL(MOD(l.lvl, 365), 'DAY') - NUMTODSINTERVAL(MOD(l.lvl, 86400), 'SECOND') AS log_date,
    'Log event payload token #' || l.lvl || ' executed action for workflow tracking with parameter hash ' || ORA_HASH(l.lvl) AS payload_details,
    MOD(l.lvl, 5) + 1 AS severity_level
FROM (
    SELECT LEVEL AS lvl
    FROM dual
    CONNECT BY LEVEL <= 100000
) l
JOIN emp_pool e ON e.rn = 1 + MOD(l.lvl, e.total_emps);

COMMIT;

PROMPT [03] 100.000 registros inseridos e commitados com sucesso.

-- Coleta de estatísticas CBO
PROMPT [03] Coletando estatísticas do Otimizador Baseado em Custo (CBO)...
BEGIN
    DBMS_STATS.GATHER_TABLE_STATS(
        ownname          => 'HR',
        tabname          => 'EMPLOYEE_ACTIVITY_LOGS',
        cascade          => TRUE,
        estimate_percent => DBMS_STATS.AUTO_SAMPLE_SIZE
    );
END;
/

-- ==============================================================================
-- 4. Conceder Acesso e Criar Sinônimo Privado para MCP_AGENT_RO
-- ==============================================================================
PROMPT [04] Concedendo permissão de SELECT e sinônimo para MCP_AGENT_RO...

GRANT SELECT ON hr.employee_activity_logs TO mcp_agent_ro;
CREATE OR REPLACE SYNONYM mcp_agent_ro.employee_activity_logs FOR hr.employee_activity_logs;

-- ==============================================================================
-- 5. Executar Consultas Não Otimizadas (com tag /* MCP_TUNING_TARGET */)
-- ==============================================================================
PROMPT [05] Executando consultas não otimizadas para registrar histórico na V$SQL...

-- Consulta 1: Join com FK não indexada + filtro de baixa seletividade (Full Table Scan)
SELECT /* MCP_TUNING_TARGET */
       e.first_name,
       e.last_name,
       e.department_id,
       l.activity_type,
       l.activity_status,
       COUNT(*) AS total_activities
FROM hr.employees e
JOIN hr.employee_activity_logs l ON e.employee_id = l.employee_id
WHERE l.activity_status = 'COMPLETED'
GROUP BY e.first_name, e.last_name, e.department_id, l.activity_type, l.activity_status
ORDER BY total_activities DESC, e.last_name
FETCH FIRST 20 ROWS ONLY;

-- Consulta 2: Função UPPER em coluna não indexada + agrupamento temporal + ordenação pesada
SELECT /* MCP_TUNING_TARGET */
       l.employee_id,
       TO_CHAR(l.log_date, 'YYYY-MM') AS activity_month,
       l.activity_type,
       COUNT(*) AS event_count,
       MAX(l.payload_details) AS sample_payload
FROM hr.employee_activity_logs l
WHERE UPPER(l.activity_status) = 'FAILED'
  AND l.log_date >= SYSTIMESTAMP - INTERVAL '180' DAY
GROUP BY l.employee_id, TO_CHAR(l.log_date, 'YYYY-MM'), l.activity_type
ORDER BY l.employee_id ASC, activity_month DESC, event_count DESC
FETCH FIRST 20 ROWS ONLY;

-- Consulta 3: Subconsulta não correlacionada com ordenação de coluna VARCHAR longa (Sort em disco/memória)
SELECT /* MCP_TUNING_TARGET */
       l.log_id,
       l.employee_id,
       l.activity_type,
       l.log_date,
       l.payload_details
FROM hr.employee_activity_logs l
WHERE l.employee_id IN (
    SELECT e.employee_id
    FROM hr.employees e
    WHERE e.salary > 8000
)
AND l.severity_level >= 3
ORDER BY l.payload_details DESC, l.log_date DESC
FETCH FIRST 20 ROWS ONLY;

PROMPT [05] Consultas executadas e planos registrados na V$SQL/V$SQL_PLAN.
PROMPT [02_seed_tuning_scenario.sql] Carga de dados e cenário de tuning concluídos!
