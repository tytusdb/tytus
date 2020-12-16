import Errores.Nodo_Error as err
from ply import lex
from AST.Sentencias import Raiz, Sentencia
import AST.SentenciasDDL as DDL
import ply.yacc as yacc

reservadas = {
    'select': 't_select',
    'distinct': 't_distinct',
    'as': 't_as',
    'from': 't_from',
    'where': 't_where',
    'having': 't_having',
    'avg': 't_avg',
    'min': 't_min',
    'max': 't_max',
    'sum': 't_sum',
    'count': 't_count',
    'insert': 't_insert',
    'into': 't_into',
    'values': 't_values',
    'delete': 't_delete',
    'update': 't_update',
    'true': 't_true',
    'false': 't_false',
    'not': 't_not',
    'and': 't_and',
    'or': 't_or',
    'smallint': 't_smallint',
    'integer': 't_integer',
    'bigint': 't_bigint',
    'decimal': 't_decimal',
    'numeric': 't_numeric',
    'real': 't_real',
    'double': 't_double',
    'precision': 't_precision',
    'money': 't_money',
    'character': 't_character',
    'varying': 't_varying',
    'varchar': 't_varchar',
    'char': 't_charn',
    'text': 't_text',
    'boolean': 't_boolean',
    'bool': 't_bool',
    'type': 't_type',
    'enum': 't_enum',
    'create': 't_create',
    'replace': 't_replace',
    'database': 't_database',
    'if': 't_if',
    'exists': 't_exists',
    'owner': 't_owner',
    'mode': 't_mode',
    'show': 't_show',
    'databases': 't_databases',
    'like': 't_like',
    'alter': 't_alter',
    'rename': 't_rename',
    'to': 't_to',
    'current_user': 't_current_user',
    'session_user': 't_session_user',
    'drop': 't_drop',
    'table': 't_table',
    'delete': 't_delete',
    'only': 't_only',
    'using': 't_using',
    'current': 't_current',
    'of': 't_of',
    'returning': 't_returning',
    'as': 't_as',
    'inherits': 't_inherits',
    'primary': 't_primary',
    'key': 't_key',
    'references': 't_references',
    'foreign': 't_foreign',
    'null': 't_null',
    'constraint': 't_constraint',
    'unique': 't_unique',
    'check': 't_check',
    'add': 't_add',
    'set': 't_set',
    'rename': 't_rename',
    'column': 't_column',
    'inner': 't_inner',
    'left': 't_left',
    'right': 't_right',
    'full': 't_full',
    'outer': 't_outer',
    'join': 't_join',
    'natural': 't_natural',
    'on': 't_on',
    'abs': 't_abs',
    'cbrt': 't_cbrt',
    'ceil': 't_ceil',
    'ceiling': 't_ceiling',
    'degrees': 't_degrees',
    'div': 't_div',
    'exp': 't_exp',
    'factorial': 't_factorial',
    'floor': 't_floor',
    'gcd': 't_gcd',
    'ln': 't_ln',
    'log': 't_log',
    'mod': 't_mod',
    'pi': 't_pi',
    'power': 't_power',
    'radians': 't_radians',
    'round': 't_round',
    'use': 't_use',
    'default' : 't_default',
    'acos' : 't_acos',
    'acosd' : 't_acosd',
    'asin' : 't_asin',
    'asind' : 't_asind',
    'atan' : 't_atan',
    'atand' : 't_atand',
    'atan2' : 't_atan2',
    'atan2d' : 't_atan2d',
    'cos' : 't_cos',
    'cosd' : 't_cosd',
    'cot' : 't_cot',
    'cotd' : 't_cotd',
    'sin' : 't_sin',
    'sind' : 't_sind',
    'tan' : 't_tan',
    'tand' : 't_tand',
    'sinh' : 't_sinh',
    'cosh' : 't_cosh',
    'tanh' : 't_tanh',
    'asinh' : 't_asinh',
    'acosh' : 't_acosh',
    'atanh' : 't_atanh',
    'min_scale' : 't_min_scale',
    'scale' : 't_scale',
    'sign' : 't_sign',
    'sqrt' : 't_sqrt',
    'trim_scale' : 't_trim_scale',
    'trunc' : 't_trunc',
    'width_bucket' : 't_width_bucket',
    'random' : 't_random',
    'setseed' : 't_setseed',
    'length' : 't_length',
    'substring' : 't_substring',
    'trim' : 't_trim',
    'md5' : 't_md5',
    'sha256' : 't_sha256',
    'substr' : 't_substr',
    'get_byte' : 't_get_byte',
    'set_byte' : 't_set_byte',
    'convert' : 't_convert',
    'encode' : 't_encode',
    'decode' : 't_decode'
}

tokens = [
             'par1',
             'par2',
             'cor1',
             'cor2',
             'asterisco',
             'mas',
             'menos',
             'pyc',
             'coma',
             'div',
             'punto',
             'igual',
             'menor',
             'mayor',
             'menori',
             'mayori',
             'diferente',
             'porcentaje',
             'diferentede',
             'pot',
             'bipunto',
             'id',
             'decimal',
             'entero',
             'char',
             'string'
         ] + list(reservadas.values())

# Tokens
t_par1 = r'\('
t_par2 = r'\)'
t_cor1 = r'\['
t_cor2 = r'\]'
t_pyc = r';'
t_punto = r'\.'
t_coma = r'\,'
t_igual = r'\='
t_mas = r'\+'
t_menos = r'-'
t_asterisco = r'\*'
t_div = r'/'
t_mayor = r'>'
t_menor = r'<'
t_mayori = r'>='
t_menori = r'<='
t_diferente = r'!='
t_porcentaje = r'\%'
t_pot = r'\^'
t_bipunto = r'::'
t_diferentede = r'<>'


def t_decimal(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("El valor es muy grande %d", t.value)
        t.value = 0
    return t


def t_entero(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("El valor de integer es muy grande %d", t.value)
        t.value = 0
    return t


def t_char(t):
    r'\'.*?\''
    t.value = t.value[1:-1]  # se remueven comillas
    return t


def t_string(t):
    r'\".*?\"'
    t.value = t.value[1:-1]  # se remueven comillas
    return t


def t_id(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value.lower(), 'id')  # Check for reserved words
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


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def t_error(t):
    ListaErrores.insertar(err.Nodo_Error("Lexico", "Caracter no valido '%s'" % t.value[0],
                                      t.lineno, find_column(input, t)))
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

precedence = (
    ('left', 'punto', 'bipunto'),
    ('left', 'coma'),
    ('right', 'igual'),
    ('left', 'cor1', 'cor2'),
    ('left', 'mas', 'menos'),
    ('left', 'asterisco', 'div', 'porcentaje'),
    ('left', 'pot'),
    ('right', 'umenos', 'umas'),
    ('left', 'par1', 'par2'),
    # Between , in , like, ilike, simiar, is isnull notnull
    ('left', 't_or'),
    ('left', 't_and'),
    ('left', 'diferente'),
    ('left', 'mayor', 'menor', 'mayori', 'menori'),
    ('right', 't_not')
)

from AST.Expresiones import *
from AST.SentenciasDML import *
reporteg = ''


def p_sql(p):
    'SQL : Sentencias_SQL'
    p[0] = Raiz(ListaErrores, p[1])
    concatenar_gramatica('\n <TR><TD> SQL → SENTENCIAS_SQL </TD> <TD>  </TD></TR>')

def p_sql2(p):
    'SQL : empty'
    p[0] = Raiz(ListaErrores)
    concatenar_gramatica('\n <TR><TD> SQL → EMPTY </TD> <TD> </TD></TR>')

def p_Sentencias_SQL_Sentencia_SQL(p):
    'Sentencias_SQL : Sentencias_SQL Sentencia_SQL'
    p[0] = p[1] + [p[2]]
    concatenar_gramatica('\n <TR><TD> SENTENCIAS_SQL → SENTENCIAS_SQL SENTENCIA_SQL </TD> <TD> </TD></TR> ')


def p_Sentencias_SQL(p):
    'Sentencias_SQL : Sentencia_SQL'
    p[0] = [p[1]]
    concatenar_gramatica('\n <TR><TD> SENTENCIAS_SQL → SENTENCIA_SQL </TD> <TD>  </TD></TR>')

def p_Sentencia_SQL_DML(p):
    'Sentencia_SQL : Sentencias_DML'
    p[0] = Sentencia("SentenciaDML", [p[1]])
    concatenar_gramatica('\n <TR><TD> SENTENCIA_SQL → SENTENCIAS_DML </TD> <TD> </TD></TR>')

#def p_Sentencia_SQL_DML(p):
 #   'Sentencia_SQL : EXP pyc'
  #  p[0] = Sentencia("EXP", [p[1]])
   
def p_Sentencia_SQL_DDL(p):
    'Sentencia_SQL : Sentencias_DDL'
    p[0] = Sentencia("SentenciaDDL", [p[1]])
    concatenar_gramatica('\n <TR><TD> SENTENCIA_SQL → SENTENCIAS_DDL </TD> <TD> </TD></TR>')

# -------------------------------------------------------------SENTENCIAS DML
def p_Sentencias_DML(p):
    '''Sentencias_DML : t_select Lista_EXP Select_SQL Condiciones pyc
                    | t_select asterisco Select_SQL Condiciones pyc
                    | t_insert t_into id Insert_SQL pyc
                    | t_update id t_set Lista_EXP t_where EXP pyc
                    | t_delete t_from id Condiciones pyc
                    | t_use t_database id pyc'''
    if p[1] == 'select':
        p[0] = Select(p[2], p[3], p[4], p.slice[2].lineno, find_column(input, p.slice[2]))
        concatenar_gramatica('\n <TR><TD> SENTENCIAS_DML → select' + str(p[2]) + 'SELECT_SQL ; </TD><TD>  </TD></TR>')
    elif p[1] == 'insert':
        p[0] = Insert(p[3], p[4], p.slice[1].lineno, find_column(input, p.slice[1]))
        concatenar_gramatica('\n <TR><TD> SENTENCIAS_DML → insert into id INSERT_SQL ; </TD> <TD>   </TD></TR>')
    elif p[1] == 'update':
        concatenar_gramatica('\n <TR><TD> SENTENCIAS_DML → update id set LISTA_EXP where EXP ; </TD>  <TD> </TD></TR>')
    elif p[1] == 'delete':
        concatenar_gramatica('\n <TR><TD> SENTENCIAS_DML → delete from id CONDICIONES ; </TD>   <TD> </TD></TR>')
    else: 
        concatenar_gramatica('\n <TR><TD> SENTENCIAS_DML → use database id ; </TD>  <TD> </TD></TR>')

def p_Select_SQL(p):
    'Select_SQL : t_from Table_Expression'
    p[0] = p[2]
    concatenar_gramatica('\n <TR><TD> SELECT_SQL → from TABLE_EXPRESSION CONDICIONES </TD>  <TD> </TD></TR>')


def p_Select2_SQL(p):
    'Select_SQL : empty'
    p[0] = []
    concatenar_gramatica('\n <TR><TD> SELECT_SQL → EMPTY </TD>  <TD> </TD></TR>')


def p_Table_Expression(p):
    '''Table_Expression : Alias_Tabla
                        | Subqueries'''
    p[0] = p[1]
    concatenar_gramatica('\n <TR><TD> TABLE_EXPRESSION → ' + str(p[1]) + '</TD>  <TD> </TD></TR>')


def p_Alias_Tabla(p):
    '''Alias_Tabla :  Lista_ID
                | Lista_Alias'''
    p[0] = p[1]
    concatenar_gramatica('\n <TR><TD> ALIAS_TABLA → ' + str(p[1]) + '</TD>  <TD> </TD></TR>')

def p_Subqueries(p):
    '''Subqueries : par1 t_select  par2'''
    concatenar_gramatica('\n <TR><TD> SUBQUERIES → ( select )</TD>  <TD> </TD></TR>')

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> INSERT <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def p_Insert_SQL(p):
    'Insert_SQL : par1 Lista_ID par2 t_values par1 Lista_EXP par2'
    p[0] = p[6]
    concatenar_gramatica('\n <TR><TD> INSERT_SQL → ( LISTA_ID ) values ( LISTA_EXP ) </TD>  <TD> </TD></TR>')

def p_Insert_SQL2(p):
    'Insert_SQL : t_values par1 Lista_EXP par2'
    p[0] = p[3]
    concatenar_gramatica('\n <TR><TD> INSERT_SQL → values ( LISTA_EXP ) </TD>  <TD> </TD></TR>')

def p_Condiciones(p):
    '''Condiciones : t_where EXP
            | empty'''
    if len(p) == 3:
        p[0] = p[1]
        concatenar_gramatica('\n <TR><TD> CONDICIONES → where EXP  </TD>  <TD> </TD></TR>')
    else:
        p[0] = []
        concatenar_gramatica('\n <TR><TD> INSERT_SQL → EMPTY </TD>  <TD> </TD></TR>')

# ---------------------------- Sentencias DDL y Enum Type --------------
def p_Sentencias_DDL(p):
    '''Sentencias_DDL : t_show t_databases pyc
                    | Enum_Type
                    | t_drop Drop pyc
                    | t_alter Alter pyc
                    | t_create Create pyc'''
    if p[1].__class__.__name__ == 'CreateType':
        p[0] = p[1]
        concatenar_gramatica('\n <TR><TD> SENTENCIAS_DDL → ENUM_TYPE </TD>  <TD> </TD></TR>')
    elif p[1].upper() == 'SHOW':
        p[0] = DDL.ShowDatabases(p.slice[1].lineno, find_column(input, p.slice[1]))
        concatenar_gramatica('\n <TR><TD> SENTENCIAS_DDL → show databases ; </TD>  <TD> </TD></TR>')
    elif p[1].upper() == 'CREATE':
        p[0] = None
        concatenar_gramatica('\n <TR><TD> SENTENCIAS_DDL → create CREATE ; </TD>  <TD> </TD></TR>')
    elif p[1].upper() == 'DROP':
        p[0] = None
        concatenar_gramatica('\n <TR><TD> SENTENCIAS_DDL → drop Drop ; </TD>  <TD> </TD></TR>')
    elif p[1].upper() == 'ALTER':
        p[0] = None
        concatenar_gramatica('\n <TR><TD> SENTENCIAS_DDL → alter ALTER ; </TD>  <TD> </TD></TR>')
    else:
        p[0] = None

def p_Enum_Type(p):
    'Enum_Type : t_create t_type id t_as t_enum par1 Lista_Enum par2 pyc'
    p[0] = DDL.CreateType(p[3].lower(), p[7], p.slice[1].lineno, find_column(input, p.slice[1]))
    concatenar_gramatica('\n <TR><TD> ENUM_TYPE → create type id as enum ( LISTA_ENUM ) ; </TD>  <TD> </TD></TR>')

def p_Drop(p):
    '''Drop : t_database DropDB id
            | t_table  id '''
    if p[1] == 'database':
        concatenar_gramatica('\n <TR><TD> DROP → database DROPDB id  </TD>  <TD> </TD></TR>')
    else: 
        concatenar_gramatica('\n <TR><TD> DROP → table  id  </TD>  <TD> </TD></TR>')
   
def p_DropDB(p):
    '''DropDB : t_if t_exists
            | empty'''
    if p[1] == 'if':
        concatenar_gramatica('\n <TR><TD> DROPDB → if exists </TD>  <TD> </TD></TR>')
    else: 
        concatenar_gramatica('\n <TR><TD> DROPDB → EMPTY </TD>  <TD> </TD></TR>')

def p_Alter(p):
    '''Alter : t_database id AlterDB
            | t_table id AlterTB '''
    if p[1] == 'database':
        concatenar_gramatica('\n <TR><TD> ALTER → database id ALTERDB </TD>  <TD> </TD></TR>')
    else: 
        concatenar_gramatica('\n <TR><TD> ALTER → table id ALTERTB </TD>  <TD> </TD></TR>')

def p_AlterDB(p):
    ''' AlterDB : t_rename t_to id
                | t_owner t_to SesionDB '''
    if p[1] == 'rename':
        concatenar_gramatica('\n <TR><TD> ALTERDB → rename to id </TD>  <TD> </TD></TR>')
    else: 
        concatenar_gramatica('\n <TR><TD> ALTERDB → owner to SESIONDB </TD> <TD> </TD></TR>')

def p_SesionDB(p):
    ''' SesionDB : id
                | t_current_user
                | t_session_user '''
    if p[1] == 'current_user':
        concatenar_gramatica('\n <TR><TD> SESSIONDB → current_user </TD>  <TD> </TD></TR>')
    elif p[1] == 'session_user': 
        concatenar_gramatica('\n <TR><TD> SESSIONDB → session_user </TD> <TD> </TD></TR>')
    else: 
        concatenar_gramatica('\n <TR><TD> SESSIONDB → id </TD> <TD> </TD></TR>')

def p_AlterTB(p):
    ''' AlterTB : t_add Add_Opc
                | t_drop Drop_Opc
                | t_alter t_column Alter_Column
                | t_rename t_column id t_to id '''
    if p[1] == 'add':
        concatenar_gramatica('\n <TR><TD> ALTERTB → add ADD_OPC </TD>  <TD> </TD></TR>')
    elif p[1] == 'drop':
        concatenar_gramatica('\n <TR><TD> ALTERTB → drop DROP_OPC </TD> <TD> </TD></TR>')
    elif p[1] == 'alter': 
        concatenar_gramatica('\n <TR><TD> ALTERTB → alter column ALTER_COLUMN </TD> <TD> </TD></TR>')
    elif p[1] == 'rename':
        concatenar_gramatica('\n <TR><TD> ALTERTB → rename column id to id </TD> <TD> </TD></TR>')

def p_Add_Opc(p):
    '''Add_Opc : t_column id Tipo
               | t_foreign t_key par1 id par2 t_references id
               | t_constraint id t_unique par1 id par2
               | t_check EXP '''
    if p[1] == 'column':
        concatenar_gramatica('\n <TR><TD> ADD_OPC → column id TIPO </TD>  <TD> </TD></TR>')
    elif p[1] == 'foreign':
        concatenar_gramatica('\n <TR><TD> ADD_OPC → foreign key ( id ) references id </TD> <TD> </TD></TR>')
    elif p[1] == 'constraint':
        concatenar_gramatica('\n <TR><TD> ADD_OPC → constraint id unique ( id ) </TD> <TD> </TD></TR>')
    elif p[1] == 'check': 
        concatenar_gramatica('\n <TR><TD> ADD_OPC → check EXP </TD> <TD> </TD></TR>')

def p_Drop_Opc(p):
    ''' Drop_Opc :  t_column id
                 |  t_constraint id '''
    if p[1] == 'column':
        concatenar_gramatica('\n <TR><TD> DROP_OPC → column id TIPO </TD>  <TD> </TD></TR>')
    elif p[1] == 'constraint': 
        concatenar_gramatica('\n <TR><TD> DROP_OPC → foreign key ( id ) references id </TD> <TD> </TD></TR>')

def p_Alter_Column(p):
    ''' Alter_Column :   id t_set t_not t_null
                     |   Alter_Columns'''
    if len(p) == 5:
        concatenar_gramatica('\n <TR><TD> ALTER_COLUMN → id set not null </TD>  <TD> </TD></TR>')
    else: 
        concatenar_gramatica('\n <TR><TD> ALTER_COLUMN → ALTER_COLUMNS </TD> <TD> </TD></TR>')

def p_Alter_Columns(p):
    ''' Alter_Columns : Alter_Columns coma Alter_Column1
                    | Alter_Column1'''
    if len(p) == 4:
        concatenar_gramatica('\n <TR><TD> ALTER_COLUMNS → ALTER_COLUMNS , ALTER_COLUMN1 </TD>  <TD> </TD></TR>')
    else: 
        concatenar_gramatica('\n <TR><TD> ALTER_COLUMNS → ALTER_COLUMN1 </TD> <TD> </TD></TR>')

def p_Alter_Colum1(p):
    '''Alter_Column1 :  id t_type t_varchar par1 entero par2
                    | t_alter t_column id t_type t_varchar par1 entero par2'''
    if p[1] == 'alter':
        concatenar_gramatica('\n <TR><TD> ALTER_COLUMN1 → alter column id type varchar ( entero ) </TD>  <TD> </TD></TR>')
    else: 
        concatenar_gramatica('\n <TR><TD> ALTER_COLUMN1 → id type varchar ( entero ) </TD> <TD> </TD></TR>')

def p_Create(p):
    'Create : CreateDB'
    p[0] = p[1]
    concatenar_gramatica('\n <TR><TD> CREATE → CREATEDB </TD>  <TD> </TD></TR>')

def p_Create1(p):
    'Create : CreateTB '
    concatenar_gramatica('\n <TR><TD> CREATE → CREATETB </TD>  <TD> </TD></TR>')

def p_CreateDB(p):
    '''CreateDB : t_database Op1_DB
                | t_or t_replace t_database Op1_DB'''
    if len(p) == 3:
        p[0] = p[1]
        concatenar_gramatica('\n <TR><TD> CREATEDB → database OP1_DB </TD>  <TD> </TD></TR>')
    else:
        p[0] = p[1]
        concatenar_gramatica('\n <TR><TD> CREATEDB → or replace database OP1_DB </TD>  <TD> </TD></TR>')

def p_Op1_DB(p):
    ''' Op1_DB : t_if t_not t_exists id Sesion
               | id Sesion'''
    if p[1] == 'if':
        p[0] = p[1]
        concatenar_gramatica('\n <TR><TD> OP1_DB → if not exists id SESION </TD>  <TD> </TD></TR>')
    else:
        p[0] = p[1]
        concatenar_gramatica('\n <TR><TD> OP1_DB → id SESION </TD>  <TD> </TD></TR>')

def p_Sesion(p):
    ''' Sesion : t_owner Op_Sesion Sesion_mode
                | t_mode Op_Sesion
                | empty '''
    if p[1] == 'owner':
        concatenar_gramatica('\n <TR><TD> SESION → owner OP_SESION SESION_MODE </TD>  <TD> </TD></TR>')
    elif p[1] == 'mode':
        concatenar_gramatica('\n <TR><TD> SESION → mode OP_SESION </TD>  <TD> </TD></TR>')
    else:
        concatenar_gramatica('\n <TR><TD> SESION → EMPTY </TD>  <TD> </TD></TR>')

def p_Op_Sesion(p):
    ''' Op_Sesion : igual id
            | id  '''
    if len(p) == 3:
        p[0] = p[2]
        concatenar_gramatica('\n <TR><TD> OP_SESION → = id </TD>  <TD> </TD></TR>')
    else:
        p[0] = p[1]
        concatenar_gramatica('\n <TR><TD> OP_SESION → id </TD>  <TD> </TD></TR>')

def p_Sesion_mode(p):
    ''' Sesion_mode : t_mode Op_Sesion
                  | empty '''
    if len(p) == 3:
        p[0] = p[2]
        concatenar_gramatica('\n <TR><TD> SESION_MODE → mode OP_SESION </TD>  <TD> </TD></TR>')
    else:
        p[0] = p[1]
        concatenar_gramatica('\n <TR><TD> SESION_MODE → EMPTY </TD>  <TD> </TD></TR>')

def p_CreateTB(p):
    'CreateTB : t_table id par1 Columnas par2 Inherits '
    concatenar_gramatica('\n <TR><TD> CREATETB → table id ( COLUMNAS ) INHERITS </TD>  <TD> </TD></TR>')

def p_Inherits(p):
    ''' Inherits : t_inherits par1 id par2
               | empty '''
    if len(p) == 5:
        concatenar_gramatica('\n <TR><TD> INHERITS → inherits ( id ) </TD>  <TD> </TD></TR>')
    else:
        p[0] = p[1]
        concatenar_gramatica('\n <TR><TD> INHERITS → EMPTY </TD>  <TD> </TD></TR>')
    
def p_Columnas(p):
    ''' Columnas : Columnas coma Columna
                | Columna '''
    if len(p) == 4:
        concatenar_gramatica('\n <TR><TD> COLUMNAS → COLUMNAS , COLUMNA </TD>  <TD> </TD></TR>')
    else:
        p[0] = p[1]
        concatenar_gramatica('\n <TR><TD> COLUMNAS → COLUMNA </TD>  <TD> </TD></TR>')

def p_Columna(p):
    ''' Columna : id Tipo Cond_CreateTB
                | Constraint'''
    if len(p) == 4:
        concatenar_gramatica('\n <TR><TD> COLUMNA → id TIPO COND_CREATETB </TD>  <TD> </TD></TR>')
    else:
        p[0] = p[1]
        concatenar_gramatica('\n <TR><TD> COLUMNA → CONSTRAINT </TD>  <TD> </TD></TR>')

def p_Cond_CreateTB(p):
    ''' Cond_CreateTB : t_default id Cond_CreateTB
                        | t_not t_null Cond_CreateTB
                        | t_null Cond_CreateTB
                        | t_constraint id Opc_Constraint Cond_CreateTB
                        | t_primary t_key Cond_CreateTB
                        | t_references id Cond_CreateTB
                        | empty'''
    if p[1] == 'default':
        concatenar_gramatica('\n <TR><TD> COND_CREATETB → default id COND_CREATETB </TD>  <TD> </TD></TR>')
    elif p[1] == 'not':
        concatenar_gramatica('\n <TR><TD> COND_CREATETB → not null COND_CREATETB </TD>  <TD> </TD></TR>')
    elif p[1] == 'null':
        concatenar_gramatica('\n <TR><TD> COND_CREATETB → null COND_CREATETB </TD>  <TD> </TD></TR>')
    elif p[1] == 'constraint':
        concatenar_gramatica('\n <TR><TD> COND_CREATETB → constraint id OPC_CONSTRAINT COND_CREATETB </TD>  <TD> </TD></TR>')
    elif p[1] == 'primary':
        concatenar_gramatica('\n <TR><TD> COND_CREATETB →  primary key COND_CREATETB </TD>  <TD> </TD></TR>')
    elif p[1] == 'references':
        concatenar_gramatica('\n <TR><TD> COND_CREATETB →  references id COND_CREATETB </TD>  <TD> </TD></TR>')
    else: 
        concatenar_gramatica('\n <TR><TD> COND_CREATETB →  EMPTY  </TD>  <TD> </TD></TR>')

def p_Opc_Constraint(p):
    ''' Opc_Constraint : t_unique
                       | t_check par1 EXP par2 '''
    if p[1] == 'unique':
        concatenar_gramatica('\n <TR><TD> OPC_CONSTRAINT →  unique  </TD>  <TD> </TD></TR>')
    elif p[1] == 'check':
        concatenar_gramatica('\n <TR><TD> OPC_CONSTRAINT →  check ( EXP )  </TD>  <TD> </TD></TR>')

def p_Constraint(p):
    ''' Constraint : t_unique par1 Lista_ID par2
                    | t_constraint id t_check par1 EXP par2
                    | t_check par1 EXP par2
                    | t_primary t_key par1 Lista_ID par2
                    | t_foreign t_key par1 Lista_ID par2 t_references id par1 Lista_ID par2
                    | empty '''
    if p[1] == 'unique':
        concatenar_gramatica('\n <TR><TD> CONSTRAINT →  unique ( LISTA_ID )  </TD>  <TD> </TD></TR>')
    elif p[1] == 'constraint':
        concatenar_gramatica('\n <TR><TD> CONSTRAINT →  constraint id check ( EXP )  </TD>  <TD> </TD></TR>')
    elif p[1] == 'check':
        concatenar_gramatica('\n <TR><TD> CONSTRAINT →  check ( EXP )  </TD>  <TD> </TD></TR>')
    elif p[1] == 'primary':
        concatenar_gramatica('\n <TR><TD> CONSTRAINT →  primary key ( LISTA_ID ) </TD>  <TD> </TD></TR>')
    elif p[1] == 'foreign': 
        concatenar_gramatica('\n <TR><TD> CONSTRAINT →  foreign key ( LISTA_ID ) references id ( LISTA_ID )  </TD>  <TD> </TD></TR>')
    else: 
        concatenar_gramatica('\n <TR><TD> CONSTRAINT →  EMPTY </TD>  <TD> </TD></TR>')

def p_Tipo(p):
    ''' Tipo : t_smallint
              | t_integer
              | t_bigint
              | t_decimal
              | t_numeric
              | t_real
              | t_double t_precision
              | t_money
              | t_character t_varying par1 Valor par2
              | t_varchar par1 Valor par2
              | t_character par1 Valor par2
              | t_charn par1 Valor par2
              | t_text
              | t_boolean '''
    p[0] = p[1]
    concatenar_gramatica('\n <TR><TD> TIPO → ' + str(p[1]) + '</TD>  <TD> </TD></TR>')

def p_Valor(p):
    ''' Valor : decimal
            | entero
            | string
            | char
            | t_true
            | t_false'''
    p[0] = Expression(p[1], p.slice[1].lineno, find_column(input, p.slice[1]), p.slice[1].type)
    concatenar_gramatica('\n <TR><TD> VALOR → ' + str(p[1]) + '</TD>  <TD> </TD></TR>')


def p_Valor2(p):
    'Valor : id'
    p[0] = Expression(p[1], p.slice[1].lineno, find_column(input, p.slice[1]))
    concatenar_gramatica('\n <TR><TD> TIPO → id </TD>  <TD> </TD></TR>')

def p_empty(p):
    'empty :'
    p[0] = []
    concatenar_gramatica('\n <TR><TD> EMPTY → epsilon </TD>  <TD> </TD></TR>')

# ----------------------------EXPRESIONES Y OPERACIONES---------------------------------------------------------------

def p_aritmeticas(p):
    '''EXP : EXP mas EXP
           | EXP menos EXP
           | EXP asterisco EXP
           | EXP div EXP
           | EXP pot EXP
           | EXP porcentaje EXP'''
    p[0] = Expression(p[1], p[3], p.slice[2].value, p.slice[2].lineno, find_column(input, p.slice[2]),'Aritmetica')
    concatenar_gramatica('\n <TR><TD> EXP → EXP' + str(p[2]) + '</TD>  <TD> </TD></TR>')

def p_parentesis(p):
    'EXP : par1 EXP par2'
    p[0] = p[2]
    concatenar_gramatica('\n <TR><TD> EXP → ( EXP ) </TD>  <TD> </TD></TR>')

def p_relacionales(p):
    '''EXP : EXP mayor EXP
           | EXP mayori EXP
           | EXP menor EXP
           | EXP menori EXP
           | EXP igual EXP
           | EXP diferente EXP
           | EXP diferentede EXP'''
    p[0] = Expression(p[1], p[3], p.slice[2].value, p.slice[2].lineno, find_column(input, p.slice[2]), 'Relacional')
    concatenar_gramatica('\n <TR><TD> EXP → EXP' + str(p[2]) + '</TD>  <TD> </TD></TR>')

def p_logicos(p):
    '''EXP : EXP t_and EXP
       | EXP t_or EXP
       '''
    p[0] = Expression(p[1], p[3], p.slice[2].value, p.slice[2].lineno, find_column(input, p.slice[2]), 'Logica')
    concatenar_gramatica('\n <TR><TD> EXP → EXP' + str(p[2]) + '</TD>  <TD> </TD></TR>')

def p_unario(p):
    '''EXP : mas EXP  %prec umas
           | menos EXP  %prec umenos
           | t_not EXP'''
    if p[1] == 'not': 
        p[0] = Expression(p.slice[1].value, p[2], p.slice[2].lineno, find_column(input, p.slice[2]), 'Unario')
        concatenar_gramatica('\n <TR><TD> EXP → not EXP </TD>  <TD> </TD></TR>')
    else: 
        p[0] = Expression(p.slice[1].value, p[2], p.slice[2].lineno, find_column(input, p.slice[2]), 'Unario')
        concatenar_gramatica('\n <TR><TD> EXP → ' + str(p[1]) + 'EXP' + str(p[3]) +  str(p[4]) +'</TD>  <TD> </TD></TR>')

def p_EXP_Valor(p):
    'EXP : Valor'
    p[0] = p[1]
    concatenar_gramatica('\n <TR><TD> EXP → VALOR </TD>  <TD> </TD></TR>')

def p_EXP_Indices(p):
    '''EXP : id punto id'''
    p[0] = p[1]
    concatenar_gramatica('\n <TR><TD> EXP → id . id </TD>  <TD> </TD></TR>')

def p_EXP_IndicesAS(p):
    '''EXP : EXP t_as EXP'''
    p[0] = p[1]
    concatenar_gramatica('\n <TR><TD> EXP → EXP as EXP </TD>  <TD> </TD></TR>')

def p_exp_agregacion(p):
    '''EXP :  t_avg par1 EXP par2
            | t_sum par1 EXP par2
            | t_count par1 EXP par2
            | t_max par1 EXP par2
            | t_min par1 EXP par2'''
    concatenar_gramatica('\n <TR><TD> EXP → ' + str(p[1]) + '( EXP ) </TD>  <TD> </TD></TR>')

def p_funciones_matematicas(p):
    ''' EXP : t_abs par1 EXP par2
            | t_cbrt par1 EXP par2
            | t_ceil par1 EXP par2
            | t_ceiling par1 EXP par2
            | t_degrees par1 EXP par2
            | t_exp par1 EXP par2
            | t_factorial par1 EXP par2
            | t_floor par1 EXP par2
            | t_ln par1 EXP par2
            | t_log par1 EXP par2
            | t_pi par1  par2
            | t_radians par1 EXP par2
            | t_round par1 EXP par2
            | t_min_scale par1 EXP par2
            | t_scale par1 EXP par2
            | t_sign par1 EXP par2
            | t_sqrt par1 EXP par2
            | t_trim_scale par1 EXP par2
            | t_trunc par1 EXP par2
            | t_width_bucket par1 Lista_EXP par2
            | t_random par1 par2
            | t_setseed par1 EXP par2'''
    concatenar_gramatica('\n <TR><TD> EXP → ' + str(p[1]) + '( EXP ) </TD>  <TD> </TD></TR>')

def p_funciones_matematicas(p):
    ''' EXP : t_div par1 EXP coma EXP par2
            | t_gcd par1 EXP coma EXP par2
            | t_mod par1 EXP coma EXP par2
            | t_power par1 EXP coma EXP par2'''
    concatenar_gramatica('\n <TR><TD> EXP → ' + str(p[1]) + '( EXP , EXP) </TD>  <TD> </TD></TR>')

def p_funciones_Trigonometricas(p):
    ''' EXP : t_acos par1 EXP par2
            | t_acosd par1 EXP par2
            | t_asin par1 EXP par2
            | t_asind par1 EXP par2
            | t_atan par1 EXP par2
            | t_atand par1 EXP par2
            | t_cos par1 EXP par2
            | t_cosd par1 EXP par2
            | t_cot par1 EXP par2
            | t_cotd par1 EXP par2
            | t_sin par1 EXP par2
            | t_sind par1 EXP par2
            | t_tan par1 EXP par2
            | t_tand par1 EXP par2 '''
    concatenar_gramatica('\n <TR><TD> EXP → ' + str(p[1]) + '( EXP ) </TD>  <TD> </TD></TR>')

def p_funciones_Trigonometricas1(p):
    ''' EXP : t_atan2 par1 EXP coma EXP par2
            | t_atan2d par1 EXP coma EXP par2 '''
    concatenar_gramatica('\n <TR><TD> EXP → ' + str(p[1]) + '( EXP , EXP ) </TD>  <TD> </TD></TR>')

def p_funciones_String_Binarias(p):
    ''' EXP : t_length par1 id par2
            | t_substring par1 char coma t_integer coma t_integer par2
            | t_trim par1 char par2
            | t_md5 par1 char par2
            | t_sha256 par1 par2
            | t_substr par1 par2
            | t_get_byte par1 par2
            | t_set_byte par1 par2
            | t_convert par1 EXP t_as Tipo par2
            | t_encode par1 par2
            | t_decode par1 par2 '''
    if p[1] == 'substring': 
        concatenar_gramatica('\n <TR><TD> EXP → substring ( char , integer , integer ) </TD>  <TD> </TD></TR>')
    elif p[1] == 'convert':
        concatenar_gramatica('\n <TR><TD> EXP → convert ( EXP as TIPO ) </TD>  <TD> </TD></TR>')
    else: 
        concatenar_gramatica('\n <TR><TD> EXP → ' + str(p[1]) + '( EXP ) </TD>  <TD> </TD></TR>')

# --------------------------------------Listas Fundamentales--------------------------------------------
def p_Lista_ID(p):
    '''Lista_ID : Lista_ID coma id
               | id '''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
        concatenar_gramatica('\n <TR><TD> LISTA_ID → LISTA_ID , id </TD>  <TD> </TD></TR>')
    else:
        p[0] = [p[1]]
        concatenar_gramatica('\n <TR><TD> LISTA_ID → id </TD>  <TD> </TD></TR>')

def p_Lista_Enum(p):
    '''Lista_Enum : Lista_Enum coma char
               | char '''
    print(len(p))
    if len(p) == 4:
        p[0] = p[1]+[p[3]]
        concatenar_gramatica('\n <TR><TD> LISTA_ENUM → LISTA_ENUM , char </TD>  <TD> </TD></TR>')
    else:
        p[0] = [p[1]]
        concatenar_gramatica('\n <TR><TD> LISTA_ID → char </TD>  <TD> </TD></TR>')

def p_Lista_EXP(p):
    '''Lista_EXP : Lista_EXP coma EXP
               | EXP '''
    if len(p) == 4:
        p[0] = p[1]+[p[3]]
        concatenar_gramatica('\n <TR><TD> LISTA_EXP → LISTA_EXP , EXP </TD>  <TD> </TD></TR>')
    else:
        p[0] = p[1]
        concatenar_gramatica('\n <TR><TD> LISTA_EXP →  EXP </TD>  <TD> </TD></TR>')

def p_Lista_Alias(p):
    '''Lista_Alias : Lista_Alias coma Nombre_Alias
               | Nombre_Alias '''
    if len(p) == 4:
        p[0] = p[1]+[p[3]]
        concatenar_gramatica('\n <TR><TD> LISTA_ALIAS → LISTA_ALIAS , Nombre_Alias </TD>  <TD> </TD></TR>')
    else:
        p[0] = p[1]
        concatenar_gramatica('\n <TR><TD> LISTA_ALIAS → Nombre_Alias </TD>  <TD> </TD></TR>')

def p_Nombre_Alias(p):
    '''Nombre_Alias : id id'''
    p[0] = p[1]
    concatenar_gramatica('\n <TR><TD> NOMBRE_ALIAS → id id </TD>  <TD> </TD></TR>')

def p_error(p):
    if not p:
        print('end of file')
        ListaErrores.insertar(err.Nodo_Error("Sintactico", "Se esperaba mas pero llega fin de texto", input.count('\n'), len(input)))
        return

    ListaErrores.insertar(err.Nodo_Error("Sintactico", str(p.value),
                                      p.lineno, find_column(input, p)))
    while True:
        tok = parser.token()
        if not tok or tok.type == 'pyc':
            break

def concatenar_gramatica(cadena):
    global reporteg
    reporteg = cadena + reporteg
    print('Gramatical:' + reporteg)

def parse(input1, errores1):
    global input
    global ListaErrores
    global reporteg
    ListaErrores = errores1
    reporteg = ''
    input = input1
    global parser
    parser = yacc.yacc()
    parser.errok()
    par = parser.parse(input, tracking=True, lexer=lexer)
    return par

