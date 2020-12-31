from enum import Enum

class TIPO(Enum) :
    DATABASE = 1
    TABLE = 2
    COLUMN = 3
    SMALLINT = 4
    INTEGER = 5
    BIGINT = 6
    DECIMAL = 7
    NUMERIC = 8
    REAL = 9
    DOUBLE_PRECISION = 10
    CHARACTER_VARYING = 11
    VARCHAR = 12
    CHARACTER = 13
    CHAR = 14
    TEXT = 15
    TIMESTAMP = 16
    DATE = 17
    TIME = 18
    INTERVAL = 19
    BOOLEAN = 20
    TUPLA = 21

class Simbolo() :
    #id = identificador numerico unico por simbolo
    #nombre = nombre principal del simbolo
    #tipo = tipo de simbolo (tabla, columna, basedatos, etc)
    #ambito = pertenencia de un simbolo o relacion con otros
    #coltab = cantidad de columnas que una tabla tiene
    #tipocol = tipo de dato que la columna almacena
    #llavecol = tipo de llave (0=Ninguna, 1=Primaria, 2=Foranea)
    #refcol = referencia de columna
    #defcol = default de columna
    #nullcol = columna null(FALSE) o not null(TRUE)
    #constcol = constraint de columna
    #numcol = Numero de la columna dentro de la tabla
    def __init__(self, id, nombre, tipo, ambito, coltab=0, tipocol="", llavecol=0, refcol="", defcol="", nullcol=False, constcol="",numcol=0,registro=[]) :
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.ambito = ambito
        self.coltab = coltab
        self.tipocol = tipocol
        self.llavecol = llavecol
        self.refcol = refcol
        self.defcol = defcol
        self.nullcol = nullcol
        self.constcol = constcol
        self.numcol = numcol
        self.registro = registro

class Tabla() :
    
    def __init__(self, simbolos = {}) :
        self.simbolos = simbolos

    def agregar(self, simbolo) :
        self.simbolos[simbolo.id] = simbolo
    
    def obtener(self, id) :
        if not id in self.simbolos :
            print('(obtener)Error: variable ', id, ' no definida.')

        return self.simbolos[id]

    def BuscarNombre(self, nombre) :
        for simbolo in self.simbolos:
            if self.simbolos[simbolo].nombre == nombre:
                return self.simbolos[simbolo]
        if not nombre in self.simbolos :
            print('(BuscarNombre)Error: variable ', nombre, ' no definida.')

    def BuscarAmbito(self, ambito) :
        for simbolo in self.simbolos:
            if self.simbolos[simbolo].ambito == ambito:
                return self.simbolos[simbolo]
        if not ambito in self.simbolos :
            print('(BuscarAmbito)Error: variable ', ambito, ' no definida.')

    def actualizar(self, simbolo) :
        if not simbolo.id in self.simbolos :
            print('(actualizar)Error: variable ', simbolo.id, ' no definida.')
        else :
            self.simbolos[simbolo.id] = simbolo
    
    ##
    ##Metodos para implementacion de queries 
    ##
    def getTabla(self,nombre,skip=0):
        sk = skip
        for simbolo in self.simbolos.values():
            if simbolo.nombre ==nombre:
                #Verificar si es tabla
                #results = []
                if simbolo.tipo == TIPO.COLUMN:
                    if sk >0:
                        sk = sk-1
                        continue
                    ambito = simbolo.ambito
                    tablaaa = self.simbolos[ambito]
                    # El nombre de la tabla es
                    tabla = tablaaa.nombre
                    # La base de datos es 
                    dbambito = tablaaa.ambito
                    #DB
                    dbb = self.simbolos[dbambito]
                    db = dbb.nombre
                    return tabla , db

        return None

    def getIndice(self,db,table,col):

        #Buscamos el ambito de la DB
        iddb = -1
        for simbolo in self.simbolos.values():  
            
            if simbolo.nombre == db and simbolo.tipo == TIPO.DATABASE : 
                iddb = simbolo.id
        #Buscamos el ambito de la Tabla
        
        idtable = -1
        for simbolo in self.simbolos.values():
            if simbolo.nombre == table and simbolo.tipo == TIPO.TABLE and simbolo.ambito == iddb : 
                idtable = simbolo.id

        #Buscamos el indice de la columna
        idcol = -1
        for simbolo in self.simbolos.values():
            if simbolo.nombre == col and simbolo.tipo == TIPO.COLUMN and simbolo.ambito == idtable : 
                idcol = simbolo.numcol
                return idcol
        return idcol

    def getColumns(self,db,table):
        #Buscamos el ambito de la DB
        iddb = -1
        for simbolo in self.simbolos.values():  
            
            if simbolo.nombre == db and simbolo.tipo == TIPO.DATABASE : 
                iddb = simbolo.id
        #Buscamos el ambito de la tabla        
        idtable = -1
        for simbolo in self.simbolos.values():
            if simbolo.nombre == table and simbolo.tipo == TIPO.TABLE and simbolo.ambito == iddb : 
                idtable = simbolo.id
        columns = []        
        for simbolo in self.simbolos.values() :
            if simbolo.tipo == TIPO.COLUMN and simbolo.ambito == idtable:
                columns.append(simbolo.nombre)
        return columns 