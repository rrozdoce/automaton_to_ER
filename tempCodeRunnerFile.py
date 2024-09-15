import copy

def convertToRegex(states, alphabet, transitions, start_state, final_states):
    # Remove símbolos vazios do alfabeto
    alphabet = [sym for sym in alphabet if sym]

    # Remove transições com símbolos vazios e transições que levam a estados vazios
    filtered_transitions = {}
    for (state_from, symbol), state_to_list in transitions.items():
        if symbol and state_to_list:  # Ignora símbolos vazios e transições para estados vazios
            filtered_transitions[(state_from, symbol)] = [state for state in state_to_list if state]

    # Inicialize o DFA com os estados e alfabeto fornecidos
    DFA = {
        'states': states[:],  # Lista de estados
        'alphabet': alphabet[:],  # Lista de símbolos do alfabeto
        'transition_function': [],  # Lista de transições
        'start_states': [start_state],  # Estado inicial
        'final_states': final_states[:]  # Lista de estados finais
    }

    # Adiciona transições ao DFA, ignorando transições vazias
    for (state_from, symbol), state_to_list in filtered_transitions.items():
        for state_to in state_to_list:
            DFA['transition_function'].append([state_from, symbol, state_to])

    # Adiciona um novo estado inicial
    i = "q_new_start"
    DFA['states'].append(i)
    DFA['transition_function'].append([i, "", DFA['start_states'][0]])
    DFA['start_states'] = [i]

    # Adiciona um novo estado final
    i = "q_new_final"
    DFA['states'].append(i)
    for state in DFA['final_states']:
        DFA['transition_function'].append([state, "", i])
    DFA['final_states'] = [i]

    # Construção do dicionário de transições
    transitions_dict = {}
    for trans in DFA['transition_function']:
        if trans[0] not in transitions_dict:
            transitions_dict[trans[0]] = {}
        if trans[1] not in transitions_dict[trans[0]]:
            transitions_dict[trans[0]][trans[1]] = []
        transitions_dict[trans[0]][trans[1]].append(trans[2])

    # Combine transições
    for state in transitions_dict.keys():
        toChange = []
        for alph1 in transitions_dict[state].keys():
            for alph2 in transitions_dict[state].keys():
                if alph1 != alph2 and transitions_dict[state][alph1] == transitions_dict[state][alph2]:
                    dest = transitions_dict[state][alph1]
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
                            exp1[0] += "+" + exp2[0]
                            exp1[2] = 1
                            exp2[2] = 1
                            toChange.remove(exp2)
                            flag = True
                        elif exp2[2] == 0:
                            exp1[0] += "+" + exp2[0]
                            exp1[2] = 1
                            exp2[2] = 1
                            toChange.remove(exp2)
                            flag = True

        toDel = []
        for key in transitions_dict[state].keys():
            for trans in toChange:
                if key in trans[0]:
                    toDel.append(key)
        for key in toDel:
            del transitions_dict[state][key]

        for trans in toChange:
            transitions_dict[state][trans[0]] = trans[1]

    DFA['transition_function'] = []
    for state in transitions_dict.keys():
        for alph in transitions_dict[state].keys():
            for dest in transitions_dict[state][alph]:
                DFA['transition_function'].append([state, alph, dest])

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
                    if R1 and R1 != "":
                        R += R1
                    if R2 and R2 != "":
                        R += R2 + "*"
                    if R3 and R3 != "":
                        R += R3

                    if R4:
                        R += "+" + R4
                else:
                    R = R4
                if R and R != "" and len(R) > 1:
                    R = "(" + R + ")"

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

    # Extrair a expressão regular final
    regEx = {}
    regEx['regex'] = DFA['transition_function'][0][1]

    return regEx

# Teste da função
states = ['q0', 'q1']
alphabet = ['u', '', 'v', 'w']  # Incluindo um símbolo vazio para testar a remoção
transitions = {
    ('q0', 'u'): ['q0'],
    ('q0', ''): [],  # Transição com símbolo vazio e sem destino
    ('q0', 'v'): ['q1'],
    ('q1', 'w'): ['q1']
}
start_state = 'q0'
final_states = ['q1']

regex = convertToRegex(states, alphabet, transitions, start_state, final_states)
print("Expressão regular resultante:")
print(regex)