# encoding: utf-8
# Importe de Graphviz
from graphviz import Graph
#importamos la libreria PLY para hacer nuestro analizador lexico.
import ply.lex as lex
#importamos la libreria para llamar al parcer de PLY
import ply.yacc as yacc
#importamos mas librerias que seran utilizadas en el analizador.
#Estas librerias son compatibles con la licencia ya que son librerias propias de python
import re
import codecs
import os
import sys

i = 0

def inc(): 
    global i
    print(str(i))
    i += 1
    return i

# creamos la lista de tokens de nuestro lenguaje.
reservadas = ['SMALLINT','INTEGER','BIGINT','DECIMAL','NUMERIC','REAL','DOBLE','PRECISION','MONEY',
              'VARYING','VARCHAR','CHARACTER','CHAR','TEXT',
              'TIMESTAMP','DATE','TIME','INTERVAL',
              'YEAR','MONTH','DAY','HOUR','MINUTE','SECOND',
              'BOOLEAN',
              'CREATE','TYPE','AS','ENUM','USE',
              'BETWEEN','LIKE','ILIKE','SIMILAR','ON','INTO','TO',
              'IS','ISNULL','NOTNULL',
              'NOT','AND','OR',
              'REPLACE','DATABASE','DATABASES','IF','EXISTS','OWNER','MODE','SELECT','EXIST',
              'ALTER','DROP','RENAME','SHOW','ADD','COLUMN','DELETE','FROM',
              'INSERT','VALUES','UPDATE','SET','GROUP','BY','HAVING','ORDER',
              'RETURNING','USING','DISTINCT',
              'TABLE','CONSTRAINT','NULL','CHECK','UNIQUE',
              'PRIMARY','KEY','REFERENCES','FOREIGN',
              'FALSE','TRUE','UNKNOWN','SYMMETRIC','SUBSTRING',
              'ALL','SOME','ANY','INNER','JOIN','LEFT','RIGTH','FULL','OUTER','NATURAL',
              'ASC','DESC','FIRST','LAST','NULLS',
              'CASE','WHEN','THEN','ELSE','END','LIMIT',
              'UNION','INTERSECT','EXCEPT','OFFSET','GREATEST','LEAST','WHERE','DEFAULT','CASCADE','NO','ACTION',
              'COUNT','SUM','AVG','MAX','MIN',
              'ABS','CBRT','CEIL','CEILING','DEGREES','DIV','EXP','FACTORIAL','FLOOR','GCD','IN','LN','LOG','MOD','PI','POWER','ROUND',
              'ACOS','ACOSD','ASIN','ASIND','ATAN','ATAND','ATAN2','ATAN2D','COS','COSD','COT','COTD','SIN','SIND','TAN','TAND',
              'SINH','COSH','TANH','ASINH','ACOSH','ATANH',
              'DATE_PART','NOW','EXTRACT','CURRENT_TIME','CURRENT_DATE',
              'LENGTH','TRIM','GET_BYTE','MD5','SET_BYTE','SHA256','SUBSTR','CONVERT','ENCODE','DECODE','DOUBLE','INHERITS','SQRT','SIGN',
              'TRUNC','RADIANS','RANDOM','WIDTH_BUCKET'
              ,'BEGIN','DECLARE','PROCEDURE','LANGUAJE','PLPGSSQL','CALL','INDEX','HASH','INCLUDE','COLLATE', 'CONSTANT', 'ALIAS', 'FOR', 'RETURN', 'NEXT', 'ELSIF',
              'ROWTYPE', 'RECORD', 'QUERY', 'STRICT', 'PERFORM', 'VAR', 'EXECUTE'
              ]

tokens = reservadas + ['FECHA_HORA','FECHA','HORA','PUNTO','PUNTO_COMA','CADENASIMPLE','COMA','SIGNO_IGUAL','PARABRE','PARCIERRE','SIGNO_MAS','SIGNO_MENOS',
                       'SIGNO_DIVISION','SIGNO_POR','NUMERO','NUM_DECIMAL','CADENA','ID','LLAVEABRE','LLAVECIERRE','CORCHETEABRE',
                       'CORCHETECIERRE','DOBLE_DOSPUNTOS','SIGNO_POTENCIA','SIGNO_MODULO','MAYORQUE','MENORQUE',
                       'MAYORIGUALQUE','MENORIGUALQUE',
                       'SIGNO_PIPE','SIGNO_DOBLE_PIPE','SIGNO_AND','SIGNO_VIRGULILLA','SIGNO_NUMERAL','SIGNO_DOBLE_MENORQUE','SIGNO_DOBLE_MAYORQUE',
                       'F_HORA','COMILLA','SIGNO_MENORQUE_MAYORQUE','SIGNO_NOT','DOSPUNTOS','DOLAR'
                       
                       ]

# lista para definir las expresiones regulares que conforman los tokens.
t_ignore = '\t\r '

t_SIGNO_DOBLE_PIPE = r'\|\|'
t_SIGNO_PIPE = r'\|'
t_SIGNO_AND = r'\&'
t_SIGNO_VIRGULILLA = r'\~'
t_SIGNO_NUMERAL = r'\#'
t_SIGNO_DOBLE_MENORQUE = r'\<\<'
t_SIGNO_DOBLE_MAYORQUE = r'\>\>'
t_SIGNO_MENORQUE_MAYORQUE = r'\<\>'
t_SIGNO_NOT = r'\!\='

t_PUNTO= r'\.'
t_PUNTO_COMA = r'\;'
t_COMA = r'\,'
t_SIGNO_IGUAL = r'\='
t_PARABRE = r'\('
t_PARCIERRE = r'\)'
t_SIGNO_MAS = r'\+'
t_SIGNO_MENOS = r'\-'
t_SIGNO_DIVISION = r'\/'
t_SIGNO_POR= r'\*'
t_LLAVEABRE = r'\{'
t_LLAVECIERRE = r'\}'
t_CORCHETEABRE = r'\['
t_CORCHETECIERRE = r'\]'
t_DOBLE_DOSPUNTOS= r'\:\:'
t_DOSPUNTOS= r'\:'
t_SIGNO_POTENCIA = r'\^'
t_SIGNO_MODULO = r'\%'
t_MAYORIGUALQUE = r'\>\='
t_MENORIGUALQUE = r'\<\='
t_MAYORQUE = r'\>'
t_MENORQUE = r'\<'
t_COMILLA = r'\''
t_DOLAR= r'\$'


# expresion regular para los id´s
def t_ID (t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        if t.value.upper() in reservadas:
            t.value = t.value.upper()
            t.type = t.value    
        return t

  
# expresion regular para comentario de linea
def t_COMMENT(t):
    r'--.*'
    t.lexer.lineno += 1

# expresion regular para comentario de linea
def t_COMMENT_MULT(t):
    r'/\*(.|\n)?\*/'
    t.lexer.lineno += t.value.count('\n')



def t_NUM_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t
    
# expresion regular para reconocer numeros
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# expresion regular para reconocer formato hora
def t_F_HORA(t):
    r'\'\s*(\d+\s+(hours|HOURS))?(\s*\d+\s+(minutes|MINUTES))?(\s*\d+\s+(seconds|SECONDS))?\s*\''
    t.value = t.value[1:-1]
    return t

# expresion regular para reconocer fecha_hora
def t_FECHA_HORA(t):
    r'\'\d+-\d+-\d+\s\d+:\d+:\d+\''
    t.value = t.value[1:-1]
    from datetime import datetime
    try:
        t.value = datetime.strptime(t.value,'%Y-%m-%d %H:%M:%S')
    except ValueError:
        t.value = datetime(1900,1,1)
    return t
    
def t_FECHA(t):
    r'\'\d\d\d\d-\d\d-\d\d\''
    t.value = t.value[1:-1]
    from datetime import datetime
    try:
        t.value = datetime.strptime(t.value,'%Y-%m-%d')
    except ValueError:
        t.value = datetime(1900,1,1)
    return t

def t_HORA(t):
    r'\'\d+:\d+:\d+\''
    t.value = t.value[1:-1]
    from datetime import datetime
    try:
        t.value = datetime.strptime(t.value,'%H:%M:%S')
    except ValueError:
        t.value = datetime(1900,1,1)
    return t

# expresion regular para reconocer cadenas
def t_CADENA(t):
    r'\".*?\"'
    t.value = str(t.value)
    t.value = t.value[1:-1]
    return t

def t_CADENASIMPLE(t):
    r'\'(\s*|.*?)\''
    t.value = str(t.value)
    return t

# expresion regular para saltos de linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
# expresion regular para reconocer errores
def t_error(t):
    print ("caracter desconocido '%s'" % t.value[0])
    t.lexer.skip(1)

# fin de las expresiones regulares para reconocer nuestro lenguaje.
    
# Construyendo el analizador léxico
# funcion para realizar el analisis lexico de nuestra entrada
def analizarASTLex(texto):    
    analizador = lex.lex()
    analizador.input(texto)# el parametro cadena, es la cadena de texto que va a analizar.

    #ciclo para la lectura caracter por caracter de la cadena de entrada.
    textoreturn = ""
    while True:
        tok = analizador.token()
        if not tok : break
        textoreturn += str(tok) + "\n"
    return textoreturn 

######### inicia el analizador Sintactico ##########

# Asociación de operadores y precedencia
#FALTAN ALGUNOS SIGNOS/PALABRAS RESERVADAS EN LA PRECEDENCIA
precedence = (
    ('left','OR'),
    ('left','AND'),
    ('left','MAYORIGUALQUE','MENORIGUALQUE','MAYORQUE','MENORQUE'),
    ('left','SIGNO_MAS','SIGNO_MENOS'),
    ('left','SIGNO_POR','SIGNO_DIVISION'),
    ('left','SIGNO_POTENCIA','SIGNO_MODULO'),    
    ('right','UMENOS')
    )                   

# Definición de la gramática
def p_inicio(t):
    '''inicio : instrucciones '''
    id = inc()
    t[0] = id

    dot.attr('node', shape='star', style='filled', color='yellow')
    dot.node(str(id), 'inicio')
    dot.attr(color='darkgreen')
    dot.edge(str(id), str(t[1]))

def p_instrucciones_lista(t):
    '''instrucciones : instrucciones instruccion 
                     | instruccion '''
    if len(t) == 3:
        id = inc()
        t[0] = id
        dot.node(str(id), 'instrucciones')
        dot.edge(str(id), str(t[1]))
        dot.edge(str(id), str(t[2]))
    else:
        id = inc()
        t[0] = id
        dot.node(str(id), 'instrucciones')
        dot.edge(str(id), str(t[1]))
    
def p_instrucciones_evaluar(t):
    '''instruccion : ins_use
                   | ins_show
                   | ins_alter
                   | ins_drop
                   | ins_create
                   | ins_insert
                   | ins_select
                   | ins_update
                   | ins_delete
                   | exp
                   | declaracion_funcion
                   | declaracion_copy
                   | declaracion_row
                   | declaracion_record
                   | asignacion
                   | return
                   | declaracion'''
    id = inc()
    t[0] = id
    dot.node(str(id), "instruccion")
    dot.edge(str(id), str(t[1]))
    

def p_instruccion_use(t):
    '''ins_use : USE ID PUNTO_COMA'''
    print('INSTRUCCION USE')
    
    id = inc()
    t[0] = id
    dot.node(str(id), "ins_use")
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), t[1])
    id3 = inc()
    dot.edge(str(id), str(id3)) 
    dot.node(str(id3), t[2])
    id4 = inc()
    dot.edge(str(id), str(id4)) 
    dot.node(str(id4), t[3])
    

def p_instruccion_show(t):
    '''ins_show : SHOW DATABASES PUNTO_COMA'''
    print('INSTRUCCION SHOW')
    id = inc()
    t[0] = id
    dot.node(str(id), "ins_show")
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), t[1])
    id3 = inc()
    dot.edge(str(id), str(id3)) 
    dot.node(str(id3), t[2])
    id4 = inc()
    dot.edge(str(id), str(id4)) 
    dot.node(str(id4), t[3])

def p_instruccion_create(t):
    '''ins_create : CREATE tipo_create'''
    print('INSTRUCCION CREATE')
    id = inc()
    t[0] = id
    dot.node(str(id), "ins_create")
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), t[1])
    dot.edge(str(id), str(t[2])) 

def p_tipo_create(t):
    '''tipo_create : ins_replace DATABASE if_exists ID create_opciones PUNTO_COMA
                   | TABLE ID PARABRE definicion_columna PARCIERRE ins_inherits PUNTO_COMA
                   | TYPE ID AS ENUM PARABRE list_vls PARCIERRE PUNTO_COMA'''
    if t[1] == 'TABLE':
        id = inc()
        t[0] = id
        print(t[3])
        dot.node(str(id), "tipo_create")
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[1]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[2]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[3]))
        id5 = inc()
        dot.edge(str(id), str(id5)) 
        dot.node(str(id5), str(t[4]))
        dot.edge(str(id5), str(t[4])) 
        id6 = inc()
        dot.edge(str(id), str(id6)) 
        dot.node(str(id6), str(t[5]))
        if t[6] != None:
            id7 = inc()
            dot.edge(str(id), str(id7)) 
            dot.node(str(id7), str(t[6]))
            dot.edge(str(id7), str(t[6]))
        id8 = inc()
        dot.edge(str(id), str(id8)) 
        dot.node(str(id8), str(t[7]))
    elif t[1] == 'TYPE':
        id = inc()
        t[0] = id
        print(t[3])
        dot.node(str(id), "tipo_create")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
        id5 = inc()
        dot.edge(str(id), str(id5)) 
        dot.node(str(id5), str(t[5]))
        id6 = inc()
        dot.edge(str(id), str(id6)) 
        dot.node(str(id6), str(t[6]))
        dot.edge(str(id6), str(t[6]))
        id7 = inc()
        dot.edge(str(id), str(id7)) 
        dot.node(str(id7), str(t[7]))
        id8 = inc()
        dot.edge(str(id), str(id8)) 
        dot.node(str(id8), str(t[7]))
    else: 
        id = inc()
        t[0] = id
        dot.node(str(id), "tipo_create")
        if t[1] != None:
            dot.edge(str(id), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), t[2])
        if t[3] != None:
            id3 = inc()
            dot.edge(str(id), str(id3)) 
            dot.node(str(id3), str(t[3]))
            dot.edge(str(id3), str(t[3])) 
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), t[4])
        if t[5] != None:
            id5 = inc()
            dot.edge(str(id), str(id5)) 
            dot.node(str(id5), str(t[5]))
            dot.edge(str(id5), str(t[5])) 
        id6 = inc()
        dot.edge(str(id), str(id6)) 
        dot.node(str(id6), t[6])

def p_ins_inherits(t):
    '''ins_inherits : INHERITS PARABRE ID PARCIERRE
                |  ''' #EPSILON
    if len(t) == 5:
        id = inc()
        t[0] = id
        dot.node(str(id), "ins_inherits")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), t[1])
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), t[2])
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), t[3])
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), t[4])
    else:
        t[0] == None

def p_definicion_columna(t):
    '''definicion_columna : definicion_columna COMA columna 
                          | columna ''' # no se *** si va la coma o no
    if len(t) == 4:
        id = inc()
        t[0] = id
        dot.node(str(id), "definicion_columna")
        dot.edge(str(id), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), t[2])
        dot.edge(str(id), str(t[3]))
    else:
        id = inc()
        t[0] = id
        dot.node(str(id), "definicion_columna")
        dot.edge(str(id), str(t[1]))


def p_columna(t):
    '''columna : ID tipo_dato definicion_valor_defecto ins_constraint
                | primary_key 
                | foreign_key 
                | unique'''
    if len(t) == 6:
        id = inc()
        t[0] = id
        dot.node(str(id), "columna")
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[1]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[2]))
        dot.edge(str(id), str(t[3])) 
        if t[4] != None:
            id4 = inc()
            dot.edge(str(id), str(id4)) 
            dot.node(str(id4), str(t[4]))
            dot.edge(str(id4), str(t[4])) 
        if t[5] != None:
            id5 = inc()
            dot.edge(str(id), str(id5)) 
            dot.node(str(id5), str(t[5]))
            dot.edge(str(id5), str(t[5])) 
    elif len(t) == 5:
        id = inc()
        t[0] = id
        dot.node(str(id), "columna")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        dot.edge(str(id), str(t[2])) 
        if t[3] != None:
            id3 = inc()
            dot.edge(str(id), str(id3)) 
            dot.node(str(id3), str(t[3]))
            dot.edge(str(id3), str(t[3])) 
        if t[4] != None:
            id4 = inc()
            dot.edge(str(id), str(id4)) 
            dot.node(str(id4), str(t[4]))
            dot.edge(str(id4), str(t[4])) 
    elif len(t) == 4:
        id = inc()
        t[0] = id
        dot.node(str(id), "columna")
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[1]))
        if t[2] != None:
            id2 = inc()
            dot.edge(str(id), str(id2)) 
            dot.node(str(id2), str(t[2]))
            dot.edge(str(id2), str(t[2]))  
        if t[3] != None:
            id3 = inc()
            dot.edge(str(id), str(id3)) 
            dot.node(str(id3), str(t[3]))
            dot.edge(str(id3), str(t[3])) 
    else: 
        id = inc()
        t[0] = id
        dot.node(str(id), "columna")
        dot.edge(str(id), str(t[1]))

def p_primary_key(t):
    '''primary_key : PRIMARY KEY PARABRE nombre_columnas PARCIERRE ins_references'''
    id = inc()
    t[0] = id
    dot.node(str(id), "primary_key")
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), str(t[1]))
    id3 = inc()
    dot.edge(str(id), str(id3)) 
    dot.node(str(id3), str(t[2]))
    id4 = inc()
    dot.edge(str(id), str(id4)) 
    dot.node(str(id4), str(t[3]))
    id0 = inc()
    dot.edge(str(id), str(id0)) 
    dot.node(str(id0), str(t[4]))
    dot.edge(str(id0), str(t[4]))
    id5 = inc()
    dot.edge(str(id), str(id5)) 
    dot.node(str(id5), str(t[5]))
    if t[6] != None:
        dot.edge(str(id), str(t[6]))

#FOREIGN KEY PARABRE ID PARCIERRE REFERENCES ID PARABRE ID PARCIERRE ins_references
def p_foreign_key(t):
    '''foreign_key : FOREIGN KEY PARABRE nombre_columnas PARCIERRE REFERENCES ID PARABRE nombre_columnas PARCIERRE ins_references'''
    print('FOREIGN KEY')
    id = inc()
    t[0] = id
    dot.node(str(id), "foreign_key")
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), str(t[1]))
    id3 = inc()
    dot.edge(str(id), str(id3)) 
    dot.node(str(id3), str(t[2]))
    id4 = inc()
    dot.edge(str(id), str(id4)) 
    dot.node(str(id4), str(t[3]))
    id0 = inc()
    dot.edge(str(id), str(id0)) 
    dot.node(str(id0), str(t[4]))
    dot.edge(str(id0), str(t[4]))
    id5 = inc()
    dot.edge(str(id), str(id5)) 
    dot.node(str(id5), str(t[5]))
    id6 = inc()
    dot.edge(str(id), str(id6)) 
    dot.node(str(id6), str(t[6]))
    id7 = inc()
    dot.edge(str(id), str(id7)) 
    dot.node(str(id7), str(t[7]))
    id8 = inc()
    dot.edge(str(id), str(id8)) 
    dot.node(str(id8), str(t[8]))
    id00 = inc()
    dot.edge(str(id), str(id00)) 
    dot.node(str(id00), str(t[9]))
    dot.edge(str(id00), str(t[9]))
    id9 = inc()
    dot.edge(str(id), str(id9)) 
    dot.node(str(id9), str(t[10]))
    if t[11] != None:
        dot.edge(str(id), str(t[11]))

def p_unique(t):
    ''' unique : UNIQUE PARABRE nombre_columnas PARCIERRE  '''
    id = inc()
    t[0] = id
    dot.node(str(id), "unique")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), str(t[2]))
    id3 = inc()
    dot.edge(str(id), str(id3)) 
    dot.node(str(id3), str(t[3]))
    dot.edge(str(id3), str(t[3]))
    id4 = inc()
    dot.edge(str(id), str(id4)) 
    dot.node(str(id4), str(t[4]))
    
def p_nombre_columnas(t):
    '''nombre_columnas : nombre_columnas COMA ID 
                          | ID '''
    if len(t) == 4:
        id = inc()
        t[0] = id
        dot.node(str(id), "nombre_columnas")
        dot.edge(str(id), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), t[2])
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), t[3])
    else:
        id = inc()
        t[0] = id
        dot.node(str(id), "nombre_columnas")
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), t[1])

def p_tipo_dato(t):
    '''tipo_dato : SMALLINT          
                 | BIGINT
                 | NUMERIC
                 | NUMERIC PARABRE NUMERO PARCIERRE
                 | DECIMAL PARABRE NUMERO COMA NUMERO PARCIERRE
                 | INTEGER
                 | REAL
                 | DOUBLE PRECISION
                 | CHAR PARABRE NUMERO PARCIERRE
                 | VARCHAR PARABRE NUMERO PARCIERRE
                 | VARCHAR
                 | CHARACTER PARABRE NUMERO PARCIERRE
                 | TEXT
                 | TIMESTAMP arg_precision
                 | TIME arg_precision
                 | DATE
                 | INTERVAL arg_tipo arg_precision
                 | BOOLEAN
                 | MONEY'''
    # TODO: tipochar falta
    if len(t) == 2:
        id = inc()
        t[0] = id
        dot.node(str(id), "tipo_dato")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
    elif t[1] == 'DOUBLE':
        id = inc()
        t[0] = id
        dot.node(str(id), "tipo_dato")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
    elif len(t) == 5:
        id = inc()
        t[0] = id
        dot.node(str(id), "tipo_dato")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
    elif len(t) == 4:
        id = inc()
        t[0] = id
        dot.node(str(id), "tipo_dato")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        if t[2] != None:
            dot.edge(str(id), str(t[2]))
        if t[3] != None:
            dot.edge(str(id), str(t[3]))
    else: 
        id = inc()
        t[0] = id
        dot.node(str(id), "tipo_dato")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        if t[2] != None:
            dot.edge(str(id), str(t[2]))

def p_arg_precision(t):
    '''arg_precision : PARABRE NUMERO PARCIERRE 
                     | ''' #epsilon
    if len(t) == 4:
        id = inc()
        t[0] = id
        dot.node(str(id), "arg_precision")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
    else:
        t[0] = None

def p_arg_tipo(t):
    '''arg_tipo : MONTH
                | YEAR
                | HOUR
                | MINUTE
                | SECOND            
                | '''
    if len(t) == 2:
        id = inc()
        t[0] = id
        dot.node(str(id), "arg_tipo")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
    else:
        t[0] = None

def p_definicion_valor_defecto(t):
    '''definicion_valor_defecto : DEFAULT tipo_default 
                                | ''' #epsilon
    if len(t) == 3:
        id = inc()
        t[0] = id
        dot.node(str(id), "definicion_valor_defecto")
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[1]))
        dot.edge(str(id), str(t[2])) 
    else:
        t[0] = None

def p_ins_constraint(t):
    '''ins_constraint : ins_constraint constraint restriccion_columna 
            | restriccion_columna
            |''' #epsilon
    if len(t) == 4:
        id = inc()
        t[0] = id
        dot.node(str(id), "ins_constraint")
        dot.edge(str(id), str(t[1])) 
        if t[2] != None:
            dot.edge(str(id), str(t[2])) 
        dot.edge(str(id), str(t[3])) 
    elif len(t) == 2:
        id = inc()
        t[0] = id
        dot.node(str(id), "ins_constraint")
        dot.edge(str(id), str(t[1])) 
    else:
        t[0] = None

def p_constraint(t):
    '''constraint :  CONSTRAINT ID 
            |  '''
    if len(t) == 3:
        id = inc()
        t[0] = id
        dot.node(str(id), "constraint")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
    else: 
        t[0] = None

def p_restriccion_columna(t):
    '''restriccion_columna : NOT NULL 
                           | SET NOT NULL 
                           | PRIMARY KEY 
                           | UNIQUE 
                           | NULL 
                           | NOT NULL PRIMARY KEY 
                           | CHECK PARABRE exp PARCIERRE 
                           | 
                           '''
    if len(t) == 5:
        id = inc()
        t[0] = id
        dot.node(str(id), "restriccion_columna")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        if t[3] == 'PRIMARY':
            id3 = inc()
            dot.edge(str(id), str(id3)) 
            dot.node(str(id3), str(t[3]))
        else: 
            id3 = inc()
            dot.edge(str(id), str(id3)) 
            dot.node(str(id3), str(t[3]))
            dot.edge(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
    elif len(t) == 4:
        id = inc()
        t[0] = id
        dot.node(str(id), "restriccion_columna")
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[1]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[2]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[3]))
    elif len(t) == 2:
        id = inc()
        t[0] = id
        dot.node(str(id), "restriccion_columna")
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[1]))
    elif len(t) == 3:
        id = inc()
        t[0] = id
        dot.node(str(id), "restriccion_columna")
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[1]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[2]))
        id5 = inc()

def p_references(t):
    '''ins_references : ON DELETE accion ins_references
                      | ON UPDATE accion ins_references
                      | '''
    if len(t) == 5:
        id = inc()
        t[0] = id
        dot.node(str(id), "ins_references")
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[1]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[2]))
        dot.edge(str(id), str(t[3]))
        if t[4] != None:
            dot.edge(str(id), str(t[4]))
    else: 
        t[0] = None

def p_accion(t):
    '''accion : CASCADE
              | SET NULL
              | SET DEFAULT
              | NO ACTION'''
    if len(t) == 2:
        id = inc()
        t[0] = id
        dot.node(str(id), "accion")
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[1]))
    else:
        id = inc()
        t[0] = id
        dot.node(str(id), "accion")
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[1]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[2]))

def p_tipo_default(t): #ESTE NO SE SI SON RESERVADAS O LOS VALORES
    '''tipo_default : NUMERO
                    | NUM_DECIMAL
                    | CADENASIMPLE
                    | CADENA
                    | TRUE
                    | FALSE
                    | FECHA
                    | FECHA_HORA
                    | NULL
                    | '''
    id = inc()
    t[0] = id
    dot.node(str(id), t[1])

def p_ins_replace(t): 
    '''ins_replace : OR REPLACE
               | '''#EPSILON
    if len(t) == 3:
        id = inc()
        t[0] = id
        dot.node(str(id), "ins_replace")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
    else:
        t[0] = None

def p_if_exists(t): 
    '''if_exists :  IF NOT EXISTS
                |  IF EXISTS
                | ''' # EPSILON
    if len(t) == 4:
        id = inc()
        t[0] = id
        dot.node(str(id), "if_exists")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
    elif len(t) == 3:
        id = inc()
        t[0] = id
        dot.node(str(id), "if_exists")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
    else:
        t[0] = None

def p_create_opciones(t): 
    '''create_opciones : OWNER SIGNO_IGUAL user_name create_opciones
                       | MODE SIGNO_IGUAL NUMERO create_opciones
                       | '''
    if len(t) == 5:
        id = inc()
        t[0] = id
        dot.node(str(id), "create_opciones")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        if t[1] == 'MODE':
            id3 = inc()
            dot.edge(str(id), str(id3)) 
            dot.node(str(id3), str(t[3]))
        else:
            id3 = inc()
            dot.edge(str(id), str(id3)) 
            dot.node(str(id3), str(t[3]))
            dot.edge(str(id3), str(t[3]))
        if t[4] != None:
            dot.edge(str(id), str(t[4])) 
    else:
        t[0] = None


def p_user_name(t):
    '''user_name : ID
                  | CADENA 
                  | CADENASIMPLE'''
    id = inc()
    t[0] = id
    dot.node(str(id), "user_name")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))

def p_alter(t): 
    '''ins_alter : ALTER tipo_alter ''' 
    print('INSTRUCCION ALTER')
    id = inc()
    t[0] = id
    dot.node(str(id), "ins_alter")
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), t[1])
    dot.edge(str(id), str(t[2]))

def p_tipo_alter(t): 
    '''tipo_alter : DATABASE ID alter_database PUNTO_COMA
                  | TABLE ID alteracion_tabla PUNTO_COMA''' # NO SE SI VAN LOS PUNTO Y COMA
    id = inc()
    t[0] = id
    dot.node(str(id), "tipo_alter")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), t[1])
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), t[2])
    if t[3] != None:
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        dot.edge(str(id3), str(t[3])) 
    id4 = inc()
    dot.edge(str(id), str(id4)) 
    dot.node(str(id4), t[4])

def p_alteracion_tabla(t): 
    '''alteracion_tabla : alteracion_tabla COMA alterar_tabla
                        | alterar_tabla'''
    if len(t) == 4:
        id = inc()
        t[0] = id
        dot.node(str(id), "alteracion_tabla")
        dot.edge(str(id), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), t[2])
        dot.edge(str(id), str(t[3]))
    else:
        id = inc()
        t[0] = id
        dot.node(str(id), "alteracion_tabla")
        dot.edge(str(id), str(t[1]))

def p_alterar_tabla(t): 
    #alter column viene como una lista
    '''alterar_tabla : ADD COLUMN ID tipo_dato
                     | ADD CONSTRAINT ID ins_constraint_dos
                     | ADD ins_constraint_dos
                     | ALTER COLUMN ID TYPE tipo_dato
                     | ALTER COLUMN ID SET NOT NULL
                     | DROP COLUMN ID
                     | DROP CONSTRAINT ID'''
    if len(t) == 3: 
        id = inc()
        t[0] = id
        dot.node(str(id), "alterar_tabla")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        dot.edge(str(id2), str(t[2]))
    elif len(t) == 5: 
        id = inc()
        t[0] = id
        dot.node(str(id), "alterar_tabla")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
        dot.edge(str(id4), str(t[4]))
    elif len(t) == 4: 
        if t[1] == 'DROP':
            id = inc()
            t[0] = id
            dot.node(str(id), "alterar_tabla")
            id2 = inc()
            dot.edge(str(id), str(id2)) 
            dot.node(str(id2), str(t[1]))
            id3 = inc()
            dot.edge(str(id), str(id3)) 
            dot.node(str(id3), str(t[2]))
            id4 = inc()
            dot.edge(str(id), str(id4)) 
            dot.node(str(id4), str(t[3]))
        else:
            id = inc()
            t[0] = id
            dot.node(str(id), "alterar_tabla")
            id2 = inc()
            dot.edge(str(id), str(id2)) 
            dot.node(str(id2), str(t[1]))
            id3 = inc()
            dot.edge(str(id), str(id3)) 
            dot.node(str(id3), str(t[2]))
            id4 = inc()
            dot.edge(str(id), str(id4)) 
            dot.node(str(id4), str(t[3]))
            dot.edge(str(id4), str(t[3]))
    elif len(t) == 7:
        id = inc()
        t[0] = id
        dot.node(str(id), "alterar_tabla")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
        id5 = inc()
        dot.edge(str(id), str(id5)) 
        dot.node(str(id5), str(t[5]))
        id6 = inc()
        dot.edge(str(id), str(id6)) 
        dot.node(str(id6), str(t[6]))
    elif len(t) == 6:
        id = inc()
        t[0] = id
        dot.node(str(id), "alterar_tabla")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
        id5 = inc()
        dot.edge(str(id), str(id5)) 
        dot.node(str(id5), str(t[5]))
        dot.edge(str(id5), str(t[5]))
    else:
        id = inc()
        t[0] = id
        dot.node(str(id), "alterar_tabla")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
        dot.edge(str(id4), str(t[4]))

def p_ins_constraint_dos(t):
    '''ins_constraint_dos : UNIQUE PARABRE ID PARCIERRE
                    | FOREIGN KEY PARABRE ID PARCIERRE REFERENCES fkid PARABRE ID PARCIERRE
                    | CHECK PARABRE exp PARCIERRE 
                    | PRIMARY KEY PARABRE ID PARCIERRE'''
    if len(t) == 5:
        if t[1] == 'UNIQUE':
            id = inc()
            t[0] = id
            dot.node(str(id), "constraint_dos")
            id1 = inc()
            dot.edge(str(id), str(id1)) 
            dot.node(str(id1), str(t[1]))
            id2 = inc()
            dot.edge(str(id), str(id2)) 
            dot.node(str(id2), str(t[2]))
            id3 = inc()
            dot.edge(str(id), str(id3)) 
            dot.node(str(id3), str(t[3]))
            id4 = inc()
            dot.edge(str(id), str(id4)) 
            dot.node(str(id4), str(t[4]))
        else:
            id = inc()
            t[0] = id
            dot.node(str(id), "constraint_dos")
            id1 = inc()
            dot.edge(str(id), str(id1)) 
            dot.node(str(id1), str(t[1]))
            id2 = inc()
            dot.edge(str(id), str(id2)) 
            dot.node(str(id2), str(t[2]))
            id3 = inc()
            dot.edge(str(id), str(id3)) 
            dot.node(str(id3), str(t[3]))
            dot.edge(str(id3), str(t[3]))
            id4 = inc()
            dot.edge(str(id), str(id4)) 
            dot.node(str(id4), str(t[4]))
    if len(t) == 6:
        id = inc()
        t[0] = id
        dot.node(str(id), "constraint_dos")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        dot.edge(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
        id5 = inc()
        dot.edge(str(id), str(id5)) 
        dot.node(str(id5), str(t[5]))
    else: 
        id = inc()
        t[0] = id
        dot.node(str(id), "constraint_dos")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
        id5 = inc()
        dot.edge(str(id), str(id5)) 
        dot.node(str(id5), str(t[5]))
        id6 = inc()
        dot.edge(str(id), str(id6)) 
        dot.node(str(id6), str(t[6]))
        id7 = inc()
        dot.edge(str(id), str(id7)) 
        dot.node(str(id7), str(t[7]))
        dot.edge(str(id7), str(t[7]))
        id8 = inc()
        dot.edge(str(id), str(id8)) 
        dot.node(str(id8), str(t[8]))
        id9 = inc()
        dot.edge(str(id), str(id9)) 
        dot.node(str(id9), str(t[9]))
        id10 = inc()
        dot.edge(str(id), str(id10)) 
        dot.node(str(id10), str(t[10]))

def p_fkid(t):
    '''fkid : ID
            | '''
    if len(t) == 2: 
        id = inc()
        t[0] = id
        dot.node(str(id), "fk_id")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), t[1])
    else:
        t[0] = None

def p_alter_database(t): 
    '''alter_database : RENAME TO ID
                      | OWNER TO ID'''
    id = inc()
    t[0] = id
    dot.node(str(id), "alter_database")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), t[1])
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), t[2])
    id3 = inc()
    dot.edge(str(id), str(id3)) 
    dot.node(str(id3), t[3])

def p_drop(t): 
    '''ins_drop : DROP tipo_drop'''
    print('INSTRUCCION DROP')
    id = inc()
    t[0] = id
    dot.node(str(id), "ins_drop")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), t[1])
    dot.edge(str(id), str(t[2]))

def p_tipo_drop(t): 
    '''tipo_drop : DATABASE if_exists ID PUNTO_COMA
                 | TABLE ID PUNTO_COMA'''
    if len(t) == 5:
        id = inc()
        t[0] = id
        dot.node(str(id), "tipo_drop")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), t[1])
        if t[2] != None:
            id2 = inc()
            dot.edge(str(id), str(id2)) 
            dot.node(str(id2), str(t[2]))
            dot.edge(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), t[3])
    else: 
        print('DROP TABLE')
        id = inc()
        t[0] = id
        dot.node(str(id), "tipo_drop")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), t[1])
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), t[2])
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), t[3])

def p_ins_insert(t):
    '''ins_insert : INSERT INTO ID VALUES PARABRE list_vls PARCIERRE PUNTO_COMA 
                | INSERT INTO ID PARABRE list_id PARCIERRE VALUES PARABRE list_vls PARCIERRE PUNTO_COMA'''
    if len(t) == 9:
        id = inc()
        t[0] = id
        dot.node(str(id), "ins_insert")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
        id5 = inc()
        dot.edge(str(id), str(id5)) 
        dot.node(str(id5), str(t[5]))
        id6 = inc()
        dot.edge(str(id), str(id6)) 
        dot.node(str(id6), str(t[6]))
        dot.edge(str(id6), str(t[6]))
        id7 = inc()
        dot.edge(str(id), str(id7)) 
        dot.node(str(id7), str(t[7]))
        id8 = inc()
        dot.edge(str(id), str(id8)) 
        dot.node(str(id8), str(t[8]))
    else:
        id = inc()
        t[0] = id
        dot.node(str(id), "ins_insert")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
        id5 = inc()
        dot.edge(str(id), str(id5)) 
        dot.node(str(id5), str(t[6]))
        dot.edge(str(id5), str(t[5]))
        id6 = inc()
        dot.edge(str(id), str(id6)) 
        dot.node(str(id6), str(t[6]))
        id7 = inc()
        dot.edge(str(id), str(id7)) 
        dot.node(str(id7), str(t[7]))
        id8 = inc()
        dot.edge(str(id), str(id8)) 
        dot.node(str(id8), str(t[8]))
        id9 = inc()
        dot.edge(str(id), str(id9)) 
        dot.node(str(id9), str(t[9]))
        dot.edge(str(id9), str(t[9]))
        id10 = inc()
        dot.edge(str(id), str(id10)) 
        dot.node(str(id10), str(t[10]))
        id11 = inc()
        dot.edge(str(id), str(id11)) 
        dot.node(str(id11), str(t[11]))

def p_list_id(t):
    '''list_id : list_id COMA ID
               | ID'''
    if len(t) == 4:
        id = inc()
        t[0] = id
        dot.node(str(id), "list_id")
        dot.edge(str(id), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
    else:
        id = inc()
        t[0] = id
        dot.node(str(id), "list_id")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))

def p_list_vls(t):
    '''list_vls : list_vls COMA val_value
                | val_value '''
    if len(t) == 4:
        id = inc()
        t[0] = id
        dot.node(str(id), "list_vls")
        dot.edge(str(id), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        dot.edge(str(id3), str(t[3]))
    else:
        id = inc()
        t[0] = id
        dot.node(str(id), "list_vls")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        dot.edge(str(id1), str(t[1]))

def p_val_value(t):
    '''val_value : CADENA
                |   CADENASIMPLE
                |   NUMERO
                |   NUM_DECIMAL
                |   FECHA_HORA
                |   TRUE
                |   FALSE 
                |   NULL
                |   F_HORA
                |   FECHA
                |   HORA'''
    id = inc()
    t[0] = id
    dot.node(str(id), "val_value")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))

def p_val_value_func(t):
    '''val_value : functions'''
    id = inc()
    t[0] = id
    dot.node(str(id), "val_value")
    dot.edge(str(id), str(t[1]))


def p_ins_select(t):
    '''ins_select :      ins_select UNION option_all ins_select PUNTO_COMA
                    |    ins_select INTERSECT option_all ins_select PUNTO_COMA
                    |    ins_select EXCEPT option_all ins_select PUNTO_COMA
                    |    SELECT arg_distict colum_list FROM table_list arg_where arg_having arg_group_by arg_order_by arg_limit arg_offset PUNTO_COMA
                    |    SELECT functions as_id PUNTO_COMA'''
    if len(t) == 5:
        id = inc()
        t[0] = id
        dot.node(str(id), "ins_select")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        if t[2] != None:
            id2 = inc()
            dot.edge(str(id), str(id2)) 
            dot.node(str(id2), str(t[2]))
            dot.edge(str(id2), str(t[2]))
        if t[3] != None:
            id3 = inc()
            dot.edge(str(id), str(id3)) 
            dot.node(str(id3), str(t[3]))
            dot.edge(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))  
    elif len(t) == 6:
        id = inc()
        t[0] = id
        dot.node(str(id), "ins_select")
        if t[1] != None:
            dot.edge(str(id), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        if t[3] != None:
            id3 = inc()
            dot.edge(str(id), str(id3)) 
            dot.node(str(id3), str(t[3]))
            dot.edge(str(id3), str(t[3]))
        if t[4] != None:
            id4 = inc()
            dot.edge(str(id), str(id4)) 
            dot.node(str(id4), str(t[4]))
            dot.edge(str(id4), str(t[4]))
        id5 = inc()
        dot.edge(str(id), str(id5)) 
        dot.node(str(id5), str(t[5]))
    else: 
        id = inc()
        t[0] = id
        dot.node(str(id), "ins_select")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        if t[2] != None:
            id2 = inc()
            dot.edge(str(id), str(id2)) 
            dot.node(str(id2), str(t[2]))
            dot.edge(str(id2), str(t[2]))
        if t[3] != None:
            id3 = inc()
            dot.edge(str(id), str(id3)) 
            dot.node(str(id3), str(t[3]))
            dot.edge(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
        if t[5] != None:
            id5 = inc()
            dot.edge(str(id), str(id5)) 
            dot.node(str(id5), str(t[5]))
            dot.edge(str(id5), str(t[5]))
        if t[6] != None:
            id6 = inc()
            dot.edge(str(id), str(id6)) 
            dot.node(str(id6), str(t[6]))
            dot.edge(str(id6), str(t[6]))
        if t[7] != None:
            id7 = inc()
            dot.edge(str(id), str(id7)) 
            dot.node(str(id7), str(t[7]))
            dot.edge(str(id7), str(t[7]))
        if t[8] != None:
            id8 = inc()
            dot.edge(str(id), str(id8)) 
            dot.node(str(id8), str(t[8]))
            dot.edge(str(id8), str(t[8]))
        if t[9] != None:
            id9 = inc()
            dot.edge(str(id), str(id9)) 
            dot.node(str(id9), str(t[9]))
            dot.edge(str(id9), str(t[9]))
        if t[10] != None:
            id10 = inc()
            dot.edge(str(id), str(id10)) 
            dot.node(str(id10), str(t[10]))
            dot.edge(str(id10), str(t[10]))
        if t[11] != None:
            id11 = inc()
            dot.edge(str(id), str(id11)) 
            dot.node(str(id11), str(t[11]))
            dot.edge(str(id11), str(t[11]))

def p_arg_having(t):
    '''arg_having    :   HAVING PARABRE exp PARCIERRE
                    |    '''
    if len(t) == 5:
        id = inc()
        t[0] = id
        dot.node(str(id), "having")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        dot.edge(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
    else:
        t[0] = None

def p_option_all(t):
    '''option_all   :   ALL
                    |    '''
    if len(t) == 3: 
        id = inc()
        t[0] = id
        dot.node(str(id), "option_all")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), t[1])
    else:
        t[0] = None

def p_arg_distict(t):
    '''arg_distict :    DISTINCT
                    |    '''
    if len(t) == 2: 
        id = inc()
        t[0] = id
        dot.node(str(id), "arg_distict")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
    else:
        t[0] = None

def p_colum_list(t):
    '''colum_list   :   s_list
                    |   SIGNO_POR '''
    if t[1] == '*':
        id = inc()
        t[0] = id
        dot.node(str(id), "colum_list")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), t[1])
    else:
        id = inc()
        t[0] = id
        dot.node(str(id), "colum_list")
        dot.edge(str(id), str(t[1]))

def p_s_list(t):
    '''s_list   :   s_list COMA columns as_id
                |   columns as_id'''
    if len(t) == 5:
        id = inc()
        t[0] = id
        dot.node(str(id), "s_list")
        dot.edge(str(id), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        dot.edge(str(id), str(t[3]))
        if t[4] != None:
            dot.edge(str(id), str(t[4]))
    else: 
        id = inc()
        t[0] = id
        dot.node(str(id), "s_list")
        dot.edge(str(id), str(t[1]))
        if t[2] != None:
            dot.edge(str(id), str(t[2]))

def p_columns(t):
    '''columns   : ID dot_table
                    |   aggregates
                    |   functions '''
    if len(t) == 3:
        id = inc()
        t[0] = id
        dot.node(str(id), "columns")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        if t[2] != None:
            dot.edge(str(id), str(t[2]))
    else: 
        id = inc()
        t[0] = id
        dot.node(str(id), "columns")
        if t[1] != None:
            dot.edge(str(id), str(t[1])) 


def p_dot_table(t):
    '''dot_table    :   PUNTO ID
                    |    '''
    if len(t) == 3: 
        id = inc()
        t[0] = id
        dot.node(str(id), "dot_table")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), t[1])
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), t[1])
    else:
        t[0] = None

def p_as_id(t): #  REVISRA CADENA Y AS CADENA
    '''as_id    :       AS ID
                    |   AS CADENA
                    |   AS CADENASIMPLE
                    |   CADENA
                    |   ID
                    |   CADENASIMPLE
                    |   '''
    print('AS ID')
    if len(t) == 3: 
        id = inc()
        t[0] = id
        dot.node(str(id), "as_id")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
    elif len(t) == 2: 
        id = inc()
        t[0] = id
        dot.node(str(id), "as_id")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
    else:
        t[0] = None

def p_aggregates(t):
    '''aggregates   :   COUNT PARABRE param PARCIERRE
                    |   SUM PARABRE param PARCIERRE
                    |   AVG PARABRE param PARCIERRE
                    |   MAX PARABRE param PARCIERRE
                    |   MIN PARABRE param PARCIERRE ''' 
    id = inc()
    t[0] = id
    dot.node(str(id), "aggregates")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), str(t[2]))
    id3 = inc()
    dot.edge(str(id), str(id3)) 
    dot.node(str(id3), str(t[3]))
    dot.edge(str(id3), str(t[3]))
    id4 = inc()
    dot.edge(str(id), str(id4)) 
    dot.node(str(id4), str(t[4]))

def p_functions(t):
    '''functions    :   math
                    |   trig
                    |   string_func
                    |   time_func '''
    # TODO: CORREGIR GRAMATICA <STRING_FUNC>
    id = inc()
    t[0] = id
    dot.node(str(id), "functions")
    dot.edge(str(id), str(t[1])) 


def p_math(t):
    '''math :    ABS PARABRE op_numero PARCIERRE
                |   CBRT PARABRE op_numero PARCIERRE
                |   CEIL PARABRE op_numero PARCIERRE
                |   CEILING PARABRE op_numero PARCIERRE
                |   DEGREES PARABRE op_numero PARCIERRE
                |   DIV PARABRE op_numero COMA op_numero PARCIERRE
                |   EXP PARABRE op_numero PARCIERRE
                |   FACTORIAL PARABRE op_numero PARCIERRE
                |   FLOOR PARABRE op_numero PARCIERRE
                |   GCD PARABRE op_numero COMA op_numero PARCIERRE
                |   LN PARABRE op_numero PARCIERRE
                |   LOG PARABRE op_numero PARCIERRE
                |   MOD PARABRE op_numero COMA op_numero PARCIERRE
                |   PI PARABRE  PARCIERRE
                |   POWER PARABRE op_numero COMA op_numero PARCIERRE 
                |   ROUND PARABRE op_numero arg_num PARCIERRE 
                |   SQRT PARABRE op_numero PARCIERRE 
                |   SIGN PARABRE op_numero PARCIERRE
                |   TRUNC PARABRE op_numero PARCIERRE
                |   RANDOM PARABRE PARCIERRE
                |   RADIANS PARABRE op_numero PARCIERRE
                |   WIDTH_BUCKET PARABRE op_numero COMA op_numero COMA op_numero COMA op_numero PARCIERRE'''
    if len(t) == 5:
        id = inc()
        t[0] = id
        dot.node(str(id), "math")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        dot.edge(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
    elif len(t) == 6:
        id = inc()
        t[0] = id
        dot.node(str(id), "math")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        dot.edge(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
        dot.edge(str(id4), str(t[4]))
        id5 = inc()
        dot.edge(str(id), str(id5)) 
        dot.node(str(id5), str(t[5]))
    elif len(t) == 7:
        id = inc()
        t[0] = id
        dot.node(str(id), "math")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        dot.edge(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
        id5 = inc()
        dot.edge(str(id), str(id5)) 
        dot.node(str(id5), str(t[5]))
        dot.edge(str(id5), str(t[5]))
        id6 = inc()
        dot.edge(str(id), str(id6)) 
        dot.node(str(id6), str(t[6]))
    elif len(t) == 4:
        id = inc()
        t[0] = id
        dot.node(str(id), "math")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
    else: 
        id = inc()
        t[0] = id
        dot.node(str(id), "math")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        dot.edge(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
        id5 = inc()
        dot.edge(str(id), str(id5)) 
        dot.node(str(id5), str(t[5]))
        dot.edge(str(id5), str(t[5]))
        id6 = inc()
        dot.edge(str(id), str(id6)) 
        dot.node(str(id6), str(t[6]))
        id7 = inc()
        dot.edge(str(id), str(id7)) 
        dot.node(str(id7), str(t[7]))
        dot.edge(str(id7), str(t[7]))
        id8 = inc()
        dot.edge(str(id), str(id8)) 
        dot.node(str(id8), str(t[8]))
        id9 = inc()
        dot.edge(str(id), str(id9)) 
        dot.node(str(id9), str(t[9]))
        dot.edge(str(id9), str(t[9]))
        id10 = inc()
        dot.edge(str(id), str(id10)) 
        dot.node(str(id10), str(t[10]))


def p_trig(t):
    '''trig :   ACOS PARABRE op_numero PARCIERRE
                |   ACOSD PARABRE op_numero PARCIERRE
                |   ASIN PARABRE op_numero PARCIERRE
                |   ASIND PARABRE op_numero PARCIERRE
                |   ATAN PARABRE op_numero PARCIERRE
                |   ATAND PARABRE op_numero PARCIERRE
                |   ATAN2 PARABRE op_numero COMA op_numero PARCIERRE
                |   ATAN2D PARABRE op_numero COMA op_numero PARCIERRE
                |   COS PARABRE op_numero PARCIERRE
                |   COSD PARABRE op_numero PARCIERRE
                |   COT PARABRE op_numero PARCIERRE
                |   COTD PARABRE op_numero PARCIERRE
                |   SIN PARABRE op_numero PARCIERRE
                |   SIND PARABRE op_numero PARCIERRE
                |   TAN PARABRE op_numero PARCIERRE
                |   TAND PARABRE op_numero PARCIERRE
                |   SINH PARABRE op_numero PARCIERRE
                |   COSH PARABRE op_numero PARCIERRE
                |   TANH PARABRE op_numero PARCIERRE
                |   ASINH PARABRE op_numero PARCIERRE
                |   ACOSH PARABRE op_numero PARCIERRE
                |   ATANH PARABRE op_numero PARCIERRE  '''
    if len(t) == 5:
        id = inc()
        t[0] = id
        dot.node(str(id), "trig")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        dot.edge(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
    else:
        id = inc()
        t[0] = id
        dot.node(str(id), "trig")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        dot.edge(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
        id5 = inc()
        dot.edge(str(id), str(id5)) 
        dot.node(str(id5), str(t[5]))
        dot.edge(str(id5), str(t[5]))
        id6 = inc()
        dot.edge(str(id), str(id6)) 
        dot.node(str(id6), str(t[6]))

def p_op_numero(t):
    '''  op_numero : NUMERO 
                | NUM_DECIMAL
                | SIGNO_MENOS NUMERO %prec UMENOS
                | SIGNO_MENOS NUM_DECIMAL %prec UMENOS'''
    if len(t) == 2:
        id = inc()
        t[0] = id
        dot.node(str(id), "op_numero")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
    else:
        id = inc()
        t[0] = id
        dot.node(str(id), "op_numero")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))

def p_string_func(t):   #TODO: CORREGIR GRAMÁTICA
    '''string_func  :   LENGTH PARABRE s_param PARCIERRE
                    |   TRIM PARABRE s_param PARCIERRE
                    |   MD5 PARABRE s_param PARCIERRE
                    |   SHA256 PARABRE s_param PARCIERRE
                    |   SUBSTRING PARABRE s_param COMA NUMERO COMA NUMERO PARCIERRE 
                    |   SUBSTRING PARABRE s_param COMA s_param COMA CADENA PARCIERRE
                    |   SET_BYTE PARABRE COMA NUMERO COMA NUMERO s_param PARCIERRE
                    |   CONVERT PARABRE tipo_dato COMA ID dot_table PARCIERRE
                    |   SUBSTR PARABRE s_param COMA NUMERO COMA NUMERO PARCIERRE
                    |   ENCODE PARABRE s_param COMA s_param PARCIERRE
                    |   DECODE PARABRE s_param COMA s_param PARCIERRE 
                    |   GET_BYTE PARABRE s_param COMA NUMERO PARCIERRE'''
    if len(t) == 9:
        if t[1] == 'SET_BYTE':
            id = inc()
            t[0] = id
            dot.node(str(id), "string_func")
            id1 = inc()
            dot.edge(str(id), str(id1)) 
            dot.node(str(id1), str(t[1]))
            id2 = inc()
            dot.edge(str(id), str(id2)) 
            dot.node(str(id2), str(t[2]))
            id3 = inc()
            dot.edge(str(id), str(id3)) 
            dot.node(str(id3), str(t[3]))
            id4 = inc()
            dot.edge(str(id), str(id4)) 
            dot.node(str(id4), str(t[4]))
            id5 = inc()
            dot.edge(str(id), str(id5)) 
            dot.node(str(id5), str(t[5]))
            id6 = inc()
            dot.edge(str(id), str(id6)) 
            dot.node(str(id6), str(t[6]))
            id7 = inc()
            dot.edge(str(id), str(id7)) 
            dot.node(str(id7), str(t[7]))
            dot.edge(str(id7), str(t[7]))
            id8 = inc()
            dot.edge(str(id), str(id8)) 
            dot.node(str(id8), str(t[8]))
        elif t[1] == 'SUBSTR':
            id = inc()
            t[0] = id
            dot.node(str(id), "string_func")
            id1 = inc()
            dot.edge(str(id), str(id1)) 
            dot.node(str(id1), str(t[1]))
            id2 = inc()
            dot.edge(str(id), str(id2)) 
            dot.node(str(id2), str(t[2]))
            id3 = inc()
            dot.edge(str(id), str(id3)) 
            dot.node(str(id3), str(t[3]))
            dot.edge(str(id3), str(t[3]))
            id4 = inc()
            dot.edge(str(id), str(id4)) 
            dot.node(str(id4), str(t[4]))
            id5 = inc()
            dot.edge(str(id), str(id5)) 
            dot.node(str(id5), str(t[5]))
            id6 = inc()
            dot.edge(str(id), str(id6)) 
            dot.node(str(id6), str(t[6]))
            id7 = inc()
            dot.edge(str(id), str(id7)) 
            dot.node(str(id7), str(t[7]))
            id8 = inc()
            dot.edge(str(id), str(id8)) 
            dot.node(str(id8), str(t[8]))
        else: 
            id = inc()
            t[0] = id
            dot.node(str(id), "string_func")
            id1 = inc()
            dot.edge(str(id), str(id1)) 
            dot.node(str(id1), str(t[1]))
            id2 = inc()
            dot.edge(str(id), str(id2)) 
            dot.node(str(id2), str(t[2]))
            id3 = inc()
            dot.edge(str(id), str(id3)) 
            dot.node(str(id3), str(t[3]))
            dot.edge(str(id3), str(t[3]))
            id4 = inc()
            dot.edge(str(id), str(id4)) 
            dot.node(str(id4), str(t[4]))
            id5 = inc()
            dot.edge(str(id), str(id5)) 
            dot.node(str(id5), str(t[5]))
            id6 = inc()
            dot.edge(str(id), str(id6)) 
            dot.node(str(id6), str(t[6]))
            id7 = inc()
            dot.edge(str(id), str(id7)) 
            dot.node(str(id7), str(t[7]))
            id8 = inc()
            dot.edge(str(id), str(id8)) 
            dot.node(str(id8), str(t[8]))
    elif len(t) == 5: #CHECK
        id = inc()
        t[0] = id
        dot.node(str(id), "string_func")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        dot.edge(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
    elif len(t) == 7:
        if t[5] == 'NUMERO':
            id = inc()
            t[0] = id
            dot.node(str(id), "string_func")
            id1 = inc()
            dot.edge(str(id), str(id1)) 
            dot.node(str(id1), str(t[1]))
            id2 = inc()
            dot.edge(str(id), str(id2)) 
            dot.node(str(id2), str(t[2]))
            id3 = inc()
            dot.edge(str(id), str(id3)) 
            dot.node(str(id3), str(t[3]))
            id4 = inc()
            dot.edge(str(id), str(id4)) 
            dot.node(str(id4), str(t[4]))
            id5 = inc()
            dot.edge(str(id), str(id5)) 
            dot.node(str(id5), str(t[5]))
            id6 = inc()
            dot.edge(str(id), str(id6)) 
            dot.node(str(id6), str(t[6]))
        else:
            id = inc()
            t[0] = id
            dot.node(str(id), "string_func")
            id1 = inc()
            dot.edge(str(id), str(id1)) 
            dot.node(str(id1), str(t[1]))
            id2 = inc()
            dot.edge(str(id), str(id2)) 
            dot.node(str(id2), str(t[2]))
            id3 = inc()
            dot.edge(str(id), str(id3)) 
            dot.node(str(id3), str(t[3]))
            id4 = inc()
            dot.edge(str(id), str(id4)) 
            dot.node(str(id4), str(t[4]))
            id5 = inc()
            dot.edge(str(id), str(id5)) 
            dot.node(str(id5), str(t[5]))
            dot.edge(str(id5), str(t[5]))
            id6 = inc()
            dot.edge(str(id), str(id6)) 
            dot.node(str(id6), str(t[6]))
    elif len(t) == 8:
        id = inc()
        t[0] = id
        dot.node(str(id), "string_func")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        dot.edge(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
        id5 = inc()
        dot.edge(str(id), str(id5)) 
        dot.node(str(id5), str(t[5]))
        id6 = inc()
        dot.edge(str(id), str(id6)) 
        dot.node(str(id6), str(t[6]))
        dot.edge(str(id6), str(t[6]))
        id7 = inc()
        dot.edge(str(id), str(id7)) 
        dot.node(str(id7), str(t[7]))

def p_s_param(t):
    '''s_param  :   s_param string_op s_param
                |   CADENA
                |   CADENASIMPLE
                |   NUMERO'''
    if len(t) == 4:
        id = inc()
        t[0] = id
        dot.node(str(id), "s_param")
        dot.edge(str(id), str(t[1])) 
        dot.edge(str(id), str(t[2])) 
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[3]))
        dot.edge(str(id1), str(t[3]))
    else: 
        id = inc()
        t[0] = id
        dot.node(str(id), "s_param")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))

def p_string_op(t):
    '''string_op    :   SIGNO_PIPE
                    |   SIGNO_DOBLE_PIPE
                    |   SIGNO_AND
                    |   SIGNO_VIRGULILLA
                    |   SIGNO_NUMERAL
                    |   SIGNO_DOBLE_MENORQUE
                    |   SIGNO_DOBLE_MAYORQUE'''
    id = inc()
    t[0] = id
    dot.node(str(id), "string_op")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))

def p_time_func(t):
    '''time_func    :   DATE_PART PARABRE  h_m_s  COMA INTERVAL F_HORA PARCIERRE 
                    |   NOW PARABRE PARCIERRE
                    |   EXTRACT PARABRE reserv_time  FROM TIMESTAMP FECHA_HORA PARCIERRE
                    |   TIMESTAMP CADENASIMPLE
                    |   CURRENT_TIME
                    |   CURRENT_DATE'''
    if len(t) == 3:
        id = inc()
        t[0] = id
        dot.node(str(id), "time_func")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
    elif len(t) == 2:
        id = inc()
        t[0] = id
        dot.node(str(id), "time_func")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
    elif len(t) == 4:
        id = inc()
        t[0] = id
        dot.node(str(id), "time_func")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
    elif len(t) == 8:
        id = inc()
        t[0] = id
        dot.node(str(id), "time_func")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        dot.edge(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
        id5 = inc()
        dot.edge(str(id), str(id5)) 
        dot.node(str(id5), str(t[5]))
        id6 = inc()
        dot.edge(str(id), str(id6)) 
        dot.node(str(id6), str(t[6]))
    else:
        id = inc()
        t[0] = id
        dot.node(str(id), "time_func")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
        dot.edge(str(id4), str(t[4]))
        id5 = inc()
        dot.edge(str(id), str(id5)) 
        dot.node(str(id5), str(t[5]))
        id6 = inc()
        dot.edge(str(id), str(id6)) 
        dot.node(str(id6), str(t[6]))
        id7 = inc()
        dot.edge(str(id), str(id7)) 
        dot.node(str(id7), str(t[7]))
        id8 = inc()
        dot.edge(str(id), str(id8)) 
        dot.node(str(id8), str(t[8]))
        id9 = inc()
        dot.edge(str(id), str(id9)) 
        dot.node(str(id9), str(t[9]))

def p_reserv_time(t):
    '''reserv_time  :   h_m_s 
                    |   YEAR
                    |   MONTH
                    |   DAY'''
    if t[1] == 'YEAR' or t[1] == 'MONTH' or t[1] == 'DAY':
        id = inc()
        t[0] = id
        dot.node(str(id), "reserv_time")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
    else: 
        id = inc()
        t[0] = id
        dot.node(str(id), "reserv_time")
        dot.edge(str(id), str(t[1]))

def p_h_m_s(t):
    '''h_m_s    :   HOUR
                    |   MINUTE
                    |   SECOND 
                    |   CADENASIMPLE'''
    id = inc()
    t[0] = id
    dot.node(str(id), "h_m_s")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))

def p_param(t):
    '''param    :   ID dot_table
                |   SIGNO_POR '''
    if len(t) == 3: 
        id = inc()
        t[0] = id
        dot.node(str(id), "param")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        dot.edge(str(id2), str(t[2]))
    else:
        id = inc()
        t[0] = id
        dot.node(str(id), "param")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))

def p_table_list(t):
    '''table_list   :   table_list COMA ID as_id
                    |   ID as_id'''
    if len(t) == 5: 
        id = inc()
        t[0] = id
        dot.node(str(id), "table_list")
        dot.edge(str(id), str(t[1])) 
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[2]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[3]))
        if t[4] != None:
            id4 = inc()
            dot.edge(str(id), str(id4)) 
            dot.node(str(id4), str(t[4]))
            dot.edge(str(id4), str(t[4]))
    else:
        id = inc()
        t[0] = id
        dot.node(str(id), "table_list")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        if t[2] != None:
            id2 = inc()
            dot.edge(str(id), str(id2)) 
            dot.node(str(id2), str(t[2]))
            dot.edge(str(id2), str(t[2]))

def p_arg_where(t):
    '''arg_where    :   WHERE PARABRE exp PARCIERRE
                    |    '''
    if len(t) == 3: 
        id = inc()
        t[0] = id
        dot.node(str(id), "arg_where")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        dot.edge(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
    else:
        t[0] = None

def p_exp(t):
    '''exp  : exp SIGNO_MAS exp
            | exp SIGNO_MENOS exp 
            | exp SIGNO_POR exp 
            | exp SIGNO_DIVISION exp 
            | exp SIGNO_MODULO exp 
            | exp SIGNO_POTENCIA exp 
            | exp OR exp 
            | exp AND exp 
            | exp MENORQUE exp 
            | exp MAYORQUE exp 
            | exp MAYORIGUALQUE exp 
            | exp MENORIGUALQUE exp 
            | exp SIGNO_IGUAL exp
            | exp SIGNO_MENORQUE_MAYORQUE exp
            | exp SIGNO_NOT exp 
            | arg_pattern
            | sub_consulta
            | NOT exp
            | EXISTS PARABRE ins_select PARCIERRE 
            | NOT EXISTS PARABRE ins_select PARCIERRE 
            | data
            | predicates
            | aggregates
            | functions
            | arg_case
            | arg_greatest
            | arg_least 
            | val_value'''
# values -> list_vls
    if len(t) == 5:
        id = inc()
        t[0] = id
        dot.node(str(id), "exp")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
    if len(t) == 4:
        id = inc()
        t[0] = id
        dot.node(str(id), "exp")
        dot.edge(str(id), str(t[1]))
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[2]))
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[3]))
        dot.edge(str(id1), str(t[3]))
    elif len(t) == 3:
        id = inc()
        t[0] = id
        dot.node(str(id), "exp")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        dot.edge(str(id), str(t[2]))
    else:
        id = inc()
        t[0] = id
        dot.node(str(id), "exp")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        dot.edge(str(id1), str(t[1]))

def p_arg_greatest(t):
    '''arg_greatest  : GREATEST PARABRE exp_list PARCIERRE''' 
    id = inc()
    t[0] = id
    dot.node(str(id), "arg_greatest")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), str(t[2]))
    id3 = inc()
    dot.edge(str(id), str(id3)) 
    dot.node(str(id3), str(t[3]))
    dot.edge(str(id3), str(t[3]))
    id4 = inc()
    dot.edge(str(id), str(id4)) 
    dot.node(str(id4), str(t[4]))

def p_arg_least(t):
    '''arg_least  : LEAST PARABRE exp_list PARCIERRE''' 
    id = inc()
    t[0] = id
    dot.node(str(id), "arg_least")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), str(t[2]))
    id3 = inc()
    dot.edge(str(id), str(id3)) 
    dot.node(str(id3), str(t[3]))
    dot.edge(str(id3), str(t[3]))
    id4 = inc()
    dot.edge(str(id), str(id4)) 
    dot.node(str(id4), str(t[4]))

def p_exp_list(t):
    '''exp_list  : exp_list COMA exp
                 | exp'''
    if len(t) == 4:
        id = inc()
        t[0] = id
        dot.node(str(id), "exp_list")
        dot.edge(str(id), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        dot.edge(str(id), str(t[3]))
    else:
        id = inc()
        t[0] = id
        dot.node(str(id), "exp_list")
        dot.edge(str(id), str(t[1]))

def p_case(t):
    '''arg_case  : CASE arg_when arg_else END''' 
    id = inc()
    t[0] = id
    dot.node(str(id), "arg_case")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), str(t[2]))
    dot.edge(str(id2), str(t[2]))
    id3 = inc()
    dot.edge(str(id), str(id3)) 
    dot.node(str(id3), str(t[3]))
    dot.edge(str(id3), str(t[3]))
    id4 = inc()
    dot.edge(str(id), str(id4)) 
    dot.node(str(id4), str(t[4]))

def p_arg_when(t):
    '''arg_when  : arg_when WHEN exp THEN exp
                 | WHEN exp THEN exp''' 
    if len(t) == 6:
        id = inc()
        t[0] = id
        dot.node(str(id), "arg_when")
        dot.edge(str(id), str(t[1])) 
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[2]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[3]))
        dot.edge(str(id2), str(t[3]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[4]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[5]))
        dot.edge(str(id4), str(t[5])) 
    else:
        id = inc()
        t[0] = id
        dot.node(str(id), "arg_when")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        dot.edge(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
        dot.edge(str(id4), str(t[4])) 
                
def p_arg_else(t):
    '''arg_else :  ELSE exp
                 | ''' # epsilon
    if len(t) == 3: 
        id = inc()
        t[0] = id
        dot.node(str(id), "arg_else")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        dot.edge(str(id2), str(t[2]))
    else:
        t[0] = None

def p_predicates(t):
    '''predicates  : data BETWEEN list_vls AND list_vls
                   | data NOT BETWEEN list_vls AND list_vls
                   | data BETWEEN SYMMETRIC list_vls AND list_vls
                   | data NOT BETWEEN SYMMETRIC list_vls AND list_vls
                   | data IS DISTINCT FROM list_vls
                   | data IS NOT DISTINCT FROM list_vls
                   | data IS NULL 
                   | data ISNULL
                   | data NOTNULL
                   | data IS TRUE
                   | data IS NOT TRUE
                   | data IS FALSE
                   | data IS NOT FALSE
                   | data IS UNKNOWN
                   | data IS NOT UNKNOWN'''
    if len(t) == 3:
        id = inc()
        t[0] = id
        dot.node(str(id), "predicates")
        dot.edge(str(id), str(t[1])) 
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[2]))
    if len(t) == 4:
        id = inc()
        t[0] = id
        dot.node(str(id), "predicates")
        dot.edge(str(id), str(t[1])) 
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[2]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[3]))
    elif len(t) == 5:
        id = inc()
        t[0] = id
        dot.node(str(id), "predicates")
        dot.edge(str(id), str(t[1])) 
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[2]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
    elif len(t) == 6:
        if t[2] == 'BETWEEN':
            id = inc()
            t[0] = id
            dot.node(str(id), "predicates")
            dot.edge(str(id), str(t[1])) 
            id1 = inc()
            dot.edge(str(id), str(id1)) 
            dot.node(str(id1), str(t[2]))
            id2 = inc()
            dot.edge(str(id), str(id2)) 
            dot.node(str(id2), str(t[3]))
            id4 = inc()
            dot.edge(str(id), str(id4)) 
            dot.node(str(id4), str(t[4]))
            id5 = inc()
            dot.edge(str(id), str(id5)) 
            dot.node(str(id5), str(t[5]))
            dot.edge(str(id5), str(t[5]))
        else: 
            id = inc()
            t[0] = id
            dot.node(str(id), "predicates")
            dot.edge(str(id), str(t[1])) 
            id1 = inc()
            dot.edge(str(id), str(id1)) 
            dot.node(str(id1), str(t[2]))
            id2 = inc()
            dot.edge(str(id), str(id2)) 
            dot.node(str(id2), str(t[3]))
            dot.edge(str(id2), str(t[3]))
            id4 = inc()
            dot.edge(str(id), str(id4)) 
            dot.node(str(id4), str(t[4]))
            id5 = inc()
            dot.edge(str(id), str(id5)) 
            dot.node(str(id5), str(t[5]))
            dot.edge(str(id5), str(t[5]))
    elif len(t) == 7:                       # PRODUCCION 7
        if t[2] == 'IS':
            id = inc()
            t[0] = id
            dot.node(str(id), "predicates")
            dot.edge(str(id), str(t[1])) 
            id1 = inc()
            dot.edge(str(id), str(id1)) 
            dot.node(str(id1), str(t[2]))
            id2 = inc()
            dot.edge(str(id), str(id2)) 
            dot.node(str(id2), str(t[3]))
            id4 = inc()
            dot.edge(str(id), str(id4)) 
            dot.node(str(id4), str(t[4]))
            id5 = inc()
            dot.edge(str(id), str(id5)) 
            dot.node(str(id5), str(t[5]))
            id6 = inc()
            dot.edge(str(id), str(id6)) 
            dot.node(str(id6), str(t[6]))
            dot.edge(str(id6), str(t[6]))
        else: 
            id = inc()
            t[0] = id
            dot.node(str(id), "predicates")
            dot.edge(str(id), str(t[1])) 
            id1 = inc()
            dot.edge(str(id), str(id1)) 
            dot.node(str(id1), str(t[2]))
            id2 = inc()
            dot.edge(str(id), str(id2)) 
            dot.node(str(id2), str(t[3]))
            id4 = inc()
            dot.edge(str(id), str(id4)) 
            dot.node(str(id4), str(t[4]))
            dot.edge(str(id4), str(t[4]))
            id5 = inc()
            dot.edge(str(id), str(id5)) 
            dot.node(str(id5), str(t[5]))
            id6 = inc()
            dot.edge(str(id), str(id6)) 
            dot.node(str(id6), str(t[6]))
            dot.edge(str(id6), str(t[6]))
    else:
        id = inc()
        t[0] = id
        dot.node(str(id), "predicates")
        dot.edge(str(id), str(t[1])) 
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[2]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[3]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[4]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[5]))
        dot.edge(str(id4), str(t[5]))
        id5 = inc()
        dot.edge(str(id), str(id5)) 
        dot.node(str(id5), str(t[6]))
        id6 = inc()
        dot.edge(str(id), str(id6)) 
        dot.node(str(id6), str(t[7]))
        dot.edge(str(id6), str(t[7]))

def p_data(t):
    '''data  : ID table_at''' 
    id = inc()
    t[0] = id
    dot.node(str(id), "data")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))
    if t[2] != None:
        id2 = inc()
        dot.edge(str(id), str(t[2]))

def p_table_at(t):
    '''table_at  : PUNTO ID
                 | ''' #epsilon
    if len(t) == 3: 
        id = inc()
        t[0] = id
        dot.node(str(id), "table_at")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
    else:
        t[0] = None
            
def p_sub_consulta(t):
    '''sub_consulta   : PARABRE ins_select  PARCIERRE''' 
    id = inc()
    t[0] = id
    dot.node(str(id), "sub_consulta")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), str(t[2]))
    dot.edge(str(id2), str(t[2]))
    id3 = inc()
    dot.edge(str(id), str(id3)) 
    dot.node(str(id3), str(t[3]))

def p_arg_pattern(t):
    '''arg_pattern   : data LIKE CADENA   
                     | data NOT LIKE CADENA '''
    if len(t) == 4:
        id = inc()
        t[0] = id
        dot.node(str(id), "arg_pattern")
        dot.edge(str(id), str(t[1]))
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[2]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[3]))
    else:
        id = inc()
        t[0] = id
        dot.node(str(id), "arg_pattern")
        dot.edge(str(id), str(t[1]))
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[2]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[3]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[4]))

def p_arg_group_by(t):
    '''arg_group_by    :   GROUP BY g_list
                       |  ''' #epsilon
    if len(t) == 4:
        id = inc()
        t[0] = id
        dot.node(str(id), "arg_group_by")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        dot.edge(str(id3), str(t[3]))
    else:
        t[0] = None

def p_g_list(t):
    '''g_list    : g_list COMA g_item
                 | g_item '''
    if len(t) == 4:
        id = inc()
        t[0] = id
        dot.node(str(id), "g_list")
        dot.edge(str(id), str(t[1]))
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[2]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[3]))
        dot.edge(str(id2), str(t[3]))
    else:
        id = inc()
        t[0] = id
        dot.node(str(id), "g_list")
        dot.edge(str(id), str(t[1]))

def p_g_item(t):
    '''g_item    : ID g_refitem''' 
    id = inc()
    t[0] = id
    dot.node(str(id), "g_item")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))
    if t[2] != None:
        dot.edge(str(id), str(t[2]))

def p_g_refitem(t):
    '''g_refitem  : PUNTO ID
                  | ''' #epsilon
    if len(t) == 3: 
        id = inc()
        t[0] = id
        dot.node(str(id), "g_refitem")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), t[1])
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), t[2])
    else:
        t[0] = None

def p_arg_order_by(t):
    '''arg_order_by    :   ORDER BY o_list
                       |  ''' #epsilon
    if len(t) == 4: 
        id = inc()
        t[0] = id
        dot.node(str(id), "arg_order_by")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        dot.edge(str(id3), str(t[3]))
    else:
        t[0] = None

def p_o_list(t):
    '''o_list    : o_list COMA o_item
                 | o_item ''' 
    if len(t) == 4: 
        id = inc()
        t[0] = id
        dot.node(str(id), "o_list")
        dot.node(str(id), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        dot.edge(str(id3), str(t[3]))
    else:
        id = inc()
        t[0] = id
        dot.node(str(id), "o_list")
        dot.node(str(id), str(t[1]))

def p_o_item(t):
    '''o_item : ID o_refitem ad arg_nulls'''
    id = inc()
    t[0] = id
    dot.node(str(id), "o_item")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[2]))
    if t[2] != None:
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        dot.edge(str(id2), str(t[2]))
    if t[3] != None:
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        dot.edge(str(id3), str(t[3]))
    if t[4] != None:
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
        dot.edge(str(id4), str(t[4]))

def p_arg_num(t):
    ''' arg_num : COMA NUMERO 
                |'''
    if len(t) == 3: 
        id = inc()
        t[0] = id
        dot.node(str(id), "arg_num")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), t[1])
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), t[2])
    else:
        t[0] = None

def p_o_refitem(t):
    '''o_refitem  : PUNTO ID
                  | ''' #epsilon
    if len(t) == 3: 
        id = inc()
        t[0] = id
        dot.node(str(id), "o_refitem")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), t[1])
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), t[2])
    else:
        t[0] = None

def p_ad(t):
    '''ad : ASC
          | DESC
          | ''' #epsilon
    if len(t) == 2: 
        id = inc()
        t[0] = id
        dot.node(str(id), "ad")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), t[1])
    else:
        t[0] = None

def p_arg_nulls(t):
    '''arg_nulls : NULLS arg_fl
                 | ''' #epsilon
    if len(t) == 3: 
        id = inc()
        t[0] = id
        dot.node(str(id), "arg_nulls")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), t[1])
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        dot.edge(str(id2), str(t[2]))
    else:
        t[0] = None

def p_arg_fl(t):
    '''arg_fl : FIRST
              | LAST''' #epsilon
    id = inc()
    t[0] = id
    dot.node(str(id), "arg_fl")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), t[1])

def p_arg_limit(t):
    '''arg_limit   :  LIMIT option_limit
                   |  ''' #epsilon
    if len(t) == 3: 
        id = inc()
        t[0] = id
        dot.node(str(id), "arg_limit")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        dot.edge(str(id2), str(t[2]))
    else:
        t[0] = None

def p_option_limit(t):
    '''option_limit   : NUMERO
                      | ALL ''' 
    id = inc()
    t[0] = id
    dot.node(str(id), "option_limit")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), t[1])

def p_arg_offset(t):
    '''arg_offset   : OFFSET NUMERO 
                    |  ''' #epsilon
    if len(t) == 3: 
        id = inc()
        t[0] = id
        dot.node(str(id), "arg_offset")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), t[1])
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), t[2])
    else:
        t[0] = None


def p_ins_update(t):
    '''ins_update   : UPDATE ID SET asign_list WHERE exp PUNTO_COMA '''
    id = inc()
    t[0] = id
    dot.node(str(id), "ins_update")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), str(t[2]))
    id3 = inc()
    dot.edge(str(id), str(id3))
    dot.node(str(id3), str(t[3]))
    id4 = inc()
    dot.edge(str(id), str(id4))
    dot.node(str(id4), str(t[4]))
    dot.edge(str(id4), str(t[4]))
    id5 = inc()
    dot.edge(str(id), str(id5))
    dot.node(str(id5), str(t[5]))
    id6 = inc()
    dot.edge(str(id), str(id6))
    dot.node(str(id6), str(t[6]))
    dot.edge(str(id6), str(t[6]))
    id7 = inc()
    dot.edge(str(id), str(id7))
    dot.node(str(id7), str(t[7]))

def p_ins_asign_list(t):
    '''asign_list  : asign_list COMA ID SIGNO_IGUAL exp
                   | ID SIGNO_IGUAL exp'''
    if len(t) == 6:
        id = inc()
        t[0] = id
        dot.node(str(id), "asign_list")
        dot.edge(str(id), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        id4 = inc()
        dot.edge(str(id), str(id4)) 
        dot.node(str(id4), str(t[4]))
        id5 = inc()
        dot.edge(str(id), str(id5)) 
        dot.node(str(id5), str(t[5]))
        dot.edge(str(id5), str(t[5]))
    else:
        id = inc()
        t[0] = id
        dot.node(str(id), "asign_list")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        id3 = inc()
        dot.edge(str(id), str(id3)) 
        dot.node(str(id3), str(t[3]))
        dot.edge(str(id3), str(t[3]))

def p_ins_delete(t):
    '''ins_delete   : DELETE FROM ID WHERE exp PUNTO_COMA'''
    id = inc()
    t[0] = id
    dot.node(str(id), "ins_delete")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), str(t[2]))
    id3 = inc()
    dot.edge(str(id), str(id3)) 
    dot.node(str(id3), str(t[3]))
    id4 = inc()
    dot.edge(str(id), str(id4)) 
    dot.node(str(id4), str(t[4]))
    id5 = inc()
    dot.edge(str(id), str(id5))
    dot.node(str(id4), str(t[5]))
    dot.edge(str(id4), str(t[5]))
    id6 = inc()
    dot.edge(str(id), str(id6)) 
    dot.node(str(id6), str(t[6]))

def p_declaracion(t):
    '''declaracion  : ID constante tipo_dato not_null declaracion_default PUNTO_COMA'''
    id = inc()
    t[0] = id
    dot.node(str(id), "declaracion")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))
    if t[2] != None:
        dot.edge(str(id), str(t[2]))
    if t[3] != None:
        dot.edge(str(id), str(t[3]))
    if t[4] != None:
        dot.edge(str(id), str(t[4]))
    if t[5] != None:
        dot.edge(str(id), str(t[5]))
    id6 = inc()
    dot.edge(str(id), str(id6)) 
    dot.node(str(id6), str(t[6]))

def p_constante(t):
    '''constante  : CONSTANT'''
    id = inc()
    t[0] = id
    dot.node(str(id), "constante")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))

def p_constante_null(t):
    '''constante  : '''
    t[0] = None

def p_not_null(t):
    '''not_null  : NOT NULL'''
    id = inc()
    t[0] = id
    dot.node(str(id), "not_null")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), str(t[2]))

def p_not_null_null(t):
    '''not_null : '''
    t[0] = None

def p_declaracion_default(t):
    '''declaracion_default  : DEFAULT exp'''
    id = inc()
    t[0] = id
    dot.node(str(id), "declaracion_default")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))
    dot.edge(str(id), str(t[2]))

def p_declaracion_default_dos(t):
    '''declaracion_default  : SIGNO_IGUAL exp '''
    id = inc()
    t[0] = id
    dot.node(str(id), "declaracion_default")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))
    dot.edge(str(id), str(t[2]))

def p_declaracion_default_signo(t):
    '''declaracion_default  : DOSPUNTOS SIGNO_IGUAL  exp'''
    id = inc()
    t[0] = id
    dot.node(str(id), "declaracion_default")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), str(t[2]))
    dot.edge(str(id), str(t[3]))

def p_declaracion_default_null(t):
    '''declaracion_default  : '''
    t[0] = None

def p_declaracionf_funcion(t):
    '''declaracion_funcion : ID ALIAS FOR DOLAR NUMERO PUNTO_COMA'''
    id = inc()
    t[0] = id
    dot.node(str(id), "declaracion_funcion")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), str(t[2]))
    id3 = inc()
    dot.edge(str(id), str(id3)) 
    dot.node(str(id3), str(t[3]))
    id4 = inc()
    dot.edge(str(id), str(id4)) 
    dot.node(str(id4), str(t[4]))
    id5 = inc()
    dot.edge(str(id), str(id5)) 
    dot.node(str(id5), str(t[5]))
    id6 = inc()
    dot.edge(str(id), str(id6)) 
    dot.node(str(id6), str(t[6]))

def p_declaracionf_funcion_rename(t):
    '''declaracion_funcion : ID ALIAS FOR ID PUNTO_COMA'''
    id = inc()
    t[0] = id
    dot.node(str(id), "declaracion_funcion")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), str(t[2]))
    id3 = inc()
    dot.edge(str(id), str(id3)) 
    dot.node(str(id3), str(t[3]))
    id4 = inc()
    dot.edge(str(id), str(id4)) 
    dot.node(str(id4), str(t[4]))
    id5 = inc()
    dot.edge(str(id), str(id5)) 
    dot.node(str(id5), str(t[5]))

def p_declaracionc_copy(t):
    '''declaracion_copy : ID ID PUNTO ID SIGNO_MODULO TYPE PUNTO_COMA'''
    id = inc()
    t[0] = id
    dot.node(str(id), "declaracion_copy")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), str(t[2]))
    id3 = inc()
    dot.edge(str(id), str(id3)) 
    dot.node(str(id3), str(t[3]))
    id4 = inc()
    dot.edge(str(id), str(id4)) 
    dot.node(str(id4), str(t[4]))
    id5 = inc()
    dot.edge(str(id), str(id5)) 
    dot.node(str(id5), str(t[5]))
    id6 = inc()
    dot.edge(str(id), str(id6)) 
    dot.node(str(id6), str(t[6]))
    id7 = inc()
    dot.edge(str(id), str(id7)) 
    dot.node(str(id7), str(t[7]))

def p_declaracionr_row(t):
    '''declaracion_row : ID ID SIGNO_MODULO ROWTYPE PUNTO_COMA'''
    id = inc()
    t[0] = id
    dot.node(str(id), "declaracion_row")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), str(t[2]))
    id3 = inc()
    dot.edge(str(id), str(id3)) 
    dot.node(str(id3), str(t[3]))
    id4 = inc()
    dot.edge(str(id), str(id4)) 
    dot.node(str(id4), str(t[4]))
    id5 = inc()
    dot.edge(str(id), str(id5)) 
    dot.node(str(id5), str(t[5]))

def p_declaracionre_record(t):
    '''declaracion_record : ID RECORD PUNTO_COMA'''
    id = inc()
    t[0] = id
    dot.node(str(id), "declaracion_record")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), str(t[2]))
    id3 = inc()
    dot.edge(str(id), str(id3)) 
    dot.node(str(id3), str(t[3]))

def p_asignacion(t):
    '''asignacion : ID referencia_id SIGNO_IGUAL exp PUNTO_COMA
                | ID referencia_id SIGNO_IGUAL ins_select PUNTO_COMA'''
    id = inc()
    t[0] = id
    dot.node(str(id), "asignacion")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))
    if t[2] != None:
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        dot.edge(str(id2), str(t[2]))
    id3 = inc()
    dot.edge(str(id), str(id3)) 
    dot.node(str(id3), str(t[3]))
    id4 = inc()
    dot.edge(str(id), str(id4)) 
    dot.node(str(id4), str(t[4]))
    dot.edge(str(id4), str(t[4]))
    id5 = inc()
    dot.edge(str(id), str(id5)) 
    dot.node(str(id5), str(t[5]))

def p_asignacion_dos(t):
    '''asignacion : ID referencia_id DOSPUNTOS SIGNO_IGUAL exp PUNTO_COMA
                | ID referencia_id DOSPUNTOS SIGNO_IGUAL ins_select PUNTO_COMA'''
    id = inc()
    t[0] = id
    dot.node(str(id), "asignacion")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))
    if t[2] != None:
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
        dot.edge(str(id2), str(t[2]))
    id3 = inc()
    dot.edge(str(id), str(id3)) 
    dot.node(str(id3), str(t[3]))
    id4 = inc()
    dot.edge(str(id), str(id4)) 
    dot.node(str(id4), str(t[4]))
    id5 = inc()
    dot.edge(str(id), str(id5)) 
    dot.node(str(id5), str(t[5]))
    dot.edge(str(id5), str(t[5]))
    id6 = inc()
    dot.edge(str(id), str(id6)) 
    dot.node(str(id6), str(t[6]))

def p_referencia_id(t):
    '''referencia_id : PUNTO ID
                | '''
    if len(t) == 3:
        id = inc()
        t[0] = id
        dot.node(str(id), "return")
        id1 = inc()
        dot.edge(str(id), str(id1)) 
        dot.node(str(id1), str(t[1]))
        id2 = inc()
        dot.edge(str(id), str(id2)) 
        dot.node(str(id2), str(t[2]))
    else: 
        t[0] = None
        
def p_return(t):
    '''return : RETURN exp PUNTO_COMA'''
    id = inc()
    t[0] = id
    dot.node(str(id), "return")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), str(t[2]))
    dot.edge(str(id2), str(t[2]))
    id3 = inc()
    dot.edge(str(id), str(id3)) 
    dot.node(str(id3), str(t[3]))

def p_return_next(t):
    '''return : RETURN NEXT exp PUNTO_COMA'''
    id = inc()
    t[0] = id
    dot.node(str(id), "return")
    id1 = inc()
    dot.edge(str(id), str(id1)) 
    dot.node(str(id1), str(t[1]))
    id2 = inc()
    dot.edge(str(id), str(id2)) 
    dot.node(str(id2), str(t[2]))
    id3 = inc()
    dot.edge(str(id), str(id3)) 
    dot.node(str(id3), str(t[3]))
    dot.edge(str(id3), str(t[3]))
    id4 = inc()
    dot.edge(str(id), str(id4)) 
    dot.node(str(id4), str(t[4]))

def p_error(t):
    print("Error sintáctico en '%s'" % t.value)

dot = Graph()
def analizarASTSin(texto):    
    parser = yacc.yacc()
    while True:
        i = 0
        dot.attr(splines='false')
        dot.node_attr.update(shape='circle')
        dot.node_attr.update(color='darkgreen')
        parser.parse(texto)
        dot.view()
        break