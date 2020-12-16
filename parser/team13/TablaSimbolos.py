class Simbolo:
    '''Clase Símbolo Para un Leguaje de Programación Convencional '''

    def __init__(self, nombre, tipo, valor, fila, columna, ambito):
        self.nombre = nombre
        self.tipo = tipo
        self.valor = valor
        self.fila = fila
        self.columna = columna
        self.ambito = ambito


class SimboloBase:
    ''' Clase Para Almacenar La Información De Una Base de Datos '''

    def __init__(self, nombre, owner, mode):
        self.nombre = nombre
        self.owner = owner
        self.mode = mode
        self.tablas = {}

    def crearTabla(self, id, tabla):
        if id not in self.tablas:
            self.tablas[id] = tabla
            return True
        return None

    def getTabla(self, id):
        return self.tablas[id]

    def deleteTable(self, id):
        if id in self.tablas:
            del self.tablas[id]
            return True
        return None

    def renameTable(self, idactual, idnuevo):
        if idactual in self.tablas:
            if idnuevo not in self.tablas:
                self.tablas[idnuevo] = self.tablas.pop(idactual)
                self.tablas[idnuevo].nombre = idnuevo
                return 0
            return 1
        return 2


class SimboloTabla:
    '''Clase Símbolo Para Almacenar Información de Las Tablas '''

    def __init__(self, nombre, padre):
        self.nombre = nombre
        self.columnas = {}
        self.padre = padre

    def crearColumna(self, id, columna):
        if id not in self.columnas:
            self.columnas[id] = columna
            return True
        return None

    def renameColumna(self, idactual, idnuevo):
        if idactual in self.columnas:
            if idnuevo not in self.columnas:
                self.columnas[idnuevo] = self.columnas.pop(idactual)
                self.columnas[idnuevo].nombre = idnuevo
                return 0
            return 1
        return 2

    def modificarUnique(self, idcol, unique, idconstraint):
        if idcol in self.columnas:
            self.columnas[idcol].unique = {"id": idconstraint, "unique": unique}
            return True
        return None

    def modificarCheck(self, idcolumna, condicion, idconstraint):
        if idcolumna in self.columnas:
            self.columnas[idcolumna].check = {"id": idconstraint, "condicion": condicion}
            return True
        return None

    def modificarFk(self, idlocal, idTablaFk, idcolFk):
        if idlocal in self.columnas:
            self.columnas[idlocal].foreign_key = {"tabla": idTablaFk, "columna": idcolFk}
            return True
        return None

    def modificarPk(self, id):
        if id in self.columnas:
            self.columnas[id].primary_key = True
            return True
        return None

    def getColumna(self, idcolumna):
        return self.columnas[idcolumna]


class SimboloColumna:
    ''' Clase Para Almacenar Información Sobre Las Columnas de Una Tabla '''

    def __init__(self, nombre, tipo, primary_key, foreign_key, unique, default, null, check):
        self.nombre = nombre
        self.tipo = tipo
        self.primary_key = primary_key
        self.foreign_key = foreign_key
        self.unique = unique
        self.default = default
        self.null = null
        self.check = check


class llaveForanea:
    def __init__(self, idbase, idtlocal, idtfk, idclocal, idcfk):
        self.idbase = idbase
        self.idtlocal = idtlocal
        self.idtfk = idtfk
        self.idclocal = idclocal
        self.idcfk = idcfk


class Constraints:
    def __init__(self, idbase, idtabla, idconstraint, idcol, tipo):
        self.idbase = idbase
        self.idtabla = idtabla
        self.idconstraint = idconstraint
        self.idcol = idcol
        self.tipo = tipo


class Entorno:

    # CONSTRUCTOR PARA LA TABLA DE SÍMBOLOS
    def __init__(self, ent):
        self.tabla = {}
        self.padre = ent

    # COLOCAR UN SÍMBOLO
    def put(self, s, simbolo):
        self.tabla[s] = simbolo

    # OBTENER EL VALOR DE UN SÍMBOLO
    def get_value(self, id):

        myEnt = self

        while myEnt != None:

            if id in myEnt.tabla:
                return myEnt.tabla[id]

            myEnt = myEnt.padre

        return None

    # GET BASE
    def get(self, id):
        for key in self.tabla.keys():
            if self.tabla[key].nombre == id:
                return self.tabla[key]
        return None

    # eliminar base
    def eliminar(self, id):
        for key in self.tabla.keys():
            if self.tabla[key].nombre == id:
                del self.tabla[key]
                return True
        return None

    # renombrar base
    def renameBase(self, idactual, idnuevo):
        actual = self.get(idactual)
        if actual != None:
            self.tabla[idnuevo] = self.tabla.pop(idactual)
            self.tabla[idnuevo].nombre = idnuevo
            return True
        return None

    # MOSTRAR Base
    def mostrar(self):
        for key in self.tabla.keys():
            print("Nombre Base")
            print(self.tabla[key].nombre)
            print("Owner")
            print(self.tabla[key].owner)
            print("Mode")
            print(self.tabla[key].mode)
            print("-------------------")
            base = self.tabla[key]
            for tab in base.tablas:
                print("Columnas")
                tabla = base.tablas[tab]
                print(tabla.columnas)
                for col in tabla.columnas:
                    print(tabla.columnas[col].nombre)
                    print(tabla.columnas[col].tipo)
                    print(tabla.columnas[col].primary_key)
                    print(tabla.columnas[col].foreign_key)
                    print(tabla.columnas[col].default)
                    print(tabla.columnas[col].check)
                    print(tabla.columnas[col].unique)

    # Get columna
    def getColumna(self, idbase, idtabla, idcol):
        base = self.get(idbase)
        if base != None:
            tabla = base.getTabla(idtabla)
            return tabla.getColumna(idcol)
        return None
