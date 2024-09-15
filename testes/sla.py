class AutomatoFinito:
    def __init__(self, estados, transicoes, estado_inicial, estados_finais):
        self.estados = estados
        self.transicoes = transicoes  # dict {(estado1, simbolo): [estados]}
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais

    def remover_estado(self, estado_remover):
        novos_arcos = {}
        
        # Para todos os pares de estados (j, k), lidando com os caminhos indiretos por i
        for (j, i), w_ji in self.transicoes.items():
            if i == estado_remover:
                for (i2, k), w_ik in self.transicoes.items():
                    if i2 == estado_remover:
                        # Caso 1 e Caso 2, adicionando arco direto entre j e k
                        if (j, k) not in novos_arcos:
                            novos_arcos[(j, k)] = f"{' + '.join(w_ji)}({i})*{' + '.join(w_ik)}"
                        else:
                            novos_arcos[(j, k)] += f" + {' + '.join(w_ji)}({i})*{' + '.join(w_ik)}"

        # Remove todos os arcos incidentes ao nó removido
        self.transicoes = {key: value for key, value in self.transicoes.items() if estado_remover not in key}

        # Adiciona os novos arcos gerados
        self.transicoes.update(novos_arcos)

    def obter_ER(self):
        estados_remover = [e for e in self.estados if e != self.estado_inicial and e not in self.estados_finais]

        # Remova um estado por vez, até que reste apenas o inicial e final
        for estado in estados_remover:
            self.remover_estado(estado)

        # A expressão regular final será o rótulo do arco entre o estado inicial e o estado final
        if (self.estado_inicial, self.estados_finais[0]) in self.transicoes:
            return self.transicoes[(self.estado_inicial, self.estados_finais[0])]
        else:
            return "Nenhuma transição direta encontrada."

# Exemplo de uso

# Definindo os estados, transições e estados finais
estados = [1, 2, 3]
transicoes = {
    (1, 2): "a",
    (2, 3): "b",
    (1, 3): "c"
}
estado_inicial = 1
estados_finais = [3]

af = AutomatoFinito(estados, transicoes, estado_inicial, estados_finais)

# Obtendo a ER
expressao_regular = af.obter_ER()
print(f"Expressão Regular: {expressao_regular}")