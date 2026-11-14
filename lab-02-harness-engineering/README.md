# Laboratório 02: Harness Engineering & Context Rot Mitigation

Implementação prática dos pilares da palestra *The APEX Dev Reinvented*:
- **Progressive Disclosure** (Slide 11 & 12): Catálogo mestre de habilidades carregadas sob demanda, evitando sobrecarga de contexto.
- **Tool Call Offloading** (Slides 13, 14 & 15): Desvio automático de consultas volumosas para persistência em disco, retornando ao agente apenas metadados, resumo e amostra inicial.

---

## 1. Estrutura de Arquivos

```
lab-02-harness-engineering/
├── README.md                                 # Esta documentação
├── skills/
│   ├── MASTER_INDEX.md                       # Catálogo de Progressive Disclosure
│   └── SKILL_DBA_TUNING_AUDIT.md             # Instrução declarativa de tuning CBO
├── tools/
│   └── offload_query.py                      # CLI de Tool Call Offloading
└── offload_cache/                            # Dumps em disco gerados pelo offloading (ignorado no git)
```

---

## 2. Como Acionar o `MASTER_INDEX.md` no Prompt do Agente

Em vez de carregar todas as regras e especificações do sistema de uma vez na janela de contexto, instrua o agente a consultar o índice mestre:

### Exemplo de Prompt (Progressive Disclosure):
> *"Consulte o catálogo mestre em `lab-02-harness-engineering/skills/MASTER_INDEX.md`. Identifique a skill adequada para diagnosticar consultas marcadas com `/* MCP_TUNING_TARGET */` no banco Oracle 23ai. Em seguida, ative essa skill específica e apresente o diagnóstico do plano de execução da tabela `EMPLOYEE_ACTIVITY_LOGS` seguindo rigorosamente as restrições e o template padronizado."*

O agente executará:
1. **DISCOVER:** Lê o `MASTER_INDEX.md` (~300 tokens).
2. **ACTIVATE:** Carrega `SKILL_DBA_TUNING_AUDIT.md` apenas quando o gatilho for detectado.
3. **EXECUTE:** Executa a auditoria no MCP Server respeitando as restrições declaradas.

---

## 3. Como Testar o `tools/offload_query.py` (Tool Call Offloading)

O script `offload_query.py` conecta como `MCP_AGENT_RO` (`localhost:1521/FREEPDB1`) em modo thin via `oracledb`.

A fórmula aplicada para estimativa de tokens é:
$$\text{Tokens} = \left\lceil \frac{\text{len(JSON)}}{4} \right\rceil$$

### Teste A: Consulta Pequena (< 1.500 Tokens — Retorno Direto)
```bash
.\.venv\Scripts\python.exe lab-02-harness-engineering/tools/offload_query.py "SELECT * FROM departments"
```
- **Comportamento:** O resultado JSON é exibido diretamente no `stdout`, pois cabe com folga na janela de contexto.

---

### Teste B: Consulta Volumosa (>= 1.500 Tokens — Disparo de Offloading)
```bash
.\.venv\Scripts\python.exe lab-02-harness-engineering/tools/offload_query.py "SELECT * FROM employee_activity_logs FETCH FIRST 500 ROWS ONLY"
```
- **Comportamento:**
  - O volume de 500 linhas gera ~70.000 caracteres (~17.500 tokens).
  - O script intercepta a saída e persiste o JSON completo em `lab-02-harness-engineering/offload_cache/dump_<timestamp>.json`.
  - O `stdout` recebe apenas um payload enxuto com status `OFFLOADED_TO_DISK`, métricas, caminho do arquivo e as 5 primeiras linhas como amostra.
