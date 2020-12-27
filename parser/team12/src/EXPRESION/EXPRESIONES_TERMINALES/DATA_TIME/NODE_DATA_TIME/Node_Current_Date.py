import sys, os
import datetime

nodo_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','..')) + '\\EXPRESION\\')
sys.path.append(nodo_dir)

nodo_ast = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','..','..')) + '\\ENTORNO\\')
sys.path.append(nodo_ast)

from Expresion import Expresion
from Tipo import Data_Type
from Tipo_Expresion import Type_Expresion

class Current_Date_Expresion(Expresion):
    
    def __init__(self, nombreNodo, fila, columna, valor):
        Expresion.__init__(self, nombreNodo, fila, columna, valor)
        self.tipo = Data_Type.non
    
    def execute(self, eviroment):
        
        self.tipo = Type_Expresion(Data_Type.data_time)
        self.valorExpresion = datetime.date.today()
        return self.valorExpresion