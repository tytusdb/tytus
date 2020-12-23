import ply.yacc as yacc
import ply.lex as lex
import re
import instrucciones as ins
from graphviz import Digraph
from graphviz import Graph

ast_graph = Digraph(comment='AST', engine='dot')

errores_lexicos = ""        #Variable para concatenar los errores lexicos y luego agregarlos al archivo de errores
errores_sintacticos = ""    #Variable para concatenar los errores sintacticos y luego agregarlos al archivo de errores
cont_error_lexico = 0
cont_error_sintactico = 0
linea = 1
columna = 1
errores = ""                #Variable para concatenar los errores que se mostraran en la consola
base_actual = None
i = 0

def inc_index():
    global i
    i += 1
    return i

# Lista de palabras reservadas
reservadas = {
    'create'        : 'CREATE',
    'type'          : 'TYPE',
    'as'            : 'AS',
    'enum'          : 'ENUM',
    'replace'       : 'REPLACE',
    'database'      : 'DATABASE',
    'if'            : 'IF',
    'not'           : 'NOT',
    'exists'        : 'EXISTS',
    'or'            : 'OR',
    'owner'         : 'OWNER',
    'mode'          : 'MODE',
    'show'          : 'SHOW',
    'like'          : 'LIKE',
    'databases'     : 'DATABASES',
    'rename'        : 'RENAME',
    'currente_user' : 'CURRENT_USER',
    'session_user'  : 'SESSION_USER',
    'text'          : 'TEXT',
    'numeric'       : 'NUMERIC',
    'integer'       : 'INTEGER',
    'alter'         : 'ALTER',
    'to'            : 'TO',
    'drop'          : 'DROP',
    'table'         : 'TABLE',
    'default'       : 'DEFAULT',
    'primary'       : 'PRIMARY',
    'key'           : 'KEY',
    'foreign'       : 'FOREIGN',
    'null'          : 'NULL',
    'constraint'    : 'CONSTRAINT',
    'unique'        : 'UNIQUE',
    'check'         : 'CHECK',
    'references'    : 'REFERENCES',
    'smallint'      : 'SMALLINT',
    'bigint'        : 'BIGINT',
    'decimal'       : 'DECIMAL',
    'real'          : 'REAL',
    'double'        : 'DOUBLE',
    'precision'     : 'PRECISION',
    'money'         : 'MONEY',
    'character'     : 'CHARACTER',
    'varying'       : 'VARYING',
    'varchar'       : 'VARCHAR',
    'char'          : 'CHAR',
    'timestamp'     : 'TIMESTAMP',
    'data'          : 'DATA',
    'time'          : 'TIME',
    'interval'      : 'INTERVAL',
    'with'          : 'WITH',
    'without'       : 'WITHOUT',
    'zone'          : 'ZONE',
    'column'        : 'COLUMN',
    'add'           : 'ADD',
    'delete'        : 'DELETE',
    'from'          : 'FROM',
    'where'         : 'WHERE',
    'insert'        : 'INSERT',
    'into'          : 'INTO',
    'values'        : 'VALUES',
    'update'        : 'UPDATE',
    'set'           : 'SET',
    'and'           : 'AND',
    'sum'           : 'SUM',
    'avg'           : 'AVG',
    'max'           : 'MAX',
    'pi'            : 'PI',
    'power'         : 'POWER',
    'sqrt'          : 'SQRT',
    'select'        : 'SELECT',
    'inner'         : 'INNER',
    'left'          : 'LEFT',
    'right'         : 'RIGHT',
    'full'          : 'FULL',
    'outer'         : 'OUTER',
    'boolean'       : 'BOOLEAN', 
    'off'           : 'OFF', 
    'on'            : 'ON',
    'join'          : 'JOIN',
    'order'         : 'ORDER',
    'by'            : 'BY', 
    'asc'           : 'ASC',
    'desc'          : 'DESC',
    'inherits'      : 'INHERITS',
    'distinct'      : 'DISTINCT',
    'abs'	        : 'ABS',
    'cbrt'	        : 'CBRT',
    'ceil'	        : 'CEIL',
    'ceiling'       : 'CEILING',
    'degrees'	    : 'DEGREES',
    'div'	        : 'DIV',
    'exp'	        : 'EXP',
    'factorial'	    : 'FACTORIAL',
    'floor'	        : 'FLOOR',
    'gcd'	        : 'GCD',
    'ln'	        : 'LN',
    'log'	        : 'LOG',
    'mod'	        : 'MOD',
    'radians'	    : 'RADIANS',
    'round'	        : 'ROUND',
    'sign'	        : 'SIGN',
    'width_bucket'	: 'WIDTH_BUCKET',
    'trunc'	        : 'TRUNC',
    'random'	    : 'RANDOM',
    'extract'	    : 'EXTRACT',
    'year'	        : 'YEAR',
    'month'	        : 'MONTH',
    'day'	        : 'DAY',
    'hour'	        : 'HOUR',
    'minute'	    : 'MINUTE',
    'second'	    : 'SECOND',
    'date_part'	    : 'DATE_PART',
    'sha256'	    : 'SHA256',
    'substr'	    : 'SUBSTR',
    'get_byte'	    : 'GET_BYTE',
    'set_byte'	    : 'SET_BYTE',
    'convert'	    : 'CONVERT',
    'encode'	    : 'ENCODE',
    'decode'	    : 'DECODE',
    'length'	    : 'LENGTH',
    'md5'	        : 'MD5',
    'substring'	    : 'SUBSTRING',
    'trim'	        : 'TRIM',
    'leading'	    : 'LEADING',
    'trailing'	    : 'TRAILING',
    'both'	        : 'BOTH',
    'acos'	        : 'ACOS',
    'acosd'	        : 'ACOSD',
    'asin'	        : 'ASIN',
    'asind'	        : 'ASIND',
    'atan'	        : 'ATAN',
    'atand'	        : 'ATAND',
    'atan2'	        : 'ATAN2',
    'atan2d'	    : 'ATAN2D',
    'cos'	        : 'COS',
    'cosd'	        : 'COSD',
    'cot'	        : 'COT',
    'cotd'	        : 'COTD',
    'sin'	        : 'SIN',
    'sind'	        : 'SIND',
    'tan'	        : 'TAN',
    'tand'	        : 'TAND',
    'sinh'	        : 'SINH',
    'cosh'	        : 'COSH',
    'asinh'	        : 'ASINH',
    'acosh'	        : 'ACOSH',
    'atanh'	        : 'ATANH',
    'use'           : 'USE',
    'now'           : 'NOW',
    'in'            : 'IN',
    'count'         : 'COUNT',
    'true'          : 'TRUE',
    'false'         : 'FALSE',
    'group'         : 'GROUP',
    'by'            : 'BY',
    'current_time'  : 'CURRENT_TIME',
    'current_date'  : 'CURRENT_DATE',
    'between'       : 'BETWEEN',
    'having'        : 'HAVING'
}

# Lista de tokens
tokens = [
    'COMA',
    'PARIZQ',
    'PARDER',
    'PTCOMA',
    'MAYIG',
    'MENIG',
    'DIFEQ',
    'MAYOR',
    'MENOR',
    'IGUAL',
    'MULTI',
    'MENOS',
    'SUMAS',
    'DIVIS',
    'POTEN',
    'CADENA',
    'ID',
    'DECIMA',
    'ENTERO',
    'PUNTO',
    'SQRTROOT',
    'CUBEROOT',
    'BITAND',
    'BITOR',
    'BITXOR',
    'BITNOT',
    'BITSLEFT',
    'BITSRIGHT'
] + list(reservadas.values())

# Expresiones regulares par los tokens
t_COMA = r','
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_PTCOMA = r';'
t_MAYIG = r'>='
t_MENIG = r'<='
t_DIFEQ = r'<>'
t_MAYOR = r'>'
t_MENOR = r'<'
t_IGUAL = r'='
t_MULTI = r'\*'
t_MENOS = r'-'
t_SUMAS = r'\+'
t_DIVIS = r'/'
t_POTEN = r'\^'
t_PUNTO = r'.'
t_SQRTROOT = r'\|/'
t_CUBEROOT = r'\|\|/'
t_BITAND = r'&'
t_BITOR = r'\|'
t_BITXOR = r'#'
t_BITNOT = r'~'
t_BITSLEFT = r'<<'
t_BITSRIGHT = r'>>'

t_ignore = " \t"

def t_COMENTARIO_S(t):
    r'--.*\n'
    global linea, columna
    linea = linea + 1
    columna = 1
    t.lexer.lineno += 1

def t_COMENTARIO_M(t):
    r'/\*(.|\n)*?\*/'
    global linea, columna
    linea = linea + t.value.count('\n')
    columna = 1
    t.lexer.lineno += t.value.count('\n')

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')    # Revisa las palabras reservadas 
     return t

def t_CADENA(t):
    r'([\"]|[\']).*?([\"]|[\'])'
    t.value = t.value[1:-1] # Remueve las comillas
    return t 

def t_DECIMA(t):
    r'\d+[.]\d+'
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

def t_nuevalinea(t):
    r'\n+'
    global linea, columna
    linea = linea + t.value.count('\n')
    columna = 1
    t.lexer.lineno += t.value.count("\n")

# Errores léxicos
def t_error(t):
    global linea, columna
    lex_error(t.value[0], linea, t.lexpos)
    t.lexer.skip(1)


lexer = lex.lex(reflags=re.IGNORECASE)

# Asociación de operadores y precedencia
precedence = (
    ('left','SUMAS','MENOS'),
    ('left','MULTI','DIVIS'),
    ('left','POTEN'),
    ('right','UMENOS', 'USUMAS'),
    ('left','MAYIG','MENIG','IGUAL','DIFEQ','MAYOR','MENOR'),
    ('right','NOT'),
    ('left','AND'),
    ('left','OR'),
    ) 

# Definir gramática

def p_entrada(p):
    '''entrada : entrada create_type
                | entrada create_db
                | entrada show_db
                | entrada alter_db
                | entrada drop_db
                | entrada create_table
                | entrada drop_table
                | entrada alter_table
                | entrada s_delete
                | entrada s_insert
                | entrada s_update
                | entrada select
                | entrada use
                | create_type
                | create_db
                | show_db
                | alter_db 
                | drop_db 
                | create_table
                | drop_table
                | alter_table
                | s_delete
                | s_insert
                | s_update
                | select
                | use'''

    #AST graphviz
    try:

        id = inc_index()
        p[0] = id
        ast_graph.node(str(id),str("entrada"))
        ast_graph.edge(str(id),str(p[1]))

        if p[2] :
            ast_graph.edge(str(id), str(p[2]))

    except IndexError:
        print('')

#region 'Select Analisis'

def p_use(p):
    'use : USE ID PTCOMA'

def p_select(p):
    'select : s_select PTCOMA'

def p_s_select(p):
    '''s_select : SELECT list_cols FROM list_from 
                | SELECT list_cols FROM list_from list_conditions 
                | SELECT list_cols FROM list_from list_order 
                | SELECT list_cols FROM list_from list_joins 
                | SELECT list_cols FROM list_from list_conditions list_order 
                | SELECT list_cols FROM list_from list_joins list_conditions 
                | SELECT list_cols FROM list_from list_joins list_order 
                | SELECT list_cols FROM list_from list_joins list_conditions list_order
                | SELECT list_cols
                | SELECT list_cols FROM list_from group_by
                | SELECT list_cols FROM list_from list_conditions group_by
                | SELECT list_cols FROM list_from group_by list_order 
                | SELECT list_cols FROM list_from list_joins group_by
                | SELECT list_cols FROM list_from list_conditions group_by list_order 
                | SELECT list_cols FROM list_from list_joins list_conditions group_by
                | SELECT list_cols FROM list_from list_joins group_by list_order 
                | SELECT list_cols FROM list_from list_joins list_conditions group_by list_order
                
                | SELECT list_cols FROM list_from group_by having
                | SELECT list_cols FROM list_from list_conditions group_by having
                | SELECT list_cols FROM list_from group_by list_order having
                | SELECT list_cols FROM list_from list_joins group_by having
                | SELECT list_cols FROM list_from list_conditions group_by list_order having
                | SELECT list_cols FROM list_from list_joins list_conditions group_by having
                | SELECT list_cols FROM list_from list_joins group_by list_order having
                | SELECT list_cols FROM list_from list_joins list_conditions group_by list_order having
                | SELECT list_cols FROM list_from list_conditions having
                | SELECT list_cols FROM list_from list_conditions list_order having
                | SELECT list_cols FROM list_from list_joins list_conditions having
                | SELECT list_cols FROM list_from list_joins list_conditions list_order having'''
    
    #AST graphviz
    try:
        id = inc_index()
        p[0] = id
        ast_graph.node(str(id),str("Select Statement"))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[1]))
        ast_graph.edge(str(id), str(id2))

        ast_graph.edge(str(id), str(p[2]))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[3]))
        ast_graph.edge(str(id), str(id2))

        ast_graph.edge(str(id), str(p[4]))

        if type(p[5]) == int:
            ast_graph.edge(str(id), str(p[5]))
        else:
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[5]))
            ast_graph.edge(str(id), str(id2))

        if type(p[6]) == int:
            ast_graph.edge(str(id), str(p[6]))
        else:
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[6]))
            ast_graph.edge(str(id), str(id2))
        
        if type(p[7]) == int:
            ast_graph.edge(str(id), str(p[7]))
        else:
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[7]))
            ast_graph.edge(str(id), str(id2))

        if type(p[8]) == int:
            ast_graph.edge(str(id), str(p[8]))
        else:
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[8]))
            ast_graph.edge(str(id), str(id2))
        
    except IndexError:
        print('')

def p_having(p):
    '''having : HAVING expresion'''

def p_instrucciones_comp(p):
    '''instrucciones_comp : instrucciones_comp list_conditions
                          | instrucciones_comp list_order
                          | instrucciones_comp list_joins
                          | instrucciones_comp group_by
                          | list_conditions
                          | list_order
                          | list_joins
                          | group_by'''

def p_group_by(p):
    '''group_by : GROUP BY list_alias'''

def p_list_cols(p):
    '''list_cols :  DISTINCT list_alias
                  | MULTI
                  | list_alias'''
    
    #AST graphviz
    try:
        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('select list'))

        if type(p[1]) == int:
            ast_graph.edge(str(id), str(p[1]))
        else:
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[1]))
            ast_graph.edge(str(id), str(id2))

        if p[2] :
            ast_graph.edge(str(id), str(p[2]))

    except IndexError:
        print('out of range')
    


def p_list_alias(p):
    '''list_alias : list_alias COMA sel_id
                  | sel_id'''
    
    #AST graphviz
    try: 
        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('select id'))

        if type(p[1]) == int:
            ast_graph.edge(str(id), str(p[1]))
        
        id2 = inc_index()
        ast_graph.node(str(id2), str(p[2]))
        ast_graph.edge(str(id), str(id2))

        if p[3]:
            ast_graph.edge(str(id), str(p[3]))

    except IndexError:
        print('')

def p_sel_id(p):
    ''' sel_id : expresion PUNTO ID AS ID
                  | ID PUNTO MULTI
                  | expresion AS ID
                  | expresion
                  | expresion ID'''

    #AST graphviz
    try:

        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('id'))

        if p[1] :
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[1]))
            ast_graph.edge(str(id), str(id2))

        if p[2] :
            id3 = inc_index()
            ast_graph.node(str(id3), str(p[2]))
            ast_graph.edge(str(id), str(id3))

        if p[3] :
            id4 = inc_index()
            ast_graph.node(str(id4), str(p[3]))
            ast_graph.edge(str(id), str(id4))

        if p[4] :
            id5 = inc_index()
            ast_graph.node(str(id5), str(p[4]))
            ast_graph.edge(str(id), str(id5))

        if p[5] :
            id6 = inc_index()
            ast_graph.node(str(id6), str(p[5]))
            ast_graph.edge(str(id), str(id6))

    
    except IndexError:
        print('')

def p_list_from(p):
    '''list_from :  list_from COMA from_id
                  | from_id'''
    
    #AST graphviz
    try:
        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('from list'))

        if type(p[1]) == int:
            ast_graph.edge(str(id), str(p[1]))
            
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[2]))
            ast_graph.edge(str(id), str(id2))

            ast_graph.edge(str(id), str(p[3]))

        else:
            ast_graph.edge(str(id), str(p[1]))


    except IndexError:
        print('')

def p_from_id(p):
    '''from_id : ID ID
                | ID'''

    #AST graphviz
    try:
        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('from id'))

        if p[1] :
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[1]))
            ast_graph.edge(str(id), str(id2))
        if p[2] :
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[2]))
            ast_graph.edge(str(id), str(id2))
        if p[3] :
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[3]))
            ast_graph.edge(str(id), str(id2))
    except IndexError:
        print('')

    

def p_list_joins(p):                            #Se agregaron las últimas 5 produciones para que acepten alias
    '''list_joins : list_joins join_type JOIN ID join_conditions 
                  | list_joins JOIN ID join_conditions 
                  | join_type JOIN ID join_conditions
                  | JOIN ID join_conditions
                  | JOIN ID
                  | list_joins join_type JOIN ID ID join_conditions 
                  | list_joins JOIN ID ID join_conditions
                  | join_type JOIN ID ID join_conditions
                  | JOIN ID ID join_conditions
                  | JOIN ID ID'''
    
    #AST graphviz
    try:
        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('join list'))

        if type(p[1]) == int :
            ast_graph.edge(str(id), str(p[1]))
        else:
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[1]))
            ast_graph.edge(str(id), str(id2))

        if type(p[2]) == int:
            ast_graph.edge(str(id), str(p[2]))
        else:
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[2]))
            ast_graph.edge(str(id), str(id2))

        if type(p[3]) == int:
            ast_graph.edge(str(id), str(p[3]))
        else:
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[3]))
            ast_graph.edge(str(id), str(id2))

        if type(p[4]) == int:
            ast_graph.edge(str(id), str(p[4]))
        else:
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[4]))
            ast_graph.edge(str(id), str(id2))

        ast_graph.edge(str(id), str(p[5]))

    except IndexError:
        print('')

    


def p_join_type(p):
    '''join_type : LEFT OUTER
                 | RIGHT OUTER
                 | FULL OUTER
                 | LEFT
                 | RIGHT
                 | FULL
                 | INNER'''
    #AST graphviz
    try:
        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('join type'))

        if p[1] :
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[1]))
            ast_graph.edge(str(id), str(id2))
        
        if p[2] :
            id3 = inc_index()
            ast_graph.node(str(id3), str(p[2]))
            ast_graph.edge(str(id), str(id3))

    except IndexError:
        print('')


def p_join_conditions(p):
    '''join_conditions : ON expresion'''
    #AST graphviz
    try:

        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('join conditions'))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[1]))
        ast_graph.edge(str(id), str(id2))

        ast_graph.edge(str(id), str(p[2]))

    except IndexError:
        print('')


def p_list_conditions(p):
    '''list_conditions : WHERE expresion
                       | WHERE ID expresion'''

    #AST graphviz
    try:

        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('list conditions'))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[1]))
        ast_graph.edge(str(id), str(id2))

        ast_graph.edge(str(id), str(p[2]))

    except IndexError:
        print('')

def p_list_order(p):
    '''list_order : ORDER BY expresion ASC
                  | ORDER BY expresion DESC
                  | ORDER BY expresion'''

    #AST graphviz
    try:
        id = inc_index()
        p[0] = id

        ast_graph.node(str(id), str('order'))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[1]))
        ast_graph.edge(str(id), str(id2))
        id3 = inc_index()
        ast_graph.node(str(id3), str(p[2]))
        ast_graph.edge(str(id), str(id3))
        id4 = inc_index()
        ast_graph.node(str(id4), str(p[3]))
        ast_graph.edge(str(id), str(id4))
        id5 = inc_index()
        ast_graph.node(str(id5), str(p[4]))
        ast_graph.edge(str(id), str(id5))
    except IndexError:
        print('')

#end region 

def p_create_type(p):
    'create_type : CREATE TYPE ID AS ENUM PARIZQ lista1 PARDER PTCOMA'

    #AST graphviz
    try:
        id = inc_index()
        p[0] = id

        ast_graph.node(str(id), str('Create Statement'))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[1]))
        ast_graph.edge(str(id), str(id2))

        id3 = inc_index()
        ast_graph.node(str(id3), str(p[2]))
        ast_graph.edge(str(id), str(id3))

        id4 = inc_index()
        ast_graph.node(str(id4), str(p[3]))
        ast_graph.edge(str(id), str(id4))

        id5 = inc_index()
        ast_graph.node(str(id5), str(p[4]))
        ast_graph.edge(str(id), str(id5))

        id6 = inc_index()
        ast_graph.node(str(id6), str(p[5]))
        ast_graph.edge(str(id), str(id6))

        id7 = inc_index()
        ast_graph.node(str(id7), str(p[6]))
        ast_graph.edge(str(id), str(id7))

        ast_graph.edge(str(id), str(p[7]))

        id8 = inc_index()
        ast_graph.node(str(id8), str(p[8]))
        ast_graph.edge(str(id), str(id8))

        id9 = inc_index()
        ast_graph.node(str(id9), str(p[9]))
        ast_graph.edge(str(id), str(id9))

    except IndexError:
        print('')

    

def p_lista1(p):
    '''lista1 : lista1 COMA CADENA
            | CADENA'''
    
    #AST Graphviz
    try:
        id = inc_index()
        p[0] = id

        ast_graph.node(str(id), str('lista cadena'))

        if type(p[1]) == int:
            ast_graph.edge(str(id), str(p[1]))
        else:
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[1]))
            ast_graph.edge(str(id), str(id2))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[2]))
        ast_graph.edge(str(id), str(id2))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[3]))
        ast_graph.edge(str(id), str(id2))
    
    except IndexError:
        print('')

def p_data_type(p):
    '''data_type : NUMERIC
            | INTEGER
            | TEXT
            | SMALLINT 
            | BIGINT
            | DECIMAL
            | DECIMAL PARIZQ ENTERO COMA ENTERO PARDER
            | REAL
            | DOUBLE PRECISION
            | MONEY
            | CHARACTER VARYING PARIZQ ENTERO PARDER
            | VARCHAR PARIZQ ENTERO PARDER
            | CHARACTER PARIZQ ENTERO PARDER
            | CHAR PARIZQ ENTERO PARDER
            | TIMESTAMP
            | TIMESTAMP time_zone
            | DATA
            | TIME
            | TIME time_zone
            | BOOLEAN
            | INTERVAL
            | ID'''
    try:
        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('data type'))

        if p[1] == 'timestamp': 
            ast_graph.edge(str(id), str(p[2]))
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[1]))
            ast_graph.edge(str(id), str(id2))
        elif p[1] == 'time':
            ast_graph.edge(str(id), str(p[2]))
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[1]))
            ast_graph.edge(str(id), str(id2))
        else :    
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[1]))
            ast_graph.edge(str(id), str(id2))

    except IndexError:
        print('')

    

def p_time_zone(p):
    '''time_zone    : WITH TIME ZONE
                    | WITHOUT TIME ZONE'''

    try:

        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('time zone'))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[1]))
        ast_graph.edge(str(id), str(id2))

        id3 = inc_index()
        ast_graph.node(str(id3), str(p[1]))
        ast_graph.edge(str(id), str(id3))

        id4 = inc_index()
        ast_graph.node(str(id4), str(p[1]))
        ast_graph.edge(str(id), str(id4))

    except IndexError:
        print('')

def p_create_db(p):
    '''create_db : CREATE DATABASE c_db PTCOMA
                 | CREATE OR REPLACE DATABASE c_db PTCOMA'''

    try:

        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('create statement'))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[1]))
        ast_graph.edge(str(id), str(id2))

        id3 = inc_index()
        ast_graph.node(str(id3), str(p[2]))
        ast_graph.edge(str(id), str(id3))

        if type(p[3]) == int:
            ast_graph.edge(str(id), str(p[3]))
        else:
            id4 = inc_index()
            ast_graph.node(str(id4), str(p[3]))
            ast_graph.edge(str(id), str(id4))

        id5 = inc_index()
        ast_graph.node(str(id5), str(p[4]))
        ast_graph.edge(str(id), str(id5))

        ast_graph.edge(str(id), str(p[5]))

        id6 = inc_index()
        ast_graph.node(str(id6), str(p[6]))
        ast_graph.edge(str(id), str(id6))

    except IndexError:
        print('')


def p_c_db(p):
    '''c_db : IF NOT EXISTS c_db1
            | c_db1'''

    try:

        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('db exist'))

        if p[2] :
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[1]))
            ast_graph.edge(str(id), str(id2))

            id3 = inc_index()
            ast_graph.node(str(id3), str(p[2]))
            ast_graph.edge(str(id), str(id3))

            id4 = inc_index()
            ast_graph.node(str(id4), str(p[3]))
            ast_graph.edge(str(id), str(id4))

            ast_graph.edge(str(id), str(p[4]))
        
        else :

            ast_graph.edge(str(id), str(p[1]))

    except IndexError:
        print('')

def p_c_db1(p):
    '''c_db1 : ID owner_mode
             | ID'''

    try: 
        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('db owner'))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[1]))
        ast_graph.edge(str(id), str(id2))

        if p[2] :
            ast_graph.edge(str(id), str(p[2]))
    except IndexError:
        print('')


def p_owner_mode(p):
    '''owner_mode : owner_mode OWNER igual_id 
                  | owner_mode MODE igual_int
                  | OWNER igual_id 
                  | MODE igual_int'''

    try:
        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('owner mode'))

        if p[3] :
            ast_graph.edge(str(id), str(p[1]))

            id2 = inc_index()
            ast_graph.node(str(id2), str(p[2]))
            ast_graph.edge(str(id), str(id2))

            ast_graph.edge(str(id), str(p[3]))
        
        else :
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[1]))
            ast_graph.edge(str(id), str(id2))

            ast_graph.edge(str(id), str(p[2]))

    except IndexError:
        print('')

def p_igual_id(p):
    '''igual_id : IGUAL expresion
                | expresion'''

    try:

        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('igual'))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[1]))
        ast_graph.edge(str(id), str(id2))

        if p[2]:
            id3 = inc_index()
            ast_graph.node(str(id3), str(p[2]))
            ast_graph.edge(str(id), str(id3))

    except IndexError:
        print('')

def p_igual_int(p):
    '''igual_int : IGUAL ENTERO
                | ENTERO'''
    try:

        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('igual entero'))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[1]))
        ast_graph.edge(str(id), str(id2))

        if p[2]:
            id3 = inc_index()
            ast_graph.node(str(id3), str(p[2]))
            ast_graph.edge(str(id), str(id3))

    except IndexError:
        print('')

def p_show_db(p):
    '''show_db : SHOW DATABASES PTCOMA'''

    try:
        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('Show Statement'))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[1]))
        ast_graph.edge(str(id), str(id2))

        id3 = inc_index()
        ast_graph.node(str(id3), str(p[2]))
        ast_graph.edge(str(id), str(id3))

        id4 = inc_index()
        ast_graph.node(str(id4), str(p[3]))
        ast_graph.edge(str(id), str(id4))
    except IndexError:
        print('')

def p_alter_db(p):
    '''alter_db : ALTER DATABASE ID al_db PTCOMA'''

    try: 
        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('Alter Statement'))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[1]))
        ast_graph.edge(str(id), str(id2))

        id3 = inc_index()
        ast_graph.node(str(id3), str(p[2]))
        ast_graph.edge(str(id), str(id3))

        id4 = inc_index()
        ast_graph.node(str(id4), str(p[3]))
        ast_graph.edge(str(id), str(id4))

        ast_graph.edge(str(id), str(p[4]))

        id5 = inc_index()
        ast_graph.node(str(id5), str(p[5]))
        ast_graph.edge(str(id), str(id5))

    except IndexError:
        print('')
     

def p_al_db(p):
    '''al_db : RENAME TO ID
            | OWNER TO owner_db'''
    
    try:
        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('Alter db'))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[1]))
        ast_graph.edge(str(id), str(id2))

        id3 = inc_index()
        ast_graph.node(str(id3), str(p[2]))
        ast_graph.edge(str(id), str(id3))

        if type(p[3]) == int: 
            ast_graph.edge(str(id), str(p[3]))
        else:
            id4 = inc_index()
            ast_graph.node(str(id4), str(p[3]))
            ast_graph.edge(str(id), str(id4))

    except IndexError:
        print('')

def p_owner_db(p):
    '''owner_db : ID
                | CURRENT_USER
                | SESSION_USER'''
    
    try:
        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('Owner db'))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[1]))
        ast_graph.edge(str(id), str(id2))

    except IndexError:
        print('')

def p_drop_db(p):
    '''drop_db  : DROP DATABASE ID PTCOMA
                | DROP DATABASE IF EXISTS ID PTCOMA'''

    try: 
        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('Drop Statement'))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[1]))
        ast_graph.edge(str(id), str(id2))

        id3 = inc_index()
        ast_graph.node(str(id3), str(p[2]))
        ast_graph.edge(str(id), str(id3))

        id4 = inc_index()
        ast_graph.node(str(id4), str(p[3]))
        ast_graph.edge(str(id), str(id4))

        id5 = inc_index()
        ast_graph.node(str(id5), str(p[4]))
        ast_graph.edge(str(id), str(id5))

        if p[5] :
            id6 = inc_index()
            ast_graph.node(str(id6), str(p[5]))
            ast_graph.edge(str(id), str(id6))

        if p[6] :
            id7 = inc_index()
            ast_graph.node(str(id7), str(p[6]))
            ast_graph.edge(str(id), str(id7))

    except IndexError:
        print('')

def p_create_table(p): 
    '''create_table   : CREATE TABLE ID PARIZQ colum_list PARDER PTCOMA
                      | CREATE TABLE ID PARIZQ colum_list PARDER INHERITS PARIZQ ID PARDER PTCOMA
                      | CREATE TABLE ID PARIZQ colum_list COMA const_keys PARDER PTCOMA
                      | CREATE TABLE ID PARIZQ colum_list COMA const_keys PARDER INHERITS PARIZQ ID PARDER PTCOMA'''

    try: 

        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('Create Table Statement'))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[1]))
        ast_graph.edge(str(id), str(id2))

        id3 = inc_index()
        ast_graph.node(str(id3), str(p[2]))
        ast_graph.edge(str(id), str(id3))

        id4 = inc_index()
        ast_graph.node(str(id4), str(p[3]))
        ast_graph.edge(str(id), str(id4))

        id5 = inc_index()
        ast_graph.node(str(id5), str(p[4]))
        ast_graph.edge(str(id), str(id5))

        ast_graph.edge(str(id), str(p[5]))

        id7 = inc_index()
        ast_graph.node(str(id7), str(p[6]))
        ast_graph.edge(str(id), str(id7))

        id8 = inc_index()
        ast_graph.node(str(id8), str(p[7]))
        ast_graph.edge(str(id), str(id8))

        if p[8] :
            id9 = inc_index()
            ast_graph.node(str(id9), str(p[8]))
            ast_graph.edge(str(id), str(id9))

        if p[9] :
            id10 = inc_index()
            ast_graph.node(str(id10), str(p[9]))
            ast_graph.edge(str(id), str(id10))

        if p[10] :
            id11 = inc_index()
            ast_graph.node(str(id11), str(p[10]))
            ast_graph.edge(str(id), str(id11))

        if p[11] :
            id12 = inc_index()
            ast_graph.node(str(id12), str(p[11]))
            ast_graph.edge(str(id), str(id12))

    except IndexError:
        print('')

def p_colum_list(p):
    '''colum_list   : colum_list COMA ID data_type 
                    | colum_list COMA ID data_type const
                    | ID data_type
                    | ID data_type const'''

    try:

        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('Column List'))

        if type(p[1]) == int :
            ast_graph.edge(str(id), str(p[1]))

            id2 = inc_index()
            ast_graph.node(str(id2), str(p[2]))
            ast_graph.edge(str(id), str(id2))

            id3 = inc_index()
            ast_graph.node(str(id3), str(p[3]))
            ast_graph.edge(str(id), str(id3))

            id4 = inc_index()
            ast_graph.node(str(id4), str(p[4]))
            ast_graph.edge(str(id), str(id4))

            ast_graph.edge(str(id), str(p[5]))

            if p[6]:
                id5 = inc_index()
                ast_graph.node(str(id5), str(p[6]))
                ast_graph.edge(str(id), str(id5))

        else:  
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[1]))
            ast_graph.edge(str(id), str(id2))  

            ast_graph.edge(str(id), str(p[2]))

            if p[3]:
                ast_graph.edge(str(id), str(p[3]))

    except IndexError:
        print('')

def p_const_keys(p):
    '''const_keys   : const_keys COMA CONSTRAINT ID PRIMARY KEY PARIZQ lista_id PARDER
                    | const_keys COMA CONSTRAINT ID FOREIGN KEY PARIZQ ID PARDER REFERENCES ID PARIZQ ID PARDER
                    | const_keys COMA PRIMARY KEY PARIZQ lista_id PARDER
                    | const_keys COMA FOREIGN KEY PARIZQ ID PARDER REFERENCES ID PARIZQ ID PARDER
                    | CONSTRAINT ID PRIMARY KEY PARIZQ lista_id PARDER
                    | CONSTRAINT ID FOREIGN KEY PARIZQ ID PARDER REFERENCES ID PARIZQ ID PARDER
                    | PRIMARY KEY PARIZQ lista_id PARDER
                    | FOREIGN KEY PARIZQ ID PARDER REFERENCES ID PARIZQ ID PARDER'''

    try:

        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('Const Keys'))

        if type(p[1]) == int :
            ast_graph.edge(str(id), str(p[1]))

            id2 = inc_index()
            ast_graph.node(str(id2), str(p[2]))
            ast_graph.edge(str(id), str(id2))

            id3 = inc_index()
            ast_graph.node(str(id3), str(p[3]))
            ast_graph.edge(str(id), str(id3))

            id4 = inc_index()
            ast_graph.node(str(id4), str(p[4]))
            ast_graph.edge(str(id), str(id4))

            id5 = inc_index()
            ast_graph.node(str(id5), str(p[5]))
            ast_graph.edge(str(id), str(id5))

            ast_graph.edge(str(id), str(p[6]))

            id6 = inc_index()
            ast_graph.node(str(id6), str(p[7]))
            ast_graph.edge(str(id), str(id6))

            if p[8]:
                id7 = inc_index()
                ast_graph.node(str(id7), str(p[8]))
                ast_graph.edge(str(id), str(id7))

            if p[9]:
                id8 = inc_index()
                ast_graph.node(str(id8), str(p[9]))
                ast_graph.edge(str(id), str(id8))

            if p[10]:
                id9 = inc_index()
                ast_graph.node(str(id9), str(p[10]))
                ast_graph.edge(str(id), str(id9))

            if p[11]:
                ast_graph.edge(str(id), str(p[11]))

            if p[12]:
                id10 = inc_index()
                ast_graph.node(str(id10), str(p[12]))
                ast_graph.edge(str(id), str(id10))
        
        else:

            id2 = inc_index()
            ast_graph.node(str(id2), str(p[1]))
            ast_graph.edge(str(id), str(id2))

            id3 = inc_index()
            ast_graph.node(str(id3), str(p[2]))
            ast_graph.edge(str(id), str(id3))

            id4 = inc_index()
            ast_graph.node(str(id4), str(p[3]))
            ast_graph.edge(str(id), str(id4))

            ast_graph.edge(str(id), str(p[4]))

            id5 = inc_index()
            ast_graph.node(str(id5), str(p[5]))
            ast_graph.edge(str(id), str(id5))

            if p[6]:
                id6 = inc_index()
                ast_graph.node(str(id6), str(p[6]))
                ast_graph.edge(str(id), str(id6))

            if p[7]:
                id7 = inc_index()
                ast_graph.node(str(id7), str(p[7]))
                ast_graph.edge(str(id), str(id7))

            if p[8]:
                id8 = inc_index()
                ast_graph.node(str(id8), str(p[8]))
                ast_graph.edge(str(id), str(id8))

            if p[9]:
                ast_graph.edge(str(id), str(p[9]))

    except IndexError:
        print('')


def p_const(p):
    '''const    : const DEFAULT expresion
                | const NOT NULL
                | const NULL
                | const CONSTRAINT ID  UNIQUE
                | const CONSTRAINT ID  UNIQUE PARIZQ lista_id PARDER
                | const UNIQUE
                | const CONSTRAINT ID CHECK PARIZQ expresion PARDER
                | const CHECK PARIZQ expresion PARDER
                | const PRIMARY KEY
                | const REFERENCES ID PARIZQ lista_id PARDER
                | DEFAULT expresion
                | NOT NULL
                | NULL
                | CONSTRAINT ID UNIQUE
                | CONSTRAINT ID  UNIQUE PARIZQ lista_id PARDER
                | UNIQUE
                | CONSTRAINT ID CHECK PARIZQ expresion PARDER
                | CHECK PARIZQ expresion PARDER
                | PRIMARY KEY
                | REFERENCES ID PARIZQ lista_id PARDER'''

    try:

        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('Constant'))

    except IndexError:
        print('')

def p_lista_id(p):
    '''lista_id : lista_id COMA ID
                | ID'''

    try: 
        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('ID List'))

        if type(p[1]) == int :
            ast_graph.edge(str(id), str(p[1]))

            id2 = inc_index()
            ast_graph.node(str(id2), str(p[2]))
            ast_graph.edge(str(id), str(id2))

            id3 = inc_index()
            ast_graph.node(str(id3), str(p[3]))
            ast_graph.edge(str(id), str(id3))

        else:
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[1]))
            ast_graph.edge(str(id), str(id2))

    except IndexError:
        print('')

def p_drop_table(p):
    'drop_table : DROP TABLE ID PTCOMA'

    try:
        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('ID List'))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[1]))
        ast_graph.edge(str(id), str(id2))

        id3 = inc_index()
        ast_graph.node(str(id3), str(p[2]))
        ast_graph.edge(str(id), str(id3))

        id4 = inc_index()
        ast_graph.node(str(id4), str(p[3]))
        ast_graph.edge(str(id), str(id4))

        id5 = inc_index()
        ast_graph.node(str(id5), str(p[4]))
        ast_graph.edge(str(id), str(id5))
    except IndexError:
        print('')

def p_alter_table(p):
    'alter_table    : ALTER TABLE ID acciones PTCOMA'
    try:
        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('ID List'))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[1]))
        ast_graph.edge(str(id), str(id2))

        id3 = inc_index()
        ast_graph.node(str(id3), str(p[2]))
        ast_graph.edge(str(id), str(id3))

        id4 = inc_index()
        ast_graph.node(str(id4), str(p[3]))
        ast_graph.edge(str(id), str(id4))

        ast_graph.edge(str(id), str(p[4]))

        id5 = inc_index()
        ast_graph.node(str(id5), str(p[5]))
        ast_graph.edge(str(id), str(id5))

    except IndexError:
        print('')

def p_acciones(p):
    '''acciones : ADD acc
                | ADD COLUMN ID data_type
                | ALTER COLUMN ID TYPE data_type
                | ALTER COLUMN ID SET const
                | DROP CONSTRAINT ID
                | DROP COLUMN ID
                | RENAME COLUMN ID TO ID'''

    try:

        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('accions'))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[1]))
        ast_graph.edge(str(id), str(id2))

        if type(p[2]) == int:
            ast_graph.edge(str(id), str(p[2]))
        else :
            id3 = inc_index()
            ast_graph.node(str(id3), str(p[2]))
            ast_graph.edge(str(id), str(id3))

        id4 = inc_index()
        ast_graph.node(str(id4), str(p[3]))
        ast_graph.edge(str(id), str(id4))

        if type(p[4]) == int:
            ast_graph.edge(str(id), str(p[4]))
        else :
            id4 = inc_index()
            ast_graph.node(str(id4), str(p[4]))
            ast_graph.edge(str(id), str(id4))

        if type(p[5]) == int:
            ast_graph.edge(str(id), str(p[5]))
        else :
            id5 = inc_index()
            ast_graph.node(str(id5), str(p[5]))
            ast_graph.edge(str(id), str(id5))

    except IndexError:
        print('')

def p_acc(p):
    '''acc  : const
            | const_keys'''

    try:

        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('acc'))

        ast_graph.edge(str(id), str(p[1]))

    except IndexError:
        print('')

def p_delete(p):
    '''s_delete : DELETE FROM ID PTCOMA
                | DELETE FROM ID WHERE expresion PTCOMA '''

    try:

        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('ID List'))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[1]))
        ast_graph.edge(str(id), str(id2))

        id3 = inc_index()
        ast_graph.node(str(id3), str(p[2]))
        ast_graph.edge(str(id), str(id3))

        id4 = inc_index()
        ast_graph.node(str(id4), str(p[3]))
        ast_graph.edge(str(id), str(id4))

        id5 = inc_index()
        ast_graph.node(str(id5), str(p[4]))
        ast_graph.edge(str(id), str(id5))

        ast_graph.edge(str(id), str(p[5]))

        id6 = inc_index()
        ast_graph.node(str(id6), str(p[6]))
        ast_graph.edge(str(id), str(id6))

    except IndexError:
        print('')

def p_insert(p):
    '''s_insert : INSERT INTO ID PARIZQ lista_id PARDER VALUES lista_values PTCOMA
                | INSERT INTO ID VALUES lista_values PTCOMA '''
                #| INSERT INTO ID PARIZQ lista_id PARDER s_select
                #| INSERT INTO ID s_select''' 

    try:

        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('Insert Statement'))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[1]))
        ast_graph.edge(str(id), str(id2))

        id3 = inc_index()
        ast_graph.node(str(id3), str(p[2]))
        ast_graph.edge(str(id), str(id3))

        id4 = inc_index()
        ast_graph.node(str(id4), str(p[3]))
        ast_graph.edge(str(id), str(id4))

        id5 = inc_index()
        ast_graph.node(str(id5), str(p[4]))
        ast_graph.edge(str(id), str(id5))

        ast_graph.edge(str(id), str(p[5]))

        id6 = inc_index()
        ast_graph.node(str(id6), str(p[6]))
        ast_graph.edge(str(id), str(id6))

        id7 = inc_index()
        ast_graph.node(str(id7), str(p[7]))
        ast_graph.edge(str(id), str(id7))

        ast_graph.edge(str(id), str(p[8]))

        id8 = inc_index()
        ast_graph.node(str(id8), str(p[9]))
        ast_graph.edge(str(id), str(id8))

    except IndexError:
        print('')

def p_lista_values(p):
    '''lista_values : lista_values COMA PARIZQ lista_valores PARDER
                     | PARIZQ lista_valores PARDER'''

    try:

        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('Value List'))

        if type(p[1]) == int:
            ast_graph.edge(str(id), str(p[1]))
        else:
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[1]))
            ast_graph.edge(str(id), str(id2))

        if type(p[2]) == int:
            ast_graph.edge(str(id), str(p[2]))
        else:
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[2]))
            ast_graph.edge(str(id), str(id2))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[3]))
        ast_graph.edge(str(id), str(id2))

        ast_graph.edge(str(id), str(p[4]))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[5]))
        ast_graph.edge(str(id), str(id2))


    except IndexError:
        print('')

def p_lista_valores(p):
    '''lista_valores : lista_valores COMA expresion
                     | expresion'''
    
    try:

        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('Values List'))
        
        ast_graph.edge(str(id), str(p[1]))

        if p[2]:
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[2]))
            ast_graph.edge(str(id), str(id2))

        if p[3]:
            ast_graph.edge(str(id), str(p[3]))

    except IndexError:
        print('')

def p_s_update(p):
    '''s_update : UPDATE ID SET lista_asig PTCOMA
                | UPDATE ID SET lista_asig WHERE expresion PTCOMA'''

    try:

        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('Values List'))

        id2 = inc_index()
        ast_graph.node(str(id2), str(p[1]))
        ast_graph.edge(str(id), str(id2))

        id3 = inc_index()
        ast_graph.node(str(id3), str(p[2]))
        ast_graph.edge(str(id), str(id3))

        id4 = inc_index()
        ast_graph.node(str(id4), str(p[3]))
        ast_graph.edge(str(id), str(id4))

        ast_graph.edge(str(id), str(p[4]))

        id5 = inc_index()
        ast_graph.node(str(id5), str(p[5]))
        ast_graph.edge(str(id), str(id5))

        if p[6]:
            ast_graph.edge(str(id), str(p[6]))

        id6 = inc_index()
        ast_graph.node(str(id6), str(p[7]))
        ast_graph.edge(str(id), str(id6))

    except IndexError:
        print('')

def p_lista_asig(p):
    '''lista_asig : lista_asig COMA ID IGUAL expresion
                  | ID IGUAL expresion'''

    try:

        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('List Asig'))

        if type(p[1]) == int :
            ast_graph.edge(str(id), str(p[1]))

            id2 = inc_index()
            ast_graph.node(str(id2), str(p[2]))
            ast_graph.edge(str(id), str(id2))

            id3 = inc_index()
            ast_graph.node(str(id3), str(p[3]))
            ast_graph.edge(str(id), str(id3))

            id4 = inc_index()
            ast_graph.node(str(id4), str(p[4]))
            ast_graph.edge(str(id), str(id4))

            ast_graph.edge(str(id), str(p[5]))

        else :

            id2 = inc_index()
            ast_graph.node(str(id2), str(p[1]))
            ast_graph.edge(str(id), str(id2))

            id3 = inc_index()
            ast_graph.node(str(id3), str(p[2]))
            ast_graph.edge(str(id), str(id3))

            ast_graph.edge(str(id), str(p[3]))

    except IndexError:
        print('')


def p_expresion(p):
    '''expresion : NOT expresion
                 | IN expresion
                 | EXISTS expresion
                 | expresion OR expresion
                 | expresion AND expresion
                 | expresion MAYOR expresion
                 | expresion MENOR expresion
                 | expresion MAYIG expresion
                 | expresion MENIG expresion
                 | expresion IGUAL expresion
                 | expresion DIFEQ expresion
                 | MENOS expresion %prec UMENOS
                 | SUMAS expresion %prec USUMAS
                 | expresion POTEN expresion
                 | expresion MULTI expresion
                 | expresion DIVIS expresion
                 | expresion SUMAS expresion
                 | expresion MENOS expresion
                 | PARIZQ expresion PARDER
                 | SUM PARIZQ expresion PARDER
                 | AVG PARIZQ expresion PARDER
                 | MAX PARIZQ expresion PARDER
                 | COUNT PARIZQ MULTI PARDER
                 | COUNT PARIZQ expresion PARDER
                 | expresion BETWEEN expresion
                 | ID
                 | CADENA
                 | ENTERO
                 | DECIMA
                 | ID PUNTO ID
                 | CURRENT_DATE
                 | CURRENT_TIME
                 | temp_exp expresion
                 | SQRTROOT expresion
                 | CUBEROOT expresion
                 | BITAND expresion
                 | BITOR expresion
                 | BITXOR expresion
                 | BITNOT expresion
                 | BITSLEFT expresion
                 | BITSRIGHT expresion
                 | math_sw
                 | math_select
                 | trigonometric
                 | ext
                 | d_part
                 | now
                 | binary_string
                 | s_select
                 | booleanos'''

    try:

        id = inc_index()
        p[0] = id
        ast_graph.node(str(id), str('Expresion'))

        if type(p[1]) == int:
            ast_graph.edge(str(id), str(p[1]))
        else:
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[1]))
            ast_graph.edge(str(id), str(id2))

        if type(p[2]) == int:
            ast_graph.edge(str(id), str(p[2]))
        else:
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[2]))
            ast_graph.edge(str(id), str(id2))

        if type(p[3]) == int:
            ast_graph.edge(str(id), str(p[3]))
        else:
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[3]))
            ast_graph.edge(str(id), str(id2))

        if type(p[4]) == int:
            ast_graph.edge(str(id), str(p[4]))
        else:
            id2 = inc_index()
            ast_graph.node(str(id2), str(p[4]))
            ast_graph.edge(str(id), str(id2))
    
    except IndexError:
        print('')

def p_booleanos(p):
    '''booleanos : TRUE
                 | FALSE
                 | ON
                 | OFF'''

def p_now(p):
    'now : NOW PARIZQ PARDER'

def p_math_sw(p):
    '''math_sw : ABS PARIZQ expresion PARDER
               | CBRT PARIZQ expresion PARDER
               | CEIL PARIZQ expresion PARDER
               | CEILING PARIZQ expresion PARDER'''

def p_math_select(p):
    '''math_select : DEGREES PARIZQ expresion PARDER
                   | DIV PARIZQ expresion COMA expresion PARDER
                   | EXP PARIZQ expresion PARDER
                   | FACTORIAL PARIZQ expresion PARDER
                   | FLOOR PARIZQ expresion PARDER
                   | GCD PARIZQ expresion PARDER
                   | LN PARIZQ expresion PARDER
                   | LOG PARIZQ expresion PARDER
                   | MOD PARIZQ expresion COMA expresion PARDER
                   | PI PARIZQ PARDER
                   | POWER PARIZQ expresion COMA expresion PARDER
                   | RADIANS PARIZQ expresion PARDER
                   | ROUND PARIZQ expresion PARDER
                   | SIGN PARIZQ expresion PARDER
                   | SQRT PARIZQ expresion PARDER
                   | WIDTH_BUCKET PARIZQ expresion lista_exp PARDER
                   | TRUNC PARIZQ expresion trunc1
                   | RANDOM PARIZQ PARDER'''

def p_lista_exp(p):
    '''lista_exp : lista_exp COMA expresion
                |  COMA expresion'''

def p_trunc1(p):
    '''trunc1 : COMA ENTERO PARDER
             | PARDER'''

def p_trigonometric(p):
    '''trigonometric : ACOS PARIZQ expresion PARDER
                     | ACOSD PARIZQ expresion PARDER
                     | ASIN PARIZQ expresion PARDER
                     | ASIND PARIZQ expresion PARDER
                     | ATAN PARIZQ expresion PARDER
                     | ATAND PARIZQ expresion PARDER
                     | ATAN2 PARIZQ expresion COMA expresion PARDER
                     | ATAN2D PARIZQ expresion COMA expresion PARDER
                     | COS PARIZQ expresion PARDER
                     | COSD PARIZQ expresion PARDER
                     | COT PARIZQ expresion PARDER
                     | COTD PARIZQ expresion PARDER
                     | SIN PARIZQ expresion PARDER
                     | SIND PARIZQ expresion PARDER
                     | TAN PARIZQ expresion PARDER
                     | TAND PARIZQ expresion PARDER
                     | SINH PARIZQ expresion PARDER
                     | COSH PARIZQ expresion PARDER
                     | ASINH PARIZQ expresion PARDER
                     | ACOSH PARIZQ expresion PARDER
                     | ATANH PARIZQ expresion PARDER'''

def p_ext(p):
    '''ext : EXTRACT PARIZQ time_type FROM temp_exp expresion PARDER
           | EXTRACT PARIZQ time_type FROM expresion PARDER'''

def p_time_type(p):
    '''time_type : YEAR
                 | MONTH
                 | DAY
                 | HOUR
                 | MINUTE
                 | SECOND'''

def p_d_part(p):
    'd_part : DATE_PART PARIZQ CADENA COMA temp_exp CADENA PARDER'

def p_temp_exp(p):
    '''temp_exp : TIMESTAMP
                | TIME
                | INTERVAL'''

def p_binary_string(p):
    '''binary_string : SHA256 PARIZQ expresion PARDER
                     | SUBSTR PARIZQ expresion COMA ENTERO COMA ENTERO PARDER
                     | GET_BYTE PARIZQ expresion COMA ENTERO PARDER
                     | SET_BYTE PARIZQ expresion COMA ENTERO COMA ENTERO PARDER
                     | CONVERT PARIZQ expresion AS data_type PARDER
                     | ENCODE PARIZQ expresion COMA expresion PARDER
                     | DECODE PARIZQ expresion COMA expresion PARDER
                     | bs_sw
                     | bs_iu
                     | bs_siuw'''

def p_bs_sw(p):
    'bs_sw : LENGTH PARIZQ expresion PARDER'

def p_bs_iu(p):
    'bs_iu : MD5 PARIZQ expresion PARDER'

def p_bs_siuw(p):
    '''bs_siuw : SUBSTRING PARIZQ expresion COMA ENTERO COMA ENTERO PARDER
               | TRIM PARIZQ trim1 PARDER'''

def p_trim(p):
    '''trim1 : trim2 FROM expresion
            | expresion'''

def p_trim1(p):
    '''trim2 : LEADING
             | TRAILING
             | BOTH'''


def p_error(p):
    global linea, columna
    sin_error(p.type, p.value, linea, p.lexpos)
    #columna = columna + len(p.value)


# Construyendo el analizador sintáctico
parser = yacc.yacc()

#Funcion para concatenar los errores léxicos en una variable
def lex_error(lex, linea, columna):
    global cont_error_lexico, errores_lexicos, errores
    cont_error_lexico = cont_error_lexico + 1
    errores = errores + 'ERROR LÉXICO : Vino el símbolo -> ' + str(lex) + ' en la linea ' + str(linea) + ' y columna ' + str(columna) + '\n'
    errores_lexicos = errores_lexicos + "<tr><td align=""center""><font color=""black"">" + str(cont_error_lexico) + "<td align=""center""><font color=""black"">" + str(lex) + "</td><td align=""center""><font color=""black"">" + str(linea) + "</td><td align=""center""><font color=""black"">" + str(columna) + "</td></tr>" + '\n'

#Construccion reporte de errores léxicos
def reporte_lex_error():
    f = open('Errores_lexicos.html', 'w')
    f.write("<html>")
    f.write("<body>")
    f.write("<table border=""1"" style=""width:100%""><tr><th>No.</th><th>Error</th><th>Linea</th><th>Columna</th></tr>")
    f.write(errores_lexicos)
    f.write("</table>")
    f.write("</body>")
    f.write("</html>")
    f.close()

#Construccion de la lista de tokens con lex.lex()
def reporte_tokens(data):
    cont = 0
    lexer.input(data)
    global errores_lexicos, cont_error_lexico, linea, columna
    linea = 1
    errores_lexicos = ""
    cont_error_lexico = 0
    f = open('Tokens.html', 'w')
    f.write("<html>")
    f.write("<body>")
    f.write("<table border=""1"" style=""width:100%""><tr><th>No.</th><th>Token</th><th>Lexema</th><th>Linea</th><th>Columna</th></tr>")
    while True:
        cont = cont + 1
        tok = lexer.token()
        x = str(tok).replace('LexToken(','')[:-len(')')].split(",")
        if(len(x) >= 4):
            f.write("<tr><td align=""center""><font color=""black"">" + str(cont) + "<td align=""center""><font color=""black"">" + x[0] + "</td><td align=""center""><font color=""black"">" + x[1] + "</td><td align=""center""><font color=""black"">" + str(linea) + "</td><td align=""center""><font color=""black"">" + str(columna) + "</td></tr>" + '\n')
            columna = columna + len(x[1])
        if not tok:
            break
    f.write("</table>")
    f.write("</body>")
    f.write("</html>")
    f.close()

#Funcion para concatenar los errores léxicos en una variable
def sin_error(token, lex, linea, columna):
    global cont_error_sintactico, errores_sintacticos, errores
    cont_error_sintactico = cont_error_sintactico + 1
    errores = errores + 'ERROR SINTÁCTICO : Vino token -> ' + str(token) + ' con lexema -> ' + str(lex) + ' en la linea ' + str(linea) + ' y columna ' + str(columna) + '\n'
    errores_sintacticos = errores_sintacticos + "<tr><td align=""center""><font color=""black"">" + str(cont_error_sintactico) + "<td align=""center""><font color=""black"">" + str(token) + "<td align=""center""><font color=""black"">" + str(lex) + "</td><td align=""center""><font color=""black"">" + str(linea) + "</td><td align=""center""><font color=""black"">" + str(columna) + "</td></tr>" + '\n'

#Construccion reporte de errores sintacticos
def reporte_sin_error():
    global cont_error_sintactico, errores_sintacticos
    f = open('Errores_sintacticos.html', 'w')
    f.write("<html>")
    f.write("<body>")
    f.write("<table border=""1"" style=""width:100%""><tr><th>No.</th><th>Token</th><th>Error</th><th>Linea</th><th>Columna</th></tr>")
    f.write(errores_sintacticos)
    f.write("</table>")
    f.write("</body>")
    f.write("</html>")
    f.close()
    cont_error_sintactico = 0
    errores_sintacticos = ""

def parse(entrada):
    global parser, linea, columna, errores
    errores = ""
    linea = 1
    columna = 1
    parse_result = parser.parse(entrada)
    print(parse_result)
    reporte_tokens(entrada)
    reporte_lex_error()
    reporte_sin_error()
    #ast_graph.render('.\\Diagrama\\Diagrama.gv', view=False) 
    #ast_graph.render('.\\Diagrama\\Diagrama.gv.pdf', view=False)
    #ast_graph.render('.\\Diagrama\\Diagrama.png', view=False)
    result = [parse_result, errores]
    return result