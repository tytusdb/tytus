from Instrucciones.TablaSimbolos.Instruccion import Instruccion

class Encode(Instruccion):
    def __init__(self, valor, tipo, linea, columna):
        Instruccion.__init__(self,tipo,linea,columna)
        self.valor = valor

    def ejecutar(self, tabla, arbol):
        super().ejecutar(tabla,arbol)
        print("ENCODE")
        #print(self.valor.encode('base64','strict'))
        #return self.valor.encode('base64','strict')
'''
instruccion = Encode("hola mundo",None, 1,2)

instruccion.ejecutar(None,None)
'''