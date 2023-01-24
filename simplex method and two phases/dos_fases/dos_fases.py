import numpy as np

from utilitarios import *


# ======================================================================================
# Objeto para guardar la ubicacion de una celda en la tabla
# ======================================================================================
class Celda:
    def __init__(self, columna, fila):
        self.columna = columna
        self.fila = fila


# ======================================================================================
# Esta funcion que ejecuta el flujo de dos fases
# ======================================================================================
def simplex_dos_fases(nombre_archivo, opcion, indice_optimizacion, numero_variables, numero_restricciones,
                      contenedor_funcion_objetivo, total_restricciones_lista):
    coeficientes_restricciones, limite_resricciones, coeficientes_funcion_objetivo, cantidad_desigualdades, cantidad_variables = mapear_eacuacion(
        nombre_archivo, opcion, indice_optimizacion, numero_variables, numero_restricciones,
        contenedor_funcion_objetivo, total_restricciones_lista)
    respuesta = Buscar_Solucion(nombre_archivo, coeficientes_restricciones, limite_resricciones,
                                coeficientes_funcion_objetivo, cantidad_desigualdades, cantidad_variables)

    # ======================================================================================
    # Respuesta a archivo y consola
    # ======================================================================================
    mensaje_iteracion = "Resultado Optima: "
    escritura_en_archivo(nombre_archivo, mensaje_iteracion)
    U = sum([x * y for x, y in zip(contenedor_funcion_objetivo, respuesta)])
    SolucionU = "U= " + str(U) + " ("
    escritura_en_archivo(nombre_archivo, SolucionU)
    print("U =", U)

    EscribirColumna(respuesta)
    listtofile(str(nombre_archivo).replace(".txt", "") + "_solucion.txt", np.array(respuesta).round(4).tolist())


# ======================================================================================
# Escrbir la lista a el archivo solucion
# ======================================================================================
def listtofile(filename, list):
    output_file = open(filename, 'a')

    for item in list:
        output_file.write(str(item) + ' | ')
    output_file.write(')\n')
    output_file.close()


# ======================================================================================
# Funcion para crear la tabla y resolver dos fases
# ======================================================================================
def Buscar_Solucion(nombre_archivo, coeficientes_restricciones, limite_resricciones, coeficientes_funcion_objetivo,
                    cantidad_desigualdades, cantidad_variables):
    if all(i <= 0 for i in coeficientes_funcion_objetivo) and all(i >= 0 for i in limite_resricciones):
        return [0] * cantidad_variables
    # ======================================================================================
    # Fase 1
    # ======================================================================================
    fase = False
    tabla, fila_fase1 = CrearTabla(coeficientes_restricciones, limite_resricciones, coeficientes_funcion_objetivo,
                                   cantidad_desigualdades, fase)
    respuesta, tabla_solucion_inicial = resolverTabla(nombre_archivo, tabla, coeficientes_restricciones,
                                                      limite_resricciones, cantidad_variables, cantidad_desigualdades,
                                                      fase, fila_fase1)

    if (respuesta == [-1] or respuesta == [float("inf")]):
        return respuesta
    validar_respuesta = respuesta_valida(respuesta, coeficientes_restricciones, limite_resricciones, cantidad_variables,
                                         cantidad_desigualdades)
    if (validar_respuesta):
        # ======================================================================================
        # Fase 2
        # ======================================================================================
        fase = True
        tabla, fila_fase1 = CrearTabla(coeficientes_restricciones, limite_resricciones, coeficientes_funcion_objetivo,
                                       cantidad_desigualdades, fase)
        respuesta, tabla_solucion_inicial = resolverTabla(nombre_archivo, tabla, coeficientes_restricciones,
                                                          limite_resricciones, cantidad_variables,
                                                          cantidad_desigualdades, fase, fila_fase1)
        resputa_primera_fase = respuesta_valida(tabla_solucion_inicial, coeficientes_restricciones, limite_resricciones,
                                                cantidad_variables, cantidad_desigualdades)
        if (respuesta == [-1] or respuesta == [float("inf")]):
            return respuesta
        validar_respuesta = respuesta_valida(respuesta, coeficientes_restricciones, limite_resricciones,
                                             cantidad_variables, cantidad_desigualdades)
    if (validar_respuesta):
        if not (resputa_primera_fase):
            return tabla_solucion_inicial
        else:
            return [-1]
    return respuesta


# ======================================================================================
# Crear tabla inicial para dos fases
# ======================================================================================
def CrearTabla(coeficientes_restricciones, limite_resricciones, coeficientes_funcion_objetivo, cantidad_desigualdades,
               fase):
    tabla = []
    primera_fila = [0] * (len(coeficientes_funcion_objetivo) + cantidad_desigualdades + 2)
    for i in range(cantidad_desigualdades):
        if fase and limite_resricciones[i] < 0:
            variables_holgura = [0] * cantidad_desigualdades
            variables_holgura[i] = -1.0
            fila = [-1 * x for x in coeficientes_restricciones[i]] + variables_holgura + [-1 * limite_resricciones[i]]
            tabla.append(fila)
            primera_fila = [a + b for a, b in zip(primera_fila, fila)]
        else:
            variables_holgura = [0] * cantidad_desigualdades
            variables_holgura[i] = 1.0
            fila = coeficientes_restricciones[i] + variables_holgura + [limite_resricciones[i]]
            tabla.append(fila)
    ultima_fila = [-1 * x for x in coeficientes_funcion_objetivo] + [0] * cantidad_desigualdades + [0]
    tabla.append(ultima_fila)
    return tabla, primera_fila


# ======================================================================================
# Esta funcion
# ======================================================================================
def resolverTabla(nombre_archivo, tabla, coeficientes_restricciones, limite_resricciones, cantidad_variables,
                  cantidad_desigualdades, fase, fila_fase1):
    filas_nobasicas = list(range(cantidad_variables, cantidad_desigualdades + cantidad_variables))
    fase1_completa = False
    solucion_fase1 = [0] * cantidad_variables
    while (fase or not all(a_mayorigual_b(i, 0) for i in tabla[len(tabla) - 1][:-1])):
        if fase and all(a_menorigual_b(k, 0) for k in fila_fase1[:-1]):
            fase = False
            fase1_completa = True
            solucion_fase1 = encontrar_respuesta(tabla, filas_nobasicas, cantidad_variables, cantidad_desigualdades)
            if all(a_mayorigual_b(i, 0) for i in tabla[len(tabla) - 1][:-1]):
                break
        notiene_solucion, celda_pivote = elegirpivote(tabla, cantidad_variables, filas_nobasicas, fase, fila_fase1)
        if notiene_solucion:
            if fase1_completa:
                return [-1], solucion_fase1
            else:
                return [float("inf")], solucion_fase1
        filas_nobasicas[celda_pivote.fila] = celda_pivote.columna
        tabla, fila_fase1 = procesar_pivote(tabla, celda_pivote, fase, fila_fase1)
        # ======================================================================================
        # Escribir iteaciones de tabla a archivo
        # ======================================================================================
        mensaje_iteracion = "iteracion \n"
        escritura_en_archivo(nombre_archivo, mensaje_iteracion)
        encabezado = crear_encabezado_dosfases(tabla)
        escritura_en_archivo(nombre_archivo, encabezado)
        contenedor_mensaje = creacion_de_matriz_en_string(np.array(tabla).round(4).tolist())
        escritura_en_archivo(nombre_archivo, contenedor_mensaje)
    return encontrar_respuesta(tabla, filas_nobasicas, cantidad_variables, cantidad_desigualdades), solucion_fase1


# ======================================================================================
# Realizar calculos para actualzar resultados de la tabla despues de elegir pivote
# ======================================================================================
def procesar_pivote(tabla, celda_pivote, fase, fila_fase1):
    pivoteporcolumnapivote = tabla[celda_pivote.fila][celda_pivote.columna]
    tabla[celda_pivote.fila] = [n / pivoteporcolumnapivote for n in tabla[celda_pivote.fila]]
    tabla[celda_pivote.fila][celda_pivote.columna] = 1.0
    for i in range(len(tabla)):
        if i != celda_pivote.fila:
            filaporpivote = tabla[i][celda_pivote.columna]
            filapivote = [j * filaporpivote for j in tabla[celda_pivote.fila]]
            tabla[i] = [a - b for a, b in zip(tabla[i], filapivote)]
            tabla[i][celda_pivote.columna] = 0
    if fase:
        filaporpivote = fila_fase1[celda_pivote.columna]
        filapivote = [j * filaporpivote for j in tabla[celda_pivote.fila]]
        fila_fase1 = [a - b for a, b in zip(fila_fase1, filapivote)]
        fila_fase1[celda_pivote.columna] = 0
    return tabla, fila_fase1


# ======================================================================================
# Funcion para encontrar el pivote de la tabla
# ======================================================================================
def elegirpivote(tabla, cantidad_variables, filas_nobasicas, fase, fila_fase1):
    posicion_pivote = Celda(0, 0)
    notiene_solucion = False
    if fase:
        posicion_pivote.columna = fila_fase1.index(max(fila_fase1[:-1]))
    else:
        posicion_pivote.columna = tabla[len(tabla) - 1][:-1].index(
            min(tabla[len(tabla) - 1][:-1]))  # Choose minimum based on first negative smallest index
    diferencias = []
    if posicion_pivote.columna != None:
        for r in range(len(tabla) - 1):
            if tabla[r][posicion_pivote.columna] > 0:
                diferencias.append(abs(tabla[r][-1] / tabla[r][posicion_pivote.columna]))
            else:
                diferencias.append(float("inf"))
        if all(i == float("inf") for i in diferencias):
            notiene_solucion = True
        fila_menor = min(diferencias)
        indice_fila_menor = [i for i, x in enumerate(diferencias) if x == fila_menor]

        if (len(indice_fila_menor) > 1):  # caso de empate
            variable_menor = []
            for j in indice_fila_menor:
                variable_menor.append(filas_nobasicas[j])
            posicion_pivote.fila = filas_nobasicas.index(min(variable_menor))
        else:
            posicion_pivote.fila = indice_fila_menor[0]
    else:
        notiene_solucion = True
    return notiene_solucion, posicion_pivote


# ======================================================================================
# Se crea la matriz la cual estara presente en el archivo
# ======================================================================================
def creacion_de_matriz_en_string(matriz):
    # ======================================================================================
    # Declaracion de variables
    # ======================================================================================
    filas = len(matriz)
    columnas = len(matriz[0])
    contenedor_mensaje = ""
    espacios_entre_numeros = "                    "
    largo = determinar_mayor(matriz)

    # ======================================================================================
    # Se recorren las filas
    # ======================================================================================
    for i in range(filas):
        # ======================================================================================
        # Se recorren las columnas
        # ======================================================================================
        for j in range(columnas):
            # ======================================================================================
            # Se le da formato entre los espacios entre numeros y el salto de linea respectivo
            # ======================================================================================
            longitud_cantidad_espacios = (largo - len(str(matriz[i][j])))
            espacio_temporal = espacios_entre_numeros[:longitud_cantidad_espacios]
            contenedor_mensaje += "  |" + espacio_temporal + str(matriz[i][j]) + "  "

        contenedor_mensaje += "\n"
    return contenedor_mensaje


# ======================================================================================
# Se determina el tamaño mayor
# ======================================================================================
def determinar_mayor(matriz):
    # ======================================================================================
    # Declaracion de variables
    # ======================================================================================
    filas = len(matriz)
    columnas = len(matriz[0])
    mayor = 2
    # ======================================================================================
    # Se recorren las filas
    # ======================================================================================
    for i in range(filas):
        # ======================================================================================
        # Se recorren las columnas
        # ======================================================================================
        for j in range(columnas):
            # ======================================================================================
            # Se determina el largo de la matriz en formato str
            # ======================================================================================
            contenedor_temporal = len(str(matriz[i][j]))
            if (mayor < contenedor_temporal):
                mayor = contenedor_temporal
    return mayor


# ======================================================================================
# imprimir encabezado
# ======================================================================================
def crear_encabezado_dosfases(tabla):
    listaEncabezado = ""
    for i in range(len(tabla[0]) - 1):
        listaEncabezado += "  |   " + "X" + str(i + 1) + "   "

    listaEncabezado += "  |   " + "LD" + "   " + "\n"
    return listaEncabezado


# ======================================================================================
# Funcion para encontrar la respuesta de la iteracion
# ======================================================================================
def encontrar_respuesta(tabla, filas_nobasicas, cantidad_variables, cantidad_desigualdades):
    respuesta = [0] * cantidad_variables
    for i in range(cantidad_desigualdades + cantidad_variables):
        if i < cantidad_variables and i in filas_nobasicas:
            indice = filas_nobasicas.index(i)
            respuesta[i] = tabla[indice][-1]
        elif i not in filas_nobasicas and tabla[-1][i] == 0:
            for j in range(cantidad_desigualdades - 1):
                if tabla[j][i] > 0:
                    return [-1]
        elif i < cantidad_variables:
            respuesta[i] = 0
    return respuesta


# ======================================================================================
# Funcion para buscar si existen respuestas validas
# ======================================================================================
def respuesta_valida(respuesta, coeficientes_restricciones, limite_resricciones, cantidad_variables,
                     cantidad_desigualdades):
    respuesta_invalida = False
    for i in range(cantidad_desigualdades):
        respuestas_validas = 0
        for j in range(cantidad_variables):
            respuestas_validas += coeficientes_restricciones[i][j] * respuesta[j]
        if a_mayor_b(respuestas_validas, limite_resricciones[i]):
            respuesta_invalida = True
    if not all(a_mayorigual_b(i, 0) for i in respuesta):
        respuesta_invalida = True
    return respuesta_invalida


# ======================================================================================
# Comparar celdas de tabla
# ======================================================================================
def a_mayor_b(a, b):
    return ((a > b) and not a_cercano_b(a, b))


def a_mayorigual_b(a, b):
    return ((a > b) or a_cercano_b(a, b))


def a_menor_b(a, b):
    return ((a < b) and not a_cercano_b(a, b))


def a_menorigual_b(a, b):
    return ((a < b) or a_cercano_b(a, b))


def a_cercano_b(a, b):
    return abs(a - b) <= np.finfo(float).eps


# ======================================================================================
# Funcion para escibir la solucion en consola
# ======================================================================================
def EscribirColumna(columna):
    largo = len(columna)
    if largo == 1 and columna[0] == -1:
        print("No tiene solucion")
    elif largo == 1 and columna[0] == float("inf"):
        print("Infinitas soluciones")
    else:
        print("Solucion acotada")
        print(' '.join(list(map(lambda x: '%.4f' % x, columna))))


# ======================================================================================
# Funcion para mepear las entradas en la ecuacion para dos fases
# ======================================================================================
def mapear_eacuacion(nombre_archivo, opcion, indice_optimizacion, numero_variables, numero_restricciones,
                     contenedor_funcion_objetivo, total_restricciones_lista):
    cantidad_variables = numero_variables
    cantidad_desigualdades = numero_restricciones
    coeficientes_restricciones = np.delete(np.array(total_restricciones_lista).astype(float), np.s_[-1:],
                                           axis=1).tolist()
    limite_resricciones = np.array(total_restricciones_lista).astype(float)[:, -1].tolist()
    coeficientes_funcion_objetivo = [float(i) for i in contenedor_funcion_objetivo]
    # print(cantidad_variables, cantidad_desigualdades, coeficientes_restricciones, limite_resricciones, coeficientes_funcion_objetivo)
    return coeficientes_restricciones, limite_resricciones, coeficientes_funcion_objetivo, cantidad_desigualdades, cantidad_variables


# ======================================================================================
# Invertir ecuaacion en caso de que incluye menor que o cambiar el signo de los coeficientes
# ======================================================================================
def invertirmenorigual(total_restricciones_lista, comparaciones):
    # ======================================================================================
    # Se declaran los simbolos a eliminar
    # ======================================================================================
    mayor_que = "<="
    menor_que = ">="
    igual_que = "="

    # ======================================================================================
    # Se recorre todas las retricciones
    # ======================================================================================
    for i, x in enumerate(comparaciones):
        # print(i, x)
        if (x == menor_que):
            # print("fila", total_restricciones_lista[i])
            total_restricciones_lista[i] = np.multiply(np.array(total_restricciones_lista[i]).astype(float),
                                                       -1.0).tolist()
            # print("fila invertida", total_restricciones_lista[i])

    return total_restricciones_lista
