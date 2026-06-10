"""
Exportador do modulo agrosentinel (Front-End & Mobile).

O AgroSentinel calcula risco por estado e gera alertas em tempo real, mas
guarda tudo em st.session_state (nao persiste em disco). Gera um exemplo
realista com a mesma estrutura de payload (risco por estado + alertas +
decisoes HITL), marcado como "exemplo".
"""
from _contrato import RAIZ, montar_documento, salvar

MODULO_DIR = RAIZ / "agrosentinel"

RISCO_POR_ESTADO_EXEMPLO = [
    {"estado": "MT", "risk_label": "Critico", "risk_score": 0.91, "lat": -12.64, "lon": -55.42, "area_agr": 17500},
    {"estado": "PA", "risk_label": "Alto", "risk_score": 0.78, "lat": -3.41, "lon": -52.29, "area_agr": 3200},
    {"estado": "MS", "risk_label": "Alto", "risk_score": 0.72, "lat": -20.51, "lon": -54.54, "area_agr": 5200},
    {"estado": "SP", "risk_label": "Moderado", "risk_score": 0.45, "lat": -22.28, "lon": -48.73, "area_agr": 5800},
    {"estado": "MG", "risk_label": "Baixo", "risk_score": 0.18, "lat": -18.51, "lon": -44.55, "area_agr": 5500},
]

ALERTAS_EXEMPLO = [
    {
        "id": "a1b2c3d4",
        "estado": "MT",
        "risk_label": "Critico",
        "mensagem": (
            "Risco critico de queimada detectado em MT. 320 focos ativos "
            "com temperatura de 36.5C e umidade de 18%."
        ),
        "acoes": [
            "Acionar Corpo de Bombeiros e Defesa Civil estadual",
            "Emitir alerta para produtores rurais da regiao",
            "Suspender queimadas controladas autorizadas",
        ],
        "criado_em": "2026-06-09",
    },
    {
        "id": "e5f6a7b8",
        "estado": "PA",
        "risk_label": "Alto",
        "mensagem": (
            "Risco alto em PA. NDVI de 0.32 indica vegetacao estressada. "
            "Precipitacao acumulada de apenas 12 mm no periodo."
        ),
        "acoes": [
            "Notificar Defesa Civil sobre risco elevado",
            "Intensificar patrulhamento em areas de preservacao",
        ],
        "criado_em": "2026-06-09",
    },
]

DECISOES_HITL_EXEMPLO = {
    "a1b2c3d4": "confirmado",
    "e5f6a7b8": "pendente",
}


def montar_payload():
    return {
        "risco_por_estado": RISCO_POR_ESTADO_EXEMPLO,
        "alertas": ALERTAS_EXEMPLO,
        "decisoes_hitl_exemplo": DECISOES_HITL_EXEMPLO,
    }


def main():
    payload = montar_payload()

    governanca = {
        "tem_dado_pessoal": False,
        "decisao_automatizada": True,
        "tem_hitl": True,
        "auditavel": False,
        "observacoes": (
            "O loop HITL existe na interface (o usuario pode confirmar ou "
            "descartar cada alerta), mas as decisoes ficam apenas em "
            "st.session_state -- nao ha persistencia em disco nem trilha de "
            "auditoria entre sessoes, por isso auditavel=false. O modelo de "
            "risco (RandomForest) e treinado com dados sinteticos, sem "
            "validacao de vies contra dados reais de campo. O painel nao "
            "possui controle de acesso por usuario."
        ),
    }

    documento = montar_documento(
        modulo="agrosentinel",
        disciplina="Front-End & Mobile",
        proveniencia="exemplo",
        payload=payload,
        governanca=governanca,
    )
    salvar(documento)


if __name__ == "__main__":
    main()
