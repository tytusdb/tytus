# LISTA DE PALABRAS RESERVADAS
reservadas = {
    # Numeric Types
    'smallint': 'tSmallint',
    'integer': 'tInteger',
    'bigint': 'tBigint',
    'decimal': 'tDecimal',
    'numeric': 'tNumeric',
    'real': 'tReal',
    'double': 'tDouble',
    'precision': 'tPrecision',
    'money': 'tMoney',

    # Character types
    'character': 'tCharacter',
    'varying': 'tVarying',
    'varchar': 'tVarchar',
    'char': 'tChar',
    'text': 'tText',

    # Date/Time Types
    'timestamp': 'tTimestamp',
    'date': 'tDate',
    'time': 'tTime',
    'interval': 'tInterval',

    # Interval Type
    'year': 'tYear',
    'month': 'tMonth',
    'day': 'tDay',
    'hour': 'tHour',
    'minute': 'tMinute',
    'second': 'tSecond',
    'to': 'tTo',

    # Boolean Type
    'boolean': 'tBoolean',
    'false': 'tFalse',
    'true': 'tTrue',

    'create': 'create',
    'database': 'database',
    'or': 'or',
    'replace': 'replace',
    'if': 'if',

    'not': 'not',
    'exists': 'exists',
    'databases': 'databases',
    'drop': 'drop',
    'owner': 'owner',

    'mode': 'mode',
    'alter': 'alter',
    'show': 'show',
    'like': 'like',
    'insert': 'insert',

    'values': 'values',
    'null': 'null',
    'primarykey': 'primarykey',
    'into': 'into',
    'from': 'from',

    'where': 'where',
    'as': 'as',
    'select': 'select',
    'update': 'tUpdate',
    'set': 'tSet',

    'delete': 'tDelete',
    'truncate': 'tTruncate',
    'table': 'table',
    'tables': 'tables',
    'between': 'tBetween',

    'rename': 'rename',
    'isNull': 'isNull',
    'in': 'tIn',
    'iLike': 'tILike',
    'similar': 'tSimilar',

    'is': 'tIs',
    'notNull': 'notNull',
    'and': 'And',
    'current_user': 'currentuser',
    'session_user': 'sessionuser',
    'type': 'ttype',
    'enum': 'tenum',
    'yes': 'yes',
    'no': 'no',
    'on': 'on',
    'off': 'off',

    # >inicia fl
    'inherits': 'tInherits',
    'default': 'tDefault',
    'primary': 'tPrimary',
    'foreign': 'tForeign',
    'key': 'tKey',
    'references': 'tReferences',
    'check': 'tCheck',
    'constraint': 'tConstraint',
    'unique': 'tUnique',
    'column': 'tColumn',
    'add': 'add',

    # >termina fl
    'no': 'no',
    'yes': 'yes',
    'on': 'on',
    'off': 'off',

    # TOKENS QUERIES
    'distinct': 'distinct',
    'group': 'group',
    'by': 'by',
    'having': 'having',
    # agregacion
    'count': 'count',
    'avg': 'avg',
    'max': 'max',
    'min': 'min',
    'sum': 'sum',
    # matematicas
    'abs': 'abs',
    'cbrt': 'cbrt',
    'ceil': 'ceil',
    'ceiling': 'ceiling',
    'degrees': 'degrees',
    'div': 'div',
    'exp': 'exp',
    'factorial': 'factorial',
    'floor': 'floor',
    'gcd': 'gcd',
    'lcm': 'lcm',
    'ln': 'ln',
    'log': 'log',
    'log10': 'log10',
    'min_scale': 'min_scale',
    'mod': 'mod',
    'pi': 'pi',
    'power': 'power',
    'radians': 'radians',
    'round': 'round',
    'scale': 'scale',
    'sign': 'sign',
    'sqrt': 'sqrt',
    'trim_scale': 'trim_scale',
    'trunc': 'trunc',
    'width_bucket': 'width_bucket',
    'random': 'random',
    'setseed': 'setseed',
    # trigonometricas
    'acos': 'acos',
    'acosd': 'acosd',
    'asin': 'asin',
    'asind': 'asind',
    'atan': 'atan',
    'atand': 'atand',
    'atan2': 'atan2',
    'atan2d': 'atan2d',
    'cos': 'cos',
    'cosd': 'cosd',
    'cot': 'cot',
    'cotd': 'cotd',
    'sin': 'sin',
    'sind': 'sind',
    'tan': 'tan',
    'tand':'tand',
    'sinh': 'sinh',
    'cosh': 'cosh',
    'tanh': 'tanh',
    'asinh': 'asinh',
    'acosh': 'acosh',
    'atanh': 'atanh',
    # binary
    'length': 'length',
    'substring': 'substring',
    'trim': 'trim',
    'get_byte': 'get_byte',
    'md5': 'md5',
    'set_byte': 'set_byte',
    'sha256': 'sha256',
    'substr': 'substr',
    'convert': 'convert',
    'encode': 'encode',
    'decode': 'decode',

    # otros
    'all': 'all',
    'any': 'any',
    'some': 'some',

    # EXPRESSIONS
    'case': 'case',
    'when': 'when',
    'then': 'then',
    'else': 'else',
    'end': 'end',
    'greatest': 'greatest',
    'leaste': 'least',
    'limit': 'limit',
    'offset': 'offset',
    'union': 'union',
    'except': 'except',
    'intersect': 'intersect',

    # otros
    'date_part': 'date_part',
    'now': 'now',
    'current_date': 'current_date',
    'current_time': 'current_time',
    'extract': 'tExtract',
    'in': 'in'

    #nuevos -10
    ,'asc':'asc',
    'desc':'desc',
    'nulls':'nulls',
    'first':'first',
    'last':'last',
    'order':'order'

}

# LISTA DE TOKENS
tokens = [
             'punto',
             'dosPts',
             'corcheI',
             'corcheD',
             'mas',

             'menos',
             'elevado',
             'multi',
             'divi',
             'modulo',

             'igual',
             'menor',
             'mayor',
             'menorIgual',
             'mayorIgual',

             'diferente',
             'id',
             'decimal',
             'entero',
             'cadena',
             'cadenaLike',

             'parAbre',
             'parCierra',
             'coma',
             'ptComa',
             # tks
             'barra',
             'barraDoble',
             'amp',
             'numeral',
             'virgulilla',
             'mayormayor',
             'menormenor',

             #TOKENS PARA EL RECONOCIMIENTO DE FECHA Y HORA
             'fecha',
             'hora',
             'fecha_hora'

         ] + list(reservadas.values())

# DEFINICIÓN DE TOKENS
t_punto = r'\.'
t_dosPts = r':'
t_corcheI = r'\['
t_corcheD = r'\]'

t_mas = r'\+'
t_menos = r'-'
t_elevado = r'\^'
t_multi = r'\*'
t_divi = r'/'

t_modulo = r'%'
t_igual = r'='
t_menor = r'<'
t_mayor = r'>'
t_menorIgual = r'<='

t_mayorIgual = r'>='
t_diferente = r'<>'

t_parAbre = r'\('
t_parCierra = r'\)'
t_coma = r','
t_ptComa = r';'

# tk_queries
t_barra = r'\|'
t_barraDoble = r'\|\|'
t_amp = r'&'
t_numeral = r'\#'
t_virgulilla = r'~'
t_mayormayor = r'>>'
t_menormenor = r'<<'


# DEFINICIÓN DE UN NÚMERO DECIMAL
def t_decimal(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Floaat value too large %d", t.value)
        t.value = 0
    return t


# DEFINICIÓN DE UN NÚMERO ENTERO
def t_entero(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


#DEFINICIÓN PARA LA HORA
def t_hora(t):
    r'\'[0-2]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9]\''
    return t


#DEFINICIÓN PARA LA FECHA
def t_fecha(t):
    r'\'[0-9]{4}-[0-1]?[0-9]-[0-3]?[0-9]\''
    return t


#DEFINICIÓN PARA TIMESTAMP
def t_fecha_hora(t):
    r'\'([0-9]{4}-[0-1]?[0-9]-[0-3]?[0-9])(\s)([0-2]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])\''
    return t


# DEFINICIÓN DE UNA CADENA PARA LIKE
def t_cadenaLike(t):
    r'\'%.*?%\'|\"%.*?%\"'
    t.value = t.value[2:-2]
    return t


# DEFINICIÓN DE UNA CADENA
def t_cadena(t):
    r'\'.*?\'|\".*?\"'
    t.value = t.value[1:-1]
    return t


# DEFINICIÓN DE UN ID
def t_id(t):
    r'[a-zA-Z]([a-zA-Z]|[0-9]|_)*'
    t.type = reservadas.get(t.value.lower(), 'id')
    return t


# Comentario de múltiples líneas /* .. */
def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')


# DEFINICIÓN DE UN COMENTARIO SIMPLE
def t_COMENTARIO_SIMPLE(t):
    r'--.*'
    #t.lexer.lineno += 1  # Descartamos la linea desde aca


# IGNORAR COMENTARIOS SIMPLES
t_ignore_COMENTARIO_SIMPLE = r'\#.*'

# Caracteres ignorados
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    t.lexer.skip(1)

    print("Caracter inválido '%s'" % t.value[0], " Línea: '%s'" % str(t.lineno))


def find_column(token):  # Columna relativa a la fila
    global con
    line_start = con.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


# Construyendo el analizador léxico
import ply.lex as lex
import re

lexer = lex.lex()
lex.lex(reflags=re.IGNORECASE)

# DEFINIENDO LA PRECEDENCIA DE LOS OPERADORES
# ---------Modificado Edi------
precedence = (
    ('right', 'not'),
    ('left', 'And'),
    ('left', 'or'),
    ('left', 'diferente', 'igual', 'mayor', 'menor', 'menorIgual', 'mayorIgual'),
    ('left', 'punto'),
    ('right', 'umenos'),
    ('left', 'mas', 'menos'),
    ('left', 'elevado'),
    ('left', 'multi', 'divi', 'modulo'),
    ('nonassoc', 'parAbre', 'parCierra')
)
# ---------Modificado Edi---------
# <<<<<<<<<<<<<<<<<<<<<<<<<<< INICIO DE LAS PRODUCCIONES <<<<<<<<<<<<<<<<<<<<<<<<<<<<
from sentencias import *


def p_init(t):
    'inicio :   sentencias'
    print("Lectura Finalizada")
    t[0] = t[1]

def p_sentencias_lista(t):
    'sentencias : sentencias sentencia'
    t[1].append(t[2])
    t[0]=t[1] 
     
def p_sentencias_sentencia(t):
    'sentencias : sentencia'
    t[0] = [t[1]] 
def p_sentencia(t):
    '''sentencia : CrearBase
                 | ShowBase
                 | AlterBase
                 | DropBase
                 | EnumType
                 | UpdateBase
                 | DeleteBase
                 | TruncateBase
                 | CREATE_TABLE
                 | SHOW_TABLES
                 | ALTER_TABLE
                 | DROP_TABLE
                 | INSERT
                 | QUERY ptComa
    '''
    t[0] = t[1]


# <<<<<<<<<<<<<<<<<<<<<<<<<<< HEIDY <<<<<<<<<<<<<<<<<<<<<<<<<<<<
def p_crearBase(t):
    '''CrearBase : create database id ptComa
                 | create database id owner igual id ptComa
                 | create database id mode igual entero ptComa
                 | create database id owner igual id mode igual entero ptComa
                 | create or replace database id ptComa
                 | create or replace database id owner igual id ptComa
                 | create or replace database id mode igual entero ptComa
                 | create or replace database id owner igual id mode igual entero ptComa
                 | create database if not exists id ptComa
                 | create database if not exists id owner igual id ptComa
                 | create database if not exists id mode igual entero ptComa
                 | create database if not exists id owner igual id mode igual entero ptComa'''
    # def __init__(self, owner, mode, replace, exists, id)
    if len(t) == 5:
        # primera produccion
        t[0] = SCrearBase(False, False, False, False, t[3])
        # agregar codigo de grafica
    elif len(t) == 8:
        if t[4].lower() == "mode":
            # tercera produccion
            t[0] = SCrearBase(False, t[6], False, False, t[3])
        elif t[4].lower() == "owner":
            print("entre aqui")
            # segunda produccion
            t[0] = SCrearBase(t[6], False, False, False, t[3])
        if t[3].lower() == "if":
            # novena produccion
            t[0] = SCrearBase(False, False, False, True, t[6])
    elif len(t) == 11:
        if t[3].lower() == "if":
            if t[7].lower() == "owner":
                # decima produccion
                t[0] = SCrearBase(t[9], False, False, True, t[6])
            elif t[7].lower() == "mode":
                # onceava produccion
                t[0] = SCrearBase(False, t[9], False, True, t[6])
        else:
            # cuarta produccion
            t[0] = SCrearBase(t[6], t[9], False, False, t[3])
    elif len(t) == 7:
        # quinta produccion
        t[0] = SCrearBase(False, False, True, False, t[5])
    elif len(t) == 10:
        if t[6].lower() == "mode":
            # septima produccion
            t[0] = SCrearBase(False, t[8], True, False, t[5])
        else:
            # sexta produccion
            t[0] = SCrearBase(t[8], False, True, False, t[5])
    elif len(t) == 13:
        # octava produccion
        t[0] = SCrearBase(t[8], t[11], True, False, t[5])
    elif len(t) == 14:
        # doceava produccion
        t[0] = SCrearBase(t[9], t[12], False, True, t[6])


def p_showBase(t):
    '''ShowBase : show databases ptComa
                | show databases like cadenaLike ptComa'''
    # def __init__(self,like,cadena):
    if len(t) == 4:
        t[0] = SShowBase(False, None)

    else:
        t[0] = SShowBase(True, t[4])


def p_AlterBase(t):
    '''AlterBase : alter database id rename tTo id ptComa
                 | alter database id owner tTo id ptComa
                 | alter database id owner tTo currentuser ptComa
                 | alter database id owner tTo sessionuser ptComa
    '''
    # def __init__(self, id, rename, owner, id):
    if t[4].lower() == "rename":
        t[0] = SAlterBase(t[3], True, False, t[6])
    else:
        t[0] = SAlterBase(t[3], False, True, t[6])


def p_DropBase(t):
    '''DropBase : drop database id ptComa
                | drop database if exists id ptComa'''
    if len(t) == 5:
        t[0] = SDropBase(False, t[3])
    else:
        t[0] = SDropBase(True, t[5])


def p_EnumType(t):
    'EnumType   : create ttype id as tenum parAbre LISTA_EXP parCierra ptComa'
    t[0] = STypeEnum(t[3], t[7])


# <<<<<<<<<<<<<<<<<<<<<<<<<<< HEIDY <<<<<<<<<<<<<<<<<<<<<<<<<<<<

# <<<<<<<<<<<<<<<<<<<<<<<<<<< ARIEL <<<<<<<<<<<<<<<<<<<<<<<<<<<<

# PRODUCCIÓN PARA HACER UN UPDATE
def p_produccion0(t):
    ''' UpdateBase   : tUpdate id tSet L_ASIGN where E ptComa '''
    t[0] = SUpdateBase(t[2], t[4], t[6])


# PRODUCCIÓN PARA HACER UN DELETE
def p_produccion0_1(t):
    ''' DeleteBase  : tDelete from id CONDICION ptComa '''
    t[0] = SDeleteBase(t[3], t[4])


# CONDICIÓN QUE PUEDE O NO VENIR DENTRO DE UN DELETE
def p_produccion0_2(t):
    ''' CONDICION   : where E
                    |  '''
    if len(t) == 3:
        t[0] = t[2]
    else:
        t[0] = False


# PRODUCCIÓN PARA HACER UN TRUNCATE
def p_produccion1_0(t):
    ''' TruncateBase    : tTruncate L_IDs ptComa'''
    t[0] = STruncateBase(t[2])


# PRODUCCIÓN PARA UNA LISTA DE IDENTIFICADORES
def p_produccion1_1(t):
    ''' L_IDs   : L_IDs coma id 
                | id '''
    if len(t) == 4:
        t[1].append(t[3])
        t[0] = t[1]
    else:
        t[0] = [t[1]]


# PRODUCCIÓN PARA UNA LISTA DE ASIGNACIONES: id1 = 2, id2 = 3, id3, = 'Hola', etc...
def p_produccion1(t):
    ''' L_ASIGN : L_ASIGN coma id igual E
                | id igual E '''
    if len(t) == 6:
        val = SValSet(t[3], t[5])
        t[1].append(val)
        t[0] = t[1]
    else:
        val = SValSet(t[1], t[3])
        t[0] = [val]


# <<<<<<<<<<<<<<<<<<<<<<<<<<< ARIEL <<<<<<<<<<<<<<<<<<<<<<<<<<<<

# <<<<<<<<<<<<<<<<<<<<<<<<<<< FRANCISCO <<<<<<<<<<<<<<<<<<<<<<<<<<<<

def p_EXPR_CREATE_TABLE(t):
    '''CREATE_TABLE : create table id parAbre COLUMNS parCierra ptComa
                    | create table id parAbre COLUMNS parCierra tInherits parAbre id parCierra ptComa '''
    if len(t) == 8:
        t[0] = SCrearTabla(t[3], False, None, t[5])
    else:
        t[0] = SCrearTabla(t[3], True, t[9], t[5])


def p_EXPR_COLUMNS(t):
    '''COLUMNS : COLUMNS coma ASSIGNS
               | ASSIGNS
    '''
    if len(t) == 4:
        t[1].append(t[3])
        t[0] = t[1]
    elif len(t) == 2:
        t[0] = [t[1]]


def p_EXPR_ASSIGNS(t):
    '''ASSIGNS : id TIPO
               | id TIPO OPCIONALES
               | tCheck E
               | tConstraint id tCheck E
               | tUnique parAbre COLS parCierra
               | tPrimary tKey parAbre COLS parCierra
               | tForeign tKey parAbre COLS parCierra tReferences id parAbre COLS parCierra'''
    if len(t) == 3:
        if t[1].lower == "check":
            t[0] = SColumnaCheck(None, t[2])
        else:
            t[0] = SColumna(t[1], t[2], None)
    elif len(t) == 4:
        t[0] = SColumna(t[1], t[2], t[3])
    elif len(t)==5:
        if t[1].lower()=="constraint":
            t[0]=SColumnaCheck(t[2],t[4])
        else:
            t[0]=SColumnaUnique(t[3])
    elif len(t)==6:
        t[0]=SColumnaPk(t[4])
    elif len(t)==11:
        t[0]=SColumnaFk(t[7],t[4],t[9])


def p_EXPR_OPCIONALES(t):
    '''OPCIONALES : OPCIONALES OPCION
                | OPCION '''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]


def p_EXPR_OPCION(t):
    '''OPCION : tDefault E'''
    t[0] = SOpcionales(TipoOpcionales.DEFAULT, t[2],None)


def p_EXPR_OPCION1(t):
    '''OPCION : tPrimary tKey'''
    t[0] = SOpcionales(TipoOpcionales.PRIMARYKEY, None,None)


def p_EXPR_OPCION2(t):
    '''OPCION : not null'''
    t[0] = SOpcionales(TipoOpcionales.NOTNULL, None,None)


def p_EXPR_OPCION3(t):
    '''OPCION : null'''
    t[0] = SOpcionales(TipoOpcionales.NULL, None,None)


def p_EXPR_OPCION4(t):
    '''OPCION : tUnique'''
    t[0] = SOpcionales(TipoOpcionales.UNIQUE, None,None)


def p_EXPR_OPCION5(t):
    '''OPCION : tCheck E'''
    t[0] = SOpcionales(TipoOpcionales.CHECK, t[2],None)


def p_EXPR_OPCION6(t):
    ''' OPCION : tConstraint id tUnique '''
    t[0] = SOpcionales(TipoOpcionales.UNIQUE, None, t[2])


def p_EXPR_OPCION7(t):
    '''OPCION : tConstraint id tCheck E'''
    t[0] = SOpcionales(TipoOpcionales.CHECK, t[4], t[2])


def p_EXPR_COLS(t):
    '''COLS : COLS coma E
            | E '''

    if len(t)==4:
        t[1].append(t[3])
        t[0]=t[1]
    else:
        t[0]=[t[1]]


def p_EXPR_TIPO(t):
    '''TIPO : NUMERIC_TYPES
            | CHAR_TYPES
            | DATE_TYPES
            | BOOL_TYPES
            | E'''
    t[0] = t[1]


def p_EXPR_NUMERIC_TYPES(t):
    '''NUMERIC_TYPES : tSmallint
                     | tInteger
                     | tBigint
                     | tDecimal
                     | tNumeric
                     | tReal
                     | tDouble tPrecision
                     | tMoney'''
    t[0] = STipoDato(t[1], TipoDato.NUMERICO, None)


def p_EXPR_CHAR_TYPES(t):
    '''CHAR_TYPES : tVarchar parAbre entero parCierra
                  | tCharacter tVarying parAbre entero parCierra
                  | tCharacter parAbre entero parCierra
                  | tChar parAbre entero parCierra
                  | tText'''
    if len(t) == 2:
        t[0] = STipoDato(t[1], TipoDato.CHAR, None)
    elif len(t) == 5:
        t[0] = STipoDato(t[1], TipoDato.CHAR, t[3])
    else:
        t[0] = STipoDato(t[2], TipoDato.CHAR, t[4])


def p_EXPR_DATE_TYPES(t):
    '''DATE_TYPES : tDate
                  | tTimestamp 
                  | tTime 
                  | tInterval
                  | tInterval FIELDS'''
    t[0] = STipoDato(t[1], TipoDato.FECHA, None)

def p_EXPR_BOOL_TYPES(t):
    '''BOOL_TYPES : tBoolean'''
    t[0]=STipoDato(t[1],TipoDato.BOOLEAN,None)

def p_EXPR_FIELDS(t):
    '''FIELDS : tYear
              | tMonth
              | tDay
              | tHour
              | tMinute
              | tSecond'''
    t[0] = STipoDato(t[1], TipoDato.FIELDS, None)


def p_EXPR_SHOW_TABLE(t):
    '''SHOW_TABLES : show tables ptComa'''
    t[0] = SShowTable()


def p_EXPR_DROP_TABLE(t):
    '''DROP_TABLE : drop table id ptComa
    '''
    t[0] = SDropTable(t[3])


def p_EXPR_ALTER_TABLE(t):
    '''ALTER_TABLE : alter table id rename tColumn id tTo id ptComa
                   | alter table id EXPR_ALTER
                   | alter table id add tColumn id CHAR_TYPES ptComa
                   | alter table id add tCheck E ptComa
                   | alter table id add tConstraint id tUnique parAbre id parCierra ptComa      
                   | alter table id add tForeign tKey parAbre id parCierra tReferences id ptComa    
                   | alter table id drop tColumn id ptComa
                   | alter table id drop tConstraint id ptComa 
                   '''
    if len(t) == 10:
        # primera produccion
        t[0] = SAlterTableRename(t[3], t[6], t[8])
    elif len(t) == 8:
        if t[4].lower() == "add":
            # cuarta produccion
            t[0] = SAlterTableCheck(t[3], t[6])
        elif t[4].lower() == "drop":
            if t[5].lower() == "column":
                t[0] = SAlterTableDrop(t[3], False, TipoAlterDrop.COLUMN)
            else:
                t[0] = SAlterTableDrop(t[3], t[6], TipoAlterDrop.CONSTRAINT)

    elif len(t) == 5:
        # segunda produccion
        t[0] = SAlterTable_AlterColumn(t[3], t[4])
    elif len(t) == 9:
        # tercera produccion
        t[0] = SAlterTableAddColumn(t[3], t[6], t[7])
    elif len(t) == 12:
        # quinta produccion
        t[0] = SAlterTableAddUnique(t[3], t[6], t[9]);
    elif len(t) == 13:
        # sexta produccion
        t[0] = SAlterTableAddFK(t[3], t[8], t[11])


def p_EXPR_ALTER(t):
    '''EXPR_ALTER : EXPR_ALTER coma alter tColumn id tSet not null ptComa
                  | EXPR_ALTER coma alter tColumn id ttype CHAR_TYPES ptComa
                  | alter tColumn id ttype CHAR_TYPES ptComa
                  | alter tColumn id tSet not null ptComa
                   '''
    if len(t) == 8:
        t[0] = [SAlterColumn(t[3], TipoAlterColumn.NOTNULL, None)]
    elif len(t) == 7:
        t[0] = [SAlterColumn(t[3], TipoAlterColumn.CAMBIOTIPO, t[5])]
    elif len(t) == 10:
        val = SAlterColumn(t[5], TipoAlterColumn.NOTNULL, None)
        t[1].append(val)
        t[0] = t[1]
    elif len(t) == 9:
        val = SAlterColumn(t[5], TipoAlterColumn.CAMBIOTIPO, t[7])
        t[1].append(val)
        t[0] = t[1]


# <<<<<<<<<<<<<<<<<<<<<<<<<<< FRANCISCO <<<<<<<<<<<<<<<<<<<<<<<<<<<<

# <<<<<<<<<<<<<<<<<<<<<<<<<<< EDI <<<<<<<<<<<<<<<<<<<<<<<<<<<<
def p_INSERT(p):
    ''' INSERT :  insert into id values parAbre LISTA_EXP parCierra ptComa   '''
    p[0] = SInsertBase(p[3], p[6])


def p_LISTA_EXP(p):
    ''' LISTA_EXP :    LISTA_EXP coma E    
                    |  E 
    '''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]


def p_E(p):
    ''' E : E or E
          |  E And       E
          |  E diferente  E
          |  E igual      E
          |  E mayor      E
          |  E menor      E
          |  E mayorIgual E
          |  E menorIgual E
          |  E mas        E
          |  E menos      E
          |  E multi      E
          |  E divi       E
          |  E modulo     E
          |  E elevado    E
          |  E punto      E
    '''
    if p[2].lower() == "or":
        p[0] = SOperacion(p[1], p[3], Logicas.OR)
    elif p[2].lower() == "and":
        p[0] = SOperacion(p[1], p[3], Logicas.AND)
    elif p[2] == "<>":
        p[0] = SOperacion(p[1], p[3], Relacionales.DIFERENTE)
    elif p[2] == "=":
        p[0] = SOperacion(p[1], p[3], Relacionales.IGUAL)
    elif p[2] == ">":
        p[0] = SOperacion(p[1], p[3], Relacionales.MAYOR_QUE)
    elif p[2] == "<":
        p[0] = SOperacion(p[1], p[3], Relacionales.MENOR_QUE)
    elif p[2] == ">=":
        p[0] = SOperacion(p[1], p[3], Relacionales.MAYORIGUAL_QUE)
    elif p[2] == "<=":
        p[0] = SOperacion(p[1], p[3], Relacionales.MENORIGUAL_QUE)
    elif p[2] == "+":
        p[0] = SOperacion(p[1], p[3], Aritmetica.MAS)
    elif p[2] == "-":
        p[0] = SOperacion(p[1], p[3], Aritmetica.MENOS)
    elif p[2] == "*":
        p[0] = SOperacion(p[1], p[3], Aritmetica.POR)
    elif p[2] == "/":
        p[0] = SOperacion(p[1], p[3], Aritmetica.DIVIDIDO)
    elif p[2] == "%":
        p[0] = SOperacion(p[1], p[3], Aritmetica.MODULO)
    elif p[2] == "**":
        p[0] = SOperacion(p[1], p[3], Aritmetica.POTENCIA)
    elif p[2] == ".":
        p[0] = SOperacion(p[1], p[3], Expresion.TABATT)


def p_OpNot(p):
    ''' E : not E '''
    p[0] = SExpresion(p[2], Logicas.NOT)


def p_OpNegativo(p):
    ''' E : menos E %prec umenos '''
    p[0] = SExpresion(p[2], Expresion.NEGATIVO)


def p_OpParentesis(p):
    ''' E : parAbre E parCierra  '''
    p[0] = p[2]


def p_entero(p):
    ''' E : entero    
    '''
    p[0] = SExpresion(p[1], Expresion.ENTERO)


def p_decimal(p):
    ''' E : decimal    
    '''
    p[0] = SExpresion(p[1], Expresion.DECIMAL)


def p_cadena(p):
    ''' E : cadena    
    '''
    p[0] = SExpresion(p[1], Expresion.CADENA)


def p_id(p):
    ''' E : id    
    '''
    p[0] = SExpresion(p[1], Expresion.ID)


def p_fecha(p):
    ''' E : fecha    
    '''
    p[0] = SExpresion(p[1], Expresion.ID)


def p_hora(p):
    ''' E : hora    
    '''
    p[0] = SExpresion(p[1], Expresion.ID)


def p_fecha_hora(p):
    ''' E : fecha_hora    
    '''
    p[0] = SExpresion(p[1], Expresion.ID)


def p_booleano(p):
    '''E  : yes
          | no
          | on
          | off
          | tTrue
          | tFalse
    '''
    p[0] = SExpresion(p[1], Expresion.BOOLEAN)


# <<<<<<<<<<<<<<<<<<<<<<<<<<< EDI <<<<<<<<<<<<<<<<<<<<<<<<<<<<

######################################### QUERIES 

def p_QUERY(p):
    '''QUERY : EXPR_SELECT 
             | EXPR_SELECT EXPR_FROM 
             | EXPR_SELECT EXPR_FROM EXPR_WHERE EXPR_GROUPBY EXPR_HAVING EXPR_ORDERBY EXPR_LIMIT 
    '''
    #LEN 2 Y 3 y 7    #select, ffrom, where, groupby, having, orderby, limit
    if len(p) == 2:
        p[0] = SQuery(p[1],False,False,False,False,False,False)
    elif len(p) == 3:
        p[0] = SQuery(p[1],p[2],False,False,False,False,False)
    else: 
        p[0] = SQuery(p[1],p[2],p[3],p[4],p[5],p[6],p[7])

    #LEN 4     #select, ffrom, where, groupby, having, orderby, limit
def p_QUERY_p4_1(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_ORDERBY''' 
    p[0] = SQuery(p[1],p[2],False,False,False,p[3],False)

def p_QUERY_p4_2(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_LIMIT''' 
    p[0] = SQuery(p[1],p[2],False,False,False,False,p[3])

def p_QUERY_p4_3(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_WHERE''' 
    p[0] = SQuery(p[1],p[2],p[3],False,False,False,False)

def p_QUERY_p4_4(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_HAVING''' 
    p[0] = SQuery(p[1],p[2],False,False,p[3],False,False)

def p_QUERY_p4_5(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_GROUPBY''' 
    p[0] = SQuery(p[1],p[2],False,p[3],False,False,False)

    #LEN 5     #select, ffrom, where, groupby, having, orderby, limit
def p_QUERY_p5_1(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_ORDERBY EXPR_LIMIT''' 
    p[0] = SQuery(p[1],p[2],False,False,False,p[3],p[4])

def p_QUERY_p5_2(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_WHERE EXPR_ORDERBY ''' 
    p[0] = SQuery(p[1],p[2],p[3],False,False,p[4],False)

def p_QUERY_p5_3(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_WHERE EXPR_LIMIT''' 
    p[0] = SQuery(p[1],p[2],p[3],False,False,False,p[4])

def p_QUERY_p5_4(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_WHERE EXPR_GROUPBY''' 
    p[0] = SQuery(p[1],p[2],p[3],p[4],False,False,False)

def p_QUERY_p5_5(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_GROUPBY EXPR_LIMIT''' 
    p[0] = SQuery(p[1],p[2],False,p[3],False,False,p[4])

def p_QUERY_p5_6(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_GROUPBY EXPR_ORDERBY ''' 
    p[0] = SQuery(p[1],p[2],False,p[3],False,p[4],False)

def p_QUERY_p5_7(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_GROUPBY EXPR_HAVING''' 
    p[0] = SQuery(p[1],p[2],False,p[3],p[4],False,False)

def p_QUERY_p5_8(p):
    '''QUERY :  EXPR_SELECT EXPR_FROM EXPR_HAVING EXPR_LIMIT''' 
    p[0] = SQuery(p[1],p[2],False,False,p[3],False,p[4])

def p_QUERY_p5_9(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_HAVING EXPR_ORDERBY''' 
    p[0] = SQuery(p[1],p[2],False,False,p[3],p[4],False)

def p_QUERY_p5_10(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_WHERE EXPR_HAVING''' 
    p[0] = SQuery(p[1],p[2],p[3],False,p[4],False,False)


 #LEN 6     #select, ffrom, where, groupby, having, orderby, limit
def p_QUERY_p6_1(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_WHERE EXPR_ORDERBY EXPR_LIMIT '''
    p[0] = SQuery(p[1],p[2],p[3],False,False,p[4],p[5])

def p_QUERY_p6_2(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_WHERE EXPR_GROUPBY EXPR_ORDERBY '''
    p[0] = SQuery(p[1],p[2],p[3],p[4],False,p[5],False)

def p_QUERY_p6_3(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_WHERE EXPR_GROUPBY EXPR_LIMIT '''
    p[0] = SQuery(p[1],p[2],p[3],p[4],False,False,p[5])

def p_QUERY_p6_4(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_WHERE EXPR_GROUPBY EXPR_HAVING '''
    p[0] = SQuery(p[1],p[2],p[3],p[4],p[5],False,False)

def p_QUERY_p6_5(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_GROUPBY EXPR_ORDERBY EXPR_LIMIT '''
    p[0] = SQuery(p[1],p[2],False,p[3],False,p[4],p[5])

def p_QUERY_p6_6(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_GROUPBY EXPR_HAVING EXPR_LIMIT '''
    p[0] = SQuery(p[1],p[2],False,p[3],p[4],False,p[5])

def p_QUERY_p6_7(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_GROUPBY EXPR_HAVING EXPR_ORDERBY '''
    p[0] = SQuery(p[1],p[2],False,p[3],p[4],p[5],False)

def p_QUERY_p6_8(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_HAVING EXPR_ORDERBY EXPR_LIMIT'''
    p[0] = SQuery(p[1],p[2],False,False,p[5],p[4],p[5])

def p_QUERY_p6_9(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_WHERE EXPR_HAVING EXPR_LIMIT'''
    p[0] = SQuery(p[1],p[2],p[3],False,p[4],False,p[5])

def p_QUERY_p6_10(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_WHERE EXPR_HAVING EXPR_ORDERBY'''
    p[0] = SQuery(p[1],p[2],p[3],False,p[4],p[5],False)

 #LEN 7     #select, ffrom, where, groupby, having, orderby, limit
def p_QUERY_p7_1(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_WHERE EXPR_GROUPBY EXPR_ORDERBY EXPR_LIMIT'''
    p[0] = SQuery(p[1],p[2],p[3],p[4],False,p[5],p[6])

def p_QUERY_p7_2(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_WHERE EXPR_GROUPBY EXPR_HAVING EXPR_LIMIT'''
    p[0] = SQuery(p[1],p[2],p[3],p[4],p[5],False,p[6])

def p_QUERY_p7_3(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_WHERE EXPR_GROUPBY EXPR_HAVING EXPR_ORDERBY'''
    p[0] = SQuery(p[1],p[2],p[3],p[4],p[5],p[6],False)

def p_QUERY_p7_4(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_GROUPBY EXPR_HAVING EXPR_ORDERBY EXPR_LIMIT'''
    p[0] = SQuery(p[1],p[2],False,p[3],p[4],p[5],p[6])

def p_QUERY_p7_5(p):
    '''QUERY : EXPR_SELECT EXPR_FROM EXPR_WHERE EXPR_HAVING EXPR_ORDERBY EXPR_LIMIT'''
    p[0] = SQuery(p[1],p[2],p[3],False,p[4],p[5],p[6])


def p_EXPR_SELECT(p):
    '''EXPR_SELECT : select distinct EXPR_COLUMNAS
                   | select multi
                   | select now parAbre parCierra
                   | select current_time
                   | select current_date
                   ''' 
    if len(p) == 3:
        print("P2 es " + p[2])
        if p[2] == "*":
            p[0] = SSelectCols(False,p[2])
        elif p[2].lower() == "current_time" :
            p[0] = SSelectFunc(p[2])
        elif p[2].lower() == "current_date" :
            p[0] = SSelectFunc(p[2])
    elif p[2].lower() == "now":
            p[0] = SSelectFunc(p[2])
    else:
        p[0] = SSelectCols(True,p[3])


def p_EXPR_SELECT_C(p):
    '''EXPR_SELECT : select EXPR_COLUMNAS''' 
    p[0] = SSelectCols(False,p[2])

    
# todos los parametros de select - columnas
def p_EXPR_COLUMNAS(p):
    '''EXPR_COLUMNAS : EXPR_COLUMNAS coma EXPR_COLUMNAS1
                     | EXPR_COLUMNAS1'''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]
    

#LEN 1 y 3
def p_EXPR_COLUMNAS1(p):
    '''EXPR_COLUMNAS1 : E
                     | EXPR_AGREGACION
                     | EXPR_MATHS
                     | EXPR_TRIG
                     | EXPR_BINARIAS
                     | EXPR_EXTRA
                     | EXPR_FECHA
                     | EXPR_CASE
                     | E as E
                     | EXPR_AGREGACION as E
                     | EXPR_MATHS as E
                     | EXPR_TRIG as E 
                     | EXPR_BINARIAS as E
                     | EXPR_EXTRA as E
                     | EXPR_FECHA as E
                     | EXPR_CASE as E '''
    if len(p) == 4:
        p[0] = SColumnasAsSelect(p[3],p[1])
    else:
        p[0] = SColumnasSelect(p[1])

#LEN 
def p_EXPR_COLUMNAS1_p1(p):
    '''EXPR_COLUMNAS1 : substring parAbre E coma E coma E parCierra
                     | greatest parAbre E_LIST parCierra
                     | least parAbre E_LIST parCierra
                     | substring parAbre E coma E coma E parCierra as E
                     | greatest parAbre E_LIST parCierra as E
                     | least parAbre E_LIST parCierra as E '''
    if p[1].lower() == "substring":
        if p[9].lower() == "as":
            p[0] = SColumnasSubstr(p[3],p[5],p[7],p[10])
        else:
            p[0] = SColumnasSubstr(p[3],p[5],p[7],False)
    elif p[1].lower() == "greatest":
        if len(p) == 7:
            p[0] = SColumnasGreatest(p[6],p[3])
        else:
            p[0] = SColumnasGreatest(False,p[3])
    elif p[1].lower() == "least":
        if len(p) == 7:
            p[0] = SColumnasLeast(p[6],p[3])
        else:
            p[0] = SColumnasLeast(False,p[3])

def p_EXPR_EXTRA(p):
    '''EXPR_EXTRA : tExtract parAbre FIELDS from tTimestamp E parCierra'''
    p[0] = SExtract(p[3],p[6])

def p_EXPR_AGREGACION(p):
    '''EXPR_AGREGACION : count E
                       | avg E
                       | max E
                       | min E
                       | sum E
                       | count parAbre multi parCierra  
                       | avg parAbre multi parCierra
                       | max parAbre multi parCierra
                       | min parAbre multi parCierra
                       | sum parAbre multi parCierra'''

    if len(p) == 3:
        p[0] = SFuncAgregacion(p[1],p[2])
    else:
        p[0] = SFuncAgregacion(p[1],p[3])



def p_EXPR_MATHS(p):
    '''EXPR_MATHS : abs E
                     | cbrt E
                     | ceil E
                     | ceiling E
                     | degrees E
                     | div parAbre E coma E parCierra
                     | exp E
                     | factorial E
                     | floor E
                     | gcd parAbre E coma E parCierra
                     | lcm E
                     | ln E
                     | log E
                     | log10 E
                     | min_scale E
                     | mod parAbre E coma E parCierra
                     | pi parAbre parCierra
                     | power parAbre E coma E parCierra
                     | radians E
                     | round E
                     | scale E
                     | sign E
                     | sqrt E
                     | trim_scale E
                     | trunc E
                     | width_bucket parAbre LISTA_EXP parCierra
                     | random parAbre parCierra
                     | setseed E  '''
    if len(p) == 3:
        p[0] = SFuncMath(p[1],p[2])
    elif len(p) == 4:
        p[0] = SFuncMathSimple(p[1])
    elif len(p) == 7:
        p[0] = SFuncMath2(p[1],p[3],p[5])
    elif len(p) == 5:
        p[0] = SFuncMathLista(p[1],p[3])
        

def p_EXPR_TRIG(p):
    '''EXPR_TRIG :  acos E 
                | acosd E 
                | asin E 
                | asind E 
                | atan E 
                | atand E 
                | atan2 parAbre E coma E parCierra
                | atan2d parAbre E coma E parCierra
                | cos E 
                | cosd E 
                | cot E 
                | cotd E 
                | sin E 
                | sind E 
                | tan E 
                | sinh E 
                | cosh E 
                | tanh E 
                | tand E 
                | asinh E 
                | acosh E 
                | atanh E'''
    if len(p) == 3:
        p[0] = SFuncTrig(p[1],p[2])
    elif len(p) == 7:
        p[0] = SFuncTrig2(p[1],p[3],p[5])


def p_EXPR_BINARIAS(p):
    '''EXPR_BINARIAS : length E
                     | trim E
                     | get_byte E
                     | md5 E
                     | set_byte E
                     | sha256 E
                     | substr E
                     | convert E
                     | encode E
                     | decode E'''
    p[0] = SFuncBinary(p[1],p[2])


def p_EXPR_FECHA(p):
    '''EXPR_FECHA : date_part parAbre E coma DATE_TYPES E parCierra
                  | current_date
                  | current_time
                  | now parAbre parCierra
                  | DATE_TYPES E'''
    if len(p) == 2:
        p[0] = SSelectFunc(p[2])
    elif len(p) == 4:
        p[0] = SSelectFunc(p[2])
    elif len(p) == 3:
        p[0] = SFechaFunc(p[1],p[2])
    else: 
        p[0] = SFechaFunc2(p[1],p[3],p[5],p[6])


def p_EXPR_CASE(p):
    '''EXPR_CASE : case CASE_LIST end
                 | case CASE_LIST else E end'''
    if len(p) == 2:
        p[0] = SCase(p[2])
    else:
        p[0] = SCaseElse(p[2],p[4])


def p_CASE_LIST(p):
    '''CASE_LIST : CASE_LIST when E then E
                | when E then E''' 
    if len(p) == 6:
        p[0] = SCaseList(p[3],p[5],p[1])
    else:
        p[0] = SCaseList(p[2],p[4],False)


def p_E_LIST(p):
    '''E_LIST : E_LIST coma E_LIST1
              | E_LIST1
              '''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_E_LIST1(p):
    '''E_LIST1 : E
               | now parAbre parCierra'''
    if len(p) == 4:
        p[0] = SSelectFunc(p[1])
    else:
        p[0] = [p[1]]

def p_EXPR_FROM(p):
    '''EXPR_FROM : from L_IDsAlias 
                 | from parAbre QUERY parCierra 
                 | from parAbre QUERY parCierra id
                 | from parAbre QUERY parCierra as id'''
    if len(p) == 3:
        p[0] = SFrom(p[2])
    elif len(p) == 4:
        p[0] = SFrom2(False,p[3])
    elif len(p) == 5:
        p[0] = SFrom2(p[5],p[3])
    elif len(p) == 6:
        p[0] = SFrom2(p[6],p[3])

def p_L_IDsAlias(p):
    '''L_IDsAlias : L_IDsAlias coma L_IDsAlias1
                  | L_IDsAlias1 '''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_L_IDsAlias_p1(p):
    '''L_IDsAlias1 : id id 
                    | id as id 
                    | id'''

def p_EXPR_WHERE(p):
    '''EXPR_WHERE : where LIST_CONDS '''


def p_LIST_CONDS(p):
    '''LIST_CONDS : LIST_CONDS COND1
                  | COND1  '''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_COND1(p):
    '''COND1 :  E 
                | E tIs distinct from E
                | E tIs not distinct from E
                | substring parAbre E coma E coma E parCierra igual E
                | E exists parAbre QUERY parCierra
                | E in parAbre QUERY parCierra 
                | E not in parAbre QUERY parCierra
                | E OPERATOR any parAbre QUERY parCierra
                | E OPERATOR some parAbre QUERY parCierra
                | E OPERATOR all parAbre QUERY parCierra'''

def p_OPERATOR(p):
    '''OPERATOR : igual
                | menor
                | mayor
                | menorIgual
                | mayorIgual
                | diferente'''


def p_EXPR_GROUPBY( p ):
    '''EXPR_GROUPBY : group by LISTA_EXP'''


def p_EXPR_HAVING(p):
    '''EXPR_HAVING : having E_FUNC OPERATOR E_FUNC'''

def p_EXPR_E_FUNC( p ):
    '''E_FUNC : EXPR_AGREGACION
              | EXPR_MATHS
              | EXPR_TRIG
              | EXPR_BINARIAS
              | EXPR_FECHA
              | E '''

def p_EXPR_ORDERBY( p ):
    '''EXPR_ORDERBY : order by LIST_ORDERBY'''

def p_LIST_ORDERBY(p):
    '''LIST_ORDERBY : LIST_ORDERBY coma LIST_ORDERBY_1
                    | LIST_ORDERBY_1'''

def p_LIST_ORDERBY_p1(p):
    '''LIST_ORDERBY_1 : E asc
                    | E asc nulls first
                    | E asc nulls last
                    | E desc 
                    | E desc nulls first
                    | E desc nulls last
                    | E 
                    | E nulls first
                    | E nulls last'''


def p_EXPR_LIMIT(p):
    '''EXPR_LIMIT : limit E
                  | limit all
                  | limit all offset E
                  | limit E offset E'''



# <<<<<<<<<<<<<<<<<<<<<<<<<<<<< FIN DE LAS PRODUCCIONES <<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def p_error(t):
    col = find_column(t)
    print("Error sintáctico en '%s'" % t.value, " Línea: '%s'" % str(t.lineno), " Columna: '%s'" % str(col) )


import ply.yacc as yacc

parser = yacc.yacc()


def parse(input):
    global con
    con = input
    return parser.parse(input)
