"""
Exportador do modulo astroguard (IoT / Cognitive IoT).

Tenta ler a ultima leitura de telemetria de um banco SQLite local
(astroguard/astroguard.db, gerado por uma simulacao Wokwi + Node-RED).
Se o banco nao existir (simulacao ainda nao rodou), gera um exemplo
realista com os campos publicados no topico MQTT astroguard/telemetria,
marcado como "exemplo".
"""
import sqlite3

from _contrato import RAIZ, montar_documento, salvar

MODULO_DIR = RAIZ / "astroguard"
DB_PATH = MODULO_DIR / "astroguard.db"

LEITURA_EXEMPLO = {
    "temperatura": 24.5,
    "umidade": 55.2,
    "luminosidade": 1800,
    "oxigenio": 78,
    "presenca": True,
    "noite": False,
    "estado": "NOMINAL",
    "airlock": "FECHADO",
    "modo": "AUTO",
}

RESUMO_ESTADO_EXEMPLO = {"NOMINAL": 18, "ALERTA": 4, "CRITICO": 1}

EVENTOS_AIRLOCK_EXEMPLO = [
    {
        "timestamp": "2026-06-09T20:14:00+00:00",
        "acao": "FECHAR",
        "origem": "AUTO",
        "motivo": "oxigenio abaixo de 60% (O2 critico)",
    },
    {
        "timestamp": "2026-06-09T20:32:00+00:00",
        "acao": "ABRIR",
        "origem": "MANUAL",
        "motivo": "operador assumiu controle via comando MQTT",
    },
]


def ler_saida_real():
    """Tenta ler a ultima leitura de telemetria de astroguard.db, se existir."""
    if not DB_PATH.exists():
        return None
    try:
        conexao = sqlite3.connect(str(DB_PATH))
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT temperatura, umidade, luminosidade, oxigenio, presenca, "
            "noite, estado, airlock, modo FROM telemetria ORDER BY id DESC LIMIT 1"
        )
        linha = cursor.fetchone()
        cursor.execute("SELECT estado, COUNT(*) FROM telemetria GROUP BY estado")
        resumo = dict(cursor.fetchall())
        conexao.close()
        if linha is None:
            return None
        colunas = ["temperatura", "umidade", "luminosidade", "oxigenio", "presenca", "noite", "estado", "airlock", "modo"]
        ultima_leitura = dict(zip(colunas, linha))
        ultima_leitura["presenca"] = bool(ultima_leitura["presenca"])
        ultima_leitura["noite"] = bool(ultima_leitura["noite"])
        return ultima_leitura, resumo
    except sqlite3.Error:
        return None


def montar_payload():
    real = ler_saida_real()
    if real is not None:
        ultima_leitura, resumo_estado = real
        proveniencia = "offline"
        eventos_airlock = EVENTOS_AIRLOCK_EXEMPLO
    else:
        ultima_leitura, resumo_estado = LEITURA_EXEMPLO, RESUMO_ESTADO_EXEMPLO
        proveniencia = "exemplo"
        eventos_airlock = EVENTOS_AIRLOCK_EXEMPLO

    payload = {
        "ultima_leitura": ultima_leitura,
        "resumo_estado": resumo_estado,
        "eventos_airlock": eventos_airlock,
    }
    return payload, proveniencia


def main():
    payload, proveniencia = montar_payload()

    governanca = {
        "tem_dado_pessoal": True,
        "decisao_automatizada": True,
        "tem_hitl": False,
        "auditavel": False,
        "observacoes": (
            "PONTO CRITICO: em modo AUTO o sistema fecha o airlock sozinho "
            "com base em limiares (ex.: oxigenio abaixo de 60%), sem humano "
            "no loop -- decisao automatizada de alto risco para a seguranca "
            "da tripulacao. O sensor PIR capta presenca de pessoas, o que "
            "configura dado pessoal em um cenario real. Auditoria parcial: a "
            "telemetria fica registrada, mas comandos remotos via MQTT nao "
            "guardam autoria de quem enviou. Risco de seguranca adicional: o "
            "broker MQTT (HiveMQ) e publico e sem autenticacao."
        ),
    }

    documento = montar_documento(
        modulo="astroguard",
        disciplina="IoT / Cognitive IoT",
        proveniencia=proveniencia,
        payload=payload,
        governanca=governanca,
    )
    salvar(documento)


if __name__ == "__main__":
    main()
