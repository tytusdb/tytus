from tkinter import messagebox

funciones_extra = ""

class GeneradorFileC3D:
    def __init__(self):
        self.path_archivo_c3d = '../interfaz/c3d.py'
        self._crea_archivo_c3d()

    def _crea_archivo_c3d(self):
        with open(self.path_archivo_c3d, 'w') as file_c3d:
            "Creo el archivo en tu computadora si aun no lo tienes"

    def escribir_archivo(self, c3d):
        global funciones_extra
        imports = '''
#Imports
from goto import with_goto
from Analisis_Ascendente.storageManager.jsonMode import *
import Analisis_Ascendente.ascendente as parser
'''
        variables_globales = '''
#Variables Globales
salida = ''
stack = [None] * 1000
top_stack = -1

'''
        funcion_intermedia = '''
@with_goto
def funcion_intermedia():
    global salida
    global stack
    global top_stack
    t1 = top_stack
    top_stack = top_stack - 1
    texto_parser = stack[t1]
    parser.ejecutarAnalisis(texto_parser)
    t1 = parser.consola
    tamanio_consola = len(t1)
    contador = 0

    label .inicio_agregar_texto_consola
    if contador < tamanio_consola: goto .agregar_texto_consola
    goto .fin_agregar_texto_consola

    label .agregar_texto_consola
    t1 = parser.consola
    t2 = t1[contador]
    salida = salida + t2
    salida = salida + '\\n'
    contador = contador + 1
    goto .inicio_agregar_texto_consola

    label .fin_agregar_texto_consola
    
    
'''
        inicio_main = '''
@with_goto
def main():
    global salida, stack, top_stack
'''

        fin_main = '''
# ----------FIN C3D---------------
    reportes = parser.RealizarReportes()
    t1 = parser.L_errores_lexicos
    reportes.generar_reporte_lexicos(t1)
    t2 = parser.L_errores_sintacticos
    reportes.generar_reporte_sintactico(t2)
    t3 = parser.ts_global
    t4 = t3.simbolos
    reportes.generar_reporte_tablaSimbolos(t4)
    t5 = parser.exceptions
    reportes.generar_reporte_semanticos(t5)
    dropAll()
    print("---------------------------------------------------------")
    print("------------------------SALIDA C3D-----------------------")
    print("------------------------SALIDA C3D-----------------------")
    print("---------------------------------------------------------")
    print(salida)


if __name__ == "__main__":
    main()
'''
        try:
            with open(self.path_archivo_c3d, 'w') as file_c3d:
                file_c3d.write(imports)
                file_c3d.write(variables_globales)
                file_c3d.write(funcion_intermedia)
                file_c3d.write(funciones_extra)
                file_c3d.write(inicio_main)
                file_c3d.write(c3d)
                file_c3d.write(fin_main)

        except Exception as er:
            messagebox.showwarning(er, "No existe archivo para guardar la informacion")


