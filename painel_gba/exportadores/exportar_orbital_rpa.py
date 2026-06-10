"""
Exportador do modulo orbital-rpa (AI for RPA).

Tenta ler a saida real gerada pelo notebook
(orbital-rpa-mission-desk/outputs/audit_log.json e orbital_events.xlsx).
Se o notebook ainda nao foi executado (pasta outputs/ vazia), gera um
exemplo realista com a mesma estrutura, marcado como "exemplo".
"""
import json
from collections import Counter

from _contrato import RAIZ, montar_documento, salvar

MODULO_DIR = RAIZ / "orbital-rpa-mission-desk"
AUDIT_LOG_PATH = MODULO_DIR / "outputs" / "audit_log.json"
EXCEL_PATH = MODULO_DIR / "outputs" / "orbital_events.xlsx"

EVENTOS_EXEMPLO = [
    {
        "event_id": "EONET-EXEMPLO-001",
        "title": "Wildfire monitoring sample in South America",
        "category": "Wildfires",
        "risk_score": 95,
        "priority": "Alta",
        "audit_reason": "Prioridade Alta: evento da categoria Wildfires, a cerca de 850 km da posicao atual da ISS.",
    },
    {
        "event_id": "EONET-EXEMPLO-002",
        "title": "Severe storm monitoring sample in Atlantic region",
        "category": "Severe Storms",
        "risk_score": 80,
        "priority": "Alta",
        "audit_reason": "Prioridade Alta: evento da categoria Severe Storms, a cerca de 1900 km da posicao atual da ISS.",
    },
    {
        "event_id": "EONET-EXEMPLO-003",
        "title": "Volcano monitoring sample in Pacific region",
        "category": "Volcanoes",
        "risk_score": 50,
        "priority": "Media",
        "audit_reason": "Prioridade Media: evento da categoria Volcanoes, a cerca de 4200 km da posicao atual da ISS.",
    },
    {
        "event_id": "EONET-EXEMPLO-004",
        "title": "Dust and haze sample over arid region",
        "category": "Dust and Haze",
        "risk_score": 45,
        "priority": "Media",
        "audit_reason": "Prioridade Media: evento da categoria Dust and Haze, a cerca de 4800 km da posicao atual da ISS.",
    },
    {
        "event_id": "EONET-EXEMPLO-005",
        "title": "Sea and lake ice sample near polar circle",
        "category": "Sea and Lake Ice",
        "risk_score": 15,
        "priority": "Baixa",
        "audit_reason": "Prioridade Baixa: evento da categoria Sea and Lake Ice, a cerca de 9000 km da posicao atual da ISS.",
    },
]

POSICAO_ISS_EXEMPLO = {"latitude": -12.5, "longitude": -50.0, "altitude_km": 420.0}


def ler_saida_real():
    """Le audit_log.json e a posicao da ISS do orbital_events.xlsx, se existirem."""
    if not AUDIT_LOG_PATH.exists():
        return None

    with open(AUDIT_LOG_PATH, "r", encoding="utf-8") as arquivo:
        eventos = json.load(arquivo)

    posicao_iss = POSICAO_ISS_EXEMPLO
    if EXCEL_PATH.exists():
        import pandas as pd
        iss_df = pd.read_excel(EXCEL_PATH, sheet_name="posicao_iss")
        if not iss_df.empty:
            linha = iss_df.iloc[0]
            posicao_iss = {
                "latitude": float(linha["latitude"]),
                "longitude": float(linha["longitude"]),
                "altitude_km": float(linha["altitude_km"]),
            }

    return eventos, posicao_iss


def montar_payload():
    real = ler_saida_real()
    if real is not None:
        eventos, posicao_iss = real
        proveniencia = "offline"
    else:
        eventos, posicao_iss = EVENTOS_EXEMPLO, POSICAO_ISS_EXEMPLO
        proveniencia = "exemplo"

    contagem_prioridade = Counter(evento.get("priority") for evento in eventos)

    payload = {
        "total_eventos": len(eventos),
        "eventos_por_prioridade": dict(contagem_prioridade),
        "top_eventos": eventos[:5],
        "posicao_iss": posicao_iss,
    }
    return payload, proveniencia


def main():
    payload, proveniencia = montar_payload()

    governanca = {
        "tem_dado_pessoal": False,
        "decisao_automatizada": True,
        "tem_hitl": True,
        "auditavel": True,
        "observacoes": (
            "Decisao automatizada por regras explicaveis (risk_score = "
            "categoria + distancia ate a ISS + numero de fontes), mas o "
            "robo nao decide sozinho: gera uma fila priorizada para revisao "
            "humana (HITL por design). Auditavel via audit_log.json, que "
            "registra a justificativa (audit_reason) de cada item. O unico "
            "dado pessoal presente no projeto e o RM dos autores, citado no "
            "codigo-fonte do notebook, e nao faz parte dos dados "
            "processados."
        ),
    }

    documento = montar_documento(
        modulo="orbital-rpa",
        disciplina="AI for RPA",
        proveniencia=proveniencia,
        payload=payload,
        governanca=governanca,
    )
    salvar(documento)


if __name__ == "__main__":
    main()
