import random
import time
from datetime import datetime
from matplotlib import pyplot as plt

def read_data(fileName):
    f = open(fileName, 'r')
    aux = []  # vectorul in care vom insera valorile si greutatile citite
    count = 1
    totalItems = 0
    maxWeight = 0
    for x in f:
        if count == 1:  # daca citim prima linie
            totalItems = int(x)
            count = count + 1
        elif count == totalItems + 2:  # daca suntem pe ultima linie
            maxWeight = int(x)
        else:
            count = count + 1
            numbers = x.split()  # despartimim linia dupa spatii
            number1 = int(numbers[1])  # fitness
            number2 = int(numbers[2])  # weight
            aux.append([number1, number2])  # cand inseram, respectam forma declarata
    return maxWeight, aux

def generate_random_valid_solution(max_weight, data):
    while True:
        # genereaza o solutie random pentru dataset-ul dat si capacitatea maxima a rucsacului
        solution = []  # contine indicii item-ilor alesi
        weight = 0  # contine greutatea rucsacului
        value = 0  # contine valoarea rucsacului
        time.sleep(0.01)  # pentru ca seed-ul dat numarului nostru random sa se schimbe
        # folosim secundele pentru a genera un seed diferit de fiecare data, astfel numerele sa fie "mai aleatoare"
        now = datetime.now().microsecond
        random.seed(int(now))
        # pentru fiecare obiect din lista, alegem aleator daca il luam sau nu
        for i in range(0, len(data)):
            choice = int((random.random() * 10) % 2)  # random genereaza un float intre 0 si 1, il
            # inmultim cu 10, facem mod 2 si int ca sa obtinem valori 0 sau 1
            if choice == 0:
                solution.append(0)
            elif choice == 1:  # daca decidem sa alegem un obiect, adunam valoare si greutatea si il adaugam la solutie
                value = value + data[i][0]
                weight = weight + data[i][1]
                solution.append(1)
        if weight <= max_weight:
            print('Am generat o solutie aleatoare cu valoarea', value, 'si greutatea', weight)
            return value, weight, solution

def calculate_weight(solution, data):
    weight = 0
    for i in range(len(solution)):
        weight = weight + data[i][1] * solution[i]
    return weight


def calculate_fitness(solution, data, max_weight):
    value = 0
    weight = 0
    for i in range(len(solution)):
        weight = weight + data[i][1] * solution[i]
        value = value + data[i][0] * solution[i]
    if weight > max_weight:
        value = -1
    return value

def select_tournir_parents(population, tournir_size, data, max_weight):
    candidates = []
    #choosing random population*tourniz/100 parents
    for i in range(len(population)):
        number = random.random()
        if number < tournir_size/100:
            candidates.append(population[i])

    #choosing the best parent
    max = 0
    max_i = 0
    for i in range(len(candidates)):
        val = calculate_fitness(candidates[i], data, max_weight)
        #print(calculate_fitness(candidates[i], data, max_weight))
        if val > max:
            max = val
            max_i = i
    if (candidates != []):
        return candidates[max_i]
    else:
        return population[0]

def select_best_individuals(population, data, max_weight, length):
    #sortam dupa fitness indivizii
    for i in range(len(population)):
        j = i + 1
        while j < len(population):
            if calculate_fitness(population[i], data, max_weight) < calculate_fitness(population[j], data, max_weight):
                aux = population[i]
                population[i] = population[j]
                population[j] = aux
            j = j + 1
    return population[:length]

def run_all(fileName, no_iterations, population_size, tournir_parents, tournir_size, moutation_probability): #no_iterations=numarul de generatii, population_size=numarul de solutii per generare
    (max_weight, data) = read_data(fileName)
    algoritm_evolutiv(max_weight,data,no_iterations,population_size, 2, tournir_size,moutation_probability)


def algoritm_evolutiv(max_weight, data, no_iterations, population_size, tournir_parents, tournir_size, moutation_probability):
    time_array = []
    fitness_array = []
    population = []
    star_time = time.time()
    #initializam populatia cu solutii random si calculam fitness-ul
    for i in range(population_size):
        (value, weight, solution) = generate_random_valid_solution(max_weight, data)
        population.append(solution)

    for iteration in range(no_iterations):
        new_population = []
        #selectia parintilor
        parents = []
        for parent in range(tournir_parents):
            candidate = select_tournir_parents(population,tournir_size,data,max_weight)
            parents.append(candidate)
            #new_population.append(candidate)

        #incrucisare
        cutting_points = 2
        number1 = int(random.random() * len(population[0]))
        number2 = int(random.random() * len(population[0]))
        if number1 > number2:
            aux = number2
            number2 = number1
            number1 = aux
        #cazuri exceptionale
        if number1 == 0 and number2 == 0:
            number1 = 1
            number2 = int(len(population)/2)

        if number1 == number2:
            number2 = number2 + 1
            number1 = number1 - 1

        solution1 = parents[0][0:number1] + parents[1][number1:number2] + parents[0][number2:]
        solution2 = parents[1][0:number1] + parents[0][number1:number2] + parents[1][number2:]
        #print(solution1)
        #print(solution2)
        #print(number1)
        #print(number2)
        if calculate_fitness(solution1, data, max_weight) > 1:
            new_population.append(solution1)

        if calculate_fitness(solution2, data, max_weight) > 1:
            new_population.append(solution2)

        #####
        #mutatii
        for i in range(len(population)):
            #executam mutatii asupra fiecarui cromozom al fiecarui individ:
            new_individual = []
            for j in range(len(population[i])):
                number = random.random()
                if number > moutation_probability / 100:
                    new_individual.append((population[i][j] + 1) % 2)
                else:
                    new_individual.append(population[i][j])
            if calculate_fitness(new_individual, data, max_weight) > 1:
                new_population.append(new_individual)

        ######
        #selectam pentru generatia urmatoare
        new_population = select_best_individuals(population + new_population, data, max_weight,population_size)
        population = new_population

        time_array.append(time.time()-star_time)
        fitness_array.append(calculate_fitness(population[0],data,max_weight))
        if iteration % 50 == 0:
            print(f"Cea mai buna solutie dupa {iteration} iteratii este: {(calculate_fitness(population[0],data,max_weight))}")
    #for i in range(len(population)):
        #print(calculate_fitness(population[i],data,max_weight))
     #   print(population[i])
    end_time = time.time()
    print(calculate_fitness(population[0],data,max_weight))
    print(calculate_weight(population[i],data))
    print(f"Timpul necesar executiei: {end_time-star_time}s")
    plt.plot(time_array,fitness_array)
    plt.show()
run_all('../data/rucsac-200.txt', 200, 50, 2, 40, 80)
#paremeters: fileName, no_iterations, population_size, tournir_parents, tournir_size, moutation_probability
