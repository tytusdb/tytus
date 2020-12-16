# from generate_ast import GraficarAST
from re import L

import libs.ply.yacc as yacc
import os

from models.instructions.shared import *
from models.instructions.DDL.database_inst import *
from models.instructions.DDL.table_inst import *
from models.instructions.DDL.column_inst import *
from models.instructions.DDL.type_inst import *
from models.instructions.DML.dml_instr import *
from models.instructions.DML.select import *
from models.instructions.Expression.expression import *
from controllers.error_controller import ErrorController
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
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]

    else:
        p[0] = [p[1]]


def p_sql_instruction(p):
    '''sqlinstruction : ddl
                    | DML
                    | MULTI_LINE_COMMENT
                    | SINGLE_LINE_COMMENT
                    | error SEMICOLON
    '''
    p[0] = p[1]


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


def p_option_create(p):
    '''optioncreate : TYPE SQLNAME AS ENUM LEFT_PARENTHESIS typelist RIGHT_PARENTHESIS
                    | DATABASE createdb
                    | OR REPLACE DATABASE createdb
                    | TABLE SQLNAME LEFT_PARENTHESIS columnstable RIGHT_PARENTHESIS
                    | TABLE SQLNAME LEFT_PARENTHESIS columnstable RIGHT_PARENTHESIS INHERITS LEFT_PARENTHESIS ID RIGHT_PARENTHESIS
    '''
    noColumn = 0
    noLine = 0

    if len(p) == 8:
        p[0] = CreateType(p[2],p[6])

    elif len(p) == 3:
        p[0] = CreateDB(p[2], False, noLine, noColumn)

    elif len(p) == 5:
        p[0] = CreateDB(p[4], True, noLine, noColumn)

    elif len(p) == 6:
        p[0] = CreateTB(p[2], p[4], None)

    elif len(p) == 10:
        p[0] = CreateTB(p[2], p[4], p[6])  # TODO INHERITS


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
    p[0] = {'if_not_exists': False, 'id': None, 'listpermits': []}

    if len(p) == 6:
        p[0]['if_not_exists'] = True
        p[0]['id'] = p[4]
        p[0]['listpermits'] = p[5]

    elif len(p) == 5:
        p[0]['if_not_exists'] = True
        p[0]['id'] = p[4]

    elif len(p) == 3:
        p[0]['id'] = p[1]
        p[0]['listpermits'] = p[2]

    else:
        p[0]['id'] = p[1]


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
    '''permits : OWNER EQUALS ID
               | OWNER ID
               | MODE EQUALS INT_NUMBER
               | MODE INT_NUMBER 
    '''
    p[0] = []


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

    if len(p) == 4:
        p[0] = CreateCol(p[1], p[2], p[3])

    elif len(p) == 3:
        p[0] = CreateCol(p[1], p[2], None)

    elif len(p) == 5:
        if p[1] == 'UNIQUE':
            p[0] = Unique(p[3])

        else:  # CHECK
            p[0] = Check(p[3])

    elif len(p) == 6:
        p[0] = PrimaryKey(p[4])

    elif len(p) == 11:
        p[0] = ForeignKey(p[4], p[7], p[9])

    elif len(p) == 7:
        p[0] = Constraint(p[2], p[5])  # TODO revisar si es constraint o check


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
    dataType = ''
    for i in range(1, len(p)):
        dataType += str(p[i])
    p[0] = dataType


def p_options_col_list(p):
    '''optionscollist : optionscollist optioncol
                      | optioncol
    '''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]

    else:
        p[0] = [p[1]]


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
                     | SHOW DATABASES LIKE ID SEMICOLON
    '''
    if len(p) == 4:
        p[0] = ShowDatabase(None)
    else:
        p[0] = ShowDatabase(p[4])


def p_alter_statement(p):
    '''alterstatement : ALTER optionsalter SEMICOLON
    '''
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
    if p[2].lower() == 'RENAME'.lower():   #Renombra la base de datos
        p[0] = AlterDatabase(1,p[1],p[4])
    else:                                  #Le cambia el duenio a la base de datos
        p[0] = AlterDatabase(2,p[1],p[4])


def p_type_owner(p):
    '''typeowner : ID
                 | CURRENT_USER
                 | SESSION_USER 
    '''
    p[0] = p[1]


def p_alter_table(p):
    '''altertable : ID alterlist
    '''
    p[0] = AlterTable(p[1],p[2])


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
    p[0] = p[2]


def p_add_alter(p):
    '''addalter : COLUMN ID typecol
                | CHECK LEFT_PARENTHESIS conditionColumn RIGHT_PARENTHESIS
                | CONSTRAINT ID UNIQUE LEFT_PARENTHESIS ID RIGHT_PARENTHESIS
                | FOREIGN KEY LEFT_PARENTHESIS ID RIGHT_PARENTHESIS REFERENCES ID
    '''
    if len(p) == 4:
        p[0] = AlterTableAdd(CreateCol(p[2],p[3],None))
    elif len(p) == 5:
        p[0] = AlterTableAdd(Check(p[4]))
    elif len(p) == 7:
        p[0] = AlterTableAdd(Constraint(p[5],Unique(p[5]))) #TODO revisar esta asignacion
    else:
        p[0] = AlterTableAdd(ForeignKey(p[4],None,p[7]))   #TODO revisar esta asignacion


def p_alter_alter(p):
    '''alteralter : COLUMN ID SET NOT NULL
                  | COLUMN ID TYPE typecol
    '''
    if len(p) == 6:
        p[0] = AlterTableAlter(None) #TODO agregar un chanceType en column
    else:
        p[0] = AlterTableAlter(None) #TODO agregar un chanceType en column


def p_drop_alter(p):
    '''dropalter : COLUMN ID
                 | CONSTRAINT ID
    '''
    if p[1].lower() == 'COLUMN'.lower():
        p[0] = AlterTableDrop(None) #TODO agregar un dropColumn en column
    else:
        p[0] = AlterTableDrop(None) #TODO agregar un dropConstrain en column


def p_rename_alter(p):
    '''renamealter : COLUMN ID TO ID
    '''
    p[0] = AlterTableRename(p[2],p[4])


def p_drop_statement(p):
    '''dropstatement : DROP optionsdrop SEMICOLON'''
    p[0] = p[2]


def p_options_drop(p):
    '''optionsdrop : DATABASE dropdatabase
                    | TABLE droptable
    '''
    p[0] = p[2]


def p_drop_database(p):
    '''dropdatabase : IF EXISTS ID
                    | ID
    '''
    noColumn = 0
    noLine = 0
    if len(p) == 4:
        p[0] = DropDB(True, p[3], noLine, noColumn)
    else:
        p[0] = DropDB(False, p[1], noLine, noColumn)


def p_drop_table(p):
    '''droptable : ID
    '''
    noColumn = 0
    noLine = 0
    p[0] = DropTB(p[1], noLine, noColumn)


# =====================================================================================
# =====================================================================================
# =====================================================================================

def p_dml(p):
    '''DML : QUERYSTATEMENT
           | INSERTSTATEMENT
           | DELETESTATEMENT
           | UPDATESTATEMENT'''
    p[0] = p[1]


def p_update_statement(p):
    '''UPDATESTATEMENT : UPDATE ID OPTIONS1 SET SETLIST OPTIONSLIST2 SEMICOLON
                       | UPDATE ID SET SETLIST OPTIONSLIST2 SEMICOLON
                       | UPDATE ID SET SETLIST  SEMICOLON '''
    if(len(p) == 7):
        p[0] = Update(p[2],p[5],p[6])
    elif(len(p) == 6):
        p[0] = Update(p[2],p[4],p[5])
    else:
        p[0] = Update(p[2],p[4],None)

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
    p[0] = ColumnVal(p[1],p[2])


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


def p_delete_statement(p):
    '''DELETESTATEMENT : DELETE FROM ID OPTIONSLIST SEMICOLON
                       | DELETE FROM ID SEMICOLON '''
    if (len(p) == 6):
        p[0] = Delete(p[3],p[4])
    else:
        p[0] = Delete(p[3],None)

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
    #TODO: PROBAR SI REALMENTE SIRVE EL ARBOL XD

def p_options1(p):
    '''OPTIONS1 : ASTERISK SQLALIAS
                | ASTERISK
                | SQLALIAS'''
    if(len(p) == 2):
        p[0] = Opt1(True, p[2])
    else:
        if(p[1] == "*"):
            p[0] = Opt1(True, None)
        else:
            p[0] = Opt1(False, p[2])

def p_options2(p):
    '''OPTIONS2 : USING USINGLIST'''
    p[0] = Using(p[2])

def p_using_list(p):
    '''USINGLIST  : USINGLIST COMMA SQLNAME
                  | SQLNAME'''
    if(len(p) == 4):
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

# def p_options3(p):
#     '''OPTIONS3 : WHERE SQLEXPRESSION'''
#     p[0] = Where(p[2]) --------> GRAMATICA SE REPITE

def p_options4(p):
    '''OPTIONS4 : RETURNING RETURNINGLIST'''
    p[0] = Returning(p[2])

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
    if(len(p) == 12):
        p[0] = Insert(p[3],p[5],p[9])
    else:
        p[0] = Insert(p[3],None,p[6])

def p_list_params_insert(p):
    '''LISTPARAMSINSERT : LISTPARAMSINSERT COMMA ID
                        | ID'''
    if(len(p) == 4):
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_query_statement(p):
    #  ELEMENTO 0       ELEMENTO 1     ELEMENTO 2      ELEMENTO 3
    '''QUERYSTATEMENT : SELECTSTATEMENT SEMICOLON'''
    p[0] = p[1]

def p_select_statement(p):
    '''SELECTSTATEMENT : SELECTWITHOUTORDER ORDERBYCLAUSE LIMITCLAUSE
                       | SELECTWITHOUTORDER ORDERBYCLAUSE 
                       | SELECTWITHOUTORDER LIMITCLAUSE 
                       | SELECTWITHOUTORDER'''
    if (len(p) == 4):
        p[0] = Select(p[1], p[2], p[3])
    elif (len(p) == 3):
        if ('ORDER' in p[2]):
            p[0] = Select(p[1], p[2], None)
        elif ('LIMIT' in p[2]):
            p[0] = Select(p[1], None, p[2])
    elif (len(p) == 2):
        p[0] = Select(p[1], None, None)


def p_select_without_order(p):
    '''SELECTWITHOUTORDER : SELECTSET
                          | SELECTWITHOUTORDER TYPECOMBINEQUERY ALL SELECTSET
                          | SELECTWITHOUTORDER TYPECOMBINEQUERY SELECTSET'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 5:
        type_combine_query = TypeQuerySelect(p[2], p[3])
        p[1].append(type_combine_query)
        p[1].append(p[4])
        p[0] = p[1]
    elif len(p) == 4:
        type_combine_query = TypeQuerySelect(p[2], optionAll=None)
        p[1].append(type_combine_query)
        p[1].append(p[3])
        p[0] = p[1]
    


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
    if len(p) == 4:
        p[0] = SelectQ(None, p[2], p[3], None)
    elif len(p) == 5:
        if ("ALL" in p[2] or 'DISTINCT' in p[2] or 'UNIQUE' in p[2]):
            p[0] = SelectQ(p[2], p[3], p[4], None)
        else:
            p[0] = SelectQ(None, p[2], p[3], p[4])
    elif len(p) == 6:
        p[0] = SelectQ(p[2], p[3], p[4], p[5])
    elif len(p) == 3:
        p[0] = SelectQ(None, p[2], None, None)


def p_select_list(p):
    '''SELECTLIST : ASTERISK
                  | LISTITEM'''
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
    '''SELECTITEM : SQLSIMPLEEXPRESSION SQLALIAS
                  | SQLSIMPLEEXPRESSION
                  | LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS'''
    if (len(p) == 3):
        p[0] = [p[1], p[2]]
    elif (len(p) == 4):
        p[0] = p[2]
    elif (len(p) == 2):
        p[0] = p[1]


def p_from_clause(p):
    '''FROMCLAUSE : FROM FROMCLAUSELIST'''
    p[0] = From(p[2])

def p_from_clause_list(p):
    '''FROMCLAUSELIST : FROMCLAUSELIST COMMA TABLEREFERENCE
                      | FROMCLAUSELIST LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS SQLALIAS
                      | FROMCLAUSELIST LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS
                      | LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS
                      | LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS SQLALIAS
                      | TABLEREFERENCE'''
    if (len(p) == 6):
        p[1].append(p[3])
        p[1].append(p[5])
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
    if (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 3):
        p[0] = [p[1], p[2]]


def p_table_reference(p):
    '''TABLEREFERENCE : OBJECTREFERENCE SQLALIAS
                      | OBJECTREFERENCE SQLALIAS JOINLIST
                      | OBJECTREFERENCE JOINLIST
                      | OBJECTREFERENCE'''
    if (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 3):
        p[0] = [p[1], p[2]]
    elif (len(p) == 4):
        p[0] = [p[1], p[2], p[3]]


def p_order_by_clause(p):
    '''ORDERBYCLAUSE : ORDER BY ORDERBYCLAUSELIST'''
    p[0] = p[3]

def p_order_by_clause_list(p):
    '''ORDERBYCLAUSELIST : ORDERBYCLAUSELIST COMMA ORDERBYEXPRESSION
                         | ORDERBYEXPRESSION'''
    if (len(p) == 4):
        p[1].append(p[3])
        p[0] = p[1]
    elif (len(p) == 2):
        p[0] = [p[1]]
   


def p_order_by_expression(p):
    '''ORDERBYEXPRESSION : SQLSIMPLEEXPRESSION ASC
                         | SQLSIMPLEEXPRESSION DESC
                         | SQLSIMPLEEXPRESSION'''
    if (len(p) == 3):
        p[0] = OrderClause(p[1], p[2])
    elif (len(p) == 2):
        p[0] = OrderClause(p[1], type_order=None)

def p_limit_clause(p):
    '''LIMITCLAUSE : LIMIT LIMITOPTIONS'''
    p[0] = [p[1], p[2]]

def p_limit_options(p):
    '''LIMITOPTIONS : LIMITTYPES OFFSETOPTION
                    | LIMITTYPES'''
    
    if (len(p) == 3):
        p[0] = LimitClause(p[1], p[2])
    else:
        p[0] = LimitClause(p[1], offset=None)
    

def p_limit_types(p):
    '''LIMITTYPES : LISTLIMITNUMBER
                  | ALL'''
    
    p[0] = p[1]
   

def p_list_limit_number(p):
    '''LISTLIMITNUMBER : LISTLIMITNUMBER COMMA INT_NUMBER
                       | INT_NUMBER'''
    
    if (len(p) == 2):
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
        p[0] = p[1]


def p_offset_option(p):
    '''OFFSETOPTION : OFFSET INT_NUMBER'''
    p[0] = p[2]

def p_where_clause(p):
    '''WHERECLAUSE : WHERE SQLEXPRESSION'''
    p[0] = Where(p[2])


def p_group_by_clause(p):
    '''GROUPBYCLAUSE : GROUP BY SQLEXPRESSIONLIST'''
    p[0] = GroupBy(p[3])


def p_having_clause(p):
    '''HAVINGCLAUSE : HAVING SQLEXPRESSION'''
    p[0] = Having(p[2])


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
    p[0] = JoinClause(p[1], p[3], p[5])


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
        p[0] = LogicalOperators(p[1], p[2], p[3])
    elif len(p) == 3:
        p[0] = NotOption(p[2])
    else:
        p[0] = p[1]

def p_exits_or_relational_clause(p):
    '''EXISTSORSQLRELATIONALCLAUSE : EXISTSCLAUSE
                                   | SQLRELATIONALEXPRESSION'''
    p[0] = p[1]
    
def p_exists_clause(p):
    '''EXISTSCLAUSE : EXISTS LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS'''
    p[0] = ExistsClause(p[3])


def p_sql_relational_expression(p):
    '''SQLRELATIONALEXPRESSION : SQLSIMPLEEXPRESSION RELOP SQLSIMPLEEXPRESSION
                               | SQLSIMPLEEXPRESSION SQLINCLAUSE
                               | SQLSIMPLEEXPRESSION SQLBETWEENCLAUSE
                               | SQLSIMPLEEXPRESSION SQLLIKECLAUSE
                               | SQLSIMPLEEXPRESSION SQLISCLAUSE
                               | SQLSIMPLEEXPRESSION'''
    if (len(p) == 3):
        p[0] = [p[1], p[2]]
    elif (len(p) == 4):
        if p[2] == '==':
            p[0] = Relop(p[1], SymbolsRelop.EQUALS, p[3])
        elif p[2] == '!=':
            p[0] = Relop(p[1], SymbolsRelop.NOT_EQUAL, p[3])
        elif p[2] == '>=':
            p[0] = Relop(p[1], SymbolsRelop.GREATE_EQUAL, p[3])
        elif p[2] == '>':
            p[0] = Relop(p[1], SymbolsRelop.GREATE_THAN, p[3])
        elif p[2] == '<=':
            p[0] = Relop(p[1], SymbolsRelop.LESS_EQUAL, p[3])
        elif p[2] == '<':
            p[0] = Relop(p[1], SymbolsRelop.LESS_THAN, p[3])
        elif p[2] == '<>':
            p[0] = Relop(p[1], SymbolsRelop.NOT_EQUAL_LR, p[3])
    else:
        p[0] = p[1]



def p_sql_in_clause(p):
    '''SQLINCLAUSE  : NOT IN LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS
                    | IN LEFT_PARENTHESIS SUBQUERY RIGHT_PARENTHESIS
                    | IN LEFT_PARENTHESIS listain RIGHT_PARENTHESIS'''
    if (len(p) == 6):
        p[0] = InClause(NotOption(p[4]))
    else:
        p[0] = InClause(p[3])

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
        if (p[3] == 'SYMMETRIC'):
            p[0] = Between(None, True, p[3], p[5])
        else:
            p[0] = Between(True, None, p[3], p[5])
    elif (len(p) == 5):
        p[0] = Between(None, True, p[3], p[5])
    else:
        p[0] = Between(True, True, p[4], p[6])

def p_sql_like_clause(p):
    '''SQLLIKECLAUSE  : NOT LIKE SQLSIMPLEEXPRESSION
                      | LIKE SQLSIMPLEEXPRESSION'''
    if (len(p) == 4):
        p[0] = LikeClause(NotOption(p[3]))
    else:
        p[0] = LikeClause(p[2])

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
    if (len(p) == 4):
        if (p[1] == "("):
            p[0] = p[2]
        else:
            if p[2] == '+':
                p[0] = ArithmeticBinaryOperation(p[1],p[3],SymbolsAritmeticos.PLUS)
            elif p[2] == '-':
                p[0] = ArithmeticBinaryOperation(p[1],p[3],SymbolsAritmeticos.MINUS)
            elif p[2] == '*':
                p[0] = ArithmeticBinaryOperation(p[1],p[3],SymbolsAritmeticos.TIMES)
            elif p[2] == '/':
                p[0] = ArithmeticBinaryOperation(p[1],p[3],SymbolsAritmeticos.DIVISON)
            elif p[2] == '^':
                p[0] = ArithmeticBinaryOperation(p[1],p[3], SymbolsAritmeticos.EXPONENT)
            elif p[2] == '%':
                p[0] = ArithmeticBinaryOperation(p[1],p[3], SymbolsAritmeticos.MODULAR)
            elif p[2] == '>>':
                p[0] = ArithmeticBinaryOperation(p[1],p[3], SymbolsAritmeticos.BITWISE_SHIFT_RIGHT)
            elif p[2] == '<<':
                p[0] = ArithmeticBinaryOperation(p[1],p[3], SymbolsAritmeticos.BITWISE_SHIFT_LEFT)
            elif p[2] == '&':
                p[0] = ArithmeticBinaryOperation(p[1],p[3], SymbolsAritmeticos.BITWISE_AND)
            elif p[2] == '|':
                p[0] = ArithmeticBinaryOperation(p[1],p[3], SymbolsAritmeticos.BITWISE_OR)
            elif p[2] == '#':
                 p[0] = ArithmeticBinaryOperation(p[1],p[3], SymbolsAritmeticos.BITWISE_XOR)
    elif (len(p) == 3):
        p[0] = UnaryOrSquareExpressions(p[1], p[2])
    else:
        if  p.slice[1].type == "TRUE" or p.slice[1].type == "FALSE":
            p[0] = PrimitiveData(DATA_TYPE.BOOLEANO, p[1])
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
    if (len(p) == 6):
        p[0] = MathematicalExpressions(p[1], p[3], p[5])
    elif (len(p) == 5):
        if (p[1] == 'PI' or p[1] == 'RANDOM'):
            p[0] = MathematicalExpressions(p[1], None, p[4])
        else:
            p[0] = MathematicalExpressions(p[1], p[3], None)
    elif (len(p) == 8):
        p[0] = MathematicalExpressions(p[1], [p[3], p[5]], p[7])
    elif (len(p) == 7):
        p[0] = MathematicalExpressions(p[1], [p[3], p[5]], None)
    elif (len(p) == 12):
        p[0] = MathematicalExpressions(p[1], [p[3], p[5], p[7], p[9]], p[11])
    elif (len(p) == 11):
        p[0] = MathematicalExpressions(p[1], [p[3], p[5], p[7], p[9]], None)

def p_binary_string_functions(p):
    '''BINARY_STRING_FUNCTIONS : LENGTH LEFT_PARENTHESIS ID RIGHT_PARENTHESIS
                               | SUBSTRING LEFT_PARENTHESIS  SQLNAME COMMA INT_NUMBER COMMA INT_NUMBER RIGHT_PARENTHESIS
                               | TRIM LEFT_PARENTHESIS ID RIGHT_PARENTHESIS
                               | MD5 LEFT_PARENTHESIS STRINGCONT RIGHT_PARENTHESIS
                               | SHA256 LEFT_PARENTHESIS STRINGCONT RIGHT_PARENTHESIS
                               | SUBSTR LEFT_PARENTHESIS ID COMMA INT_NUMBER COMMA INT_NUMBER RIGHT_PARENTHESIS
                               | CONVERT LEFT_PARENTHESIS SQLNAME AS DATE RIGHT_PARENTHESIS
                               | CONVERT LEFT_PARENTHESIS SQLNAME AS INTEGER RIGHT_PARENTHESIS
                               | DECODE LEFT_PARENTHESIS STRINGCONT COMMA STRINGCONT  RIGHT_PARENTHESIS'''
def p_greatest_or_least(p):
    '''GREATESTORLEAST : GREATEST LEFT_PARENTHESIS LISTVALUESINSERT RIGHT_PARENTHESIS
                       | LEAST LEFT_PARENTHESIS LISTVALUESINSERT RIGHT_PARENTHESIS'''
    p[0] = ExpressionsGreastLeast(p[1], p[3])

def p_case_clause(p):
    '''CASECLAUSE : CASE CASECLAUSELIST END ID
                  | CASE CASECLAUSELIST ELSE SQLSIMPLEEXPRESSION END ID'''
    if(len(p) == 5):
        p[0] = Case(p[2], None)
    else:
        p[0] = Case(p[2], p[4])


def p_case_clause_list(p):
    '''CASECLAUSELIST : CASECLAUSELIST WHEN SQLSIMPLEEXPRESSION RELOP SQLSIMPLEEXPRESSION THEN SQLSIMPLEEXPRESSION
                      | CASECLAUSELIST WHEN SQLSIMPLEEXPRESSION THEN SQLSIMPLEEXPRESSION
                      | WHEN SQLSIMPLEEXPRESSION RELOP SQLSIMPLEEXPRESSION THEN SQLSIMPLEEXPRESSION
                      | WHEN SQLSIMPLEEXPRESSION THEN SQLSIMPLEEXPRESSION'''

    # El ELSE solo puede venir una vez ---> las producciones de abajo permitian que viniera varias veces
    # WHEN SQLSIMPLEEXPRESSION THEN SQLSIMPLEEXPRESSION  ELSE SQLSIMPLEEXPRESSION
    # WHEN SQLSIMPLEEXPRESSION RELOP SQLSIMPLEEXPRESSION THEN SQLSIMPLEEXPRESSION ELSE SQLSIMPLEEXPRESSION
    if (len(p) == 8):
        p[1].append( CaseOption( Relop(p[3],p[5],p[4]), p[7] ) )
        p[0] = p[1]
    elif (len(p) == 7):
        p[0] = [CaseOption( Relop(p[3],p[5],p[4]), p[7] )]
    elif (len(p) == 6):
        p[1].append( CaseOption(p[3], p[5]) )
        p[0] = p[1]
    else: #len = 5
        p[0] = [CaseOption(p[3], p[5])]

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
        p[0] = ExpressionsTrigonometric(p[1], p[3], None)
    else:
        p[0] = ExpressionsTrigonometric(p[1], p[3], p[5])
#TODO: REVISAR QUE SQLALIAS SEA OPCIONAL, Asi esta bien >:v pinche juan marcos 
def p_sql_alias(p):
    '''SQLALIAS : AS SQLNAME
                | SQLNAME'''
    if (len(p) == 3):
        p[0] = p[2]
    elif (len(p) == 2):
        p[0] = p[1]


def p_expressions_time(p):
    '''EXPRESSIONSTIME : EXTRACT LEFT_PARENTHESIS DATETYPES FROM TIMESTAMP SQLNAME RIGHT_PARENTHESIS
                       | NOW LEFT_PARENTHESIS RIGHT_PARENTHESIS
                       | DATE_PART LEFT_PARENTHESIS SQLNAME COMMA INTERVAL SQLNAME RIGHT_PARENTHESIS
                       | CURRENT_DATE
                       | CURRENT_TIME
                       | TIMESTAMP SQLNAME'''
    if (len(p) == 8):
        p[0] = ExpressionsTime(p[1], p[3], p[6])
    elif (len(p) == 3):
        p[0] = ExpressionsTime(p[1], None, p[3])
    else:
        p[0] = ExpressionsTime(p[1], None, None)

def p_aggregate_functions(p):
    '''AGGREGATEFUNCTIONS : AGGREGATETYPES LEFT_PARENTHESIS CONTOFAGGREGATE RIGHT_PARENTHESIS
                          | AGGREGATETYPES LEFT_PARENTHESIS CONTOFAGGREGATE RIGHT_PARENTHESIS SQLALIAS'''
    if (len(p) == 5):
        p[0] = AgreggateFunctions(p[1], p[3], None)
    else:
        p[0] = AgreggateFunctions(p[1], p[3], p[5])

def p_cont_of_aggregate(p):
    '''CONTOFAGGREGATE : ASTERISK
                       | SQLSIMPLEEXPRESSION'''
    if (p[1] == '*'):
        p[0] = p[1]
    else:
        p[0] = p[1]

def p_sql_object_reference(p):
    '''OBJECTREFERENCE : SQLNAME DOT SQLNAME DOT SQLNAME
                       | SQLNAME DOT SQLNAME
                       | SQLNAME DOT ASTERISK
                       | SQLNAME'''
    if (len(p) == 2):
        p[0] = ObjectReference(None, None, p[1], None)
    elif (len(p) == 4):
        if (p[3] == '*'):
            p[0] = ObjectReference(None, None, p[1], p[3])
        else:
            p[0] = ObjectReference(None, p[1], p[3], None)
    else:
        p[0] = ObjectReference(p[1], p[3], p[5], None)

def p_list_values_insert(p):
    '''LISTVALUESINSERT : LISTVALUESINSERT COMMA SQLSIMPLEEXPRESSION
                        | SQLSIMPLEEXPRESSION'''
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
    p[0] = p[1]


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
    p[0] = p[1]

def p_sql_integer(p):
    '''SQLINTEGER : INT_NUMBER
                  | FLOAT_NUMBER'''
    p[0] = PrimitiveData(DATA_TYPE.NUMBER, p[1])


def p_sql_name(p):
    '''SQLNAME : STRINGCONT
               | CHARCONT
               | ID'''
               
    if (p.slice[1].type == "STRINGCONT" or p.slice[1].type == "CHARCONT"):
        p[0] = PrimitiveData(DATA_TYPE.STRING, p[1])
    else:
        p[0] = PrimitiveData(DATA_TYPE.STRING, p[1]) #TODO: REVISAR MANEJOR DE IDS


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
    global input
    ErrorController().destroy()
    lexer = lex.lex()
    lexer.lineno = 1
    input = inpu
    get_text(input)
    return parser.parse(inpu, lexer=lexer)

# parser = yacc.yacc()
# graficadora = GraficarAST()
# s = '''SELECT EXTRACT(SECOND FROM TIMESTAMP '2001-02-16 20:38:40');
#        SELECT User.name FROM Users INNER JOIN Ordenes ON Ordenes.id = Users.id GROUP BY ID;
#        SELECT COUNT(*) AS Name FROM User;
#        DELETE FROM USERS As User Where User.name = 12;
#        DELETE FROM products WHERE price = 10;
#        UPDATE products SET price = 10 WHERE price = 5 RETURNING *;'''

# result = parser.parse(s)
# s = '''SELECT * FROM USER;'''

# result = parser.parse(s)
# report = open('test.txt', 'w')
# report.write(graficadora.generate_string(result))
# report.close()
# os.system('dot -Tpdf test.txt -o ast.pdf')
# os.system('xdg-open ast.pdf')
