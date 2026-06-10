"""
Exportador do modulo neurospace-alert (Computacao Neuromorfica).

Le o resumo real de execucao gerado pelo notebook
(neurospace-alert/resultados/resumo_execucao.json) e converte para o
contrato de dados comum do painel GBA.
"""
import json

from _contrato import RAIZ, montar_documento, salvar

MODULO_DIR = RAIZ / "neurospace-alert"
RESUMO_PATH = MODULO_DIR / "resultados" / "resumo_execucao.json"


def montar_payload():
    with open(RESUMO_PATH, "r", encoding="utf-8") as arquivo:
        resumo = json.load(arquivo)

    return {
        "dataset_rows": resumo.get("dataset_rows"),
        "primeira_atencao_real_min": resumo.get("primeira_atencao_real_min"),
        "primeira_critica_real_min": resumo.get("primeira_critica_real_min"),
        "recomendado": resumo.get("recomendado"),
        "resumos": resumo.get("resumos", []),
        "comparacao": resumo.get("comparacao", []),
    }


def main():
    payload = montar_payload()

    governanca = {
        "tem_dado_pessoal": False,
        "decisao_automatizada": True,
        "tem_hitl": False,
        "auditavel": True,
        "observacoes": (
            "Decisao automatizada: o LED de alerta (NOMINAL/ALERTA/CRITICO) e "
            "acionado por um limiar de tensao (V_limiar) fixo, sem revisao "
            "humana antes do acionamento. Os limiares sao definidos por "
            "design da equipe, o que representa um vies de design embutido "
            "no sistema. Auditavel: tabelas comparativas (ajuste original vs. "
            "alterado) registram o efeito de cada calibracao testada."
        ),
    }

    documento = montar_documento(
        modulo="neurospace-alert",
        disciplina="Computacao Neuromorfica",
        proveniencia="offline",
        payload=payload,
        governanca=governanca,
    )
    salvar(documento)


if __name__ == "__main__":
    main()
