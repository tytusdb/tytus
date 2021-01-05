from Instrucciones.Identificador import Identificador
from Instrucciones.TablaSimbolos.Tipo import Tipo, Tipo_Dato
from Instrucciones.Expresiones.Primitivo import Primitivo
from Instrucciones.TablaSimbolos.Instruccion import Instruccion
from Instrucciones.Excepcion import *
import base64
class Encode(Instruccion):
    def __init__(self, valor, tipo, codificacion, strGram, linea, columna):
        Instruccion.__init__(self,tipo,linea,columna, strGram)
        self.valor = valor
        self.codificacion = codificacion

    def ejecutar(self, tabla, arbol):
        super().ejecutar(tabla,arbol)
        resultado = self.valor.ejecutar(tabla,arbol)
        if isinstance(resultado, Excepcion):
            return resultado
        if self.valor.tipo.tipo== Tipo_Dato.CHAR or self.valor.tipo.tipo== Tipo_Dato.CHARACTER or self.valor.tipo.tipo== Tipo_Dato.TEXT:
            if str(self.codificacion.valor)=='base64':
                message_bytes = resultado.encode('ascii')
                base64_bytes = base64.b64encode(message_bytes)
                base64_message = base64_bytes.decode('ascii')
                resultado=base64_message
                self.tipo = Tipo(Tipo_Dato.TEXT)
                return resultado
            if str(self.codificacion.valor)=='hex':
                self.tipo = Tipo(Tipo_Dato.TEXT)
                return str(resultado).encode("utf-8").hex()

        error = Excepcion('22023',"Semántico",f"No se reconoce la codificación{self.valor.tipo.toString()})",self.linea,self.columna)
        arbol.excepciones.append(error)
        #arbol.consola.append("HINT: Ninguna función coincide en el nombre y tipos de argumentos. Puede ser necesario agregar conversión explícita de tipos.")
        arbol.consola.append(error.toString())
        return error        
'''
instruccion = Encode("hola mundo",None, 1,2)

instruccion.ejecutar(None,None)
'''