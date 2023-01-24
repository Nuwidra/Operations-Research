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
# Proyecto 1: SIMPLEX Y DOS FASES                   |   
#                                                   |
# ==================================================|
from sympy import *
import sys
from sympy import *

from dos_fases.dos_fases import *
from simplex_simple.simplex_simple import *
from utilitarios import *

# ======================================================================================
# Esta funcion se encargara de a partir del metodo ingresado se decide que procedimiento
# realizar, puede ser simplex simple o dos fases
# ======================================================================================
def seleccionar_metodo(nombre_archivo, lista_contenido, opcion, indice_optimizacion, numero_variables, numero_restricciones, total_restricciones_lista, total_igualdades_lista):

    # ======================================================================================
    # Se recorren las restricciones del archivo de entrada del archivo.txt
    # ======================================================================================
    recorrer_restricciones(numero_variables, total_restricciones_lista, total_igualdades_lista)

    # ======================================================================================
    # En el caso que opcion sea 1, se ejecutar el metodo simplex simple
    # ======================================================================================
    if (opcion == 1):
        # ======================================================================================
        # Se valida si la entrada cumple con el formato de simplex
        # ======================================================================================
        if (validar_simplex(lista_contenido[2:], numero_variables)):

            # ======================================================================================
            # Se elimina los simbolos de las restricciones para el manejo de los numeros
            # ======================================================================================
            total_restricciones_lista, comparaciones  = eliminar_restricciones(numero_variables, lista_contenido[2:])

            # ======================================================================================
            # En el caso que sea un problema de maximizacion
            # ======================================================================================
            if (indice_optimizacion == "max"):
                print("============")
                print("Maximización")
                print("============")
                # ======================================================================================
                # Se ejecuta simplex
                # ======================================================================================
                return simplex(nombre_archivo, opcion, indice_optimizacion, numero_variables, numero_restricciones, 
                                    conversor_lista_a_numeros(lista_contenido[1]),
                                    total_restricciones_lista)

            # ======================================================================================
            # En el caso que sea un problema de minimizacion
            # ======================================================================================
            elif (indice_optimizacion == "min"):
                print("============")
                print("Minimización")
                print("============")

                # ======================================================================================
                # Se convierten lo obtenido del la lista a transformarlo en numeros
                # ======================================================================================
                funcion_objetivo_inicial = conversor_lista_a_numeros(lista_contenido[1])

                # ======================================================================================
                # Se declara contenedor para la funcion objetivo
                # ======================================================================================
                contenedor_funcion_objetivo = []

                # ======================================================================================
                # La funcion objetivo inicial se debe de igualar a 0
                # ======================================================================================
                for parametros in funcion_objetivo_inicial:  
                    contenedor_funcion_objetivo.append(parametros * -1)

                # ======================================================================================
                # Se ejecuta simplex
                # ======================================================================================
                return simplex(nombre_archivo, opcion, indice_optimizacion, numero_variables, numero_restricciones, 
                                    contenedor_funcion_objetivo,
                                    total_restricciones_lista)
            else:
                # ======================================================================================
                # En el caso que el usuario dijite algo que no sea max o min
                # ======================================================================================
                print("Las opciones válidas son 'max' o 'min' nada mas")

    elif (opcion == 2):

        # ======================================================================================
        # Se elimina los simbolos de las restricciones para el manejo de los numeros
        # ======================================================================================
        total_restricciones_lista, comparaciones  = eliminar_restricciones(numero_variables, lista_contenido[2:])

        # ======================================================================================
        # En el caso que sea un problema de maximizacion
        # ======================================================================================
        if (indice_optimizacion == "max"):
            print("============")
            print("Maximización")
            print("============")
            total_restricciones_lista = invertirmenorigual(total_restricciones_lista, comparaciones)
            # ======================================================================================
            # Se ejecuta simplex
            # ======================================================================================
            return simplex_dos_fases(nombre_archivo, opcion, indice_optimizacion, numero_variables, numero_restricciones,
                                conversor_lista_a_numeros(lista_contenido[1]),
                                total_restricciones_lista)

        # ======================================================================================
        # En el caso que sea un problema de minimizacion
        # ======================================================================================
        elif (indice_optimizacion == "min"):
            print("============")
            print("Minimización")
            print("============")

            # ======================================================================================
            # Se convierten lo obtenido del la lista a transformarlo en numeros
            # ======================================================================================
            funcion_objetivo_inicial = conversor_lista_a_numeros(lista_contenido[1])

            # ======================================================================================
            # Se declara contenedor para la funcion objetivo
            # ======================================================================================
            contenedor_funcion_objetivo = []

            # ======================================================================================
            # La funcion objetivo inicial se debe de igualar a 0
            # ======================================================================================
            for parametros in funcion_objetivo_inicial:
                contenedor_funcion_objetivo.append(parametros * -1)

            total_restricciones_lista = invertirmenorigual(total_restricciones_lista, comparaciones)
            # ======================================================================================
            # Se ejecuta simplex
            # ======================================================================================
            return simplex_dos_fases(nombre_archivo, opcion, indice_optimizacion, numero_variables, numero_restricciones,
                                contenedor_funcion_objetivo,
                                total_restricciones_lista)
        else:
            # ======================================================================================
            # En el caso que el usuario dijite algo que no sea max o min
            # ======================================================================================
            print("Las opciones válidas son 'max' o 'min' nada mas")


# ======================================================================================
# Mensaje de ayuda para el usuario
# ======================================================================================
def mensaje_de_ayuda_de_uso():
    mensaje = " =====================================================\n" \
           + "|    ______  ____           ___    ____   ___   ___   |\n" \
           + "|   /_  __/ / __ \         |__ \  / __ \ |__ \ |__ \  |\n" \
           + "|    / /   / / / /  _____  __/ / / / / / __/ / __/ /  |\n" \
           + "|  _/ /_  / /_/ /  /____/ / __/ / /_/ / / __/ / __/   |\n" \
           + "| /____/  \____/         /____/ \____/ /____//____/   |\n" \
           + "|=====================================================|\n" \
           + "|Parece que ocupas ayuda, sigue estos pasos:          |\n" \
           + "|Tienes que ingresar el siguiente comando en terminal |\n" \
           + "| * python simplex.py -h nombre_archivo.txt           |\n" \
           + "|=====================================================|\n" \
           + "|Para el archivo de entrada debe de ir en este formato|\n" \
           + "|0,max,2,3                                            |\n" \
           + "|3,5                                                  |\n" \
           + "|2,1,<=,6                                             |\n" \
           + "|-1,3,<=,9                                            |\n" \
           + "|0,1,<=,4                                             |\n" \
           + "|=====================================================|\n" \
           + "|Donde los parametros son en este formato:            |\n" \
           + "|Método, optimización, número de variables de         |\n" \
           + "|decisión, número de restricciones                    |\n" \
           + "|Donde optimización puede ser: min o max              |\n" \
           + "|Coeficientes de la función objetivo                  |\n" \
           + "|Coeficientes de las restricciones                    |\n" \
           + "|Opciones de método: 0 = Simplex, 1 = DosFases        |\n" \
           + " =====================================================\n" \

    print(mensaje)

# ======================================================================================
# Determinar el uso de los parametros ingresados
# ======================================================================================
def parametros_ingresados(args):
    global nombre_archivo

    # ======================================================================================
    # En el caso que exista -h y el nombre del archivo en la linea de comando ingresada
    # ======================================================================================
    if len(args) == 3 and args[1] == "-h":
        mensaje_de_ayuda_de_uso()
        nombre_archivo = args[2]
        lista_contenido, metodo, optimizacion, numero_variables, numero_restricciones, total_restricciones_lista, listaIgualdades = leer_achivo(nombre_archivo)
        seleccionar_metodo(nombre_archivo, lista_contenido, metodo, optimizacion, numero_variables, numero_restricciones, total_restricciones_lista,
                           listaIgualdades)
    # ======================================================================================
    # En el caso que solo ingrese -h en la linea de comando ingresada
    # ======================================================================================
    elif len(args) == 2:
        if args[1] == "-h":
            mensaje_de_ayuda_de_uso()
        else:
            nombre_archivo = args[1]
            lista_contenido, metodo, optimizacion, numero_variables, numero_restricciones, total_restricciones_lista, listaIgualdades = leer_achivo(nombre_archivo)
            seleccionar_metodo(nombre_archivo, lista_contenido, metodo, optimizacion, numero_variables, numero_restricciones, total_restricciones_lista, listaIgualdades)
    else:
        # ======================================================================================
        # Mensaje de sugerencia
        # ======================================================================================
        print("\nIngresar -h para una ayudita \n")


parametros_ingresados(sys.argv)
