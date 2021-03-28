import libs.ply.lex as lex
from libs.ply.lex import TOKEN

from controllers.error_controller import ErrorController

# Hacen falta palabras reservadas hay que anadirlas
# Definitions of tokens reserved
k_reserved = {
    'DEF': 'DEF',
    'IMPORT': 'IMPORT',
    'FROM': 'FROM',
    'GOTO': 'GOTO',
    'WITH_GOTO': 'WITH_GOTO',
    'IF': 'IF',
    'LABEL': 'LABEL',
    'GLOBAL': 'GLOBAL',
    'PRINT': 'PRINT'
}


# Definitios of tokens not reserved
tokens = [
    'ID',

    # Symbols
    'DOT',
    'ARROBA',
    'ASTERISK',
    'LEFT_PARENTHESIS',
    'RIGHT_PARENTHESIS',
    'COLON',
    'LEFT_CORCH',
    'RIGHT_CORCH',

    'BITWISE_AND',
    'BITWISE_OR',
    'BITWISE_XOR',
    'BITWISE_NOT',
    'BITWISE_SHIFT_LEFT',
    'BITWISE_SHIFT_RIGHT',

    # Logical Operators
    'LESS_THAN',
    'LESS_EQUAL',
    'GREATE_THAN',
    'GREATE_EQUAL',
    'NOT_EQUAL',
    'NOT_EQUAL_LR',

    # Basic Operators
    'PLUS',
    'REST',
    'DIVISION',
    'EXPONENT',
    'MODULAR',
    'DIVISION_DOUBLE',
    # Assignment Operators
    'EQUALS_EQUALS',
    'EQUALS',
    'COMMA',

    # Types of Contents
    'INT_NUMBER',
    'FLOAT_NUMBER',
    'STRINGCONT',
    'CHARCONT',
    'SINGLE_LINE_COMMENT'

]

tokens += list(k_reserved.values())

# Definition of patrons for tokens
digit = r'[0-9]+'
letter = r'([_A-Za-z])'
identifier = r'(' + letter + r'(' + digit + r'|' + letter + r')*)'
decimal = r'\d+\.\d+'
char = r'\'[^\']*\''
string = r'\"[^\"]*\"'
single_line = r'\#.*\n'
# Definition of Symbols
t_DOT = r'\.'
t_ASTERISK = r'\*'
t_COMMA = r'\,'
t_LEFT_PARENTHESIS = r'\('
t_RIGHT_PARENTHESIS = r'\)'
t_LESS_THAN = r'\<'
t_LESS_EQUAL = r'\<\='
t_GREATE_THAN = r'\>'
t_GREATE_EQUAL = r'\>\='
t_NOT_EQUAL = r'\!\='
t_NOT_EQUAL_LR = r'\<\>'
t_EQUALS_EQUALS = r'\=\='
t_EQUALS = r'\='
t_COLON = r'\:'
t_PLUS = r'\+'
t_REST = r'\-'
t_DIVISION = r'\/'
t_EXPONENT = r'\^'
t_MODULAR = r'\%'
t_BITWISE_AND = r'\&'
t_BITWISE_OR = r'\|'
t_BITWISE_XOR = r'\#'
t_BITWISE_NOT = r'\~'
t_BITWISE_SHIFT_LEFT = r'\<\<'
t_BITWISE_SHIFT_RIGHT = r'\>\>'
t_LEFT_CORCH = r'\['
t_RIGHT_CORCH = r'\]'
t_ARROBA = r'\@'
t_DIVISION_DOUBLE = r'\/\/'
# Token recognition using patterns


input = ""


@TOKEN(decimal)
def t_FLOAT_NUMBER(t):
    # r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print(f'Error: %d {t.value}')
        t.value = 0
    return t


@TOKEN(digit)
def t_INT_NUMBER(t):
    try:
        t.value = int(t.value)
    except ValueError:
        print(f'Error: {t.value}')
        t.value = 0
    return t


@TOKEN(identifier)
def t_ID(t):
    t.type = k_reserved.get(t.value.upper(), 'ID')
    return t


@TOKEN(string)
def t_STRINGCONT(t):
    t.value = t.value[1:-1]
    t.lexer.lineno += t.value.count("\n")
    return t


@TOKEN(char)
def t_CHARCONT(t):
    t.value = t.value[1:-1]
    t.lexer.lineno += t.value.count("\n")
    return t

@TOKEN(single_line)
def t_SINGLE_LINE_COMMENT(t):
    t.lexer.lineno += t.value.count('\n')
# New line recognition
def t_new_line(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Skip white spaces


def t_white_space(t):
    r'\s+'
    t.lexer.lineno += t.value.count('\n')

# Recognition of errors


def t_error(t):
    global input

    description = ' or near ' + str(t.value[0])
    column = find_column(t)
    ErrorController().add(33, 'Lexical', description, t.lexer.lineno, column)

    print(f"The character {t.value[0]} ilegal, {t.lexer.lineno} {find_column(t)}")

    t.lexer.skip(1)

# Find column


def find_column(token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def get_text(entra):
    global input
    input = entra
    return input
