# GRUPO 5
# 201213062 - Mónica Raquel Calderon Muñoz
# 201213223 - Astrid Edith Hernandez Gonzalez
# 201213255 - Leonel Eduardo Avila Calvillo
# 201220159 - Diego Ahtohil Noj Armira
# 201220165 - Oscar Rolando Bernard Peralta

# IMPORT SECTION
import ply.lex as lex
import ply.yacc as yacc
from Expresiones import *
from Instrucciones import *
import re

# VARIABLES GLOBALES
counter_lexical_error = 1
counter_syntactic_error = 1

# LISTADO DE PALABRAS RESERVADAS
palabras_reservadas = {
    'select'        : 'SELECT',
    'where'         : 'WHERE',
    'limit'         : 'LIMIT',
    'group'         : 'GROUP',
    'by'            : 'BY',
    'having'        : 'HAVING',
    'order'         : 'ORDER',
    'asc'           : 'ASC',
    'desc'          : 'DESC',
    'offset'        : 'OFFSET',
    'nulls'         : 'NULLS',
    'last'          : 'LAST',
    'first'         : 'FIRST',
    'as'            : 'AS',
    'is'            : 'IS',
    'isnull'        : 'ISNULL',
    'notnull'       : 'NOTNULL',
    'and'           : 'AND',
    'or'            : 'OR',
    'true'          : 'TRUE',
    'false'         : 'FALSE',
    'not'           : 'NOT',
    'distinct'      : 'DISTINCT',
    'count'         : 'COUNT',
    'avg'           : 'AVG',
    'sum'           : 'SUM',
    'max'           : 'MAX',
    'min'           : 'MIN',
    'greatest'      : 'GREATEST',
    'least'         : 'LEAST',
    'unknown'       : 'UNKNOWN',
    'between'       : 'BETWEEN',
    'simmetric'     : 'SIMMETRIC',
    'null'          : 'NULL',
    'union'         : 'UNION',
    'all'           : 'ALL',
    'intersect'     : 'INTERSECT',
    'except'        : 'EXCEPT',
    'case'          : 'CASE',
    'when'          : 'WHEN',
    'end'           : 'END',
    'then'          : 'THEN',
    'else'          : 'ELSE',
    'pi'            : 'PI',
    'in'            : 'IN',
    'any'           : 'ANY',
    'some'          : 'SOME',
    'like'          : 'LIKE',
    'substring'     : 'SUBSTRING',
    'substr'        : 'SUBSTR',
    'trim'          : 'TRIM',
    'leading'       : 'LEADING',
    'trailing'      : 'TRAILING',
    'both'          : 'BOTH',
    'encode'        : 'ENCODE',
    'decode'        : 'DECODE',
    'abs'           : 'ABS',
    'cbrt'          : 'CBRT',
    'ceil'          : 'CEIL',
    'ceiling'       : 'CEILING',
    'degrees'       : 'DEGREES',
    'div'           : 'DIV',
    'factorial'     : 'FACTORIAL',
    'floor'         : 'FLOOR',
    'gcd'           : 'GCD',
    'ln'            : 'LN',
    'log'           : 'LOG',
    'mod'           : 'MOD',
    'power'         : 'POWER',
    'radians'       : 'RADIANS',
    'round'         : 'ROUND',
    'sign'          : 'SIGN',
    'sqrt'          : 'SQRT',
    'width_bucket'  : 'WIDTH_BUCKET',
    'trunc'         : 'TRUNC',
    'random'        : 'RANDOM',
    'exp'           : 'FEXP',
    'extract'       : 'EXTRACT',
    'now'           : 'NOW',
    'hour'          : 'HOUR',
    'minute'        : 'MINUTE',
    'second'        : 'SECOND',
    'year'          : 'YEAR',
    'month'         : 'MONTH',
    'day'           : 'DAY',
    'timestamp'     : 'TIMESTAMP',
    'interval'      : 'INTERVAL',
    'date_part'     : 'DATE_PART',
    'current_date'  : 'CURRENT_DATE',
    'current_time'  : 'CURRENT_TIME',
    'length'        : 'LENGTH',
    'sha256'        : 'SHA256',
    'date'          : 'DATE',
    'integer'       : 'INTEGER',
    'convert'       : 'CONVERT',
    'create'        : 'CREATE',
    'replace'       : 'REPLACE',
    'database'      : 'DATABASE',
    'if'            : 'IF',
    'exists'        : 'EXISTS',
    'owner'         : 'OWNER',
    'mode'          : 'MODE',
    'alter'         : 'ALTER',
    'drop'          : 'DROP',
    'show'          : 'SHOW',
    'rename'        : 'RENAME',
    'to'            : 'TO',
    'insert'        : 'INSERT',
    'update'        : 'UPDATE',
    'set'           : 'SET',
    'into'          : 'INTO',
    'values'        : 'VALUES',
    'table'         : 'TABLE',
    'from'          : 'FROM',
    'delete'        : 'DELETE',
    'acos'          : 'ACOS',
    'acosd'         : 'ACOSD',
    'asin'          : 'ASIN',
    'asind'         : 'ASIND',
    'atan'          : 'ATAN',
    'atand'         : 'ATAND',
    'atan2'         : 'ATAN2',
    'atan2d'        : 'ATAN2D',
    'cos'           : 'COS',
    'cosd'          : 'COSD',
    'cot'           : 'COT',
    'cotd'          : 'COTD',
    'sin'           : 'SIN',
    'sind'          : 'SIND',
    'tan'           : 'TAN',
    'tand'          : 'TAND',
    'sinh'          : 'SINH',
    'cosh'          : 'COSH',
    'tanh'          : 'TANH',
    'asinh'         : 'ASINH',
    'acosh'         : 'ACOSH',
    'atanh'         : 'ATANH',
    'get_byte'      : 'GETBYTE',
    'set_byte'      : 'SETBYTE',
    'inherits'      : 'INHERITS',
    'primary'       : 'PRIMARY',
    'key'           : 'KEY',
    'foreign'       : 'FOREIGN',
    'references'    : 'REFERENCES',
    'constraint'    : 'CONSTRAINT',
    'check'         : 'CHECK',
    'unique'        : 'UNIQUE',
    'default'       : 'DEFAULT',
    'smallint'      : 'SMALLINT',
    'bigint'        : 'BIGINT',
    'numeric'       : 'NUMERIC',
    'real'          : 'REAL',
    'double'        : 'DOUBLE',
    'money'         : 'MONEY',
    'character'     : 'CHARACTER',
    'varchar'       : 'VARCHAR',
    'char'          : 'CHAR',
    'text'          : 'TEXT',
    'time'          : 'TIME',
    'boolean'       : 'BOOLEAN',
    'varying'       : 'VARYING',
    'type'          : 'TYPE',
    'enum'          : 'ENUM',
    'add'           : 'ADD',
    'column'        : 'COLUMN',
    'use'           : 'USE'
}

# LISTADO DE SIMBOLOS Y TOKENS
tokens = [
    'COMA',
    'ID',
    'PABRE',
    'PCIERRA',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'MODULO',
    'EXP',
    'PUNTO',
    'IGUAL',     
    'DIF',       
    'DIF1',      
    'MENOR',     
    'MENORIGUAL',
    'MAYOR',     
    'MAYORIGUAL',
    'NUMERO',
    'DECIMAL',
    'CADENA',
    'PCOMA',
    'IDALIAS',
    'raizCuadrada',
    'raizCubica',
    'BAnd',
    'BOr',
    'BXor',
    'BNot',
    'DesplazaI',
    'DesplazaD',
    'CADENASI'
] + list(palabras_reservadas.values())

# EXPRESIONES REGULARES PARA TOKENS
t_COMA            = r','
t_PABRE           = r'\('
t_PCIERRA         = r'\)'
t_MAS             = r'\+'
t_MENOS           = r'-'
t_POR             = r'\*'
t_DIVIDIDO        = r'/'
t_MODULO          = r'\%'
t_EXP             = r'\^'
t_PUNTO           = r'\.'
t_IGUAL           = r'\='
t_DIF             = r'<>'
t_DIF1            = r'!='
t_MENOR           = r'<'
t_MENORIGUAL      = r'<='
t_MAYOR           = r'>'
t_MAYORIGUAL      = r'>='
t_PCOMA           = r';'
t_raizCuadrada    = r'\|\/'
t_raizCubica      = r'\|\|\/'
t_BAnd            = r'&'
t_BOr             = r'\|'
t_BXor            = r'#'
t_BNot            = r'~'
t_DesplazaI       = r'<<'
t_DesplazaD       = r'>>'

# TOKENS IGNORADOS
t_ignore = " \t"


def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_NUMERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = palabras_reservadas.get(t.value.lower(),'ID')    
    return t

def t_IDALIAS(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    return t

def t_CADENA(t):
    r'\'.*?\''
    t.value = t.value[1:-1] 
    return t 

def t_CADENASI(t):
    r'\'.*?\''
    t.value = t.value[1:-1] 
    return t 

def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

def t_COMENTARIO_SIMPLE(t):
    r'--.*\n'
    t.lexer.lineno += 1


# Function to count lines in input
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


# Function to get column of a token
def get_column(p_input, p_token):
    line = p_input.rfind('\n', 0, p_token.lexpos) + 1
    column = (p_token.lexpos - line) + 1
    return column


# Function to print LEXICAL ERRORS
def t_error(t):
    global counter_lexical_error
    print("CARACTER ILEGAL '%s'" % t.value[0])
    err = open("reports/error_lexical.txt", "a+")
    txt = '<tr><td>' + str(counter_lexical_error) + '</td>'
    txt += '<td>' + str(t.value[0]) + '</td>'
    txt += '<td>' + 'Caracter ingresado no admitido.' + '</td>'
    txt += '<td>' + str(t.lexer.lineno) + '</td>'
    txt += '<td>' + str(get_column(t.lexer.lexdata, t)) + '</td><tr>\n'
    err.write(txt)
    err.close()
    counter_lexical_error += 1
    t.lexer.skip(1)


# BUILDING LEXICAL FILES
lexer = lex.lex(reflags=re.IGNORECASE)


# OPERATORS PRECEDENCE
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('nonassoc', 'IS', 'ISNULL', 'NOTNULL'),
    ('left', 'MENORIGUAL', 'MAYORIGUAL', 'IGUAL', 'DIF', 'DIF1', 'MENOR', 'MAYOR'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO', 'MODULO'),
    ('left', 'EXP'),
    ('right', 'UMENOS', 'UMAS'),
    ('nonassoc', 'BETWEEN', 'NOTB')
)


# GRAMMAR DEFINITION
def p_init(t):
    """
        init            :   INSTRUCCIONES
    """
    t[0] = t[1]


def p_instrucciones1(t):
    """
        INSTRUCCIONES   :   INSTRUCCIONES INSTRUCCION
    """
    t[1].append(t[2])
    t[0] = t[1]


def p_instrucciones2(t):
    """
        INSTRUCCIONES   :   INSTRUCCION
    """
    t[0] = [t[1]]


def p_instruccion1(t):
    """
        INSTRUCCION     :   I_SELECT COMPLEMENTOSELECT
    """
    t[0] = t[1]


def p_instruccion2(t):
    """
        INSTRUCCION     :   I_CREATE
                        |   I_DROP
                        |   I_INSERT
                        |   I_ALTER
                        |   I_UPDATE
                        |   I_SHOW
                        |   I_DELETE
                        |   I_USE
    """
    t[0] = t[1]


def p_use(t):
    """
        I_USE           :   USE DATABASE ID PCOMA
    """
    t[0] = t[1]


def p_create(t):
    """
        I_CREATE        :   CREATE I_TCREATE
    """
    t[0] = t[2]
    # CLASE CREATE


def p_tcreate(t):
    """
        I_TCREATE       :   I_REPLACE
                        |   I_CTABLE
                        |   I_CTYPE
    """
    t[0] = t[1]
    # INSTRUCCION CREATE (I_REPLACE)
    # INSTRUCCION CREATE1 (I_CTABLE)
    # INSTRUCCION CREATE2 (I_CTYPE)


def p_ctype(t):
    """
        I_CTYPE       : TYPE ID AS ENUM PABRE I_LCAD PCIERRA
    """
    # Instruccion


def p_lcad1(t):
    """
        I_LCAD          :   I_LCAD CADENASI
    """
    # Instruccion


def p_lcad2(t):
    """
        I_LCAD          :   CADENASI
    """
    # Instruccion


def p_ctable(t):
    """
        I_CTABLE        :   TABLE ID PABRE I_LTATRIBUTOS PCIERRA I_INHERITS
    """
    # Instruccion


def p_inherits(t):
    'I_INHERITS    : INHERITS PABRE ID PCIERRA PCOMA'

def p_tAtributos(t):
    'I_LTATRIBUTOS    : I_LTATRIBUTOS COMA I_TATRIBUTOS'

def p_tAtributos1(t):
    'I_LTATRIBUTOS    : I_TATRIBUTOS'

def p_atributosT(t):
    'I_TATRIBUTOS     : ID I_TIPO I_LLAVES'

def p_atributosT1(t):
    'I_TATRIBUTOS     : PRIMARY KEY PABRE I_LIDS PCIERRA'

def p_atributosT2(t):
    'I_TATRIBUTOS     : FOREIGN KEY PABRE I_LIDS PCIERRA REFERENCES ID PABRE I_LIDS PCIERRA'

def p_atributosT3(t):
    'I_TATRIBUTOS     : CONSTRAINT ID CHECK I_CCHECK'

def p_atributosT4(t):
    'I_TATRIBUTOS     : CHECK I_CCHECK'

def p_ccheck(t):
    'I_CCHECK         : PABRE CONDICION PCIERRA'

def p_atributosT5(t):
    'I_TATRIBUTOS     : UNIQUE I_UNIQUE'

def p_unique(t):
    'I_UNIQUE         : PABRE I_LIDS PCIERRA'

def p_llave(t):
    'I_LLAVES         : PRIMARY KEY I_DEFAULT'

def p_default(t):
    'I_DEFAULT        : DEFAULT I_VALOR I_NULL'

def p_default1(t):
    'I_DEFAULT        : I_NULL'

def p_null(t):
    'I_NULL           : NOT NULL I_CUNIQUE '

def p_null1(t):
    'I_NULL           : NULL I_CUNIQUE '

def p_null2(t):
    'I_NULL           : I_CUNIQUE '

def p_cunique(t):
    'I_CUNIQUE        : CONSTRAINT ID UNIQUE I_CHECK'

def p_check(t):
    'I_CHECK          : CONSTRAINT ID CHECK PABRE CONDICION PCIERRA'

def p_check1(t):
    'I_CHECK          : CHECK PABRE CONDICION PCIERRA'

def p_check2(t):
    'I_CHECK          : '

def p_llave2(t):
    'I_LLAVES         : REFERENCES ID PABRE I_CREFERENCE PCIERRA I_DEFAULT' 

def p_cRef(t):
    'I_CREFERENCE     : I_CREFERENCE COMA ID'

def p_cRef2(t):
    'I_CREFERENCE     : ID'

def p_llave3(t):
    'I_LLAVES         : REFERENCES ID I_DEFAULT'

def p_llave4(t):
    'I_LLAVES         : I_DEFAULT'

def p_lIds(t):
    'I_LIDS           : I_LIDS COMA ID'

def p_lIds1(t):
    'I_LIDS           : ID'

def p_tipo(t):
    'I_TIPO           : SMALLINT'

def p_tipo2(t):
    'I_TIPO           : INTEGER'

def p_tipo3(t):
    'I_TIPO           : BIGINT'

def p_tipo4(t):
    'I_TIPO           : DECIMAL'

def p_tipo5(t):
    'I_TIPO           : NUMERIC'

def p_tipo6(t):
    'I_TIPO           : REAL'

def p_tipo7(t):
    'I_TIPO           : DOUBLE I_PREC'

def p_tipo8(t):
    'I_TIPO           : MONEY'

def p_tipo9(t):
    'I_TIPO           : CHARACTER I_TCHAR'

def p_tipo11(t):
    'I_TIPO           : VARCHAR PABRE NUMERO PCIERRA'

def p_tipo22(t):
    'I_TIPO           : CHAR PABRE NUMERO PCIERRA'

def p_tipo33(t):
    'I_TIPO           : TEXT'

def p_tipo44(t):
    'I_TIPO           : TIMESTAMP I_PREC'

def p_tipo55(t):
    'I_TIPO           : TIME I_PREC'

def p_tipo66(t):
    'I_TIPO           : DATE'

def p_tipo77(t):
    'I_TIPO           : INTERVAL I_FIELDS I_PREC'

def p_tipo88(t):
    'I_TIPO           : BOOLEAN'

def p_tipo99(t):
    'I_TIPO           : ID'

def p_tchar(t):
    'I_TCHAR          : VARYING PABRE NUMERO PCIERRA'

def p_tchar1(t):
    'I_TCHAR          : PABRE NUMERO PCIERRA'

def p_prec(t):
    'I_PREC           : PABRE NUMERO PCIERRA'

def p_prec1(t):
    'I_PREC           : '

def p_fields(t):
    'I_FIELDS         : MONTH'

def p_fields1(t):
    'I_FIELDS         : HOUR'

def p_fields2(t):
    'I_FIELDS         : MINUTE'

def p_fields3(t):
    'I_FIELDS         : SECOND'

def p_fields4(t):
    'I_FIELDS         : YEAR'

def p_inherits1(t):
    'I_INHERITS    : PCOMA'


def p_Replace(t):
    'I_REPLACE     : OR REPLACE DATABASE I_EXIST'
    t[0] = t[4]
def p_Replace1(t):
    'I_REPLACE     : DATABASE I_EXIST'
    t[0] = t[2]

def p_drop(t):
    'I_DROP      : DROP I_TDROP ' 

def p_alter(t):
    'I_ALTER     : ALTER I_TALTER'

def p_tAlter(t):
    'I_TALTER    : I_ALTERDB'

def p_tAlter1(t):
    'I_TALTER    : I_ALTERTB'

def p_alterTB(t):
    'I_ALTERTB   : TABLE ID I_OPALTER '

def p_opAlterTB(t):
    'I_OPALTER   : I_LADDC PCOMA'

def p_opAlterTB1(t):
    'I_OPALTER   : I_LDROPC PCOMA'

def p_opAlterTB2(t):
    'I_OPALTER   : ADD I_TALTER PCOMA'

def p_opAlterTB3(t):
    'I_OPALTER   : ALTER COLUMN ID SET NOT NULL PCOMA'

def p_opAlterTB4(t):
    'I_OPALTER   : DROP CONSTRAINT ID PCOMA'

def p_opAlterTB5(t):
    'I_OPALTER   : ID I_LCOL PCOMA'

def p_lCol(t):
    'I_LCOL      : I_LCOL COMA I_PCOL'

def p_lCol2(t):
    'I_LCOL      : I_PCOL'

def p_pCol3(t):
    'I_PCOL      : ALTER COLUMN ID TYPE VARCHAR PABRE NUMERO PCIERRA'

def p_tipAlterC(t): 
    'I_TALTER    : CHECK CONDICION '

def p_tipAlterU(t): 
    'I_TALTER    : UNIQUE PABRE I_LIDS  PCIERRA'

def p_tipAlterFK(t): 
    'I_TALTER    : FOREIGN KEY PABRE I_LIDS PCIERRA REFERENCES ID PABRE I_LIDS PCIERRA '

def p_tipAlterCo(t): 
    'I_TALTER    : CONSTRAINT ID I_TCONST '

def p_tipoConstraintC(t):
    'I_TCONST    : CHECK CONDICION '

def p_tipoConstraintU(t):
    'I_TCONST    : UNIQUE PABRE I_LIDS PCIERRA'

def p_tipoConstraintFK(t):
    'I_TCONST    : FOREIGN KEY PABRE I_LIDS PCIERRA REFERENCES ID PABRE I_LIDS PCIERRA  '

def p_lCDrop(t):
    'I_LDROPC    : I_LDROPC COMA I_DROPC'

def p_lCDrop1(t):
    'I_LDROPC    : I_DROPC'

def p_cDrop(t):
    'I_DROPC     : DROP COLUMN ID'

def p_lCAdd(t):
    'I_LADDC     : I_LADDC COMA I_ADDC'

def p_lCAdd2(t):
    'I_LADDC     : I_ADDC'

def p_cAdd(t):
    'I_ADDC      : ADD COLUMN ID I_TIPO'

def p_tDrop(t):
    'I_TDROP     : I_DROPDB'
    # INSTRUCCION DROP

def p_tDrop2(t):
    'I_TDROP     : I_DROPTB'

def p_dropDB(t):
    'I_DROPDB    : DATABASE I_IFEXIST'
    # INSTRUCCION DROPDB

def p_ifExist(t):
    'I_IFEXIST     : IF EXISTS ID PCOMA'
    # INSTRUCCION IFEXIST

def p_ifExist2(t):
    'I_IFEXIST     : ID PCOMA'
    # INSTRUCCION IFEXIST 

def p_Exist(t):
    'I_EXIST       : IF NOT EXISTS ID I_OWMOD '
    t[0] = t[4]
def p_Exist1(t):
    'I_EXIST       : ID PCOMA'
    t[0] = t[1]

def p_Owmod(t):
    'I_OWMOD       : OWNER IGUAL ID I_MODE'

def p_Owmod1(t):
    'I_OWMOD       : MODE IGUAL ID I_OWNER'

def p_Owmod2(t):
    'I_OWMOD       : PCOMA'

def p_Mode(t):
    'I_MODE        : MODE IGUAL ID PCOMA'

def p_Mode1(t):
    'I_MODE        : PCOMA'

def p_Owner(t):
    'I_OWNER       : OWNER IGUAL ID PCOMA'

def p_Owner1(t):
    'I_OWNER       : PCOMA'

def p_AlterDB(t):
    'I_ALTERDB     : ALTER DATABASE ID I_OPALTERDB I_VALALTDB'

def p_opAlterDB(t):
    'I_OPALTERDB   : RENAME TO'

def p_opAlterDB2(t):
    'I_OPALTERDB   : OWNER TO'

def p_valAlterDb(t):
    'I_VALALTDB    : ID'

def p_valAlterDb1(t):
    'I_VALALTDB    : CADENASI'

def p_dropTB(t):
    'I_DROPTB      : TABLE ID PCOMA'

def p_insertTB(t):
    'I_INSERT      : INSERT INTO ID VALUES PABRE I_LVALT PCIERRA PCOMA'

def p_lValt(t):
    'I_LVALT       : I_LVALT COMA I_VALTAB'

def p_update(t):
    'I_UPDATE      : UPDATE ID SET I_LUPDATE PWHERE '

def p_lUpdate(t):
    'I_LUPDATE     : I_LUPDATE COMA I_VALUPDATE'

def p_lUpdate1(t):
    'I_LUPDATE     : I_VALUPDATE'

def p_valUpdate(t):
    'I_VALUPDATE   : ID IGUAL I_VALOR'

def p_valor(t):
    'I_VALOR       : CADENASI'

def p_valor1(t):
    'I_VALOR      : NUMERO'

def p_show(t):
    'I_SHOW       : SHOW DATABASE PCOMA'

def p_delete(t):
    'I_DELETE     : DELETE FROM ID PWHERE'

def p_lValt1(t):
    'I_LVALT       : I_VALTAB'

def p_valTab(t):
    'I_VALTAB      : NUMERO'

def p_valTab1(t):
    'I_VALTAB      : CADENASI'

def p_ISelect(t):
    'I_SELECT  :   SELECT VALORES PFROM COMPLEMENTO   '
    #CLASE SELECT MINIMO
    
def p_ISelect1(t):
    'I_SELECT  :   SELECT VALORES PFROM PWHERE COMPLEMENTO    '
    # INSTRUCCION SELECT WITH WHERE 


def p_ISelect2(t):
    'I_SELECT  :   SELECT DISTINCT VALORES PFROM COMPLEMENTO   '
     # INSTRUCCION SELECT DISTINCT 

def p_ISelect3(t):
    'I_SELECT  :   SELECT DISTINCT VALORES PFROM PWHERE COMPLEMENTO    '
    # INSTRUCCION SELECT DISTINCT WITH WHERE

def p_ISelect4(t):
    'I_SELECT   :   SELECT VALORES '
    #INSTRUCCION SELECT SOLO VALORES 

def p_ComplementoH(t):
    'COMPLEMENTO  :   PGROUPBY PHAVING  '

def p_ComplementoHL(t):
    'COMPLEMENTO  :   PGROUPBY PHAVING PLIMIT   '

def p_ComplementoG(t):
    'COMPLEMENTO  :   PGROUPBY  '

def p_ComplementoGL(t):
    'COMPLEMENTO  :   PGROUPBY PLIMIT   '

def p_ComplementoO(t):
    'COMPLEMENTO  :   PORDERBY  '

def p_ComplementoOL(t):
    'COMPLEMENTO  :   PORDERBY PLIMIT   '

def p_ComplementoL(t):
    'COMPLEMENTO  :   PLIMIT    '

def p_ComplementoE(t):
    'COMPLEMENTO  :   EMPTY '

def p_ComplementoSelectUnion(t):
    'COMPLEMENTOSELECT  : UNION I_SELECT PCOMA  '
    # INSTRUCCION COMPLEMENTOSELECTUNION

def p_ComplementoSelectUnionAll(t):
    'COMPLEMENTOSELECT  : UNION ALL I_SELECT PCOMA '
    # INSTRUCCION COMPLEMENTOSELECTALL

def p_ComplementoSelectIntersect(t):
    'COMPLEMENTOSELECT  : INTERSECT I_SELECT PCOMA '
    # INSTRUCCION COMPLEMENTOSELECTINTERSECT

def p_ComplementoSelectIntersectALL(t):
    'COMPLEMENTOSELECT  : INTERSECT ALL I_SELECT PCOMA '
    # INSTRUCCION COMPLEMENTOSELECTINTERSECTALL

def p_ComplementoSelectExcept(t):
    'COMPLEMENTOSELECT  : EXCEPT I_SELECT PCOMA '
    # INSTRUCCION COMPLEMENTOSELECTEXCEPT

def p_ComplementoSelectExceptAll(t):
    'COMPLEMENTOSELECT  : EXCEPT ALL I_SELECT PCOMA '
    # INSTRUCCION COMPLEMENTOSELECTEXCEPTALL

def p_ComplementoSelectExceptPcoma(t):
    'COMPLEMENTOSELECT  : PCOMA '
    # INSTRUCCION COMPLEMENTOSELECTEXCEPTPCOMA

def p_Limit(t):
    'PLIMIT  :   LIMIT CONDICION    '

def p_LimitOff(t):
    'PLIMIT  :   LIMIT CONDICION OFFSET CONDICION   '

def p_OrderBy(t):
    'PORDERBY  :   ORDER BY LCOMPLEMENTOORDERBY '

def p_ComplementoOrderL(t):
    'LCOMPLEMENTOORDERBY  :   LCOMPLEMENTOORDERBY COMA COMPLEMENTOORDERBY  '

def p_ComplementoOrderL1(t):
    'LCOMPLEMENTOORDERBY  :   COMPLEMENTOORDERBY    '

def p_ComplementoOrderCI(t):
    'COMPLEMENTOORDERBY  :   ID COMPLEMENTOORDERBY1    '

def p_ComplementoOrderCOBC(t):
    'COMPLEMENTOORDERBY1  :   COMPLEMENTOORDER   '

def p_ComplementoOrderCOBP(t):
    'COMPLEMENTOORDERBY1  :   PUNTO ID COMPLEMENTOORDER   '


def p_ComplementoOrder(t):
    'COMPLEMENTOORDER  :   ASC  '

def p_ComplementoOD(t):
    'COMPLEMENTOORDER  :   DESC '

def p_ComplementoOANF(t):
    'COMPLEMENTOORDER  :   ASC NULLS FIRST  '

def p_ComplementoOANL(t):
    'COMPLEMENTOORDER  :   ASC NULLS LAST   '

def p_ComplementoODNF(t):
    'COMPLEMENTOORDER  :   DESC NULLS FIRST '

def p_ComplementoODNL(t):
    'COMPLEMENTOORDER  :   DESC NULLS LAST  '

def p_ComplementoEm(t):
    'COMPLEMENTOORDER  :   EMPTY    '


def p_Having(t):
    'PHAVING  :   HAVING CONDICION '

def p_GroupBy(t):
    'PGROUPBY  :   GROUP BY LCOMPLEMENTOGROUP '

def p_ComplementoGroupL(t):
    'LCOMPLEMENTOGROUP  :   LCOMPLEMENTOGROUP COMA COMPLEMENTOGROUP '

def p_ComplementoGroupLS(t):
    'LCOMPLEMENTOGROUP  :   COMPLEMENTOGROUP '

def p_ComplementoGroupC(t):
    'COMPLEMENTOGROUP  :   ID '

def p_ComplementoGroupC1(t):
    'COMPLEMENTOGROUP  :   ID PUNTO ID '

def p_Valores(t):
    'VALORES  :   POR '

def p_ValoresLista(t):
    'VALORES  :   LISTAVALORES '

def p_ListaValores(t):
    'LISTAVALORES  :   LISTAVALORES COMA VALOR '

def p_ListaValoresS(t):
    'LISTAVALORES  :   VALOR '


def p_ValorSub(t):
    'VALOR  :   PABRE SUBCONSULTA PCIERRA ALIAS'

def p_ValorSub1(t):
    'VALOR  :   PABRE SUBCONSULTA PCIERRA '

def p_ValorCountAa(t):
    'VALOR  :   COUNT PABRE POR PCIERRA ALIAS'

def p_ValorCounta(t):
    'VALOR  :   COUNT PABRE ID PCIERRA ALIAS'

def p_ValorCountA(t):
    'VALOR  :   COUNT PABRE POR PCIERRA '

def p_ValorCount(t):
    'VALOR  :   COUNT PABRE ID PCIERRA '

def p_ValorCountAliasId(t):
    'VALOR  :   COUNT PABRE ID PUNTO ID PCIERRA ALIAS'

def p_ValorCountIdP(t):
    'VALOR  :   COUNT PABRE ID PUNTO ID PCIERRA'

def p_ValorFunciones(t):
    'VALOR  :   FUNCION PABRE ID PUNTO ID PCIERRA'

def p_ValorFunciones1(t):
    'VALOR  :   FUNCION PABRE ID  PCIERRA'

def p_ValorFuncionesA(t):
    'VALOR  :   FUNCION PABRE ID PUNTO ID PCIERRA ALIAS'

def p_ValorFunciones1A(t):
    'VALOR  :   FUNCION PABRE ID  PCIERRA ALIAS'

def p_ValorCondicion(t):
    'VALOR  :   CONDICION'
    
def p_ValorCondicionAlias(t):
    'VALOR  :   CONDICION ALIAS '

def p_ValorFTrigonometricas(t):
    'VALOR  :   FTRIGONOMETRICAS PABRE LNUM PCIERRA '

def p_ValorFTrigonometricasAlias(t):
    'VALOR  :   FTRIGONOMETRICAS PABRE LNUM PCIERRA ALIAS '

def p_ValorGreatest(t):
    'VALOR  :   GREATEST PABRE LNUM PCIERRA '

def p_ValorLeast(t):
    'VALOR  :   LEAST PABRE LNUM PCIERRA '

def p_ValorGreatestAlias(t):
    'VALOR  :   GREATEST PABRE LNUM PCIERRA ALIAS'

def p_ValorLeastAlias(t):
    'VALOR  :   LEAST PABRE LNUM PCIERRA ALIAS'

def p_ValorRandomA(t):
    'VALOR  :   RANDOM PABRE PCIERRA ALIAS'

def p_ValorRandom(t):
    'VALOR  :   RANDOM PABRE PCIERRA '

def p_ValorPiAlias(t):
    'VALOR  :   PI PABRE PCIERRA   ALIAS '
    
def p_ValorPi(t):
    'VALOR  :   PI PABRE PCIERRA '

def p_ValorFuncionesDecodeA(t):
    'VALOR  :   DECODE PABRE CADENA COMA CADENA PCIERRA ALIAS   '

def p_ValorFuncionesDecode(t):
    'VALOR  :   DECODE PABRE CADENA COMA CADENA PCIERRA   '

def p_ValorFuncionesEncodeA(t):
    'VALOR  :   ENCODE PABRE CADENA COMA CADENA PCIERRA ALIAS   '

def p_ValorFuncionesEncode(t):
    'VALOR  :   ENCODE PABRE CADENA COMA CADENA PCIERRA   '

def p_ValorFuncionesConvertDate(t):
    'VALOR  :   CONVERT PABRE CADENA AS DATE PCIERRA   '

def p_ValorFuncionesConvertInt(t):
    'VALOR  :   CONVERT PABRE CADENA AS INTEGER PCIERRA   '

def p_ValorFuncionesConvertDateA(t):
    'VALOR  :   CONVERT PABRE CADENA AS DATE PCIERRA ALIAS   '

def p_ValorFuncionesConvertIntA(t):
    'VALOR  :   CONVERT PABRE CADENA AS INTEGER PCIERRA ALIAS   '

def p_ValorFuncionesSha(t):
    'VALOR  :   SHA256 PABRE CADENA PCIERRA   '

def p_ValorFuncionesShaA(t):
    'VALOR  :   SHA256 PABRE CADENA PCIERRA ALIAS   '

def p_ValorOperadorMatAlias(t):
    'VALOR  :   NUM OPERADOR NUM ALIAS '

def p_ValorOperadorMat(t):
    'VALOR  :   NUM OPERADOR NUM '

def p_ValorOperadorNotA(t):
    'VALOR  :   BNot NUM ALIAS '

def p_ValorOperadorNot(t):
    'VALOR  :   BNot NUM '

def p_ValorRaizCuadradaA(t):
    'VALOR  :   raizCuadrada NUM ALIAS '

def p_ValorRaizCuadrada(t):
    'VALOR  :   raizCuadrada NUM '

def p_ValorRaizCubicaA(t):
    'VALOR  :   raizCubica NUM ALIAS '

def p_ValorRaizCubica(t):
    'VALOR  :   raizCubica NUM '

def p_ValorFuncionesGetByte(t):
    'VALOR  :   GETBYTE PABRE CADENA COMA NUMERO PCIERRA '

def p_ValorFuncionesGetByteA(t):
    'VALOR  :   GETBYTE PABRE CADENA COMA NUMERO PCIERRA ALIAS '

def p_ValorFuncionesSetByte(t):
    'VALOR  :   SETBYTE PABRE CADENA COMA NUMERO COMA NUMERO PCIERRA '

def p_ValorFuncionesSetByteA(t):
    'VALOR  :   SETBYTE PABRE CADENA COMA NUMERO COMA NUMERO PCIERRA ALIAS '

def p_ValorCase(t):
    'VALOR  :   CASE LWHEN END '

def p_ValorCaseAlias(t):
    'VALOR  :   CASE LWHEN END ALIAS'

def p_ValorFunAlias(t):
    'VALOR  :   ID_VALOR PABRE LCONDICION_FUNCION PCIERRA ALIAS   '

def p_ValorFun(t):
    'VALOR  :   ID_VALOR PABRE LCONDICION_FUNCION PCIERRA   '

def p_LWHEN(t):
    'LWHEN  :   WHEN CONDICION THEN CONDICION LWHEN '

def p_LWHENSimple(t):
    'LWHEN  :   WHEN CONDICION THEN CONDICION '

def p_LWHENElse(t):
    'LWHEN  :   ELSE CONDICION '

def p_IdFuncionDegrees(t):
    'ID_VALOR  :   DEGREES  '

def p_IdFuncionDiv(t):
    'ID_VALOR  :   DIV  '

def p_IdFuncionExp(t):
    'ID_VALOR  :   FEXP  '

def p_IdFuncionFactorial(t):
    'ID_VALOR  :   FACTORIAL  '

def p_IdFuncionFloor(t):
    'ID_VALOR  :   FLOOR  '

def p_IdFuncionGcd(t):
    'ID_VALOR  :   GCD  '

def p_IdFuncionLn(t):
    'ID_VALOR  :   LN  '

def p_IdFuncionLog(t):
    'ID_VALOR  :   LOG  '

def p_IdFuncionMod(t):
    'ID_VALOR  :   MOD  '

def p_IdFuncionPower(t):
    'ID_VALOR  :   POWER  '

def p_IdFuncionRadians(t):
    'ID_VALOR  :   RADIANS  '

def p_IdFuncionRound(t):
    'ID_VALOR  :   ROUND  '

def p_IdFuncionSign(t):
    'ID_VALOR  :   SIGN  '

def p_IdFuncionSqrt(t):
    'ID_VALOR  :   SQRT  '

def p_IdFuncionWidth_bucket(t):
    'ID_VALOR  :   WIDTH_BUCKET  '

def p_IdFuncionTrunc(t):
    'ID_VALOR  :   TRUNC  '

def p_OPERADORAnd(t):
    'OPERADOR  :   BAnd '

def p_OPERADOROr(t):
    'OPERADOR  :   BOr '

def p_OPERADORXor(t):
    'OPERADOR  :   BXor '

def p_OPERADORDIz(t):
    'OPERADOR  :   DesplazaI '

def p_OPERADORDDe(t):
    'OPERADOR  :   DesplazaD '

def p_LNumNumLNum(t):
    'LNUM  : LNUM COMA NUM'

def p_LNumNum(t):
    'LNUM   : NUM'

def p_NumNumero(t):  
    'NUM    : NUMERO '

def p_NumDecimal(t):
    'NUM  :   DECIMAL '

def p_NumCadena(t):
    'NUM  :   CADENA '

def p_FTrigonometricasAcos(t):
    'FTRIGONOMETRICAS  :   ACOS '

def p_FTrigonometricasAcosd(t):
    'FTRIGONOMETRICAS  :   ACOSD '

def p_FTrigonometricasAsin(t):
    'FTRIGONOMETRICAS  :   ASIN '

def p_FTrigonometricasAsind(t):
    'FTRIGONOMETRICAS  :   ASIND '

def p_FTrigonometricasAtan(t):
    'FTRIGONOMETRICAS  :   ATAN '

def p_FTrigonometricasAtand(t):
    'FTRIGONOMETRICAS  :   ATAND '

def p_FTrigonometricasAtan2(t):
    'FTRIGONOMETRICAS  :   ATAN2 '

def p_FTrigonometricasAtan2d(t):
    'FTRIGONOMETRICAS  :   ATAN2D '

def p_FTrigonometricasCos(t):
    'FTRIGONOMETRICAS  :   COS '

def p_FTrigonometricasCosd(t):
    'FTRIGONOMETRICAS  :   COSD '

def p_FTrigonometricasCot(t):
    'FTRIGONOMETRICAS  :   COT '

def p_FTrigonometricasCotd(t):
    'FTRIGONOMETRICAS  :   COTD '

def p_FTrigonometricasSin(t):
    'FTRIGONOMETRICAS  :   SIN '

def p_FTrigonometricasSind(t):
    'FTRIGONOMETRICAS  :   SIND '

def p_FTrigonometricasTan(t):
    'FTRIGONOMETRICAS  :   TAN '

def p_FTrigonometricasTand(t):
    'FTRIGONOMETRICAS  :   TAND '

def p_FTrigonometricasSinh(t):
    'FTRIGONOMETRICAS  :   SINH '

def p_FTrigonometricasCosh(t):
    'FTRIGONOMETRICAS  :   COSH '

def p_FTrigonometricasTanh(t):
    'FTRIGONOMETRICAS  :   TANH '

def p_FTrigonometricasAsinh(t):
    'FTRIGONOMETRICAS  :   ASINH '

def p_FTrigonometricasAcosh(t):
    'FTRIGONOMETRICAS  :   ACOSH '

def p_FTrigonometricasAtanh(t):
    'FTRIGONOMETRICAS  :   ATANH '

def p_funcionAvg(t):
    'FUNCION    :   AVG'

def p_funcionSum(t):
    'FUNCION    :   SUM'

def p_funcionMin(t):
    'FUNCION    :   MIN'

def p_funcionMax(t):
    'FUNCION    :   MAX'

def p_Alias(t):
    'ALIAS  :   AS ID '

def p_AliasS(t):
    'ALIAS  :   ID '

def p_AliasC(t):
    'ALIAS  :   AS IDALIAS'

def p_AliasCS(t):
    'ALIAS  :   IDALIAS'

def p_FromIdA(t):
    'PFROM  :   FROM ID ALIAS '

def p_FromId(t):
    'PFROM  :   FROM ID '

def p_FromSub(t):
    'PFROM  :   FROM PABRE SUBCONSULTA PCIERRA ALIAS    '

def p_SubconsultaFrom(t):
    'SUBCONSULTA    :   SELECT VALORES PFROM COMPLEMENTO '

def p_SubconsultaFromW(t):
    'SUBCONSULTA    :   SELECT VALORES PFROM PWHERE COMPLEMENTO '


def p_Where(t):
    'PWHERE  :   WHERE CONDICION '

def p_CondicionIgual(t):
    'CONDICION  :   CONDICION IGUAL CONDICION '

def p_CondicionDif(t):
    'CONDICION  :   CONDICION DIF CONDICION '

def p_CondicionDif1(t):
    'CONDICION  :   CONDICION DIF1 CONDICION '

def p_CondicionMenor(t):
    'CONDICION  :   CONDICION MENOR CONDICION '

def p_CondicionMenorI(t):
    'CONDICION  :   CONDICION MENORIGUAL CONDICION '

def p_CondicionMayor(t):
    'CONDICION  :   CONDICION MAYOR CONDICION '

def p_CondicionMayorI(t):
    'CONDICION  :   CONDICION MAYORIGUAL CONDICION '

def p_CondicionAnd(t):
    'CONDICION  :   CONDICION AND CONDICION '

def p_CondicionOr(t):
    'CONDICION  :   CONDICION OR CONDICION '

def p_CondicionNot(t):
    'CONDICION  :   NOT CONDICION '

def p_CondicionParentesis(t):
    'CONDICION  :   PABRE CONDICION PCIERRA '

def p_CondicionMas(t):
    'CONDICION  :   CONDICION MAS CONDICION '

def p_CondicionMenos(t):
    'CONDICION  :   CONDICION MENOS CONDICION '

def p_CondicionPor(t):
    'CONDICION  :   CONDICION POR CONDICION '

def p_CondicionDiv(t):
    'CONDICION  :   CONDICION DIVIDIDO CONDICION '

def p_CondicionMod(t):
    'CONDICION  :   CONDICION MODULO CONDICION '

def p_CondicionExp(t):
    'CONDICION  :   CONDICION EXP CONDICION '

def p_CondicionIs(t):
    'CONDICION  :   CONDICION IS CONDICION '

def p_CondicionIsN(t):
    'CONDICION  :   CONDICION ISNULL CONDICION '

def p_CondicionNotN(t):
    'CONDICION  :   CONDICION NOTNULL CONDICION '

def p_CondicionM(t):
    'CONDICION  :   MENOS CONDICION %prec UMENOS'

def p_CondicionP(t):
    'CONDICION  :   MAS CONDICION %prec UMAS'

def p_CondicionExtract(t):
    'CONDICION  :   EXTRACT PABRE DATETIME FROM PTIMESTAMP PCIERRA '

def p_CondicionFuncionWhere(t):
    'CONDICION  :   FUNCIONES_WHERE '

def p_CondicionNum(t):
    'CONDICION  :   NUMERO '

def p_CondicionDec(t):
    'CONDICION  :   DECIMAL'

def p_CondicionCad(t):
    'CONDICION  :   CADENA '

def p_CondicionTrue(t):
    'CONDICION  :   TRUE '

def p_CondicionFalse(t):
    'CONDICION  :   FALSE '

def p_CondicionId(t):
    'CONDICION  :   ID '

def p_CondicionIdP(t):
    'CONDICION  :   ID PUNTO ID '

def p_CondicionFuncionSistema(t):
    'CONDICION  :   FUNCIONES_SISTEMA '

def p_CondicionDatePart(t):
    'CONDICION  :   DATE_PART PABRE CADENA COMA INTERVAL CADENA PCIERRA '

def p_CondicionCurrentDate(t):
    'CONDICION  :   CURRENT_DATE '

def p_CondicionCurrentTime(t):
    'CONDICION  :   CURRENT_TIME '

def p_CondicionTimeStamp(t):
    'CONDICION  :   TIMESTAMP CADENA '

def p_CondicionBetween(t):
    'CONDICION  :   CONDICION BETWEEN CONDICION '

def p_CondicionNotBetween(t):
    'CONDICION  :   CONDICION NOT BETWEEN CONDICION %prec NOTB'

def p_CondicionBetweenSimetric(t):
    'CONDICION  :   CONDICION BETWEEN SIMMETRIC CONDICION '

def p_CondicionBetweenNotSimetric(t):
    'CONDICION  :   CONDICION NOT BETWEEN SIMMETRIC CONDICION  %prec NOTB'

def p_CondicionIsDistinct(t):
    'CONDICION  :   CONDICION IS DISTINCT FROM CONDICION '

def p_CondicionIsNotDistinct(t):
    'CONDICION  :   CONDICION IS NOT DISTINCT FROM CONDICION '

def p_CondicionNull(t):
    'CONDICION  :   NULL '

def p_CondicionUnknown(t):
    'CONDICION  :   UNKNOWN '

def p_CondicionSubConsulta(t):
    'CONDICION  :   PABRE SUBCONSULTA PCIERRA '

def p_CondicionFunciones(t):
    'CONDICION  :   FUNCION PABRE ID PCIERRA'

def p_CondicionFunciones1(t):
    'CONDICION  :   FUNCION PABRE ID PUNTO ID PCIERRA'

def p_CondicionNow(t):
    'CONDICION  :   NOW PABRE PCIERRA '

def p_FuncionesSistemaAlias(t):
    'FUNCIONES_SISTEMA  :   ID_FUNCION PABRE LCONDICION_FUNCION PCIERRA ALIAS   '

def p_FuncionesSistema(t):
    'FUNCIONES_SISTEMA  :   ID_FUNCION PABRE LCONDICION_FUNCION PCIERRA   '

def p_FuncionesSistemaString(t):
    'FUNCIONES_SISTEMA  :   ID_FUNCION_S PABRE LCONDICION_FUNCION_S PCIERRA ALIAS   '

def p_FuncionesSistemaString1(t):
    'FUNCIONES_SISTEMA  :   ID_FUNCION_S PABRE LCONDICION_FUNCION_S PCIERRA   '

def p_FuncionesSistemaTrimA(t):
    'FUNCIONES_SISTEMA  :   TRIM PABRE LBOTH CADENA FROM CADENA PCIERRA ALIAS   '

def p_FuncionesSistemaTrim(t):
    'FUNCIONES_SISTEMA  :   TRIM PABRE LBOTH CADENA FROM CADENA PCIERRA   '

def p_FuncionesSistemaTrimA1(t):
    'FUNCIONES_SISTEMA  :   TRIM PABRE LBOTH FROM CADENA COMA CADENA PCIERRA ALIAS   '

def p_FuncionesSistemaTrim1(t):
    'FUNCIONES_SISTEMA  :   TRIM PABRE LBOTH FROM CADENA COMA CADENA PCIERRA   '

def p_Id_FuncionSubstring(t):
    'ID_FUNCION_S  :   SUBSTRING   '

def p_Id_FuncionLength(t):
    'ID_FUNCION_S  :   LENGTH   '

def p_Id_FuncionSubstr(t):
    'ID_FUNCION_S  :   SUBSTR   '

def p_LBOTHLeading(t):
    'LBOTH  :   LEADING   '

def p_LBOTHTrailing(t):
    'LBOTH  :   TRAILING   '

def p_LBOTHBoth(t):
    'LBOTH  :   BOTH   '

def p_LCondicionFuncion_Condicion(t):
    'LCONDICION_FUNCION_S  :   CONDICION   '

def p_LCondicionFuncion_S(t):
    'LCONDICION_FUNCION_S  :   CONDICION COMA NUMERO COMA NUMERO   '

def p_IdFuncionAbs(t):
    'ID_FUNCION  :   ABS  '

def p_IdFuncionCBRT(t):
    'ID_FUNCION  :   CBRT  '

def p_IdFuncionCeil(t):
    'ID_FUNCION  :   CEIL  '

def p_IdFuncionCeiling(t):
    'ID_FUNCION  :   CEILING  '

def p_LCondicionFuncion1(t):
    'LCONDICION_FUNCION  :   CONDICION  '

def p_LCondicionFuncion(t):
    'LCONDICION_FUNCION  :   LCONDICION_FUNCION COMA CONDICION  '

def p_DateTimeYear(t):
    'DATETIME  :   YEAR '

def p_DateTimeHour(t):
    'DATETIME  :   HOUR '

def p_DateTimeMinute(t):
    'DATETIME  :   MINUTE '

def p_DateTimeSecond(t):
    'DATETIME  :   SECOND '

def p_DateTimeMonth(t):
    'DATETIME  :   MONTH '
    
def p_DateTimeDay(t):
    'DATETIME  :   DAY '

def p_FuncionesWhereExist(t):
    'FUNCIONES_WHERE  :   EXISTS PABRE SUBCONSULTA PCIERRA   '

def p_FuncionesWhereIn(t):
    'FUNCIONES_WHERE  :   CONDICION IN PABRE SUBCONSULTA PCIERRA   '

def p_FuncionesWhereNotIn(t):
    'FUNCIONES_WHERE  :   CONDICION NOT IN PABRE SUBCONSULTA PCIERRA   '

def p_FuncionesWhereAny(t):
    'FUNCIONES_WHERE  :   CONDICION OPERATOR_FW ANY PABRE SUBCONSULTA PCIERRA   '

def p_FuncionesWhereAll(t):
    'FUNCIONES_WHERE  :   CONDICION OPERATOR_FW ALL PABRE SUBCONSULTA PCIERRA   '

def p_FuncionesWhereSome(t):
    'FUNCIONES_WHERE  :   CONDICION OPERATOR_FW SOME PABRE SUBCONSULTA PCIERRA   '

def p_FuncionesWhereLike(t):
    'FUNCIONES_WHERE  :   CONDICION LIKE CADENA   '

def p_FuncionesWhereNotLike(t):
    'FUNCIONES_WHERE  :   CONDICION NOT LIKE CADENA   '

def p_OperatorFwMenor(t):
    'OPERATOR_FW  :   MENOR   '

def p_OperatorFwMayor(t):
    'OPERATOR_FW  :   MAYOR   '

def p_OperatorFwMenorIgual(t):
    'OPERATOR_FW  :   MENORIGUAL   '

def p_OperatorFwMayorIgual(t):
    'OPERATOR_FW  :   MAYORIGUAL   '

def p_OperatorFwIgual(t):
    'OPERATOR_FW  :   IGUAL   '

def p_OperatorFwDif(t):
    'OPERATOR_FW  :   DIF   '

def p_OperatorFwDif1(t):
    'OPERATOR_FW  :   DIF1   '

def p_PTimestamC(t):
    'PTIMESTAMP  :   TIMESTAMP CADENA '

def p_PTimestamId(t):
    'PTIMESTAMP  :   TIMESTAMP ID '

def p_PTimestamIdPId(t):
    'PTIMESTAMP  :   TIMESTAMP ID PUNTO ID '

def p_PTimestamCadena(t):
    'PTIMESTAMP  :   CADENA '

def p_PTimestamId1(t):
    'PTIMESTAMP  :   ID '

def p_PTimestamIdP(t):
    'PTIMESTAMP  :   ID PUNTO ID '

def p_empty(t):
    'EMPTY :'

def p_error(t):
    global counter_syntactic_error
    err = open("reports/error_syntactic.txt", "a+")
    txt = '<tr><td>' + str(counter_syntactic_error) + '</td>'
    txt += '<td>' + str(t.value) + '</td>'
    txt += '<td>' + 'Texto ingresado no reconocido.' + '</td>'
    txt += '<td>' + str(t.lexer.lineno) + '</td>'
    txt += '<td>' + str(get_column(t.lexer.lexdata, t)) + '</td><tr>\n'
    err.write(txt)
    err.close()
    counter_syntactic_error += 1
    if not t:
        return
    while True:
        entry = parser.token()
        if not entry or entry.type == 'RBRACE':
            break
    parser.restart()


# START PARSING THE INPUT TEXT
parser = yacc.yacc()


def parse(p_input):
    global counter_lexical_error, counter_syntactic_error
    counter_lexical_error = 1
    counter_syntactic_error = 1
    return parser.parse(p_input)
