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
import sys
# ======================================================================================
# Funcion que valida la cantidad de argumentos ingresados en terminal
# Entradas: Nada
# Salidas: 1 o 0
# ======================================================================================
def validar_entrada_de_argumentos():
    # ======================================================================================
    # Si es mas que 3
    # ======================================================================================
    if (len(sys.argv) < 3):
        print("POCOS PARAMETROS PAPI SUBELE A LA VARA")
        return 0
    # ======================================================================================
    # Si es menos que 3
    # ======================================================================================
    elif (len(sys.argv) > 3):
        print("MUCHOS PARAMETROS PAPI BAJELE A ESA VARA")
        return 0
    else:
        return 1
# ======================================================================================
# Funcion crea una matriz inicial de ceros por rellenar con numeros
# Entradas: valores_lista
# Salidas: lista_resultante
# ======================================================================================
def crear_matriz_de_ceros(filas, columnas):
    matriz_nula = []
    # ======================================================================================
    # Se recorren las filas
    # ======================================================================================
    for i in range(0, filas):
        contenedor = []
        # ======================================================================================
        # Se recorren las columnas
        # ======================================================================================
        for j in range(0, columnas):
            # ======================================================================================
            # Se pone un 0 en el espacio entre las columnas y filas para llenar toda la matriz
            # ======================================================================================
            contenedor.append(0)
        matriz_nula.append(contenedor)
    return matriz_nula 
# ======================================================================================
# Funcion valida los valores de beneficio a valores validos y usables
# Entradas: matriz_en_txt, capacidad_mochila
# Salidas: 1 o 0
# ======================================================================================
def validar_valores_beneficios(matriz_en_txt, capacidad_mochila):
    # ======================================================================================
    # Se recorre la matriz
    # ======================================================================================
    for i in matriz_en_txt:
        # ======================================================================================
        # Si se llega a validar que si el valor de la capacidad de la mochila es negativo o no
        # ======================================================================================
        for j in i:
            if (j < 0):
                return 1
            if (capacidad_mochila < 0):
                return 1
    return 0
    