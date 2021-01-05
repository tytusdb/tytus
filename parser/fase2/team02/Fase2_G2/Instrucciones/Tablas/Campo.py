from Instrucciones.TablaSimbolos.Instruccion import Instruccion
from Instrucciones.Expresiones.Primitivo import Primitivo
from storageManager.jsonMode import *

class Campo():
    'Esta clase se utiliza para crear un campo'
    def __init__(self, nombre, tipo, pk, orden, constraint):
        self.nombre = nombre
        self.tipo = tipo
        self.pk = pk
        self.orden = orden
        self.constraint = constraint  #LISTA DE CONSTRAINT
    
    def obtenerNombre(self):
        return self.nombre