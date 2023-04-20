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
def converterBinParaIntDosConjuntos(listaBin, tipo):
    listaConjuntos = []

    if tipo == 'linha':
        for i in range(len(listaBin)):
            listaAux = []
            for j in range(len(listaBin[0])):
                if listaBin[i][j]:
                    listaAux.append(j)
            listaConjuntos.append(listaAux)
    
    elif tipo == 'coluna':
        for j in range(len(listaBin[0])):
            listaAux = []
            for i in range(len(listaBin)):
                if listaBin[i][j]:
                    listaAux.append(i)
            listaConjuntos.append(listaAux)
    
    return listaConjuntos


# Função que faz a primeira regra pedida do problema:
def regra1(restricao, solucao, modificacoes, listaSubconjOriginais):
    aux, coluna = 0, 0
    indicesLinhas = []
    solucaoColetada = set()

    # Corrigir depois caso tenha apenas 1 elemento, tipo: [[1]]
    if restricao.shape == (1,):
        solucao.add(int(listaSubconjOriginais))
        restricao = []
        modificacoes = True
        
    else:
        for i in range(len(restricao)):
            cobertura = 0
            for j in range(len(restricao[0])):
                cobertura += restricao[i][j]
                if restricao[i][j]:
                    coluna = j
            if cobertura == 1:
                for k in range(len(listaSubconjOriginais[0])):
                    if restricao[i][k]:
                        aux = listaSubconjOriginais[0][k]
                solucaoColetada.add(coluna)
                indicesLinhas.append(i)
                solucao.add(aux)
                modificacoes = True


        indiceSolucao = list(solucaoColetada)


        for i in range(len(restricao)):
            for j in indiceSolucao:
                if restricao[i][j] and i not in indicesLinhas:
                    indicesLinhas.append(i)

        restricao = np.delete(restricao, indicesLinhas, axis=0)
        listaSubconjOriginais = np.delete(listaSubconjOriginais, indicesLinhas, axis=0)

    return restricao, solucao, modificacoes, listaSubconjOriginais
        

def regra2(conjuntos, restricao, modificacoes, listaSubconjOriginais):
    listaAux = []
    
    # Por convenção decidi criar um laço duplo para salvar os elementos dos subconjuntos das restrições redundantes do problema em uma lista 'l'
    for m in range(len(conjuntos)):
        set1 = set(conjuntos[m])
        for n in range(m + 1, len(conjuntos)):
            set2 = set(conjuntos[n])
            if set1 >= set2:
                if m not in listaAux:
                    listaAux.append(m)
                    modificacoes = True
            elif set1 < set2:
                if n not in listaAux:
                    listaAux.append(n)
                    modificacoes = True
        
    restricao = np.delete(restricao, listaAux, axis=0)
    listaSubconjOriginais = np.delete(listaSubconjOriginais, listaAux, axis=0)

    return restricao, modificacoes, listaSubconjOriginais
 

def regra3(conjuntos, restricao, modificacoes, listaSubconjOriginais):
    listaAux = []
    
    # Por convenção decidi criar um laço duplo para salvar os elementos dos subconjuntos das restrições redundantes do problema em uma lista 'l'
    for m in range(len(conjuntos)):
        set1 = set(conjuntos[m])
        for n in range(m + 1, len(conjuntos)):
            set2 = set(conjuntos[n])
            if set1 <= set2:
                if m not in listaAux and set1 is not {}:
                    listaAux.append(m)
                    modificacoes = True
            elif set1 > set2:
                if n not in listaAux and set2 is not None:
                    listaAux.append(n)
                    modificacoes = True
        
    if len(restricao) == 1:
        restricao = np.delete(restricao, listaAux)
        listaSubconjOriginais = np.delete(listaSubconjOriginais, listaAux)

    else:
        restricao = np.delete(restricao, listaAux, axis=1)
        listaSubconjOriginais = np.delete(listaSubconjOriginais, listaAux, axis=1)

    return restricao, modificacoes, listaSubconjOriginais
        


def main():
    fileGen = open('entrada.txt', 'r')

    conjunto = fileGen.read()
    lista = conjunto.split('\n')
    restricoes = converterStringParaInt(lista)
    restricoesArray = np.array(restricoes)
    del lista, conjunto

    #listaSubconjOriginais, _ = np.meshgrid(np.arange(len(restricoesArray[0])), np.arange(len(restricoesArray)))
    listaSubconjOriginais, _ = np.meshgrid(np.arange(len(restricoesArray[0])), np.arange(len(restricoesArray)))
    solucao = set()
    modificacoes = bool
    
    while modificacoes:
        modificacoes = False
        resultado_regra1 = []
        if len(restricoesArray) != 0:
            resultado_regra1 = regra1(restricoesArray, solucao, modificacoes, listaSubconjOriginais)
            restricoesArray, solucao, modificacoes, listaSubconjOriginais = resultado_regra1[0], resultado_regra1[1], resultado_regra1[2], resultado_regra1[3]

        
        # Aqui coloquei um segundo argumento de 'restricoes' para eu conseguir deletar as restricoes que possuem conjuntos redundantes, sobrando apenas seus subconjuntos:
        if len(restricoesArray) != 1 and len(restricoesArray) != 0:
            resultado_regra2 = regra2(converterBinParaIntDosConjuntos(restricoesArray, 'linha'), restricoesArray, modificacoes, listaSubconjOriginais)
            restricoesArray, modificacoes, listaSubconjOriginais = resultado_regra2[0], resultado_regra2[1], resultado_regra2[2]
        
        if len(restricoesArray) != 0:
            resultado_regra3 = regra3(converterBinParaIntDosConjuntos(restricoesArray, 'coluna'), restricoesArray, modificacoes, listaSubconjOriginais)
            restricoesArray, modificacoes, listaSubconjOriginais = resultado_regra3[0], resultado_regra3[1], resultado_regra3[2]


    print(solucao, '\n', len(solucao), '\n', len(restricoesArray[0]), len(restricoesArray))


if __name__ == '__main__':
    main()