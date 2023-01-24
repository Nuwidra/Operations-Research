import warnings
import numpy as np
import sys
from sympy import *
from sympy import *
from utilitarios import *

# ======================================================================================
# Esta funcion se encargara de validad que si el problema ingresado es simplex o no
# ======================================================================================
def validar_simplex(total_restricciones_lista, numero_variables):
    simbolo = "="

    # ======================================================================================
    # Se recorren todas las restricciones de la lista
    # ======================================================================================
    for lista in total_restricciones_lista:

        # ======================================================================================
        # En el caso que la lista tenga algo diferente retorna True
        # ======================================================================================
        if (lista[numero_variables] != simbolo):
            return True
        else:
            False

# ======================================================================================
# Se elimina las restricciones del problema
# ======================================================================================
def eliminar_restricciones(numero_variables, total_restricciones_lista):
    # ======================================================================================
    # Se declaran los simbolos a eliminar
    # ======================================================================================
    mayor_que = "<="
    menor_que = ">="
    igual_que = "="
    comparaciones = []

    # ======================================================================================
    # Se recorre todas las retricciones
    # ======================================================================================
    for i in total_restricciones_lista:

        # ======================================================================================
        # En el caso que mayor que se elimina
        # ======================================================================================
        if (i[numero_variables] == mayor_que):
            comparaciones.append(i[numero_variables])
            i.remove(mayor_que)

        # ======================================================================================
        # En el caso que igual que se elimina
        # ======================================================================================
        elif (i[numero_variables] == igual_que):
            comparaciones.append(i[numero_variables])
            i.remove(igual_que)

        # ======================================================================================
        # En el caso que menor que se elimina
        # ======================================================================================
        elif (i[numero_variables] == menor_que):
            comparaciones.append(i[numero_variables])
            i.remove(menor_que)

    # ======================================================================================
    # Se retorna las restricciones
    # ======================================================================================
    return total_restricciones_lista, comparaciones


# ======================================================================================
# Funcion principal para simplex que llamara recursivamente a una funcion auxiliar
# hasta que se acabe el problema
# ======================================================================================
def simplex(nombre_archivo, opcion, indice_optimizacion, numero_variables, numero_restricciones,
            funcion_objetivo_inicial, total_restricciones_lista):
    # ======================================================================================
    # Se transforma las restricciones totales en formato manejable
    # ======================================================================================
    total_restricciones_lista = convertor_de_matriz_a_numeros(total_restricciones_lista)

    contenedor_funcion_objetivo = []

    # ======================================================================================
    # La funcion objetivo inicial se debe de igualar a 0
    # ======================================================================================
    for parametros in funcion_objetivo_inicial:
        contenedor_funcion_objetivo.append(parametros * -1)

    # ======================================================================================
    # Crear la matriz inicial
    # ======================================================================================
    matriz_inicio = crear_matriz_inicial(numero_variables, numero_restricciones, contenedor_funcion_objetivo,
                                         total_restricciones_lista,
                                         opcion)

    # ======================================================================================
    # Se llama la funcion auxiliar
    # ======================================================================================
    return simplex_aux(nombre_archivo, numero_variables, indice_optimizacion, matriz_inicio, opcion)


# ======================================================================================
# Funcion auxiliar donde esta misma va a contemplar mensajes de iteracion y solciones
# no optimas y optimas para el problema, se ejecutan las iteraciones y validaciones
# ======================================================================================
def simplex_aux(nombre_archivo, numero_variables, indice_optimizacion, matriz_anterior, opcion):
    # ======================================================================================
    # Se parsea la matriz inicial del problema
    # ======================================================================================
    mensaje_matriz_incial = "\n----------------------------------------------------\n" \
                            + "Matriz Inicial: \n" \
                            + "----------------------------------------------------\n" \
                            + creacion_de_matriz_en_string(matriz_anterior) \
                            + "----------------------------------------------------\n" \
                            + "Respuesta Parcial:  " \
                            + retornar_resultados_solucion_optima(matriz_anterior, indice_optimizacion) \
                            + "\n----------------------------------------------------\n" \
                            + "\n\n"
    # ======================================================================================
    # Se escribe la matriz en el archivo
    # ======================================================================================
    escritura_en_archivo(nombre_archivo, mensaje_matriz_incial)

    # ======================================================================================
    # Declaracion de variables
    # ======================================================================================
    nueva_matriz = []
    iteracion = 0

    # ======================================================================================
    # Se establece el minimo numero y el signo menor de la tabla o matriz
    # ======================================================================================
    signo_mas_menor, numero_menor = establecer_minimo(matriz_anterior[1][2:], opcion)

    # ======================================================================================
    # En el caso que en la solucion U haya un numero menor se recorrara de manera que llegue
    # a haber ningun menor
    # ======================================================================================
    while (signo_mas_menor < 0):

        # ======================================================================================
        # Se almacena la solucion aumentada
        # ======================================================================================
        solucion_aumentada = retornar_resultados_solucion_optima(matriz_anterior, indice_optimizacion)

        # ======================================================================================
        # Se incrementa la iteracion
        # ======================================================================================
        iteracion = iteracion + 1

        # ======================================================================================
        # La U menor de la solucion sera el numero menor
        # ======================================================================================
        U_menor = numero_menor

        # ======================================================================================
        # La columna pivote sera en el indice donde esta la U menor
        # ======================================================================================
        numero_columna_pivote = matriz_anterior[1].index(U_menor)

        # ======================================================================================
        # Resultados sera las iteraciones respectivas
        # ======================================================================================
        resultados = realizar_iteraciones(nombre_archivo, matriz_anterior, U_menor, numero_columna_pivote)
        nueva_matriz = resultados[0]

        # ======================================================================================
        # En el caso que NO SEA ACOTADA, ya que matriz estara vacia
        # ======================================================================================
        if (nueva_matriz == []):
            solucion_no_acorada_mensaje = "Solucion NO acotada"
            # ======================================================================================
            # Se escribe en el archivo dicho mensaje y se imprime
            # ======================================================================================
            escritura_en_archivo(nombre_archivo, solucion_no_acorada_mensaje)
            print("Solucion NO acotada")
            quit()

        # ======================================================================================
        # Se establece que la matriz anterior sea la nueva matriz a manejar
        # ======================================================================================
        matriz_anterior = nueva_matriz

        # ======================================================================================
        # Impresion de la iteracion en el archivo
        # ======================================================================================
        nueva_matriz_impresion = "\n---------------------------------------------------------------------------\n" \
                                 + "Iteración " + str(iteracion) + "\n" \
                                 + "---------------------------------------------------------------------------\n" \
                                 + creacion_de_matriz_en_string(matriz_anterior) + "\n" \
                                 + "---------------------------------------------------------------------------\n" \
                                 + "Respuesta Parcial:  " \
                                 + retornar_resultados_solucion_optima(matriz_anterior, indice_optimizacion) \
                                 + "\n" + resultados[1] + "\n"

        # ======================================================================================
        # Se escribe en el archivo
        # ======================================================================================
        escritura_en_archivo(nombre_archivo, nueva_matriz_impresion)

        # ======================================================================================
        # Nuevamente se establece el minimo del signo y el numero respectivo
        # ======================================================================================
        signo_mas_menor, numero_menor = establecer_minimo(matriz_anterior[1][2:], opcion)

    # ======================================================================================
    # Se recorre dicha solucion para saber si es multiple o no
    # ======================================================================================
    validacion_solucion_multiple(nombre_archivo, numero_variables, indice_optimizacion, matriz_anterior, nueva_matriz)

    # ======================================================================================
    # El resultado final de la matriz
    # ======================================================================================
    matriz_resultante = "\n---------------------------------------------------------------------------\n" \
                        + "\nMatriz Final Resultante\n" + creacion_de_matriz_en_string(matriz_anterior) + "\n"

    # ======================================================================================
    # Se escribe en el archivo
    # ======================================================================================
    escritura_en_archivo(nombre_archivo, matriz_resultante)

    # ======================================================================================
    # Se valida si todas las "X" son >=0
    # ======================================================================================
    if (not (validar_solucion_no_factible(matriz_anterior))):
        no_factible_mensaje = "Problema no factible"
        escritura_en_archivo(nombre_archivo, no_factible_mensaje)
        print("Problema no factible")

    # ======================================================================================
    # Se imprime en la terminal y el archivo la solucion optima
    # ======================================================================================
    solucion_aumentada = retornar_resultados_solucion_optima(nueva_matriz, indice_optimizacion)
    solucion_optima_mensaje = "---------------------------------------------------------------------------\n" \
                              + "Resultado Optimo:  " + solucion_aumentada
    escritura_en_archivo(nombre_archivo, solucion_optima_mensaje)
    print(solucion_optima_mensaje)


# ======================================================================================
# Validar que la solucion sea multiple
# ======================================================================================
def validacion_solucion_multiple(nombre_archivo, numero_variables, indice_optimizacion, matriz_anterior, nueva_matriz):
    # ======================================================================================
    # En el caso que la matriz anterior se vean variables multiples
    # ======================================================================================
    if (matriz_anterior[1][2 + numero_variables:-1].count(0) > 0):

        # ======================================================================================
        # Se retornar el parseador de los resultados de la solucion
        # ======================================================================================
        solucion_aumentada = retornar_resultados_solucion_optima(matriz_anterior, indice_optimizacion)

        # ======================================================================================
        # Se establece la holgura como el indice de la matriz segun las cantidad de variables
        # ======================================================================================
        holgura = matriz_anterior[1][2 + numero_variables:-1].index(0)

        # ======================================================================================
        # Se retornar el parseador de los resultados de la solucion
        # ======================================================================================
        indice = holgura + 2 + numero_variables

        # ======================================================================================
        # Se extrae la columna para comparar dicha columna para saber si tiene solucion multiple
        # ======================================================================================
        columna_de_holgura = extraccion_columna(indice, matriz_anterior)

        # ======================================================================================
        # Se define la cantidad inicial de la columna
        # ======================================================================================
        cantidad_inicial = columna_de_holgura.count(0)

        cantidad = columna_de_holgura.count(1)

        # ======================================================================================
        # Se establece el total de la cantidad
        # ======================================================================================
        total_de_cantidad = cantidad_inicial + cantidad + 1

        # ======================================================================================
        # En el caso que el largo de la columna sea mas grande que el total hay mas de una solucion
        # ======================================================================================
        if (total_de_cantidad < len(columna_de_holgura)):
            # ======================================================================================
            # Se da el mensaje que el solucion multiple retornando de una vez los resultados
            # ======================================================================================
            solucion_aumentada = retornar_resultados_solucion_optima(nueva_matriz, indice_optimizacion)
            print("Problema Digitado es de solucion multiple")
            print(creacion_de_matriz_en_string(nueva_matriz))
            print("Respuesta Final:  ", solucion_aumentada)

            # ======================================================================================
            # Se realizan las iteraciones
            # ======================================================================================
            resultados = realizar_iteraciones(nombre_archivo, matriz_anterior, 0, indice)
            nueva_matriz = resultados[0]

            # ======================================================================================
            # Se parsea el mensaje para el usuario en el archivo
            # ======================================================================================
            solucion_multiple_mensaje = "Solucion multiple del problema por lo cual se finaliza el problema\n" + "Estado Final " + " \n" \
                                        + creacion_de_matriz_en_string(matriz_anterior) + "\nRespuesta Final:  " \
                                        + retornar_resultados_solucion_optima(matriz_anterior,
                                                                              indice_optimizacion) + "\n" + \
                                        resultados[1] + "\n"

            # ======================================================================================
            # Se escribe dicha solucion en el archivo
            # ======================================================================================
            escritura_en_archivo(nombre_archivo, solucion_multiple_mensaje)

        matriz_anterior = nueva_matriz


# ======================================================================================
# Se crea la martriz inicial
# ======================================================================================
def crear_matriz_inicial(numero_variables, numero_restricciones,
                         funcion_objetivo_inicial, total_restricciones_lista, indice_optimizacion):
    # ======================================================================================
    # Se crea primero el encabezado
    # ======================================================================================
    matriz_inicio = [creacion_del_encabezado(numero_variables, numero_restricciones)]

    # ======================================================================================
    # Se establece y determina el longitud encabezado
    # ======================================================================================
    longitud_del_encabezado = len(matriz_inicio[0])

    # ======================================================================================
    # En el caso sea un problema de maximizacion
    # ======================================================================================
    if (indice_optimizacion == "max"):
        lista_temportal_matriz = [0, "U"] + funcion_objetivo_inicial

    # ======================================================================================
    # En el caso sea un problema de minimizacion
    # ======================================================================================
    else:
        lista_temportal_matriz = [0, "-U"] + funcion_objetivo_inicial

    # ======================================================================================
    # Se iguala la funcion objetivo a 0
    # ======================================================================================
    for u in range(len(lista_temportal_matriz), longitud_del_encabezado):
        lista_temportal_matriz.append(0)

    # ======================================================================================
    # Se agrega a la matriz inicio la lista de una matriz temporal
    # ======================================================================================
    matriz_inicio.append(lista_temportal_matriz)

    # ======================================================================================
    # Se ignora el U por el 1, para recorrer el numero de restricciones
    # ======================================================================================
    for i in range(1, numero_restricciones + 1):
        lista_temportal_matriz = [i, "Y" + str(i)]

        # ======================================================================================
        # Se recorren las variables
        # ======================================================================================
        for n in range(numero_variables):
            # ======================================================================================
            # Agrega las restricciones menos el valor de LD
            # ======================================================================================
            lista_temportal_matriz = lista_temportal_matriz + [total_restricciones_lista[i - 1][n]]
        for j in range(1, numero_restricciones + 1):
            lista_temportal_matriz = lista_temportal_matriz + [0]
        # ======================================================================================
        # Agrega el valor LD a la tabla
        # ======================================================================================
        lista_temportal_matriz = lista_temportal_matriz + [total_restricciones_lista[i - 1][-1]]
        matriz_inicio.append(lista_temportal_matriz)

        # ======================================================================================
        # Agrega el valor de las variables de holgura
        # ======================================================================================
        matriz_inicio[i + 1][2 + numero_variables + i - 1] = 1
    return matriz_inicio


# ======================================================================================
# Se crea la martriz inicial
# ======================================================================================
def retornar_resultados_solucion_optima(matriz_actual, indice_optimizacion):
    u = matriz_actual[1][-1]
    contenido_solucion_aumentada = ""
    solucion_aumentada = ""

    # ======================================================================================
    # De la matriz actual se tomando el inicio
    # ======================================================================================
    for x in matriz_actual[0][2:-1]:
        # ======================================================================================
        # Se realiza un resultado determinado para la solucion optima
        # ======================================================================================
        resultado_predetermiado = "0"

        # ======================================================================================
        # Se recorre el largo de la matriz actual
        # ======================================================================================
        for i in range(1, len(matriz_actual)):

            # ======================================================================================
            # Si es el caso que el indice cuadre con la X sera parte de la solucion optima
            # ======================================================================================
            if (matriz_actual[i][1] == x):
                # ======================================================================================
                # Se cambia el resultado predeterminado a un string
                # ======================================================================================
                resultado_predetermiado = str(matriz_actual[i][-1])

        # ======================================================================================
        # Se crea el contenido de la solcion aumentada
        # ======================================================================================
        contenido_solucion_aumentada = contenido_solucion_aumentada + resultado_predetermiado + ", "

    contenido_solucion_aumentada = contenido_solucion_aumentada[:-1]
    # ======================================================================================
    # Hacer el mensaje de la solcion optima en caso de ser max o min
    # ======================================================================================
    if (indice_optimizacion == "max"):
        solucion_aumentada = "U = " + str(u) + " (" + contenido_solucion_aumentada + ")"
    else:
        solucion_aumentada = "-U = " + str(u) + " (" + contenido_solucion_aumentada + ")"

    return solucion_aumentada


# ======================================================================================
# Se realiza las iteraciones del metodo simplex
# ======================================================================================
def realizar_iteraciones(nombre_archivo, matriz_anterior, U_menor, numero_columna_pivote):
    # ======================================================================================
    # Se establece la columna pivote
    # ======================================================================================
    columna_pivote = extraccion_columna(numero_columna_pivote, matriz_anterior[1:])

    # ======================================================================================
    # Se extra la columna de los valores LD
    # ======================================================================================
    columna_LD = extraccion_columna(len(matriz_anterior[0]) - 1, matriz_anterior[1:])

    mensaje_opcional = ""
    if not sys.warnoptions:  # Ignora advertencia de warning por los resultados inf
        warnings.simplefilter("ignore")

    # ======================================================================================
    # Se dividen los valores de LD entre las que estan en los pivotes sacados de la columna pivote
    # ======================================================================================
    division_inicial = np.array(columna_LD[1:]) / np.array(columna_pivote[1:])

    # ======================================================================================
    # Validaciones varias sobre la iteracion
    # ======================================================================================
    # ======================================================================================
    # Se valida si el problema es acotado
    # ======================================================================================
    if (validar_acotacion(division_inicial)):
        return [[], ""]
    # ======================================================================================
    # Se valida si el problema es degenerado
    # ======================================================================================
    if (validar_degradacion(matriz_anterior[1][2:], division_inicial)):
        # ======================================================================================
        # Se retorna el mensaje en el archivo y se imprime en terminal
        # ======================================================================================
        mensaje = "La solucion es degenerada"
        escritura_en_archivo(nombre_archivo, mensaje)
        print(mensaje)
        print(creacion_de_matriz_en_string(matriz_anterior))
    # ======================================================================================
    # Se establece el resultado minimo de la columna LD para establecer la fila pivote
    # ======================================================================================
    menor_resultado_columna_LD = minimo_resultado_positivo(division_inicial)

    # ======================================================================================
    # Establecer el indice de la fila pivote con ayuda la division inicial con el menor
    # resultado de la columna LD
    # ======================================================================================
    indice_pivote_fila = np.where(division_inicial == menor_resultado_columna_LD)[0][0] + 2

    # ======================================================================================
    # Se establece toda la fila pivote segun el indice pivote fila
    # ======================================================================================
    fila_pivote = matriz_anterior[indice_pivote_fila][2:]

    # ======================================================================================
    # Se establece el numero especifico del pivote con ayuda del pivote y la columna
    # ======================================================================================
    numero_para_pivote = matriz_anterior[indice_pivote_fila][numero_columna_pivote]

    # ======================================================================================
    # La matriz anterior es la nueva
    # ======================================================================================
    nueva_matriz = matriz_anterior

    # ======================================================================================
    # Se establece la variable que entra
    # ======================================================================================
    variable_que_entra = matriz_anterior[0][numero_columna_pivote]

    # ======================================================================================
    # Se establece la variable que sale
    # ======================================================================================
    variable_que_sale = matriz_anterior[indice_pivote_fila][1]

    # ======================================================================================
    # Cambio de la columna de VB
    # ======================================================================================
    nueva_matriz[indice_pivote_fila][1] = matriz_anterior[0][numero_columna_pivote]

    # ======================================================================================
    # la nueva fila se calcula la nueva fila resultante
    # ======================================================================================
    nueva_fila = calcular_fila_nueva(fila_pivote, numero_para_pivote)

    # ======================================================================================
    # En la matriz nueva con el indice del pivote sera igual que la nueva fila
    # ======================================================================================
    nueva_matriz[indice_pivote_fila][2:] = nueva_fila

    # ======================================================================================
    # En la nueva matriz se establece columna de pivote nueva
    # ======================================================================================
    nueva_matriz = columna_pivote_nueva(columna_pivote, nueva_fila, nueva_matriz, indice_pivote_fila)

    # ======================================================================================
    # Se parsea el mensaje de informacion relevante que contendra la variable que entra, la
    # que sale y el numero del pivote
    # ======================================================================================
    impresion_informacion_relevante = "\n---------------------------Información Relevante---------------------------\n" \
                                      "Variable Básica que entra: " + variable_que_entra + "\n" \
                                      + "---------------------------------------------------------------------------\n" \
                                      + "Variable Básica que sale: " + variable_que_sale + "\n" \
                                      + "---------------------------------------------------------------------------\n" \
                                      + "El número del Pivote: " + str(numero_para_pivote) \
                                      + mensaje_opcional + "\n" \
                                      + "---------------------------FINAL DE LA ITERACIÓN---------------------------\n"

    return [nueva_matriz, impresion_informacion_relevante]


# ======================================================================================
# Validar las iteraciones en el caso que sea degradada y acotada
# ======================================================================================
def validaciones_por_iteraciones(division_inicial, matriz_anterior):
    # ======================================================================================
    # Se valida si el problema es acotado
    # ======================================================================================
    if (validar_acotacion(division_inicial)):
        return [[], ""]
    # ======================================================================================
    # Se valida si el problema es degenerado
    # ======================================================================================
    if (validar_degradacion(matriz_anterior[1][2:], division_inicial)):
        # ======================================================================================
        # Se retorna el mensaje en el archivo y se imprime en terminal
        # ======================================================================================
        mensaje = "La solucion es degenerada"
        escritura_en_archivo(nombre_archivo, mensaje)
        print(mensaje)
        print(creacion_de_matriz_en_string(matriz_anterior))


# ======================================================================================
# Funcion que calcula una fila nueva para la iteracion
# ======================================================================================
def calcular_fila_nueva(fila_pivote, numero_para_pivote):
    contenedor = []

    # ======================================================================================
    # Se recorre la fila pivote
    # ======================================================================================
    for indice in fila_pivote:

        # ======================================================================================
        # Si el residuo del indice y el numero pivote es 0 entonces se divide el indice y el pivote
        # ======================================================================================
        if (indice % numero_para_pivote == 0):
            contenedor.append(int(indice / numero_para_pivote))

        # ======================================================================================
        # Se determina la cantidad de decimales a usar para el calculo de las nuevas filas
        # ======================================================================================
        elif (definir_decimales(indice / numero_para_pivote) > 4):
            contenedor.append(float("{0:.4f}".format((indice / numero_para_pivote))))
        else:
            contenedor.append(indice / numero_para_pivote)
    return contenedor

# ======================================================================================
# Se definen los decimales
# ======================================================================================
def definir_decimales(numero):

    # ======================================================================================
    # Dado el largo del numero
    # ======================================================================================
    largo_numero = len(str(numero))

    # ======================================================================================
    # Se determina la cantidad de digitos antes del .
    # ======================================================================================
    indice = str(numero).index(".")

    # ======================================================================================
    # Se resta la diferencia
    # ======================================================================================
    resultado = largo_numero - (indice + 1)
    return resultado

# ======================================================================================
# Se establece la nueva columna que va a ser de pivote con ayuda de un minimo
# ======================================================================================
def columna_pivote_nueva(columna_pivote, nueva_fila, nueva_matriz, indice_pivote_fila):

    # ======================================================================================
    # La matriz resultante sera una nueva matriz inicial
    # ======================================================================================
    matriz_resultante = [nueva_matriz[0]]

    # ======================================================================================
    # Se recorre la matriz sin tomar en cuenta columnas innecesarias
    # ======================================================================================
    for i in range(1, len(nueva_matriz)):
        matriz_temporal = nueva_matriz[i][:2]

        # ======================================================================================
        # A partir de la columna determinada del largo de la nueva matriz sera recorrida
        # ======================================================================================
        for j in range(2, len(nueva_matriz[i])):

            # ======================================================================================
            # Si el indice no encaja ni con la columna pivote o fila pivote a con un nuevo calculo
            # ======================================================================================
            if ((columna_pivote[i - 1] != 0) and (i != indice_pivote_fila)):

                # ======================================================================================
                # Resultado sera una nueva matriz menos la columna menos el encabezado y las filas menos
                # las 2 filas de relleno que tiene
                # ======================================================================================
                resultado = nueva_matriz[i][j] - (columna_pivote[i - 1] * nueva_fila[j - 2])
                if (resultado % 1 == 0 or type(resultado) == Add or type(resultado) == Symbol):
                    # ======================================================================================
                    # Se establece resultado
                    # ======================================================================================
                    resultado = resultado
                # ======================================================================================
                # Se definen los decimales a usar al tener en cuenta este calculo
                # ======================================================================================
                elif (definir_decimales(resultado) > 4):
                    resultado = float("{0:.4f}".format(resultado))
                matriz_temporal.append(resultado)
            else:
                matriz_temporal = (nueva_matriz[i])
        # ======================================================================================
        # Se agrega la matriz temporar a la matriz resultante
        # ======================================================================================
        matriz_resultante.append(matriz_temporal)
    return matriz_resultante

# ======================================================================================
# SSe establece el minimo resultado
# ======================================================================================
def minimo_resultado_positivo(lista):
    # ======================================================================================
    # Se determina el largo de la lista
    # ======================================================================================
    largo_de_la_lista = len(lista)

    # ======================================================================================
    # Se recorre la lista ingresada
    # ======================================================================================
    for numero in range(largo_de_la_lista):
        if (lista[numero] < 0):
            lista[numero] = 777

    # ======================================================================================
    # El minimo de la lista recorrida
    # ======================================================================================
    temporal = min(lista)
    return temporal

# ======================================================================================
# Se valida si la solucion es degradada
# ======================================================================================
def validar_degradacion(lista_de_valores_U, resultados_en_LD):

    resultados = np.unique(resultados_en_LD)

    # ======================================================================================
    # Se recorren los valores de la lista de U
    # ======================================================================================
    for valores in (lista_de_valores_U):
        if ((lista_de_valores_U.count(valores) > 1) and (valores != 0)):
            return True

    # ======================================================================================
    # En el caso que los resultados no sean iguales a los resultados de LD no es degradada
    # ======================================================================================
    if (len(resultados) != len(resultados_en_LD)):
        return True

    # ======================================================================================
    # En el caso que los resultados sean iguales a los resultados de LD no es degradada
    # ======================================================================================
    if (len(resultados) == len(resultados_en_LD)):
        return False

# ======================================================================================
# Validar si la solucion es acotada o no
# ======================================================================================
def validar_acotacion(resultados_en_LD):
    resultado_booleano = True
    # ======================================================================================
    # Se recorre los resultados LD
    # ======================================================================================
    for n in  (resultados_en_LD):
        if ((n >= 0) and (n != np.inf) and (n != -np.inf) ):
            resultado_booleano = False
    return resultado_booleano


# ======================================================================================
# Validar si la solucion es factible o no
# ======================================================================================
def validar_solucion_no_factible(matriz):

    # ======================================================================================
    # Se recorre el largo de la matriz para saber si el resultado que tiene sean validos
    # ======================================================================================
    for i in range(1, len(matriz)):
        if (matriz[i][1][0] == "X"):
            if (matriz[i][-1] <= 0):
                return False
            else:
                return True

    # ======================================================================================
    # Dado el largo se determina si que atraves de la evaualcion numerica dicha solucion es
    # factible o no
    # ======================================================================================
    for j in range(1, len(matriz)):
        if (matriz[j][1][0] == "R"):
            if (type(matriz[j][-1]) == Add):
                # ======================================================================================
                # Podemos convertir una expresión SymPy en una expresión que se pueda evaluar
                # numéricamente. lambdify actúa como una función lambda
                # ======================================================================================
                evaluacion_numerica = lambdify(matriz[j][-1])
                resultado = evaluacion_numerica(777)
                if (resultado > 0):
                    return False
                if (resultado <= 0):
                    return True
            else:
                if (matriz[j][-1] > 0):
                    return False
    return True

# ======================================================================================
# Se establece el minido dado los valores de U respectivamente
# ======================================================================================
def establecer_minimo(todos_los_valores_U, opcion):

    lista_temporal = []
    resultados = []

    if (opcion == 0):
        # ======================================================================================
        # Se copian los valores de U en la lista temporal
        # ======================================================================================
        lista_temporal = todos_los_valores_U.copy()

        # ======================================================================================
        # Se establece la lista temporal dado el largo de dichos valores
        # ======================================================================================
        lista_temporal = lista_temporal[0:len(todos_los_valores_U) - 1]

        # ======================================================================================
        # Se recorre la lista temporal
        # ======================================================================================
        for i in range(len(lista_temporal)):
            if (type(lista_temporal[i]) == Add):

                # ======================================================================================
                # Podemos convertir una expresión SymPy en una expresión que se pueda evaluar
                # numéricamente. lambdify actúa como una función lambda
                # ======================================================================================
                evaluacion_numerica = lambdify(lista_temporal[i])
                resultados += [evaluacion_numerica()]
            else:
                resultados += lista_temporal[i]

        # ======================================================================================
        # Se recorre los resultados y se retornan los minimos de los valores
        # ======================================================================================
        for j in range(len(resultados)):
            if (resultados[j] == min(resultados)):
                return min(resultados), todos_los_valores_U[j]
        return 0, 0
    return min(todos_los_valores_U), min(todos_los_valores_U)


