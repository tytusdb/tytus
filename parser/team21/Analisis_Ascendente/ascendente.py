import re


from Compi2RepoAux.team21.Analisis_Ascendente.reportes.Reportes import RealizarReportes,Error





L_errores_lexicos = []
L_errores_sintacticos = []
consola = []
exceptions = []
columna = 0

from graphviz import Digraph


varGramatical = []
varSemantico = []
reservadas = {
    'smallint': 'SMALLINT',
    'integer': 'INTEGER',
    'bigint': 'BIGINT',
    'decimal': 'DECIMAL',
    'numeric': 'NUMERIC',
    'double': 'DOUBLE',
    'precision': 'PRECISION',
    'real': 'REAL',
    'money': 'MONEY',
    'text': 'TEXT',
    'varying': 'VARYING',
    'varchar': 'VARCHAR',
    'character': 'CHARACTER',
    'char': 'CHAR',
    'timestamp': 'TIMESTAMP',
    'date': 'DATE',
    'time': 'TIME',
    'interval': 'INTERVAL',
    'year': 'YEAR',
    'month': 'MONTH',
    'day': 'DAY',
    'hour': 'HOUR',
    'minute': 'MINUTE',
    'second': 'SECOND',
    'to': 'TO',
    'boolean': 'BOOLEAN',
    'true': 'TRUE',
    'false': 'FALSE',
    'create': 'CREATE',
    'type': 'TYPE',
    'as': 'AS',
    'enum': 'ENUM',
    'not': 'NOT',
    'and': 'AND',
    'or': 'OR',
    'is': 'IS',
    'null': 'NULL',
    'between': 'BETWEEN',
    'in': 'IN',
    'ilike': 'ILIKE',
    'like': 'LIKE',
    'similar': 'SIMILAR',
    'table': 'TABLE',
    'replace': 'REPLACE',
    'database': 'DATABASE',
    'databases': 'DATABASES',
    'show': 'SHOW',
    'if': 'IF',
    'exists': 'EXISTS',
    'alter': 'ALTER',
    'rename': 'RENAME',
    'owner': 'OWNER',
    'mode': 'MODE',
    'drop': 'DROP',
    'constraint': 'CONSTRAINT',
    'unique': 'UNIQUE',
    'check': 'CHECK',
    'references': 'REFERENCES',
    'primary': 'PRIMARY',
    'key': 'KEY',
    'foreign': 'FOREIGN',
    'add': 'ADD',
    'column': 'COLUMN',
    'set': 'SET',
    'select': 'SELECT',
    'from': 'FROM',
    'delete': 'DELETE',
    'where': 'WHERE',
    'default': 'DEFAULT',
    'insert': 'INSERT',
    'into': 'INTO',
    'values': 'VALUES',
    'update': 'UPDATE',
    'count': 'COUNT',
    'avg': 'AVG',
    'sum': 'SUM',
    'distinct': 'DISTINCT',
    'abs': 'ABS',
    'cbrt': 'CBRT',
    'ceil': 'CEIL',
    'ceiling': 'CEILING',
    'degrees': 'DEGREES',
    'div': 'DIV',
    'exp': 'EXP',
    'factorial': 'FACTORIAL',
    'floor': 'FLOOR',
    'gcd': 'GCD',
    'lcm': 'LCM',
    'ln': 'LN',
    'log': 'LOG',
    'log10': 'LOG10',
    'min_scale': 'MIN_SCALE',
    'mod': 'MOD',
    'pi': 'PI',
    'power': 'POWER',
    'radians': 'RADIANS',
    'round': 'ROUND',
    'scale': 'SCALE',
    'sign': 'SIGN',
    'sqrt': 'SQRT',
    'trim_scale': 'TRIM_SCALE',
    'truc': 'TRUC',
    'width_bucket': 'WIDTH_BUCKET',
    'random': 'RANDOM',
    'setseed': 'SETSEED',
    'max': 'MAX',
    'min': 'MIN',
    'having': 'HAVING',
    'union': 'UNION',
    'intersect': 'INTERSECT',
    'except': 'EXCEPT',
    'all': 'ALL',
    'acos': 'ACOS',
    'acosd': 'ACOSD',
    'asin': 'ASIN',
    'asind': 'ASIND',
    'atan': 'ATAN',
    'atand': 'ATAND',
    'atan2': 'ATAN2',
    'atan2d': 'ATAN2D',
    'cos': 'COS',
    'cosd': 'COSD',
    'cot': 'COT',
    'cotd': 'COTD',
    'sin': 'SIN',
    'sind': 'SIND',
    'tan': 'TAN',
    'tand': 'TAND',
    'sinh': 'SINH',
    'cosh': 'COSH',
    'tanh': 'TANH',
    'asinh': 'ASINH',
    'acosh': 'ACOSH',
    'atanh': 'ATANH',
    'group': 'GROUP',
    'by': 'BY',
    'now': 'NOW',
    'current_date': 'CURRENT_DATE',
    'current_time': 'CURRENT_TIME',
    'date_part': 'date_part',
    'isnull': 'ISNULL',
    'notnull': 'NOTNULL',
    'unknown': 'UNKNOWN',
    'extract': 'EXTRACT',
    'inherits':'INHERITS',
    'serial':'SERIAL',
    'on':'ON',
    'inner':'INNER',
    'join':'JOIN',
    'left':"LEFT",
    'right':"RIGHT",
    'full':'FULL',
    'outer':'OUTER',
    'md5':'MD5',
    'sing':'SING',
    'width_bucket':'WIDTH_BUCKET',
    'trunc':'TRUNC',
    'length':'LENGTH',
    'substring':'SUBSTRING',
    'trim':'TRIM',
    'sha256':'SHA256',
    'substr':'SUBSTR',
    'get_byte':'GET_BYTE',
    'set_byte':'SET_BYTE',
    'convert':'CONVERT',
    'encode':'ENCODE',
    'decode':'DECODE',
    'greatest':'GREATEST',
    'least':'LEAST',
    'order':'ORDER',
    'by':'BY',
    'limit':'LIMIT',
    'offset':'OFFSET',
    'when':'WHEN',
    'case':'CASE',
    'then':'THEN',
    'end':'END'


}




tokens = [
             'PTCOMA',
             'COMA',
             'LLIZQ',
             'LLDR',
             'PARIZQ',
             'PARDR',
             'IGUAL',
             'MAS',
             'MENOS',
             'GNOT',
             'MULT',
             'DIVI',
             'ANDO',
             'ORO',
             'NOTO',
             'MENOR',
             'MAYOR',
             'IGUALIGUAL',
             'NOIGUAL',
             'NUMDECIMAL',
             'ENTERO',
             'CADENA',
             'ID',
             'MODU',
             'PUNTO',
             'EXPO',
             'MAYORIGUAL',
             'MENORIGUAL',
             'MENMEN',
             'MAYMAY',
             'MENMAY',
             'CRIZQ',
             'CRDR',

         ] + list(reservadas.values())

# Tokens
t_PTCOMA = r';'
t_COMA = r','
t_PARIZQ = r'\('
t_PARDR = r'\)'
t_IGUAL = r'='
t_MAS = r'\+'
t_MENOS = r'-'
t_GNOT = r'~'
t_MULT = r'\*'
t_DIVI = r'/'
t_ANDO = r'\&'
t_ORO = r'\|'
t_NOTO = r'!'
t_MENOR = r'<'
t_MAYOR = r'>'
t_IGUALIGUAL = r'=='
t_MAYORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_MENMEN = r'<<'
t_MAYMAY = r'>>'
t_NOIGUAL = r'!='
t_MENMAY = r'<>'
t_MODU = r'%'
t_PUNTO = r'\.'
t_EXPO = r'\^'
t_LLIZQ = r'\{'
t_LLDR = r'\}'
t_CRIZQ = r'\['
t_CRDR = r'\]'


def t_NUMDECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
        global columna
        columna = contador_columas(len(str(t.value)))
    except ValueError:
        print("Valor no es parseable a decimal %d", t.value)
        t.value = 0
    return t


def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
        global columna
        columna = contador_columas(len(str(t.value)))
    except ValueError:
        print("Valor no es parseable a integer %d", t.value)
        t.value = 0
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9_]*'
    t.type = reservadas.get(t.value.lower(), 'ID')
    global columna
    columna = contador_columas(len(str(t.value)))
    return t


def t_CADENA(t):
    r'(\".*?\")|(\'.*?\')'
    t.value = t.value[1:-1]  # remuevo las comillas
    global columna
    columna = contador_columas(len(str(t.value)))
    return t


def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    global columna
    columna = 0


# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'--.*\n'
    t.lexer.lineno += 1
    global columna
    columna = 0


#t_ignore = " \t"
def t_IGNORAR(t):
    r'\ |\t'
    global columna
    if t.value == '\t':
        columna = contador_columas(columna+7)
    else:
        columna = contador_columas(columna)


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    global columna
    columna = 0


def t_error(t):
    global L_errores_lexicos;
    global columna

    colum = contador_columas(columna)
    data = Error(str("Error Lexico"),str(t.value[0]), str(t.lexer.lineno),str(colum))
    L_errores_lexicos.append(data)
    print("Caracter irreconocible! '%s'" % t.value[0])
    t.lexer.skip(1)


import ply.lex as lex

lexer = lex.lex()
lex.lex(reflags=re.IGNORECASE)

# from expresion import *

from Compi2RepoAux.team21.Analisis_Ascendente.Instrucciones.expresion import *
from Compi2RepoAux.team21.Analisis_Ascendente.Instrucciones.instruccion import *
from Compi2RepoAux.team21.Analisis_Ascendente.Instrucciones.Create.createTable import CreateTable
from Compi2RepoAux.team21.Analisis_Ascendente.Instrucciones.Create.createDatabase import CreateReplace,ComplementoCR



precedence = (
    ('left', 'OR'),
    ('left', 'AND', 'BETWEEN', 'NOT', 'LIKE', 'ILIKE', 'IN','ON'),
    ('left', 'ORO'),
    ('left', 'ANDO'),
    ('left', 'NOIGUAL', 'MENMAY', 'IGUALIGUAL'),
    ('left', 'MAYOR', 'MENOR', 'MAYORIGUAL', 'MENORIGUAL'),
    ('left', 'MAYMAY', 'MENMEN'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'MULT', 'DIVI', 'MODU'),
    ('left', 'EXPO'),
    ('left', 'NOTO', 'GNOT'),
    ('left', 'PARIZQ', 'PARDR')
)



#varSemantico.append('SEMANTICO')
def p_s(t):
    's               : instrucciones'
    t[0] = t[1]
    print(t[0])
    varGramatical.append('s ::= intrucciones')
    varSemantico.append('g ')

def p_instrucciones(t):
    '''instrucciones    : instrucciones instruccion'''
    t[1].append(t[2])
    t[0] = t[1]
    varGramatical.append('instrucciones ::= instrucciones instruccion')
    varSemantico.append('f ')

def p_instruccion(t):
    'instrucciones      : instruccion'
    t[0] = [t[1]]
    varGramatical.append('instrucciones ::= instruccion')
    varSemantico.append('e ')

# CREATE
def p_create(t):
    'instruccion        : CREATE TABLE ID PARIZQ campos PARDR PTCOMA'

    t[0] = CreateTable(t[3], t[5], None)
    varGramatical.append('instruccion :: = CREATE TABLE ID PARIZQ campos PARDR PTCOMA')
    varSemantico.append('t ')



def p_create2(t):
    'instruccion        : CREATE TABLE ID PARIZQ campos PARDR INHERITS PARIZQ ID PARDR PTCOMA'
    t[0] = CreateTable(t[3], t[5], t[9])
    varGramatical.append('instruccion :: = CREATE TABLE ID PARIZQ campos PARDR INHERITS PARIZQ ID PARDR PTCOMA')
    varSemantico.append('tw ')

def p_campos(t):
    '''campos           : campos COMA campo'''
    t[1].append(t[3])
    t[0] = t[1]
    varGramatical.append('campos :: = campos COMA campo')
    varSemantico.append('y ')

def p_campos2(t):
    'campos             : campo'
    t[0] = [t[1]]
    varGramatical.append('campos :: = campo')
    varSemantico.append(' p')

def p_campoSimple(t):
    'campo              : ID tipo'
    t[0] = Campo(1, t[1], t[2], None, None, None, None)
    varGramatical.append('campo :: = ID tipo')
    varSemantico.append(' q')

def p_campo(t):
    '''campo            : ID tipo acompaniamiento'''
    t[0] = Campo(1, t[1], t[2], t[3], None, None, None)
    varGramatical.append('campo :: = ID tipo acompaniamiento')
    varSemantico.append('m ')

def p_foreign(t):
    'campo              : CONSTRAINT ID FOREIGN KEY PARIZQ listaID PARDR REFERENCES ID PARIZQ listaID PARDR'
    t[0] = Campo(2, t[2], None, None, t[6], t[9], t[11])
    varGramatical.append('campo :: = CONSTRAINT ID FOREIGN KEY PARIZQ listaID PARDR REFERENCES ID PARIZQ listaID PARDR')
    varSemantico.append('z ')

def p_foreign2(t):
    'campo              : FOREIGN KEY PARIZQ listaID PARDR REFERENCES ID PARIZQ listaID PARDR'
    t[0] = Campo(3, None, None, None, t[4], t[7], t[9])
    varGramatical.append('campo :: = FOREIGN KEY PARIZQ listaID PARDR REFERENCES ID PARIZQ listaID PARDR')
    varSemantico.append(' x')

def p_campoCadenas(t):
    'campo              : CADENA'
    varGramatical.append('campo :: = CADENA')
    varSemantico.append(' x')

def p_primary(t):
    'campo              : PRIMARY KEY PARIZQ listaID PARDR'
    t[0] = Campo(4, t[4], None, None, None, None, None)
    varGramatical.append('campo :: = PRIMARY KEY PARIZQ listaID PARDR')
    varSemantico.append('c ')

def p_listacampo(t):
    '''acompaniamiento  : acompaniamiento acom'''
    t[1].append(t[2])
    t[0] = t[1]
    # print(t[0])
    varGramatical.append('acompaniamiento :: = acompaniamiento acom')
    varSemantico.append(' v')

def p_listacampo2(t):
    'acompaniamiento    : acom'
    t[0] = [t[1]]
    varGramatical.append('acompaniamiento :: = acom')
    varSemantico.append('b ')

def p_acompaniamiento(t):
    '''acom             : NOT NULL
                        | NULL
                        | UNIQUE PARIZQ listaID PARDR
                        | DEFAULT valores
                        | PRIMARY KEY
                        | CONSTRAINT ID
                        | REFERENCES ID
                        | CHECK PARIZQ checkprima PARDR
                        '''


    if t[1].lower() == 'not'         :
        t[0] = Acompaniamiento('NOT', None)
        varGramatical.append('acom :: = NOT NULL')
        varSemantico.append(' n')
    elif t[1].lower() == 'null'      :
        t[0] = Acompaniamiento('NULL', None)
        varGramatical.append('acom :: = NULL')
        varSemantico.append('re ')
    elif t[1].lower() == 'unique'    :
        t[0] = Acompaniamiento('UNIQUE', t[3])
        varGramatical.append('acom :: = UNIQUE PARIZQ listaID PARDR')
        varSemantico.append(' we')
    elif t[1].lower() == 'default'   :
        t[0] = Acompaniamiento('DEFAULT', t[2])
        varGramatical.append('acom :: = DEFAULT valores')
        varSemantico.append(' qw')
    elif t[1].lower() == 'primary'   :
        t[0] = Acompaniamiento('PRIMARY', None)
        varGramatical.append('acom :: = PRIMARY KEY')
        varSemantico.append('yt ')
    elif t[1].lower() == 'constraint':
        t[0] = Acompaniamiento('CONSTRAINT',t[2])
        varGramatical.append('acom :: = CONSTRAINT ID')
        varSemantico.append('yt ')
    elif t[1].lower() == 'references':
        t[0] = Acompaniamiento('REFERENCES',t[2])
        varGramatical.append('acom :: = REFERENCES ID')
        varSemantico.append('yt ')
    elif t[1].lower() == 'check'   :
        t[0] = Acompaniamiento('CHECK', None)
        varGramatical.append('acom :: = CHECK PARIZQ checkprima PARDR')
        varSemantico.append('yt ')




def p_acompaniamiento2(t):
    'acom               : UNIQUE'
    t[0] = Acompaniamiento('UNIQUE', None)
    varGramatical.append('acom :: = UNIQUE')
    varSemantico.append('yt3 ')

def p_acompaniamiento3(t):
    'acom               : UNIQUE ID'
    t[0] = Acompaniamiento('UNIQUE', Id(t[2]))
    varGramatical.append('acom :: = UNIQUE ID')
    varSemantico.append('yt3 ')


def p_tipos(t):
    '''tipo             : SMALLINT
                        | INTEGER
                        | BIGINT
                        | DECIMAL
                        | NUMERIC
                        | REAL
                        | DOUBLE
                        | MONEY
                        | TEXT
                        | TIMESTAMP
                        | DATE
                        | TIME
                        | INTERVAL
                        | BOOLEAN
                        | SERIAL'''
    t[0] = Tipo(t[1].upper(), None)
    varGramatical.append('tipo :: = '+str(t[1]))
    varSemantico.append('fr ')


def p_tiposTexto(t):
    '''tipo             : CHARACTER PARIZQ ENTERO PARDR
                        | VARCHAR PARIZQ ENTERO PARDR
                        | CHAR PARIZQ ENTERO PARDR
                        | CHARACTER VARYING PARIZQ ENTERO PARDR'''

    if t[2] == '(':
        t[0] = Tipo(t[1].upper(), Primitivo(t[3]))
    else:
        t[0] = Tipo(t[1].upper() + ' ' + t[2].upper(), Primitivo(t[4]))

    if t[3]=='(':
        varGramatical.append('tipo :: =' + str(t[1]) + str(t[2]) + str(t[3])+ str(t[4]) + str(t[5]))
        varSemantico.append('gt ')
    else:
        varGramatical.append('tipo :: =' + str(t[1]) + str(t[2]) + str(t[3]) + str(t[4]))
        varSemantico.append('yt5 ')

# INSERT INTO
def p_insertInto(t):
    'instruccion        : INSERT INTO ID PARIZQ listaID PARDR VALUES values PTCOMA'
    t[0] = t[1]
    varGramatical.append('instruccion :: = INSERT INTO ID PARIZQ listaID PARDR VALUES values PTCOMA')
    varSemantico.append('ot ')


def p_insertInto2(t):
    'instruccion        : INSERT INTO ID VALUES values PTCOMA'
    t[0] = InsertInto(t[3], None, t[5])
    varGramatical.append('instruccion :: = INSERT INTO ID VALUES values PTCOMA')
    varSemantico.append('yg ')


# lista de id
def p_listaID(t):
    'listaID            : listaID COMA var'
    t[1].append(t[3])
    t[0] = t[1]
    varGramatical.append('listaID :: = listaID COMA var')
    varSemantico.append('io ')



def p_listaID2(t):
    'listaID            : var'
    t[0] = [t[1]]
    varGramatical.append('listaID :: = var')
    varSemantico.append('iq ')



def p_values(t):
    'values             : values COMA value'
    t[1].append(t[3])
    t[0] = t[1]
    varGramatical.append('values :: = values COMA value')
    varSemantico.append('iw ')



def p_values2(t):
    'values             : value'
    t[0] = [t[1]]
    varGramatical.append('values :: = value')
    varSemantico.append('ie ')

def p_value(t):
    'value              : PARIZQ listaValores PARDR'
    t[0] = t[2]
    varGramatical.append('value :: = PARIZQ listaValores PARDR')
    varSemantico.append('ir ')

# lista de valores
def p_listaValores(t):
    'listaValores       : listaValores COMA valores'
    t[1].append(t[3])
    t[0] = t[1]
    varGramatical.append('listaValores :: = listaValores COMA valores')
    varSemantico.append('it ')



def p_listaValores2(t):
    'listaValores       : valores'
    t[0] = [t[1]]
    varGramatical.append('listaValores :: = valores')
    varSemantico.append('iy ')



# VALORES
def p_valores(t):

    '''valores          : ENTERO '''

    t[0] = Primitivo(t[1])
    varGramatical.append('valores ::= ENTERO')
    varSemantico.append('iu ')

def p_valoresDec(t):
    '''valores          : NUMDECIMAL  '''
    t[0] = Primitivo(t[1])
    varGramatical.append('valores ::= NUMDECIMAL')
    varSemantico.append('iu2 ')

def p_valoresCad(t):
    '''valores          : CADENA  '''
    t[0] = Primitivo(t[1])
    varGramatical.append('valores ::= CADENA')
    varSemantico.append('ii ')



#este es un conjunto de valores o llamada a metodos
# ejemplo (1,2,3,4,5,6)  now()  sqrt()
def p_valoresCad1(t):
    '''valores          : columna  '''
    t[0] = Primitivo(t[1])
    varGramatical.append('valores ::= columna')
    varSemantico.append('fd ')

def p_valoresCad2(t):
    '''valores          : NOW PARIZQ PARDR  '''
    t[0] = Primitivo(t[1])
    varGramatical.append('valores ::= NOW PARIZQ PARDR')
    varSemantico.append('fd ')


#def p_valores2(t):
 #   '''valores2         : valores
  #                      | var'''
   # t[0] = Primitivo(t[1])



# UPDATE
def p_update(t):
    'instruccion        : UPDATE ID SET asignaciones PTCOMA'
    t[0] = Update(t[2], t[4], None)
    varGramatical.append('instruccion ::= UPDATE ID SET asignaciones PTCOMA')
    varSemantico.append('ip ')



def p_update2(t):
    'instruccion        : UPDATE ID SET asignaciones WHERE andOr PTCOMA'
    t[0] = Update(t[2], t[4], t[6])
    varGramatical.append('instruccion ::= UPDATE ID SET asignaciones WHERE andOr PTCOMA')
    varSemantico.append('is ')



def p_asignaciones(t):
    'asignaciones       : asignaciones COMA asignacion'
    t[1].append(t[3])
    t[0] = t[1]
    varGramatical.append('asignaciones ::= asignaciones COMA asignacion')
    varSemantico.append('id ')



def p_asignaciones2(t):
    'asignaciones       : asignacion'
    t[0] = [t[1]]
    varGramatical.append('asignaciones ::= asignacion')
    varSemantico.append('if ')


def p_where(t):
    '''where            : asignacion
                        '''
    t[0] = t[1]
    varGramatical.append('where ::= asignacion')
    varSemantico.append('ig ')



def p_where7(t):
    '''where            : boolean
                        '''
    t[0] = t[1]
    varGramatical.append('where ::= boolean')
    varSemantico.append('in ')


def p_whereN(t):
    '''where            : NOT boolean
                        | columna IN PARIZQ listaValores PARDR
                        | columna BETWEEN valores AND valores '''
    #if t[1].lower() == 'not'     :
        #t[0] = Where(1, t[2], None, None, None)
     #   varGramatical.append('where ::= NOT boolean')
      #  varSemantico.append('in3 ')
    #elif t[2].lower() == 'in'    :
       #t[0] = Where(2, None, t[4], None, None)
     #  varGramatical.append('where ::= columna IN PARIZQ listaValores PARDR')
     #  varSemantico.append('in3 ')
    #else                         :
       #t[0] = Where(3, None, None, t[3], t[5])
     #   varGramatical.append('where ::= columna BETWEEN valores AND valores')
     #   varSemantico.append('in3 ')
# revisar aqui

def p_whereN_1(t):
    '''where             : var ILIKE valores
                         | var LIKE valores
                          '''
    if t[2] == 'ILIKE':
        varGramatical.append('where ::= ILIKE')
        varSemantico.append('in3 ')
    else:
        varGramatical.append('where ::= LIKE')
        varSemantico.append('in4 ')

def p_where1(t):
    '''where            : valores  comparisonP2
                        | var comparisonP2
                        | boolean  comparisonP
                        '''
    t[0] = t[1]
    #varGramatical.append('where ::= NOT boolean')
    #varSemantico.append('ih ')

def p_where2(t):

    '''where            : var IS NOT DISTINCT FROM valores '''
    t[0] = t[1]
    varGramatical.append('where ::= var IS NOT DISTINCT FROM valores')
    varSemantico.append('ih ')
#corregir aqui freddy

def p_where3(t):
    '''where            : var IS DISTINCT FROM valores
                        '''
    t[0] = t[1]
    varGramatical.append('where ::= var IS DISTINCT FROM valores')
    varSemantico.append('ih3 ')


def p_where4(t):
    '''where            : var NOT IN PARIZQ select2 PARDR
                        '''
    t[0] = t[1]
    varGramatical.append('where ::= var NOT IN PARIZQ select2 PARDR')
    varSemantico.append('ih4 ')

def p_ComparisonP(t):
    ''' comparisonP     : IS TRUE
                        | IS FALSE
                        | IS UNKNOWN
    '''
    varGramatical.append('comparisonP ::= '+str(t[1])+' '+str(t[2]))
    varSemantico.append('ix ')

def p_ComparisonP1(t):
    ''' comparisonP     : IS NOT TRUE
                        | IS NOT FALSE
                        | IS NOT UNKNOWN
    '''
    varGramatical.append('comparisonP ::= ' + str(t[1])+' '+str(t[2])+' '+str(t[3]))
    varSemantico.append('ix3 ')


def p_ComparisonP2(t):
    ''' comparisonP2    : IS NULL
    '''
    varGramatical.append('comparisonP2 ::= IS NULL')
    varSemantico.append('zx ')


def p_ComparisonP3(t):
    ''' comparisonP2    : IS NOT NULL
    '''
    varGramatical.append('comparisonP2 ::=  IS NOT NULL')
    varSemantico.append('cx ')


def p_ComparisonP4(t):
    ''' comparisonP2    : NOTNULL
                        | ISNULL
    '''
    varGramatical.append('comparisonP2 ::= ' + str(t[1]))
    varSemantico.append('iv ')


def p_andOr(t):
    '''andOr            : andOr AND andOr
                        | andOr OR andOr
                         '''
    t[0] = Expresion(t[1], t[3], t[2])
    if t[2].lower() == 'and':
        varGramatical.append('andOr ::= andOr AND andOr')
        varSemantico.append('iv9 ')
    else:
        varGramatical.append('andOr ::= andOr OR andOr')
        varSemantico.append('iv8 ')

def p_andOr2(t):
    'andOr              : where'
    t[0] = t[1]
    varGramatical.append('andOr ::= where')
    varSemantico.append('iv6 ')

#LA ASGINACION SE DEJA DE ESTA FORMA PUESTO QUE LA EXPRESION
#ABSORVE ESTO
def p_asignacion(t):
    '''asignacion       : E IGUAL E

    '''
    t[0] = Asignacion(t[1], t[3])
    varGramatical.append('asignacion ::= E IGUAL E')
    varSemantico.append('iv6 ')


def p_E(t):
    '''E                : operando
	                    | boolean
                        | unario
                        | valores
                        | var
                        | pnum
                        | math'''
    t[0] = t[1]



def p_E1(t):
    '''E                : PARIZQ E PARDR '''
    t[0] = t[2]
    varGramatical.append('E ::= PARIZQ E PARDR')
    varSemantico.append('iv61 ')
#    print("expresion")
#    if t[1] == '('  : t[0] = t[2]
#    else            : t[0] = t[1]

def p_E2(t):
    '''boolean          : FALSE
                        | TRUE'''
    t[0] = Primitivo(t[1])
    varGramatical.append('boolean ::= '+ str(t[1]))
    varSemantico.append('iv62 ')

def p_oper(t):
    '''operando         : E MAS E
	                    | E MENOS E
	                    | E MULT E
 	                    | E DIVI E
                        | E MODU E
                        | E EXPO E
	                    | E MENMEN E
	                    | E MAYMAY E
	                    | E ANDO E
	                    | E ORO E
	                '''
    t[0] = Expresion(t[1], t[3], t[2])
    varGramatical.append('operando ::= E '+str(t[2])+' '+'E')
    varSemantico.append('iv134 ')

def p_booleanos(t):
    '''boolean          : E IGUALIGUAL E
	                    | E NOIGUAL E
                        | E MENMAY E
	                    | E MENOR E
	                    | E MAYOR E
	                    | E MENORIGUAL E
	                    | E MAYORIGUAL E'''
    t[0] = Expresion(t[1], t[3], t[2])
    if t[2] =='==':
        varGramatical.append('boolean ::= E IGUALIGUAL E')
        varSemantico.append('iv62 ')
    elif t[2] =='!=':
        varGramatical.append('boolean ::= E NOIGUAL E')
        varSemantico.append('iv62 ')
    elif t[2] =='<>':
        varGramatical.append('boolean ::= E MENMAY E')
        varSemantico.append('iv62 ')
    elif t[2] == '<':
        varGramatical.append('boolean ::= E MENOR E')
        varSemantico.append('iv62 ')
    elif t[2] == '>':
        varGramatical.append('boolean ::= E MAYOR E')
        varSemantico.append('iv62 ')
    elif t[2] == '<=':
        varGramatical.append('boolean ::= E MENORIGUAL E')
        varSemantico.append('iv62 ')
    elif t[2] == '>=':
        varGramatical.append('boolean ::= E MAYORIGUAL E')
        varSemantico.append('iv62 ')

def p_unarios(t):
    '''unario           : NOTO E
	                    | MENOS E
	                    | GNOT E
                        | MAS E '''
    t[0] = Unario(t[1], t[2])
    print(t[1])
    if t[1] =='!':
        varGramatical.append('unario ::= NOTO E')
        varSemantico.append('iv64 ')
    elif t[1] =='-':
        varGramatical.append('unario ::= MENOS E')
        varSemantico.append('iv624 ')
    elif t[1] =='~':
        varGramatical.append('unario ::= GNOT E')
        varSemantico.append('iv625 ')
    elif t[1] == '+':
        varGramatical.append('unario ::= MAS E')
        varSemantico.append('iv626 ')

def p_var(t):
    'var                : ID'
    t[0] = Id(t[1])
    varGramatical.append('var ::= ID')
    varSemantico.append('iv626 ')


def p_alias(t):
    'var                : ID PUNTO ID'
    print(t[1] +t[2]+t[3])
    t[0] = IdId(Id(t[1]), Id(t[3]))
    varGramatical.append('var ::= ID PUNTO ID')
    varSemantico.append('ip5 ')

def p_pnum2(t):
    '''pnum                : PUNTO E'''
    print('punto')
    # t[0] = Id(t[1])
    varGramatical.append('pnum ::= PUNTO E')
    varSemantico.append('ip4 ')

# DELETE
def p_delete(t):
    'instruccion        : DELETE FROM ID WHERE andOr PTCOMA'
    t[0] = Delete(t[3], t[5])
    varGramatical.append('instruccion ::= DELETE FROM ID WHERE andOr PTCOMA')
    varSemantico.append('ip3 ')

def p_delete2(t):
    'instruccion        : DELETE FROM ID PTCOMA'
    t[0] = Delete(t[3], None)
    varGramatical.append('instruccion ::= DELETE FROM ID PTCOMA')
    varSemantico.append('ip31 ')

# DROP
def p_drop(t):
    '''instruccion      : DROP DATABASE ID PTCOMA
                        | DROP DATABASE IF EXISTS ID PTCOMA
                        | DROP TABLE ID PTCOMA'''
    if t[2].upper() == 'TABLE'  :
        t[0] = Drop(2, False, t[3])
        varGramatical.append('instruccion ::= DROP TABLE ID PTCOMA')
        varSemantico.append('ip32 ')
    elif t[3].upper() == 'IF'   :
        t[0] = Drop(1, True, t[5])
        varGramatical.append('instruccion ::= DROP DATABASE IF EXISTS ID PTCOMA')
        varSemantico.append('ip33 ')
    else                        :
        t[0] = Drop(1, False, t[3])
        varGramatical.append('instruccion ::= DROP DATABASE ID PTCOMA')
        varSemantico.append('ip34 ')


# CREATE or REPLACE DATABASE
def p_createDB(t):
    '''instruccion      : opcionCR ID PTCOMA
                        | opcionCR IF NOT EXISTS ID PTCOMA'''
    if t[2] == 'IF'     :
        t[0] = CreateReplace(t[1], True, t[5], None)
        varGramatical.append('instruccion ::= opcionCR IF NOT EXISTS ID PTCOMA')
        varSemantico.append('ip35 ')
    else                :
        t[0] = CreateReplace(t[1], False, t[2], None)
        varGramatical.append('instruccion ::= opcionCR ID PTCOMA')
        varSemantico.append('ip36 ')


def p_createDB2(t):
    '''instruccion      : opcionCR ID complemento PTCOMA
                        | opcionCR IF NOT EXISTS ID complemento PTCOMA'''
    if t[2] == 'IF'     :
        t[0] = CreateReplace(t[1], True, t[5], t[6])
        varGramatical.append('instruccion ::= opcionCR IF NOT EXISTS ID complemento PTCOMA')
        varSemantico.append('ip38 ')
    else                :
        t[0] = CreateReplace(t[1], False, t[2], t[3])
        varGramatical.append('instruccion ::= opcionCR ID complemento PTCOMA')
        varSemantico.append('ip37 ')

def p_opcionCR(t):
    '''opcionCR         : CREATE DATABASE
                        | CREATE OR REPLACE DATABASE'''
    if t[2].upper() == 'OR'     :
        t[0] = 2
        varGramatical.append('opcionCR ::= CREATE OR REPLACE DATABASE')
        varSemantico.append('ip38 ')
    else                        :
        t[0] = 1
        varGramatical.append('opcionCR ::= CREATE DATABASE')
        varSemantico.append('ip39 ')

def p_complementoCR(t):
    '''complemento      : OWNER IGUAL ID
                        | OWNER ID'''
    if t[2] == '='      :
        t[0] = ComplementoCR(t[3], None)
        varGramatical.append('complemento ::= OWNER IGUAL ID')
        varSemantico.append('ip40 ')
    else                :
        t[0] = ComplementoCR(t[2], None)
        varGramatical.append('complemento ::= OWNER ID')
        varSemantico.append('ip41 ')

def p_complementoCR2(t):
    '''complemento      : OWNER IGUAL ID MODE IGUAL ENTERO
                        | OWNER ID MODE IGUAL ENTERO
                        | OWNER IGUAL ID MODE ENTERO
                        | OWNER ID MODE ENTERO
                        '''
    if t[2] == '='      : 
        if t[5] == '='  :
            t[0] = ComplementoCR(t[3], t[6])
            varGramatical.append('complemento ::= OWNER IGUAL ID MODE IGUAL ENTERO')
            varSemantico.append('ip42 ')

        else            :
            t[0] = ComplementoCR(t[3], t[5])
            varGramatical.append('complemento ::= OWNER IGUAL ID MODE ENTERO')
            varSemantico.append('ip43 ')
    else                : 
        if t[4] == '='  :
            t[0] = ComplementoCR(t[2], t[5])
            varGramatical.append('complemento ::= OWNER ID MODE IGUAL ENTERO')
            varSemantico.append('ip44 ')
        else            :
            t[0] = ComplementoCR(t[2], t[4])
            varGramatical.append('complemento ::= OWNER ID MODE ENTERO')
            varSemantico.append('ip45 ')

# SHOW
def p_showDB(t):
    'instruccion        : SHOW DATABASES PTCOMA'
    t[0] = Show(True)
    varGramatical.append('instruccion ::= SHOW DATABASES PTCOMA')
    varSemantico.append('ip46 ')

def p_showDB1(t):
    'instruccion        : SHOW DATABASES LIKE CADENA PTCOMA'
    t[0] = t[1]
    varGramatical.append('instruccion ::= SHOW DATABASES LIKE CADENA PTCOMA')
    varSemantico.append('ip47 ')

# ALTER
def p_alterDB(t):
    '''instruccion      : ALTER DATABASE ID RENAME TO ID PTCOMA

                        | ALTER DATABASE ID OWNER TO ID PTCOMA'''

    if t[4].upper() == 'RENAME'     :
        t[0] = AlterDatabase(1, t[3], t[6].upper())
        varGramatical.append('instruccion ::= ALTER DATABASE ID RENAME TO ID PTCOMA')
        varSemantico.append('ip48 ')
    else                            :
        t[0] = AlterDatabase(2, t[3], t[6].upper())
        varGramatical.append('instruccion ::= ALTER DATABASE ID OWNER TO ID PTCOMA')
        varSemantico.append('ip49 ')



def p_alterT(t):
    '''instruccion      : ALTER TABLE ID lalterprima PTCOMA
                        '''
    t[0] = AlterTable(t[3], t[4])
    varGramatical.append('instruccion ::= ALTER TABLE ID lalterprima PTCOMA')
    varSemantico.append('ip50 ')
                         #t[3]         #t[6] #t[7]
   # t[0] = AlterTable(1, t[3], None, None, None, None, None, None, None, None, None, None)
#caso, id, columnConstraint, idAdd, tipoAdd, checkAdd, constraintId, columnId, listaFK, listaReferences, idDrop, columnAlter)
#def p_alterT2(t):
#    'instruccion        : ALTER TABLE ID  PTCOMA'
#    t[0] = AlterTable(2, t[3], 'COLUMN', None, None, None, None, None, None, None, t[6], None)

#def p_alterT3(t):
#    'instruccion        : ALTER TABLE ID  PTCOMA'
#    t[0] = AlterTable(1, t[3], None, None, None, t[6], None, None, None, None, None, None)

#def p_alterT4(t):
#    'instruccion        : ALTER TABLE ID PTCOMA'
#    t[0] = AlterTable(1, t[3], None, None, None, None, t[6], t[9], None, None, None, None)

#def p_alterT5(t):
#    'instruccion        : ALTER TABLE ID PTCOMA'
#    t[0] = AlterTable(1, t[3], None, None, None, None, None, None, t[8], t[11], None, None)

#def p_alterT6(t):
#    'instruccion        : ALTER TABLE ID  PTCOMA'
#    t[0] = AlterTable(3, t[3], None, None, None, None, None, None, None, None, None, t[6])

#def p_alterT7(t):
#    'instruccion        : ALTER TABLE ID  PTCOMA'
#    t[0] = AlterTable(2, t[3], 'CONSTRAINT', None, None, None, None, None, None, None, t[6], None)

def p_alterT8(t):
    'lalterprima         : lalterprima COMA alterprima'
    t[1].append(t[3])
    t[0] = t[1]
    varGramatical.append('lalterprima ::= lalterprima COMA alterprima')
    varSemantico.append('ip51 ')

def p_alterT9(t):
    'lalterprima         : alterprima'
    t[0] = [t[1]]
    varGramatical.append('lalterprima ::= alterprima')
    varSemantico.append('ip52 ')

def p_alterT10(t):
    'alterprima         : ADD COLUMN ID tipo '
    t[0] = Alter('ADD', 'COLUMN', t[3], t[4], None, None, None)
    varGramatical.append('alterprima ::= ADD COLUMN ID tipo')
    varSemantico.append('ip53 ')

def p_alterT11(t):
    'alterprima         : DROP COLUMN ID'
    t[0] = Alter('DROP', 'COLUMN', t[3], None, None, None, None)
    varGramatical.append('alterprima ::= DROP COLUMN ID')
    varSemantico.append('ip54 ')

def p_alterT12(t):
    'alterprima         : ADD CHECK checkprima'
    t[0] = Alter('ADD', 'CHECK', None, None, t[3], None, None)
    varGramatical.append('alterprima ::= ADD CHECK checkprima')
    varSemantico.append('ip55 ')

def p_alterT13(t):
    'alterprima         : DROP CONSTRAINT ID'
    t[0] = Alter('DROP', 'CONSTRAINT', t[3], None, None, None, None)
    varGramatical.append('alterprima ::= DROP CONSTRAINT ID')
    varSemantico.append('ip56 ')

def p_alterT14(t):
    'alterprima         : ADD CONSTRAINT ID UNIQUE PARIZQ ID PARDR'
    t[0] = Alter('ADD', 'CONSTRAINT', t[3], None, None, t[6], None)
    varGramatical.append('alterprima ::= ADD CONSTRAINT ID UNIQUE PARIZQ ID PARDR')
    varSemantico.append('ip57 ')

def p_alterT15(t):
    'alterprima         : ADD FOREIGN KEY PARIZQ listaID PARDR REFERENCES listaID'
    t[0] = Alter('ADD', 'FOREIGN', t[5], None, None, t[8], None)
    varGramatical.append('alterprima ::= ADD FOREIGN KEY PARIZQ listaID PARDR REFERENCES listaID')
    varSemantico.append('ip58 ')

def p_alterT16(t):
    'alterprima         : ALTER COLUMN ID TYPE tipo'
    t[0] = Alter('ALTER', 'COLUMN', t[3], t[5], None, None, 'TYPE')
    varGramatical.append('alterprima ::= ALTER COLUMN ID TYPE tipo')
    varSemantico.append('ip59 ')

def p_alterT17(t):
    'alterprima         : ALTER COLUMN ID SET NOT NULL'
    t[0] = Alter('ALTER', 'COLUMN', t[3], None, None, None, 'SET')
    varGramatical.append('alterprima ::= ALTER COLUMN ID SET NOT NULL')
    varSemantico.append('ip60 ')
    # alterbiprima'

#def p_alterT17(t):
#    '''alterbiprima     : TYPE tipo
 #                       | SET NOT NULL'''



##################################################################
# SELECT
def p_selectTime(t):
    ''' instruccion     : SELECT Time PTCOMA'''
    varGramatical.append('instruccion ::= SELECT Time PTCOMA')
    varSemantico.append('ip61 ')

def p_selectTime2(t):
    ''' Time            : EXTRACT PARIZQ momento FROM TIMESTAMP  CADENA PARDR
                        | date_part PARIZQ CADENA COMA INTERVAL CADENA PARDR
    '''
    t[0] = t[1]
    if t[1].lower() == 'extract':
        varGramatical.append('Time ::= EXTRACT PARIZQ momento FROM TIMESTAMP  CADENA PARDR')
        varSemantico.append('ip62 ')
    else:
        varGramatical.append('Time ::= date_part PARIZQ CADENA COMA INTERVAL CADENA PARDR')
        varSemantico.append('ip63 ')

def p_selectTime3(t):
    ''' Time            : NOW PARIZQ PARDR
                        | TIMESTAMP CADENA
    '''
    t[0] = t[1]
    if t[1].lower() == 'now':
        varGramatical.append('Time ::= NOW PARIZQ PARDR')
        varSemantico.append('ip64 ')
    else:
        varGramatical.append('Time ::= TIMESTAMP CADENA')
        varSemantico.append('ip65 ')

def p_selectTime4(t):
    ''' Time            : CURRENT_TIME
                        | CURRENT_DATE
    '''
    t[0] = t[1]
    if t[1].lower() == 'current_time':
        varGramatical.append('Time ::= CURRENT_TIME')
        varSemantico.append('ip66 ')
    else:
        varGramatical.append('Time ::= CURRENT_DATE')
        varSemantico.append('ip67 ')

def p_momento(t):
    ''' momento         : YEAR
                        | MONTH
                        | DAY
                        | HOUR
                        | MINUTE
                        | SECOND
    '''
    t[0] = t[1]
    varGramatical.append('momento ::= '+ str(t[1]))
    varSemantico.append('ip68 ')
#ESTE SELECT SIRVE PARA HACER UNA LLAMADA A UNA CONSULTA QUE POSIBLEMENTE USE LA UNION
# INTERSECT U OTRO
def p_instruccionSELECT(t):
    '''instruccion : PARIZQ select2 PARDR inst_union
                    '''
    # t[0]=t[1]
    varGramatical.append('instruccion ::= PARIZQ select2 PARDR inst_union')
    varSemantico.append('ip69 ')
#SELECT SENCILLO QUE LLAMA FUNCIONES
def p_instruccionSELECT2(t):
    '''instruccion : select2 PTCOMA
                     '''
    varGramatical.append('instruccion ::= select2 PTCOMA')
    varSemantico.append('ip70 ')
#SELECT AUXILIAR QUE PROCEDE HACER EL UNION
def p_union2(t):
    '''inst_union : UNION ALL  PARIZQ select2 PARDR PTCOMA
              '''
    varGramatical.append('inst_union ::= UNION ALL  PARIZQ select2 PARDR PTCOMA')
    varSemantico.append('ip71 ')
#SELECT AUXILIAR QUE PROCEDE HACER EL INTERSECT CON OTRO QUERY
def p_union3(t):
    '''inst_union : INTERSECT ALL  PARIZQ select2 PARDR PTCOMA
             '''
    varGramatical.append('inst_union ::= INTERSECT ALL  PARIZQ select2 PARDR PTCOMA')
    varSemantico.append('ip72 ')
#SELECT AUXILIAR QUE PROCEDE HACER EL EXCEP CON OTRO QUERY
def p_union4(t):
    '''inst_union : EXCEPT ALL  PARIZQ select2 PARDR PTCOMA
          '''
    varGramatical.append('inst_union ::= EXCEPT ALL  PARIZQ select2 PARDR PTCOMA')
    varSemantico.append('ip73 ')
#ESTOS HACEN LO MISMO SIN LA PALABRA RESERVADA ALL
def p_union5(t):
    '''inst_union : UNION  PARIZQ select2 PARDR PTCOMA
              '''
    varGramatical.append('inst_union ::= UNION  PARIZQ select2 PARDR PTCOMA')
    varSemantico.append('ip74 ')

def p_union6(t):
    '''inst_union : INTERSECT  PARIZQ select2 PARDR PTCOMA
              '''
    varGramatical.append('inst_union ::= INTERSECT  PARIZQ select2 PARDR PTCOMA')
    varSemantico.append('ip75 ')

def p_union7(t):
    '''inst_union : EXCEPT  PARIZQ select2 PARDR PTCOMA
              '''
    varGramatical.append('inst_union ::= EXCEPT  PARIZQ select2 PARDR PTCOMA')
    varSemantico.append('ip76 ')

def p_groupBy(t):
    '''compSelect           : table_expr
    '''
    # t[0] = t[3]
    varGramatical.append('compSelect ::= table_expr')
    varSemantico.append('ip77 ')

def p_groupBy1(t):
    '''compSelect           : table_expr GROUP BY  compGroup
    '''
    varGramatical.append('compSelect ::= table_expr GROUP BY  compGroup')
    varSemantico.append('ip78 ')

def p_having(t):
    '''compGroup        : list
    '''
    varGramatical.append('compGroup ::= list')
    varSemantico.append('ip79 ')

def p_having1(t):
    '''compGroup        :  list HAVING andOr
    '''
    varGramatical.append('compGroup ::= list HAVING andOr')
    varSemantico.append('ip80 ')
#--------------------------------------------------------------
#aqui imician los select que vienen sin union intersect o excep
#select 's
def p_instselect(t):
    '''select2 : SELECT DISTINCT select_list FROM inner orderby
                    '''
    # t[0] = t[1]+' '+t[2]+' '+t[3]+' '+t[4]+ ' '+t[5]
    varGramatical.append('select2 ::= SELECT DISTINCT select_list FROM inner orderby')
    varSemantico.append('ip81 ')

def p_instselect2(t):
    '''select2 : SELECT select_list FROM subquery inner orderby limit
    '''
    varGramatical.append('select2 ::= SELECT select_list FROM subquery inner orderby limit')
    varSemantico.append('ip82 ')

def p_instselect3(t):
    '''select2 : SELECT select_list
                    '''
    varGramatical.append('select2 ::= SELECT select_list')
    varSemantico.append('ip83 ')

def p_instselect4(t):
    '''select2 : SELECT select_list FROM subquery inner WHERE complemSelect orderby limit
                    '''
    varGramatical.append('select2 ::= SELECT select_list FROM subquery inner WHERE complemSelect orderby limit')
    varSemantico.append('ip84 ')

def p_instselect7(t):
    '''select2 : SELECT DISTINCT select_list FROM subquery inner WHERE complemSelect orderby limit
                    '''
    varGramatical.append('select2 ::= SELECT DISTINCT select_list FROM subquery inner WHERE complemSelect orderby limit')
    varSemantico.append('ip85 ')

#------------------------------------------------------------------------
def p_order_by(t):
    '''orderby : ORDER BY listaID
                |'''
    varGramatical.append('orderby ::= ORDER BY listaID')
    varSemantico.append('ip86 ')


def p_order_limit(t):
    '''limit : LIMIT ENTERO
               | LIMIT ALL
               | LIMIT ENTERO OFFSET ENTERO
               '''
    if t[2].lower()=='all':
        varGramatical.append('limit ::= LIMIT ALL')
        varSemantico.append('lk12 ')
    elif t[3].lower()=='offset':
        varGramatical.append('limit ::= LIMIT ENTERO OFFSET ENTERO')
        varSemantico.append('lk12 ')
    else:
        varGramatical.append('limit ::= LIMIT ENTERO')
        varSemantico.append('lk12 ')

def p_subquery(t):
    '''subquery : PARIZQ select2 PARDR
                | '''
    varGramatical.append('subquery ::= PARIZQ select2 PARDR')
    varSemantico.append('ip88 ')

def p_innerjoin(t):
    '''inner    :  table_expr '''
    varGramatical.append('inner ::= table_expr')
    varSemantico.append('ip89 ')

def p_innerjoin1(t):
    '''inner    :  compSelect '''
    varGramatical.append('inner ::= compSelect')
    varSemantico.append('ip90 ')
# hasta aqui no viene inner

def p_innerjoin2(t):
    '''inner    :  table_expr INNER JOIN columna ON asignacion '''
    varGramatical.append('inner ::= table_expr INNER JOIN columna ON asignacion')
    varSemantico.append('ip91 ')

def p_innerjoin3(t):
    '''inner    :  table_expr INNER JOIN columna ON asignacion complemSelect '''
# aqui si viene inner join pero sin where
    varGramatical.append('inner ::= table_expr INNER JOIN columna ON asignacion complemSelect')
    varSemantico.append('ip92 ')



def p_instselect5(t):
    '''complemSelect : andOr
    '''
    varGramatical.append('complemSelect ::= andOr')
    varSemantico.append('ip93 ')



def p_instselect6(t):
    '''complemSelect : andOr GROUP BY  compGroup
                    '''
    varGramatical.append('complemSelect ::= andOr GROUP BY  compGroup')
    varSemantico.append('ip94 ')


def p_selectList(t):
    '''select_list : MULT
                    | list'''
    if t[1]=='*':
        varGramatical.append('select_list ::= MULT')
        varSemantico.append('ip95 ')
    else:
        varGramatical.append('select_list ::= list')
        varSemantico.append('ip96 ')

def p_list2(t):
    '''list : list COMA columna '''
    varGramatical.append('list ::= list COMA columna')
    varSemantico.append('ip97 ')

def p_list3(t):
    '''list : columna '''
    varGramatical.append('list ::= columna')
    varSemantico.append('ip98 ')

def p_cases(t):
    '''columna : CASE cases END ID
    '''
    varGramatical.append('columna ::= CASE cases END ID')
    varSemantico.append('ip99 ')


def p_cases1(t):
    '''cases : cases case
    '''
    varGramatical.append('cases ::= cases case')
    varSemantico.append('ip100 ')

def p_cases2(t):
    '''cases : case
    '''
    varGramatical.append('cases ::= case')
    varSemantico.append('ip101 ')

def p_cases3(t):
    '''case : WHEN asignacion THEN valores '''
    varGramatical.append('cases ::= WHEN asignacion THEN valores')
    varSemantico.append('ip102 ')




def p_columna0(t):
    '''columna : PARIZQ select2 PARDR
                '''
    varGramatical.append('columna ::= PARIZQ select2 PARDR')
    varSemantico.append('ip103 ')


#aqui no se puede hacer el llamdo a subquery pero no obstante pueden venir consultas entre columnas
def p_columna1_0(t):
    '''columna : Time
                '''
    varGramatical.append('columna ::= Time')
    varSemantico.append('ip104 ')

def p_columna1_1(t):
    '''columna : Time AS ID
                '''
    varGramatical.append('columna ::= Time AS ID')
    varSemantico.append('ip105 ')


def p_columna1_2(t):
    '''columna : Time ID
                '''
    varGramatical.append('columna ::= Time ID')
    varSemantico.append('ip106 ')


def p_columna1_3(t):
    '''columna : Time AS CADENA
                '''
    varGramatical.append('columna ::= Time AS CADENA')
    varSemantico.append('ip107 ')

def p_columna1_4(t):
    '''columna : Time CADENA
                '''
    varGramatical.append('columna ::= Time CADENA')
    varSemantico.append('ip108 ')

def p_columna2(t):
    '''columna : ID opcionID
                '''
    varGramatical.append('columna ::= ID opcionID')
    varSemantico.append('ip109 ')

def p_columna3(t):
    '''columna : ID AS ID
                '''
    varGramatical.append('columna ::= ID AS ID')
    varSemantico.append('ip110 ')

def p_columna4(t):
    '''columna : ID
                '''
    varGramatical.append('columna ::= ID')
    varSemantico.append('ip111 ')


def p_columna4_1(t):
    '''columna : ID ID
                '''
    varGramatical.append('columna ::= ID ID')
    varSemantico.append('ip112 ')


def p_columna4_2(t):
    '''columna : ID CADENA
                '''
    varGramatical.append('columna ::= ID CADENA')
    varSemantico.append('ip113 ')


def p_columna5(t):
    '''columna : ID AS CADENA
                '''
    varGramatical.append('columna ::= ID AS CADENA')
    varSemantico.append('ip114 ')

def p_columna6(t):
    '''columna : math AS ID
                '''
    varGramatical.append('columna ::= math AS ID')
    varSemantico.append('ip115 ')

def p_columna7(t):
    '''columna : math AS CADENA
                '''
    varGramatical.append('columna ::= math AS CADENA')
    varSemantico.append('ip116 ')


def p_columna7_1(t):
    '''columna : math CADENA
                '''
    varGramatical.append('columna ::= math CADENA')
    varSemantico.append('ip117 ')


def p_columna7_2(t):
    '''columna : math ID
                '''
    varGramatical.append('columna ::= math ID')
    varSemantico.append('ip118 ')

def p_columna8(t):
    '''columna : math
                '''
    varGramatical.append('columna ::= math')
    varSemantico.append('ip119 ')

def p_columna9(t):
    '''columna : trig AS CADENA
                '''
    varGramatical.append('columna ::= trig AS CADENA')
    varSemantico.append('ip120 ')

def p_columna10(t):
    '''columna : trig
                '''
    varGramatical.append('columna ::= trig')
    varSemantico.append('ip121 ')

def p_columna11(t):
    '''columna : trig AS ID
                '''
    varGramatical.append('columna ::= trig AS ID')
    varSemantico.append('ip122 ')


def p_columna13(t):
    '''columna : bina AS CADENA
                '''
    varGramatical.append('columna ::= bina AS CADENA')
    varSemantico.append('ip123 ')

def p_columna14(t):
    '''columna : bina
                '''
    varGramatical.append('columna ::= bina')
    varSemantico.append('ip124 ')

def p_columna15(t):
    '''columna : bina AS ID
                '''
    varGramatical.append('columna ::= bina AS ID')
    varSemantico.append('ip125 ')

def p_opcionID2(t):
    '''opcionID : PUNTO ascolumnaux
                | ID'''
    varGramatical.append('opcionID ::= PUNTO ascolumnaux')
    varSemantico.append('ip126 ')

def p_opcionID3(t):
    '''ascolumnaux : ID AS ID
                    '''
    varGramatical.append('ascolumnaux ::= ID AS ID')
    varSemantico.append('ip127 ')

def p_opcionID4(t):
    '''ascolumnaux : ID CADENA
                    '''
    varGramatical.append('ascolumnaux ::= ID CADENA')
    varSemantico.append('ip128 ')


def p_opcionID4_1(t):
    '''ascolumnaux : ID ID
                    '''
    varGramatical.append('ascolumnaux ::= ID ID')
    varSemantico.append('ip129 ')

def p_opcionID4_2(t):
    '''ascolumnaux : ID
                    '''
    varGramatical.append('ascolumnaux ::= ID')
    varSemantico.append('ip130 ')


def p_opcionID5(t):
    '''ascolumnaux : ID AS CADENA
                '''
    varGramatical.append('ascolumnaux ::= ID AS CADENA')
    varSemantico.append('ip131 ')

def p_math2(t):
    ''' math  : ABS PARIZQ E PARDR
                | CBRT PARIZQ E PARDR
                | CEIL PARIZQ E PARDR
                | CEILING PARIZQ E PARDR
                | DEGREES PARIZQ E PARDR
                | EXP PARIZQ E PARDR
                | FACTORIAL PARIZQ E PARDR
                | FLOOR PARIZQ E PARDR
                | LCM PARIZQ E PARDR
                | LN PARIZQ E PARDR
                | LOG PARIZQ E PARDR
                | LOG10 PARIZQ E PARDR
                | RADIANS PARIZQ E PARDR
                | ROUND PARIZQ E PARDR
                | SIGN PARIZQ E PARDR
                | SQRT PARIZQ E PARDR
                | TRUC PARIZQ E PARDR
                | WIDTH_BUCKET PARIZQ E PARDR
                | SETSEED PARIZQ E PARDR
                | SUM PARIZQ E PARDR
                | MD5 PARIZQ E PARDR
                | SING PARIZQ E PARDR
                | WIDTH_BUCKET PARIZQ listaValores PARDR
                | AVG PARIZQ E PARDR
                | COUNT PARIZQ E PARDR
                | COUNT PARIZQ MULT PARDR
                | MIN PARIZQ E PARDR
                | MAX PARIZQ E PARDR
                | TRUNC PARIZQ E PARDR
                '''
    varGramatical.append('math ::= ' + str(t[1]) + ' ' + str(t[2]) + ' E ' + str(t[4]))
    varSemantico.append('vw ')

def p_math3(t):
    ''' math  :  DIV PARIZQ E COMA E PARDR
                | GCD PARIZQ E COMA E PARDR
                | MOD PARIZQ E COMA E PARDR
                | POWER PARIZQ E COMA E PARDR
                '''
    varGramatical.append('math ::= ' + str(t[1]) + ' ' + str(t[2]) + ' E ' + str(t[4]) + ' E ' + str(t[6]))
    varSemantico.append('ve ')

def p_math4(t):
    ''' math  :  PI PARIZQ PARDR
                | RANDOM PARIZQ PARDR
                '''
    varGramatical.append('math ::= ' + str(t[1]) + ' ' + str(t[2]) + ' ' + str(t[3]))
    varSemantico.append('vt ')

def p_math6(t):
    ''' math  : MIN_SCALE
                | SCALE
                | TRIM_SCALE
                '''
    varGramatical.append('math ::= ' + str(t[1]))
    varSemantico.append('vy ')


def p_binarios(t):
    '''bina : LENGTH PARIZQ E PARDR
            | SHA256 PARIZQ E PARDR
            | ENCODE PARIZQ E PARDR
            | DECODE PARIZQ E PARDR
            '''
    varGramatical.append('bina ::= ' + str(t[1]) + ' ' + str(t[2]) + ' E ' + str(t[4]))
    varSemantico.append('ve ')


def p_binarios2(t):
    '''bina : SUBSTRING PARIZQ var COMA ENTERO COMA ENTERO PARDR
            | SUBSTR PARIZQ var COMA ENTERO COMA ENTERO PARDR'''
    if t[1].lower()=='substring':
        varGramatical.append('bina ::= SUBSTRING PARIZQ var COMA ENTERO COMA ENTERO PARDR')
        varSemantico.append('ve1 ')
    else:
        varGramatical.append('bina ::= SUBSTR PARIZQ var COMA ENTERO COMA ENTERO PARDR')
        varSemantico.append('ve2 ')

def p_binarios3(t):
    '''bina : TRIM PARIZQ CADENA FROM columna PARDR'''
    varGramatical.append('bina ::= TRIM PARIZQ CADENA FROM columna PARDR')
    varSemantico.append('ve3 ')


def p_binarios4(t):
    '''bina : GET_BYTE PARIZQ CADENA COMA ENTERO PARDR'''
    varGramatical.append('bina ::= GET_BYTE PARIZQ CADENA COMA ENTERO PARDR')
    varSemantico.append('ve4 ')

def p_binarios5(t):
    '''bina : SET_BYTE PARIZQ CADENA COMA ENTERO COMA ENTERO PARDR'''
    varGramatical.append('bina ::= SET_BYTE PARIZQ CADENA COMA ENTERO COMA ENTERO PARDR')
    varSemantico.append('ve5 ')


def p_binarios6(t):
    '''bina : CONVERT PARIZQ CADENA AS tipo PARDR'''
    varGramatical.append('bina ::= CONVERT PARIZQ CADENA AS tipo PARDR')
    varSemantico.append('ve6 ')

def p_funcionesAgregadas(t):
    '''bina : GREATEST PARIZQ listaValores PARDR'''
    varGramatical.append('bina ::= GREATEST PARIZQ listaValores PARDR')
    varSemantico.append('ve7 ')

def p_funcionesAgregadas1(t):
    '''
    bina : LEAST PARIZQ listaValores PARDR'''
    varGramatical.append('bina ::= LEAST PARIZQ listaValores PARDR')
    varSemantico.append('ve8 ')

def p_trig2(t):
    ''' trig : ACOS PARIZQ E PARDR
              | ACOSD PARIZQ E PARDR
              | ASIN PARIZQ E PARDR
              | ASIND PARIZQ E PARDR
              | ATAN PARIZQ E PARDR
              | ATAND PARIZQ E PARDR
              | ATAN2 PARIZQ E PARDR
              | ATAN2D PARIZQ E PARDR
              | COS PARIZQ E PARDR
              | COSD PARIZQ E PARDR
              | COT PARIZQ E PARDR
              | COTD PARIZQ E PARDR
              | SIN PARIZQ E PARDR
              | SIND PARIZQ E PARDR
              | TAN PARIZQ E PARDR
              | TAND PARIZQ E PARDR
              | SINH PARIZQ E PARDR
              | COSH PARIZQ E PARDR
              | TANH PARIZQ E PARDR
              | ASINH PARIZQ E PARDR
              | ACOSH PARIZQ E PARDR
              | ATANH PARIZQ E PARDR '''
    varGramatical.append('trig ::= ' + str(t[1]) + ' ' + str(t[2]) + ' E ' + str(t[4]))
    varSemantico.append('vw1 ')

def p_tableexpr2(t):
    '''table_expr : table_expr COMA tablaR
                    '''
    varGramatical.append('table_expr ::= table_expr COMA tablaR')
    varSemantico.append('vw1 ')

def p_tableexpr3(t):
    '''table_expr : tablaR
                    '''
    varGramatical.append('table_expr ::= tablaR')
    varSemantico.append('vw3 ')

def p_tablaR2(t):
    '''tablaR : ID ID
                '''
    varGramatical.append('tablaR ::= ID ID')
    varSemantico.append('vw4 ')

def p_tablaR3(t):
    '''tablaR : ID AS ID
                '''
    varGramatical.append('tablaR ::= ID AS ID')
    varSemantico.append('vw5 ')

def p_tablaR4(t):
    '''tablaR : ID
                '''
    varGramatical.append('tablaR ::= ID')
    varSemantico.append('vw6 ')


def p_instruccion_createEnum(t):
    ''' instruccion : CREATE TYPE ID AS ENUM PARIZQ campos PARDR PTCOMA
    '''
    varGramatical.append('instruccion ::= CREATE TYPE ID AS ENUM PARIZQ campos PARDR PTCOMA')
    varSemantico.append('vw7 ')

def p_checkopcional(t):
    ''' checkprima : listaValores
                    | E               '''
    t[0] = t[1]
    varGramatical.append('checkprima ::= listaValores')
    varSemantico.append('vw7 ')

# def p_condicion2(t):
#   '''condi
#   cion : andOr HAVING
#              | andOr'''
####################################################################
# MODO PANICO ***************************************
def p_error(t):
    global L_errores_sintacticos
    print("Error sintáctico en '%s'" % t.value)

    colum = contador_columas(columna)
    print("Columna ",colum)
    print("columna lexer pos ",lexer.lexpos)
    data = Error(str("Error Sintactico"), str(t.value), str(t.lexer.lineno), str(colum))
    L_errores_sintacticos.append(data)

    if not t:
        print("Fin del Archivo!")
        return



    # Read ahead looking for a closing '}'
    while True:
        tok = parser.token()  # Get the next token
        if not tok or tok.type == 'PTCOMA':
            print("Se recupero con ;")
            break
    parser.restart()


def contador_columas(args):
    columna = args + 2
    return columna


def reporteGram(gram,sem):
    varGramatical.append('PRODUCCIONES')

    varSemantico.append('SEMANTICO')

    s = Digraph('gramatica', filename='reporteGramatica.gv', node_attr={'shape': 'plaintext'})
    u = len(gram)
    g = 'g [label =  <<TABLE>'
    for x in range(0, u):
        g += '<TR>'+'\n'+'<TD border="3"  bgcolor="/rdylgn11/6:/rdylgn11/9" gradientangle="270">'+str(gram.pop())+'</TD>'+'\n'+'<TD border="3"  bgcolor="/rdylgn11/6:/rdylgn11/9" gradientangle="270">'+str(sem.pop())+'</TD>'+'\n'+'</TR>'

    g += '</TABLE>>, ];'
    s.body.append(g)
    #s.view


import ply.yacc as yacc

import Compi2RepoAux.team21.Analisis_Ascendente.reportes.AST.AST as AST
import Compi2RepoAux.team21.Analisis_Ascendente.Tabla_simbolos.TablaSimbolos as TS

parser = yacc.yacc()
#analisis semantico
def procesar_instrucciones(instrucciones, ts) :
    ## lista de instrucciones recolectadas
    global consola
    for instr in instrucciones :
        if isinstance(instr, CreateReplace) :
            CreateReplace.ejecutar(instr, ts,consola)
            print("ejecute create")

    #    elif isinstance(instr, Definicion) : procesar_definicion(instr, ts)
    #    elif isinstance(instr, Asignacion) : procesar_asignacion(instr, ts)
    #    elif isinstance(instr, Mientras) : procesar_mientras(instr, ts)
    #    elif isinstance(instr, If) : procesar_if(instr, ts)
    #    elif isinstance(instr, IfElse) : procesar_if_else(instr, ts)
        else : print('Error: instrucción no válida')

def ejecutarAnalisis(entrada):
    global L_errores_lexicos
    global L_errores_sintacticos
    global consola
    global exceptions
    consola = []
    L_errores_lexicos = []
    L_errores_sintacticos = []
    # f = open("./entrada.txt", "r")
    #input = f.read()
    #print(input)

    #realiza analisis lexico y semantico
    instrucciones = parser.parse(entrada)
    reporte = AST.AST(instrucciones)
    reporte.ReportarAST()
    #inicia analisis semantico
    ts_global = TS.TablaDeSimbolos()
    procesar_instrucciones(instrucciones, ts_global)
    #limpiar
    lexer.input("")
    lexer.lineno=0
    print("Lista Lexico\n", L_errores_lexicos)
    print("Lista Sintactico\n", L_errores_sintacticos)
    #Reporte de analisis lexico y sintactico
    reportes = RealizarReportes()
    reportes.generar_reporte_lexicos(L_errores_lexicos)
    reportes.generar_reporte_sintactico(L_errores_sintacticos)
    print("Fin de analisis")
    print("Realizando reporte gramatical")
    reporteGram(varGramatical, varSemantico)
    return consola











