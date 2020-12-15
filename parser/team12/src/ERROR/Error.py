from enum import Enum

class Tipo(Enum):
    LEXICO = 1
    SINTACTICO = 2
    SEMANTICO = 3

class Error():
    def __init__(self, tipo : Tipo, descripcion, linea):
        self.tipo = tipo
        self.descripcion = descripcion
        self.linea = linea

