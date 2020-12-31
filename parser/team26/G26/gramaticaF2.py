from error import error

errores = list()

reservadas = {
    'smallint' : 'SMALLINT',
    'integer' : 'INTEGER',
    'bigint' : 'BIGINT',
    'decimal' : 'DECIMAL',
    'numeric' : 'NUMERIC',
    'real' : 'REAL',
    'double' : 'DOUBLE',
    'precision' : "PRECISION",
    'money' : 'MONEY',
    'character' : 'CHARACTER',
    'varying' : 'VARYING',
    'varchar' : 'VARCHAR',
    'char' : 'CHAR',
    'text' : 'TEXT',
    'use' : 'USE',
    'timestamp' : 'TIMESTAMP',
    'time' : 'TIME',
    'interval' : 'INTERVAL',
    'year' : 'YEAR',
    'month' : 'MONTH',
    'day' : 'DAY',
    'hour' : 'HOUR',
    'minute' : 'MINUTE',
    'second' : 'SECOND',
    'boolean' : 'BOLEANO',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'between' : 'BETWEEN',
    'like' : 'LIKE',
    'ilike' : 'ILIKE',
    'similar' : 'SIMILAR',
    'isnull' : 'ISNULL',
    'is' : 'IS',
    'notnull' : 'NOTNULL',
    'not' : 'NOT',
    'and' : 'AND',
    'or' : 'OR',
    'unknown' : 'UNKNOWN',
    'null' : 'NULL',
    'sum' : 'SUM',
    'avg' : 'AVG',
    'count' : 'COUNT',
    'max' : 'MAX',
    'min' : 'MIN',
    'create' : 'CREATE',
    'type' : 'TYPE',
    'as' : 'AS',
    'enum' : 'ENUM',
    'replace' : 'REPLACE',
    'databases' : 'DATABASES',
    'database' : 'DATABASE',
    'if' : 'IF',
    'not' : 'NOT',
    'exists' : 'EXISTS',
    'owner' : 'OWNER',
    'mode' : 'MODE',
    'like' : 'LIKE',
    'rename' : 'RENAME',
    'to' : 'TO',
    'drop' : 'DROP',
    'table' : 'TABLE',
    'default' : 'DEFAULT',
    'constraint' : 'CONSTRAINT',
    'unique' : 'UNIQUE',
    'check' : 'CHECK',
    'primary' : 'PRIMARY',
    'foreign' : 'FOREIGN',
    'key' : 'KEY',
    'references' : 'REFERENCES',
    'drop' : 'DROP',
    'alter' : 'ALTER',
    'add' : 'ADD',
    'column' : 'COLUMN',
    'delete' : 'DELETE',
    'from' : 'FROM',
    'only' : 'ONLY',
    'where' : 'WHERE',
    'of' : 'OF',
    'returning' : 'RETURNING',
    'inherits' : 'INHERITS',
    'insert' : 'INSERT',
    'into' : 'INTO',
    'values' : 'VALUES',
    'update' : 'UPDATE',
    'set' : 'SET',
    'select' : 'SELECT',
    'distinct' : 'DISTINCT',
    'group' : 'GROUP',
    'by' : 'BY',
    'having' : 'HAVING',
    'substring' : 'SUBSTRING',
    'join' : 'JOIN',
    'inner' : 'INNER',
    'left' : 'LEFT',
    'right' : 'RIGHT',
    'full' : 'FULL',
    'outer' : 'OUTER',
    'on' : 'ON',
    'natural' : 'NATURAL',
    'nulls' : 'NULLS',
    'first' : 'FIRST',
    'last' : 'LAST',
    'greatest' : 'GREATEST',
    'least' : 'LEAST',
    'limit' : 'LIMIT',
    'offset' : 'OFFSET',
    'all' : 'ALL',
    'any' : 'ANY',
    'union' : 'UNION',
    'intersect' : 'INTERSECT',
    'except' : 'EXCEPT',
    'abs' : 'ABS',
    'cbrt' : 'CBRT',
    'ceiling' : 'CEILING',
    'ceil' : 'CEIL',
    'degrees' : 'DEGREES',
    'div' : 'DIV',
    'exp' : 'EXP',
    'floor' : 'FLOOR',
    'gcd' : 'GCD',
    'lcm' : 'LCM',
    'ln' : 'LN',
    'log' : 'LOG',
    'min_scale' : 'MINSCALE',
    'mod' : 'MOD',
    'pi' : 'PI',
    'power' : 'POWER',
    'radians' : 'RADIANS',
    'round' : 'ROUND',
    'scale' : 'SCALE',
    'sign' : 'SIGN',
    'sqrt' : 'SQRT',
    'trim_scale' : 'TRIM',
    'width_bucket' : 'BUCKET',
    'random' : 'RANDOM',
    'setseed' : 'SETSEED',
    'acos' : 'ACOS',
    'acosd' : 'ACOSD',
    'asin' : 'ASIN',
    'asind' : 'ASIND',
    'atan' : 'ATAN',
    'atand' : 'ATAND',
    'atan2' : 'ATANDOS',
    'atan2d' : 'ATANDOSD',
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
    'get_byte' : 'GETBYTE',
    'factorial' : 'FACTORIAL',
    'md5' : 'MD5',
    'set_byte' : 'SETBYTE',
    'sha256' : 'SHA',
    'substr' : 'SUBSTR',
    'convert' : 'CONVERT',
    'encode' : 'ENCODE',
    'decode' : 'DECODE',
    'date_part' : 'DATEPART',
    'now' : 'NOW',
    'extract' : 'EXTRACT',
    'current_date' : 'CURRENTDATE',
    'current_time' : 'CURRENTTIME',
    'date' : 'DATE',
    'current_user' : 'CURRENT_USER',
    'session_user' : 'SESSION_USER',
    'show'  :   'SHOW',
    'symmetric' : 'SYMMETRIC',
    'bytea' : 'BYTEA',
    'case' : 'CASE',
    'end' : 'END',
    'else' : 'ELSE',
    'then' : 'THEN',
    'when':'WHEN',
    'trunc' :'TRUNC',
    'some' : 'SOME',
    'in': 'IN',
    'all': 'ALL',
    'index': 'INDEX',
    'using': 'USING',
    'hash': 'HASH',
    'lower': 'LOWER',
    'desc': 'DESC',
    'asc' : 'ASC'
}

tokens = [
    'PTCOMA',
    'LLAVEIZQ',
    'LLAVEDER',
    'PARENIZQ',
    'PARENDER',
    'IGUAL',
    'MAS',
    'GUION',
    'BARRA',
    'ASTERISCO',
    'MAYORQUE',
    'MENORQUE',
    'MENORIGUALQUE',
    'MAYORIGUALQUE',
    'DIFERENTELL',
    'PUNTO',
    'COMA',
    'ENTERO',
    'CADENA',
    'ID',
    'FEED',
    'NEWLINE',
    'RETURN',
    'TAB',
    'FECHA',
    'PORCENTAJE',
    'POTENCIA',
    'DOSPUNTOS',
    'PLECA',
    'AMPERSON',
    'NUMERAL',
    'VIRGULILLA'
] + list(reservadas.values())

#tokens
t_PLECA         = r'\|'
t_AMPERSON      = r'&'
t_VIRGULILLA    = r'~'
t_NUMERAL       = r'\#'
t_DOSPUNTOS     = r':'
t_PTCOMA        = r';'
t_LLAVEIZQ      = r'{'
t_LLAVEDER      = r'}'
t_PARENIZQ      = r'\('
t_PARENDER      = r'\)'
t_IGUAL         = r'='
t_MAS           = r'\+'
t_GUION         = r'-'
t_ASTERISCO     = r'\*'
t_BARRA         = r'/'
t_MAYORIGUALQUE = r'>='
t_MAYORQUE      = r'>'
t_MENORIGUALQUE = r'<='
t_MENORQUE      = r'<'
t_DIFERENTELL   = r'<>|!='
t_PUNTO         = r'.'
t_COMA          = r'\,'
t_FEED          = r'\\f'
t_NEWLINE       = r'\\n'
t_TAB           = r'\\r'
t_PORCENTAJE    = r'%'
t_POTENCIA      = r'\^'

def t_DECIMAL(t):
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

def t_FECHA(t):
    r'\'\d+-\d+-\d+ \d+:\d+:\d+\''
    return t

def t_CADENA(t):
    r'\'.*?\''
    t.value = t.value[1:-1] # remuevo las comillas
    return t

def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'--.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    description = "Error lexico con -> " + t.value
    mistake = error("Lexico", description, str(t.lineno))
    errores.append(mistake)
    t.lexer.skip(1)

# Construyendo el analizador léxico
import Librerias.ply.lex as lex
lexer = lex.lex()

from imports import *

grafo = graph.Grafo(0)
tempos = temp.Code3D()

precedence = (
    ('left','MAS','GUION'),
    ('left','ASTERISCO','BARRA', 'PORCENTAJE'),
    ('left','POTENCIA'),
    ('right','UMENOS', 'UMAS'),
    )

def p_init(t) :
    'init            : instrucciones'
    text = t[1]['text']
    t[0] =  {'text': text, 'c3d' : '' }


def p_instrucciones_lista(t) :
    'instrucciones : instrucciones instruccion'
    text = t[1]['text'] + "\n" + t[2]['text']
    t[0] =  {'text': text, 'c3d' : '' }

def p_instruciones(t):
    'instrucciones : instruccion'''
    text = t[1]['text']
    t[0] =  {'text': text, 'c3d' : '' }

def p_instruccion(t) :
    '''instruccion      : CREATE createops'''
                        #| USE use
                        #| SHOW show
                        #| DROP drop
                        #| DELETE delete
                        #| INSERT insert
                        #| UPDATE update
    txt = tempos.newTemp() + ' = \'' + t[1] + t[2]['text'] + '\'\n'
    txt += 'heap.append('+str(tempos.index)+')\n'
    txt += 'mediador()\n'
    t[0] = {'text' : txt, 'c3d': ''}

#----------------testing condiciones--------------------
def p_instrcond(t):
    'instruccion    : condiciones'
    t[0] = {'text' : t[1]['c3d'], 'c3d': ''}
#-------------------------------------------------------

def p_instruccion_ccreate(t):
    'createops    : create'
    t[0] = {'text' : t[1]['text'], 'c3d': ''}

def p_instruccion_ccreateind(t):
    'createops    : createindex'
    t[0] = {'text' : t[1]['text'], 'c3d': ''}

def p_instruccionSelect(t):
    'instruccion  : select PTCOMA'
    text = t[1]['text'] + ";"
    t[0] =  {'text': text, 'c3d' : '' }

def p_instruccionQuerys(t):
    'instruccion  : querys'
    text = t[1]['text'] 
    t[0] =  {'text': text, 'c3d' : '' }

def p_instruccionError(t):
    'instruccion  : problem'
    text = "\n"
    t[0] =  {'text': text, 'c3d' : '' }

def p_problem(t):
    '''problem  :  error PTCOMA'''

#---------------------------------------------------------------INDEX-----------------------------------
def p_createindex(t):
    '''createindex  : UNIQUE INDEX ID ON ID predicadoindexU PTCOMA
                    | INDEX ID ON ID predicadoindex PTCOMA'''
    if t[1].lower() == 'unique':
        txt = ' UNIQUE INDEX ' + t[3] + ' ON ' + t[5] + t[6]['text'] + ';'
    elif t[1].lower() == 'index':
        txt = ' INDEX ' + t[2] + ' ON ' + t[4] + t[5]['text'] + ';'
    t[0] = {'text' : txt, 'c3d': ''}

def p_indexPredicateU(t):
    'predicadoindexU   : PARENIZQ listaids PARENDER WHERE condiciones'
    txt = ' (' + t[2]['text'] + ') WHERE ' + t[5]['text']
    t[0] = {'text' : txt, 'c3d': ''}

def p_indexPredicateUP(t):
    'predicadoindexU   : PARENIZQ listaids PARENDER'
    txt = ' (' + t[2]['text'] + ') '
    t[0] = {'text' : txt, 'c3d': ''}

def p_indexPredicate(t):
    'predicadoindex   : USING HASH PARENIZQ ID PARENDER'
    txt = ' USING HASH (' + t[4] + ') '
    t[0] = {'text' : txt, 'c3d': ''}

def p_indexPredicateP(t):
    'predicadoindex   : PARENIZQ indexargs PARENDER WHERE condiciones'
    txt = ' (' + t[2]['text'] + ') WHERE ' + t[5]['text']
    t[0] = {'text' : txt, 'c3d': ''}

def p_indexPredicateS(t):
    'predicadoindex   : PARENIZQ indexargs PARENDER'
    txt = ' (' + t[2]['text'] + ') '
    t[0] = {'text' : txt, 'c3d': ''}

def p_indexargs(t):
    'indexargs   : listaids'
    txt = t[1]['text']
    t[0] = {'text' : txt, 'c3d': ''}

def p_indexargsP(t):
    'indexargs   : LOWER PARENIZQ ID PARENDER'
    txt = ' LOWER (' + t[3] + ') '
    t[0] = {'text' : txt, 'c3d': ''}

def p_indexargsS(t):
    'indexargs   : ID asdcordesc NULLS firstorlast'
    txt = t[1] + ' ' + t[2]['text'] + ' NULLS ' + t[4]['text']
    t[0] = {'text' : txt, 'c3d': ''}

def p_asdcordesc(t):
    '''asdcordesc   : ASC
                    | DESC'''
    txt = t[1] + ' '
    t[0] = {'text' : txt, 'c3d': ''}

def p_asdcordescE(t):
    'asdcordesc   : '
    t[0] = {'text' : '', 'c3d': ''}

def p_firstorlast(t):
    '''firstorlast   : FIRST
                    | LAST'''
    txt = ' '+t[1]+' '
    t[0] = {'text' : txt, 'c3d': ''}

#----------------------------------------------------------------SELECT---------------------------------
def p_querys(t):
    '''querys : select UNION allopcional select
              | select INTERSECT  allopcional select
              | select EXCEPT  allopcional select'''
    text = ""
    if t[2].lower() == 'union' :
        text = t[1]['text'] + "\n UNION \n" + t[3]['text'] + t[4]['text']
    elif t[2].lower() == 'intersect' :
        text = t[1]['text'] + "\n INTERSECT \n" + t[3]['text'] + t[4]['text']
    elif t[2].lower() == 'except' :
        text = t[1]['text'] + "\n EXCEPT \n" + t[3]['text'] + t[4]['text']
    t[0] =  {'text': text, 'c3d' : '' }

def p_all_opcional(t):
    'allopcional  : ALL'
    text = "ALL "
    t[0] =  {'text': text, 'c3d' : '' }

def p_all_opcional_null(t):
    'allopcional : '
    text = "\n"
    t[0] =  {'text': text, 'c3d' : '' }

#aqui
def p_select(t):
    'select : SELECT parametrosselect fromopcional'
    text = "SELECT " + t[2]['text'] + t[3]['text']
    t[0] =  {'text': text, 'c3d' : '' }

def p_select_err(t):
    'select : problem'
    text = "\n"
    t[0] =  {'text': text, 'c3d' : '' }

def p_from_opcional(t):
    'fromopcional     :  FROM parametrosfrom whereopcional '
    text = " FROM "+ t[2]['text'] + t[3]['text']
    t[0] =  {'text': text, 'c3d' : '' }

def p_from_opcional_2(t):
    'fromopcional     :  FROM parametrosfrom groupbyopcional '
    text = " FROM "+ t[2]['text'] + t[3]['text']
    t[0] =  {'text': text, 'c3d' : '' }

def p_from_opcional_null(t):
    'fromopcional : '
    text = " "
    t[0] =  {'text': text, 'c3d' : '' }

def p_where_opcional(t):
    'whereopcional :  WHERE condiciones groupbyopcional'
    text = " FROM "+ t[2]['text'] + t[3]['text']
    t[0] =  {'text': text, 'c3d' : '' }

def p_where_opcional_null(t):
    'whereopcional :   '
    text = "\n"
    t[0] =  {'text': text, 'c3d' : '' }

def p_group_by_opcional(t):
    'groupbyopcional  : GROUP BY listaids havings'
    text = " GROUP BY " + t[3]['text'] +  t[4]['text']
    t[0] =  {'text': text, 'c3d' : '' }

def p_group_by_opcional_numeros(t):
    'groupbyopcional  : GROUP BY listanumeros havings'
    text = " GROUP BY "+ t[3]['text'] + t[4]['text']
    t[0] =  {'text': text, 'c3d' : '' }

def p_having(t):
    'havings   : HAVING condiciones'
    text = " HAVING "+ t[2]['text']
    t[0] =  {'text': text, 'c3d' : '' }

def p_having_null(t):
    'havings : '
    text = "\n"
    t[0] =  {'text': text, 'c3d' : '' }

def p_listanumeros_r(t):
    'listanumeros : listanumeros COMA ENTERO'
    text = t[1]['text'] + ", " + t[3] 
    t[0] =  {'text': text, 'c3d' : '' }

def p_listanumeros(t):
    'listanumeros : ENTERO'
    text = t[1]
    t[0] =  {'text': text, 'c3d' : '' }

def p_group_by_opcional_null(t):
    'groupbyopcional  : '
    text = "\n"
    t[0] =  {'text': text, 'c3d' : '' }

def p_parametros_from(t):
    'parametrosfrom : parametrosfrom COMA parametrosfromr asopcional'
    text = t[1]['text'] + ", " + t[3]['text'] + t[4]['text'] 
    t[0] =  {'text': text, 'c3d' : '' }

def p_parametros_from_r(t):
    'parametrosfrom : parametrosfromr asopcional'
    text = t[1]['text'] + ", " + t[3] 
    t[0] =  {'text': text, 'c3d' : '' }

def p_parametros_fromr(t):
    '''parametrosfromr   : ID
                        | PARENIZQ select PARENDER'''
    text = ""
    if t[1] == '(' :
        text = "(" + t[2]['text'] + ")\n"
    else :
        text = t[1]
    t[0] =  {'text': text, 'c3d' : '' }


def p_parametros_select(t):
    'parametrosselect : DISTINCT listadeseleccion'
    text = " DISTINCT " + t[2]['text'] 
    t[0] =  {'text': text, 'c3d' : '' }

def p_parametros_select_r(t):
    'parametrosselect : listadeseleccion'
    text = t[1]['text'] 
    t[0] =  {'text': text, 'c3d' : '' }

def p_lista_de_seleccion(t):
    'listadeseleccion : listadeseleccion COMA listadeseleccionados  asopcional'
    text = t[1]['text'] + ", " + t[3]['text'] + t[4]['text']
    t[0] =  {'text': text, 'c3d' : '' }

def p_lista_de_seleccion_r(t):
    'listadeseleccion : listadeseleccionados asopcional'
    text = t[1]['text'] + t[2]['text']
    t[0] =  {'text': text, 'c3d' : '' }

def p_lista_de_seleccionados(t):
    '''listadeseleccionados : PARENIZQ select PARENDER
                            | ASTERISCO
                            | GREATEST PARENIZQ listadeargumentos  PARENDER
                            | LEAST PARENIZQ listadeargumentos  PARENDER
                            | CASE cases  END ID '''
    text = ""
    if t[1].lower() == 'greatest' :
        text = "GREATEST (" + t[3]['text'] + ")"
    elif t[1].lower() == 'least' :
        text = "LEAST (" + t[3]['text'] + ")"
    elif t[1].lower() == 'case' :
        text = "CASE " + t[2]['text'] + " END " + t[4]
    elif t[1] == '*' :
        text = " * "
    elif t[1] == '(' :
        text = "(" + t[2]['text'] + ")"
    t[0] =  {'text': text, 'c3d' : '' }

def p_lista_de_seleccionados_noterminal(t):
    '''listadeseleccionados : funcionesmatematicassimples
                            | funcionestrigonometricas
                            | funcionesmatematicas
                            | funcionesdefechas
                            | funcionesbinarias
                            | operadoresselect'''
    text = t[1]['text']
    t[0] =  {'text': text, 'c3d' : '' }

def p_lista_de_argumentos(t):
    'listadeargumentos : listadeargumentos COMA argument'
    text = t[1]['text']
    t[0] =  {'text': text, 'c3d' : '' }

def p_lista_de_argumentos_r(t):
    'listadeargumentos : argument '
    text = t[1]['text']
    t[0] =  {'text': text, 'c3d' : '' }
    
def p_casos(t):
    'cases    : cases case elsecase'

def p_casos_r(t):
    'cases : case elsecase'

def p_case(t):
    'case : WHEN condiciones  THEN  argument'

def p_else_case(t):
    'elsecase  : ELSE argument '
    

def p_else_case_null(t):
    'elsecase  : '
    


def p_operadores_select_t(t):
    '''operadoresselect : PLECA argumentodeoperadores
                        | VIRGULILLA argumentodeoperadores'''
    text = ""
    if t[1] == '|':
        text = "PLECA " + t[2]['text']
    else :
        text = "VIRGULILLA "+ t[2]['text']
    t[0] =  {'text': text, 'c3d' : '' }

def p_operadores_s_pleca(t):
    ' operadoresselect : PLECA PLECA argumentodeoperadores'
    

def p_operadores_select_nt(t):
    '''operadoresselect : argumentodeoperadores AMPERSON argumentodeoperadores
                        | argumentodeoperadores PLECA argumentodeoperadores
                        | argumentodeoperadores NUMERAL argumentodeoperadores
                        | argumentodeoperadores MENORQUE MENORQUE argumentodeoperadores
                        | argumentodeoperadores MAYORQUE MAYORQUE argumentodeoperadores'''
    text = ""
    if t[2] == '&' :
        text = t[1]['text'] + " & " + t[3]['reporte']
    elif t[2] == '|' :
        text = t[1]['text'] + " | " + t[3]['reporte']
    elif t[2] == '#' :
        text = t[1]['text'] + " # " + t[3]['reporte']
    elif t[2] == '<' :
        text = t[1]['text'] + " <> " + t[3]['reporte']
    elif t[2] == '>' :
        text = t[1]['text'] + " >> " + t[3]['reporte']
    t[0] =  {'text': text, 'c3d' : '' }
    
def p_argumento_de_operadores(t):
    '''argumentodeoperadores    : argumentodeoperadores MAS argumentodeoperadores
                                | argumentodeoperadores GUION argumentodeoperadores
                                | argumentodeoperadores BARRA argumentodeoperadores
                                | argumentodeoperadores ASTERISCO argumentodeoperadores
                                | argumentodeoperadores PORCENTAJE argumentodeoperadores
                                | argumentodeoperadores POTENCIA argumentodeoperadores'''
    text = ""
    if t[2] == '+'   :
        text = t[1]['text'] + " + " + t[3]['reporte']
    elif t[2] == '-' :
        text = t[1]['text'] + " - " + t[3]['reporte']
    elif t[2] == '/' :
        text = t[1]['text'] + " / " + t[3]['reporte']
    elif t[2] == '*' :
        text = t[1]['text'] + " * " + t[3]['reporte']
    elif t[2] == '%' :
        text = t[1]['text'] + " % " + t[3]['reporte']
    elif t[2] == '^' :
        text = t[1]['text'] + " ^ " + t[3]['reporte']
    t[0] =  {'text': text, 'c3d' : '' }


def p_argumento_de_operadores_decimal(t):
    'argumentodeoperadores : DECIMAL'
    

def p_argumento_de_operadores_entero(t):
    'argumentodeoperadores : ENTERO'
    

def p_argumento_de_operadores_ID(t):
    '''argumentodeoperadores : ID'''
    

def p_funciones_matematicas_simples(t):
    '''funcionesmatematicassimples  : COUNT PARENIZQ argument  PARENDER
                                    | MAX PARENIZQ argument  PARENDER
                                    | SUM PARENIZQ argument  PARENDER
                                    | AVG PARENIZQ argument  PARENDER
                                    | MIN PARENIZQ argument  PARENDER'''
    text = ""
    if t[1].lower() == "count":
        text = "COUNT (" + t[3]['text'] + ")"
    elif t[1].lower() == "max":
        text = "MAX (" + t[3]['text'] + ")"
    elif t[1].lower() == "sum":
        text = "SUM (" + t[3]['text'] + ")"
    elif t[1].lower() == "avg":
        text = "AVG (" + t[3]['text'] + ")"
    elif t[1].lower() == "min":
        text = "MIN (" + t[3]['text'] + ")"
    t[0] =  {'text': text, 'c3d' : '' }

def p_funciones_matematicas_simplesa(t):
    'funcionesmatematicassimples  : COUNT PARENIZQ ASTERISCO  PARENDER '
    

def p_funciones_binarias(t):
    '''funcionesbinarias    : LENGTH PARENIZQ  argument   PARENDER
                            | SUBSTRING PARENIZQ  argument  COMA  ENTERO  COMA  ENTERO  PARENDER
                            | TRIM PARENIZQ  argument   PARENDER
                            | MD5 PARENIZQ  argument   PARENDER
                            | SHA PARENIZQ  argument   PARENDER
                            | SUBSTR PARENIZQ  argument  COMA  ENTERO  COMA  ENTERO  PARENDER
                            | GETBYTE PARENIZQ argument DOSPUNTOS DOSPUNTOS BYTEA COMA argument PARENDER
                            | SETBYTE PARENIZQ argument DOSPUNTOS DOSPUNTOS BYTEA COMA argument COMA argument PARENDER
                            | CONVERT PARENIZQ argument AS tipo
                            | ENCODE PARENIZQ argument DOSPUNTOS DOSPUNTOS BYTEA COMA CADENA PARENDER
                            | DECODE PARENIZQ argument COMA CADENA PARENDER '''
    text = ""
    if t[1].lower() == 'length' :
        text = "LENG(" + t[3]['text'] + ")"
    elif t[1].lower() == 'substring' :
        text = "SUBSTRING(" + t[3]['text'] + ", " + t[5] + ", " + t[7] + ")"
    elif t[1].lower() == 'trim' :
        text = "TRIM(" + t[3]['text'] + ")"
    elif t[1].lower() == 'md5' :
        text = "MD5(" + t[3]['text'] + ")"
    elif t[1].lower() == 'sha256' :
        text = "SHA256(" + t[3]['text'] + ")"
    elif t[1].lower() == 'substr' :
        text = "SUBSTR(" + t[3]['text'] + ", " + t[5] + ", " + t[7] + ")"
    elif t[1].lower() == 'get_byte' :
        text = "GET_BYTE(" + t[3]['text'] + ":: BYTEA" + ", " + t[8]['text'] + ", " + t[10]['text'] + ")"
    elif t[1].lower() == 'set_byte' :
        text = "SET_BYTE(" + t[3]['text'] + ":: BYTEA" + ", " + t[8]['text'] + ", " + t[10]['text'] + ")"
    elif t[1].lower() == 'convert' :
        text = "CONVERT(" + t[3]['text'] + ") AS " + t[5]['text']
    elif t[1].lower() == 'decode' :
        text = "DECODE(" + t[3]['text'] + ", " + t[5] + ")"
    elif t[1].lower() == 'encode' :
        text = "ENCODE(" + t[3]['text'] + ":: BYTEA , " + t[8] + ")"
    t[0] =  {'text': text, 'c3d' : '' }

def p_funciones_matematicas_S (t):
    '''funcionesmatematicas : PI PARENIZQ PARENDER
                            | RANDOM PARENIZQ PARENDER'''
    text = ""
    if t[1].lower() == "random":
        text = "RANDOM()"
    else:
        text = "PI()"
    t[0] =  {'text': text, 'c3d' : '' }

def p_funciones_matematicas_1 (t):
    '''funcionesmatematicas : ABS PARENIZQ  argument  PARENDER
                            | CBRT PARENIZQ  argument   PARENDER
                            | CEIL PARENIZQ  argument   PARENDER
                            | CEILING PARENIZQ  argument   PARENDER
                            | DEGREES PARENIZQ  argument   PARENDER
                            | EXP PARENIZQ  argument   PARENDER
                            | FLOOR PARENIZQ  argument   PARENDER
                            | LN PARENIZQ  argument   PARENDER
                            | LOG PARENIZQ  argument   PARENDER
                            | RADIANS PARENIZQ  argument   PARENDER
                            | SCALE PARENIZQ  argument   PARENDER
                            | SIGN PARENIZQ  argument   PARENDER
                            | SQRT PARENIZQ  argument   PARENDER
                            | TRUNC PARENIZQ  argument   PARENDER'''
    text = ""
    if t[1].lower() == "abs":
        text = " ABS(" + t[3]['text'] + ")"
    elif t[1].lower() == "cbrt":
        text = " CBRT(" + t[3]['text'] + ")"
    elif t[1].lower() == "ceil":
        text = " CEIL(" + t[3]['text'] + ")"
    elif t[1].lower() == "ceiling":
        text = " CEILING(" + t[3]['text'] + ")"
    elif t[1].lower() == "degrees":
        text = " DEGREES(" + t[3]['text'] + ")"
    elif t[1].lower() == "exp":
        text = " EXP(" + t[3]['text'] + ")"
    elif t[1].lower() == "floor":
        text = " FLOOR(" + t[3]['text'] + ")"
    elif t[1].lower() == "ln":
        text = " LN(" + t[3]['text'] + ")"
    elif t[1].lower() == "log":
        text = " LOG(" + t[3]['text'] + ")"
    elif t[1].lower() == "radians":
        text = " RADIANS(" + t[3]['text'] + ")"
    elif t[1].lower() == "scale":
        text = " SCALE(" + t[3]['text'] + ")"
    elif t[1].lower() == "sign":
        text = " SIGN(" + t[3]['text'] + ")"
    elif t[1].lower() == "sqrt":
        text = " SQRT(" + t[3]['text'] + ")"
    elif t[1].lower() == "trunc":
        text = " TRUNC(" + t[3]['text'] + ")"
    t[0] =  {'text': text, 'c3d' : '' }

def p_funciones_matematicas_2 (t):
    '''funcionesmatematicas : DIV PARENIZQ  argument  COMA  argument  PARENDER
                            | GCD PARENIZQ  argument  COMA  argument  PARENDER
                            | MOD PARENIZQ  argument  COMA  argument   PARENDER
                            | POWER PARENIZQ  argument  COMA  argument   PARENDER'''
    text =""
    if t[1].lower() == "div":
        text  = " DIV( " + t[3]['text'] + ", " + t[5]['text'] + ")"
    elif t[1].lower() == "gcd":
        text  = " GCD( " + t[3]['text'] + ", " + t[5]['text'] + ")"
    elif t[1].lower() == "mod":
        text  = " MOD( " + t[3]['text'] + ", " + t[5]['text'] + ")"
    elif t[1].lower() == "power":
        text  = " POWER( " + t[3]['text'] + ", " + t[5]['text'] + ")"
    t[0] =  {'text': text, 'c3d' : '' }

def p_funciones_matematicas_2R (t):
    'funcionesmatematicas : ROUND PARENIZQ  argument   tipoderound  PARENDER'

def p_tipo_de_round(t):
    'tipoderound  : COMA  argument'

def p_tipo_de_round_null(t):
    'tipoderound  :'


def p_funciones_matematicas_4 (t):
    'funcionesmatematicas : BUCKET PARENIZQ  argument COMA argument COMA argument COMA argument PARENDER'

def p_funciones_trigonometricas(t):
    '''funcionestrigonometricas :  ACOS PARENIZQ argument  PARENDER
                                | ASIN PARENIZQ argument  PARENDER
                                | ACOSD PARENIZQ argument  PARENDER
                                | ASIND PARENIZQ argument  PARENDER
                                | ATAN PARENIZQ argument  PARENDER
                                | ATAND PARENIZQ argument  PARENDER
                                | ATANDOS PARENIZQ argument COMA argument PARENDER
                                | ATANDOSD PARENIZQ argument COMA argument PARENDER
                                | COS PARENIZQ argument  PARENDER
                                | COSD PARENIZQ argument  PARENDER
                                | COT PARENIZQ argument  PARENDER
                                | COTD PARENIZQ argument  PARENDER
                                | SIN PARENIZQ argument  PARENDER
                                | SIND PARENIZQ argument  PARENDER
                                | TAN PARENIZQ argument  PARENDER
                                | TAND PARENIZQ argument  PARENDER
                                | SINH PARENIZQ argument  PARENDER
                                | COSH PARENIZQ argument  PARENDER
                                | TANH PARENIZQ argument  PARENDER
                                | ASINH PARENIZQ argument  PARENDER
                                | ACOSH PARENIZQ argument  PARENDER
                                | ATANH PARENIZQ argument  PARENDER '''
    text = ""
    if t[1].lower() == 'atan2':
        text = "ATAN2( " + t[3]['text'] + ", " + t[5]['text'] + ")"
    else :
        if t[1].lower() == "acos":
            text = "ACOS(" + t[3]['text'] + ")"
        elif t[1].lower() == "asin":
            text = "ASIN(" + t[3]['text'] + ")"
        elif t[1].lower() == "acosd":
            text = "ACOSD(" + t[3]['text'] + ")"
        elif t[1].lower() == "asind":
            text = "ASIND(" + t[3]['text'] + ")"
        elif t[1].lower() == "atan":
            text = "ATAN(" + t[3]['text'] + ")"
        elif t[1].lower() == "atand":
            text = "ATAND(" + t[3]['text'] + ")"
        elif t[1].lower() == "cos":
            text = "COS(" + t[3]['text'] + ")"
        elif t[1].lower() == "cosd":
            text = "COSD(" + t[3]['text'] + ")"
        elif t[1].lower() == "cot":
            text = "COT(" + t[3]['text'] + ")"
        elif t[1].lower() == "cotd":
            text = "COTD(" + t[3]['text'] + ")"
        elif t[1].lower() == "sin":
            text = "SIN(" + t[3]['text'] + ")"
        elif t[1].lower() == "sind":
            text = "SIND(" + t[3]['text'] + ")"
        elif t[1].lower() == "tan":
            text = "TAN(" + t[3]['text'] + ")"
        elif t[1].lower() == "tand":
            text = "TAND(" + t[3]['text'] + ")"
        elif t[1].lower() == "sinh":
            text = "SINH(" + t[3]['text'] + ")"
        elif t[1].lower() == "cosh":
            text = "COSH(" + t[3]['text'] + ")"
        elif t[1].lower() == "tanh":
            text = "TANH(" + t[3]['text'] + ")"
        elif t[1].lower() == "asinh":
            text = "ASINH(" + t[3]['text'] + ")"
        elif t[1].lower() == "acosh":
            text = "ACOSH(" + t[3]['text'] + ")"
        elif t[1].lower() == "atanh":
            text = "ATANH(" + t[3]['text'] + ")"
        elif t[1].lower() == "atan2d":
            text = "ATAN2D(" + t[3]['text'] + ")"
        t[0] =  {'text': text, 'c3d' : '' }


def p_funciones_de_fechas(t):
    '''funcionesdefechas    : EXTRACT PARENIZQ  partedelafecha  FROM TIMESTAMP argument PARENDER
                            | DATEPART PARENIZQ argument COMA INTERVAL argument PARENDER
                            | NOW PARENIZQ PARENDER
                            | CURRENTDATE
                            | CURRENTTIME
                            | TIMESTAMP argument  '''
    text = ""
    if t[1].lower() == 'extract' :
        text = "EXTRACT(" + t[3]['text'] + " FROM TIMESTAMP " + t[6]['text'] + ")"
    elif t[1].lower() == 'date_part' :
        text = "DATEPART (" + t[3]['text'] + ", INTERVAL " + t[6]['text'] + ")"
    elif t[1].lower() == 'now' :
        text = "NOW()"
    elif t[1].lower() == 'current_date' :
        text = "CURRENTDATE"
    elif t[1].lower() == 'current_time' :
        text = "CURRENTTIME"
    elif t[1].lower() == 'timestamp' :
        text = "TIMESTAMP " + t[2]['text']
    t[0] =  {'text': text, 'c3d' : '' }

def p_parte_de_la_decha(t):
    '''partedelafecha   : YEAR
                        | MONTH
                        | DAY
                        | HOUR
                        | MINUTE
                        | SECOND'''
    text = ""
    if t[1].lower() == "year":
        text = " YEAR"
    elif t[1].lower() == "month":
        text = " MONTH"
    elif t[1].lower() == "day":
        text = " DAY"
    elif t[1].lower() == "hour":
        text = " HOUR"
    elif t[1].lower() == "minute":
        text = " MINUTE"
    elif t[1].lower() == "second":
        text = " SECOND"
    t[0] =  {'text': text, 'c3d' : '' }


def p_lista_de_seleccionados_id(t):
    'listadeseleccionados : ID'
    text = "ID"
    t[0] =  {'text': text, 'c3d' : '' }

def p_lista_de_seleccionados_id_punto_id(t):
    'listadeseleccionados : ID PUNTO ID'

def p_lista_de_seleccionados_id_punto_asterisco(t):
    'listadeseleccionados : ID PUNTO ASTERISCO'

def p_asopcional(t):
    'asopcional  : AS ID '

def p_asopcional_argument(t):
    'asopcional  : ID'

def p_asopcionalS(t):
    'asopcional  : AS CADENA '

def p_asopcional_argumentS(t):
    'asopcional  : CADENA'

def p_asopcional_null(t):
    'asopcional  : '

def p_argument_noterminal(t):
    '''argument : funcionesmatematicassimples
                | funcionestrigonometricas
                | funcionesmatematicas
                | funcionesdefechas
                | funcionesbinarias'''
    text = t[1]['text']
    t[0] =  {'text': text, 'c3d' : '' }


#-------------------------------------------CREATEEE----------------------------------------------------
def p_create_instruccion(t) :
    '''create : TYPE createenum
              | TABLE createtable
              | OR REPLACE DATABASE createdatabase
              | DATABASE createdatabase'''
    if t[1].lower() == 'or' :
        txt = ' OR REPLACE DATABASE '  + t[4]['text']
        t[0] = {'text' : txt, 'c3d': ''}
    else :
        txt = ' ' + t[1] + ' ' + t[2]['text']
        t[0] = {'text' : txt, 'c3d': ''}

def p_create_instruccion_err(t):
    "create : problem"
    t[0] = {'text' : '', 'c3d': ''}

def p_createenum(t):
    'createenum : ID AS ENUM PARENIZQ listacadenas PARENDER PTCOMA'
    txt = ' ' + t[1] + ' AS ENUM (' + t[5]['text'] + '); '
    t[0] = {'text' : txt, 'c3d': ''}

def p_listacadenas_recursiva(t):
    'listacadenas : listacadenas COMA CADENA'
    txt = t[1]['text'] + ', ' + t[3]
    t[0] = {'text' : txt, 'c3d': ''}

def p_listacadenas(t):
    'listacadenas : CADENA'
    txt = ' \'' + t[1] + '\' '
    t[0] = {'text' : txt, 'c3d': ''}

def p_createdatabase(t):
    '''createdatabase : IF NOT EXISTS ID databaseowner
                      | ID databaseowner'''
    if t[1].lower() == 'if' :
        txt = ' IF NOT EXISTS ' + t[4] + ' ' + t[5]['text']
        t[0] = {'text' : txt, 'c3d': ''}
    else :
        txt = ' ' + t[1] + ' ' + t[2]['text']
        t[0] = {'text' : txt, 'c3d': ''}

def p_databaseowner(t):
    '''databaseowner : OWNER IGUAL tipoowner databasemode'''
    txt = ' OWNER ' + t[3]['text'] + t[4]['text']
    t[0] = {'text' : txt, 'c3d': ''}

def p_databaseownerS(t):
    '''databaseowner : OWNER tipoowner databasemode'''
    txt = ' OWNER ' + t[2]['text'] + t[3]['text']
    t[0] = {'text' : txt, 'c3d': ''}

def p_tipoowner_id(t) :
    'tipoowner : ID'
    txt = ' ' + t[1] + ' '
    t[0] = {'text' : txt, 'c3d': ''}

def p_tipoowner_cadena(t) :
    'tipoowner : CADENA'
    txt = ' \'' + t[1] + '\' '
    t[0] = {'text' : txt, 'c3d': ''}

def p_databaseownerP(t):
    'databaseowner  : databasemode'
    txt = t[1]['text']
    t[0] = {'text' : txt, 'c3d': ''}

def p_databasemode(t):
    '''databasemode : MODE IGUAL ENTERO PTCOMA
                    | MODE ENTERO PTCOMA
                    | PTCOMA'''
    if t[1] == ';' :
        txt = ';'
        t[0] = {'text' : txt, 'c3d': ''}
    else :
        if t[2] == '=' :
            txt = ' MODE = ' + str(t[3]) + ';'
            t[0] = {'text' : txt, 'c3d': ''}
        else :
            txt = ' MODE ' + str(t[2]) + ';'
            t[0] = {'text' : txt, 'c3d': ''}

def p_createtable(t):
    'createtable : ID PARENIZQ tabledescriptions PARENDER tableherencia'
    txt = ' ' + t[1] + ' (' + t[3]['text'] + ' ) ' + t[5]['text']
    t[0] = {'text' : txt, 'c3d': ''}

def p_tableherencia(t):
    '''tableherencia : INHERITS PARENIZQ ID PARENDER PTCOMA
                     | PTCOMA'''
    if t[1].lower() == 'inherits' :
        txt = ' INHERITS ( ' + t[3] + ' );'
        t[0] = {'text' : txt, 'c3d': ''}
    else :
        txt = ' ;'
        t[0] = {'text' : txt, 'c3d': ''}

def p_tabledescriptions_recursivo(t):
    'tabledescriptions : tabledescriptions COMA tabledescription'
    txt = t[1]['text'] + ', ' + t[3]['text']
    t[0] = {'text' : txt, 'c3d': ''}

def p_tabledescriptions(t):
    'tabledescriptions :  tabledescription'
    txt = t[1]['text']
    t[0] = {'text' : txt, 'c3d': ''}

def p_tabledescription(t):
    '''tabledescription : ID tipo tablekey
                        | PRIMARY KEY PARENIZQ listaids PARENDER
                        | FOREIGN KEY PARENIZQ listaids PARENDER REFERENCES ID PARENIZQ listaids PARENDER
                        | CONSTRAINT ID CHECK finalconstraintcheck
                        | CHECK finalconstraintcheck
                        | UNIQUE finalunique'''
    if t[1].lower() == 'primary' :
        txt = ' PRIMARY KEY (' + t[4]['text'] + ')'
    elif t[1].lower() == 'foreign' :
        txt = ' FOREIGN KEY (' + t[4]['text'] + ') REFERENCES ' + t[7] + ' (' + t[9]['text'] + ')'
    elif t[1].lower() == 'constraint' :
        txt = ' CONSTRAINT ' + t[2] + ' CHECK ' + t[4]['text']
    elif t[1].lower() == 'check' :
        txt = ' CHECK ' + t[2]['text']
    elif t[1].lower() == 'unique' :
        txt = ' UNIQUE ' + t[2]['text']
    else :
        txt = ' ' + t[1] + ' ' + t[2]['text'] + t[3]['text']

    t[0] = {'text' : txt, 'c3d': ''}


def p_tablekey(t):
    '''tablekey : PRIMARY KEY tabledefault
                | REFERENCES ID PARENIZQ ID PARENDER tabledefault'''
    if t[1].lower() == 'primary' :
        txt = ' PRIMARY KEY ' + t[3]['text']
    elif t[1].lower() == 'references' :
        txt = ' REFERENCES ' + t[2] + ' (' + t[4] + ') ' + t[6]['text']
    t[0] = {'text' : txt, 'c3d': ''}

def p_tablekeyP(t):
    'tablekey   : REFERENCES ID tabledefault'
    txt = ' REFERENCES ' + t[2] + ' ' + t[3]['text']
    t[0] = {'text' : txt, 'c3d': ''}

def p_tablekeyP2(t):
    'tablekey   : tabledefault'
    txt = t[1]['text']
    t[0] = {'text' : txt, 'c3d': ''}

def p_columnreferences_r(t):
    'columnreferences : columnreferences COMA ID'
    txt = t[1]['text'] + ', ' + t[3]
    t[0] = {'text' : txt, 'c3d': ''}

def p_columnreferences_r2(t):
    'columnreferences : ID'
    txt = t[1]
    t[0] = {'text' : txt, 'c3d': ''}

def p_tabledefault(t):
    '''tabledefault : DEFAULT value tablenull'''
    txt = ' DEFAULT ' + t[2]['text'] + t[3]['text']
    t[0] = {'text' : txt, 'c3d': ''}

def p_tabledefaultP(t):
    'tabledefault   : tablenull'
    txt = t[1]['text']
    t[0] = {'text' : txt, 'c3d': ''}

def p_tablenull(t):
    '''tablenull : NOT NULL tableconstraintunique
                 | NULL tableconstraintunique'''
    if t[1].lower() == 'not' :
        txt = ' NOT NULL ' + t[3]['text']
    else :
        txt = ' NULL ' + t[2]['text']

    t[0] = {'text' : txt, 'c3d': ''}

def p_tablenullP(t):
    'tablenull  : tableconstraintunique'
    txt = t[1]['text']
    t[0] = {'text' : txt, 'c3d': ''}

def p_tableconstraintunique(t):
    '''tableconstraintunique : CONSTRAINT ID UNIQUE tableconstraintcheck
                             | UNIQUE tableconstraintcheck'''
    if t[1].lower() == 'constraint' :
        txt = ' CONSTRAINT ' + t[2] + ' UNIQUE ' + t[4]['text']
    else :
        txt = ' UNIQUE ' + t[2]['text']
    
    t[0] = {'text' : txt, 'c3d': ''}

def p_tableconstraintuniqueP(t):
    'tableconstraintunique  : tableconstraintcheck'
    txt = t[1]['text']
    t[0] = {'text' : txt, 'c3d': ''}

def p_tableconstraintcheck(t):
    '''tableconstraintcheck : CONSTRAINT ID CHECK PARENIZQ condiciones PARENDER
                            | CHECK PARENIZQ condiciones PARENDER'''
    if t[1].lower() == 'constraint' :
        txt = ' CONSTRAINT ' + t[2] + ' CHECK (' + t[4]['text'] + ')'
    else :
        txt = ' CHECK (' + t[3]['text'] + ')'
    
    t[0] = {'text' : txt, 'c3d': ''}

def p_tableconstraintcheckE(t):
    'tableconstraintcheck : '
    t[0] = {'text' : '', 'c3d': ''}

def p_finalconstraintcheck(t):
    'finalconstraintcheck : PARENIZQ condiciones PARENDER'
    txt = ' (' + t[2]['text'] + ') '
    t[0] = {'text' : txt, 'c3d': ''}

def p_finalunique(t):
    'finalunique : PARENIZQ listaids PARENDER'
    txt = ' (' + t[2]['text'] + ') '
    t[0] = {'text' : txt, 'c3d': ''}

def p_listaids_r(t):
    'listaids : listaids COMA ID'
    txt = t[1]['text'] + ', ' + t[3]
    t[0] = {'text' : txt, 'c3d': ''}

def p_listaids(t):
    'listaids : ID'
    txt = t[1]
    t[0] = {'text' : txt, 'c3d': ''}

def p_listaidcts_r(t):
    'listaidcts : listaidcts COMA ID PUNTO ID'
    txt = t[1]['text'] + ', ' + t[3] + '.' + t[5]
    t[0] = {'text' : txt, 'c3d': ''}

def p_listaidcts_re(t):
    'listaidcts : listaidcts COMA ID'
    txt = t[1]['text'] + ', ' + t[3]
    t[0] = {'text' : txt, 'c3d': ''}

def p_listaidcts(t):
    'listaidcts : ID PUNTO ID'
    txt =  t[1] + '.' + t[3]
    t[0] = {'text' : txt, 'c3d': ''}

def p_listaidctse(t):
    'listaidcts : ID'
    txt = t[1]
    t[0] = {'text' : txt, 'c3d': ''}

def p_tipo(t):
    '''tipo : SMALLINT
            | INTEGER
            | BIGINT
            | DECIMAL
            | NUMERIC
            | REAL
            | DOUBLE PRECISION
            | MONEY
            | CHARACTER tipochar
            | VARCHAR PARENIZQ ENTERO PARENDER
            | CHAR PARENIZQ ENTERO PARENDER
            | TEXT
            | TIMESTAMP precision
            | TIME precision
            | DATE
            | INTERVAL fields precision
            | BOLEANO
            | ID'''
    txt = t[1]
    if t[1].lower() == 'character' :
        txt += t[2]['text']
    elif t[1].lower() == 'varchar' :
        txt += '(' + str(t[3]) + ')'
    elif t[1].lower() == 'char' :
        txt += '(' + str(t[3]) + ')'
    elif t[1].lower() == 'timestamp' :
        txt += t[2]['text']
    elif t[1].lower() == 'time' :
        txt += t[2]['text']
    elif t[1].lower() == 'interval' :
        txt += t[2]['text'] + t[3]['text']

    t[0] = {'text' : txt, 'c3d': ''}

def p_tipochar(t):
    '''tipochar : VARYING PARENIZQ ENTERO PARENDER
                | PARENIZQ ENTERO PARENDER'''
    if t[1].lower() == 'varying' :
        txt = ' VARYING ('+str(t[3])+')'
    else :
        txt = ' ('+str(t[2])+')'

    t[0] = {'text' : txt, 'c3d': ''}

def p_precision(t):
    '''precision : PARENIZQ ENTERO PARENDER'''
    txt = ' ('+str(t[2])+')'
    t[0] = {'text' : txt, 'c3d': ''}

def p_precisionE(t):
    'precision  :'
    t[0] = {'text' : '', 'c3d': ''}

def p_fields(t):
    '''fields : MONTH
              | HOUR
              | MINUTE
              | SECOND
              | YEAR'''
    txt = t[1]
    t[0] = {'text' : txt, 'c3d': ''}

def p_fieldsE(t):
    'fields :'
    t[0] = {'text' : '', 'c3d': ''}

#------------------------------------------------------CONDICIONES-----------------------------------------
def p_condiciones_recursivo(t):
    'condiciones    : condiciones comparacionlogica condicion'
    c3 = t[1]['c3d']
    c3 += t[3]['c3d']
    c3 += tempos.newTemp() + ' = ' + t[1]['tflag'] + ' ' + t[2] + ' ' + t[3]['tflag'] + '\n'
    t[0] = {'text' : '', 'c3d' : c3, 'tflag' : 't'+str(tempos.index)}

def p_codiciones(t):
    'condiciones    :  condicion'
    t[0] = t[1]

def p_comparacionlogica(t):
    '''comparacionlogica    : AND
                            | OR'''
    t[0] = t[1].lower()

def p_condicion(t):
    'condicion    : NOT condicion'
    c3 = t[2]['c3d']
    c3 += tempos.newTemp() + ' = ' + t[1].lower() + ' ' + t[2]['tflag']  + '\n'
    t[0] = {'text' : '', 'c3d' : c3, 'tflag' : 't'+str(tempos.index)}

def p_condicionP(t):
    '''condicion    : condicions'''
    t[0] = t[1]

def p_condicions(t):
    '''condicions : argument MENORQUE argument
                  | argument MAYORQUE argument
                  | argument IGUAL argument
                  | argument MENORIGUALQUE argument
                  | argument MAYORIGUALQUE argument
                  | argument DIFERENTELL argument
                  | argument BETWEEN betweenopcion
                  | argument ISNULL
                  | argument NOTNULL
                  | argument IS isopcion
                  | argument IN  PARENIZQ select PARENDER
                  | argument NOT BETWEEN betweenopcion
                  | argument NOT IN  PARENIZQ select PARENDER'''
    if t[2] == '<'    :
        c3 = t[1]['c3d']
        c3 += t[3]['c3d']
        c3 += tempos.newTemp() + ' = ' + t[1]['tflag'] + ' ' + t[2] + ' ' + t[3]['tflag'] + '\n'
    elif t[2] == '>'  :
        c3 = t[1]['c3d']
        c3 += t[3]['c3d']
        c3 += tempos.newTemp() + ' = ' + t[1]['tflag'] + ' ' + t[2] + ' ' + t[3]['tflag'] + '\n'
    elif t[2] == '='  :
        c3 = t[1]['c3d']
        c3 += t[3]['c3d']
        c3 += tempos.newTemp() + ' = ' + t[1]['tflag'] + ' == ' + t[3]['tflag'] + '\n'
    elif t[2] == '<=' :
        c3 = t[1]['c3d']
        c3 += t[3]['c3d']
        c3 += tempos.newTemp() + ' = ' + t[1]['tflag'] + ' ' + t[2] + ' ' + t[3]['tflag'] + '\n'
    elif t[2] == '>=' :
        c3 = t[1]['c3d']
        c3 = t[3]['c3d']
        c3 = tempos.newTemp() + ' = ' + t[1]['tflag'] + ' ' + t[2] + ' ' + t[3]['tflag'] + '\n'
    elif t[2] == '<>' or t[2] == '!=' :
        c3 = t[1]['c3d']
        c3 += t[3]['c3d']
        c3 += tempos.newTemp() + ' = ' + t[1]['tflag'] + ' != ' + t[3]['tflag'] + '\n'
    elif t[2].lower() == 'between' :
        tp = tempos.newTemp()
        c3 = tp + ' = ' + t[1]['tflag'] + ' >= ' + t[3]['c3d'] + '\n'
        ts = tempos.newTemp()
        c3 += ts + ' = ' + t[1]['tflag'] + ' <= ' + t[3]['tflag'] + '\n'
        c3 += tempos.newTemp() + ' = ' + tp + ' and ' + ts + '\n'
    elif t[2].lower() == 'not' :
        if t[3].lower() == 'between':
            tp = tempos.newTemp()
            c3 = tp + ' = ' + t[1]['tflag'] + ' >= ' + t[4]['c3d'] + '\n'
            ts = tempos.newTemp()
            c3 += ts + ' = ' + t[1]['tflag'] + ' <= ' + t[4]['tflag'] + '\n'
            c3 += tempos.newTemp() + ' = ' + tp + ' and ' + ts + '\n'
        else :
            reporte = "<condicions> ::= <argument> NOT IN  PARENIZQ <select> PARENDER\n" + t[1]['reporte'] + t[5]['reporte']
            t[0] = {'ast' : condicion.Condicionales(t[1]['ast'], t[5]['ast'], 'not in', None), 'graph' : grafo.index, 'reporte': reporte}
    elif t[2].lower() == 'isnull' :
        tp = tempos.newTemp()
        c3 = tempos.newTemp() + ' = ' + t[1]['tflag'] + ' == \'null\' \n'
        ts = tempos.newTemp()
        c3 += tempos.newTemp() + ' = ' + t[1]['tflag'] + ' == \'\' \n'
        c3 += tempos.newTemp() + ' = ' + tp + ' or ' + ts + '\n'
    elif t[2].lower() == 'notnull' :
        tp = tempos.newTemp()
        c3 = tempos.newTemp() + ' = ' + t[1]['tflag'] + ' != \'null\' \n'
        ts = tempos.newTemp()
        c3 += tempos.newTemp() + ' = ' + t[1]['tflag'] + ' != \'\' \n'
        c3 += tempos.newTemp() + ' = ' + tp + ' or ' + ts + '\n'
    elif t[2].lower() == 'is' :
        c3 = t[3]['c3d']
        #c3 += tempos.newTemp() + ' = ' + t[3]['tflag']
    else :
        reporte = "<condicions> ::= <argument> IN  PARENIZQ <select> PARENDER\n" + t[1]['reporte'] +t[4]['reporte']
        t[0] = {'ast' : condicion.Condicionales(t[1]['ast'], t[4]['ast'], 'in', None), 'graph' : grafo.index, 'reporte': reporte}
    
    t[0] = {'text' : '', 'c3d' : c3, 'tflag' : 't'+str(tempos.index)}

def p_condicionsP(t):
    'condicions : EXISTS PARENIZQ select PARENDER'
    reporte = "<condicions> ::= EXISTS PARENIZQ <select> PARENDER\n" + t[3]['reporte']
    t[0] = {'ast' : None, 'graph' : grafo.index, 'reporte': reporte}

def p_betweenopcion(t):
    '''betweenopcion    : argument AND argument'''
    t[0] = {'text' : '', 'c3d' : t[1]['tflag'], 'tflag' : t[3]['tflag']}
    

def p_betweenopcionP(t):
    '''betweenopcion    : symm argument AND argument'''
    t[0] = {'text' : '', 'c3d' : t[2]['tflag'], 'tflag' : t[4]['tflag']}

def p_symmetric(t):
    'symm   : SYMMETRIC'
    t[0] = t[1].upper()

def p_isopcion(t):
    '''isopcion : DISTINCT FROM argument
                | NULL
                | TRUE
                | FALSE
                | UNKNOWN
                | NOT isnotoptions'''
    c3 = ''
    if t[1].lower() == 'distinct' :
        c3 = tempos.newTemp() + ' = ' + t[-2]['tflag'] + ' != ' + t[3]['tflag'] + '\n'
    elif t[1].lower() == 'null' :
        tp = tempos.newTemp()
        c3 = tempos.newTemp() + ' = ' + t[-2]['tflag'] + ' == \'null\' \n'
        ts = tempos.newTemp()
        c3 += tempos.newTemp() + ' = ' + t[-2]['tflag'] + ' == \'\' \n'
        c3 += tempos.newTemp() + ' = ' + tp + ' or ' + ts + '\n'
    elif t[1].lower() == 'true' :
        c3 = tempos.newTemp() + ' = ' + t[-2]['tflag'] + ' == True' + '\n'
    elif t[1].lower() == 'false' :
        c3 = tempos.newTemp() + ' = ' + t[-2]['tflag'] + ' == False' + '\n'
    elif t[1].lower() == 'unknown' :
        tp = tempos.newTemp()
        c3 = tempos.newTemp() + ' = ' + t[-2]['tflag'] + ' == \'null\' \n'
        ts = tempos.newTemp()
        c3 += tempos.newTemp() + ' = ' + t[-2]['tflag'] + ' == \'\' \n'
        c3 += tempos.newTemp() + ' = ' + tp + ' or ' + ts + '\n'
    elif t[1].lower() == 'not' :
        c3 = t[2]['c3d']
    
    t[0] = {'text' : '', 'c3d' : c3, 'tflag' : 't'+str(tempos.index)}

def p_isnotoptions(t):
    '''isnotoptions : FALSE
                    | UNKNOWN
                    | TRUE
                    | NULL
                    | DISTINCT FROM argument'''
    c3 = ''
    if t[1].lower() == 'null' :
        tp = tempos.newTemp()
        c3 = tempos.newTemp() + ' = ' + t[-3]['tflag'] + ' != \'null\' \n'
        ts = tempos.newTemp()
        c3 += tempos.newTemp() + ' = ' + t[-3]['tflag'] + ' != \'\' \n'
        c3 += tempos.newTemp() + ' = ' + tp + ' or ' + ts + '\n'
    elif t[1].lower() == 'true' :
        c3 = tempos.newTemp() + ' = ' + t[-3]['tflag'] + ' == False' + '\n'
    elif t[1].lower() == 'false' :
        c3 = tempos.newTemp() + ' = ' + t[-3]['tflag'] + ' == True' + '\n'
    elif t[1].lower() == 'unknown' :
        tp = tempos.newTemp()
        c3 = tempos.newTemp() + ' = ' + t[-3]['tflag'] + ' != \'null\' \n'
        ts = tempos.newTemp()
        c3 += tempos.newTemp() + ' = ' + t[-3]['tflag'] + ' != \'\' \n'
        c3 += tempos.newTemp() + ' = ' + tp + ' or ' + ts + '\n'
    elif t[1].lower() == 'distinct' :
        c3 = tempos.newTemp() + ' = ' + t[-3]['tflag'] + ' == ' + t[3]['tflag'] + '\n'

    t[0] = {'text' : '', 'c3d' : c3, 'tflag' : 't'+str(tempos.index)}

def p_argument_binary(t):
    '''argument : argument MAS argument
                | argument GUION argument
                | argument BARRA argument
                | argument ASTERISCO argument
                | argument PORCENTAJE argument
                | argument POTENCIA argument'''
    c3 = t[1]['c3d']
    c3 += t[3]['c3d']
    c3 += tempos.newTemp() + ' = ' + t[1]['tflag'] + ' ' + t[2] + ' ' + t[3]['tflag'] + '\n'
    t[0] = {'text' : '', 'c3d' : c3, 'tflag' : 't'+str(tempos.index)}

def p_argument_bolano(t):
    'argument : boleano'
    t[0] = t[1]

def p_argument_unary(t):
    '''argument : MAS argument %prec UMAS
                | GUION argument %prec UMENOS'''
    c3 = t[2]['c3d']         
    c3 += tempos.newTemp() + ' = ' + t[1] + ' ' + t[2]['tflag'] + '\n'
    t[0] = {'text' : '', 'c3d' : c3, 'tflag' : 't'+str(tempos.index)}

def p_argument_agrupacion(t):
    '''argument : PARENIZQ argument PARENDER'''
    t[0] = t[2]

def p_argument_entero(t):
    '''argument : ENTERO'''
    t[0] = {'text' : '', 'c3d' : '', 'tflag' : str(t[1])}

def p_argument_decimal(t):
    'argument : DECIMAL'
    t[0] = {'text' : '', 'c3d' : '', 'tflag' : str(t[1])}

def p_argument_cadena(t):
    '''argument : CADENA'''
    t[0] = {'text' : '', 'c3d' : '', 'tflag' : str(t[1])}

def p_argument_id(t):
    '''argument : ID'''
    t[0] = {'text' : '', 'c3d' : '', 'tflag' : t[1]}

def p_argument_idpid(t):
    '''argument : ID PUNTO ID'''
    t[0] = {'text' : '', 'c3d' : '', 'tflag' : 't[1]'}

def p_boleano(t):
    '''boleano  : TRUE
                | FALSE'''
    t[0] = {'text' : '', 'c3d' : '', 'tflag' : str(t[1])}

def p_error(t):
    description = "Error sintactico con: " + t.value
    mistake = error("Sintactico", description, str(t.lineno))
    errores.append(mistake)
    return None

def getMistakes():
    return errores
    errores.clear()

import Librerias.ply.yacc as yacc
parser = yacc.yacc()

def parse(input) :
    return parser.parse(input)
