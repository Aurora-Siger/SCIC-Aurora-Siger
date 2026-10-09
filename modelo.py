"""
modelo.py - Regressao linear para prever latencia e metricas   [Isabelle]

Este arquivo cuida do modelo de previsão do SCIC (seção 5.3 do enunciado):
- preparar_dados: cria a coluna de potência (P = V x I)
- separar_x_y: separa o que o modelo usa (X) do que ele prevê (y)
- treinar_modelo: divide em treino e teste e treina a regressão linear
- calcular_metricas: MAE, MSE, RMSE e R²
- avaliar_modelo: compara o modelo com um chute pela média e com a
  previsão original da base, e testa o modelo nos registros em alerta
- gerar_grafico_previsao: salva o gráfico em graficos_ou_imagens/
- menu_modelo: opção 3 do menu principal
"""

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import dados

PASTA_GRAFICOS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "graficos_ou_imagens")


# ===========================================================================
# 1. PREPARAÇÃO DOS DADOS
# ===========================================================================
def preparar_dados(df):
    """Cria a coluna de potência (P = V x I) usada pelo modelo."""
    df = df.copy()   # copia para não alterar o DataFrame original
    df["potencia"] = df["tensao"] * df["corrente"]
    return df


def montar_x(df):
    """Monta a tabela X: potência, ciclo e tipo (o tipo vira colunas de 0 e 1).
    drop_first=True tira a coluna de agricultura, que vira a referência.
    """
    return pd.get_dummies(df[["potencia", "ciclo", "tipo"]],
                          columns=["tipo"], drop_first=True, dtype=int)


def separar_x_y(df):
    """Separa o que o modelo usa (X) do que ele prevê (y).
    Usa só os registros normais: o modelo aprende o comportamento
    esperado da colônia, e os alertas ficam de fora do treino.
    """
    normais = df[df["status"] != "alerta"]
    X = montar_x(normais)
    y = normais["latencia_obs"]   # a latência real, que o modelo tenta prever
    return X, y


# ===========================================================================
# 2. TREINO E MÉTRICAS
# ===========================================================================
def treinar_modelo(X, y):
    """Divide os dados em treino (75%) e teste (25%) e treina a regressão."""
    # random_state=42 garante que a divisão seja sempre a mesma
    X_treino, X_teste, y_treino, y_teste = train_test_split(
        X, y, test_size=0.25, random_state=42)

    modelo = LinearRegression()
    modelo.fit(X_treino, y_treino)   # aqui o modelo aprende
    return modelo, X_treino, X_teste, y_treino, y_teste


def calcular_metricas(real, previsto):
    """Calcula as 4 métricas de regressão estudadas na fase.

    MAE  -> erro médio, em ms (quanto o modelo erra, em média)
    MSE  -> média dos erros ao quadrado (pune mais os erros grandes)
    RMSE -> raiz do MSE, volta para ms (comparável ao MAE)
    R²   -> quanto da variação da latência o modelo explica (1 = tudo)
    """
    mse = mean_squared_error(real, previsto)
    return {
        "MAE": mean_absolute_error(real, previsto),
        "MSE": mse,
        "RMSE": np.sqrt(mse),
        "R2": r2_score(real, previsto),
    }


def avaliar_modelo(df):
    """Treina o modelo e reúne todos os resultados em um dicionário.

    Compara três previsões sobre os MESMOS registros de teste:
      - o nosso modelo
      - um chute que sempre usa a latência média do treino (baseline)
      - a previsão original que já vinha na base (latencia_prev)
    Depois aplica o modelo nos registros em alerta, que ele nunca viu.
    """
    df = preparar_dados(df)
    X, y = separar_x_y(df)
    modelo, X_treino, X_teste, y_treino, y_teste = treinar_modelo(X, y)

    previsto = modelo.predict(X_teste)
    chute_media = np.full(len(y_teste), y_treino.mean())
    previsao_base = df.loc[y_teste.index, "latencia_prev"]

    # Registros em alerta: o modelo prevê a latência "esperada" e
    # comparamos com a observada. Erro alto = comportamento anormal.
    alertas = df[df["status"] == "alerta"]
    X_alertas = montar_x(alertas).reindex(columns=X.columns, fill_value=0)
    previsto_alertas = modelo.predict(X_alertas)

    return {
        "modelo": modelo,
        "colunas": list(X.columns),
        "n_treino": len(X_treino),
        "n_teste": len(X_teste),
        "y_teste": y_teste,
        "previsto": previsto,
        "metricas_modelo": calcular_metricas(y_teste, previsto),
        "metricas_media": calcular_metricas(y_teste, chute_media),
        "metricas_base": calcular_metricas(y_teste, previsao_base),
        "alertas": alertas,
        "previsto_alertas": previsto_alertas,
        "erro_medio_alertas": mean_absolute_error(alertas["latencia_obs"], previsto_alertas),
    }


# ===========================================================================
# 3. GRÁFICO
# ===========================================================================
def gerar_grafico_previsao(res):
    """Salva o gráfico de latência real x prevista.
    Pontos sobre a linha tracejada = previsão perfeita.
    """
    import matplotlib
    matplotlib.use("Agg")            # gera o arquivo sem abrir janela
    import matplotlib.pyplot as plt

    os.makedirs(PASTA_GRAFICOS, exist_ok=True)
    caminho = os.path.join(PASTA_GRAFICOS, "latencia_real_x_prevista.png")

    real_alertas = res["alertas"]["latencia_obs"]
    todos = np.concatenate([res["y_teste"], res["previsto"],
                            real_alertas, res["previsto_alertas"]])
    minimo, maximo = todos.min() * 0.9, todos.max() * 1.05

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot([minimo, maximo], [minimo, maximo], color="#52514e",
            linestyle="--", linewidth=1, label="Previsão perfeita")
    ax.scatter(res["previsto"], res["y_teste"], s=60, color="#2a78d6",
               marker="o", edgecolor="white", linewidth=1.5,
               label="Registros normais (teste)", zorder=3)
    ax.scatter(res["previsto_alertas"], real_alertas, s=70, color="#d03b3b",
               marker="^", edgecolor="white", linewidth=1.5,
               label="Registros em alerta", zorder=3)

    # Identifica cada alerta pelo código do módulo e ciclo. Se houver outro
    # alerta logo à direita, o rótulo vai para a esquerda para não sobrepor.
    pontos = list(zip(res["previsto_alertas"], real_alertas,
                      res["alertas"]["codigo_modulo"], res["alertas"]["ciclo"]))
    for prev, real, cod, ciclo in pontos:
        vizinho = any(0 < p2 - prev < 15 and abs(r2 - real) < 15 for p2, r2, _, _ in pontos)
        ax.annotate("%s (c%d)" % (cod.replace("MOD-", ""), ciclo), (prev, real),
                    xytext=(-6, 2) if vizinho else (6, 2), textcoords="offset points",
                    ha="right" if vizinho else "left", fontsize=8, color="#52514e")

    ax.set_xlim(minimo, maximo)
    ax.set_ylim(minimo, maximo)
    ax.set_xlabel("Latência prevista pelo modelo (ms)", color="#52514e")
    ax.set_ylabel("Latência observada (ms)", color="#52514e")
    ax.set_title("Latência real x prevista", loc="left", fontsize=12,
                 color="#0b0b0b", pad=12)
    for lado in ["top", "right"]:
        ax.spines[lado].set_visible(False)
    ax.tick_params(colors="#52514e")
    ax.grid(color="#e6e6e3", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(loc="upper left", frameon=False, fontsize=9)

    fig.tight_layout()
    fig.savefig(caminho, dpi=150)
    plt.close(fig)
    return caminho


# ===========================================================================
# 4. OPÇÃO DO MENU
# ===========================================================================
def mostrar_metricas(res):
    """Exibe a tabela comparando as três previsões."""
    print("\n--- Métricas no conjunto de teste (%d registros normais) ---\n" % res["n_teste"])
    print("%-28s %8s %9s %8s %7s" % ("Previsão", "MAE(ms)", "MSE", "RMSE(ms)", "R²"))
    linhas = [("Nosso modelo", res["metricas_modelo"]),
              ("Chute pela média", res["metricas_media"]),
              ("Previsão original da base", res["metricas_base"])]
    for nome, m in linhas:
        print("%-28s %8.1f %9.1f %8.1f %7.2f" % (nome, m["MAE"], m["MSE"], m["RMSE"], m["R2"]))


def mostrar_interpretacao(res):
    """Explica o que os números significam para a colônia."""
    mod, med = res["metricas_modelo"], res["metricas_media"]
    coef = dict(zip(res["colunas"], res["modelo"].coef_))

    print("\n--- Interpretação ---\n")
    print("- O modelo erra em média %.1f ms (MAE). O chute pela média erra %.1f ms:"
          % (mod["MAE"], med["MAE"]))
    print("  o modelo aprendeu um padrão real dos dados.")

    base = res["metricas_base"]
    if base["MAE"] < mod["MAE"]:
        print("- A previsão original da base ficou um pouco melhor (MAE %.1f ms), mas ela"
              % base["MAE"])
        print("  não mostra como foi calculada. O nosso modelo chega perto (%.1f ms) usando"
              % mod["MAE"])
        print("  só potência, ciclo e tipo, e pode ser refeito a cada novo ciclo de dados.")
    else:
        print("- O modelo superou a previsão original da base (MAE %.1f ms contra %.1f ms)."
              % (mod["MAE"], base["MAE"]))

    print("- R² = %.2f: o modelo explica %.0f%% da variação da latência nos registros"
          % (mod["R2"], mod["R2"] * 100))
    print("  normais. Um R² alto NÃO significa que o modelo é perfeito: foram só %d"
          % res["n_teste"])
    print("  registros de teste, os dados são simulados e ele não prevê anomalias.")

    print("- RMSE (%.1f ms) maior que o MAE (%.1f ms) indica que alguns erros são"
          % (mod["RMSE"], mod["MAE"]))
    print("  maiores que a média, já que o RMSE pesa mais os erros grandes.")

    print("- Cada 1 W a mais de potência muda a latência em %+.2f ms, e cada"
          % coef["potencia"])
    print("  ciclo muda em %+.2f ms (a rede fica mais lenta com o tempo)." % coef["ciclo"])

    print("\n--- O modelo como detector de anomalias ---\n")
    print("Nos registros normais o erro médio é de %.1f ms. Nos %d registros em alerta,"
          % (mod["MAE"], len(res["alertas"])))
    print("que o modelo nunca viu, o erro médio sobe para %.1f ms:" % res["erro_medio_alertas"])
    for (_, l), prev in zip(res["alertas"].iterrows(), res["previsto_alertas"]):
        print("  Ciclo %d | %s | observada %6.1f ms | esperada %6.1f ms | diferença %+6.1f ms"
              % (l["ciclo"], l["codigo_modulo"], l["latencia_obs"], prev, l["latencia_obs"] - prev))
    print("Quando a latência real se afasta muito do que o modelo espera, o SCIC")
    print("tem um sinal objetivo de que algo saiu do comportamento normal.")


def menu_modelo(df):
    """Opção 3 do menu principal: treina o modelo e mostra MAE, MSE, RMSE e R²."""
    res = avaliar_modelo(df)

    print("\n=== MODELO DE PREVISÃO DE LATÊNCIA (REGRESSÃO LINEAR) ===\n")
    print("Entradas (X): potência (P = V x I), ciclo e tipo do módulo")
    print("Saída (y):    latência observada (ms)")
    print("Treino: %d registros normais | Teste: %d registros normais"
          % (res["n_treino"], res["n_teste"]))

    mostrar_metricas(res)
    mostrar_interpretacao(res)

    try:
        caminho = gerar_grafico_previsao(res)
        print("\nGráfico salvo em: %s" % os.path.relpath(caminho))
    except ImportError:
        print("\n[aviso] matplotlib não instalado: gráfico não gerado.")


# Exemplo de execução direta: py modelo.py
if __name__ == "__main__":
    menu_modelo(dados.carregar_dados())