import sys
import time

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
    
def principal():
    """
    funcion principal
    parametros de entrada: algoritmo archivo.txt
    algoritmo parámetro requerido, valores 1=fuerza bruta, 2=programación dinámica
    archivo.txt archivo con datos del problema
    Ejemplo: python mina.py 1 mina1.txt
    :return: Impresion de resultados en consola
    """
    inicio = time.perf_counter()
    if (validar_entrada_de_argumentos() == 1):
        archivo = sys.argv[len(sys.argv) - 1]
        opcion = int(sys.argv[len(sys.argv) - 2])
        matriz = leer_Minastxt(archivo)

        if opcion == 1:
            output, ruta = mina_fuerza_bruta(matriz)
            print("output: ", output)
            print("selección de casillas: ", ruta)

        elif opcion == 2:
            output, ruta = mina_dinamico(matriz)
            print("output: ", output)
            print("selección de casillas: ", ruta)

        fin = time.perf_counter()

    print("Tiempo de ejecucion: " + str(fin - inicio) + " segundos")


def leer_Minastxt(archivo):
    """
    leer el archivo de texto
    :param archivo:
    :return:
    """
    with open(archivo, 'r') as f:
        matriz = [[int(num) for num in line.split(',')] for line in f]
    return matriz


# Fuerza bruta
def mina_fuerza_bruta(matriz):
    """
    :param matriz: matriz de enteros
    :return: oro maximo y el camino tomado con fuerza bruta recursiva
    """
    rutas = []
    cantidad_filas = len(matriz)
    cantidad_columnas = len(matriz[0])

    for i in range(len(matriz)):
        rutas += recorrer_caminos_fuerza_bruta([(i, 0)], cantidad_filas, cantidad_columnas, [])

    maximo = rutas[0]
    caminos = []
    for i in rutas:
        maximo = comparar_caminos(maximo, i, matriz, cantidad_columnas, caminos)
    caminos += [maximo]
    oro_maximo = 0

    for i in maximo:
        oro_maximo += matriz[i[0]][i[1]]

    return oro_maximo, caminos


def recorrer_caminos_fuerza_bruta(indice, cantidad_fila, cantidad_columna, ruta):
    """
    encontrar los caminos con fuerza bruta desde el indice
    :param indice: indice de la matriz
    :param cantidad_fila:
    :param cantidad_columna:
    :param ruta:
    :return:
    """
    ultimo = indice[-1]
    fila = ultimo[0]
    columna = ultimo[1] + 1

    if (columna < cantidad_columna):
        camino = []
        if (fila - 1 >= 0):
            camino += (
                recorrer_caminos_fuerza_bruta(indice + [(fila - 1, columna)], cantidad_fila, cantidad_columna, ruta))

        if (fila + 1 < cantidad_fila):
            camino += (
                recorrer_caminos_fuerza_bruta(indice + [(fila + 1, columna)], cantidad_fila, cantidad_columna, ruta))
        camino += (recorrer_caminos_fuerza_bruta(indice + [(fila, columna)], cantidad_fila, cantidad_columna, ruta))
        return ruta + camino
    else:
        return [indice]


def comparar_caminos(camino_a, camino_b, matriz, cantidad_columnas, caminos):
    """
    Comparar la cantidad de oro de los caminos
    :param camino_a: camino a comparar
    :param camino_b: camino a comparar
    :param matriz: mina
    :param cantidad_columnas:
    :param caminos:
    :return:
    """
    contador_camino_a = 0
    contador_camino_b = 0

    for i in range(cantidad_columnas):
        contador_camino_a += matriz[camino_a[i][0]][camino_a[i][1]]
        contador_camino_b += matriz[camino_b[i][0]][camino_b[i][1]]

    if (contador_camino_a > contador_camino_b):
        return camino_a
    elif (contador_camino_a == contador_camino_b):
        caminos += [camino_b]
        return camino_a
    else:
        del caminos[:]
        return camino_b


# Dinamico
def mina_dinamico(matriz):
    """
    :param matriz: matriz de enteros
    :return: resultado de maximo de oro y el camino tomado con programacion dinamica
    """
    cantidad_filas = len(matriz)
    cantidad_columnas = len(matriz[0])
    oro_maximo = 0
    ruta = []

    tabla_oro = [[-1 for i in range(cantidad_columnas)] for j in range(cantidad_filas)]

    tabla_ruta = [[-1 for i in range(cantidad_columnas)] for j in range(cantidad_filas)]

    for indice_fila in range(cantidad_filas):
        oro_camino, caminos = recorrer_caminos_dinamico(matriz, indice_fila, 0, cantidad_filas, cantidad_columnas,
                                                        tabla_oro, tabla_ruta)
        oro_maximo = max(oro_maximo, oro_camino)
        if oro_maximo == oro_camino:
            ruta = caminos
    return oro_maximo, ruta


def recorrer_caminos_dinamico(matriz, indice_fila, indice_columna, cantidad_filas, cantidad_columnas, tabla_oro,
                              tabla_ruta):
    """
    :param matriz: matriz de enteros
    :param indice_fila:
    :param indice_columna:
    :param cantidad_filas:
    :param cantidad_columnas:
    :param tabla_oro:
    :param tabla_ruta:
    :return: tabla de oro y tabla de ruta
    """

    if ((indice_fila < 0) or (indice_fila == cantidad_filas) or (indice_columna == cantidad_columnas)):
        camino = []
        return 0, camino

    if (tabla_oro[indice_fila][indice_columna] != -1):
        return tabla_oro[indice_fila][indice_columna], tabla_ruta[indice_fila][indice_columna]

    # Derecha
    derecha, ruta_derecha = recorrer_caminos_dinamico(matriz, indice_fila, indice_columna + 1, cantidad_filas,
                                                      cantidad_columnas, tabla_oro, tabla_ruta)

    # Diagonal arriba
    diagonal_arriba, ruta_diagonal_arriba = recorrer_caminos_dinamico(matriz, indice_fila - 1, indice_columna + 1,
                                                                      cantidad_filas, cantidad_columnas, tabla_oro,
                                                                      tabla_ruta)

    # Diagonal abajo
    diagonal_abajo, ruta_diagonal_abajo = recorrer_caminos_dinamico(matriz, indice_fila + 1, indice_columna + 1,
                                                                    cantidad_filas, cantidad_columnas, tabla_oro,
                                                                    tabla_ruta)

    # retornar el maximo y guarda el valor
    mina = matriz[indice_fila][indice_columna]
    camino = [[indice_fila, indice_columna]]

    maximoCamino = max(diagonal_arriba, diagonal_abajo, derecha)
    tabla_oro[indice_fila][indice_columna] = mina + maximoCamino

    tabla_ruta = guardar_ruta(maximoCamino, derecha, diagonal_arriba, diagonal_abajo, ruta_derecha,
                              ruta_diagonal_arriba, ruta_diagonal_abajo, camino, tabla_ruta, indice_fila,
                              indice_columna)

    return tabla_oro[indice_fila][indice_columna], tabla_ruta[indice_fila][indice_columna]


def guardar_ruta(maximoCamino, derecha, diagonal_arriba, diagonal_abajo, ruta_derecha, ruta_diagonal_arriba,
                 ruta_diagonal_abajo, camino_actual, tabla_ruta, indice_fila, indice_columna):
    """
    guardar la ruta tomada para el maximo de oro
    :param maximoCamino:
    :param derecha:
    :param diagonal_arriba:
    :param diagonal_abajo:
    :param ruta_derecha:
    :param ruta_diagonal_arriba:
    :param ruta_diagonal_abajo:
    :param camino_actual:
    :param tabla_ruta:
    :param indice_fila:
    :param indice_columna:
    :return: tablero con ruta
    """
    # Derecha
    if maximoCamino == derecha:
        if ruta_derecha != []:
            tabla_ruta[indice_fila][indice_columna] = camino_actual + ruta_derecha
        else:
            tabla_ruta[indice_fila][indice_columna] = camino_actual
    # Diagonal arriba
    elif maximoCamino == diagonal_arriba:
        if ruta_diagonal_arriba != []:
            tabla_ruta[indice_fila][indice_columna] = camino_actual + ruta_diagonal_arriba
        else:
            tabla_ruta[indice_fila][indice_columna] = camino_actual
    # Diagonal abajo
    else:
        if ruta_diagonal_abajo != []:
            tabla_ruta[indice_fila][indice_columna] = camino_actual + ruta_diagonal_abajo
        else:
            tabla_ruta[indice_fila][indice_columna] = camino_actual
    return tabla_ruta


principal()
