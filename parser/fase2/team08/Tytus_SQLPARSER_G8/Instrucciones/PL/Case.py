from Instrucciones.TablaSimbolos.Instruccion import Instruccion
from Instrucciones.TablaSimbolos.Tipo import Tipo_Dato
from Instrucciones.TablaSimbolos.Nodo3D import Nodo3D
from Instrucciones.TablaSimbolos.Arbol import Arbol
from Instrucciones.TablaSimbolos.Tabla import Tabla
from Instrucciones.Excepcion import Excepcion

class Case(Instruccion):
    def __init__(self, expresion2, instrucciones, strGram, linea, columna):
        Instruccion.__init__(self,None,linea,columna,strGram)
        self.expresion2 = expresion2 
        self.instrucciones = instrucciones

    def ejecutar(self, tabla, arbol):
        super().ejecutar(tabla,arbol)
        pass

    def analizar(self, tabla, arbol):
        super().analizar(tabla,arbol)
        for i in self.instrucciones:
            i.analizar(tabla, arbol)
        
        
    def traducir(self, tabla:Tabla, arbol:Arbol):
        super().traducir(tabla,arbol)
        retorno = Nodo3D()
        arbol.addc3d("# Inicia When")
    
        # Se traducen todas las funciones dentro del case
        for i in self.instrucciones:
            i.traducir(tabla, arbol)

        return