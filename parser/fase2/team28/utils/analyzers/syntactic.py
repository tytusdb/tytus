# from generate_ast import GraficarAST
from models.Other.delete_function import DeleteFunction
from models.Indexes.indexes import AlterIndex, DropIndex, Indexes
from models.instructions.Expression.trigonometric_functions import ExpressionsTrigonometric
from models.instructions.Expression.extract_from_column import ExtractFromIdentifiers
from re import L

import libs.ply.yacc as yacc
import os
import json

from models.instructions.shared import *
from models.instructions.DDL.database_inst import *
from models.instructions.DDL.table_inst import *
from models.instructions.DDL.column_inst import *
from models.instructions.DDL.type_inst import *
from models.instructions.DML.dml_instr import *
from models.instructions.DML.select import *
from models.instructions.Expression.expression import *
from models.instructions.Expression.type_enum import *
from models.instructions.Expression.math_funcs import *
from models.instructions.Expression.string_funcs import *
from controllers.error_controller import ErrorController
from utils.analyzers.lex import *

from models.Other.funcion import Funcion, Parametro, ProcedimientoAlmacenado
from models.Other.declaracion import DeclaracionID, AsignacionID
from models.procedural.clases import BodyDeclaration, ReturnFuncProce
from models.procedural.if_statement import If,anidarIFs


# Precedencia, entre mayor sea el nivel mayor sera su inportancia para su uso

precedence = (
    ('left', 'OR'),  # Level 1
    ('left', 'AND'),  # Level 2
    ('right', 'NOT'),  # Level 3
    ('nonassoc', 'LESS_THAN', 'LESS_EQUAL', 'GREATE_THAN',
     'GREATE_EQUAL', 'EQUALS', 'NOT_EQUAL_LR', 'COLONEQUALS'),  # Level 4
    ('nonassoc', 'BETWEEN', 'IN', 'LIKE', 'ILIKE', 'SIMILAR'),  # Level 5
    ('left', 'SEMICOLON', 'LEFT_PARENTHESIS',
     'RIGHT_PARENTHESIS', 'COMMA', 'COLON', 'NOT_EQUAL'),  # Level 6
    ('left', 'PLUS', 'REST','CONCAT'),  # Level 7
    ('left', 'ASTERISK', 'DIVISION', 'MODULAR', 'BITWISE_SHIFT_RIGHT',
     'BITWISE_SHIFT_LEFT', 'BITWISE_AND', 'BITWISE_OR'),  # Level 8
    ('left', 'EXPONENT',  'BITWISE_XOR', 'SQUARE_ROOT', 'CUBE_ROOT'),  # Level 9
    ('right', 'UPLUS', 'UREST'),  # Level 10
    ('left', 'DOT')  # Level 13
)

contador_instr = 0
arr_instr = []
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
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]

    else:
        p[0] = [p[1]]


def p_sql_instruction(p):
    '''sqlinstruction : ddl
                      | DML
                      | SQL_FUNCTIONS
                      | SQL_DROP_FUNCTION
                      | SQL_DROP_PROCEDURE
                      | SQL_PROCEDURES
                      | usestatement
                      | MULTI_LINE_COMMENT
                      | SINGLE_LINE_COMMENT
                      | INDEXES_STATEMENT
                      | CALL_FUNCTIONS_PROCEDURE SEMICOLON
                      | error SEMICOLON
    '''
    global contador_instr, arr_instr
    p[0] = p[1]
    if p.slice[1].type != "error":
        contador_instr += 1
    # print("STRING PARA PASARLO: \n" + p[0]._tac)


def p_use_statement(p):
    '''usestatement : USE ID SEMICOLON'''
    noColumn = find_column(p.slice[1])
    noLine = p.slice[1].lineno
    p[0] = UseDatabase(p[2], generateC3D(p), noLine, noColumn)


def p_ddl(p):
    '''ddl : createstatement
           | showstatement
           | alterstatement
           | dropstatement
    '''
    p[0] = p[1]


def p_create_statement(p):
    '''createstatement : CREATE optioncreate SEMICOLON'''
    p[0] = p[2]
    p[0]._tac = f'CREATE {p[2]._tac};'

def p_option_create(p):
    '''optioncreate : TYPE SQLNAME AS ENUM LEFT_PARENTHESIS typelist RIGHT_PARENTHESIS
                    | DATABASE createdb
                    | OR REPLACE DATABASE createdb
                    | TABLE SQLNAME LEFT_PARENTHESIS columnstable RIGHT_PARENTHESIS
                    | TABLE SQLNAME LEFT_PARENTHESIS columnstable RIGHT_PARENTHESIS INHERITS LEFT_PARENTHESIS ID RIGHT_PARENTHESIS
    '''
    noColumn = find_column(p.slice[1])
    noLine = p.slice[1].lineno

    if len(p) == 8:
        p[0] = CreateType(p[2], p[6], generateC3D(p))

        string = ''
        for index, var in enumerate(p[6]):
            if index > 0: string += f', {var._tac}'
            else: string += f'{var._tac}'

        p[0]._tac = f"TYPE {p[2]._tac} AS ENUM ({string})"
        
    elif len(p) == 3:
        p[0] = CreateDB(p[2], False, generateC3D(p), noLine, noColumn)
        p[0]._tac = f"DATABASE {p[2]['_tac']} "
    elif len(p) == 5:
        p[0] = CreateDB(p[4], True, generateC3D(p), noLine, noColumn)
        p[0]._tac = f"OR REPLACE DATABASE {p[2]['_tac']} "

    elif len(p) == 6:
        p[0] = CreateTB(p[2], p[4], None, generateC3D(p))
        string = ''
        for index, var in enumerate(p[4]):
            if index > 0: string += f', {var._tac}'
            else: string += f'{var._tac}'

        p[0]._tac = f"TABLE {p[2]._tac} ({string}) "

    elif len(p) == 10:
        p[0] = CreateTB(p[2], p[4], p[8], generateC3D(p))
        string = ''
        for index, var in enumerate(p[4]):
            if index > 0: string += f', {var._tac}'
            else: string += f'{var._tac}'
        p[0]._tac = f"TABLE {p[2]._tac} ({string}) INHERITS ({p[8]})"

def p_type_list(p):
    '''typelist : typelist COMMA SQLNAME
                | SQLNAME '''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]

    else:
        p[0] = [p[1]]


def p_create_db(p):
    '''createdb : IF NOT EXISTS ID listpermits
                | IF NOT EXISTS ID
                | ID listpermits
                | ID 
    '''
    string = ''
    p[0] = {'if_not_exists': False, 'id': None, 'listpermits': [], '_tac': ''}

    if len(p) == 6: #IF NOT EXISTS ID listpermits
        p[0]['if_not_exists'] = True
        p[0]['id'] = p[4]
        p[0]['listpermits'] = p[5]
        for index, var in enumerate(p[5]):
            if index > 0: string += f', {var["_tac"]}'
            else: string += f'{var["_tac"]}'
        p[0]['_tac'] = f'IF NOT EXISTS {p[4]} {string}'

    elif len(p) == 5: #IF NOT EXISTS ID
        p[0]['if_not_exists'] = True
        p[0]['id'] = p[4]
        p[0]['_tac'] = f'IF NOT EXISTS {p[4]}'

    elif len(p) == 3: #ID listpermits
        p[0]['id'] = p[1]
        p[0]['listpermits'] = p[2]
        for index, var in enumerate(p[2]):
            if index > 0: string += f', {var["_tac"]}'
            else: string += f'{var["_tac"]}'
        p[0]['_tac'] = f'{p[1]} {string}'

    else: #ID
        p[0]['id'] = p[1]
        p[0]['_tac'] = f'{p[1]}'

def p_list_permits(p):
    '''listpermits : listpermits permits
                   | permits
    '''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]

    else:
        p[0] = [p[1]]


def p_permits(p):
    '''permits : OWNER EQUALS SQLNAME
               | OWNER SQLNAME
               | MODE EQUALS INT_NUMBER
               | MODE INT_NUMBER 
    '''
    if p[1].lower() == 'MODE'.lower():
        if len(p) == 4:
            p[0] = {'MODE': p[3], '_tac': f'MODE = {p[3]}'}
        else:
            p[0] = {'MODE': p[2], '_tac': f'MODE {p[2]}' }
    else:
        if len(p) == 4:
            p[0] = {'OWNER': p[3], '_tac': f'OWNER = {p[3]._tac}'}
        else:
            p[0] = {'OWNER': p[2], '_tac': f'OWNER {p[2]}'}


def p_columns_table(p):
    '''columnstable : columnstable COMMA column
                    | column
    '''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]

    else:
        p[0] = [p[1]]

def p_column(p):
    '''column : ID typecol optionscollist
              | ID typecol
              | UNIQUE LEFT_PARENTHESIS columnlist RIGHT_PARENTHESIS
              | PRIMARY KEY LEFT_PARENTHESIS columnlist RIGHT_PARENTHESIS
              | FOREIGN KEY LEFT_PARENTHESIS columnlist RIGHT_PARENTHESIS REFERENCES ID LEFT_PARENTHESIS columnlist RIGHT_PARENTHESIS
              | CONSTRAINT ID CHECK LEFT_PARENTHESIS conditionColumn RIGHT_PARENTHESIS
              | CHECK LEFT_PARENTHESIS conditionColumn RIGHT_PARENTHESIS
    '''
    string = ''
    if len(p) == 4:
        p[0] = CreateCol(p[1], p[2], p[3])
        for index, var in enumerate(p[3]):
                if index > 0: string += f' {var["_tac"]} '
                else: string += f'{var["_tac"]}'
        p[0]._tac = f'{p[1]} {p[2]._tac} {string}'

    elif len(p) == 3:
        p[0] = CreateCol(p[1], p[2], [{
            'default_value': None,
            'is_null': None,
            'constraint_unique': None,
            'unique': None,
            'constraint_check_condition': None,
            'check_condition': None,
            'pk_option': None,
            'fk_references_to': None
        }])
        p[0]._tac = f'{p[1]} {p[2]._tac} '

    elif len(p) == 5:
        if p[1].lower() == 'UNIQUE'.lower():
            for index, var in enumerate(p[3]):
                if index > 0: string += f', {var}'
                else: string += f'{var}'
            p[0] = Unique(p[3])
            p[0]._tac = f'UNIQUE ({string})'

        else:  # CHECK
            p[0] = Check(p[3])
            p[0]._tac = f'CHECK ({p[3]._tac})'

    elif len(p) == 6:
        p[0] = PrimaryKey(p[4])
        string = ''
        string2 = ''
        for index, var in enumerate(p[4]):
            if index > 0: string += f', {var}'
            else: string += f'{var}'
        p[0]._tac = f'PRIMARY KEY ({string})'
    elif len(p) == 11:
        string = ''
        string2 = ''
        for index, var in enumerate(p[4]):
            if index > 0: string += f', {var}'
            else: string += f'{var}'
        for index, var in enumerate(p[9]):
            if index > 0: string2 += f', {var}'
            else: string2 += f'{var}'
        p[0] = ForeignKey(p[4], p[7], p[9])
        p[0]._tac = f'FOREIGN KEY ({string}) REFERENCES {p[7]}({string2})'

    elif len(p) == 7:
        p[0] = Constraint(p[2], p[5])
        p[0]._tac = f'CONSTRAINT {p[2]} ({p[5]._tac})'


def p_type_col(p):
    '''typecol : BIGINT
               | BOOLEAN
               | CHAR
               | CHAR LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS
               | CHARACTER
               | CHARACTER LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS
               | CHARACTER VARYING
               | CHARACTER VARYING LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS
               | DATE
               | DECIMAL LEFT_PARENTHESIS INT_NUMBER COMMA INT_NUMBER RIGHT_PARENTHESIS
               | DECIMAL LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS
               | DOUBLE PRECISION
               | INTEGER
               | INTERVAL SQLNAME
               | MONEY
               | NUMERIC LEFT_PARENTHESIS INT_NUMBER COMMA INT_NUMBER RIGHT_PARENTHESIS
               | NUMERIC LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS
               | REAL
               | SMALLINT
               | TEXT
               | TIMESTAMP LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS
               | TIMESTAMP
               | TIME LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS
               | TIME
               | VARCHAR LEFT_PARENTHESIS INT_NUMBER RIGHT_PARENTHESIS
               | VARCHAR

    '''

    if p[1].lower() == 'BIGINT'.lower():
        p[0] = ColumnTipo(ColumnsTypes.BIGINT, None, None)
        p[0]._tac = f'{p[1]}'
    elif p[1].lower() == 'BOOLEAN'.lower():
        p[0] = ColumnTipo(ColumnsTypes.BOOLEAN, None, None)
        p[0]._tac = f'{p[1]}'
    elif p[1].lower() == 'CHAR'.lower():
        if len(p) == 2:
            p[0] = ColumnTipo(ColumnsTypes.CHAR, None, None)
            p[0]._tac = f'{p[1]}'
        else:
            p[0] = ColumnTipo(ColumnsTypes.CHAR, p[3], None)
            p[0]._tac = f"{p[1]}({p[3]})"
    elif p[1].lower() == 'CHARACTER'.lower():
        if len(p) == 6:
            p[0] = ColumnTipo(ColumnsTypes.CHARACTER_VARYING, p[4], None)
            p[0]._tac = f'{p[1]} {p[2]} {p[3]}{p[4]}{p[5]}'
        elif len(p) == 3:
            p[0] = ColumnTipo(ColumnsTypes.CHARACTER_VARYING, None, None)
            p[0]._tac = f'{p[1]} {p[2]}'
        elif len(p) == 5:
            p[0] = ColumnTipo(ColumnsTypes.CHARACTER, p[3], None)
            p[0]._tac = f'{p[1]} {p[2]}{p[3]}{p[4]}'
        else:
            p[0] = ColumnTipo(ColumnsTypes.CHARACTER, None, None)
            p[0]._tac = f'{p[1]}'

    elif p[1].lower() == 'DATE'.lower():
        p[0] = ColumnTipo(ColumnsTypes.DATE, None, None)
        p[0]._tac = f'{p[1]}'
    elif p[1].lower() == 'DECIMAL'.lower():
        if len(p) == 7:
            p[0] = ColumnTipo(ColumnsTypes.DECIMAL, p[3], p[5])
            p[0]._tac = f'{p[1]} {p[2]}{p[3]}{p[4]}{p[5]}{p[6]}'
        else:
            p[0] = ColumnTipo(ColumnsTypes.DECIMAL, p[3], None)
            p[0]._tac = f'{p[1]} {p[2]}{p[3]}{p[4]}'
    elif p[1].lower() == 'DOUBLE'.lower():
        p[0] = ColumnTipo(ColumnsTypes.DOUBLE_PRECISION, None, None)
        p[0]._tac = f'{p[1]} {p[2]}'

    elif p[1].lower() == 'INTEGER'.lower():
        p[0] = ColumnTipo(ColumnsTypes.INTEGER, None, None)
        p[0]._tac = f'{p[1]}'
    elif p[1].lower() == 'INTERVAL'.lower():
        p[0] = ColumnTipo(ColumnsTypes.INTERVAL, p[2], None)
        p[0]._tac = f'{p[1]} {p[2]._tac}'
    elif p[1].lower() == 'MONEY'.lower():
        p[0] = ColumnTipo(ColumnsTypes.MONEY, None, None)
        p[0]._tac = f'{p[1]}'
    elif p[1].lower() == 'NUMERIC'.lower():
        if len(p) == 7:
            p[0] = ColumnTipo(ColumnsTypes.NUMERIC, p[3], p[5])
            p[0]._tac = f'{p[1]} {p[2]}{p[3]}{p[4]}{p[5]}{p[6]}'
        else:
            p[0] = ColumnTipo(ColumnsTypes.NUMERIC, p[3], None)
            p[0]._tac = f'{p[1]} {p[2]}{p[3]}{p[4]}'

    elif p[1].lower() == 'REAL'.lower():
        p[0] = ColumnTipo(ColumnsTypes.REAL, None, None)
        p[0]._tac = f'{p[1]}'

    elif p[1].lower() == 'SMALLINT'.lower():
        p[0] = ColumnTipo(ColumnsTypes.SMALLINT, None, None)
        p[0]._tac = f'{p[1]}'

    elif p[1].lower() == 'TEXT'.lower():
        p[0] = ColumnTipo(ColumnsTypes.TEXT, None, None)
        p[0]._tac = f'{p[1]}'

    elif p[1].lower() == 'TIMESTAMP'.lower():
        if len(p) == 5:
            p[0] = ColumnTipo(ColumnsTypes.TIMESTAMP, p[3], None)
            p[0]._tac = f'{p[1]} {p[2]}{p[3]}{p[4]}'
        else:
            p[0] = ColumnTipo(ColumnsTypes.TIMESTAMP, None, None)
            p[0]._tac = f'{p[1]}'

    elif p[1].lower() == 'TIME'.lower():
        if len(p) == 5:
            p[0] = ColumnTipo(ColumnsTypes.TIME, p[3], None)
            p[0]._tac = f'{p[1]} {p[2]}{p[3]}{p[4]}'
        else:
            p[0] = ColumnTipo(ColumnsTypes.TIME, None, None)
            p[0]._tac = f'{p[1]}'

    elif p[1].lower() == 'VARCHAR'.lower():
        if len(p) == 5:
            p[0] = ColumnTipo(ColumnsTypes.VARCHAR, p[3], None)
            p[0]._tac = f'{p[1]} {p[2]}{p[3]}{p[4]}'
        else:
            p[0] = ColumnTipo(ColumnsTypes.VARCHAR, None, None)
            p[0]._tac = f'{p[1]}'


    # if len(p) == 2:
    #     p[0]._tac = p[1].upper()
    
    # elif p.slice[3].type == "VARYING":
    #     if len(p) == 3:
    #         p[0]._tac = 'CHARACTER VARYING'
    #     else:
    #         p[0]._tac = f'CHARACTER VARYING ({p[4]})'

    # elif p.slice[2].type == "INTERVAL":
    #     p[0]._tac = f'INTERVAL {p[3]._tac}'

    # elif p.slice[2].type == "DOUBLE":
    #     p[0]._tac = 'DOUBLE PRECISION'

    # elif len(p) == 5:
    #     p[0]._tac = f'{p[1].upper()}({p[3]})'

    # elif len(p) == 7:
    #     p[0]._tac = f'{p[1].upper()}({p[3]}, {p[5]})'


#TODO: TIPOS CON MAS PARAMETROS

def p_options_col_list(p):
    '''optionscollist : optionscollist optioncol
                      | optioncol
    '''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]

    else:
        p[0] = [p[1]]

def p_indexes_statement(p):
    '''INDEXES_STATEMENT : CREATE_INDEXES
                         | DROP_INDEXES SEMICOLON
                         | ALTER_INDEXES SEMICOLON'''
    if len(p) == 3:
        p[1]._tac = f'{p[1]._tac};'
        p[0] = p[1]
    else:
        p[0] = p[1]

def p_indexes_drop(p):
    '''DROP_INDEXES : DROP INDEX CONCURRENTLY IF EXISTS columnlist CASCADE
                    | DROP INDEX CONCURRENTLY IF EXISTS columnlist RESTRICT
                    | DROP INDEX IF EXISTS columnlist RESTRICT
                    | DROP INDEX IF EXISTS columnlist CASCADE
                    | DROP INDEX columnlist CASCADE
                    | DROP INDEX columnlist RESTRICT 
                    | DROP INDEX CONCURRENTLY IF EXISTS columnlist
                    | DROP INDEX CONCURRENTLY columnlist
                    | DROP INDEX IF EXISTS columnlist
                    | DROP INDEX columnlist'''
    string = ""
    if len(p) == 8:
        if p.slice[7].type == "CASCADE":
            p[0] = DropIndex(p[6], p.lineno(1), find_column(p.slice[1]))
        else:
            p[0] = DropIndex(p[6], p.lineno(1), find_column(p.slice[1]))
        for index, var in enumerate(p[6]):
                if index > 0: string += f', {var}'
                else: string += f'{var}'
        p[0]._tac = f'{p[1]} {p[2]} {p[3]} {p[4]} {p[5]} {string} {p[7]}'
    elif len(p) == 7:
        if p.slice[6].type == "CASCADE":
            for index, var in enumerate(p[5]):
                if index > 0: string += f', {var}'
                else: string += f'{var}'
            p[0] = DropIndex(p[5], p.lineno(1), find_column(p.slice[1]))
            p[0]._tac = f'{p[1]} {p[2]} {p[3]} {p[4]} {string} {p[6]}'
        elif p.slice[3].type == "CONCURRENTLY":
            for index, var in enumerate(p[6]):
                if index > 0: string += f', {var}'
                else: string += f'{var}'
            p[0] = DropIndex(p[6], p.lineno(1), find_column(p.slice[1]))
            p[0]._tac = f'{p[1]} {p[2]} {p[3]} {p[4]} {p[5]} {string}'
        else:
            for index, var in enumerate(p[5]):
                if index > 0: string += f', {var}'
                else: string += f'{var}'
            p[0] = DropIndex(p[5], p.lineno(1), find_column(p.slice[1]))
            p[0]._tac = f'{p[1]} {p[2]} {p[3]} {p[4]} {string} {p[6]}'
    elif len(p) == 6:
        for index, var in enumerate(p[5]):
                if index > 0: string += f', {var}'
                else: string += f'{var}'
        p[0] = DropIndex(p[5], p.lineno(1), find_column(p.slice[1]))
        p[0]._tac = f'{p[1]} {p[2]} {p[3]} {p[4]} {string}'
    elif len(p) == 5:
        if p.slice[4].type == "CASCADE":
            for index, var in enumerate(p[3]):
                if index > 0: string += f', {var}'
                else: string += f'{var}'
            p[0] = DropIndex(p[3], p.lineno(1), find_column(p.slice[1]))
            p[0]._tac = f'{p[1]} {p[2]} {string} {p[4]}'
        elif p.slice[3].type == "CONCURRENTLY":
            for index, var in enumerate(p[4]):
                if index > 0: string += f', {var}'
                else: string += f'{var}'
            p[0] = DropIndex(p[4], p.lineno(1), find_column(p.slice[1]))
            p[0]._tac = f'{p[1]} {p[2]} {p[3]} {string}'
        else:
            for index, var in enumerate(p[3]):
                if index > 0: string += f', {var}'
                else: string += f'{var}'
            p[0] = DropIndex(p[3], p.lineno(1), find_column(p.slice[1]))
            p[0]._tac = f'{p[1]} {p[2]} {string} {p[4]}'
            
    else:
        for index, var in enumerate(p[3]):
                if index > 0: string += f', {var}'
                else: string += f'{var}'
        p[0] = DropIndex(p[3], p.lineno(1), find_column(p.slice[1]))
        p[0]._tac = f"{p[1]} {p[2]} {string}"
    
def p_indexes_alter(p):
    '''ALTER_INDEXES : ALTER INDEX IF EXISTS ID RENAME TO ID
                     | ALTER INDEX ID RENAME TO ID
                     | ALTER INDEX IF EXISTS ID ALTER COLUMN ID body_cont_index
                     | ALTER INDEX ID ALTER COLUMN ID body_cont_index
                     | ALTER INDEX ID ALTER ID body_cont_index
                     | ALTER INDEX IF EXISTS ID ALTER ID body_cont_index'''
    if len(p) == 9:
        if p.slice[6].type == "ALTER":
            p[0] = AlterIndex(p[5], p[7], p.lineno(1), find_column(p.slice[1]), True, p[8])
            p[0]._tac = f'{p[1]} {p[2]} {p[3]} {p[4]} {p[5]} {p[6]} {p[7]} {p[8]}'
        else:
            p[0] = AlterIndex(p[5], p[8], p.lineno(1), find_column(p.slice[1]), False, None)
            p[0]._tac = f'{p[1]} {p[2]} {p[3]} {p[4]} {p[5]} {p[6]} {p[7]} {p[8]}'
    elif len(p) == 10:
        p[0] = AlterIndex(p[5], p[8], p.lineno(1), find_column(p.slice[1]), True, p[9])
        p[0]._tac = f'{p[1]} {p[2]} {p[3]} {p[4]} {p[5]} {p[6]} {p[7]} {p[8]} {p[9]}'
    elif len(p) == 7:
        p[0] = AlterIndex(p[3], p[5], p.lineno(1), find_column(p.slice[1]), True, p[6])
        p[0]._tac = f'{p[1]} {p[2]} {p[3]} {p[4]} {p[5]} {p[6]}'
    elif len(p) == 8:
        p[0] = AlterIndex(p[3], p[6], p.lineno(1), find_column(p.slice[1]), True, p[7])
        p[0]._tac = f'{p[1]} {p[2]} {p[3]} {p[4]} {p[5]} {p[6]} {p[7]}'
    else:
        p[0] = AlterIndex(p[3], p[6], p.lineno(1), find_column(p.slice[1]), False, None)
        p[0]._tac = f'{p[1]} {p[2]} {p[3]} {p[4]} {p[5]} {p[6]}'
def p_index_alter_body(p):
    '''body_cont_index : ID
                       | INT_NUMBER'''
    p[0] = p[1]

def p_indexes_create(p):
                            #1      #2       #3 #4 #5      #6               #7           #8           #9                #10       #11      
    '''CREATE_INDEXES    : CREATE TYPE_INDEX ID ON ID OPTIONS1_INDEXES LEFT_PARENTHESIS BODY_INDEX RIGHT_PARENTHESIS WHERECLAUSE SEMICOLON
                         | CREATE TYPE_INDEX ID ON ID OPTIONS1_INDEXES LEFT_PARENTHESIS BODY_INDEX RIGHT_PARENTHESIS  SEMICOLON
                         | CREATE TYPE_INDEX ID ON ID LEFT_PARENTHESIS BODY_INDEX RIGHT_PARENTHESIS  WHERECLAUSE SEMICOLON
                         | CREATE TYPE_INDEX ID ON ID LEFT_PARENTHESIS BODY_INDEX RIGHT_PARENTHESIS SEMICOLON 
    '''
    string = ''
    lista_valores = []
    
    if len(p) == 10:
        count = 0
        for lista, var in p[7]:
            for ids in lista:
                lista_valores.append(ids)
            if count > 0: string += f', {var}'
            else: string += f'{var}'
            count += 1 
        p[0] = Indexes(p[2]["value"],p[5], p[3], None, lista_valores, None, p.lineno(1), find_column(p.slice[1]))
        p[0]._tac = f'{p[1]} {p[2]["_tac"]} {p[3]} {p[4]} {p[5]} {p[6]}{string}{p[8]};'
    elif len(p) == 11:
        if p.slice[6].type == "LEFT_PARENTHESIS":
            count = 0
            for lista, var in p[7]:
                for ids in lista:
                    lista_valores.append(ids)
                if count > 0: string += f', {var}'
                else: string += f'{var}'
                count += 1 
            p[0] = Indexes(p[2]["value"], p[5], p[3], None, lista_valores, p[9], p.lineno(1), find_column(p.slice[1]))
            p[0]._tac = f'{p[1]} {p[2]["_tac"]} {p[3]} {p[4]} {p[5]} {p[6]}{string}{p[8]} {p[9]._tac};'
        else:
            count = 0
            for lista, var in p[8]:
                for ids in lista:
                    lista_valores.append(ids)
                if count > 0: string += f', {var}'
                else: string += f'{var}'
                count += 1
            p[0] = Indexes(p[2]["value"], p[5], p[3], p[6]["value"], lista_valores, None, p.lineno(1), find_column(p.slice[1]))
            p[0]._tac = f'{p[1]} {p[2]["_tac"]} {p[3]} {p[4]} {p[5]} {p[6]["_tac"]} {p[7]}{string}{p[9]};'
    else:
        count = 0
        for lista, var in p[8]:
            for ids in lista:
                lista_valores.append(ids)
            if count > 0: string += f', {var}'
            else: string += f'{var}'
            count += 1
        p[0] = Indexes(p[2]["value"], p[5], p[3], p[6]["value"], lista_valores, p[10], p.lineno(1), find_column(p.slice[1]))
        p[0]._tac = f"{p[1]} {p[2]['_tac']} {p[3]} {p[4]} {p[5]} {p[6]['_tac']} {p[7]}{string}{p[9]} {p[10]._tac};"
def p_type_index(p):
    ''' TYPE_INDEX : INDEX
                   | UNIQUE INDEX
    '''
    
    if len(p) == 2:
        valores = {'value': p[1], '_tac': f'{p[1]}'}
        p[0] = valores
    else:
        valores = {'value': p[1], '_tac': f'{p[1]} {p[2]}'}
        p[0] = valores

def p_options1_indexes(p):
    ''' OPTIONS1_INDEXES : USING TYPE_MODE_INDEX
    '''
    valores = {'value': p[2], '_tac': f'{p[1]} {p[2]}'}
    p[0] = valores

def p_type_mode_index(p):
    ''' TYPE_MODE_INDEX : BTREE 
                        | HASH
    '''
    p[0] = p[1]

def p_body_index(p):
    ''' BODY_INDEX : BODY_INDEX COMMA BODY_INDEX_AUX 
                   | BODY_INDEX_AUX
    '''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    elif len(p) == 2:
        p[0] = [p[1]]

def p_body_index_aux(p):
    '''BODY_INDEX_AUX : ID OPTIONS2_INDEXES
                      | LOWER LEFT_PARENTHESIS ID RIGHT_PARENTHESIS
                      | LOWER LEFT_PARENTHESIS ID RIGHT_PARENTHESIS OPTIONS2_INDEXES
                      | ID'''
    string = ''
    if len(p) == 6:
        string = f'{p[1]}{p[2]}{p[3]}{p[4]} {p[5][1]}'
        p[0] = [[p[3], p[5][0]], string]
    elif len(p) == 5:
        string = f'{p[1]}{p[2]}{p[3]}{p[4]}'
        p[0] = [[p[3]], string]
    elif len(p) == 3:
        string = f'{p[1]} {p[2][1]}'
        p[0] = [[p[1], p[2][0]], string]
    elif len(p) == 2:
        string = f'{p[1]}'
        p[0] = [[p[1]], string]

def p_options2_indexes(p):
    '''  OPTIONS2_INDEXES : ASC NULLS FIRST 
                          | DESC NULLS LAST
                          | NULLS FIRST
                          | NULLS LAST
                          | ASC
                          | DESC
    '''
    string = ''
    if len(p) == 4:
        string = f'{p[1]} {p[2]} {p[3]}'
        if p.slice[1].type == 'ASC':
            p[0] = [False, string]
        else:
            p[0] = [True, string]
    elif len(p) == 3:
        string = f'{p[1]} {p[2]}'
        if p.slice[2].type == 'FIRST':
            p[0] = [True, string]
        else:
            p[0] = [False, string]
    else:
        string = f'{p[1]}'
        if p.slice[1].type == 'ASC':
            p[0] = [False, string]
        else:
            p[0] = [True, string]

def p_call_functions_or_procedure(p):
    '''CALL_FUNCTIONS_PROCEDURE : ID LEFT_PARENTHESIS LISTVALUESINSERT  RIGHT_PARENTHESIS
                                | ID LEFT_PARENTHESIS  RIGHT_PARENTHESIS 
                                | EXECUTE ID LEFT_PARENTHESIS  RIGHT_PARENTHESIS 
                                | EXECUTE ID LEFT_PARENTHESIS LISTVALUESINSERT  RIGHT_PARENTHESIS '''
    noColumn = find_column(p.slice[1])
    noLine = p.slice[1].lineno
    if p.slice[1].type == 'EXECUTE':
        if len(p) == 5: #Tercera produccion
            p[0] = Funcion(p[2], [], [], None, False, True, noLine, noColumn)
            p[0]._tac = f"{p[2]}()"
        else:           #Cuarta produccion
            p[0] = Funcion(p[2], p[4], [], None, False, True, noLine, noColumn)
            string = ''
            for index, var in enumerate(p[4]):
                if index > 0: string += f', {var._tac}'
                else: string += f'{var._tac}'
            p[0]._tac = f"{p[2]}({string})"   
    else:
        if len(p) == 5: #Primera produccion
            p[0] = Funcion(p[1], p[3], [], None, False, True, noLine, noColumn)
            string = ''
            for index, var in enumerate(p[3]):
                if index > 0: string += f', {var._tac}'
                else: string += f'{var._tac}'
            p[0]._tac = f"{p[1]}({string})" 
        else:           #Segunda produccion
            p[0] = Funcion(p[1], [], [], None, False, True, noLine, noColumn)
            p[0]._tac = f"{p[1]}()"

def p_option_col(p):  # TODO verificar
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
    p[0] = {
        'default_value': None,
        'is_null': None,
        'constraint_unique': None,
        'unique': None,
        'constraint_check_condition': None,
        'check_condition': None,
        'pk_option': None,
        'fk_references_to': None,
        '_tac': ''
    }
    if p[1].lower() == 'DEFAULT'.lower():
        p[0]['default_value'] = p[2]
        p[0]['_tac'] = f'{p[1]} {p[2]._tac}'
    elif p[1].lower() == 'NOT'.lower():
        p[0]['is_null'] = False
        p[0]['_tac'] = f'{p[1]} {p[2]}'
    elif p[1].lower() == 'NULL'.lower():
        p[0]['is_null'] = True
        p[0]['_tac'] = f'{p[1]}'
    elif p[1].lower() == 'CONSTRAINT'.lower() and len(p) == 4:
        p[0]['constraint_unique'] = p[2]
        p[0]['_tac'] = f'{p[1]} {p[2]} {p[3]}'
    elif p[1].lower() == 'UNIQUE'.lower():
        p[0]['unique'] = True
        p[0]['_tac'] = f'{p[1]}'
    elif p[1].lower() == 'CONSTRAINT'.lower() and len(p) == 7:
        p[0]['constraint_check_condition'] = p[5]
        p[0]['_tac'] = f'{p[1]} {p[2]} {p[3]} {p[4]} {p[5]._tac} {p[6]}'
    elif p[1].lower() == 'CHECK'.lower():
        p[0]['check_condition'] = p[3]
        p[0]['_tac'] = f'{p[1]} {p[2]} {p[3]._tac} {p[4]}'
    elif p[1].lower() == 'PRIMARY'.lower():
        p[0]['pk_option'] = True
        p[0]['_tac'] = f'{p[1]} {p[2]}'
    elif p[1].lower() == 'REFERENCES'.lower():
        p[0]['fk_references_to'] = p[2]
        p[0]['_tac'] = f'{p[1]} {p[2]}'


def p_condition_column(p):
    '''conditionColumn : conditioncheck'''
    p[0] = p[1]


def p_condition_check(p):
    '''conditioncheck : SQLRELATIONALEXPRESSION
    '''
    p[0] = p[1]


def p_column_list(p):
    '''columnlist : columnlist COMMA ID
                  | ID
    '''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]

    else:
        p[0] = [p[1]]


def p_show_statement(p):
    '''showstatement : SHOW DATABASES SEMICOLON
                     | SHOW DATABASES LIKE SQLNAME SEMICOLON
    '''
    if len(p) == 4:
        p[0] = ShowDatabase(None, generateC3D(p))
        p[0]._tac = f'{p[1]} {p[2]} {p[3]}'
    else:
        p[0] = ShowDatabase(p[4], generateC3D(p))
        p[0]._tac = f'{p[1]} {p[2]} {p[3]} {p[4]._tac} {p[5]}'
        


def p_alter_statement(p):
    '''alterstatement : ALTER optionsalter SEMICOLON
    '''
    string = f'{p[1]} {p[2]._tac};'
    p[2]._tac = string
    p[0] = p[2]


def p_options_alter(p):
    '''optionsalter : DATABASE alterdatabase
                    | TABLE altertable
    '''
    p[0] = p[2]


def p_alter_database(p):
    '''alterdatabase : ID RENAME TO ID
                     | ID OWNER TO typeowner
    '''
    noColumn = find_column(p.slice[1])
    noLine = p.slice[1].lineno
    if p[2].lower() == 'RENAME'.lower():  # Renombra la base de datos
        p[0] = AlterDatabase(1, p[1], p[4], generateC3D(p), noLine, noColumn)
        p[0]._tac = f'{p[1]} {p[2]} {p[3]} {p[4]}'
    else:  # Le cambia el duenio a la base de datos
        p[0] = AlterDatabase(2, p[1], p[4], generateC3D(p), noLine, noColumn)
        p[0]._tac = f'{p[1]} {p[2]} {p[3]} {p[4]}'


def p_type_owner(p):
    '''typeowner : ID
                 | CURRENT_USER
                 | SESSION_USER 
    '''
    p[0] = p[1]


def p_alter_table(p):
    '''altertable : ID alterlist
    '''
    string = ''
    for index, var in enumerate(p[2]):
            if index > 0: string += f', {var._tac}'
            else: string += f'{var._tac}'
    p[0] = AlterTable(p[1], p[2], generateC3D(p))
    p[0]._tac = f'TABLE {p[1]} {string}'


def p_alter_list(p):
    '''alterlist : alterlist COMMA typealter
                 | typealter
    '''
    if(len(p) == 4):
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]


def p_type_alter(p):
    '''typealter : ADD addalter
                 | ALTER alteralter
                 | DROP dropalter
                 | RENAME  renamealter
    '''
    string_viejo = p[2]._tac
    p[2]._tac = f'{p[1]} {string_viejo}'
    p[0] = p[2]
    


def p_add_alter(p):
    '''addalter : COLUMN ID typecol
                | CHECK LEFT_PARENTHESIS conditionColumn RIGHT_PARENTHESIS
                | CONSTRAINT ID UNIQUE LEFT_PARENTHESIS ID RIGHT_PARENTHESIS
                | FOREIGN KEY LEFT_PARENTHESIS columnlist RIGHT_PARENTHESIS REFERENCES ID LEFT_PARENTHESIS columnlist RIGHT_PARENTHESIS
    '''
    column_list = ''
    string = ""
    string2 = ""
    if len(p) == 4:
        p[0] = AlterTableAdd(CreateCol(p[2], p[3], [{
            'default_value': None,
            'is_null': None,
            'constraint_unique': None,
            'unique': None,
            'constraint_check_condition': None,
            'check_condition': None,
            'pk_option': None,
            'fk_references_to': None
        }]))
        p[0]._tac = f'{p[1]} {p[2]} {p[3]._tac}'
    elif len(p) == 5:   
        p[0] = AlterTableAdd(Check(p[3]))
        p[0]._tac = f'{p[1]} {p[2]} {p[3]._tac} {p[4]} '
    elif len(p) == 7:
        # TODO revisar esta asignacion
        p[0] = AlterTableAdd(Constraint(p[2], Unique(p[5])))
        p[0]._tac = f'{p[1]} {p[2]} {p[3]} {p[4]} {p[5]} {p[6]} '
    else:
        for index, var in enumerate(p[4]):
            if index > 0: string += f', {var}'
            else: string += f'{var}'
        for index, var in enumerate(p[9]):
            if index > 0: string2 += f', {var}'
            else: string2 += f'{var}'
        p[0] = AlterTableAdd(ForeignKey(p[4], p[7], p[9]))
        p[0]._tac = f'{p[1]} {p[2]} {p[3]} {string} {p[5]} {p[6]} {p[7]} {p[8]} {string2} {p[10]} '

def p_alter_alter(p):
    '''alteralter : COLUMN ID SET NOT NULL
                  | COLUMN ID TYPE typecol
    '''
    if len(p) == 6:
        p[0] = AlterTableAlter(
            {'change': 'not_null', 'id_column': p[2], 'type': None})
        p[0]._tac = f'{p[1]} {p[2]} {p[3]} {p[4]} {p[5]}'
    else:
        p[0] = AlterTableAlter(
            {'change': 'type_column', 'id_column': p[2], 'type': p[4]})
        p[0]._tac = f'{p[1]} {p[2]} {p[3]} {p[4]._tac}'


def p_drop_alter(p):
    '''dropalter : COLUMN ID
                 | CONSTRAINT ID
    '''
    if p[1].lower() == 'COLUMN'.lower():
        p[0] = AlterTableDrop({'change': 'column', 'id': p[2]})
        p[0]._tac = f'{p[1]} {p[2]}'
    else:
        p[0] = AlterTableDrop({'change': 'constraint', 'id': p[2]})
        p[0]._tac = f'{p[1]} {p[2]}'


def p_rename_alter(p):
    '''renamealter : COLUMN ID TO ID
    '''
    p[0] = AlterTableRename(p[2], p[4])
    p[0]._tac = f'{p[1]} {p[2]} {p[3]} {p[4]}'


def p_drop_statement(p):
    '''dropstatement : DROP optionsdrop SEMICOLON'''
    string_viejo = p[2]._tac
    p[2]._tac = f'{p[1]} {string_viejo};'
    p[0] = p[2]


def p_options_drop(p):
    '''optionsdrop : DATABASE dropdatabase
                   | TABLE droptable
    '''
    string_viejo = p[2]._tac
    p[2]._tac = f'{p[1]} {string_viejo}'
    p[0] = p[2]


def p_drop_database(p):
    '''dropdatabase : IF EXISTS ID
                    | ID
    '''
    noColumn = find_column(p.slice[1])
    noLine = p.slice[1].lineno
    if len(p) == 4:
        p[0] = DropDB(True, p[3], generateC3D(p), noLine, noColumn)
        p[0]._tac = f'{p[1]} {p[2]} {p[3]}'
    else:
        p[0] = DropDB(False, p[1], generateC3D(p), noLine, noColumn)
        p[0]._tac = f'{p[1]}'

def p_drop_table(p):
    '''droptable : ID
    '''
    noColumn = find_column(p.slice[1])
    noLine = p.slice[1].lineno
    p[0] = DropTB(p[1], generateC3D(p), noLine, noColumn)
    p[0]._tac = f'{p[1]}'


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def p_sql_functions(p):
    '''SQL_FUNCTIONS : CREATE FUNCTION ID LEFT_PARENTHESIS LIST_ARGUMENT RIGHT_PARENTHESIS RETURNS typeReturns AS bodyBlock LANGUAGE PLPGSQL SEMICOLON
                     | CREATE FUNCTION ID LEFT_PARENTHESIS RIGHT_PARENTHESIS  RETURNS typeReturns AS bodyBlock LANGUAGE PLPGSQL SEMICOLON
                     | CREATE FUNCTION ID LEFT_PARENTHESIS LIST_ARGUMENT RIGHT_PARENTHESIS  AS bodyBlock LANGUAGE PLPGSQL SEMICOLON
                     | CREATE FUNCTION ID LEFT_PARENTHESIS RIGHT_PARENTHESIS AS bodyBlock LANGUAGE PLPGSQL SEMICOLON
    '''
    noColumn = find_column(p.slice[1])
    noLine = p.slice[1].lineno
    if len(p) == 14:
        p[0] = Funcion(p[3], p[5], p[10], p[8], True, False, noLine, noColumn)
    elif len(p) == 13:
        p[0] = Funcion(p[3], [], p[9], p[7], True, False, noLine, noColumn)
    elif len(p) == 12:
        p[0] = Funcion(p[3], [5], p[8], None, True, False, noLine, noColumn)
    else:
        p[0] = Funcion(p[3], [], p[7], None, True, False, noLine, noColumn)

#--->

def p_sql_functions_drop_inst(p):
    '''SQL_DROP_FUNCTION : DROP FUNCTION IF EXISTS DETAIL_FUNC_DROP SEMICOLON
                        | DROP FUNCTION DETAIL_FUNC_DROP SEMICOLON
    '''
    string = ''
    if len(p) == 7:
        for index, var in enumerate(p[5]):
            if index > 0: string += f', {var["_tac"]}'
            else: string += f'{var["_tac"]}'
        p[0] = DeleteFunction(p[5], True, p.lineno(1), find_column(p.slice[1]))
        p[0]._tac = f'{p[1]} {p[2]} {p[3]} {p[4]} {string};'
    else:
        for index, var in enumerate(p[3]):
            if index > 0: string += f', {var["_tac"]}'
            else: string += f'{var["_tac"]}'
        p[0] = DeleteFunction(p[3], False, p.lineno(1), find_column(p.slice[1]))
        p[0]._tac = f'{p[1]} {p[2]} {string};'

def p_sql_procedures_drop_inst(p):
    '''SQL_DROP_PROCEDURE : DROP PROCEDURE IF EXISTS DETAIL_FUNC_DROP SEMICOLON
                          | DROP PROCEDURE DETAIL_FUNC_DROP SEMICOLON
    '''
    string = ''
    if len(p) == 7:
        for index, var in enumerate(p[5]):
            if index > 0: string += f', {var["_tac"]}'
            else: string += f'{var["_tac"]}'

        p[0] = DeleteFunction(p[5], True, p.lineno(1), find_column(p.slice[1]))
        p[0]._tac = f'{p[1]} {p[2]} {p[3]} {p[4]} {string};'
    else:
        for index, var in enumerate(p[3]):
            if index > 0: string += f', {var["_tac"]}'
            else: string += f'{var["_tac"]}'
        p[0] = DeleteFunction(p[3], False, p.lineno(1), find_column(p.slice[1]))
        p[0]._tac = f'{p[1]} {p[2]} {string};'

def p_sql_detail_func_drop(p):
    '''DETAIL_FUNC_DROP : DETAIL_FUNC_DROP COMMA FUNCTIONS_TO_DROP
                         | FUNCTIONS_TO_DROP
    '''
    if(len(p) == 4):
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_sql_functions_to_drop(p):
    '''FUNCTIONS_TO_DROP : ID LEFT_PARENTHESIS LIST_ARGUMENT RIGHT_PARENTHESIS
                         | ID LEFT_PARENTHESIS  RIGHT_PARENTHESIS
                         | ID
    '''
    if len(p) == 2:
        p[1] = {'value': p[1], '_tac': f'{p[1]}'}
        p[0] = p[1]
    elif len(p) == 4:
        p[1] = {'value': p[1], '_tac': f'{p[1]}{p[2]}{p[3]}'}
        p[0] = p[1]
    elif len(p) == 5:
        string = ''
        for index, var in enumerate(p[3]):
                if hasattr(var, '_tac'):
                    if index > 0: string += f', {var._tac}'
                    else: string += f'{var._tac}'
        p[1] = {'value': p[1], '_tac': f'{p[1]}{p[2]}{string}{p[4]}'}


#--->


def p_sql_procedures(p):
    '''SQL_PROCEDURES : CREATE PROCEDURE ID LEFT_PARENTHESIS LIST_ARGUMENT RIGHT_PARENTHESIS LANGUAGE PLPGSQL AS bodyBlock
                      | CREATE PROCEDURE ID LEFT_PARENTHESIS RIGHT_PARENTHESIS LANGUAGE PLPGSQL AS bodyBlock
    '''
    noColumn = find_column(p.slice[1])
    noLine = p.slice[1].lineno
    if len(p) == 11:
        p[0] = ProcedimientoAlmacenado(p[3], p[5], p[10], True, False, noLine, noColumn)
    else:
        p[0] = ProcedimientoAlmacenado(p[3], [], p[9], True, False, noLine, noColumn)

def p_returns_type_func(p):
    '''typeReturns : typecol
                   | VOID
                   | TABLE LEFT_PARENTHESIS LIST_ARGUMENT RIGHT_PARENTHESIS
    '''
    p[0] = p[1]

def p_list_argument(p):
    '''LIST_ARGUMENT : LIST_ARGUMENT COMMA param
                     | param
    '''
    if(len(p) == 4):
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_param(p):
    '''param : ID typecol
             | typecol
             | VARIADIC ID typecol
             | ID ID
    '''
    noColumn = find_column(p.slice[1])
    noLine = p.slice[1].lineno
    if(len(p) == 3):
        p[0] = Parametro(p[1], p[2], noLine, noColumn)
    if len(p) == 3:
        p[0]._tac = f'{p[1]} {p[2]._tac}'
    elif len(p) == 2:
        p[0]._tac = f'{p[1]._tac}'

def p_body_block(p):
    '''bodyBlock : DOUBLE_DOLLAR BODY_DECLARATION DOUBLE_DOLLAR
                 | DOLLAR SQLNAME DOLLAR BODY_DECLARATION DOLLAR SQLNAME DOLLAR
    '''
    if(len(p) == 4):
        p[0] = p[2]
    else:
        p[0] = p[4]


def p_body_declaration(p):
    '''BODY_DECLARATION : headerBodyList BEGIN STATEMENTS END ID SEMICOLON 
                        | headerBodyList BEGIN STATEMENTS EXCEPTION bodyExceptionList END ID SEMICOLON
                        | headerBodyList BEGIN STATEMENTS END SEMICOLON
                        | headerBodyList BEGIN STATEMENTS EXCEPTION bodyExceptionList END SEMICOLON
                        | BEGIN STATEMENTS END ID SEMICOLON
                        | BEGIN STATEMENTS EXCEPTION bodyExceptionList END ID SEMICOLON
                        | BEGIN STATEMENTS END SEMICOLON
                        | BEGIN STATEMENTS EXCEPTION bodyExceptionList END SEMICOLON
    '''
    if p.slice[1].type == "BEGIN":
        p[0] = BodyDeclaration(None, p[2])
    else:
        p[0] = BodyDeclaration(p[1], p[3])

    # p[0] = "CUERPO DE INSTRUCCIONES"
    # print(p.slice)

def p_header_body_list(p):
    '''headerBodyList : headerBodyList header
                      | header
    '''
    if p.slice[1].type == "headerBodyList":
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]
        if len(p[0]) == 1:
            p[0] = p[0][0]

def p_header(p):
    '''header : BITWISE_SHIFT_LEFT ID BITWISE_SHIFT_RIGHT
              | DECLARE declarationsList
    '''
    if p.slice[1].type == "DECLARE":
        p[0] = p[2]

def p_declarations_list(p):
    '''declarationsList : declarationsList SQL_VAR_DECLARATIONS
                        | SQL_VAR_DECLARATIONS
    '''
    if p.slice[1].type == "declarationsList":
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_sql_var_declarations(p):
    '''SQL_VAR_DECLARATIONS : ID CONSTANT typeDeclare detailDeclaration SEMICOLON
                            | ID CONSTANT typeDeclare SEMICOLON
                            | ID typeDeclare detailDeclaration SEMICOLON
                            | ID typeDeclare SEMICOLON
                            | ID ALIAS FOR DOLLAR SQLINTEGER SEMICOLON
    '''
    if len(p) == 5:
        p[0] = DeclaracionID(p[1], p[2], p[3],find_column(p.slice[1]), p.slice[1].lineno)
    elif len(p) == 4:
        p[0] = DeclaracionID(p[1], p[2], None,find_column(p.slice[1]), p.slice[1].lineno)

def p_type_param(p):
    '''typeDeclare : typecol
                 | ID MODULAR ROWTYPE
                 | ID DOT ID MODULAR TYPE
                 | RECORD
                 | OUT
    '''
    p[0] = p[1]

#def p_options_declaration(p):
#    '''optionsDeclaration : optionsDeclaration detailDeclaration
#                          | detailDeclaration
#    '''
#    if(len(p) == 3):
#        p[1].append(p[2])
#        p[0] = p[1]
#    else:
#        p[0] = [p[1]]

def p_detail_declaration(p):
    '''detailDeclaration : COLLATE ID NOT NULL ASSIGNATION_SYMBOL PLPSQL_EXPRESSION
                         | NOT NULL ASSIGNATION_SYMBOL PLPSQL_EXPRESSION
                         | COLLATE ID NOT NULL
                         | COLLATE ID ASSIGNATION_SYMBOL PLPSQL_EXPRESSION
                         | COLLATE ID
                         | NOT NULL
                         | ASSIGNATION_SYMBOL PLPSQL_EXPRESSION
    '''
    if len(p) == 3:
        p[0] = p[2]

def p_assignation_symbol(p):
    '''ASSIGNATION_SYMBOL : EQUALS
                          | COLONEQUALS
                          | DEFAULT
    '''

#El primero es un opciones con un return de expresion
#El segundo es solo un return expresion
#El tercero es un cuerpo
def p_staments(p):
    '''STATEMENTS : OPTIONS_STATEMENTS RETURN PLPSQL_EXPRESSION SEMICOLON
                  | OPTIONS_STATEMENTS RETURN SEMICOLON
                  | RETURN PLPSQL_EXPRESSION SEMICOLON 
                  | RETURN SEMICOLON 
                  | OPTIONS_STATEMENTS

    '''
    if p.slice[1].type == "OPTIONS_STATEMENTS":
        if len(p) == 4:     #segunda produccion
            p[1].append(ReturnFuncProce(None))
        elif len(p) == 2:
            pass
        else:               #primera produccion
            p[1].append(ReturnFuncProce(p[3]))

        p[0] = p[1]

    elif p.slice[1].type == "RETURN":
        if len(p) == 3:     #tercera produccion
            p[0] = [ReturnFuncProce(None)]
        else:               #cuarta produccion
            p[0] = [ReturnFuncProce(p[2])]
    

def p_options_statements(p):
    '''OPTIONS_STATEMENTS : OPTIONS_STATEMENTS statementType
                          | statementType

    '''
    if p.slice[1].type == "OPTIONS_STATEMENTS":
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_statement_type(p):
    '''statementType : PLPSQL_EXPRESSION  SEMICOLON 
                    |  PLPSQL_PRIMARY_EXPRESSION ASSIGNATION_SYMBOL QUERYSTATEMENT
                    |  RAISE_EXCEPTION 
                    |  BODY_DECLARATION
                    |  ifStatement
                    |  CASECLAUSE
                    |  DML
                    | ddl
                    | CALL_FUNCTIONS_PROCEDURE SEMICOLON
    '''
    if len(p) == 4:
        if isinstance(p[1], ObjectReference): 
            p[0] = AsignacionID(p[1].reference_column.value, p[3], 0, 0)
        else:
            p[0] = AsignacionID(p[1], p[3], 0, 0)
    else:
        p[0] = p[1]

#TODO: CONCAT
def p_plpsql_expression(p):
    '''PLPSQL_EXPRESSION : PLPSQL_EXPRESSION CONCAT PLPSQL_EXPRESSION
                         | PLPSQL_EXPRESSION AND PLPSQL_EXPRESSION
                         | PLPSQL_EXPRESSION OR PLPSQL_EXPRESSION
                         | PLPSQL_PRIMARY_EXPRESSION ASSIGNATION_SYMBOL SQLRELATIONALEXPRESSION
                         | PLPSQL_PRIMARY_EXPRESSION ASSIGNATION_SYMBOL CALL_FUNCTIONS_PROCEDURE
                         | PLPSQL_PRIMARY_EXPRESSION NOT_EQUAL PLPSQL_PRIMARY_EXPRESSION
                         | PLPSQL_PRIMARY_EXPRESSION GREATE_EQUAL PLPSQL_PRIMARY_EXPRESSION
                         | PLPSQL_PRIMARY_EXPRESSION GREATE_THAN PLPSQL_PRIMARY_EXPRESSION
                         | PLPSQL_PRIMARY_EXPRESSION LESS_THAN PLPSQL_PRIMARY_EXPRESSION
                         | PLPSQL_PRIMARY_EXPRESSION LESS_EQUAL PLPSQL_PRIMARY_EXPRESSION
                         | PLPSQL_PRIMARY_EXPRESSION
                         
    '''
    if len(p) == 4:
        if p.slice[2].type == "ASSIGNATION_SYMBOL":
            if isinstance(p[1], ObjectReference): 
                p[0] = AsignacionID(p[1].reference_column.value, p[3], 0, 0)
        else:
            if p[2] == '!=':
                p[0] = Relop(p[1], SymbolsRelop.NOT_EQUAL, p[3], p[2]
                        [1], p[2].lineno, find_column(p[2]))
            elif p[2] == '>=':
                p[0] = Relop(p[1], SymbolsRelop.GREATE_EQUAL, p[3],
                            p[2], p[2].lineno, find_column(p[2]))
            elif p[2] == '>':
                p[0] = Relop(p[1], SymbolsRelop.GREATE_THAN, p[3], p[2]
                            [1], p[2].lineno, find_column(p[2]))
            elif p[2] == '<=':
                p[0] = Relop(p[1], SymbolsRelop.LESS_EQUAL, p[3], p[2]
                            [1], p[2].lineno, find_column(p[2]))
            elif p[2] == '<':
                p[0] = Relop(p[1], SymbolsRelop.LESS_THAN, p[3], p[2]
                            [1], p[2].lineno, find_column(p[2]))
    else:
        p[0] = p[1]
        


def p_plpsql_primary_expression(p):
    '''PLPSQL_PRIMARY_EXPRESSION : PLPSQL_PRIMARY_EXPRESSION PLUS PLPSQL_PRIMARY_EXPRESSION
                                 | PLPSQL_PRIMARY_EXPRESSION REST PLPSQL_PRIMARY_EXPRESSION
                                 | PLPSQL_PRIMARY_EXPRESSION ASTERISK PLPSQL_PRIMARY_EXPRESSION
                                 | PLPSQL_PRIMARY_EXPRESSION DIVISION PLPSQL_PRIMARY_EXPRESSION
                                 | PLPSQL_PRIMARY_EXPRESSION EXPONENT PLPSQL_PRIMARY_EXPRESSION
                                 | PLPSQL_PRIMARY_EXPRESSION MODULAR PLPSQL_PRIMARY_EXPRESSION
                                 | LEFT_PARENTHESIS PLPSQL_EXPRESSION RIGHT_PARENTHESIS
                                 | REST PLPSQL_PRIMARY_EXPRESSION %prec UREST
                                 | PLUS PLPSQL_PRIMARY_EXPRESSION %prec UPLUS
                                 | AGGREGATEFUNCTIONS
                                 | GREATESTORLEAST
                                 | EXPRESSIONSTIME
                                 | SQUARE_ROOT SQLSIMPLEEXPRESSION
                                 | CUBE_ROOT SQLSIMPLEEXPRESSION
                                 | MATHEMATICALFUNCTIONS
                                 | BINARY_STRING_FUNCTIONS
                                 | TRIGONOMETRIC_FUNCTIONS
                                 | TRUE
                                 | FALSE
                                 | OBJECTREFERENCE
                                 | SQLINTEGER
                                 | DOLLAR SQLINTEGER
    '''
    if (len(p) == 4):
        if (p[1] == "("):
            p[0] = p[2]
        else:
            if p[2] == '+':
                p[0] = ArithmeticBinaryOperation(
                    p[1], p[3], SymbolsAritmeticos.PLUS, '+', p.lineno(2), find_column(p.slice[2]))
            elif p[2] == '-':
                p[0] = ArithmeticBinaryOperation(
                    p[1], p[3], SymbolsAritmeticos.MINUS, '-', p.lineno(2), find_column(p.slice[2]))
            elif p[2] == '*':
                p[0] = ArithmeticBinaryOperation(
                    p[1], p[3], SymbolsAritmeticos.TIMES, '*', p.lineno(2), find_column(p.slice[2]))
            elif p[2] == '/':
                p[0] = ArithmeticBinaryOperation(
                    p[1], p[3], SymbolsAritmeticos.DIVISON, '/', p.lineno(2), find_column(p.slice[2]))
            elif p[2] == '^':
                p[0] = ArithmeticBinaryOperation(
                    p[1], p[3], SymbolsAritmeticos.EXPONENT, '^', p.lineno(2), find_column(p.slice[2]))
            elif p[2] == '%':
                p[0] = ArithmeticBinaryOperation(
                    p[1], p[3], SymbolsAritmeticos.MODULAR, '%', p.lineno(2), find_column(p.slice[2]))
    elif (len(p) == 3):
        if p[1] == '-':
            p[0] = UnaryOrSquareExpressions(
                SymbolsUnaryOrOthers.UMINUS, p[2], p.lineno(1), find_column(p.slice[1]), p[1])
        elif p[1] == '+':
            p[0] = UnaryOrSquareExpressions(
                SymbolsUnaryOrOthers.UPLUS, p[2], p.lineno(1), find_column(p.slice[1]), p[1])
    else:
        if p.slice[1].type == "TRUE" or p.slice[1].type == "FALSE":
            v = True
            if p.slice[1].type == "FALSE":
                v = False
            p[0] = PrimitiveData(DATA_TYPE.BOOLEANO, v, p.lineno(1), find_column(p.slice[1]))
            
        else:
            p[0] = p[1]


def p_if_statement(p):
    '''ifStatement : IF SQLEXPRESSION THEN STATEMENTS elseIfBlocks ELSE STATEMENTS END IF SEMICOLON
                   | IF SQLEXPRESSION THEN STATEMENTS elseIfBlocks END IF SEMICOLON
                   | IF SQLEXPRESSION THEN STATEMENTS ELSE STATEMENTS END IF SEMICOLON
                   | IF SQLEXPRESSION THEN STATEMENTS END IF SEMICOLON
    ''' 
    
    if len(p) == 11: #Primera produccion
        if_anidados = anidarIFs(0, p[5], p[7])
        p[0] = If(p[2], p[4], None, if_anidados)

    elif len(p) == 9: #Segunda produccion
        if_anidados = anidarIFs(0, p[5], None)
        p[0] = If(p[2], p[4], None, if_anidados)

    elif len(p) == 10: #Tercera produccion
        p[0] = If(p[2], p[4], None, p[6])
    else: #Cuarta produccion
        p[0] = If(p[2], p[4], None, None)
        

def p_elseIfBlocks(p):
    '''elseIfBlocks : elseIfBlocks elseIfBlock
                    | elseIfBlock
    '''
    if(len(p) == 3):
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_elseIfBlock(p):
    '''elseIfBlock : elseIfWord SQLEXPRESSION THEN STATEMENTS
    '''
    p[0] = If(p[2], p[4], None, None)

def p_else_word(p):
    '''elseIfWord : ELSEIF
                  | ELSIF
    '''

def p_bodyExceptionList(p):
    '''bodyExceptionList : bodyExceptionList bodyException
                         | bodyException
    '''

def p_bodyException(p):
    '''bodyException : WHEN SQLEXPRESSION THEN STATEMENTS
    '''

def p_raise_exception(p):
    '''RAISE_EXCEPTION : RAISE NOTICE SQLNAME COMMA OBJECTREFERENCE SEMICOLON
                       | RAISE SQLNAME COMMA OBJECTREFERENCE SEMICOLON 
    '''

# =====================================================================================
# =====================================================================================
# =====================================================================================




def p_dml(p):
    '''DML : QUERYSTATEMENT
           | INSERTSTATEMENT
           | DELETESTATEMENT
           | UPDATESTATEMENT'''
    p[0] = p[1]

#TODO: PROBAR UPDATE
def p_update_statement(p):
    '''UPDATESTATEMENT : UPDATE ID OPTIONS1 SET SETLIST OPTIONSLIST2 SEMICOLON
                       | UPDATE ID SET SETLIST OPTIONSLIST2 SEMICOLON
                       | UPDATE ID SET SETLIST  SEMICOLON '''
    string = ''
    if(len(p) == 8):
        p[0] = Update(p[2], p[5], p[6], generateC3D(p),
                      p.lineno(1), find_column(p.slice[1]))

        for index, var in enumerate(p[5]):
            if index > 0: string += f', {var._tac}'
            else: string += f'{var._tac}'

        p[0]._tac = f'UPDATE {p[2]} {p[3]._tac} SET {string} {p[6]._tac};'

    elif(len(p) == 7):
        p[0] = Update(p[2], p[4], p[5], generateC3D(p),
                      p.lineno(1), find_column(p.slice[1]))

        for index, var in enumerate(p[4]):
            if index > 0: string += f', {var._tac}'
            else: string += f'{var._tac}'

        p[0]._tac = f'UPDATE {p[2]} SET {string} {p[5]._tac};'
    else:
        p[0] = Update(p[2], p[4], None, generateC3D(p),
                      p.lineno(1), find_column(p.slice[1]))

        for index, var in enumerate(p[4]):
            if index > 0: string += f', {var._tac}'
            else: string += f'{var._tac}'

        p[0]._tac = f'UPDATE {p[2]} SET {string};'


def p_set_list(p):
    '''SETLIST : SETLIST COMMA COLUMNVALUES
               | COLUMNVALUES'''
    if(len(p) == 4):
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]


def p_column_values(p):
    '''COLUMNVALUES : OBJECTREFERENCE EQUALS SQLEXPRESSION2'''
    p[0] = ColumnVal(p[1], p[3])
    p[0]._tac = f"{p[1]._tac} {p[2]} {p[3]._tac} "

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
                      | ACOSD LEFT_PARENTHESIS SQLEXPRESSION2 RIGHT_PARENTHESIS
                      | ASIND LEFT_PARENTHESIS SQLEXPRESSION2 RIGHT_PARENTHESIS
                      | SUBSTRING LEFT_PARENTHESIS ID COMMA SQLINTEGER COMMA SQLINTEGER RIGHT_PARENTHESIS
                      | SQLNAME
                      | SQLINTEGER
                      | TRUE
                      | DOLLAR SQLINTEGER
                      | FALSE'''
    # TODO: CUALES SON LOS UNARIOS QUE ACEPTA ---> REVISAR
    if len(p) == 4:
        if p[1] == '(':
            p[0] = p[2]
        elif p[2] == '+':
            p[0] = ArithmeticBinaryOperation(
                p[1], p[3], SymbolsAritmeticos.PLUS, '+', p.lineno(2), find_column(p.slice[2]))
        elif p[2] == '-':
            p[0] = ArithmeticBinaryOperation(
                p[1], p[3], SymbolsAritmeticos.MINUS, '-', p.lineno(2), find_column(p.slice[2]))
        elif p[2] == '*':
            p[0] = ArithmeticBinaryOperation(
                p[1], p[3], SymbolsAritmeticos.TIMES, '*', p.lineno(2), find_column(p.slice[2]))
        elif p[2] == '/':
            p[0] = ArithmeticBinaryOperation(
                p[1], p[3], SymbolsAritmeticos.DIVISON, '/', p.lineno(2), find_column(p.slice[2]))
        elif p[2] == '^':
            p[0] = ArithmeticBinaryOperation(
                p[1], p[3], SymbolsAritmeticos.EXPONENT, '^', p.lineno(2), find_column(p.slice[2]))
        elif p[2] == '%':
            p[0] = ArithmeticBinaryOperation(
                p[1], p[3], SymbolsAritmeticos.MODULAR, '%', p.lineno(2), find_column(p.slice[2]))
    elif len(p) == 2:
        if p.slice[1].type == "TRUE" or p.slice[1].type == "FALSE":
            v = True
            if p.slice[1].type == "FALSE":
                v = False
            p[0] = PrimitiveData(DATA_TYPE.BOOLEANO, v, p.lineno(1), find_column(p.slice[1]))
        else:
            p[0] = p[1]
    elif len(p) == 5:
        p[0] = ExpressionsTrigonometric(
            p[1], p[3], None, p.lineno(1), find_column(p.slice[1]))


def p_options_list2(p):
    '''OPTIONSLIST2 : WHERECLAUSE OPTIONS4
                    | WHERECLAUSE
                    | OPTIONS4'''
    # if (len(p) == 3):
    #     nodo.add_childrens(p[1])
    #     nodo.add_childrens(p[2])
    # else:
    #     nodo.add_childrens(p[1])
    # p[0] = nodo
    p[0] = p[1]

def p_delete_statement(p):
    '''DELETESTATEMENT : DELETE FROM ID OPTIONSLIST SEMICOLON
                       | DELETE FROM ID SEMICOLON '''
    if (len(p) == 6):
        p[0] = Delete(p[3], p[4], generateC3D(p),
                      p.lineno(1), find_column(p.slice[1]))
        string = ''
        for val in p[4]:
            string += val._tac
        p[0]._tac = f'DELETE FROM {p[3]} {string};'
    else:
        p[0] = Delete(p[3], None, generateC3D(p),
                      p.lineno(1), find_column(p.slice[1]))
        p[0]._tac = f'DELETE FROM {p[3]};'


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
    if (len(p) == 5):
        p[0] = [p[1]]
        p[1].append(p[2])
        p[1].append(p[3])
        p[1].append(p[4])
    elif (len(p) == 4):
        p[0] = [p[1]]
        p[1].append(p[2])
        p[1].append(p[3])
    elif (len(p) == 3):
        p[0] = [p[1]]
        p[1].append(p[2])

    p[0] = [p[1]]
    # TODO: PROBAR SI REALMENTE SIRVE EL ARBOL XD PINCHE JUAN MARCOS >:V


def p_options1(p):
    '''OPTIONS1 : ASTERISK SQLALIAS
                | ASTERISK
                | SQLALIAS'''
    if(len(p) == 3):
        p[0] = Opt1(True, p[2])

        p[0]._tac = f'* {p[2]._tac}'
    else:
        if(p[1] == "*"):
            p[0] = Opt1(True, None)
            p[0]._tac = f'* '

        else:
            p[0] = Opt1(False, p[2])
            p[0]._tac = f'{p[2]._tac} '


def p_options2(p):
    '''OPTIONS2 : USING USINGLIST'''
    p[0] = Using(p[2])
    string = ''
    for index, var in enumerate(p[2]):
        if index > 0: string += f', {var._tac}'
        else: string += f'{var._tac}'
    p[0]._tac = f'USING {string}'


def p_using_list(p):
    '''USINGLIST  : USINGLIST COMMA SQLNAME
                  | SQLNAME'''
    if(len(p) == 4):
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_options4(p):
    '''OPTIONS4 : RETURNING RETURNINGLIST'''
    p[0] = Returning(p[2])
    string = ''
    if type(p[2]) is list:
        for index, var in enumerate(p[4]):
            if index > 0: string += f', {var._tac}'
            else: string += f'{var._tac}'
    else: string = '* '
    p[0]._tac = f'RETURNING {string}'

def p_returning_list(p):
    '''RETURNINGLIST   : ASTERISK
                       | EXPRESSIONRETURNING'''
    p[0] = p[1]


def p_returning_expression(p):
    '''EXPRESSIONRETURNING : EXPRESSIONRETURNING COMMA SQLEXPRESSION SQLALIAS
                           | SQLEXPRESSION SQLALIAS'''
    if(len(p) == 5):
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_insert_statement(p):
    '''INSERTSTATEMENT : INSERT INTO SQLNAME LEFT_PARENTHESIS LISTPARAMSINSERT RIGHT_PARENTHESIS VALUES LEFT_PARENTHESIS LISTVALUESINSERT RIGHT_PARENTHESIS SEMICOLON
                       | INSERT INTO SQLNAME VALUES LEFT_PARENTHESIS LISTVALUESINSERT RIGHT_PARENTHESIS SEMICOLON '''
    string = ''
    string1 = ''
    if(len(p) == 12):
        p[0] = Insert(p[3], p[5], p[9], generateC3D(p),
                      p.lineno(1), find_column(p.slice[1]))
        
        #LISTPARAMSINSERT
        for index, var in enumerate(p[5]):
            if index > 0: string += f', {var._tac}'
            else: string += f'{var._tac}'
        #LISTVALUESINSERT
        for index, var in enumerate(p[9]):
            if index > 0: string1 += f', {var._tac}'
            else: string1 += f'{var._tac}'

        p[0]._tac = f'INSERT INTO {p[3]._tac} ({string}) VALUES ({string1});'
    else:
        p[0] = Insert(p[3], None, p[6], generateC3D(p),
                      p.lineno(1), find_column(p.slice[1]))
        #LISTVALUESINSERT
        for index, var in enumerate(p[6]):
            if index > 0: string += f', {var._tac}'
            else: string += f'{var._tac}'

        p[0]._tac = f'INSERT INTO {p[3]._tac} VALUES ({string});'

def p_list_params_insert(p):
    '''LISTPARAMSINSERT : LISTPARAMSINSERT COMMA SQLNAME
                        | SQLNAME'''
    if(len(p) == 4):
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]


def p_query_statement(p):
    #  ELEMENTO 0       ELEMENTO 1     ELEMENTO 2      ELEMENTO 3
    '''QUERYSTATEMENT : SELECTSTATEMENT SEMICOLON'''
    p[0] = p[1]
    p[0]._tac = f'{p[1]._tac};'


def p_select_statement(p):
    '''SELECTSTATEMENT : SELECTWITHOUTORDER ORDERBYCLAUSE LIMITCLAUSE
                       | SELECTWITHOUTORDER ORDERBYCLAUSE 
                       | SELECTWITHOUTORDER LIMITCLAUSE 
                       | SELECTWITHOUTORDER'''
    if (len(p) == 4):
        p[2] = p[2][1]
        [3].pop(0)
        p[3] = p[3][0]
        p[0] = Select(p[1], p[2], p[3], generateC3D(p))
        p[0]._tac = f'{p[1]._tac} {p[2]._tac} {p[3]._tac}'
    elif (len(p) == 3):
        if ('ORDER' in p[2]):
            p[2] = p[2][1]
            p[0] = Select(p[1], p[2], None, generateC3D(p))
            p[0]._tac = f'{p[1]._tac} {p[2]._tac}'
        elif ('LIMIT' in p[2]):
            [2].pop(0)
            p[2] = p[2][0]
            p[0] = Select(p[1], None, p[2], generateC3D(p))
            p[0]._tac = f'{p[1]._tac} {p[2]._tac}'
    elif (len(p) == 2):
        p[0] = Select(p[1], None, None, generateC3D(p))
        p[0]._tac = f'{p[1]._tac}'


def p_select_without_order(p):
    '''SELECTWITHOUTORDER : SELECTSET
                          | SELECTWITHOUTORDER TYPECOMBINEQUERY ALL SELECTSET
                          | SELECTWITHOUTORDER TYPECOMBINEQUERY SELECTSET'''
    lista_union = []
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 5:
        lista_union.append(p[1])
        lista_union.append(p[2])
        lista_union.append(p[3])
        lista_union.append(p[4])
        p[0] = TypeQuerySelect(lista_union, p.lineno(3),
                               find_column(p.slice[3]))
        p[0]._tac = f'({p[1]._tac}) {p[2]} {p[3]} ({p[4]._tac})'
    elif len(p) == 4:
        lista_union.append(p[1])
        lista_union.append(p[2])
        lista_union.append(p[3])
        p[0] = TypeQuerySelect(lista_union, 0, 0)
        p[0]._tac = f'({p[1]._tac}) {p[2]} ({p[3]._tac})'

def p_select_set(p):
    '''SELECTSET : SELECTQ 
                 | LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[2]


def p_selectq(p):
    '''SELECTQ : SELECT SELECTLIST FROMCLAUSE
               | SELECT SELECTLIST FROMCLAUSE SELECTWHEREAGGREGATE
               | SELECT TYPESELECT SELECTLIST FROMCLAUSE
               | SELECT TYPESELECT SELECTLIST FROMCLAUSE SELECTWHEREAGGREGATE
               | SELECT SELECTLIST'''
    string = ''
    from_list = ''
    if len(p) == 4:
        p[0] = SelectQ(None, p[2], p[3], None, p.lineno(1),
                       find_column(p.slice[1]))        
        for index, var in enumerate(p[2]):
            if index > 0: string += f', {var._tac}'
            else: string += f'{var._tac}'
        p[0]._tac = f'SELECT {string} {p[3]._tac}'

    elif len(p) == 5:
        if (p.slice[2].type == "TYPESELECT"):
            p[0] = SelectQ(p[2], p[3], p[4], None, p.lineno(1),
                           find_column(p.slice[1]))
            for index, var in enumerate(p[3]):
                if index > 0: string += f', {var._tac}'
                else: string += f'{var._tac}'
            p[0]._tac = f'SELECT {p[2]} {string} {p[4]._tac}'
            
        else:
            p[0] = SelectQ(None, p[2], p[3], p[4], p.lineno(1),
                           find_column(p.slice[1]))
            for index, var in enumerate(p[2]):
                if index > 0: string += f', {var._tac}'
                else: string += f'{var._tac}'
            if isinstance(p[4], list):
                p[0]._tac = f'SELECT {string} {p[3]._tac} {p[4][0]._tac} {p[4][1]._tac}'
            else:
                p[0]._tac = f'SELECT {string} {p[3]._tac} {p[4]._tac}'
    elif len(p) == 6:
        p[0] = SelectQ(p[2], p[3], p[4], p[5], p.lineno(1),
                       find_column(p.slice[1]))
        for index, var in enumerate(p[3]):
                if index > 0: string += f', {var._tac}'
                else: string += f'{var._tac}'
        if isinstance(p[5], list):
            p[0]._tac = f'SELECT {p[2]} {string} {p[4]._tac} {p[5][0]._tac} {p[5][1]._tac}'
        else:
            p[0]._tac = f'SELECT {p[2]} {string} {p[4]._tac} {p[5]._tac}'

    elif len(p) == 3:
        p[0] = SelectQ(None, p[2], None, None, p.lineno(1),
                       find_column(p.slice[1]))
        for index, var in enumerate(p[2]):
            if index > 0: string += f', {var._tac}'
            else: string += f'{var._tac}'
        p[0]._tac = f'SELECT {string}'


def p_select_list(p):
    '''SELECTLIST : ASTERISK
                  | LISTITEM'''
    if (p[1] == "*"):
        p[0] = [PrimitiveData(DATA_TYPE.STRING, p[1],
                              p.lineno(1), find_column(p.slice[1]))]
    else:
        p[0] = p[1]


def p_list_item(p):
    '''LISTITEM : LISTITEM COMMA SELECTITEM
                | SELECTITEM'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]


def p_select_item(p):
    '''SELECTITEM : SQLEXPRESSION SQLALIAS
                  | SQLEXPRESSION
                  | CALL_FUNCTIONS_PROCEDURE SQLALIAS
                  | CALL_FUNCTIONS_PROCEDURE
                  | LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS'''
    if (len(p) == 3):
        p[1].alias = p[2].alias
        p[1]._tac = f'{p[1]._tac} {p[2]._tac}'
        p[0] = p[1]
    elif (len(p) == 4):
        p[0] = p[2]
    elif (len(p) == 2):
        p[0] = p[1]


def p_from_clause(p):
    '''FROMCLAUSE : FROM FROMCLAUSELIST'''
    string = ""
    p[0] = From(p[2])
    for index, var in enumerate(p[2]):
        if index > 0: string += f', {var._tac}'
        else: string += f'{var._tac}'
    p[0]._tac = f'FROM {string}'
# TODO le faltaba un coma xd


def p_from_clause_list(p):
    '''FROMCLAUSELIST : FROMCLAUSELIST COMMA TABLEREFERENCE
                      | FROMCLAUSELIST COMMA LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS SQLALIAS
                      | FROMCLAUSELIST COMMA LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS
                      | LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS
                      | LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS SQLALIAS
                      | TABLEREFERENCE'''
    if (len(p) == 6):
        p[1].append(p[3])
        p[0] = p[1]
    elif (len(p) == 5):
        if (p[1] == "("):
            p[0] = [p[2], p[4]]
        else:
            p[1].append(p[3])
            p[0] = p[1]
    elif (len(p) == 4):
        if (p[1] == "("):
            p[0] = [p[2]]
        else:
            p[1].append(p[3])
            p[0] = p[1]
    elif (len(p) == 2):
        p[0] = [p[1]]


def p_where_aggregate(p):
    '''SELECTWHEREAGGREGATE : WHERECLAUSE  SELECTGROUPHAVING
                            | SELECTGROUPHAVING
                            | WHERECLAUSE'''
    if (len(p) == 3):
        p[0] = [p[1], p[2]]
    elif (len(p) == 2):
        p[0] = p[1]


def p_select_group_having(p):
    '''SELECTGROUPHAVING : GROUPBYCLAUSE
                         | HAVINGCLAUSE GROUPBYCLAUSE
                         | GROUPBYCLAUSE HAVINGCLAUSE'''
    string = ""
    for index, var in enumerate(p[1]):
                if index > 0: string += f', {var._tac}'
                else: string += f'{var._tac}'
    if (len(p) == 2):
        p[0] = GroupBy(p[1], None)
        p[0]._tac = f'GROUP BY {string}'
    elif (len(p) == 3):
        p[0] = GroupBy(p[1], p[2])
        p[0]._tac = f'GROUP BY {string} HAVING {p[2]._tac}'

def p_table_reference(p):
    '''TABLEREFERENCE : SQLNAME SQLALIAS
                      | SQLNAME SQLALIAS JOINLIST
                      | SQLNAME JOINLIST
                      | SQLNAME'''
    if (len(p) == 2):
        p[0] = TableReference(
            p[1], None, None, p.slice[1].value.line, p.slice[1].value.column)
        p[0]._tac = f'{p[1]._tac}'
    elif (len(p) == 3):
        p[0] = TableReference(
            p[1], p[2], p[2], p.slice[1].value.line, p.slice[1].value.column)
        p[0]._tac = f'{p[1]._tac} {p[2]._tac}'
    elif (len(p) == 4):
        p[0] = TableReference(
            p[1], p[3], p[2], p.slice[1].value.line, p.slice[1].value.column)
        p[0]._tac = f'{p[1]._tac} {p[2]._tac}'


def p_order_by_clause(p):
    '''ORDERBYCLAUSE : ORDER BY ORDERBYEXPRESSION'''
    p[0] = [p.slice[1].type, p[3]]


def p_order_by_clause_list(p):
    '''ORDERBYEXPRESSION : LISTPARAMSINSERT ASC
                         | LISTPARAMSINSERT DESC
                         | LISTPARAMSINSERT'''
    string = 'ORDER BY '
    if (len(p) == 3):
        for index, var in enumerate(p[1]):
                if index > 0: string += f', {var._tac}'
                else: string += f'{var._tac}'
        if p.slice[2].type == 'ASC':
            string += f' {p[2]}'
        else:
            string += f' {p[2]}'
        p[0] = OrderClause(p[1], p[2], p.lineno(2), find_column(p.slice[2]))
        p[0]._tac = string
        
    elif (len(p) == 2):
        for index, var in enumerate(p[1]):
                if index > 0: string += f', {var._tac}'
                else: string += f'{var._tac}'
        p[0] = OrderClause(p[1], None, None, None)
        p[0]._tac = string


def p_limit_clause(p):
    '''LIMITCLAUSE : LIMIT LIMITTYPES OFFSET INT_NUMBER
                   | LIMIT LIMITTYPES'''
    string = ''
    if (len(p) == 5):
        string = f'{p[1]} {p[2]} {p[3]} {p[4]}'
        p[0] = [LimitClause(p[2], p[4], p.lineno(
            3), find_column(p.slice[3])), p.slice[1].type]
        p[0][0]._tac = string
    elif (len(p) == 3):
        string = f'{p[1]} {p[2]}'
        p[0] = [LimitClause(p[2], None, p.lineno(1), find_column(p.slice[1])), p.slice[1].type]
        p[0][0]._tac = string


def p_limit_types(p):
    '''LIMITTYPES : INT_NUMBER
                  | ALL'''
    p[0] = p[1]


def p_where_clause(p):
    '''WHERECLAUSE : WHERE SQLEXPRESSION'''
    string = ""
    p[0] = Where(p[2])
    if isinstance(p[2], list):
        for index, var in enumerate(p[2]):
            if hasattr(var, '_tac'):
                string += f'{var._tac}'
        p[0]._tac = f'WHERE {string}'
    else:
        p[0]._tac = f'WHERE {p[2]._tac}'

def p_group_by_clause(p):
    '''GROUPBYCLAUSE : GROUP BY SQLEXPRESSIONLIST'''
    p[0] = p[3]


def p_having_clause(p):
    '''HAVINGCLAUSE : HAVING SQLEXPRESSION'''
    p[0] = p[2]


def p_join_list(p):
    '''JOINLIST : JOINLIST JOINP
                | JOINP'''
    if (len(p) == 2):
        p[0] = [p[1]]
    elif (len(p) == 3):
        p[1].append(p[2])
        p[0] = p[1]


def p_joinp(p):
    '''JOINP : JOINTYPE JOIN TABLEREFERENCE ON SQLEXPRESSION'''
    p[0] = JoinClause(p[1], p[3], p[5], p.lineno(2), find_column(p.slice[2]))


def p_join_type(p):
    '''JOINTYPE : INNER
                | LEFT OUTER
                | RIGHT OUTER
                | FULL OUTER'''

    if (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 3):
        p[0] = [p[1], p[2]]


def p_sql_expression(p):
    '''SQLEXPRESSION : SQLEXPRESSION OR SQLEXPRESSION
                     | SQLEXPRESSION AND SQLEXPRESSION
                     | NOT EXISTSORSQLRELATIONALCLAUSE
                     | EXISTSORSQLRELATIONALCLAUSE'''
    if len(p) == 4:
        p[0] = LogicalOperators(
            p[1], p[2], p[3], p.lineno(2), find_column(p.slice[2]))
    elif len(p) == 3:
        p[2]._tac = f'{p[1]} {p[2]._tac}'
        p[0] = [True, p[2]]
    else:
        p[0] = p[1]


def p_exits_or_relational_clause(p):
    '''EXISTSORSQLRELATIONALCLAUSE : EXISTSCLAUSE
                                   | SQLRELATIONALEXPRESSION'''
    p[0] = p[1]


def p_exists_clause(p):
    # TODO este tambien tenes que agregar al ast grafico, perdon didier xd
    '''EXISTSCLAUSE : EXISTS LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS'''
    p[0] = ExistsClause(None,  False,  p[3], p.lineno(1),
                        find_column(p.slice[1]))
    p[0]._tac = f'{p[1]}{p[2]}{p[3]._tac}{p[4]}'

def p_sql_relational_expression(p):
    '''SQLRELATIONALEXPRESSION : SQLSIMPLEEXPRESSION RELOP SQLSIMPLEEXPRESSION
                               | SQLSIMPLEEXPRESSION SQLINCLAUSE
                               | SQLSIMPLEEXPRESSION SQLBETWEENCLAUSE
                               | SQLSIMPLEEXPRESSION SQLLIKECLAUSE
                               | SQLSIMPLEEXPRESSION SQLISCLAUSE
                               | SQLSIMPLEEXPRESSION'''
    if (len(p) == 3):
        if p[2][1] == "LIKE":
            p[0] = LikeClause(p[2][0], p[1], p[2][2], p[2][3], p[2][4])
            p[0]._tac = f'{p[1]._tac} {p[2][5]}'
        elif p[2][0] == "BETWEEN":
            p[0] = Between(p[1], p[2][1], p[2][2], p[2]
                           [3], p[2][4], p[2][5], p[2][6])
            p[0]._tac = f'{p[1]._tac} {p[2][7]}'
        elif p[2][0] == "IS":
            p[0] = isClause(p[1], p[2][1], p[2][2], p[2][3])
            p[0]._tac = f'{p[1]._tac} {p[2][4]}'
        elif p[2][0] == "IN":
            p[0] = InClause(p[1], p[2][1], p[2][2], p[2][3], p[2][4])
            p[0]._tac = f'{p[1]._tac} {p[2][5]}'
        else:
            p[0] = [p[1], p[2]]
    elif (len(p) == 4):
        # print(p[2])
        if p[2][1] == '=':
            p[0] = Relop(p[1], SymbolsRelop.EQUALS, p[3], p[2][1],
                         p[2][0].lineno, find_column(p[2][0]))
        elif p[2][1] == '!=':
            p[0] = Relop(p[1], SymbolsRelop.NOT_EQUAL, p[3], p[2]
                         [1], p[2][0].lineno, find_column(p[2][0]))
        elif p[2][1] == '>=':
            p[0] = Relop(p[1], SymbolsRelop.GREATE_EQUAL, p[3],
                         p[2][1], p[2][0].lineno, find_column(p[2][0]))
        elif p[2][1] == '>':
            p[0] = Relop(p[1], SymbolsRelop.GREATE_THAN, p[3], p[2]
                         [1], p[2][0].lineno, find_column(p[2][0]))
        elif p[2][1] == '<=':
            p[0] = Relop(p[1], SymbolsRelop.LESS_EQUAL, p[3], p[2]
                         [1], p[2][0].lineno, find_column(p[2][0]))
        elif p[2][1] == '<':
            p[0] = Relop(p[1], SymbolsRelop.LESS_THAN, p[3], p[2]
                         [1], p[2][0].lineno, find_column(p[2][0]))
        elif p[2][1] == '<>':
            p[0] = Relop(p[1], SymbolsRelop.NOT_EQUAL_LR, p[3],
                         p[2][1], p[2][0].lineno, find_column(p[2][0]))
    else:
        p[0] = p[1]


def p_sql_in_clause(p):
    '''SQLINCLAUSE  : NOT IN LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS
                    | NOT IN LEFT_PARENTHESIS listain RIGHT_PARENTHESIS
                    | IN LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS
                    | IN LEFT_PARENTHESIS listain RIGHT_PARENTHESIS'''
    if (len(p) == 6):
        string = ""
        if isinstance(p[4], list):
            string = f'NOT IN ('
            for index, var in enumerate(p[4]):
                if index > 0: string += f', {var._tac}'
                else: string += f'{var._tac}'
            string += ")"
        else:
            string = f'NOT IN ({p[4]._tac})'
        p[0] = [p.slice[2].type, True, p[4],
                p.lineno(2), find_column(p.slice[2]), string]
    else:
        string = ""
        if isinstance(p[3], list):
            string = f'IN ('
            for index, var in enumerate(p[3]):
                if hasattr(var, '_tac'):
                    if index > 0: string += f', {var._tac}'
                    else: string += f'{var._tac}'
            string += ")"
        else:
            string = f'IN ({p[3]._tac})'
        p[0] = [p.slice[1].type, False, p[3],
                p.lineno(1), find_column(p.slice[1]), string]


def p_lista_in(p):
    '''listain : listain COMMA SQLSIMPLEEXPRESSION
               | SQLSIMPLEEXPRESSION 
    '''
    if (len(p) == 4):
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]


def p_sql_between_clause(p):
    '''SQLBETWEENCLAUSE : NOT BETWEEN SQLSIMPLEEXPRESSION AND SQLSIMPLEEXPRESSION
                        | NOT BETWEEN SYMMETRIC SQLSIMPLEEXPRESSION AND SQLSIMPLEEXPRESSION
                        | BETWEEN SQLSIMPLEEXPRESSION AND SQLSIMPLEEXPRESSION 
                        | BETWEEN SYMMETRIC SQLSIMPLEEXPRESSION AND SQLSIMPLEEXPRESSION '''
    if (len(p) == 6):
        if (p.slice[2].type == 'SYMMETRIC'):
            string = f'BETWEEN SYMMETRIC {p[3]._tac} AND {p[5]._tac}'
            p[0] = [p.slice[1].type, None, True, p[3],
                    p[5], p.lineno(1), find_column(p.slice[1]), string]
        else:
            string = f'NOT BETWEEN {p[3]._tac} AND {p[5]._tac}'
            p[0] = [p.slice[2].type, True, None, p[3],
                    p[5], p.lineno(2), find_column(p.slice[2]), string]
    elif (len(p) == 5):
        string = f'BETWEEN {p[2]._tac} AND {p[4]._tac}'
        p[0] = [p.slice[1].type, None, None, p[2],
                p[4], p.lineno(1), find_column(p.slice[1]), string]
    else:  # len 7
        string = f'NOT BETWEEN SYMMETRIC {p[4]._tac} AND {p[6]._tac}'
        p[0] = [p.slice[2].type, True, True, p[4],
                p[6], p.lineno(2), find_column(p.slice[2]), string]


def p_sql_like_clause(p):
    '''SQLLIKECLAUSE  : NOT LIKE SQLSIMPLEEXPRESSION
                      | LIKE SQLSIMPLEEXPRESSION'''
    if (len(p) == 4):
        string = f'NOT LIKE {p[3]._tac}'
        p[0] = [True, p.slice[2].type, p[3],
                p.lineno(1), find_column(p.slice[1]), string]
    else:
        string = f'LIKE {p[2]._tac}'
        p[0] = [False,  p.slice[1].type, p[2],
                p.lineno(1), find_column(p.slice[1]), string]

# TODO A qui no se como se guardaria esto xd


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
    if len(p) == 3:
        string = f'IS '
        if p.slice[2].type == "NULL":
            string += "NULL"
        elif p.slice[2].type == "TRUE":
            string += "TRUE"
        elif p.slice[2].type == "FALSE":
            string += "FALSE"
        elif p.slice[2].type == "UNKNOWN":
            string += "UNKNOWN"
        p[0] = [p.slice[1].type, [p[2]], p.lineno(1), find_column(p.slice[1]), string]
    elif len(p) == 4:
        string = f'IS NOT '
        if p.slice[3].type == "NULL":
            string += "NULL"
        elif p.slice[3].type == "TRUE":
            string += "TRUE"
        elif p.slice[3].type == "FALSE":
            string += "FALSE"
        p[0] = [p.slice[1].type, [p[2], p[3]],
                p.lineno(1), find_column(p.slice[1]), string]
    elif len(p) == 2:
        string = ""
        if p.slice[1].type == "ISNULL":
            string += "ISNULL"
        elif p.slice[1].type == "NOTNULL":
            string += "NOTNULL"
        p[0] = ["IS", [p[1]], p.lineno(1), find_column(p.slice[1]), string]
    elif len(p) == 6:
        string = f'IS NOT DISTINCT FROM {p[5]._tac}'
        p[0] = [p.slice[1].type, [p[2], p[3], p[4], p[5]],
                p.lineno(1), find_column(p.slice[1]), string]
    else:  # len 5
        string = f'IS DISTINCT FROM  {p[4]._tac}'
        p[0] = [p.slice[1].type, [p[2], p[3], p[4]],
                p.lineno(1), find_column(p.slice[1]), string]


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
                           | DOLLAR SQLINTEGER
                           | FALSE'''
    if (len(p) == 4):
        if (p[1] == "("):
            p[0] = p[2]
        else:
            if p[2] == '+':
                p[0] = ArithmeticBinaryOperation(
                    p[1], p[3], SymbolsAritmeticos.PLUS, '+', p.lineno(2), find_column(p.slice[2]))
            elif p[2] == '-':
                p[0] = ArithmeticBinaryOperation(
                    p[1], p[3], SymbolsAritmeticos.MINUS, '-', p.lineno(2), find_column(p.slice[2]))
            elif p[2] == '*':
                p[0] = ArithmeticBinaryOperation(
                    p[1], p[3], SymbolsAritmeticos.TIMES, '*', p.lineno(2), find_column(p.slice[2]))
            elif p[2] == '/':
                p[0] = ArithmeticBinaryOperation(
                    p[1], p[3], SymbolsAritmeticos.DIVISON, '/', p.lineno(2), find_column(p.slice[2]))
            elif p[2] == '^':
                p[0] = ArithmeticBinaryOperation(
                    p[1], p[3], SymbolsAritmeticos.EXPONENT, '^', p.lineno(2), find_column(p.slice[2]))
            elif p[2] == '%':
                p[0] = ArithmeticBinaryOperation(
                    p[1], p[3], SymbolsAritmeticos.MODULAR, '%', p.lineno(2), find_column(p.slice[2]))
            elif p[2] == '>>':
                p[0] = ArithmeticBinaryOperation(
                    p[1], p[3], SymbolsAritmeticos.BITWISE_SHIFT_RIGHT, '>>', p.lineno(2), find_column(p.slice[2]))
            elif p[2] == '<<':
                p[0] = ArithmeticBinaryOperation(
                    p[1], p[3], SymbolsAritmeticos.BITWISE_SHIFT_LEFT, '<<', p.lineno(2), find_column(p.slice[2]))
            elif p[2] == '&':
                p[0] = ArithmeticBinaryOperation(
                    p[1], p[3], SymbolsAritmeticos.BITWISE_AND, '&', p.lineno(2), find_column(p.slice[2]))
            elif p[2] == '|':
                p[0] = ArithmeticBinaryOperation(
                    p[1], p[3], SymbolsAritmeticos.BITWISE_OR, '|', p.lineno(2), find_column(p.slice[2]))
            elif p[2] == '#':
                p[0] = ArithmeticBinaryOperation(
                    p[1], p[3], SymbolsAritmeticos.BITWISE_XOR, '#', p.lineno(2), find_column(p.slice[2]))
    elif (len(p) == 3):
        if p[1] == '-':
            p[0] = UnaryOrSquareExpressions(
                SymbolsUnaryOrOthers.UMINUS, p[2], p.lineno(1), find_column(p.slice[1]), p[1])
        elif p[1] == '+':
            p[0] = UnaryOrSquareExpressions(
                SymbolsUnaryOrOthers.UPLUS, p[2], p.lineno(1), find_column(p.slice[1]), p[1])
        elif p[1] == '||/':
            p[0] = UnaryOrSquareExpressions(
                SymbolsUnaryOrOthers.CUBE_ROOT, p[2], p.lineno(1), find_column(p.slice[1]), p[1])
        elif p[1] == '|/':
            p[0] = UnaryOrSquareExpressions(
                SymbolsUnaryOrOthers.SQUARE_ROOT, p[2], p.lineno(1), find_column(p.slice[1]), p[1])
        elif p[1] == '~':
            p[0] = UnaryOrSquareExpressions(
                SymbolsUnaryOrOthers.BITWISE_NOT, p[2], p.lineno(1), find_column(p.slice[1]), p[1])
    else:
        if p.slice[1].type == "TRUE" or p.slice[1].type == "FALSE":
            v = True
            if p.slice[1].type == "FALSE":
                v = False
            p[0] = PrimitiveData(DATA_TYPE.BOOLEANO, v, p.lineno(1), find_column(p.slice[1]))
        else:
            p[0] = p[1]


def p_sql_expression_list(p):
    '''SQLEXPRESSIONLIST : SQLEXPRESSIONLIST COMMA SQLEXPRESSION
                         | SQLEXPRESSION'''
    if (len(p) == 4):
        p[1].append(p[3])
        p[0] = p[1]
    elif (len(p) == 2):
        p[0] = [p[1]]


def p_mathematical_functions(p):
    '''MATHEMATICALFUNCTIONS : ABS LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | CBRT LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | CEIL LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | CEILING LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | DEGREES LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | DIV LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | EXP LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | FACTORIAL LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | FLOOR LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | GCD LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | LN LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | LOG LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | MOD LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | PI LEFT_PARENTHESIS RIGHT_PARENTHESIS
                             | POWER LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | RADIANS LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | ROUND LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | SIGN LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | SQRT LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | WIDTH_BUCKET LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | TRUNC LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                             | RANDOM LEFT_PARENTHESIS RIGHT_PARENTHESIS '''

    # TODO: RANDOM Y MANEJO DE ALIAS
    if p.slice[1].type == "ABS":
        p[0] = Abs(p[3], p[1], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "CBRT":
        p[0] = Cbrt(p[3], p[1], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "CEIL":
        p[0] = Ceil(p[3], p[1], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "CEILING":
        p[0] = Ceiling(p[3], p[1], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "DEGREES":
        p[0] = Degrees(p[3], p[1], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "DIV":
        p[0] = Div(p[3], p[5], p[1], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "EXP":
        p[0] = Exp(p[3], p[1], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "FACTORIAL":
        p[0] = Factorial(p[3], p[1], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "FLOOR":
        p[0] = Floor(p[3], p[1], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "GCD":
        p[0] = Gcd(p[3], p[5], p[1], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "LN":
        p[0] = Ln(p[3], p[1], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "LOG":
        p[0] = Log(p[3], p[1], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "MOD":
        p[0] = Mod(p[3], p[5], p[1], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "PI":
        p[0] = Pi(p[1], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "POWER":
        p[0] = Power(p[3], p[5], p[1], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "RADIANS":
        p[0] = Radians(p[3], p[1], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "ROUND":
        p[0] = Round(p[3], p[5], p[1], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "SIGN":
        p[0] = Sign(p[3], p[1], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "SQRT":
        p[0] = Sqrt(p[3], p[1], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "WIDTH_BUCKET":
        p[0] = WithBucket(p[3], p[5], p[7], p[9], p[1],
                          p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "TRUNC":
        p[0] = Trunc(p[3], p[1], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "RANDOM":
        p[0] = Random(p[1], p.lineno(1), find_column(p.slice[1]))


def p_binary_string_functions(p):
    '''BINARY_STRING_FUNCTIONS : LENGTH LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | SUBSTRING LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | TRIM LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | MD5 LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | SHA256 LEFT_PARENTHESIS SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | SUBSTR LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION RIGHT_PARENTHESIS
                               | CONVERT LEFT_PARENTHESIS SQLSIMPLEEXPRESSION AS DATE RIGHT_PARENTHESIS
                               | CONVERT LEFT_PARENTHESIS SQLSIMPLEEXPRESSION AS INTEGER RIGHT_PARENTHESIS
                               | DECODE LEFT_PARENTHESIS SQLSIMPLEEXPRESSION COMMA SQLSIMPLEEXPRESSION  RIGHT_PARENTHESIS'''
    if p.slice[1].type == "LENGTH":
        p[0] = Length(p[3], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "SUBSTRING":
        p[0] = Substring(p[3], p[5], p[7], p.lineno(1),
                         find_column(p.slice[1]))
    elif p.slice[1].type == "TRIM":
        p[0] = Trim(p[3], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "MD5":
        p[0] = MD5(p[3], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "SHA256":
        p[0] = SHA256(p[3], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "SUBSTR":
        p[0] = Substr(p[3], p[5], p[7], p.lineno(1), find_column(p.slice[1]))
    elif p.slice[1].type == "CONVERT":
        p[0] = Convert(p[3], p[5], p.lineno(1), find_column(p.slice[1]))
    else:  # p.slice[1].type == "DECODE"
        p[0] = Decode(p[3], p[1], p.lineno(1), find_column(p.slice[1]))


def p_greatest_or_least(p):
    '''GREATESTORLEAST : GREATEST LEFT_PARENTHESIS LISTVALUESINSERT RIGHT_PARENTHESIS
                       | LEAST LEFT_PARENTHESIS LISTVALUESINSERT RIGHT_PARENTHESIS'''
    string = ""
    for index, var in enumerate(p[3]):
                if index > 0: string += f', {var._tac}'
                else: string += f'{var._tac}'
    if p.slice[1].type == "GREATEST":
        p[0] = Greatest(p[3], p[1], p.lineno(1), find_column(p.slice[1]))
        p[0]._tac = f"GREATEST({string})"
    else:
        p[0] = Least(p[3], p[1], p.lineno(1), find_column(p.slice[1]))
        p[0]._tac = f"LEAST({string})"

def p_case_clause(p):
    '''CASECLAUSE : CASE CASECLAUSELIST END CASE SEMICOLON
                  | CASE CASECLAUSELIST ELSE STATEMENTS END CASE SEMICOLON
                  | CASE OBJECTREFERENCE CASECLAUSELIST END CASE SEMICOLON
                  | CASE OBJECTREFERENCE CASECLAUSELIST ELSE STATEMENTS END CASE SEMICOLON'''
    if p.slice[2].type == "OBJECTREFERENCE": 
        if(len(p) == 7):
            p[0] = Case(p[2], p[3], None, p.lineno(1), find_column(p.slice[1]))
        else:
            p[0] = Case(p[2], p[3], p[5], p.lineno(1), find_column(p.slice[1]))
    else:             
        if(len(p) == 6):
            p[0] = Case(None, p[2], None, p.lineno(1), find_column(p.slice[1]))
        else:
            p[0] = Case(None, p[2], p[4], p.lineno(1), find_column(p.slice[1]))


def p_case_clause_list(p):
    '''CASECLAUSELIST : CASECLAUSELIST WHEN SQLEXPRESSIONLIST THEN STATEMENTS
                      | WHEN SQLEXPRESSIONLIST THEN STATEMENTS'''

    if (len(p) == 6):
        p[1].append( CaseOption(p[3], p[5], 0, 0) )
        p[0] = p[1]
    else:
        p[0] = [ CaseOption(p[2], p[4], 0, 0) ]


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
    if (len(p) == 5):
        p[0] = ExpressionsTrigonometric(
            p[1], p[3], None, p.lineno(1), find_column(p.slice[1]))
        p[0]._tac = f'{p[1]}({p[3].alias})'
    else:
        p[0] = ExpressionsTrigonometric(
            p[1], p[3], p[5], p.lineno(1), find_column(p.slice[1]))
        p[0]._tac = f'{p[1]}({p[3].alias},{p[5].alias})'


def p_sql_alias(p):
    '''SQLALIAS : AS SQLNAME
                | SQLNAME'''
    if (len(p) == 3):
        p[0] = p[2]
        p[0]._tac = f"{p[1]} {p[2]._tac}"
    elif (len(p) == 2):
        p[0] = p[1]


def p_expressions_time(p):
    '''EXPRESSIONSTIME : EXTRACT LEFT_PARENTHESIS DATETYPES FROM TIMESTAMP SQLNAME RIGHT_PARENTHESIS
                       | EXTRACT LEFT_PARENTHESIS DATETYPES FROM SQLNAME RIGHT_PARENTHESIS
                       | NOW LEFT_PARENTHESIS RIGHT_PARENTHESIS
                       | DATE_PART LEFT_PARENTHESIS SQLNAME COMMA INTERVAL SQLNAME RIGHT_PARENTHESIS
                       | CURRENT_DATE
                       | CURRENT_TIME
                       | TIMESTAMP SQLNAME'''
    if (len(p) == 8):
        if p.slice[1].type.upper() == 'EXTRACT':
            p[0] = ExpressionsTime(
                SymbolsTime.EXTRACT, p[3], p[6], p[1], p.lineno(1), find_column(p.slice[1]))
            p[0]._tac = f'EXTRACT ( {p[3]._tac} FROM TIMESTAMP {p[6]._tac} )'
        elif p.slice[1].type.upper() == 'DATE_PART':
            p[0] = ExpressionsTime(
                SymbolsTime.DATE_PART, p[3], p[6], p[1], p.lineno(1), find_column(p.slice[1]))
            p[0]._tac = f'DATE_PART ({p[3]._tac} , INTERVAL {p[6]._tac})'
    elif (len(p) == 3):
        p[0] = ExpressionsTime(SymbolsTime.TIMESTAMP, None,
                               p[2], p[1], p.lineno(1), find_column(p.slice[1]))
        p[0]._tac = f'TIMESTAMP {p[2]._tac}'
    elif (len(p) == 7):
        p[0] = ExtractFromIdentifiers(
            SymbolsTime.EXTRACT, p[3], p[5], p[1], p.lineno(1), find_column(p.slice[1]))
        p[0]._tac = f"EXTRACT ({p[3]} FROM {p[5]._tac})"
    else:
        if p.slice[1].type.upper() == 'CURRENT_DATE':
            p[0] = ExpressionsTime(SymbolsTime.CURRENT_DATE, None, None, p[1], p.lineno(
                1), find_column(p.slice[1]))
            p[0]._tac = f'CURRENT_DATE'
        elif p.slice[1].type.upper() == 'CURRENT_TIME':
            p[0] = ExpressionsTime(SymbolsTime.CURRENT_TIME, None, None, p[1], p.lineno(
                1), find_column(p.slice[1]))
            p[0]._tac = f'CURRENT_TIME'
        elif p.slice[1].type.upper() == 'NOW':
            p[0] = ExpressionsTime(
                SymbolsTime.NOW, None, None, p[1], p.lineno(1), find_column(p.slice[1]))
            p[0]._tac = f'NOW()'


def p_aggregate_functions(p):
    '''AGGREGATEFUNCTIONS : AGGREGATETYPES LEFT_PARENTHESIS CONTOFAGGREGATE RIGHT_PARENTHESIS
                          | AGGREGATETYPES LEFT_PARENTHESIS CONTOFAGGREGATE RIGHT_PARENTHESIS SQLALIAS'''
    if (len(p) == 5):
        p[0] = AgreggateFunctions(
            p[1], p[3], None, p.lineno(2), find_column(p.slice[2]))
        p[0]._tac = f'{p[1]} ({p[3]._tac})'
    else:
        p[0] = AgreggateFunctions(
            p[1], p[3], p[5], p.lineno(2), find_column(p.slice[2]))
        p[0]._tac = f'{p[1]}({p[3]._tac}) {p[5]}'

def p_cont_of_aggregate(p):
    '''CONTOFAGGREGATE : ASTERISK
                       | SQLSIMPLEEXPRESSION'''
    if (p[1] == '*'):
        p[0] = PrimitiveData(DATA_TYPE.STRING, p[1],
                             p.lineno(1), find_column(p.slice[1]))
    else:
        p[0] = p[1]


def p_sql_object_reference(p):
    '''OBJECTREFERENCE : SQLNAME DOT ASTERISK
                       | SQLNAME DOT SQLNAME
                       | SQLNAME'''
    if (len(p) == 2):
        p[0] = ObjectReference(p[1], None, None)
        p[0]._tac = f'{p[1]._tac}'
    elif (len(p) == 4):
        if p[3] == "*":
            p[0] = ObjectReference(p[1], p[3], None)
            p[0]._tac = f'{p[1]._tac}{p[2]}{p[3]}'
        else:
            p[0] = ObjectReference(p[3], None, p[1])
            p[0]._tac = f'{p[1]._tac}{p[2]}{p[3]._tac}'


def p_list_values_insert(p):
    '''LISTVALUESINSERT : LISTVALUESINSERT COMMA SQLSIMPLEEXPRESSION
                        | LISTVALUESINSERT COMMA CALL_FUNCTIONS_PROCEDURE
                        | SQLSIMPLEEXPRESSION
                        | CALL_FUNCTIONS_PROCEDURE'''
    if(len(p) == 4):
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]


def p_type_combine_query(p):
    '''TYPECOMBINEQUERY : UNION
                        | INTERSECT
                        | EXCEPT'''
    p[0] = p[1]


def p_relop(p):
    '''RELOP : EQUALS 
             | NOT_EQUAL
             | GREATE_EQUAL
             | GREATE_THAN
             | LESS_THAN
             | LESS_EQUAL
             | NOT_EQUAL_LR'''
    p[0] = [p.slice[1], p[1]]


def p_aggregate_types(p):
    '''AGGREGATETYPES : AVG
                      | SUM
                      | COUNT
                      | MAX
                      | MIN'''
    p[0] = p[1]


def p_date_types(p):
    '''DATETYPES : YEAR
                 | MONTH
                 | DAY
                 | HOUR
                 | MINUTE
                 | SECOND'''
    p[0] = PrimitiveData(DATA_TYPE.STRING, p[1],
                         p.lineno(1), find_column(p.slice[1]))


def p_sql_integer(p):
    '''SQLINTEGER : INT_NUMBER
                  | FLOAT_NUMBER'''
    p[0] = PrimitiveData(DATA_TYPE.NUMBER, p[1],
                         p.lineno(1), find_column(p.slice[1]))


def p_sql_name(p):
    '''SQLNAME : STRINGCONT
               | CHARCONT
               | ID'''
    if p.slice[1].type == "STRINGCONT" or p.slice[1].type == "CHARCONT":
        p[0] = PrimitiveData(DATA_TYPE.STRING, p[1],
                             p.lineno(1), find_column(p.slice[1]))                     
        p[0]._tac = f'\'{p[1]}\''

    else:
        p[0] = Identifiers(p[1], p.lineno(1), find_column(p.slice[1]))
        p[0]._tac = f'{p[1]}'
        

def p_type_select(p):
    '''TYPESELECT : ALL
                  | DISTINCT
                  | UNIQUE'''
    p[0] = p[1]


def p_sub_query(p):
    '''SUBQUERY : SELECTSTATEMENT'''
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


def parse(inpu):
    global input, contador_instr
    contador_instr = 0
    ErrorController().destroy()
    lexer = lex.lex()
    lexer.lineno = 1
    input = inpu
    get_text(input)
    return parser.parse(inpu, lexer=lexer)


# Generacion de C3D
def generateC3D(p):
    global contador_instr
    arr_instr = p.lexer.lexdata.split(sep=";", maxsplit=contador_instr+1)
    aux = arr_instr[contador_instr].replace("\n", " ").strip()
    return ' '.join(aux.split())
    #temp = ThreeAddressCode().newTemp()
    #ThreeAddressCode().addCode(f"{temp} = '{aux};'")
