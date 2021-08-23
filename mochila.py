# coding: utf-8
from random import randint, choices, random

'''
Para este experimento foi utilizado 
o conjunto de objetos P08 fornecido no endereço:
https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/knapsack_01.html
'''

c = 6404180 #capacidade da mochila
n_obj = 24 #número de objetos

p = [
    382745, 799601, 909247, 729069, 467902, 44328, 34610, 698150, 823460, 
    903959, 853665, 551830, 610856, 670702, 488960, 951111, 323046, 446298,
    931161, 31385, 496951, 264724, 224916, 169684
] #peso de cada objeto referenciado pelo índice

v = [
    825594, 1677009, 1676628, 1523970, 943972, 97426, 69666, 1296457,
    1679693, 1902996, 1844992, 1049289, 1252836, 1319836, 953277, 2067538,
    675367, 853655, 1826027, 65731, 901489, 577243, 466257, 369261
] #valor de cada objeto referenciado pelo índice

gen = 100 #número de gerações
tam_pop = 100 #tamanho da população
tx_cruz = 0.8 #taxa de cruzamento
tx_mut = 0.1 #taxa de mutação

#Função objetivo
def func_obj(x):

    peso_total = sum(i * p[j] for j, i in enumerate(x))

    if peso_total <= c:
        fit = sum(i * v[j] for j, i in enumerate(x))
    
    else:
        fit = sum(i * v[j] for j, i in enumerate(x)) *\
                ((1 - ((sum(i * p[j] for j, i in enumerate(x)) - c)/c ))/1.1)
    
    return fit


#Função de seleção de pais
def selecao(pop, fit):
    
    indices = []
    for i in range(min(5, len(fit))):
        s = randint(0, len(fit)-1)
        while s in indices:
            s = randint(0,len(fit)-1)
        indices.append(s)
    grupo = [fit[i] for i in indices]
    pai1 = fit.index(max(grupo))
    grupo.remove(fit[pai1])
    
    pai2 = fit.index(max(grupo))
    if pai2 == pai1: pai2 = fit.index(max(grupo),pai1+1)

    return pai1, pai2

#Função de cruzamento
def cruzamento(pai1, pai2):

    if random() <= tx_cruz:
        corte = randint(0,23)
        filho1 = pai1[:corte]+pai2[corte:]
        filho2 = pai2[:corte]+pai1[corte:]
    
    else:
        filho1 = pai1
        filho2 = pai2

    return filho1, filho2

#Função de mutação
def mutacao(pop):

    for i in pop:
        for j in range(n_obj):
            if random() <= tx_mut:
                i[j] = 1 - i[j]

    return pop

def main():

    if (tam_pop%2 != 0):
        print("Não é possível cruzar todos os pais porque o tamanho da população é ímpar!")
        exit(0)

    #Criação da população
    pop = [[randint(0, 1) for i in range(n_obj)] for j in range(tam_pop)]

    for i in range(gen):

        #Cálculo do fitness
        fit = []
        for k in range(len(pop)):
            fit.append(func_obj(pop[k]))

        elitista = pop[fit.index(max(fit))] #Melhor indivíduo daquela geração

        pop_int = [] #população intermediária
        fit_cpy = fit[:]

        while(len(pop) != 0):
            
            pai1, pai2 = selecao(pop, fit_cpy)
            filho1, filho2 = cruzamento(pop[pai1], pop[pai2])
            pop_int.append(filho1)
            pop_int.append(filho2)

# Verificação para remover o maior índice primeiro 
# já que lista sofre um shift nas posições quando um elemento é removido
            if (pai1 > pai2):
                fit_cpy.pop(pai1)
                fit_cpy.pop(pai2)
                pop.pop(pai1)
                pop.pop(pai2)
            
            else:
                fit_cpy.pop(pai2)
                fit_cpy.pop(pai1)
                pop.pop(pai2)
                pop.pop(pai1)

        pop = pop_int

        pop = mutacao(pop)

        pop[randint(0, tam_pop-1)] = elitista

        print(
            "Geração", i, "\b:\nIndivíduo:", pop[fit.index(max(fit))], 
            "\nFit =", max(fit)
            )

    print("\nMelhor indivíduo encontrado:", pop[fit.index(max(fit))], "\n")

if __name__ == '__main__': main()    