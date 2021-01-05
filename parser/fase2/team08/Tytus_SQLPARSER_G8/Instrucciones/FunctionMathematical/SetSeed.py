import math
import random
from Instrucciones.TablaSimbolos.Instruccion import Instruccion

class SetSeed(Instruccion):
    def __init__(self, valor, tipo, strGram, linea, columna):
        Instruccion.__init__(self,tipo,linea,columna, strGram)
        self.valor = valor

    def ejecutar(self, tabla, arbol):
        super().ejecutar(tabla,arbol)
        #print(random.seed(self.valor))
        arbol.consola.append('Función en proceso...')

    def analizar(self, tabla, arbol):
        pass

    def traducir(self, tabla, arbol):
        
        retorno = self.valor.traducir(tabla,arbol)
        #print(retorno.temporalAnterior)
        #print(type(self.valor))
        #print(self.valor.opIzq.traducir(tabla,arbol).temporalAnterior)
        return f"SETSEED({self.valor.traducir(tabla,arbol).temporalAnterior})"