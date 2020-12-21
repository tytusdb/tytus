from Entorno.Simbolo import Simbolo

class Entorno:
    def __init__(self, anterior = None):
        self.anterior = anterior
        self.database = "" 
        self.tablaSimbolo = {}
        self.consola = []

    def nuevoSimbolo(self, symbol):
        x = self.tablaSimbolo.get(symbol.nombre)

        if x == None:
            self.tablaSimbolo[symbol.nombre] = symbol
            return "ok"
        
        return str("El simbolo " + symbol.nombre + " no se puede agregar porque ya existe")

    def editarSimbolo(self, identificador, nuevo):
        x = self.tablaSimbolo.get(identificador)

        if x != None:
            self.tablaSimbolo[identificador] = nuevo
            return "ok"
        
        return str("El simbolo " + identificador + " no se puede modificar porque no existe")
    
    def eliminarSimbolo(self, identificador):
        x = self.tablaSimbolo.get(identificador)

        if x != None:
            del self.tablaSimbolo[identificador]
            return "ok"
        
        return str("el simbolo " + identificador + " no se puede eliminar porque no existe")
    
    def buscarSimbolo(self, identificador):
        ent = self

        while ent != None:
            x = ent.tablaSimbolo.get(identificador)
            if x != None:
                return x
            ent = ent.anterior
        
        return None

    def mostrarSimbolos(self):
        ent = self

        #nombre,tipoSym,baseDatos,tabla,valor
        salida = "digraph G {shortName [shape=record label=<<TABLE><TR><TD>NOMBRE</TD><TD>TIPO</TD><TD>BASE DE DATOS</TD><TD>TABLA</TD><TD>VALOR</TD></TR>"
        while ent != None:
            for x in ent.tablaSimbolo.values():
                if x != None:
                    salida += x.toString()
                
            ent = ent.anterior
        
        salida += "</TABLE>>]}"
        return salida

    def getDataBase(self):
        ent = self

        while ent != None:
            x = ent.database
            if x != "":
                return x
            ent = ent.anterior
        
        return None