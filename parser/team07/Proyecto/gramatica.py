from ply import *

reservadas = {
    'smallint' : 'SMALLINT',
    'integer' : 'INTEGER',
    'biginit' : 'BIGINIT',
    'decimal' : 'DECIMAL',
    'numeric' : 'NUMERIC',
    'real' : 'REAL',
    'double' : 'DOUBLE',
    'precision' : 'PRECISION',
    'money' : 'MONEY',
    'varchar' : 'VARCHAR',
    'character' : 'CHARACTER',
    'text' : 'TEXT',
    'timestamp' : 'TIMESTAMP',
    'without' : 'WITHOUT',
    'time' : 'TIME',
    'zone' : 'ZONE',
    'with' : 'WITH',
    'date' : 'DATE',    
    'interval' : 'INTERVAL',
    'year' : 'YEAR',
    'month' : 'MONTH',
    'day' : 'DAY',
    'hour' : 'HOUR', 
    'minute' : 'MINUTE',
    'second' : 'SECOND',
    'to' : 'TO', 
    'boolean' : 'BOOLEAN',
    'create' : 'CREATE',
    'type' : 'TYPE',
    'as' : 'AS',
    'enum' : 'ENUM',
    'between' : 'BETWEEN',
    'in' : 'IN',
    'like' : 'LIKE',
    'ilike' : 'ILIKE',
    'similar' : 'SIMILAR',
    'isnull' : 'ISNULL',
    'notnull' : 'NOTNULL',
    'not' : 'NOT',
    'null' : 'NULL',
    'and' : 'AND',
    'or' : 'OR',
    'replace' : 'REPLACE',
    'database' : 'DATABASE',
    'if' : 'IF',
    'exists' : 'EXISTS',
    'owner' : 'OWNER',
    'mode' : 'MODE',
    'show' : 'SHOW',
    'databases' : 'DATABASES',
    'alter' : 'ALTER',
    'rename' : 'RENAME',
    'drop' : 'DROP',
    'table' : 'TABLE',
    'constraint' : 'CONSTRAINT',
    'unique' : 'UNIQUE',
    'check' : 'CHECK',
    'primary' : 'PRIMARY',
    'key' : 'KEY',
    'references' : 'REFERENCES',
    'foreign' : 'FOREIGN',
    'add' : 'ADD',
    'set' : 'SET',
    'delete' : 'DELETE',
    'from' : 'FROM',
    'where' : 'WHERE',
    'inherits' : 'INHERITS',
    'insert' : 'INSERT',
    'into' : 'INTO',
    'update' : 'UPDATE',
    'values' : 'VALUES',
    'select' : 'SELECT',
    'distinct' : 'DISTINCT',
    'group' : 'GROUP',
    'by' : 'BY',
    'having' : 'HAVING',
    'sum' : 'SUM',
    'count' : 'COUNT',
    'avg' : 'AVG',
    'max' : 'MAX',
    'min' : 'MIN',
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
    'width_bucket' : 'WIDTH_BUCKET',
    'random' : 'RANDOM',
    'setseed' : 'SETSEED',
    'acos' : 'ACOS',
    'acosd' : 'ACOSD',
    'asin' : 'ASIN',
    'asind' : 'ASIND',
    'atan' : 'ATAN',
    'atand' : 'ATAND',
    'atan2' : 'ATAN2',
    'atan2d' : 'ATAN2D',
    'cos' : 'COS',
    'cosd' : 'COSD',
    'cot' : 'COT',
    'cotd' : 'COTD',
    'sin' : 'SIN',
    'sind' : 'SIND',
    'tan' : 'TAN',
    'tand' : 'TAND',
    'sinh' : 'SINH',
    'cosh' : 'COSH',
    'tanh' : 'TANH',
    'asinh' : 'ASINH',
    'acosh' : 'ACOSH',
    'atanh' : 'ATANH',
    'length' : 'LENGTH',
    'substring' : 'SUBSTRING',
    'trim' : 'TRIM',
    'get_byte' : 'GET_BYTE',
    'md5' : 'MD5',
    'set_byte' : 'SET_BYTE',
    'sha256' : 'SHA256',
    'substr' : 'SUBSTR',
    'convert' : 'CONVERT',
    'encode' : 'ENCODE',
    'decode' : 'DECODE',
    'extract' : 'EXTRACT',
    'century' : 'CENTURY',
    'decade' : 'DECADE',
    'dow' : 'DOW',
    'doy' : 'DOY',
    'epoch' : 'EPOCH',
    'isodown' : 'ISODOWN',
    'isoyear' : 'ISOYEAR',
    'microseconds' : 'MICROSECONDS',
    'millennium' : 'MILENNIUM',
    'milliseconds' : 'MILLISECONDS',
    'quarter' : 'QUARTER',
    'timezone' : 'TIMEZONE',
    'timezone_hour' : 'TIMEZONE_HOUR',
    'timezone_minute' : 'TIMEZONE_MINUTE',
    'week' : 'WEEK',
    'at' : 'AT',        
    'current_date' : 'CURRENT_DATE',
    'current_time' : 'CURRENT_TIME',
    'current_timestamp' : 'CURRENT_TIMESTAMP',    
    'localtime' : 'LOCALTIME',
    'localtimestamp' : 'LOCALTIMESTAMP',
    'pg_sleep' : 'PG_SLEEP',
    'pg_sleep_for' : 'PG_SLEEP_FOR',
    'pg_sleep_until' : 'PG_SLEEP_UNTIL',
    'inner' : 'INNER',
    'left' : 'LEFT',
    'right' : 'RIGHT',
    'full' : 'FULL',
    'outer' : 'OUTER',
    'join' : 'JOIN',
    'all' : 'ALL',
    'any' : 'ANY',
    'some' : 'SOME',
    'order' : 'ORDER',    
    'asc' : 'ASC',
    'desc' : 'DESC',
    'case' : 'CASE',
    'when' : 'WHEN',
    'then' : 'THEN',
    'else' : 'ELSE',
    'end' : 'END',
    'greatest' : 'GREATEST',
    'least' : 'LEAST',
    'limit' : 'LIMIT',
    'union' : 'UNION',
    'intersect' : 'INTERSECT',
    'except' : 'EXCEPT',
    'is'    :   'IS',
    'default'   :   'DEFAULT',
    'true'      :   'TRUE',
    'false'     :   'FALSE',
    'column' : 'COLUMN',
    'current_user' : 'CURRENT_USER',
    'session_user' : 'SESSION_USER',
    'date_part' :   'DATE_PART',
    'now'       :   'NOW',
    'trunc' :   'TRUNC',
    'offset'    :   'OFFSET',
    'nulls' :   'NULLS',
    'first' :   'FIRST',
    'last'  :   'LAST',
    'char'  :   'CHAR'
}

tokens  = [
    'PTCOMA',
    'COMA',
    'PUNTO',
    'TYPECAST',
    'MAS',
    'MENOS',
    'POTENCIA',
    'MULTIPLICACION',
    'DIVISION',
    'MODULO',
    'MENOR_QUE',
    'MENOR_IGUAL',
    'MAYOR_QUE',
    'MAYOR_IGUAL',
    'IGUAL',
    'DISTINTO',
    'LLAVEIZQ',
    'LLAVEDER',
    'PARIZQUIERDO',
    'PARDERECHO',
    'DECIMAL_',
    'ENTERO',
    'CADENA',
    'ID',
    'ESPACIO'
] + list(reservadas.values())

# Tokens

t_PTCOMA  = r';'
t_LLAVEIZQ = r'{'
t_LLAVEDER = r'}'
t_PARIZQUIERDO = r'\('
t_PARDERECHO = r'\)'
t_COMA = r','
t_PUNTO = r'\.'
t_TYPECAST = r'::'
t_MAS = r'\+'
t_MENOS = r'-'
t_POTENCIA = r'\^'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_MODULO = r'%'
t_IGUAL = r'\='
t_MENOR_QUE = r'\<'
t_MAYOR_QUE = r'\>'
t_MENOR_IGUAL = r'\<='
t_MAYOR_IGUAL = r'\>='
t_DISTINTO = r'<>'


def t_DECIMAL_(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t



def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')    # Check for reserved words
     return t

def t_CADENA(t):
    r'\'.*?\''
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

# Comentario de múltiples líneas /* .. */
def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'--.*\n'
    t.lexer.lineno += 1



def t_ESPACIO(t):
    r' |\t'
    global columna
    if t.value == '\t':

        columna = IncColuma(columna+8)
    else:

        columna = IncColuma(columna)


# Caracteres ignorados
t_ignore = "\r"

global columna
columna = 0
global numNodo
numNodo = 0


def incNodo(valor):
    numNodo = valor +1
    return numNodo

def IncColuma(valor):
    columna = valor + 1
    return columna

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    global columna
    columna = 0


    
def t_error(t):
    print("token: '%s'" %t)
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def find_column(input, token):
     line_start = input.rfind('\n', 0, token.lexpos) + 1
     return (token.lexpos - line_start) + 1

def crear_nodo_general(nombre, valor,fila,column):
    nNodo = incNodo(numNodo)
    nodoEnviar = nodoGeneral.NodoGeneral()
    nodoEnviar.setearValores(fila,columna,nombre,nNodo,valor)
    return nodoEnviar

# Construyendo el analizador léxico
import re
import ply.lex as lex
lexer = lex.lex(reflags=re.IGNORECASE)

# Asociación de operadores y precedencia
# faltan los unarios de positivo, negativo 
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('nonassoc', 'IS', 'ISNULL', 'NOTNULL'),
    ('nonassoc', 'MENOR_QUE', 'MENOR_IGUAL', 'MAYOR_QUE', 'MAYOR_IGUAL', 'IGUAL', 'DISTINTO'),
    ('nonassoc', 'BETWEEN','IN','LIKE','ILIKE','SIMILAR','TO'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'MULTIPLICACION', 'DIVISION', 'MODULO'),
    ('left', 'POTENCIA'),
    ('left','TYPECAST'),    
    ('left','PUNTO')
    
)


# Definición de la gramática
from clasesAbstractas import createType
from clasesAbstractas import insertTable
from clasesAbstractas import nodoGeneral
from tablaSimbolos import tipoSimbolo
from clasesAbstractas import deleteTable
from clasesAbstractas import updateColumna
from clasesAbstractas import updateTable
from clasesAbstractas import expresion
from clasesAbstractas import betweenIN
from clasesAbstractas import createTable
from clasesAbstractas import createDatabase
from clasesAbstractas import alterDatabase 
from clasesAbstractas import alterTable
from clasesAbstractas import dropDatabase
from clasesAbstractas import dropTable


def p_init(t):
    'init   :   instrucciones'
    t[0] = t [1]

def p_lista_instrucciones(t):
    'instrucciones  :   instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]

def p_instrucciones_instruccion(t):
    'instrucciones  :   instruccion'
    t[0] = [t[1]]

def p_instruccion(t):
    '''instruccion  :   insert_table
                    |   delete_table
                    |   update_table'''
    t[0] = t[1]
    
def p_instruccion_crear(t):
    'instruccion      : crear_instr'
    t[0] = t[1]

def p_instruccion_alter(t):
    'instruccion : alter_instr'
    t[0] = t[1]

def p_instruccion_drop(t):
    'instruccion : drop_instr'
    t[0] = t[1]
    
def p_instruccion_select(t):
    'instruccion  :   inst_select PTCOMA'



#--------------------------------------------Instrucciones crear------------------------------------------------------------
def p_instruccion_crear_table(t):
    'crear_instr : CREATE TABLE ID PARIZQUIERDO columnas PARDERECHO herencia PTCOMA'
    linea = str(t.lexer.lineno)
    hijos = []
    nNodo = incNodo(numNodo)
    nodoId = crear_nodo_general("ID",t[3],linea,columna)
    nodoColumnas = t[5]
    nodoHerencia = t[7]
    instru = createTable.createTable(t[3],t[7],t[5].hijos)  
    hijos.append(nodoId)
    hijos.append(nodoColumnas)
    hijos.append(nodoHerencia)
    instru.setearValores(linea,columna,"CREATE_TABLE",nNodo,"",hijos)
    t[0] = instru

def p_crear_database(t):
    'crear_instr : CREATE opReplace DATABASE opExists ID opDatabase PTCOMA'
    linea = str(t.lexer.lineno)
    hijos = []
    nNodo = incNodo(numNodo)
    nodoId = crear_nodo_general("ID",t[5],linea,columna)
    nodoOpciones = t[6]
    instru = createDatabase.createDatabase(t[5],t[6].hijos)
    hijos.append(nodoId)
    hijos.append(nodoOpciones)
    instru.setearValores(linea,columna,"CREATE_DATABASE",nNodo,"",hijos)
    t[0] = instru

def p_instr_crear_enum(t):
    'crear_instr     :   CREATE TYPE ID AS ENUM PARIZQUIERDO ID PARDERECHO PTCOMA'
    
    instru = createType.createType(t[3],[t[7]])    
    nNodo = incNodo(numNodo)
    hijos = []
    hijos.append(t[3])
    hijos.append(t[7])
    instru.setearValores(str(t.lexer.lineno),columna,"Crear_Enum",nNodo,"",hijos)
    t[0] = instru
    print("Linea: ", instru.fila)
    print("Columna: ", instru.columna)    
    print("numNodo: ", nNodo)
    print("Valor 1: '%s'" %t)
    
def p_instr_insert(t):
    '''insert_table   :   INSERT INTO ID VALUES lista_valores PTCOMA
                      |   INSERT INTO ID PARIZQUIERDO  lista_columnas  PARDERECHO VALUES lista_valores PTCOMA
                      |   INSERT INTO ID DEFAULT VALUES PTCOMA
                      |   INSERT INTO ID PARIZQUIERDO lista_columnas PARDERECHO DEFAULT VALUES PTCOMA'''
    
    #Se crea el nodo del Id    
    linea = str(t.lexer.lineno)
    nodoId = crear_nodo_general("ID",t[3],str(linea),columna)
    

    nNodo = incNodo(numNodo)
    identificador = t[4]    
    hijos = []
    if identificador.lower() == 'values':    #Primera produccion
        instru = insertTable.InsertTable(t[3],[],t[5].hijos)
        hijos.append(nodoId)
        hijos.append(t[5])
        instru.setearValores(str(linea),columna,"Insert_table",nNodo,"",hijos)
        t[0] = instru
    elif identificador.lower() == 'default':   #Terdera producción
        instru = insertTable.InsertTable(t[3],[],[],True)
        nDefault = crear_nodo_general("default","default values",str(linea),columna)
        hijos.append(nodoId)
        hijos.append(nDefault)
        instru.setearValores(str(linea),columna,"Insert_Table",nNodo,"",hijos)
        t[0] = instru
    elif identificador == '(':
        if t[7].lower() == "values":  # Segunda Producción
            instru = insertTable.InsertTable(t[3],t[5].hijos,t[8].hijos)
            hijos.append(nodoId)
            hijos.append(t[5])
            hijos.append(t[8])
            instru.setearValores(str(linea),columna,"Insert_table",nNodo,"",hijos)
            t[0] = instru
        else:       #Cuarta producción
            instru = insertTable.InsertTable(t[3],t[5].hijos,[],True)
            nDefault = crear_nodo_general("default","default values",str(linea),columna)
            hijos.append(nodoId)
            hijos.append(t[5])
            hijos.append(nDefault)
            instru.setearValores(linea,columna,"Insert_table",nNodo,"",hijos)
            t[0] = instru

def p_lista_columnas(t):
    '''lista_columnas     :   lista_columnas COMA ID
                          |   ID'''

    if len(t) == 2:
        linea = str(t.lexer.lineno)
        nodoId = crear_nodo_general("ID",t[1],str(linea),columna)
        nodoLista = crear_nodo_general("lista_columnas","",linea,columna)
        nodoLista.hijos.append(nodoId)
        t[0] = nodoLista    
    else:
        linea = str(t.lexer.lineno)
        nodoPadre = t[1]
        nodoId = crear_nodo_general("ID",t[3],str(linea),columna)
        nodoPadre.hijos.append(nodoId)
        t[0] = nodoPadre
    

def p_lista_valores(t):
    '''lista_valores  :   lista_valores COMA tupla
                      |   tupla'''
    if len(t) == 2:
        nodoLista = crear_nodo_general("Lista_valores","",str(t.lexer.lineno),columna)
        nodoLista.hijos.append(t[1])
        t[0] = nodoLista
    else:
        nodoLista = t[1]
        nodoLista.hijos.append(t[3])
        t[0] = nodoLista    


def p_tupla(t):
    'tupla  :   PARIZQUIERDO lista_expresiones PARDERECHO'
    nodoTupla = crear_nodo_general("Tupla","",str(t.lexer.lineno),columna)
    nodoTupla.hijos.append(t[2])
    t[0] = nodoTupla


def p_lista_expresiones(t):
    'lista_expresiones  :   lista_expresiones COMA expresion'
    nodoLista = t[1]
    nodoLista.hijos.append(t[3])
    t[0] = nodoLista

def p_lista_expresiones_expresion(t):
    'lista_expresiones  :   expresion'
    nodoLista = crear_nodo_general("lista_expresiones","",str(t.lexer.lineno),columna)
    nodoLista.hijos.append(t[1])
    t[0] = nodoLista
    


def p_expresion_cadena(t):
    'expresion  :   CADENA'
    nNodo = incNodo(numNodo)
    nodoExp = expresion.Expresion()
    nodoExp.valorPrimitivo(t[1],tipoSimbolo.TipoSimbolo.CADENA)
    nodoExp.setearValores(str(t.lexer.lineno),columna,"CADENA",nNodo,t[1])
    t[0] = nodoExp


def p_expresion_entero(t):
    'expresion  :   ENTERO'
    nNodo = incNodo(numNodo)
    nodoExp = expresion.Expresion()
    nodoExp.valorPrimitivo(t[1],tipoSimbolo.TipoSimbolo.ENTERO)
    nodoExp.setearValores(str(t.lexer.lineno),columna,"ENTERO",nNodo,t[1])
    t[0] = nodoExp


def p_expresion_decimal(t):
    'expresion  :   DECIMAL_'

    nNodo = incNodo(numNodo)
    nodoExp = expresion.Expresion()
    nodoExp.valorPrimitivo(t[1],tipoSimbolo.TipoSimbolo.DECIMAL)
    nodoExp.setearValores(str(t.lexer.lineno),columna,"DECIMAL_",nNodo,t[1])
    t[0] = nodoExp

def p_instr_delete(t):
    '''delete_table   :   DELETE FROM ID PTCOMA
                      |   DELETE FROM ID WHERE exp_operacion PTCOMA'''
    
    
    linea = str(t.lexer.lineno)
    nodoId = crear_nodo_general("ID",t[3],linea,columna)
    nNodo = incNodo(numNodo)

    hijos = []
    if len(t) == 5:
        nodoDelete = deleteTable.DeleteTable(t[3],None)
        hijos.append(nodoId)
        nodoDelete.setearValores(linea,columna,"DELETE_FROM",nNodo,"",hijos)
        t[0] = nodoDelete
    else:
        nodoDelete = deleteTable.DeleteTable(t[3],t[4])
        hijos.append(nodoId)
        hijos.append(t[4])
        nodoDelete.setearValores(linea,columna,"DELETE_FROM",nNodo,"",hijos)
        t[0] = nodoDelete

def p_instr_condicion_where(t):
    'exp_operacion  :  exp_logica'
    nodoExp = crear_nodo_general("OPERACION","",str(t.lexer.lineno),columna)
    nodoExp.hijos.append(nodoExp)
    t[0] = nodoExp

def p_exp_logica(t):
    '''exp_logica     :   exp_logica OR exp_logica
                      |   exp_logica AND exp_logica
                      |   NOT exp_logica
                      |   exp_relacional'''
    
    if len(t) == 2:
        t[0] = t[1]
    elif len(t) == 3:        
        linea = str(t.lexer.lineno)
        nNodo = incNodo(numNodo)
        nodoExp = expresion.Expresion()
        nodoExp.setearValores(linea,columna,"EXPRESION_LOGICA",nNodo,"")
        nodoExp.operacionUnaria(t[2],tipoSimbolo.TipoSimbolo.NOT)
        nodoMas = crear_nodo_general("NOT","not",linea,columna)
        nodoExp.hijos.append(nodoMas)
        nodoExp.hijos.append(t[2])                
        t[0] = nodoExp
    else:
        tipOp = t[2]
        linea = str(t.lexer.lineno)
        nNodo = incNodo(numNodo)
        nodoExp = expresion.Expresion()
        nodoExp.setearValores(linea,columna,"EXPRESION_LOGICA",nNodo,"")

        if tipOp.lower() == "or":
            nodoExp.operacionBinaria(t[1],t[3],tipoSimbolo.TipoSimbolo.OR)
            nodoMas = crear_nodo_general("OR","or",linea,columna)
            nodoExp.hijos.append(t[1])
            nodoExp.hijos.append(nodoMas)
            nodoExp.hijos.append(t[3])
            t[0] = nodoExp
        elif tipOp.lower() == "and":
            nodoExp.operacionBinaria(t[1],t[3],tipoSimbolo.TipoSimbolo.AND)
            nodoMas = crear_nodo_general("AND","and",linea,columna)
            nodoExp.hijos.append(t[1])
            nodoExp.hijos.append(nodoMas)
            nodoExp.hijos.append(t[3])
            t[0] = nodoExp



def p_exp_relacional(t):
    '''exp_relacional   :   exp_relacional MENOR_QUE exp_relacional
                        |   exp_relacional MENOR_IGUAL exp_relacional
                        |   exp_relacional MAYOR_QUE exp_relacional
                        |   exp_relacional MAYOR_IGUAL exp_relacional
                        |   exp_relacional DISTINTO exp_relacional
                        |   exp_relacional IGUAL exp_relacional
                        |   exp_aritmetica'''
    
    if len(t) == 2:
        t[0] = t[1]
    else :
        tipOp = t[2]
        linea = str(t.lexer.lineno)
        nNodo = incNodo(numNodo)
        nodoExp = expresion.Expresion()
        nodoExp.setearValores(linea,columna,"EXPRESION_RELACIONAL",nNodo,"")

        if tipOp == "<":
            nodoExp.operacionBinaria(t[1],t[3],tipoSimbolo.TipoSimbolo.MENOR_QUE)
            nodoMas = crear_nodo_general("MENOR_QUE","<",linea,columna)
            nodoExp.hijos.append(t[1])
            nodoExp.hijos.append(nodoMas)
            nodoExp.hijos.append(t[3])
            t[0] = nodoExp
        elif tipOp == "<=":
            nodoExp.operacionBinaria(t[1],t[3],tipoSimbolo.TipoSimbolo.MENOR_IGUAL)
            nodoMas = crear_nodo_general("MENOR_IGUAL","<=",linea,columna)
            nodoExp.hijos.append(t[1])
            nodoExp.hijos.append(nodoMas)
            nodoExp.hijos.append(t[3])
            t[0] = nodoExp
        elif tipOp == ">":
            nodoExp.operacionBinaria(t[1],t[3],tipoSimbolo.TipoSimbolo.MAYOR_QUE)
            nodoMas = crear_nodo_general("MAYOR_QUE",">",linea,columna)
            nodoExp.hijos.append(t[1])
            nodoExp.hijos.append(nodoMas)
            nodoExp.hijos.append(t[3])
            t[0] = nodoExp
        elif tipOp == ">=":
            nodoExp.operacionBinaria(t[1],t[3],tipoSimbolo.TipoSimbolo.MAYOR_IGUAL)
            nodoMas = crear_nodo_general("MAYOR_IGUAL",">=",linea,columna)
            nodoExp.hijos.append(t[1])
            nodoExp.hijos.append(nodoMas)
            nodoExp.hijos.append(t[3])
            t[0] = nodoExp
        elif tipOp == "<>":
            nodoExp.operacionBinaria(t[1],t[3],tipoSimbolo.TipoSimbolo.DISTINTO)
            nodoMas = crear_nodo_general("DISTINTO","<>",linea,columna)
            nodoExp.hijos.append(t[1])
            nodoExp.hijos.append(nodoMas)
            nodoExp.hijos.append(t[3])
            t[0] = nodoExp
        elif tipOp == "=":
            nodoExp.operacionBinaria(t[1],t[3],tipoSimbolo.TipoSimbolo.IGUALACION)
            nodoMas = crear_nodo_general("IGUALACION","=",linea,columna)
            nodoExp.hijos.append(t[1])
            nodoExp.hijos.append(nodoMas)
            nodoExp.hijos.append(t[3])
            t[0] = nodoExp




def p_exp_aritmetica(t):
    '''exp_aritmetica   :   exp_aritmetica MAS exp_aritmetica
                        |   exp_aritmetica MENOS exp_aritmetica
                        |   exp_aritmetica MULTIPLICACION exp_aritmetica
                        |   exp_aritmetica DIVISION exp_aritmetica
                        |   exp_aritmetica MODULO exp_aritmetica
                        |   exp_aritmetica POTENCIA exp_aritmetica
                        |   exp_aritmetica BETWEEN exp_aritmetica AND exp_aritmetica
                        |   exp_aritmetica NOT BETWEEN exp_aritmetica AND exp_aritmetica
                        |   exp_aritmetica IN PARIZQUIERDO lista_expresiones PARDERECHO
                        |   exp_aritmetica NOT IN PARIZQUIERDO lista_expresiones PARDERECHO
                        |   exp_aritmetica IN subquery 
                        |   exp_aritmetica NOT IN subquery
                        |   exp_aritmetica LIKE exp_aritmetica
                        |   exp_aritmetica NOT LIKE exp_aritmetica
                        |   exp_aritmetica ILIKE exp_aritmetica
                        |   exp_aritmetica NOT ILIKE exp_aritmetica
                        |   exp_aritmetica SIMILAR TO exp_aritmetica
                        |   exp_aritmetica IS NULL
                        |   exp_aritmetica IS NOT NULL
                        |   primitivo'''

    ##----------SE AGREGO
    ##          |   exp_aritmetica IN subquery 
    ##          |   exp_aritmetica NOT IN subquery
    
    
    if len(t) == 2:
        t[0] = t[1]
    else:
        tipOp = t[2]
        linea = str(t.lexer.lineno)
        nNodo = incNodo(numNodo)
        nodoExp = expresion.Expresion()
        nodoExp.setearValores(linea,columna,"EXPRESION_ARITMETICA",nNodo,"")

        if tipOp == "+":
            nodoExp.operacionBinaria(t[1],t[3],tipoSimbolo.TipoSimbolo.SUMA)
            nodoMas = crear_nodo_general("MAS","+",linea,columna)
            nodoExp.hijos.append(t[1])
            nodoExp.hijos.append(nodoMas)
            nodoExp.hijos.append(t[3])
            t[0] = nodoExp
        elif tipOp == "-":
            nodoExp.operacionBinaria(t[1],t[3],tipoSimbolo.TipoSimbolo.RESTA)
            nodoMas = crear_nodo_general("MENOS","-",linea,columna)
            nodoExp.hijos.append(t[1])
            nodoExp.hijos.append(nodoMas)
            nodoExp.hijos.append(t[3])
            t[0] = nodoExp
        elif tipOp == "*":
            nodoExp.operacionBinaria(t[1],t[3],tipoSimbolo.TipoSimbolo.MULTIPLICACION)
            nodoMas = crear_nodo_general("MULTIPLICACION","*",linea,columna)
            nodoExp.hijos.append(t[1])
            nodoExp.hijos.append(nodoMas)
            nodoExp.hijos.append(t[3])
            t[0] = nodoExp
        elif tipOp == "/":
            nodoExp.operacionBinaria(t[1],t[3],tipoSimbolo.TipoSimbolo.DIVISION)
            nodoMas = crear_nodo_general("DIVISION","/",linea,columna)
            nodoExp.hijos.append(t[1])
            nodoExp.hijos.append(nodoMas)
            nodoExp.hijos.append(t[3])
            t[0] = nodoExp
        elif tipOp == "%":
            nodoExp.operacionBinaria(t[1],t[3],tipoSimbolo.TipoSimbolo.MODULO)
            nodoMas = crear_nodo_general("MODULO","%",linea,columna)
            nodoExp.hijos.append(t[1])
            nodoExp.hijos.append(nodoMas)
            nodoExp.hijos.append(t[3])
            t[0] = nodoExp
        elif tipOp == "^":
            nodoExp.operacionBinaria(t[1],t[3],tipoSimbolo.TipoSimbolo.POTENCIA)
            nodoMas = crear_nodo_general("POTENCIA","^",linea,columna)
            nodoExp.hijos.append(t[1])
            nodoExp.hijos.append(nodoMas)
            nodoExp.hijos.append(t[3])
            t[0] = nodoExp
        elif tipOp.lower() == "between":
            nNodo = incNodo(numNodo)
            nodoBetween = betweenIN.BetweenIn()
            nodoBetween.between(t[1],t[3],t[5],tipoSimbolo.TipoSimbolo.BETWEEN)
            hijosBetween = []
            hijosBetween.append(t[1])
            hijosBetween.append(t[3])
            hijosBetween.append(t[5])
            nodoBetween.setearValores(linea,columna,"BETWEEN",nNodo,"",hijosBetween)
            nodoExp.operacionUnaria(nodoBetween,tipoSimbolo.TipoSimbolo.BETWEEN)
            nodoExp.hijos.append(nodoBetween)
            t[0] = nodoExp
        elif tipOp.lower() == "in":
            if len(t) == 4:
                nNodo = incNodo(numNodo)
                nodoBetween = betweenIN.BetweenIn()
                nodoBetween.innSubquery(t[1],None,tipoSimbolo.TipoSimbolo.INN)                
                hijosBetween = []
                hijosBetween.append(t[1])
                hijosBetween.append(None)
                nodoBetween.setearValores(linea,columna,"IN",nNodo,"",hijosBetween)
                nodoExp.operacionUnaria(nodoBetween,tipoSimbolo.TipoSimbolo.INN)
                nodoExp.hijos.append(nodoBetween)
                t[0] = nodoExp 
            else:

                nNodo = incNodo(numNodo)
                nodoBetween = betweenIN.BetweenIn()
                nodoBetween.inn(t[1],t[4],tipoSimbolo.TipoSimbolo.INN)    
                hijosBetween = []
                hijosBetween.append(t[1])
                hijosBetween.append(t[4])        
                nodoBetween.setearValores(linea,columna,"IN",nNodo,"",hijosBetween)
                nodoExp.operacionUnaria(nodoBetween,tipoSimbolo.TipoSimbolo.INN)
                nodoExp.hijos.append(nodoBetween)
                t[0] = nodoExp    
        elif tipOp.lower() == "like":
            nodoExp.operacionBinaria(t[1],t[3],tipoSimbolo.TipoSimbolo.LIKE)
            nodoMas = crear_nodo_general("LIKE","like",linea,columna)
            nodoExp.hijos.append(t[1])
            nodoExp.hijos.append(nodoMas)
            nodoExp.hijos.append(t[3])
            t[0] = nodoExp
        elif tipOp.lower() == "ilike":
            nodoExp.operacionBinaria(t[1],t[3],tipoSimbolo.TipoSimbolo.ILIKE)
            nodoMas = crear_nodo_general("ILIKE","ilike",linea,columna)
            nodoExp.hijos.append(t[1])
            nodoExp.hijos.append(nodoMas)
            nodoExp.hijos.append(t[3])
            t[0] = nodoExp
        elif tipOp.lower() == "similar":
            nodoExp.operacionBinaria(t[1],t[4],tipoSimbolo.TipoSimbolo.SIMILAR)
            nodoMas = crear_nodo_general("SIMILAR","similar to",linea,columna)
            nodoExp.hijos.append(t[1])
            nodoExp.hijos.append(nodoMas)
            nodoExp.hijos.append(t[4])
            t[0] = nodoExp
        elif tipOp.lower() == "is":
            if len(t) == 4:
                nodoExp.operacionUnaria(t[1],tipoSimbolo.TipoSimbolo.IS_NULL)
                nodoMas = crear_nodo_general("IS_NULL","is null",linea,columna)
                nodoExp.hijos.append(t[1])
                nodoExp.hijos.append(nodoMas)            
                t[0] = nodoExp
            else:
                nodoExp.operacionUnaria(t[1],tipoSimbolo.TipoSimbolo.IS_NOT_NULL)
                nodoMas = crear_nodo_general("IS_NOT_NULL","is not null",linea,columna)
                nodoExp.hijos.append(t[1])
                nodoExp.hijos.append(nodoMas)            
                t[0] = nodoExp
        elif tipOp.lower() == "not":
            tip2 = t[3]
            if tip2.lower() == "between":
                nNodo = incNodo(numNodo)
                nodoBetween = betweenIN.BetweenIn()
                nodoBetween.between(t[1],t[4],t[6],tipoSimbolo.TipoSimbolo.NOT_BETWEEN)
                hijosBetween = []
                hijosBetween.append(t[1])
                hijosBetween.append(t[4])
                hijosBetween.append(t[6])
                nodoBetween.setearValores(linea,columna,"NOT_BETWEEN",nNodo,"",hijosBetween)
                nodoExp.operacionUnaria(nodoBetween,tipoSimbolo.TipoSimbolo.NOT_BETWEEN)
                nodoExp.hijos.append(nodoBetween)
                t[0] = nodoExp
            elif tip2.lower() == "in":

                if len(t) == 5:
                    nNodo = incNodo(numNodo)
                    nodoBetween = betweenIN.BetweenIn()
                    nodoBetween.innSubquery(t[1],None,tipoSimbolo.TipoSimbolo.NOT_INN)                    
                    hijosBetween = []
                    hijosBetween.append(t[1])
                    hijosBetween.append(None)        
                    nodoBetween.setearValores(linea,columna,"NOT_IN",nNodo,"",hijosBetween)
                    nodoExp.operacionUnaria(nodoBetween,tipoSimbolo.TipoSimbolo.NOT_INN)
                    nodoExp.hijos.append(nodoBetween)
                    t[0] = nodoExp                 
                else:
                    nNodo = incNodo(numNodo)
                    nodoBetween = betweenIN.BetweenIn()
                    nodoBetween.inn(t[1],t[5],tipoSimbolo.TipoSimbolo.NOT_INN)    
                    hijosBetween = []
                    hijosBetween.append(t[1])
                    hijosBetween.append(t[5])        
                    nodoBetween.setearValores(linea,columna,"NOT_IN",nNodo,"",hijosBetween)
                    nodoExp.operacionUnaria(nodoBetween,tipoSimbolo.TipoSimbolo.NOT_INN)
                    nodoExp.hijos.append(nodoBetween)
                    t[0] = nodoExp    
            elif tip2.lower() == "like":
                nodoExp.operacionBinaria(t[1],t[4],tipoSimbolo.TipoSimbolo.NOT_LIKE)
                nodoMas = crear_nodo_general("NOT_LIKE","not like",linea,columna)
                nodoExp.hijos.append(t[1])
                nodoExp.hijos.append(nodoMas)
                nodoExp.hijos.append(t[4])
                t[0] = nodoExp
            elif tip2.lower() == "ilike":
                nodoExp.operacionBinaria(t[1],t[4],tipoSimbolo.TipoSimbolo.NOT_ILIKE)
                nodoMas = crear_nodo_general("NOT_ILIKE","not ilike",linea,columna)
                nodoExp.hijos.append(t[1])
                nodoExp.hijos.append(nodoMas)
                nodoExp.hijos.append(t[4])
                t[0] = nodoExp







def p_primitivo_columna(t):
    'primitivo  :   ID'
    
    linea = str(t.lexer.lineno)
    nodoId = crear_nodo_general("NombreColumna",t[1],linea,columna)
    hijos = []
    nNodo = incNodo(numNodo)    
    nodoPri = expresion.Expresion()
    nodoPri.valorPrimitivo(t[1],tipoSimbolo.TipoSimbolo.NOMBRE_COLUMNA)
    hijos.append(nodoId) 
    nodoPri.setearValores(linea,columna,"PRIMITIVO",nNodo,t[1],hijos)    
    t[0] = nodoPri



def p_primitivo_primitivo(t):
    '''primitivo    :   MAS primitivo
                    |   MENOS primitivo
                    |   PARIZQUIERDO exp_operacion PARDERECHO'''
    

    if len(t) == 4:
        t[0] = t[2]
    else:       
        linea = str(t.lexer.lineno)
        nodoPri = expresion.Expresion()
        hijos = []

        if t[1] == '+':
            nodoOp = crear_nodo_general("MAS","+",linea,columna)
            nNodo = incNodo(numNodo)            
            nodoPri.operacionUnaria(t[2],tipoSimbolo.TipoSimbolo.POSITIVO_UNARIO)
            hijos.append(nodoOp)
            hijos.append(t[2])
            nodoPri.setearValores(linea,columna,"PRIMITIVO",nNodo,"",hijos)
            t[0] = nodoPri
        else:
            nodoOp = crear_nodo_general("MENOS","-",linea,columna)
            nNodo = incNodo(numNodo)
            nodoPri.operacionUnaria(t[2],tipoSimbolo.TipoSimbolo.NEGATIVO_UNARIO)
            hijos.append(nodoOp)
            hijos.append(t[2])
            nodoPri.setearValores(linea,columna,"PRIMITIVO",nNodo,"",hijos)
            t[0] = nodoPri
            


def p_primitivo_entero(t):
    'primitivo  :   ENTERO'
    nNodo = incNodo(numNodo)
    linea = str(t.lexer.lineno)
    nodoPri = expresion.Expresion()
    nodoPri.valorPrimitivo(t[1],tipoSimbolo.TipoSimbolo.ENTERO)
    nodoPri.setearValores(linea,columna,"PRIMITIVO",nNodo,t[1])
    t[0] = nodoPri

def p_primitivo_decimal(t):
    'primitivo    :   DECIMAL_'                 

    nNodo = incNodo(numNodo)
    linea = str(t.lexer.lineno)
    nodoPri = expresion.Expresion()
    nodoPri.valorPrimitivo(t[1],tipoSimbolo.TipoSimbolo.DECIMAL)
    nodoPri.setearValores(linea,columna,"PRIMITIVO",nNodo,t[1])
    t[0] = nodoPri

    

def p_primitivo_cadena(t):
    'primitivo  :   CADENA'

    nNodo = incNodo(numNodo)
    linea = str(t.lexer.lineno)
    nodoPri = expresion.Expresion()
    nodoPri.valorPrimitivo(t[1],tipoSimbolo.TipoSimbolo.CADENA)
    nodoPri.setearValores(linea,columna,"PRIMITIVO",nNodo,t[1])
    t[0] = nodoPri

def p_primitivo_booleano(t):
    '''primitivo  :   TRUE
                  |   FALSE'''
    
    nNodo = incNodo(numNodo)
    linea = str(t.lexer.lineno)
    tipo = t[1]
    if (tipo.lower()=="true"):
        nodoPri = expresion.Expresion()
        nodoPri.valorPrimitivo(True,tipoSimbolo.TipoSimbolo.BOOLEANO)
        nodoPri.setearValores(linea,columna,"PRIMTIVO",nNodo,True)
        t[0] = nodoPri
    else:
        nodoPri = expresion.Expresion()
        nodoPri.valorPrimitivo(False,tipoSimbolo.TipoSimbolo.BOOLEANO)
        nodoPri.setearValores(linea,columna,"PRIMTIVO",nNodo,False)
        t[0] = nodoPri


def p_instr_update_table(t):
    '''update_table     :   UPDATE ID SET lista_seteos PTCOMA
                        |   UPDATE ID SET lista_seteos WHERE exp_operacion PTCOMA'''
    
    linea = str(t.lexer.lineno)
    nodoId = crear_nodo_general("ID",t[2],linea,columna)
    nNodo = incNodo(numNodo)
    hijos = []

    if len(t) == 6:
        nodoUpdate = updateTable.UpdateTable(t[2],t[4].hijos,None)
        hijos.append(nodoId)
        hijos.append(t[4])
        nodoUpdate.setearValores(linea,columna,"UPDATE_TABLE",nNodo,"",hijos)
        t[0] = nodoUpdate
    else:
        nodoUpdate = updateTable.UpdateTable(t[2],t[4].hijos,t[6])
        hijos.append(nodoId)
        hijos.append(t[4])
        hijos.append(t[6])
        nodoUpdate.setearValores(linea,columna,"UPDATE_TABLE",nNodo,"",hijos)
        t[0] = nodoUpdate


def p_lista_seteos(t):
    '''lista_seteos     :   lista_seteos COMA set_columna
                        |   set_columna'''

    linea = str(t.lexer.lineno)
    if len(t) == 2:
        nodoLista = crear_nodo_general("LISTA_SETEOS","",linea,columna)
        nodoLista.hijos.append(t[1])
        t[0] = nodoLista
    else:
        nodoLista = t[1]
        nodoLista.hijos.append(t[3])
        t[0] = nodoLista
        
def p_set_columna(t):
    'set_columna    :   ID IGUAL exp_operacion'
    
    linea = str(t.lexer.lineno)
    nodoId = crear_nodo_general("ID",t[1],linea,columna)
    nNodo = incNodo(numNodo)
    hijos = []
    nodoSet = updateColumna.UpdateColumna(t[1],t[3])
    hijos.append(nodoId)
    hijos.append(t[3])
    nodoSet.setearValores(linea,columna,"set_columna",nNodo,"",hijos)
    t[0] = nodoSet
        
#--------------------------------------------Definiciones de las columnas de tablas----------------------------------------------------    
def p_columnas_lista(t):
    'columnas : columnas COMA columna'
    linea = str(t.lexer.lineno)
    nodoColumnas = t[1]
    nodoColumna = t[3]
    nodoColumnas.hijos.append(nodoColumna)
    t[0] = nodoColumnas

def p_columnas_columna(t):
    'columnas : columna'
    linea = str(t.lexer.lineno)
    nodoColumna = t[1]
    nodoColumnas = crear_nodo_general("columnas","",linea,columna)
    nodoColumnas.hijos.append(nodoColumna)
    t[0] = nodoColumnas

def p_columna_id(t):
    'columna : ID tipos opcional'
    linea = str(t.lexer.lineno)
    nodoColumna = crear_nodo_general("columna","",linea,columna)
    nodoId = crear_nodo_general("ID",t[1],linea,columna)
    nodoTipo = t[2]
    nodoOpcional = t[3]
    nodoColumna.hijos.append(nodoId)
    nodoColumna.hijos.append(nodoTipo)
    nodoColumna.hijos.append(nodoOpcional)
    t[0] = nodoColumna

def p_columna_primary(t):
    'columna : PRIMARY KEY PARIZQUIERDO identificadores PARDERECHO'
    linea = str(t.lexer.lineno)
    nodoColumna = crear_nodo_general("columna","",linea,columna)
    nodoPK = crear_nodo_general("PRIMARY","PRIMARY KEY",linea,columna)
    listaIds = t[4]
    nodoColumna.hijos.append(nodoPK)
    nodoColumna.hijos.append(listaIds)
    t[0] = nodoColumna

def p_columna_foreign(t):
    'columna : FOREIGN KEY PARIZQUIERDO identificadores PARDERECHO REFERENCES ID PARIZQUIERDO identificadores PARDERECHO'
    linea = str(t.lexer.lineno)
    nodoColumna = crear_nodo_general("columna","",linea,columna)
    nodoFK = crear_nodo_general("FOREIGN","FOREIGN KEY",linea,columna)
    listaId1 = t[4]
    nodoReferences = crear_nodo_general("REFERENCES","REFERENCES",linea,columna)
    nodoId = crear_nodo_general("ID",t[7],linea,columna)
    listaId2 = t[9]
    nodoColumna.hijos.append(nodoFK)
    nodoColumna.hijos.append(listaId1)
    nodoColumna.hijos.append(nodoReferences)
    nodoColumna.hijos.append(nodoId)
    nodoColumna.hijos.append(listaId2)
    t[0] = nodoColumna


def p_columna_unique(t):
    'columna : UNIQUE PARIZQUIERDO identificadores PARDERECHO'
    linea = str(t.lexer.lineno)
    nodoColumna = crear_nodo_general("columna","",linea,columna)
    nodoUnique = crear_nodo_general("UNIQUE","UNIQUE",linea,columna)
    listaIds = t[3]
    nodoColumna.hijos.append(nodoUnique)
    nodoColumna.hijos.append(listaIds)
    t[0] = nodoColumna

#-------------------------------------------Definiciones de opcionales para la columna ID Tipo...---------------------------------------
def p_opcionales(t):
    'opcional : DEFAULT opcionNull'
    linea = str(t.lexer.lineno)
    nodoOpcional = crear_nodo_general("opcional","",linea,columna)
    nodoDefault = crear_nodo_general("DEFAULT","DEFAULT",linea,columna)
    nodoOpNull = t[2]
    nodoOpcional.hijos.append(nodoDefault)
    nodoOpcional.hijos.append(nodoOpNull)
    t[0] = nodoOpcional

def p_opcional_opcionNull(t):
    'opcional : opcionNull'
    linea = str(t.lexer.lineno)
    nodoOpcional = crear_nodo_general("opcional","",linea,columna)
    nodoOpNull = t[1]
    nodoOpcional.hijos.append(nodoOpNull)
    t[0] = nodoOpcional

def p_opcion_null(t):
    'opcionNull : NULL opConstraint'
    linea = str(t.lexer.lineno)
    nodoOpNull = crear_nodo_general("opcionNull","",linea,columna)
    nodoNull = crear_nodo_general("NULL","NULL",linea,columna)
    nodoOpConstraint = t[2]
    nodoOpNull.hijos.append(nodoNull)
    nodoOpNull.hijos.append(nodoOpConstraint)
    t[0] = nodoOpNull

def p_opcion_not_null(t):
    'opcionNull : NOT NULL opConstraint'
    linea = str(t.lexer.lineno)
    nodoOpNull = crear_nodo_general("opcionNull","",linea,columna)
    nodoNull = crear_nodo_general("NOTNULL","NOT NULL",linea,columna)
    nodoOpConstraint = t[3]
    nodoOpNull.hijos.append(nodoNull)
    nodoOpNull.hijos.append(nodoOpConstraint)
    t[0] = nodoOpNull

def p_opcion_null_constraint(t):
    'opcionNull : opConstraint '
    linea = str(t.lexer.lineno)
    nodoOpNull = crear_nodo_general("opcionNull","",linea,columna)
    nodoOpConstraint = t[1]
    nodoOpNull.hijos.append(nodoOpConstraint)
    t[0] = nodoOpNull

def p_op_constraint(t):
    'opConstraint : CONSTRAINT ID opUniqueCheck'
    linea = str(t.lexer.lineno)
    nodoOpConstraint = crear_nodo_general("opConstraint","",linea,columna)
    nodoConstrant = crear_nodo_general("CONSTRAINT","CONSTRAINT",linea,columna)
    nodoId = crear_nodo_general("ID",t[2],linea,columna)
    nodoopUniqueCheck = t[3]
    nodoOpConstraint.hijos.append(nodoConstrant)
    nodoOpConstraint.hijos.append(nodoId)
    nodoOpConstraint.hijos.append(nodoopUniqueCheck)
    t[0] = nodoOpConstraint
    

def p_op_constraint_unique_check(t):
    'opConstraint : opUniqueCheck'
    linea = str(t.lexer.lineno)
    nodoOpUnique = t[1]
    nodoOpConstraint = crear_nodo_general("opConstraint","",linea,columna)
    nodoOpConstraint.hijos.append(nodoOpUnique)
    t[0] = nodoOpConstraint

def p_op_unique_check(t):
    'opUniqueCheck : UNIQUE'
    linea = str(t.lexer.lineno)
    nodoUnique = crear_nodo_general("UNIQUE","UNIQUE",linea,columna)
    nodoOpUnique = crear_nodo_general("opUniqueCheck","",linea,columna)
    nodoOpUnique.hijos.append(nodoUnique)
    t[0] = nodoOpUnique

def p_op_unique_check_check(t):
    'opUniqueCheck : CHECK PARIZQUIERDO condicion_check PARDERECHO' 
    linea =  str(t.lexer.lineno)
    nodoopUniqueCheck = crear_nodo_general("opUniqueCheck","",linea,columna)
    nodoCheck = crear_nodo_general("CHECK","CHECK",linea,columna)
    nodoCondicion = t[3]
    nodoopUniqueCheck.hijos.append(nodoCheck)
    nodoopUniqueCheck.hijos.append(nodoCondicion)
    t[0] = nodoopUniqueCheck

def p_condicion_check(t):
    '''condicion_check : ID MENOR_QUE expresion
                        | ID MENOR_IGUAL expresion
                        | ID MAYOR_QUE expresion
                        | ID MAYOR_IGUAL expresion
                        | ID DISTINTO expresion
                        | ID IGUAL expresion '''
    linea = str(t.lexer.lineno)
    hijos = []
    nodoId = crear_nodo_general("ID",t[1],linea,columna)
    nodoComp = crear_nodo_general("comparacion",t[2],linea,columna)
    nodoPrimitivo = crear_nodo_general("primitivo",t[3],linea,columna)
    nodoCondicion = crear_nodo_general("condicion_check","",linea,columna)
    nodoCondicion.hijos.append(nodoId)
    nodoCondicion.hijos.append(nodoComp)
    nodoCondicion.hijos.append(nodoPrimitivo)
    t[0] = nodoCondicion                       

def p_op_unique_empty(t):
    'opUniqueCheck : empty'
    t[0] = None
 #------------------------------------------------Definicion de regla epsilon y herencia----------------------------------------------------------   

def p_empty(t):
     'empty :'
     pass

def p_herencia(t):
    'herencia : INHERITS PARIZQUIERDO ID PARDERECHO'
    linea = str(t.lexer.lineno)
    nodoId = crear_nodo_general("ID",t[3],linea,columna)
    nodoHerencia = crear_nodo_general("herencia","",linea,columna)
    nodoHerencia.hijos.append(nodoId)
    t[0] = nodoHerencia

def p_herencia_empty(t):
    'herencia : empty'
    t[0] = None
#--------------------------------------------------Lista de identificadores y cadenas------------------------------------------------------------
def p_identificadores_lista(t):
    'identificadores : identificadores COMA ID'
    linea = str(t.lexer.lineno)
    nodoPadre = t[1]
    nodoId = crear_nodo_general("ID",t[3],str(linea),columna)
    nodoPadre.hijos.append(nodoId)
    t[0] = nodoPadre

def p_identificadores_id(t):
    'identificadores : ID'
    linea = str(t.lexer.lineno)
    nodoId = crear_nodo_general("ID",t[1],str(linea),columna)
    nodoLista = crear_nodo_general("identificadores","",linea,columna)
    nodoLista.hijos.append(nodoId)
    t[0] = nodoLista

def p_cadenas_lista(t):
    'cadenas : cadenas COMA  CADENA'
    linea = str(t.lexer.lineno)
    nodoPadre = t[1]
    nodoId = crear_nodo_general("CADENA",t[3],str(linea),columna)
    nodoPadre.hijos.append(nodoId)
    t[0] = nodoPadre

def p_cadenas_cadena(t):
    'cadenas : CADENA'
    linea = str(t.lexer.lineno)
    nodoId = crear_nodo_general("CADENA",t[1],str(linea),columna)
    nodoLista = crear_nodo_general("cadenas","",linea,columna)
    nodoLista.hijos.append(nodoId)
    t[0] = nodoLista

#-------------------------------------------------Definiciones de opcionales para crear databases--------------------------------------
def p_op_replace(t):
    'opReplace : OR REPLACE'
    linea = str(t.lexer.lineno)
    nodoOpReplace = crear_nodo_general("opReplace","",linea,columna)
    nodoOrReplace = crear_nodo_general("ORREPLACE", "OR REPLACE",linea,columna)
    nodoOpReplace.hijos.append(nodoOrReplace)
    t[0] = nodoOpReplace

def p_op_replace_empty(t):
    'opReplace : empty'
    t[0] = None

def p_op_exists(t):
    'opExists : IF NOT EXISTS'
    linea = str(t.lexer.lineno)
    nodoOpExists = crear_nodo_general("opExists","",linea,columna)
    nodoCondicion = crear_nodo_general("IFNOTEXISTS","IF NOT EXISTS",linea,columna)
    nodoOpExists.hijos.append(nodoCondicion)
    t[0] = nodoOpExists

def p_op_exists_empty(t):
    'opExists : empty'
    t[0] = None

def p_op_database(t):
    'opDatabase : OWNER opIgual ID mode'
    linea = str(t.lexer.lineno)
    nodoOpDatabase = crear_nodo_general("opDatabase","",linea,columna)
    nodoOwner = crear_nodo_general("OWNER","OWNER",linea,columna)
    nodoOpIgual = t[2]
    nodoId = crear_nodo_general("ID",t[3],linea,columna)
    nodoModo = crear_nodo_general("mode",t[4],linea,columna)
    nodoOpDatabase.hijos.append(nodoOwner)
    nodoOpDatabase.hijos.append(nodoOpIgual)
    nodoOpDatabase.hijos.append(nodoId)
    nodoOpDatabase.hijos.append(nodoModo)
    t[0] = nodoOpDatabase

def p_op_database_mode(t):
    'opDatabase : mode'
    linea = str(t.lexer.lineno)
    nodoOpDatabase = crear_nodo_general("opDatabase","",linea,columna)
    nodoModo = t[1]
    nodoOpDatabase.hijos.append(nodoModo)
    t[0] = nodoOpDatabase

def p_op_igual(t):
    'opIgual : IGUAL'
    linea = str(t.lexer.lineno)
    nodoOpIgual = crear_nodo_general("opIgual","",linea,columna)
    nodoIgual = crear_nodo_general("IGUAL",t[1],linea,columna)
    nodoOpIgual.hijos.append(nodoIgual)
    t[0] = nodoOpIgual

def p_op_igual_empty(t):
    'opIgual : empty'
    t[0] = None 

def p_mode(t):
    'mode : MODE opIgual ENTERO'
    linea = str(t.lexer.lineno)
    nodoModo = crear_nodo_general("modo","",linea,columna)
    nodoMode = crear_nodo_general("MODE",t[1],linea,columna)
    nodoOpIgual = t[2]
    nodoEntero = crear_nodo_general("ENTERO",t[3],linea,columna)
    nodoModo.hijos.append(nodoMode)
    nodoModo.hijos.append(nodoOpIgual)
    nodoModo.hijos.append(nodoEntero)
    t[0] = nodoModo

def p_mode_empty(t):
    'mode : empty'
    t[0] = None 


#---------------------------------------------------Instrucciones alter------------------------------------
def p_alter_instr(t):
    'alter_instr : ALTER DATABASE ID opAlterDatabase PTCOMA'
    linea = str(t.lexer.lineno)
    hijos = []
    nNodo = incNodo(numNodo)
    nodoId = crear_nodo_general("ID",t[3],linea,columna)
    nodoInstr = t[4]
    instru = alterDatabase.alterDatabase(t[3],t[4].hijos)
    hijos.append(nodoId)
    hijos.append(nodoInstr)
    instru.setearValores(linea,columna,"ALTER_DATABASE",nNodo,"",hijos)
    t[0] = instru

def p_alter_instr_table(t):
    'alter_instr : ALTER TABLE ID alter_table_instr PTCOMA'
    linea = str(t.lexer.lineno)
    hijos = []
    nNodo = incNodo(numNodo)
    nodoId = crear_nodo_general("ID",t[3],linea,columna)
    nodoInstr = t[4]
    instru = alterTable.alterTable(t[3],t[4].hijos)
    hijos.append(nodoId)
    hijos.append(nodoInstr)
    instru.setearValores(linea,columna,"ALTER_TABLE",nNodo,"",hijos)
    t[0] = instru

def p_op_alter_database(t):
    'opAlterDatabase : RENAME TO ID'
    linea = str(t.lexer.lineno)
    nodoOpAlter = crear_nodo_general("opAlterDatabase","",linea,columna)
    nodoRename = crear_nodo_general("RENAME","RENAME TO",linea,columna)
    nodoId = crear_nodo_general("ID",t[3],linea,columna)
    nodoOpAlter.hijos.append(nodoRename)
    nodoOpAlter.hijos.append(nodoId)
    t[0] = nodoOpAlter

def p_op_alter_database_owner(t):
    'opAlterDatabase : OWNER TO ownerList'
    linea = str(t.lexer.lineno)
    nodoOpAlter = crear_nodo_general("opAlterDatabase","",linea,columna)
    nodoOwner = crear_nodo_general("OWNER","OWNER TO",linea,columna)
    nodoOwnerList = t[3]
    nodoOpAlter.hijos.append(nodoOwner)
    nodoOpAlter.hijos.append(nodoOwnerList)
    t[0] = nodoOpAlter

def p_owner_list(t):
    'ownerList : ID'
    linea = str(t.lexer.lineno)
    nodoOwnerList = crear_nodo_general("ownerList","",linea,columna)
    nodoId = crear_nodo_general("ID",t[1],linea,columna)
    nodoOwnerList.hijos.append(nodoId)
    t[0] = nodoOwnerList

def p_owner_current(t):
    'ownerList : CURRENT_USER'
    linea = str(t.lexer.lineno)
    nodoOwnerList = crear_nodo_general("ownerList","",linea,columna)
    nodoCurrent = crear_nodo_general("CURRENT_USER",t[1],linea,columna)
    nodoOwnerList.hijos.append(nodoCurrent)
    t[0] = nodoOwnerList

def p_owner_session(t):
    'ownerList : SESSION_USER'
    linea = str(t.lexer.lineno)
    nodoOwnerList = crear_nodo_general("ownerList","",linea,columna)
    nodoSession = crear_nodo_general("SESSION_USER",t[1],linea,columna)
    nodoOwnerList.hijos.append(nodoSession)
    t[0] = nodoOwnerList

def p_alter_table_instr(t):
    'alter_table_instr : ADD add_instr'
    linea = str(t.lexer.lineno)
    nodoAddI = t[2]
    nodoAdd = crear_nodo_general("ADD","ADD",linea,columna)
    nodoAlter = crear_nodo_general("alter_column_instr","",linea,columna)
    nodoAlter.hijos.append(nodoAdd)
    nodoAlter.hijos.append(nodoAddI)
    t[0] = nodoAlter

def p_alter_table_instr_column(t):
    'alter_table_instr : alter_columnas'
    linea = str(t.lexer.lineno)
    nodoColumnas = t[1]
    nodoAlter = crear_nodo_general("alter_column_instr","",linea,columna)
    nodoAlter.hijos.append(nodoColumnas)
    t[0] = nodoAlter

def p_alter_table_instr_drop_columnas(t):
    'alter_table_instr : drop_columnas'
    linea = str(t.lexer.lineno)
    nodoDrop = t[1]
    nodoAlter = crear_nodo_general("alter_column_instr","",linea,columna)
    nodoAlter.hijos.append(nodoDrop)
    t[0] = nodoAlter

def p_alter_columnas(t):
    'alter_columnas : alter_columnas COMA alter_columna'
    linea = str(t.lexer.lineno)
    nodoColumnas = t[1]
    nodoColumna = t[3]
    nodoColumnas.hijos.append(nodoColumna)
    t[0] = nodoColumnas
    
def p_alter_columnas_columna(t):
    'alter_columnas : alter_columna'
    linea = str(t.lexer.lineno)
    nodoColumna = t[1]
    nodoColumnas = crear_nodo_general("alter_columnas","",linea,columna)
    nodoColumnas.hijos.append(nodoColumna)
    t[0] = nodoColumnas

def p_alter_columna(t):
    'alter_columna : ALTER COLUMN ID alter_column_instr'
    linea = str(t.lexer.lineno)
    nodoIAlterColumn = crear_nodo_general("alter_columna","",linea,columna)
    nodoAlterColumn = crear_nodo_general("ALTER","ALTER COLUMN",linea,columna)
    nodoId = crear_nodo_general("ID",t[3],linea,columna)
    nodoAlterInstr = t[4]
    nodoIAlterColumn.hijos.append(nodoAlterColumn)
    nodoIAlterColumn.hijos.append(nodoId)
    nodoIAlterColumn.hijos.append(nodoAlterInstr)
    t[0] = nodoIAlterColumn

def p_drop_columnas(t):
    'drop_columnas : drop_columnas COMA drop_columna'
    linea = str(t.lexer.lineno)
    nodoColumnas = t[1]
    nodoColumna = t[3]
    nodoColumnas.hijos.append(nodoColumna)
    t[0] = nodoColumnas


def p_drop_columnas_columna(t):
    'drop_columnas : drop_columna'
    linea = str(t.lexer.lineno)
    nodoColumna = t[1]
    nodoColumnas = crear_nodo_general("drop_columnas","",linea,columna)
    nodoColumnas.hijos.append(nodoColumna)
    t[0] = nodoColumnas

def p_drop_columna(t):
    'drop_columna : DROP COLUMN ID'
    linea = str(t.lexer.lineno)
    nodoDropInstr = crear_nodo_general("drop_instr","",linea,columna)
    nodoDrop = crear_nodo_general("DROP","DROP",linea,columna)
    nodoColumna = crear_nodo_general("COLUMN","COLUMN",linea,columna)
    nodoId = crear_nodo_general("ID",t[3],linea,columna)
    nodoDropInstr.hijos.append(nodoDrop)
    nodoDropInstr.hijos.append(nodoColumna)
    nodoDropInstr.hijos.append(nodoId)
    t[0] = nodoDropInstr

def p_alter_table_instr_drop(t):
    'alter_table_instr : DROP CONSTRAINT ID'
    linea = str(t.lexer.lineno)
    nodoAlter = crear_nodo_general("alter_table_instr","",linea,columna)
    nodoDrop = crear_nodo_general("DROP","DROP",linea,columna)
    nodoConstrant = crear_nodo_general("CONSTRAINT","CONSTRAINT",linea,columna)
    nodoId = crear_nodo_general("ID",t[3],linea,columna)
    nodoAlter.hijos.append(nodoDrop)
    nodoAlter.hijos.append(nodoConstrant)
    nodoAlter.hijos.append(nodoId)
    t[0] = nodoAlter

def p_add_instr(t):
    'add_instr : CHECK PARIZQUIERDO condicion_check PARDERECHO'
    linea = str(t.lexer.lineno)
    nodoAdd = crear_nodo_general("add_instr","",linea,columna)
    nodoCheck = crear_nodo_general("CHECK","CHECK",linea,columna)
    nodoCondicion = crear_nodo_general("condicion_check",t[3],linea,columna)
    nodoAdd.hijos.append(nodoCheck)
    nodoAdd.hijos.append(nodoCondicion)
    t[0] = nodoAdd

def p_add_instr_constraint(t):
    'add_instr : CONSTRAINT ID UNIQUE PARIZQUIERDO ID PARDERECHO'
    linea = str(t.lexer.lineno)
    nodoAdd = crear_nodo_general("add_instr","",linea,columna)
    nodoConstrant = crear_nodo_general("CONSTRAINT","CONSTRAINT",linea,columna)
    nodoId1 = crear_nodo_general("ID",t[2],linea,columna)
    nodoUnique = crear_nodo_general("UNIQUE","UNIQUE",linea,columna)
    nodoId2 = crear_nodo_general("ID",t[5],linea,columna)
    nodoAdd.hijos.append(nodoConstrant)
    nodoAdd.hijos.append(nodoId1)
    nodoAdd.hijos.append(nodoUnique)
    nodoAdd.hijos.append(nodoId2)
    t[0] = nodoAdd

def p_alter_column_instr(t):
    'alter_column_instr : SET NOT NULL'
    linea = str(t.lexer.lineno)
    nodoAlterColumn = crear_nodo_general("alter_table_instr","",linea,columna)
    nodoSet = crear_nodo_general("SET","SET",linea,columna)
    nodoNull = crear_nodo_general("NOTNULL","NOT NULL",linea,columna)
    nodoAlterColumn.hijos.append(nodoSet)
    nodoAlterColumn.hijos.append(nodoNull)
    t[0] = nodoAlterColumn

def p_alter_column_instr_null(t):
    'alter_column_instr : SET NULL'
    linea = str(t.lexer.lineno)
    nodoAlterColumn = crear_nodo_general("alter_table_instr","",linea,columna)
    nodoSet = crear_nodo_general("SET","SET",linea,columna)
    nodoNull = crear_nodo_general("NULL","NULL",linea,columna)
    nodoAlterColumn.hijos.append(nodoSet)
    nodoAlterColumn.hijos.append(nodoNull)
    t[0] = nodoAlterColumn

def p_alter_column_instr_tipo(t):
    'alter_column_instr : TYPE ID '   #HAY QUE COLOCAR UN TIPO
    linea = str(t.lexer.lineno)
    nodoAlterColumn = crear_nodo_general("alter_table_instr","",linea,columna)
    nodoType = crear_nodo_general("TYPE","TYPE",linea,columna)
    nodoId = crear_nodo_general("ID",t[2],linea,columna)
    nodoAlterColumn.hijos.append(nodoType)
    nodoAlterColumn.hijos.append(nodoId)
    t[0] = nodoAlterColumn

#--------------------------------------------------------INSTRUCCIONES DROP-------------------------------------------------------------
def p_drop_instr(t):
    'drop_instr : DROP DATABASE si_existe ID PTCOMA'
    linea = str(t.lexer.lineno)
    hijos = []
    nNodo = incNodo(numNodo)
    nodoId = crear_nodo_general("ID",t[4],linea,columna)
    instru = dropDatabase.dropDatabase(t[4])
    hijos.append(nodoId)
    instru.setearValores(linea,columna,"DROP_DATABASE",nNodo,"",hijos)   
    t[0] = instru

def p_drop_instr_table(t):
    'drop_instr : DROP TABLE ID PTCOMA'
    linea = str(t.lexer.lineno)
    hijos = []
    nNodo = incNodo(numNodo)
    nodoId = crear_nodo_general("ID",t[3],linea,columna)
    instru = dropDatabase.dropDatabase(t[3])
    hijos.append(nodoId)
    instru.setearValores(linea,columna,"drop_instr",nNodo,"DROP TABLE",hijos)
    t[0] = instru

def p_si_existe(t):
    'si_existe : IF EXISTS'
    nodoPadre = crear_nodo_general("si_existe","",str(t.lexer.lineno),columna)
    nodo = crear_nodo_general("IFEXISTS","IF EXISTS",str(t.lexer.lineno),columna)
    nodoPadre.hijos.append(nodo)
    t[0] = nodo

def p_si_existe_empty(t):
    'si_existe : empty'
    t[0] = None 
#----------------------------------------------------------INSTRUCCIONES SELECT----------------------------------------------------------------

def p_inst_query(t):
    '''inst_select  :   select_query
                    |   select_query UNION select_query
                    |   select_query UNION ALL select_query
                    |   select_query INTERSECT select_query
                    |   select_query INTERSECT ALL select_query
                    |   select_query EXCEPT select_query
                    |   select_query EXCEPT ALL select_query'''

def p_select_query(t):
    '''select_query     :   SELECT DISTINCT select_list FROM from_query_list lista_condiciones_query
                        |   SELECT select_list FROM from_query_list lista_condiciones_query
                        |   SELECT DISTINCT select_list FROM from_query_list 
                        |   SELECT select_list FROM from_query_list
                        |   SELECT select_list'''

def p_select_list(t):
    '''select_list  :   MULTIPLICACION
                    |   elementos_select_list'''

def p_elementos_select_list(t):
    '''elementos_select_list    :   elementos_select_list COMA elemento_select
                                |   elemento_select'''

def p_elemento_select(t):
    '''elemento_select  :   dec_select_columna
                        |   subquery AS ID
                        |   subquery ID
                        |   subquery
                        |   funcion AS ID
                        |   funcion ID
                        |   funcion'''

def p_dec_select_columna(t):
    '''dec_select_columna   :   ID PUNTO ID AS ID
                            |   ID PUNTO ID ID
                            |   ID PUNTO ID
                            |   ID'''

def p_funcion(t):
    '''funcion  :   funcion_time
                |   funcion_mate
                |   funcion_trig
                |   funcion_binstr
                |   funcion_exprecion'''

def p_funcion_time(t):
    '''funcion_time :   EXTRACT PARIZQUIERDO var_time FROM var_timeextract CADENA PARDERECHO
                    |   DATE_PART PARIZQUIERDO CADENA COMA var_timeextract CADENA PARDERECHO
                    |   NOW PARIZQUIERDO PARDERECHO
                    |   var_timeextract CADENA
                    |   CURRENT_DATE
                    |   CURRENT_TIME'''

def p_var_time(t):
    '''var_time :   YEAR
                |   MONTH
                |   DAY
                |   HOUR
                |   MINUTE
                |   SECOND'''

def p_var_timeextract(t):
    '''var_timeextract  :   TIMESTAMP
                        |   TIME
                        |   DATE
                        |   INTERVAL'''

def p_funcion_mate(t):
    '''funcion_mate :   ABS PARIZQUIERDO exp_operacion PARDERECHO
                    |   CBRT PARIZQUIERDO exp_operacion PARDERECHO
                    |   CEIL PARIZQUIERDO exp_operacion PARDERECHO
                    |   CEILING PARIZQUIERDO exp_operacion PARDERECHO
                    |   DEGREES PARIZQUIERDO exp_operacion PARDERECHO
                    |   DIV PARIZQUIERDO exp_operacion COMA exp_operacion PARDERECHO
                    |   EXP PARIZQUIERDO exp_operacion PARDERECHO
                    |   FACTORIAL PARIZQUIERDO exp_operacion PARDERECHO
                    |   FLOOR PARIZQUIERDO exp_operacion PARDERECHO
                    |   GCD PARIZQUIERDO exp_operacion COMA exp_operacion PARDERECHO
                    |   LN PARIZQUIERDO exp_operacion PARDERECHO
                    |   LOG PARIZQUIERDO exp_operacion PARDERECHO
                    |   MOD PARIZQUIERDO exp_operacion COMA exp_operacion PARDERECHO
                    |   PI PARIZQUIERDO PARDERECHO
                    |   POWER PARIZQUIERDO exp_operacion COMA exp_operacion PARDERECHO
                    |   RADIANS PARIZQUIERDO exp_operacion PARDERECHO
                    |   ROUND PARIZQUIERDO exp_operacion COMA exp_operacion PARDERECHO
                    |   SIGN PARIZQUIERDO exp_operacion PARDERECHO
                    |   SQRT PARIZQUIERDO exp_operacion PARDERECHO
                    |   WIDTH_BUCKET PARIZQUIERDO exp_operacion COMA exp_operacion COMA exp_operacion COMA exp_operacion PARDERECHO
                    |   TRUNC PARIZQUIERDO exp_operacion PARDERECHO
                    |   RANDOM PARIZQUIERDO exp_operacion PARDERECHO
                    |   SUM PARIZQUIERDO exp_operacion PARDERECHO
                    |   COUNT PARIZQUIERDO exp_operacion PARDERECHO
                    |   COUNT PARIZQUIERDO MULTIPLICACION PARDERECHO
                    |   AVG PARIZQUIERDO exp_operacion PARDERECHO
                    |   MAX PARIZQUIERDO exp_operacion PARDERECHO
                    |   MIN PARIZQUIERDO exp_operacion PARDERECHO'''
                    
def p_funcion_trig(t):
    '''funcion_trig :   ACOS PARIZQUIERDO exp_operacion PARDERECHO
                    |   ACOSD PARIZQUIERDO exp_operacion PARDERECHO
                    |   ASIN PARIZQUIERDO exp_operacion PARDERECHO
                    |   ASIND PARIZQUIERDO exp_operacion PARDERECHO
                    |   ATAN PARIZQUIERDO exp_operacion PARDERECHO
                    |   ATAND PARIZQUIERDO exp_operacion PARDERECHO
                    |   ATAN2 PARIZQUIERDO exp_operacion COMA exp_operacion PARDERECHO
                    |   ATAN2D PARIZQUIERDO exp_operacion COMA exp_operacion PARDERECHO
                    |   COS PARIZQUIERDO exp_operacion PARDERECHO
                    |   COSD PARIZQUIERDO exp_operacion PARDERECHO
                    |   SIN PARIZQUIERDO exp_operacion PARDERECHO
                    |   SIND PARIZQUIERDO exp_operacion PARDERECHO
                    |   TAN PARIZQUIERDO exp_operacion PARDERECHO
                    |   TAND PARIZQUIERDO exp_operacion PARDERECHO
                    |   SINH PARIZQUIERDO exp_operacion PARDERECHO
                    |   COSH PARIZQUIERDO exp_operacion PARDERECHO
                    |   TANH PARIZQUIERDO exp_operacion PARDERECHO
                    |   ASINH PARIZQUIERDO exp_operacion PARDERECHO
                    |   ACOSH PARIZQUIERDO exp_operacion PARDERECHO
                    |   ATANH PARIZQUIERDO exp_operacion PARDERECHO'''

def p_funcion_binstr(t):
    '''funcion_binstr   :   LENGTH PARIZQUIERDO exp_operacion PARDERECHO
                        |   SUBSTRING PARIZQUIERDO exp_operacion COMA exp_operacion COMA exp_operacion PARDERECHO
                        |   TRIM PARIZQUIERDO exp_operacion PARDERECHO
                        |   MD5 PARIZQUIERDO exp_operacion PARDERECHO
                        |   SHA256 PARIZQUIERDO exp_operacion PARDERECHO
                        |   SUBSTR PARIZQUIERDO exp_operacion COMA exp_operacion COMA exp_operacion PARDERECHO
                        |   GET_BYTE PARIZQUIERDO exp_operacion COMA exp_operacion PARDERECHO
                        |   SET_BYTE PARIZQUIERDO exp_operacion COMA exp_operacion PARDERECHO
                        |   CONVERT PARIZQUIERDO exp_operacion AS tipos PARDERECHO
                        |   ENCODE PARIZQUIERDO exp_operacion COMA exp_operacion PARDERECHO
                        |   DECODE PARIZQUIERDO exp_operacion COMA exp_operacion PARDERECHO'''

def p_funcion_exprecion(t):
    '''funcion_exprecion    :   GREATEST PARIZQUIERDO lista_exp PARDERECHO
                            |   LEAST PARIZQUIERDO lista_exp PARDERECHO
                            |   dec_case'''

def p_dec_case(t):
    '''dec_case :   CASE lista_when_case ELSE exp_operacion END
                |   CASE lista_when_case END'''

def p_lista_when_case(t):
    '''lista_when_case  :   lista_when_case WHEN exp_operacion THEN exp_operacion
                        |   WHEN exp_operacion THEN exp_operacion'''

def p_from_query_list(t):
    '''from_query_list  :   from_query_list COMA from_query_element
                        |   from_query_element'''


def p_from_query_element(t):
    '''from_query_element   :   dec_id_from
                            |   subquery AS ID
                            |   subquery ID
                            |   subquery'''

def p_dec_id_from(t):
    '''dec_id_from  :   ID AS ID
                    |   ID ID
                    |   ID'''


def p_lista_condiciones_query(t):
    '''lista_condiciones_query      :   lista_condiciones_query condicion_query
                                    |   condicion_query'''

def p_condicion_query(t):
    '''condicion_query  :   WHERE exp_operacion
                        |   GROUP BY lista_ids
                        |   HAVING exp_operacion
                        |   ORDER BY lista_order_by
                        |   LIMIT condicion_limit OFFSET exp_operacion
                        |   LIMIT condicion_limit'''

def p_condicion_limit(t):
    '''condicion_limit  :   exp_operacion
                        |   ALL'''

def p_lista_ids(t):
    '''lista_ids    :   lista_ids COMA dec_select_columna
                    |   dec_select_columna'''

def p_lista_order_by(t):
    '''lista_order_by   :   lista_order_by COMA elemento_order_by
                        |   elemento_order_by'''

def p_elemento_order_by(t):
    '''elemento_order_by    :   exp_operacion asc_desc condicion_null
                            |   exp_operacion asc_desc'''

def p_asc_desc(t):
    '''asc_desc :   ASC
                |   DESC'''


def p_condicion_null(t):
    '''condicion_null   :   NULLS FIRST
                        |   NULLS LAST'''

def p_pimitivo_id_punto(t):
    'primitivo    :   ID PUNTO ID'

def p_primitivo_funcion(t):
    'primitivo  :   funcion'

def p_subquery(t):
    '''subquery :   PARIZQUIERDO select_query PARDERECHO'''

def p_lista_exp(t):
    '''lista_exp    :   lista_exp COMA exp_operacion
                    |   exp_operacion'''

#--------------------------------------------------------------Tipos de datos------------------------------------------------------------------
def p_tipos(t):
    '''tipos : SMALLINT
             | INTEGER
             | BIGINIT
             | DECIMAL
             | NUMERIC
             | REAL
             | DOUBLE
             | MONEY
             | VARCHAR
             | CHARACTER
             | TEXT
             | TIMESTAMP
             | TIME
             | DATE
             | INTERVAL
             | BOOLEAN
    '''
    nodoType = crear_nodo_general("TYPE",t[1],str(t.lexer.lineno),columna)
    t[0] = nodoType

import ply.yacc as yacc
parser = yacc.yacc()


def parse(input) :
    return parser.parse(input)
