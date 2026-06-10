# GS 2026.1 — Governança em IA & Business Analytics

Projeto integrador da Global Solution 2026.1 do curso Tecnólogo em Inteligência Artificial (FIAP, turma 2TIAP). Esta entrega reúne os oito projetos desenvolvidos nas demais disciplinas do semestre e os integra em um sistema único, sob uma camada de governança, no tema "Soluções de IA para a Nova Economia Espacial".

## Integrantes

| Nome | RM |
| --- | --- |
| Murilo de Faria Benhossi | 562358 |
| Luis Fernando de Oliveira Salgado | 561401 |
| Nícolas Lemos Ribeiro | 553273 |

## Sobre o projeto

Cada disciplina do semestre entregou uma Global Solution própria, com tema e tecnologia distintos. Esta GS de Governança em IA & Business Analytics tem um papel diferente: em vez de criar mais um projeto isolado, ela conecta os oito módulos existentes em um fluxo único e aplica sobre eles uma camada de governança — auditoria, rastreabilidade, verificação de privacidade (LGPD), registro de viés, validação humana (HITL) e explicabilidade.

A integração é feita por contrato de dados: cada módulo expõe sua saída em um formato JSON padronizado, depositado na pasta `dados_integrados/`. Um painel orquestrador em Streamlit lê todas essas saídas, demonstra o fluxo de ponta a ponta e consolida a governança de todos os módulos em uma única interface.

## Os oito módulos integrados

| Módulo | Disciplina | Papel no sistema |
| --- | --- | --- |
| Orbital RPA | AI for RPA | Coleta de eventos naturais (NASA EONET) e posição da ISS |
| AstroGuard | IoT / Cognitive IoT | Sensoriamento físico do habitat (telemetria de sensores) |
| NeuroSpace Alert | Computação Neuromórfica | Sensor de condição crítica com memristor virtual |
| Quântica Mythos | Computação Quântica | Previsão de chuva extrema (modelos quânticos vs. clássicos) |
| Wildfire VC | Visão Computacional | Confirmação visual de incêndio por imagem de satélite |
| AgroSentinel | Front-End & Mobile | Cálculo de risco regional, alertas e validação humana |
| RAG Espacial | Inteligência Artificial Generativa | Assistente de consulta com LLM na nuvem |
| RAG Net Zero | NLP | Assistente técnico com RAG local |

## Arquitetura da integração

O sistema é organizado em quatro camadas:

1. Coleta e sensoriamento — Orbital RPA, AstroGuard e NeuroSpace Alert produzem os dados de entrada (eventos, telemetria, estado de sensores).
2. Previsão e confirmação — Quântica Mythos prevê risco climático e Wildfire VC confirma incêndios por imagem.
3. Análise e consulta — AgroSentinel consolida o risco e os alertas; os dois módulos RAG respondem consultas técnicas.
4. Orquestração e governança — o painel GBA lê as saídas de todos os módulos, demonstra o fluxo integrado e aplica a camada de governança.

## Estrutura do repositório

```
gbs-gs/
├── orbital-rpa/             # módulo — AI for RPA
├── astroguard/              # módulo — IoT
├── neurospace-alert/        # módulo — Computação Neuromórfica
├── quantica-mythos/         # módulo — Computação Quântica
├── wildfire-vc/             # módulo — Visão Computacional
├── agrosentinel/            # módulo — Front-End & Mobile
├── rag-espacial/            # módulo — IA Generativa
├── rag-net-zero/            # módulo — NLP
├── dados_integrados/        # saídas padronizadas (JSON) de cada módulo
└── painel_gba/              # painel orquestrador (Streamlit)
    ├── app.py
    ├── contrato_de_dados.md
    ├── exportadores/        # conversores de saída para o contrato comum
    ├── requirements.txt
    └── README.md
```

## Como executar o painel

Pré-requisitos: Python 3.13.

1. Instale as dependências:

```
python3.13 -m pip install -r painel_gba/requirements.txt
```

2. (Opcional) Atualize as saídas dos módulos. Os exportadores leem a saída real de cada módulo quando ela existe em disco e, caso contrário, geram um exemplo. Para regenerar:

```
python3.13 painel_gba/exportadores/exportar_todos.py
```

3. Rode o painel:

```
python3.13 -m streamlit run painel_gba/app.py
```

O painel abre no navegador com quatro abas: Visão geral, Fluxo de dados, Governança e Auditoria.

## Contrato de dados

Cada módulo é representado por um arquivo `dados_integrados/<modulo>.json` com identificação, timestamp, proveniência do dado (real ou exemplo), o conteúdo específico do módulo e um bloco de governança com as marcações de privacidade, decisão automatizada, validação humana e auditabilidade. O detalhamento do schema está em `painel_gba/contrato_de_dados.md`.

## Links

- Repositório: https://github.com/murilo2318/gbs-gs
- Painel: execução local (ver instruções acima)

Integrantes:
Nome	RM
Nícolas Lemos Ribeiro	553273
Luís Fernando de Oliveira Salgado	561401
Murilo de Faria Benhossi	562358
