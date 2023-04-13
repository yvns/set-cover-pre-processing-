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
    #print(elementos)
    # Caso ele tenha apenas uma restrição em objetos, ele roda apenas uma vez e tira os valores dos conjuntos que contém em cada restrição:
    if len(listaBin) == 1:
        for i in range(tamanhoDasRestricoes):
            if listaBin[0][i] == 1:
                listaConjuntos.append(i)
    else:
        for j in range(len(listaBin)):
            listaAux = []
            for i in range(tamanhoDasRestricoes):
                if listaBin[j][i] == 1:
                    listaAux.append(i)
            listaConjuntos.append(listaAux)
    
    return listaConjuntos


# Função que faz a primeira regra pedida do problema:
def regra1(restricao):
    cobertura = 0
    indice = 0

    for j in range(len(restricao)):
        cobertura += restricao[j]
        if restricao[j]:
            indice = j
    
    # Se tiver algum 'Xi' que tenha apenas ele como cobertura daquela restrição, ele deve ser igual a 1 (Xi + n*0 >= 1):
    if cobertura == 1:
        return indice
    else:
        return None


def regra2(conjuntos, restricao):
    #print(lista)
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
    listaAux.sort()
    aux = 0
    for k in listaAux:
        del restricao[k - aux]
        aux += 1
    
    return restricao
    # for i, linha in enumerate(objetos):
    #     print(i, linha)   


# para a terceira regra agora é analisar as colunas/subconj redundantes, porém dessa vez devemos escolher o conjunto Si com a maior cobertura entre as restrições:
# vamos repetir as 3 regras até o conjunto ficar vazio = []
#def regra3():


def main():
    caminho = "/Users/aluno/Downloads/t/set-cover-pre-processing-/entrada.txt"

    fileGen = open(caminho, 'r')

    conjunto = fileGen.read()
    lista = conjunto.split('\n')
    solucao = []

    restricoes = converterStringParaInt(lista)

    resultado_Regra1 = []
    # Uma forma de evitar problema com a indexação da lista foi utilizar um auxiliador 'j' que volta a quantidade de elementos que foram retirados da lista!
    auxRegra1 = 0
    # Selecionar a 'solução' da primeira regra e deletar a restrição:
    for i in range(len(restricoes)):
        xx = regra1(restricoes[i - auxRegra1])

        # Há um problema nesse código, caso exista uma restrição [1,0,0,0,0,0,0], ele não consegue adicionar o '0' na lista, pois ele diz que o '0' é nulo (?)
        if xx != None:
            print(xx)
            resultado_Regra1.append(xx)

            # Para evitar que acabe selecionando a mesma variável 'Xi' duas vezes no conjunto solução caso exista uma restrição igual:
            if resultado_Regra1[-1] not in solucao:
                solucao.append(resultado_Regra1[-1])
            del restricoes[i - auxRegra1]
            auxRegra1 += 1
    print(solucao)

    # Da mesma forma que usei o 'j' para evitar o erro, estamos usando aqui o auxiliador 'k':
    aux = 0
    # Aqui iremos excluir as restrições já cobertas pelo conjunto solução, pois sabemos que satisfaz a condição '>= 1' para os conjuntos em 'solucao':
    if solucao is not []:
        for i in range(len(restricoes)):
            for auxRegra1 in range(len(solucao)):
                    if restricoes[i - aux][solucao[auxRegra1]]:
                        del restricoes[i - aux]
                        aux += 1

    # Aqui coloquei um segundo argumento de 'restricoes' para eu conseguir deletar as restricoes que possuem conjuntos redundantes, sobrando apenas seus subconjuntos:
    if len(restricoes) != 1:
        restricoes_nao_redundantes = regra2(converterBinParaIntDosConjuntos(restricoes), restricoes)
        print(restricoes_nao_redundantes)

    #resultados = regra3(restricoes_nao_redundantes)

    


if __name__ == '__main__':
    main()