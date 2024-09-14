class AFN:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_finais):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais

    def epsilon_fechamento(self, estados):
        pilha = list(estados)
        fechamento = set(estados)

        while pilha:
            estado = pilha.pop()
            if (estado, '') in self.transicoes:
                destinos = self.transicoes[(estado, '')]
                for destino in destinos:
                    if destino not in fechamento:
                        fechamento.add(destino)
                        pilha.append(destino)

        return sorted(fechamento)

    def eh_deterministico(self):
        for (estado, simbolo), destinos in self.transicoes.items():
            if len(destinos) > 1 or '' in self.alfabeto:
                return False
        return True


class AFD:
    def __init__(self):
        self.estados = []
        self.alfabeto = []
        self.transicoes = {}
        self.estado_inicial = None
        self.estados_finais = []

    @classmethod
    def converter_afn_para_afd(cls, afn):
        if afn.eh_deterministico():
            print("O autômato fornecido já é um AFD.")
            return afn  # Retorna o próprio AFD sem modificações

        afd = cls()
        afd.alfabeto = [simbolo for simbolo in afn.alfabeto if simbolo != '']
        afd_estado_inicial = afn.epsilon_fechamento([afn.estado_inicial])

        pilha = [afd_estado_inicial]
        visitados = set()

        while pilha:
            conjunto = pilha.pop()
            conjunto_str = ''.join(conjunto) if conjunto else '∅'
            if conjunto_str in visitados:
                continue
            visitados.add(conjunto_str)
            afd.estados.append(conjunto_str)

            if any(estado in afn.estados_finais for estado in conjunto):
                afd.estados_finais.append(conjunto_str)

            for simbolo in afd.alfabeto:
                destinos = []
                for estado in conjunto:
                    if (estado, simbolo) in afn.transicoes:
                        destinos.extend(afn.transicoes[(estado, simbolo)])

                epsilon_destinos = afn.epsilon_fechamento(destinos)
                destino_str = ''.join(epsilon_destinos) if epsilon_destinos else '∅'

                afd.transicoes[(conjunto_str, simbolo)] = destino_str

                if destino_str and destino_str not in visitados:
                    pilha.append(epsilon_destinos)

        afd.estado_inicial = ''.join(afd_estado_inicial) if afd_estado_inicial else '∅'
        return afd

def ler_entradas_usuario():
    print("---------Conversão AFN/AFNe/AFD---------------")
    estados = input("Informe os estados: ").split(",")
    alfabeto = input("Informe o alfabeto: ").split(",")
    usa_epsilon = input("O autômato possui transições epsilon (S/N)? ").strip().upper()
    if usa_epsilon == 'S':
        alfabeto.append('')  # Adicionando o símbolo vazio ao alfabeto

    transicoes = {}

    print("Informe as transições:")
    for estado in estados:
        for simbolo in alfabeto:
            proximos_estados = input(f"D({estado},{simbolo}): ").split(",")
            transicoes[(estado, simbolo)] = proximos_estados

    estado_inicial = input("Informe o estado inicial: ")
    estados_de_aceitacao = input("Informe o(s) estado(s) de aceitação: ").split(",")

    return AFN(estados, alfabeto, transicoes, estado_inicial, estados_de_aceitacao)


# Leitura das entradas do usuário
afn = ler_entradas_usuario()

# Verifica se o AFN precisa ser convertido para AFD
afd = AFD.converter_afn_para_afd(afn)

# Exibindo os resultados
print("---------Resultado da Conversão---------")
print("Estados:")
for estado in afd.estados:
    print(estado)

print("\nAlfabeto:")
print(afd.alfabeto)

print("\nTransições:")
for transicao, destino in afd.transicoes.items():
    print(f"D({transicao[0]}, {transicao[1]}): {destino}")

print("\nEstado Inicial:")
print(afd.estado_inicial)

print("\nEstados Finais:")
for estado_final in afd.estados_finais:
    print(estado_final)