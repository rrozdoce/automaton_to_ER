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
    
    def remover_estado(transicoes, alfabeto ,estado_remover):
        ...
    
    def criar_er(self):
        estados = self.estados.copy()  # Corrigido o uso de .copy()
        alfabeto = self.alfabeto.copy()
        estado_inicial = self.estado_inicial
        estados_finais = self.estados_finais.copy()
        transicoes = self.transicoes.copy()
    
        estado_start = 'qs'
        estado_accept = 'qa'
    
        estados.append(estado_start)
        estados.append(estado_accept)
    
        # Liga o estado start com o estado inicial
        transicoes[(estado_start, '')] = [estado_inicial]
    
        # Liga os estados finais com o estado de aceitação
    
        for estado in estados_finais:
            transicoes[(estado, '')] = estado_accept
        # Construção da expressão regular
        expressao_regular = {}
        string_aux = ''
        novo_alfabeto = alfabeto.copy()
    
        for estado in estados:
            if estado != estado_start:
                for simbolo in novo_alfabeto:
                    if transicoes.get((estado_start, simbolo)) == estado:
                        quantidade_estado = sum(1 for chave in transicoes if chave[0] == estado)
                    
                        # Caso existam várias transições do estado
                        if quantidade_estado > 1:
                            for simbolo_i in novo_alfabeto:
                                transicao_atual = transicoes.get((estado, simbolo_i))
                                if transicao_atual and transicao_atual != estado:
                                    transicoes[(estado_start, simbolo_i)] = transicao_atual
                                elif transicao_atual == estado:
                                    transicoes[(estado_start, simbolo_i + "*")] = transicao_atual
                                    novo_alfabeto.append(simbolo_i + "*")
                    
                        # Deleta a transição antiga
                        transicoes.pop((estado, simbolo), None)

        # Aqui você pode finalizar a construção da expressão regular
        # Usando `expressao_regular` para armazenar os resultados.
        return expressao_regular  # Retorna a expressão regular final


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
#er = afd.criar_er()
print(afd.estados)
print(afd.alfabeto)
print(afd.estado_inicial)
print(afd.estados_finais)

for transicoes in afd.transicoes.items():
    print(transicoes)