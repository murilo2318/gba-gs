# Contrato de dados — GBA (Governança em IA & Business Analytics)

Este documento define o formato único que todos os módulos do projeto seguem
para expor seus resultados ao painel orquestrador (`painel_gba/app.py`).

Cada módulo gera **um único arquivo** em `dados_integrados/<modulo>.json`,
seguindo exatamente esta estrutura:

```json
{
  "modulo": "orbital-rpa",
  "disciplina": "AI for RPA",
  "timestamp": "2026-06-09T23:50:00+00:00",
  "proveniencia": "online | cache | offline | exemplo",
  "payload": {
    "...": "dados específicos do módulo, ver detalhes abaixo"
  },
  "governanca": {
    "tem_dado_pessoal": false,
    "decisao_automatizada": true,
    "tem_hitl": true,
    "auditavel": true,
    "observacoes": "texto curto sobre o ponto de governança do módulo"
  }
}
```

## Campos do nível raiz

| Campo | Tipo | Descrição |
|---|---|---|
| `modulo` | string | slug curto do módulo (ex.: `orbital-rpa`) |
| `disciplina` | string | nome da disciplina FIAP correspondente |
| `timestamp` | string ISO-8601 | momento em que o exportador gerou o arquivo |
| `proveniencia` | string | `online` (dado buscado ao vivo de API externa), `cache` (dado de cache local de API), `offline` (saída real gerada por execução anterior do módulo, lida do disco), `exemplo` (dado fictício, usado quando o módulo ainda não produziu saída real) |
| `payload` | objeto | dados específicos do módulo (ver seção "Payload por módulo") |
| `governanca` | objeto | flags e observações de governança (ver seção "Bloco de governança") |

## Bloco de governança

| Campo | Tipo | Descrição |
|---|---|---|
| `tem_dado_pessoal` | bool | o módulo manipula dado pessoal (LGPD) em algum ponto? |
| `decisao_automatizada` | bool | o módulo toma alguma decisão sem intervenção humana? |
| `tem_hitl` | bool | existe um ponto de revisão humana (Human-in-the-Loop)? |
| `auditavel` | bool | existe trilha/registro que permite auditar a decisão? |
| `observacoes` | string | ponto de governança crítico e específico do módulo |

## Payload por módulo

### `orbital-rpa` (AI for RPA)
Espelha `outputs/audit_log.json` e a aba `eventos_priorizados` de
`outputs/orbital_events.xlsx`.

```json
{
  "total_eventos": 8,
  "eventos_por_prioridade": {"Alta": 3, "Media": 4, "Baixa": 1},
  "top_eventos": [
    {
      "event_id": "EONET-...",
      "title": "...",
      "category": "Wildfires",
      "risk_score": 78,
      "priority": "Alta",
      "audit_reason": "Prioridade Alta: evento da categoria ..., a cerca de ... km da ISS."
    }
  ],
  "posicao_iss": {"latitude": -12.5, "longitude": -50.0, "altitude_km": 420.0}
}
```

### `astroguard` (IoT / Cognitive IoT)
Espelha o JSON publicado no tópico MQTT `astroguard/telemetria` e o status
de `astroguard/status`.

```json
{
  "ultima_leitura": {
    "temperatura": 24.5, "umidade": 55.2, "luminosidade": 1800,
    "oxigenio": 78, "presenca": true, "noite": false,
    "estado": "NOMINAL", "airlock": "FECHADO", "modo": "AUTO"
  },
  "resumo_estado": {"NOMINAL": 18, "ALERTA": 4, "CRITICO": 1},
  "eventos_airlock": [
    {"timestamp": "...", "acao": "FECHAR", "origem": "AUTO", "motivo": "oxigenio < 60%"}
  ]
}
```

### `neurospace-alert` (Computação Neuromórfica)
Extraído de `resultados/resumo_execucao.json` (dado real).

```json
{
  "dataset_rows": 61,
  "primeira_atencao_real_min": 155,
  "primeira_critica_real_min": 200,
  "recomendado": {"grupo": "Alterado", "ajuste": "Ajuste_B_equilibrado_alterado", "...": "..."},
  "resumos": ["lista resumida dos 6 ajustes simulados"],
  "comparacao": ["lista de deltas entre original e alterado"]
}
```

### `quantica-mythos` (Computação Quântica)
Extraído de `data/results.json` (dado real).

```json
{
  "n_total_dataset": 21912,
  "taxa_evento_extremo": 0.0439,
  "coorte": 500,
  "teste": 150,
  "tabela": ["métricas dos 4 modelos: QSVC, VQC, SVM-RBF, Random Forest"],
  "melhor_classico": {"modelo": "SVM-RBF (clássico)", "AUC_ROC": 0.7257},
  "melhor_quantico": {"modelo": "VQC (quântico)", "AUC_ROC": 0.4802}
}
```

### `wildfire-vc` (Visão Computacional)
Notebook ainda não executado — exemplo realista baseado na arquitetura
descrita (MobileNetV2, classes `Wildfire` / `No Wildfire`).

```json
{
  "classes": ["Wildfire", "No Wildfire"],
  "metricas_exemplo": {"accuracy": 0.93, "precision": 0.91, "recall": 0.89, "f1": 0.90, "auc": 0.96},
  "exemplo_classificacao": {"imagem": "wildfire_0021.jpg", "classe_predita": "Wildfire", "probabilidade": 0.94}
}
```

### `agrosentinel` (Front-End & Mobile)
Estado vive em `st.session_state`, sem persistência — exemplo baseado em
`pipelines/risk_pipeline.py` e `pipelines/alert_pipeline.py`.

```json
{
  "risco_por_estado": [
    {"estado": "MT", "risk_label": "Alto", "risk_score": 0.81, "lat": -12.64, "lon": -55.42, "area_agr": 17500}
  ],
  "alertas": [
    {"id": "a1b2c3d4", "estado": "MT", "risk_label": "Alto", "mensagem": "...", "acoes": ["..."], "criado_em": "2026-06-09"}
  ],
  "decisoes_hitl_exemplo": {"a1b2c3d4": "pendente"}
}
```

### `rag-espacial` (IA Generativa)
Sem persistência de respostas — exemplo baseado em `rag_engine.Resposta`.

```json
{
  "pergunta_exemplo": "Como satélites ajudam no monitoramento de queimadas?",
  "resposta_exemplo": "...",
  "fontes": [{"origem": "satelites_monitoramento.txt", "distancia": 0.21}],
  "documentos_indexados": ["agricultura_clima_desastres.txt", "satelites_monitoramento.txt"]
}
```

### `rag-net-zero` (NLP)
Extraído de `outputs/avaliacao.json` (dado real).

```json
{
  "total_perguntas_avaliadas": 10,
  "exemplo_pergunta": {
    "pergunta": "O que e definido como aguas cinzas...",
    "resposta_resumida": "...",
    "fontes_citadas": [{"titulo": "...", "fonte": "...", "score": 0.86}]
  },
  "categorias_corpus": {"energia": 6, "agua": 3, "geral": 4}
}
```

## Como adicionar um novo módulo

1. Criar `painel_gba/exportadores/exportar_<modulo>.py` seguindo o mesmo
   padrão dos demais (ler saída real se existir, senão gerar exemplo).
2. Adicionar o novo módulo na lista de `painel_gba/exportadores/exportar_todos.py`.
3. Escrever `dados_integrados/<modulo>.json` seguindo este contrato.
4. O painel (`painel_gba/app.py`) lê automaticamente todos os arquivos em
   `dados_integrados/*.json` — não é necessário alterar o app, exceto para
   posicionar o novo módulo na camada correta da Visão Geral.
