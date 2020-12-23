from Instrucciones.TablaSimbolos.Instruccion import Instruccion
from Instrucciones.TablaSimbolos.Tipo import Tipo_Dato, Tipo

class Enum(Instruccion):
    def __init__(self, id, tipo, linea, columna):
        Instruccion.__init__(self,Tipo(Tipo_Dato.CHAR),linea,columna)
        self.id = id
        self.listaValores = []

    def ejecutar(self, tabla, arbol):
        super().ejecutar(tabla,arbol)
        return self.valor