# ==================================================|
#                                                   |
#    ______  ____           ___    ____   ___   ___ |
#   /_  __/ / __ \         |__ \  / __ \ |__ \ |__ \|
#    / /   / / / /  _____  __/ / / / / / __/ / __/ /|
#  _/ /_  / /_/ /  /____/ / __/ / /_/ / / __/ / __/ |
# /____/  \____/         /____/ \____/ /____//____/ |
#                                                   |
# Instituto Tecnológico de Costa Rica               |
# Carrera:                                          |
#        Bachillerato en Ingeniería en Computación  |
# Curso:                                            |
#        Investigación de Operaciones               |
# Profesor:                                         |
#        Carlos Gamboa García                       |
# Alumnos:                                          |
#        Jonathan Quesada Salas                     |
#        Rodolfo Cruz                               |
#                                                   |
# Proyecto 3: Algoritmos Genéticos                  |
#                                                   |
# ==================================================|
import random
from individual import Individual

class Population(): # population class
    # ===========================================================
    # Se inicializa la poblacion, la contaseña correcta y los individuales
    # ===========================================================
    def __init__(self, population_size, correct_passcode):
        """
        constructor
        :param population_size:
        :param correct_passcode:
        """
        self.population_size = population_size
        self.correct_passcode = correct_passcode
        self.individuals = []
    # ===========================================================
    # Se obtiene el tamaño de la poblacion
    # ===========================================================
    def get_population_size(self):
        return self.population_size
    # ===========================================================
    # Se obtiene la contraseña correcta
    # ===========================================================
    def get_correct_passcode(self): # get the correct passcode
        return self.correct_passcode
    # ===========================================================
    # Se obtiene los individuales
    # ===========================================================
    def get_individuals(self): # get the individuals
        return self.individuals
    # ===========================================================
    # Se inicializa la primera de la poblacion
    # ===========================================================
    def set_first_population(self):
        # ===========================================================
        # Se recorre todo la población
        # ===========================================================
        for i in range(self.population_size):
            # ===========================================================
            # Se crea "individual"
            # ===========================================================
            individual = Individual(self.correct_passcode)
            # ===========================================================
            # Se obtiene una palabra random
            # ===========================================================
            individual.set_random_word()
            # ===========================================================
            # Se setea el fitness
            # ===========================================================
            individual.set_fitness(individual.fitnesss())
            # ===========================================================
            # Añadir el individuo a la población
            # ===========================================================
            self.individuals.append(individual)
    # ===========================================================
    # Ordenar la población por fitness
    # ===========================================================
    def sort_population(self):
        self.individuals.sort(key=lambda x: x.get_fitness(), reverse=True)
    # ===========================================================
    # Se selecciones el mejor individuo con el mejor fitness
    # ===========================================================
    def select_best_individuals(self, best_individuals, selection_method):
        # ===========================================================
        # Se inicializa la siguiente generacion
        # ===========================================================
        next_generation = []
        # ===========================================================
        # El caso que sea el metodo de seleccion de elite
        # ===========================================================
        if selection_method == "elite":
            # ===========================================================
            # Se recorre todos los mejores individuos
            # ===========================================================
            for i in range(best_individuals):
                # ===========================================================
                # Agregar los individuos a la próxima generación
                # ===========================================================
                next_generation.append(self.individuals[i])
        # ===========================================================
        # El caso que sea el metodo de seleccion de roulette
        # ===========================================================
        elif selection_method == "roulette":
            # ===========================================================
            # Se recorre todos los mejores individuos
            # ===========================================================
            for i in range(best_individuals):
                # ===========================================================
                # Agregar los individuos a la próxima generación
                # ===========================================================
                next_generation.append(self.roulette())
        # ===========================================================
        # El caso que sea el metodo de seleccion de ranking
        # ===========================================================
        elif selection_method == "ranking":
            # ===========================================================
            # Se recorre todos los mejores individuos
            # ===========================================================
            for i in range(best_individuals):
                # ===========================================================
                # Agregar los individuos a la próxima generación
                # ===========================================================
                next_generation.append(self.ranking())
        # ===========================================================
        # Se retorna la siguiente generacion
        # ===========================================================
        return next_generation

    def roulette(self):
        # ===========================================================
        # El total de fitness
        # ===========================================================
        total_fitness = 0 # total fitness
        # ===========================================================
        # Se recorre todos los individuos
        # ===========================================================
        for i in range(len(self.individuals)):
            # ===========================================================
            # Se añade el fitness en el total
            # ===========================================================
            total_fitness += self.individuals[i].get_fitness()
        # ===========================================================
        # Se crea un random entre 0 y el total de fitness
        # ===========================================================
        rand = random.uniform(0, total_fitness)
        # ===========================================================
        # Se recorre todos los individuos
        # ===========================================================
        for i in range(len(self.individuals)):
            # ===========================================================
            # Se extrae el fitness del numero random generado
            # ===========================================================
            rand -= self.individuals[i].get_fitness()
            # ===========================================================
            # Si el numero es menor o igual a 0
            # ===========================================================
            if rand <= 0:
                # ===========================================================
                # De ser el caso se retorna los individuos
                # ===========================================================
                return self.individuals[i]

    def ranking(self):
        # ===========================================================
        # el total de fitness
        # ===========================================================
        total_fitness = 0
        # ===========================================================
        # Se recorre todos los individuos
        # ===========================================================
        for i in range(len(self.individuals)):
            # ===========================================================
            # Se añade al total de fitness
            # ===========================================================
            total_fitness += i + 1
        # ===========================================================
        # se crea un numero aleatorio entre 0 y el total
        # ===========================================================
        rand = random.uniform(0, total_fitness)
        # ===========================================================
        # Se recorre el largo de los individuos
        # ===========================================================
        for i in range(len(self.individuals)):
            # ===========================================================
            # Se extrae el rango del numero aleatorio
            # ===========================================================
            rand -= i + 1
            # ===========================================================
            # En el caso que sea menor o igual a 0
            # ===========================================================
            if rand <= 0:
                # ===========================================================
                # Se retorna los individuos
                # ===========================================================
                return self.individuals[i]

    def create_child(self, parent1, parent2, crossover_method):
        child = ""
        # ===========================================================
        # Si es el caso que el metodo de crossover sea one-point
        # ===========================================================
        if crossover_method == "one-point":
            # ===========================================================
            # Apartir del random se genera un crossover point de 0 a el padre
            # ===========================================================
            crossover_point = random.randint(0, len(parent1.get_word()))
            child = parent1.get_word()[:crossover_point] + parent2.get_word()[crossover_point:]
        # ===========================================================
        # Si es el caso que el metodo de crossover sea two-point
        # ===========================================================
        elif crossover_method == "two-point":
            # ===========================================================
            # Apartir del random se genera un crossover point de 0 a el padre
            # ===========================================================
            crossover_point = random.randint(0, len(parent1.get_word()))
            child = parent1.get_word()[:crossover_point] + parent2.get_word()[crossover_point:]
            # ===========================================================
            # Apartir del random se genera un crossover point de 0 a el padre
            # ===========================================================
            crossover_point = random.randint(0, len(parent1.get_word()))
            child = child[:crossover_point] + parent1.get_word()[crossover_point:]
        # ===========================================================
        # Si es el caso que el metodo de crossover sea uniform
        # ===========================================================
        elif crossover_method == "uniform":
            # ===========================================================
            # Se recorre todo el largo de la palabra establecida por el padre
            # ===========================================================
            for i in range(len(parent1.get_word())):
                # ===========================================================
                # Si es menor a 0.5
                # ===========================================================
                if random.random() < 0.5:
                    child += parent1.get_word()[i]
                else:
                    child += parent2.get_word()[i]
        # ===========================================================
        # Se crea el individuo
        # ===========================================================
        new_individual = Individual(self.correct_passcode)
        # ===========================================================
        # Se seatea la palabra a establecer
        # ===========================================================
        new_individual.set_word(child)
        # ===========================================================
        # Se declara un determinado fitness
        # ===========================================================
        new_individual.set_fitness(new_individual.fitnesss())
        # ===========================================================
        # Se retorna el nuevo individuo
        # ===========================================================
        return new_individual

    def create_children(self, parents, crossover_method):
        # ===========================================================
        # Se declara la siguiente poblacion
        # ===========================================================
        next_population = []
        # ===========================================================
        # En dado caso que el crossover sea one-point
        # ===========================================================
        if crossover_method == "one-point":
            # ===========================================================
            # Se recorre todos los padres
            # ===========================================================
            for i in range(len(parents)):
                for j in range(len(parents)):
                    if i != j:
                        # ===========================================================
                        # Se añade a la siguiente poblacion, es como un filtro
                        # ===========================================================
                        next_population.append(self.create_child(parents[i], parents[j], crossover_method))
        # ===========================================================
        # En dado caso que el crossover sea two-point
        # ===========================================================
        elif crossover_method == "two-point":
            # ===========================================================
            # Se recorre todos los padres
            # ===========================================================
            for i in range(len(parents)):
                for j in range(len(parents)):
                    if i != j:
                        # ===========================================================
                        # Se añade a la siguiente poblacion, es como un filtro
                        # ===========================================================
                        next_population.append(self.create_child(parents[i], parents[j], crossover_method))
        # ===========================================================
        # En dado caso que el crossover sea uniform
        # ===========================================================
        elif crossover_method == "uniform":
            # ===========================================================
            # Se recorre la mitad de los padres
            # ===========================================================
            for i in range(int(len(parents) / 2)):
                for j in range(4):
                    next_population.append(self.create_child(parents[i], parents[len(parents) - 1 - i], crossover_method))
        self.individuals = next_population


    def mutation(self, mutation_rate):
        # ===========================================================
        # Se recorre todo el largo de los individuos
        # ===========================================================
        for i in range(len(self.individuals)):
            # ===========================================================
            # Si el random generado es menos a mutation rate se muta los individuos
            # ===========================================================
            if random.random() < mutation_rate:
                #print("Mutation")
                self.individuals[i].mutate()









