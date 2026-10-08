"""
============================================================================
 SCIC - Sistema de Comunicacao Interplanetaria da Colonia
 Colonia Aurora Siger  |  Fase 6 - "Comunicacao interplanetaria"
============================================================================
 Arquivo principal do sistema: execute este arquivo.
 Ele exibe o menu no terminal e chama as funcoes dos demais modulos:

   dados.py       -> leitura e consulta da base (Pandas)          [Isabelle]
   analise.py     -> indicadores, erro absoluto e relativo         [Isabelle]
   modelo.py      -> regressao linear e metricas (scikit-learn)    [Isabelle]
   estruturas.py  -> heap (alertas) e trie (busca por prefixo)     [Mirela]
   hardware.py    -> bases numericas, potencia e Lei de Ohm        [Mirela]
============================================================================
"""

import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import dados
import analise
import modelo
import estruturas
import hardware


# ===========================================================================
# 1. MENU PRINCIPAL
# ===========================================================================
MENU = """
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
╚══════════════════════════════════════════════════════╝"""


def executar(funcao, df):
    """Executa a funcao de uma opcao do menu.
    Enquanto a funcao nao estiver pronta, mostra um aviso em vez de quebrar.
    """
    try:
        funcao(df)
    except NotImplementedError:
        print("\n[em desenvolvimento] Esta opção ainda não foi implementada.")


def main():
    df = dados.carregar_dados()
    print("\nBase carregada: %d registros." % len(df))

    opcoes = {
        "1": dados.menu_consultas,
        "2": analise.menu_analise,
        "3": modelo.menu_modelo,
        "4": estruturas.menu_heap,
        "5": estruturas.menu_trie,
        "6": hardware.menu_hardware,
        "7": analise.analise_final,
    }

    while True:
        print(MENU)
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "0":
            print("\nEncerrando o SCIC. Até logo!")
            break
        if escolha in opcoes:
            executar(opcoes[escolha], df)
        else:
            print("\nOpção inválida. Digite um número de 0 a 7.")
        input("\nPressione Enter para voltar ao menu...")


if __name__ == "__main__":
    main()
