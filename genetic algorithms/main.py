import tomllib
import utils
import random
import population

# ===========================================================
# Funcion que carga el archivo toml
# ===========================================================
def load_tomlib(filename):
    # ===========================================================
    # Se abre el archivo
    # ===========================================================
    with open(filename, "rb") as f:
        # ===========================================================
        # Se carga los datos
        # ===========================================================
        data = tomllib.load(f)
    # ===========================================================
    # Retorna la data
    # ===========================================================
    return data

if __name__ == '__main__':
    # ===========================================================
    # Se carga los datos del archivo toml
    # ===========================================================
    data = load_tomlib('pyproject.toml')
    #utils.Utils(data)
    #utils.Utils.calculate_fitness(data, "test")
    #print(data)
    #print(data['ag']['population_size'])
    #print(data['passcode']['correct_passcode'])

    # ===========================================================
    # Crear una población de individuos del tamaño de la población
    # ===========================================================
    previous_population = population.Population(data['ag']['population_size'], data['passcode']['correct_passcode'])
    # ===========================================================
    # Establecer la primera población
    # ===========================================================
    previous_population.set_first_population()
    # ===========================================================
    # Ordenar la población por fitness
    # ===========================================================
    previous_population.sort_population()
    # ===========================================================
    # Obtener los individuos
    # ===========================================================
    individuals = previous_population.get_individuals()
    # ===========================================================
    # Contador de generaciones
    # ===========================================================
    generation = 0
    # ===========================================================
    # Mientras que el mejor individuo no es el código de acceso correcto
    # ===========================================================
    while individuals[0].get_fitness() <= 100.0:
        # ===========================================================
        # Se imprime la generacion
        # ===========================================================
        print("Generation: ", generation)
        # ===========================================================
        # Si el mejor individuo es totalmente correcto
        # ===========================================================
        if (individuals[0].get_fitness() == 100):
            print("Solution found")
            break
        else:
            # ===========================================================
            # Si el mejor individuo no es 100% correcto
            # ===========================================================
            print("Solution not found")

        # ===========================================================
        # Selecciona los mejores individuos
        # ===========================================================
        next_parents = previous_population.select_best_individuals(data['ag']['num_parents'], data['ag']['selection_method']) # select the best individuals
        # print("parents", len(next_parents))
        # for i in range(len(next_parents)):
        #     print(next_parents[i].get_word(), next_parents[i].get_fitness())
        # ===========================================================
        # Crea la siguiente poblacion
        # ===========================================================
        next_population = population.Population(data['ag']['population_size'], data['passcode']['correct_passcode'])
        # ===========================================================
        # Se crean hijos apartir de los mejores individuos
        # ===========================================================
        next_population.create_children(next_parents, data['ag']['crossover_method'])
        # ===========================================================
        # Se muta el hijos
        # ===========================================================
        next_population.mutation(data['ag']['mutation_rate'])
        # ===========================================================
        # Se ordena la poblacion apartir del fitness que tengan
        # ===========================================================
        next_population.sort_population()
        # ===========================================================
        # Obtener los individuos de la próxima generación
        # ===========================================================
        next_generation_individuals = next_population.get_individuals()
        # ===========================================================
        # Establecer la próxima generación como la generación actual
        # ===========================================================
        previous_population = next_population
        # ===========================================================
        # Establecer los individuos de la próxima generación como los individuos actuales
        # ===========================================================
        individuals = next_generation_individuals
        generation += 1
        print("Best individual: ", individuals[0].get_word(), individuals[0].get_fitness())
    # ===========================================================
    # Se imprime el mejor individuo
    # ===========================================================
    print("Best individual: ", individuals[0].get_word(), individuals[0].get_fitness()) # print the best individual
    # ===========================================================
    # Se imprime la generación donde se encontró la solución
    # ===========================================================
    print("Solution found on generation", generation)