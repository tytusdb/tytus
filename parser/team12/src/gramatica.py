#Definicion de tokens

#Definicion de palabras reservadas del lenguaje
keywords = {
'ABS' : 'ABS',
'ACOS' : 'ACOS',
'ACOSD' : 'ACOSD',
'ACOSH' : 'ACOSH',
'ADD' : 'ADD',
'ALL' : 'ALL',
'ALTER' : 'ALTER',
'AND' : 'AND',
'ANY' : 'ANY',
'AS' : 'AS',
'ASC' : 'ASC',
'ASIN' : 'ASIN',
'ASIND' : 'ASIND',
'ASINH' : 'ASINH',
'ATAN' : 'ATAN',
'ATAN2' : 'ATAN2',
'ATAN2D' : 'ATAN2D',
'ATAND' : 'ATAND',
'ATANH' : 'ATANH',
'AVG' : 'AVG',
'BETWEEN' : 'BETWEEN',
'BIGINT' : 'BIGINT',
'BOOLEAN' : 'BOOLEAN',
'BY' : 'BY',
'CASE' : 'CASE',
'CBRT' : 'CBRT',
'CEIL' : 'CEIL',
'CEILING' : 'CEILING',
'CHAR' : 'CHAR',
'CHARACTER' : 'CHARACTER',
'CHECK' : 'CHECK',
'COLUMN' : 'COLUMN',
'CONSTRAINT' : 'CONSTRAINT',
'CONVERT' : 'CONVERT',
'COS' : 'COS',
'COSD' : 'COSD',
'COSH' : 'COSH',
'COT' : 'COT',
'COTD' : 'COTD',
'COUNT' : 'COUNT',
'CREATE' : 'CREATE',
'CURRENT' : 'CURRENT',
'CURRENT_DATE' : 'CURRENT_DATE',
'CURRENT_TIME' : 'CURRENT_TIME',
'CURRENT_USER' : 'CURRENT_USER',
'DATABASE' : 'DATABASE',
'DATE_PART' : 'DATE_PART',
'DAY' : 'DAY',
'DECIMAL' : 'DECIMAL',
'DECODE' : 'DECODE',
'DEFAULT' : 'DEFAULT',
'DEGREES' : 'DEGREES',
'DELETE' : 'DELETE',
'DESC' : 'DESC',
'DIV' : 'DIV',
'DOUBLE' : 'DOUBLE',
'DROP' : 'DROP',
'ELSE' : 'ELSE',
'ENCODE' : 'ENCODE',
'END' : 'END',
'ENUM' : 'ENUM',
'ESCAPE' : 'ESCAPE',
'EXCEPT' : 'EXCEPT',
'EXISTS' : 'EXISTS',
'EXP' : 'EXP',
'EXTRACT' : 'EXTRACT',
'FACTORIAL' : 'FACTORIAL',
'FALSE' : 'FALSE',
'FIRST' : 'FIRST',
'FLOAT' : 'FLOAT',
'FLOOR' : 'FLOOR',
'FOREIGN' : 'FOREIGN',
'FROM' : 'FROM',
'FULL' : 'FULL',
'GCD' : 'GCD',
'GET_BYTE' : 'GET_BYTE',
'GREATEST' : 'GREATEST',
'GROUP' : 'GROUP',
'HAVING' : 'HAVING',
'HOUR' : 'HOUR',
'IF' : 'IF',
'ILIKE' : 'ILIKE',
'IN' : 'IN',
'INHERITS' : 'INHERITS',
'INNER' : 'INNER',
'INSERT' : 'INSERT',
'INT' : 'INT',
'INTEGER' : 'INTEGER',
'INTERSECT' : 'INTERSECT',
'INTERVAL' : 'INTERVAL',
'INTO' : 'INTO',
'IS' : 'IS',
'JOIN' : 'JOIN',
'KEY' : 'KEY',
'LAST' : 'LAST',
'LCM' : 'LCM',
'LEAST' : 'LEAST',
'LEFT' : 'LEFT',
'LENGTH' : 'LENGTH',
'LIKE' : 'LIKE',
'LIMIT' : 'LIMIT',
'LN' : 'LN',
'LOG' : 'LOG',
'LOG10' : 'LOG10',
'MAX' : 'MAX',
'MD5' : 'MD5',
'MIN' : 'MIN',
'MIN_SCALE' : 'MIN_SCALE',
'MINUTE' : 'MINUTE',
'MOD' : 'MOD',
'MODE' : 'MODE',
'MONEY' : 'MONEY',
'MONTH' : 'MONTH',
'NATURAL' : 'NATURAL',
'NOT' : 'NOT',
'NOTNULL' : 'NOTNULL',
'NOW' : 'NOW',
'NULL' : 'NULL',
'NULLS' : 'NULLS',
'NUMERIC' : 'NUMERIC',
'OF' : 'OF',
'OFFSET' : 'OFFSET',
'ON' : 'ON',
'ONLY' : 'ONLY',
'ORDER' : 'ORDER',
'OUTER' : 'OUTER',
'OWNER' : 'OWNER',
'PI' : 'PI',
'POWER' : 'POWER',
'PRECISION' : 'PRECISION',
'PRIMARY' : 'PRIMARY',
'RADIANS' : 'RADIANS',
'RANDOM' : 'RANDOM',
'REAL' : 'REAL',
'REFERENCES' : 'REFERENCES',
'RENAME' : 'RENAME',
'RETURNING' : 'RETURNING',
'RIGHT' : 'RIGHT',
'ROUND' : 'ROUND',
'SCALE' : 'SCALE',
'SECOND' : 'SECOND',
'SELECT' : 'SELECT',
'SESSION_USER' : 'SESSION_USER',
'SET' : 'SET',
'SET_BYTE' : 'SET_BYTE',
'SETSEED' : 'SETSEED',
'SHA256' : 'SHA256',
'SIGN' : 'SIGN',
'SIMILAR' : 'SIMILAR',
'SIN' : 'SIN',
'SIND' : 'SIND',
'SINH' : 'SINH',
'SMALLINT' : 'SMALLINT',
'SOME' : 'SOME',
'SQRT' : 'SQRT',
'SUBSTR' : 'SUBSTR',
'SUBSTRING' : 'SUBSTRING',
'SUM' : 'SUM',
'SYMMETRIC' : 'SYMMETRIC',
'TABLE' : 'TABLE',
'TAN' : 'TAN',
'TAND' : 'TAND',
'TANH' : 'TANH',
'TEXT' : 'TEXT',
'THEN' : 'THEN',
'TIME' : 'TIME',
'TIMESTAMP' : 'TIMESTAMP',
'TO' : 'TO',
'TRIM' : 'TRIM',
'TRIM_SCALE' : 'TRIM_SCALE',
'TRUC' : 'TRUC',
'TRUE' : 'TRUE',
'TYPE' : 'TYPE',
'UNION' : 'UNION',
'UNIQUE' : 'UNIQUE',
'UNKNOWN' : 'UNKNOWN',
'UPDATE' : 'UPDATE',
'USING' : 'USING',
'VALUES' : 'VALUES',
'VARCHAR' : 'VARCHAR',
'VARYING' : 'VARYING',
'WHEN' : 'WHEN',
'WHERE' : 'WHERE',
'WIDTH_BUCKET' : 'WIDTH_BUCKET',
'WITH' : 'WITH',
'WITHOUT' : 'WITHOUT',
'YEAR' : 'YEAR',
'ZONE' : 'ZONE'
}

#Definicion de tokens del lenguaje
#Se agregan las keywords
tokens = [
    'ASTERISCO',
    'COMA',
    'DIFERENTEQUE',
    'IGUAL',
    'MAYORIGUAL',
    'PARENTESISIZQ',
    'PARENTESISDER',
    'PUNTOYCOMA',
    'IDENTIFICADOR',
    'CADENA',
    'ENTERO',
    'NUMDECIMAL',
    'MENORQUE',
    'MAYORQUE',
    'MENORIGUAL',
] + list(keywords.values())

#Definicion de patrones de los tokens

t_ASTERISCO = r'\*'
t_COMA = r','


t_DIFERENTEQUE = r'<>'

t_IGUAL = r'='

t_MAYORIGUAL = r'>='
t_MAYORQUE = r'>'
t_MENORIGUAL = r'<='
t_MENORQUE = r'<'

t_PARENTESISDER = r'\)'
t_PARENTESISIZQ = r'\('



t_PUNTOYCOMA = r';'


def t_NUMDECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Decimal demasiado extenso %d", t.value)
        t.value = 0
    return t

def t_IDENTIFICADOR(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = keywords.get(t.value.upper(),'IDENTIFICADOR') 
     print(t.type)   # Check for reserved words
     return t    

def t_CADENA(t):
    r'\'.*?\''
    #Supresion de comillas
    t.value = t.value[1:-1]
    return t 

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

#Defincion de los errores lexicos
def t_error(t):
    print("Carácter no válido'%s'" % t.value[0])
    t.lexer.skip(1)

#Caracteres a ser ignorados por el lenguaje
t_ignore = " \t"

#Generación del lexer
import ply.lex as lex
lexer = lex.lex()



#Análisis sintáctico
def p_instrucciones_lista(t):
    '''instrucciones    : instruccion instrucciones
                        | instruccion '''
    print("Jalo",t[1])

def p_instruccion(t):
    '''instruccion : IDENTIFICADOR
                    | COSD
                    | ENTERO
                    | NUMDECIMAL
                    | CADENA '''
    t[0] = t[1]


import ply.yacc as yacc
parser = yacc.yacc()
parser.parse("COSD nombre1 12.5 'HOLA'")                        