
# ======================================================================================
# Se leer el archivo respectivamente
# ======================================================================================
def leer_achivo(nombre_archivo):
    global contenido
    # ======================================================================================
    # Se abre el archivo y se lee linea por linea
    # ======================================================================================
    with open(nombre_archivo) as archivo:
        contenido = archivo.readlines()
    # ======================================================================================
    # Parsea las variables a continuacion
    # ======================================================================================
    lista_contenido, opcion, indice_optimizacion, numero_variables, numero_restricciones, total_restricciones_lista, total_igualdades_lista = parseo_archivo(
        nombre_archivo)

    # ======================================================================================
    # Se retornan dichas variables
    # ======================================================================================
    return lista_contenido, opcion, indice_optimizacion, numero_variables, numero_restricciones, total_restricciones_lista, total_igualdades_lista


# ======================================================================================
# Se parsea el contenido del archivo especificando
# ======================================================================================
def parseo_archivo(nombre_archivo):
    # ======================================================================================
    # Se establece la lista de contenidos a partir de la matriz dado un contenido
    # ======================================================================================
    lista_contenido = transformador_lineas_matriz(contenido)
    # ======================================================================================
    # Locacion de cada una en el archivo de entrada
    # ======================================================================================
    opcion = int(lista_contenido[0][0])
    indice_optimizacion = lista_contenido[0][1]
    numero_variables = int(lista_contenido[0][2])
    numero_restricciones = int(lista_contenido[0][3])
    total_restricciones_lista = lista_contenido[2:]
    total_igualdades_lista = []

    # ======================================================================================
    # Se retornan dichas variables
    # ======================================================================================
    return lista_contenido, opcion, indice_optimizacion, numero_variables, numero_restricciones, total_restricciones_lista, total_igualdades_lista


# ======================================================================================
# Se recorren la totalidad de las restricciones
# ======================================================================================
def recorrer_restricciones(numero_variables, total_restricciones_lista, total_igualdades_lista):
    # ======================================================================================
    # Se recorre todas las restricciones
    # ======================================================================================
    for i in range(len(total_restricciones_lista)):
        total_igualdades_lista += [total_restricciones_lista[i][numero_variables]]


# ======================================================================================
# Transformador de las lineas del texto a una matriz
# ======================================================================================
def transformador_lineas_matriz(lista):
    contenedor_resultado = []
    # ======================================================================================
    # Se recorre la lista
    # ======================================================================================
    for datos in lista:
        coma_espacio = ', '
        # ======================================================================================
        # Se limina el caracter determiando
        # ======================================================================================
        sublista = datos.split(coma_espacio)

        for elemento in sublista:
            coma = ','
            # ======================================================================================
            # Se limina el caracter determiando
            # ======================================================================================
            sub = elemento.split(coma)

        # ======================================================================================
        # Dicho resultado es agregado al contenedor resultado
        # ======================================================================================
        contenedor_resultado.append(sub)
    return (contenedor_resultado)


# ======================================================================================
# Escritura del archivo de salida archivo solucion
# ======================================================================================
def escritura_en_archivo(nombre_archivo, contenido):
    # ======================================================================================
    # Extension solicitada del archivo
    # ======================================================================================

    archivo = str(nombre_archivo).replace(".txt", "") + "_solucion.txt"
    # ======================================================================================
    # Se abre el archivo con permisos de escritura y lectura
    # ======================================================================================
    f = open(archivo, "a")
    # ======================================================================================
    # Se escribe el archivo
    # ======================================================================================
    f.write(contenido)
    # ======================================================================================
    # Se cierra el archivo
    # ======================================================================================
    f.close()


# ======================================================================================
# Se transforman los datos de la lista a numeros legibles para respectivos calculos
# ======================================================================================
def conversor_lista_a_numeros(lista):
    resultado = []

    # ======================================================================================
    # Se recorren los numeros de la lista
    # ======================================================================================
    for numero in lista:
        # ======================================================================================
        # Para un numero entero
        # ======================================================================================
        if (numero.count(".") == 0):
            resultado.append(int(numero))
        # ======================================================================================
        # Para un numero flotante
        # ======================================================================================
        if (numero.count(".") != 0):
            resultado.append(float(numero))
    return resultado


# ======================================================================================
# Convertir la matriz en numeros si es el caso
# ======================================================================================
def convertor_de_matriz_a_numeros(lista):

    # ======================================================================================
    # Contenedor de los numeros
    # ======================================================================================
    resultado = []
    # ======================================================================================
    # Se recorren los numeros
    # ======================================================================================
    for i in lista:
        contenedor_temporal = []
        for j in i:
            # ======================================================================================
            # En el caso que sea entero
            # ======================================================================================
            if (j.count(".") == 0):
                contenedor_temporal.append(int(j))
            # ======================================================================================
            # En el caso que sea flotante
            # ======================================================================================
            if (j.count(".") != 0):
                contenedor_temporal.append(float(j))
        resultado.append(contenedor_temporal)
    return resultado

# ======================================================================================
# Se crea el encabezado de la manera solicitada
# ======================================================================================
def creacion_del_encabezado(numero_variables, numero_restricciones):
    encabezado = ["Renglon", "VB"]

    # ======================================================================================
    # Se determinan la cantidad de variables basicas
    # ======================================================================================
    for x in range(1, numero_variables + 1):
        encabezado.append("X" + str(x))
    # ======================================================================================
    # Se determinan la cantidad de variables no basicas
    # ======================================================================================
    for y in range(1, numero_restricciones + 1):
        encabezado.append("Y" + str(y))

    # ======================================================================================
    # Se imprime el LD
    # ======================================================================================
    encabezado.append("LD")
    return encabezado


# ======================================================================================
# Extraer una columna
# ======================================================================================
def extraccion_columna(numero_columna, matriz):

    contenedor = []
    # ======================================================================================
    # Se recorre la matriz
    # ======================================================================================
    for indice in range(len(matriz)):
        # ======================================================================================
        # Dado el numero de columna se almacena en el contenedor y se retorna
        # ======================================================================================
        contenedor.append(matriz[indice][numero_columna])
    return contenedor


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
