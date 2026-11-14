# Catálogo Mestre de Skills — Progressive Disclosure (Harness Engineering)

> **Padrão Arquitetural (Slide 11 & 12):** Evita o *Context Rot* mantendo a janela de contexto do LLM enxuta.
> O agente consulta este índice compacto para descobrir a skill adequada e carrega os detalhes completos sob demanda via `read_file` apenas quando o gatilho de ativação for satisfeito.

---

## Fluxo de Execução em 3 Etapas

```
  [ 1. DISCOVER ]               [ 2. ACTIVATE ]                [ 3. EXECUTE ]
Consultar MASTER_INDEX  --->   Carregar SKILL.md       --->   Executar Tarefa com
(Metadados leves)              (Apenas a necessária)          Restrições do Harness
```

---

## Catálogo de Skills Especializadas

| Skill | Quando Ativar (Trigger) | Arquivo da Skill | Responsabilidade Principal |
| :--- | :--- | :--- | :--- |
| **`DBA_TUNING_AUDIT`** | Diagnóstico de lentidão, queries com a tag `/* MCP_TUNING_TARGET */`, análise de planos de execução (`V$SQL_PLAN`), cardinalidade em `ALL_TAB_COL_STATISTICS` e recomendações de índices B-Tree/Bitmap. | [`SKILL_DBA_TUNING_AUDIT.md`](SKILL_DBA_TUNING_AUDIT.md) | Especialista em Otimizador Baseado em Custo (CBO) do Oracle 23ai e tuning com menor privilégio. |
| **`TOOL_OFFLOADING`** | Execução de consultas SQL que retornam mais de 50 linhas ou payloads JSON volumosos que possam exceder 1.500 tokens na janela de contexto. | [`../tools/offload_query.py`](../tools/offload_query.py) | CLI de Offloading que desvia payloads extensos para cache em disco (`offload_cache/`) e retorna resumo ao agente. |
| **`SECURITY_GOVERNANCE`** | Auditoria de acessos de IA, inspeção de triggers `AFTER LOGON` em `ADMIN_AUDIT_MCP_SESSIONS` e validação de `QUOTA 0M` em schemas corporativos. | [`../../lab-01-sqlcl-mcp/README.md`](../../lab-01-sqlcl-mcp/README.md) | Governança de acesso seguro via SQLcl MCP Server sem privilégios de `SYS`/`SYSTEM`. |

---

## Protocolo de Ativação pelo Agente de IA

1. **Varredura Inicial:** Ao receber uma solicitação do usuário, compare o objetivo com a coluna **Quando Ativar (Trigger)**.
2. **Carga Sob Demanda:** Use a ferramenta `read_file` apontando exclusivamente para o arquivo da skill correspondente.
3. **Não Carregue em Massa:** Nunca carregue múltiplas skills simultaneamente sem que haja necessidade explícita no passo atual do raciocínio.
