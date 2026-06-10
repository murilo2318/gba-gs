"""
Funcoes utilitarias compartilhadas pelos exportadores do painel GBA.

Cada exportador monta um dicionario seguindo o contrato definido em
painel_gba/contrato_de_dados.md e usa as funcoes daqui para gravar o
arquivo em dados_integrados/<modulo>.json de forma padronizada.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

# gba-gs/ (pasta-mae do projeto)
RAIZ = Path(__file__).resolve().parents[2]
DADOS_INTEGRADOS = RAIZ / "dados_integrados"


def agora_iso() -> str:
    """Timestamp atual em ISO-8601 (UTC)."""
    return datetime.now(timezone.utc).isoformat()


def montar_documento(modulo: str, disciplina: str, proveniencia: str, payload: dict, governanca: dict) -> dict:
    """Monta o documento no formato do contrato de dados comum."""
    return {
        "modulo": modulo,
        "disciplina": disciplina,
        "timestamp": agora_iso(),
        "proveniencia": proveniencia,
        "payload": payload,
        "governanca": governanca,
    }


def salvar(documento: dict) -> Path:
    """Grava o documento em dados_integrados/<modulo>.json."""
    DADOS_INTEGRADOS.mkdir(parents=True, exist_ok=True)
    destino = DADOS_INTEGRADOS / f"{documento['modulo']}.json"
    with open(destino, "w", encoding="utf-8") as arquivo:
        json.dump(documento, arquivo, ensure_ascii=False, indent=2)
    print(f"[ok] {documento['modulo']:18s} -> {destino.relative_to(RAIZ)}  (proveniencia={documento['proveniencia']})")
    return destino
