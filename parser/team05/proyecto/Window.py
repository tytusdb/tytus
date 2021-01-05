# GRUPO 5
# 201213062 - Mónica Raquel Calderon Muñoz
# 201213223 - Astrid Edith Hernandez Gonzalez
# 201213255 - Leonel Eduardo Avila Calvillo
# 201220159 - Diego Ahtohil Noj Armira
# 201220165 - Oscar Rolando Bernard Peralta

# IMPORT SECTION
import WidgetLineNumber as ln
import tkinter.scrolledtext as tkst
from tkinter.ttk import *
from tkinter import Menu, Frame, ttk, filedialog, messagebox, simpledialog
from tkinter.simpledialog import askstring
import tkinter as tk
from tkinter import *
from tkinter import filedialog

import Lexico as g
import TablaSimbolos as st
import errorSemanticos as es
import CTable as ct
import os
import re
from Instrucciones import *
from jsonMode import *
from Expresiones import *
from reporteTS import *
import webbrowser
from Graficar import Graficar


# MAIN CLASS
class Main(tk.Tk):
    # Main definition
    def __init__(self):
        super().__init__()

        # Global variables in class
        self.tab_counter = 1
        self.use_db = None
        self.array_tabs = []
        self.array_canvas = []
        self.array_name = []
        self.search_list = list()
        self.active_file = ""
        self.DATA_TYPES_BLUE = ["CREATE", "create", "SHOW", "show", "USE", "use", "ALTER", "alter", "DROP", "drop"]
        self.KEYWORDS_FUNCTIONS = ["DATABASE", "database"]
        self.SPACES_REGEX = re.compile("^\s*")
        self.STRING_REGEX_SINGLE = re.compile("'[^'\r\n]*'")
        self.STRING_REGEX_DOUBLE = re.compile('"[^"\r\n]*"')
        self.NUMBER_REGEX = re.compile(r"\b(?=\(*)\d+\.?\d*(?=\)*\,*)\b")
        self.KEYWORDS_REGEX = re.compile("(?=\(*)(?<![a-z])(None|True|False)(?=\)*\,*)")
        self.SELF_REGEX = re.compile("(?=\(*)(?<![a-z])(self)(?=\)*\,*)")
        self.FUNCTIONS_REGEX = re.compile("(?=\(*)(?<![a-z])(print|list|dict|set|int|str)(?=\()")
        self.raiz_ast = None

        self.REGEX_TO_TAG = {
            self.STRING_REGEX_SINGLE: "string",
            self.STRING_REGEX_DOUBLE: "string",
            self.NUMBER_REGEX: "digit",
            self.KEYWORDS_REGEX: "keywordcaps",
            self.SELF_REGEX: "keyword1",
            self.FUNCTIONS_REGEX: "keywordfunc",
        }

        # Properties of the window -------------------------------------------------
        self.title("Tytus DB - Grupo 5")
        self.geometry("1200x800")
        self.minsize(800, 800)
        self.maxsize(1200, 800)

        # Menu Widget
        self.menu_bar = Menu()
        # Submenu [File]
        self.sm_file = Menu(self.menu_bar, tearoff=False)
        self.sm_file.add_command(label="Nueva pestaña", command=lambda: self.file_new_tab())
        self.sm_file.add_command(label="Abrir", command=lambda: self.file_open())
        self.sm_file.add_command(label="Guardar", command=lambda: self.file_save())
        self.sm_file.add_command(label="Guardar como", command=lambda: self.file_save_as())
        self.sm_file.add_command(label="Cerrar pestaña", command=lambda: self.file_close_tab())
        self.sm_file.add_command(label="Salir", command=lambda: self.exit_program())
        self.menu_bar.add_cascade(label="Archivo", menu=self.sm_file)
        # Submenu [Edit]
        self.sm_edit = Menu(self.menu_bar, tearoff=False)
        self.sm_edit.add_command(label="Copiar", command=lambda: self.edit_copy())
        self.sm_edit.add_command(label="Cortar", command=lambda: self.edit_cut())
        self.sm_edit.add_command(label="Pegar", command=lambda: self.edit_paste())
        self.sm_edit.add_command(label="Buscar", command=lambda: self.edit_search())
        self.sm_edit.add_command(label="Reemplazar", command=lambda: self.edit_replace())
        self.menu_bar.add_cascade(label="Edicion", menu=self.sm_edit)
        # Submenu [Analysis]
        self.sm_analyze = Menu(self.menu_bar, tearoff=False)
        self.sm_analyze.add_command(label="Ejecutar", command=lambda: self.tytus_ejecutar())
        self.sm_analyze.add_command(label="Cerrar pestaña", command=lambda: self.close_output_tab())
        self.sm_analyze.add_command(label="Cerrar pestañas", command=lambda: self.delete_outputs())
        self.menu_bar.add_cascade(label="Queries", menu=self.sm_analyze)
        # Submenu [Reports]
        self.sm_report = Menu(self.menu_bar, tearoff=False)
        self.sm_report.add_command(label="Reporte Léxico", command=lambda: self.report_lexic())
        self.sm_report.add_command(label="Reporte Sintáctico", command=lambda: self.report_syntactic())
        self.sm_report.add_command(label="Reporte Semántico", command=lambda: self.report_semantic())
        self.sm_report.add_command(label="Reporte Tabla de Simbolos", command=lambda: self.report_st())
        self.sm_report.add_command(label="Reporte AST", command=lambda: self.ast_report())
        self.menu_bar.add_cascade(label="Reportes", menu=self.sm_report)
        # Submenu [Help]
        self.sm_help = Menu(self.menu_bar, tearoff=False)
        self.sm_help.add_command(label="Manual de Usuario", command=lambda: self.help_user_manual())
        self.sm_help.add_command(label="Manual Técnico", command=lambda: self.help_technical_manual())
        self.sm_help.add_command(label="Acerca de", command=lambda: self.help_about_it())
        self.menu_bar.add_cascade(label="Ayuda", menu=self.sm_help)
        # Input Frame & Widget
        self.in_frame = Frame(self)
        self.in_frame.pack(fill="both", pady=5, expand=1)
        self.ta_input = Notebook(self.in_frame, width=150, height=20)
        self.ta_input.pack(fill="both", expand=1)
        # Output Frame & Widget
        self.out_frame = Frame(self)
        self.out_frame.pack(fill="both", pady=5, expand=1)
        self.ta_output = Notebook(self.out_frame, width=150, height=15)
        self.ta_output.pack(fill="both", expand=1)
        # Menu Configuration
        self.config(menu=self.menu_bar)
        # Opening first tab
        self.file_new_tab()

    def _on_change(self, event):
        index = self.ta_input.index(self.ta_input.select())
        canvas = self.array_canvas[index]
        canvas.redraw()
        del index, canvas

    # New output tab
    def new_output(self, output=""):
        try:
            # Creando nueva tab
            tab1 = Frame(self.ta_output)
            self.ta_output.add(tab1, text="SALIDA")
            self.ta_output.pack(expand=1, fill="both")
            # Creando campo de texto
            text = ln.TextAreaWidget(tab1, bg="black", fg="white", width=150, height=15)
            text.pack(side="right", fill="both", expand=True)
            text.insert(END, output)
            del text
        except:
            messagebox.showerror("A OCURRIDO UN ERROR",
                                 "No se ha podido crear una nueva pestaña. Por favor, intente nuevamente.")

    # Close output tab
    def close_output_tab(self):
        try:
            # Getting selected tab & deleting it
            index = self.ta_output.index(self.ta_output.select())
            self.ta_output.forget(index)
            del index
        except:
            pass

    # Delete outputs
    def delete_outputs(self):
        try:
            _list = self.ta_output.winfo_children()
            for item in _list:
                if item.winfo_children():
                    self.ta_output.forget(item)
            del _list
        except:
            pass

    # New tab with custom text widget
    def file_new_tab(self):
        try:
            # Creating the tab
            tab1 = Frame(self.ta_input)
            self.ta_input.add(tab1, text="Tab " + str(self.tab_counter))
            self.ta_input.pack(expand=1, fill="both")
            # Creating text input
            text = ln.TextAreaWidget(tab1)
            text.bind("<KeyRelease>", self.tag_keywords)
            text.tag_config("keyword1", foreground="blue")
            text.tag_config("keywordfunc", foreground="darkgrey")
            line_numbers = ln.LineNumber(tab1, width=30)
            line_numbers.attach(text)
            line_numbers.pack(side="left", fill="y")
            text.pack(side="right", fill="both", expand=True)
            text.bind("<<Change>>", self._on_change)
            text.bind("<Configure>", self._on_change)
            self.array_tabs.append(text)
            self.array_name.append("Tab " + str(self.tab_counter))
            self.array_canvas.append(line_numbers)
            self.tab_counter += 1
            del tab1, text, line_numbers
        except:
            messagebox.showerror("A OCURRIDO UN ERROR",
                                 "No se ha podido crear una nueva pestaña. Por favor, intente nuevamente.")

    # Open new file with .txt extension
    def file_open(self):
        try:
            # Getting file name & content
            filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(
                ("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*")))
            a_file = open(filename)
            txt_input = a_file.read()
            file_title = os.path.basename(a_file.name)
            # Creating the tab
            tab1 = Frame(self.ta_input)
            self.ta_input.add(tab1, text=file_title)
            self.ta_input.pack(expand=1, fill="both")
            # Creating the text area
            text = ln.TextAreaWidget(tab1)
            text.insert(END, txt_input)
            line_numbers = ln.LineNumber(tab1, width=30)
            line_numbers.attach(text)
            line_numbers.pack(side="left", fill="y")
            text.pack(side="right", fill="both", expand=True)
            text.bind("<<Change>>", self._on_change)
            text.bind("<Configure>", self._on_change)
            self.array_tabs.append(text)
            self.array_name.append(a_file.name)
            self.array_canvas.append(line_numbers)
            self.tab_counter += 1
            a_file.close()
            del filename, a_file, tab1, text, line_numbers
        except:
            pass

    # Save opened file
    def file_save(self):
        try:
            # Getting text from tab and file path
            index = self.ta_input.index(self.ta_input.select())
            txt_input = self.array_tabs[index].get("1.0", END)
            txt_filepath = self.array_name[index]
            if os.path.exists(txt_filepath):
                a_file = open(txt_filepath, "r+")
                a_file.write(txt_input)
                a_file.close()
            else:
                self.file_save_as()
            messagebox.showinfo("INFO",
                                "El archivo ha sido guardado exitosamente")
            del index, txt_input, txt_filepath, a_file
        except:
            messagebox.showerror("A OCURRIDO UN ERROR",
                                 "No se ha podido guardar. Por favor, intente nuevamente.")

    # Save as new file
    def file_save_as(self):
        try:
            # Getting text from tab
            index = self.ta_input.index(self.ta_input.select())
            input_text = self.array_tabs[index].get("1.0", END)
            # Path of new file
            file = filedialog.asksaveasfile(initialdir="/", title="Select file", filetypes=(
                ("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*"))).name
            if not ".txt" in file:
                file += ".txt"
            # Creating file
            a_file = open(file, "w+")
            a_file.write(input_text)
            a_file.close()
            messagebox.showinfo("INFO",
                                "El archivo ha sido guardado exitosamente")
            del index, input_text, file, a_file
        except:
            messagebox.showerror("A OCURRIDO UN ERROR",
                                 "No se tiene seleccionada una pestaña para guardar. Por favor, intente nuevamente.")

    # Exit tab
    def file_close_tab(self):
        try:
            # Getting selected tab & deleting it
            index = self.ta_input.index(self.ta_input.select())
            self.ta_input.forget(index)
            del self.array_name[index]
            del self.array_tabs[index]
            del index
        except:
            pass

    # Exiting IDE
    def exit_program(self):
        self.destroy()

    # Copy option
    def edit_copy(self, event=None):
        self.clipboard_clear()
        index = self.ta_input.index(self.ta_input.select())
        input_text = self.array_tabs[index]
        text = input_text.get("sel.first", "sel.last")
        self.clipboard_append(text)
        del index, input_text, text

    # Cut option
    def edit_cut(self):
        self.edit_copy()
        index = self.ta_input.index(self.ta_input.select())
        input_text = self.array_tabs[index]
        input_text.delete("sel.first", "sel.last")
        del index, input_text

    # Paste option
    def edit_paste(self):
        index = self.ta_input.index(self.ta_input.select())
        input_text = self.array_tabs[index]
        text = self.selection_get(selection='CLIPBOARD')
        input_text.insert('insert', text)
        del index, input_text, text

    # Search word option
    def edit_search(self):
        # Getting the word to search
        word = askstring('Buscar palabra', '¿Qué palabra desea buscar?')
        # Getting the input widget
        index = self.ta_input.index(self.ta_input.select())
        input_widget = self.array_tabs[index]
        input_text = input_widget.get("1.0", END)
        # Reset list
        self.search_list.clear()
        input_widget.tag_remove(SEL, 1.0, "end-1c")
        # Searching word
        input_widget.focus_set()
        if word:
            if not self.search_list:
                idx = "1.0"
            else:
                idx = self.search_list[-1]

            idx = input_widget.search(word, idx, nocase=1, stopindex=END)
            lastidx = '%s+%dc' % (idx, len(word))

            try:
                input_widget.tag_remove(SEL, 1.0, lastidx)
            except:
                pass

            try:
                input_widget.tag_add(SEL, idx, lastidx)
                counter_list = []
                counter_list = str(idx).split('.')
                input_widget.mark_set("insert", "%d.%d" % (float(int(counter_list[0])), float(int(counter_list[1]))))
                input_widget.see(float(int(counter_list[0])))
                self.search_list.append(lastidx)
            except:
                messagebox.showinfo("Busqueda completada", "No hay coincidencias.")
                self.search_list.clear()
                input_widget.tag_remove(SEL, 1.0, "end-1c")
        del word, index, input_widget, input_text, idx, lastidx, counter_list

    # Replace word option
    def edit_replace(self):
        # Getting the words to search and replace
        word = askstring('Reemplazar palabra', '¿Qué palabra desea reemplazar?')
        replace = askstring('Nueva palabra', 'Nuevo valor para \'' + word + '\'')
        # Getting the input widget
        index = self.ta_input.index(self.ta_input.select())
        input_widget = self.array_tabs[index]
        input_text = input_widget.get("1.0", END)
        # Reset list
        self.search_list.clear()
        input_widget.tag_remove(SEL, 1.0, "end-1c")
        # Searching word
        input_widget.focus_set()
        if word:
            if not self.search_list:
                idx = "1.0"
            else:
                idx = self.search_list[-1]

            idx = input_widget.search(word, idx, nocase=1, stopindex=END)
            lastidx = '%s+%dc' % (idx, len(word))

            try:
                input_widget.tag_remove(SEL, 1.0, lastidx)
            except:
                pass

            try:
                input_widget.delete(idx, lastidx)
                input_widget.insert(idx, replace)

            except:
                messagebox.showinfo("Busqueda completada", "No hay coincidencias para reemplazar.")
                self.search_list.clear()
                input_widget.tag_remove(SEL, 1.0, "end-1c")
        del word, index, input_widget, input_text, idx, lastidx

    # Lexic report
    def report_lexic(self):
        if os.path.exists("reports/reporte_lexico.html"):
            os.remove("reports/reporte_lexico.html")

        if os.path.exists("reports/error_lexical.txt"):
            report = open("reports/reporte_lexico.html", "a")
            file1 = open("reports/inicio_error_lexico.txt", "r")
            file2 = open("reports/error_lexical.txt", "r")
            file3 = open("reports/fin_error.txt", "r")
            report.write(file1.read())
            report.write(file2.read())
            report.write(file3.read())
            report.close()
            webbrowser.open('file://' + os.path.realpath("reports/reporte_lexico.html"))
        else:
            messagebox.showerror("INFO", "No exite un archivo de reporte.")

    # Syntactic report
    def report_syntactic(self):
        if os.path.exists("reports/reporte_sintactico.html"):
            os.remove("reports/reporte_sintactico.html")

        if os.path.exists("reports/error_syntactic.txt"):
            report = open("reports/reporte_sintactico.html", "a")
            file1 = open("reports/inicio_error_sintactico.txt", "r")
            file2 = open("reports/error_syntactic.txt", "r")
            file3 = open("reports/fin_error.txt", "r")
            report.write(file1.read())
            report.write(file2.read())
            report.write(file3.read())
            report.close()
            webbrowser.open('file://' + os.path.realpath("reports/reporte_sintactico.html"))
        else:
            messagebox.showerror("INFO", "No exite un archivo de reporte.")

    # Semantic report
    def report_semantic(self):
        eS = es.ListaErroresSemanticos()
        generarReporte(eS)

    # ST report
    def report_st(self):
        tSimbolo = st.SymbolTable()
        generarTablaSimbolos(tSimbolo)

    # AST report
    def ast_report(self):
        g = Graficar()
        g.graficar_arbol(self.raiz_ast)

    def help_user_manual(self):
        webbrowser.open('file://' + os.path.realpath("documents/Manual de Usuario.pdf"))

    def help_technical_manual(self):
        webbrowser.open('file://' + os.path.realpath("documents/Manual Técnico.pdf"))

    # About it section
    def help_about_it(self):
        messagebox.showinfo("Tytus DB",
                            "Organización de Lenguajes y Compiladores 2\n"
                            "Proyecto Fase 1\n\n"
                            "201213062 - Mónica Raquel Calderon Muñoz\n"
                            "201213223 - Astrid Edith Hernandez Gonzalez\n"
                            "201213255 - Leonel Eduardo Avila Calvillo\n"
                            "201220159 - Diego Ahtohil Noj Armira\n"
                            "201220165 - Oscar Rolando Bernard Peralta")

    # Highlight of MinorC words
    def tag_keywords(self, event=None, current_index=None):
        if not (event.keysym == "Home" or event.keysym == "Shift_L"):
            # Getting selected tab's widget
            index = self.ta_input.index(self.ta_input.select())
            input_text = self.array_tabs[index]
            # Getting position of last letter written
            if not current_index:
                current_index = input_text.index(tk.INSERT)
            line_number = current_index.split(".")[0]
            line_beginning = ".".join([line_number, "0"])
            line_text = input_text.get(line_beginning, line_beginning + " lineend")
            line_words = line_text.split()
            number_of_spaces = self.number_of_leading_spaces(line_text)
            y_position = number_of_spaces

            for tag in input_text.tag_names():
                input_text.tag_remove(tag, line_beginning, line_beginning + " lineend")

            self.add_regex_tags(line_number, line_text)

            for word in line_words:
                stripped_word = word.strip("():,")

                word_start = str(y_position)
                word_end = str(y_position + len(stripped_word))
                start_index = ".".join([line_number, word_start])
                end_index = ".".join([line_number, word_end])

                if stripped_word in self.DATA_TYPES_BLUE:
                    input_text.tag_add("keyword1", start_index, end_index)

                y_position += len(word) + 1

    # Number of leading spaces
    def number_of_leading_spaces(self, line):
        spaces = re.search(self.SPACES_REGEX, line)
        if spaces.group(0) is not None:
            number_of_spaces = len(spaces.group(0))
        else:
            number_of_spaces = 0

        return number_of_spaces

    # Add regex tags
    def add_regex_tags(self, line_number, line_text):
        # Getting selected tab's widget
        index = self.ta_input.index(self.ta_input.select())
        input_text = self.array_tabs[index]
        #
        for regex, tag in self.REGEX_TO_TAG.items():
            for match in regex.finditer(line_text):
                start, end = match.span()
                start_index = ".".join([line_number, str(start)])
                end_index = ".".join([line_number, str(end)])
                input_text.tag_add(tag, start_index, end_index)

    def do_nothing(self, event=None):
        if not (event.keysym == "Home" or event.keysym == "Shift_L"):
            print(event.keysym)

    # Ejecución de Parser
    def tytus_ejecutar(self):
        # Getting widget
        index = self.ta_input.index(self.ta_input.select())
        ta_input = self.array_tabs[index]

        # Delete old lexical report
        if os.path.exists("reports/error_lexical.txt"):
            os.remove("reports/error_lexical.txt")

        # Delete old syntactic report
        if os.path.exists("reports/error_syntactic.txt"):
            os.remove("reports/error_syntactic.txt")

        # Delete old semantic report
        if os.path.exists("reports/error_semantic.txt"):
            os.remove("reports/error_semantic.txt")

        if ta_input.compare("end-1c", "!=", "1.0"):
            # Gets new input
            tytus = ta_input.get(1.0, END)

            # Start parser
            ins = g.parse(tytus)
           ##g.analizar(tytus)
            st_global = st.SymbolTable()
            es_global = es.ListaErroresSemanticos()
            ct_global = ct.crearTabla()


            if not ins:
                messagebox.showerror("ERROR", "Ha ocurrido un error. Verificar reportes.")
            else:
                self.do_body(ins.getInstruccion(), st_global, es_global, ct_global)
                if es_global is Null:
                    self.raiz_ast = ins.getNodo()
                else:
                    messagebox.showerror("ERROR", "Verificar reporte semántico")
        else:
            messagebox.showerror("INFO", "El campo de entrada esta vacío.")

    # EJECUCIÓN DE ANÁLISIS - PARSER --------------------------
    def do_body(self, p_instruccion, p_st, es_global, ct_global):
        if not p_instruccion:
            messagebox.showerror("Tytus DB",
                                 "Ha ocurrido un problema en la ejecución del programa. Revisar los reportes de errores. ")
            return

        for inst in p_instruccion:
            if isinstance(inst, UseDatabase):
                self.do_use(inst, p_st, es_global)
            elif isinstance(inst, IfExist1):
                self.do_drop_db(inst, p_st, es_global)
            elif isinstance(inst, CreateDatabase):
                self.do_create_database(inst, p_st, es_global)
            elif isinstance(inst, Insert):
                self.do_insert_tb(inst, p_st, es_global)
            elif isinstance(inst, DropT):
                self.do_drop_tb(inst, p_st, es_global)
            elif isinstance(inst, CreateTable):
                self.do_create_tb(inst, p_st, es_global, ct_global)
            elif isinstance(inst, AlterDB):
                self.do_alter_db(inst,p_st,es_global)
            elif isinstance(inst, Select3):
                self.do_select(inst, p_st, es_global, ct_global)
            elif isinstance(inst, Show):
                self.do_show(inst, p_st, es_global, ct_global)
            else:
                print(inst)

        print("--- ANÁLISIS TERMINADO ---")

    # MODIFICACION NOMBRE BASE DE DATOS
    def do_alter_db(self, p_inst, p_st, p_es):
        key = 'CBD_' + p_inst.nombreDB
        existe = p_st.get(key)
        if existe:
            newDB = p_inst.operacion.cadena
            key = 'ADB_' + p_inst.nombreDB
            simbolo = st.Symbol(key, p_inst.nombreDB, 'Alter database', newDB)
            p_st.add(simbolo)
            alterDatabase(p_inst.nombreDB, newDB)

        else:
            error = es.errorSemantico('ADB_' + p_inst.nombreDB, 'La base de datos ' + p_inst.nombreDB + ' no existe')
            p_es.agregar(error)

        print('a')

    # USO DE BASE DE DATOS
    def do_use(self, p_inst, p_st, p_es):
        sKey = 'CBD_' + p_inst.nombre
        existe = p_st.get(sKey)
        if existe:
            simbolo = st.Symbol('UDB_' + p_inst.nombre, p_inst.nombre, 'use', '')
            p_st.add(simbolo)
            self.new_output("SE USARÁ LA BASE DE DATOS \'" + p_inst.nombre + "\'")
            self.use_db = p_inst.nombre
        else:
            error = es.errorSemantico('UDB_' + p_inst.nombre, 'La base de datos ' + p_inst.nombre + ' no existe')
            p_es.agregar(error)
            self.new_output(error.tipo)

    # CREACIÓN DE BASE DE DATOS
    def do_create_database(self, p_inst, p_st, p_es):
        key = 'CBD_' + p_inst.idData
        simbolo = st.Symbol(key, p_inst.idData, 'create', '')
        existe = p_st.get(key)
        if existe and p_inst.Replace:
            p_st.add(simbolo)
            createDatabase(p_inst.idData)
            self.new_output("BASE DE DATOS \'" + p_inst.idData + "\' HA SIDO CREADA EXITOSAMENTE.")
        elif existe and p_inst.IfNot:
            p_st.add(simbolo)
            createDatabase(p_inst.idData)
            self.new_output("BASE DE DATOS \'" + p_inst.idData + "\' HA SIDO CREADA EXITOSAMENTE.")
        elif not existe:
            p_st.add(simbolo)
            createDatabase(p_inst.idData)
            self.new_output("BASE DE DATOS \'" + p_inst.idData + "\' HA SIDO CREADA EXITOSAMENTE.")
        else:
            error = es.errorSemantico(key, 'La base de datos ' + p_inst.idData + ' ya existe')
            p_es.agregar(error)
            self.new_output(error.tipo)

    # ELIMINACIÓN DE BASE DE DATOS
    def do_drop_db(self, p_inst, p_st, p_es):
        sKey = 'CBD_' + p_inst.nombre
        existe = p_st.get(sKey)

        if existe:
            simbolo = st.Symbol('DDB_' + p_inst.nombre, p_inst.nombre, 'drop', '')
            p_st.add(simbolo)
            dropDatabase(p_inst.nombre)
            self.new_output("BASE DE DATOS \'" + p_inst.nombre + "\' HA SIDO ELIMINADA EXITOSAMENTE.")
        elif not existe and not p_inst.exist:
            error = es.errorSemantico('DDB_' + p_inst.nombre, 'La base de datos ' + p_inst.nombre + ' no existe')
            p_es.agregar(error)
            self.new_output(error.tipo)

    # CREACIÓN DE LISTADO DE TIPOS
    def do_create_type(self, p_inst, p_st):
        print('CREACIÓN DE LISTADO DE TIPOS')
        print('Nombre: ' + p_inst.nombre)
        print('Items: ' + str(p_inst.listado))
        print()

    # CREACIÓN DE TABLAS EN BASE DE DATOS
    def do_create_tb(self, p_inst, p_st, p_es, p_ct):
        list = []
        valor = 0
        for keys, value in p_st.symbols.items():
            if value.type == 'use':
                valor = 1
                list.append(value.id)

        if valor == 0:
            error = es.errorSemantico('CTB_' + p_inst.nombreTabla, 'No se ha seleccionado ninguna base de datos para crear la tabla ' + p_inst.nombreTabla)
            p_es.agregar(error)
            self.new_output(error.tipo)
        else:
            BDD = list.pop()
            cantCol = len(p_inst.atributos)
            nTB = p_inst.nombreTabla

        key = 'CTB_'+p_inst.nombreTabla+'_'+BDD

        existe = p_st.get(key)
        if existe:
            error = es.errorSemantico(key, 'La tabla ' + p_inst.nombreTabla + ' ya existe')
            p_es.agregar(error)
            self.new_output(error.tipo)
        else:
            simbolo = st.Symbol(key, p_inst.nombreTabla, 'create table', BDD)
            p_st.add(simbolo)
            createTable(BDD, nTB, cantCol)
            self.new_output("SE HA CREADO LA TABLA \'" + p_inst.nombreTabla + "\' EN BASE DE DATOS \'" + BDD + "\'.")

    # INSERTAR DATOS A TABLA EN BASE DE DATOS
    def do_insert_tb(self, p_inst, p_st, p_es):
        valor2 = 0
        list = []
        listI = []
        for keys, value in p_st.symbols.items():
            if value.id == p_inst.tabla:
                BDD = value.value

        for keys, value in p_st.symbols.items():
            if value.type == 'use':
                valor2 = 1
                list.append(value.id)

        if valor2 == 0:
            error = es.errorSemantico('ITB_' + p_inst.tabla, 'No se ha seleccionado ninguna base de datos para crear la tabla ' + p_inst.tabla)
            p_es.agregar(error)
        else:
            BDDU = list.pop()
            if BDDU == BDD:
                key = 'ITB_'+p_inst.tabla
                simbolo = st.Symbol(key, p_inst.tabla, 'insert table', BDD)
                p_st.add(simbolo)
                for val in p_inst.valores:
                    if isinstance(val,Numero) or isinstance(val,Decimal) or isinstance(val,bool) or isinstance(val,Cadena):
                        listI.append(val.valor)
                insert(BDD, p_inst.tabla,listI)
            else:
                error = es.errorSemantico('ITB_' + p_inst.tabla, 'La tabla ' + p_inst.tabla + ' no existe')
                p_es.agregar(error)

    # DROP A TABLAS EN BASE DE DATOS
    def do_drop_tb(self, p_inst, p_st, p_es):
        valor2 = 0
        list = []
        listI = []
        for keys, value in p_st.symbols.items():
            if value.id == p_inst.nombre:
                BDD = value.value

        for keys, value in p_st.symbols.items():
            if value.type == 'use':
                valor2 = 1
                list.append(value.id)
        if valor2 == 0:
            error = es.errorSemantico('DTB_' + p_inst.nombre, 'No se ha seleccionado ninguna base de datos para crear la tabla ' + p_inst.nombre)
            p_es.agregar(error)
            self.new_output(error.tipo)
        else:
            BDDU = list.pop()
            if BDDU == BDD:
                key = 'DTB_'+p_inst.nombre
                simbolo = st.Symbol(key, p_inst.nombre, 'drop table', BDD)
                p_st.add(simbolo)
                dropTable(BDD, p_inst.nombre)
                self.new_output("SE LA ELIMINADO LA TABLA \'" + p_inst.nombre + "\' EN LA BASE DE DATOS \'" + BDD + "\'.")
            else:
                error = es.errorSemantico('DTB_' + p_inst.tabla, 'La tabla ' + p_inst.tabla + ' no existe')
                p_es.agregar(error)
                self.new_output(error.tipo)

    # SHOW DATABASES
    def do_show(self, p_inst, p_st, es_global, ct_global):
        output = ""
        key = 1
        listado = showDatabases()

        for db in listado:
            output += str(key) + '. ' + str(db) + '\n'
            key += 1

        if output == "":
            self.new_output("-- NO HAY BASES DE DATOS CREADAS --")
        else:
            self.new_output(output)

    # SELECT A TABLAS EN BASE DE DATOS
    def do_select(self, p_inst, p_st, p_es, ct_global):
        valor2 = 0
        list = []

        for keys, value in p_st.symbols.items():
            if value.type == 'use':
                valor2 = 1
                list.append(value.id)
        if valor2 == 0:
            error = es.errorSemantico('SLT_', 'No se ha seleccionado ninguna base de datos para realizar el select')
            p_es.agregar(error)
            self.new_output(error.tipo)
        else:
            tablas_listado = []
            for keys, value in p_st.symbols.items():
                if value.value == self.use_db and value.type == 'create table':
                    tablas_listado.append(value.id)
                if value.value == self.use_db and value.type == 'drop table':
                    tablas_listado.remove(value.id)

            for table in p_inst.pfrom:
                ans = self.search_table(tablas_listado, table.valor)
                if ans is False:
                    error = es.errorSemantico('SLT_',
                                              'No se puede ejecutar la instrucción SELECT. Una de las tabla \'' + table.valor + '\' no existe en la base de datos.')
                    p_es.agregar(error)
                    self.new_output(error.tipo)
                    return

            if p_inst.valores == '*':
                out = ""
                for table in p_inst.pfrom:
                    output = extractTable(self.use_db, table.valor)
                    if len(output) > 0:
                        out += table.valor + '\n'
                        out += '---------------------------------------\n'
                        for item in output:
                            out += str(item) + '\n'
                        out += '\n'
                    else:
                        out += table.valor + '\n'
                        out += '---------------------------------------\n'
                        out += '... TABLA VACIA ...' + '\n\n'
                self.new_output(out)
            else:
                listado = []
                listado2 = []
                for col in p_inst.valores:
                    listado.append(col.valor.valor)

                for col in p_inst.valores:
                    if col.alias is None:
                        listado2.append(col.valor.valor)
                    else:
                        listado2.append(col.alias.valor)

                out = ""
                for table in p_inst.pfrom:
                    output = extractRow(self.use_db, table.valor, listado)
                    if len(output) > 0:
                        out += table.valor + '\n'
                        out += str(listado2) + '\n'
                        out += '---------------------------------------\n'
                        for item in output:
                            out += str(item) + '\n'
                        out += '\n'
                    else:
                        out += table.valor + '\n'
                        out += str(listado2) + '\n'
                        out += '---------------------------------------\n'
                        out += '... TABLA VACIA ...' + '\n\n'
                self.new_output(out)

    def search_table(self, listado, tabla):
        for item in listado:
            if item == tabla:
                return True
        return False


if __name__ == "__main__":
    main = Main()
    main.mainloop()