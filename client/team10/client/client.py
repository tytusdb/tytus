import os
import sys
import webbrowser
import platform
import socket
import sys
from tkinter import *
import tkinter as tk
from tkinter import ttk, font, messagebox
from datetime import date
from datetime import datetime

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_add = ('localhost', 10000)
print('connection to port=>', serv_add)
serv.connect(serv_add)


class cliente():

    def __init__(self, img_carpeta, iconos):
        # Prueba de conexion a base de datos
        message = 'data from client'
        print(message)
        serv.sendall(message.encode('utf-8'))

        recibido = 0
        esperado = len(message)

        while recibido < esperado:
            data = serv.recv(4096)
            recibido += len(data)
            print(data)

        # Creacion de la Ventana
        self.raiz = Tk()
        self.treeview = ttk.Treeview(self.raiz)

        '''
        iconos = (ruta_r + "pyremoto64x64.png",
              ruta_r + "conec16x16.png",
              ruta_r + "salir16x16.png",
              ruta_r + "star16x16.png",
              ruta_r + "conec32x32.png",
              ruta_r + "salir32x32.png",
              ruta_r + "grupo32x32.png", 
              ruta_r + "tytusdb.png",
              ruta_r + "open.png",
              ruta_r + "save.png",
              ruta_r + "serv.png") 
        '''

        # Definicion de Iconos
        self.img_carpeta = img_carpeta
        self.iconos = iconos
        self.PYREMOTO_ICON = PhotoImage(file=self.iconos[0])
        # icono2 = PhotoImage(file=self.iconos[1])
        # icono3 = PhotoImage(file=self.iconos[2])
        self.START_ICON = PhotoImage(file=self.iconos[3])
        self.CONNECT_ICON = PhotoImage(file=self.iconos[4])
        self.EXIT_ICON = PhotoImage(file=self.iconos[5])
        self.GRUPO_ICON = PhotoImage(file=self.iconos[6])
        self.TYTUS_ICON = PhotoImage(file=self.iconos[7])
        self.OPEN_ICON = PhotoImage(file=self.iconos[8])
        self.SAVE_ICON = PhotoImage(file=self.iconos[9])
        self.SERV_ICON = PhotoImage(file=self.iconos[10])
        self.BD_ICON = PhotoImage(file = self.iconos[11])
        self.TB_ICON = PhotoImage(file = self.iconos[12])
        self.COL_ICON = PhotoImage(file = self.iconos[13])

        # Preconfiguracion de la ventana

        self.raiz.title("TytusDB ")
        self.raiz.iconphoto(self.raiz, self.PYREMOTO_ICON)
        self.raiz.option_add("*Font", "Helvetica 12")
        self.raiz.option_add('*tearOff', True)
        self.raiz.attributes('-fullscreen', True)
        self.raiz.minsize(400, 300)
        self.fuente = font.Font(weight='normal')

        self.CFG_TIPOCONEX = IntVar()
        self.CFG_TIPOCONEX.set(1)
        self.CFG_TIPOEMUT = IntVar()
        self.CFG_TIPOEMUT.set(1)
        self.CFG_TIPOEXP = IntVar()
        self.CFG_TIPOEXP.set(1)

        self.estado = IntVar()
        self.estado.set(1)

        # Definicion del Menu
        barramenu = Menu(self.raiz)
        self.raiz['menu'] = barramenu
        self.fileMenu = Menu(barramenu)
        self.objectMenu = Menu(barramenu)
        self.toolsMenu = Menu(barramenu)
        self.aboutMenu = Menu(barramenu)
        barramenu.add_cascade(menu=self.fileMenu, label='FILE')
        barramenu.add_cascade(menu=self.objectMenu, label='OBJECT')
        barramenu.add_cascade(menu=self.toolsMenu, label='TOOLS')
        barramenu.add_cascade(menu=self.aboutMenu, label='ABOUT')

        # Programacion del Menu de Archivos
        self.fileMenu.add_command(label='   Abrir archivo *.sql', underline=0,
                                  image=self.OPEN_ICON, compound=LEFT, state="disabled")
        self.fileMenu.add_command(label='   Guardar archivo *.sql', underline=0,
                                  image=self.SAVE_ICON, compound=LEFT, state="disabled")

        # Programacion del Menu de Objetos

        # Programacion del Menu de Herramientas
        self.toolsMenu.add_command(
            label="Query Tool", command=self.f_query_tool, image=self.START_ICON, compound=LEFT)

        # Programacion del Menu de informacion
        self.aboutMenu.add_command(
            label="GRUPO 10", command=self.f_integrantes, image=self.GRUPO_ICON, compound=LEFT)
        self.aboutMenu.add_command(
            label="TytusDB", command=self.f_web, image=self.TYTUS_ICON, compound=LEFT)

        # Definicion de la Barra De Herramientas
        barraherr = Frame(self.raiz, relief=RAISED, bd=2, bg="#E5E5E5")
        barraherr.pack(side=TOP, fill=X)

        # Programacion del Boton de salida de la aplicacion
        bot2 = Button(barraherr, image=self.EXIT_ICON,  command=self.f_salir)
        bot2.pack(side=RIGHT, padx=1, pady=1)

        # Programacion del Boton de conexion a la base de datos
        bot1 = Button(barraherr, image=self.CONNECT_ICON,
                      command=self.f_conectar)
        bot1.pack(side=RIGHT, padx=2, pady=2)

        # Barra Inferior
        now = datetime.now()
        format = now.strftime(
            'Día :%d, Mes: %m, Año: %Y, Hora: %H, Minutos: %M, Segundos: %S')
        print(format)
        mensaje = " " + format
        self.barraest = Label(self.raiz, text=mensaje,
                              bd=1, relief=SUNKEN, anchor=W)
        self.barraest.pack(side=BOTTOM, fill=X)

        self.menucontext = Menu(self.raiz, tearoff=FALSE)
        self.menucontext.add_command(
            label="Salir", command=self.f_salir, compound=LEFT)

        # Definicion del Cuerpo de la Aplicacion
        # Cuerpo Principal
        cuerpo = Frame(self.raiz, relief=RAISED, bd=2, bg="blue")
        cuerpo.pack(side=BOTTOM, fill=BOTH, expand=True)

        # Cuerpo del Treeview
        treeFrame = LabelFrame(cuerpo,bg="white")
        treeFrame.config(bg='steelblue', width="300")
        treeFrame.pack(side=LEFT, fill=Y)
        style = ttk.Style(treeFrame)
        style.configure('Treeview', rowheight=40)
        self.treeview = ttk.Treeview(treeFrame, selectmode="extended")
        self.treeview.column("#0", anchor=W, width=300)
        
        item = self.treeview.insert("", tk.END, text="Server", image=self.SERV_ICON)
        for x in range(1, 5):
            item2 = self.treeview.insert(item, tk.END,text="Databases"+str(x),image=self.BD_ICON)
            item3 = self.treeview.insert(item2, tk.END, text="Tables",image=self.TB_ICON)
            for x in range(1, 5):
                item4 = self.treeview.insert(item3, tk.END, text="Tabla"+str(x),image=self.TB_ICON)
                for x in range(1, 4):
                    self.treeview.insert(item4, tk.END, text="Columna"+str(x),image=self.COL_ICON)
        self.treeview.pack(fill=BOTH, expand=True)

        # SubCuerpo
        SubCuerpo = LabelFrame(cuerpo, text='SubCuerpo')
        SubCuerpo.config(bg='yellow')
        SubCuerpo.pack(side=LEFT, fill=BOTH, expand=True)

        # QueryTool
        QueryTool = LabelFrame(SubCuerpo, text='QueryTool')
        QueryTool.config(bg='green', height="400")
        QueryTool.pack(side=TOP, fill=X)

        # Consola
        ConsoleTool = LabelFrame(SubCuerpo, text='Consola')
        ConsoleTool.config(bg='white')
        ConsoleTool.pack(side=BOTTOM, fill=BOTH, expand=True)

        # Ejecucion de la ventana
        self.raiz.mainloop()

    def f_query_tool(self):
        messagebox.showinfo(
            "Loading...", "DEBERA DEJAR EDITAR O MOSTRAR QUERY TOOL")

    def f_conectar(self):
        print("Conectando")

    def f_cambiaropc(self):
        self.objectMenu.entryconfig("Guardar", state="normal")

    def f_verestado(self):

        if self.estado.get() == 0:
            self.barraest.pack_forget()
        else:
            self.barraest.pack(side=BOTTOM, fill=X)

    def f_web(self):
        tytus = 'https://github.com/tytusdb/tytus'
        webbrowser.open_new_tab(tytus)

    def f_integrantes(self):
        messagebox.showinfo("INTEGRANTES", "BRANDON ALEXANDER VARGAS SARPEC     201709343\nALDO RIGOBERTO HERNÁNDEZ AVILA         201800585\nKEVIN ESTUARDO CARDONA LÓPEZ            201800596\nSERGIO FERNANDO MARTÍNEZ CABRERA   201801442\n")

    def f_acerca(self):
        acerca = Toplevel()
        acerca.geometry("320x200")
        acerca.resizable(width=False, height=False)
        acerca.title("Acerca de")
        marco1 = ttk.Frame(acerca, padding=(10, 10, 10, 10), relief=RAISED)
        marco1.pack(side=TOP, fill=BOTH, expand=True)
        etiq1 = Label(marco1, image=self.CONNECT_ICON, relief='raised')
        etiq1.pack(side=TOP, padx=10, pady=10, ipadx=10, ipady=10)
        etiq2 = Label(marco1, text="PyRemoto "+__version__,
                      foreground='blue', font=self.fuente)
        etiq2.pack(side=TOP, padx=10)
        etiq3 = Label(marco1, text="Python para impacientes")
        etiq3.pack(side=TOP, padx=10)
        boton1 = Button(marco1, text="Salir", command=acerca.destroy)
        boton1.pack(side=TOP, padx=10, pady=10)
        boton1.focus_set()
        acerca.transient(self.raiz)
        self.raiz.wait_window(acerca)

    def f_salir(self):
        print("connection close")
        serv.close()
        self.raiz.destroy()


def f_verificar_iconos(iconos):
    for icono in iconos:
        if not os.path.exists(icono):
            print('Icono no encontrado:', icono)
            return(1)
    return(0)


def main():
    ruta_relativa = os.getcwd()
    ruta_r = ruta_relativa + os.sep + "imagen" + os.sep

    iconos = (ruta_r + "pyremoto64x64.png",
              ruta_r + "conec16x16.png",
              ruta_r + "salir16x16.png",
              ruta_r + "star16x16.png",
              ruta_r + "conec32x32.png",
              ruta_r + "salir32x32.png",
              ruta_r + "grupo32x32.png",
              ruta_r + "tytusdb.png",
              ruta_r + "open.png",
              ruta_r + "save.png",
              ruta_r + "serv.png",
              ruta_r + "bd.png",
              ruta_r + "tb.png",
              ruta_r + "col.png"
              )
    error1 = f_verificar_iconos(iconos)

    if not error1:
        mi_app = cliente(ruta_r, iconos)
    return(0)


if __name__ == '__main__':
    main()
