"""
analise.py - Indicadores de comunicação e erros numéricos   [Isabelle]

Este arquivo cuida da análise numérica do SCIC (seção 5.2 do enunciado):
- calcular_erros: erro absoluto e relativo entre latência prevista e observada
- classificar_erro: diz se o erro é aceitável, de atenção ou crítico
- calcular_indicadores: indicadores gerais de comunicação da colônia
- erros_por_modulo: compara módulos com escalas diferentes de latência
- demonstrar_ponto_flutuante: mostra diferenças causadas por arredondamento
- gerar_grafico_erros: salva o gráfico em graficos_ou_imagens/
- menu_analise / analise_final: opções 2 e 7 do menu principal
"""

import math
import os

# Limites de erro relativo usados em todo o sistema
LIMITE_ACEITAVEL = 0.10   # até 10%: variação normal da rede da colônia
LIMITE_CRITICO = 0.25     # acima de 25%: risco de atraso em comandos e alertas

PASTA_GRAFICOS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "graficos_ou_imagens")


# ===========================================================================
# 1. ERROS NUMÉRICOS
# ===========================================================================
def classificar_erro(erro_relativo):
    """Classifica o erro relativo de acordo com os limites da colônia."""
    if erro_relativo <= LIMITE_ACEITAVEL:
        return "aceitável"
    elif erro_relativo <= LIMITE_CRITICO:
        return "atenção"
    return "crítico"


def calcular_erros(df):
    """Acrescenta ao DataFrame as colunas de erro (sem alterar o original).

    erro_abs = |latência observada - latência prevista|      (em ms)
    erro_rel = erro_abs / latência observada                  (fração; 0.10 = 10%)

    O erro absoluto diz QUANTOS ms o modelo errou. O erro relativo diz o
    quanto isso pesa para aquele módulo: 20 ms de erro é grave para um
    módulo de 80 ms, mas pequeno para um de 300 ms.
    """
    df = df.copy()
    df["erro_abs"] = (df["latencia_obs"] - df["latencia_prev"]).abs()
    # Proteção: latência observada igual a 0 não permite dividir
    df["erro_rel"] = df.apply(
        lambda l: l["erro_abs"] / l["latencia_obs"] if l["latencia_obs"] != 0 else float("nan"),
        axis=1)
    df["classificacao"] = df["erro_rel"].apply(classificar_erro)
    return df


# ===========================================================================
# 2. INDICADORES DE COMUNICAÇÃO
# ===========================================================================
def calcular_indicadores(df):
    """Calcula os indicadores gerais de comunicação da colônia.
    Recebe o DataFrame já com as colunas de erro (calcular_erros).
    """
    return {
        "latencia_media_obs": df["latencia_obs"].mean(),
        "latencia_media_prev": df["latencia_prev"].mean(),
        # Indicador principal: quantos registros ficaram acima do previsto
        "pct_acima_previsto": (df["latencia_obs"] > df["latencia_prev"]).mean() * 100,
        "erro_abs_medio": df["erro_abs"].mean(),
        "erro_rel_medio": df["erro_rel"].mean() * 100,
        "pct_aceitavel": (df["classificacao"] == "aceitável").mean() * 100,
        "qtd_atencao": int((df["classificacao"] == "atenção").sum()),
        "qtd_critico": int((df["classificacao"] == "crítico").sum()),
        "disponibilidade": (df["status"] == "ativo").mean() * 100,
    }


def erros_por_modulo(df):
    """Agrupa os erros por módulo para comparar escalas diferentes."""
    tabela = df.groupby(["codigo_modulo", "modulo", "tipo"]).agg(
        latencia_media=("latencia_obs", "mean"),
        erro_abs_medio=("erro_abs", "mean"),
        erro_rel_medio=("erro_rel", "mean"),
        erro_rel_max=("erro_rel", "max"),
        alertas=("status", lambda s: int((s == "alerta").sum())),
    ).reset_index()
    return tabela.sort_values("erro_rel_medio", ascending=False)


def latencia_por_ciclo(df):
    """Latência média observada em cada ciclo (tendência ao longo do tempo)."""
    return df.groupby("ciclo")["latencia_obs"].mean()


# ===========================================================================
# 3. PONTO FLUTUANTE E ARREDONDAMENTO
# ===========================================================================
def demonstrar_ponto_flutuante(df):
    """Mostra por que comparar números decimais exige cuidado."""
    print("\n--- Ponto flutuante e arredondamento ---")

    # O computador guarda números em binário, e 0.1 não tem representação exata
    soma = 0.1 + 0.2
    print("0.1 + 0.2 = %r" % soma)
    print("0.1 + 0.2 == 0.3  ->  %s" % (soma == 0.3))
    print("math.isclose(0.1 + 0.2, 0.3)  ->  %s" % math.isclose(soma, 0.3))

    # Exemplo com a própria base: o primeiro registro cuja subtração
    # observada - prevista não dá o valor "redondo" esperado
    for _, l in df.iterrows():
        diferenca = l["latencia_obs"] - l["latencia_prev"]
        esperado = round(diferenca, 1)
        if diferenca != esperado:
            desvio = abs(diferenca - esperado)
            print("\nExemplo da base (%s, ciclo %d):" % (l["codigo_modulo"], l["ciclo"]))
            print("%.1f - %.1f = %r   (o esperado seria %.1f)"
                  % (l["latencia_obs"], l["latencia_prev"], diferenca, esperado))
            print("Desvio causado pela representação binária: %.1e ms" % desvio)
            break

    print("\nConclusão: esse desvio é bilhões de vezes menor que a precisão do")
    print("sensor (0,1 ms) e não muda nenhuma decisão. Mesmo assim, o sistema")
    print("nunca compara decimais com ==: usa limites (10% e 25%) e arredonda")
    print("os valores só na hora de exibir.")


# ===========================================================================
# 4. GRÁFICO
# ===========================================================================
def gerar_grafico_erros(tabela):
    """Salva um gráfico de barras com o erro relativo médio de cada módulo."""
    import matplotlib
    matplotlib.use("Agg")            # gera o arquivo sem abrir janela
    import matplotlib.pyplot as plt

    os.makedirs(PASTA_GRAFICOS, exist_ok=True)
    caminho = os.path.join(PASTA_GRAFICOS, "erro_relativo_por_modulo.png")

    # Ordem crescente para o maior erro ficar no topo do gráfico
    dados = tabela.sort_values("erro_rel_medio")
    rotulos = dados["codigo_modulo"] + "  " + dados["modulo"]
    valores = dados["erro_rel_medio"] * 100

    fig, ax = plt.subplots(figsize=(9, 4.8))
    barras = ax.barh(rotulos, valores, color="#2a78d6", height=0.6)

    # Linha do limite aceitável
    ax.axvline(LIMITE_ACEITAVEL * 100, color="#52514e", linestyle="--", linewidth=1)
    ax.text(LIMITE_ACEITAVEL * 100 + 0.2, len(dados) - 0.45, "limite aceitável (10%)",
            color="#52514e", fontsize=9, va="bottom")

    # Valor ao lado de cada barra
    for barra, valor in zip(barras, valores):
        ax.text(valor + 0.2, barra.get_y() + barra.get_height() / 2,
                "%.1f%%" % valor, va="center", fontsize=9, color="#0b0b0b")

    ax.set_title("Erro relativo médio da latência por módulo",
                 loc="left", fontsize=12, color="#0b0b0b", pad=16)
    ax.set_xlabel("Erro relativo médio (%)", color="#52514e")
    ax.set_xlim(0, max(valores.max(), LIMITE_ACEITAVEL * 100) * 1.25)
    for lado in ["top", "right"]:
        ax.spines[lado].set_visible(False)
    ax.tick_params(colors="#52514e")
    ax.grid(axis="x", color="#e6e6e3", linewidth=0.8)
    ax.set_axisbelow(True)

    fig.tight_layout()
    fig.savefig(caminho, dpi=150)
    plt.close(fig)
    return caminho


# ===========================================================================
# 5. OPÇÕES DO MENU
# ===========================================================================
def mostrar_indicadores(ind):
    """Exibe os indicadores no terminal."""
    print("\n=== INDICADORES DE COMUNICAÇÃO DA COLÔNIA ===\n")
    print("Latência média observada:      %7.1f ms" % ind["latencia_media_obs"])
    print("Latência média prevista:       %7.1f ms" % ind["latencia_media_prev"])
    print("Registros acima do previsto:   %7.1f %%" % ind["pct_acima_previsto"])
    print("Erro absoluto médio:           %7.1f ms" % ind["erro_abs_medio"])
    print("Erro relativo médio:           %7.1f %%" % ind["erro_rel_medio"])
    print("Registros com erro aceitável:  %7.1f %%" % ind["pct_aceitavel"])
    print("Registros em atenção (10-25%%): %5d" % ind["qtd_atencao"])
    print("Registros críticos (>25%%):     %5d" % ind["qtd_critico"])
    print("Disponibilidade (status ativo):%7.1f %%" % ind["disponibilidade"])


def mostrar_tabela_modulos(tabela):
    """Exibe a comparação de erros entre os módulos."""
    print("\n--- Erros por módulo (do maior para o menor erro relativo) ---\n")
    print("%-11s %-28s %9s %10s %9s %9s %8s" % ("Código", "Módulo", "Lat.(ms)",
          "Erro(ms)", "Erro rel", "Pior", "Alertas"))
    for _, l in tabela.iterrows():
        print("%-11s %-28s %9.1f %10.1f %8.1f%% %8.1f%% %8d" % (
            l["codigo_modulo"], l["modulo"][:28], l["latencia_media"],
            l["erro_abs_medio"], l["erro_rel_medio"] * 100,
            l["erro_rel_max"] * 100, l["alertas"]))


def mostrar_criticos(df):
    """Lista os registros com erro relativo acima do limite crítico."""
    criticos = df[df["classificacao"] == "crítico"].sort_values("erro_rel", ascending=False)
    print("\n--- Registros críticos (erro relativo > %d%%) ---\n" % (LIMITE_CRITICO * 100))
    for _, l in criticos.iterrows():
        print("Ciclo %d | %s %-28s | obs %6.1f ms | prev %6.1f ms | erro %5.1f ms (%.1f%%)" % (
            l["ciclo"], l["codigo_modulo"], l["modulo"][:28], l["latencia_obs"],
            l["latencia_prev"], l["erro_abs"], l["erro_rel"] * 100))


def menu_analise(df):
    """Opção 2 do menu principal: indicadores e erros numéricos."""
    df_erros = calcular_erros(df)
    tabela = erros_por_modulo(df_erros)

    mostrar_indicadores(calcular_indicadores(df_erros))
    mostrar_tabela_modulos(tabela)
    mostrar_criticos(df_erros)
    demonstrar_ponto_flutuante(df_erros)

    try:
        caminho = gerar_grafico_erros(tabela)
        print("\nGráfico salvo em: %s" % os.path.relpath(caminho))
    except ImportError:
        print("\n[aviso] matplotlib não instalado: gráfico não gerado.")


def analise_final(df):
    """Opção 7 do menu principal: resumo final dos resultados do SCIC."""
    df_erros = calcular_erros(df)
    ind = calcular_indicadores(df_erros)
    tabela = erros_por_modulo(df_erros)
    pior = tabela.iloc[0]
    por_ciclo = latencia_por_ciclo(df_erros)

    print("\n=== ANÁLISE FINAL DO SCIC ===\n")
    print("1. Situação geral")
    print("   %.1f%% dos registros têm erro aceitável (até 10%%), mas %.1f%% ficaram"
          % (ind["pct_aceitavel"], ind["pct_acima_previsto"]))
    print("   acima da latência prevista: o modelo atual tende a subestimar a latência.")

    print("\n2. Módulo mais preocupante")
    print("   %s (%s): erro relativo médio de %.1f%%, pior caso de %.1f%%"
          % (pior["codigo_modulo"], pior["modulo"], pior["erro_rel_medio"] * 100,
             pior["erro_rel_max"] * 100))
    print("   e %d alerta(s) no período." % pior["alertas"])
    if pior["tipo"] == "comunicação":
        print("   Como os alertas de todos os módulos dependem da comunicação, uma")
        print("   falha aqui atrasa a resposta da colônia inteira: prioridade máxima.")
    else:
        print("   Esse módulo deve entrar como prioridade na manutenção preventiva.")

    print("\n3. Tendência ao longo do tempo")
    print("   A latência média passou de %.1f ms no ciclo %d para %.1f ms no ciclo %d"
          % (por_ciclo.iloc[0], por_ciclo.index[0], por_ciclo.iloc[-1], por_ciclo.index[-1]))
    variacao = (por_ciclo.iloc[-1] / por_ciclo.iloc[0] - 1) * 100
    print("   (variação de %+.1f%%), indicando aumento gradual de carga na rede." % variacao)

    print("\n4. Recomendações")
    print("   - Monitoramento contínuo dos módulos com erro acima de 10%")
    print("   - Enlace redundante para o módulo de Comunicação")
    print("   - Manutenção preditiva usando o modelo de previsão de latência")
    print("   - Validação humana das decisões automáticas em alertas críticos")


# Exemplo de execução direta: python analise.py
if __name__ == "__main__":
    import dados
    menu_analise(dados.carregar_dados())
    analise_final(dados.carregar_dados())
