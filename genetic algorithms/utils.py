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

#global variable to save the correct passcode
class Utils():
    def __init__(self, config):
        
        self.correct_passcode = config['passcode']['correct_passcode']
        if len(self.correct_passcode) > 0:
            print("MESSAGE: correct passcode read")
    
    #@params
    #   cromosome - type list, example: [character, character, character, ..., character-n]
    def calculate_fitness(self, cromosome): 
        #correct_passcode to list
        value = 0 ##temporal value to calculate fitness
        #your code here
        return value # 0.0 - 1.0

