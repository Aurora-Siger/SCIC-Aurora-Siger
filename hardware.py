"""
hardware.py - SCIC (Fase 6)

Este arquivo tem 3 funções que trabalham com os dados dos sensores:
- converter_bases: mostra o código do sensor em binário e hexadecimal
- calcular_potencia: calcula a potência (P = V x I)
- calcular_resistencia: calcula a resistência (R = V / I)

Só usei Python puro (módulos csv e os, que já vêm com o Python).
"""

import csv  # para ler o arquivo CSV
import os   # para achar a pasta onde o arquivo está


def converter_bases(codigo):
    """
    Pega o código do sensor (número decimal) e devolve ele escrito
    em binário e em hexadecimal.

    Exemplo: 172 -> ('10101100', 'AC')
    """
    # No CSV tudo vem como texto, então transformo em número inteiro
    codigo = int(codigo)

    # bin() devolve '0b10101100'. O [2:] tira o '0b' do começo
    binario = bin(codigo)[2:]

    # hex() devolve '0xac'. O [2:] tira o '0x' e o upper() deixa a letra maiúscula
    hexadecimal = hex(codigo)[2:].upper()

    return binario, hexadecimal


def calcular_potencia(tensao, corrente):
    """
    Calcula a potência em watts (W): tensão x corrente.

    tensao   -> volts (V)
    corrente -> amperes (A)
    """
    # float() transforma o texto do CSV em número com vírgula para poder multiplicar
    return float(tensao) * float(corrente)


def calcular_resistencia(tensao, corrente):
    """
    Calcula a resistência em ohms: tensão / corrente (Lei de Ohm).

    Se a corrente for 0, não dá para dividir, então devolvo
    uma mensagem de erro no lugar do resultado.
    """
    tensao = float(tensao)
    corrente = float(corrente)

    # Dividir por zero não existe e travaria o programa, por isso faço essa checagem
    if corrente == 0:
        return "Erro: corrente igual a 0, não é possível calcular a resistência."

    return tensao / corrente


def menu_hardware(df):
    """
    Opção 6 do menu do SCIC: aplica as 3 funções acima a todos os
    módulos da colônia (usa o último ciclo registrado de cada módulo).
    df -> DataFrame com os dados do CSV (vem do codigo_fonte.py)
    """
    # Pego só a última linha de cada módulo para não repetir 6 vezes o mesmo
    ultimos = df.sort_values("ciclo").groupby("codigo_modulo").tail(1)

    print("\n=== HARDWARE: BASES NUMÉRICAS E ELETRICIDADE ===\n")
    print(f"{'Módulo':<12}{'Sensor':>7}{'Binário':>11}{'Hexa':>6}"
          f"{'Tensão(V)':>11}{'Corrente(A)':>13}{'Potência(W)':>13}{'Resist.(Ω)':>12}")
    print("-" * 85)

    for _, linha in ultimos.sort_values("codigo_modulo").iterrows():
        binario, hexa = converter_bases(linha["codigo_sensor"])
        potencia = calcular_potencia(linha["tensao"], linha["corrente"])
        resistencia = calcular_resistencia(linha["tensao"], linha["corrente"])
        # Se voltou texto (corrente 0), mostro "erro" no lugar do número
        res_txt = "erro" if isinstance(resistencia, str) else f"{resistencia:.2f}"
        print(f"{linha['codigo_modulo']:<12}{linha['codigo_sensor']:>7}{binario:>11}{hexa:>6}"
              f"{linha['tensao']:>11.2f}{linha['corrente']:>13.2f}{potencia:>13.2f}{res_txt:>12}")

    # Consulta livre: o usuário digita um código e vê a conversão
    codigo = input("\nDigite um código de sensor para converter (Enter para pular): ").strip()
    if codigo:
        if codigo.isdigit():
            binario, hexa = converter_bases(codigo)
            print(f"Decimal {codigo} -> binário {binario} -> hexadecimal {hexa}")
        else:
            print("Código inválido: digite apenas números.")


# ---------------------------------------------------------------
# Exemplo: lê as primeiras linhas do CSV e mostra os resultados
# ---------------------------------------------------------------
# Esse if faz o exemplo rodar só quando eu executo este arquivo direto.
# Se outro arquivo importar as funções, o exemplo não roda sozinho.
if __name__ == "__main__":
    NOME_CSV = "dados_aurora_siger.csv"  # nome do arquivo de dados
    QTD_LINHAS = 3                       # quantas linhas mostrar

    # Procuro o CSV na mesma pasta do hardware.py
    pasta = os.path.dirname(os.path.abspath(__file__))
    ARQUIVO_CSV = os.path.join(pasta, NOME_CSV)

    try:
        with open(ARQUIVO_CSV, newline="", encoding="utf-8") as arquivo:
            # DictReader usa a primeira linha (cabeçalho) como nome das colunas
            leitor = csv.DictReader(arquivo)

            # Passo pelas linhas uma de cada vez e paro quando chegar em 3
            for i, linha in enumerate(leitor):
                if i >= QTD_LINHAS:
                    break

                # Pego só as 3 colunas que preciso
                codigo = linha["codigo_sensor"]
                tensao = linha["tensao"]
                corrente = linha["corrente"]

                # Chamo as 3 funções com os dados da linha
                binario, hexa = converter_bases(codigo)
                potencia = calcular_potencia(tensao, corrente)
                resistencia = calcular_resistencia(tensao, corrente)

                # Mostro tudo no terminal (:.2f deixa só 2 casas decimais)
                print(f"Sensor {codigo}: binário = {binario}, hexadecimal = {hexa}")
                print(f"  Tensão = {tensao} V | Corrente = {corrente} A")
                print(f"  Potência = {potencia:.2f} W")

                # Se voltou texto, é a mensagem de erro (corrente 0)
                if isinstance(resistencia, str):
                    print(f"  Resistência = {resistencia}")
                else:
                    print(f"  Resistência = {resistencia:.2f} ohms")
                print("-" * 40)

    except FileNotFoundError:
        # Se o CSV não estiver na pasta, mostra um aviso em vez de dar erro
        print(f"Arquivo '{NOME_CSV}' não encontrado na pasta {pasta}.")
        print("Coloque o CSV na mesma pasta do hardware.py e confira o nome.")
