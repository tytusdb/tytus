import TypeCheck.ListaAtributos as ListaAtributos
import TypeCheck.ListaConstraints as ListaConstraints

class Tabla:
    def __init__(self,nombreTabla:str):
        self.nombreTabla = nombreTabla
        self.listaAtributos = ListaAtributos.ListaAtributos()
        self.listaConstraints = ListaConstraints.ListaConstraints()
        #Punteros
        self.siguiente = None
        self.anterior = None
