from Instrucciones.TablaSimbolos.Instruccion import Instruccion

class JoinLeft(Instruccion):
    
    def __init__(self, valor, tipo, valor2, linea, columna):
        Instruccion.__init__(self,tipo,linea,columna, strGram)
        self.izq = valor
        self.der = valor2

    def ejecutar(self, tabla, arbol):
        super().ejecutar(tabla,arbol)


'''
instruccion = JoinLeft("hola mundo",None, 1,2)

instruccion.ejecutar(None,None)
'''