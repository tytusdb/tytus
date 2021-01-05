from Instrucciones.TablaSimbolos.Instruccion import Instruccion
from Instrucciones.TablaSimbolos.Tipo import Tipo_Dato, Tipo
from Instrucciones.Excepcion import Excepcion
from Instrucciones.Expresiones.Primitivo import Primitivo
class Div(Instruccion):
    def __init__(self, opIzq, opDer, strGram, linea, columna):
        Instruccion.__init__(self,Tipo(Tipo_Dato.NUMERIC),linea,columna,strGram)
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
            return int(resultadoIzq // resultadoDer)
        else:
            error = Excepcion('42883',"Semántico","el operador no existe: "+self.opIzq.tipo.toString()+" / "+self.opDer.tipo.toString(),self.linea,self.columna)
            arbol.excepciones.append(error)
            arbol.consola.append(error.toString())
            return error

    def analizar(self, tabla, arbol):
        pass

    def traducir(self, tabla, arbol):
        concatena ="DIV("
        if isinstance(self.opIzq, Primitivo):
            concatena += f"{self.opIzq.traducir(tabla,arbol).temporalAnterior}"
        concatena += ","
        if isinstance(self.opDer, Primitivo):
            concatena += f"{self.opDer.traducir(tabla,arbol).temporalAnterior}"

        concatena +=")"
        return concatena

