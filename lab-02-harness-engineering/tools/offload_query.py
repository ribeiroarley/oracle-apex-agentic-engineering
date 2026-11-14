#!/usr/bin/env python3
"""
tools/offload_query.py
Laboratório 02: Harness Engineering & Context Rot Mitigation
Implementação de Tool Call Offloading (Slides 13, 14 e 15 da palestra APEX).

Conecta ao Oracle Database 23ai Free via oracledb (thin mode) como MCP_AGENT_RO.
Executa a consulta SQL fornecida e calcula a estimativa de tokens:
    tokens = CEIL(len(output_json) / 4)

- Se tokens < 1500: Retorna o JSON completo diretamente no stdout.
- Se tokens >= 1500: Salva o JSON completo em offload_cache/dump_<timestamp>.json
  e retorna ao agente apenas um resumo estruturado (Summary + File Pointer).
"""

import argparse
import datetime
import decimal
import json
import math
import os
import sys
from pathlib import Path

try:
    import oracledb
except ImportError:
    print(
        json.dumps(
            {
                "error": "Biblioteca oracledb não encontrada. Instale com: pip install oracledb"
            }
        ),
        file=sys.stderr,
    )
    sys.exit(1)


def custom_json_serializer(obj):
    """Serializador para tipos Oracle não suportados nativamente pelo json."""
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    if isinstance(obj, decimal.Decimal):
        return float(obj) if obj % 1 else int(obj)
    if hasattr(obj, "read"):  # LOB objects
        return obj.read()
    raise TypeError(f"Tipo {type(obj)} não é serializável em JSON")


def get_default_connection_params():
    """Lê credenciais de variáveis de ambiente ou utiliza os padrões do lab-01."""
    return {
        "user": os.getenv("MCP_RO_USER", "mcp_agent_ro"),
        "password": os.getenv("MCP_RO_PWD", "McpReadOnly2026!"),
        "host": os.getenv("ORACLE_HOST", "localhost"),
        "port": int(os.getenv("ORACLE_PORT", 1521)),
        "service_name": os.getenv("ORACLE_PDB", "FREEPDB1"),
    }


def execute_query(sql_query: str, params: dict) -> list:
    """Executa a query no Oracle 23ai em modo Thin e retorna lista de dicionários."""
    dsn = f"{params['host']}:{params['port']}/{params['service_name']}"
    connection = oracledb.connect(
        user=params["user"],
        password=params["password"],
        dsn=dsn,
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            if not cursor.description:
                return []

            columns = [col[0].lower() for col in cursor.description]
            rows = cursor.fetchall()
            result = [dict(zip(columns, row)) for row in rows]
            return result
    finally:
        connection.close()


def main():
    parser = argparse.ArgumentParser(
        description="Tool Call Offloading CLI para Oracle Database (Context Rot Mitigation)"
    )
    parser.add_argument(
        "query",
        nargs="?",
        type=str,
        help="Instrução SQL a executar (ou forneça via --query)",
    )
    parser.add_argument(
        "--query",
        dest="query_opt",
        type=str,
        help="Instrução SQL a executar",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=1500,
        help="Limite de tokens para disparo do offloading (padrão: 1500 tokens)",
    )
    parser.add_argument(
        "--cache-dir",
        type=str,
        default=None,
        help="Diretório para armazenamento de cache offload",
    )

    args = parser.parse_args()
    sql_query = args.query or args.query_opt

    if not sql_query:
        print(
            json.dumps(
                {
                    "error": "Nenhuma query fornecida. Exemplo: python offload_query.py 'SELECT * FROM employee_activity_logs FETCH FIRST 100 ROWS ONLY'"
                }
            ),
            file=sys.stderr,
        )
        sys.exit(1)

    # 1. Obter parâmetros de conexão
    conn_params = get_default_connection_params()

    # 2. Executar consulta
    try:
        records = execute_query(sql_query, conn_params)
    except Exception as exc:
        err_payload = {
            "status": "ERROR",
            "error_type": type(exc).__name__,
            "message": str(exc),
            "sql_query": sql_query,
        }
        print(json.dumps(err_payload, indent=2, ensure_ascii=False))
        sys.exit(1)

    # 3. Serializar resultado para JSON
    json_text = json.dumps(records, default=custom_json_serializer, ensure_ascii=False)

    # 4. Estimar consumo de tokens: CEIL(len(output) / 4) — Slide 15
    estimated_tokens = math.ceil(len(json_text) / 4)
    threshold = args.threshold

    # 5. Avaliação do limiar de Offloading
    if estimated_tokens < threshold:
        # Retorno Direto (Direct Return) — o payload cabe com segurança na janela
        sys.stdout.write(json_text + "\n")
        sys.exit(0)
    else:
        # Offload disparado! Salvar payload completo em disco e retornar apenas ponteiro + resumo
        base_dir = (
            Path(args.cache_dir)
            if args.cache_dir
            else Path(__file__).resolve().parent.parent / "offload_cache"
        )
        base_dir.mkdir(parents=True, exist_ok=True)

        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        dump_filename = f"dump_{timestamp_str}.json"
        dump_filepath = base_dir / dump_filename

        with open(dump_filepath, "w", encoding="utf-8") as f:
            f.write(json_text)

        # Preparar amostra das 5 primeiras linhas
        sample_rows = records[:5]
        tokens_saved = estimated_tokens

        summary_payload = {
            "status": "OFFLOADED_TO_DISK",
            "architecture_pattern": "Tool Call Offloading (Slide 15 - APEX Dev Reinvented)",
            "context_rot_mitigation": {
                "threshold_tokens": threshold,
                "estimated_tokens_generated": estimated_tokens,
                "tokens_saved_from_context": tokens_saved,
            },
            "metrics": {
                "total_rows_returned": len(records),
                "cache_file_bytes": os.path.getsize(dump_filepath),
                "cache_file_path": str(dump_filepath.resolve()).replace("\\", "/"),
            },
            "sample_first_5_rows": sample_rows,
            "instructions_for_agent": (
                f"O resultado excedeu {threshold} tokens e foi persistido em disco para evitar saturação "
                f"da janela de contexto (Context Rot). Utilize ferramentas de arquivo direcionadas "
                f"(ex: read_file com paginação ou scripts de processamento) no arquivo "
                f"'{dump_filepath.name}' se necessitar inspecionar registros específicos."
            ),
        }

        print(
            json.dumps(
                summary_payload,
                indent=2,
                ensure_ascii=False,
                default=custom_json_serializer,
            )
        )
        sys.exit(0)


if __name__ == "__main__":
    main()
