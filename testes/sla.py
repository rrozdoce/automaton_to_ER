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
    
    def eh_afd(self):
        # Verifica se o AFN é um AFD
        for (estado, simbolo), destinos in self.transicoes.items():
            if len(destinos) > 1:
                return False
        return True


class AFD:
    def __init__(self, estados=None, alfabeto=None, transicoes=None, estado_inicial=None, estados_finais=None):
        self.estados = estados if estados is not None else []
        self.alfabeto = alfabeto if alfabeto is not None else []
        self.transicoes = transicoes if transicoes is not None else {}
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais if estados_finais is not None else []

    @classmethod
    def converter_afn_para_afd(cls, afn):
        if afn.eh_afd():
            print("O automato já é um AFD.")
            return AFD(
                estados=afn.estados,
                alfabeto=afn.alfabeto,
                transicoes=afn.transicoes,
                estado_inicial=afn.estado_inicial,
                estados_finais=afn.estados_finais
            )
               
        afd = cls()
        afd.alfabeto = [simbolo for simbolo in afn.alfabeto if simbolo != '']
        afd_estado_inicial = afn.epsilon_fechamento([afn.estado_inicial])

        pilha = [afd_estado_inicial]
        visitados = set()

        while pilha:
            conjunto = pilha.pop()
            conjunto_str = ''.join(conjunto) if conjunto else ''
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
                destino_str = ''.join(epsilon_destinos) if epsilon_destinos else ''

                afd.transicoes[(conjunto_str, simbolo)] = destino_str

                if destino_str and destino_str not in visitados:
                    pilha.append(epsilon_destinos)

        afd.estado_inicial = ''.join(afd_estado_inicial) if afd_estado_inicial else ''
        return afd
    
    def criar_er(self):
        # Inicializando a variável que irá armazenar a ER
        er = ""
        estado_atual = None
        
        # Percorrer todas as transições do AFD
        for (estado_origem, simbolo), estado_destino in self.transicoes.items():
            if estado_origem == estado_destino:
                # Loop (usando fechamento de Kleene para loops)
                er += f"{simbolo}*"
            else:
                # Transição normal
                if estado_atual != estado_origem:
                    if estado_atual is not None:
                        er += "+"
                    estado_atual = estado_origem
                er += f"{simbolo}"
        
        return er

def ler_entradas_usuario():
    print("---------Conversão AFN para AFD---------------")
    estados = input("Informe os estados (separados por vírgula): ").split(",")
    alfabeto = input("Informe o alfabeto (separados por vírgula): ").split(",")
    alfabeto.append('')  # Adicionando o símbolo vazio ao alfabeto
    transicoes = {}

    print("Informe as transições (pressione Enter para nenhuma transição):")
    for estado in estados:
        for simbolo in alfabeto:
            entrada = input(f"D({estado},{'ε' if simbolo == '' else simbolo}): ").strip()
            if entrada == '':
                transicoes[(estado, simbolo)] = []
            else:
                transicoes[(estado, simbolo)] = entrada.split(",")

    estado_inicial = input("Informe o estado inicial: ").strip()
    estados_de_aceitacao = input("Informe o(s) estado(s) de aceitação (separados por vírgula): ").split(",")

    return AFN(estados, alfabeto, transicoes, estado_inicial, estados_de_aceitacao)

# Leitura das entradas do usuário
afn = ler_entradas_usuario()

# Chamada da função para converter o AFN em AFD
afd = AFD.converter_afn_para_afd(afn)

# Geração da expressão regular
er = afd.criar_er()

print("Expressão regular gerada:")
print(er)