"""
Exportador do modulo rag-net-zero (NLP).

Le a avaliacao real do RAG local (rag-net-zero/outputs/avaliacao.json) e a
estrutura do corpus (rag-net-zero/corpus/<categoria>/) e converte para o
contrato de dados comum do painel GBA.
"""
import json

from _contrato import RAIZ, montar_documento, salvar

MODULO_DIR = RAIZ / "rag-net-zero"
AVALIACAO_PATH = MODULO_DIR / "outputs" / "avaliacao.json"
CORPUS_DIR = MODULO_DIR / "corpus"

LIMITE_RESUMO = 400


def contar_documentos_corpus():
    """Conta arquivos de documento por categoria em corpus/<categoria>/."""
    categorias = {}
    if not CORPUS_DIR.exists():
        return categorias
    for pasta in sorted(CORPUS_DIR.iterdir()):
        if pasta.is_dir():
            arquivos = [f for f in pasta.iterdir() if f.is_file() and not f.name.startswith(".")]
            categorias[pasta.name] = len(arquivos)
    return categorias


def montar_payload():
    with open(AVALIACAO_PATH, "r", encoding="utf-8") as arquivo:
        avaliacao = json.load(arquivo)

    primeira = avaliacao[0]
    resposta = primeira.get("resposta_rag", "")
    resposta_resumida = resposta[:LIMITE_RESUMO] + ("..." if len(resposta) > LIMITE_RESUMO else "")

    return {
        "total_perguntas_avaliadas": len(avaliacao),
        "exemplo_pergunta": {
            "pergunta": primeira.get("pergunta"),
            "resposta_resumida": resposta_resumida,
            "fontes_citadas": primeira.get("fontes_citadas", []),
        },
        "categorias_corpus": contar_documentos_corpus(),
    }


def main():
    payload = montar_payload()

    governanca = {
        "tem_dado_pessoal": False,
        "decisao_automatizada": False,
        "tem_hitl": True,
        "auditavel": True,
        "observacoes": (
            "RAG 100% local via Ollama (privacy by design): nenhum trecho de "
            "documento e enviado a API externa. Auditavel via "
            "outputs/avaliacao.json, que registra pergunta, resposta e "
            "fontes recuperadas. HITL existe apenas na etapa de avaliacao "
            "das respostas (revisao humana do avaliacao.json), nao em tempo "
            "de execucao do assistente. Vies de corpus documentado: corpus "
            "tem mais documentos sobre energia do que sobre agua, o que pode "
            "enviesar respostas comparativas."
        ),
    }

    documento = montar_documento(
        modulo="rag-net-zero",
        disciplina="NLP",
        proveniencia="offline",
        payload=payload,
        governanca=governanca,
    )
    salvar(documento)


if __name__ == "__main__":
    main()
