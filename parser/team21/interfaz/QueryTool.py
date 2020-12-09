# encoding: utf-8
import os
import sys
import tkinter as tk
from tkinter import ttk, font, messagebox, Image, filedialog
# from PIL import Image,ImageTk
# vscode://vscode.github-authentication/did-authenticate?windowId=1&code=31765953f382697fc389&state=b734c53a-ca11-4477-9538-dad90e23013c
class Ctxt(tk.Text):  # Custom Text Widget with Highlight Pattern   - - - - -
    # Credits to the owner of this custom class - - - - - - - - - - - - -
    def __init__(self,*args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        #tk.Text.configure('name','nuevo_0')

    def highlight_pattern(self, pattern, tag, start="1.0", end="end", regexp=False):
        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)
        count = tk.IntVar()
        while True:
            index = self.search(
                pattern, "matchEnd", "searchLimit", count=count, regexp=regexp
            )
            if index == "":
                break
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs, highlightthickness=2)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, fill="#FDFEFD")
            i = self.textwidget.index("%s+1line" % i)


class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """

    def __init__(self, widget, text='widget info'):

        self.waittime = 500  # miliseconds
        self.wraplength = 180  # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                         background="#ffffff", relief='solid', borderwidth=1,
                         wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()

# testing ...


class Application(ttk.Frame):
    def __init__(self, ventana, iconos):
        super().__init__(ventana)
        self.contadorN = 1
        self.Copiado = ""
        ventana.title("Query Tool")
        # anchoxAlto
        ventana.geometry("1200x700")
        # width, height
        ventana.resizable(False, False)
        ventana.iconbitmap("./Images/icono.ico")
        ventana.configure(background="RoyalBlue1")
        # cambiar icono
        menu = tk.Menu(ventana)

        new_item = tk.Menu(menu, tearoff=0)
        new_item.add_command(label="Cerrar Todo", command=self.f_CerrarTodo)
        new_item.add_command(label="Exit", command=self.f_exit)
        menu.add_cascade(label='Archivo', menu=new_item)

        new_item2 = tk.Menu(menu, tearoff=0)
        new_item2.add_command(label="Nuevo", command=self.f_nuevaPestania)
        new_item2.add_command(label="Abrir", command=self.f_abrir)
        new_item2.add_command(label="Guardar", command=self.f_guardar)
        new_item2.add_command(label="Guardar Como", command=self.f_guardarcomo)
        menu.add_cascade(label='Project', menu=new_item2)

        new_item3 = tk.Menu(menu, tearoff=0)
        new_item3.add_command(
            label="Copiar", accelerator="Ctrl+c", command=lambda: self.tab_control.event_generate('<Control-c>'))
        new_item3.add_command(label="Cortar", accelerator="Ctrl+x",
                              command=lambda: self.tab_control.event_generate('<Control-x>'))
        new_item3.add_command(label="Pegar", accelerator="Ctrl+v",
                              command=lambda: self.tab_control.event_generate('<Control-v>'))
        menu.add_cascade(label='Edit', menu=new_item3)

        new_item4 = tk.Menu(menu, tearoff=0)
        new_item4.add_command(label="Correr", command=self.f_correr)
        menu.add_cascade(label='Programa', menu=new_item4)

        new_item5 = tk.Menu(menu, tearoff=0)
        new_item5.add_command(label="Acerca")
        menu.add_cascade(label='Ayuda', menu=new_item5)

        # barra de herramientas----------------------------------------------------------------

        BarraH = tk.Frame()
        BarraH.config(bg="DodgerBlue4", relief=tk.RAISED, height="100", bd=2)

        imgBoton1 = tk.PhotoImage(file=iconos[0])
        bot1 = tk.Button(BarraH, image=imgBoton1,
                         height=50, width=50, command=self.f_CerrarTodo)
        bot1.pack(side=tk.LEFT, padx=3, pady=3)
        button1_ttp = CreateToolTip(bot1, 'CERRAR TODO')

        imgBoton2 = tk.PhotoImage(file=iconos[1])
        bot2 = tk.Button(BarraH, image=imgBoton2,
                         height=50, width=50, command=self.f_nuevaPestania)
        bot2.pack(side=tk.LEFT, padx=3, pady=3)
        button2_ttp = CreateToolTip(bot2, 'NUEVO')

        imgBoton3 = tk.PhotoImage(file=iconos[2])
        bot3 = tk.Button(BarraH, image=imgBoton3,
                         height=50, width=50, command=self.f_abrir)
        bot3.pack(side=tk.LEFT, padx=3, pady=3)
        button3_ttp = CreateToolTip(bot3, 'ABRIR')

        imgBoton4 = tk.PhotoImage(file=iconos[3])
        bot4 = tk.Button(BarraH, image=imgBoton4,
                         height=50, width=50, command=self.f_guardar)
        bot4.pack(side=tk.LEFT, padx=3, pady=3)
        button4_ttp = CreateToolTip(bot4, 'GUARDAR')

        imgBoton5 = tk.PhotoImage(file=iconos[4])
        bot5 = tk.Button(BarraH, image=imgBoton5,
                         height=50, width=50, command=self.f_guardarcomo)
        bot5.pack(side=tk.LEFT, padx=3, pady=3)
        button5_ttp = CreateToolTip(bot5, 'GUARDAR COMO')

        imgBoton6 = tk.PhotoImage(file=iconos[5])
        bot6 = tk.Button(BarraH, image=imgBoton6,
                         height=50, width=50, command=self.f_correr)
        bot6.pack(side=tk.LEFT, padx=3, pady=3)
        button6_ttp = CreateToolTip(bot6, 'RUN')

        imgBoton7 = tk.PhotoImage(file=iconos[6])
        bot7 = tk.Button(BarraH, image=imgBoton7,
                         height=50, width=50, command="")
        bot7.pack(side=tk.LEFT, padx=3, pady=3)
        button7_ttp = CreateToolTip(bot7, 'START DEBBUGING')

        imgBoton8 = tk.PhotoImage(file=iconos[7])
        bot8 = tk.Button(BarraH, image=imgBoton8,
                         height=50, width=50, command="")
        bot8.pack(side=tk.LEFT, padx=3, pady=3)
        button8_ttp = CreateToolTip(bot8, 'NEXT')

        # PESTAniAS ----------------------------------------------------------------------------
        PanelPestania = tk.Frame()
        PanelPestania.config(
            bg="SteelBlue1", relief=tk.RAISED, width="700", bd=2)

        self.tab_control = ttk.Notebook(PanelPestania)
        self.tab_control.config(width="600")
        tab1 = ttk.Frame(self.tab_control, name='f_0')
        self.tab_control.add(tab1, text='nuevo_0')
        self.tab_control.pack(expand=1, fill='both')

        S1 = tk.Scrollbar(tab1)
        numberLines = TextLineNumbers(tab1, width=40, bg='#313335')
        #T1 = tk.Text(tab1, bg="white", name='nuevo_0')
        T1 = Ctxt(tab1)
        numberLines.attach(T1)
        S1.pack(side=tk.RIGHT, fill=tk.Y)
        numberLines.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        T1.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        S1.config(command=T1.yview)
        T1.config(yscrollcommand=S1.set)

        T1.tag_config("green", foreground="green")
        T1.highlight_pattern("\mread\M", "green", regexp=True)
        

        # self.f_crearTag(0)
        def onScrollPress(event):
            S1.bind("<B1-Motion>", numberLines.redraw)

        def onScrollRelease(event):
            S1.unbind("<B1-Motion>", numberLines.redraw)

        def onPressDelay(event):
            self.after(2,numberLines.redraw)
            self.after(2, T1.highlight_pattern("(\/\*(\w|\s)*\*\/)", "green", regexp=True))

        T1.bind("<Key>", onPressDelay)
        T1.bind("<Button-1>", numberLines.redraw)
        S1.bind("<Button-1>", onScrollPress)
        T1.bind("<MouseWheel>", onPressDelay)

        

        # CONSOLA-------------------------------------------------------------------------------
        Consola = tk.Frame()
        Consola.config(bg="SteelBlue1", relief=tk.RAISED, width="700", bd=2)

        S = tk.Scrollbar(Consola)
        self.T = tk.Text(Consola, height=4, width=50, bg="black", fg="chartreuse2")
        S.pack(side=tk.RIGHT, fill=tk.Y)
        self.T.pack(side=tk.LEFT, fill=tk.Y)
        S.config(command=self.T.yview)
        self.T.config(yscrollcommand=S.set)
        quote = """>>>\n"""
        self.T.insert(tk.END, quote)
        # menucontextual----------------------------------------------
        menuContext = tk.Menu(self.tab_control, tearoff=0)
        menuContext.add_command(label="Cerrar", command=self.f_cerrarPestania)
        # eventos-----------------------------------------------------

        def f_key(event):
            if(event.keycode == 13):
                T.insert(tk.END, """>>>""")

        def f_mostrarContext(event):
            menuContext.post(event.x_root, event.y_root)

        self.T.bind("<Key>", f_key)
        ventana.bind("<Button-3>", f_mostrarContext)

        # metodos extras-------------------------------------------------------

        BarraH.pack(side=tk.TOP, fill=tk.X)
        PanelPestania.pack(side=tk.LEFT, fill=tk.Y, pady=10, padx=10)
        Consola.pack(side=tk.LEFT, fill=tk.Y, pady=10, padx=10)
        ventana.config(menu=menu)
        ventana.mainloop()

    def f_cerrarPestania(self):

        # if(tab_control.tab(tab_control.select(), "text")) == "Nuevo":
        respuesta = messagebox.askyesno(title="", message="¿Desea cerrar esta pestania sin guardar?")

        if(respuesta):
            self.tab_control.forget(self.tab_control.select())
        else:
            if self.tab_control.tab(self.tab_control.select(), "text")[0] != '/':
                self.f_guardarcomo()
                self.tab_control.forget(self.tab_control.select())
            else:
                # guardar
                self.f_guardar()
                self.tab_control.forget(self.tab_control.select())
                print("debemos guardarlo")

    def f_nuevaPestania(self):
        tab1 = ttk.Frame(self.tab_control, name="f_"+str(self.contadorN))
        self.tab_control.add(tab1, text='nuevo_'+str(self.contadorN))
        # self.tab_control.pack(expand=1, fill='both')
        S1 = tk.Scrollbar(tab1)
        numberLines = TextLineNumbers(tab1, width=40, bg='#313335')
        #T1 = tk.Text(tab1, bg="white")
        T1 = Ctxt(tab1)
        numberLines.attach(T1)
        S1.pack(side=tk.RIGHT, fill=tk.Y)
        numberLines.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        T1.pack(side=tk.LEFT, fill='both')

        S1.config(command=T1.yview)
        T1.config(yscrollcommand=S1.set)

        T1.tag_config("green", foreground="green")
        T1.highlight_pattern("\mread\M", "green", regexp=True)
        

        def onScrollPress(event):
            S1.bind("<B1-Motion>", numberLines.redraw)

        def onScrollRelease(event):
            S1.unbind("<B1-Motion>", numberLines.redraw)

        def onPressDelay(event):
            self.after(2,numberLines.redraw)
            self.after(2, T1.highlight_pattern("(\/\*(\w|\s)*\*\/)", "green", regexp=True))

        T1.bind("<Key>", onPressDelay)
        T1.bind("<Button-1>", numberLines.redraw)
        S1.bind("<Button-1>", onScrollPress)
        T1.bind("<MouseWheel>", onPressDelay)

        self.f_crearTag(self.contadorN)
        self.contadorN = self.contadorN+1
        idtab = self.tab_control.index("end")-1
        self.tab_control.select(idtab)
        return self.contadorN-1
        # print(str(self.tab_control.index(tk.END)))

    def f_crearTag(self, idd):
        # self.text.tag_config("start", background="black", foreground="yellow")
        tabActual = "nuevo_"+str(idd)
        if tabActual[0] != '/':
            try:
                self.tab_control.children[tabActual.replace("nuevo", "f")].children[tabActual].tag_config(
                    "find", background="blue", foreground="white")
            except:
                print("")
        else:
            try:
                self.tab_control.children[tabActual].children[tabActual].tag_config(
                    "find", background="blue", foreground="white")
            except:
                self.Copiado = ""

    def f_guardarcomo(self):
        filename = filedialog.asksaveasfilename(
            initialdir="./", title="Guardar Como")

        tabActual = self.tab_control.tab(tk.CURRENT)['text']
        if self.tab_control.tab(self.tab_control.select(), "text")[0] != '/':
            Contenido = self.tab_control.children[tabActual.replace(
                "nuevo", "f")].winfo_children()[2].get("1.0", tk.END)
        else:
            # guardar
            Contenido = self.tab_control.children[tabActual].winfo_children()[2].get("1.0", tk.END)

        # escribir nuevo archivo con filename y contenido
        self.WriteFile(filename, Contenido)
        x = filename.split("/")

        # dictionary[new_key] = dictionary.pop(old_key)

        messagebox.showinfo(title="Guardar Como",
                            message="ARCHIVO GUARDADO CON ÉXITO")

    def f_guardar(self):
        tabActual = self.tab_control.tab(tk.CURRENT)['text']
        #
        if tabActual[0] != '/':
            self.f_guardarcomo()
        else:
            filename = "./pruebas/" + tabActual
            Contenido = self.tab_control.children[tabActual].winfo_children()[2].get("1.0", tk.END)
            # escribir nuevo archivo con filename y contenido
            self.WriteFile(filename, Contenido)
            messagebox.showinfo(title="Guardar",
                                message="ARCHIVO GUARDADO CON ÉXITO")

    def f_abrir(self):

        try:
            with filedialog.askopenfile(initialdir="./", title="Abrir Archivo") as f:
                Contenido = f.read()
                x = (f.name).split("/")
                name = "/"+x[len(x)-1]

                tabs = self.f_nuevaPestania()

                idtab = self.tab_control.index("end")-1
                self.tab_control.select(idtab)

                print(tabs)
                print(self.tab_control.children["f_"+str(tabs)].winfo_children()[2])
                
                # insertar texto
                self.tab_control.children["f_"+str(tabs)].winfo_children()[2].insert(
                    tk.END, Contenido)

        except:
            print("no hacer nada")

    def WriteFile(self, filename, Content):
        try:
            file = open(filename, "w")
            file.write(Content)

        finally:
            file.close()

    def f_CerrarTodo(self):
        print(self.tab_control.index("end"))
        while self.tab_control.index("end") > 0:
            self.tab_control.select(0)
            self.f_cerrarPestania()

    def f_exit(self):
        if self.tab_control.index("end") > 0:
            self.f_CerrarTodo()
            sys.exit()
        else:
            sys.exit()

    def f_parsear(self,texto):
        self.T.insert(tk.END, texto)
        print(texto)


    def f_correr(self):
        lista = []
        tabActual = self.tab_control.tab(tk.CURRENT)['text']
        if tabActual[0] != '/':
            texto = self.tab_control.children[tabActual.replace(
                "nuevo", "f")].winfo_children()[2].get("1.0", tk.END)
            start = 0
            return self.f_parsear(texto)
        else:
            texto = self.tab_control.children[tabActual].winfo_children()[2].get("1.0", tk.END).get(
                "1.0", tk.END)
            start = 0
            return self.f_parsear(texto)

    
        




def main():

    ventana = tk.Tk()

    # INICIALIZAR VARIABLES CON RUTAS

    app_carpeta = os.getcwd()
    img_carpeta = app_carpeta + os.sep + "Images" + os.sep

    # DECLARAR Y VERIFICAR ICONOS DE LA APLICACIÓN:

    iconos = (img_carpeta + "cerrar.png",
              img_carpeta + "nuevo.png",
              img_carpeta + "abrir.png",
              img_carpeta + "guardar.png",
              img_carpeta + "guardar_como.png",
              img_carpeta + "play.png",
              img_carpeta + "debug.png",
              img_carpeta + "next.png"
              )
    app = Application(ventana, iconos)


if __name__ == '__main__':
    main()
