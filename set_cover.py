import numpy as np
# Função que converte a lista contendo as restrições como 'string' para 'int' que está contida em uma lista de listas de Inteiros:
def converterStringParaInt(listaStr):
    # Faço uma primeira iteração atribuída a cada restrição do problema:
    restricoes = []
    
    for i in range(len(listaStr)):
        listaAux = []
        elemento = listaStr[i]
        # Faço essa iteração envolvendo cada valor de cada restrição gerada, como estava dando erro usando apenas a transformação para int, decidi fazer com 'float' para 'int':
        for j in range(len(elemento)):
            listaAux.append(int(elemento[j]))      
        restricoes.append(listaAux)
    # Como a função gerador acaba gerando uma linha em branco no final de todas as restrições, deletei ela com essa linha:
    restricoes.pop()
    return restricoes


# Converte as restrições que antes estava em 0 e 1, para apenas os valores das posições do 1, para conseguirmos trabalhar na 2ª regra:
def converterBinParaIntDosConjuntos(listaBin):
    listaConjuntos = []
    tamanhoDasRestricoes = len(listaBin[0])

    # Caso ele tenha apenas uma restrição em objetos, ele roda apenas uma vez e tira os valores dos conjuntos que contém em cada restrição:
    if len(listaBin) == 1:
        for j in range(tamanhoDasRestricoes):
            if listaBin[0][j] == 1:
                listaConjuntos.append(j)
    else:
        for i in range(len(listaBin)):
            listaAux = []
            for j in range(tamanhoDasRestricoes):
                if listaBin[j][i] == 1:
                    listaAux.append(i)
            listaConjuntos.append(listaAux)
    
    listaConjuntos = np.array(listaConjuntos)
    return listaConjuntos


# Função que faz a primeira regra pedida do problema:
def regra1(restricao, solucao, modificacoes, listaSubconjOriginais):
    aux = 0
    indicesLinhas = []

    for i in range(len(restricao)):
        cobertura = 0
        for j in range(len(restricao[0])):
            cobertura += restricao[i][j]
            if restricao[i][j]:
                aux = j
        if cobertura == 1:
            indicesLinhas.append(i)
            solucao.add(aux)
            modificacoes = True

    indiceSolucao = list(solucao)

    for i in range(len(restricao)):
        for j in indiceSolucao:
            if restricao[i][j] and i not in indicesLinhas:
                indicesLinhas.append(i)
    
    restricaoNova = np.delete(restricao, indicesLinhas, axis=0)
    listaSubconjOriginaisNovo = np.delete(listaSubconjOriginais, indicesLinhas, axis=0)

    return restricaoNova, solucao, modificacoes, listaSubconjOriginaisNovo
        


def regra2(conjuntos, restricao, modificacoes):
    listaAux = []
    
    # Por convenção decidi criar um laço duplo para salvar os elementos dos subconjuntos das restrições redundantes do problema em uma lista 'l'
    for m in range(len(conjuntos)):
        set1 = set(conjuntos[m])
        for n in range(m + 1, len(conjuntos)):
            set2 = set(conjuntos[n])
            if set1 >= set2:
                if m not in listaAux:
                    listaAux.append(m)
            elif set1 < set2:
                # Não sei como ficaria esse 'if' caso ouvesse um caso de 3 restrições serem identicas tipo [0,1,1,0,0,0,0] aparecer 3 vezes (?)
                if n not in listaAux:
                    listaAux.append(n)
    
 
    # Agora farei um laço duplo para pegar os elementos salvos da lista 'l' e compará-los com a 'lista' de entrada que é a lista de conjuntos (Xi) em cada restrição, para deletarmos depois:
    # Por preguiça e falta de ideia, criei uma lista anteriormente 'aux1' para salvar a restrição que é repetido e possui seus idênticos no problema para fazer sua inclusão novamente nos objetos
    # listaAux.sort()
    # aux = 0
    # for k in listaAux:
    #     del restricao[k - aux]
    #     aux += 1
    #     modificacoes = True
    restricaoModificada = np.delete(restricao, listaAux, axis=0)

    return restricaoModificada, modificacoes
 


# def regra3(restricoes, solucao, modificado, listaSubconjRemovidos):
#     maiorPrioridade, indiceConjunto, prioridade = 0, 0, 0

#     for j in range(len(restricoes)):
#         if len(restricoes) == 1:
#             if restricoes[0][j]:
#                 indiceConjunto = j
#                 solucao.add(j)
#                 return restricoes
        
#         else:
#             for i in range(len(restricoes)):
#                 if restricoes[i][j]:
#                     prioridade += restricoes[i][j]
            
#             if prioridade > maiorPrioridade:
#                 maiorPrioridade = prioridade
#                 indiceConjunto = j
#             prioridade = 0
        
#     return indiceConjunto
        


def main():
    fileGen = open('entrada.txt', 'r')

    conjunto = fileGen.read()
    lista = conjunto.split('\n')
    restricoes = converterStringParaInt(lista)
    restricoesArray = np.array(restricoes)

    listaSubconjOriginais = restricoesArray
    solucao = set()
    modificacoes = True

    linhas = len(restricoes)
    
    while modificacoes:
        modificacoes = False
        resultado_regra1 = []
            
        resultado_regra1 = regra1(restricoes, solucao, modificacoes, listaSubconjOriginais)
        restricoes, solucao, modificacoes, listaSubconjOriginais = resultado_regra1[0], resultado_regra1[1], resultado_regra1[2], resultado_regra1[3]

        # Aqui coloquei um segundo argumento de 'restricoes' para eu conseguir deletar as restricoes que possuem conjuntos redundantes, sobrando apenas seus subconjuntos:
        if len(restricoes) != 1:
            resultado_regra2 = regra2(converterBinParaIntDosConjuntos(restricoes), restricoes, modificacoes)
            restricoes, modificacoes = resultado_regra2[0], resultado_regra2[1]
            #print(restricoes, modificacoes)
        
        modificacoes = False
        #resultado_regra3 = regra3(restricoes, modificado, colunas)


    #print(solucao, '\n', len(solucao))


if __name__ == '__main__':
    main()