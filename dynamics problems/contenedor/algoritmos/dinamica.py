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
# ======================================================================================
# Funcion que resuelve el problema de la mochila con dinamica (Vista en clase)
# Entradas: matriz_vacia, texto_de_entrada, n, W
# Salidas: Ninguna
# ======================================================================================
def algoritmo_dinamica(matriz_vacia, texto_de_entrada, n, W):
    # ======================================================================================
    # Se recorre el rango de 1 a n
    # ======================================================================================
    for i in range(1, n):
        # ======================================================================================
        # Se determinan los valores de beneficio
        # ======================================================================================
        w_i, b_i = valores_de_beneficios(i, texto_de_entrada)
        for w in range(0, W):
            # ======================================================================================
            # En el caso que w_i sea mayor que w
            # ======================================================================================
            if w_i > w: matriz_vacia[i][w] = matriz_vacia[i-1][w]
            # ======================================================================================
            # En el caso que w_i sea menor que w
            # ======================================================================================
            else:
                # ======================================================================================
                # En el caso que b_i mas la matriz vacia sea sea mayor a lo faltante de la mochila
                # ======================================================================================
                if b_i + matriz_vacia[i-1][w-w_i] > matriz_vacia[i-1][w]:
                    matriz_vacia[i][w] = b_i + matriz_vacia[i-1][w-w_i]
                else:
                    matriz_vacia[i][w] = matriz_vacia[i-1][w]
# ======================================================================================
# Funcion que determina los beneficiones apartir de la lista de paquetes y sus valores
# Entradas: valor, lista_paquetes
# Salidas: valor_inicial_del_paquete, beneficio_inicial_del_paquete
# ======================================================================================
def valores_de_beneficios(valor, lista_paquetes):
    # ======================================================================================
    # Valores iniciales
    # ======================================================================================
    valor_inicial_del_paquete = 0
    beneficio_inicial_del_paquete = 0
    # ======================================================================================
    # Se recorren los paquetes
    # ======================================================================================
    for paquete in lista_paquetes:
        # ======================================================================================
        # Si es igual al valor se dispone del befenicio
        # ======================================================================================
        if paquete[0] == valor:
            valor_inicial_del_paquete = paquete[1]
            beneficio_inicial_del_paquete = paquete[2]
    return valor_inicial_del_paquete, beneficio_inicial_del_paquete
# ======================================================================================
# Funcion que determina el tiempo de duracion del problema de mochila en dinamica
# Entradas: contenedor_mochila, matriz_archivo, n, capacidad_mochila
# Salidas: tiempo_ejecucion
# ======================================================================================
def determinar_tiempo_dinamica(contenedor_mochila, matriz_archivo, n, capacidad_mochila):
    # ======================================================================================
    # Se establece un inicio y un fin para luego restar y retornar el tiempo dado
    # ======================================================================================
    inicio = time.perf_counter()
    algoritmo_dinamica(contenedor_mochila, matriz_archivo, n, capacidad_mochila)
    fin = time.perf_counter()
    tiempo_ejecucion = fin - inicio
    return tiempo_ejecucion