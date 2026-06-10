# Painel GBA — Governanca em IA & Business Analytics

Camada de integracao que reune os oito modulos da GS "Solucoes de IA para a
Nova Economia Espacial / monitoramento ambiental e de risco" em um sistema
unico, conectado por um contrato de dados comum e apresentado em um painel
Streamlit com uma camada de governanca (auditoria, LGPD, vies, HITL,
explicabilidade).

> Nenhum arquivo das oito pastas originais dos modulos foi alterado. Tudo o
> que foi criado para esta integracao vive em `dados_integrados/` e
> `painel_gba/`.

## Estrutura

```
gba-gs/
├── dados_integrados/            # JSONs padronizados, um por modulo
├── painel_gba/
│   ├── app.py                   # painel Streamlit (orquestrador)
│   ├── contrato_de_dados.md     # schema do contrato de dados comum
│   ├── requirements.txt
│   ├── README.md                # este arquivo
│   └── exportadores/
│       ├── _contrato.py         # funcoes utilitarias compartilhadas
│       ├── exportar_<modulo>.py # um exportador por modulo
│       └── exportar_todos.py    # roda todos os exportadores
└── <oito pastas dos modulos>/   # nao alteradas
```

## Como rodar

A partir da pasta `gba-gs/`:

```bash
python3.13 -m pip install -r painel_gba/requirements.txt

# (opcional) gera/atualiza dados_integrados/*.json a partir das saidas reais
python3.13 painel_gba/exportadores/exportar_todos.py

# abre o painel
python3.13 -m streamlit run painel_gba/app.py
```

O painel funciona mesmo sem rodar os exportadores antes, pois
`dados_integrados/` ja vem com um JSON por modulo (gerado na primeira
implementacao). Rode `exportar_todos.py` sempre que quiser atualizar os
dados — por exemplo, depois de executar um dos notebooks ou a simulacao do
AstroGuard.

## O contrato de dados

Cada modulo expoe sua saida em `dados_integrados/<modulo>.json`, no formato:

```json
{
  "modulo": "orbital-rpa",
  "disciplina": "AI for RPA",
  "timestamp": "ISO-8601",
  "proveniencia": "online | cache | offline | exemplo",
  "payload": { "...": "dados especificos do modulo" },
  "governanca": {
    "tem_dado_pessoal": false,
    "decisao_automatizada": true,
    "tem_hitl": true,
    "auditavel": true,
    "observacoes": "ponto de governanca critico do modulo"
  }
}
```

Detalhes do payload de cada modulo e dos valores de `proveniencia` estao em
[`contrato_de_dados.md`](contrato_de_dados.md).

### Proveniencia dos dados atuais

| Modulo | Proveniencia | Origem |
|---|---|---|
| orbital-rpa | `exemplo` | notebook ainda nao executado nesta maquina |
| astroguard | `exemplo` | simulacao Wokwi/Node-RED ainda nao gerou `astroguard.db` |
| neurospace-alert | `offline` | `resultados/resumo_execucao.json` real |
| quantica-mythos | `offline` | `data/results.json` real |
| wildfire-vc | `exemplo` | notebook ainda nao executado nesta maquina |
| agrosentinel | `exemplo` | dados ficam em `st.session_state`, sem persistencia |
| rag-espacial | `exemplo` | assistente nao persiste respostas |
| rag-net-zero | `offline` | `outputs/avaliacao.json` real |

Quando `orbital-rpa`, `wildfire-vc` ou `astroguard` gerarem suas saidas reais
(rodando o notebook/simulacao correspondente), basta rodar
`exportar_todos.py` novamente: os exportadores ja sabem ler o arquivo real e
trocar `proveniencia` para `offline` automaticamente.

## As quatro abas do painel

- **Visao geral** — as quatro camadas do sistema (Coleta/Sensoriamento,
  Previsao/Confirmacao, Analise/Consulta e Governanca como camada
  transversal), com um card por modulo mostrando estado, proveniencia e o
  dado principal do payload.
- **Fluxo de dados** — demonstracao ponta a ponta: um evento coletado pelo
  Orbital RPA, confirmado pelo Wildfire VC, contextualizado pelo
  AgroSentinel e pela Quantica Mythos, e consultado via RAG Net Zero.
- **Governanca** — tabela consolidada com as flags de governanca de todos os
  modulos, grafico de barras com os pontos de governanca por modulo, e o
  detalhe (`observacoes`) de cada modulo, destacando os pontos criticos.
- **Auditoria** — proveniencia e timestamp de cada modulo, com grafico da
  distribuicao de proveniencia (online/cache/offline/exemplo).

A barra lateral permite filtrar por camada do fluxo, disciplina e nivel de
risco de governanca (Alto/Medio/Baixo, calculado a partir das flags de cada
modulo).

## Como adicionar um novo modulo no futuro

1. Crie `painel_gba/exportadores/exportar_<novo_modulo>.py`, seguindo o
   padrao dos demais: leia a saida real do modulo se ela existir (marcando
   `proveniencia: "offline"`), ou gere um exemplo realista
   (`proveniencia: "exemplo"`) caso contrario. Use as funcoes de
   `_contrato.py` (`montar_documento` e `salvar`) para gravar o resultado.
2. Adicione o novo exportador a lista `EXPORTADORES` em
   `exportar_todos.py`.
3. Adicione o novo modulo a lista `MODULOS` em `app.py`, definindo `slug`,
   `nome`, `disciplina`, `papel` e `camada` (uma das tres camadas do
   pipeline).
4. (Opcional) Adicione um caso em `resumo_payload()` para definir qual dado
   do payload aparece no card da Visao Geral.
5. Documente o payload do novo modulo em `contrato_de_dados.md`.
