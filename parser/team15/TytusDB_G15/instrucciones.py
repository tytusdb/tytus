class Instruccion:
    ''' Esta sera la clase de Instrucciones '''

class Definicion(Instruccion):
    def __init__(self, tipo, id):
        self.tipo = tipo
        self.id = id

class CreateDatabase(Instruccion):
    def __init__(self, nombre, usuario, modo = 1, replace = 0):
        self.nombre = nombre
        self.usuario = usuario
        self.modo = modo
        self.replace = replace

class LLave_Primaria(Instruccion):
    def __init__(self, id):
        self.id  = id

class Definicon_Foranea(Instruccion):
    def __init__(self, nombre_tabla, referencia_tabla , campo_referencia):
        self.nombre_tabla = nombre_tabla
        self.referencia_tabla = referencia_tabla
        self.campo_referencia = campo_referencia

class Definicion_check(Instruccion):
    def __init__(self, exp_logica = []):
        self.exp_logica = exp_logica

class Etiqueta_tipo(Instruccion):
    def __init__(self, etiqueta):
        self.etiqueta = etiqueta

class Etiqueta_Interval(Instruccion):
    def __init__(self,ext_time, ext_time1,etiqueta):
        self.ext_time = ext_time
        self.ext_time1 = ext_time1
        self.etiqueta = etiqueta

class Create_Table(Instruccion):
    def __init__(self, id, herencia, instrucciones = []):
        self.id  = id
        self.herencia = herencia
        self.instrucciones = instrucciones

class Definicion_Columnas(Instruccion):
    def __init__(self, id, tipo_datos, etiqueta, id_referencia, opciones_constraint = []):
        self.id = id
        self.tipo_datos = tipo_datos
        self.etiqueta = etiqueta
        self.id_referencia = id_referencia
        self.opciones_constraint = opciones_constraint

class Lista_Parametros(Instruccion):
    def __init__(self ,identificadores = []):
        self.identificadores = identificadores

class definicion_constraint(Instruccion):
    def __init__(self, id, tipo , referencia,columna,opciones_contraint = []):
        self.id = id
        self.tipo = tipo
        self.referencia = referencia
        self.columna = columna
        self.opciones_constraint = opciones_contraint

class showDatabases(Instruccion):
    def __init__(self):
        ''' SHOW DATABASES'''

class dropDatabase(Instruccion):
    def __init__(self,id, exists = 0):
        self.id = id
        self.exists = exists

class useDatabase(Instruccion):
    def __init__(self,id):
        self.id = id

class Create_Alterdatabase(Instruccion):
    def __init__(self,id_tabla, tipo_id):
        self.id_tabla = id_tabla
        self.tipo_id = tipo_id

class showTables(Instruccion):
    def __init__(self):
        ''' SHOW DATABASES'''

class Create_update(Instruccion):
    def __init__(self,identificador,expresion,lista_update = []):
        self.identificador = identificador
        self.lista_update = lista_update
        self.expresion = expresion

class Create_Parametro_update(Instruccion):
    def __init__(self,ids,expresion):
        self.ids = ids
        self.expresion = expresion

class Crear_Drop(Instruccion):
    def __init__(self, lista_ids = []):
        self.lista_ids = lista_ids

class Crear_altertable(Instruccion):
    def __init__(self,etiqueta,identificador,columnid,tocolumnid,expresionlogica,lista_campos = [],lista_ref = []):
        self.etiqueta = etiqueta
        self.identificador = identificador
        self.columnid = columnid
        self.tocolumnid = tocolumnid
        self.lista_campos = lista_campos
        self.expresionlogica = expresionlogica
        self.lista_ref = lista_ref

class Crear_tipodato(Instruccion):
    def __init__(self,identificador,tipo,par1,par2):
        self.identificador = identificador
        self.tipo = tipo
        self.par1 = par1
        self.par2 = par2

class Definicion_Insert(Instruccion):
    def __init__(self, id, etiqueta ,lista_parametros = [], lista_datos = []):
        self.id = id
        self.etiqueta = etiqueta
        self.lista_parametros = lista_parametros
        self.lista_datos = lista_datos

class Create_type(Instruccion):
    def __init__(self,identificador,lista_datos = []):
        self.identificador = identificador
        self.lista_datos = lista_datos

class Definicion_delete(Instruccion):
    def __init__(self, id, etiqueta, expresion, id_using, returning = []):
        self.id = id
        self.etiqueta = etiqueta
        self.expresion = expresion
        self.id_using = id_using
        self.returning = returning

class Create_hijo_select(Instruccion):
    def init(self,etiqueta,expresion,expresion2, lista_objetos = []):
        self.etiqueta = etiqueta
        self.expresion = expresion
        self.expresion2 = expresion2
        self.lista_objetos = lista_objetos