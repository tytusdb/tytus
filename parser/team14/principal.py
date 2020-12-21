import arbol.AST as a
import gramatica2 as g
import os
from tkinter import *
from reportes import *
from subprocess import check_call
from Entorno.Entorno import Entorno
from storageManager import jsonMode
from Expresion.variablesestaticas import variables

#variables.ventana = Tk()
variables.ventana.geometry("1000x600")
variables.ventana.resizable(False, False)
variables.ventana.config(background="gray25")


def reporte_lex_sin():
    if len(reporteerrores) != 0:
        contenido = "Digraph  reporte{label=\"REPORTE ERRORES LEXICOS Y SINTACTICOS\"\n"
        contenido += "node [shape=record,style=rounded,color=\"#4b8dc5\"];\n"
        contenido += "arset [label=<\n<TABLE border= \"2\"  cellspacing= \"-1\" color=\"#4b8dc5\">\n"
        contenido += "<TR>\n<TD bgcolor=\"#1ED0EC\">Tipo</TD>\n<TD bgcolor=\"#1ED0EC\">Linea</TD>\n"
        contenido += "<TD bgcolor=\"#1ED0EC\">Columna</TD>\n<TD bgcolor=\"#1ED0EC\">Descripcion</TD>\n</TR>\n"

        for error in reporteerrores:
            contenido += '<TR> <TD>' + error.tipo + '</TD><TD>' + error.linea + '</TD> <TD>' + error.columna + '</TD><TD>' + error.descripcion + '</TD></TR>'

        contenido += '</TABLE>\n>, ];}'

        with open('reporteerrores.dot', 'w', encoding='utf8') as reporte:
            reporte.write(contenido)


def mostrarimagenre():
    check_call(['dot', '-Tpng', 'reporteerrores.dot', '-o', 'imagenerrores.png'])



def send_data():
    print("Analizando Entrada:")
    print("==============================================")
    # reporteerrores = []
    contenido = Tentrada.get(1.0, 'end')
    variables.consola.delete("1.0", "end")
    variables.consola.configure(state='normal')

    # print(contenido)
    Principal = Entorno()
    jsonMode.dropAll()

    # Principal.database = "DB1"
    instrucciones = g.parse(contenido)
    variables.consola.insert(INSERT, "Salida de consultas\n")
    for instr in instrucciones:
        if instr != None:

            res = instr.ejecutar(Principal)
            if res != None:
                res = str(res) + '\n'
                variables.consola.insert(INSERT, res)
                
    variables.consola.configure(state='disabled')
    #variables.consola.configure()

    tSym = Principal.mostrarSimbolos()
    with open('ts.dot', 'w', encoding='utf8') as ts:
            ts.write(tSym)
            
    check_call(['dot', '-Tpdf', 'ts.dot', '-o', 'ts.pdf'])

    reporte_lex_sin()


def arbol_ast():
    contenido = Tentrada.get(1.0, 'end')
    a.generarArbol(contenido)

def verSimbolos():
    os.system('start ts.pdf')


entrada = StringVar()
Tentrada = Text(variables.ventana)
Tentrada.config(width=120, height=20)
Tentrada.config(background="gray18")
Tentrada.config(foreground="white")
Tentrada.config(insertbackground="white")
Tentrada.place(x=10, y=10)

variables.consola = Text(variables.ventana)
variables.consola.config(width=120, height=15)
variables.consola.config(background="gray10")
variables.consola.config(foreground="white")
variables.consola.config(insertbackground="white")
variables.consola.place(x=10, y=350)
variables.consola.configure(state='disabled')
menu_bar = Menu(variables.ventana)

variables.ventana.config(menu=menu_bar)
# Menu Ejecutar
ej_menu = Menu(menu_bar)
menu_bar.add_cascade(label="Ejecutar", menu=ej_menu)
ej_menu.add_command(label="Analizar Entrada", command=send_data)

# Menu Reportes

reps_menu = Menu(menu_bar)
menu_bar.add_cascade(label="Reportes", menu=reps_menu)
reps_menu.add_command(label="Errores Lexicos y Sintacticos", command=mostrarimagenre)
reps_menu.add_command(label="Tabla de Simbolos", command=verSimbolos)
reps_menu.add_command(label="AST", command=arbol_ast)
reps_menu.add_command(label="Gramatica", command=send_data)

variables.ventana.mainloop()