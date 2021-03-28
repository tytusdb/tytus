import libs.ply.yacc as yacc
from Optimizador.lex2 import *
from controllers.error_controller import ErrorController
from Optimizador.clases3d import * 
precedence = (
    ('nonassoc', 'LESS_THAN', 'LESS_EQUAL', 'GREATE_THAN',
     'GREATE_EQUAL', 'EQUALS', 'EQUALS_EQUALS','NOT_EQUAL_LR', 'LEFT_CORCH', 'RIGHT_CORCH'),  # Level 4
    ('left', 'LEFT_PARENTHESIS',
     'RIGHT_PARENTHESIS', 'COLON', 'NOT_EQUAL'),  # Level 6
    ('left', 'PLUS', 'REST'),  # Level 7
    ('left', 'ASTERISK', 'DIVISION', 'DIVISION_DOUBLE', 'MODULAR', 'BITWISE_SHIFT_RIGHT',
     'BITWISE_SHIFT_LEFT', 'BITWISE_AND', 'BITWISE_OR'),  # Level 8
    ('left', 'EXPONENT',  'BITWISE_XOR'),  # Level 9
    ('right', 'UPLUS', 'UREST'),  # Level 10
    ('left', 'DOT')  # Level 13
)
# ponete vivo xd 

def p_instruction_list(p):
    '''instructionlist : instructionlist instruction
                       | instruction
    '''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]

    else:
        p[0] = [p[1]]


def p_instruction(p):
    '''instruction : import_instr
                   | alias_instr
                   | ifInstr
                   | SINGLE_LINE_COMMENT
                   | definition_instr
                   | labels_instr
                   | goto_instr
                   | error EQUALS
    '''
    if p.slice[1].type == 'definition_instr':
        p[0] = p[1]
    elif p.slice[1].type == 'goto_instr':
        p[0] = p[1]
    elif p.slice[1].type == 'labels_instr':
        p[0] = p[1]
    elif p.slice[1].type == 'ifInstr':
        p[0] = p[1]
    else:
        pass


def p_import_instr(p):
    '''import_instr : FROM GOTO IMPORT WITH_GOTO
                    | FROM LIST_DOT IMPORT LIST_ID
                    | FROM LIST_DOT IMPORT ASTERISK'''

def p_definition_instr(p):
    '''definition_instr : DEF ID LEFT_PARENTHESIS RIGHT_PARENTHESIS COLON
                        | GLOBAL LIST_ID
                        | PRINT LEFT_PARENTHESIS LIST_EXPRESSION  RIGHT_PARENTHESIS
                        | ID EQUALS comparasion
                        | ID LEFT_CORCH EXPRESSION RIGHT_CORCH EQUALS comparasion
                        | ID LEFT_PARENTHESIS RIGHT_PARENTHESIS'''
    if len(p) == 4:
        if p.slice[2].type == "EQUALS":
            p[0] = AsignacionID(p[1], p[3])
    elif len(p) == 7:
        valor = f'{p[1]}{p[2]}{str(p[3])}{p[4]}'
        p[0] = AsignacionID(valor, p[6])


def p_list_expression(p):
    '''LIST_EXPRESSION : LIST_EXPRESSION COMMA  EXPRESSION
                       | EXPRESSION'''

def p_alias_instr(p):
    '''alias_instr : ARROBA WITH_GOTO'''

def p_list_id(p):
    '''LIST_ID : LIST_ID COMMA ID
               | ID'''

def p_list_dot(p):
    '''LIST_DOT :  LIST_DOT DOT ID
                |  ID'''

# def p_list_dot_asignacion(p):
#     '''LIST_DOT_ASIGNACION : LIST_DOT_ASIGNACION DOT ID LEFT_PARENTHESIS ID EXPRESSION  RIGHT_PARENTHESIS
#                            | LIST_DOT_ASIGNACION DOT ID LEFT_PARENTHESIS  RIGHT_PARENTHESIS
#                            | LIST_DOT_ASIGNACION DOT ID LEFT_PARENTHESIS LIST_DOT_ASIGNACION  RIGHT_PARENTHESIS
#                            | ID LEFT_PARENTHESIS  RIGHT_PARENTHESIS
#                            | ID LEFT_PARENTHESIS ID EXPRESSION RIGHT_PARENTHESIS'''


def p_goto_instr(p):
    ''' goto_instr : GOTO DOT ID'''
    p[0] = Goto(p[3])
def p_labels_instr(p):
    '''labels_instr : LABEL DOT ID'''
    p[0] = LabelIF(p[3])
def p_ifInstr(p):
    '''ifInstr : IF comparasion COLON GOTO DOT ID
               | IF LEFT_PARENTHESIS comparasion RIGHT_PARENTHESIS COLON GOTO DOT ID'''
    if len(p) == 7:
        p[0] = ifStatement(p[2], Goto(p[6]))
    else:
        p[0] = ifStatement(p[3], Goto(p[8]))

def p_comparasion(p):
    ''' comparasion : EXPRESSION RELOP EXPRESSION
                    | EXPRESSION'''
    if len(p) == 4:
        p[0] = Relop(p[1], p[2], p[3])
    else:
        p[0] = p[1]

def p_expression(p):
    '''EXPRESSION : EXPRESSION PLUS EXPRESSION
                  | EXPRESSION REST EXPRESSION
                  | EXPRESSION ASTERISK EXPRESSION
                  | EXPRESSION DIVISION EXPRESSION
                  | EXPRESSION EXPONENT EXPRESSION
                  | EXPRESSION MODULAR EXPRESSION
                  | EXPRESSION DOT EXPRESSION 
                  | EXPRESSION DIVISION_DOUBLE EXPRESSION 
                  | REST EXPRESSION %prec UREST
                  | PLUS EXPRESSION %prec UPLUS
                  | EXPRESSION BITWISE_SHIFT_RIGHT EXPRESSION
                  | EXPRESSION BITWISE_SHIFT_LEFT EXPRESSION
                  | EXPRESSION BITWISE_AND EXPRESSION
                  | EXPRESSION BITWISE_OR EXPRESSION
                  | EXPRESSION BITWISE_XOR EXPRESSION
                  | BITWISE_NOT EXPRESSION %prec UREST
                  | LEFT_CORCH comparasion RIGHT_CORCH
                  | ID LEFT_PARENTHESIS comparasion RIGHT_PARENTHESIS
                  | ID LEFT_PARENTHESIS RIGHT_PARENTHESIS
                  | ID LEFT_CORCH comparasion RIGHT_CORCH
                  | ID LEFT_CORCH ID COLON ID RIGHT_CORCH
                  | STRING_CADENAS
                  | INTEGER_NUMBERS'''
                  # Si ya estas ahora xd ponete vivo x2
    if len(p) == 4:
        if p.slice[1].type == "LEFT_CORCH":
            p[0] = p[2]
        else:
            p[0] = ArithmeticBinaryOperation(p[1], p[3], p[2])
    elif len(p) == 5:
        valor = f'{p[1]}{p[2]}{str(p[3])}{p[4]}'
        p[0] = valor
    elif len(p) == 2:
        p[0] = p[1]


def p_relop(p):
    '''RELOP : EQUALS_EQUALS
             | NOT_EQUAL
             | GREATE_EQUAL
             | GREATE_THAN
             | LESS_THAN
             | LESS_EQUAL
             | NOT_EQUAL_LR'''
    p[0] = p[1]

def p_string_cadenas(p):
    '''STRING_CADENAS :  STRINGCONT
                      |  CHARCONT
                      |  ID'''
    p[0] = p[1]
def p_integer_numbers(p):
    '''INTEGER_NUMBERS : INT_NUMBER
                       | FLOAT_NUMBER '''
    p[0] = p[1]

def p_error(p):
    try:
        # print(str(p.value))
        description = ' or near ' + str(p.value)
        column = find_column(p)
        ErrorController().add(33, 'Syntactic', description, p.lineno, column)
    except AttributeError:
        # print(number_error, description)
        ErrorController().add(1, 'Syntactic', '', 'EOF', 'EOF')


parser = yacc.yacc()


def parse_optimizacion(inpu):
    global input, contador_instr
    contador_instr = 0
    ErrorController().destroy()
    lexer = lex.lex()
    lexer.lineno = 1
    input = inpu
    get_text(input)
    return parser.parse(inpu, lexer=lexer)