import copy

class NFA:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def epsilon_closure(self, states):
        stack = list(states)
        closure = set(states)

        while stack:
            state = stack.pop()

            if (state, '') in self.transitions:
                destinations = self.transitions[(state, '')]

                for destination in destinations:
                    if destination not in closure:
                        closure.add(destination)
                        stack.append(destination)

        return sorted(closure)
    
    # Check if the automaton is already a DFA
    def is_dfa(self):
        # Checks if the NFA is a DFA
        for (state, symbol), destinations in self.transitions.items():
            if len(destinations) > 1:
                return False
        return True
    
class DFA:
    def __init__(self, states=None, alphabet=None, transitions=None, initial_state=None, final_states=None):
        self.states = states if states is not None else []
        self.alphabet = alphabet if alphabet is not None else []
        self.transitions = transitions if transitions is not None else {}
        self.initial_state = initial_state
        self.final_states = final_states if final_states is not None else []

    @classmethod
    def convert_nfa_to_dfa(cls, nfa):
        if nfa.is_dfa():
            return DFA(
                states=nfa.states,
                alphabet=nfa.alphabet,
                transitions=nfa.transitions,
                initial_state=nfa.initial_state,
                final_states=nfa.final_states
            )
               
        dfa = cls()
        dfa.alphabet = [symbol for symbol in nfa.alphabet if symbol != '']
        dfa_initial_state = nfa.epsilon_closure([nfa.initial_state])

        stack = [dfa_initial_state]
        visited = set()

        while stack:
            state_set = stack.pop()
            state_set_str = ''.join(state_set) if state_set else ''
            if state_set_str in visited:
                continue
            visited.add(state_set_str)
            dfa.states.append(state_set_str)

            if any(state in nfa.final_states for state in state_set):
                dfa.final_states.append(state_set_str)

            for symbol in dfa.alphabet:
                destinations = []

                for state in state_set:
                    if (state, symbol) in nfa.transitions:
                        destinations.extend(nfa.transitions[(state, symbol)])

                epsilon_destinations = nfa.epsilon_closure(destinations)
                destination_str = ''.join(epsilon_destinations) if epsilon_destinations else ''

                dfa.transitions[(state_set_str, symbol)] = destination_str

                if destination_str and destination_str not in visited:
                    stack.append(epsilon_destinations)

        dfa.initial_state = ''.join(dfa_initial_state) if dfa_initial_state else ''
        return dfa

def read_user_input():
    states = input("Enter the states (separated by commas): ").split(",")
    alphabet = input("Enter the alphabet (separated by commas): ").split(",")
    alphabet.append('')  # Add the empty symbol to the alphabet
    transitions = {}

    print("Enter the transitions (press Enter for no transition):")
    for state in states:
        for symbol in alphabet:
            entry = input(f"D({state},{'ε' if symbol == '' else symbol}): ").strip()
            if entry == '':
                transitions[(state, symbol)] = []
            else:
                transitions[(state, symbol)] = entry.split(",")

    initial_state = input("Enter the initial state: ").strip()
    acceptance_states = input("Enter the acceptance state(s) (separated by commas): ").split(",")

    return NFA(states, alphabet, transitions, initial_state, acceptance_states)

def convert_transitions(transitions):
    converted_transitions = []
    
    for (state, symbol), destination in transitions.items():
        if destination:  # Check if the destination is not empty
            if isinstance(destination, list):  # If destinations are a list
                for d in destination:
                    converted_transitions.append([state, symbol, d])
            else:  # If destination is a single string
                converted_transitions.append([state, symbol, destination])
    
    return converted_transitions

def read_DFA(states, alphabet, transitions, initial_state, final_states):
    # Create the DFA
    DFA = {
        'states': states,
        'alphabet': alphabet,
        'transition_function': transitions,
        'initial_states': [initial_state],
        'final_states': final_states
    }
    
    return DFA

def convert_to_ER(DFA):
    i = "q0"
    c = 0
    while i in DFA['states']:
        c += 1
        i = "q"+str(c)

    DFA['states'].append(i)
    DFA['transition_function'].append([i, "$", DFA['initial_states'][0]])
    DFA['initial_states'] = [i]

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
            print(f"Invalid transition: {trans}. Expected format [state, symbol, state].")
            continue
        if trans[0] not in transitions.keys():
            transitions[trans[0]] = {}
        transitions[trans[0]][trans[1]] = trans[2]
    
    for state in transitions.keys():
        to_modify = []
        for alphabet1 in transitions[state].keys():
            for alphabet2 in transitions[state].keys():
                if alphabet1 != alphabet2 and transitions[state][alphabet1] == transitions[state][alphabet2]:
                    destination = transitions[state][alphabet1]
                    to_modify.append([alphabet1, destination, 0])
                    to_modify.append([alphabet2, destination, 0])
    
        to_modify = [list(x) for x in set(tuple(x) for x in to_modify)]
    
        flag = True
        while flag:
            flag = False
            for exp1 in to_modify:
                for exp2 in to_modify:
                    if exp1[0] != exp2[0] and exp1[1] == exp2[1]:
                        if exp1[2] == 0:
                            exp1[0] += "+"+exp2[0]
                            exp1[2] = 1
                            exp2[2] = 1
                            to_modify.remove(exp2)
                            flag = True
                        elif exp2[2] == 0:
                            exp1[0] += "+"+exp2[0]
                            exp1[2] = 1
                            exp2[2] = 1
                            to_modify.remove(exp2)
                            flag = True
        to_remove = []
        for key in transitions[state].keys():
            for trans in to_modify:
                if key in trans[0]:
                    to_remove.append(key)
        for key in to_remove:
            del transitions[state][key]
              
        for trans in to_modify:
            transitions[state][trans[0]] = trans[1]
        
    DFA['transition_function'] = []
    for state in transitions.keys():
        for alphabet in transitions[state].keys():
            DFA['transition_function'].append([state, alphabet, transitions[state][alphabet]])
    
    while len(DFA['states']) > 2:
        new_transitions = copy.deepcopy(DFA['transition_function'])
        
        state_to_remove = ""
        for state in DFA['states']:
            if state not in DFA['initial_states'] and state not in DFA['final_states']:
                state_to_remove = state
                break
        for state1 in DFA['states']:
            for state2 in DFA['states']:
                if state1 in DFA['final_states']:
                    continue
                if state2 in DFA['initial_states']:
                    continue
                R1 = ""
                R2 = ""
                R3 = ""
                R4 = ""
                for trans in DFA['transition_function']:
                    if trans[0] == state1 and trans[2] == state_to_remove:
                        R1 = trans[1]
                    if trans[0] == state_to_remove and trans[2] == state_to_remove:
                        R2 = trans[1]
                    if trans[0] == state_to_remove and trans[2] == state2:
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
                for trans in new_transitions:
                    if state1 == trans[0] and state2 == trans[2]:
                        trans[1] = R
                        added = True
                if not added:
                    new_transitions.append([state1, R, state2])
                
        DFA['transition_function'] = new_transitions
        DFA['states'] = [state for state in DFA['states'] if state != state_to_remove]
        DFA['final_states'] = [state for state in DFA['final_states'] if state != state_to_remove]
    
    return DFA


# Convert NFA to DFA
nfa = read_user_input()
dfa = DFA.convert_nfa_to_dfa(nfa)

# Generate Expression Regular from DFA
dfa_ER = convert_to_ER(dfa)
print("Generated ER from DFA:", dfa_ER)