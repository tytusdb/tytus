from abstract.instruccion import *
from tools.console_text import *
from tools.tabla_tipos import *

class create_column(instruccion):

    def __init__(self, id_column, type_, condicion, line, column, num_nodo):
        super().__init__(line, column)
        self.id_column = id_column
        self.type_ = type_
        self.condicion = condicion

        #Nodo AST Create Column
        self.nodo = nodo_AST('COLUMN', num_nodo)
        self.nodo.hijos.append(nodo_AST(id_column, num_nodo+1))

        self.nodo.hijos.append(nodo_AST(type_, num_nodo+2))

        if condicion != None:
            for cond in condicion:
                self.nodo.hijos.append(cond.nodo)


    def ejecutar(self):
        pass