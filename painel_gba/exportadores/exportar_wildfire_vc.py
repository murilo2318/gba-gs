"""
Exportador do modulo wildfire-vc (Visao Computacional).

O notebook (gs-vc-wildfire-monitoramento/) treina um classificador binario
(Wildfire / No Wildfire) com MobileNetV2, mas ainda nao foi executado neste
ambiente -- nao ha metricas persistidas em disco. Gera um exemplo realista
com a mesma estrutura de saida (classes, metricas e uma classificacao de
exemplo), marcado como "exemplo".
"""
from _contrato import RAIZ, montar_documento, salvar

MODULO_DIR = RAIZ / "gs-vc-wildfire-monitoramento"

CLASSES = ["Wildfire", "No Wildfire"]

METRICAS_EXEMPLO = {
    "accuracy": 0.93,
    "precision": 0.91,
    "recall": 0.89,
    "f1": 0.90,
    "auc": 0.96,
}

CLASSIFICACAO_EXEMPLO = {
    "imagem": "wildfire_0021.jpg",
    "classe_predita": "Wildfire",
    "probabilidade": 0.94,
}


def montar_payload():
    return {
        "classes": CLASSES,
        "metricas_exemplo": METRICAS_EXEMPLO,
        "exemplo_classificacao": CLASSIFICACAO_EXEMPLO,
    }


def main():
    payload = montar_payload()

    governanca = {
        "tem_dado_pessoal": False,
        "decisao_automatizada": True,
        "tem_hitl": False,
        "auditavel": False,
        "observacoes": (
            "HITL e logging das decisoes de classificacao sao mencionados na "
            "proposta do projeto, mas NAO estao implementados no notebook "
            "atual -- por isso tem_hitl=false e auditavel=false refletem o "
            "estado real. Vies de classes mitigado parcialmente via "
            "class_weight balanceado no treino. Para este caso de uso, o "
            "falso negativo (classificar uma imagem com incendio real como "
            "'No Wildfire') e o erro mais grave, pois atrasa a resposta a um "
            "evento critico."
        ),
    }

    documento = montar_documento(
        modulo="wildfire-vc",
        disciplina="Visao Computacional",
        proveniencia="exemplo",
        payload=payload,
        governanca=governanca,
    )
    salvar(documento)


if __name__ == "__main__":
    main()
