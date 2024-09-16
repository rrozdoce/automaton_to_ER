import copy

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
            #print("O automato já é um AFD.")
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

def ler_entradas_usuario():
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

def converter_transicoes(transicoes):
    transicoes_convertidas = []
    
    for (estado, simbolo), destino in transicoes.items():
        if destino:  # Verifica se o destino não está vazio
            if isinstance(destino, list):  # Se os destinos forem uma lista
                for d in destino:
                    transicoes_convertidas.append([estado, simbolo, d])
            else:  # Se o destino for uma string única
                transicoes_convertidas.append([estado, simbolo, destino])
    
    return transicoes_convertidas

def lerAFD(estados, alfabeto, transicoes, estado_inicial, estados_finais):
    # Cria o AFD
    AFD = {
        'estados': estados,
        'alfabeto': alfabeto,
        'funcao_transicao': transicoes,
        'estados_iniciais': [estado_inicial],
        'estados_finais': estados_finais
    }
    
    return AFD

def converterParaER(AFD):
    i = "q0"
    c = 0
    while i in AFD['estados']:
        c += 1
        i = "q"+str(c)

    AFD['estados'].append(i)
    AFD['funcao_transicao'].append([i, "$", AFD['estados_iniciais'][0]])
    AFD['estados_iniciais'] = [i]

    i = "q0"
    c = 0
    while i in AFD['estados']:
        c += 1
        i = "q"+str(c)

    AFD['estados'].append(i)
    for estado in AFD['estados_finais']:
        AFD['funcao_transicao'].append([estado, "$", i])
    AFD['estados_finais'] = [i]
    
    transicoes = {}
    for trans in AFD['funcao_transicao']:
        if len(trans) != 3:
            print(f"Transição inválida: {trans}. Esperado formato [estado, simbolo, estado].")
            continue
        if trans[0] not in transicoes.keys():
            transicoes[trans[0]] = {}
        transicoes[trans[0]][trans[1]] = trans[2]
    
    for estado in transicoes.keys():
        aAlterar = []
        for alfabeto1 in transicoes[estado].keys():
            for alfabeto2 in transicoes[estado].keys():
                if alfabeto1 != alfabeto2 and transicoes[estado][alfabeto1] == transicoes[estado][alfabeto2]:
                    destino = transicoes[estado][alfabeto1]
                    aAlterar.append([alfabeto1, destino, 0])
                    aAlterar.append([alfabeto2, destino, 0])
    
        aAlterar = [list(x) for x in set(tuple(x) for x in aAlterar)]
    
        flag = True
        while flag:
            flag = False
            for exp1 in aAlterar:
                for exp2 in aAlterar:
                    if exp1[0] != exp2[0] and exp1[1] == exp2[1]:
                        if exp1[2] == 0:
                            exp1[0] += "+"+exp2[0]
                            exp1[2] = 1
                            exp2[2] = 1
                            aAlterar.remove(exp2)
                            flag = True
                        elif exp2[2] == 0:
                            exp1[0] += "+"+exp2[0]
                            exp1[2] = 1
                            exp2[2] = 1
                            aAlterar.remove(exp2)
                            flag = True
        aExcluir = []
        for chave in transicoes[estado].keys():
            for trans in aAlterar:
                if chave in trans[0]:
                    aExcluir.append(chave)
        for chave in aExcluir:
            del transicoes[estado][chave]
              
        for trans in aAlterar:
            transicoes[estado][trans[0]] = trans[1]
        
    AFD['funcao_transicao'] = []
    for estado in transicoes.keys():
        for alfabeto in transicoes[estado].keys():
            AFD['funcao_transicao'].append([estado, alfabeto, transicoes[estado][alfabeto]])
    
    while len(AFD['estados']) > 2:
        novasTransicoes = copy.deepcopy(AFD['funcao_transicao'])
        
        estadoEliminar = ""
        for estado in AFD['estados']:
            if estado not in AFD['estados_iniciais'] and estado not in AFD['estados_finais']:
                estadoEliminar = estado
                break
        for estado1 in AFD['estados']:
            for estado2 in AFD['estados']:
                if estado1 in AFD['estados_finais']:
                    continue
                if estado2 in AFD['estados_iniciais']:
                    continue
                R1 = ""
                R2 = ""
                R3 = ""
                R4 = ""
                for trans in AFD['funcao_transicao']:
                    if trans[0] == estado1 and trans[2] == estadoEliminar:
                        R1 = trans[1]
                    if trans[0] == estadoEliminar and trans[2] == estadoEliminar:
                        R2 = trans[1]
                    if trans[0] == estadoEliminar and trans[2] == estado2:
                        R3 = trans[1]
                    if trans[0] == estado1 and trans[2] == estado2:
                        R4 = trans[1]
                
                
                R = ""
                if R1 and R3:
                    if R1 and R1 != "$":
                        R += R1
                    if R2 and R2 != "$":
                        R += R2 + "*"
                    if R3 and R3 != "$":
                        R += R3
                        
                    if R4:
                        R += "+"+R4 
                else:
                    R = R4 
                if R and R != "$" and len(R) > 1:
                    R = "("+R+")"
                
                adicionado = False    
                for trans in novasTransicoes:
                    if estado1 == trans[0] and estado2 == trans[2]:
                        trans[1] = R
                        adicionado = True
                if not adicionado and R:
                    novasTransicoes.append([estado1, R, estado2])
            
            
        AFD['estados'].remove(estadoEliminar)
        aExcluir = []
        for trans in novasTransicoes:
            if trans[0] == estadoEliminar or trans[2] == estadoEliminar:
                aExcluir.append(trans)
        for trans in aExcluir:
            novasTransicoes.remove(trans)
            
        AFD['funcao_transicao'] = novasTransicoes
    
    # Retorna apenas a expressão regular
    if AFD['funcao_transicao']:
        return AFD['funcao_transicao'][0][1]
    else:
        return ""

# Leitura das entradas do usuário
afn = ler_entradas_usuario()

# Chamada da função para converter o AFN em AFD
afd = AFD.converter_afn_para_afd(afn)

transicoes = converter_transicoes(afd.transicoes)

novo_afd = lerAFD(afd.estados, afd.alfabeto, transicoes, afd.estado_inicial, afd.estados_finais)

er = converterParaER(novo_afd)

print(f"expressão regular: {er}")