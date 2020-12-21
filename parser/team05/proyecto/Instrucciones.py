# GRUPO 5
# 201213062 - Mónica Raquel Calderon Muñoz
# 201213223 - Astrid Edith Hernandez Gonzalez
# 201213255 - Leonel Eduardo Avila Calvillo
# 201220159 - Diego Ahtohil Noj Armira
# 201220165 - Oscar Rolando Bernard Peralta

# INSTRUCCIONES [select]
class Instruccion:
    """ This is an abstract class """


# INSTRUCCION SELECT COMPLETO
class SelectCompleto(Instruccion):
    """ Instrucción SELECT COMPLETO """

    def __init__(self, select, complemento):
        self.select = select
        self.complemento = complemento

# INSTRUCCION SELECT MINIMO
class Select(Instruccion):
    """ Instrucción SELECT """

    def __init__(self, valores, pfrom, complementos):
        self.valores = valores
        self.pfrom = pfrom
        self.complementos = complementos

# INSTRUCCION SELECT WITH WHERE
class Select1(Instruccion):
    """ Instrucción SELECT """

    def __init__(self, valores, pfrom, where, complementos):
        self.valores = valores
        self.pfrom = pfrom
        self.where = where
        self.complementos = complementos

# INSTRUCCION SELECT DISTINCT
class Select2(Instruccion):
    """ Instrucción SELECT """

    def __init__(self, valores, pfrom, complementos):
        self.valores = valores
        self.pfrom = pfrom
        self.complementos = complementos

# INSTRUCCION SELECT DISTINCT WITH WHERE
class Select3(Instruccion):
    """ Instrucción SELECT """

    def __init__(self, valores, pfrom, where, complementos, distinct):
        self.valores = valores
        self.pfrom = pfrom
        self.where = where
        self.complementos = complementos
        self.distinct = distinct


# INSTRUCCION SELECT SOLO VALORES
class Select4(Instruccion):
    """ Instrucción SELECT """

    def __init__(self, valores):
        self.valores = valores

# INSTRUCCION COMPLEMENTOSELECTUNION
class ComplementoSelectUnion(Instruccion):
    """ Instrucción COMPLEMENTO SELECT """

    def __init__(self, select):
        self.select = select

# INSTRUCCION COMPLEMENTOSELECTALL
class ComplementoSelectUnionAll(Instruccion):
    """ Instrucción COMPLEMENTO SELECT """

    def __init__(self, select):
        self.select = select

class Union(Instruccion):
    def __init__(self, sel1, sel2):
        self.sel1 = sel1
        self.sel2 = sel2

class UnionAll(Instruccion):
    def __init__(self, sel1, sel2):
        self.sel1 = sel1
        self.sel2 = sel2

class Intersect(Instruccion):
    def __init__(self, sel1, sel2):
        self.sel1 = sel1
        self.sel2 = sel2

class IntersectAll(Instruccion):
    def __init__(self, sel1, sel2):
        self.sel1 = sel1
        self.sel2 = sel2

class Except(Instruccion):
    def __init__(self, sel1, sel2):
        self.sel1 = sel1
        self.sel2 = sel2

class ExceptAll(Instruccion):
    def __init__(self, sel1, sel2):
        self.sel1 = sel1
        self.sel2 = sel2

# INSTRUCCION COMPLEMENTOSELECTINTERSECT
class ComplementoSelectIntersect(Instruccion):
    """ Instrucción COMPLEMENTO SELECT """

    def __init__(self, select):
        self.select = select

# INSTRUCCION COMPLEMENTOSELECTINTERSECTALL
class ComplementoSelectIntersectALL(Instruccion):
    """ Instrucción COMPLEMENTO SELECT """

    def __init__(self, select):
        self.select = select

# INSTRUCCION COMPLEMENTOSELECTEXCEPT
class ComplementoSelectExcept(Instruccion):
    """ Instrucción COMPLEMENTO SELECT """

    def __init__(self, select):
        self.select = select

# INSTRUCCION COMPLEMENTOSELECTEXCEPTALL
class ComplementoSelectExceptAll(Instruccion):
    """ Instrucción COMPLEMENTO SELECT """

    def __init__(self, select):
        self.select = select

# INSTRUCCION COMPLEMENTOSELECTEXCEPTPCOMA
class ComplementoSelectExceptPcoma(Instruccion):
    """ Instrucción COMPLEMENTO SELECT """

    def __init__(self, param=None):
        self.param = param
        # NO RECIBE PARAMETROS
# ----------FIN DE CLASES SELECT--------------


# ----------INICIO DE REPLACE------------------
#INSTRUCCION REPLACE1
class Replace1(Instruccion):
    """ Instrucción REPLACE1 """

    def __init__(self, exist):
        self.exist = exist

#INSTRUCCION REPLACE2
class Replace2(Instruccion):
    """ Instrucción REPLACE2 """

    def __init__(self, exist):
        self.exist = exist

# ----------FIN DE REPLACE------------------


# ----------INICIO DE CTABLE------------------
#INSTRUCCION CTABLE
class Ctable(Instruccion):
    """ Instrucción CTABLE """

    def __init__(self, i_id,inherits):
        self.i_id = i_id
        self.atributos = atributos
        self.inherits = inherits

# ----------FIN DE CTABLE------------------


# ----------INICIO DE CTYPE------------------
#INSTRUCCION CTYPE
class Ctype(Instruccion):
    """ Instrucción CTABLE """

    def __init__(self, i_id,cadenas):
        self.i_id = i_id
        self.cadenas = cadenas

# ----------FIN DE CTYPE------------------


# ----------INICIO DE CREATE------------------

# INSTRUCCION CREATE
class Create(Instruccion):
    """ Instrucción CREATE """

    def __init__(self, replace):
        self.replace = replace

# INSTRUCCION CREATE1
class Create(Instruccion):
    """ Instrucción CREATE """

    def __init__(self, table):
        self.table = table

# INSTRUCCION CREATE2
class Create(Instruccion):
    """ Instrucción CREATE """

    def __init__(self, tipe):
        self.tipe = tipe

# ----------FIN DE CLASES CREATE--------------


# ----------INICIO DE DROP--------------------
# INSTRUCCION DROP
# class Drop(Instruccion):
#     """ Instrucción DROP """

#     def __init__(self, tdrop):
#         self.tdrop = tdrop


class DropDB(Instruccion):
    """ Instrucción DROP DATABASE """

    def __init__(self, ifexist):
        self.ifexist = ifexist


        # INSTRUCCION DROPTB
class DropTB(Instruccion):
    """ Instrucción DROPTB """

    def __init__(self, i_id):
        self.i_id = i_id
        

# INSTRUCCION IFEXIST1
class IfExist1(Instruccion):
    """ Instrucción IF EXIST """

    def __init__(self, nombre):
        self.nombre = nombre

        
# INSTRUCCION IFEXIST2
class IfExist2(Instruccion):
    """ Instrucción IF EXIST """

    def __init__(self, i_id):
        self.i_id = i_id
# ----------FIN DE DROP--------------------


# ----------INICIO DE INSERT--------------------
# INSTRUCCION INSERTTB
class InsertTB(Instruccion):
    """ Instrucción INSERTTB """

    def __init__(self, i_id,  lvalt):
        self.i_id = i_id
        self.lvalt = lvalt

# INSTRUCCION INSERTTB1
class InsertTB(Instruccion):
    """ Instrucción INSERTTB """

    def __init__(self, i_id, lvalt, lvalt2):
        self.i_id = i_id
        self.lvalt = lvalt
        self.lvalt2 = lvalt2


# INSTRUCCION VALTAB
class ValTab(Instruccion):
    """ Instrucción VALTAB """

    def __init__(self, valor ):
        self.valor = valor
# ----------FIN DE INSERT--------------------


# ----------INICIO DE ALTER--------------------
#INSTRUCCION TIPALTERC
class TipAlterC(Instruccion):
    """ Instrucción TALTER """

    def __init__(self, condicion ):
        self.condicion = condicion

#INSTRUCCION TIPALTERU
class TipAlterU(Instruccion):
    """ Instrucción TALTERU """

    def __init__(self, lids ):
        self.lids = lids

#INSTRUCCION TIPALTERFK
class TipAlterFK(Instruccion):
    """ Instrucción TALTERFK """

    def __init__(self, lids, i_id, lids2 ):
        self.lids = lids
        self.i_id = i_id
        self.lids2 = lids2

#INSTRUCCION TIPALTERFK1
class TipAlterFK1(Instruccion):
    """ Instrucción TALTERFK """

    def __init__(self, lids, i_id):
        self.lids = lids
        self.i_id = i_id

#INSTRUCCION TIPALTERCO
class TipAlterCo(Instruccion):
    """ Instrucción TALTERFK """

    def __init__(self, i_id, tconst ):
        self.i_id = i_id
        self.tconst = tconst

#INSTRUCCION TIPOCONSTRAINTC
class TipoConstraintC(Instruccion):
    """ Instrucción TIPOCONSTRAINTC """

    def __init__(self, condicion ):
        self.condicion = condicion

#INSTRUCCION TIPOCONSTRAINTU
class TipoConstraintU(Instruccion):
    """ Instrucción TIPOCONSTRAINTU """

    def __init__(self, lids ):
        self.lids = lids

#INSTRUCCION TIPOCONSTRAINTFK
class TipoConstraintFK(Instruccion):
    """ Instrucción TIPOCONSTRAINTFK """

    def __init__(self, lids, i_id, lids2 ):
        self.lids = lids
        self.i_id = i_id
        self.lids2 = lids2

# INSTRUCCION ALTER
class Alter(Instruccion):
    """ Instrucción ALTER """

    def __init__(self, valores ):
        self.valores = valores

# INSTRUCCION ALTERDB
class AlterDB(Instruccion):
    """ Instrucción ALTERDB """

    def __init__(self, i_id, operacion, val):
        self.i_id = i_id
        self.operacion = operacion
        self.val = val
# ----------FIN DE ALTER--------------------


# ----------INICIO DE UPDATE--------------------
# INSTRUCCION UPDATE
class Update(Instruccion):
    """ Instrucción UPDATE """

    def __init__(self, i_id, lvalor ):
        self.i_id = i_id
        self.lvalor = lvalor

# INSTRUCCION UPDATE
class Update(Instruccion):
    """ Instrucción UPDATE """

    def __init__(self, i_id, lvalor ):
        self.i_id = i_id
        self.lvalor = lvalor
# ----------FIN DE UPDATE--------------------


# ----------INICIO DE SHOW--------------------
# INSTRUCCION SHOW
class Show(Instruccion):
    """ Instrucción SHOW """

    def __init__(self, param=None):
        self.param = param

# ----------FIN DE SHOW--------------------


# ----------INICIO DE DELETE--------------------
# INSTRUCCION DELETE
class Delete(Instruccion):
    """ Instrucción DELETE """

    def __init__(self,i_id, where ):
        self.i_id = i_id
        self.where = where
# ----------FIN DE DELETE--------------------


# ----------INICIO DE USE DATABASE------------
class UseDatabase(Instruccion):
    """ Instrucción USE DATABASE """

    def __init__(self, nombre):
        self.nombre = nombre

# ----------FIN DE USE DATABASE---------------


# ----------INICIO DE CREATE DATABASE---------
class CreateDatabase(Instruccion):
    """ Instrucción CREATE DATABASE """

    def __init__(self, replace, datos):
        self.replace = replace
        self.datos = datos


class DatabaseInfo(Instruccion):
    """ Parte de la instrucción de CREATE DATABASE - Nombre, IF NOT EXIST, DATOS[OWNER, MODE] """

    def __init__(self, noexiste, nombre, datos):
        self.noexiste = noexiste
        self.nombre = nombre
        self.datos = datos


class Owner_Mode(Instruccion):
    """ Parte de la instrucción de CREATE DATABASE - Owner, Mode """

    def __init__(self, owner, mode):
        self.owner = owner
        self.mode = mode
# ----------FIN DE CREATE DATABASE------------

# CREATE TYPE

class CreateType(Instruccion):
    def __init__(self,idtype,valores):
        self.idtype = idtype
        self.valores = valores

# DELETE

class DeleteFrom(Instruccion):

    def __init__(self, valor,pwhere ):
        self.valor = valor
        self.pwhere = pwhere

#SUBCONSULTA

class Subconsulta(Instruccion):
    def __init__(self, subconsulta, alias):
        self.subconsulta = subconsulta
        self.alias = alias

#FUNCIONES DE AGREGACION
#COUNT AVG SUM MIN MAX
class FuncionAgregacion(Instruccion):
    
    def __init__(self,nombre,parametro,alias):
        self.nombre = nombre
        self.parametro = parametro
        self.alias = alias 

#FUNCION QUE GUARDARA EL VALOR DE CONDICION Y SU ALIAS
#VIENE DE PRODUCCION VALOR -> CONDICION ALIAS Y VALOR -> CONDICION
class Valores(Instruccion):
    
    def __init__(self, valor, alias):
        self.valor = valor
        self.alias = alias

#FUNCIONES TRIGONOMETRICAS
#ACOS ACOSD ASIN ASIND ATAN ATAND ATAN2 ATAN2D COS COSD COT COTD SIN SIND TAN TAND SINH COSH TANH ASINH ACOSH ATANH
class FuncionesTrigonometricas(Instruccion):
    
    def __init__(self,nombre,parametro,alias):
        self.nombre = nombre
        self.parametro = parametro
        self.alias = alias

#FUNCION GREATEST
class FuncionGreatest(Instruccion):
    
    def __init__(self, parametros, alias):
        self.parametros = parametros
        self.alias = alias

#FUNCION LEAST
class FuncionLeast(Instruccion):
    def __init__(self, parametros, alias):
        self.parametros = parametros
        self.alias = alias

#FUNCION RANDOM
class FuncionRandom(Instruccion):
    def __init__(self, alias):
        self.alias = alias

#FUNCION PI
class FuncionPi(Instruccion):
    def __init__(self, alias):
        self.alias = alias

#FUNCION DECODE
class Decode(Instruccion):
    
    def __init__(self,cadena,base, alias):
        self.cadena = cadena
        self.base = base
        self.alias = alias

#FUNCION ENCODE
class Encode(Instruccion):
    
    def __init__(self,cadena,base, alias):
        self.cadena = cadena
        self.base = base
        self.alias = alias

#FUNCION CONVERT
class Convert(Instruccion):
    
    def __init__(self,cadena, tipo, alias):
        self.cadena = cadena
        self.tipo = tipo
        self.alias = alias

#FUNCION SHA 256
class Sha256(Instruccion):
    def __init__(self,cadena, alias):
        self.cadena = cadena
        self.alias = alias

#FUNCION GETBYTE
class GetByte(Instruccion):
    
    def __init__(self,cadena,base, alias):
        self.cadena = cadena
        self.base = base
        self.alias = alias

#FUNCION SETBYTE
class SetByte(Instruccion):
    
    def __init__(self,cadena, offset, cambio, alias):
        self.cadena = cadena
        self.offset = offset
        self.cambio = cambio
        self.alias = alias

#CLASES PARA EL CASE
class InstruccionCase(Instruccion):
    def __init__(self, lwhen, alias):
        self.lwhen = lwhen
        self.alias = alias

class InstruccionWhen(Instruccion):
    def __init__(self, condicion, valor):
        self.codicion = condicion
        self.valor = valor

class InstruccionElse(Instruccion):
    def __init__(self, valor):
        self.valor = valor

#FUNCIONES MATEMATICAS
class FuncionesMatematicas(Instruccion):
    
    def __init__(self,nombre,parametro,alias = ''):
        self.nombre = nombre
        self.parametro = parametro
        self.alias = alias