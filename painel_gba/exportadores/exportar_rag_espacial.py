"""
Exportador do modulo rag-espacial (IA Generativa).

O assistente (rag-espacial/app.py) responde perguntas em tempo real usando
RAG + API de terceiro na nuvem (Groq/OpenAI), sem persistir respostas em
disco. Le a lista real de documentos de exemplo
(rag-espacial/documentos_exemplo/) e gera uma pergunta/resposta de exemplo
com a mesma estrutura de rag_engine.Resposta, marcada como "exemplo".
"""
from _contrato import RAIZ, montar_documento, salvar

MODULO_DIR = RAIZ / "rag-espacial"
DOCUMENTOS_DIR = MODULO_DIR / "documentos_exemplo"

PERGUNTA_EXEMPLO = "Como satelites ajudam no monitoramento de queimadas e desastres?"

RESPOSTA_EXEMPLO = (
    "Satelites de observacao da Terra monitoram queimadas e desastres "
    "naturais ao detectar focos de calor, fumaca e mudancas na cobertura "
    "vegetal em grandes areas, com revisitas frequentes. Essas informacoes "
    "ajudam orgaos de defesa civil e equipes agricolas a priorizar regioes "
    "para resposta rapida."
)

FONTES_EXEMPLO = [
    {"origem": "satelites_monitoramento.txt", "distancia": 0.18},
    {"origem": "agricultura_clima_desastres.txt", "distancia": 0.27},
]


def listar_documentos_indexados():
    """Lista os documentos de exemplo realmente presentes na pasta do modulo."""
    if not DOCUMENTOS_DIR.exists():
        return []
    extensoes = {".txt", ".pdf", ".docx", ".md"}
    return sorted(
        arquivo.name
        for arquivo in DOCUMENTOS_DIR.iterdir()
        if arquivo.is_file() and arquivo.suffix.lower() in extensoes
    )


def montar_payload():
    return {
        "pergunta_exemplo": PERGUNTA_EXEMPLO,
        "resposta_exemplo": RESPOSTA_EXEMPLO,
        "fontes": FONTES_EXEMPLO,
        "documentos_indexados": listar_documentos_indexados(),
    }


def main():
    payload = montar_payload()

    governanca = {
        "tem_dado_pessoal": True,
        "decisao_automatizada": False,
        "tem_hitl": False,
        "auditavel": False,
        "observacoes": (
            "PONTO CRITICO (LGPD): o assistente permite upload livre de "
            "documentos pelo usuario e envia trechos desses documentos para "
            "uma API de terceiro na nuvem (Groq/OpenAI) para gerar a "
            "resposta -- sem controle sobre o conteudo enviado nem logging "
            "persistente das consultas. E um assistente de apoio a decisao "
            "(nao toma decisao automatizada). Vies linguistico: os "
            "embeddings tem melhor desempenho em ingles, o que pode reduzir "
            "a qualidade da recuperacao para conteudo em portugues."
        ),
    }

    documento = montar_documento(
        modulo="rag-espacial",
        disciplina="IA Generativa",
        proveniencia="exemplo",
        payload=payload,
        governanca=governanca,
    )
    salvar(documento)


if __name__ == "__main__":
    main()
