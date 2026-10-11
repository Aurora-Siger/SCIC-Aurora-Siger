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

Ao carregar a base, o sistema faz uma limpeza automática: padroniza textos, converte as colunas numéricas, descarta registros sem latência, tensão ou corrente e remove duplicados.

---

## Funcionalidades

| Opção | O que faz | Arquivo | Status |
|-------|-----------|---------|--------|
| 1 | Resumo da base e consultas por módulo, status e tipo | `dados.py` | ✅ Pronto |
| 2 | Erro absoluto e relativo, indicadores, erros por módulo, ponto flutuante e gráfico | `analise.py` | ✅ Pronto |
| 3 | Regressão linear para prever a latência, com MAE, MSE, RMSE e R² | `modelo.py` | ✅ Pronto |
| 4 | Priorização dos alertas mais críticos com heap | `estruturas.py` | ✅ Pronto |
| 5 | Busca de módulos, nomes e códigos de sensores por prefixo com trie | `estruturas.py` | ✅ Pronto |
| 6 | Código do sensor em binário e hexadecimal, potência (P = V × I) e resistência (R = V / I) | `hardware.py` | ✅ Pronto |
| 7 | Análise final: situação geral, módulo mais preocupante, tendência, modelo, alertas prioritários e recomendações | `analise.py` | ✅ Pronto |

---

## Análise de erros

O erro é calculado entre a latência prevista e a observada em cada registro:

```
erro absoluto = |latência observada − latência prevista|        (ms)
erro relativo = erro absoluto / latência observada               (%)
```

O erro absoluto diz quantos milissegundos a previsão errou. O erro relativo permite comparar módulos com escalas diferentes: 20 ms de erro é grave para um módulo de 80 ms, mas pequeno para um de 300 ms.

| Erro relativo | Classificação | Significado para a colônia |
|---------------|---------------|----------------------------|
| até 10% | Aceitável | Variação normal da rede interna |
| 10% a 25% | Atenção | Módulo deve ser acompanhado |
| acima de 25% | Crítico | Risco de atraso em comandos e alertas |

### Indicadores da base atual

| Indicador | Valor |
|-----------|-------|
| Latência média observada | 161,2 ms |
| Latência média prevista | 150,4 ms |
| Registros acima do previsto | 58,3% |
| Erro absoluto médio | 14,6 ms |
| Erro relativo médio | 7,6% |
| Registros com erro aceitável | 83,3% |
| Registros críticos (> 25%) | 6 |
| Disponibilidade (status ativo) | 68,8% |

![Erro relativo médio por módulo](graficos_ou_imagens/erro_relativo_por_modulo.png)

O módulo de **Comunicação (MOD-CM-008)** é o único com erro relativo médio acima do limite aceitável (15,1%), com pior caso de 40,0% no ciclo 3. Como os alertas de todos os módulos dependem dele, ele é tratado como prioridade máxima.

**Ponto flutuante:** o sistema mostra que `120.6 − 119.9` resulta em `0.6999999999999886` no Python, por causa da representação binária dos decimais. O desvio (cerca de 10⁻¹⁴ ms) é irrelevante diante da precisão do sensor (0,1 ms), mas por isso o sistema nunca compara decimais com `==`: usa limites e arredonda apenas na exibição.

---

## Modelo de previsão

Uma **regressão linear** (scikit-learn) prevê a latência de cada módulo a partir da **potência** do transmissor (P = V × I), do **ciclo** e do **tipo** do módulo. O modelo é treinado só com os registros normais, para aprender o comportamento esperado da colônia. Divisão: 75% treino (30 registros) e 25% teste (10 registros).

| Previsão | MAE | MSE | RMSE | R² |
|----------|-----|-----|------|----|
| Nosso modelo | 5,1 ms | 35,0 | 5,9 ms | 0,97 |
| Chute pela média (baseline) | 41,3 ms | 2127,0 | 46,1 ms | −0,56 |
| Previsão original da base | 4,0 ms | 25,8 | 5,1 ms | 0,98 |

- O modelo erra 8 vezes menos que o chute pela média: aprendeu um padrão real.
- R² de 0,97 **não** significa modelo perfeito: são só 10 registros de teste, com dados simulados.
- RMSE maior que o MAE indica que alguns erros são maiores que a média.
- Cada ciclo deixa a rede 4,25 ms mais lenta, e cada 1 W de potência reduz a latência em 0,19 ms.

**Detector de anomalias:** nos registros normais o erro médio é de 5,1 ms; nos 8 registros em alerta, que o modelo nunca viu, sobe para 62,9 ms. Quando a latência real se afasta muito do esperado, o SCIC tem um sinal objetivo de comportamento anormal.

![Latência real x prevista](graficos_ou_imagens/latencia_real_x_prevista.png)

---

## Heap e trie

**Heap (opção 4):** max-heap implementado à mão (sem `heapq`), com `heapify_up` e `heapify_down`. A prioridade de cada alerta é `prioridade_alerta × 10`, +5 se a latência ficou acima da prevista e +5 se o módulo for de comunicação ou suporte à vida. O alerta mais urgente fica sempre na raiz; inserir e remover custam O(log n), contra O(n) para achar o mais urgente numa lista comum.

| Ordem | Módulo | Ciclo | Prioridade |
|-------|--------|-------|------------|
| 1º | MOD-CM-008 Comunicação | 3 | 60 |
| 2º | MOD-SV-002 Sistemas de Suporte à Vida | 4 | 60 |
| 3º | MOD-CM-008 Comunicação | 5 | 60 |

**Trie (opção 5):** guarda os códigos dos módulos, os nomes e os códigos dos sensores (24 palavras). A busca percorre só as letras do prefixo, em O(m).

| Prefixo | Resultado |
|---------|-----------|
| `mod-s` | MOD-SC-004, MOD-SV-002 |
| `com` | Comunicação (MOD-CM-008) |
| `17` | Sensores 172, 173, 174 e 175 |

---

## Estrutura de arquivos

```
SCIC-Aurora-Siger
├── codigo_fonte.py          # sistema principal — execute aqui
├── dados.py                 # leitura, limpeza e consulta da base
├── analise.py               # indicadores, erro absoluto e relativo, análise final
├── modelo.py                # regressão linear e métricas
├── estruturas.py            # heap e trie
├── hardware.py              # bases numéricas, potência e Lei de Ohm
├── dados_aurora_siger.csv   # base de dados simulada
├── relatorio_tecnico.md     # relatório técnico do projeto
├── requirements.txt         # dependências
├── link_video.txt           # link do vídeo (YouTube · Não listado)
├── .gitignore               # arquivos temporários ignorados pelo Git
└── graficos_ou_imagens/
    ├── erro_relativo_por_modulo.png
    └── latencia_real_x_prevista.png
```

> Todos os arquivos `.py` e o CSV devem ficar na mesma pasta. Os gráficos são gerados automaticamente em `graficos_ou_imagens/` ao executar as opções 2 e 3.

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
