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
import time
from algoritmos.fuerza_bruta import *
from algoritmos.dinamica import *
from utilitarios.utilitarios_archivo import *
from utilitarios.utilitarios import *
# ======================================================================================
# Funcion valida los valores de beneficio a valores validos y usables
# Entradas: matriz_inicial, achivo_matriz_txt, n, w
# Salidas: contenedor, identificador_contenedor
# ======================================================================================
def obtener_informacion_valores_mochila(matriz_inicial, achivo_matriz_txt, n, w):
    # ======================================================================================
    # Se establecen las variables iniciales
    # ======================================================================================
    i = n
    k = w
    contenedor = []
    identificador_contenedor = []
    # ======================================================================================
    # En el caso que i sea mayor o igual que 0
    # ======================================================================================
    while(i >= 0):
        w_bi = achivo_matriz_txt[i-1][1]
        if matriz_inicial[i][k] == matriz_inicial[i-1][k]:
            i = i-1
        # ======================================================================================
        # En el caso que la matriz inicial sea diferente a una matriz inicial dada la fila anterior
        # ======================================================================================
        if matriz_inicial[i][k] != matriz_inicial[i-1][k]:
            contenedor.append(achivo_matriz_txt[i-1])
            identificador_contenedor.append(i)
            i = i-1
            k = k-w_bi
    return contenedor, identificador_contenedor
# ======================================================================================
# Funcion valida los valores de beneficio a valores validos y usables
# Entradas: Ninguna
# Salidas: Ninguna
# ======================================================================================
def principal():
    # ======================================================================================
    # Si validar entrada de argumentos es igual que 1 quiere decir que todo anda bien siga adelante
    # ======================================================================================
    if (validar_entrada_de_argumentos() == 1):
        # ======================================================================================
        # Se establece la posicion de cada uno de los argumentos
        # ======================================================================================
        archivo = sys.argv[len(sys.argv) - 1]
        opcion = int(sys.argv[len(sys.argv) - 2])
        matriz_archivo, capacidad_mochila = leer_achivo(archivo)
        # ======================================================================================
        # Se valida si existe un negativo en el archivo
        # ======================================================================================
        if (validar_valores_beneficios(matriz_archivo, capacidad_mochila) == 1):
            print("POR AHI DEBE DE ANDAR UN NEGATIVILLO")
            return 0
        # ======================================================================================
        # Opcion para ejecutar el problema con fuerza bruta
        # ======================================================================================
        if (opcion == 1):
            # ======================================================================================
            # Se establece el inicio y final de la funcion para luego retornar el tiempo de ejecucion
            # ======================================================================================
            inicio = time.perf_counter()
            contenedor, pesoMochila, beneficio = algoritmo_fuerza_bruta(matriz_archivo, capacidad_mochila-1)
            fin = time.perf_counter()
            tiempo_ejecucion = fin - inicio
            print("Input: (", archivo, ")")
            # ======================================================================================
            # Se imprime el contenido del archivo
            # ======================================================================================
            contenido_archivo(archivo)
            print(" Output: ", "\n", "Beneficio maximo: ", beneficio, "\n", "Incluidos: ", [x[0] for x in contenedor], "Tiempo de ejecucion: ", tiempo_ejecucion, "segundos")
        # ======================================================================================
        # Opcion para ejecutar el problema con dinamica
        # ======================================================================================
        elif (opcion == 2):
            n = matriz_archivo[-1][0] + 1
            # ======================================================================================
            # Se crea primero una matriz nula
            # ======================================================================================
            contenedor_mochila = crear_matriz_de_ceros(n, capacidad_mochila) 
            # ======================================================================================
            # Se establece el inicio y final de la funcion para luego retornar el tiempo de ejecucion
            # ======================================================================================
            determinar_tiempo_dinamica(contenedor_mochila, matriz_archivo, n, capacidad_mochila)
            # ======================================================================================
            # Se obtiene la informacion respectiva de los valores de la mochila
            # ======================================================================================
            mochila, paquetes = obtener_informacion_valores_mochila(contenedor_mochila, matriz_archivo, n-1, capacidad_mochila-1)
            # ======================================================================================
            # Se determina los respectivos beneficios
            # ======================================================================================
            valoreMaximo, beneficio = determinar_beneficio_maximo(mochila)
            
            paquetes_finales = list(reversed(paquetes))
            # ======================================================================================
            # Se imprime la informacion respectiva solicitada
            # ======================================================================================
            print("Input: ", archivo)
            contenido_archivo(archivo)
            print( " Output: ", "\n", "Beneficio maximo: ", beneficio, "\n", "Incluidos: ", paquetes_finales, "\n", "Tiempo de ejecucion: ", determinar_tiempo_dinamica(contenedor_mochila, matriz_archivo, n, capacidad_mochila), "segundos")
            
principal()