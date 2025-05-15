from collections import Counter


def compara_prescricao_estoque(prescricao, estoque):
    '''Função que verifica se a dose do medicamento prescrita está disponível no estoque'''
    # conta a quantidade de cada medicamento na prescrição
    contagem_prescricao = Counter(prescricao)

    # conta a quantidade de cada medicamento no estoque
    contagem_estoque = Counter(estoque)

    # verifica se a frequência do medicamento prescrita é maior do que a presente no estoque
    for med in contagem_prescricao:
        if contagem_prescricao[med] > contagem_estoque[med]:
            return False
        
    return True

# Entrada dos dados de prescrição e estoque
entrada = input("Digite prescricao,estoque: ").lower().split(",")
prescricao = entrada[0]
estoque = entrada[1]

# Exibe o resultado booleano retornado pela função
resultado = compara_prescricao_estoque(prescricao, estoque)
print(resultado)
