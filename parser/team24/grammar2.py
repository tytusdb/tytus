#Parte lexica en ply
from reportError import CError
from reportError import insert_error
from reportBNF import insertProduction
from reportBNF import insertRegla

entrada = ''

import InstruccionesDGA as inst
reservadas = {
    'now' : 'NOW',
    'smallint' : 'SMALLINT',
    'integer' : 'INTEGER',
    'bigint' : 'BIGINT',
    'decimal' : 'DECIMAL',
    'numeric' : 'NUMERIC',
    'real' : 'REAL',
    'double' : 'DOUBLE',
    'precision' : 'PRECISION',
    'character' : 'CHARACTER',
    'varying' : 'VARYING',
    'text' : 'TEXT',
    'timestamp' : 'TIMESTAMP',
    'select': 'SELECT',
    'extract' : 'EXTRACT',
    'year' : 'YEAR',
    'day' : 'DAY',
    'hour' : 'HOUR',
    'minute' : 'MINUTE',
    'second' : 'SECOND',
    'month' : 'MONTH',
    'date_part' : 'DATE_PART',
    'from' : 'FROM',
    'current_date' : 'CURRENT_DATE',
    'current_time' : 'CURRENT_TIME',
    'boolean' : 'BOOLEAN',
    'create' : 'CREATE',
    'type' : 'TYPE',
    'as' : 'AS',
    'between': 'BETWEEN',
    'is' : 'IS',
    'like' : 'LIKE',
    'in' : 'IN',
    'null' : 'NULL',
    'not' : 'NOT',
    'and' : 'AND',
    'or' : 'OR',
    'replace' : 'REPLACE',
    'database' : 'DATABASE',
    'if' : 'IF',
    'owner' : 'OWNER',
    'alter' : 'ALTER',
    'rename' : 'RENAME',
    'to' : 'TO',
    'current_user' : 'CURRENT_USER',
    'session_user' : 'SESSION_USER',
    'drop' : 'DROP',
    'exists' : 'EXISTS',
    'table' : 'TABLE',
    'contraint' : 'CONSTRAINT',
    'unique' : 'UNIQUE',
    'check' : 'CHECK',
    'key' : 'KEY',
    'primary' : 'PRIMARY',
    'references' : 'REFERENCES',
    'foreign' : 'FOREIGN',
    'set' : 'SET',
    'column' : 'COLUMN',
    'inherits' : 'INHERITS',
    'insert' : 'INSERT',
    'into' : 'INTO',
    'update' : 'UPDATE',
    'delete' : 'DELETE',
    'where' : 'WHERE',
    'values' : 'VALUES',
    'by' : 'BY',
    'having' : 'HAVING',
    'abs' : 'ABS',
    'cbrt' : 'CBRT',
    'ceil' : 'CEIL',
    'ceiling' : 'CEILING',
    'degrees' : 'DEGREES',
    'div' : 'DIV',
    'exp' : 'EXP',
    'factorial' : 'FACTORIAL',
    'floor' : 'FLOOR',
    'gcd' : 'GCD',
    'lcm' : 'LCM',
    'ln' : 'LN',
    'log' : 'LOG',
    'log10' : 'LOG10',
    'min_scale' : 'MIN_SCALE',
    'mod' : 'MOD',
    'pi' : 'PI',
    'power' : 'POWER',
    'radians' : 'RADIANS',
    'round' : 'ROUND',
    'scale' : 'SCALE',
    'sign' : 'SIGN',
    'sqrt' : 'SQRT',
    'trim_scale' : 'TRIM_SCALE',
    'trunc' : 'TRUNC',
    'width_bucket' : 'WIDTH_BUCKET',
    'random' : 'RANDOM',
    'setseed' : 'SETSEED',
    'count' : 'COUNT',
    'length' : 'LENGHT',
    'substring' : 'SUBSTRING',
    'trim' : 'TRIM',
    'get_byte' : 'GET_BYTE',
    'md5' : 'MD5',
    'set_byte' : 'SET_BYTE',
    'sha256' : 'SHA256',
    'substr' : 'SUBSTR',
    'case' : 'CASE',
    'when' : 'WHEN',
    'else' : 'ELSE',
    'end' : 'END',
    'greatest' : 'GREATEST',
    'least' : 'LEAST',
    'limit' : 'LIMIT',
    'asc' : 'ASC',
    'desc' : 'DESC',
    'first' : 'FISRT',
    'last' : 'LAST',
    'nulls' : 'NULLS',
    'offset' : 'OFFSET',
    'all' : 'ALL',
    'union' : 'UNION',
    'intersect' : 'INTERSECT',
    'then' : 'THEN',
    'decode' : 'DECODE',
    'except' : 'EXCEPT',
    'distinct':'DISTINCT',
    'acos':'ACOS',
    'acosd':'ACOSD',
    'asin':'ASIN',
    'asind':'ASIND',
    'atan':'ATAN',
    'atand':'ATAND',
    'atan2':'ATAN2',
    'atan2d':'ATAN2D',
    'cos':'COS',
    'cosd':'COSD',
    'cot':'COT',
    'cotd':'COTD',
    'sin':'SIN',
    'sind':'SIND',
    'tan':'TAN',
    'tand':'TAND',
    'sinh':'SINH',
    'cosh':'COSH',
    'tanh':'TANH',
    'asinh':'ASINH',
    'acosh':'ACOSH',
    'atanh':'ATANH',
    'trunc':'TRUNC',
    'sum':'SUM',
    'avg':'AVG',
    'max':'MAX',
    'min':'MIN',
    'length':'LENGTH',
    'convert' : 'CONVERT',
    'false' : 'FALSE',
    'true' : 'TRUE',
    'group' : 'GROUP',
    'order' : 'ORDER',
    'show' : 'SHOW',
    'databases' : 'DATABASES',
    'mode' : 'MODE',
    'add' : 'ADD',
    'only' : 'ONLY',
    'serial' : 'SERIAL',
    'name' : 'NAME',
    'default' : 'DEFAULT',
    'use'   :   'USE',
    'money' :   'MONEY',
    'date'  :   'DATE',
    'varchar'   :   'VARCHAR'


    
}

tokens = [
            'VIR',
            'DEC',
            'MAS',
            'MENOS',
            'ELEVADO',
            'MULTIPLICACION',
            'DIVISION',
            'MODULO',
            'MENOR',
            'MAYOR',
            'IGUAL',
            'MENOR_IGUAL',
            'MAYOR_IGUAL',
            'MENOR_MENOR',
            'MAYOR_MAYOR',
            'DIFERENTE',
            'SIMBOLOOR',
            'SIMBOLOAND',
            'LLAVEA',
            'LLAVEC',
            'PARA',
            'PARC',
            'DOSPUNTOS',
            'COMA',
            'PUNTO',
            'INT',
            'TEXTO',
            'CHAR',
            'ID',
            'PTCOMA',
            'CORCHETEA',
            'CORCHETEC'
] + list(reservadas.values())

#Token

t_VIR = r'~'
t_MAS = r'\+' 
t_MENOS = r'-'
t_ELEVADO= r'\^'
t_MULTIPLICACION = r'\*'
t_DIVISION =r'/'
t_MODULO= r'%'
t_MENOR =r'<'
t_MAYOR =r'>'
t_IGUAL =r'='
t_MENOR_IGUAL =r'<='
t_MAYOR_IGUAL =r'>='
t_MENOR_MENOR =r'<<'
t_MAYOR_MAYOR =r'>>'
t_DIFERENTE=r'<>'
t_SIMBOLOOR=r'\|'
t_SIMBOLOAND = r'\&'
t_LLAVEA = r'\{'
t_LLAVEC = r'\}'
t_PARA = r'\('
t_PARC = r'\)'
t_DOSPUNTOS=r'\:'
t_COMA=r'\,'
t_PUNTO=r'\.'
t_PTCOMA = r'\;'
t_CORCHETEA=r'\['
t_CORCHETEC=r'\]'


def t_DEC(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        descript = 'error lexico at token ' + str(t.value)
        linea = str(t.lineno)
        columna = str(find_column(t))
        nuevo_error = CError(linea,columna,descript,'Lexico')
        insert_error(nuevo_error)
        print("Error no se puede convertir %d", t.value)
        t.value = 0
    return t


def t_INT(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        descript = 'error lexico at token ' + str(t.value)
        linea = str(t.lineno)
        columna = str(find_column(t))
        nuevo_error = CError(linea,columna,descript,'Lexico')
        insert_error(nuevo_error)
        print("Valor numerico incorrecto %d", t.value)
        t.value = 0
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value.lower(), 'ID')  
    return t


def t_VARCHAR(t):
    r'\'.*?\''
    t.value = t.value[1:-1]  # remuevo las comillas
    return t

def t_COMENT_SIMPLE(t):
    r'//.*\n'
    t.lexer.lineno += 1



def t_COMENT_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

t_ignore = " \t"

def t_nuevalinea(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    descript = 'error lexico at token ' + str(t.value[0])
    linea = str(t.lineno)
    columna = str(find_column(t))
    nuevo_error = CError(linea,columna,descript,'Lexico')
    insert_error(nuevo_error)
    t.lexer.skip(1)


from classesQuerys import *
import ply.lex as lex
lexer = lex.lex()

precedence = (
    ('left','PUNTO'),
    ('right','UMAS','UMENOS'),
    ('left','ELEVADO'),
    ('left','MULTIPLICACION','DIVISION','MODULO'),
    ('left','MAS','MENOS'),
    ('left','BETWEEN','IN','LIKE'),
    ('left','MENOR','MAYOR','MENOR_IGUAL','MAYOR_IGUAL','IGUAL','DIFERENTE'),
    ('right','NOT'),
    ('left','AND'),
    ('left','OR')
)
"""INICIO ANALIZADOR"""
#PRODUCCIONES GENERALES
def p_inicio(p):
    """
    inicio  :   inicio inst
    """
    p[1].append(p[2])
    p[0] = p[1]
    for instrucciones in p[0]:
        instrucciones.ejecutar()
    inst.Textoresultado()
    insertProduction(p.slice, len(p.slice))

def p_inicio2(p):
    """
    inicio  :   inst
    """
    p[0] = [p[1]]
    insertProduction(p.slice, len(p.slice))
    
def p_inst(p):
    """
    inst    :   createdb
            |   showdb
            |   alterdb
            |   dropdb
            |   createtb
            |   droptb
            |   altertb
            |   insert
            |   update
            |   delete
            |   usedb
            |   query
    """
    p[0] = p[1]
    insertProduction(p.slice, len(p.slice))

def p_id(p):
    "id : ID"
    p[0] = p[1]
    insertProduction(p.slice, len(p.slice))

def p_valortipo(p):
    """
    valortipo   :   INT
                |   ID
                |   DEC
                |   TEXTO
    """
    p[0] = str(p[1])
    insertProduction(p.slice, len(p.slice))

def p_cond(p):
    """
    cond    :   id MAYOR valortipo
            |   id MENOR valortipo
            |   id IGUAL valortipo
            |   id MENOR_IGUAL valortipo
            |   id MAYOR_IGUAL valortipo
    """
    p[0] = inst.cond(p[1],p[2],p[3])
    insertProduction(p.slice, len(p.slice))

def p_wherecond(p):
    "wherecond  :  id BETWEEN valortipo AND valortipo"
    p[0] = inst.wherecond(p[1],p[3],p[5])
    insertProduction(p.slice, len(p.slice))

def p_wherecond1(p):
    "wherecond  :  id IGUAL valortipo"
    p[0] = inst.wherecond1(p[1],p[3])
    insertProduction(p.slice, len(p.slice))

def p_reservadatipo(p):
    """
    reservadatipo   :   SMALLINT
                    |   INTEGER
                    |   BIGINT
                    |   DECIMAL
                    |   NUMERIC
                    |   REAL
                    |   MONEY
                    |   TEXT
                    |   DATE
                    |   BOOLEAN
    """
    p[0] = p[1]
    insertProduction(p.slice, len(p.slice))

def p_reservadatipo1(p):
    """
    reservadatipo   :   VARCHAR PARA INT PARC
                    |   CHARACTER PARA INT PARC
                    |   CHAR PARA INT PARC
    """
    p[0] = inst.reservadatipo(p[1],p[3])
    insertProduction(p.slice, len(p.slice))

#MANIPULACION DE BASES DE DATOS
#CREATEDB----------------------
def p_createdb(p):
    "createdb   :   CREATE replacedb DATABASE ifnotexists id owner mode PTCOMA"
    p[0] = inst.createdb(p[2],p[4],p[5],p[6],p[7])
    insertProduction(p.slice, len(p.slice))

def p_replacedb(p):
    "replacedb  :   OR REPLACE"
    p[0] = p[1]
    insertProduction(p.slice, len(p.slice))

def p_replacedb1(p):
    "replacedb  :   "
    p[0] = ""
    insertProduction(p.slice, len(p.slice))

def p_ifnotexists(p):
    "ifnotexists    :   IF NOT EXISTS"
    p[0] = p[1]
    insertProduction(p.slice, len(p.slice))

def p_ifnotexists1(p):
    "ifnotexists    :   "
    p[0] = ""
    insertProduction(p.slice, len(p.slice))

def p_owner(p):
    "owner :   OWNER IGUAL valortipo"
    p[0] = p[1]
    insertProduction(p.slice, len(p.slice))

def p_owner1(p):
    "owner  :   "
    p[0] = ""
    insertProduction(p.slice, len(p.slice))

def p_mode(p):
    "mode   :   MODE IGUAL valortipo"
    p[0] = p[3]
    insertProduction(p.slice, len(p.slice))

def p_mode1(p):
    "mode   :   "
    p[0] = ""
    insertProduction(p.slice, len(p.slice))

#SHOW DATABASES------------------
def p_showdb(p):
    "showdb :   SHOW DATABASES PTCOMA"
    p[0] = inst.showdb(p[1])
    insertProduction(p.slice, len(p.slice))
   
#ALTER DATABASE------------------
def p_alterdb(p):
    "alterdb    :   ALTER DATABASE alterdb2 PTCOMA"
    p[0] = inst.alterdb(p[3])
    insertProduction(p.slice, len(p.slice))

def p_alterdb2(p):
    "alterdb2   :   id alterdb3"
    p[0] = inst.alterdb2(p[1],p[2])
    insertProduction(p.slice, len(p.slice))

def p_alterdb21(p):
    "alterdb2    :   NAME OWNER TO valortipo"
    p[0] = inst.alterdb21(p[4])
    insertProduction(p.slice, len(p.slice))

def p_alterdb3(p):
    "alterdb3   :   RENAME TO valortipo"
    p[0] = inst.alterdb3(p[3])
    insertProduction(p.slice, len(p.slice))

def p_alterdb31(p):
    "alterdb3   :   OWNER TO LLAVEA valortipo SIMBOLOOR valortipo SIMBOLOOR valortipo LLAVEC"
    p[0] = inst.alterdb31(p[4],p[6],p[8])
    insertProduction(p.slice, len(p.slice))

#DROP DATABASE--------------------
def p_dropdb(p):
    "dropdb :   DROP DATABASE ifexists id PTCOMA"
    insertProduction(p.slice, len(p.slice))

def p_ifexists(p):
    "ifexists   :   IF EXISTS"
    p[0] = p[1]
    insertProduction(p.slice, len(p.slice))

def p_ifexists1(p):
    "ifexists   :   "
    p[0] = ""
    insertProduction(p.slice, len(p.slice))

#USE DATABASE----------------------
def p_usedb(p):
    "usedb  :   USE id PTCOMA"
    p[0] = inst.usedb(p[2])
    insertProduction(p.slice, len(p.slice))

#MANIPULACION DE TABLAS
# CREATE TABLE-------------------
def p_createtb(p):
    "createtb   :   CREATE TABLE id PARA coltb PARC PTCOMA inherits"
    p[0] = inst.createtb(p[3],p[5],p[8])
    insertProduction(p.slice, len(p.slice))

def p_inherits(p):
    "inherits   :   INHERITS PARA id PARC PTCOMA"
    p[0] = p[3]
    insertProduction(p.slice, len(p.slice))

def p_inhrits1(p):
    "inherits   :   "
    p[0] = ""
    insertProduction(p.slice, len(p.slice))

def p_coltb(p):
    "coltb  :   coltb COMA columna"
    p[1].append(p[3])
    p[0] = p[1]
    insertProduction(p.slice, len(p.slice))

def p_coltb1(p):
    "coltb  :   columna"
    p[0] = [p[1]]
    insertProduction(p.slice, len(p.slice))

def p_columna(p):
    "columna    :   id reservadatipo notnull key references default constraint"
    p[0] = inst.columna(p[1],p[2],p[3],p[4],p[5],p[6],p[7])
    insertProduction(p.slice, len(p.slice))

def p_references(p):
    "references :   REFERENCES id"
    p[0] = p[2]
    insertProduction(p.slice, len(p.slice))

def p_references1(p):
    "references :   "
    p[0] = ""
    insertProduction(p.slice, len(p.slice))

def p_key(p):
    """
    key :   SERIAL PRIMARY KEY
        |   PRIMARY KEY colkey
        |   FOREIGN KEY colkey
    """
    p[0] = p[1] + " " + p[2] + " " + p[3]
    insertProduction(p.slice, len(p.slice))

def p_key1(p):
    "key    :   "
    p[0] = ""
    insertProduction(p.slice, len(p.slice))

def p_colkey(p):
    "colkey :   PARA colkey2 PARC"
    p[0] = p[2]
    insertProduction(p.slice, len(p.slice))

def p_colkey1(p):
    "colkey :   "
    p[0] = ""
    insertProduction(p.slice, len(p.slice))

def p_colkey2(p):
    "colkey2    :   colkey2 COMA id"
    p[0] = [p[1],p[3]]
    insertProduction(p.slice, len(p.slice))

def p_colkey21(p):
    "colkey2    :   id"
    p[0] = p[1]
    insertProduction(p.slice, len(p.slice))

def p_default(p):
    "default    :   DEFAULT id"
    p[0] = p[2]
    insertProduction(p.slice, len(p.slice))

def p_default1(p):
    "default    :   "
    p[0] = ""
    insertProduction(p.slice, len(p.slice))

def p_notnull(p):
    "notnull    :   not NULL"
    p[0] = p[1]
    insertProduction(p.slice, len(p.slice))

def p_notnull1(p):
    "notnull    :   "
    p[0] = ""
    insertProduction(p.slice, len(p.slice))

def p_not(p):
    "not : NOT"
    p[0] = p[1]
    insertProduction(p.slice, len(p.slice))

def p_not1(p):
    "not : "
    p[0] = ""
    insertProduction(p.slice, len(p.slice))

def p_constraint(p):
    "constraint :   UNIQUE"
    p[0] = p[1]
    insertProduction(p.slice, len(p.slice))

def p_constraint1(p):
    "constraint :   const CHECK PARA cond PARC"
    p[0] = [p[1],p[4]]
    insertProduction(p.slice, len(p.slice))

def p_constraint11(p):
    "constraint :   "
    p[0] = ""
    insertProduction(p.slice, len(p.slice))

def p_const(p):
    "const  :   CONSTRAINT id"
    p[0] = p[2]
    insertProduction(p.slice, len(p.slice))

def p_const1(p):
    "const  :   "
    p[0] = ""
    insertProduction(p.slice, len(p.slice))

#DROP TABLE----------
def p_droptb(p):
    "droptb :   DROP TABLE id PTCOMA"
    p[0] = inst.droptb(p[3])
    insertProduction(p.slice, len(p.slice))

#ALTER TABLE---------
def p_altertb(p):
    "altertb    :   ALTER TABLE id altertb2 PTCOMA"
    p[0] = inst.altertb(p[3],p[4])
    insertProduction(p.slice, len(p.slice))

def p_altertb2(p):
    "altertb2   :   altertb2 alteracion"
    p[1].append(p[2])
    p[0] = p[1]
    insertProduction(p.slice, len(p.slice))

def p_altertb21(p):
    "altertb2   :   alteracion"
    p[0] = [p[1]]
    insertProduction(p.slice, len(p.slice))

def p_alteracion1(p):
    """
    alteracion  :   DROP dropprop id
                |   SET NOT NULL
    """
    p[0] = inst.alteracion1(p[1] + " " + p[2], p[3])
    insertProduction(p.slice, len(p.slice))

def p_dropprop(p):
    """
    dropprop    :   COLUMN
                |   CONSTRAINT
    """
    p[0] = p[1]
    insertProduction(p.slice, len(p.slice))

def p_alteracion11(p):
    "alteracion :   ADD addprop"
    p[0] = inst.alteracion11(p[1],p[2])
    insertProduction(p.slice, len(p.slice))

def p_addprop(p):
    "addprop    :   CHECK PARA cond PARC"
    p[0] = inst.addprop(p[1],p[3])
    insertProduction(p.slice, len(p.slice))

def p_addprop1(p):
    """
    addprop :   CONSTRAINT id
            |   COLUMN columna
    """
    p[0] = inst.addprop(p[1],p[2])
    insertProduction(p.slice, len(p.slice))

def p_alteracion111(p):
    "alteracion :   UNIQUE colkey"
    p[0] = p[2]
    insertProduction(p.slice, len(p.slice))

def p_alteracion1111(p):
    "alteracion :   altcol"
    p[0] = p[1]
    insertProduction(p.slice, len(p.slice))
    
def p_altcol(p):
    "altcol :   altcol COMA alter"
    p[1].append(p[3])
    p[0] = p[1]
    insertProduction(p.slice, len(p.slice))
    
def p_altcol1(p):
    "altcol :   alter"
    p[0] = [p[1]]
    insertProduction(p.slice, len(p.slice))
    
def p_alter(p):
    "alter  :   ALTER COLUMN id propaltcol"
    p[0] = inst.alter(p[3],p[4])
    insertProduction(p.slice, len(p.slice))
    
def p_propaltcol(p):
    "propaltcol :   TYPE reservadatipo"
    p[0] = p[2]
    insertProduction(p.slice, len(p.slice))

def p_alteracion11111(p):
    """
    alteracion  :   FOREIGN KEY colkey
                |   REFERENCES id colkey 
    """
    p[0] = inst.alteracion11111(p[1],p[2],p[3])
    insertProduction(p.slice, len(p.slice))

#MANIPULACION DE DATOS
#INSERT---------------
def p_insert(p):
    "insert :   INSERT INTO id VALUES PARA valores PARC PTCOMA"
    p[0] = inst.insert(p[3],p[6])
    insertProduction(p.slice, len(p.slice))

def p_valores(p):
    "valores    :   valores COMA valortipo"
    p[1].append(p[3])
    p[0] = p[1]
    insertProduction(p.slice, len(p.slice))

def p_valores1(p):
    """
    valores    :   valortipo
    """
    p[0] = [p[1]]
    insertProduction(p.slice, len(p.slice))

#UPDATE----------------
def p_update(p):
    "update :   UPDATE id SET cond WHERE wherecond PTCOMA"
    p[0] = inst.update(p[2],p[4],p[6])
    insertProduction(p.slice, len(p.slice))

#DELETE----------------
def p_delete(p):
    "delete :   DELETE FROM id WHERE wherecond PTCOMA"
    p[0] = inst.delete(p[3],p[5])
    insertProduction(p.slice, len(p.slice))

"""FIN ANALIZADOR SINTACTICO ASCENDENTE"""

def p_empty(p):
     'empty :'
     pass
     insertProduction(p.slice, len(p.slice))

def p_query(t):
    'query : queryp com PTCOMA'
    #por el momento 
    t[0] = t[1]
    insertProduction(t.slice, len(t.slice))

def p_com(t):
    ''' 
    com : UNION query 
        | INTERSECT query
        | EXCEPT query
        | empty
    '''
    insertProduction(t.slice, len(t.slice))

def p_queryP(t):
    'queryp : SELECT distinct select_list FROM table_expression condition group having order lim off  '
    t[0] =  select(t[2],t[3],t[5],t[6],t[7],t[8],t[9],t[10],t[11])
    insertProduction(t.slice, len(t.slice))

def p_distinct(t):
    'distinct : DISTINCT'
    t[0] = True
    insertProduction(t.slice, len(t.slice))

def p_distinctEmpty(t):
    'distinct : empty'
    t[0] = False
    insertProduction(t.slice, len(t.slice))

def p_select_listAll(t):
    'select_list : MULTIPLICACION'
    t[0]=[exp_id('*',None)]
    insertProduction(t.slice, len(t.slice))

def p_select_listList(t):
    'select_list : list'
    t[0] = t[1]
    insertProduction(t.slice, len(t.slice))

def p_list(t):
    'list : list COMA column aliascol'
    t[3].alias = t[4]
    t[1].append(t[3])
    t[0] = t[1]
    insertProduction(t.slice, len(t.slice))

def p_listSingle(t):
    'list : column aliascol'
    t[1].alias = t[2]
    t[0] = [t[1]]
    insertProduction(t.slice, len(t.slice))

def p_column(t):
    'column : ID columnp '
    if t[2] is None:
        t[0] = exp_id(t[1],None)
    else:
        t[0] = exp_id(t[2],t[1])
    insertProduction(t.slice, len(t.slice))

def p_columnFunc(t):
    '''
    column : trig
            | math
            | function
            | casewhen

    '''
    t[0] = t[1]
    insertProduction(t.slice, len(t.slice))

def p_TRIG(t):
    '''
        trig : ACOS PARA exp PARC
		| ACOSD PARA exp PARC
		| ASIN PARA exp PARC
		| ASIND PARA exp PARC
		| ATAN PARA exp PARC
		| ATAND PARA exp PARC
		| ATAN2 PARA exp COMA exp PARC
		| ATAN2D PARA exp COMA exp PARC
		| COS PARA exp PARC
		| COSD PARA exp PARC
		| COT PARA exp PARC
		| COTD PARA exp PARC
		| SIN PARA exp PARC
		| SIND PARA exp PARC
		| TAN PARA exp PARC
		| TAND PARA exp PARC
		| SINH PARA exp PARC
		| COSH PARA exp PARC 
		| TANH PARA exp PARC
		| ASINH PARA exp PARC
		| ACOSH PARA exp PARC
		| ATANH PARA exp PARC
    '''
    if t[1].lower() == 'acos' : t[0] =  trig_acos(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'acosd' : t[0] =  trig_acosd(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'asin' : t[0] =  trig_asin(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'asind' : t[0] =  trig_asind(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'atan' : t[0] =  trig_atan(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'atand' : t[0] =  trig_atand(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'atan2' : t[0] =  trig_atan2(t[3],t[5],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'atan2d' : t[0] =  trig_atan2d(t[3],t[5],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'cos' : t[0] =  trig_cos(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'cosd' : t[0] =  trig_cosd(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'cot' : t[0] =  trig_cot(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'cotd' : t[0] =  trig_cotd(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'sin' : t[0] =  trig_sin(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'sind' : t[0] =  trig_sind(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'tan' : t[0] =  trig_tan(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'tand' : t[0] =  trig_tand(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'sinh' : t[0] =  trig_sinh(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'cosh' : t[0] =  trig_cosh(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'tanh' : t[0] =  trig_tanh(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'asinh' : t[0] =  trig_asinh(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'acosh' : t[0] =  trig_acosh(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'atanh' : t[0] =  trig_atanh(t[3],None);insertProduction(t.slice, len(t.slice))


def p_math(t):
    '''
    math : ABS PARA  exp PARC
		| CBRT PARA  exp PARC
		| CEIL PARA  exp PARC
		| CEILING PARA  exp PARC
		| DEGREES PARA  exp PARC
		| DIV PARA  exp COMA exp PARC	
		| EXP PARA  exp PARC	
		| FACTORIAL PARA  exp PARC
		| FLOOR PARA  exp PARC
		| GCD PARA  exp COMA exp PARC
		| LCM PARA  exp COMA exp PARC
		| LN PARA  exp PARC
		| LOG PARA  exp COMA exp PARC
		| LOG10 PARA  exp PARC
		| MIN_SCALE PARA exp PARC
		| MOD PARA exp COMA exp PARC
		| PI PARA PARC
		| POWER PARA  exp COMA exp PARC
		| RADIANS PARA  exp PARC
		| ROUND PARA  exp PARC
		| SCALE PARA  exp PARC
		| SIGN PARA  exp PARC
		| SQRT PARA  exp PARC
		| TRIM_SCALE PARA exp PARC
		| TRUNC PARA  exp PARC 
		| WIDTH_BUCKET PARA  exp COMA exp COMA exp COMA exp PARC
		| RANDOM PARA PARC
		| SETSEED PARA  exp PARC    

    '''
    if t[1].lower() == 'abs' : t[0] =  math_abs(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'cbrt' : t[0] =  math_cbrt(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'ceil' : t[0] =  math_ceil(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'ceiling' : t[0] =  math_ceil(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'div' : t[0] =  math_div(t[3],t[5],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'exp' : t[0] =  math_exp(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'factorial' : t[0] =  math_factorial(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'floor' : t[0] =  math_floor(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'gcd' : t[0] =  math_gcd(t[3],t[5],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'lcm' : t[0] =  math_lcm(t[3],t[5],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'ln' : t[0] =  math_ln(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'log' : t[0] =  math_log(t[3],t[5],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'log10' : t[0] =  math_log10(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'min_scale' : t[0] =  math_min_scale(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'mod' : t[0] =  math_mod(t[3],t[5],None);(t.slice, len(t.slice))
    elif t[1].lower() == 'pi' : t[0] =  math_pi(None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'power' : t[0] =  math_power(t[3],t[5],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'radians' : t[0] =  math_radians(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'round' : t[0] =  math_round(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'scale' : t[0] =  math_scale(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'sign' : t[0] =  math_sign(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'sqrt' : t[0] =  math_sqrt(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'trim_scale' : t[0] =  math_trim_scale(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'trunc' : t[0] =  math_trunc(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'width_bucket' : t[0] =  math_widthBucket(t[3],t[5],t[7],t[9],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'random' : t[0] =  math_random(None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'setseed' : t[0] =  math_setseed(t[3],None);insertProduction(t.slice, len(t.slice))



def p_function(t):
    '''
        function : SUM PARA exp PARC
                | AVG PARA exp PARC
                | MAX PARA exp PARC
                | MIN PARA exp PARC
                | COUNT PARA exp PARC
                | LENGTH PARA exp PARC
                | SUBSTRING PARA exp COMA INT COMA INT PARC
                | TRIM PARA exp PARC
                | MD5 PARA exp PARC
                | SHA256 PARA exp PARC
                | SUBSTR PARA exp COMA INT COMA INT PARC
                | CONVERT PARA exp AS type PARC
                | GREATEST PARA lexps PARC
                | LEAST PARA lexps PARC
                | NOW PARA PARC

    '''
    if t[1].lower() == 'sum' : t[0] = fun_sum(t[3],None);insertProduction(t.slice, len(t.slice))
    elif t[1].lower() == 'avg' : t[0] = fun_avg(t[3],None);insertProduction(t.slice, len(t.slice))
    if t[1].lower() == 'max' : t[0] = fun_max(t[3],None);insertProduction(t.slice, len(t.slice))
    if t[1].lower() == 'min' : t[0] = fun_min(t[3],None);insertProduction(t.slice, len(t.slice))
    if t[1].lower() == 'count' : t[0] = fun_count(t[3],None);insertProduction(t.slice, len(t.slice))
    if t[1].lower() == 'length' : t[0] = fun_length(t[3],None);insertProduction(t.slice, len(t.slice))
    if t[1].lower() == 'substring' : t[0] = fun_substr(t[3],t[5],t[7],None);insertProduction(t.slice, len(t.slice))
    if t[1].lower() == 'trim' : t[0] = fun_trim(t[3],None);insertProduction(t.slice, len(t.slice))
    if t[1].lower() == 'md5' : t[0] = fun_md5(t[3],None);insertProduction(t.slice, len(t.slice))
    if t[1].lower() == 'sha256' : t[0] = fun_sha256(t[3],None);insertProduction(t.slice, len(t.slice))
    if t[1].lower() == 'substr' : t[0] = fun_substr(t[3],t[5],t[7],None);insertProduction(t.slice, len(t.slice))
    if t[1].lower() == 'convert' : t[0] = fun_convert(t[3],t[5],None);insertProduction(t.slice, len(t.slice))
    if t[1].lower() == 'greatest' : t[0] = fun_greatest(t[3],None);insertProduction(t.slice, len(t.slice))
    if t[1].lower() == 'least' : t[0] = fun_least(t[3],None);insertProduction(t.slice, len(t.slice))
    if t[1].lower() == 'NOW' : t[0] = fun_now();insertProduction(t.slice, len(t.slice))
    
def p_type(t):
    '''
    type : SMALLINT
        | INTEGER
        | BIGINT
        | DECIMAL
        | NUMERIC  
        | REAL 
        | DOUBLE   
        | PRECISION
        | CHARACTER
        | CHARACTER VARYING   
        | TEXT 
        | TIMESTAMP
    '''
    t[0] = t[1]
    insertProduction(t.slice, len(t.slice))

def p_lexps(t):
    'lexps : lexps COMA exp'
    t[1].append(t[3])
    t[0] = t[1]
    insertProduction(t.slice, len(t.slice))

def p_lexpsSingle(t):
    'lexps : exp '
    t[0] = [t[1]]
    insertProduction(t.slice, len(t.slice))

def p_columnp(t):
    '''columnp : PUNTO ID
            | PUNTO MULTIPLICACION
    '''
    t[0] = t[2]
    insertProduction(t.slice, len(t.slice))

def p_columnpEmpty(t):
    'columnp : empty'
    t[0] = None
    insertProduction(t.slice, len(t.slice))

def p_aliascol(t):
    'aliascol : AS ID'
    t[0] = t[2]
    insertProduction(t.slice, len(t.slice))

def p_aliascolEmpty(t):
    'aliascol : empty'
    t[0] = None
    insertProduction(t.slice, len(t.slice))

def p_table_expression(t):
    'table_expression : table_expression COMA texp'
    t[1].append(t[3])
    t[0] = t[1]
    insertProduction(t.slice, len(t.slice))

def p_table_expressionSingle(t):
    'table_expression : texp'
    t[0] = [t[1]]
    insertProduction(t.slice, len(t.slice))
    
def p_texp_id(t):
    'texp : ID aliastable'
    t[0] = texp_id(t[1],t[2])
    insertProduction(t.slice, len(t.slice))

def p_table_expressionQuery(t):
    'texp : PARA query PARC aliastable '
    t[0] = texp_query(t[2],t[4])
    insertProduction(t.slice, len(t.slice))

def p_aliastable(t):
    'aliastable : ID'
    t[0] = t[1]
    insertProduction(t.slice, len(t.slice))

def p_aliastableEmpty(t):
    'aliastable : empty'
    t[0] = None
    insertProduction(t.slice, len(t.slice))

def p_casewhen(t):
    'casewhen : CASE WHEN exp_case THEN exp casos else END aliastable'
    t[0] = casewhen( t[3], t[5], t[6], t[7], t[8])
    insertProduction(t.slice, len(t.slice))

def p_exp_case(t):
    'exp_case : exp oper exp'
    if t[2] == '='  : t[0] = exp_igual(t[1],t[3]);insertProduction(t.slice, len(t.slice))
    elif t[2] == '>': t[0] = exp_mayor(t[1], t[3]);insertProduction(t.slice, len(t.slice))
    elif t[2] == '<': t[0] = exp_menor(t[1], t[3]);insertProduction(t.slice, len(t.slice))
    elif t[2] == '<>': t[0] = exp_diferente(t[1], t[3]);insertProduction(t.slice, len(t.slice))
    elif t[2] == '>=': t[0] = exp_mayor_igual(t[1], t[3]);insertProduction(t.slice, len(t.slice))
    elif t[2] == '<=': t[0] = exp_menor_igual(t[1], t[3]);insertProduction(t.slice, len(t.slice))

def p_expcaseIn(t):
    'exp_case : exp IN PARA queryp PARC'
    t[0] = exp_in(t[1],t[4])
    insertProduction(t.slice, len(t.slice))

def p_expcaseNotIn(t):
    'exp_case : exp NOT IN PARA queryp PARC'
    t[0] = exp_not_in(t[1],t[5])
    insertProduction(t.slice, len(t.slice))

def p_expcaseBetween(t):
    'exp_case : exp BETWEEN exp AND exp'
    t[0] = exp_between(t[1],t[3],t[5])
    insertProduction(t.slice, len(t.slice))

def p_expcaseIsDistinct(t):
    'exp_case : exp IS DISTINCT FROM exp'
    t[0] = exp_diferente(t[1],t[5])
    insertProduction(t.slice, len(t.slice))

def p_expcaseIsNotDistinct(t):
    'exp_case : exp IS NOT DISTINCT FROM exp'
    t[0] = exp_igual(t[1],t[6])
    insertProduction(t.slice, len(t.slice))

def p_expcaseExists(t):
    'exp_case : EXISTS PARA queryp PARC'
    t[0] = exp_exists(t[3],None,True)
    insertProduction(t.slice, len(t.slice))

def p_expcaseNotExists(t):
    'exp_case : NOT EXISTS PARA queryp PARC'
    t[0] = exp_exists(t[3],None,False)
    insertProduction(t.slice, len(t.slice))

def p_expNum(t):
    '''exp : INT
            | DEC
    
    '''
    t[0] = exp_num(t[1])
    insertProduction(t.slice, len(t.slice))

def p_expText(t):
    'exp : VARCHAR'
    t[0] = exp_text(t[1])
    insertProduction(t.slice, len(t.slice))

def p_expBoolean(t):
    '''exp : TRUE
        | FALSE'''
    t[0] = exp_bool(t[1])
    insertProduction(t.slice, len(t.slice))

def p_expID(t):
    'exp : ID columnp'
    if t[2] is None:
        t[0] = exp_id(t[1],None)
    else:
        t[0] = exp_id(t[2],t[1])
    insertProduction(t.slice, len(t.slice))

def p_expUmas(t):
    'exp : MAS exp %prec UMAS'
    if not isinstance(t[2],exp_num):
        #Error semántico
        return
    t[0] = t[2]
    insertProduction(t.slice, len(t.slice))

def p_expUmenos(t):
    'exp : MENOS exp %prec UMENOS'
    if not isinstance(t[2],exp_num):
        #Error semántico
        return
    t[2].val *= -1
    t[0] = t[2]
    insertProduction(t.slice, len(t.slice))
    
def p_expCombined(t):
    ''' exp : exp MAS exp
            | exp MENOS exp
            | exp MULTIPLICACION exp
            | exp DIVISION exp 
            | PARA exp PARC

    '''
    if t[1] == '(' : 
        t[0] = t[2]
    else:
        if t[2] == '+'  : t[0] = exp_suma(t[1],t[3])
        elif t[2] == '-': t[0] = exp_resta(t[1], t[3])
        elif t[2] == '*': t[0] = exp_multiplicacion(t[1], t[3])
        elif t[2] == '/': t[0] = exp_division(t[1], t[3])
    insertProduction(t.slice, len(t.slice))

def p_oper(t):
    ''' oper : IGUAL
            | MAYOR
            | MENOR
            | MAYOR_IGUAL   
            | MENOR_IGUAL
            | DIFERENTE
    '''
    t[0] = t[1]
    insertProduction(t.slice, len(t.slice))

def p_casos(t):
    '''casos : lcases
    '''
    t[0] = t[1]
    insertProduction(t.slice, len(t.slice))

def p_casosEmpty(t):
    '''casos :  empty             
    '''
    t[0] = None
    insertProduction(t.slice, len(t.slice))

def p_lista_cases(t):
    'lcases : lcases WHEN exp_case THEN exp '
    t[2] = case(t[3],t[5])
    t[1].append(t[2])
    t[0] = t[1]
    insertProduction(t.slice, len(t.slice))

def p_lcasesSingle(t):
    'lcases :  WHEN exp_case THEN exp '
    t[0] =  [case(t[2],t[4])]
    insertProduction(t.slice, len(t.slice))

def p_else(t):
    'else : ELSE  exp '
    t[0] = t[2]
    insertProduction(t.slice, len(t.slice))

def p_elseEmpty(t):
    'else : empty'
    t[0] = None
    insertProduction(t.slice, len(t.slice))

def p_condition(t):
    'condition : WHERE lconditions  '
    t[0] = t[2]
    insertProduction(t.slice, len(t.slice))

def p_lconditions(t):
    'lconditions : lconditions andor exp_case'
    c = condition(t[3],t[2])
    t[1].append(c)
    t[0] = t[1]
    insertProduction(t.slice, len(t.slice))

def p_lconditionsSingle(t):
    'lconditions : exp_case'
    t[0] = [condition(t[1],None)]
    insertProduction(t.slice, len(t.slice))

def p_andor(t):
    '''
    andor : AND
        | OR
    '''
    t[0] = t[1]
    insertProduction(t.slice, len(t.slice))

def p_conditionEmpty(t):
    'condition : empty'
    t[0] = None
    insertProduction(t.slice, len(t.slice))

def p_groupby(t):
    'group : GROUP BY lids'
    t[0] = True
    insertProduction(t.slice, len(t.slice))

def p_groupbyEmpty(t):
    'group : empty'
    t[0] = False
    insertProduction(t.slice, len(t.slice))

def p_lids(t):
    'lids : lids COMA ID columnp'
    insertProduction(t.slice, len(t.slice))

def p_lidsSingle(t):
    'lids : ID columnp'
    insertProduction(t.slice, len(t.slice))

def p_having(t):
    'having : HAVING PARA exp_case PARC '
    t[0] = condition(t[3],'AND')
    insertProduction(t.slice, len(t.slice))

def p_havingEmpty(t):
    'having : empty'
    t[0] = None
    insertProduction(t.slice, len(t.slice))

def p_orderby(t):
    'order : ORDER BY ID columnp ascdsc'
    t[0] = [t[3],t[4],t[5]]
    insertProduction(t.slice, len(t.slice))

def p_orderbyEmpty(t):
    'order : empty'
    t[0] = None
    insertProduction(t.slice, len(t.slice))

def p_ascdsc(t):
    '''ascdsc : ASC
                | DESC
    
    '''
    t[0] = t[1]
    insertProduction(t.slice, len(t.slice))

def p_lim(t):
    'lim : LIMIT INT'
    t[0] = t[2]
    insertProduction(t.slice, len(t.slice))

def p_limit(t):
    'lim : empty'
    t[0] = 0
    insertProduction(t.slice, len(t.slice))

def p_offset(t):
    'off : OFFSET INT'
    t[0] = t[2]
    insertProduction(t.slice, len(t.slice))

def p_offsetEmpty(t):
    'off : empty'
    t[0] = 0
    insertProduction(t.slice, len(t.slice))

def p_error(t):
    if t:
        descript = 'error sintactico en el token ' + str(t.type)
        linea = str(t.lineno)
        columna = str(find_column(t))
        nuevo_error = CError(linea,columna,descript,'Sintactico')
        insert_error(nuevo_error)
        parser.errok()
    else:
        print("Syntax error at EOF")
    return

import ply.yacc as yacc
parser = yacc.yacc()  

def parse(input):
    global entrada
    entrada = input
    return parser.parse(input)

def find_column(token):
    global entrada
    line_start = entrada.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1