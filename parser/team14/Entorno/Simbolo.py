from Entorno.TipoSimbolo import TipoSimbolo

class Simbolo:
    def __init__(self, tipo = "", nombre = "", valor = None, linea = 0):
        self.tipo = tipo
        self.nombre = nombre
        self.valor = valor
        self.linea = linea
        self.atributos = {}
        self.baseDatos = ""
        self.tabla = ""
    
    def toString(self):
        if self.nombre != None:
            print(self.tipo, ";", self.nombre, ";", self.valor, ";", self.baseDatos, ";", self.tabla)
        