"""
dados.py - Leitura, limpeza e consulta da base da Aurora Siger   [Isabelle]

Este arquivo cuida da base de dados do SCIC:
- carregar_dados: lê o CSV com Pandas e faz a limpeza básica
- resumo_base: mostra um panorama geral da colônia
- consultar_modulo / filtrar_por_status / filtrar_por_tipo: consultas simples
- menu_consultas: opção 1 do menu principal
"""

import os
import pandas as pd

# O CSV fica na mesma pasta deste arquivo
CAMINHO_DADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "dados_aurora_siger.csv")

# Colunas que precisam ser numéricas para os cálculos do sistema
COLUNAS_NUMERICAS = ["codigo_sensor", "latencia_obs", "latencia_prev",
                     "tensao", "corrente", "prioridade_alerta", "ciclo"]

# Colunas exibidas nas consultas (para a tabela caber no terminal)
COLUNAS_EXIBICAO = ["codigo_modulo", "modulo", "ciclo", "latencia_obs",
                    "latencia_prev", "status", "prioridade_alerta"]


# ===========================================================================
# 1. CARGA E LIMPEZA
# ===========================================================================
def carregar_dados(caminho=CAMINHO_DADOS, mostrar_limpeza=False):
    """Lê o CSV da colônia e devolve um DataFrame limpo.

    Limpeza aplicada:
      1. Remove espaços extras dos textos e padroniza status e tipo em minúsculas
      2. Converte as colunas numéricas (valor inválido vira NaN em vez de travar)
      3. Remove registros sem os campos essenciais para os cálculos
      4. Remove registros duplicados
    """
    df = pd.read_csv(caminho, encoding="utf-8")
    total_inicial = len(df)

    # 1. Textos: tira espaços e padroniza
    for coluna in ["codigo_modulo", "modulo", "tipo", "status", "mensagem"]:
        df[coluna] = df[coluna].astype(str).str.strip()
    df["status"] = df["status"].str.lower()
    df["tipo"] = df["tipo"].str.lower()
    df["codigo_modulo"] = df["codigo_modulo"].str.upper()

    # 2. Números: errors="coerce" transforma texto inválido em NaN
    for coluna in COLUNAS_NUMERICAS:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    # 3. Sem latência, tensão ou corrente não dá para calcular nada
    df = df.dropna(subset=["latencia_obs", "latencia_prev", "tensao", "corrente"])

    # 4. Duplicados
    df = df.drop_duplicates()

    # Colunas inteiras voltam a ser int (o NaN tinha transformado em float)
    for coluna in ["codigo_sensor", "prioridade_alerta", "ciclo"]:
        df[coluna] = df[coluna].fillna(0).astype(int)

    df = df.reset_index(drop=True)

    if mostrar_limpeza:
        print("Registros lidos: %d | removidos na limpeza: %d | válidos: %d"
              % (total_inicial, total_inicial - len(df), len(df)))
    return df


# ===========================================================================
# 2. CONSULTAS
# ===========================================================================
def resumo_base(df):
    """Mostra um panorama geral da base: módulos, ciclos e status."""
    print("\n=== RESUMO DA BASE DA COLÔNIA ===\n")
    print("Registros: %d" % len(df))
    print("Módulos monitorados: %d" % df["codigo_modulo"].nunique())
    print("Ciclos registrados: %d a %d" % (df["ciclo"].min(), df["ciclo"].max()))

    print("\nRegistros por status:")
    for status, qtd in df["status"].value_counts().items():
        print("  %-12s %3d  (%.1f%%)" % (status, qtd, qtd / len(df) * 100))

    print("\nMódulos da colônia:")
    modulos = df.drop_duplicates("codigo_modulo").sort_values("codigo_modulo")
    for _, linha in modulos.iterrows():
        print("  %s  %-30s (%s)" % (linha["codigo_modulo"], linha["modulo"], linha["tipo"]))


def consultar_modulo(df, termo):
    """Busca registros pelo código ou por parte do nome do módulo.
    Ex.: 'MOD-CM-008', 'CM-008' ou 'comunic' encontram o módulo de Comunicação.
    """
    termo = termo.strip().lower()
    filtro = (df["codigo_modulo"].str.lower().str.contains(termo, regex=False)
              | df["modulo"].str.lower().str.contains(termo, regex=False))
    return df[filtro]


def filtrar_por_status(df, status):
    """Retorna os registros com o status informado (ativo, manutenção, alerta)."""
    return df[df["status"] == status.strip().lower()]


def filtrar_por_tipo(df, tipo):
    """Retorna os registros do tipo informado (comunicação, energia...)."""
    return df[df["tipo"] == tipo.strip().lower()]


def mostrar_registros(registros):
    """Exibe os registros em tabela ou avisa quando não há resultado."""
    if registros.empty:
        print("\nNenhum registro encontrado.")
    else:
        print()
        print(registros[COLUNAS_EXIBICAO].to_string(index=False))
        print("\n%d registro(s) encontrado(s)." % len(registros))


# ===========================================================================
# 3. OPÇÃO DO MENU
# ===========================================================================
def menu_consultas(df):
    """Opção 1 do menu principal: submenu de consultas à base."""
    while True:
        print("\n--- CONSULTAR REGISTROS ---")
        print("1. Resumo da base")
        print("2. Buscar por módulo (código ou nome)")
        print("3. Filtrar por status")
        print("4. Filtrar por tipo de módulo")
        print("0. Voltar")
        opcao = input("Escolha: ").strip()

        if opcao == "0":
            break
        elif opcao == "1":
            resumo_base(df)
        elif opcao == "2":
            termo = input("Código ou nome do módulo (ex.: CM-008): ")
            mostrar_registros(consultar_modulo(df, termo))
        elif opcao == "3":
            opcoes = ", ".join(sorted(df["status"].unique()))
            status = input("Status (%s): " % opcoes)
            mostrar_registros(filtrar_por_status(df, status))
        elif opcao == "4":
            opcoes = ", ".join(sorted(df["tipo"].unique()))
            tipo = input("Tipo (%s): " % opcoes)
            mostrar_registros(filtrar_por_tipo(df, tipo))
        else:
            print("Opção inválida.")


# Exemplo de execução direta: python dados.py
if __name__ == "__main__":
    base = carregar_dados(mostrar_limpeza=True)
    resumo_base(base)
    print("\nExemplo - registros em alerta:")
    mostrar_registros(filtrar_por_status(base, "alerta"))
