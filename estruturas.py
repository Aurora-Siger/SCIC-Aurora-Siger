"""
estruturas.py - Heap para priorizar alertas e Trie para busca por prefixo   [Mirela]
Apenas Python puro (sem heapq).
"""


# ===========================================================================
# 1. HEAP (fila de prioridade de alertas)
# ===========================================================================
class HeapAlertas:
    """Max-heap: o alerta mais urgente fica sempre na raiz (posicao 0).

    Na lista, as posicoes se relacionam assim:
    - pai do elemento i    -> (i - 1) // 2
    - filho esquerdo de i  -> 2 * i + 1
    - filho direito de i   -> 2 * i + 2
    """

    def __init__(self):
        self.itens = []   # lista de tuplas (prioridade_calculada, alerta)

    @staticmethod
    def calcular_prioridade(alerta):
        """Calcula a prioridade de um alerta (dicionario com a linha do CSV):
        - prioridade_alerta x 10
        - +5 se a latencia observada for maior que a prevista
        - +5 se o tipo for comunicacao ou suporte a vida
        """
        # int() e float() garantem que sao numeros (no CSV tudo vem como texto)
        prioridade = int(alerta["prioridade_alerta"]) * 10

        if float(alerta["latencia_obs"]) > float(alerta["latencia_prev"]):
            prioridade += 5

        if str(alerta["tipo"]).lower() in ("comunicação", "suporte à vida"):
            prioridade += 5

        return prioridade

    def inserir(self, alerta):
        """Adiciona o alerta no fim da lista e chama heapify_up."""
        prioridade = self.calcular_prioridade(alerta)
        self.itens.append((prioridade, alerta))   # entra no final da lista
        self.heapify_up(len(self.itens) - 1)      # sobe ate o lugar certo

    def remover_mais_urgente(self):
        """Troca a raiz com o ultimo, remove (pop) e chama heapify_down."""
        if self.esta_vazio():
            return None   # nao tem nenhum alerta para remover

        # Troca a raiz (mais urgente) com o ultimo elemento da lista
        self.itens[0], self.itens[-1] = self.itens[-1], self.itens[0]

        # Tira o ultimo, que agora e o mais urgente
        prioridade, alerta = self.itens.pop()

        # Quem foi parar na raiz pode estar no lugar errado, entao desce ele
        if self.itens:
            self.heapify_down(0)

        return alerta

    def heapify_up(self, indice):
        """Sobe o elemento enquanto ele for maior que o pai."""
        while indice > 0:
            pai = (indice - 1) // 2

            # Compara so a prioridade (posicao [0] da tupla)
            if self.itens[indice][0] > self.itens[pai][0]:
                # Maior que o pai: troca de lugar com ele
                self.itens[indice], self.itens[pai] = self.itens[pai], self.itens[indice]
                indice = pai   # continua a partir da nova posicao
            else:
                break          # ja esta no lugar certo

    def heapify_down(self, indice):
        """Desce o elemento enquanto algum filho for maior que ele."""
        tamanho = len(self.itens)

        while True:
            esquerdo = 2 * indice + 1
            direito = 2 * indice + 2
            maior = indice   # comeco achando que o maior e o proprio elemento

            # O filho esquerdo e maior?
            if esquerdo < tamanho and self.itens[esquerdo][0] > self.itens[maior][0]:
                maior = esquerdo

            # O filho direito e ainda maior?
            if direito < tamanho and self.itens[direito][0] > self.itens[maior][0]:
                maior = direito

            # Se nenhum filho e maior, o elemento ja esta no lugar certo
            if maior == indice:
                break

            # Senao, troca com o maior filho e continua descendo
            self.itens[indice], self.itens[maior] = self.itens[maior], self.itens[indice]
            indice = maior

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
        palavra = palavra.lower()   # converto tudo para minusculas
        no = self.raiz

        for letra in palavra:
            # Se esse caminho ainda nao existe, cria um no novo
            if letra not in no.filhos:
                no.filhos[letra] = NoTrie()
            no = no.filhos[letra]   # desce para o no da letra

        no.fim = True   # marca que aqui termina uma palavra

    def buscar_prefixo(self, prefixo):
        """Retorna a lista de palavras que comecam com o prefixo."""
        prefixo = prefixo.lower()
        no = self.raiz

        # Primeiro, sigo o caminho das letras do prefixo
        for letra in prefixo:
            if letra not in no.filhos:
                return []   # esse prefixo nao existe na trie
            no = no.filhos[letra]

        # Depois, a partir desse no, junto todas as palavras que continuam
        resultados = []
        self._coletar(no, prefixo, resultados)
        return resultados

    def _coletar(self, no, palavra_atual, resultados):
        """Auxiliar: percorre os nos abaixo e guarda as palavras completas."""
        # Se aqui termina uma palavra, adiciona na lista
        if no.fim:
            resultados.append(palavra_atual)

        # Continua por cada filho (em ordem alfabetica)
        for letra in sorted(no.filhos):
            self._coletar(no.filhos[letra], palavra_atual + letra, resultados)


# ===========================================================================
# 3. OPCOES DO MENU
# ===========================================================================
def montar_heap_alertas(df):
    """Coloca no heap todos os registros com status 'alerta' da base."""
    heap = HeapAlertas()
    for _, linha in df[df["status"] == "alerta"].iterrows():
        heap.inserir(linha.to_dict())   # cada alerta vira um dicionario
    return heap


def menu_heap(df):
    """Opcao 4 do menu: monta o heap com os alertas e mostra a ordem de urgencia."""
    heap = montar_heap_alertas(df)
    total = len(heap.itens)

    print("\n=== PRIORIZAÇÃO DE ALERTAS (HEAP) ===\n")
    print("Alertas inseridos no heap: %d" % total)
    print("Raiz do heap (mais urgente): %s, ciclo %d, prioridade %d"
          % (heap.itens[0][1]["codigo_modulo"], heap.itens[0][1]["ciclo"], heap.itens[0][0]))

    print("\nOrdem de atendimento (removendo sempre a raiz):\n")
    print("%-3s %-11s %-28s %5s %9s %9s %10s" % ("#", "Código", "Módulo", "Ciclo",
          "Obs(ms)", "Prev(ms)", "Prioridade"))
    posicao = 1
    while not heap.esta_vazio():
        alerta = heap.remover_mais_urgente()
        print("%-3d %-11s %-28s %5d %9.1f %9.1f %10d" % (
            posicao, alerta["codigo_modulo"], str(alerta["modulo"])[:28], alerta["ciclo"],
            alerta["latencia_obs"], alerta["latencia_prev"],
            HeapAlertas.calcular_prioridade(alerta)))
        posicao += 1

    print("\nPrioridade = prioridade_alerta x 10, +5 se a latência ficou acima da")
    print("prevista, +5 se o módulo for de comunicação ou suporte à vida.")
    print("\nPor que heap? O alerta mais urgente fica sempre na raiz (posição 0).")
    print("Inserir ou remover custa O(log n): com %d alertas, no máximo %d trocas."
          % (total, max(1, total.bit_length() - 1)))
    print("Numa lista comum, achar o mais urgente exigiria percorrer tudo: O(n).")


def montar_trie(df):
    """Insere na trie os codigos dos modulos, os nomes e os codigos dos sensores.
    Retorna a trie e um dicionario palavra -> codigo do modulo, para mostrar
    os detalhes de cada resultado.
    """
    trie = Trie()
    referencia = {}
    modulos = df.drop_duplicates("codigo_modulo")
    for _, linha in modulos.iterrows():
        for palavra in (linha["codigo_modulo"], linha["modulo"], str(linha["codigo_sensor"])):
            trie.inserir(palavra)
            referencia[palavra.lower()] = linha["codigo_modulo"]
    return trie, referencia


def menu_trie(df):
    """Opcao 5 do menu: busca modulos e codigos pelo prefixo digitado."""
    trie, referencia = montar_trie(df)
    modulos = df.drop_duplicates("codigo_modulo").set_index("codigo_modulo")

    print("\n=== BUSCA POR PREFIXO (TRIE) ===\n")
    print("A trie guarda %d palavras: códigos dos módulos, nomes e códigos dos sensores."
          % len(referencia))
    print("Exemplos: 'mod-s', 'com', 'sis', '17'")

    while True:
        prefixo = input("\nDigite um prefixo (Enter para voltar): ").strip()
        if not prefixo:
            break

        resultados = trie.buscar_prefixo(prefixo)
        if not resultados:
            print("Nenhum registro começa com '%s'." % prefixo)
            continue

        print("%d resultado(s):" % len(resultados))
        for palavra in resultados:
            codigo = referencia[palavra]
            info = modulos.loc[codigo]
            print("  %-30s -> %s | %s | sensor %d"
                  % (palavra, codigo, info["modulo"], info["codigo_sensor"]))

    print("\nPor que trie? A busca segue só as letras do prefixo (O(m), m = tamanho")
    print("do prefixo), sem comparar com todas as palavras da base.")


# Exemplo de execucao direta: py estruturas.py
if __name__ == "__main__":
    import dados
    base = dados.carregar_dados()
    menu_heap(base)
    trie, _ = montar_trie(base)
    print("\nTeste da trie: 'mod-s' ->", trie.buscar_prefixo("mod-s"))
    print("Teste da trie: 'com'   ->", trie.buscar_prefixo("com"))
