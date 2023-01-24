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
import numpy as np
import sys
import time
# ======================================================================================
# VARIABLES INICIALES GLOBALES
# ======================================================================================
ORIGEN = 0
ARRIBA = 1
IZQUIERDA = 2
DIAGONAL = 4
# ======================================================================================
# Funcion para crear la tabla de puntaje
# Entradas: primera_secuencia: str, 
#           segunda_secuencia: str, 
#           coincidencia, no_coincidencia, penalización_por_hueco
# Salidas: lista_de_feclas, cuadricula_para_puntuacion
# ======================================================================================
def construir_tabla_puntaje(primera_secuencia: str, segunda_secuencia: str, coincidencia, no_coincidencia, penalización_por_hueco) -> tuple([[], np.ndarray]):
    # ======================================================================================
    # Se agrega 2 para la esquina y 2 espacios iniciales
    # ======================================================================================
    cuadricula_para_puntuacion = np.zeros((len(primera_secuencia)+1, (len(segunda_secuencia)+1)), dtype=np.int64)
    # ======================================================================================
    # Establecer puntuaciones constantes en la esquina
    # ======================================================================================
    cuadricula_para_puntuacion[0][0] = 0
    cuadricula_para_puntuacion[1][0] = penalización_por_hueco
    cuadricula_para_puntuacion[0][1] = penalización_por_hueco
    # ======================================================================================
    # Primeramente se encuentra la lista vacia, pero eventualmente podría ser reemplazado por un ndarry (usando máscaras de bits)
    # ======================================================================================
    lista_de_feclas = [[] for y in range(0, len(segunda_secuencia)+1)]
    # ======================================================================================
    # Configurar celda superior izquierda, para que pueda ser de un mejor manejo en rastreador
    # ======================================================================================
    lista_de_feclas[0].append([ORIGEN])
    # ======================================================================================
    # Se llenan las respectivas listas
    # ======================================================================================
    rellenar(primera_secuencia, segunda_secuencia, cuadricula_para_puntuacion, penalización_por_hueco, lista_de_feclas, coincidencia,no_coincidencia)                                              
    
    return (lista_de_feclas, cuadricula_para_puntuacion)

# ======================================================================================
# Funcion para rellenar las diferentes listas
# Entradas: primera_secuencia, segunda_secuencia, 
#           cuadricula_para_puntuacion, penalización_por_hueco, 
#           lista_de_feclas, coincidencia,no_coincidencia
# Salidas: Nada (Solo rellena)
# ======================================================================================
def rellenar(primera_secuencia, segunda_secuencia, cuadricula_para_puntuacion, penalización_por_hueco, lista_de_feclas, coincidencia,no_coincidencia):
    # ======================================================================================
    # Se llena primero la zona de la primera secuencia
    # ======================================================================================
    for letra_s1 in range(1, len(primera_secuencia) + 1):
        cuadricula_para_puntuacion[letra_s1][0] = penalización_por_hueco + cuadricula_para_puntuacion[letra_s1-1][0]
        lista_de_feclas[0].append([IZQUIERDA])
    # ======================================================================================
    # Se llena primero la zona de la segunda secuencia
    # ======================================================================================
    for letra_s2 in range(1, len(segunda_secuencia) + 1):
        cuadricula_para_puntuacion[0][letra_s2] = penalización_por_hueco + cuadricula_para_puntuacion[0][letra_s2-1]
        lista_de_feclas[letra_s2].append([ARRIBA])
    # ======================================================================================
    # Se llena la fila
    # ======================================================================================
    for y in range(0, len(segunda_secuencia)):
        for x in range(1, len(primera_secuencia) + 1):
            # ======================================================================================
            # Se obtiene los puntajes de las celdas relevantes o de mayor importancia
            # arriba, izquierda y diagonal
            # ======================================================================================
            resultado_celdas = celdas_para_puntaje(primera_secuencia[x-1], segunda_secuencia[y], cuadricula_para_puntuacion[x][y], cuadricula_para_puntuacion[x-1][y+1], cuadricula_para_puntuacion[x-1][y], coincidencia, no_coincidencia, penalización_por_hueco)
            # ======================================================================================
            # Puntuacion resultado_celdas[0]
            # Flechas resultado_celdas[1]
            # ======================================================================================
            cuadricula_para_puntuacion[x][y+1] = resultado_celdas[0]
            lista_de_feclas[y+1].append(resultado_celdas[1])
          
# ======================================================================================
# Funcion para establecer las celdas para el puntaje
# Entradas: primera_secuencia: str, segunda_secuencia: str, 
#           arriba: int, izquierda: int, diagonal: int, 
#           coincidencia: int, no_coincidencia: int, penalización_por_hueco: int
# Salidas: puntuacion_maxima, flechas_para_almacenar
# ======================================================================================
def celdas_para_puntaje(primera_secuencia: str, segunda_secuencia: str, arriba: int, izquierda: int, diagonal: int, coincidencia: int, no_coincidencia: int, penalización_por_hueco: int) -> tuple([int, []]):
    
    # ======================================================================================
    # Obtenga la puntuación máxima y la lista de flechas para una celda determinada.
    # ======================================================================================
    # Inicializar a valores muy bajos
    # ======================================================================================
    puntuacion_de_diagonal = -sys.maxsize
    puntuacion_de_arriba = -sys.maxsize
    puntuacion_de_izquierda = -sys.maxsize
    # ======================================================================================
    # Calcule la puntuación en la diagonal superior izquierda
    # ======================================================================================
    if primera_secuencia == segunda_secuencia:
        puntuacion_de_diagonal = diagonal + coincidencia
    else: 
        puntuacion_de_diagonal = diagonal + no_coincidencia
    # ======================================================================================
    # Calcular el puntaje de las celdas de arriba
    # ======================================================================================
    puntuacion_de_arriba = arriba + penalización_por_hueco
    # ======================================================================================
    # Calcular el puntaje de las celdas de las izquierda
    # ======================================================================================
    puntuacion_de_izquierda = izquierda + penalización_por_hueco
    # ======================================================================================
    # Se encuentra la maxima puntuacion
    # ======================================================================================
    puntuacion_maxima = max(puntuacion_de_diagonal, puntuacion_de_arriba, puntuacion_de_izquierda)
    # ======================================================================================
    # Eleccion de las feclas
    # ======================================================================================
    flechas_para_almacenar = []
    if puntuacion_maxima == puntuacion_de_izquierda: flechas_para_almacenar.append(IZQUIERDA)
    
    if puntuacion_maxima == puntuacion_de_arriba: flechas_para_almacenar.append(ARRIBA)
    
    if puntuacion_maxima == puntuacion_de_diagonal: flechas_para_almacenar.append(DIAGONAL)
    
    return (puntuacion_maxima, flechas_para_almacenar)

# ======================================================================================
# Funcion para rastrear la mejor opcion apartir de las secuencias
# Entradas: primera_secuencia: str, segunda_secuencia: str, lista_de_fechas: []
# Salidas: lista_de_secuencia
# ======================================================================================
def rastreador(primera_secuencia: str, segunda_secuencia: str, lista_de_fechas: []) -> []:
    
    lista_flechas_x, lista_flechas_y = len(lista_de_fechas[0])-1, len(lista_de_fechas)-1
    # ======================================================================================
    # Lista a rastrear
    # ======================================================================================
    lista_a_rastrear = []
    # ======================================================================================
    # Se recorre cada una de las cadenas realizadas tanto las iniciales como las resultantes
    # ======================================================================================
    for i in range(0, len(lista_de_fechas[lista_flechas_y][lista_flechas_x])):
        lista_a_rastrear.append({'lista_flechas_x': lista_flechas_x, 'lista_flechas_y': lista_flechas_y, 'nueva_primera_secuencia': '', 'nueva_segunda_secuencia': '', 'flecha': lista_de_fechas[lista_flechas_y][lista_flechas_x][i]})
    # ======================================================================================
    # Lista para almacenar las secuencias
    # ======================================================================================
    lista_de_secuencia = []
    # ======================================================================================
    # Si la lista a rastrear no es vacia se recorre
    # ======================================================================================
    while (len(lista_a_rastrear) > 0):
        # ======================================================================================
        # Lista para rastrear
        # ======================================================================================
        lista_flechas_x = lista_a_rastrear[0]['lista_flechas_x']
        lista_flechas_y = lista_a_rastrear[0]['lista_flechas_y']
        # ======================================================================================
        # Lista para almacenar las nuevas secuencias
        # ======================================================================================
        nueva_primera_secuencia = lista_a_rastrear[0]['nueva_primera_secuencia']
        nueva_segunda_secuencia = lista_a_rastrear[0]['nueva_segunda_secuencia']
        # ======================================================================================
        # Definir una lista para almacenar las flechas a rastrear
        # ======================================================================================
        lista_de_flechas_a_rastrear = lista_a_rastrear[0]['flecha']

        while lista_flechas_x + lista_flechas_y > 0:
            # ======================================================================================
            # Lista pasa secuencia 1 y 2
            # ======================================================================================
            lista_s1 = primera_secuencia[lista_flechas_x-1]
            lista_s2 = segunda_secuencia[lista_flechas_y-1]
            # ======================================================================================
            # En el caso que sea diagonal
            # ======================================================================================
            if lista_de_flechas_a_rastrear == DIAGONAL:
                nueva_primera_secuencia = lista_s1 + nueva_primera_secuencia
                nueva_segunda_secuencia = lista_s2 + nueva_segunda_secuencia

                lista_flechas_x -= 1
                lista_flechas_y -= 1
            # ======================================================================================
            # En el caso que sea izquierda
            # ======================================================================================
            elif lista_de_flechas_a_rastrear == IZQUIERDA:
                nueva_primera_secuencia = lista_s1 + nueva_primera_secuencia
                nueva_segunda_secuencia = '-' + nueva_segunda_secuencia

                lista_flechas_x -= 1
            # ======================================================================================
            # En el caso que sea arriba
            # ======================================================================================
            else:
                nueva_primera_secuencia = '-' + nueva_primera_secuencia
                nueva_segunda_secuencia = lista_s2 + nueva_segunda_secuencia

                lista_flechas_y -= 1
            # ======================================================================================
            # Apartir de la lista generada se declarara como esa la actual lista de flechas a rastrear
            # ======================================================================================
            curr_lista_de_fechas = lista_de_fechas[lista_flechas_y][lista_flechas_x]
            lista_de_flechas_a_rastrear = curr_lista_de_fechas[0]
        # ======================================================================================
        # Se añade la lista de las secuencias
        # ======================================================================================
        lista_de_secuencia.append([nueva_primera_secuencia, nueva_segunda_secuencia])     
        lista_a_rastrear = lista_a_rastrear[1:]
        
    return lista_de_secuencia

# ======================================================================================
# Funcion para validar entradas y datos incorrectos
# Entradas: primera_secuencia: str, segunda_secuencia: str, 
#           coincidencia: int = 1, no_coincidencia: int = -1, 
#           penalización_por_hueco: int = -2
# Salidas: cadenas_resultantes, puntaje_de_coincidencias
# ======================================================================================
def validador(primera_secuencia: str, segunda_secuencia: str, coincidencia: int = 1, no_coincidencia: int = -1, penalización_por_hueco: int = -2) -> tuple([[], int]):
    # ======================================================================================
    # Casos invalidos de entrada de parte de las secuencias
    # ======================================================================================
    if primera_secuencia == '': raise ValueError('El ejercicio debe de tener 2 secuencias querido usuario')
    
    if segunda_secuencia == '': raise ValueError('El ejercicio debe de tener 2 secuencias querido usuario')

    if primera_secuencia == None: raise ValueError('No hay nada compa')
    
    if segunda_secuencia == None: raise ValueError('No hay nada compa')
    # ======================================================================================
    # Configurar tablas de puntuación y flechas
    # ======================================================================================
    tabla_resultante = construir_tabla_puntaje(primera_secuencia, segunda_secuencia, coincidencia, no_coincidencia, penalización_por_hueco)
    
    tabla_flechas = tabla_resultante[0]
    tabla_puntaje = tabla_resultante[1]
    # ======================================================================================
    # La dimension debe de ser cuadrada, sino no deberia ser ejecutada
    # ======================================================================================
    dimension = tabla_puntaje.shape
    # ======================================================================================
    # Se debe de ejecutar el rastreador de la tabla de flechas dadas en la clase
    # ======================================================================================
    cadenas_resultantes = rastreador(primera_secuencia, segunda_secuencia, tabla_flechas)
    puntaje_de_coincidencias = tabla_puntaje[dimension[0]-1][dimension[1]-1]
    
    return (cadenas_resultantes, puntaje_de_coincidencias)

# ======================================================================================
# Funcion ejecutar el programa y establecer el tiempo de duracion del programa junto con
# el formato que se solicita de impresion
# Entradas: Ninguna
# Salidas: Ninguna
# ======================================================================================
def principal():
    # ======================================================================================
    # leer desde archivo como parametro
    # ======================================================================================
    if (validar_entrada_de_argumentos() == 1):
        archivo = sys.argv[len(sys.argv) - 1]
        matriz = leer_Minastxt(archivo)
        # ======================================================================================
        # limpiar dos cadenas
        # ======================================================================================
        cadena1 = matriz[0].strip("\n")
        cadena2 = matriz[1]

    # ======================================================================================
    # Se establece un inicio y un fin para la ejecuncion del programa
    # ======================================================================================
    inicio = time.perf_counter()

    resultado_cadenas = validador(cadena1, cadena2)
    fin = time.perf_counter()
    # ======================================================================================
    # Se establece el tiempo de ejecucion
    # ======================================================================================
    tiempo_ejecucion = fin - inicio
    # ======================================================================================
    # Cadenas resultantes sean las iniciales
    # ======================================================================================
    cadenas_resultantes = resultado_cadenas[0]
    # ======================================================================================
    # Se retorna el puntaje mas eficiente
    # ======================================================================================
    print('Score:', f'{resultado_cadenas[1]}')
    # ======================================================================================
    # Se recorren las cadenas de caracteres del problema
    # ======================================================================================
    for n in range(0,len(cadenas_resultantes)):
        print(cadenas_resultantes[n][0])
        print(cadenas_resultantes[n][1])
    # ======================================================================================
    # Se imprime el tiempo de ejecucion
    # ======================================================================================
    print("Tiempo de ejecución:", tiempo_ejecucion, "segundos")

# ======================================================================================
# Leer archivo agregar lineas a matriz
# ======================================================================================
def leer_Minastxt(archivo):
    """
    leer el archivo de texto
    :param archivo:
    :return:
    """
    with open(archivo, 'r') as f:
        matriz = f.readlines()
    return matriz

# ======================================================================================
# Funcion que valida la cantidad de argumentos ingresados en terminal
# Entradas: Nada
# Salidas: 1 o 0
# ======================================================================================
def validar_entrada_de_argumentos():
    # ======================================================================================
    # Si es mas que 3
    # ======================================================================================
    if (len(sys.argv) < 2):
        print("POCOS PARAMETROS PAPI SUBELE A LA VARA")
        return 0
    # ======================================================================================
    # Si es menos que 3
    # ======================================================================================
    elif (len(sys.argv) > 2):
        print("MUCHOS PARAMETROS PAPI BAJELE A ESA VARA")
        return 0
    else:
        return 1

principal()