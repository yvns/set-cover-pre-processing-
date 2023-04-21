import numpy as np


# Função para converter a leitura do arquivo 'entrada.txt', de string para inteiros:
def converterStringParaInt(listaStr):
    restricoes = []
    
    # Aqui faço dois laços que eu vou pegar cada 'char' e salvar como inteiro em uma lista nova:
    for i in range(len(listaStr)):
        listaAux = []
        elemento = listaStr[i]
        for j in range(len(elemento)):
            listaAux.append(int(elemento[j]))      
        restricoes.append(listaAux)
    
    # Como o arquivo gerador termina com um '\n', eu deleto ele:
    restricoes.pop()
    return restricoes


#   Converte as restrições que antes estava em 0 e 1, para apenas os índices que incidem o 1, para
# trabalharmos na 2ª e 3ª regra:
def converterBinParaIntDosConjuntos(listaBin, tipo):
    listaConjuntos = []

    # Condição de gerar um conjunto para a 2ª regra:
    if tipo == 'linha':
        for i in range(len(listaBin)):
            listaAux = []
            for j in range(len(listaBin[0])):
                if listaBin[i][j]:
                    listaAux.append(j)
            listaConjuntos.append(listaAux)

    # Condição de gerar um conjunto para a 3ª regra:    
    elif tipo == 'coluna':
        for j in range(len(listaBin[0])):
            listaAux = []
            for i in range(len(listaBin)):
                if listaBin[i][j]:
                    listaAux.append(i)
            listaConjuntos.append(listaAux)
    
    return listaConjuntos


#   Função que faz a primeira regra pedida do problema, em que se resume em caso haja uma linha da matriz
# do problema contendo apenas 1 subconj, '[0 1 0 0]', nela, o índice, o nº do subconjunto dela é inserido
# na solução; e com isso deletamos sua linha, restrição, e as demais linhas que esse subconjunto cobre também:
def regra1(restricao, solucao, modificacoes, matrizSubconjOriginais):
    aux, coluna = 0, 0
    indicesLinhas = []
    solucaoColetada = set()

    # Caso tenha restrição seja uma lista após a remoção na regra 3, ele entrará no 'if':
    if isinstance(restricao, list):
        for h in range(len(restricao)):
                if restricao != [] and restricao[h]:
                    solucao.add(matrizSubconjOriginais[h])
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
                for k in range(len(matrizSubconjOriginais[0])):
                    if restricao[i][k]:
                        aux = matrizSubconjOriginais[0][k]
                solucaoColetada.add(coluna)
                indicesLinhas.append(i)
                solucao.add(aux)
                modificacoes = True

        #   Possuo dois tipos de soluções porque uma representa representa as colunas dessa matrix
        # que já foi modificada pelas outras deleções das regras 2 e 3, então seu subconjunto original,
        # índice, foi perdido, por isso o uso dessa outra matrix, 'listaSubconjOriginais'.
        
        indiceSolucao = list(solucaoColetada)

        for i in range(len(restricao)):
            for j in indiceSolucao:
                if restricao[i][j] and i not in indicesLinhas:
                    indicesLinhas.append(i)

        restricao = np.delete(restricao, indicesLinhas, axis=0)
        matrizSubconjOriginais = np.delete(matrizSubconjOriginais, indicesLinhas, axis=0)

    return restricao, solucao, modificacoes, matrizSubconjOriginais


#   A 2ª regra desse problema consiste em verificar restrições redundantes, ela faz a comparação utilizando
# conjuntos, 'set()', que são iterados após a 'converterBinParaIntDosConjuntos', e a condição de ser
# redudante é uma restrição conter os mesmos subconjuntos que outra(s), ou até a mais que ela, por exemplo
# {1, 2} e o deletado {1, 2, 5}:
def regra2(conjuntos, restricao, modificacoes, matrizSubconjOriginais):
    listaAux = []
    
    #   Para evitar erro de comparar o mesmo elemento, mesmo índice, e até diminuir o tamanho do laço a
    # cada iteração considerei o segundo laço ser o índice do anterior mais 1, 'm + 1', e a partir daí
    # verifico as duas desigualdades e salvo o índice dos redundantes, para a deleção a seguir:
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
    matrizSubconjOriginais = np.delete(matrizSubconjOriginais, listaAux, axis=0)

    return restricao, modificacoes, matrizSubconjOriginais
 

#    Essa regra assemelha com a segunda com a diferença que agora os índices comparados são os dos
# subconjuntos e a redundância retirada não é mais do conjunto com menor cobertura, mas o de maior,
# por exemplo {0, 2, 4, 5} e o deletado sendo {0, 2}:
def regra3(conjuntos, restricao, modificacoes, matrizSubconjOriginais):
    listaAux = []
    
    for m in range(len(conjuntos)):
        set1 = set(conjuntos[m])
        for n in range(m + 1, len(conjuntos)):
            set2 = set(conjuntos[n])
            if set1 <= set2:
                if m not in listaAux:
                    listaAux.append(m)
                    modificacoes = True
            elif set1 > set2:
                if n not in listaAux:
                    listaAux.append(n)
                    modificacoes = True
        
    # Por conta do problema envolvendo o 'axis', caso haja apenas uma linha e evitar o problema
    # de matriz com o '.shape', que pode ser '(k, )': 
    if len(restricao) == 1:
        restricao = np.delete(restricao, listaAux)
        restricao = list(restricao)
        matrizSubconjOriginais = np.delete(matrizSubconjOriginais, listaAux)
        matrizSubconjOriginais = list(matrizSubconjOriginais)
    else:
        restricao = np.delete(restricao, listaAux, axis=1)
        matrizSubconjOriginais = np.delete(matrizSubconjOriginais, listaAux, axis=1)

    return restricao, modificacoes, matrizSubconjOriginais


# Execução do algoritmo guloso p/ minimum set cover, baseado no pseudocódigo:
def algoritmoGuloso(restricoes, solucoes, matrizSubconjOriginais):
    # Executo esse algoritmo até restrições ficarem vazia, quer dizer, resolvemos o problema:
    while len(restricoes) != 0:
        linhasParaRemover, listaAux = [], []
        indiceOriginal, indiceModificado, coberturaMax, subconjEscolhido = 0, 0, 0, 0
        
        #   Transformei em uma lista para poder evitar que a matriz tenha dimensões (k, ), em que
        # k é uma constante qualquer:
        if isinstance(restricoes, list):
            for h in range(len(restricoes)):
                if restricoes != [] and restricoes[h]:
                    solucoes.add(matrizSubconjOriginais[h])
                    restricoes = []
        else:
            for j in range(len(restricoes[0])):
                cobertura = 0
                for i in range(len(restricoes)):
                    cobertura += restricoes[i][j]
                # Essa 'listaT' apenas foi um auxiliar para adicionar 3 elementos a uma lista:
                listaT = [cobertura, matrizSubconjOriginais[i][j], j]
                listaAux.append(listaT)

            #   Aqui vamos pegar o subconjunto que tem a mior cobertura entre eles e atualizamos
            # sempre que 'coberturaMax' seja maior que a cobertura analisada e daí atualizamos
            # todas as demais informações:
            for m in range(len(listaAux)):
                if coberturaMax == 0:
                    coberturaMax = listaAux[m][0]
                    indiceOriginal = listaAux[m][1]
                    indiceModificado = listaAux[m][2]
                for n in range(m + 1, len(listaAux)):
                    if coberturaMax < listaAux[n][0]:
                        coberturaMax = listaAux[n][0]
                        indiceOriginal = listaAux[n][1]
                        indiceModificado = listaAux[n][2]
            
            #   A partir do indice das restrições modificada adicionamos as linhas que tem a
            # cobertura daquele subconjunto para retirá-las do problema:
            for k in range(len(restricoes)):
                if restricoes[k][indiceModificado]:
                    linhasParaRemover.append(k)

            solucoes.add(indiceOriginal)
            subconjEscolhido = indiceModificado

            restricoes = np.delete(restricoes, linhasParaRemover, axis=0)
            matrizSubconjOriginais = np.delete(matrizSubconjOriginais, linhasParaRemover, axis=0)
            #   Sempre que executamos a remoção de um subconjunto de uma restrição que tenha apenas 
            # uma linha, ele gera uma matriz de tamanho (k, )
            if len(restricoes) == 1:
                restricoes = np.delete(restricoes, subconjEscolhido)
                restricoes = list(restricoes)
                matrizSubconjOriginais = np.delete(matrizSubconjOriginais, subconjEscolhido)
                matrizSubconjOriginais = list(matrizSubconjOriginais)
            else:
                restricoes = np.delete(restricoes, subconjEscolhido, axis=1)
                matrizSubconjOriginais = np.delete(matrizSubconjOriginais, subconjEscolhido, axis=1)
    
    return solucoes



def main():
    fileGen = open('entrada.txt', 'r')

    conjunto = fileGen.read()
    lista = conjunto.split('\n')
    restricoes = converterStringParaInt(lista)
    restricoesArray = np.array(restricoes)
    del lista, conjunto

    #   Como eu estava em dúvida e estava dando alguns problemas em trabalhar apenas com uma lista contendo os
    # subconjuntos do problema, eu decidi trabalhar com a matriz mesmo com as dimensões do problema real:
    matrizSubconjOriginais, _ = np.meshgrid(np.arange(len(restricoesArray[0])), np.arange(len(restricoesArray)))
    solucao = set()
    modificacoes = bool
    
    #   Esse enquanto funciona de quando houver modificação na matrix 'restriçõesArray', ele recebe 'True' e a
    # partir daí o algoritmo continua rodando, caso contrário, ele para:
    while modificacoes:
        modificacoes = False

        if len(restricoesArray) != 0:
            resultado_regra1 = regra1(restricoesArray, solucao, modificacoes, matrizSubconjOriginais)
            restricoesArray, solucao, modificacoes, matrizSubconjOriginais = resultado_regra1[0], resultado_regra1[1], resultado_regra1[2], resultado_regra1[3]
        # Caso haja apenas uma linha no 'restricoesArray' ele não irá rodar a 2ª regra:
        if len(restricoesArray) > 1:
            resultado_regra2 = regra2(converterBinParaIntDosConjuntos(restricoesArray, 'linha'), restricoesArray, modificacoes, matrizSubconjOriginais)
            restricoesArray, modificacoes, matrizSubconjOriginais = resultado_regra2[0], resultado_regra2[1], resultado_regra2[2]
        if len(restricoesArray) != 0:
            resultado_regra3 = regra3(converterBinParaIntDosConjuntos(restricoesArray, 'coluna'), restricoesArray, modificacoes, matrizSubconjOriginais)
            restricoesArray, modificacoes, matrizSubconjOriginais = resultado_regra3[0], resultado_regra3[1], resultado_regra3[2]

    if isinstance(restricoesArray, list):
        print('Restrições e Subconjuntos remanescentes =', len(restricoesArray))
    else:
        print('Restrições remanescentes =', len(restricoesArray), '\nSubconjuntos remanescentes =', len(restricoesArray[0]))

    # Caso já tenha achado a solução no pré-processamento ele nem entra no 'if':
    if len(restricoesArray) != 0:
        solucaoFinal = algoritmoGuloso(restricoesArray, solucao, matrizSubconjOriginais)
        print('Solução dado pelo Algoritmo guloso =', solucaoFinal, 'tamanho =', len(solucaoFinal))
    else:
        print('Solução dada pelo pré-processamento =', solucao, 'tamanho =', len(solucao))
    
    
if __name__ == '__main__':
    main()