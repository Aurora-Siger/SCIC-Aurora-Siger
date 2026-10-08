<div align="center">

# Sistema de Comunicação Interplanetária da Colônia
**Colônia Aurora Siger · Fase 6 — A Aurora Estabelece Comunicação Interplanetária com Inteligência e Precisão**

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Dados-150458?style=flat-square&logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-Regressão-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)
![Fase](https://img.shields.io/badge/Fase-6-orange?style=flat-square)

</div>

---

## O que é o SCIC?

O SCIC é a camada de avaliação, organização e interpretação técnica dos dados de comunicação da Colônia Aurora Siger. Ele monitora a **latência de comunicação dos 8 módulos da colônia**, calcula erros entre valores previstos e observados, treina um modelo simples de previsão, prioriza alertas críticos com **heap** e permite buscas rápidas por prefixo com **trie**.

> A latência analisada é a da **rede interna da colônia** (comunicação entre módulos), medida em milissegundos. O atraso Terra–Marte (3 a 22 minutos) é fixo pela distância entre os planetas e não entra no modelo.

---

## Equipe

| Nome | RM |
|---|---|
| Isabelle Caroline de Camargo Francisco | 572096 |
| Matheus Lyncoln Souza Dias | 570765 |
| Mirela Aparecida Bispo Miguel | 570830 |
| Rodrigo Abrantes Mizerani | 571808 |

---

## Início rápido

```bash
# Instale as dependências (uma vez):
pip install -r requirements.txt

# Execute o sistema:
python codigo_fonte.py

# Windows
py codigo_fonte.py
```

---

## Menu do sistema

```
╔══════════════════════════════════════════════════════╗
║           SCIC — Colônia Aurora Siger                ║
╠══════════════════════════════════════════════════════╣
║  1. Consultar registros da colônia                   ║
║  2. Indicadores e erros numéricos                    ║
║  3. Modelo de previsão de latência   [Regressão]     ║
║  4. Priorizar alertas                [Heap]          ║
║  5. Buscar registros por prefixo     [Trie]          ║
║  6. Hardware: bases e eletricidade   [COA]           ║
║  7. Análise final                                    ║
║  0. Sair                                             ║
╚══════════════════════════════════════════════════════╝
```

---

## A base de dados

O arquivo `dados_aurora_siger.csv` traz **48 registros simulados**: os mesmos 8 módulos das fases anteriores (MOD-EN-001 a MOD-CM-008), acompanhados ao longo de 6 ciclos de operação.

| Coluna | Descrição |
|--------|-----------|
| `codigo_modulo` | Código do módulo (ex.: MOD-CM-008) |
| `modulo` / `tipo` | Nome e tipo do módulo |
| `codigo_sensor` | Código do sensor em decimal (convertido para binário e hexadecimal no sistema) |
| `latencia_obs` / `latencia_prev` | Latência observada e prevista, em ms |
| `tensao` / `corrente` | Tensão (V) e corrente (A) do transmissor |
| `status` | ativo, manutenção ou alerta |
| `prioridade_alerta` | Urgência do alerta, de 1 (baixa) a 5 (crítica) |
| `mensagem` | Resumo do alerta |
| `ciclo` | Ciclo de registro (1 a 6) |

**Critério de alerta:** erro relativo acima de 10% gera alerta; acima de 25%, alerta crítico. Módulos essenciais (energia, suporte à vida, habitação, logística e comunicação) recebem prioridade maior.

---

## Estrutura de arquivos

```
SCIC-Aurora-Siger
├── codigo_fonte.py          # sistema principal — execute aqui
├── dados.py                 # leitura e consulta da base
├── analise.py               # indicadores, erro absoluto e relativo
├── modelo.py                # regressão linear e métricas
├── estruturas.py            # heap e trie
├── hardware.py              # bases numéricas, potência e Lei de Ohm
├── dados_aurora_siger.csv   # base de dados simulada
├── relatorio_tecnico.md     # relatório técnico do projeto
├── requirements.txt         # dependências
├── link_video.txt           # link do vídeo (YouTube · Não listado)
└── graficos_ou_imagens/     # gráficos gerados pelo sistema
```

---

## Dependências

| Biblioteca | Uso |
|------------|-----|
| `pandas` | Leitura, limpeza e consulta da base |
| `numpy` | Cálculos numéricos |
| `matplotlib` | Gráficos de latência e erros |
| `scikit-learn` | Regressão linear, divisão treino/teste e métricas |

Heap, trie e conversões de base usam apenas a biblioteca padrão do Python.

---

## Conceitos aplicados

`Erro absoluto` `Erro relativo` `Ponto flutuante` `Regressão linear` `MAE` `MSE` `RMSE` `R²`
`Heap` `Heapify-up` `Heapify-down` `Trie` `Busca por prefixo` `Bases numéricas`
`Lei de Ohm` `Potência` `Redes inteligentes de comunicação` `Manutenção preditiva`

<div align="center">
<sub>FIAP · Fase 6 — Comunicação Interplanetária · Colônia Aurora Siger</sub>
</div>
