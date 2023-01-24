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
# Proyecto 2: Desempeño de Programación Dinámica    |
#                                                   |
# ==================================================|
from itertools import combinations
# ======================================================================================
# Funcion desarrolla el problema de la mochila con fuerza bruta
# Entradas: lista_paquetes, tamaño_mochila
# Salidas: contenedor_mochila, peso_mochila, valor
# ======================================================================================
def algoritmo_fuerza_bruta(lista_paquetes, tamaño_mochila):
    # ======================================================================================
    # Se declaran variables iniciales
    # ======================================================================================
    contenedor_mochila = []
    peso_mochila = 0
    beneficio = 0
    # ======================================================================================
    # Se crean combinaciones y se recorre cada una de ellas
    # ======================================================================================
    for combinacion in crear_combinaciones_de_lista(lista_paquetes):
        # ======================================================================================
        # Se determina el beneficio maximo dada la conbinacion
        # ======================================================================================
        maximo_peso, maximo_beneficio = determinar_beneficio_maximo(combinacion)
        # ======================================================================================
        # Si el maximo beneficio es mayor al beneficio
        # ======================================================================================
        if maximo_beneficio > beneficio:
            # ======================================================================================
            # Si el objeto llega a ser de capacidad similar al tamaño de la mochila
            # ======================================================================================
            if maximo_peso <= tamaño_mochila:
                valor = maximo_beneficio
                peso_mochila = maximo_peso
                contenedor_mochila = combinacion
                        
    return contenedor_mochila, peso_mochila, valor
# ======================================================================================
# Funcion desarrolla las combinaciones para el problema de fuerza bruta
# Entradas: lista_paquete
# Salidas: contenedor
# ======================================================================================
def crear_combinaciones_de_lista(lista_paquete):
    contenedor = []
    # ======================================================================================
    # Paquetes por recorrer
    # ======================================================================================
    for paquete in range(0, len(lista_paquete) + 1):
        # ======================================================================================
        # Se realizan las combinaciones dado los paquetes
        # ======================================================================================
        combinaciones = [list(i) for i in combinations(lista_paquete, paquete)]
        aux = combinaciones
        contenedor.extend(aux)
    return contenedor
# ======================================================================================
# Funcion determian el beneficio maximo dado una lista de paquetes
# Entradas: lista_paquete
# Salidas: sum(valores), sum(beneficios)
# ======================================================================================
def determinar_beneficio_maximo(lista_paquetes):
    valores = []
    beneficios = []
    # ======================================================================================
    # Se recorren los paquetes dado una lista de paquetes
    # ======================================================================================
    for paquete in lista_paquetes:
        valores.append(paquete[1]), beneficios.append(paquete[2])
    # ======================================================================================
    # Se retorna la suma de los valores y el beneficio
    # ======================================================================================
    return sum(valores), sum(beneficios)
