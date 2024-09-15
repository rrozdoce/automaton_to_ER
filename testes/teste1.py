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

# Dados de entrada para o primeiro exemplo
estados1 = ['q0']
alfabeto1 = ['u']
transicoes1 = {
    ('q0', 'u'): ['q0'],
    ('q0', ''): []
}
estado_inicial1 = 'q0'
estados_finais1 = ['q0']

# Dados de entrada para o segundo exemplo
estados2 = ['q0', 'q0q1']
alfabeto2 = ['u', 'v']
transicoes2 = {
    ('q0', 'u'): 'q0q1',
    ('q0', 'v'): 'q0',
    ('q0q1', 'u'): 'q0q1',
    ('q0q1', 'v'): 'q0'
}
estado_inicial2 = 'q0'
estados_finais2 = ['q0q1']

# Conversão para o primeiro exemplo
transicoes_convertidas1 = converter_transicoes(transicoes1)
print("Para o primeiro exemplo:")
print("estados:", estados1)
print("alfabeto:", alfabeto1)
print("transicoes:", transicoes_convertidas1)
print("estado inicial:", estado_inicial1)
print("estados finais:", estados_finais1)

# Conversão para o segundo exemplo
transicoes_convertidas2 = converter_transicoes(transicoes2)
print("\nPara o segundo exemplo:")
print("estados:", estados2)
print("alfabeto:", alfabeto2)
print("transicoes:", transicoes_convertidas2)
print("estado inicial:", estado_inicial2)
print("estados finais:", estados_finais2)
