"""
Exportador do modulo quantica-mythos (Computacao Quantica).

Le os resultados reais gerados pelo notebook
(GS2026_CQ_2TIAP_Mythos/data/results.json) e converte para o contrato de
dados comum do painel GBA. Destaca o melhor modelo classico vs. o melhor
modelo quantico, para a transparencia anti "quantum-washing".
"""
import json

from _contrato import RAIZ, montar_documento, salvar

MODULO_DIR = RAIZ / "GS2026_CQ_2TIAP_Mythos"
RESULTS_PATH = MODULO_DIR / "data" / "results.json"


def melhor_modelo(tabela, palavra_chave):
    candidatos = [linha for linha in tabela if palavra_chave in linha["modelo"].lower()]
    return max(candidatos, key=lambda linha: linha["AUC_ROC"]) if candidatos else None


def montar_payload():
    with open(RESULTS_PATH, "r", encoding="utf-8") as arquivo:
        results = json.load(arquivo)

    tabela = results.get("tabela", [])

    return {
        "n_total_dataset": results.get("n_total_dataset"),
        "taxa_evento_extremo": results.get("taxa_evento_extremo"),
        "coorte": results.get("coorte"),
        "treino_quantico_pos_smote": results.get("treino_quantico_pos_smote"),
        "teste": results.get("teste"),
        "n_qubits": results.get("n_qubits"),
        "tabela": tabela,
        "melhor_classico": melhor_modelo(tabela, "clássico"),
        "melhor_quantico": melhor_modelo(tabela, "quântico"),
    }


def main():
    payload = montar_payload()

    governanca = {
        "tem_dado_pessoal": False,
        "decisao_automatizada": True,
        "tem_hitl": False,
        "auditavel": True,
        "observacoes": (
            "Transparencia critica anti 'quantum-washing': os resultados "
            "mostram desempenho inferior dos modelos quanticos (QSVC e VQC, "
            "AUC_ROC ~0.46-0.48) em relacao aos modelos classicos (SVM-RBF "
            "AUC_ROC ~0.73), e isso e reportado de forma explicita em vez de "
            "ser omitido. Decisao automatizada (classificacao de chuva "
            "extrema) e reprodutivel: seed fixa e metricas registradas em "
            "results.json."
        ),
    }

    documento = montar_documento(
        modulo="quantica-mythos",
        disciplina="Computacao Quantica",
        proveniencia="offline",
        payload=payload,
        governanca=governanca,
    )
    salvar(documento)


if __name__ == "__main__":
    main()
