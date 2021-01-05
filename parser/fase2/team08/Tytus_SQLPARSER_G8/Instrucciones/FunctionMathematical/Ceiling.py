
import math
from Instrucciones.TablaSimbolos.Instruccion import Instruccion
from Instrucciones.TablaSimbolos.Tipo import Tipo_Dato, Tipo
from Instrucciones.Excepcion import Excepcion

class Ceiling(Instruccion):
    def __init__(self, valor, linea, columna):
        Instruccion.__init__(self,None,linea,columna,strGram)
        self.valor = valor

    def ejecutar(self, tabla, arbol):
        super().ejecutar(tabla,arbol)
        resultado = self.valor.ejecutar(tabla,arbol)
        if self.valor.tipo.tipo != Tipo_Dato.SMALLINT and self.valor.tipo.tipo != Tipo_Dato.INTEGER and self.valor.tipo.tipo != Tipo_Dato.BIGINT and self.valor.tipo.tipo != Tipo_Dato.DECIMAL and self.valor.tipo.tipo != Tipo_Dato.NUMERIC and self.valor.tipo.tipo != Tipo_Dato.REAL and self.valor.tipo.tipo != Tipo_Dato.DOUBLE_PRECISION:
            error = Excepcion('42883',"Semántico","No existe la función ceiling("+self.valor.tipo.toString()+")",self.linea,self.columna)
            arbol.excepciones.append(error)
            arbol.consola.append(error.toString())
            return error
        '''
        if resultado < 0:
            error = Excepcion('2201F',"Semántico","La función CEILING únicamente acepta valores númericos positivos",self.linea,self.columna)
            arbol.excepciones.append(error)
            arbol.consola.append(error.toString())
            return error
        '''
        if isinstance(resultado,int):
            self.tipo = Tipo(Tipo_Dato.DOUBLE_PRECISION)
            return math.ceil(resultado)
        else:
            self.tipo = Tipo(Tipo_Dato.NUMERIC)
            return math.ceil(resultado)
            
    def analizar(self, tabla, arbol):
        pass

    def traducir(self, tabla, arbol):
        
        retorno = self.valor.traducir(tabla,arbol)
        #print(retorno.temporalAnterior)
        #print(type(self.valor))
        #print(self.valor.opIzq.traducir(tabla,arbol).temporalAnterior)
        return f"CEILING({self.valor.traducir(tabla,arbol).temporalAnterior})"
