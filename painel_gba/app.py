"""
Painel GBA - Governanca em IA & Business Analytics

Le os arquivos padronizados em dados_integrados/*.json (um por modulo) e
apresenta o sistema integrado dos oito projetos da GS, com uma camada de
governanca (auditoria, LGPD, vies, HITL, explicabilidade) por cima de tudo.

Rodar com:
    python3.13 -m streamlit run painel_gba/app.py
"""
import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

RAIZ = Path(__file__).resolve().parents[1]
DADOS_DIR = RAIZ / "dados_integrados"

st.set_page_config(
    page_title="Painel GBA - Governanca em IA & Business Analytics",
    page_icon="🛰️",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Metadados dos modulos: nome de exibicao, disciplina, papel e camada no
# fluxo integrado. A "Governanca" e tratada como camada transversal, nao
# como uma quarta coluna de modulos.
# ---------------------------------------------------------------------------
CAMADAS_ORDEM = ["Coleta / Sensoriamento", "Previsao / Confirmacao", "Analise / Consulta"]

MODULOS = [
    {
        "slug": "orbital-rpa",
        "nome": "Orbital RPA Mission Desk",
        "disciplina": "AI for RPA",
        "papel": "Coleta de eventos (NASA EONET + posicao da ISS)",
        "camada": "Coleta / Sensoriamento",
    },
    {
        "slug": "astroguard",
        "nome": "AstroGuard",
        "disciplina": "IoT / Cognitive IoT",
        "papel": "Sensoriamento fisico do habitat (telemetria MQTT)",
        "camada": "Coleta / Sensoriamento",
    },
    {
        "slug": "neurospace-alert",
        "nome": "NeuroSpace Alert",
        "disciplina": "Computacao Neuromorfica",
        "papel": "Sensor neuromorfico de condicao critica",
        "camada": "Coleta / Sensoriamento",
    },
    {
        "slug": "quantica-mythos",
        "nome": "Quantica Mythos",
        "disciplina": "Computacao Quantica",
        "papel": "Previsao climatica (chuva extrema)",
        "camada": "Previsao / Confirmacao",
    },
    {
        "slug": "wildfire-vc",
        "nome": "Wildfire VC",
        "disciplina": "Visao Computacional",
        "papel": "Confirmacao visual de incendio em imagem de satelite",
        "camada": "Previsao / Confirmacao",
    },
    {
        "slug": "agrosentinel",
        "nome": "AgroSentinel",
        "disciplina": "Front-End & Mobile",
        "papel": "Analise de risco agroclimatico por estado + alertas HITL",
        "camada": "Analise / Consulta",
    },
    {
        "slug": "rag-espacial",
        "nome": "RAG Espacial",
        "disciplina": "IA Generativa",
        "papel": "Assistente de consulta em linguagem natural (nuvem)",
        "camada": "Analise / Consulta",
    },
    {
        "slug": "rag-net-zero",
        "nome": "RAG Net Zero",
        "disciplina": "NLP",
        "papel": "Assistente tecnico com RAG 100% local",
        "camada": "Analise / Consulta",
    },
]

PROVENIENCIA_LABEL = {
    "online": "🟢 online",
    "cache": "🔵 cache",
    "offline": "🟣 offline (dado real)",
    "exemplo": "🟠 exemplo",
}

RISCO_LABEL = {
    "Alto": "🔴 Alto",
    "Medio": "🟡 Medio",
    "Baixo": "🟢 Baixo",
}


# ---------------------------------------------------------------------------
# Carregamento dos dados
# ---------------------------------------------------------------------------
@st.cache_data
def carregar_dados():
    """Le dados_integrados/<modulo>.json para cada modulo. Retorna dict slug -> doc (ou None)."""
    dados = {}
    for modulo in MODULOS:
        caminho = DADOS_DIR / f"{modulo['slug']}.json"
        if caminho.exists():
            with open(caminho, "r", encoding="utf-8") as arquivo:
                dados[modulo["slug"]] = json.load(arquivo)
        else:
            dados[modulo["slug"]] = None
    return dados


def nivel_risco_governanca(governanca: dict) -> str:
    """Classifica o modulo em Alto/Medio/Baixo a partir das flags de governanca."""
    pontos = 0
    if governanca.get("tem_dado_pessoal"):
        pontos += 1
    if governanca.get("decisao_automatizada") and not governanca.get("tem_hitl"):
        pontos += 1
    if not governanca.get("auditavel"):
        pontos += 1
    if pontos >= 2:
        return "Alto"
    if pontos == 1:
        return "Medio"
    return "Baixo"


def resumo_payload(slug: str, payload: dict) -> str:
    """Retorna uma linha curta com o dado principal do payload de cada modulo."""
    try:
        if slug == "orbital-rpa":
            alta = payload["eventos_por_prioridade"].get("Alta", 0)
            return f"{payload['total_eventos']} eventos monitorados, {alta} de prioridade Alta"
        if slug == "astroguard":
            leitura = payload["ultima_leitura"]
            return f"Estado {leitura['estado']} | O2 {leitura['oxigenio']}% | Airlock {leitura['airlock']} ({leitura['modo']})"
        if slug == "neurospace-alert":
            rec = payload["recomendado"]
            return f"Ajuste recomendado: {rec['ajuste']} | LED final: {rec['LED_final']}"
        if slug == "quantica-mythos":
            mc, mq = payload["melhor_classico"], payload["melhor_quantico"]
            return f"Melhor classico: {mc['modelo']} (AUC {mc['AUC_ROC']}) | melhor quantico: {mq['modelo']} (AUC {mq['AUC_ROC']})"
        if slug == "wildfire-vc":
            ex = payload["exemplo_classificacao"]
            return f"Classificacao de exemplo: {ex['classe_predita']} ({ex['probabilidade'] * 100:.0f}% de confianca)"
        if slug == "agrosentinel":
            top = payload["risco_por_estado"][0]
            return f"{len(payload['alertas'])} alerta(s) ativo(s) | Maior risco: {top['estado']} ({top['risk_label']})"
        if slug == "rag-espacial":
            return f"Pergunta de exemplo: \"{payload['pergunta_exemplo']}\""
        if slug == "rag-net-zero":
            total_docs = sum(payload["categorias_corpus"].values())
            return f"{payload['total_perguntas_avaliadas']} perguntas avaliadas | corpus com {total_docs} documentos"
    except (KeyError, IndexError, TypeError):
        pass
    return "Dado principal indisponivel."


# ---------------------------------------------------------------------------
# Sidebar - filtros
# ---------------------------------------------------------------------------
dados = carregar_dados()

st.sidebar.title("Filtros")

if st.sidebar.button("🔄 Recarregar dados_integrados/"):
    carregar_dados.clear()
    st.rerun()

camadas_disponiveis = CAMADAS_ORDEM
disciplinas_disponiveis = sorted({m["disciplina"] for m in MODULOS})

filtro_camada = st.sidebar.multiselect("Camada do fluxo", camadas_disponiveis, default=camadas_disponiveis)
filtro_disciplina = st.sidebar.multiselect("Disciplina", disciplinas_disponiveis, default=disciplinas_disponiveis)
filtro_risco = st.sidebar.multiselect(
    "Risco de governanca",
    ["Alto", "Medio", "Baixo"],
    default=["Alto", "Medio", "Baixo"],
)

st.sidebar.caption(
    "O risco de governanca combina tres sinais: dado pessoal envolvido, "
    "decisao automatizada sem HITL e ausencia de trilha de auditoria."
)


def modulo_passa_filtro(modulo: dict) -> bool:
    if modulo["camada"] not in filtro_camada:
        return False
    if modulo["disciplina"] not in filtro_disciplina:
        return False
    doc = dados[modulo["slug"]]
    risco = nivel_risco_governanca(doc["governanca"]) if doc else "Alto"
    return risco in filtro_risco


modulos_filtrados = [m for m in MODULOS if modulo_passa_filtro(m)]
slugs_filtrados = {m["slug"] for m in modulos_filtrados}


# ---------------------------------------------------------------------------
# Cabecalho
# ---------------------------------------------------------------------------
st.title("🛰️ Painel GBA — Governanca em IA & Business Analytics")
st.caption(
    "Camada de integracao dos oito modulos da GS — IA para a Nova Economia "
    "Espacial / monitoramento ambiental e de risco. Cada modulo expoe sua "
    "saida em dados_integrados/<modulo>.json, seguindo um contrato de dados "
    "comum (veja painel_gba/contrato_de_dados.md)."
)

aba_visao, aba_fluxo, aba_governanca, aba_auditoria = st.tabs(
    ["Visao geral", "Fluxo de dados", "Governanca", "Auditoria"]
)


# ---------------------------------------------------------------------------
# Aba 1 - Visao geral
# ---------------------------------------------------------------------------
with aba_visao:
    st.subheader("As quatro camadas do sistema integrado")
    st.caption(
        "As tres primeiras camadas reunem os modulos do pipeline. A "
        "Governanca e uma camada transversal, aplicada sobre todas as "
        "demais (ver aba 'Governanca')."
    )

    colunas = st.columns(4)

    for indice, camada in enumerate(CAMADAS_ORDEM):
        with colunas[indice]:
            st.markdown(f"#### {camada}")
            modulos_camada = [m for m in MODULOS if m["camada"] == camada]
            for modulo in modulos_camada:
                if modulo["slug"] not in slugs_filtrados:
                    continue
                doc = dados[modulo["slug"]]
                with st.container(border=True):
                    st.markdown(f"**{modulo['nome']}**")
                    st.caption(f"{modulo['disciplina']} — {modulo['papel']}")
                    if doc is None:
                        st.warning("Modulo nao exportado ainda.")
                        continue
                    st.markdown(PROVENIENCIA_LABEL.get(doc["proveniencia"], doc["proveniencia"]))
                    st.write(resumo_payload(modulo["slug"], doc["payload"]))

    with colunas[3]:
        st.markdown("#### Governanca (camada transversal)")
        with st.container(border=True):
            st.markdown("**Auditoria · LGPD · Vies · HITL · Explicabilidade**")
            st.caption(
                "Aplicada sobre as tres camadas anteriores, sem alterar o "
                "codigo de nenhum modulo."
            )
            st.write(
                "Consulte a aba 'Governanca' para a tabela consolidada de "
                "flags por modulo e a aba 'Auditoria' para a trilha de "
                "proveniencia e timestamps."
            )

    if not modulos_filtrados:
        st.info("Nenhum modulo corresponde aos filtros selecionados na barra lateral.")


# ---------------------------------------------------------------------------
# Aba 2 - Fluxo de dados (ponta a ponta)
# ---------------------------------------------------------------------------
with aba_fluxo:
    st.subheader("Fluxo de dados de ponta a ponta")
    st.caption(
        "Demonstracao de como a saida de um modulo alimenta o proximo, ate "
        "chegar a uma consulta em linguagem natural respondida por um dos "
        "assistentes RAG. Esta aba mostra o pipeline completo, "
        "independente dos filtros da barra lateral."
    )

    def doc_de(slug):
        return dados.get(slug)

    etapas = []

    # Etapa 1 - Orbital RPA detecta evento
    doc = doc_de("orbital-rpa")
    if doc:
        evento = doc["payload"]["top_eventos"][0]
        etapas.append((
            "1. Orbital RPA Mission Desk — coleta",
            f"Evento de maior prioridade detectado: **{evento['title']}** "
            f"(categoria {evento['category']}, prioridade {evento['priority']}, "
            f"risk_score {evento['risk_score']}).",
            evento,
        ))

    # Etapa 2 - Wildfire VC confirma visualmente
    doc = doc_de("wildfire-vc")
    if doc:
        clas = doc["payload"]["exemplo_classificacao"]
        etapas.append((
            "2. Wildfire VC — confirmacao visual",
            f"Imagem de satelite da regiao classificada como "
            f"**{clas['classe_predita']}** com {clas['probabilidade'] * 100:.0f}% "
            f"de confianca, confirmando o alerta coletado na etapa 1.",
            clas,
        ))

    # Etapa 3 - AgroSentinel contextualiza risco regional
    doc = doc_de("agrosentinel")
    if doc:
        top = doc["payload"]["risco_por_estado"][0]
        alerta = doc["payload"]["alertas"][0]
        etapas.append((
            "3. AgroSentinel — contexto de risco regional",
            f"Estado **{top['estado']}** classificado com risco "
            f"**{top['risk_label']}** (score {top['risk_score']}). "
            f"Alerta gerado: \"{alerta['mensagem']}\"",
            top,
        ))

    # Etapa 4 - Quantica Mythos contextualiza previsao climatica
    doc = doc_de("quantica-mythos")
    if doc:
        mc = doc["payload"]["melhor_classico"]
        taxa = doc["payload"]["taxa_evento_extremo"]
        etapas.append((
            "4. Quantica Mythos — previsao climatica",
            f"Modelo {mc['modelo']} estima AUC {mc['AUC_ROC']} para a "
            f"classificacao de chuva extrema. Taxa historica de eventos "
            f"extremos no dataset: {taxa * 100:.1f}%. Esse contexto climatico "
            f"reforca o alerta da regiao.",
            mc,
        ))

    # Etapa 5 - RAG responde a consulta da equipe
    doc = doc_de("rag-net-zero")
    if doc:
        ex = doc["payload"]["exemplo_pergunta"]
        etapas.append((
            "5. RAG Net Zero — assistente tecnico (local)",
            f"Equipe consulta o assistente: \"{ex['pergunta']}\". "
            f"Resposta gerada com base no corpus local, citando "
            f"{len(ex['fontes_citadas'])} fonte(s).",
            ex,
        ))

    for titulo, texto, detalhe in etapas:
        with st.container(border=True):
            st.markdown(f"**{titulo}**")
            st.write(texto)
            with st.expander("Ver dado bruto desta etapa"):
                st.json(detalhe)
        st.markdown(
            "<div style='text-align:center; color:#888; margin: -8px 0 8px 0;'>⬇ alimenta a proxima etapa</div>",
            unsafe_allow_html=True,
        )

    if not etapas:
        st.info("Nenhum dado disponivel para montar o fluxo. Rode os exportadores primeiro.")


# ---------------------------------------------------------------------------
# Aba 3 - Governanca
# ---------------------------------------------------------------------------
with aba_governanca:
    st.subheader("Tabela consolidada de governanca")
    st.caption(
        "Uma linha por modulo, com as flags definidas no contrato de dados "
        "(painel_gba/contrato_de_dados.md). Filtros da barra lateral se "
        "aplicam a esta tabela."
    )

    linhas_governanca = []
    for modulo in modulos_filtrados:
        doc = dados[modulo["slug"]]
        if doc is None:
            linhas_governanca.append({
                "Modulo": modulo["nome"],
                "Disciplina": modulo["disciplina"],
                "Dado pessoal": None,
                "Decisao automatizada": None,
                "HITL": None,
                "Auditavel": None,
                "Risco": "Nao exportado",
            })
            continue
        g = doc["governanca"]
        linhas_governanca.append({
            "Modulo": modulo["nome"],
            "Disciplina": modulo["disciplina"],
            "Dado pessoal": g["tem_dado_pessoal"],
            "Decisao automatizada": g["decisao_automatizada"],
            "HITL": g["tem_hitl"],
            "Auditavel": g["auditavel"],
            "Risco": nivel_risco_governanca(g),
        })

    df_governanca = pd.DataFrame(linhas_governanca)

    if df_governanca.empty:
        st.info("Nenhum modulo corresponde aos filtros selecionados na barra lateral.")
    else:
        st.dataframe(
            df_governanca,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Dado pessoal": st.column_config.CheckboxColumn(),
                "Decisao automatizada": st.column_config.CheckboxColumn(),
                "HITL": st.column_config.CheckboxColumn(),
                "Auditavel": st.column_config.CheckboxColumn(),
            },
        )

        st.markdown("#### Pontos de governanca por modulo")
        df_flags = df_governanca.dropna(subset=["Dado pessoal"]).melt(
            id_vars=["Modulo"],
            value_vars=["Dado pessoal", "Decisao automatizada", "HITL", "Auditavel"],
            var_name="Flag",
            value_name="Valor",
        )
        df_flags["Valor"] = df_flags["Valor"].astype(int)
        fig_flags = px.bar(
            df_flags,
            x="Modulo",
            y="Valor",
            color="Flag",
            barmode="group",
            title="Flags de governanca ativas por modulo",
        )
        fig_flags.update_layout(yaxis=dict(tickvals=[0, 1], ticktext=["Nao", "Sim"]))
        st.plotly_chart(fig_flags, use_container_width=True)

    st.subheader("Pontos de governanca por modulo (detalhe)")
    for modulo in modulos_filtrados:
        doc = dados[modulo["slug"]]
        if doc is None:
            continue
        g = doc["governanca"]
        risco = nivel_risco_governanca(g)
        with st.expander(f"{RISCO_LABEL.get(risco, risco)} — {modulo['nome']} ({modulo['disciplina']})"):
            if risco == "Alto":
                st.error(g["observacoes"])
            elif risco == "Medio":
                st.warning(g["observacoes"])
            else:
                st.success(g["observacoes"])


# ---------------------------------------------------------------------------
# Aba 4 - Auditoria
# ---------------------------------------------------------------------------
with aba_auditoria:
    st.subheader("Trilha de auditoria do sistema integrado")
    st.caption(
        "Proveniencia e timestamp de exportacao de cada modulo, simulando "
        "uma trilha de auditoria do sistema integrado."
    )

    linhas_auditoria = []
    for modulo in modulos_filtrados:
        doc = dados[modulo["slug"]]
        if doc is None:
            linhas_auditoria.append({
                "Modulo": modulo["nome"],
                "Disciplina": modulo["disciplina"],
                "Proveniencia": "nao exportado",
                "Timestamp": "-",
            })
            continue
        linhas_auditoria.append({
            "Modulo": modulo["nome"],
            "Disciplina": modulo["disciplina"],
            "Proveniencia": doc["proveniencia"],
            "Timestamp": doc["timestamp"],
        })

    df_auditoria = pd.DataFrame(linhas_auditoria)

    if df_auditoria.empty:
        st.info("Nenhum modulo corresponde aos filtros selecionados na barra lateral.")
    else:
        st.dataframe(df_auditoria, use_container_width=True, hide_index=True)

        st.markdown("#### Distribuicao de proveniencia dos dados")
        fig_prov = px.pie(
            df_auditoria,
            names="Proveniencia",
            title="Proveniencia dos dados exibidos no painel",
        )
        st.plotly_chart(fig_prov, use_container_width=True)

    st.caption(
        "proveniencia: online = buscado ao vivo de API externa | cache = "
        "cache local de API | offline = saida real gerada por execucao "
        "anterior do modulo | exemplo = dado fictício usado quando o modulo "
        "ainda nao produziu saida real."
    )
