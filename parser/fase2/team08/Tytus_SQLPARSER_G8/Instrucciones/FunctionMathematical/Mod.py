from Instrucciones.Expresiones.Aritmetica import Aritmetica
import math
from Instrucciones.TablaSimbolos.Instruccion import Instruccion
from Instrucciones.TablaSimbolos.Tipo import Tipo_Dato, Tipo
from Instrucciones.Excepcion import Excepcion

class Mod(Instruccion):
    def __init__(self, opIzq, opDer, strGram, linea, columna):
        Instruccion.__init__(self,None,linea,columna,strGram)
        self.opIzq = opIzq
        self.opDer = opDer

    def ejecutar(self, tabla, arbol):
        super().ejecutar(tabla,arbol)
        # Si existe algún error en el operador izquierdo, retorno el error.
        resultadoIzq = self.opIzq.ejecutar(tabla, arbol)
        if isinstance(resultadoIzq, Excepcion):
            return resultadoIzq
        # Si existe algún error en el operador derecho, retorno el error.
        resultadoDer = self.opDer.ejecutar(tabla, arbol)
        if isinstance(resultadoDer, Excepcion):
            return resultadoDer
        if (self.opIzq.tipo.tipo == Tipo_Dato.INTEGER or self.opIzq.tipo.tipo == Tipo_Dato.DOUBLE_PRECISION or self.opIzq.tipo.tipo == Tipo_Dato.NUMERIC) and (self.opDer.tipo.tipo == Tipo_Dato.INTEGER or self.opDer.tipo.tipo == Tipo_Dato.DOUBLE_PRECISION or self.opDer.tipo.tipo == Tipo_Dato.NUMERIC):
            if resultadoDer == 0:
                error = Excepcion('42883',"Semántico","No se puede dividir entre cero",self.linea,self.columna)
                arbol.excepciones.append(error)
                arbol.consola.append(error.toString())
                return error
            if isinstance(resultadoIzq, int) and isinstance(resultadoDer, int):
                self.tipo = Tipo(Tipo_Dato.DOUBLE_PRECISION)
                return int(math.fmod(resultadoIzq,resultadoDer))
            else:
                self.tipo = Tipo(Tipo_Dato.NUMERIC)
                return math.fmod(resultadoIzq,resultadoDer)           
        else:
            error = Excepcion('42883',"Semántico","No existe la función mod("+self.opIzq.tipo.toString()+", "+self.opDer.tipo.toString()+")",self.linea,self.columna)
            arbol.excepciones.append(error)
            arbol.consola.append(error.toString())
            return error
        
    def analizar(self, tabla, arbol):
        pass

    def traducir(self, tabla, arbol):
        cadena ="MOD("
        if(isinstance(self.opIzq, Aritmetica)):
            cadena += f"{self.opIzq.concatenar(tabla,arbol)}"
        else:
            cadena += f"{self.opIzq.traducir(tabla,arbol).temporalAnterior}"
        cadena+= ","
        if(isinstance(self.opDer, Aritmetica)):
            cadena += f"{self.opDer.concatenar(tabla,arbol)}"
        else:
            cadena += f"{self.opDer.traducir(tabla,arbol).temporalAnterior}"
        cadena += ")"
        return cadena

'''
instruccion = Mod(12.5, 5.5, None, 1,2)
instruccion.ejecutar(None,None)
'''