# Relatório Técnico — SCIC
**Sistema de Comunicação Interplanetária da Colônia · Colônia Aurora Siger · FIAP Fase 6**

| Integrante | RM |
|------------|-----|
| Isabelle Caroline de Camargo Francisco | 572096 |
| Matheus Lyncoln Souza Dias | 570765 |
| Mirela Aparecida Bispo Miguel | 570830 |
| Rodrigo Abrantes Mizerani | 571808 |

Repositório: https://github.com/Aurora-Siger/SCIC-Aurora-Siger

---

## Sumário

1. Contexto da solução
2. Descrição dos dados
3. Indicadores e análise de erros
4. Modelo de previsão e métricas
5. Priorização de alertas com heap
6. Busca de registros com trie
7. Dispositivos, bases numéricas e eletricidade
8. Gerenciamento inteligente da comunicação
9. Reflexão social, cultural e sustentável
10. Limitações e possíveis melhorias
11. Uso de ferramentas de IA

---

## 1. Contexto da solução

Nas fases anteriores, a Aurora Siger ganhou módulos conectados (SIGIC), registros operacionais e um núcleo cognitivo (NCAS). Com a colônia maior, a pergunta deixou de ser "os dados existem?" e passou a ser "os dados são confiáveis?". O SCIC responde a essa pergunta: ele avalia se a latência de comunicação de cada módulo está dentro do esperado, mede o erro das previsões, aprende o comportamento normal da rede e organiza os alertas por urgência.

O sistema é um protótipo em Python executado pelo terminal (`codigo_fonte.py`), com um menu de 7 opções:

| Opção | Funcionalidade | Arquivo |
|-------|----------------|---------|
| 1 | Consultar registros da colônia | `dados.py` |
| 2 | Indicadores e erros numéricos | `analise.py` |
| 3 | Modelo de previsão de latência | `modelo.py` |
| 4 | Priorizar alertas (heap) | `estruturas.py` |
| 5 | Buscar registros por prefixo (trie) | `estruturas.py` |
| 6 | Hardware: bases numéricas e eletricidade | `hardware.py` |
| 7 | Análise final | `analise.py` |

**Qual latência é analisada.** O SCIC analisa a latência da **rede interna da colônia**, ou seja, o tempo de comunicação entre os módulos, medido em milissegundos. O atraso Terra–Marte, de 3 a 22 minutos, depende só da distância entre os planetas e não pode ser reduzido por gestão de rede. Por isso ele não entra no modelo.

**Por que a Comunicação é um módulo essencial nesta fase.** No SIGIC (Fase 4), o módulo de Comunicação (MOD-CM-008) tinha prioridade 4, abaixo de energia, suporte à vida, habitação e logística. No SCIC ele passa a ser tratado como essencial, porque todos os alertas dos outros módulos dependem dele para chegar à equipe. Uma falha na Comunicação atrasa a resposta da colônia inteira.

---

## 2. Descrição dos dados

A base `dados_aurora_siger.csv` foi construída pela equipe com **48 registros simulados**: os mesmos 8 módulos das fases anteriores (MOD-EN-001 a MOD-CM-008), acompanhados ao longo de 6 ciclos de operação.

| Coluna | Descrição |
|--------|-----------|
| `codigo_modulo`, `modulo`, `tipo` | Identificação do módulo |
| `codigo_sensor` | Código do sensor em decimal (101 a 200) |
| `latencia_obs` | Latência observada (ms) |
| `latencia_prev` | Latência prevista pela estimativa original (ms) |
| `tensao`, `corrente` | Tensão (11,4 a 50,3 V) e corrente (0,8 a 4,5 A) do transmissor |
| `status` | ativo (33), manutenção (7) ou alerta (8) |
| `prioridade_alerta` | Urgência do alerta, de 1 a 5 |
| `mensagem` | Resumo do alerta |
| `ciclo` | Ciclo de registro (1 a 6) |

**Organização no código.** Os dados são lidos com Pandas e ficam em um DataFrame. Ao carregar, o sistema padroniza os textos, converte as colunas numéricas (valores inválidos viram `NaN` em vez de travar o programa), descarta registros sem latência, tensão ou corrente e remove duplicados. Testamos a limpeza com uma linha duplicada e uma linha com latência inválida: as duas foram removidas, e os 48 registros válidos permaneceram.

**Alertas propositais.** Os 8 registros em alerta foram incluídos de propósito, com latência bem acima da prevista, para testar a análise de erros, o modelo e o heap. A Comunicação concentra 3 desses alertas (ciclos 3, 5 e 6).

---

## 3. Indicadores e análise de erros

### Fórmulas

```
erro absoluto = |latência observada − latência prevista|      (ms)
erro relativo = erro absoluto / latência observada             (%)
```

O **erro absoluto** diz quantos milissegundos a previsão errou. O **erro relativo** permite comparar módulos com escalas diferentes: 20 ms de erro é grave para o Suporte à Vida, com latência média de 104 ms, e bem menos para a Agricultura, com 224 ms. Dividimos pela latência observada porque ela é o valor real medido, que serve de referência.

### Quando o erro é aceitável

| Erro relativo | Classificação | Significado para a colônia |
|---------------|---------------|----------------------------|
| até 10% | Aceitável | Variação normal da rede interna |
| 10% a 25% | Atenção | Módulo deve ser acompanhado |
| acima de 25% | Crítico | Risco de atraso em comandos e alertas |

### Resultados

| Indicador | Valor |
|-----------|-------|
| Latência média observada | 161,2 ms |
| Latência média prevista | 150,4 ms |
| Registros acima do previsto | 58,3% |
| Erro absoluto médio | 14,6 ms |
| Erro relativo médio | 7,6% |
| Registros com erro aceitável | 83,3% |
| Registros em atenção / críticos | 2 / 6 |
| Disponibilidade (status ativo) | 68,8% |

| Módulo | Erro relativo médio | Pior caso | Alertas |
|--------|---------------------|-----------|---------|
| MOD-CM-008 Comunicação | **15,1%** | 40,0% | 3 |
| MOD-EN-001 Geradores + Painéis Solares | 8,5% | 20,6% | 1 |
| MOD-HB-003 Módulos Infláveis BEAM | 8,0% | 30,8% | 1 |
| MOD-SV-002 Sistemas de Suporte à Vida | 7,6% | 35,0% | 1 |
| MOD-AG-007 Agricultura | 7,3% | 32,3% | 1 |
| MOD-MN-005 Mineração e Produção ISRU | 6,8% | 26,7% | 1 |
| MOD-SC-004 Sensores Científicos | 4,2% | 7,1% | 0 |
| MOD-LG-006 Logística e Suprimentos | 3,4% | 5,8% | 0 |

![Erro relativo médio por módulo](graficos_ou_imagens/erro_relativo_por_modulo.png)

**Interpretação.** A maior parte da rede está saudável (83,3% dos registros com erro aceitável), mas a média esconde problemas pontuais: 6 registros passaram de 25% de erro. A Comunicação é o único módulo com erro médio acima do limite. Além disso, 58,3% dos registros ficaram acima da previsão, o que mostra que a estimativa original tende a **subestimar** a latência. A latência média também subiu de 140,2 ms no ciclo 1 para 169,7 ms no ciclo 6 (+21%), sinal de aumento gradual de carga na rede.

### Precisão numérica e ponto flutuante

No Python, `0.1 + 0.2` resulta em `0.30000000000000004`, e não em `0.3`, porque o computador guarda números em binário e alguns decimais não têm representação exata. Na nossa própria base, `120.6 − 119.9` resulta em `0.6999999999999886` em vez de `0.7`.

O desvio é de cerca de 10⁻¹⁴ ms, muito menor que a precisão do sensor (0,1 ms), então não muda nenhuma decisão. Mesmo assim, o sistema segue duas regras: nunca compara decimais com `==` (usa limites, como 10% e 25%, e `math.isclose` quando precisa comparar) e arredonda os valores apenas na hora de exibir.

---

## 4. Modelo de previsão e métricas

### O modelo

Usamos uma **regressão linear** (scikit-learn) para prever a latência de cada módulo.

- **Entradas (X):** potência do transmissor (P = V × I), ciclo e tipo do módulo. O tipo é texto, então foi convertido em colunas de 0 e 1 com `pd.get_dummies`, usando a agricultura como referência.
- **Saída (y):** latência observada (ms).
- **Dados de treino:** apenas os 40 registros normais. A ideia é que o modelo aprenda o comportamento esperado da colônia, sem ser influenciado pelas anomalias.
- **Divisão:** 75% para treino (30 registros) e 25% para teste (10 registros), com `random_state=42` para o resultado ser reproduzível.

### Métricas no conjunto de teste

| Previsão | MAE | MSE | RMSE | R² |
|----------|-----|-----|------|----|
| **Nosso modelo** | 5,1 ms | 35,0 | 5,9 ms | 0,97 |
| Chute pela média (baseline) | 41,3 ms | 2127,0 | 46,1 ms | −0,56 |
| Previsão original da base | 4,0 ms | 25,8 | 5,1 ms | 0,98 |

- **MAE** (erro absoluto médio): quanto o modelo erra, em média, em ms.
- **MSE** (erro quadrático médio): eleva os erros ao quadrado, então pune mais os erros grandes.
- **RMSE** (raiz do MSE): volta para ms, comparável ao MAE.
- **R²**: quanto da variação da latência o modelo explica (1 = tudo; abaixo de 0 = pior que chutar a média).

![Latência real x prevista](graficos_ou_imagens/latencia_real_x_prevista.png)

### Interpretação

Um único número não basta para avaliar o modelo, por isso olhamos as métricas em conjunto:

- **O modelo aprendeu um padrão real.** Ele erra 5,1 ms em média, contra 41,3 ms do chute pela média: 8 vezes menos.
- **R² alto não significa modelo perfeito.** O R² de 0,97 foi medido em apenas 10 registros de teste, com dados simulados e sem anomalias. Em dados reais, com mais ruído, ele tende a ser menor.
- **RMSE x MAE.** O RMSE (5,9 ms) é um pouco maior que o MAE (5,1 ms). Como o RMSE pesa mais os erros grandes, a diferença pequena indica que os erros são parecidos entre si, sem nenhum registro muito fora da curva no teste.
- **Comparação com a previsão original.** A estimativa que já vinha na base foi um pouco melhor (MAE de 4,0 ms), mas não sabemos como ela foi calculada. O nosso modelo chega perto usando só três informações e pode ser refeito a cada novo ciclo de dados.
- **Coeficientes.** Cada ciclo deixa a rede 4,25 ms mais lenta, o que confirma a tendência de alta vista na análise de erros. Cada 1 W a mais de potência reduz a latência em 0,19 ms.

### O modelo como detector de anomalias

Aplicamos o modelo nos 8 registros em alerta, que ele nunca viu. Nos registros normais o erro médio é de 5,1 ms; nos alertas, sobe para **62,9 ms**. A diferença entre a latência observada e a esperada pelo modelo foi de +18,0 ms no menor caso (Comunicação, ciclo 6) e de +86,8 ms no maior (Agricultura, ciclo 2). No gráfico, os pontos normais ficam sobre a linha de previsão perfeita e os alertas ficam bem acima dela. Assim, o modelo dá ao SCIC um critério objetivo para identificar comportamento fora do normal.

---

## 5. Priorização de alertas com heap

**Como os alertas são representados.** Cada alerta é um dicionário com a linha do CSV (módulo, ciclo, latências, tipo, prioridade). No heap, ele é guardado como uma tupla `(prioridade_calculada, alerta)`.

**Critério de prioridade.**

```
prioridade = prioridade_alerta × 10
           + 5  se a latência observada ficou acima da prevista
           + 5  se o módulo for de comunicação ou suporte à vida
```

**Como o heap organiza os alertas.** Implementamos um **max-heap** à mão, sem a biblioteca `heapq`, usando uma lista. Para o elemento na posição `i`, o pai fica em `(i − 1) // 2` e os filhos em `2i + 1` e `2i + 2`.

- **Inserir:** o alerta entra no fim da lista e sobe (`heapify_up`) enquanto for maior que o pai.
- **Remover o mais urgente:** a raiz troca de lugar com o último elemento, o último sai da lista (`pop`) e o novo elemento da raiz desce (`heapify_down`) enquanto algum filho for maior que ele.

**Como o sistema seleciona o mais urgente.** O mais urgente está sempre na raiz, na posição 0. A opção 4 do menu remove a raiz repetidamente e mostra a ordem de atendimento:

| Ordem | Módulo | Ciclo | Prioridade |
|-------|--------|-------|------------|
| 1º | MOD-CM-008 Comunicação | 3 | 60 |
| 2º | MOD-SV-002 Sistemas de Suporte à Vida | 4 | 60 |
| 3º | MOD-CM-008 Comunicação | 5 | 60 |
| 4º | MOD-HB-003 Módulos Infláveis BEAM | 6 | 55 |
| 5º | MOD-CM-008 Comunicação | 6 | 50 |
| 6º a 8º | EN-001 (c3), AG-007 (c2), MN-005 (c5) | — | 45 |

**Vantagem sobre uma lista simples.** Numa lista comum, achar o alerta mais urgente exige percorrer todos os elementos: O(n). No heap, o mais urgente está sempre na raiz, e inserir ou remover custa O(log n). Com 8 alertas, isso significa no máximo 3 trocas por operação. A diferença cresce com a colônia: com 1.000 alertas, seriam no máximo 9 trocas, contra 1.000 comparações na lista.

**Testes.** Inserimos 500 sequências aleatórias de alertas e conferimos que a ordem de saída sempre bateu com a ordenação decrescente das prioridades. Também testamos a remoção com o heap vazio, que retorna `None` sem erro.

---

## 6. Busca de registros com trie

**Como funciona.** A trie é uma árvore em que cada nó representa uma letra. Cada nó (`NoTrie`) guarda um dicionário de filhos (letra → nó) e um marcador `fim`, que indica se uma palavra termina ali. Palavras com o mesmo começo compartilham o mesmo caminho na árvore.

- **Inserir:** percorre a palavra letra por letra (em minúsculas), criando os nós que ainda não existem, e marca o último como `fim`.
- **Buscar por prefixo:** segue as letras do prefixo. Se alguma não existir, retorna lista vazia. Se chegar ao fim do prefixo, percorre todos os nós abaixo e junta as palavras completas.

**O que está na trie.** 24 palavras: os 8 códigos dos módulos, os 8 nomes e os 8 códigos dos sensores.

| Prefixo digitado | Resultado |
|------------------|-----------|
| `mod-s` | MOD-SC-004, MOD-SV-002 |
| `com` | Comunicação (MOD-CM-008) |
| `sis` | Sistemas de Suporte à Vida (MOD-SV-002) |
| `17` | Sensores 172, 173, 174 e 175 |
| `xyz` | Nenhum registro |

**Por que a trie é adequada para prefixos.** A busca percorre só as letras do prefixo: O(m), em que m é o tamanho do prefixo. Ela não precisa comparar o prefixo com todas as palavras da base, como faria uma busca em lista. Na colônia, isso permite que um operador digite as primeiras letras de um código e encontre o sensor ou o módulo na hora, mesmo com milhares de registros. Também é a base de recursos como o autocompletar de comandos.

---

## 7. Dispositivos, bases numéricas e eletricidade

### Dispositivos de entrada e saída

| Tipo | No protótipo | Na colônia real |
|------|--------------|-----------------|
| **Entrada** | Arquivo CSV e teclado (menu) | Sensores de latência, medidores de tensão e corrente nos transmissores |
| **Saída** | Terminal, gráficos PNG e relatório | Monitor da central de operações, painel (dashboard) e alertas sonoros |
| **Interfaces** | — (conceitual) | Rede cabeada entre módulos, Wi-Fi para dispositivos móveis, USB para manutenção local e Bluetooth para sensores de curto alcance |

### Bases numéricas

Cada sensor tem um código em decimal, e o sistema converte para binário e hexadecimal (opção 6). Exemplo com o sensor da Comunicação, código 200:

```
200 ÷ 16 = 12, resto 8   →  hexadecimal: C8   (12 = C)
200 em binário: 128 + 64 + 8 = 11001000
```

Outro exemplo: o sensor 172 (Sensores Científicos) vira `10101100` em binário e `AC` em hexadecimal. O hexadecimal é útil como identificador porque é mais curto que o binário e cada dígito representa exatamente 4 bits: `C8` corresponde a `1100 1000`.

### Eletricidade básica

A opção 6 calcula, para cada módulo, a potência do transmissor e a resistência equivalente:

```
P = V × I     (potência, em watts)
R = V / I     (Lei de Ohm, em ohms)
```

Exemplo com o transmissor da Comunicação no ciclo 6: tensão de 47,61 V e corrente de 4,38 A.

```
P = 47,61 × 4,38 = 208,53 W
R = 47,61 / 4,38 = 10,87 Ω
```

A potência não é só um cálculo isolado: ela entra no modelo de previsão (seção 4), em que cada 1 W a mais reduz a latência em 0,19 ms. Ou seja, a eletricidade do transmissor tem efeito direto na qualidade da comunicação. Se a corrente for zero, o sistema mostra uma mensagem de erro em vez de dividir por zero.

---

## 8. Gerenciamento inteligente da comunicação

Os resultados do SCIC mostram como uma rede de comunicação inteligente poderia funcionar na Aurora Siger.

**Sensores e medidores inteligentes.** Hoje o SCIC lê um CSV com um registro por ciclo. Na colônia real, cada transmissor teria sensores de latência e medidores de tensão e corrente enviando dados continuamente. Os códigos de sensor da base (101 a 200, em hexadecimal 65 a C8) já funcionam como identificadores desses dispositivos.

**Monitoramento contínuo.** O erro de 40% da Comunicação no ciclo 3 só foi percebido na análise do ciclo. Com monitoramento contínuo, a mesma regra do SCIC (erro relativo acima de 25% = crítico) dispararia o alerta no momento em que a latência subisse. Os dados também mostram por que isso importa: a latência média subiu 21% em seis ciclos, uma piora gradual que só aparece quando os dados são acompanhados ao longo do tempo.

**Automação para decisões rápidas.** O heap já automatiza a pergunta "o que atender primeiro?": em situação crítica, a equipe sabe na hora que o primeiro da fila é a Comunicação no ciclo 3, seguida do Suporte à Vida no ciclo 4. Um sistema real poderia ir além, por exemplo redirecionando o tráfego de um módulo em alerta para outro enlace automaticamente.

**Armazenamento de dados e enlaces redundantes.** A Comunicação é o módulo mais crítico: maior erro médio (15,1%), 3 dos 8 alertas e, segundo o SIGIC, ligada ao resto da rede por uma única conexão (ponte crítica MOD-CM-008 ↔ MOD-AG-007). Um enlace redundante evitaria que uma falha nessa conexão isolasse a colônia. O armazenamento do histórico de ciclos, como o nosso CSV, é o que permite treinar o modelo e comparar o comportamento atual com o passado.

**Manutenção preditiva.** O modelo de regressão é a base para isso: ele sabe qual latência esperar de cada módulo, com erro médio de 5,1 ms. Quando a diferença entre o observado e o esperado cresce, como os +18 ms da Comunicação no ciclo 6, a equipe pode agir antes da falha. O coeficiente do ciclo (+4,25 ms por ciclo) também permite prever quando a rede vai ultrapassar um limite e programar a manutenção com antecedência. Os módulos em manutenção na base (Energia, Sensores Científicos e Suporte à Vida) mostram que a colônia já faz manutenção preventiva; a manutenção preditiva tornaria isso mais preciso.

**Redes inteligentes e microrredes.** No SIGIC, a energia da colônia foi modelada como uma rede de módulos. Uma rede de comunicação inteligente segue a mesma lógica: dividir a colônia em microrredes, grupos de módulos que continuam se comunicando entre si mesmo se a conexão principal cair. Como a potência do transmissor afeta a latência (seção 7), a gestão de energia e a de comunicação precisam funcionar juntas, por exemplo direcionando mais potência para a Comunicação em momentos críticos.

---

## 9. Reflexão social, cultural e sustentável

**Uso eficiente da comunicação e sustentabilidade.** Em Marte, energia é um recurso escasso. O modelo mostrou que a latência depende da potência do transmissor, então transmitir com potência máxima o tempo todo seria desperdício. Um sistema como o SCIC permite usar mais potência só onde é necessário, como na Comunicação durante um alerta, e economizar nos módulos estáveis, como Logística e Sensores Científicos, que tiveram os menores erros (3,4% e 4,2%).

**Equipe humana responsável pelas decisões.** O heap decide a ordem de atendimento por uma fórmula, mas a fórmula foi definida por pessoas e pode estar incompleta. Por exemplo, ela trata como empatados (prioridade 60) um alerta da Comunicação e um do Suporte à Vida, embora na prática uma falha no suporte à vida possa ser mais grave para os colonos. Por isso o SCIC recomenda que a decisão final em alertas críticos seja sempre validada pela equipe humana.

**Transparência nas decisões baseadas em dados.** O SCIC mostra de onde vem cada número: a fórmula da prioridade, os limites de 10% e 25% e as métricas do modelo, incluindo as limitações (seção 10). Também comparamos o nosso modelo com a previsão original da base e registramos que a original foi um pouco melhor. Em uma comunidade, decisões automáticas só são aceitas quando as pessoas conseguem entender e questionar como foram tomadas.

**Conhecimentos tradicionais e respeito aos recursos.** Muitas culturas indígenas tratam os recursos da natureza como algo a ser usado com equilíbrio e pensando nas próximas gerações. Na Aurora Siger, onde cada watt e cada peça de reposição vêm de longe, essa visão inspira priorizar a manutenção preditiva em vez de esperar a falha e substituir equipamentos.

**Evitar sistemas excludentes.** As mensagens do sistema usam linguagem técnica neutra e descrevem o problema, não as pessoas responsáveis. Em uma versão real, seria importante que o painel fosse acessível a toda a equipe, inclusive em outros idiomas, e que os critérios de prioridade fossem revisados por pessoas de áreas diferentes, para não favorecer apenas os módulos de quem projetou o sistema.

---

## 10. Limitações e possíveis melhorias

**Limitações**

- **Dados simulados.** Os 48 registros foram criados pela equipe, e os alertas foram incluídos de propósito. Os resultados mostram que o método funciona, mas não representam medições reais.
- **Base pequena.** O modelo foi testado em apenas 10 registros, o que deixa as métricas instáveis: outra divisão entre treino e teste daria valores um pouco diferentes.
- **Modelo simples.** A regressão linear assume que a latência muda de forma proporcional às entradas. Efeitos mais complexos, como congestionamento repentino da rede, não são capturados.
- **Critério de prioridade fixo.** A fórmula do heap tem pesos escolhidos pela equipe e gera empates (três alertas com prioridade 60).
- **Análise por ciclo.** O sistema analisa os dados depois do ciclo, e não em tempo real.

**Possíveis melhorias**

- Usar validação cruzada para avaliar o modelo em várias divisões de treino e teste, e comparar modelos alternativos com Grid Search.
- Incluir o tempo desde o registro como critério de desempate no heap.
- Ler os dados continuamente dos sensores, em vez de um CSV, e disparar alertas na hora.
- Criar um painel visual para a central de operações.
- Usar o modelo para prever quando cada módulo vai ultrapassar o limite de latência e agendar a manutenção.

---

## 11. Uso de ferramentas de IA

A equipe usou o Claude (Anthropic) como assistente durante o desenvolvimento, para apoiar a organização das tarefas, a escrita de partes do código e a redação da documentação. Todas as partes foram executadas e testadas pela equipe, e os resultados apresentados neste relatório foram conferidos rodando o sistema.
