-- ==============================================================================
-- 01_setup_hr_and_mcp_governance.sql
-- Laboratório: Oracle Database 23ai Free + Oracle SQLcl MCP Server
-- Objetivo: Configuração do schema HR, governança de acesso (Menor Privilégio)
--           para o usuário MCP_AGENT_RO e auditoria de conexões.
-- ==============================================================================

SET ECHO ON;
SET DEFINE OFF;
SET SERVEROUTPUT ON;

-- 1. Alternar sessão para a Pluggable Database (FREEPDB1)
ALTER SESSION SET CONTAINER = FREEPDB1;

PROMPT [01] Sessão alternada com sucesso para FREEPDB1.

-- ==============================================================================
-- 2. Garantir existência e desbloqueio do Schema HR
-- ==============================================================================
PROMPT [02] Configurando schema HR...

DECLARE
    v_user_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_user_count FROM dba_users WHERE username = 'HR';
    IF v_user_count = 0 THEN
        EXECUTE IMMEDIATE 'CREATE USER hr IDENTIFIED BY "HrSchema2026!" DEFAULT TABLESPACE users QUOTA UNLIMITED ON users';
        EXECUTE IMMEDIATE 'GRANT CREATE SESSION, CREATE TABLE, CREATE VIEW, CREATE SEQUENCE, CREATE PROCEDURE, CREATE SYNONYM, CREATE TRIGGER TO hr';
        DBMS_OUTPUT.PUT_LINE('Usuário HR criado com sucesso.');
    ELSE
        EXECUTE IMMEDIATE 'ALTER USER hr IDENTIFIED BY "HrSchema2026!" ACCOUNT UNLOCK';
        EXECUTE IMMEDIATE 'ALTER USER hr QUOTA UNLIMITED ON users';
        DBMS_OUTPUT.PUT_LINE('Usuário HR desbloqueado e senha atualizada.');
    END IF;
END;
/

-- Criar estrutura e dados do HR caso as tabelas ainda não existam no container
DECLARE
    v_tbl_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_tbl_count FROM dba_tables WHERE owner = 'HR' AND table_name = 'EMPLOYEES';
    IF v_tbl_count = 0 THEN
        -- REGIONS
        EXECUTE IMMEDIATE '
        CREATE TABLE hr.regions (
            region_id NUMBER CONSTRAINT reg_id_pk PRIMARY KEY,
            region_name VARCHAR2(25)
        )';
        EXECUTE IMMEDIATE 'INSERT INTO hr.regions VALUES (1, ''Europe'')';
        EXECUTE IMMEDIATE 'INSERT INTO hr.regions VALUES (2, ''Americas'')';
        EXECUTE IMMEDIATE 'INSERT INTO hr.regions VALUES (3, ''Asia'')';
        EXECUTE IMMEDIATE 'INSERT INTO hr.regions VALUES (4, ''Middle East and Africa'')';

        -- COUNTRIES
        EXECUTE IMMEDIATE '
        CREATE TABLE hr.countries (
            country_id CHAR(2) CONSTRAINT country_c_id_pk PRIMARY KEY,
            country_name VARCHAR2(40),
            region_id NUMBER CONSTRAINT countr_reg_fk REFERENCES hr.regions(region_id)
        )';
        EXECUTE IMMEDIATE 'INSERT INTO hr.countries VALUES (''US'', ''United States of America'', 2)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.countries VALUES (''CA'', ''Canada'', 2)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.countries VALUES (''BR'', ''Brazil'', 2)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.countries VALUES (''UK'', ''United Kingdom'', 1)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.countries VALUES (''DE'', ''Germany'', 1)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.countries VALUES (''JP'', ''Japan'', 3)';

        -- LOCATIONS
        EXECUTE IMMEDIATE '
        CREATE TABLE hr.locations (
            location_id NUMBER(4) CONSTRAINT loc_id_pk PRIMARY KEY,
            street_address VARCHAR2(40),
            postal_code VARCHAR2(12),
            city VARCHAR2(30) NOT NULL,
            state_province VARCHAR2(25),
            country_id CHAR(2) CONSTRAINT loc_c_id_fk REFERENCES hr.countries(country_id)
        )';
        EXECUTE IMMEDIATE 'INSERT INTO hr.locations VALUES (1400, ''2014 Jabberwocky Rd'', ''26192'', ''Southlake'', ''Texas'', ''US'')';
        EXECUTE IMMEDIATE 'INSERT INTO hr.locations VALUES (1500, ''2011 Interiors Blvd'', ''99236'', ''South San Francisco'', ''California'', ''US'')';
        EXECUTE IMMEDIATE 'INSERT INTO hr.locations VALUES (1700, ''2004 Charade Rd'', ''98199'', ''Seattle'', ''Washington'', ''US'')';
        EXECUTE IMMEDIATE 'INSERT INTO hr.locations VALUES (1800, ''147 Spadina Ave'', ''M5V 2L7'', ''Toronto'', ''Ontario'', ''CA'')';
        EXECUTE IMMEDIATE 'INSERT INTO hr.locations VALUES (2500, ''Magdalen Centre, The Oxford Science Park'', ''OX4 4GA'', ''Oxford'', ''Oxford'', ''UK'')';
        EXECUTE IMMEDIATE 'INSERT INTO hr.locations VALUES (2700, ''Schwanthalerstr. 7031'', ''80339'', ''Munich'', ''Bavaria'', ''DE'')';

        -- DEPARTMENTS
        EXECUTE IMMEDIATE '
        CREATE TABLE hr.departments (
            department_id NUMBER(4) CONSTRAINT dept_id_pk PRIMARY KEY,
            department_name VARCHAR2(30) NOT NULL,
            manager_id NUMBER(6),
            location_id NUMBER(4) CONSTRAINT dept_loc_fk REFERENCES hr.locations(location_id)
        )';
        EXECUTE IMMEDIATE 'INSERT INTO hr.departments VALUES (10, ''Administration'', 200, 1700)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.departments VALUES (20, ''Marketing'', 201, 1800)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.departments VALUES (30, ''Purchasing'', 114, 1700)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.departments VALUES (40, ''Human Resources'', 203, 2500)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.departments VALUES (50, ''Shipping'', 121, 1500)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.departments VALUES (60, ''IT'', 103, 1400)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.departments VALUES (70, ''Public Relations'', 204, 2700)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.departments VALUES (80, ''Sales'', 145, 2500)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.departments VALUES (90, ''Executive'', 100, 1700)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.departments VALUES (100, ''Finance'', 108, 1700)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.departments VALUES (110, ''Accounting'', 205, 1700)';

        -- JOBS
        EXECUTE IMMEDIATE '
        CREATE TABLE hr.jobs (
            job_id VARCHAR2(10) CONSTRAINT job_id_pk PRIMARY KEY,
            job_title VARCHAR2(35) NOT NULL,
            min_salary NUMBER(6),
            max_salary NUMBER(6)
        )';
        EXECUTE IMMEDIATE 'INSERT INTO hr.jobs VALUES (''AD_PRES'', ''President'', 20080, 40000)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.jobs VALUES (''AD_VP'', ''Administration Vice President'', 15000, 30000)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.jobs VALUES (''AD_ASST'', ''Administration Assistant'', 3000, 6000)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.jobs VALUES (''FI_MGR'', ''Finance Manager'', 8200, 16000)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.jobs VALUES (''FI_ACCOUNT'', ''Accountant'', 4200, 9000)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.jobs VALUES (''AC_MGR'', ''Accounting Manager'', 8200, 16000)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.jobs VALUES (''AC_ACCOUNT'', ''Public Accountant'', 4200, 9000)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.jobs VALUES (''SA_MAN'', ''Sales Manager'', 10000, 20080)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.jobs VALUES (''SA_REP'', ''Sales Representative'', 6000, 12008)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.jobs VALUES (''PU_MAN'', ''Purchasing Manager'', 8000, 15000)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.jobs VALUES (''PU_CLERK'', ''Purchasing Clerk'', 2500, 5500)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.jobs VALUES (''ST_MAN'', ''Stock Manager'', 5500, 8500)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.jobs VALUES (''ST_CLERK'', ''Stock Clerk'', 2008, 5000)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.jobs VALUES (''SH_CLERK'', ''Shipping Clerk'', 2500, 5500)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.jobs VALUES (''IT_PROG'', ''Programmer'', 4000, 10000)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.jobs VALUES (''MK_MAN'', ''Marketing Manager'', 9000, 15000)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.jobs VALUES (''MK_REP'', ''Marketing Representative'', 4000, 9000)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.jobs VALUES (''HR_REP'', ''Human Resources Representative'', 4000, 9000)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.jobs VALUES (''PR_REP'', ''Public Relations Representative'', 4500, 10500)';

        -- EMPLOYEES
        EXECUTE IMMEDIATE '
        CREATE TABLE hr.employees (
            employee_id NUMBER(6) CONSTRAINT emp_emp_id_pk PRIMARY KEY,
            first_name VARCHAR2(20),
            last_name VARCHAR2(25) NOT NULL,
            email VARCHAR2(25) NOT NULL CONSTRAINT emp_email_uk UNIQUE,
            phone_number VARCHAR2(20),
            hire_date DATE NOT NULL,
            job_id VARCHAR2(10) NOT NULL CONSTRAINT emp_job_fk REFERENCES hr.jobs(job_id),
            salary NUMBER(8,2),
            commission_pct NUMBER(2,2),
            manager_id NUMBER(6),
            department_id NUMBER(4) CONSTRAINT emp_dept_fk REFERENCES hr.departments(department_id)
        )';

        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (100, ''Steven'', ''King'', ''SKING'', ''515.123.4567'', TO_DATE(''17-06-2013'', ''dd-mm-yyyy''), ''AD_PRES'', 24000, NULL, NULL, 90)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (101, ''Neena'', ''Kochhar'', ''NKOCHHAR'', ''515.123.4568'', TO_DATE(''21-09-2015'', ''dd-mm-yyyy''), ''AD_VP'', 17000, NULL, 100, 90)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (102, ''Lex'', ''De Haan'', ''LDEHAAN'', ''515.123.4569'', TO_DATE(''13-01-2011'', ''dd-mm-yyyy''), ''AD_VP'', 17000, NULL, 100, 90)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (103, ''Alexander'', ''Hunold'', ''AHUNOLD'', ''590.423.4567'', TO_DATE(''03-01-2016'', ''dd-mm-yyyy''), ''IT_PROG'', 9000, NULL, 102, 60)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (104, ''Bruce'', ''Ernst'', ''BERNST'', ''590.423.4568'', TO_DATE(''21-05-2017'', ''dd-mm-yyyy''), ''IT_PROG'', 6000, NULL, 103, 60)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (105, ''David'', ''Austin'', ''DAUSTIN'', ''590.423.4569'', TO_DATE(''25-06-2015'', ''dd-mm-yyyy''), ''IT_PROG'', 4800, NULL, 103, 60)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (106, ''Valli'', ''Pataballa'', ''VPATABAL'', ''590.423.4560'', TO_DATE(''05-02-2016'', ''dd-mm-yyyy''), ''IT_PROG'', 4800, NULL, 103, 60)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (107, ''Diana'', ''Lorentz'', ''DLORENTZ'', ''590.423.5567'', TO_DATE(''07-02-2017'', ''dd-mm-yyyy''), ''IT_PROG'', 4200, NULL, 103, 60)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (108, ''Nancy'', ''Greenberg'', ''NGREENBE'', ''515.124.4569'', TO_DATE(''17-08-2012'', ''dd-mm-yyyy''), ''FI_MGR'', 12008, NULL, 101, 100)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (109, ''Daniel'', ''Faviet'', ''DFAVIET'', ''515.124.4169'', TO_DATE(''16-08-2012'', ''dd-mm-yyyy''), ''FI_ACCOUNT'', 9000, NULL, 108, 100)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (110, ''John'', ''Chen'', ''JCHEN'', ''515.124.4269'', TO_DATE(''28-09-2015'', ''dd-mm-yyyy''), ''FI_ACCOUNT'', 8200, NULL, 108, 100)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (111, ''Ismael'', ''Sciarra'', ''ISCIARRA'', ''515.124.4369'', TO_DATE(''30-09-2015'', ''dd-mm-yyyy''), ''FI_ACCOUNT'', 7700, NULL, 108, 100)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (112, ''Jose Manuel'', ''Urman'', ''JMURMAN'', ''515.124.4469'', TO_DATE(''07-03-2016'', ''dd-mm-yyyy''), ''FI_ACCOUNT'', 7800, NULL, 108, 100)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (113, ''Luis'', ''Popp'', ''LPOPP'', ''515.124.4567'', TO_DATE(''07-12-2017'', ''dd-mm-yyyy''), ''FI_ACCOUNT'', 6900, NULL, 108, 100)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (114, ''Den'', ''Raphaely'', ''DRAPHEAL'', ''515.127.4561'', TO_DATE(''07-12-2012'', ''dd-mm-yyyy''), ''PU_MAN'', 11000, NULL, 100, 30)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (115, ''Alexander'', ''Khoo'', ''AKHOO'', ''515.127.4562'', TO_DATE(''18-05-2013'', ''dd-mm-yyyy''), ''PU_CLERK'', 3100, NULL, 114, 30)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (116, ''Shelli'', ''Baida'', ''SBAIDA'', ''515.127.4563'', TO_DATE(''24-12-2015'', ''dd-mm-yyyy''), ''PU_CLERK'', 2900, NULL, 114, 30)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (117, ''Sigal'', ''Tobias'', ''STOBIAS'', ''515.127.4564'', TO_DATE(''24-07-2015'', ''dd-mm-yyyy''), ''PU_CLERK'', 2800, NULL, 114, 30)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (118, ''Guy'', ''Himuro'', ''GHIMURO'', ''515.127.4565'', TO_DATE(''15-11-2016'', ''dd-mm-yyyy''), ''PU_CLERK'', 2600, NULL, 114, 30)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (119, ''Karen'', ''Colmenares'', ''KCOLMENA'', ''515.127.4566'', TO_DATE(''10-08-2017'', ''dd-mm-yyyy''), ''PU_CLERK'', 2500, NULL, 114, 30)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (120, ''Matthew'', ''Weiss'', ''MWEISS'', ''650.123.1234'', TO_DATE(''18-07-2014'', ''dd-mm-yyyy''), ''ST_MAN'', 8000, NULL, 100, 50)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (121, ''Adam'', ''Fripp'', ''AFRIPP'', ''650.123.2234'', TO_DATE(''10-04-2015'', ''dd-mm-yyyy''), ''ST_MAN'', 8200, NULL, 100, 50)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (122, ''Payam'', ''Kaufling'', ''PKAUFLIN'', ''650.123.3234'', TO_DATE(''01-05-2013'', ''dd-mm-yyyy''), ''ST_MAN'', 7900, NULL, 100, 50)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (123, ''Shanta'', ''Vollman'', ''SVOLLMAN'', ''650.123.4234'', TO_DATE(''10-10-2015'', ''dd-mm-yyyy''), ''ST_MAN'', 6500, NULL, 100, 50)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (124, ''Kevin'', ''Mourgos'', ''KMOURGOS'', ''650.123.5234'', TO_DATE(''16-11-2017'', ''dd-mm-yyyy''), ''ST_MAN'', 5800, NULL, 100, 50)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (145, ''John'', ''Russell'', ''JRUSSEL'', ''011.44.1344.429268'', TO_DATE(''01-10-2014'', ''dd-mm-yyyy''), ''SA_MAN'', 14000, 0.4, 100, 80)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (146, ''Karen'', ''Partners'', ''KPARTNER'', ''011.44.1344.467268'', TO_DATE(''05-01-2015'', ''dd-mm-yyyy''), ''SA_MAN'', 13500, 0.3, 100, 80)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (147, ''Alberto'', ''Errazuriz'', ''AERRAZUR'', ''011.44.1344.429278'', TO_DATE(''10-03-2015'', ''dd-mm-yyyy''), ''SA_MAN'', 12000, 0.3, 100, 80)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (148, ''Gerald'', ''Cambrault'', ''GCAMBRAU'', ''011.44.1344.619268'', TO_DATE(''15-10-2017'', ''dd-mm-yyyy''), ''SA_MAN'', 11000, 0.3, 100, 80)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (149, ''Eleni'', ''Zlotkey'', ''EZLOTKEY'', ''011.44.1344.429018'', TO_DATE(''29-01-2018'', ''dd-mm-yyyy''), ''SA_MAN'', 10500, 0.2, 100, 80)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (174, ''Ellen'', ''Abel'', ''EABEL'', ''011.44.1644.429267'', TO_DATE(''11-05-2014'', ''dd-mm-yyyy''), ''SA_REP'', 11000, 0.3, 145, 80)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (175, ''Alyssa'', ''Hutton'', ''AHUTTON'', ''011.44.1644.429266'', TO_DATE(''19-03-2015'', ''dd-mm-yyyy''), ''SA_REP'', 8800, 0.25, 145, 80)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (176, ''Jonathon'', ''Taylor'', ''JTAYLOR'', ''011.44.1644.429265'', TO_DATE(''24-03-2016'', ''dd-mm-yyyy''), ''SA_REP'', 8600, 0.2, 145, 80)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (177, ''Jack'', ''Livingston'', ''JLIVINGS'', ''011.44.1644.429264'', TO_DATE(''23-04-2016'', ''dd-mm-yyyy''), ''SA_REP'', 8400, 0.2, 145, 80)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (178, ''Kimberely'', ''Grant'', ''KGRANT'', ''011.44.1644.429263'', TO_DATE(''24-05-2017'', ''dd-mm-yyyy''), ''SA_REP'', 7000, 0.15, 145, NULL)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (179, ''Charles'', ''Johnson'', ''CJOHNSON'', ''011.44.1644.429262'', TO_DATE(''04-01-2018'', ''dd-mm-yyyy''), ''SA_REP'', 6200, 0.1, 145, 80)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (200, ''Jennifer'', ''Whalen'', ''JWHALEN'', ''515.123.4444'', TO_DATE(''17-09-2013'', ''dd-mm-yyyy''), ''AD_ASST'', 4400, NULL, 101, 10)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (201, ''Michael'', ''Hartstein'', ''MHARTSTE'', ''515.123.5555'', TO_DATE(''17-02-2014'', ''dd-mm-yyyy''), ''MK_MAN'', 13000, NULL, 100, 20)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (202, ''Pat'', ''Fay'', ''PFAY'', ''603.123.6666'', TO_DATE(''17-08-2015'', ''dd-mm-yyyy''), ''MK_REP'', 6000, NULL, 201, 20)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (203, ''Susan'', ''Mavris'', ''SMAVRIS'', ''515.123.7777'', TO_DATE(''07-06-2012'', ''dd-mm-yyyy''), ''HR_REP'', 6500, NULL, 101, 40)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (204, ''Hermann'', ''Baer'', ''HBAER'', ''515.123.8888'', TO_DATE(''07-06-2012'', ''dd-mm-yyyy''), ''PR_REP'', 10000, NULL, 101, 70)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (205, ''Shelley'', ''Higgins'', ''SHIGGINS'', ''515.123.8080'', TO_DATE(''07-06-2012'', ''dd-mm-yyyy''), ''AC_MGR'', 12008, NULL, 101, 110)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.employees VALUES (206, ''William'', ''Gietz'', ''WGIETZ'', ''515.123.8181'', TO_DATE(''07-06-2012'', ''dd-mm-yyyy''), ''AC_ACCOUNT'', 8300, NULL, 205, 110)';

        -- JOB_HISTORY
        EXECUTE IMMEDIATE '
        CREATE TABLE hr.job_history (
            employee_id NUMBER(6) NOT NULL CONSTRAINT jhist_emp_fk REFERENCES hr.employees(employee_id),
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            job_id VARCHAR2(10) NOT NULL CONSTRAINT jhist_job_fk REFERENCES hr.jobs(job_id),
            department_id NUMBER(4) CONSTRAINT jhist_dept_fk REFERENCES hr.departments(department_id),
            CONSTRAINT jhist_emp_id_st_date_pk PRIMARY KEY (employee_id, start_date)
        )';
        EXECUTE IMMEDIATE 'INSERT INTO hr.job_history VALUES (102, TO_DATE(''13-01-2011'', ''dd-mm-yyyy''), TO_DATE(''24-07-2016'', ''dd-mm-yyyy''), ''IT_PROG'', 60)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.job_history VALUES (101, TO_DATE(''21-09-2015'', ''dd-mm-yyyy''), TO_DATE(''27-10-2017'', ''dd-mm-yyyy''), ''AC_ACCOUNT'', 110)';
        EXECUTE IMMEDIATE 'INSERT INTO hr.job_history VALUES (200, TO_DATE(''17-09-2013'', ''dd-mm-yyyy''), TO_DATE(''17-06-2016'', ''dd-mm-yyyy''), ''AD_ASST'', 90)';

        COMMIT;
        DBMS_OUTPUT.PUT_LINE('Estrutura e dados do HR criados e commitados.');
    ELSE
        DBMS_OUTPUT.PUT_LINE('Tabelas do HR já existem.');
    END IF;
END;
/

-- ==============================================================================
-- 3. Criação do Usuário de Governança MCP_AGENT_RO (Princípio do Menor Privilégio)
-- ==============================================================================
PROMPT [03] Configurando usuário dedicado MCP_AGENT_RO...

DECLARE
    v_user_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_user_count FROM dba_users WHERE username = 'MCP_AGENT_RO';
    IF v_user_count = 0 THEN
        EXECUTE IMMEDIATE 'CREATE USER mcp_agent_ro IDENTIFIED BY "McpReadOnly2026!" DEFAULT TABLESPACE users QUOTA 0M ON users';
        DBMS_OUTPUT.PUT_LINE('Usuário MCP_AGENT_RO criado com QUOTA 0M.');
    ELSE
        EXECUTE IMMEDIATE 'ALTER USER mcp_agent_ro IDENTIFIED BY "McpReadOnly2026!" QUOTA 0M ON users ACCOUNT UNLOCK';
        DBMS_OUTPUT.PUT_LINE('Usuário MCP_AGENT_RO atualizado.');
    END IF;
END;
/

-- Revogar UNLIMITED TABLESPACE para garantir rigorosamente QUOTA 0M
BEGIN
    EXECUTE IMMEDIATE 'REVOKE UNLIMITED TABLESPACE FROM mcp_agent_ro';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

-- Conceder privilégio de sessão
GRANT CREATE SESSION TO mcp_agent_ro;
GRANT CREATE SYNONYM TO mcp_agent_ro;

-- ==============================================================================
-- 4. Permissões de Leitura no Dicionário e Views de Performance (Tuning & Planos)
-- ==============================================================================
PROMPT [04] Concedendo privilégios de dicionário e views de performance...

GRANT SELECT ANY DICTIONARY TO mcp_agent_ro;
GRANT SELECT ON sys.v_$sql TO mcp_agent_ro;
GRANT SELECT ON sys.v_$sql_plan TO mcp_agent_ro;
GRANT SELECT ON sys.v_$sql_plan_statistics_all TO mcp_agent_ro;
GRANT SELECT ON sys.v_$session TO mcp_agent_ro;

-- ==============================================================================
-- 5. Conceder SELECT em todas as tabelas de HR e Criar Sinônimos Privados
-- ==============================================================================
PROMPT [05] Concedendo SELECT em tabelas HR e criando sinônimos privados para MCP_AGENT_RO...

DECLARE
    v_sql VARCHAR2(1000);
BEGIN
    FOR t IN (SELECT table_name FROM dba_tables WHERE owner = 'HR') LOOP
        v_sql := 'GRANT SELECT ON hr.' || DBMS_ASSERT.ENQUOTE_NAME(t.table_name, FALSE) || ' TO mcp_agent_ro';
        EXECUTE IMMEDIATE v_sql;

        v_sql := 'CREATE OR REPLACE SYNONYM mcp_agent_ro.' || DBMS_ASSERT.ENQUOTE_NAME(t.table_name, FALSE) || ' FOR hr.' || DBMS_ASSERT.ENQUOTE_NAME(t.table_name, FALSE);
        EXECUTE IMMEDIATE v_sql;

        DBMS_OUTPUT.PUT_LINE('Grant SELECT & Sinônimo criado: ' || t.table_name);
    END LOOP;
END;
/

-- ==============================================================================
-- 6. Tabela de Auditoria e Trigger AFTER LOGON para MCP_AGENT_RO
-- ==============================================================================
PROMPT [06] Criando tabela de auditoria e trigger AFTER LOGON...

DECLARE
    v_tbl_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_tbl_count FROM dba_tables WHERE owner = 'SYSTEM' AND table_name = 'ADMIN_AUDIT_MCP_SESSIONS';
    IF v_tbl_count = 0 THEN
        EXECUTE IMMEDIATE '
        CREATE TABLE system.admin_audit_mcp_sessions (
            audit_id     NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
            logon_time   TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
            username     VARCHAR2(128) NOT NULL,
            os_user      VARCHAR2(128),
            module       VARCHAR2(64),
            machine      VARCHAR2(128),
            ip_address   VARCHAR2(64),
            session_id   NUMBER
        )';
        DBMS_OUTPUT.PUT_LINE('Tabela SYSTEM.ADMIN_AUDIT_MCP_SESSIONS criada.');
    ELSE
        DBMS_OUTPUT.PUT_LINE('Tabela SYSTEM.ADMIN_AUDIT_MCP_SESSIONS já existe.');
    END IF;
END;
/

-- Permitir que MCP_AGENT_RO consulte sua própria auditoria via sinônimo
GRANT SELECT ON system.admin_audit_mcp_sessions TO mcp_agent_ro;
CREATE OR REPLACE SYNONYM mcp_agent_ro.admin_audit_mcp_sessions FOR system.admin_audit_mcp_sessions;

-- Conceder privilégio necessário para trigger no nível de banco em PDB
GRANT ADMINISTER DATABASE TRIGGER TO system;

-- Criar trigger de logon
CREATE OR REPLACE TRIGGER system.trg_audit_mcp_agent_logon
AFTER LOGON ON DATABASE
BEGIN
    IF UPPER(SYS_CONTEXT('USERENV', 'SESSION_USER')) = 'MCP_AGENT_RO' THEN
        INSERT INTO system.admin_audit_mcp_sessions (
            username,
            os_user,
            module,
            machine,
            ip_address,
            session_id,
            logon_time
        ) VALUES (
            SYS_CONTEXT('USERENV', 'SESSION_USER'),
            SYS_CONTEXT('USERENV', 'OS_USER'),
            SYS_CONTEXT('USERENV', 'MODULE'),
            SYS_CONTEXT('USERENV', 'HOST'),
            SYS_CONTEXT('USERENV', 'IP_ADDRESS'),
            TO_NUMBER(SYS_CONTEXT('USERENV', 'SESSIONID')),
            SYSTIMESTAMP
        );
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        -- Garantir que falha em auditoria nunca impeça o logon
        NULL;
END;
/

PROMPT [06] Trigger de auditoria TRG_AUDIT_MCP_AGENT_LOGON ativado.
PROMPT [01_setup_hr_and_mcp_governance.sql] Concluído com sucesso!
