from Instrucciones.TablaSimbolos.Instruccion import Instruccion

class OrderBy(Instruccion):
    def __init__(self, valor, tipo, linea, columna):
        Instruccion.__init__(self,tipo,linea,columna)
        self.valor = valor

    def ejecutar(self, tabla, arbol):
        super().ejecutar(tabla,arbol)
        print("ORDER BY")
        
'''
instruccion = OrderBy("hola mundo",None, 1,2)

instruccion.ejecutar(None,None)
'''