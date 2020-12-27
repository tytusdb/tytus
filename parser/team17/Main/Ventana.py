import traceback
from tkinter import *
from tkinter import filedialog
from Parser.Ascendente.gramatica import parse as AnaParse
from Parser.Ascendente.gramatica import parse_1 as AnaParse_1
from Parser.Reportes.gramatica1 import parse as ReportParse
from Interprete.Tabla_de_simbolos import Tabla_de_simbolos
from Interprete.Arbol import Arbol
from Interprete.Manejo_errores.ErroresSemanticos import ErroresSemanticos
from Interprete.Manejo_errores.ErroresSintacticos import ErroresSintacticos
from Interprete.Manejo_errores.ErroresLexicos import ErroresLexicos
from Interprete.Manejo_errores.ReporteTS import ReporteTS

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from Parser.Reportes.Nodo import Nodo
from Parser.Reportes.TourTree import TourTree

from graphviz import Source

arboAux_errores: Arbol = None

dotString = ''
cadena = ''
root = Tk()
root.title('Editor ML WEB')
root.geometry("1200x660")
# =====================Para leer una archivo de pureba
f = open("./../Parser/Ascendente/entrada.txt", "r")
input = f.read()


# =====================Para leer una archivo de prueba FIn

# #############################################################################################
# ############################ Init Funciones #################################################
# #############################################################################################

def new_file():
    my_text.delete("1.0", END)
    root.title('New File - TextPad!')


def getName(ruta):
    files = ruta.split('/')
    nameWithExtension = files[len(files) - 1]
    names = nameWithExtension.split('.')
    name = names[0]
    return name


def getExtension(ruta):
    files = ruta.split('/')
    nameWithExtension = files[len(files) - 1]
    names = nameWithExtension.split('.')
    name = names[1]
    return name


def open_file():
    my_text.delete("1.0", END)
    text_file = filedialog.askopenfilename(title="Open File", filetypes=[("Text Files", "*.sql")])
    name = text_file
    name.replace('/home/jonathan/Documentos/MLWEBEDITOR/', '')

    # Obtension de extension y nombres
    nameFile = getName(name)
    extension = getExtension(name)

    my_text.setvar("nameFile", nameFile)
    my_text.setvar("Extension", extension)

    # Open the file
    text_file = open(text_file, 'r')
    stuff = text_file.read()
    # Add file to textbox
    my_text.insert(END, stuff)
    # Close the opened file
    text_file.close()


def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".*", title="Save File",
                                             filetypes=[("Text Files", "*.sql")])

    # Save the file
    text_file = open(text_file, 'w')
    text_file.write(my_text.get(1.0, END))

    # Close the file
    text_file.close()


def analizador():
    '''
        Se obtiene el texto del text area
        se pasa el parser y se ejecuta el patron interprete
    '''
    my_text1.delete("1.0", END)

    try:
        cadena = my_text.get("1.0", END)

        result: Arbol = AnaParse(cadena)

        entornoCero: Tabla_de_simbolos = Tabla_de_simbolos()
        entornoCero.NuevoAmbito()

        for item in result.instrucciones:
            item.execute(entornoCero, result)

        consola = ""
        for item in result.console:
            consola = consola + item

        my_text1.insert(END, consola)

        global arboAux_errores

        arboAux_errores = result

    except:
        print(traceback)
        my_text1.insert(END, 'Ocurrio un error al compilar')


def Seleccionar():
    try:
        cadena = my_text.get(SEL_FIRST, SEL_LAST)
        print('>> ' + cadena)

        result: Arbol = AnaParse(cadena)
        entornoCero: Tabla_de_simbolos = Tabla_de_simbolos()
        entornoCero.NuevoAmbito()

        for item in result.instrucciones:
            item.execute(entornoCero, result)

        consola = ""
        for item in result.console:
            consola = consola + item

        my_text1.insert(END, consola)
    except:
        my_text1.insert(END, 'Ocurrio un error al compilar')


def ReporteSelect():
    global dotString
    cadena = my_text.get(SEL_FIRST, SEL_LAST)
    result: Nodo = ReportParse(cadena)
    tour:TourTree = TourTree()
    dotString = tour.getDot(result)
    graph = Source(dotString)
    #graph.render(view=True, format='svg')

    try:
        graph.render(format='svg')
        print('Reporte Generado Con exito')
    except:
        print('No se genero el reporte:w')


def Reporte():
     global dotString
     cadena = my_text.get("1.0", END)
     result: Nodo = ReportParse(cadena)
     tour:TourTree = TourTree()
     dotString = tour.getDot(result)
     graph = Source(dotString)
    #graph.render(view=True, format='svg')

     try:
        graph.render(format='svg')
        print('Reporte Generado Con exito')
     except:
        print('No se genero el reporte:w')



def Err_Lexico():

    global arboAux_errores

    texto = '''
            <!DOCTYPE html>
            <html lang=\"es\">
            <head><meta charset=\"UTF-8\">  <title> Errores Lexicos</title> 
            <style type=\"text/css\"> \n'''
    texto += """body{ background-color: white; font-family: Arial;} 
        #main-container{ margin: 170px auto; width: 500px;}
        table{ background-color: white; text-align: center; border-collapse: collapse; width: 100%;}
        th, td{padding: 10px;}
        thead{background-color: #2464333;border-bottom: solid 5px #0F3543; color: black;}
        tr:nth-child(even){ background-color: #ddd;}
        tr:hover td{background-color: black;color: white;}"""
    texto += '''</style> </head> </body>
            <div id=\"main-container\">
            <h1>Reporte de errores Lexicos OLC2- G17</h1>
            <table> <thead> <tr>
            <th>#</th>
            <th>Descripcion</th>
            <th>Fila</th>
            <th>Origen</th>
            </tr> </thead>
            '''
    contador = 1

    for i in arboAux_errores.ErroresLexicos:
        Error: ErroresLexicos = i
        texto += '<tr><td> ' + str(contador) + '</td>'
        texto += '<td> ' + Error.descripcion + '</td>'
        texto += '<td> ' + str(Error.linea) + '</td>'
        texto += '<td> ' + Error.origen + '</td></tr>'
        contador = contador + 1
    texto += "</table> </div> </body> </html>"

    try:
        with open('ErroresLexicos.html', 'w') as lexicos:
            lexicos.write(texto)
    except Exception as e:
        print("No fue posible escribir el html: " + str(e))


def Err_Sintactico():
    global arboAux_errores

    texto = '''
        <!DOCTYPE html>
        <html lang=\"es\">
        <head><meta charset=\"UTF-8\">  <title> Errores Sintacticos</title> 
        <style type=\"text/css\"> \n'''
    texto += """body{ background-color: white; font-family: Arial;} 
    #main-container{ margin: 170px auto; width: 500px;}
    table{ background-color: white; text-align: center; border-collapse: collapse; width: 100%;}
    th, td{padding: 10px;}
    thead{background-color: #2464333;border-bottom: solid 5px #0F3543; color: black;}
    tr:nth-child(even){ background-color: #ddd;}
    tr:hover td{background-color: black;color: white;}"""
    texto += '''</style> </head> </body>
        <div id=\"main-container\">
        <h1>Reporte de errores Sintacticos OLC2- G17</h1>
        <table> <thead> <tr>
        <th>#</th>
        <th>Descripcion</th>
        <th>Fila</th>
        <th>Origen</th>
        </tr> </thead>
        '''
    contador = 1

    for i in arboAux_errores.ErroresSintacticos:
        Error: ErroresLexicos = i
        texto += '<tr><td> ' + str(contador) + '</td>'
        texto += '<td> ' + Error.descripcion + '</td>'
        texto += '<td> ' + str(Error.linea) + '</td>'
        texto += '<td> ' + Error.origen + '</td></tr>'
        contador = contador + 1
    texto += "</table> </div> </body> </html>"

    try:
        with open('ErroresSintacticos.html', 'w') as sintacticos:
            sintacticos.write(texto)
    except Exception as e:
        print("No fue posible escribir el html: " + str(e))





def Err_Semantico():

    global arboAux_errores

    texto = '''
            <!DOCTYPE html>
            <html lang=\"es\">
            <head><meta charset=\"UTF-8\">  <title> Errores Semanticos</title> 
            <style type=\"text/css\"> \n'''
    texto += """body{ background-color: white; font-family: Arial;} 
        #main-container{ margin: 170px auto; width: 500px;}
        table{ background-color: white; text-align: center; border-collapse: collapse; width: 100%;}
        th, td{padding: 10px;}
        thead{background-color: #2464333;border-bottom: solid 5px #0F3543; color: black;}
        tr:nth-child(even){ background-color: #ddd;}
        tr:hover td{background-color: black;color: white;}"""
    texto += '''</style> </head> </body>
            <div id=\"main-container\">
            <h1>Reporte de errores Semanticos OLC2- G17</h1>
            <table> <thead> <tr>
            <th>#</th>
            <th>Descripcion</th>
      
            <th>Origen</th>
            </tr> </thead>
            '''
    contador = 1

    for i in arboAux_errores.ErroresSemanticos:
        Error: ErroresSemanticos = i
        texto += '<tr><td> ' + str(contador) + '</td>'
        texto += '<td> ' + Error.descripcion + '</td>'

        texto += '<td> ' + Error.origen + '</td></tr>'
        contador = contador + 1
    texto += "</table> </div> </body> </html>"

    try:
        with open('ErroresSemanticos.html', 'w') as semanticos:
            semanticos.write(texto)
    except Exception as e:
        print("No fue posible escribir el html: " + str(e))


def Tabla_Simbolos():
    print('Estamos en SImbolos')
    global arboAux_errores

    texto = '''
                <!DOCTYPE html>
                <html lang=\"es\">
                <head><meta charset=\"UTF-8\">  <title> Tabla de Simbolos</title> 
                <style type=\"text/css\"> \n'''
    texto += """body{ background-color: white; font-family: Arial;} 
            #main-container{ margin: 170px auto; width: 500px;}
            table{ background-color: white; text-align: center; border-collapse: collapse; width: 100%;}
            th, td{padding: 10px;}
            thead{background-color: #2464333;border-bottom: solid 5px #0F3543; color: black;}
            tr:nth-child(even){ background-color: #ddd;}
            tr:hover td{background-color: black;color: white;}"""
    texto += '''</style> </head> </body>
                <div id=\"main-container\">
                <h1>Reporte de Tabla de Simbolos OLC2- G17</h1>
                <table> <thead> <tr>
                <th>#</th>
                <th>identificador</th>
                <th>tipo</th>
                <th>declarada_en</th>
                <th>linea</th>
                </tr> </thead>
                '''

    contador = 1

    for i in arboAux_errores.ReporteTS:
        Simbolo: ReporteTS = i
        texto += '<tr><td> ' + str(contador) + '</td>'
        texto += '<td> ' + Simbolo.identificador + '</td>'
        texto += '<td> ' + Simbolo.tipo + '</td>'
        texto += '<td> ' + Simbolo.declarada_en + '</td>'
        texto += '<td> ' + str(Simbolo.linea) + '</td></tr>'
        contador = contador + 1
    texto += "</table> </div> </body> </html>"

    try:
        with open('tabladesimbolos.html', 'w') as ts:
            ts.write(texto)
    except Exception as e:
        print("No fue posible escribir el html: " + str(e))


# ############################################################################################
# ############################ Fin Funciones #################################################
# ############################################################################################


# ############################ Entrada  #################################################
# Create a toolbar frame
toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X)

# Boton analizador
Analizador_button = Button(toolbar_frame, text="Analizador", command=analizador)
Analizador_button.grid(row=0, column=0, padx=2)

# Ejecutar Seleccion
Report_button = Button(toolbar_frame, text="Seleccion", command=Seleccionar)
Report_button.grid(row=0, column=20, padx=2)

# Boton Reporte
Report_button = Button(toolbar_frame, text="Reporte", command=Reporte)
Report_button.grid(row=0, column=40, padx=2)

# Boton Reporte
Report_Select = Button(toolbar_frame, text="Report Select", command=ReporteSelect)
Report_Select.grid(row=0, column=60, padx=2)

# Create Main Frame
my_frame = Frame(root)
my_frame.pack(pady=0, padx=0, side=LEFT)

# Create our Scrollbar for the Text Box
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

# Create a Text Box
my_text = Text(my_frame, width=60, height=30, font=("Helvetica", 13), selectbackground="yellow",
               selectforeground="black", undo=True, yscrollcommand=text_scroll.set)
my_text.insert(END, input)
my_text.pack(side=LEFT)
text_scroll.config(command=my_text.yview)

# ############################ Salida Consola #################################################
my_frame1 = Frame(root)
my_frame1.pack(pady=0, padx=0, side=LEFT)

text_scroll1 = Scrollbar(my_frame1)
text_scroll1.pack(side=RIGHT, fill=Y)

my_text1 = Text(my_frame1, width=60, height=40, font=("Consolas", 15), selectbackground="yellow",
                selectforeground="black", undo=True, yscrollcommand=text_scroll1.set,foreground="white",
                background="black")
my_text1.pack(side=LEFT)
text_scroll1.config(command=my_text1.yview)

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add File Menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='New', command=new_file)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=root.quit)

# Add Edit Menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label='Reportes', menu=edit_menu)
edit_menu.add_command(label='Lexico', command=Err_Lexico)
edit_menu.add_command(label='Sintactico', command=Err_Sintactico)
edit_menu.add_command(label='Semantico', command=Err_Semantico)
edit_menu.add_command(label='Tabla Simbolos', command=Tabla_Simbolos)
file_menu.add_separator()
