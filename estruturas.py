"""
estruturas.py - Heap para priorizar alertas e Trie para busca por prefixo   [Mirela]
Apenas Python puro (sem heapq).
"""


# ===========================================================================
# 1. HEAP (fila de prioridade de alertas)
# ===========================================================================
class HeapAlertas:
    """Max-heap: o alerta mais urgente fica sempre na raiz (posicao 0)."""

    def __init__(self):
        self.itens = []   # lista de tuplas (prioridade_calculada, alerta)

    def inserir(self, alerta):
        """Adiciona o alerta no fim da lista e chama heapify_up."""
        raise NotImplementedError

    def remover_mais_urgente(self):
        """Troca a raiz com o ultimo, remove (pop) e chama heapify_down."""
        raise NotImplementedError

    def heapify_up(self, indice):
        """Sobe o elemento enquanto ele for maior que o pai."""
        raise NotImplementedError

    def heapify_down(self, indice):
        """Desce o elemento enquanto algum filho for maior que ele."""
        raise NotImplementedError

    def esta_vazio(self):
        return len(self.itens) == 0


# ===========================================================================
# 2. TRIE (busca por prefixo)
# ===========================================================================
class NoTrie:
    def __init__(self):
        self.filhos = {}      # letra -> NoTrie
        self.fim = False      # True se uma palavra termina neste no


class Trie:
    def __init__(self):
        self.raiz = NoTrie()

    def inserir(self, palavra):
        """Insere a palavra (em minusculas) letra por letra."""
        raise NotImplementedError

    def buscar_prefixo(self, prefixo):
        """Retorna a lista de palavras que comecam com o prefixo."""
        raise NotImplementedError


# ===========================================================================
# 3. OPCOES DO MENU
# ===========================================================================
def menu_heap(df):
    """Opcao 4 do menu: monta o heap com os alertas e mostra a ordem de urgencia."""
    raise NotImplementedError


def menu_trie(df):
    """Opcao 5 do menu: busca modulos e codigos pelo prefixo digitado."""
    raise NotImplementedError
