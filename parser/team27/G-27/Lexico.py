# ======================================================================
#                          IMPORTES Y PLY
# ======================================================================
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
# ======================================================================
#                          ENTORNO Y PRINCIPAL
# ======================================================================
from execution.symbol.environment import Environment
from execution.main import Main

# ======================================================================
#                          INSTRUCCIONES DDL
# ======================================================================
from execution.querie.use import Use
from execution.querie.create import Create
from execution.querie.show_database import Show_Database
from execution.querie.drop_database import Drop_Database
from execution.querie.alter_database import Alter_Database
from execution.querie.add_column import Add_Column
from execution.querie.add_constraint import Add_Constraint
from execution.querie.alter_column import Alter_Column
from execution.querie.alter_table import Alter_Table
from execution.querie.case import Case
from execution.querie.create_t import Create_Table
from execution.querie.create_type import Create_Type
from execution.querie.drop_column import Drop_Column
from execution.querie.drop_constraint import Drop_Constraint
from execution.querie.drop_database import Drop_Database
from execution.querie.drop_t import Drop_Table

# ======================================================================
#                          INSTRUCCIONES DML
# ======================================================================
from execution.querie.insert import Insert
from execution.querie.update import Update
from execution.querie.select_ import Select
from execution.querie.delete import Delete

# ======================================================================
#                             EXPRESIONES
# ======================================================================
from execution.expression.arithmetic import Arithmetic
from execution.expression.greatest import Greatest
from execution.expression.id import Id
from execution.expression.least import Least
from execution.expression.literal import Literal
from execution.expression.logic import Logic
from execution.expression.predicates import Predicates
from execution.expression.relational import Relational
from execution.expression.stringop import Stringop

# ======================================================================
#                        FUNCIONES MATEMATICAS
# ======================================================================
from execution.function.mathematical.abs import Abs
from execution.function.mathematical.cbrt import Cbrt
from execution.function.mathematical.ceil import Ceil
from execution.function.mathematical.ceiling import Ceiling
from execution.function.mathematical.degrees import Degrees
from execution.function.mathematical.div import Div
from execution.function.mathematical.exp import Exp
from execution.function.mathematical.factorial import Factorial
from execution.function.mathematical.floor import Floor
from execution.function.mathematical.gcd import Gcd
from execution.function.mathematical.ln import Ln
from execution.function.mathematical.log import Log
from execution.function.mathematical.pi import Pi
from execution.function.mathematical.power import Power
from execution.function.mathematical.radians import Radians
from execution.function.mathematical.random import Randomic
from execution.function.mathematical.round import Round
from execution.function.mathematical.sign import Sign
from execution.function.mathematical.sqrt import Sqrt
from execution.function.mathematical.trunc import Trunc

# ======================================================================
#                       FUNCIONES TRIGONOMETRICAS
# ======================================================================
from execution.function.trigonometric.acos import Acos
from execution.function.trigonometric.acosd import Acosd
from execution.function.trigonometric.acosh import Acosh
from execution.function.trigonometric.asin import Asin
from execution.function.trigonometric.asind import Asind
from execution.function.trigonometric.asinh import Asinh
from execution.function.trigonometric.atan import Atan
from execution.function.trigonometric.atan2 import Atan2
from execution.function.trigonometric.atan2d import Atan2d
from execution.function.trigonometric.atand import Atand
from execution.function.trigonometric.atanh import Atanh
from execution.function.trigonometric.cos import Cos
from execution.function.trigonometric.cosd import Cosd
from execution.function.trigonometric.cosh import Cosh
from execution.function.trigonometric.cot import Cot
from execution.function.trigonometric.cotd import Cotd
from execution.function.trigonometric.sin import Sin
from execution.function.trigonometric.sind import Sind
from execution.function.trigonometric.sinh import Sinh
from execution.function.trigonometric.tan import Tan
from execution.function.trigonometric.tand import Tand
from execution.function.trigonometric.tanh import Tanh

# ======================================================================
#                       FUNCIONES DE AGREGADO
# ======================================================================
from execution.function.agreggates.avg import Avg
from execution.function.agreggates.count import Count
from execution.function.agreggates.max import Max
from execution.function.agreggates.min import Min
from execution.function.agreggates.sum import Sum

# ======================================================================
#                       FUNCIONES BINARIAS
# ======================================================================
from execution.function.binary.get_byte import Get_Byte
from execution.function.binary.length import Length
from execution.function.binary.md5 import Md5
from execution.function.binary.set_byte import Set_Byte
from execution.function.binary.sha256 import Sha256
from execution.function.binary.substr import Substr
from execution.function.binary.substring import Substring
from execution.function.binary.trim import Trim

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
              'CBRT','CEIL','CEILING','DEGREES','DIV','EXP','FACTORIAL','FLOOR','GCD','IN','LOG','MOD','PI','POWER','ROUND',
              'ACOS','ACOSD','ASIN','ASIND','ATAN','ATAND','ATAN2','ATAN2D','COS','COSD','COT','COTD','SIN','SIND','TAN','TAND',
              'SINH','COSH','TANH','ASINH','ACOSH','ATANH',
              'DATE_PART','NOW','EXTRACT','CURRENT_TIME','CURRENT_DATE',
              'LENGTH','TRIM','GET_BYTE','MOD5','SET_BYTE','SHA256','SUBSTR','CONVERT','ENCODE','DECODE','DOUBLE','INHERITS'
              ]

tokens = reservadas + ['PUNTO','PUNTO_COMA','CADENASIMPLE','COMA','SIGNO_IGUAL','PARABRE','PARCIERRE','SIGNO_MAS','SIGNO_MENOS',
                       'SIGNO_DIVISION','SIGNO_POR','NUMERO','NUM_DECIMAL','CADENA','ID','LLAVEABRE','LLAVECIERRE','CORCHETEABRE',
                       'CORCHETECIERRE','DOBLE_DOSPUNTOS','SIGNO_POTENCIA','SIGNO_MODULO','MAYORQUE','MENORQUE',
                       'MAYORIGUALQUE','MENORIGUALQUE',
                       'SIGNO_PIPE','SIGNO_DOBLE_PIPE','SIGNO_AND','SIGNO_VIRGULILLA','SIGNO_NUMERAL','SIGNO_DOBLE_MENORQUE','SIGNO_DOBLE_MAYORQUE',
                       'FECHA_HORA','F_HORA','COMILLA','SIGNO_MENORQUE_MAYORQUE','SIGNO_NOT'
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
t_SIGNO_POTENCIA = r'\^'
t_SIGNO_MODULO = r'\%'
t_MAYORIGUALQUE = r'\>\='
t_MENORIGUALQUE = r'\<\='
t_MAYORQUE = r'\>'
t_MENORQUE = r'\<'
t_COMILLA = r'\''


# expresion regular para los id´s
def t_ID (t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        if t.value.upper() in reservadas:
            t.value = t.value.upper()
            t.type = t.value    
        return t

def t_CADENASIMPLE(t):
    r'\'.*?\''
    t.value = str(t.value)
    t.value = t.value[1:-1]
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
    r'\'\d+-\d+-\d+ \d+:\d+:\d+\''
    t.value = t.value[1:-1]
    return t
    
# expresion regular para reconocer cadenas
def t_CADENA(t):
    r'\".*?\"'
    t.value = str(t.value)
    t.value = t.value[1:-1]
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


# funcion para realizar el analisis lexico de nuestra entrada
def analizarLex(texto):    
    analizador = lex.lex()
    analizador.input(texto)# el parametro cadena, es la cadena de texto que va a analizar.

    #ciclo para la lectura caracter por caracter de la cadena de entrada.
    textoreturn = ""
    while True:
        tok = analizador.token()
        if not tok : break
        #print(tok)
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
    )          


# Definición de la gramática
def p_inicio(t):
    '''inicio : instrucciones '''
    envGlobal = Environment(None)
    iniciarEjecucion = Main(t[1])
    iniciarEjecucion.execute(envGlobal)

def p_instrucciones_lista(t):
    '''instrucciones : instrucciones instruccion 
                     | instruccion '''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_instrucciones_evaluar(t):
    '''instruccion : ins_use
                   | ins_show
                   | ins_alter
                   | ins_drop
                   | ins_create
                   | ins_insert
                   | ins_select
                   | ins_update
                   | ins_delete'''
    t[0] = t[1]

def p_instruccion_use(t):
    '''ins_use : USE ID PUNTO_COMA'''
    t[0] = Use(t[2], 0, 0)

def p_instruccion_show(t):
    '''ins_show : SHOW DATABASES PUNTO_COMA'''
    #t[0] = Show_Database(0, 0)

def p_instruccion_create(t):
    '''ins_create : CREATE tipo_create'''
    #t[0] = t[2]  

def p_tipo_create(t):
    '''tipo_create : ins_replace DATABASE if_exists ID create_opciones PUNTO_COMA
                   | TABLE ID PARABRE definicion_columna PARCIERRE ins_inherits PUNTO_COMA
                   | TYPE ID AS ENUM PARABRE list_vls PARCIERRE PUNTO_COMA'''
    #if t[1] == 'TYPE':
    #    print('TYPE')
    #elif t[1] == 'TABLE':
    #    print('TABLE')
    #else:
    #    t[0] = Create(t[1], 0, t[4], 0, 0)

def p_definicion_columna(t):
    '''definicion_columna : definicion_columna COMA columna 
                          | columna ''' # no se *** si va la coma o no

def p_columna(t):
    '''columna : ID tipo_dato definicion_valor_defecto ins_constraint
                | ID definicion_valor_defecto ins_constraint
                | ID TYPE tipo_dato definicion_valor_defecto ins_constraint
                | primary_key 
                | foreign_key '''

def p_ins_inherits(t):
    '''ins_inherits : INHERITS PARABRE ID PARCIERRE
                |  ''' #EPSILON

def p_primary_key(t):
    '''primary_key : PRIMARY KEY PARABRE nombre_columnas PARCIERRE ins_references'''

def p_foreign_key(t):
    '''foreign_key : FOREIGN KEY PARABRE nombre_columnas PARCIERRE REFERENCES ID PARABRE nombre_columnas PARCIERRE ins_references'''

def p_nombre_columnas(t):
    '''nombre_columnas : nombre_columnas COMA ID 
                          | ID '''

def p_tipo_dato(t):
    '''tipo_dato : SMALLINT          
                 | BIGINT
                 | NUMERIC
                 | DECIMAL
                 | INTEGER
                 | REAL
                 | DOUBLE PRECISION
                 | CHAR PARABRE NUMERO PARCIERRE
                 | VARCHAR PARABRE NUMERO PARCIERRE
                 | CHARACTER PARABRE NUMERO PARCIERRE
                 | TEXT
                 | TIMESTAMP arg_precision
                 | TIME arg_precision
                 | DATE
                 | INTERVAL arg_tipo arg_precision
                 | BOOLEAN
                 | MONEY'''

def p_arg_precision(t):
    '''arg_precision : PARABRE NUMERO PARCIERRE 
                     | ''' #epsilon
def p_arg_tipo(t):
    '''arg_tipo : MONTH
                | YEAR
                | HOUR
                | MINUTE
                | SECOND            
                | '''

def p_definicion_valor_defecto(t):
    '''definicion_valor_defecto : DEFAULT tipo_default 
                                | ''' #epsilon

def p_ins_constraint(t):
    '''ins_constraint : ins_constraint constraint restriccion_columna 
                        | restriccion_columna
                        |''' #epsilon

def p_constraint(t):
    '''constraint :  CONSTRAINT ID 
                    |  '''

def p_restriccion_columna(t):
    '''restriccion_columna : NOT NULL 
                           | SET NOT NULL 
                           | PRIMARY KEY 
                           | UNIQUE 
                           | NULL 
                           | NOT NULL PRIMARY KEY 
                           | CHECK PARABRE exp PARCIERRE 
                           | 
                           ''' #cambio del condicion columna

def p_references(t):
    '''ins_references : ON DELETE accion ins_references
                      | ON UPDATE accion ins_references
                      | '''

def p_accion(t):
    '''accion : CASCADE
              | SET NULL
              | SET DEFAULT
              | NO ACTION'''

def p_tipo_default(t): #ESTE NO SE SI SON RESERVADAS O LOS VALORES
    '''tipo_default : NUMERIC
                    | DECIMAL
                    | NULL'''

def p_ins_replace(t): 
    '''ins_replace : OR REPLACE
               | '''#EPSILON
    if len(t) ==3:
        t[0] = True
    else: 
        t[0] = False

def p_if_exists(t): 
    '''if_exists :  IF NOT EXISTS
                |  IF EXISTS
                | ''' # EPSILON

def p_create_opciones(t): 
    '''create_opciones : OWNER SIGNO_IGUAL user_name create_opciones
                       | MODE SIGNO_IGUAL NUMERO create_opciones
                       | '''
    #if len(t) == 5:
    #    if t[1] == 'MODE':
    #        t[0] = t[3]
    #    else:
    #        t[0] = 0
    #else: 
    #    t[0] = 0

def p_user_name(t):
    '''user_name : ID
                  | CADENA 
                  | CADENASIMPLE'''
    #t[0] = t[1]

def p_alter(t): 
    '''ins_alter : ALTER tipo_alter ''' 
    #t[0] = t[2]

def p_tipo_alter(t): 
    '''tipo_alter : DATABASE ID alter_database PUNTO_COMA
                  | TABLE ID alteracion_tabla PUNTO_COMA''' # NO SE SI VAN LOS PUNTO Y COMA
    #if t[1] == 'DATABASE':
    #    if t[3] == None:
    #        t[0] = Alter_Database(t[2],t[2], 0, 0)
    #    else: 
    #        t[0] = Alter_Database(t[2],t[3], 0, 0)
    #else: 
    #    print('TABLE')

def p_alteracion_tabla(t): 
    '''alteracion_tabla : alteracion_tabla COMA alterar_tabla
                        | alterar_tabla'''

def p_alterar_tabla(t): 
    #alter column viene como una lista
    '''alterar_tabla : ADD COLUMN ID tipo_dato
                     | ADD CONSTRAINT ins_constraint
                     | ALTER COLUMN ID TYPE tipo_dato
                     | ALTER COLUMN ID SET NOT NULL
                     | DROP COLUMN ID
                     | DROP CONSTRAINT ID'''

def p_alter_database(t): 
    '''alter_database : RENAME TO ID
                      | OWNER TO ID'''
    #if t[1] == 'RENAME':
    #    t[0] = t[3]
    #else:
    #    t[0] = None

def p_drop(t): 
    '''ins_drop : DROP tipo_drop'''
    #t[0] = t[2]

def p_tipo_drop(t): 
    '''tipo_drop : DATABASE if_exists ID PUNTO_COMA
                 | TABLE ID PUNTO_COMA'''
    #if len(t) == 5:
    #    t[0] = Drop_Database(t[3], 0, 0)

def p_ins_insert(t):
    '''ins_insert : INSERT INTO ID VALUES PARABRE list_vls PARCIERRE PUNTO_COMA 
                  | INSERT INTO ID PARABRE list_id PARCIERRE VALUES PARABRE list_vls PARCIERRE PUNTO_COMA'''
    print('INSERT INTO ID VALUES ( *values* )')

def p_list_id(t):
    '''list_id : list_id COMA id
               | id'''

def p_list_vls(t):
    '''list_vls : list_vls COMA val_value
                | val_value '''

def p_val_value(t):
    '''val_value : CADENA
                |   CADENASIMPLE
                |   NUMERO
                |   NUM_DECIMAL
                |   FECHA_HORA
                |   TRUE
                |   FALSE 
                |   NULL
                |   F_HORA'''

def p_ins_select(t):
    '''ins_select : ins_select UNION option_all ins_select PUNTO_COMA
                    |    ins_select INTERSECT option_all ins_select PUNTO_COMA
                    |    ins_select EXCEPT option_all ins_select PUNTO_COMA
                    |    SELECT arg_distict colum_list FROM table_list arg_where arg_group_by arg_order_by arg_limit arg_offset PUNTO_COMA'''

def p_option_all(t):
    '''option_all   :   ALL
                    |    '''

def p_arg_distict(t):
    '''arg_distict :    DISTINCT
                    |    '''

def p_colum_list(t):
    '''colum_list   :   s_list
                    |   SIGNO_POR '''

def p_s_list(t):
    '''s_list   :   s_list COMA columns as_id
                |   columns as_id'''


def p_columns(t):
    '''columns   : ID dot_table
                    |   aggregates
                    |   functions '''

def p_dot_table(t):
    '''dot_table    :   PUNTO ID
                    |    '''

def p_as_id(t): #  REVISRA CADENA Y AS CADENA
    '''as_id    :   AS ID
                    |   AS CADENA
                    |   CADENA
                    |   '''


def p_aggregates(t):
    '''aggregates   :   COUNT PARABRE param PARCIERRE
                    |   SUM PARABRE param PARCIERRE
                    |   AVG PARABRE param PARCIERRE
                    |   MAX PARABRE param PARCIERRE
                    |   MIN PARABRE param PARCIERRE ''' 

def p_functions(t):
    '''functions    :   math
                    |   trig
                    |   string_func
                    |   time_func
                     '''
                    # CORREGIR GRAMATICA <STRING_FUNC>

def p_math(t):
    '''math :   AVG PARABRE NUMERO PARCIERRE
                |   CBRT PARABRE NUMERO PARCIERRE
                |   CEIL PARABRE NUMERO PARCIERRE
                |   CEILING PARABRE NUMERO PARCIERRE
                |   DEGREES PARABRE NUMERO PARCIERRE
                |   DIV PARABRE NUMERO COMA NUMERO PARCIERRE
                |   EXP PARABRE NUMERO PARCIERRE
                |   FACTORIAL PARABRE NUMERO PARCIERRE
                |   FLOOR PARABRE NUMERO PARCIERRE
                |   GCD PARABRE NUMERO COMA NUMERO PARCIERRE
                |   IN PARABRE NUMERO PARCIERRE
                |   LOG PARABRE NUMERO PARCIERRE
                |   MOD PARABRE NUMERO COMA NUMERO PARCIERRE
                |   PI PARABRE  PARCIERRE
                |   POWER PARABRE NUMERO COMA NUMERO PARCIERRE 
                |   ROUND PARABRE NUMERO PARCIERRE '''

def p_trig(t):
    '''trig :   ACOS PARABRE NUMERO PARCIERRE
                |   ACOSD PARABRE NUMERO PARCIERRE
                |   ASIN PARABRE NUMERO PARCIERRE
                |   ASIND PARABRE NUMERO PARCIERRE
                |   ATAN PARABRE NUMERO PARCIERRE
                |   ATAND PARABRE NUMERO PARCIERRE
                |   ATAN2 PARABRE NUMERO COMA NUMERO PARCIERRE
                |   ATAN2D PARABRE NUMERO COMA NUMERO PARCIERRE
                |   COS PARABRE NUMERO PARCIERRE
                |   COSD PARABRE NUMERO PARCIERRE
                |   COT PARABRE NUMERO PARCIERRE
                |   COTD PARABRE NUMERO PARCIERRE
                |   SIN PARABRE NUMERO PARCIERRE
                |   SIND PARABRE NUMERO PARCIERRE
                |   TAN PARABRE NUMERO PARCIERRE
                |   TAND PARABRE NUMERO PARCIERRE
                |   SINH PARABRE NUMERO PARCIERRE
                |   COSH PARABRE NUMERO PARCIERRE
                |   TANH PARABRE NUMERO PARCIERRE
                |   ASINH PARABRE NUMERO PARCIERRE
                |   ACOSH PARABRE NUMERO PARCIERRE
                |   ATANH PARABRE NUMERO PARCIERRE  '''

def p_string_func(t):   # CORREGIR GRAMÁTICA
    '''string_func  :   LENGTH PARABRE s_param PARCIERRE
                    |   SUBSTRING PARABRE s_param COMA NUMERO COMA NUMERO PARCIERRE
                    |   SUBSTRING PARABRE s_param COMA s_param COMA CADENA PARCIERRE
                    |   TRIM PARABRE s_param PARCIERRE
                    |   GET_BYTE PARABRE s_param COMA NUMERO PARCIERRE
                    |   MOD5 PARABRE s_param PARCIERRE
                    |   SET_BYTE PARABRE COMA NUMERO COMA NUMERO s_param PARCIERRE
                    |   SHA256 PARABRE s_param PARCIERRE
                    |   SUBSTR PARABRE s_param COMA NUMERO COMA NUMERO PARCIERRE
                    |   CONVERT PARABRE tipo_dato COMA ID dot_table PARCIERRE
                    |   ENCODE PARABRE s_param COMA s_param PARCIERRE
                    |   DECODE PARABRE s_param COMA s_param PARCIERRE '''

def p_s_param(t):
    '''s_param  :   s_param string_op CADENA
                |   CADENA '''

def p_string_op(t):
    '''string_op    :   SIGNO_PIPE
                    |   SIGNO_DOBLE_PIPE
                    |   SIGNO_AND
                    |   SIGNO_VIRGULILLA
                    |   SIGNO_NUMERAL
                    |   SIGNO_DOBLE_MENORQUE
                    |   SIGNO_DOBLE_MAYORQUE'''


def p_time_func(t):
    '''time_func    :   DATE_PART PARABRE COMILLA h_m_s COMILLA COMA INTERVAL F_HORA PARCIERRE 
                    |   NOW PARABRE PARCIERRE
                    |   EXTRACT PARABRE reserv_time  FROM TIMESTAMP  PARCIERRE
                    |   CURRENT_TIME
                    |   CURRENT_DATE'''

def p_reserv_time(t):
    '''reserv_time  :   h_m_s 
                    |   YEAR
                    |   MONTH
                    |   DAY'''

def p_h_m_s(t):
    '''h_m_s    :   HOUR
                    |   MINUTE
                    |   SECOND '''

def p_param(t):
    '''param    :   ID dot_table
                |   SIGNO_POR '''

def p_table_list(t):
    '''table_list   :   table_list COMA ID as_id
                    |   ID as_id'''

def p_arg_where(t):
    '''arg_where    :   WHERE exp
                    |    '''

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
            | data
            | predicates
            | aggregates
            | functions
            | arg_case
            | arg_greatest
            | arg_least 
            | val_value'''
# values -> list_vls


def p_arg_greatest(t):
    '''arg_greatest  : GREATEST PARABRE exp_list PARCIERRE''' 

def p_arg_least(t):
    '''arg_least  : LEAST PARABRE exp_list PARCIERRE''' 

def p_exp_list(t):
    '''exp_list  : exp_list COMA exp
                 | exp'''

def p_case(t):
    '''arg_case  : CASE arg_when arg_else END''' 

def p_arg_when(t):
    '''arg_when  : arg_when WHEN exp THEN exp
                 | WHEN exp THEN exp''' 
def p_arg_else(t):
    '''arg_else :  ELSE exp
                 | ''' # epsilon

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

def p_data(t):
    '''data  : ID table_at''' 

def p_table_at(t):
    '''table_at  : PUNTO ID
                 | ''' #epsilon
            
def p_sub_consulta(t):
    '''sub_consulta   : PARABRE ins_select  PARCIERRE''' 

def p_arg_pattern(t):
    '''arg_pattern   : data LIKE CADENA   
                     | data NOT LIKE CADENA ''' 

def p_arg_group_by(t):
    '''arg_group_by    :   GROUP BY g_list
                       |  ''' #epsilon

def p_g_list(t):
    '''g_list    : g_list COMA g_item
                 | g_item ''' 

def p_g_item(t):
    '''g_item    : ID g_refitem''' 

def p_g_refitem(t):
    '''g_refitem  : PUNTO ID
                  | ''' #epsilon

def p_arg_order_by(t):
    '''arg_order_by    :   ORDER BY o_list
                       |  ''' #epsilon

def p_o_list(t):
    '''o_list    : o_list COMA o_item
                 | o_item ''' 

def p_o_item(t):
    '''o_item    : ID o_refitem ad arg_nulls''' 

def p_o_refitem(t):
    '''o_refitem  : PUNTO ID
                  | ''' #epsilon

def p_ad(t):
    '''ad : ASC
          | DESC
          | ''' #epsilon

def p_arg_nulls(t):
    '''arg_nulls : NULLS arg_fl
                 | ''' #epsilon

def p_arg_fl(t):
    '''arg_fl : FIRST
              | LAST''' #epsilon

def p_arg_limit(t):
    '''arg_limit   :  LIMIT option_limit
                   |  ''' #epsilon

def p_option_limit(t):
    '''option_limit   : NUMERO
                      | ALL ''' 

def p_arg_offset(t):
    '''arg_offset   : OFFSET NUMERO 
                    |  ''' #epsilon


def p_ins_update(t):
    '''ins_update   : UPDATE ID SET asign_list WHERE exp PUNTO_COMA '''

def p_ins_asign_list(t):
    '''asign_list  : asign_list COMA ID SIGNO_IGUAL exp 
                   | ID SIGNO_IGUAL exp'''

def p_ins_delete(t):
    '''ins_delete   : DELETE FROM ID WHERE exp PUNTO_COMA'''

def p_error(t):
    print("Error sintáctico en '%s'" % t.value)
    print(str(t.lineno))






# metodo para realizar el analisis sintactico, que es llamado a nuestra clase principal
#"texto" -> en este parametro enviaremos el texto que deseamos analizar
def analizarSin(texto):    
    parser = yacc.yacc()
    parser.parse(texto)# el parametro cadena, es la cadena de texto que va a analizar.

