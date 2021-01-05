class Instruccion:
    '''This is an abstract class'''

class Principal(Instruccion):
    def __init__(self, instrucciones):
        self.instrucciones = instrucciones

class Declaracion(Instruccion):
    def __init__(self, id, exp):
        self.id = id
        self.exp = exp

class ListaDeclaraciones(Instruccion):
    def __init__(self, tipo, declaraciones):
        self.tipo = tipo
        self.declaraciones = declaraciones

class Asignacion(Instruccion):
    def __init__(self, id, exp):
        self.id = id
        self.exp = exp

class Impresion(Instruccion):
    def __init__(self, impresiones):
        self.impresiones = impresiones

class Etiqueta(Instruccion):
    def __init__(self, id):
        self.id = id

class Salto(Instruccion):
    def __init__(self, id):
        self.id = id

class SentenciaIf(Instruccion):
    def __init__(self, exp, si, sino):
        self.exp = exp
        self.si = si
        self.sino = sino

class SentenciaCase(Instruccion):
    def __init__(self, exp, casos):
        self.exp = exp
        self.casos = casos

class Caso(Instruccion):
    def __init__(self, exp, sentencias):
        self.exp = exp
        self.sentencias = sentencias

class Funcion(Instruccion):
    def __init__(self, tipo, id, parametros, instrucciones):
        self.tipo = tipo
        self.id = id
        self. parametros = parametros
        self.instrucciones = instrucciones

class LlamadaFuncion(Instruccion):
    def __init__(self, id, parametros):
        self.id = id
        self.parametros = parametros

class Parametro(Instruccion):
    def __init__(self, tipo, id):
        self.tipo = tipo
        self.id = id





