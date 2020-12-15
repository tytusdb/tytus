#Imports

from graphviz import Digraph
from expresiones import *
from instrucciones import *
import tablasimbolos as TS

contador = 0
lista_instrucciones = []

class DOTAST: 

    def __init__(self):
        print("Generando el TextDot del AST")

    def getDot(self,instrucciones):
        global contador, TextDot, lista_instrucciones
        lista_instrucciones = instrucciones
        contador = 2
        TextDot = Digraph('AST', node_attr={'shape': 'box', 'style': 'filled','color': 'whitesmoke'}, edge_attr={'color':'blue'})
        TextDot.node('node1','INICIO')
        TextDot.node('node2','INSTRUCCIONES')
        TextDot.edge('node1','node2')
        tam = 0
        while tam < len(lista_instrucciones) :
            instruccion = lista_instrucciones[tam]

            if isinstance(instruccion, CrearBD):
                self.getTextDotCrearDB("node2",instruccion)
            elif isinstance(instruccion, CrearTabla):
                self.getTextDotCrearTabla("node2",instruccion)
            elif isinstance(instruccion,EliminarDB):
                self.getTextDotEliminarBD("node2",instruccion)
            elif isinstance(instruccion,CrearType):
                self.getTextDotCrearType("node2",instruccion)
            tam = tam +1
            print(TextDot)
        TextDot.view('reporte_AST', cleanup=True)


    #Creacion de base de datos
    def getTextDotCrearDB(self,padre,instr):
        global contador,TextDot
        contador=contador+1
        TextDot.node("node"+str(contador),"CREATE_BD")
        TextDot.edge(padre,"node"+str(contador))
        aux = "node"+str(contador)
        self.getTextDotExpresion(aux,instr.nombre)
        

    #Creacion de tabla 
    def getTextDotCrearTabla(self,padre,instr):
        global contador,TextDot
        contador = contador+1
        TextDot.node("node"+str(contador),"CREATE_TABLE")
        TextDot.edge(padre, "node"+str(contador))
        aux = "node"+str(contador)
        self.getTextDotNombreTabla(aux,instr)

        if instr.columnas != []:
            for ins in instr.columnas:
                if isinstance(ins, columnaTabla): 
                    self.getTextDotColumna(aux,ins)
              

    def getTextDotColumna(self,padre,instr):
        global contador,TextDot
        contador = contador+1
        TextDot.node("node"+str(contador),"DATOS_COLUMNA")
        TextDot.edge(padre, "node"+str(contador))
        aux = "node"+str(contador)
        self.getTextDotNombreColumna(aux,instr.id)
        self.getTextDotTipoDato(aux,instr)
        
    def getTextDotNombreTabla(self,padre,instr):
        global contador,TextDot
        contador = contador+1
        TextDot.node("node"+str(contador),"NOMBRE TABLA")
        TextDot.edge(padre, "node"+str(contador))
        aux = "node"+str(contador)
        self.getTextDotExpresion(aux,instr.nombre)    

    def getTextDotNombreColumna(self,padre,instr):
        global contador,TextDot
        contador = contador+1
        TextDot.node("node"+str(contador),"NOMBRE COLUMNA")
        TextDot.edge(padre, "node"+str(contador))
        aux = "node"+str(contador)
        self.getTextDotExpresion(aux,instr.id)

    def getTextDotTipoDato(self,padre,instr):
        global contador,TextDot
        contador = contador+1
        TextDot.node("node"+str(contador),"TIPO_DATO")
        TextDot.edge(padre, "node"+str(contador))
        aux = "node"+str(contador)
        self.getTextDotExpresion(aux,instr.tipo)
        #TextDot.node(aux,instr.tipo)

    #Creacion de type   
    def getTextDotCrearType(self,padre,instr):
        global contador,TextDot
        contador = contador+1
        TextDot.node("node"+str(contador),"CREATE_TYPE")
        TextDot.edge(padre, "node"+str(contador))
        aux = "node"+str(contador)
        self.getTextDotNombreType(aux,instr.nombre)

        '''if instr.valores != []:
            for indice, valor in enumerate(instr.valores):
                self.getTextDotListaType(aux.valor[indice])'''
              

    def getTextDotNombreType(self,padre,instr):
        global contador,TextDot
        contador = contador+1
        TextDot.node("node"+str(contador),"NOMBRE TYPE")
        TextDot.edge(padre, "node"+str(contador))
        aux = "node"+str(contador)
        self.getTextDotExpresion(aux,instr)
    
    def getTextDotListaType(self,padre,instr):
        global contador,TextDot
        contador = contador+1
        TextDot.node("node"+str(contador),"VALOR")
        TextDot.edge(padre, "node"+str(contador))
        aux = "node"+str(contador)
        self.getTextDotExpresion(aux,instr)


    #Eliminar database
    def getTextDotEliminarBD(self,padre,instr):
        global contador,TextDot
        contador = contador+1
        TextDot.node("node"+str(contador),"DROP_BD")
        TextDot.edge(padre, "node"+str(contador))
        aux = "node"+str(contador)
        self.getTextDotExpresion(aux,instr.nombre)

    #Expresiones resultantes 
    def getTextDotExpresion(self, padre, expresion):
        global contador, TextDot
        if isinstance(expresion, ExpresionIdentificador):
            contador = contador + 1
            TextDot.node("node" + str(contador), str(expresion.id))
            TextDot.edge(padre, "node" + str(contador))
        elif isinstance(expresion, ExpresionNumero):
            contador = contador + 1 
            TextDot.node("node" + str(contador), str(expresion.val))
            TextDot.edge(padre, "node" + str(contador))
        elif isinstance(expresion, ExpresionDobleComilla):
            contador = contador + 1
            TextDot.node("node"+str(contador),str(expresion.val))
            TextDot.edge(padre,"node"+str(contador))
        else:
            contador = contador + 1
            TextDot.node("node"+str(contador),str(expresion))
            TextDot.edge(padre,"node"+str(contador))

    