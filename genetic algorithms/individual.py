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
import string
import random

from utils import Utils

# ===========================================================
# Variable global para guardar el código de acceso correcto
# ===========================================================
class Individual():
    # ===========================================================
    # Se inicializa la contraseña, la palabra y el fitness
    # ===========================================================
    def __init__(self, correct_passcode):
        """
        :param correct_passcode: correct passcode
        """
        self.word = ""
        self.correct_passcode = correct_passcode
        self.fitness = self.fitnesss()
    # ===========================================================
    # Se obtiene la palabra
    # ===========================================================
    def get_word(self):
        return self.word
    # ===========================================================
    # Se setea la palabra
    # ===========================================================
    def set_word(self, word):
        self.word = word
    # ===========================================================
    # Se obtiene el fitness
    # ===========================================================
    def get_fitness(self):
        return self.fitness
    # ===========================================================
    # Se setea un random de la palabra
    # ===========================================================
    def set_random_word(self):
        self.word = self.new_word(self.correct_passcode)
    # ===========================================================
    # Se setea el fitness
    # ===========================================================
    def set_fitness(self, fitness):
        self.fitness = self.fitnesss()
    # ===========================================================
    # El parametro de este funcion sera la contraseña correcta y se retorna la palabra
    # ===========================================================
    def new_word(self, correct_passcode):
        """
        create a new word
        :param correct_passcode: correct passcode
        :param correct_passcode:
        :return:
        """
        word = ""
        for i in range(len(correct_passcode)):
            word+=(random.choice(string.ascii_letters + string.digits))
        return word
    # ===========================================================
    # fitnesss se encarga de calcular el fitness de la palabra como tal
    # ===========================================================
    def fitnesss(self):
        # ===========================================================
        # Se inicializa el score
        # ===========================================================
        score = 0
        # ===========================================================
        # Si el largo de la contraseña es diferente de la palabra entra
        # ===========================================================
        if (len(self.correct_passcode) != len(self.word)):
            #rint("length do not match")
            return
        else:
            # ===========================================================
            # De lo contrario se aumenta el score para el retorno de la misma
            # ===========================================================
            for i in range(len(self.correct_passcode)):
                if (self.correct_passcode[i] == self.word[i]):
                    score += 1

            return score * 100 / len(self.correct_passcode)
    # ===========================================================
    # Mutate se encarga de mutar la palabra segun la eleccion que se tuvo
    # ===========================================================
    def mutate(self):
        """
        mutate the word
        :return:
        """
        index = random.randint(0, len(self.word) - 1)
        self.word = self.word[:index] + random.choice(string.ascii_letters + string.digits) + self.word[index + 1:]







