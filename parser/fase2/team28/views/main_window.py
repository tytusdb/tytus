from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter.font import Font
from prettytable import PrettyTable

import os
import json

from utils.analyzers.syntactic import *
from controllers.ast_construction import *
from utils.reports.generate_ast import GraficarAST
from controllers.error_controller import ErrorController
from utils.reports.report_error import ReportError
from utils.reports.symbol_report import SymbolTableReport
from utils.reports.tchecker_report import TypeCheckerReport
from views.data_window import DataWindow

report_error = None
report_ast = None


class MainWindow(object):
    archivo = ''

    def __init__(self, window):
        self.ventana = window
        # Defino un titulo para el GUI
        self.ventana.title('Query Tool')
        # Defino un fondo para usar, pueden cambiarlo por otro color mas bonito
        self.ventana.configure(background='#3c3f41')

        self.ventana.columnconfigure(0, weight=1)
        self.ventana.rowconfigure(0, weight=1)

        # Creo un frame para que contenga la intefaz, es como en java se hace con swing
        frame = LabelFrame(self.ventana)
        # Posiciono el frame
        frame.grid(row=0, column=0, columnspan=10, pady=10)
        # Defino un fondo para usar, pueden cambiarlo por otro color mas bonito
        frame.configure(background='#3c3f41', borderwidth=0)
        #############################################_MENU_#############################################
        # Creo un menu, es decir una lista desplegable
        barraMenu = Menu(self.ventana)
        self.ventana.config(menu=barraMenu)
        archivoMenu = Menu(barraMenu, tearoff=0)
        #############################################MENU Abrir#############################################
        archivoOpen = Menu(archivoMenu, tearoff=0)
        archivoOpen.add_command(label='Abrir Archivo',
                                command=self.open_file_editor)
        #############################################MENU Archivo#############################################
        archivoMenu.add_command(label='Nuevo', command=self.nuevo)
        archivoMenu.add_separator()
        archivoMenu.add_cascade(label='Abrir', menu=archivoOpen)
        archivoMenu.add_separator()
        archivoMenu.add_command(label='Guardar', command=self.guardar)
        archivoMenu.add_command(label='Guardar como...',
                                command=self.guardar_como)
        archivoMenu.add_separator()
        archivoMenu.add_command(label='Ejecutar',
                                command=self.analizar_entrada)
        archivoMenu.add_separator()
        archivoMenu.add_command(label='Salir', command=self.terminar)
        #############################################MENU WINDOWS##############################################
        windows_menu = Menu(barraMenu, tearoff=0)
        windows_menu.add_command(label='AST',
                                 command=self.report_ast_windows)
        windows_menu.add_separator()
        windows_menu.add_command(label='Tabla de errores',
                                 command=self.report_errors_windows)
        windows_menu.add_command(label='Tabla de simbolos',
                                 command=self.report_symbols_windows)
        windows_menu.add_separator()
        windows_menu.add_command(label='Type Checker',
                                 command=self.report_typeChecker_windows)
        windows_menu.add_separator()
        windows_menu.add_command(label='Reporte Gramatical',
                                 command=self.report_bnf_windows)
        #############################################MENU LINUX################################################
        ubuntu_menu = Menu(barraMenu, tearoff=0)
        ubuntu_menu.add_command(label='AST',
                                command=self.report_ast_ubuntu)
        ubuntu_menu.add_separator()
        ubuntu_menu.add_command(label='Tabla de errores',
                                command=self.report_errors_ubuntu)
        ubuntu_menu.add_command(label='Tabla de simbolos',
                                command=self.report_symbols_ubuntu)
        ubuntu_menu.add_separator()
        ubuntu_menu.add_command(label='Type Checker',
                                command=self.report_typeChecker_ubuntu)
        ubuntu_menu.add_separator()
        ubuntu_menu.add_command(label='Reporte Gramatical',
                                command=self.report_bnf_ubuntu)
        #############################################MENU REPORTES#############################################
        archivoReportes = Menu(barraMenu, tearoff=0)
        archivoReportes.add_cascade(label='Windows', menu=windows_menu)
        archivoReportes.add_separator()
        archivoReportes.add_cascade(label='Linux', menu=ubuntu_menu)
        #############################################MENU PRINCIPAL#############################################
        barraMenu.add_cascade(label='Archivo',
                              menu=archivoMenu)  # anade submenu
        barraMenu.add_cascade(label='Reportes', menu=archivoReportes)
        barraMenu.configure(background='SpringGreen')
        ############################################_ENTRADA_############################################
        Label(frame, text='Archivo de Entrada', borderwidth=0,
              font='Arial 15 bold', width=52, bg='#3c3f41', foreground='#fff').grid(row=3, column=0)

        hor_scroll = Scrollbar(frame, orient='horizontal')
        ver_scroll = Scrollbar(frame, orient='vertical')
        # Crea un scroll por si el texto es muy largo
        self.entrada = Text(frame, borderwidth=0, height=35,
                            width=70, bg='#2e2e31', foreground='#fff', undo=True, wrap='none', xscrollcommand=hor_scroll.set, yscrollcommand=ver_scroll.set)
        self.entrada.grid(row=4, column=0, padx=30)

        ver_scroll.config(command=self.entrada.yview)
        ver_scroll.grid(column=0, row=4, sticky='NE',ipady=255,padx=12)
        hor_scroll.config(command=self.entrada.xview)
        hor_scroll.grid(column=0, row=5, sticky='NS',ipadx=255)

        # Para este editor aun hay que ver si lo usamos como consola para errores, si no lo quitamos
        dataWindow = DataWindow()
        dataWindow.console = frame
        self.console = dataWindow.console
        self.console.grid(row=4, column=1, padx=30)
        # self.salida.insert(INSERT, 'Some text')
        # self.salida.insert(END, my_table)

        # END
        # Metodo para abrir archivo y colocarlo en el editor

    def open_file_editor(self):
        filename = askopenfilename(title='Abrir Archivo')
        archivo = open(filename, 'r')
        texto = archivo.read()
        self.entrada.insert(INSERT, texto)
        archivo.close()
        messagebox.showinfo('CARGA', 'SE CARGO CORRECTAMENTE EL ARCHIVO SQL')
        return
    # Crea una nueva pestana

    def nuevo(self):
        self.entrada.delete(1.0, END)
        DataWindow().clearConsole()
        self.archivo = ''

    # Guarda el archivo
    def guardar(self):
        if self.archivo == '':
            self.guardar_como()
        else:
            guardar_info = open(self.archivo, 'w')
            guardar_info.write(self.entrada.get('1.0', END))
            guardar_info.close()

    # Opcion para guardar como
    def guardar_como(self):
        guardar_info = asksaveasfilename(title='Guardar Archivo')
        write_file = open(guardar_info, 'w+')
        write_file.write(self.entrada.get('1.0', END))
        write_file.close()
        self.archivo = guardar_info

    # Opcion para ejecutar el texto de entrada del editor
    def analizar_entrada(self):
        global report_error
        global report_ast

        DataWindow().clearConsole()
        SymbolTable().destroy()

        texto = self.entrada.get('1.0', END)
        result = parse(texto)
        # jsonStr = json.dumps(result, default=lambda o: o.__dict__) #Convierte el AST a formato JSON para poder saber como se esta formando
        print(result)  # Imprime el AST

        report_error = ReportError()
        if len(ErrorController().getList()) > 0:
            messagebox.showerror('ERRORES', 'Se encontraron errores')
        else:
            result2 = parse2(texto)
            report_ast = result2
            messagebox.showinfo('EXITO', 'SE FINALIZO EL ANALISIS CON EXITO')

            # # ---------- TEST ---------
            # for inst in result:
            #     # esto es por los select anidados (subquerys), no encontre otra menera
            #     # de retornar la tabla dibujada, lo hacia en mi clase
            #     # pero si lo dejaba ahi me tronaban las subquery,
            #     # prueben que no les de problema
            #     if isinstance(inst, Select):
            #         result = inst.process(0)
            #         if isinstance(result, DataFrame):
            #             DataWindow().consoleText(format_df(result))
            #         elif isinstance(result, list):
            #             DataWindow().consoleText(format_table_list(result))
            #     else:
            #         inst.process(0)
            # ---------- TEST ---------

    # Para mostrar el editor
    def report_ast_ubuntu(self):
        global report_ast
        graficadora = GraficarAST()
        report = open('./team28/ast.dot', 'w')
        report.write(graficadora.generate_string(report_ast))
        report.close()
        os.system('dot -Tpng ./team28/ast.dot -o ./team28/ast.png')
        # Si estan en ubuntu dejan esta linea si no la comentan y descomentan la otra para windows
        os.system('xdg-open ./team28/ast.png')
        # os.open('ast.png')
        # os.startfile('ast.png')

    def report_errors_ubuntu(self):
        global report_error
        report = open('./team28/errors.dot', 'w')
        report.write(report_error.get_report())
        report.close()
        os.system('dot -Tpng ./team28/errors.dot -o ./team28/error.png')
        os.system('xdg-open ./team28/error.png')

    def report_symbols_ubuntu(self):
        report = open('symbolTable.dot', 'w')
        report.write(SymbolTableReport().generateReport())
        report.close()
        os.system('dot -Tpng ./team28/symbolTable.dot -o ./team28/symbolTable.png')
        os.system('xdg-open ./team28/symbolTable.png')

    def report_typeChecker_ubuntu(self):
        report = open('typeChecker.dot', 'w')
        report.write(TypeCheckerReport().generateReport())
        report.close()
        os.system('dot -Tpng ./team28/typeChecker.dot -o ./team28/typeChecker.png')
        os.system('xdg-open ./team28/typeChecker.png')

    def report_bnf_ubuntu(self):
        global report_ast
        report = open('bfn.txt', 'w')
        report.write(report_ast.production)
        report.close()
        os.system('xdg-open ./team28/bfn.txt')

    def report_ast_windows(self):
        global report_ast
        graficadora = GraficarAST()
        report = open('ast.dot', 'w')
        report.write(graficadora.generate_string(report_ast))
        report.close()
        os.system('dot -Tpng ast.dot -o ast.png')
        os.startfile('ast.png')

    def report_errors_windows(self):
        global report_error
        report = open('errors.dot', 'w')
        report.write(report_error.get_report())
        report.close()
        os.system('dot -Tpng errors.dot -o  error.png')
        os.startfile('error.png')

    def report_symbols_windows(self):
        report = open('symbolTable.dot', 'w')
        report.write(SymbolTableReport().generateReport())
        report.close()
        os.system('dot -Tpng symbolTable.dot -o symbolTable.png')
        os.startfile('symbolTable.png')

    def report_typeChecker_windows(self):
        report = open('typeChecker.dot', 'w')
        report.write(TypeCheckerReport().generateReport())
        report.close()
        os.system('dot -Tpng typeChecker.dot -o typeChecker.png')
        os.startfile('typeChecker.png')

    def report_bnf_windows(self):
        global report_ast
        report = open('bfn.txt', 'w')
        report.write(report_ast.production)
        report.close()
        os.startfile('bfn.txt')

    # Para salir de la aplicacion
    def terminar(self):
        salir = messagebox.askokcancel('Salir', 'Está seguro que desea salir?')
        if salir:
            self.ventana.destroy()
        return
