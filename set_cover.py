# Função que converte a lista contendo as restrições como 'string' para 'int' que está contida em uma lista de listas de Inteiros:
def converterStringParaInt(listaStr):
    # Faço uma primeira iteração atribuída a cada restrição do problema:
    restricoes = []
    for i in range(len(listaStr)):
        s = []
        elemento = listaStr[i]
        # Faço essa iteração envolvendo cada valor de cada restrição gerada, como estava dando erro usando apenas a transformação para int, decidi fazer com 'float' para 'int':
        for j in range(len(elemento)):
            s.append(int(elemento[j]))      
        restricoes.append(s)
    # Como a função gerador acaba gerando uma linha em branco no final de todas as restrições, deletei ela com essa linha:
    restricoes.pop()
    return restricoes


# Converte as restrições que antes estava em 0 e 1, para apenas os valores das posições do 1, para conseguirmos trabalhar na 2ª regra:
def converterBinParaIntDosConjuntos(lista):
    l = []
    elementos = len(lista[0])
    #print(elementos)
    # Caso ele tenha apenas uma restrição em objetos, ele roda apenas uma vez e tira os valores dos conjuntos que contém em cada restrição:
    if len(lista) == 1:
        for i in range(elementos):
            if lista[0][i] == 1:
                l.append(i)
    else:
        for j in range(len(lista)):
            k = []
            for i in range(elementos):
                if lista[j][i] == 1:
                    k.append(i)
            l.append(k)
    
    return l


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
    l = []
    lista_Aux = []
    
    # Por convenção decidi criar um laço duplo para salvar os elementos dos subconjuntos das restrições redundantes do problema em uma lista 'l'
    for m in range(len(conjuntos)):
        Set1 = set(conjuntos[m])
        for n in range(m + 1, len(conjuntos)):
            Set2 = set(conjuntos[n])
            if Set1 >= Set2:
                if m not in l:
                    l.append(m)
            elif Set1 < Set2:
                # Não sei como ficaria esse 'if' caso ouvesse um caso de 3 restrições serem identicas tipo [0,1,1,0,0,0,0] aparecer 3 vezes (?)
                if n not in l:
                    l.append(n)
 
    # Agora farei um laço duplo para pegar os elementos salvos da lista 'l' e compará-los com a 'lista' de entrada que é a lista de conjuntos (Xi) em cada restrição, para deletarmos depois:
    # Por preguiça e falta de ideia, criei uma lista anteriormente 'aux1' para salvar a restrição que é repetido e possui seus idênticos no problema para fazer sua inclusão novamente nos objetos
    l.sort()
    aux = 0
    for k in l:
        del restricao[k - aux]
        aux += 1
    
    return restricao
    # for i, linha in enumerate(objetos):
    #     print(i, linha)   


# para a terceira regra agora é analisar as colunas/subconj redundantes, porém dessa vez devemos escolher o conjunto Si com a maior cobertura entre as restrições:
# vamos repetir as 3 regras até o conjunto ficar vazio = []
#def regra3():


def main():
    path = "/Users/aluno/Downloads/t/set-cover-pre-processing-/entrada.txt"

    fileGen = open(path, 'r')

    conjunto = fileGen.read()
    lista = conjunto.split('\n')
    solucao = []

    restricoes = converterStringParaInt(lista)

    resultado_Regra1 = []
    # Uma forma de evitar problema com a indexação da lista foi utilizar um auxiliador 'j' que volta a quantidade de elementos que foram retirados da lista!
    j = 0
    # Selecionar a 'solução' da primeira regra e deletar a restrição:
    for i in range(len(restricoes)):
        xx = regra1(restricoes[i - j])
        
        # Há um problema nesse código, caso exista uma restrição [1,0,0,0,0,0,0], ele não consegue adicionar o '0' na lista, pois ele diz que o '0' é nulo (?)
        if xx == 0:
            print(xx)
        resultado_Regra1.append(xx)
        if resultado_Regra1[i]:
            # Para evitar que acabe selecionando a mesma variável 'Xi' duas vezes no conjunto solução caso exista uma restrição igual:
            if resultado_Regra1[i] not in solucao:
                solucao.append(resultado_Regra1[i])
            print(solucao)
            del restricoes[i - j]
            j += 1

    # Da mesma forma que usei o 'j' para evitar o erro, estamos usando aqui o auxiliador 'k':
    k = 0
    # Aqui iremos excluir as restrições já cobertas pelo conjunto solução, pois sabemos que satisfaz a condição '>= 1' para os conjuntos em 'solucao':
    if solucao is not []:
        for i in range(len(restricoes)):
            for j in range(len(solucao)):
                    if restricoes[i - k][solucao[j]]:
                        del restricoes[i - k]
                        k += 1

    # Aqui coloquei um segundo argumento de 'restricoes' para eu conseguir deletar as restricoes que possuem conjuntos redundantes, sobrando apenas seus subconjuntos:
    r = regra2(converterBinParaIntDosConjuntos(restricoes), restricoes)

    #regra3()

    print(r)


if __name__ == '__main__':
    main()