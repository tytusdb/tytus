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
    ('left', 'ASTERISK', 'DIVISION', 'MODULAR', 'BITWISE_SHIFT_RIGHT', 'BITWISE_SHIFT_LEFT', 'BITWISE_AND', 'BITWISE_OR'),  # Level 8
    ('left', 'EXPONENT',  'BITWISE_XOR', 'SQUARE_ROOT', 'CUBE_ROOT'),  # Level 9
    ('right', 'UPLUS', 'UREST'),  # Level 10
    ('left', 'DOT')  # Level 13
)

# Definicion de Gramatica, un poco de defincion
# Para que no se confundad, para crear la gramatica y se reconocida
# siempre se empieza la funcion con la letra p, ejemplo p_name_function y
# siempre recibe el paramatro p, en la gramatica los dos puntos es como usar :=
# No debe quedar junto a los no terminales, ejemplo EXPRESSION:, por que en este caso marcara un error
# si la gramatica solo consta de una linea se pueden usar comillas simples ' ' pero si ya consta de varias lineas
# se usa ''' ''' para que no marque error
# Nota: p siempre es un array y para llamar los tokens, solo se escriben tal y como fueron definidos en la clase lex.py
# y estos no pueden ser usados para los nombres de los no terminales, si no lanzara error


# =====================================================================================
# =====================================================================================
# ====================================================================================


def p_instruction_list(p):
    '''instructionlist : instructionlist sqlinstruction
                       | sqlinstruction
    '''
    nodo = Node('instructionlist')
    if len(p) == 3:
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        p[0] = nodo        


def p_sql_instruction(p):
    '''sqlinstruction : ddl
                    | DML
    '''
    nodo = Node('sqlinstruction')
    nodo.add_childrens(p[1])
    p[0] = nodo

def p_ddl(p):
    '''ddl : createstatement
           | showstatement
           | alterstatement
           | dropstatement
    '''
    nodo = Node('ddl')
    nodo.add_childrens(p[1])
    p[0] = nodo

def p_create_statement(p):
    '''createstatement : CREATE optioncreate SEMICOLON'''
    nodo = Node('createstatement')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.add_childrens(Node(p[3]))
    p[0] = nodo

def p_option_create(p):
    '''optioncreate : TYPE SQLNAME AS ENUM LEFT_PARENTHESIS typelist RIGHT_PARENTHESIS
                    | DATABASE createdb
                    | OR REPLACE DATABASE createdb
                    | TABLE SQLNAME LEFT_PARENTHESIS columnstable RIGHT_PARENTHESIS
                    | TABLE SQLNAME LEFT_PARENTHESIS columnstable RIGHT_PARENTHESIS INHERITS LEFT_PARENTHESIS ID RIGHT_PARENTHESIS
    '''
    nodo = Node('optioncreate')
    if len(p) == 8:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(Node(p[5]))
        nodo.add_childrens(p[6])
        nodo.add_childrens(Node(p[7]))
        p[0] = nodo

    elif len(p) == 3:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        p[0] = nodo

    elif len(p) == 5:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        p[0] = nodo

    elif len(p) == 6:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.add_childrens(Node(p[5]))
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
        p[0] = nodo


def p_type_list(p):
    '''typelist : typelist COMMA SQLNAME
                | SQLNAME '''
    nodo = Node('typelist')
    if len(p) == 4:
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        p[0] = nodo


def p_create_db(p):
    '''createdb : IF NOT EXISTS ID listpermits
                | IF NOT EXISTS ID
                | ID listpermits
                | ID 
    '''
    nodo = Node('createdb')
    if len(p) == 6:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        p[0] = nodo

    elif len(p) == 5:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        p[0] = nodo

    elif len(p) == 3:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        p[0] = nodo


def p_list_permits(p):
    '''listpermits : listpermits permits
                   | permits
    '''
    nodo  = Node('listpermits')
    if len(p) == 3:
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        p[0] = nodo


def p_permits(p):
    '''permits : OWNER EQUALS ID
               | OWNER ID
               | MODE EQUALS INT_NUMBER
               | MODE INT_NUMBER 
    '''
    nodo = Node('permits')
    if len(p) == 4:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        p[0] = nodo
    elif len(p) == 3:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        p[0] = nodo

def p_columns_table(p):
    '''columnstable : columnstable COMMA column
                    | column
    '''
    nodo = Node('columnstable')
    if len(p) == 4:
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        p[0] = nodo

    else:
        nodo.add_childrens(p[1])
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
    nodo =  Node('column')
    if len(p) == 4:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(p[3])
        p[0] = nodo

    elif len(p) == 3:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        p[0] = nodo

    elif len(p) == 5:
        if p[1] == 'UNIQUE':
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(Node(p[2]))
            nodo.add_childrens(p[3])
            nodo.add_childrens(Node(p[4]))
            p[0] = nodo

        else:  # CHECK
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(Node(p[2]))
            nodo.add_childrens(p[3])
            nodo.add_childrens(Node(p[4]))
            p[0] = nodo

    elif len(p) == 6:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.add_childrens(Node(p[5]))
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
        p[0] = nodo

    elif len(p) == 7:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        nodo.add_childrens(Node(p[6]))
        p[0] = nodo


def p_type_col(p):
    '''typecol : SMALLINT
               | INTEGER
               | BIGINT
               | DECIMAL LEFT_PARENTHESIS INT_NUMBER COMMA INT_NUMBER RIGHT_PARENTHESIS
               | DECIMAL LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS
               | NUMERIC LEFT_PARENTHESIS INT_NUMBER COMMA INT_NUMBER RIGHT_PARENTHESIS
               | NUMERIC LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS
               | REAL
               | DOUBLE PRECISION
               | MONEY
               | CHARACTER VARYING LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS
               | CHARACTER VARYING
               | VARCHAR LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS
               | VARCHAR
               | CHARACTER LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS
               | CHARACTER
               | CHAR LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS
               | CHAR
               | TEXT
               | TIMESTAMP LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS
               | TIMESTAMP
               | DATE
               | TIME LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS
               | TIME
               | INTERVAL SQLNAME
               | BOOLEAN
    '''
    nodo = Node('typecol')
    if len(p) == 2:
        nodo.add_childrens(Node(p[1]))
        p[0] = nodo

    elif len(p) == 3:
        if p[2] == 'PRECISION' or p[2] == 'VARYING':
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(Node(p[2]))
            p[0] = nodo
        else:
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(p[2])
            p[0] = nodo

    elif len(p) == 5:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        p[0] = nodo
    
    elif len(p) == 6:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(Node(p[5]))
        p[0] = nodo
    
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(Node(p[5]))
        nodo.add_childrens(Node(p[6]))
        p[0] = nodo

def p_options_col_list(p):
    '''optionscollist : optionscollist optioncol
                      | optioncol
    '''
    nodo = Node('optionscollist')
    if len(p) == 3:
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        p[0] = nodo


def p_option_col(p):
    '''optioncol : DEFAULT SQLSIMPLEEXPRESSION                
                 | NOT NULL
                 | NULL
                 | CONSTRAINT ID UNIQUE
                 | UNIQUE
                 | CONSTRAINT ID CHECK LEFT_PARENTHESIS conditionColumn RIGHT_PARENTHESIS
                 | CHECK LEFT_PARENTHESIS conditionColumn RIGHT_PARENTHESIS
                 | PRIMARY KEY 
                 | REFERENCES ID 
    '''
    nodo = Node('optioncol')
    if len(p) == 3:
        if p[2] == 'NULL' or p[2] == 'ID' or p[2] == 'KEY':
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(Node(p[2]))
            p[0] = nodo
        else:
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(p[2])
            p[0] = nodo
    elif len(p) == 2:
        nodo.add_childrens(Node(p[1]))
        p[0] = nodo
    elif len(p) == 4:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        p[0] = nodo
    elif len(p) == 5:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        nodo.add_childrens(Node(p[6]))
        p[0] = nodo

        
def p_condition_column(p):
    '''conditionColumn : conditioncheck'''
    nodo = Node('conditionColumn')
    nodo.add_childrens(p[1])
    p[0] = nodo


def p_condition_check(p):
    '''conditioncheck : SQLRELATIONALEXPRESSION
    '''
    nodo = Node('conditioncheck')
    nodo.add_childrens(p[1])
    p[0] = nodo


def p_column_list(p):
    '''columnlist : columnlist COMMA ID
                  | ID
    '''
    nodo = Node('columnlist')
    if len(p) == 4:
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        p[0] = nodo


def p_show_statement(p):
    '''showstatement : SHOW DATABASES SEMICOLON
                     | SHOW DATABASES LIKE ID SEMICOLON
    '''
    nodo = Node('showstatement')
    if len(p) == 4:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(Node(p[5]))
        p[0] = nodo


def p_alter_statement(p):
    '''alterstatement : ALTER optionsalter SEMICOLON
    '''
    nodo = Node('alterstatement')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.add_childrens(Node(p[3]))
    p[0] = nodo

def p_options_alter(p):
    '''optionsalter : DATABASE alterdatabase
                    | TABLE altertable
    '''
    nodo = Node('optionsalter')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    p[0] = nodo


def p_alter_database(p):
    '''alterdatabase : ID RENAME TO ID
                     | ID OWNER TO typeowner
    '''
    nodo = Node('alterdatabase')
    if p[2] == 'RENAME':
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])                       
        p[0] = nodo


def p_type_owner(p):
    '''typeowner : ID
                 | CURRENT_USER
                 | SESSION_USER 
    '''
    nodo = Node('typeowner')
    nodo.add_childrens(Node(p[1]))
    p[0] = nodo


def p_alter_table(p):
    '''altertable : ID alterlist
    '''
    nodo = Node('altertable')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    p[0] = nodo


def p_alter_list(p):
    '''alterlist : alterlist COMMA typealter
                 | typealter
    '''
    nodo = Node('alterlist')
    if(len(p) == 4):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        p[0] = nodo


def p_type_alter(p):
    '''typealter : ADD addalter
                 | ALTER alteralter
                 | DROP dropalter
                 | RENAME  renamealter
    '''
    nodo = Node('typealter')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    p[0] = nodo

def p_add_alter(p):
    '''addalter : COLUMN ID typecol
                | CHECK LEFT_PARENTHESIS conditionColumn RIGHT_PARENTHESIS
                | CONSTRAINT ID UNIQUE LEFT_PARENTHESIS ID RIGHT_PARENTHESIS
                | FOREIGN KEY LEFT_PARENTHESIS ID RIGHT_PARENTHESIS REFERENCES ID
    '''
    nodo = Node('addalter')
   
    if len(p) == 4:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        p[0] = nodo
   
    elif len(p) == 5:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        p[0] = nodo
   
    elif len(p) == 7:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(Node(p[5]))
        nodo.add_childrens(Node(p[6]))
        p[0] = nodo
    
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(Node(p[5]))
        nodo.add_childrens(Node(p[6]))
        nodo.add_childrens(Node(p[7]))
        p[0] = nodo


def p_alter_alter(p):
    '''alteralter : COLUMN ID SET NOT NULL
                  | COLUMN ID TYPE typecol
    '''
    nodo = Node('alteralter')
    if len(p) == 6:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(Node(p[5]))
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        p[0] = nodo


def p_drop_alter(p):
    '''dropalter : COLUMN ID
                 | CONSTRAINT ID
    '''
    nodo = Node('dropalter')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    p[0] = nodo

def p_rename_alter(p):
    '''renamealter : COLUMN ID TO ID
    '''
    nodo = Node('renamealter')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(Node(p[3]))
    nodo.add_childrens(Node(p[4]))
    p[0] = nodo


def p_drop_statement(p):
    '''dropstatement : DROP optionsdrop SEMICOLON'''
    nodo = Node('dropstatement')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    nodo.add_childrens(Node(p[3]))
    p[0] = nodo


def p_options_drop(p):
    '''optionsdrop : DATABASE dropdatabase
                    | TABLE droptable
    '''
    nodo = Node('optionsdrop')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    p[0] = nodo


def p_drop_database(p):
    '''dropdatabase : IF EXISTS ID
                    | ID
    '''
    nodo = Node('dropdatabase')
    if len(p) == 4:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        p[0] = nodo


def p_drop_table(p):
    '''droptable : ID
    '''
    nodo = Node('droptable')
    nodo.add_childrens(Node(p[1]))
    p[0] = nodo


# =====================================================================================
# =====================================================================================
# =====================================================================================

def p_dml(p):
    '''DML : QUERYSTATEMENT
           | INSERTSTATEMENT
           | DELETESTATEMENT
           | UPDATESTATEMENT'''
    nodo = Node('DML')
    nodo.add_childrens(p[1])
    p[0] = nodo


def p_update_statement(p):
    '''UPDATESTATEMENT : UPDATE ID OPTIONS1 SET SETLIST OPTIONSLIST2 SEMICOLON
                       | UPDATE ID SET SETLIST OPTIONSLIST2 SEMICOLON
                       | UPDATE ID SET SETLIST  SEMICOLON '''
    nodo = Node('UPDATESTATEMENT')
    if(len(p) == 7):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.add_childrens(p[5])
        nodo.add_childrens(Node(p[6]))
        p[0] = nodo
    elif(len(p) == 6):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.add_childrens(Node(p[5]))
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        nodo.add_childrens(p[6])
        nodo.add_childrens(Node(p[7]))
        p[0] = nodo

def p_set_list(p):
    '''SETLIST : SETLIST COMMA COLUMNVALUES
               | COLUMNVALUES'''
    nodo = Node('SETLIST')
    if(len(p) == 4):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        p[0] = nodo

def p_column_values(p):
    '''COLUMNVALUES : OBJECTREFERENCE EQUALS SQLEXPRESSION2'''
    nodo = Node('COLUMNVALUES')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    p[0] = nodo


def p_sql_expression2(p):
    '''SQLEXPRESSION2 : SQLEXPRESSION2 PLUS SQLEXPRESSION2 
                      | SQLEXPRESSION2 REST SQLEXPRESSION2 
                      | SQLEXPRESSION2 DIVISION SQLEXPRESSION2 
                      | SQLEXPRESSION2 ASTERISK SQLEXPRESSION2 
                      | SQLEXPRESSION2 MODULAR SQLEXPRESSION2
                      | SQLEXPRESSION2 EXPONENT SQLEXPRESSION2 
                      | REST SQLEXPRESSION2 %prec UREST
                      | PLUS SQLEXPRESSION2 %prec UPLUS
                      | LEFT_PARENTHESIS SQLEXPRESSION2 RIGHT_PARENTHESIS
                      | SQLNAME
                      | SQLINTEGER'''
    nodo = Node('SQLEXPRESSION2')
    if len(p) == 4:
        if p[1] == '(':
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(p[2])
            nodo.add_childrens(Node(p[3]))
            p[0] = nodo
        else:
            nodo.add_childrens(p[1])
            nodo.add_childrens(Node(p[2]))
            nodo.add_childrens(p[3])
            p[0] = nodo
    elif len(p) == 3:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        p[0] = nodo

def p_options_list2(p):
    '''OPTIONSLIST2 : WHERECLAUSE OPTIONS4
                    | WHERECLAUSE
                    | OPTIONS4'''
    nodo = Node('OPTIONSLIST2')
    if (len(p) == 3):
         nodo.add_childrens(p[1])
         nodo.add_childrens(p[2])
         p[0] = nodo
    else:
         nodo.add_childrens(p[1])
         p[0] = nodo


def p_delete_statement(p):
    '''DELETESTATEMENT : DELETE FROM ID OPTIONSLIST SEMICOLON
                       | DELETE FROM ID SEMICOLON '''
    nodo = Node('DELETESTATEMENT')
    if (len(p) == 6):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.add_childrens(Node(p[5]))
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        p[0] = nodo

def p_options_list(p):
    '''OPTIONSLIST : OPTIONS1 OPTIONS2 WHERECLAUSE OPTIONS4
                   | OPTIONS1 OPTIONS2 WHERECLAUSE
                   | OPTIONS1 WHERECLAUSE OPTIONS4
                   | OPTIONS1 OPTIONS2 OPTIONS4
                   | OPTIONS2 WHERECLAUSE OPTIONS4
                   | OPTIONS1 OPTIONS2
                   | OPTIONS1 WHERECLAUSE
                   | OPTIONS1 OPTIONS4
                   | OPTIONS2 WHERECLAUSE
                   | OPTIONS2 OPTIONS4
                   | WHERECLAUSE OPTIONS4
                   | OPTIONS1
                   | OPTIONS2
                   | WHERECLAUSE
                   | OPTIONS4'''
    nodo = Node('OPTIONSLIST')
    if (len(p) == 5):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        nodo.add_childrens(p[3])
        nodo.add_childrens(p[4])
        p[0] = nodo
    elif (len(p) == 4):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        nodo.add_childrens(p[3])
        p[0] = nodo
    elif (len(p) == 3):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        p[0] = nodo

def p_options1(p):
    '''OPTIONS1 : ASTERISK SQLALIAS
                | ASTERISK
                | SQLALIAS'''
    nodo = Node('OPTIONS1')
    if(len(p) == 2):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        p[0] = nodo
    else:
        if(p[1] == "*"):
            nodo.add_childrens(Node(p[1]))
            p[0] = nodo
        else:
            nodo.add_childrens(p[1])
            p[0] = nodo

def p_options2(p):
    '''OPTIONS2 : USING USINGLIST'''
    nodo = Node('OPTIONS2')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    p[0] = nodo

def p_using_list(p):
    '''USINGLIST  : USINGLIST COMMA SQLNAME
                  | SQLNAME'''
    nodo = Node('USINGLIST')
    if(len(p) == 4):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        p[0] = nodo

# def p_options3(p):
#     '''OPTIONS3 : WHERE SQLEXPRESSION'''
#     p[0] = Where(p[2]) --------> GRAMATICA SE REPITE

def p_options4(p):
    '''OPTIONS4 : RETURNING RETURNINGLIST'''
    nodo = Node('OPTIONS4')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    p[0] = nodo

def p_returning_list(p):
    '''RETURNINGLIST   : ASTERISK
                       | EXPRESSIONRETURNING'''
    nodo = Node('RETURNINGLIST')
    if p[1] == '*':
        nodo.add_childrens(Node(p[1]))
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        p[0] = nodo

def p_returning_expression(p):
    '''EXPRESSIONRETURNING : EXPRESSIONRETURNING COMMA SQLEXPRESSION SQLALIAS
                           | SQLEXPRESSION SQLALIAS'''
    nodo = Node('EXPRESSIONRETURNING')
    if(len(p) == 5):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(p[4])
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        p[0] = nodo

def p_insert_statement(p):
    '''INSERTSTATEMENT : INSERT INTO SQLNAME LEFT_PARENTHESIS LISTPARAMSINSERT RIGHT_PARENTHESIS VALUES LEFT_PARENTHESIS LISTVALUESINSERT RIGHT_PARENTHESIS SEMICOLON
                       | INSERT INTO SQLNAME VALUES LEFT_PARENTHESIS LISTVALUESINSERT RIGHT_PARENTHESIS SEMICOLON '''
    nodo = Node('INSERTSTATEMENT')
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
        p[0] = nodo

def p_list_params_insert(p):
    '''LISTPARAMSINSERT : LISTPARAMSINSERT COMMA ID
                        | ID'''
    nodo = Node("LISTPARAMSINSERT")
    if(len(p) == 4):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        p[0] = nodo

def p_query_statement(p):
    #  ELEMENTO 0       ELEMENTO 1     ELEMENTO 2      ELEMENTO 3
    '''QUERYSTATEMENT : SELECTSTATEMENT SEMICOLON'''
    nodo = Node('QUERYSTATEMENT')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    p[0] = nodo

def p_select_statement(p):
    '''SELECTSTATEMENT : SELECTWITHOUTORDER ORDERBYCLAUSE LIMITCLAUSE
                       | SELECTWITHOUTORDER ORDERBYCLAUSE 
                       | SELECTWITHOUTORDER LIMITCLAUSE 
                       | SELECTWITHOUTORDER'''
    nodo = Node('SELECTSTATEMENT')
    if (len(p) == 4):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        nodo.add_childrens(p[3])
        p[0] = nodo
    elif (len(p) == 3):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        p[0] = nodo
    elif (len(p) == 2):
        nodo.add_childrens(p[1])
        p[0] = nodo


def p_select_without_order(p):
    '''SELECTWITHOUTORDER : SELECTSET
                          | SELECTWITHOUTORDER TYPECOMBINEQUERY ALL SELECTSET
                          | SELECTWITHOUTORDER TYPECOMBINEQUERY SELECTSET'''
    nodo = Node('SELECTWITHOUTORDER')
    if len(p) == 2:
        nodo.add_childrens(p[1])
        p[0] = nodo
    elif len(p) == 5:
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        p[0] = nodo
    elif len(p) == 4:
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        nodo.add_childrens(p[3])
        p[0] = nodo
    


def p_select_set(p):
    '''SELECTSET : SELECTQ 
                 | LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS'''
    nodo = Node('SELECTSET')
    if len(p) == 2:
        nodo.add_childrens(p[1])
        p[0] = nodo
    elif len(p) == 4:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(Node(p[3]))
        p[0] = nodo

def p_selectq(p):
    '''SELECTQ : SELECT SELECTLIST FROMCLAUSE
               | SELECT SELECTLIST FROMCLAUSE SELECTWHEREAGGREGATE
               | SELECT TYPESELECT SELECTLIST FROMCLAUSE
               | SELECT TYPESELECT SELECTLIST FROMCLAUSE SELECTWHEREAGGREGATE
               | SELECT SELECTLIST'''
    nodo = Node('SELECTQ')
    if len(p) == 4:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(p[3])
        p[0] = nodo
    elif len(p) == 5:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(p[3])
        nodo.add_childrens(p[4])
        p[0] = nodo
    elif len(p) == 6:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(p[3])
        nodo.add_childrens(p[4])
        nodo.add_childrens(p[5])
        p[0] = nodo
    elif len(p) == 3:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        p[0] = nodo


def p_select_list(p):
    '''SELECTLIST : ASTERISK
                  | LISTITEM'''
    nodo = Node('SELECTLIST')
    if p[1] == '*':
        nodo.add_childrens(Node(p[1]))
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        p[0] = nodo

def p_list_item(p):
    '''LISTITEM : LISTITEM COMMA SELECTITEM
                | SELECTITEM'''
    nodo = Node('LISTITEM')
    if len(p) == 2:
        nodo.add_childrens(p[1])
        p[0] = nodo
    elif len(p) == 4:
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        p[0] = nodo

def p_select_item(p):
    '''SELECTITEM : SQLSIMPLEEXPRESSION SQLALIAS
                  | SQLSIMPLEEXPRESSION
                  | LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS'''
    nodo = Node('SELECTITEM')
    if (len(p) == 3):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        p[0] = nodo
    elif (len(p) == 4):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(Node(p[3]))
        p[0] = nodo
    elif (len(p) == 2):
        nodo.add_childrens(p[1])
        p[0] = nodo


def p_from_clause(p):
    '''FROMCLAUSE : FROM FROMCLAUSELIST'''
    nodo = Node('FROMCLAUSE')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    p[0] = nodo

def p_from_clause_list(p):
    '''FROMCLAUSELIST : FROMCLAUSELIST COMMA TABLEREFERENCE
                      | FROMCLAUSELIST LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS SQLALIAS
                      | FROMCLAUSELIST LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS
                      | LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS
                      | LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS SQLALIAS
                      | TABLEREFERENCE'''
    nodo = Node('FROMCLAUSELIST')
    if (len(p) == 6):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        p[0] = nodo
    elif (len(p) == 5):
        if (p[1] == "("):
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(p[2])
            nodo.add_childrens(Node(p[3]))
            nodo.add_childrens(p[4])
            p[0] = nodo
        else:
            nodo.add_childrens(p[1])
            nodo.add_childrens(Node(p[2]))
            nodo.add_childrens(p[3])
            nodo.add_childrens(Node(p[4]))
            p[0] = nodo
    elif (len(p) == 4):
        if (p[1] == "("):
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(p[2])
            nodo.add_childrens(Node(p[3]))
            p[0] = nodo
        else:
            nodo.add_childrens(p[1])
            nodo.add_childrens(Node(p[2]))
            nodo.add_childrens(p[3])
            p[0] = nodo
    elif (len(p) == 2):
        nodo.add_childrens(p[1])
        p[0] = nodo
    
def p_where_aggregate(p):
    '''SELECTWHEREAGGREGATE : WHERECLAUSE  SELECTGROUPHAVING
                            | SELECTGROUPHAVING
                            | WHERECLAUSE'''
    nodo = Node('SELECTWHEREAGGREGATE')
    if (len(p) == 3):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        p[0] = nodo
    elif (len(p) == 2):
        nodo.add_childrens(p[1])
        p[0] = nodo

def p_select_group_having(p):
    '''SELECTGROUPHAVING : GROUPBYCLAUSE
                         | HAVINGCLAUSE GROUPBYCLAUSE
                         | GROUPBYCLAUSE HAVINGCLAUSE'''
    nodo = Node('SELECTGROUPHAVING')
    if (len(p) == 2):
        nodo.add_childrens(p[1])
        p[0] = nodo
    elif (len(p) == 3):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        p[0] = nodo


def p_table_reference(p):
    '''TABLEREFERENCE : OBJECTREFERENCE SQLALIAS
                      | OBJECTREFERENCE SQLALIAS JOINLIST
                      | OBJECTREFERENCE JOINLIST
                      | OBJECTREFERENCE'''
    nodo = Node('TABLEREFERENCE')
    if (len(p) == 2):
        nodo.add_childrens(p[1])
        p[0] = nodo
    elif (len(p) == 3):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        p[0] = nodo
    elif (len(p) == 4):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        nodo.add_childrens(p[3])
        p[0] = nodo


def p_order_by_clause(p):
    '''ORDERBYCLAUSE : ORDER BY ORDERBYCLAUSELIST'''
    nodo = Node('ORDERBYCLAUSE')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    p[0] = nodo

def p_order_by_clause_list(p):
    '''ORDERBYCLAUSELIST : ORDERBYCLAUSELIST COMMA ORDERBYEXPRESSION
                         | ORDERBYEXPRESSION'''
    nodo = Node('ORDERBYCLAUSELIST')
    if (len(p) == 4):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        p[0] = nodo
    elif (len(p) == 2):
        nodo.add_childrens(p[1])
        p[0] = nodo
   


def p_order_by_expression(p):
    '''ORDERBYEXPRESSION : SQLSIMPLEEXPRESSION ASC
                         | SQLSIMPLEEXPRESSION DESC
                         | SQLSIMPLEEXPRESSION'''
    nodo = Node('ORDERBYEXPRESSION')
    if (len(p) == 3):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        p[0] = nodo
    elif (len(p) == 2):
        nodo.add_childrens(p[1])
        p[0] = nodo

def p_limit_clause(p):
    '''LIMITCLAUSE : LIMIT LIMITOPTIONS'''
    nodo = Node('LIMITCLAUSE')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    p[0] = nodo

def p_limit_options(p):
    '''LIMITOPTIONS : LIMITTYPES OFFSETOPTION
                    | LIMITTYPES'''
    nodo = Node('LIMITOPTIONS')
    if (len(p) == 3):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        p[0] = nodo
    

def p_limit_types(p):
    '''LIMITTYPES : LISTLIMITNUMBER
                  | ALL'''
    nodo = Node('LIMITTYPES')
    if p[1] == 'ALL':
        nodo.add_childrens(Node(p[1]))
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        p[0] = p[1]
   

def p_list_limit_number(p):
    '''LISTLIMITNUMBER : LISTLIMITNUMBER COMMA INT_NUMBER
                       | INT_NUMBER'''
    nodo = Node('LISTLIMITNUMBER')
    if (len(p) == 2):
        nodo.add_childrens(Node(p[1]))
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        p[0] = nodo


def p_offset_option(p):
    '''OFFSETOPTION : OFFSET INT_NUMBER'''
    nodo = Node('OFFSETOPTION')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    p[0] = nodo

def p_where_clause(p):
    '''WHERECLAUSE : WHERE SQLEXPRESSION'''
    nodo = Node('WHERECLAUSE')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    p[0] = nodo


def p_group_by_clause(p):
    '''GROUPBYCLAUSE : GROUP BY SQLEXPRESSIONLIST'''
    nodo = Node('GROUPBYCLAUSE')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    p[0] = nodo


def p_having_clause(p):
    '''HAVINGCLAUSE : HAVING SQLEXPRESSION'''
    nodo = Node('HAVINGCLAUSE')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(p[2])
    p[0] = nodo


def p_join_list(p):
    '''JOINLIST : JOINLIST JOINP
                | JOINP'''
    nodo = Node('JOINLIST')
    if (len(p) == 2):
        nodo.add_childrens(p[1])
        p[0] = nodo
    elif (len(p) == 3):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        p[0] = nodo


def p_joinp(p):
    '''JOINP : JOINTYPE JOIN TABLEREFERENCE ON SQLEXPRESSION'''
    nodo = Node('JOINP')
    nodo.add_childrens(p[1])
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    nodo.add_childrens(p[5])
    p[0] = nodo


def p_join_type(p):
    '''JOINTYPE : INNER
                | LEFT OUTER
                | RIGHT OUTER
                | FULL OUTER'''
    nodo = Node('JOINTYPE')
    if (len(p) == 2):
        nodo.add_childrens(Node(p[1]))
        p[0] = nodo
    elif (len(p) == 3):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        p[0] = nodo


def p_sql_expression(p):
    '''SQLEXPRESSION : SQLEXPRESSION OR SQLEXPRESSION
                     | SQLEXPRESSION AND SQLEXPRESSION
                     | NOT EXISTSORSQLRELATIONALCLAUSE
                     | EXISTSORSQLRELATIONALCLAUSE'''
    nodo = Node('SQLEXPRESSION')
    if len(p) == 4:
       nodo.add_childrens(p[1])
       nodo.add_childrens(Node(p[2]))
       nodo.add_childrens(p[3])
       p[0] = nodo
    elif len(p) == 3:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        p[0] = nodo

def p_exits_or_relational_clause(p):
    '''EXISTSORSQLRELATIONALCLAUSE : EXISTSCLAUSE
                                   | SQLRELATIONALEXPRESSION'''
    nodo = Node('EXISTSORSQLRELATIONALCLAUSE')
    nodo.add_childrens(p[1])
    p[0] = nodo
    
def p_exists_clause(p):
    '''EXISTSCLAUSE : EXISTS LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS'''
    nodo = Node('EXISTSCLAUSE')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    p[0] = nodo


def p_sql_relational_expression(p):
    '''SQLRELATIONALEXPRESSION : SQLSIMPLEEXPRESSION RELOP SQLSIMPLEEXPRESSION
                               | SQLSIMPLEEXPRESSION SQLINCLAUSE
                               | SQLSIMPLEEXPRESSION SQLBETWEENCLAUSE
                               | SQLSIMPLEEXPRESSION SQLLIKECLAUSE
                               | SQLSIMPLEEXPRESSION SQLISCLAUSE
                               | SQLSIMPLEEXPRESSION'''
    nodo = Node('SQLRELATIONALEXPRESSION')
    if (len(p) == 3):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        p[0] = nodo
    elif (len(p) == 4):
        nodo.add_childrens(p[1])
        nodo.add_childrens(p[2])
        nodo.add_childrens(p[3])
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        p[0] = nodo



def p_sql_in_clause(p):
    '''SQLINCLAUSE  : NOT IN LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS
                    | IN LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS
                    | IN LEFT_PARENTHESIS LISTVALUESINSERT RIGHT_PARENTHESIS'''
    nodo = Node('SQLINCLAUSE')
    if (len(p) == 6):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.add_childrens(Node(p[5]))
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        p[0] = nodo


def p_sql_between_clause(p):
    '''SQLBETWEENCLAUSE : NOT BETWEEN SQLSIMPLEEXPRESSION AND SQLSIMPLEEXPRESSION
                        | NOT BETWEEN SYMMETRIC SQLSIMPLEEXPRESSION AND SQLSIMPLEEXPRESSION
                        | BETWEEN SQLSIMPLEEXPRESSION AND SQLSIMPLEEXPRESSION 
                        | BETWEEN SYMMETRIC SQLSIMPLEEXPRESSION AND SQLSIMPLEEXPRESSION '''
    nodo = Node('SQLBETWEENCLAUSE')
    if (len(p) == 6):
        if (p[3] == 'SYMMETRIC'):
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(Node(p[2]))
            nodo.add_childrens(p[3])
            nodo.add_childrens(Node(p[4]))
            nodo.add_childrens(p[5])
            p[0] = nodo
        else:
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(Node(p[2]))
            nodo.add_childrens(p[3])
            nodo.add_childrens(Node(p[4]))
            nodo.add_childrens(p[5])
            p[0] = nodo
    elif (len(p) == 5):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.add_childrens(Node(p[5]))
        nodo.add_childrens(p[6])
        p[0] = nodo

def p_sql_like_clause(p):
    '''SQLLIKECLAUSE  : NOT LIKE SQLSIMPLEEXPRESSION
                      | LIKE SQLSIMPLEEXPRESSION'''
    nodo = Node('SQLLIKECLAUSE')
    if (len(p) == 4):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        p[0] = nodo

def p_sql_is_clause(p):
    '''SQLISCLAUSE : IS NULL
                   | IS NOT NULL
                   | ISNULL
                   | NOTNULL
                   | IS TRUE
                   | IS NOT TRUE
                   | IS FALSE
                   | IS NOT FALSE
                   | IS UNKNOWN
                   | IS NOT UNKNOWN
                   | IS NOT DISTINCT FROM SQLNAME
                   | IS DISTINCT FROM SQLNAME'''
    nodo = Node('SQLISCLAUSE')
    if len(p) == 2:
        nodo.add_childrens(Node(p[1]))
        p[0] = nodo
    elif len(p) == 3:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        p[0] = nodo
    elif len(p) == 4:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        p[0] = nodo
    elif len(p) == 5:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        p[0] = nodo

def p_sql_simple_expression(p):
    '''SQLSIMPLEEXPRESSION : SQLSIMPLEEXPRESSION PLUS SQLSIMPLEEXPRESSION
                           | SQLSIMPLEEXPRESSION REST SQLSIMPLEEXPRESSION
                           | SQLSIMPLEEXPRESSION ASTERISK SQLSIMPLEEXPRESSION
                           | SQLSIMPLEEXPRESSION DIVISION SQLSIMPLEEXPRESSION
                           | SQLSIMPLEEXPRESSION EXPONENT SQLSIMPLEEXPRESSION
                           | SQLSIMPLEEXPRESSION MODULAR SQLSIMPLEEXPRESSION
                           | REST SQLSIMPLEEXPRESSION %prec UREST
                           | PLUS SQLSIMPLEEXPRESSION %prec UPLUS
                           | SQLSIMPLEEXPRESSION BITWISE_SHIFT_RIGHT SQLSIMPLEEXPRESSION
                           | SQLSIMPLEEXPRESSION BITWISE_SHIFT_LEFT SQLSIMPLEEXPRESSION
                           | SQLSIMPLEEXPRESSION BITWISE_AND SQLSIMPLEEXPRESSION
                           | SQLSIMPLEEXPRESSION BITWISE_OR SQLSIMPLEEXPRESSION
                           | SQLSIMPLEEXPRESSION BITWISE_XOR SQLSIMPLEEXPRESSION
                           | BITWISE_NOT SQLSIMPLEEXPRESSION %prec UREST
                           | LEFT_PARENTHESIS SQLEXPRESSION RIGHT_PARENTHESIS
                           | AGGREGATEFUNCTIONS
                           | GREATESTORLEAST
                           | EXPRESSIONSTIME
                           | SQUARE_ROOT SQLSIMPLEEXPRESSION
                           | CUBE_ROOT SQLSIMPLEEXPRESSION
                           | MATHEMATICALFUNCTIONS
                           | CASECLAUSE
                           | BINARY_STRING_FUNCTIONS
                           | TRIGONOMETRIC_FUNCTIONS
                           | SQLINTEGER
                           | OBJECTREFERENCE
                           | NULL
                           | TRUE
                           | FALSE'''
    nodo = Node('SQLSIMPLEEXPRESSION')
    if (len(p) == 4):
        if (p[1] == "("):
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(p[2])
            nodo.add_childrens(Node(p[3]))
            p[0] = nodo
        else:
            nodo.add_childrens(p[1])
            nodo.add_childrens(Node(p[2]))
            nodo.add_childrens(p[3])
            p[0] = nodo
    elif (len(p) == 3):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        p[0] = nodo
    else:
        if p[1] == 'NULL' or p[1] == 'TRUE' or p[1] == 'FALSE':
            nodo.add_childrens(Node(p[1]))
            p[0] = nodo
        else:
            nodo.add_childrens(p[1])
            p[0] = nodo


def p_sql_expression_list(p):
    '''SQLEXPRESSIONLIST : SQLEXPRESSIONLIST COMMA SQLEXPRESSION
                         | SQLEXPRESSION'''
    nodo = Node('SQLEXPRESSIONLIST')
    if (len(p) == 4):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        p[0] = nodo
    elif (len(p) == 2):
        nodo.add_childrens(p[1])
        p[0] = nodo

def p_mathematical_functions(p):
    '''MATHEMATICALFUNCTIONS : ABS LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS SQLALIAS
                             | ABS LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | CBRT LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS SQLALIAS
                             | CBRT LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | CEIL LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS SQLALIAS
                             | CEIL LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | CEILING LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS SQLALIAS
                             | CEILING LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | DEGREES LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS SQLALIAS
                             | DEGREES LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | DIV LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS SQLALIAS
                             | DIV LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | EXP LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS SQLALIAS
                             | EXP LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | FACTORIAL LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS SQLALIAS
                             | FACTORIAL LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | FLOOR LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS SQLALIAS
                             | FLOOR LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | GCD LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS SQLALIAS
                             | GCD LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | LN LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS SQLALIAS
                             | LN LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | LOG LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS SQLALIAS
                             | LOG LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | MOD LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS SQLALIAS
                             | MOD LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | PI LEFT_PARENTHESIS RIGHT_PARENTHESIS SQLALIAS
                             | PI LEFT_PARENTHESIS RIGHT_PARENTHESIS
                             | POWER LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS SQLALIAS
                             | POWER LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | RADIANS LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS SQLALIAS
                             | RADIANS LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | ROUND LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS SQLALIAS
                             | ROUND LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | SIGN LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS SQLALIAS
                             | SIGN LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | SQRT LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS SQLALIAS
                             | SQRT LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | WIDTH_BUCKET LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS SQLALIAS
                             | WIDTH_BUCKET LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | TRUNC LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS SQLALIAS
                             | TRUNC LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | RANDOM LEFT_PARENTHESIS RIGHT_PARENTHESIS SQLALIAS
                             | RANDOM LEFT_PARENTHESIS RIGHT_PARENTHESIS '''
    nodo = Node('MATHEMATICALFUNCTIONS')
    if (len(p) == 6):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        p[0] = nodo
    elif (len(p) == 5):
        if (p[1] == 'PI' or p[1] == 'RANDOM'):
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(Node(p[2]))
            nodo.add_childrens(Node(p[3]))
            nodo.add_childrens(p[4])
            p[0] = nodo
        else:
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(Node(p[2]))
            nodo.add_childrens(p[3])
            nodo.add_childrens(Node(p[4]))
            p[0] = nodo
    elif len(p) == 4:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        p[0] = nodo
    elif (len(p) == 8):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        nodo.add_childrens(Node(p[6]))
        nodo.add_childrens(p[7])
        p[0] = nodo
    elif (len(p) == 7):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        nodo.add_childrens(Node(p[6]))
        p[0] = nodo
    elif (len(p) == 12):
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
        nodo.add_childrens(p[11])
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
        p[0] = nodo

def p_binary_string_functions(p):
    '''BINARY_STRING_FUNCTIONS : LENGTH LEFT_PARENTHESIS ID RIGHT_PARENTHESIS
                               | SUBSTRING LEFT_PARENTHESIS  SQLNAME COMMA INT_NUMBER COMMA INT_NUMBER RIGHT_PARENTHESIS
                               | TRIM LEFT_PARENTHESIS ID RIGHT_PARENTHESIS
                               | MD5 LEFT_PARENTHESIS STRINGCONT RIGHT_PARENTHESIS
                               | SHA256 LEFT_PARENTHESIS STRINGCONT RIGHT_PARENTHESIS
                               | SUBSTR LEFT_PARENTHESIS SQLNAME COMMA INT_NUMBER COMMA INT_NUMBER RIGHT_PARENTHESIS
                               | CONVERT LEFT_PARENTHESIS SQLNAME AS DATE RIGHT_PARENTHESIS
                               | CONVERT LEFT_PARENTHESIS SQLNAME AS INTEGER RIGHT_PARENTHESIS
                               | DECODE LEFT_PARENTHESIS STRINGCONT COMMA STRINGCONT  RIGHT_PARENTHESIS'''
    nodo = Node('BINARY_STRING_FUNCTIONS')
    if len(p) == 9:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(Node(p[5]))
        nodo.add_childrens(Node(p[6]))
        nodo.add_childrens(Node(p[7]))
        nodo.add_childrens(Node(p[8]))
        p[0] = nodo
    elif len(p) == 7:
        if p[3] == 'STRINGCONT':
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(Node(p[2]))
            nodo.add_childrens(Node(p[3]))
            nodo.add_childrens(Node(p[4]))
            nodo.add_childrens(Node(p[5]))
            nodo.add_childrens(Node(p[6]))
            p[0] = nodo
        else:
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(Node(p[2]))
            nodo.add_childrens(p[3])
            nodo.add_childrens(Node(p[4]))
            nodo.add_childrens(Node(p[5]))
            nodo.add_childrens(Node(p[6]))
            p[0] = nodo
    elif len(p) == 5:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        p[0] = nodo

def p_greatest_or_least(p):
    '''GREATESTORLEAST : GREATEST LEFT_PARENTHESIS LISTVALUESINSERT RIGHT_PARENTHESIS
                       | LEAST LEFT_PARENTHESIS LISTVALUESINSERT RIGHT_PARENTHESIS'''
    nodo = Node('GREATESTORLEAST')
    nodo.add_childrens(Node(p[1]))
    nodo.add_childrens(Node(p[2]))
    nodo.add_childrens(p[3])
    nodo.add_childrens(Node(p[4]))
    p[0] = nodo

def p_case_clause(p):
    '''CASECLAUSE : CASE CASECLAUSELIST END ID
                  | CASE CASECLAUSELIST ELSE SQLSIMPLEEXPRESSION END ID'''
    nodo = Node('CASECLAUSE')
    if(len(p) == 5):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(Node(p[4]))
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        nodo.add_childrens(Node(p[5]))
        nodo.add_childrens(Node(p[6]))
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
        p[0] = nodo
    elif (len(p) == 7):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(p[3])
        nodo.add_childrens(p[4])
        nodo.add_childrens(Node(p[5]))
        nodo.add_childrens(p[6])
        p[0] = nodo
    elif (len(p) == 6):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        p[0] = nodo
    else: #len = 5
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        nodo.add_childrens(Node(p[3]))
        nodo.add_childrens(p[4])
        p[0] = nodo

def p_trigonometric_functions(p):
    '''TRIGONOMETRIC_FUNCTIONS : ACOS LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | ACOSD LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | ASIN LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | ASIND LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | ATAN LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | ATAND LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | ATAN2 LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | ATAN2D LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | COS LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | COSD LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | COT LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | COTD LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | SIN LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | SIND LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | TAN LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | TAND LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | COSH LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | SINH LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | TANH LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | ACOSH LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | ASINH LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | ATANH LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS'''
    nodo = Node('TRIGONOMETRIC_FUNCTIONS')
    if (len(p) == 5):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        nodo.add_childrens(Node(p[6]))
        p[0] = nodo

def p_sql_alias(p):
    '''SQLALIAS : AS SQLNAME
                | SQLNAME'''
    nodo = Node('SQLALIAS')
    if (len(p) == 3):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        p[0] = nodo
    elif (len(p) == 2):
        nodo.add_childrens(p[1])
        p[0] = nodo


def p_expressions_time(p):
    '''EXPRESSIONSTIME : EXTRACT LEFT_PARENTHESIS DATETYPES FROM TIMESTAMP SQLNAME RIGHT_PARENTHESIS
                       | NOW LEFT_PARENTHESIS RIGHT_PARENTHESIS
                       | DATE_PART LEFT_PARENTHESIS SQLNAME COMMA INTERVAL SQLNAME RIGHT_PARENTHESIS
                       | CURRENT_DATE
                       | CURRENT_TIME
                       | TIMESTAMP SQLNAME'''
    nodo = Node('EXPRESSIONSTIME')
    if (len(p) == 8):
        if (p[1] == 'EXTRACT'):
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(Node(p[2]))
            nodo.add_childrens(p[3])
            nodo.add_childrens(Node(p[4]))
            nodo.add_childrens(Node(p[5]))
            nodo.add_childrens(p[6])
            nodo.add_childrens(Node(p[7]))
            p[0] = nodo
        else:
            nodo.add_childrens(Node(p[1]))
            nodo.add_childrens(Node(p[2]))
            nodo.add_childrens(p[3])
            nodo.add_childrens(Node(p[4]))
            nodo.add_childrens(Node(p[5]))
            nodo.add_childrens(p[6])
            nodo.add_childrens(Node(p[7]))
            p[0] = nodo
    
    elif (len(p) == 3):
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(p[2])
        p[0] = nodo
    elif len(p) == 4:
        nodo.add_childrens(Node(p[1]))
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(Node(p[3]))
        p[0] = nodo
    else:
        nodo.add_childrens(Node(p[1]))
        p[0] = nodo

def p_aggregate_functions(p):
    '''AGGREGATEFUNCTIONS : AGGREGATETYPES LEFT_PARENTHESIS CONTOFAGGREGATE RIGHT_PARENTHESIS
                          | AGGREGATETYPES LEFT_PARENTHESIS CONTOFAGGREGATE RIGHT_PARENTHESIS SQLALIAS'''
    nodo = Node('AGGREGATEFUNCTIONS')
    if (len(p) == 5):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        p[0] = nodo

def p_cont_of_aggregate(p):
    '''CONTOFAGGREGATE : ASTERISK
                       | SQLSIMPLEEXPRESSION'''
    nodo = Node('CONTOFAGGREGATE')
    if (p[1] == '*'):
        nodo.add_childrens(Node(p[1]))
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        p[0] = nodo

def p_sql_object_reference(p):
    '''OBJECTREFERENCE : SQLNAME DOT SQLNAME DOT SQLNAME
                       | SQLNAME DOT SQLNAME
                       | SQLNAME DOT ASTERISK
                       | SQLNAME'''
    nodo = Node('OBJECTREFERENCE')
    if (len(p) == 2):
        nodo.add_childrens(p[1])
        p[0] = nodo
    elif (len(p) == 4):
        if (p[3] == '*'):
            nodo.add_childrens(p[1])
            nodo.add_childrens(Node(p[2]))
            nodo.add_childrens(Node(p[3]))
            p[0] = nodo
        else:
            nodo.add_childrens(p[1])
            nodo.add_childrens(Node(p[2]))
            nodo.add_childrens(p[3])
            p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        nodo.add_childrens(Node(p[4]))
        nodo.add_childrens(p[5])
        p[0] = nodo

def p_list_values_insert(p):
    '''LISTVALUESINSERT : LISTVALUESINSERT COMMA SQLSIMPLEEXPRESSION
                        | SQLSIMPLEEXPRESSION'''
    nodo = Node('LISTVALUESINSERT')
    if(len(p) == 4):
        nodo.add_childrens(p[1])
        nodo.add_childrens(Node(p[2]))
        nodo.add_childrens(p[3])
        p[0] = nodo
    else:
        nodo.add_childrens(p[1])
        p[0] = nodo
        

def p_type_combine_query(p):
    '''TYPECOMBINEQUERY : UNION
                        | INTERSECT
                        | EXCEPT'''
    nodo = Node('TYPECOMBINEQUERY')
    nodo.add_childrens(Node(p[1]))
    p[0] = nodo

def p_relop(p):
    '''RELOP : EQUALS 
             | NOT_EQUAL
             | GREATE_EQUAL
             | GREATE_THAN
             | LESS_THAN
             | LESS_EQUAL
             | NOT_EQUAL_LR'''
    nodo = Node('RELOP')
    nodo.add_childrens(Node(p[1]))
    p[0] = nodo


def p_aggregate_types(p):
    '''AGGREGATETYPES : AVG
                      | SUM
                      | COUNT
                      | MAX
                      | MIN'''
    nodo = Node('AGGREGATETYPES')
    nodo.add_childrens(Node(p[1]))
    p[0] = nodo


def p_date_types(p):
    '''DATETYPES : YEAR
                 | MONTH
                 | DAY
                 | HOUR
                 | MINUTE
                 | SECOND'''
    nodo = Node('DATETYPES')
    nodo.add_childrens(Node(p[1]))
    p[0] = nodo

def p_sql_integer(p):
    '''SQLINTEGER : INT_NUMBER
                  | FLOAT_NUMBER'''
    nodo = Node('SQLINTEGER')
    nodo.add_childrens(Node(p[1]))
    p[0] = nodo


def p_sql_name(p):
    '''SQLNAME : STRINGCONT
               | CHARCONT
               | ID'''
    nodo = Node('SQLNAME')
    nodo.add_childrens(Node(p[1]))
    p[0] = nodo


def p_type_select(p):
    '''TYPESELECT : ALL
                  | DISTINCT
                  | UNIQUE'''
    nodo = Node('TYPESELECT')
    nodo.add_childrens(Node(p[1]))
    p[0] = nodo

def p_sub_query(p):
    '''SUBQUERY : SELECTSTATEMENT'''
    nodo = Node('SUBQUERY')
    nodo.add_childrens(p[1])
    p[0] = nodo

def p_error(p):
    print('error xd')

parser = yacc.yacc()
def parse2(inpu):
    lexer = lex.lex()
    lexer.lineno = 1
    return parser.parse(inpu, lexer=lexer)
