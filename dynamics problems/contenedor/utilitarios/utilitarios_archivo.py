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

# ======================================================================================
# Funcion imprime el contenido del archivo ingresado
# Entradas: nombre_archivo
# Salidas: Nada
# ======================================================================================
def contenido_archivo(nombre_archivo):
    with open(nombre_archivo, "r") as archivo:
        for linea in archivo:
            print(linea)
# ======================================================================================
# Funcion convierte de texto a numeros legibles para realizar el problema de la mochila
# Entradas: valores_lista
# Salidas: lista_resultante
# ======================================================================================
def conversion_a_numeros(valores_lista):
    bandera = False
    lista_resultante = []
    # ======================================================================================
    # Se recorren los valores dada la lista de valores
    # ======================================================================================
    for valor in valores_lista:
        # ======================================================================================
        # Dado un numero la bandera sera true para que sirva en las condicionales posteriores
        # ======================================================================================
        for numero in valor:
            if (numero == '.'):
                bandera = True
                break
        # ======================================================================================
        # En el caso que sea flotante
        # ======================================================================================
        if (bandera == True):
            lista_resultante.append(int(round(float(valor))))
            bandera = False
        # ======================================================================================
        # Entero
        # ======================================================================================
        else:
            lista_resultante.append(int(valor))
    return lista_resultante
# ======================================================================================
# Funcion lee el archivo dado como parametros en el comando a ingresar
# Entradas: valores_lista
# Salidas: lista_resultante
# ======================================================================================
def leer_achivo(nombre_achivo):
    matriz_inicial = []
    contador = 1
    capacidad_mochila = 0
    # ======================================================================================
    # Se abre el archivo
    # ======================================================================================
    with open(nombre_achivo) as archivo:
        # ======================================================================================
        # Se recorre todas las lineas
        # ======================================================================================
        for linea in archivo:
            if contador == 1:
                capacidad_mochila = int(linea)
                contador += 1
            else:
                # ======================================================================================
                # Se realiza la conversion de la lista de caracteres a una lista de numeros
                # ======================================================================================
                linea = linea.rsplit()
                linea[0] = str(contador-1) + ',' + linea[0]
                lista = linea[0].split(',')
                lista = conversion_a_numeros(lista)
                matriz_inicial.append(lista)
                contador += 1
    return matriz_inicial, capacidad_mochila