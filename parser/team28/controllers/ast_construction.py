# from generate_ast import GraficarAST
from re import L

import libs.ply.yacc as yacc
import os

from models.nodo import Node
from utils.analyzers.lex import *


# Precedencia, entre mayor sea el nivel mayor sera su inportancia para su uso

precedence = (
    ('left', 'OR'),  # Level 1
    ('left', 'AND'),  # Level 2
    ('right', 'NOT'),  # Level 3
    ('nonassoc', 'LESS_THAN', 'LESS_EQUAL', 'GREATE_THAN',
     'GREATE_EQUAL', 'EQUALS', 'NOT_EQUAL_LR'),  # Level 4
    ('nonassoc', 'BETWEEN', 'IN', 'LIKE', 'ILIKE', 'SIMILAR'),  # Level 5
    ('left', 'SEMICOLON', 'LEFT_PARENTHESIS',
     'RIGHT_PARENTHESIS', 'COMMA', 'COLON', 'NOT_EQUAL'),  # Level 6
    ('left', 'PLUS', 'REST'),  # Level 7
    ('left', 'ASTERISK', 'DIVISION', 'MODULAR', 'BITWISE_SHIFT_RIGHT',
     'BITWISE_SHIFT_LEFT', 'BITWISE_AND', 'BITWISE_OR'),  # Level 8
    ('left', 'EXPONENT',  'BITWISE_XOR', 'SQUARE_ROOT', 'CUBE_ROOT'),  # Level 9
    ('right', 'UPLUS', 'UREST'),  # Level 10
    ('left', 'DOT')  # Level 13
)

# Definicion de Gramatica, un poco de defincion
# Para que no se confundad, para crear la gramatica y se reconocida
# siempre se empieza la funcion con la letra p, ejemplo p_name_function y
# siempre recibe el paramatro p, en la gramatica los dos puntos es como usar ::=
# No debe quedar junto a los no terminales, ejemplo EXPRESSION:, por que en este caso marcara un error
# si la gramatica solo consta de una linea se pueden usar comillas simples ' ' pero si ya consta de varias lineas
# se usa ''' ''' para que no marque error
# Nota: p siempre es un array y para llamar los tokens, solo se escriben tal y como fueron definidos en la clase lex.py
# y estos no pueden ser usados para los nombres de los no terminales, si no lanzara error

# =====================================================================================
# =====================================================================================
# ====================================================================================


def p_initial(p):
    '''root : instructionlist
    '''
    nodo = Node('ROOT')
    nodo.add_childrens(p[1])
    nodo.production = f"<root> ::= <instructionlist>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_instruction_list(p):
    '''instructionlist : instructionlist sqlinstruction
                       | sqlinstruction
    '''
    nodo = Node('Instruction List')
    if len(p) == 3:
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        nodo.production = f"<instructionlist> ::= <instructionlist> <sqlinstruction>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[2].production}"
    else:
        nodo.add_childrens(p[1])
        nodo.production = f"<instructionlist> ::= <sqlinstruction>\n"
        nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_sql_instructionDDL(p):
    '''sqlinstruction : ddl
    '''
    nodo = Node('SQL Instruction')
    nodo.add_childrens(p[1])
    nodo.production = f"<sqlinstruction> ::= <DDL>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_sql_instructionDML(p):
    '''sqlinstruction :  DML
    '''
    nodo = Node('SQL Instruction')
    nodo.add_childrens(p[1])
    nodo.production = f"<sqlinstruction> ::= <DML>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_sql_instruction_usestatement(p):
    '''sqlinstruction :  usestatement
    '''
    nodo = Node('SQL Instruction')
    nodo.add_childrens(p[1])
    nodo.production = f"<sqlinstruction> ::= <usestatement>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_sql_instruction_COMMENT(p):
    '''sqlinstruction :  MULTI_LINE_COMMENT
                    | SINGLE_LINE_COMMENT
    '''
    nodo = Node('SQL Instruction')
    nodo.add_childrens(p[1])
    nodo.production = f"<sqlinstruction> ::= <COMMENT>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_use_statement(p):
    '''usestatement : USE ID SEMICOLON'''
    nodo = Node('USE Statement')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(Node(p[3]))
    nodo.production = f"<usestatement> ::= USE ID SEMICOLON\n"
    p[0] = nodo


def p_ddl_createstatement(p):
    '''ddl : createstatement
    '''
    nodo = Node('DDL')
    nodo.add_childrens(p[1])
    nodo.production = f"<DDL> ::= <createstatement>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_ddl_showstatement(p):
    '''ddl : showstatement
    '''
    nodo = Node('DDL')
    nodo.add_childrens(p[1])
    nodo.production = f"<DDL> ::= <showstatement>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_ddl_alterstatement(p):
    '''ddl : alterstatement
    '''
    nodo = Node('DDL')
    nodo.add_childrens(p[1])
    nodo.production = f"<DDL> ::= <alterstatement>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_ddl_dropstatement(p):
    '''ddl : dropstatement
    '''
    nodo = Node('DDL')
    nodo.add_childrens(p[1])
    nodo.production = f"<DDL> ::= <dropstatement>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_create_statement(p):
    '''createstatement : CREATE optioncreate SEMICOLON'''
    nodo = Node('Create Statement')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.add_childrens(Node(p[3]))
    nodo.production = f"<createstatement> ::= CREATE <optioncreate> SEMICOLON\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_option_create(p):
    '''optioncreate : TYPE SQLNAME AS ENUM LEFT_PARENTHESIS typelist RIGHT_PARENTHESIS
                    | DATABASE createdb
                    | OR REPLACE DATABASE createdb
                    | TABLE SQLNAME LEFT_PARENTHESIS columnstable RIGHT_PARENTHESIS
                    | TABLE SQLNAME LEFT_PARENTHESIS columnstable RIGHT_PARENTHESIS INHERITS LEFT_PARENTHESIS ID RIGHT_PARENTHESIS
    '''
    nodo = Node('Option Create')
    if len(p) == 8:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(Node(p[5]))
        nodo.add_childrens(p[6])
        nodo.add_childrens(Node(p[7]))
        nodo.production = f"<optioncreate> ::= <TYPE> <SQLNAME> AS ENUM LEFT_PARENTHESIS typelist RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[2].production}"
        nodo.production += f"{p[6].production}"
        p[0] = nodo

    elif len(p) == 3:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.production = f"<optioncreate> ::= DATABASE <createdb>\n"
        nodo.production += f"{p[2].production}"
        p[0] = nodo

    elif len(p) == 5:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.production = f"<optioncreate> ::= OR REPLACE DATABASE <createdb>\n"
        nodo.production += f"{p[4].production}"
        p[0] = nodo

    elif len(p) == 6:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.add_childrens(Node(p[5]))
        nodo.production = f"<optioncreate> ::= TABLE <SQLNAME> LEFT_PARENTHESIS <columnstable> RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[2].production}"
        nodo.production += f"{p[4].production}"
        p[0] = nodo

    elif len(p) == 10:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.add_childrens(Node(p[5]))
        nodo.add_childrens(Node(p[6]))
        nodo.add_childrens(Node(p[7]))
        nodo.add_childrens(Node(p[8]))
        nodo.add_childrens(Node(p[9]))
        nodo.production = f"<optioncreate> ::= TABLE <SQLNAME> LEFT_PARENTHESIS <columnstable> RIGHT_PARENTHESIS INHERITS LEFT_PARENTHESIS ID RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[2].production}"
        nodo.production += f"{p[4].production}"
        p[0] = nodo


def p_type_list(p):
    '''typelist : typelist COMMA SQLNAME
                | SQLNAME '''
    nodo = Node('Type List')

    if len(p) == 4:
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.production = f"<typelist> ::= <typelist> <SQLNAME>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[3].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        nodo.production = f"<typelist> ::= <SQLNAME>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo


def p_create_db(p):
    '''createdb : IF NOT EXISTS ID listpermits
                | IF NOT EXISTS ID
                | ID listpermits
                | ID 
    '''
    nodo = Node('Create Database')

    if len(p) == 6:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        nodo.production = f"<createdb> ::= IF NOT EXISTS ID <listpermits>\n"
        nodo.production += f"{p[5].production}"
        p[0] = nodo

    elif len(p) == 5:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        nodo.production = f"<createdb> ::= IF NOT EXISTS ID\n"
        p[0] = nodo

    elif len(p) == 3:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.production = f"<createdb> ::= ID <listpermits>\n"
        nodo.production += f"{p[2].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.production = f"<createdb> ::= ID\n"
        p[0] = nodo


def p_list_permits(p):
    '''listpermits : listpermits permits
                   | permits
    '''

    nodo = Node('List Permits')
    if len(p) == 3:
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        nodo.production = f"<listpermits> ::= <listpermits> <permits>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[2].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        nodo.production = f"<listpermits> ::= <permits>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo


def p_permits_OWNER_EQUALS(p):
    '''permits : OWNER EQUALS SQLNAME
    '''
    nodo = Node('Permits')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.production = f"<listpermits> ::= OWNER EQUALS <SQLNAME>\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_permits_OWNER(p):
    '''permits : OWNER SQLNAME
    '''
    nodo = Node('Permits')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.production = f"<permits> ::= OWNER <SQLNAME>\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_permits_MODE_EQUALS(p):
    '''permits : MODE EQUALS INT_NUMBER
    '''
    nodo = Node('Permits')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(Node(p[3]))
    nodo.production = f"<permits> ::= MODE EQUALS INT_NUMBER\n"
    p[0] = nodo


def p_permits_MODE(p):
    '''permits : MODE INT_NUMBER 
    '''
    nodo = Node('Permits')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.production = f"<permits> ::= MODE INT_NUMBER\n"
    p[0] = nodo


def p_columns_table(p):
    '''columnstable : columnstable COMMA column
                    | column
    '''
    nodo = Node('Columns Table')
    if len(p) == 4:
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.production = f"<columnstable> ::= <columnstable> COMMA <column>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[3].production}"
        p[0] = nodo

    else:
        nodo.add_childrens(p[1])
        nodo.production = f"<columnstable> ::= <column>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo


def p_column(p):
    '''column : ID typecol optionscollist
              | ID typecol
              | UNIQUE LEFT_PARENTHESIS columnlist RIGHT_PARENTHESIS
              | PRIMARY KEY LEFT_PARENTHESIS columnlist RIGHT_PARENTHESIS
              | FOREIGN KEY LEFT_PARENTHESIS columnlist RIGHT_PARENTHESIS REFERENCES ID LEFT_PARENTHESIS columnlist RIGHT_PARENTHESIS
              | CONSTRAINT ID CHECK LEFT_PARENTHESIS conditionColumn RIGHT_PARENTHESIS
              | CHECK LEFT_PARENTHESIS conditionColumn RIGHT_PARENTHESIS
    '''
    nodo = Node('Column')

    if len(p) == 4:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(p[3])
        nodo.production = f"<column> ::= ID <typecol> <optionscollist>\n"
        nodo.production += f"{p[2].production}"
        nodo.production += f"{p[3].production}"
        p[0] = nodo

    elif len(p) == 3:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.production = f"<column> ::= ID <typecol>\n"
        nodo.production += f"{p[2].production}"
        p[0] = nodo

    elif len(p) == 5:
        if p[1].lower() == 'UNIQUE'.lower():
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(Node(p[2]))
            nodo.add_childrens(p[3])
            nodo.add_childrens(Node(p[4]))
            nodo.production = f"<column> ::= UNIQUE LEFT_PARENTHESIS <columnlist> RIGHT_PARENTHESIS\n"
            nodo.production += f"{p[3].production}"
            p[0] = nodo

        else:  # CHECK
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(Node(p[2]))
            nodo.add_childrens(p[3])
            nodo.add_childrens(Node(p[4]))
            nodo.production = f"<column> ::= CHECK LEFT_PARENTHESIS <conditionColumn> RIGHT_PARENTHESIS\n"
            nodo.production += f"{p[3].production}"
            p[0] = nodo

    elif len(p) == 6:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.add_childrens(Node(p[5]))
        nodo.production = f"<column> ::= PRIMARY KEY LEFT_PARENTHESIS <columnlist> RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[4].production}"
        p[0] = nodo

    elif len(p) == 11:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.add_childrens(Node(p[5]))
        nodo.add_childrens(Node(p[6]))
        nodo.add_childrens(Node(p[7]))
        nodo.add_childrens(Node(p[8]))
        nodo.add_childrens(p[9])
        nodo.add_childrens(Node(p[10]))
        nodo.production = f"<column> ::= FOREIGN KEY LEFT_PARENTHESIS <columnlist> RIGHT_PARENTHESIS REFERENCES ID LEFT_PARENTHESIS <columnlist> RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[4].production}"
        nodo.production += f"{p[9].production}"
        p[0] = nodo

    elif len(p) == 7:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        nodo.add_childrens(Node(p[6]))
        nodo.production = f"<column> ::= CONSTRAINT ID CHECK LEFT_PARENTHESIS <conditionColumn> RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[5].production}"
        p[0] = nodo


def p_type_col_SMALLINT(p):
    '''typecol : SMALLINT
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<typecol> ::= SMALLINT\n"
    p[0] = nodo


def p_type_col_INTEGER(p):
    '''typecol :  INTEGER
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<typecol> ::= INTEGER\n"
    p[0] = nodo


def p_type_col_BIGINT(p):
    '''typecol : BIGINT
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<typecol> ::= BIGINT\n"
    p[0] = nodo


def p_type_col_DECIMAL_list(p):
    '''typecol : DECIMAL LEFT_PARENTHESIS INT_NUMBER COMMA INT_NUMBER RIGHT_PARENTHESIS
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(Node(p[3]))
    nodo.add_childrens(Node(p[4]))
    nodo.add_childrens(Node(p[5]))
    nodo.add_childrens(Node(p[6]))
    nodo.production = f"<typecol> ::= DECIMAL LEFT_PARENTHESIS INT_NUMBER COMMA INT_NUMBER RIGHT_PARENTHESIS\n"
    p[0] = nodo


def p_type_col_DECIMAL(p):
    '''typecol : DECIMAL LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(Node(p[3]))
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<typecol> ::= DECIMAL LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS\n"
    p[0] = nodo


def p_type_col_NUMERIC_list(p):
    '''typecol : NUMERIC LEFT_PARENTHESIS INT_NUMBER COMMA INT_NUMBER RIGHT_PARENTHESIS
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(Node(p[3]))
    nodo.add_childrens(Node(p[4]))
    nodo.add_childrens(Node(p[5]))
    nodo.add_childrens(Node(p[6]))
    nodo.production = f"<typecol> ::= NUMERIC LEFT_PARENTHESIS INT_NUMBER COMMA INT_NUMBER RIGHT_PARENTHESIS\n"
    p[0] = nodo


def p_type_col_NUMERIC(p):
    '''typecol : NUMERIC LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(Node(p[3]))
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<typecol> ::= NUMERIC LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS\n"
    p[0] = nodo


def p_type_col_REAL(p):
    '''typecol : REAL
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<typecol> ::= REAL\n"
    p[0] = nodo


def p_type_col_DOUBLE(p):
    '''typecol : DOUBLE PRECISION
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.production = f"<typecol> ::= DOUBLE PRECISION\n"
    p[0] = nodo


def p_type_col_MONEY(p):
    '''typecol : MONEY
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<typecol> ::= MONEY\n"
    p[0] = nodo


def p_type_col_CHARACTER_VARYING_INT(p):
    '''typecol : CHARACTER VARYING LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(Node(p[3]))
    nodo.add_childrens(Node(p[4]))
    nodo.add_childrens(Node(p[5]))
    nodo.production = f"<typecol> ::= CHARACTER VARYING LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS\n"
    p[0] = nodo


def p_type_col_CHARACTER_VARYING(p):
    '''typecol : CHARACTER VARYING
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.production = f"<typecol> ::= CHARACTER VARYING\n"
    p[0] = nodo


def p_type_col_VARCHAR_INT(p):
    '''typecol : VARCHAR LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(Node(p[3]))
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<typecol> ::= VARCHAR LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESI\n"
    p[0] = nodo


def p_type_col_VARCHAR(p):
    '''typecol : VARCHAR
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<typecol> ::= VARCHAR\n"
    p[0] = nodo


def p_type_col_CHARACTER_INT(p):
    '''typecol : CHARACTER LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(Node(p[3]))
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<typecol> ::= CHARACTER LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS\n"
    p[0] = nodo


def p_type_col_CHARACTER(p):
    '''typecol : CHARACTER
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<typecol> ::= CHARACTER\n"
    p[0] = nodo


def p_type_col_CHAR_INT(p):
    '''typecol : CHAR LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(Node(p[3]))
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<typecol> ::= CHAR LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS\n"
    p[0] = nodo


def p_type_col_CHAR(p):
    '''typecol : CHAR
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<typecol> ::= CHAR\n"
    p[0] = nodo


def p_type_col_TEXT(p):
    '''typecol : TEXT
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<typecol> ::= TEXT\n"
    p[0] = nodo


def p_type_col_TIMESTAMP_INT(p):
    '''typecol : TIMESTAMP LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(Node(p[3]))
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<typecol> ::= TIMESTAMP LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS\n"
    p[0] = nodo


def p_type_col_TIMESTAMP(p):
    '''typecol : TIMESTAMP 
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<typecol> ::= TIMESTAMP\n"
    p[0] = nodo


def p_type_col_DATE(p):
    '''typecol : DATE
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<typecol> ::= TIMESTAMP\n"
    p[0] = nodo


def p_type_col_TIME_INT(p):
    '''typecol : TIME LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(Node(p[3]))
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<typecol> ::= TIME LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS\n"
    p[0] = nodo


def p_type_col_TIME(p):
    '''typecol : TIME
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<typecol> ::= TIME\n"
    p[0] = nodo


def p_type_col_INTERVAL(p):
    '''typecol : INTERVAL SQLNAME
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.production = f"<typecol> ::= INTERVAL <SQLNAME>\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_type_col_BOOLEAN(p):
    '''typecol : BOOLEAN
    '''
    nodo = Node('Type Column')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<typecol> ::= BOOLEAN\n"
    p[0] = nodo


def p_options_col_list(p):
    '''optionscollist : optionscollist optioncol
                      | optioncol
    '''
    nodo = Node('Options Column List')
    if len(p) == 3:
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        nodo.production = f"<optionscollist> ::= <optionscollist> <optioncol>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[2].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        nodo.production = f"<optionscollist> ::= <optioncol>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo


def p_option_col_DEFAULT_SIMP(p):
    '''optioncol : DEFAULT SQLSIMPLEEXPRESSION
    '''
    nodo = Node('Option Column')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.production = f"<optioncol> ::= DEFAULT <SQLSIMPLEEXPRESSION>\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_option_col_NOT_NULL(p):
    '''optioncol : NOT NULL
    '''
    nodo = Node('Option Column')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.production = f"<optioncol> ::= NOT NULL\n"
    p[0] = nodo


def p_option_col_NULL(p):
    '''optioncol : NULL
    '''
    nodo = Node('Option Column')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<optioncol> ::= NULL\n"
    p[0] = nodo


def p_option_col_constraint_unique(p):
    '''optioncol : CONSTRAINT ID UNIQUE 
    '''
    nodo = Node('Option Column')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(Node(p[3]))
    nodo.production = f"<optioncol> ::= CONSTRAINT ID UNIQUE\n"
    p[0] = nodo


def p_option_col_UNIQUE(p):
    '''optioncol : UNIQUE
    '''
    nodo = Node('Option Column')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<optioncol> ::= UNIQUE\n"
    p[0] = nodo


def p_option_col_CONSTRAINT_CHECK(p):
    '''optioncol : CONSTRAINT ID CHECK LEFT_PARENTHESIS conditionColumn RIGHT_PARENTHESIS
                 | CHECK LEFT_PARENTHESIS conditionColumn RIGHT_PARENTHESIS
                 | PRIMARY KEY
    '''
    nodo = Node('Option Column')
    if len(p) == 3:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.production = f"<optioncol> ::= PRIMARY KEY\n"
        p[0] = nodo
    elif len(p) == 5:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.production = f"<optioncol> ::= CHECK LEFT_PARENTHESIS <conditionColumn> RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[3].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        nodo.add_childrens(Node(p[6]))
        nodo.production = f"<optioncol> ::= CONSTRAINT ID CHECK LEFT_PARENTHESIS <conditionColumn> RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[5].production}"
        p[0] = nodo


def p_option_col(p):
    '''optioncol : REFERENCES ID 
    '''
    nodo = Node('Option Column')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.production = f"<optioncol> ::= REFERENCES ID\n"
    p[0] = nodo


def p_condition_column(p):
    '''conditionColumn : conditioncheck'''
    nodo = Node('Condition Column')
    nodo.add_childrens(p[1])
    nodo.production = f"<conditionColumn> ::= <conditioncheck>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_condition_check(p):
    '''conditioncheck : SQLRELATIONALEXPRESSION
    '''
    nodo = Node('Condition Check')
    nodo.add_childrens(p[1])
    nodo.production = f"<conditioncheck> ::= <SQLRELATIONALEXPRESSION>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_column_list(p):
    '''columnlist : columnlist COMMA ID
                  | ID
    '''
    nodo = Node('Column List')
    if len(p) == 4:
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.production = f"<columnlist> ::= <columnlist> COMMA ID>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.production = f"<columnlist> ::= ID\n"
        p[0] = nodo


def p_show_statement(p):
    '''showstatement : SHOW DATABASES SEMICOLON
                     | SHOW DATABASES LIKE SQLNAME SEMICOLON
    '''
    nodo = Node('Show Statement')
    if len(p) == 4:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.production = f"<showstatement> ::= SHOW DATABASES SEMICOLON\n"
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.add_childrens(Node(p[5]))
        nodo.production = f"<showstatement> ::= SHOW DATABASES LIKE <SQLNAME> SEMICOLON\n"
        nodo.production += f"{p[4].production}"
        p[0] = nodo


def p_alter_statement(p):
    '''alterstatement : ALTER optionsalter SEMICOLON
    '''
    nodo = Node('Alter Statement')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.add_childrens(Node(p[3]))
    nodo.production = f"<alterstatement> ::= ALTER <optionsalter> SEMICOLON\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_options_alter_DATABASE(p):
    '''optionsalter : DATABASE alterdatabase
    '''
    nodo = Node('Options Alter')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.production = f"<optionsalter> ::= DATABASE <alterdatabase>\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_options_alter_TABLE(p):
    '''optionsalter : TABLE altertable
    '''
    nodo = Node('Options Alter')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.production = f"<optionsalter> ::= TABLE <altertable>\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_alter_database(p):
    '''alterdatabase : ID RENAME TO ID
                     | ID OWNER TO typeowner
    '''
    nodo = Node('Alter Database')
    if p[2].lower() == 'RENAME'.lower():
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        nodo.production = f"<alterdatabase> ::= ID RENAME TO ID\n"
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.production = f"<alterdatabase> ::= ID OWNER TO <typeowner>\n"
        nodo.production += f"{p[4].production}"
        p[0] = nodo


def p_type_owner_ID(p):
    '''typeowner : ID
    '''
    nodo = Node('Type Owner')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<typeowner> ::= ID\n"
    p[0] = nodo


def p_type_owner_CURRENT_USER(p):
    '''typeowner : CURRENT_USER
    '''
    nodo = Node('Type Owner')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<typeowner> ::= CURRENT_USER\n"
    p[0] = nodo


def p_type_owner_SESSION_USER(p):
    '''typeowner : SESSION_USER 
    '''
    nodo = Node('Type Owner')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<typeowner> ::= SESSION_USER\n"
    p[0] = nodo


def p_alter_table(p):
    '''altertable : ID alterlist
    '''
    nodo = Node('Alter Table')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.production = f"<altertable> ::= ID <alterlist>\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_alter_list(p):
    '''alterlist : alterlist COMMA typealter
                 | typealter
    '''
    nodo = Node('Alter List')
    if(len(p) == 4):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.production = f"<alterlist> ::= <alterlist> COMMA <typealter>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[3].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        p[0] = nodo
        nodo.production = f"<alterlist> ::= <typealter>\n"
        nodo.production += f"{p[1].production}"


def p_type_alter_ADD(p):
    '''typealter : ADD addalter
    '''
    nodo = Node('Type Alter')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.production = f"<typealter> ::= ADD <addalter>\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_type_alter_ALTER(p):
    '''typealter : ALTER alteralter
    '''
    nodo = Node('Type Alter')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.production = f"<typealter> ::= ALTER <alteralter>\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_type_alter_DROP(p):
    '''typealter : DROP dropalter
    '''
    nodo = Node('Type Alter')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.production = f"<typealter> ::= DROP <dropalter>\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_type_alter_RENAME(p):
    '''typealter : RENAME  renamealter
    '''
    nodo = Node('Type Alter')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.production = f"<typealter> ::= RENAME <renamealter>\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_add_alter(p):
    '''addalter : COLUMN ID typecol
                | CHECK LEFT_PARENTHESIS conditionColumn RIGHT_PARENTHESIS
                | CONSTRAINT ID UNIQUE LEFT_PARENTHESIS ID RIGHT_PARENTHESIS
                | FOREIGN KEY LEFT_PARENTHESIS columnlist RIGHT_PARENTHESIS REFERENCES ID LEFT_PARENTHESIS columnlist RIGHT_PARENTHESIS
    '''
    nodo = Node('Add Alter')

    if len(p) == 4:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.production = f"<addalter> ::= COLUMN ID <typecol>\n"
        nodo.production += f"{p[3].production}"
        p[0] = nodo

    elif len(p) == 5:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.production = f"<addalter> ::= CHECK LEFT_PARENTHESIS <conditionColumn> RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[3].production}"
        p[0] = nodo

    elif len(p) == 7:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(Node(p[5]))
        nodo.add_childrens(Node(p[6]))
        nodo.production = f"<addalter> ::= CONSTRAINT ID UNIQUE LEFT_PARENTHESIS ID RIGHT_PARENTHESIS\n"
        p[0] = nodo

    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.add_childrens(Node(p[5]))
        nodo.add_childrens(Node(p[6]))
        nodo.add_childrens(Node(p[7]))
        nodo.add_childrens(Node(p[8]))
        nodo.add_childrens(p[9])
        nodo.add_childrens(Node(p[10]))
        nodo.production = f"<addalter> ::= FOREIGN KEY LEFT_PARENTHESIS <columnlist> RIGHT_PARENTHESIS REFERENCES ID LEFT_PARENTHESIS <columnlist> RIGHT_PARENTHESIS\n"
        p[0] = nodo


def p_alter_alter(p):
    '''alteralter : COLUMN ID SET NOT NULL
                  | COLUMN ID TYPE typecol
    '''
    nodo = Node('Alter Alter')
    if len(p) == 6:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(Node(p[5]))
        nodo.production = f"<alteralter> ::= COLUMN ID SET NOT NULL\n"
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.production = f"<alteralter> ::= COLUMN ID TYPE <typecol>\n"
        nodo.production += f"{p[4].production}"
        p[0] = nodo


def p_drop_alter_COLUMN(p):
    '''dropalter : COLUMN ID
    '''
    nodo = Node('Drop Alter')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.production = f"<dropalter> ::= COLUMN ID\n"
    p[0] = nodo


def p_drop_alter_CONSTRAINT(p):
    '''dropalter : CONSTRAINT ID
    '''
    nodo = Node('Drop Alter')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.production = f"<dropalter> ::= CONSTRAINT ID\n"
    p[0] = nodo


def p_rename_alter(p):
    '''renamealter : COLUMN ID TO ID
    '''
    nodo = Node('Rename Alter')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(Node(p[3]))
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<renamealter> ::= COLUMN ID TO ID\n"
    p[0] = nodo


def p_drop_statement(p):
    '''dropstatement : DROP optionsdrop SEMICOLON'''
    nodo = Node('Drop Statement')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.add_childrens(Node(p[3]))
    nodo.production = f"<dropstatement> ::= DROP <optionsdrop> SEMICOLON\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_options_drop_dropdatabase(p):
    '''optionsdrop : DATABASE dropdatabase
    '''
    nodo = Node('Options Drop')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.production = f"<optionsdrop> ::= DATABASE <dropdatabase>\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_options_drop_(p):
    '''optionsdrop : TABLE droptable
    '''
    nodo = Node('Options Drop')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.production = f"<optionsdrop> ::= TABLE <droptable>\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_drop_database(p):
    '''dropdatabase : IF EXISTS ID
                    | ID
    '''
    nodo = Node('Drop Database')
    if len(p) == 4:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.production = f"<dropdatabase> ::= IF EXISTS ID\n"
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.production = f"<dropdatabase> ::= ID\n"
        p[0] = nodo


def p_drop_table(p):
    '''droptable : ID
    '''
    nodo = Node('Drop Table')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<droptable> ::= ID\n"
    p[0] = nodo


# =====================================================================================
# =====================================================================================
# =====================================================================================

def p_dml_QUERYSTATEMENT(p):
    '''DML : QUERYSTATEMENT'''
    nodo = Node('DML')
    nodo.add_childrens(p[1])
    nodo.production = f"<DML> ::= <QUERYSTATEMENT>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_dml_INSERTSTATEMENT(p):
    '''DML : INSERTSTATEMENT'''
    nodo = Node('DML')
    nodo.add_childrens(p[1])
    nodo.production = f"<DML> ::= <QUERYSTATEMENT>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_dml_DELETESTATEMENT(p):
    '''DML : DELETESTATEMENT'''
    nodo = Node('DML')
    nodo.add_childrens(p[1])
    nodo.production = f"<DML> ::= <DELETESTATEMENT>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_dml_UPDATESTATEMENT(p):
    '''DML : UPDATESTATEMENT'''
    nodo = Node('DML')
    nodo.add_childrens(p[1])
    nodo.production = f"<DML> ::= <UPDATESTATEMENT>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_update_statement(p):
    '''UPDATESTATEMENT : UPDATE ID OPTIONS1 SET SETLIST OPTIONSLIST2 SEMICOLON
                       | UPDATE ID SET SETLIST OPTIONSLIST2 SEMICOLON
                       | UPDATE ID SET SETLIST SEMICOLON'''
    nodo = Node('Update Statement')
    if(len(p) == 7):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.add_childrens(p[5])
        nodo.add_childrens(Node(p[6]))
        nodo.production = f"<UPDATESTATEMENT> ::= UPDATE ID SET <SETLIST> <OPTIONSLIST2> SEMICOLON\n"
        nodo.production += f"{p[4].production}"
        nodo.production += f"{p[5].production}"
        p[0] = nodo
    elif(len(p) == 6):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.add_childrens(Node(p[5]))
        nodo.production = f"<UPDATESTATEMENT> ::= UPDATE ID SET <SETLIST> SEMICOLON\n"
        nodo.production += f"{p[4].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        nodo.add_childrens(p[6])
        nodo.add_childrens(Node(p[7]))
        nodo.production = f"<UPDATESTATEMENT> ::= UPDATE ID <OPTIONS1> SET <SETLIST> <OPTIONSLIST2> SEMICOLON\n"
        nodo.production += f"{p[3].production}"
        nodo.production += f"{p[5].production}"
        nodo.production += f"{p[6].production}"
        p[0] = nodo


def p_set_list(p):
    '''SETLIST : SETLIST COMMA COLUMNVALUES
               | COLUMNVALUES'''
    nodo = Node('Set List')
    if(len(p) == 4):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.production = f"<SETLIST> ::= <SETLIST> COMMA <COLUMNVALUES>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[3].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        nodo.production = f"<SETLIST> ::= <COLUMNVALUES>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo


def p_column_values(p):
    '''COLUMNVALUES : OBJECTREFERENCE EQUALS SQLEXPRESSION2'''
    nodo = Node('Column Values')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.production = f"<COLUMNVALUES> ::= <OBJECTREFERENCE> EQUALS <SQLEXPRESSION2>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_sql_expression2_PLUS(p):
    '''SQLEXPRESSION2 : SQLEXPRESSION2 PLUS SQLEXPRESSION2'''
    nodo = Node('SQL Expression 2')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.production = f"<SQLEXPRESSION2> ::= <SQLEXPRESSION2> PLUS <SQLEXPRESSION2>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_sql_expression2_REST(p):
    '''SQLEXPRESSION2 : SQLEXPRESSION2 REST SQLEXPRESSION2'''
    nodo = Node('SQL Expression 2')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.production = f"<SQLEXPRESSION2> ::= <SQLEXPRESSION2> REST <SQLEXPRESSION2>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_sql_expression2_DIVISION(p):
    '''SQLEXPRESSION2 : SQLEXPRESSION2 DIVISION SQLEXPRESSION2'''
    nodo = Node('SQL Expression 2')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.production = f"<SQLEXPRESSION2> ::= <SQLEXPRESSION2> DIVISION <SQLEXPRESSION2>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_sql_expression2_ASTERISK(p):
    '''SQLEXPRESSION2 : SQLEXPRESSION2 ASTERISK SQLEXPRESSION2'''
    nodo = Node('SQL Expression 2')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.production = f"<SQLEXPRESSION2> ::= <SQLEXPRESSION2> ASTERISK <SQLEXPRESSION2>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_sql_expression2_MODULAR(p):
    '''SQLEXPRESSION2 : SQLEXPRESSION2 MODULAR SQLEXPRESSION2'''
    nodo = Node('SQL Expression 2')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.production = f"<SQLEXPRESSION2> ::= <SQLEXPRESSION2> MODULAR <SQLEXPRESSION2>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_sql_expression2_EXPONENT(p):
    '''SQLEXPRESSION2 : SQLEXPRESSION2 EXPONENT SQLEXPRESSION2'''
    nodo = Node('SQL Expression 2')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.production = f"<SQLEXPRESSION2> ::= <SQLEXPRESSION2> EXPONENT <SQLEXPRESSION2>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_sql_expression2_uREST(p):
    '''SQLEXPRESSION2 : REST SQLEXPRESSION2 %prec UREST'''
    nodo = Node('SQL Expression 2')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.production = f"<SQLEXPRESSION2> ::= REST <SQLEXPRESSION2> %prec UREST\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_sql_expression2_uPLUS(p):
    '''SQLEXPRESSION2 : PLUS SQLEXPRESSION2 %prec UPLUS'''
    nodo = Node('SQL Expression 2')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.production = f"<SQLEXPRESSION2> ::= PLUS <SQLEXPRESSION2> %prec UPLUS\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_sql_expression2_LEFT_PARENTHESIS(p):
    '''SQLEXPRESSION2 : LEFT_PARENTHESIS SQLEXPRESSION2 RIGHT_PARENTHESIS'''
    nodo = Node('SQL Expression 2')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.add_childrens(Node(p[3]))
    nodo.production = f"<SQLEXPRESSION2> ::= LEFT_PARENTHESIS <SQLEXPRESSION2> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_sql_expression2_LEFT_ACOSD(p):
    '''SQLEXPRESSION2 : ACOSD LEFT_PARENTHESIS SQLEXPRESSION2 RIGHT_PARENTHESIS'''
    nodo = Node('SQL Expression 2')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<SQLEXPRESSION2> ::= ACOSD LEFT_PARENTHESIS <SQLEXPRESSION2> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_sql_expression2_LEFT_ASIND(p):
    '''SQLEXPRESSION2 : ASIND LEFT_PARENTHESIS SQLEXPRESSION2 RIGHT_PARENTHESIS'''
    nodo = Node('SQL Expression 2')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<SQLEXPRESSION2> ::= ASIND LEFT_PARENTHESIS <SQLEXPRESSION2> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_sql_expression2(p):
    '''SQLEXPRESSION2 : SUBSTRING LEFT_PARENTHESIS ID COMMA SQLINTEGER COMMA SQLINTEGER RIGHT_PARENTHESIS
                      | SQLNAME'''
    nodo = Node('SQL Expression 2')
    if len(p) == 9:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        nodo.add_childrens(Node(p[6]))
        nodo.add_childrens(p[7])
        nodo.add_childrens(Node(p[8]))
        nodo.production = f"<SQLEXPRESSION2> ::= SUBSTRING LEFT_PARENTHESIS ID COMMA <SQLINTEGER> COMMA <SQLINTEGER> RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[5].production}"
        nodo.production += f"{p[7].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        nodo.production = f"<SQLEXPRESSION2> ::= <SQLNAME>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo


def p_sql_expression2_SQLINTEGER(p):
    '''SQLEXPRESSION2 : SQLINTEGER'''
    nodo = Node('SQL Expression 2')
    nodo.add_childrens(p[1])
    nodo.production = f"<SQLEXPRESSION2> ::= <SQLINTEGER>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_sql_expression2_TRUE(p):
    '''SQLEXPRESSION2 : TRUE'''
    nodo = Node('SQL Expression 2')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<SQLEXPRESSION2> ::= TRUE\n"
    p[0] = nodo


def p_sql_expression2_FALSE(p):
    '''SQLEXPRESSION2 : FALSE'''
    nodo = Node('SQL Expression 2')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<SQLEXPRESSION2> ::= FALSE\n"
    p[0] = nodo


def p_options_list2_WHERECLAUSE(p):
    '''OPTIONSLIST2 : WHERECLAUSE OPTIONS4
                    | WHERECLAUSE'''
    nodo = Node('Options List 2')
    if (len(p) == 3):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        nodo.production = f"<OPTIONSLIST2> ::= <WHERECLAUSE> <OPTIONS4>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[2].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        nodo.production = f"<OPTIONSLIST2> ::= <WHERECLAUSE>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo


def p_options_list2(p):
    '''OPTIONSLIST2 : OPTIONS4'''
    nodo = Node('Options List 2')
    nodo.add_childrens(p[1])
    nodo.production = f"<OPTIONSLIST2> ::= <OPTIONS4>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_delete_statement(p):
    '''DELETESTATEMENT : DELETE FROM ID OPTIONSLIST SEMICOLON
                       | DELETE FROM ID SEMICOLON '''
    nodo = Node('Delete Statement')
    if (len(p) == 6):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.add_childrens(Node(p[5]))
        nodo.production = f"<DELETESTATEMENT> ::= DELETE FROM ID <OPTIONSLIST> SEMICOLON\n"
        nodo.production += f"{p[4].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        nodo.production = f"<DELETESTATEMENT> ::= DELETE FROM ID SEMICOLON\n"
        p[0] = nodo


def p_options_list_op12W4(p):
    '''OPTIONSLIST : OPTIONS1 OPTIONS2 WHERECLAUSE OPTIONS4'''
    nodo = Node('Options List')
    nodo.add_childrens(p[1])
    nodo.add_childrens(p[2])
    nodo.add_childrens(p[3])
    nodo.add_childrens(p[4])
    nodo.production = f"<OPTIONSLIST> ::= <OPTIONS1> <OPTIONS2> <WHERECLAUSE> <OPTIONS4>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[2].production}"
    nodo.production += f"{p[3].production}"
    nodo.production += f"{p[4].production}"
    p[0] = nodo


def p_options_list_op12W(p):
    '''OPTIONSLIST : OPTIONS1 OPTIONS2 WHERECLAUSE'''
    nodo = Node('Options List')
    nodo.add_childrens(p[1])
    nodo.add_childrens(p[2])
    nodo.add_childrens(p[3])
    nodo.production = f"<OPTIONSLIST> ::= <OPTIONS1> <OPTIONS2> <WHERECLAUSE>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[2].production}"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_options_list_op1W4(p):
    '''OPTIONSLIST : OPTIONS1 WHERECLAUSE OPTIONS4'''
    nodo = Node('Options List')
    nodo.add_childrens(p[1])
    nodo.add_childrens(p[2])
    nodo.add_childrens(p[3])
    nodo.production = f"<OPTIONSLIST> ::= <OPTIONS1> <WHERECLAUSE> <OPTIONS4>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[2].production}"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_options_list_op124(p):
    '''OPTIONSLIST : OPTIONS1 OPTIONS2 OPTIONS4'''
    nodo = Node('Options List')
    nodo.add_childrens(p[1])
    nodo.add_childrens(p[2])
    nodo.add_childrens(p[3])
    nodo.production = f"<OPTIONSLIST> ::= <OPTIONS1> <OPTIONS2> <OPTIONS4>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[2].production}"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_options_list_op2w4(p):
    '''OPTIONSLIST : OPTIONS2 WHERECLAUSE OPTIONS4'''
    nodo = Node('Options List')
    nodo.add_childrens(p[1])
    nodo.add_childrens(p[2])
    nodo.add_childrens(p[3])
    nodo.production = f"<OPTIONSLIST> ::= <OPTIONS2> <WHERECLAUSE> <OPTIONS4>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[2].production}"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_options_list_op12(p):
    '''OPTIONSLIST : OPTIONS1 OPTIONS2'''
    nodo = Node('Options List')
    nodo.add_childrens(p[1])
    nodo.add_childrens(p[2])
    nodo.production = f"<OPTIONSLIST> ::= <OPTIONS1> <OPTIONS2>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_options_list_op1w(p):
    '''OPTIONSLIST : OPTIONS1 WHERECLAUSE'''
    nodo = Node('Options List')
    nodo.add_childrens(p[1])
    nodo.add_childrens(p[2])
    nodo.production = f"<OPTIONSLIST> ::= <OPTIONS1> <WHERECLAUSE>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_options_list_op14(p):
    '''OPTIONSLIST : OPTIONS1 OPTIONS4'''
    nodo = Node('Options List')
    nodo.add_childrens(p[1])
    nodo.add_childrens(p[2])
    nodo.production = f"<OPTIONSLIST> ::= <OPTIONS1> <OPTIONS4>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_options_list_op2w(p):
    '''OPTIONSLIST : OPTIONS2 WHERECLAUSE'''
    nodo = Node('Options List')
    nodo.add_childrens(p[1])
    nodo.add_childrens(p[2])
    nodo.production = f"<OPTIONSLIST> ::= <OPTIONS2> <WHERECLAUSE>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_options_list_op24(p):
    '''OPTIONSLIST : OPTIONS2 OPTIONS4'''
    nodo = Node('Options List')
    nodo.add_childrens(p[1])
    nodo.add_childrens(p[2])
    nodo.production = f"<OPTIONSLIST> ::= <OPTIONS2> <OPTIONS4>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_options_list_opw4(p):
    '''OPTIONSLIST : WHERECLAUSE OPTIONS4'''
    nodo = Node('Options List')
    nodo.add_childrens(p[1])
    nodo.add_childrens(p[2])
    nodo.production = f"<OPTIONSLIST> ::= <WHERECLAUSE> <OPTIONS4>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_options_list_op1(p):
    '''OPTIONSLIST : OPTIONS1'''
    nodo = Node('Options List')
    nodo.add_childrens(p[1])
    nodo.production = f"<OPTIONSLIST> ::= <OPTIONS1>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_options_list_op2(p):
    '''OPTIONSLIST : OPTIONS2'''
    nodo = Node('Options List')
    nodo.add_childrens(p[1])
    nodo.production = f"<OPTIONSLIST> ::= <OPTIONS2>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_options_list_w(p):
    '''OPTIONSLIST : WHERECLAUSE'''
    nodo = Node('Options List')
    nodo.add_childrens(p[1])
    nodo.production = f"<OPTIONSLIST> ::= <WHERECLAUSE>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_options_list_op4(p):
    '''OPTIONSLIST : OPTIONS4'''
    nodo = Node('Options List')
    nodo.add_childrens(p[1])
    nodo.production = f"<OPTIONSLIST> ::= <OPTIONS4>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_options1(p):
    '''OPTIONS1 : ASTERISK SQLALIAS
                | ASTERISK
                | SQLALIAS'''
    nodo = Node('Options 1')
    if(len(p) == 2):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.production = f"<OPTIONS1> ::= ASTERISK <SQLALIAS>\n"
        nodo.production += f"{p[2].production}"
        p[0] = nodo
    else:
        if(p[1] == "*"):
            nodo.add_childrens(Node(p[1]))
            nodo.production = f"<OPTIONS1> ::= ASTERISK\n"
            p[0] = nodo
        else:
            nodo.add_childrens(p[1])
            nodo.production = f"<OPTIONS1> ::= <SQLALIAS>\n"
            nodo.production += f"{p[1].production}"
            p[0] = nodo


def p_options2(p):
    '''OPTIONS2 : USING USINGLIST'''
    nodo = Node('Options 2')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.production = f"<OPTIONS2> ::= USING <USINGLIST>\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_using_list(p):
    '''USINGLIST  : USINGLIST COMMA SQLNAME
                  | SQLNAME'''
    nodo = Node('Using List')
    if(len(p) == 4):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.production = f"<USINGLIST> ::= <USINGLIST> COMMA <SQLNAME>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[3].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        nodo.production = f"<USINGLIST> ::= <SQLNAME>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo

# def p_options3(p):
#     '''OPTIONS3 : WHERE SQLEXPRESSION'''
#     p[0] = Where(p[2]) --------> GRAMATICA SE REPITE


def p_options4(p):
    '''OPTIONS4 : RETURNING RETURNINGLIST'''
    nodo = Node('Options 4')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.production = f"<OPTIONS4> ::= RETURNING <RETURNINGLIST>\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_returning_list(p):
    '''RETURNINGLIST   : ASTERISK
                       | EXPRESSIONRETURNING'''
    nodo = Node('Returning List')
    if p[1] == '*':
        nodo.add_childrens(Node(p[1]))
        nodo.production = f"<RETURNINGLIST> ::= ASTERISK\n"
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        nodo.production = f"<RETURNINGLIST> ::= <EXPRESSIONRETURNING>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo


def p_returning_expression(p):
    '''EXPRESSIONRETURNING : EXPRESSIONRETURNING COMMA SQLEXPRESSION SQLALIAS
                           | SQLEXPRESSION SQLALIAS'''
    nodo = Node('Expression Returning')
    if(len(p) == 5):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(p[4])
        nodo.production = f"<EXPRESSIONRETURNING> ::= <EXPRESSIONRETURNING> COMMA <SQLEXPRESSION> <SQLALIAS>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[3].production}"
        nodo.production += f"{p[4].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        nodo.production = f"<EXPRESSIONRETURNING> ::= <SQLEXPRESSION> <SQLALIAS>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[2].production}"
        p[0] = nodo


def p_insert_statement(p):
    '''INSERTSTATEMENT : INSERT INTO SQLNAME LEFT_PARENTHESIS LISTPARAMSINSERT RIGHT_PARENTHESIS VALUES LEFT_PARENTHESIS LISTVALUESINSERT RIGHT_PARENTHESIS SEMICOLON
                       | INSERT INTO SQLNAME VALUES LEFT_PARENTHESIS LISTVALUESINSERT RIGHT_PARENTHESIS SEMICOLON '''
    nodo = Node('Insert Statement')
    if(len(p) == 12):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        nodo.add_childrens(Node(p[6]))
        nodo.add_childrens(Node(p[7]))
        nodo.add_childrens(Node(p[8]))
        nodo.add_childrens(p[9])
        nodo.add_childrens(Node(p[10]))
        nodo.add_childrens(Node(p[11]))
        nodo.production = f"<INSERTSTATEMENT> ::= INSERT INTO <SQLNAME> LEFT_PARENTHESIS <LISTPARAMSINSERT> RIGHT_PARENTHESIS VALUES LEFT_PARENTHESIS <LISTVALUESINSERT> RIGHT_PARENTHESIS SEMICOLON\n"
        nodo.production += f"{p[3].production}"
        nodo.production += f"{p[5].production}"
        nodo.production += f"{p[9].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(Node(p[5]))
        nodo.add_childrens(p[6])
        nodo.add_childrens(Node(p[7]))
        nodo.add_childrens(Node(p[8]))
        nodo.production = f"<INSERTSTATEMENT> ::= INSERT INTO <SQLNAME> VALUES LEFT_PARENTHESIS <LISTVALUESINSERT> RIGHT_PARENTHESIS SEMICOLON\n"
        nodo.production += f"{p[3].production}"
        nodo.production += f"{p[6].production}"
        p[0] = nodo


def p_list_params_insert(p):
    '''LISTPARAMSINSERT : LISTPARAMSINSERT COMMA SQLNAME
                        | SQLNAME'''
    nodo = Node("List Params Insert")
    if(len(p) == 4):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.production = f"<LISTPARAMSINSERT> ::= <LISTPARAMSINSERT> COMMA <SQLNAME>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[3].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        nodo.production = f"<LISTPARAMSINSERT> ::= <SQLNAME>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo


def p_query_statement(p):
    #  ELEMENTO 0       ELEMENTO 1     ELEMENTO 2      ELEMENTO 3
    '''QUERYSTATEMENT : SELECTSTATEMENT SEMICOLON'''
    nodo = Node('Query Statement')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.production = f"<QUERYSTATEMENT> ::= <SELECTSTATEMENT> SEMICOLON\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_select_statement(p):
    '''SELECTSTATEMENT : SELECTWITHOUTORDER ORDERBYCLAUSE LIMITCLAUSE
                       | SELECTWITHOUTORDER ORDERBYCLAUSE
                       | SELECTWITHOUTORDER'''
    nodo = Node('Select Statement')
    if (len(p) == 4):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        nodo.add_childrens(p[3])
        nodo.production = f"<SELECTSTATEMENT> ::= <SELECTWITHOUTORDER> <ORDERBYCLAUSE> <LIMITCLAUSE>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[2].production}"
        nodo.production += f"{p[3].production}"
        p[0] = nodo
    elif (len(p) == 3):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        nodo.production = f"<SELECTSTATEMENT> ::= <SELECTWITHOUTORDER> <ORDERBYCLAUSE>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[2].production}"
        p[0] = nodo
    elif (len(p) == 2):
        nodo.add_childrens(p[1])
        nodo.production = f"<SELECTSTATEMENT> ::= <SELECTWITHOUTORDER>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo


def p_select_statement_LIMITCLAUSE(p):
    '''SELECTSTATEMENT : SELECTWITHOUTORDER LIMITCLAUSE'''
    nodo = Node('Select Statement')
    nodo.add_childrens(p[1])
    nodo.add_childrens(p[2])
    nodo.production = f"<SELECTSTATEMENT> ::= <SELECTWITHOUTORDER> <LIMITCLAUSE>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_select_without_order(p):
    '''SELECTWITHOUTORDER : SELECTSET
                          | SELECTWITHOUTORDER TYPECOMBINEQUERY ALL SELECTSET
                          | SELECTWITHOUTORDER TYPECOMBINEQUERY SELECTSET'''
    nodo = Node('Select With Out Order')
    if len(p) == 2:
        nodo.add_childrens(p[1])
        nodo.production = f"<SELECTWITHOUTORDER> ::= <SELECTSET>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo
    elif len(p) == 5:
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.production = f"<SELECTWITHOUTORDER> ::= <SELECTWITHOUTORDER> <TYPECOMBINEQUERY> ALL <SELECTSET>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[2].production}"
        nodo.production += f"{p[4].production}"
        p[0] = nodo
    elif len(p) == 4:
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        nodo.add_childrens(p[3])
        nodo.production = f"<SELECTWITHOUTORDER> ::= <SELECTWITHOUTORDER> <TYPECOMBINEQUERY> <SELECTSET>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[2].production}"
        nodo.production += f"{p[3].production}"
        p[0] = nodo


def p_select_set(p):
    '''SELECTSET : SELECTQ 
                 | LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS'''
    nodo = Node('Select Set')
    if len(p) == 2:
        nodo.add_childrens(p[1])
        nodo.production = f"<SELECTSET> ::= <SELECTQ>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo
    elif len(p) == 4:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(Node(p[3]))
        nodo.production = f"<SELECTSET> ::= LEFT_PARENTHESIS <SUBQUERY> RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[2].production}"
        p[0] = nodo


def p_selectq(p):
    '''SELECTQ : SELECT SELECTLIST FROMCLAUSE
               | SELECT SELECTLIST FROMCLAUSE SELECTWHEREAGGREGATE
               | SELECT TYPESELECT SELECTLIST FROMCLAUSE SELECTWHEREAGGREGATE
               | SELECT SELECTLIST'''
    nodo = Node('Select Q')
    if len(p) == 4:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(p[3])
        nodo.production = f"<SELECTQ> ::= SELECT <SELECTLIST> <FROMCLAUSE>\n"
        nodo.production += f"{p[2].production}"
        nodo.production += f"{p[3].production}"
        p[0] = nodo
    elif len(p) == 5:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(p[3])
        nodo.add_childrens(p[4])
        nodo.production = f"<SELECTQ> ::= SELECT <SELECTLIST> <FROMCLAUSE> <SELECTWHEREAGGREGATE>\n"
        nodo.production += f"{p[2].production}"
        nodo.production += f"{p[3].production}"
        nodo.production += f"{p[4].production}"
        p[0] = nodo
    elif len(p) == 6:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(p[3])
        nodo.add_childrens(p[4])
        nodo.add_childrens(p[5])
        nodo.production = f"<SELECTQ> ::= SELECT <TYPESELECT> <SELECTLIST> <FROMCLAUSE> <SELECTWHEREAGGREGATE>\n"
        nodo.production += f"{p[2].production}"
        nodo.production += f"{p[3].production}"
        nodo.production += f"{p[4].production}"
        nodo.production += f"{p[5].production}"
        p[0] = nodo
    elif len(p) == 3:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.production = f"<SELECTQ> ::= SELECT <SELECTLIST>\n"
        nodo.production += f"{p[2].production}"
        p[0] = nodo


def p_selectq_FROMCLAUSE(p):
    '''SELECTQ : SELECT TYPESELECT SELECTLIST FROMCLAUSE'''
    nodo = Node('Select Q')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.add_childrens(p[3])
    nodo.add_childrens(p[4])
    nodo.production = f"<SELECTQ> ::= SELECT <TYPESELECT> <SELECTLIST> <FROMCLAUSE>\n"
    nodo.production += f"{p[2].production}"
    nodo.production += f"{p[3].production}"
    nodo.production += f"{p[4].production}"
    p[0] = nodo


def p_select_list(p):
    '''SELECTLIST : ASTERISK
                  | LISTITEM'''
    nodo = Node('Select List')
    if p[1] == '*':
        nodo.add_childrens(Node(p[1]))
        nodo.production = f"<SELECTLIST> ::= ASTERISK\n"
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        nodo.production = f"<SELECTLIST> ::= <LISTITEM>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo


def p_list_item(p):
    '''LISTITEM : LISTITEM COMMA SELECTITEM
                | SELECTITEM'''
    nodo = Node('List Item')
    if len(p) == 2:
        nodo.add_childrens(p[1])
        nodo.production = f"<LISTITEM> ::= <SELECTITEM>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo
    elif len(p) == 4:
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.production = f"<LISTITEM> ::= <LISTITEM> COMMA <SELECTITEM>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[3].production}"
        p[0] = nodo


def p_select_item(p):
    '''SELECTITEM : SQLEXPRESSION SQLALIAS
                  | SQLEXPRESSION
                  | LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS'''
    nodo = Node('Select Item')
    if (len(p) == 3):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        nodo.production = f"<SELECTITEM> ::= <SQLEXPRESSION> <SQLALIAS>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[2].production}"
        p[0] = nodo
    elif (len(p) == 4):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(Node(p[3]))
        nodo.production = f"<SELECTITEM> ::= LEFT_PARENTHESIS <SUBQUERY> RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[2].production}"
        p[0] = nodo
    elif (len(p) == 2):
        nodo.add_childrens(p[1])
        nodo.production = f"<SELECTITEM> ::= <SQLEXPRESSION>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo


def p_from_clause(p):
    '''FROMCLAUSE : FROM FROMCLAUSELIST'''
    nodo = Node('From Clause')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.production = f"<FROMCLAUSE> ::= FROM <FROMCLAUSELIST>\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_from_clause_list(p):
    '''FROMCLAUSELIST : FROMCLAUSELIST COMMA TABLEREFERENCE
                      | FROMCLAUSELIST COMMA LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS SQLALIAS
                      | FROMCLAUSELIST COMMA LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS
                      | LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS
                      | LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS SQLALIAS
                      | TABLEREFERENCE'''
    nodo = Node('From Clause List')
    if (len(p) == 7):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.add_childrens(Node(p[5]))
        nodo.add_childrens(p[6])
        nodo.production = f"<FROMCLAUSELIST> ::= <FROMCLAUSELIST> COMMA LEFT_PARENTHESIS <SUBQUERY> RIGHT_PARENTHESIS <SQLALIAS>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[4].production}"
        nodo.production += f"{p[6].production}"
        p[0] = nodo
    elif (len(p) == 5):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.production = f"<FROMCLAUSELIST> ::= LEFT_PARENTHESIS <SUBQUERY> RIGHT_PARENTHESIS <SQLALIAS>\n"
        nodo.production += f"{p[2].production}"
        nodo.production += f"{p[4].production}"
        p[0] = nodo
    elif (len(p) == 6):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.add_childrens(Node(p[5]))
        nodo.production = f"<FROMCLAUSELIST> ::= <FROMCLAUSELIST> COMMA LEFT_PARENTHESIS <SUBQUERY> RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[4].production}"
        p[0] = nodo
    elif (len(p) == 4):
        if (p[1] == "("):
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(p[2])
            nodo.add_childrens(Node(p[3]))
            nodo.production = f"<FROMCLAUSELIST> ::= LEFT_PARENTHESIS <SUBQUERY> RIGHT_PARENTHESIS\n"
            nodo.production += f"{p[2].production}"
            p[0] = nodo
        else:
            nodo.add_childrens(p[1])
            nodo.add_childrens(Node(p[2]))
            nodo.add_childrens(p[3])
            nodo.production = f"<FROMCLAUSELIST> ::= <FROMCLAUSELIST> COMMA <TABLEREFERENCE>\n"
            nodo.production += f"{p[1].production}"
            nodo.production += f"{p[3].production}"
            p[0] = nodo
    elif (len(p) == 2):
        nodo.add_childrens(p[1])
        nodo.production = f"<FROMCLAUSELIST> ::= <TABLEREFERENCE>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo


def p_where_aggregate(p):
    '''SELECTWHEREAGGREGATE : WHERECLAUSE  SELECTGROUPHAVING
                            | SELECTGROUPHAVING'''
    nodo = Node('Select Where Aggregate')
    if (len(p) == 3):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        nodo.production = f"<SELECTWHEREAGGREGATE> ::= <WHERECLAUSE> <SELECTGROUPHAVING>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[2].production}"
        p[0] = nodo
    elif (len(p) == 2):
        nodo.add_childrens(p[1])
        nodo.production = f"<SELECTWHEREAGGREGATE> ::= <SELECTGROUPHAVING>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo


def p_where_aggregate_WHERECLAUSE(p):
    '''SELECTWHEREAGGREGATE : WHERECLAUSE'''
    nodo = Node('Select Where Aggregate')
    nodo.add_childrens(p[1])
    nodo.production = f"<SELECTWHEREAGGREGATE> ::= <WHERECLAUSE>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_select_group_having(p):
    '''SELECTGROUPHAVING : GROUPBYCLAUSE
                         | HAVINGCLAUSE GROUPBYCLAUSE'''
    nodo = Node('Select Group Having')
    if (len(p) == 2):
        nodo.add_childrens(p[1])
        nodo.production = f"<SELECTGROUPHAVING> ::= <GROUPBYCLAUSE>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo
    elif (len(p) == 3):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        nodo.production = f"<SELECTGROUPHAVING> ::= <HAVINGCLAUSE> <GROUPBYCLAUSE>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[2].production}"
        p[0] = nodo


def p_select_group_having_GROUPBYCLAUSE(p):
    '''SELECTGROUPHAVING : GROUPBYCLAUSE HAVINGCLAUSE'''
    nodo = Node('Select Group Having')
    nodo.add_childrens(p[1])
    nodo.add_childrens(p[2])
    nodo.production = f"<SELECTGROUPHAVING> ::= <HAVINGCLAUSE> <GROUPBYCLAUSE>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_table_reference(p):
    '''TABLEREFERENCE : SQLNAME SQLALIAS
                      | SQLNAME SQLALIAS JOINLIST
                      | SQLNAME'''
    nodo = Node('Table Reference')
    if (len(p) == 2):
        nodo.add_childrens(p[1])
        nodo.production = f"<TABLEREFERENCE> ::= <SQLNAME>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo
    elif (len(p) == 3):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        nodo.production = f"<TABLEREFERENCE> ::= <SQLNAME> <SQLALIAS>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[2].production}"
        p[0] = nodo
    elif (len(p) == 4):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        nodo.add_childrens(p[3])
        nodo.production = f"<TABLEREFERENCE> ::= <SQLNAME> <SQLALIAS> <JOINLIST>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[2].production}"
        nodo.production += f"{p[3].production}"
        p[0] = nodo


def p_table_reference_JOINLIST(p):
    '''TABLEREFERENCE : SQLNAME JOINLIST'''
    nodo = Node('Table Reference')
    nodo.add_childrens(p[1])
    nodo.add_childrens(p[2])
    nodo.production = f"<TABLEREFERENCE> ::= <SQLNAME> <JOINLIST>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_order_by_clause(p):
    '''ORDERBYCLAUSE : ORDER BY ORDERBYEXPRESSION'''
    nodo = Node('Order By Clause')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.production = f"<ORDERBYCLAUSE> ::= ORDER BY <ORDERBYEXPRESSION>\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_order_by_expression(p):
    '''ORDERBYEXPRESSION : LISTPARAMSINSERT ASC
                         | LISTPARAMSINSERT'''
    nodo = Node('Oder By Expression')
    if (len(p) == 3):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.production = f"<ORDERBYEXPRESSION> ::= <LISTPARAMSINSERT> ASC\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo
    elif (len(p) == 2):
        nodo.add_childrens(p[1])
        nodo.production = f"<ORDERBYEXPRESSION> ::= <LISTPARAMSINSERT>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo


def p_order_by_expression_DESC(p):
    '''ORDERBYEXPRESSION : LISTPARAMSINSERT DESC'''
    nodo = Node('Oder By Expression')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.production = f"<ORDERBYEXPRESSION> ::= <LISTPARAMSINSERT> DESC\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_limit_clause(p):
    '''LIMITCLAUSE : LIMIT LIMITTYPES OFFSET INT_NUMBER
                   | LIMIT LIMITTYPES'''
    nodo = Node('LIMIT CLAUSE')
    if len(p) == 5:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        nodo.production = f"<LIMITCLAUSE> ::= LIMIT <LIMITTYPES> OFFSET INT_NUMBER\n"
        nodo.production += f"{p[2].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.production = f"<LIMITCLAUSE> ::= LIMIT <LIMITTYPES>\n"
        nodo.production += f"{p[2].production}"
        p[0] = nodo


def p_limit_types(p):
    '''LIMITTYPES : INT_NUMBER
                  | ALL'''
    nodo = Node('Limit Types')
    if p[1] == 'ALL':
        nodo.add_childrens(Node(p[1]))
        nodo.production = f"<LIMITTYPES> ::= INT_NUMBER\n"
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.production = f"<LIMITTYPES> ::= ALL\n"
        p[0] = nodo


def p_where_clause(p):
    '''WHERECLAUSE : WHERE SQLEXPRESSION'''
    nodo = Node('Where Clause')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.production = f"<WHERECLAUSE> ::= WHERE <SQLEXPRESSION>\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_group_by_clause(p):
    '''GROUPBYCLAUSE : GROUP BY SQLEXPRESSIONLIST'''
    nodo = Node('Group By Clause')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.production = f"<GROUPBYCLAUSE> ::= GROUP BY <SQLEXPRESSIONLIST>\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_having_clause(p):
    '''HAVINGCLAUSE : HAVING SQLEXPRESSION'''
    nodo = Node('Having Clause')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.production = f"<HAVINGCLAUSE> ::= HAVING <SQLEXPRESSION>\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_join_list(p):
    '''JOINLIST : JOINLIST JOINP
                | JOINP'''
    nodo = Node('Join List')
    if (len(p) == 2):
        nodo.add_childrens(p[1])
        nodo.production = f"<JOINLIST> ::= <JOINP>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo
    elif (len(p) == 3):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        nodo.production = f"<JOINLIST> ::= <JOINLIST> <JOINP>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[2].production}"
        p[0] = nodo


def p_joinp(p):
    '''JOINP : JOINTYPE JOIN TABLEREFERENCE ON SQLEXPRESSION'''
    nodo = Node('JoinP')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.add_childrens(p[5])
    nodo.production = f"<JOINP> ::= <JOINTYPE> JOIN <TABLEREFERENCE> ON <SQLEXPRESSION>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[3].production}"
    nodo.production += f"{p[5].production}"
    p[0] = nodo


def p_join_type(p):
    '''JOINTYPE : INNER
                | LEFT OUTER'''
    nodo = Node('Join Type')
    if (len(p) == 2):
        nodo.add_childrens(Node(p[1]))
        nodo.production = f"<JOINTYPE> ::= INNER\n"
        p[0] = nodo
    elif (len(p) == 3):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.production = f"<JOINTYPE> ::= LEFT OUTER\n"
        p[0] = nodo


def p_join_type_RIGHT(p):
    '''JOINTYPE : RIGHT OUTER'''
    nodo = Node('Join Type')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.production = f"<JOINTYPE> ::= RIGHT OUTER\n"
    p[0] = nodo


def p_join_type_FULL(p):
    '''JOINTYPE : FULL OUTER'''
    nodo = Node('Join Type')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.production = f"<JOINTYPE> ::= FULL OUTER\n"
    p[0] = nodo


def p_sql_expression(p):
    '''SQLEXPRESSION : SQLEXPRESSION OR SQLEXPRESSION
                     | NOT EXISTSORSQLRELATIONALCLAUSE
                     | EXISTSORSQLRELATIONALCLAUSE'''
    nodo = Node('SQL Expression')
    if len(p) == 4:
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.production = f"<SQLEXPRESSION> ::= <SQLEXPRESSION> OR <SQLEXPRESSION>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[3].production}"
        p[0] = nodo
    elif len(p) == 3:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.production = f"<SQLEXPRESSION> ::= OR <EXISTSORSQLRELATIONALCLAUSE>\n"
        nodo.production += f"{p[2].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        nodo.production = f"<SQLEXPRESSION> ::= <EXISTSORSQLRELATIONALCLAUSE>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo


def p_sql_expression_AND(p):
    '''SQLEXPRESSION : SQLEXPRESSION AND SQLEXPRESSION'''
    nodo = Node('SQL Expression')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.production = f"<SQLEXPRESSION> ::= <SQLEXPRESSION> AND <SQLEXPRESSION>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_exits_or_relational_clause(p):
    '''EXISTSORSQLRELATIONALCLAUSE : EXISTSCLAUSE'''
    nodo = Node('Exists Or SQL Relational Clause')
    nodo.add_childrens(p[1])
    nodo.production = f"<EXISTSORSQLRELATIONALCLAUSE> ::= <EXISTSCLAUSE>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_exits_or_relational_clause_SQLRELATIONALEXPRESSION(p):
    '''EXISTSORSQLRELATIONALCLAUSE : SQLRELATIONALEXPRESSION'''
    nodo = Node('Exists Or SQL Relational Clause')
    nodo.add_childrens(p[1])
    nodo.production = f"<EXISTSORSQLRELATIONALCLAUSE> ::= <SQLRELATIONALEXPRESSION>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_exists_clause(p):
    '''EXISTSCLAUSE : EXISTS LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS'''
    nodo = Node('Exists Clause')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<EXISTSCLAUSE> ::= EXISTS LEFT_PARENTHESIS <SUBQUERY> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_sql_relational_expression(p):
    '''SQLRELATIONALEXPRESSION : SQLSIMPLEEXPRESSION RELOP SQLSIMPLEEXPRESSION
                               | SQLSIMPLEEXPRESSION SQLINCLAUSE
                               | SQLSIMPLEEXPRESSION'''
    nodo = Node('SQL Relational Expression')
    if (len(p) == 3):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        nodo.production = f"<SQLRELATIONALEXPRESSION> ::= <SQLSIMPLEEXPRESSION> <SQLINCLAUSE>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[2].production}"
        p[0] = nodo
    elif (len(p) == 4):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        nodo.add_childrens(p[3])
        nodo.production = f"<SQLRELATIONALEXPRESSION> ::= <SQLSIMPLEEXPRESSION> <RELOP> <SQLSIMPLEEXPRESSION>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[2].production}"
        nodo.production += f"{p[3].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        nodo.production = f"<SQLRELATIONALEXPRESSION> ::= <SQLSIMPLEEXPRESSION>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo


def p_sql_relational_expression_SQLBETWEENCLAUSE(p):
    '''SQLRELATIONALEXPRESSION : SQLSIMPLEEXPRESSION SQLBETWEENCLAUSE'''
    nodo = Node('SQL Relational Expression')
    nodo.add_childrens(p[1])
    nodo.add_childrens(p[2])
    nodo.production = f"<SQLRELATIONALEXPRESSION> ::= <SQLSIMPLEEXPRESSION> <SQLBETWEENCLAUSE>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_sql_relational_expression_SQLLIKECLAUSE(p):
    '''SQLRELATIONALEXPRESSION : SQLSIMPLEEXPRESSION SQLLIKECLAUSE'''
    nodo = Node('SQL Relational Expression')
    nodo.add_childrens(p[1])
    nodo.add_childrens(p[2])
    nodo.production = f"<SQLRELATIONALEXPRESSION> ::= <SQLSIMPLEEXPRESSION> <SQLLIKECLAUSE>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_sql_relational_expression_SQLISCLAUSE(p):
    '''SQLRELATIONALEXPRESSION : SQLSIMPLEEXPRESSION SQLISCLAUSE'''
    nodo = Node('SQL Relational Expression')
    nodo.add_childrens(p[1])
    nodo.add_childrens(p[2])
    nodo.production = f"<SQLRELATIONALEXPRESSION> ::= <SQLSIMPLEEXPRESSION> <SQLISCLAUSE>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_sql_in_clause(p):
    '''SQLINCLAUSE  : NOT IN LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS
                    | IN LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS'''
    nodo = Node('SQL In Clause')
    if (len(p) == 6):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.add_childrens(Node(p[5]))
        nodo.production = f"<SQLINCLAUSE> ::= NOT IN LEFT_PARENTHESIS <SUBQUERY> RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[4].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.production = f"<SQLINCLAUSE> ::= IN LEFT_PARENTHESIS <SUBQUERY> RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[3].production}"
        p[0] = nodo


def p_sql_in_clause_listain(p):
    '''SQLINCLAUSE  : NOT IN LEFT_PARENTHESIS listain RIGHT_PARENTHESIS
                    | IN LEFT_PARENTHESIS listain RIGHT_PARENTHESIS'''
    nodo = Node('SQL In Clause')
    if (len(p) == 6):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.add_childrens(Node(p[5]))
        nodo.production = f"<SQLINCLAUSE> ::= NOT IN LEFT_PARENTHESIS <listain> RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[4].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.production = f"<SQLINCLAUSE> ::= IN LEFT_PARENTHESIS <listain> RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[3].production}"
        p[0] = nodo


def p_lista_in(p):
    '''listain : listain COMMA SQLSIMPLEEXPRESSION
               | SQLSIMPLEEXPRESSION 
    '''
    nodo = Node('List In')
    if len(p) == 4:
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.production = f"<listain> ::= <listain> COMMA <SQLSIMPLEEXPRESSION>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[3].production}"
        p[0] = nodo

    else:
        nodo.add_childrens(p[1])
        nodo.production = f"<listain> ::= <SQLSIMPLEEXPRESSION>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo


def p_sql_between_clause(p):
    '''SQLBETWEENCLAUSE : NOT BETWEEN SQLSIMPLEEXPRESSION AND SQLSIMPLEEXPRESSION
                        | NOT BETWEEN SYMMETRIC SQLSIMPLEEXPRESSION AND SQLSIMPLEEXPRESSION
                        | BETWEEN SQLSIMPLEEXPRESSION AND SQLSIMPLEEXPRESSION 
                        | BETWEEN SYMMETRIC SQLSIMPLEEXPRESSION AND SQLSIMPLEEXPRESSION '''
    nodo = Node('SQL Between Clause')
    if (len(p) == 6):
        if (p[3] == 'SYMMETRIC'):
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(Node(p[2]))
            nodo.add_childrens(p[3])
            nodo.add_childrens(Node(p[4]))
            nodo.add_childrens(p[5])
            nodo.production = f"<SQLBETWEENCLAUSE> ::= BETWEEN SYMMETRIC <SQLSIMPLEEXPRESSION> AND <SQLSIMPLEEXPRESSION>\n"
            nodo.production += f"{p[3].production}"
            nodo.production += f"{p[5].production}"
            p[0] = nodo
        else:
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(Node(p[2]))
            nodo.add_childrens(p[3])
            nodo.add_childrens(Node(p[4]))
            nodo.add_childrens(p[5])
            nodo.production = f"<SQLBETWEENCLAUSE> ::= NOT BETWEEN <SQLSIMPLEEXPRESSION> AND <SQLSIMPLEEXPRESSION>\n"
            nodo.production += f"{p[3].production}"
            nodo.production += f"{p[5].production}"
            p[0] = nodo
    elif (len(p) == 5):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.production = f"<SQLBETWEENCLAUSE> ::= BETWEEN <SQLSIMPLEEXPRESSION> AND <SQLSIMPLEEXPRESSION>\n"
        nodo.production += f"{p[2].production}"
        nodo.production += f"{p[4].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.add_childrens(Node(p[5]))
        nodo.add_childrens(p[6])
        nodo.production = f"<SQLBETWEENCLAUSE> ::= NOT BETWEEN SYMMETRIC <SQLSIMPLEEXPRESSION> AND <SQLSIMPLEEXPRESSION>\n"
        nodo.production += f"{p[4].production}"
        nodo.production += f"{p[6].production}"
        p[0] = nodo


def p_sql_like_clause(p):
    '''SQLLIKECLAUSE  : NOT LIKE SQLSIMPLEEXPRESSION
                      | LIKE SQLSIMPLEEXPRESSION'''
    nodo = Node('SQL Like Clause')
    if (len(p) == 4):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.production = f"<SQLLIKECLAUSE> ::= NOT LIKE <SQLSIMPLEEXPRESSION>\n"
        nodo.production += f"{p[3].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.production = f"<SQLLIKECLAUSE> ::= LIKE <SQLSIMPLEEXPRESSION>\n"
        nodo.production += f"{p[2].production}"
        p[0] = nodo


def p_sql_is_clause(p):
    '''SQLISCLAUSE : IS NULL
                   | ISNULL
                   | IS NOT TRUE
                   | IS NOT DISTINCT FROM SQLNAME
                   | IS DISTINCT FROM SQLNAME'''
    nodo = Node('SQL Is Clause')
    if len(p) == 2:
        nodo.add_childrens(Node(p[1]))
        nodo.production = f"<SQLISCLAUSE> ::= ISNULL\n"
        p[0] = nodo
    elif len(p) == 3:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.production = f"<SQLISCLAUSE> ::= IS NULL\n"
        p[0] = nodo
    elif len(p) == 4:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.production = f"<SQLISCLAUSE> ::= IS NOT TRUE\n"
        p[0] = nodo
    elif len(p) == 5:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.production = f"<SQLISCLAUSE> ::= IS DISTINCT FROM <SQLNAME>\n"
        nodo.production += f"{p[4].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        nodo.production = f"<SQLISCLAUSE> ::= IS NOT DISTINCT FROM <SQLNAME>\n"
        nodo.production += f"{p[5].production}"
        p[0] = nodo


def p_sql_is_clause_2(p):
    '''SQLISCLAUSE : IS NOT NULL
                   | NOTNULL
                   | IS TRUE'''
    nodo = Node('SQL Is Clause')
    if len(p) == 2:
        nodo.add_childrens(Node(p[1]))
        nodo.production = f"<SQLISCLAUSE> ::= NOTNULL\n"
        p[0] = nodo
    elif len(p) == 3:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.production = f"<SQLISCLAUSE> ::= IS TRUE\n"
        p[0] = nodo
    elif len(p) == 4:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.production = f"<SQLISCLAUSE> ::= IS NOT NULL\n"
        p[0] = nodo


def p_sql_is_clause_3(p):
    '''SQLISCLAUSE : IS FALSE
                   | IS NOT FALSE'''
    nodo = Node('SQL Is Clause')
    if len(p) == 3:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.production = f"<SQLISCLAUSE> ::= IS FALSE\n"
        p[0] = nodo
    elif len(p) == 4:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.production = f"<SQLISCLAUSE> ::= IS NOT FALSE\n"
        p[0] = nodo


def p_sql_is_clause_4(p):
    '''SQLISCLAUSE : IS UNKNOWN
                   | IS NOT UNKNOWN'''
    nodo = Node('SQL Is Clause')
    if len(p) == 3:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.production = f"<SQLISCLAUSE> ::= IS UNKNOWN\n"
        p[0] = nodo
    elif len(p) == 4:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.production = f"<SQLISCLAUSE> ::= IS NOT UNKNOWN\n"
        p[0] = nodo


def p_sql_simple_expression_PLUS(p):
    '''SQLSIMPLEEXPRESSION : SQLSIMPLEEXPRESSION PLUS SQLSIMPLEEXPRESSION'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= <SQLSIMPLEEXPRESSION> PLUS <SQLSIMPLEEXPRESSION>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_sql_simple_expression_REST(p):
    '''SQLSIMPLEEXPRESSION : SQLSIMPLEEXPRESSION REST SQLSIMPLEEXPRESSION'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= <SQLSIMPLEEXPRESSION> REST <SQLSIMPLEEXPRESSION>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_sql_simple_expression_ASTERISK(p):
    '''SQLSIMPLEEXPRESSION : SQLSIMPLEEXPRESSION ASTERISK SQLSIMPLEEXPRESSION'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= <SQLSIMPLEEXPRESSION> ASTERISK <SQLSIMPLEEXPRESSION>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_sql_simple_expression_DIVISION(p):
    '''SQLSIMPLEEXPRESSION : SQLSIMPLEEXPRESSION DIVISION SQLSIMPLEEXPRESSION'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= <SQLSIMPLEEXPRESSION> DIVISION <SQLSIMPLEEXPRESSION>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_sql_simple_expression_EXPONENT(p):
    '''SQLSIMPLEEXPRESSION : SQLSIMPLEEXPRESSION EXPONENT SQLSIMPLEEXPRESSION'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= <SQLSIMPLEEXPRESSION> EXPONENT <SQLSIMPLEEXPRESSION>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_sql_simple_expression_MODULAR(p):
    '''SQLSIMPLEEXPRESSION : SQLSIMPLEEXPRESSION MODULAR SQLSIMPLEEXPRESSION'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= <SQLSIMPLEEXPRESSION> MODULAR <SQLSIMPLEEXPRESSION>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_sql_simple_expression_uREST(p):
    '''SQLSIMPLEEXPRESSION : REST SQLSIMPLEEXPRESSION %prec UREST'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= REST <SQLSIMPLEEXPRESSION> %prec UREST\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_sql_simple_expression_uPLUS(p):
    '''SQLSIMPLEEXPRESSION : PLUS SQLSIMPLEEXPRESSION %prec UPLUS'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= PLUS <SQLSIMPLEEXPRESSION> %prec UPLUS\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_sql_simple_expression_BITWISE_SHIFT_RIGHT(p):
    '''SQLSIMPLEEXPRESSION : SQLSIMPLEEXPRESSION BITWISE_SHIFT_RIGHT SQLSIMPLEEXPRESSION'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= <SQLSIMPLEEXPRESSION> BITWISE_SHIFT_RIGHT <SQLSIMPLEEXPRESSION>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_sql_simple_expression_BITWISE_SHIFT_LEFT(p):
    '''SQLSIMPLEEXPRESSION : SQLSIMPLEEXPRESSION BITWISE_SHIFT_LEFT SQLSIMPLEEXPRESSION'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= <SQLSIMPLEEXPRESSION> BITWISE_SHIFT_LEFT <SQLSIMPLEEXPRESSION>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_sql_simple_expression_BITWISE_AND(p):
    '''SQLSIMPLEEXPRESSION : SQLSIMPLEEXPRESSION BITWISE_AND SQLSIMPLEEXPRESSION'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= <SQLSIMPLEEXPRESSION> BITWISE_AND <SQLSIMPLEEXPRESSION>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_sql_simple_expression_BITWISE_OR(p):
    '''SQLSIMPLEEXPRESSION : SQLSIMPLEEXPRESSION BITWISE_OR SQLSIMPLEEXPRESSION'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= <SQLSIMPLEEXPRESSION> BITWISE_OR <SQLSIMPLEEXPRESSION>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_sql_simple_expression_BITWISE_XOR(p):
    '''SQLSIMPLEEXPRESSION : SQLSIMPLEEXPRESSION BITWISE_XOR SQLSIMPLEEXPRESSION'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= <SQLSIMPLEEXPRESSION> BITWISE_XOR <SQLSIMPLEEXPRESSION>\n"
    nodo.production += f"{p[1].production}"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_sql_simple_expression_BITWISE_NOT(p):
    '''SQLSIMPLEEXPRESSION : BITWISE_NOT SQLSIMPLEEXPRESSION %prec UREST'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= BITWISE_NOT <SQLSIMPLEEXPRESSION> %prec UREST\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_sql_simple_expression_SQLEXPRESSION(p):
    '''SQLSIMPLEEXPRESSION : LEFT_PARENTHESIS SQLEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.add_childrens(Node(p[3]))
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= LEFT_PARENTHESIS <SQLEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_sql_simple_expression_AGGREGATEFUNCTIONS(p):
    '''SQLSIMPLEEXPRESSION : AGGREGATEFUNCTIONS'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(p[1])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= <AGGREGATEFUNCTIONS>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_sql_simple_expression_GREATESTORLEAST(p):
    '''SQLSIMPLEEXPRESSION : GREATESTORLEAST'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(p[1])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= <GREATESTORLEAST>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_sql_simple_expression_EXPRESSIONSTIME(p):
    '''SQLSIMPLEEXPRESSION : EXPRESSIONSTIME'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(p[1])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= <EXPRESSIONSTIME>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_sql_simple_expression_SQUARE_ROOT(p):
    '''SQLSIMPLEEXPRESSION : SQUARE_ROOT SQLSIMPLEEXPRESSION'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= SQUARE_ROOT <SQLSIMPLEEXPRESSION>\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_sql_simple_expression_CUBE_ROOT(p):
    '''SQLSIMPLEEXPRESSION : CUBE_ROOT SQLSIMPLEEXPRESSION'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= CUBE_ROOT <SQLSIMPLEEXPRESSION>\n"
    nodo.production += f"{p[2].production}"
    p[0] = nodo


def p_sql_simple_expression_MATHEMATICALFUNCTIONS(p):
    '''SQLSIMPLEEXPRESSION : MATHEMATICALFUNCTIONS'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(p[1])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= <MATHEMATICALFUNCTIONS>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_sql_simple_expression_CASECLAUSE(p):
    '''SQLSIMPLEEXPRESSION : CASECLAUSE'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(p[1])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= <CASECLAUSE>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_sql_simple_expression_BINARY_STRING_FUNCTIONS(p):
    '''SQLSIMPLEEXPRESSION : BINARY_STRING_FUNCTIONS'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(p[1])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= <BINARY_STRING_FUNCTIONS>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_sql_simple_expression_TRIGONOMETRIC_FUNCTIONS(p):
    '''SQLSIMPLEEXPRESSION : TRIGONOMETRIC_FUNCTIONS'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(p[1])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= <TRIGONOMETRIC_FUNCTIONS>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_sql_simple_expression_SQLINTEGER(p):
    '''SQLSIMPLEEXPRESSION : SQLINTEGER'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(p[1])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= <SQLINTEGER>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_sql_simple_expression_OBJECTREFERENCE(p):
    '''SQLSIMPLEEXPRESSION : OBJECTREFERENCE'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(p[1])
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= <OBJECTREFERENCE>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_sql_simple_expression_NULL(p):
    '''SQLSIMPLEEXPRESSION : NULL'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= NULL\n"
    p[0] = nodo


def p_sql_simple_expression_TRUE(p):
    '''SQLSIMPLEEXPRESSION : TRUE'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= TRUE\n"
    p[0] = nodo


def p_sql_simple_expression(p):
    '''SQLSIMPLEEXPRESSION : FALSE'''
    nodo = Node('SQL Simple Expression')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<SQLSIMPLEEXPRESSION> ::= FALSE\n"
    p[0] = nodo


def p_sql_expression_list(p):
    '''SQLEXPRESSIONLIST : SQLEXPRESSIONLIST COMMA SQLEXPRESSION
                         | SQLEXPRESSION'''
    nodo = Node('SQL Expression List')
    if (len(p) == 4):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.production = f"<SQLEXPRESSIONLIST> ::= <SQLEXPRESSIONLIST> COMMA <SQLEXPRESSION>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[3].production}"
        p[0] = nodo
    elif (len(p) == 2):
        nodo.add_childrens(p[1])
        nodo.production = f"<SQLEXPRESSIONLIST> ::= <SQLEXPRESSION>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo


def p_mathematical_functions_ABS(p):
    '''MATHEMATICALFUNCTIONS : ABS LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Mathematical Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<MATHEMATICALFUNCTIONS> ::= ABS LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_mathematical_functions_CBRT(p):
    '''MATHEMATICALFUNCTIONS : CBRT LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Mathematical Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<MATHEMATICALFUNCTIONS> ::= CBRT LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_mathematical_functions_CEIL(p):
    '''MATHEMATICALFUNCTIONS : CEIL LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Mathematical Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<MATHEMATICALFUNCTIONS> ::= CEIL LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_mathematical_functions_CEILING(p):
    '''MATHEMATICALFUNCTIONS : CEILING LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Mathematical Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<MATHEMATICALFUNCTIONS> ::= CEILING LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_mathematical_functions_DEGREES(p):
    '''MATHEMATICALFUNCTIONS : DEGREES LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Mathematical Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<MATHEMATICALFUNCTIONS> ::= DEGREES LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_mathematical_functions_DIV(p):
    '''MATHEMATICALFUNCTIONS : DIV LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Mathematical Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.add_childrens(p[5])
    nodo.add_childrens(Node(p[6]))
    nodo.production = f"<MATHEMATICALFUNCTIONS> ::= DIV LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> COMMA <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    nodo.production += f"{p[5].production}"
    p[0] = nodo


def p_mathematical_functions_EXP(p):
    '''MATHEMATICALFUNCTIONS : EXP LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Mathematical Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<MATHEMATICALFUNCTIONS> ::= EXP LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_mathematical_functions_FACTORIAL(p):
    '''MATHEMATICALFUNCTIONS : FACTORIAL LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Mathematical Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<MATHEMATICALFUNCTIONS> ::= FACTORIAL LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_mathematical_functions_FLOOR(p):
    '''MATHEMATICALFUNCTIONS : FLOOR LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Mathematical Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<MATHEMATICALFUNCTIONS> ::= FLOOR LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_mathematical_functions_GCD(p):
    '''MATHEMATICALFUNCTIONS : GCD LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Mathematical Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.add_childrens(p[5])
    nodo.add_childrens(Node(p[6]))
    nodo.production = f"<MATHEMATICALFUNCTIONS> ::= GCD LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> COMMA <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    nodo.production += f"{p[5].production}"
    p[0] = nodo


def p_mathematical_functions_LN(p):
    '''MATHEMATICALFUNCTIONS : LN LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Mathematical Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<MATHEMATICALFUNCTIONS> ::= LN LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_mathematical_functions_LOG(p):
    '''MATHEMATICALFUNCTIONS : LOG LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Mathematical Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<MATHEMATICALFUNCTIONS> ::= LOG LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_mathematical_functions_MOD(p):
    '''MATHEMATICALFUNCTIONS : MOD LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Mathematical Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.add_childrens(p[5])
    nodo.add_childrens(Node(p[6]))
    nodo.production = f"<MATHEMATICALFUNCTIONS> ::= MOD LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> COMMA <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    nodo.production += f"{p[5].production}"
    p[0] = nodo


def p_mathematical_functions_POWER(p):
    '''MATHEMATICALFUNCTIONS : POWER LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Mathematical Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.add_childrens(p[5])
    nodo.add_childrens(Node(p[6]))
    nodo.production = f"<MATHEMATICALFUNCTIONS> ::= POWER LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> COMMA <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    nodo.production += f"{p[5].production}"
    p[0] = nodo


def p_mathematical_functions_RADIANS(p):
    '''MATHEMATICALFUNCTIONS : RADIANS LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Mathematical Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<MATHEMATICALFUNCTIONS> ::= RADIANS LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_mathematical_functions_SIGN(p):
    '''MATHEMATICALFUNCTIONS : SIGN LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Mathematical Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<MATHEMATICALFUNCTIONS> ::= SIGN LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_mathematical_functions_SQRT(p):
    '''MATHEMATICALFUNCTIONS : SQRT LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Mathematical Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<MATHEMATICALFUNCTIONS> ::= SQRT LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_mathematical_functions_RANDOM(p):
    '''MATHEMATICALFUNCTIONS : RANDOM LEFT_PARENTHESIS RIGHT_PARENTHESIS'''
    nodo = Node('Mathematical Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(Node(p[3]))
    nodo.production = f"<MATHEMATICALFUNCTIONS> ::= RANDOM LEFT_PARENTHESIS RIGHT_PARENTHESIS\n"
    p[0] = nodo


def p_mathematical_functions(p):
    '''MATHEMATICALFUNCTIONS : PI LEFT_PARENTHESIS RIGHT_PARENTHESIS
                             | ROUND LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | WIDTH_BUCKET LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | TRUNC LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Mathematical Functions')
    if (len(p) == 5):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.production = f"<MATHEMATICALFUNCTIONS> ::= TRUNC LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[3].production}"
        p[0] = nodo
    elif len(p) == 4:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.production = f"<MATHEMATICALFUNCTIONS> ::= PI LEFT_PARENTHESIS RIGHT_PARENTHESIS\n"
        p[0] = nodo
    elif (len(p) == 7):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        nodo.add_childrens(Node(p[6]))
        nodo.production = f"<MATHEMATICALFUNCTIONS> ::= ROUND LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> COMMA <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[3].production}"
        nodo.production += f"{p[5].production}"
        p[0] = nodo
    elif (len(p) == 11):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        nodo.add_childrens(Node(p[6]))
        nodo.add_childrens(p[7])
        nodo.add_childrens(Node(p[8]))
        nodo.add_childrens(p[9])
        nodo.add_childrens(Node(p[10]))
        nodo.production = f"<MATHEMATICALFUNCTIONS> ::= WIDTH_BUCKET LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> COMMA <SQLSIMPLEEXPRESSION> COMMA <SQLSIMPLEEXPRESSION> COMMA <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[3].production}"
        nodo.production += f"{p[5].production}"
        nodo.production += f"{p[7].production}"
        nodo.production += f"{p[9].production}"
        p[0] = nodo


def p_binary_string_functions(p):
    '''BINARY_STRING_FUNCTIONS : LENGTH LEFT_PARENTHESIS SQLNAME RIGHT_PARENTHESIS
                               | SUBSTRING LEFT_PARENTHESIS SQLNAME COMMA SQLINTEGER COMMA SQLINTEGER RIGHT_PARENTHESIS
                               | CONVERT LEFT_PARENTHESIS SQLNAME AS DATE RIGHT_PARENTHESIS'''
    nodo = Node('Binary String Functions')
    if len(p) == 5:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.production = f"<BINARY_STRING_FUNCTIONS> ::= LENGTH LEFT_PARENTHESIS <SQLNAME> RIGHT_PARENTHESIS\n"
        p[0] = nodo
    elif len(p) == 9:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        nodo.add_childrens(Node(p[6]))
        nodo.add_childrens(p[7])
        nodo.add_childrens(Node(p[8]))
        nodo.production = f"<BINARY_STRING_FUNCTIONS> ::= SUBSTRING LEFT_PARENTHESIS <SQLNAME> COMMA <SQLINTEGER> COMMA <SQLINTEGER> RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[3].production}"
        p[0] = nodo
    elif len(p) == 7:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(Node(p[5]))
        nodo.add_childrens(Node(p[6]))
        nodo.production = f"<BINARY_STRING_FUNCTIONS> ::= CONVERT LEFT_PARENTHESIS <SQLNAME> AS DATE RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[3].production}"
        p[0] = nodo


def p_binary_string_functions_TRIM(p):
    '''BINARY_STRING_FUNCTIONS : TRIM LEFT_PARENTHESIS SQLNAME RIGHT_PARENTHESIS
                               | SUBSTR LEFT_PARENTHESIS SQLNAME COMMA SQLINTEGER COMMA SQLINTEGER RIGHT_PARENTHESIS
                               | CONVERT LEFT_PARENTHESIS SQLNAME AS INTEGER RIGHT_PARENTHESIS'''
    nodo = Node('Binary String Functions')
    if len(p) == 5:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.production = f"<BINARY_STRING_FUNCTIONS> ::= TRIM LEFT_PARENTHESIS <SQLNAME> RIGHT_PARENTHESIS\n"
        p[0] = nodo
    elif len(p) == 9:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        nodo.add_childrens(Node(p[6]))
        nodo.add_childrens(p[7])
        nodo.add_childrens(Node(p[8]))
        nodo.production = f"<BINARY_STRING_FUNCTIONS> ::= SUBSTR LEFT_PARENTHESIS <SQLNAME> COMMA <SQLINTEGER> COMMA <SQLINTEGER> RIGHT_PARENTHESIS\n"
        p[0] = nodo
    elif len(p) == 7:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(Node(p[5]))
        nodo.add_childrens(Node(p[6]))
        nodo.production = f"<BINARY_STRING_FUNCTIONS> ::= CONVERT LEFT_PARENTHESIS <SQLNAME> AS INTEGER RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[3].production}"
        p[0] = nodo


def p_binary_string_functions_MD5(p):
    '''BINARY_STRING_FUNCTIONS : MD5 LEFT_PARENTHESIS SQLNAME RIGHT_PARENTHESIS
                               | DECODE LEFT_PARENTHESIS SQLNAME COMMA SQLNAME RIGHT_PARENTHESIS'''
    nodo = Node('Binary String Functions')
    if len(p) == 5:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.production = f"<BINARY_STRING_FUNCTIONS> ::= MD5 LEFT_PARENTHESIS <SQLNAME> RIGHT_PARENTHESIS\n"
        p[0] = nodo
    elif len(p) == 7:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        nodo.add_childrens(Node(p[6]))
        nodo.production = f"<BINARY_STRING_FUNCTIONS> ::= DECODE LEFT_PARENTHESIS <SQLNAME> COMMA <SQLNAME> RIGHT_PARENTHESIS\n"
        p[0] = nodo


def p_binary_string_functions_SHA256(p):
    '''BINARY_STRING_FUNCTIONS : SHA256 LEFT_PARENTHESIS SQLNAME RIGHT_PARENTHESIS'''
    nodo = Node('Binary String Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<BINARY_STRING_FUNCTIONS> ::= SHA256 LEFT_PARENTHESIS <SQLNAME> RIGHT_PARENTHESIS\n"
    p[0] = nodo


def p_greatest(p):
    '''GREATESTORLEAST : GREATEST LEFT_PARENTHESIS LISTVALUESINSERT RIGHT_PARENTHESIS'''
    nodo = Node('Greatest or Least')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<GREATESTORLEAST> ::= GREATEST LEFT_PARENTHESIS <LISTVALUESINSERT> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_least(p):
    '''GREATESTORLEAST : LEAST LEFT_PARENTHESIS LISTVALUESINSERT RIGHT_PARENTHESIS'''
    nodo = Node('Greatest or Least')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<GREATESTORLEAST> ::= LEAST LEFT_PARENTHESIS <LISTVALUESINSERT> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_case_clause(p):
    '''CASECLAUSE : CASE CASECLAUSELIST END ID
                  | CASE CASECLAUSELIST ELSE SQLSIMPLEEXPRESSION END ID'''
    nodo = Node('Case Clause')
    if(len(p) == 5):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        nodo.production = f"<CASECLAUSE> ::= CASE <CASECLAUSELIST> END ID\n"
        nodo.production += f"{p[2].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.add_childrens(Node(p[5]))
        nodo.add_childrens(Node(p[6]))
        nodo.production = f"<CASECLAUSE> ::= CASE <CASECLAUSELIST> ELSE <SQLSIMPLEEXPRESSION> END ID\n"
        nodo.production += f"{p[2].production}"
        nodo.production += f"{p[4].production}"
        p[0] = nodo


def p_case_clause_list(p):
    '''CASECLAUSELIST : CASECLAUSELIST WHEN SQLSIMPLEEXPRESSION RELOP SQLSIMPLEEXPRESSION THEN SQLSIMPLEEXPRESSION
                      | CASECLAUSELIST WHEN SQLSIMPLEEXPRESSION THEN SQLSIMPLEEXPRESSION
                      | WHEN SQLSIMPLEEXPRESSION RELOP SQLSIMPLEEXPRESSION THEN SQLSIMPLEEXPRESSION
                      | WHEN SQLSIMPLEEXPRESSION THEN SQLSIMPLEEXPRESSION'''
    nodo = Node('CASECLAUSELIST')
    if (len(p) == 8):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(p[4])
        nodo.add_childrens(p[5])
        nodo.add_childrens(Node(p[6]))
        nodo.add_childrens(p[7])
        nodo.production = f"<CASECLAUSELIST> ::= <CASECLAUSELIST> WHEN <SQLSIMPLEEXPRESSION> <RELOP> <SQLSIMPLEEXPRESSION> THEN <SQLSIMPLEEXPRESSION>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[3].production}"
        nodo.production += f"{p[4].production}"
        nodo.production += f"{p[5].production}"
        nodo.production += f"{p[7].production}"
        p[0] = nodo
    elif (len(p) == 7):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(p[3])
        nodo.add_childrens(p[4])
        nodo.add_childrens(Node(p[5]))
        nodo.add_childrens(p[6])
        nodo.production = f"<CASECLAUSELIST> ::= WHEN <SQLSIMPLEEXPRESSION> <RELOP> <SQLSIMPLEEXPRESSION> THEN <SQLSIMPLEEXPRESSION>\n"
        nodo.production += f"{p[2].production}"
        nodo.production += f"{p[3].production}"
        nodo.production += f"{p[4].production}"
        nodo.production += f"{p[6].production}"
        p[0] = nodo
    elif (len(p) == 6):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        nodo.production = f"<CASECLAUSELIST> ::= <CASECLAUSELIST> WHEN <SQLSIMPLEEXPRESSION> THEN <SQLSIMPLEEXPRESSION>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[3].production}"
        nodo.production += f"{p[5].production}"
        p[0] = nodo
    else:  # len = 5
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.production = f"<CASECLAUSELIST> ::= WHEN <SQLSIMPLEEXPRESSION> THEN <SQLSIMPLEEXPRESSION>\n"
        nodo.production += f"{p[2].production}"
        nodo.production += f"{p[4].production}"
        p[0] = nodo


def p_trigonometric_functions_ACOS(p):
    '''TRIGONOMETRIC_FUNCTIONS : ACOS LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | ATAN2 LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Trigonometric Functions')
    if (len(p) == 5):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.production = f"<TRIGONOMETRIC_FUNCTIONS> ::= ACOS LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[3].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        nodo.add_childrens(Node(p[6]))
        nodo.production = f"<TRIGONOMETRIC_FUNCTIONS> ::= ATAN2 LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> COMMA <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[3].production}"
        nodo.production += f"{p[5].production}"
        p[0] = nodo


def p_trigonometric_functions_ACOSD(p):
    '''TRIGONOMETRIC_FUNCTIONS : ACOSD LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | ATAN2D LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Trigonometric Functions')
    if (len(p) == 5):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.production = f"<TRIGONOMETRIC_FUNCTIONS> ::= ACOSD LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[3].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        nodo.add_childrens(Node(p[6]))
        nodo.production = f"<TRIGONOMETRIC_FUNCTIONS> ::= ATAN2D LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> COMMA <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[3].production}"
        nodo.production += f"{p[5].production}"
        p[0] = nodo


def p_trigonometric_functions_ASIN(p):
    '''TRIGONOMETRIC_FUNCTIONS : ASIN LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Trigonometric Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<TRIGONOMETRIC_FUNCTIONS> ::= ASIN LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_trigonometric_functions_ASIND(p):
    '''TRIGONOMETRIC_FUNCTIONS : ASIND LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Trigonometric Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<TRIGONOMETRIC_FUNCTIONS> ::= ASIND LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_trigonometric_functions_ATAN(p):
    '''TRIGONOMETRIC_FUNCTIONS : ATAN LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Trigonometric Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<TRIGONOMETRIC_FUNCTIONS> ::= ATAN LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_trigonometric_functions_ATAND(p):
    '''TRIGONOMETRIC_FUNCTIONS : ATAND LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Trigonometric Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<TRIGONOMETRIC_FUNCTIONS> ::= ATAND LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_trigonometric_functions_COS(p):
    '''TRIGONOMETRIC_FUNCTIONS : COS LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Trigonometric Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<TRIGONOMETRIC_FUNCTIONS> ::= COS LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_trigonometric_functions_COSD(p):
    '''TRIGONOMETRIC_FUNCTIONS : COSD LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Trigonometric Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<TRIGONOMETRIC_FUNCTIONS> ::= COSD LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_trigonometric_functions_COT(p):
    '''TRIGONOMETRIC_FUNCTIONS : COT LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Trigonometric Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<TRIGONOMETRIC_FUNCTIONS> ::= COT LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_trigonometric_functions_COTD(p):
    '''TRIGONOMETRIC_FUNCTIONS : COTD LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Trigonometric Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<TRIGONOMETRIC_FUNCTIONS> ::= COTD LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_trigonometric_functions_SIN(p):
    '''TRIGONOMETRIC_FUNCTIONS : SIN LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Trigonometric Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<TRIGONOMETRIC_FUNCTIONS> ::= SIN LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_trigonometric_functions_SIND(p):
    '''TRIGONOMETRIC_FUNCTIONS : SIND LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Trigonometric Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<TRIGONOMETRIC_FUNCTIONS> ::= SIND LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_trigonometric_functions_TAN(p):
    '''TRIGONOMETRIC_FUNCTIONS : TAN LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Trigonometric Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<TRIGONOMETRIC_FUNCTIONS> ::= TAN LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_trigonometric_functions_TAND(p):
    '''TRIGONOMETRIC_FUNCTIONS : TAND LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Trigonometric Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<TRIGONOMETRIC_FUNCTIONS> ::= TAND LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_trigonometric_functions_COSH(p):
    '''TRIGONOMETRIC_FUNCTIONS : COSH LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Trigonometric Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<TRIGONOMETRIC_FUNCTIONS> ::= COSH LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_trigonometric_functions_SINH(p):
    '''TRIGONOMETRIC_FUNCTIONS : SINH LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Trigonometric Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<TRIGONOMETRIC_FUNCTIONS> ::= SINH LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_trigonometric_functions_TANH(p):
    '''TRIGONOMETRIC_FUNCTIONS : TANH LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Trigonometric Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<TRIGONOMETRIC_FUNCTIONS> ::= TANH LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_trigonometric_functions_ACOSH(p):
    '''TRIGONOMETRIC_FUNCTIONS : ACOSH LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Trigonometric Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<TRIGONOMETRIC_FUNCTIONS> ::= ACOSH LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_trigonometric_functions_ASINH(p):
    '''TRIGONOMETRIC_FUNCTIONS : ASINH LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Trigonometric Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<TRIGONOMETRIC_FUNCTIONS> ::= ASINH LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_trigonometric_functions_ATANH(p):
    '''TRIGONOMETRIC_FUNCTIONS : ATANH LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('Trigonometric Functions')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.production = f"<TRIGONOMETRIC_FUNCTIONS> ::= ATANH LEFT_PARENTHESIS <SQLSIMPLEEXPRESSION> RIGHT_PARENTHESIS\n"
    nodo.production += f"{p[3].production}"
    p[0] = nodo


def p_sql_alias(p):
    '''SQLALIAS : AS SQLNAME
                | SQLNAME'''
    nodo = Node('SQL Alias')
    if (len(p) == 3):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.production = f"<SQLALIAS> ::= AS <SQLNAME>\n"
        nodo.production += f"{p[2].production}"
        p[0] = nodo
    elif (len(p) == 2):
        nodo.add_childrens(p[1])
        nodo.production = f"<SQLALIAS> ::= <SQLNAME>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo


def p_expressions_time(p):
    '''EXPRESSIONSTIME : EXTRACT LEFT_PARENTHESIS DATETYPES FROM TIMESTAMP SQLNAME RIGHT_PARENTHESIS
                       | NOW LEFT_PARENTHESIS RIGHT_PARENTHESIS
                       | DATE_PART LEFT_PARENTHESIS SQLNAME COMMA INTERVAL SQLNAME RIGHT_PARENTHESIS
                       | CURRENT_DATE
                       | TIMESTAMP SQLNAME'''
    nodo = Node('Expressions Time')
    if (len(p) == 8):
        if (p[1] == 'EXTRACT'):
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(Node(p[2]))
            nodo.add_childrens(p[3])
            nodo.add_childrens(Node(p[4]))
            nodo.add_childrens(Node(p[5]))
            nodo.add_childrens(p[6])
            nodo.add_childrens(Node(p[7]))
            nodo.production = f"<EXPRESSIONSTIME> ::= EXTRACT LEFT_PARENTHESIS <DATETYPES> FROM TIMESTAMP <SQLNAME> RIGHT_PARENTHESIS\n"
            nodo.production += f"{p[3].production}"
            nodo.production += f"{p[6].production}"
            p[0] = nodo
        else:
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(Node(p[2]))
            nodo.add_childrens(p[3])
            nodo.add_childrens(Node(p[4]))
            nodo.add_childrens(Node(p[5]))
            nodo.add_childrens(p[6])
            nodo.add_childrens(Node(p[7]))
            nodo.production = f"<EXPRESSIONSTIME> ::= DATE_PART LEFT_PARENTHESIS <SQLNAME> COMMA INTERVAL <SQLNAME> RIGHT_PARENTHESIS\n"
            nodo.production += f"{p[3].production}"
            nodo.production += f"{p[6].production}"
            p[0] = nodo

    elif (len(p) == 3):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.production = f"<EXPRESSIONSTIME> ::= TIMESTAMP <SQLNAME>\n"
        nodo.production += f"{p[2].production}"
        p[0] = nodo

    elif len(p) == 4:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.production = f"<EXPRESSIONSTIME> ::= NOW LEFT_PARENTHESIS RIGHT_PARENTHESIS\n"
        p[0] = nodo

    else:
        nodo.add_childrens(Node(p[1]))
        nodo.production = f"<EXPRESSIONSTIME> ::= CURRENT_DATE\n"
        p[0] = nodo


def p_expressions_time_CURRENT_TIME(p):
    '''EXPRESSIONSTIME : CURRENT_TIME'''
    nodo = Node('Expressions Time')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<EXPRESSIONSTIME> ::= CURRENT_TIME\n"
    p[0] = nodo


def p_aggregate_functions(p):
    '''AGGREGATEFUNCTIONS : AGGREGATETYPES LEFT_PARENTHESIS CONTOFAGGREGATE RIGHT_PARENTHESIS
                          | AGGREGATETYPES LEFT_PARENTHESIS CONTOFAGGREGATE RIGHT_PARENTHESIS SQLALIAS'''
    nodo = Node('Aggregate Functions')
    if (len(p) == 5):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.production = f"<AGGREGATEFUNCTIONS> ::= <AGGREGATETYPES> LEFT_PARENTHESIS <CONTOFAGGREGATE> RIGHT_PARENTHESIS\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[3].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        nodo.production = f"<AGGREGATEFUNCTIONS> ::= <AGGREGATETYPES> LEFT_PARENTHESIS <CONTOFAGGREGATE> RIGHT_PARENTHESIS <SQLALIAS>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[3].production}"
        nodo.production += f"{p[5].production}"
        p[0] = nodo


def p_cont_of_aggregate(p):
    '''CONTOFAGGREGATE : ASTERISK
                       | SQLSIMPLEEXPRESSION'''
    nodo = Node('Contof Aggregate')
    if (p[1] == '*'):
        nodo.add_childrens(Node(p[1]))
        nodo.production = f"<CONTOFAGGREGATE> ::= ASTERISK\n"
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        nodo.production = f"<CONTOFAGGREGATE> ::= <SQLSIMPLEEXPRESSION>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo


def p_sql_object_reference(p):
    '''OBJECTREFERENCE : SQLNAME DOT ASTERISK
                       | SQLNAME'''
    nodo = Node('Object Reference')
    if (len(p) == 2):
        nodo.add_childrens(p[1])
        nodo.production = f"<OBJECTREFERENCE> ::= <SQLNAME>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo
    elif (len(p) == 4):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.production = f"<OBJECTREFERENCE> ::= <SQLNAME> DOT ASTERISK\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo


def p_sql_object_reference_SQLNAME(p):
    '''OBJECTREFERENCE : SQLNAME DOT SQLNAME'''
    nodo = Node('Object Reference')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.production = f"<OBJECTREFERENCE> ::= <SQLNAME> DOT <SQLNAME>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_list_values_insert(p):
    '''LISTVALUESINSERT : LISTVALUESINSERT COMMA SQLSIMPLEEXPRESSION
                        | SQLSIMPLEEXPRESSION'''
    nodo = Node('List Values Insert')
    if(len(p) == 4):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.production = f"<LISTVALUESINSERT> ::= <LISTVALUESINSERT> COMMA <SQLSIMPLEEXPRESSION>\n"
        nodo.production += f"{p[1].production}"
        nodo.production += f"{p[3].production}"
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        nodo.production = f"<LISTVALUESINSERT> ::= <SQLSIMPLEEXPRESSION>\n"
        nodo.production += f"{p[1].production}"
        p[0] = nodo


def p_type_combine_query_UNION(p):
    '''TYPECOMBINEQUERY : UNION'''
    nodo = Node('Type Combine Query')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<TYPECOMBINEQUERY> ::= UNION\n"
    p[0] = nodo


def p_type_combine_query_INTERSECT(p):
    '''TYPECOMBINEQUERY : INTERSECT'''
    nodo = Node('Type Combine Query')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<TYPECOMBINEQUERY> ::= INTERSECT\n"
    p[0] = nodo


def p_type_combine_query_EXCEPT(p):
    '''TYPECOMBINEQUERY : EXCEPT'''
    nodo = Node('Type Combine Query')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<TYPECOMBINEQUERY> ::= EXCEPT\n"
    p[0] = nodo


def p_relop_EQUALS(p):
    '''RELOP : EQUALS'''
    nodo = Node('Relop')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<RELOP> ::= EQUALS\n"
    p[0] = nodo


def p_relop_NOT_EQUAL(p):
    '''RELOP : NOT_EQUAL'''
    nodo = Node('Relop')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<RELOP> ::= NOT_EQUAL\n"
    p[0] = nodo


def p_relop_GREATE_EQUAL(p):
    '''RELOP : GREATE_EQUAL'''
    nodo = Node('Relop')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<RELOP> ::= GREATE_EQUAL\n"
    p[0] = nodo


def p_relop_GREATE_THAN(p):
    '''RELOP : GREATE_THAN'''
    nodo = Node('Relop')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<RELOP> ::= GREATE_THAN\n"
    p[0] = nodo


def p_relop_LESS_THAN(p):
    '''RELOP : LESS_THAN'''
    nodo = Node('Relop')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<RELOP> ::= LESS_THAN\n"
    p[0] = nodo


def p_relop_LESS_EQUAL(p):
    '''RELOP : LESS_EQUAL'''
    nodo = Node('Relop')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<RELOP> ::= LESS_EQUAL\n"
    p[0] = nodo


def p_relop_NOT_EQUAL_LR(p):
    '''RELOP : NOT_EQUAL_LR'''
    nodo = Node('Relop')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<RELOP> ::= NOT_EQUAL_LR\n"
    p[0] = nodo


def p_aggregate_types_AVG(p):
    '''AGGREGATETYPES : AVG'''
    nodo = Node('Aggregate Types')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<AGGREGATETYPES> ::= AVG\n"
    p[0] = nodo


def p_aggregate_types_SUM(p):
    '''AGGREGATETYPES : SUM'''
    nodo = Node('Aggregate Types')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<AGGREGATETYPES> ::= SUM\n"
    p[0] = nodo


def p_aggregate_types_COUNT(p):
    '''AGGREGATETYPES : COUNT'''
    nodo = Node('Aggregate Types')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<AGGREGATETYPES> ::= COUNT\n"
    p[0] = nodo


def p_aggregate_types_MAX(p):
    '''AGGREGATETYPES : MAX'''
    nodo = Node('Aggregate Types')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<AGGREGATETYPES> ::= MAX\n"
    p[0] = nodo


def p_aggregate_types_MIN(p):
    '''AGGREGATETYPES : MIN'''
    nodo = Node('Aggregate Types')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<AGGREGATETYPES> ::= MIN\n"
    p[0] = nodo


def p_date_types_YEAR(p):
    '''DATETYPES : YEAR'''
    nodo = Node('Date Types')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<DATETYPES> ::= YEAR\n"
    p[0] = nodo


def p_date_types_MONTH(p):
    '''DATETYPES : MONTH'''
    nodo = Node('Date Types')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<DATETYPES> ::= MONTH\n"
    p[0] = nodo


def p_date_types_DAY(p):
    '''DATETYPES : DAY'''
    nodo = Node('Date Types')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<DATETYPES> ::= DAY\n"
    p[0] = nodo


def p_date_types_HOUR(p):
    '''DATETYPES : HOUR'''
    nodo = Node('Date Types')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<DATETYPES> ::= HOUR\n"
    p[0] = nodo


def p_date_types_MINUTE(p):
    '''DATETYPES : MINUTE'''
    nodo = Node('Date Types')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<DATETYPES> ::= MINUTE\n"
    p[0] = nodo


def p_date_types_SECOND(p):
    '''DATETYPES : SECOND'''
    nodo = Node('Date Types')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<DATETYPES> ::= SECOND\n"
    p[0] = nodo


def p_sql_integer(p):
    '''SQLINTEGER : INT_NUMBER'''
    nodo = Node('SQL Integer')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<SQLINTEGER> ::= INT_NUMBER\n"
    p[0] = nodo


def p_sql_integer_FLOAT_NUMBER(p):
    '''SQLINTEGER : FLOAT_NUMBER'''
    nodo = Node('SQL Integer')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<SQLINTEGER> ::= FLOAT_NUMBER\n"
    p[0] = nodo


def p_sql_name_STRINGCONT(p):
    '''SQLNAME : STRINGCONT'''
    nodo = Node('SQL Name')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<SQLINTEGER> ::= STRINGCONT\n"
    p[0] = nodo


def p_sql_name_CHARCONT(p):
    '''SQLNAME : CHARCONT'''
    nodo = Node('SQL Name')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<SQLINTEGER> ::= CHARCONT\n"
    p[0] = nodo


def p_sql_name(p):
    '''SQLNAME : ID'''
    nodo = Node('SQL Name')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<SQLINTEGER> ::= ID\n"
    p[0] = nodo


def p_type_select_ALL(p):
    '''TYPESELECT : ALL'''
    nodo = Node('Type Select')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<TYPESELECT> ::= ALL\n"
    p[0] = nodo


def p_type_select_DISTINCT(p):
    '''TYPESELECT : DISTINCT'''
    nodo = Node('Type Select')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<TYPESELECT> ::= DISTINCT\n"
    p[0] = nodo


def p_type_select_UNIQUE(p):
    '''TYPESELECT : UNIQUE'''
    nodo = Node('Type Select')
    nodo.add_childrens(Node(p[1]))
    nodo.production = f"<TYPESELECT> ::= UNIQUE\n"
    p[0] = nodo


def p_sub_query(p):
    '''SUBQUERY : SELECTSTATEMENT'''
    nodo = Node('SubQuery')
    nodo.add_childrens(p[1])
    nodo.production = f"<SUBQUERY> ::= <SELECTSTATEMENT>\n"
    nodo.production += f"{p[1].production}"
    p[0] = nodo


def p_error(p):
    print('error xd')


parser = yacc.yacc()


def parse2(inpu):
    lexer = lex.lex()
    lexer.lineno = 1
    return parser.parse(inpu, lexer=lexer)
