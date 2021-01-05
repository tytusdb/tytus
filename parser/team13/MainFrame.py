import tkinter as tk
import gramaticaASC as g
from tkinter import filedialog as FileDialog
from tkinter import colorchooser as ColorChooser
from tkinter import messagebox as MessageBox

import Graficar as graficando
import principal as principal
import os
from tkinter import filedialog
from tkinter import StringVar
from tkinter.constants import END, INSERT
import TablaSimbolos as TS

tablaSimbolos = TS.Entorno(None)
from tkinter import messagebox
import pickle
from graphviz import Digraph

pathFile=''

#################################### CLASE TextLineNumbers ####################################
class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)


################################## FIN CLASE TextLineNumbers ##################################


###################################### CLASE CustomText #######################################
class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        try:
            result = self.tk.call(cmd)
        except Exception:
            return None

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or
                args[0:3] == ("mark", "set", "insert") or
                args[0:2] == ("xview", "moveto") or
                args[0:2] == ("xview", "scroll") or
                args[0:2] == ("yview", "moveto") or
                args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result


#################################### FIN CLASE CustomText #####################################


######################################## CLASE Example ########################################
class Example(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.text = CustomText(self)
        self.vsb = tk.Scrollbar(orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.text)

        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)

    def _on_change(self, event):
        self.linenumbers.redraw()
        global fila
        global colum

        filaString = "Fila: " + str(self.text.index(tk.INSERT).split(".")[0])
        fila.set(filaString)

        columnString = "Columna: " + str(self.text.index(tk.INSERT).split(".")[1])
        colum.set(columnString)

    def insert_text(self, text):
        self.text.insert(INSERT, text)


###################################### FIN CLASE Example ######################################


if __name__ == "__main__":

    ########################################## FUNCIONES ##########################################
    

    #FUNCIÓN PARA IMPRIMIR EN CONSOLA
    def imprimir_consola(expresion):
        consola.configure(state=tk.NORMAL)
        consola.delete('1.0',END)
        consola.insert(INSERT, expresion)
        consola.configure(state=tk.DISABLED)
    

    #FUNCIÓN PARA ADJUNTAR TEXTO EN LA CONSOLA (SIN LIMPIARLA)
    def append_consola(expresion):
        consola.configure(state=tk.NORMAL)
        consola.insert(INSERT, expresion + '\n')
        consola.configure(state=tk.DISABLED)
    
    
    # FUNCIÓN PARA CREAR UN NUEVO ARCHIVO
    def __funcion_nuevo():
        global pathFile
        pathFile = ""
        my_editor.text.delete(1.0, "end")

    # FUNCIÓN PRIVADA PARA ABRIR UN ARCHIVO DE TEXTO
    def __funcion_abrir():
        global pathFile 
        pathFile = FileDialog.askopenfilename(
        initialdir='.',
        filetypes=( 
            ("All file", "*"),  
        ), 
        title="Abrir Archivo"
        )
        #input = filedialog.askopenfilename(initialdir="/")
        if pathFile != "":
            archivo = open(pathFile, "r", encoding="utf8")
            contenido = archivo.read()
            my_editor.text.delete('1.0', END)
            my_editor.text.insert(INSERT, contenido)


    # FUNCIÓN PARA GUARDAR UN NUEVO ARCHIVO
    def __funcion_guardar():
        print('Guardando...')
        global pathFile
        if pathFile != "":
            contenido = my_editor.text.get('1.0', END)
            archivo = open(pathFile, 'w+')         
            archivo.write(contenido)           
            archivo.close()
            MessageBox.showinfo("Archivo guardado","El archivo se guardo exitosamente")
        else :
            MessageBox.showwarning("Guardar","Abra un archivo primero")
 
        # FUNCIÓN PARA GUARDAR COMO


    def __funcion_guardar_como():
        print('Guardando como...')
        global pathFile
        archivo = FileDialog.asksaveasfile(title="Guardar archivo", mode='w',
        defaultextension=".txt")
        if archivo is not None:
             pathFile = archivo.name  
             contenido = my_editor.text.get('1.0', END)
             archivo = open(pathFile, 'w+') 
             archivo.write(contenido) 
             archivo.close()
             MessageBox.showinfo("Archivo guardado","El archivo se guardo exitosamente")
        else:
             MessageBox.showinfo("Archivo no guardado","El archivo no se guardó")

          
        # FUNCIÓN PARA DETENER EL PROGRAMA

    def __funcion_cerrar():
        root.quit()
        print('Cerrando...')




    def __funcion_analizar():

        g.errores_lexicos.clear()
        g.errores_sintacticos.clear()
        
        principal.consola = ""
        principal.listaSemanticos.clear()
        
        entrada = my_editor.text.get('1.0', END)

        arbol = g.parse(entrada)

        if len(g.errores_lexicos) == 0:

            if len(g.errores_sintacticos) == 0:
                imprimir_consola("") 
                data=principal.interpretar_sentencias(arbol,tablaSimbolos)
                #tablaSimbolos.mostrar()
                imprimir_consola(data)
                #append_consola(tablaSimbolos.mostrar_tabla())
                raiz = graficando.analizador(entrada)
                graficando.GraficarAST(raiz)
                graficando.ReporteGramatical()
            else:

                imprimir_consola('Se detectaron algunos errores sintácticos')
                append_consola('')
                append_consola('No. \t Lexema \t Tipo \t\t Fila \t Columna \t Descripción ')
                
                i = 0
                while i < len(g.errores_sintacticos):
                    
                    append_consola( str(i) + ' \t ' + str(g.errores_sintacticos[i].lexema) +  ' \t ' + str(g.errores_sintacticos[i].tipo) +  ' \t ' + str(g.errores_sintacticos[i].fila) +  ' \t ' + str(g.errores_sintacticos[i].columna) +  ' \t ' + str(g.errores_sintacticos[i].descripcion) +  ' ')
                    i += 1
        else:

            imprimir_consola('Se detectaron algunos errores léxicos')
            append_consola('')
            append_consola('No. \t Lexema \t Tipo \t\t Fila \t Columna \t Descripción ')
                
            i = 0
            while i < len(g.errores_lexicos):
                    
                append_consola( str(i) + ' \t ' + str(g.errores_lexicos[i].lexema) +  ' \t ' + str(g.errores_lexicos[i].tipo) +  ' \t ' + str(g.errores_lexicos[i].fila) +  ' \t ' + str(g.errores_lexicos[i].columna) +  ' \t ' + str(g.errores_lexicos[i].descripcion) +  ' ')
                i += 1


        # FUNCIÓN PRIVADA PARA ANALIZAR EL ARCHIVO DE ENTRADA
    def __funcion_analizar_desc():
    
        """ entrada = my_editor.text.get('1.0',END)
        gd.parse(entrada) """


    # FUNCIÓN PRIVADA PARA REALIZAR EL REPORTE DE ERRORES LÉXICOS
    def __funcion_errores_lexicos():

        g.erroresLexicos()
    
        """ entrada = my_editor.text.get('1.0',END)
        gd.parse(entrada) """


    # FUNCIÓN PRIVADA PARA REALIZAR EL REPORTE DE ERRORES SINTÁCTICOS
    def __funcion_errores_sintacticos():

        g.erroresSintacticos()
    
        """ entrada = my_editor.text.get('1.0',END)
        gd.parse(entrada) """
    # FUNCIÓN PRIVADA PARA REALIZAR EL REPORTE DE ERRORES SINTÁCTICOS
    def __funcion_GramaticalEstatico():
            os.startfile('gramaticaEstatico.txt') 
            os.startfile('GramaticaEstaticoDescendente.txt') 
    def __funcion_GramaticalDinamico():
            os.startfile('gramaticaDinamico.txt') 
   

    def __funcion_AST():
            os.startfile('arbol.jpg') 


    def __funcion_TS():

        ast = Digraph('AST', filename='c:/source/ast.gv', node_attr={'color': 'black', 'fillcolor': 'white','style': 'filled', 'shape': 'record'})
        ast.attr(rankdir='TB',ordering='in')
        ast.edge_attr.update(arrowhead='none')
        
        clus = 'cluster_'
        c_clus = 0
        con = 0
        tag = "t"
        for i in tablaSimbolos.tabla:

            base = tablaSimbolos.tabla[i]

            cl = clus + str(c_clus)
            with ast.subgraph(name=cl) as c:
                c.attr(label= "NOMBRE BD: '%s'\\nOWNER: '%s'\\nMODE: '%s'" % (base.nombre,base.owner,base.mode))
                c_clus += 1
                
                for j in base.tablas:

                    tabla = base.tablas[j]
                    label = ""

                    for k in  tabla.columnas:

                        column = tabla.columnas[k]
                        
                        label += "| COLUMNA: " + str(column.nombre) + " | { Tipo | " + str(column.tipo) + " } | { Llave Primaria | " + str(column.primary_key) +" } | { LLave Foránea | " + str(column.foreign_key) + " } | { Unique | " + str(column.unique) + " } | { Default | " + str(column.default) + " } | { Null | " + str(column.null) + " } | { Check |  " + str(column.check) + "  } | { Index | " + str(column.index) + " } "
                    label2 = label
                    t = tag + str(con)
                    c.node(t, "{ NOMBRE TABLA: " + str(tabla.nombre) + "\\nPADRE: " + str(tabla.padre) + " " + label2 +" }")
                    con += 1

        ast.render('tablaS', format='png', view=True)

    def __funcion_on_closing():
        if messagebox.askokcancel("Salir", "¿Realmente desea finalizar el programa?"):

            # try:
            #     pickle.dump(tablaSimbolos,open("ts.p","wb"))
            #     pickle.dump(principal.listaConstraint,open("lc.p","wb"))
            #     pickle.dump(principal.listaFK,open("lf.p","wb"))
                
            # except Exception as e:
            #     print(e)

            root.destroy()

    def __funcion_ManualTecnico():
        os.startfile('Manual_Tecnico.pdf') 
   
    def __funcion_ManualUsuario():
        os.startfile('Manual_Usuario.pdf') 
   
    def __funcion_AcercaDe():
        MessageBox.showinfo("Ayuda- Grupo13",
                        '''Interprete DATABASE - USAC. Es un interprete basado en el lenguaje SQL .''')
 
   

######################################## FIN FUNCIONES ########################################


######################### CONFIGURANDO LOS PARÁMETROS PARA LA VENTANA #########################
    root = tk.Tk()
    m = root.maxsize()
    root.geometry('{}x{}+0+0'.format(*m))
    root.title("[G13]OLC2 TytusDB Query tool ")

    # VENTANA PRINCIPAL
    frame = tk.Frame(root)
    frame.place(x=0, y=0, width=1366, height=500)

    ############################### BARRA DE MENÚS DE LA APLICACIÓN ###############################
    top = frame.winfo_toplevel()

    # DECLARACIÓN DE LA BARRA DE MENÚ
    menubar = tk.Menu(top, font='Helvetica 25 bold')

    ### MENÚ ARCHIVO
    menu_archivo = tk.Menu(menubar, tearoff=0)

    # SUB MENÚS PARA EL MENÚ ARCHIVO
    menu_archivo.add_command(label="Nuevo", command=__funcion_nuevo)
    menu_archivo.add_command(label="Abrir", command=__funcion_abrir)
    menu_archivo.add_command(label="Guardar", command=__funcion_guardar)
    menu_archivo.add_command(label="Guardar como", command=__funcion_guardar_como)
    menu_archivo.add_separator()
    menu_archivo.add_command(label="Salir", command=__funcion_cerrar)

    # CREACIÓN DEL MENÚ ARCHIVO INCRUSTANDO LOS SUBMENÚS
    menubar.add_cascade(label="Archivo", menu=menu_archivo)

    ### MENÚ ANALIZAR
    menu_analizar = tk.Menu(menubar, tearoff=0)

    #SUB MENÚS PARA EL MENÚ ANALIZAR
    menu_analizar.add_command(label="Análisis Ascendente", command=__funcion_analizar)
    menu_analizar.add_command(label="Análisis Descendente", command=__funcion_analizar_desc)

    # CREACIÓN DEL MENÚ ANALIZAR INCRUSTANDO LOS SUBMENÚS
    menubar.add_cascade(label="Analizar", menu=menu_analizar)

    # SE AGREGA LA BARRA DE MENÚ A LA RAÍZ
    root.config(menu=menubar)

    ### MENÚ REPORTES
    menu_reporte = tk.Menu(menubar, tearoff=0)

    #SUB MENÚS PARA EL MENÚ ANALIZAR
    menu_reporte.add_command(label="AST", command=__funcion_AST)
    menu_reporte.add_command(label="Gramatical Estatico", command=__funcion_GramaticalEstatico)
    menu_reporte.add_command(label="Gramatical Dinamico", command=__funcion_GramaticalDinamico)
    menu_reporte.add_command(label="Tabla de Símbolos", command=__funcion_TS)

       
    menu_reporte.add_separator()
    menu_reporte.add_command(label="Errores Léxicos", command=__funcion_errores_lexicos)
    menu_reporte.add_command(label="Errores Sintácticos", command=__funcion_errores_sintacticos)
    menu_reporte.add_command(label="Errores Semánticos", command=__funcion_analizar)
     # CREACIÓN DEL MENÚ ANALIZAR INCRUSTANDO LOS SUBMENÚS
    menubar.add_cascade(label="Reportes", menu=menu_reporte)
   
    #SUB MENÚS PARA EL MENÚ AYUDA
    ### MENÚ REPORTES
    menu_ayuda = tk.Menu(menubar, tearoff=0)

    menu_ayuda.add_command(label="Manual Tecnico", command=__funcion_ManualTecnico)
    menu_ayuda.add_command(label="Manual Usuario", command=__funcion_ManualUsuario)
    menu_ayuda.add_command(label="Acerca DE", command=__funcion_AcercaDe)
    
     # MENU AYUDA
   
    menubar.add_cascade(label="Ayuda",    menu=menu_ayuda)
     
    # SE AGREGA LA BARRA DE MENÚ A LA RAÍZ
    root.config(menu=menubar)

    ####################################### EDITOR DE TEXTO #######################################

    # EDITOR DE TEXTO
    my_editor = Example(frame)
    my_editor.pack(side="top", fill="both", expand=True)
    
    
    # ETIQUETAS PARA LA FILA Y COLUMNA ACTUAL

    fila = StringVar()
    colum = StringVar()

    filaL = tk.Label(frame, textvariable=fila)
    filaL.place(x=100, y=550, width=100, height=25)
    filaL.pack()

    columnaL = tk.Label(frame, textvariable=colum)
    columnaL.place(x=100, y=590, width=100, height=25)
    columnaL.pack()

    ######################################### CONSOLA #############################################

    consola = tk.Text(root, bg='black', fg='white', state=tk.DISABLED)
    consola.place(x=30, y=505, width=1330, height=140)

    root.protocol("WM_DELETE_WINDOW", __funcion_on_closing)
    try:
        tablaSimbolos = pickle.load(open("ts.p","rb"))
        principal.listaConstraint = pickle.load(open("lc.p","rb"))
        principal.listaFK = pickle.load(open("lf.p","rb"))
        #tablaSimbolos.mostrar()
    except Exception as e:
        print(e)
    
    root.mainloop()
