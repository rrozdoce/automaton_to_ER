import json
import sys
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

def readDFA(states, alphabet, transitions, start_state, final_states):
    
    
    # Cria o DFA
    DFA = {
        'states': states,
        'alphabet': alphabet,
        'transition_function': transitions,
        'start_states': [start_state],
        'final_states': final_states
    }
    
    return DFA

def convertToRegex(DFA):
    i = "q0"
    c = 0
    while i in DFA['states']:
        c += 1
        i = "q"+str(c)

    DFA['states'].append(i)
    DFA['transition_function'].append([i, "$", DFA['start_states'][0]])
    DFA['start_states'] = [i]

    i = "q0"
    c = 0
    while i in DFA['states']:
        c += 1
        i = "q"+str(c)

    DFA['states'].append(i)
    for state in DFA['final_states']:
        DFA['transition_function'].append([state, "$", i])
    DFA['final_states'] = [i]
    
    transitions = {}
    for trans in DFA['transition_function']:
        if len(trans) != 3:
            print(f"Transição inválida: {trans}. Esperado formato [estado, simbolo, estado].")
            continue
        if trans[0] not in transitions.keys():
            transitions[trans[0]] = {}
        transitions[trans[0]][trans[1]] = trans[2]
    
    for state in transitions.keys():
        toChange = []
        for alph1 in transitions[state].keys():
            for alph2 in transitions[state].keys():
                if alph1 != alph2 and transitions[state][alph1] == transitions[state][alph2]:
                    dest = transitions[state][alph1]
                    toChange.append([alph1, dest, 0])
                    toChange.append([alph2, dest, 0])
    
        toChange = [list(x) for x in set(tuple(x) for x in toChange)]
    
        flag = True
        while flag:
            flag = False
            for exp1 in toChange:
                for exp2 in toChange:
                    if exp1[0] != exp2[0] and exp1[1] == exp2[1]:
                        if exp1[2] == 0:
                            exp1[0] += "+"+exp2[0]
                            exp1[2] = 1
                            exp2[2] = 1
                            toChange.remove(exp2)
                            flag = True
                        elif exp2[2] == 0:
                            exp1[0] += "+"+exp2[0]
                            exp1[2] = 1
                            exp2[2] = 1
                            toChange.remove(exp2)
                            flag = True
        toDel = []
        for key in transitions[state].keys():
            for trans in toChange:
                if key in trans[0]:
                    toDel.append(key)
        for key in toDel:
            del transitions[state][key]
              
        for trans in toChange:
            transitions[state][trans[0]] = trans[1]
        
    DFA['transition_function'] = []
    for state in transitions.keys():
        for alph in transitions[state].keys():
            DFA['transition_function'].append([state, alph, transitions[state][alph]])
    
    while len(DFA['states']) > 2:
        newTrans = copy.deepcopy(DFA['transition_function'])
        
        rip_state = ""
        for state in DFA['states']:
            if state not in DFA['start_states'] and state not in DFA['final_states']:
                rip_state = state
                break
        for state1 in DFA['states']:
            for state2 in DFA['states']:
                if state1 in DFA['final_states']:
                    continue
                if state2 in DFA['start_states']:
                    continue
                R1 = ""
                R2 = ""
                R3 = ""
                R4 = ""
                for trans in DFA['transition_function']:
                    if trans[0] == state1 and trans[2] == rip_state:
                        R1 = trans[1]
                    if trans[0] == rip_state and trans[2] == rip_state:
                        R2 = trans[1]
                    if trans[0] == rip_state and trans[2] == state2:
                        R3 = trans[1]
                    if trans[0] == state1 and trans[2] == state2:
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
                
                added = False    
                for trans in newTrans:
                    if state1 == trans[0] and state2 == trans[2]:
                        trans[1] = R
                        added = True
                if not added and R:
                    newTrans.append([state1, R, state2])
            
            
        DFA['states'].remove(rip_state)
        toDel = []
        for trans in newTrans:
            if trans[0] == rip_state or trans[2] == rip_state:
                toDel.append(trans)
        for trans in toDel:
            newTrans.remove(trans)
            
        DFA['transition_function'] = newTrans
    
    # Retorna apenas a expressão regular
    if DFA['transition_function']:
        return DFA['transition_function'][0][1]
    else:
        return ""

# Leitura das entradas do usuário
afn = ler_entradas_usuario()

# Chamada da função para converter o AFN em AFD
afd = AFD.converter_afn_para_afd(afn)

#readDFA(states, alphabet, transitions, start_state, final_states)

transicoes = converter_transicoes(afd.transicoes)

novo_afd = readDFA(afd.estados, afd.alfabeto, transicoes, afd.estado_inicial, afd.estados_finais)

er = convertToRegex(novo_afd)

print(f"expressão regular: {er}")