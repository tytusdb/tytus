import sys, os.path
nodo_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')) + '\\AST\\')
sys.path.append(nodo_dir)
from Nodo import Nodo


class Drop(Nodo):
    def __init__(self, nombreNodo,fila = -1 ,columna = -1 ,valor = None):
        Nodo.__init__(self,nombreNodo, fila, columna, valor)

    def execute(self,enviroment = None):
        #Se debe llamar al metodo showDatabases() -> list:
        pass


    def addChild(self, node):
        self.hijos.append(node)