path = "/Users/yvens/Documents/Faculdade/PI/entrada.txt"


fileGen = open(path, 'r')

conjunto = fileGen.read()
lista = conjunto.split('\n')
índice = 0
objetos = []
solucao = []


# Função que converte a lista contendo as restrições como 'string' para 'int' que está contida em uma lista de listas de Inteiros:
def conversor_Listas(lista):
    # Faço uma primeira iteração atribuída a cada restrição do problema:
    for i in range(len(lista)):
        s = []
        elemento = lista[i]
        # Faço essa iteração envolvendo cada valor de cada restrição gerada, como estava dando erro usando apenas a transformação para int, decidi fazer com 'float' para 'int':
        for j in range(len(elemento)):
            s.append(int(float(elemento[j])))        
        objetos.append(s)
        
    # Como a função gerador acaba gerando uma linha em branco no final de todas as restrições, deletei ela com essa linha:
    objetos.pop()


# Converte as restrições que antes estava em 0 e 1, para apenas os valores das posições do 1, para conseguirmos trabalhar na 2ª regra:
def conversor_Indices(lista):
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
def regra1(lista):
    cobertura = 0
    indice = 0

    for j in range(len(lista)):
        cobertura += lista[j]
        if lista[j]:
            indice = j
    
    # Se tiver algum 'Xi' que tenha apenas ele como cobertura daquela restrição, ele deve ser igual a 1 (Xi + n*0 >= 1):
    if cobertura == 1:
        return indice
    else:
        return 0


def regra2(lista):
    l = []
    lista_Aux = []
    
    # Por convenção decidi criar um laço duplo para salvar os elementos dos subconjuntos das restrições redundantes do problema em uma lista 'l'
    for m in range(len(objetos)):
        Set1 = set(lista[m])
        for n in range(len(objetos)):
            Set2 = set(lista[n])
            if Set1 > Set2:
                if lista[m] not in l:
                    l.append(lista[m])
            elif Set1 == Set2 and m != n:
                # Não sei como ficaria esse 'if' caso ouvesse um caso de 3 restrições serem identicas tipo [0,1,1,0,0,0,0] aparecer 3 vezes (?)
                if lista[m] not in l:
                    l.append(lista[m])
                    lista_Aux.append(objetos[m])
    
    # Agora farei um laço duplo para pegar os elementos salvos da lista 'l' e compará-los com a 'lista' de entrada que é a lista de conjuntos (Xi) em cada restrição, para deletarmos depois:
    # Por preguiça e falta de ideia, criei uma lista anteriormente 'aux1' para salvar a restrição que é repetido e possui seus idênticos no problema para fazer sua inclusão novamente nos objetos
    for k in range(len(l)):
        aux1 = 0
        for j in range(len(lista)):
            if l[k] == lista[j - aux1] and k:
                del objetos[j - aux1]
                del lista[j - aux1]
                if not aux1:
                    aux1 += 1

    for i in range(len(lista_Aux)):
        objetos.append(lista_Aux[i])



# para a terceira regra agora é analisar as colunas/subconj redundantes, porém dessa vez devemos escolher o conjunto Si com a maior cobertura entre as restrições:
# vamos repetir as 3 regras até o conjunto ficar vazio = []
#def regra3():


conversor_Listas(lista)

resultado_Regra1 = []
restricoesRedundantes = []
# Uma forma de evitar problema com a indexação da lista foi utilizar um auxiliador 'j' que volta a quantidade de elementos que foram retirados da lista!
j = 0
# Selecionar a 'solução' da primeira regra e deletar a restrição:
for i in range(len(objetos)):
    # Há um problema nesse código, caso exista uma restrição [1,0,0,0,0,0,0], ele não consegue adicionar o '0' na lista, pois ele diz que o '0' é nulo (?)
    resultado_Regra1.append(regra1(objetos[i - j]))
    if resultado_Regra1[i]:
        # Para evitar que acabe selecionando a mesma variável 'Xi' duas vezes no conjunto solução caso exista uma restrição igual:
        if resultado_Regra1[i] not in solucao:
            solucao.append(resultado_Regra1[i])
        print(solucao)
        del objetos[i - j]
        j += 1


# Da mesma forma que usei o 'j' para evitar o erro, estamos usando aqui o auxiliador 'k':
k = 0
# Aqui iremos excluir as restrições já cobertas pelo conjunto solução, pois sabemos que satisfaz a condição '>= 1' para os conjuntos em 'solucao':
if solucao is not []:
    for i in range(len(objetos)):
        for j in range(len(solucao)):
                if objetos[i - k][solucao[j]]:
                    del objetos[i - k]
                    k += 1


regra2(conversor_Indices(objetos))

#regra3()

print(objetos)