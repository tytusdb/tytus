import ply.yacc as yacc

from astDML import UpdateTable
from lexicosql import tokens
from astExpresion import ExpresionComparacion, ExpresionLogica, ExpresionNegativa, ExpresionNumero, ExpresionPositiva, OPERACION_LOGICA, OPERACION_RELACIONAL, TIPO_DE_DATO, ExpresionAritmetica, OPERACION_ARITMETICA,ExpresionNegada,ExpresionUnariaIs,OPERACION_UNARIA_IS, ExpresionBinariaIs, OPERACION_BINARIA_IS
from astExpresion import ExpresionCadena, ExpresionID ,ExpresionBooleano
from astFunciones import FuncionNumerica , FuncionCadena
from astUse import Use
from arbol import Arbol
from reporteBnf.reporteBnf import bnf 
#_______________________________________________________________________________________________________________________________
#                                                          PARSER
#_______________________________________________________________________________________________________________________________

#---------------- MANEJO DE LA PRECEDENCIA
precedence = (
    ('left','IS','ISNULL','NOTNULL','FROM' , 'SYMMETRIC','NOTBETWEEN'),
    ('left', 'NOT'),
    ('left','AND','OR'),
    ('left','IGUAL','DIFERENTE','DIFERENTE2','MENOR','MAYOR','MENORIGUAL','MAYORIGUAL'),
    ('left','BETWEEN','IN','LIKE','ILIKE','SIMILAR'),
    ('left','MAS','MENOS'),
    ('left','ASTERISCO','DIVISION','MODULO'),
    ('right','UMENOS','UMAS'),
    ('left', 'EXPONENT')
)

def p_init(p):
    'init : instrucciones'
    bnf.addProduccion('\<init> ::= \<instrucciones>')
    p[0] = Arbol(p[1])
    

def p_instrucciones_list(p):
    '''instrucciones    : instrucciones instruccion '''
    p[1].append(p[2])
    p[0] = p[1]
    bnf.addProduccion('\<instrucciones> ::= \<instrucciones> \<instruccion>')

def p_instrucciones_instruccion(p):
    'instrucciones  :   instruccion'
    p[0] = [p[1]]
    bnf.addProduccion('\<instrucciones> ::= \<instruccion>')


def p_instruccion1(p):
    '''instruccion :  sentenciaUpdate   PTCOMA '''
    p[0] = p[1]
    bnf.addProduccion('\<instruccion> ::= \<update> "." ')

def p_instruccion2(p):
    'instruccion : sentenciaDelete   PTCOMA '
    p[0] = p[1]
    bnf.addProduccion('\<instruccion> ::= \<delete> "." ')

def p_instruccion3(p):
    'instruccion : insert   PTCOMA '
    p[0] = p[1]
    bnf.addProduccion('\<instruccion> ::= \<insert> "." ')
    
def p_instruccion4(p):
    'instruccion : definicion  PTCOMA '
    p[0] = p[1]
    bnf.addProduccion('\<instruccion> ::= \<definicion> "."')

def p_instruccion5(p):
    '''instruccion : alter_table       PTCOMA	'''
    p[0] = p[1]
    bnf.addProduccion('\<instruccion> ::= \<alter_table> "." ')                    

def p_instruccion6(p):
    'instruccion : combine_querys    PTCOMA '
    p[0] = p[1]
    bnf.addProduccion('\<instruccion> ::= \<combine_querys> "." ') 

def p_instruccion7(p):
    'instruccion : use PTCOMA '
    p[0] = p[1]
    bnf.addProduccion('\<instruccion> ::= \<use> "." ') 
    
def p_use(p):
    'use : USE ID'
    p[0] = Use(p[2], p.slice[2].lineno)
    bnf.addProduccion('\<use> ::= "USE" "ID" ') 

# __________________________________________definicion

# <DEFINICION> ::= 'create' 'type' 'ID' 'as' 'enum' '(' <LISTA_ENUM> ')'
#               | <CREATE_OR_REPLACE> 'database' <COMBINACIONES1>
#               | 'show' 'databases' 'like' regex
#               | 'show' 'databases'
#               | 'alter' 'database' id <ALTER>
#               | 'drop' 'database' 'if' 'exists' id
#               | 'drop' 'database' id
#               | 'drop' 'table' id
#               | 'create' 'table' id (<COLUMNAS>)<INHERITS>
#               | 'create' 'table' id (<COLUMNAS>)


def p_definicion_1(p):
    'definicion : CREATE TYPE ID  AS ENUM PABRE lista_enum PCIERRA'
    bnf.addProduccion('\<definicion> ::= "CREATE" "TYPE" "AS" "ENUM" "(" \<lista_enum> ")"') 


def p_definicion_2(p):
    'definicion : create_or_replace DATABASE combinaciones1'
    bnf.addProduccion('\<definicion> ::= \<create_or_replace> "DATABASE"  \<combinaciones1>')

def p_definicion_3(p):
    'definicion : SHOW DATABASES LIKE REGEX'
    bnf.addProduccion('\<definicion> ::= "SHOW" "DATABASE" "LIKE" "REGEX"') 


def p_definicion_4(p):
    'definicion : SHOW DATABASES'
    bnf.addProduccion('\<definicion> ::= "SHOW" "DATABASES"')
    print("databases")


def p_definicion_5(p):
    'definicion : ALTER DATABASE ID  alter'
    bnf.addProduccion('\<definicion> ::= "ALTER" "DATABASE" "ID" \<alter>') 


def p_definicion_6(p):
    'definicion : DROP DATABASE IF EXISTS ID'
    bnf.addProduccion('\<definicion> ::= "DROP" "DATABASE" "IF" "EXISTS" "ID"') 


def p_definicion_7(p):
    'definicion : DROP DATABASE ID'
    bnf.addProduccion('\<definicion> ::= "DROP" "DATABASE" "ID"') 


def p_definicion_8(p):
    'definicion : DROP TABLE ID'
    bnf.addProduccion('\<definicion> ::= "DROP" "TABLE" "ID"') 


def p_definicion_9(p):
    'definicion : CREATE TABLE ID PABRE columnas PCIERRA inherits'
    bnf.addProduccion('\<definicion> ::= "CREATE" "TABLE" "ID" "(" \<columnas> ")" \<inherits>') 


def p_definicion_10(p):
    'definicion : CREATE TABLE ID PABRE columnas PCIERRA'
    bnf.addProduccion('\<definicion> ::= "CREATE" "TABLE" "ID" "(" \<columnas> ")"') 

def p_alter_table(p):
    '''alter_table : ALTER TABLE ID alter_options'''
    bnf.addProduccion('\<alter_table> ::= "ALTER" "TABLE" "ID"  \<alter_varchar_lista> ') 
    
def p_alter_table2(p):
    'alter_table :  ALTER TABLE ID alter_varchar_lista'
    bnf.addProduccion('\<alter_table> ::= "ALTER" "TABLE" "ID"  \<alter_varchar_lista> ')

        
def p_alter_options(p):
    'alter_options : ADD COLUMN ID tipo '
    bnf.addProduccion('\<alter_options> ::= "ADD" "COLUMN" "ID" \<tipo>')

def p_alter_options2(p):
    'alter_options : DROP COLUMN ID '
    bnf.addProduccion('\<alter_options> ::= "DROP" "COLUMN" "ID" ')

def p_alter_options3(p):
    'alter_options : ADD CHECK PABRE ID DIFERENTE CADENA PCIERRA '
    bnf.addProduccion('\<alter_options> ::= "ADD" "CHECK" "(" "<>" "CADENA" ")" ')

def p_alter_options4(p):
    'alter_options : ADD CONSTRAINT ID UNIQUE PABRE ID PCIERRA '
    bnf.addProduccion('\<alter_options> ::= "ADD" "CONSTRAINT" "ID" "UNIQUE" "(" "ID" ")"')

def p_alter_options5(p):
    'alter_options : ADD CONSTRAINT ID add_foreing'
    bnf.addProduccion('\<alter_options> ::= "ADD" "CONSTRAINT" "ID" \<add_foreing>')

def p_alter_options6(p):
    'alter_options : ADD add_foreing ' 
    bnf.addProduccion('\<alter_options> ::= "ADD" \<add_foreing>')       
#______________________________________________________________________________________________________________________________ NUEVA
def p_add_foreing(p):
    'add_foreing : FOREIGN KEY PABRE lista_ids PCIERRA REFERENCES ID PABRE lista_ids PCIERRA ' 
    bnf.addProduccion('\<add_foreing> ::=  "FOREIGN" "KEY" "(" \<lista_ids> ")" "REFERENCES" "ID" "("\<lista_ids> ")"')   


def p_alter_options7(p):
    'alter_options : ALTER COLUMN ID SET NOT NULL '
    bnf.addProduccion('\<alter_options> ::= "ALTER" "COLUMN" "ID" "SET" "NOT"  "NULL"')      
    
def p_alter_options8(p):
    'alter_options : DROP CONSTRAINT ID '
    bnf.addProduccion('\<alter_options> ::= "DROP" "CONSTRAINT" "ID"')                


def p_alter_varchar_lista(p):
    '''alter_varchar_lista :  alter_varchar
                           |  alter_varchar_lista COMA alter_varchar'''
    if len(p) == 2:
        bnf.addProduccion('\<alter_varchar_lista> ::= \<alter_varchar>')
    else:
        bnf.addProduccion('\<alter_varchar_lista> ::= \<alter_varchar> "," \<alter_varchar>')

def p_alter_varchar(p):
    '''alter_varchar : ALTER COLUMN ID TYPE VARCHAR PABRE NUMERO PCIERRA '''
    bnf.addProduccion('\<alter_varchar> ::= "ALTER" "COLUMN" "ID" "TYPE" "VARCHAR" "(" NUMERO ")"')

# <TABLA> ::=  'id' 
#          |   'id' 'as' 'id'
#          |   <SUBQUERY>
#          |   <SUBQUERY> 'as' 'id'
def p_tablas(p):
    '''tabla : ID
            |  ID alias
            |  ID AS alias '''
    if len(p) == 2:
        print("TABLA ID ")
        bnf.addProduccion('\<tabla> ::= "ID"')
    elif len(p) == 3:
        print("TABLA CON ID")
        bnf.addProduccion('\<tabla> ::= "ID" \<alias>')
    else:
        print("TABLA CON AS ID")
        bnf.addProduccion('\<tabla> ::= "ID" "AS" \<alias>')
def p_tablas2(p):
    '''tabla : subquery
            |  subquery alias 
            |  subquery AS alias '''
    if len(p) == 2:
        bnf.addProduccion('\<tabla> ::= \<subquery>')
    elif len(p) ==3:
        bnf.addProduccion('\<tabla> ::= \<subquery> \<alias>')
    else:
        bnf.addProduccion('\<tabla> ::= \<subquery> "AS" \<alias>')            


def p_filtro(p):
    '''filtro : where group_by having
              | where group_by
              | where '''
    if len(p) == 4:
        bnf.addProduccion('\<filtro> ::= \<where> \<group_by> \<having>')
    elif len(p) == 3:
        bnf.addProduccion('\<filtro> ::= \<where> \<group_by>')
    else:
        bnf.addProduccion('\<filtro> ::= \<where>')
#<JOIN>
def p_joinRecursivo(p):
    '''
    join : join instruccionJoin
         | instruccionJoin 
    '''

def p_join(p):
    '''instruccionJoin :  join_type JOIN ID ON expresion
            |  join_type JOIN ID alias ON expresion
            |  join_type JOIN ID USING PABRE JOIN lista_ids PCIERRA
            |  NATURAL join_type JOIN ID'''
    if len(p) == 6:
        bnf.addProduccion('\<join> ::= \<join_type> "JOIN" "ID" "ON" \<expresion>')
    elif len(p) == 7:
        bnf.addProduccion('\<join> ::= \<join_type> "JOIN" "ID" \<alias> "ON" \<expresion>')
    elif len(p) == 9:
        bnf.addProduccion('\<join> ::= \<join_type> "JOIN" "ID" "USING "(" \<lista_ids> ")"')
    else:
        bnf.addProduccion('\<join> ::= "NATURAL" \<join_type> "JOIN" "ID"')
        

def p_join_type(p):
    '''join_type : INNER'''
    bnf.addProduccion('\<join_type> ::= "INNER"')
def p_join_type2(p):
    '''join_type : outer'''
    bnf.addProduccion('\<join> ::= \<outer>')
    

def p_outer(p):
    '''outer : LEFT OUTER
            |  RIGHT OUTER
            |  FULL OUTER'''
    bnf.addProduccion(f'\<outer> ::= "{p[1].upper()}" "{p[2].upper()}"')
    
def p_outer2(p):            
    '''outer :  LEFT        
            |  RIGHT
            |  FULL'''
    bnf.addProduccion(f'\<outer> ::= "{p[1].upper()}"')

def p_combine_querys1(p):
    'combine_querys : combine_querys UNION ALL select'
    bnf.addProduccion('\<combine_querys> ::= \<combine_querys> "UNION" "ALL" \<select>')

def p_combine_querys2(p):
    'combine_querys : combine_querys UNION select'
    bnf.addProduccion('\<combine_querys> ::= \<combine_querys> "UNION"  \<select>')

def p_combine_querys3(p):
    'combine_querys : combine_querys INTERSECT ALL select'
    bnf.addProduccion('\<combine_querys> ::= \<combine_querys> "INTERSECT" "ALL"  \<select>')

def p_combine_querys4(p):
    'combine_querys : combine_querys INTERSECT select'
    bnf.addProduccion('\<combine_querys> ::= \<combine_querys> "INTERSECT"  \<select>')

def p_combine_querys5(p):
    'combine_querys : combine_querys EXCEPT ALL select'
    bnf.addProduccion('\<combine_querys> ::= \<combine_querys> "EXCEPT" "ALL" \<select>')

def p_combine_querys6(p):
    'combine_querys : combine_querys EXCEPT select'
    bnf.addProduccion('\<combine_querys> ::= \<combine_querys> "EXCEPT"  \<select>')

def p_combine_querys7(p):
    'combine_querys : select'
    bnf.addProduccion('\<combine_querys> ::= \<select> ')
#_____________________________________________________________ SELECT

def p_select1(p): #_____________ en esta fase NO por el join 
    'select : SELECT select_list FROM lista_tablas filtro join'
    bnf.addProduccion('\<select> ::= "SELECT" \<select_list> "FROM"  \<lista_tablas> \<filtro> \<join>')

def p_select2(p):
    'select : SELECT select_list FROM lista_tablas filtro'
    bnf.addProduccion('\<select> ::= "SELECT" \<select_list> "FROM"  \<lista_tablas> \<filtro>')


def p_select3(p):#_____________ en esta fase NO por el join 
    'select : SELECT select_list FROM lista_tablas orders limits offset join'
    bnf.addProduccion('\<select> ::= "SELECT" \<select_list> "FROM"  \<lista_tablas> \<orders> \<limits> \<offset> \<join>')

def p_select4(p):
    'select : SELECT select_list FROM lista_tablas orders limits offset'
    bnf.addProduccion('\<select> ::= "SELECT" \<select_list> "FROM"  \<lista_tablas> \<orders> \<limits> \<offset>')

def p_select5(p):#_____________ en esta fase NO por el join 
    'select : SELECT select_list FROM lista_tablas orders limits join'
    bnf.addProduccion('\<select> ::= "SELECT" \<select_list> "FROM"  \<lista_tablas> \<orders> \<limits> \<join>')

def p_select6(p):
    'select : SELECT select_list FROM lista_tablas orders limits'
    bnf.addProduccion('\<select> ::= "SELECT" \<select_list> "FROM"  \<lista_tablas> \<orders> \<limits>')

def p_select7(p):#_____________ en esta fase NO por el join 
    'select : SELECT select_list FROM lista_tablas orders offset join'
    bnf.addProduccion('\<select> ::= "SELECT" \<select_list> "FROM"  \<lista_tablas> \<orders> \<offset> \<join>')

def p_select8(p):
    'select : SELECT select_list FROM lista_tablas orders offset'
    bnf.addProduccion('\<select> ::= "SELECT" \<select_list> "FROM"  \<lista_tablas> \<orders> \<offset>')

def p_select9(p):#_____________ en esta fase NO por el join 
    'select : SELECT select_list FROM lista_tablas orders join'
    bnf.addProduccion('\<select> ::= "SELECT" \<select_list> "FROM"  \<lista_tablas> \<orders> \<join>')

def p_select10(p):
    'select : SELECT select_list FROM lista_tablas orders'
    bnf.addProduccion('\<select> ::= "SELECT" \<select_list> "FROM"  \<lista_tablas> \<orders>')
def p_select11(p):#_____________ en esta fase NO por el join 
    'select : SELECT select_list FROM lista_tablas limits offset join'
    bnf.addProduccion('\<select> ::= "SELECT" \<select_list> "FROM"  \<lista_tablas> \<limits>  \<offset> \<join>')
    
def p_select12(p):
    'select : SELECT select_list FROM lista_tablas limits offset'
    bnf.addProduccion('\<select> ::= "SELECT" \<select_list> "FROM"  \<lista_tablas> \<limits>  \<offset>')

def p_select13(p):#_____________ en esta fase NO por el join 
    'select : SELECT select_list FROM lista_tablas limits join'
    bnf.addProduccion('\<select> ::= "SELECT" \<select_list> "FROM"  \<lista_tablas> \<limits>  \<join>')
    
def p_select14(p):
    'select : SELECT select_list FROM lista_tablas limits'
    bnf.addProduccion('\<select> ::= "SELECT" \<select_list> "FROM"  \<lista_tablas> \<limits> ')

def p_select15(p):#_____________ en esta fase NO por el join 
    'select : SELECT select_list FROM lista_tablas offset join'
    bnf.addProduccion('\<select> ::= "SELECT" \<select_list> "FROM"  \<lista_tablas> \<offset> \<join>')

def p_select16(p):
    'select : SELECT select_list FROM lista_tablas offset'
    bnf.addProduccion('\<select> ::= "SELECT" \<select_list> "FROM"  \<lista_tablas> \<offset>')

def p_select17(p):#_____________ en esta fase NO por el join 
    'select : SELECT ASTERISCO FROM lista_tablas filtro join'
    bnf.addProduccion('\<select> ::= "SELECT" "*" "FROM"  \<lista_tablas> \<filtro> \<join>')

def p_select19(p):#_____________ en esta fase NO por el join 
    'select : SELECT DISTINCT select_list FROM lista_tablas filtro join'
    bnf.addProduccion('\<select> ::= "SELECT" "DISTINCT" \<select_list>  "FROM"  \<lista_tablas> \<filtro> \<join>')

def p_select20(p):
    'select : SELECT DISTINCT select_list FROM lista_tablas filtro'
    bnf.addProduccion('\<select> ::= "SELECT" "DISTINCT" \<select_list>  "FROM"  \<lista_tablas> \<filtro>')

def p_select23(p):#_____________ en esta fase NO por el join 
    'select : SELECT select_list FROM lista_tablas join'
    bnf.addProduccion('\<select> ::= "SELECT" \<select_list> "FROM"  \<lista_tablas> \<join>')

def p_select24(p):
    'select : SELECT select_list FROM lista_tablas'
    bnf.addProduccion('\<select> ::= "SELECT" \<select_list> "FROM"  \<lista_tablas>')

def p_select27(p):#_____________ en esta fase NO por el join 
    'select : SELECT DISTINCT select_list FROM lista_tablas join'
    bnf.addProduccion('\<select> ::= "SELECT" "DISTINCT" \<select_list> "FROM"  \<lista_tablas>  \<join>')

def p_select28(p):
    'select : SELECT DISTINCT select_list FROM lista_tablas'
    bnf.addProduccion('\<select> ::= "SELECT" "DISTINCT" \<select_list> "FROM"  \<lista_tablas>')

def p_select30(p):
    'select : SELECT select_list'
    bnf.addProduccion('\<select> ::= "SELECT" \<select_list>')
    
def p_select31(p):
    'select : SELECT DISTINCT select_list'
    bnf.addProduccion('\<select> ::= "SELECT" "DISTINCT" \<select_list>')

def p_select32(p):
    'select : SELECT  select_list FROM  lista_tablas group_by'
    bnf.addProduccion('\<select> ::= "SELECT" "DISTINCT" \<select_list>')
    # ENTRADA DE PRUEBA
    # select *
    # from t10
    # group by cadena;



#________________________________________ LIMIT 

def p_limits(p):
    'limits : LIMIT limitc'
    bnf.addProduccion('\<limitc> ::= "LIMIT" \<limitc>')

def p_limitc1(p):
    'limitc : NUMERO'
    bnf.addProduccion(f'\<limitc> ::= "{p[1].upper()}"')
    p[0] = p[1]
    

def p_limitc2(p):
    'limitc : ALL'
    bnf.addProduccion(f'\<limitc> ::= "{p[1].upper()}"')
    p[0] = p[1]

def p_offset(p):
    'offset : OFFSET NUMERO'
    bnf.addProduccion(f'\<offset> ::= "{p[1].upper()}" "NUMERO"')
#__________________________________________________________________________________________________________ FUNCIONES 
def p_funciones1(p):#ya
    'funciones : LENGTH PABRE exp_aux PCIERRA'
    p[0] = FuncionCadena(funcion='LENGTH',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')

def p_funciones2(p):#ya
    'funciones : SUBSTRING PABRE exp_aux COMA exp_aux COMA exp_aux PCIERRA'
    p[0] = FuncionCadena(funcion='SUBSTRING',parametro1=p[3],parametro2= p[5],parametro3=p[7], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> "," \<exp_aux> "," \<exp_aux> ")"')
    
def p_funciones3(p):#ya
    'funciones : TRIM PABRE exp_aux PCIERRA'
    p[0] = FuncionCadena(funcion='TRIM',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')

def p_funciones4(p):#ya
    'funciones : MD5 PABRE exp_aux PCIERRA'
    p[0] = FuncionCadena(funcion='MD5',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')

def p_funciones5(p):#ya
    'funciones : SHA256 PABRE exp_aux PCIERRA'
    p[0] = FuncionCadena(funcion='SHA256',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')

def p_funciones6(p):#ya
    'funciones : SUBSTR PABRE exp_aux COMA exp_aux COMA exp_aux PCIERRA'
    p[0] = FuncionCadena(funcion='SUBSTR',parametro1=p[3], parametro2=p[5] , parametro3=p[7],  linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> "," \<exp_aux> "," \<exp_aux>  ")"')

def p_funciones7(p):# cadena , numero 
    'funciones : GET_BYTE PABRE exp_aux TYPECAST BYTEA COMA exp_aux PCIERRA'
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> "TYPECAST" "BYTEA" "," \<exp_aux>  ")"')

def p_funciones8(p):# cadena , numero , numero 
    'funciones : SET_BYTE PABRE CADENA TYPECAST BYTEA COMA NUMERO COMA NUMERO PCIERRA'
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" "CADENA" "TYPECAST" "BYTEA" "," "NUMERO" "," "NUMERO" ")"')

def p_funciones9(p):
    'funciones : CONVERT PABRE CADENA AS DATE PCIERRA'
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" "CADENA"  "AS" "DATE"  ")"')

def p_funciones10(p): 
    'funciones : CONVERT PABRE CADENA AS INTEGER PCIERRA'
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" "CADENA"  "AS" "INTEGER" ")"')
    
def p_funciones11(p): # FASE 2 
    'funciones : ENCODE PABRE CADENA BYTEA COMA CADENA PCIERRA'
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" "CADENA"  "BYTEA" "," "CADENA" ")"')

def p_funciones12(p): # FASE 2 
    'funciones : DECODE PABRE CADENA COMA CADENA PCIERRA'
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" "CADENA"  "," "CADENA" ")"')



def p_funciones14(p):#ya
    'funciones : ACOS PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='ACOS',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')
    
def p_funciones15(p):#ya
    'funciones : ACOSD PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='ACOSD',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')
    

def p_funciones16(p):#ya
    'funciones : ASIN PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='ASIN',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')
    
def p_funciones17(p):#ya
    'funciones : ASIND PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='ASIND',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')

def p_funciones18(p):#ya
    'funciones : ATAN PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='ATAN',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')
    
def p_funciones19(p):#ya
    'funciones : ATAND PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='ATAND',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')
#_______________________________________ BINARIAS
def p_funciones20(p):#ya
    'funciones : ATAN2 PABRE exp_aux COMA exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='ATAN2',parametro1=p[3], parametro2=p[5], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> "," \<exp_aux> ")"')
    
def p_funciones21(p):#ya
    'funciones : ATAN2D PABRE exp_aux COMA exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='ATAN2D',parametro1=p[3], parametro2=p[5], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> "," \<exp_aux> ")"')

def p_funciones22(p):#ya
    'funciones : COS PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='COS',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')
 
def p_funciones23(p):#ya
    'funciones : COSD PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='COSD',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')

def p_funciones24(p):#ya
    'funciones : COT PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='COT',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')

def p_funciones25(p):#ya
    'funciones : COTD PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='COTD',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')
 
def p_funciones26(p):#ya
    'funciones : SIN PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='SIN',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')

def p_funciones27(p):#ya
    'funciones : SIND PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='SIND',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')

def p_funciones28(p):#ya
    'funciones : TAN PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='TAN',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')
    
def p_funciones29(p):#ya
    'funciones : TAND PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='TAND',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')
    
def p_funciones30(p):#ya
    'funciones : COSH PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='COSH',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')
    
def p_funciones31(p):#YA
    'funciones : SINH PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='SINH',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')
     
def p_funciones32(p):#YA
    'funciones : TANH PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='TANH',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')
 
def p_funciones33(p):#YA
    'funciones : ACOSH PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='ACOSH',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')

def p_funciones34(p):#ya
    'funciones : ASINH PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='ASINH',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')

def p_funciones35(p):#ya
    'funciones : ATANH PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='ATANH',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')

def p_funciones36(p):#ya
    'funciones : ABS PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='ABS',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')
 
def p_funciones37(p):#ya
    'funciones : CBRT PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='CBRT',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')
    
def p_funciones38(p):#ya
    'funciones : CEIL PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='CEIL',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')
    
def p_funciones39(p):#ya
    'funciones : CEILING PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='CEILING',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')
    
def p_funciones40(p):#ya
    'funciones : DEGREES PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='DEGREES',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')
    
def p_funciones41(p):#ya
    'funciones : DIV PABRE exp_aux COMA exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='DIV',parametro1=p[3], parametro2=p[5], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> "," \<exp_aux>  ")"')#BINARIA 
    
def p_funciones42(p):# ya 
    'funciones : FACTORIAL PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='FACTORIAL',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"') 
    
def p_funciones43(p):# ya 
    'funciones : FLOOR PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='FLOOR',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"') 
    
def p_funciones44(p):#ya
    'funciones : GCD PABRE exp_aux COMA exp_aux  PCIERRA'
    p[0] = FuncionNumerica(funcion='GCD',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> "," \<exp_aux>  ")"')#BINARIA 
    
def p_funciones45(p):#ya
    'funciones : LN PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='LN',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')

def p_funciones46(p):#ya
    'funciones : LOG PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='LOG',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')
 
def p_funciones47(p):#ya
    'funciones : EXP PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='EXP',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')

def p_funciones48(p):#ya
    'funciones : MOD PABRE exp_aux COMA exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='MOD',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> "," \<exp_aux>  ")"')#BINARIA 

def p_funciones49(p):#YA
    'funciones : PI PABRE PCIERRA'
    p[0] = FuncionNumerica(funcion='PI', linea= p.slice[1].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" ")"')

def p_funciones50(p):#ya 
    'funciones : POWER PABRE exp_aux COMA exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='POWER',parametro1=p[3], parametro2=p[5], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> "," \<exp_aux>  ")"')#BINARIA
    
def p_funciones51(p):#ya
    'funciones : RADIANS PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='RADIANS',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')
    
def p_funciones52(p):#ya
    'funciones : ROUND PABRE   exp_aux  PCIERRA'
    p[0] = FuncionNumerica(funcion='ROUND',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')

def p_funciones52_version2(p):#ya
    'funciones : ROUND PABRE exp_aux  COMA  exp_aux  PCIERRA '
    p[0] = FuncionNumerica(funcion='ROUND',parametro1=p[3],parametro2 = p[5] , linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> "," \<exp_aux>  ")"')#BINARIA

def p_funciones53(p):#ya
    'funciones : SIGN PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='SIGN',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')

def p_funciones54(p):#ya 
    'funciones : SQRT PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='SQRT',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')
    
def p_funciones55(p):# decimal y entero  , LISTA DE NUMEROS []
    'funciones : WIDTH_BUCKET PABRE lista_exp PCIERRA'
    p[0] = FuncionNumerica(funcion='WIDTH_BUCKET',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<lista_exp> ")"')

def p_funciones56(p):#ya
    'funciones : TRUNC PABRE exp_aux COMA exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='TRUNC',parametro1=p[3], parametro2=p[5], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> "," \<exp_aux>  ")"')#BINARIA
    
def p_funciones57(p):#ya
    'funciones : TRUNC PABRE exp_aux PCIERRA'
    p[0] = FuncionNumerica(funcion='TRUNC',parametro1=p[3], linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')
    
def p_funciones58(p):#ya
    'funciones : RANDOM PABRE PCIERRA'
    p[0] = FuncionNumerica(funcion='RANDOM', linea= p.slice[2].lineno)
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" \<exp_aux> ")"')

def p_funciones61(p):
    'funciones : DOBLE_PIPE tipo_numero'
    bnf.addProduccion('\<funciones> ::= "||" \<tipo_numero> ')

def p_funciones65(p):
    'funciones : PIPE tipo_numero'
    bnf.addProduccion('\<funciones> ::= "~" \<tipo_numero>')
    
def p_funciones65(p):
    'funciones : BITWISE_NOT tipo_numero'
    bnf.addProduccion('\<funciones> ::= "~" \<tipo_numero>')


def p_funciones62(p):
    'funciones : tipo_numero AMPERSAND tipo_numero'
    bnf.addProduccion('\<funciones> ::= \<tipo_numero> "&" \<tipo_numero> ')

def p_funciones63(p):
    'funciones : tipo_numero PIPE tipo_numero'
    bnf.addProduccion('\<funciones> ::= \<tipo_numero> "|" \<tipo_numero> ')

def p_funciones64(p):
    'funciones : tipo_numero NUMERAL tipo_numero'
    bnf.addProduccion('\<funciones> ::= \<tipo_numero> "#" \<tipo_numero> ')



def p_funciones66(p):
    'funciones : tipo_numero CORRIMIENTO_IZQ tipo_numero'
    bnf.addProduccion('\<funciones> ::= \<tipo_numero> "<<" \<tipo_numero> ')

def p_funciones67(p):
    'funciones : tipo_numero CORRIMIENTO_DER tipo_numero'
    bnf.addProduccion('\<funciones> ::= \<tipo_numero> ">>" \<tipo_numero> ')
    
def p_funciones_time1(p):
    'funciones : NOW PABRE PCIERRA'
    bnf.addProduccion(f'\<funciones> ::= "{p[1].upper()}" "(" ")"')
    
def p_funciones_time2(p):
    'funciones : TIMESTAMP CADENA_NOW'
    bnf.addProduccion(f'\<timestamp> ::= "{p[1].upper()}" "CADENA_NOW"')

def p_funciones_time3(p):
    'funciones : EXTRACT PABRE opcionesTime FROM TIMESTAMP CADENA_DATE PCIERRA'
    bnf.addProduccion('\<funciones> ::= "EXTRACT" "(" \<opcionesTime> "FROM" "TIMESTAMP" "CADENA_DATE" ")"')
    
def p_funciones_time4(p):# esta cadena fijo tiene que ser minutes secods o hours
    'funciones : DATE_PART PABRE CADENA COMA INTERVAL CADENA_INTERVAL PCIERRA'
    bnf.addProduccion('\<funciones> ::= "DATE_PART" "(" "CADENA" "," "INTERVAL" "CADENA_INTERVAL" ")"')

def p_funciones_time5(p):
    'funciones : CURRENT_DATE'
    bnf.addProduccion('\<funciones> ::= "CURRENT_DATE"')
    
def p_funciones_time6(p):
    'funciones : CURRENT_TIME'
    bnf.addProduccion('\<funciones> ::= "CURRENT_TIME"')

      
def p_opcionesTime(p):
    '''
    opcionesTime : YEAR
                 | MONTH
                 | DAY
                 | HOUR
                 | MINUTE
                 | SECOND
    '''
    p[0] = p[1]

#___________________________________ <TIPO_NUMERO>                    
#    <TIPO_NUMERO> ::= 'numero'
#                  |   'decimal'
def p_tipo_numero1(p):
    'tipo_numero : NUMERO'
    p[0] = ExpresionNumero(p[1], TIPO_DE_DATO.ENTERO, p.slice[1].lineno)
    bnf.addProduccion(f'\<tipo_numero> ::= "NUMERO"')

def p_tipo_numero2(p):
    'tipo_numero : DECIMAL_LITERAL'
    p[0] = ExpresionNumero(p[1], TIPO_DE_DATO.DECIMAL, p.slice[1].lineno)
    bnf.addProduccion(f'\<tipo_numero> ::= "DECIMAL_LITERAL"')
    

def p_lista_tablas(p):
    '''
    lista_tablas : lista_tablas COMA tabla
                 | tabla
    '''
    if (len(p) == 4):
        p[1].append(p[3])
        p[0] = p[1]
        bnf.addProduccion('\<lista_tablas> ::= \<lista_tablas> "," \<tabla> ')
    else:
        p[0] = [p[1]]
        bnf.addProduccion('\<lista_tablas> ::= \<tabla>')

    

def p_select_list(p):
    '''
    select_list : select_item
                | select_item alias
                | select_item AS alias
    '''
    if len(p) == 2:
        p[0] = [p[1]]
        bnf.addProduccion('\<select_list> ::= \<select_item>')
    elif len(p) == 3:
        p[0] = [p[1]] # considerar que este ya tendria un alias
        bnf.addProduccion('\<select_list> ::= \<select_item>  "ID"')
    elif len(p) == 4:
        p[0] = [p[1]] # considerar que este ya tendria un alias
        bnf.addProduccion('\<select_list> ::= \<select_item> "AS" \<alias>')

def p_select_list2(p):
    '''
    select_list : select_list COMA select_item
                | select_list COMA select_item alias 
                | select_list COMA select_item AS alias 
    '''
    if (len(p) == 4):
        p[1].append(p[3])
        p[0] = p[1]
        bnf.addProduccion('\<select_list> ::= \<select_list> "," \<select_item> ')
    elif len(p) == 5:
        p[0] = [p[1]] # considerar que este ya tendria un alias
        bnf.addProduccion('\<select_list> ::= \<select_list> "," \<select_item> "ID"')
    elif len(p) == 6:
        p[0] = [p[1]] # considerar que este ya tendria un alias
        bnf.addProduccion('\<select_list> ::= \<select_list> "," \<select_item> "AS" \<alias>')

# __________________________________________ lista_enum
# <LISTA_ENUM> ::= <ITEM>
#               | <LISTA_ENUM> ',' <ITEM>


def p_lista_enum_1(p):
    'lista_enum : item'
    bnf.addProduccion('\<lista_enum> ::= \<item>')
    p[0] = [p[1]]


def p_lista_enum_2(p):
    'lista_enum : lista_enum COMA item'
    p[1].append(p[3])
    p[0] = p[1]
    bnf.addProduccion('\<lista_enum> ::= \<lista_enum> "," \<item>')
# __________________________________________ ITEM
# <ITEM> ::= cadena


def p_item(p):
    'item : CADENA'
    p[0] = ExpresionCadena(p[1], TIPO_DE_DATO.CADENA, p.slice[1].lineno)
    bnf.addProduccion(f'\<item> ::= "{p[1].upper()}"')
# __________________________________________ create_or_replace
# <CREATE_OR_REPLACE> ::= 'create'
#                      | 'create or replace'


def p_create_or_replace_1(p):
    'create_or_replace : CREATE '
    p[0] = p[1]
    bnf.addProduccion(f'\<create_or_replace> ::= "{p[1].upper()}"')


def p_create_or_replace_2(p):
    'create_or_replace : CREATE OR REPLACE'
    
    bnf.addProduccion(f'\<create_or_replace> ::= "{p[1].upper()}" "OR" "REPLACE"')

# __________________________________________ combinaciones1
# <COMBINACIONES1> ::= 'if' 'not' 'exists' id <COMBINACIONES2>
#                   | id <COMBINACIONES2>
#                   | id
def p_combinaciones1_0(p):
    'combinaciones1 : IF NOT EXISTS ID'
    bnf.addProduccion(f'\<combinaciones1> ::= "{p[1].upper()}" "NOT" "EXISTS" "ID"')

def p_combinaciones1_1(p):
    'combinaciones1 : IF NOT EXISTS ID combinaciones2'
    bnf.addProduccion(f'\<combinaciones1> ::= "{p[1].upper()}" "NOT" "EXISTS" "ID" \<combinaciones2>')

def p_combinaciones1_2(p):
    'combinaciones1 : ID combinaciones2'
    bnf.addProduccion(f'\<combinaciones1> ::= "{p[1].upper()}" \<combinaciones2>')


def p_combinaciones1_3(p):
    'combinaciones1 : ID'
    bnf.addProduccion(f'\<combinaciones1> ::= "{p[1].upper()}"')
    p[0] = ExpresionID(p[1], p.slice[1].lineno)
# ________________________________________ combinaciones2
# <COMBINACIONES2> ::= <OWNER>
#                   |<MODE>
#                   |<OWNER><MODE>


def p_combinaciones2_1(p):
    'combinaciones2 : owner'
    bnf.addProduccion('\<combinaciones2> ::= \<owner>')
    p[0] = p[1]


def p_combinaciones2_2(p):
    'combinaciones2 : mode'
    bnf.addProduccion('\<combinaciones2> ::= \<mode>')
    p[0] = p[1]


def p_combinaciones2_3(p):
    'combinaciones2 : owner mode'
    bnf.addProduccion('\<combinaciones2> ::= \<owner> \<mode>')

def p_owner_1(p):
    'owner : OWNER alias'
    bnf.addProduccion('\<owner> ::= "OWNER" \<alias>')

def p_owner_2(p):
    'owner : OWNER IGUAL alias'
    bnf.addProduccion('\<owner> ::= "OWNER" "=" \<alias>')

# ________________________________________ <MODE>
# <MODE> ::= 'mode' entero
#         | 'mode' '=' entero


def p_mode_1(p):
    'mode : MODE NUMERO'
    bnf.addProduccion('\<mode> ::= "MODE" "NUMERO"')


def p_mode_2(p):
    'mode : MODE IGUAL NUMERO'
    bnf.addProduccion('\<mode> ::= "MODE" "=" "NUMERO"')


# _________________________________________ <alter>
# <ALTER> ::= 'rename to' id
#          | 'owner to' <NEW_OWNER>

def p_alter_1(p):
    'alter : RENAME TO ID'
    bnf.addProduccion('\<alter> ::= "RENAME" "TO" "ID"')


def p_alter_2(p):
    'alter : OWNER TO new_owner'
    bnf.addProduccion('\<alter> ::= "OWNER" "TO" \<new_owner>')

# _________________________________________ new_owner
#  <NEW_OWNER> ::= id
#              | 'current_user'
#              | 'session_user'


def p_new_owner_1(p):
    'new_owner : ID '
    bnf.addProduccion('\<new_owner> ::= "ID"')
    p[0] = p[1]


def p_new_owner_2(p):
    'new_owner : CURRENT_USER '
    bnf.addProduccion('\<new_owner> ::= "CURRENT_USER"')
    p[0]=p[1]


def p_new_owner_3(p):
    'new_owner : SESSION_USER'
    bnf.addProduccion('\<new_owner> ::= "SESSION_USER"')
    p[0]=p[1]

# _________________________________________ inherits
# <INHERITS> ::= 'INHERITS' '('ID')'


def p_inherits(p):
    'inherits : INHERITS PABRE ID PCIERRA'
    bnf.addProduccion('\<inherits> ::= "INHERITS" "(" "ID" ")"')

# _________________________________________ columnas
# <COLUMNAS> ::= <COLUMNA>
#             | <COLUMNAS>, <COLUMNA>


def p_columnas_1(p):
    'columnas : columna'
    bnf.addProduccion('\<columnas> ::= \<columna>')
    p[0] = [p[1]]

def p_columnas_2(p):
    'columnas : columnas COMA columna'
    bnf.addProduccion('\<columnas> ::= \<columnas> ","  \<columna> ')
    p[1].append(p[3])
    p[0] = p[1]
    


# _________________________________________ columna
#  <COLUMNA> ::=
#             | id' <TIPO>
#             | id' <TIPO> <listaOpciones>
#             | 'constraint' 'id' 'check' (<lista_exp>)
#             | 'id' 'check' (<lista_exp>)
#             | 'unique' (<LISTA_IDS>)
#             | 'primary' 'key' (<LISTA_IDS>)
#             | 'foreign' 'key' (<LISTA_IDS>) 'references' 'id' (<LISTA_IDS>)

# listaOpciones> ::= <listaOpciones> <opCol>
#                  | <opCol>

# <opCol>   ::=  <DEFAULT>
#             |  <CONSTRAINTS>
#             |  <CHECKS>
#             |  <nulleable>
#             |  'primary' 'key'
#             |  'references' 'id'

# ___________________________________________ declaracion de columna
def p_columna_1(p):
    'columna : ID tipo'
    bnf.addProduccion('\<columna> ::= "ID"  \<tipo>')


def p_columna_2(p):
    'columna : ID tipo listaOpciones'
    bnf.addProduccion('\<columna> ::= "ID"  \<tipo> \<listaOpciones>')


def p_columna_3(p):
    'columna : CONSTRAINT  ID CHECK PABRE lista_exp PCIERRA '
    bnf.addProduccion('\<columna> ::= "CONSTRAINT" "ID" "CHECK" "(" \<lista_exp> ")"')


def p_columna_4(p):
    'columna : UNIQUE PABRE lista_ids PCIERRA'
    bnf.addProduccion('\<columna> ::= "UNIQUE" "(" \<lista_exp> ")"')


def p_columna_5(p):
    'columna :  PRIMARY KEY PABRE lista_ids PCIERRA'
    bnf.addProduccion('\<columna> ::= "PRIMARY" "KEY" "(" \<lista_exp> ")"')


def p_columna_6(p):
    'columna : FOREIGN KEY PABRE lista_ids PCIERRA REFERENCES ID PABRE lista_ids PCIERRA'
    bnf.addProduccion('\<columna> ::= "FOREIGN" "KEY" "(" \<lista_exp> ")" "REFERENCES" "ID" "(" \<lista_ids> ")"')


def p_columna_7(p):
    'columna : CHECK PABRE lista_exp PCIERRA'
    bnf.addProduccion('\<columna> ::= "CHECK"  "(" \<lista_exp> ")"')


def p_listaOpciones_List(p):
    'listaOpciones : listaOpciones opCol'
    bnf.addProduccion('\<listaOpciones> ::= \<listaOpciones> \<opCol>')
    p[1].append(p[2])
    p[0] = p[1]
        
 
        
def p_listaOpciones_una(p):
    'listaOpciones : opCol'
    bnf.addProduccion('\<listaOpciones> ::= \<opCol>')
    p[0] = [p[1]]


def p_opCol_1(p):
    'opCol : default'
    bnf.addProduccion('\<opCol> ::= \<default>')
    p[0] = p[1]


def p_opCol_2(p):
    'opCol : constraints'
    bnf.addProduccion('\<opCol> ::= \<constraints>')
    p[0] = p[1]


def p_opCol_3(p):
    'opCol :  checks'
    bnf.addProduccion('\<opCol> ::= \<checks>')
    p[0] = p[1]


def p_opCol_4(p):
    'opCol :  PRIMARY KEY'
    bnf.addProduccion('\<opCol> ::= "PRIMARY" "KEY"')


def p_opCol_5(p):
    'opCol : REFERENCES ID'
    bnf.addProduccion('\<opCol> ::= "REFERENCES" "ID"')


def p_opCol_6(p):
    'opCol : nullable'
    bnf.addProduccion('\<opCol> ::= \<nullable>')
    p[0] = p[1]


# __________________________________________ <TIPO>

# <TIPO> ::= 'smallint'
#         |  'integer'
#         |  'bigint'
#         |  'decimal'
#         |  'numeric'
#         |  'real'
#         |  'double' 'precision'
#         |  'money'
#         |  'character' 'varying' ('numero')
#         |  'varchar' ('numero')
#         |  'character' ('numero')
#         |  'char' ('numero')
#         |  'text'
#         |  <TIMESTAMP>
#         |  'date'
#         |  <TIME>
#         |  <INTERVAL>
#         |  'boolean'
#         |  ID 

def p_tipo_1(p):
    'tipo : SMALLINT'
    bnf.addProduccion(f'\<opCol> ::="{p[1].upper()}"')
    p[0] = p[1]    


def p_tipo_2(p):
    'tipo : INTEGER'
    bnf.addProduccion(f'\<opCol> ::="{p[1].upper()}"')
    p[0] = p[1]


def p_tipo_3(p):
    'tipo : BIGINT'
    bnf.addProduccion(f'\<opCol> ::="{p[1].upper()}"')
    p[0] = p[1]

def p_tipo_4(p):
    'tipo : DECIMAL'
    bnf.addProduccion(f'\<opCol> ::="{p[1].upper()}"')
    p[0] = p[1]

def p_tipo_5(p):
    'tipo : NUMERIC'
    bnf.addProduccion(f'\<opCol> ::="{p[1].upper()}"')
    p[0] = p[1]

def p_tipo_6(p):
    'tipo : REAL'
    bnf.addProduccion(f'\<opCol> ::="{p[1].upper()}"')
    p[0] = p[1]

def p_tipo_7(p):
    'tipo : DOUBLE PRECISION'
    bnf.addProduccion(f'\<opCol> ::="{p[1].upper()}" "{p[2].upper()}"')
    

def p_tipo_8(p):
    'tipo : MONEY'
    bnf.addProduccion(f'\<opCol> ::="{p[1].upper()}"')
    p[0] = p[1]


def p_tipo_9(p):
    'tipo : CHARACTER VARYING PABRE NUMERO PCIERRA'
    bnf.addProduccion(f'\<tipo> ::="{p[1].upper()}" "VARYING" "(" "NUMERO" ")"')

def p_tipo_10(p):
    'tipo : VARCHAR PABRE NUMERO PCIERRA'
    bnf.addProduccion(f'\<tipo> ::="{p[1].upper()}" "(" "NUMERO" ")"')

def p_tipo_11(p):
    'tipo : CHARACTER PABRE NUMERO PCIERRA'
    bnf.addProduccion(f'\<tipo> ::="{p[1].upper()}" "(" "NUMERO" ")"')


def p_tipo_12(p):
    'tipo : CHAR PABRE NUMERO PCIERRA'
    bnf.addProduccion(f'\<tipo> ::="{p[1].upper()}" "(" "NUMERO" ")"')


def p_tipo_13(p):
    'tipo : TEXT '
    bnf.addProduccion(f'\<opCol> ::="{p[1].upper()}"')
    p[0] = p[1]

def p_tipo_14(p):
    'tipo : timestamp'
    bnf.addProduccion('\<opCol> ::= \<timestamp>')
    p[0] = p[1]


def p_tipo_15(p):
    'tipo : DATE'
    bnf.addProduccion(f'\<opCol> ::="{p[1].upper()}"')
    p[0] = p[1]


def p_tipo_16(p):
    'tipo : time'
    bnf.addProduccion('\<opCol> ::= \<time>')
    p[0] = p[1]


def p_tipo_17(p):
    'tipo : interval'
    bnf.addProduccion('\<opCol> ::= \<interval>')
    p[0] = p[1]


def p_tipo_18(p):
    'tipo : BOOLEAN'
    bnf.addProduccion(f'\<opCol> ::="{p[1].upper()}"')
    p[0] = p[1]

def p_tipo_19(p):# produccion para los enum
    'tipo : ID'
    bnf.addProduccion('\<opCol> ::= "ID"')
    p[0] = p[1]
# __________________________________________ <INTERVAL>
# <INTERVAL> ::= 'interval' <FIELDS> ('numero')
#             |  'interval' <FIELDS>
#             |  'interval' ('numero')
#             |  'interval'


def p_interval_1(p):
    'interval : INTERVAL fields PABRE NUMERO PCIERRA'
    bnf.addProduccion('\<interval> ::= "INTERVAL" \<fields> "(" "NUMERO" ")"')


def p_interval_2(p):
    'interval : INTERVAL fields'
    bnf.addProduccion('\<interval> ::= "INTERVAL" \<fields>')


def p_interval_3(p):
    'interval : INTERVAL PABRE NUMERO PCIERRA'
    bnf.addProduccion('\<interval> ::= "INTERVAL" "(" "NUMERO" ")"')


def p_interval_4(p):
    'interval : INTERVAL '
    bnf.addProduccion('\<interval> ::= "INTERVAL"')
    p[0] = p[1]

# _________________________________________ <fields>
# <FIELDS> ::= 'year'
#           |  'month'
#           |  'day'
#           |  'hour'
#           |  'minute'
#           |  'second'


def p_fields(p):
    '''fields : YEAR 
              | MONTH
              | DAY
              | HOUR
              | MINUTE
              | SECOND '''
    bnf.addProduccion(f'\<fields> ::= "{p[1].upper()}"')
    p[0] = p[1]  # fijo es un sintetizado

# __________________________________________ <time>
# <TIME> ::= 'time' ('numero') 'tmstamp'
#         |  'time' 'tmstamp'
#         |  'time' ('numero')
#         |  'time'


def p_time_1(p):
    'time : TIME PABRE NUMERO PCIERRA CADENA'
    bnf.addProduccion(f'\<time> ::= "{p[1].upper()}" "(" "NUMERO" ")" "CADENA"')


def p_time_2(p):
    'time : TIME CADENA'
    bnf.addProduccion(f'\<time> ::= "{p[1].upper()}" "CADENA"')


def p_time_3(p):
    'time : TIME PABRE NUMERO PCIERRA'
    bnf.addProduccion(f'\<time> ::= "{p[1].upper()}" "(" "NUMERO" ")"')


def p_time_4(p):
    'time : TIME'
    bnf.addProduccion(f'\<time> ::= "{p[1].upper()}"')
    p[0] =p[1]

# __________________________________________ <timestamp>
# <TIMESTAMP>
def p_timestamp_1(p):
    'timestamp : TIMESTAMP PABRE NUMERO PCIERRA CADENA_DATE '
    bnf.addProduccion(f'\<timestamp> ::= "{p[1].upper()}" "(" "NUMERO" ")" "CADENA"')

def p_timestamp_2(p):
    'timestamp : TIMESTAMP  CADENA_DATE'
    bnf.addProduccion(f'\<timestamp> ::= "{p[1].upper()}" "CADENA"')


def p_timestamp_3(p):
    'timestamp : TIMESTAMP PABRE NUMERO PCIERRA '
    bnf.addProduccion(f'\<timestamp> ::= "{p[1].upper()}" "(" "NUMERO" ")"')

def p_timestamp_4(p):
    'timestamp : TIMESTAMP'
    bnf.addProduccion(f'\<timestamp> ::= "{p[1].upper()}"')
    p[0] =p[1]

def p_timestamp_5(p):
    'timestamp : TIMESTAMP NOW PABRE PCIERRA'
    bnf.addProduccion(f'\<timestamp> ::= "{p[1].upper()}" "(" ")"')

def p_timestamp_6(p):
    'timestamp : TIMESTAMP CADENA_NOW'
    bnf.addProduccion(f'\<timestamp> ::= "{p[1].upper()}" "CADENA_NOW"')
# __________________________________________ <DEFAULT>
# <DEFAULT> ::= 'default' <VALOR>


def p_default(p):
    'default : DEFAULT expresion'
    bnf.addProduccion(f'\<default> ::= "{p[1].upper()}" \<expresion>')

# _________________________________________ <VALOR>
# falta la produccion valor , le deje expresion :v

# __________________________________________ <NULLABLE>
# <NULLABLE> ::= 'not' 'null'
#             | 'null'


def p_nullable_1(p):
    'nullable : NOT NULL'
    bnf.addProduccion(f'\<nullable> ::= "{p[1].upper()}" "NULL"')

def p_nullable_2(p):
    'nullable : NULL'
    bnf.addProduccion(f'\<nullable> ::= "{p[1].upper()}" ')
    p[0] = p[1]
# __________________________________________ <CONSTRAINTS>
# <CONSTRAINTS> ::= 'constraint' id 'unique'
#                 | 'unique'


def p_constraints_1(p):
    'constraints : CONSTRAINT ID UNIQUE'
    bnf.addProduccion(f'\<constraints> ::= "{p[1].upper()}" "ID" "UNIQUE"')


def p_constraints_2(p):
    'constraints : UNIQUE'
    bnf.addProduccion(f'\<constraints> ::= "{p[1].upper()}" ')
    p[0] = p[1]


#_________________________________________ <CHECKS>
# <CHECKS> ::= 'constraint' 'id' 'check' '('<EXPRESION>')'
#             |'check' '('<EXPRESION>')' 

def p_checks_1(p):
    'checks : CONSTRAINT ID CHECK PABRE expresion PCIERRA '
    bnf.addProduccion(f'\<checks> ::= "{p[1].upper()}" "ID" "CHECK" "(" \<expresion> ")" ')

def p_checks_2(p):
    'checks : CHECK PABRE expresion PCIERRA'
    bnf.addProduccion(f'\<checks> ::= "{p[1].upper()}" "(" \<expresion> ")" ')  







# __________________________________________update
def p_update(p):
    '''sentenciaUpdate : UPDATE ID SET lista_asignaciones WHERE expresion 
                       | UPDATE ID SET lista_asignaciones '''
    if (len(p) == 7):
        bnf.addProduccion(f'\<update> ::= "{p[1].upper()}" "ID" "SET" \<lista_asignaciones> "WHERE" \<expresion>') 
        p[0] = UpdateTable(tabla = p[2], asignaciones= p[4] , condiciones=p[6])
    else:
        bnf.addProduccion(f'\<update> ::= "{p[1].upper()}" "ID" "SET" \<lista_asignaciones>') 
        p[0] = UpdateTable(tabla = p[2], asignaciones= p[4])
# __________________________________________INSERT


def p_sentenciaInsert(p):
    ''' insert : INSERT INTO ID VALUES PABRE lista_exp PCIERRA'''
    bnf.addProduccion(f'\<insert> ::= "{p[1].upper()}" "INTO" "ID" "VALUES"  "( "\<lista_exp> ")"')
    
def p_sentenciaInsert2(p):
    ''' insert : INSERT INTO ID parametros VALUES PABRE lista_exp PCIERRA'''
    bnf.addProduccion(f'\<insert> ::= "{p[1].upper()}" "INTO" "ID" \<parametros> "VALUES"  "( "\<lista_exp> ")"') 
# ___________________________________________PARAMETROS


def p_parametros(p):
    ''' parametros : PABRE lista_ids  PCIERRA'''
    bnf.addProduccion('\<parametros> ::= "(" \<lista_ids> ")"') 
    p[0] = p[2]
# __________________________________________lista ids
# <LISTA_IDS> ::= <LISTA_IDS> ',' 'ID'
#          | 'ID'


def p_lista_ids(p):
    ''' lista_ids : lista_ids COMA  ID
                  | ID '''

    if (len(p) == 4):
        p[1].append(p[3])
        p[0] = p[1]
        bnf.addProduccion('\<lista_ids> ::= \<lista_ids> "," "ID"') 
    else:
        p[0] = [p[1]]
        bnf.addProduccion('\<lista_ids> ::= "ID"') 


# __________________________________________DELETE
def p_sentenciaDelete(p):
    ''' sentenciaDelete : DELETE FROM ID WHERE expresion
                        | DELETE FROM ID '''
    if len(p) == 6:
        bnf.addProduccion('\<delete> ::= "DELETE" "FROM" "ID" "WHERE" <expresion>')
    else:
        bnf.addProduccion('\<delete> ::= "DELETE" "FROM" "ID"')


# ___________________________________________ASIGNACION____________________________________

def p_lista_asignaciones(p):
    '''lista_asignaciones : lista_asignaciones COMA asignacion
                          | asignacion'''
    if (len(p) == 4):
        p[1].append(p[3])
        p[0] = p[1]
        bnf.addProduccion('\<lista_asignaciones> ::=  \<lista_asignaciones> "," \<asignacion>')
    else:
        p[0] = [p[1]]
        bnf.addProduccion('\<lista_asignaciones> ::= \<asignacion>')


def p_asignacion(p):
    ''' asignacion : ID IGUAL expresion'''
    bnf.addProduccion('\<asignacion> ::= "ID" "=" \<expresion>')
    p[0] = p[1]


# ______________________________________________EXPRESION_______________________________
def p_expresionBooleanaTrue(p):
    '''expresion : TRUE '''
    p[0] = ExpresionBooleano(True, p.slice[1].lineno)
    bnf.addProduccion('\<expresion> ::= "TRUE"')

def p_expresionBooleanaFalse(p):
    '''expresion : FALSE '''
    p[0] = ExpresionBooleano(False, p.slice[1].lineno)
    bnf.addProduccion('\<expresion> ::= "FALSE"')
def p_exp_auxBooleanaTrue(p):
    '''exp_aux : TRUE '''
    p[0] = ExpresionBooleano(True, p.slice[1].lineno)
    bnf.addProduccion('\<expresion> ::= "TRUE"')

def p_exp_auxBooleanaFalse(p):
    '''exp_aux : FALSE '''
    p[0] = ExpresionBooleano(False, p.slice[1].lineno)
    bnf.addProduccion('\<expresion> ::= "FALSE"')  



def p_expresiones_unarias(p):
    ''' expresion : MENOS expresion %prec UMENOS 
                  | MAS expresion %prec UMAS
                  | NOT expresion'''
    if p[1] == '+':
        p[0] = ExpresionPositiva(p[2], p.slice[1].lineno)
        bnf.addProduccion('\<expresion> ::= "-" \<expresion>')
    elif p[1] == '-':
        p[0] = ExpresionNegativa(p[2], p.slice[1].lineno)
        bnf.addProduccion('\<expresion> ::= "+" \<expresion>')
    else:
        p[0] = ExpresionNegada(p[2])
        bnf.addProduccion('\<expresion> ::= "NOT" \<expresion>')
    
def p_expresiones_is_complemento(p):
    'expresion : expresion IS TRUE'
    p[0] = ExpresionUnariaIs(p[1], p.slice[2].lineno, OPERACION_UNARIA_IS.IS_TRUE)
    bnf.addProduccion('\<expresion> ::= \<expresion> "IS" "TRUE"')

def p_expresiones_is_complemento1(p):
    'expresion : expresion IS FALSE'
    p[0] = ExpresionUnariaIs(p[1], p.slice[2].lineno, OPERACION_UNARIA_IS.IS_FALSE)
    bnf.addProduccion('\<expresion> ::= \<expresion> "IS" "FALSE"')

def p_expresiones_is_complemento2_false(p):
    'expresion : expresion IS NOT FALSE'
    p[0] = ExpresionUnariaIs(p[1], p.slice[2].lineno, OPERACION_UNARIA_IS.IS_NOT_FALSE)
    bnf.addProduccion('\<expresion> ::= \<expresion> "IS" "NOT" "FALSE"')
    
def p_expresiones_is_complemento2_true(p):
    'expresion : expresion IS NOT TRUE'
    p[0] = ExpresionUnariaIs(p[1], p.slice[2].lineno, OPERACION_UNARIA_IS.IS_NOT_TRUE)
    bnf.addProduccion('\<expresion> ::= \<expresion> "IS" "NOT" "TRUE"')
    
def p_expresiones_is_complemento4(p):
    'expresion : expresion IS NOT DISTINCT FROM expresion'
    p[0] = ExpresionBinariaIs(p[1], p[6], OPERACION_BINARIA_IS.IS_NOT_DISTINCT_FROM, p.slice[2].lineno)
    bnf.addProduccion('\<expresion> ::= \<expresion> "IS" "NOT ""DISTINCT" "FROM" \<expresion>')
    
def p_expresiones_is_complemento_nulleable(p):
    '''
    expresion    : expresion IS NULL    
                 | expresion IS NOT NULL '''
    if len(p) == 4:
        bnf.addProduccion('\<expresion> ::= \<expresion> "IS" "NULL"')
    else:
        bnf.addProduccion('\<expresion> ::= \<expresion> "IS" "NOT "NULL"')

        
def p_expresiones_is_complemento2(p):
    '''       
    expresion  : expresion ISNULL 
               | expresion NOTNULL'''
    if p[2].upper() == 'ISNULL':
        bnf.addProduccion('\<expresion> ::= \<expresion> "ISNULL"')
    else:
        bnf.addProduccion('\<expresion> ::= \<expresion> "NOTNULL"')
        
def p_expresiones_is_complemento5(p):               
    ''' expresion   : expresion IS UNKNOWN
                    | expresion IS NOT UNKNOWN '''
    if len(p) == 4:
        bnf.addProduccion('\<expresion> ::= \<expresion> "IS" "UNKNOWN"')
    else: 
        bnf.addProduccion('\<expresion> ::= \<expresion> "IS" "NOT" "UNKNOWN"')        
        
        
def p_expresiones_is_complemento6(p):     
    ''' expresion   : expresion IS DISTINCT FROM expresion '''
    bnf.addProduccion('\<expresion> ::= \<expresion> "IS" "DISTINCT" "FROM" \<expresion> ') 



def p_expresion_ternaria(p): 
    '''expresion : expresion BETWEEN  exp_aux AND exp_aux
                 | expresion BETWEEN SYMMETRIC exp_aux AND exp_aux '''
    if len(p) == 6:
        bnf.addProduccion('\<expresion> ::= \<expresion> "BETWEEN" \<exp_aux> "AND" \<exp_aux>')
    else:
        bnf.addProduccion('\<expresion> ::= \<expresion> "BETWEEN" "SYMMETRIC" \<exp_aux> "AND" \<exp_aux>')
        
def p_expresion_ternaria2(p):
    '''expresion : expresion NOTBETWEEN exp_aux AND exp_aux
                 | expresion NOTBETWEEN SYMMETRIC exp_aux AND exp_aux'''
    if len(p) == 6:
        bnf.addProduccion('\<expresion> ::= \<expresion> "NOTBETWEEN" \<exp_aux> "AND" \<exp_aux>')
    else:
        bnf.addProduccion('\<expresion> ::= \<expresion> "NOTBETWEEN" "SYMMETRIC" \<exp_aux> "AND" \<exp_aux>')
        
        

def p_expreion_funciones(p):
    'expresion : funciones'
    bnf.addProduccion('\<expresion> ::= \<funciones>')
    p[0] = p[1]
    
def p_expreion_entre_parentesis(p):
    'expresion : PABRE expresion  PCIERRA'
    bnf.addProduccion('\<expresion> ::= "(" \<expresion> ")"')
    p[0] = p[2]

def p_expresion_primitivo(p):
    'expresion : CADENA'
    p[0] = ExpresionCadena(p[1], TIPO_DE_DATO.CADENA, p.slice[1].lineno)
    bnf.addProduccion(f'\<expresion> ::= "CADENA"')

def p_expresion_primitivo1(p):
    'expresion : NUMERO'
    p[0] = ExpresionNumero(p[1], TIPO_DE_DATO.ENTERO, p.slice[1].lineno)
    bnf.addProduccion(f'\<expresion> ::= "NUMERO"')

def p_expresion_primitivo2(p):
    'expresion : DECIMAL_LITERAL'
    p[0] = ExpresionNumero(p[1], TIPO_DE_DATO.DECIMAL, p.slice[1].lineno)
    bnf.addProduccion(f'\<expresion> ::= "DECIMAL_LITERAL"')

def p_expresion_id(p):
    'expresion : ID'
    p[0] = ExpresionID(p[1], p.slice[1].lineno)
    p[0] = p[1]
    bnf.addProduccion(f'\<expresion> ::= "ID"')
    
def p_expresion_tabla_campo(p):
    'expresion : ID PUNTO ID'
    p[0] = ExpresionID(p[3], p.slice[1].lineno , tabla = p[1])
    bnf.addProduccion('\<exp_aux> ::= "ID" "." "ID"')
        

def p_expresion_con_dos_nodos(p):
    '''expresion : expresion MAS expresion 
                 | expresion MENOS expresion
                 | expresion ASTERISCO expresion
                 | expresion DIVISION expresion 
                 | expresion MAYOR expresion 
                 | expresion MENOR expresion
                 | expresion MAYORIGUAL expresion
                 | expresion MENORIGUAL expresion
                 | expresion DIFERENTE expresion
                 | expresion DIFERENTE2 expresion
                 | expresion IGUAL expresion
                 | expresion EXPONENT expresion
                 | expresion MODULO expresion
                 | expresion OR expresion
                 | expresion AND expresion
    '''
    bnf.addProduccion(f'\<expresion> ::= \<expresion> "{p.slice[2].value}" \<expresion>')
    if p[2] == '+':
        p[0] = ExpresionAritmetica(p[1], p[3], OPERACION_ARITMETICA.MAS, p.slice[2].lineno)
    elif p[2] == '-':
        p[0] = ExpresionAritmetica(p[1], p[3], OPERACION_ARITMETICA.MENOS, p.slice[2].lineno)
    elif p[2] == '*':
        p[0] = ExpresionAritmetica(p[1], p[3], OPERACION_ARITMETICA.POR, p.slice[2].lineno)
    elif p[2] == '/':
        p[0] = ExpresionAritmetica(p[1], p[3], OPERACION_ARITMETICA.DIVIDO, p.slice[2].lineno)
    elif p[2] == '%':
        p[0] = ExpresionAritmetica(p[1], p[3], OPERACION_ARITMETICA.MODULO, p.slice[2].lineno)
    elif p[2] == '^':
        p[0] = ExpresionAritmetica(p[1], p[3], OPERACION_ARITMETICA.EXPONENTE, p.slice[2].lineno)
    elif p[2] == '<':
        p[0] = ExpresionComparacion(p[1], p[3], OPERACION_RELACIONAL.MENOR, p.slice[2].lineno)
    elif p[2] == '>':
        p[0] = ExpresionComparacion(p[1], p[3], OPERACION_RELACIONAL.MAYOR, p.slice[2].lineno)
    elif p[2] == '<=':
        p[0] = ExpresionComparacion(p[1], p[3], OPERACION_RELACIONAL.MENORIGUAL, p.slice[2].lineno)
    elif p[2] == '>=':
        p[0] = ExpresionComparacion(p[1], p[3], OPERACION_RELACIONAL.MAYORIGUAL, p.slice[2].lineno)
    elif p[2] == '=':
        p[0] = ExpresionComparacion(p[1], p[3], OPERACION_RELACIONAL.IGUAL, p.slice[2].lineno)
    elif p[2] == '<>':
        p[0] = ExpresionComparacion(p[1], p[3], OPERACION_RELACIONAL.DESIGUAL, p.slice[2].lineno)
    elif p[2] == '!=':
        p[0] = ExpresionComparacion(p[1], p[3], OPERACION_RELACIONAL.DESIGUAL, p.slice[2].lineno)
    elif p[2] == 'and':
        p[0] = ExpresionLogica(p[1], p[3], OPERACION_LOGICA.AND, p.slice[2].lineno)
    elif p[2] == 'AND':
        p[0] = ExpresionLogica(p[1], p[3], OPERACION_LOGICA.AND, p.slice[2].lineno)
    elif p[2] == 'or':
        p[0] = ExpresionLogica(p[1], p[3], OPERACION_LOGICA.OR, p.slice[2].lineno)
    elif p[2] == 'OR':
        p[0] = ExpresionLogica(p[1], p[3], OPERACION_LOGICA.OR, p.slice[2].lineno)

#----------------------------------------------------------------------------------------------------- FIN EXPRESION
#<EXP_AUX>::= '-'  <EXP_AUX>
#          |    '+'  <EXP_AUX>
#          | <EXP_AUX>  '+'  <EXP_AUX>
#          | <EXP_AUX>  '-'  <EXP_AUX>
#          | <EXP_AUX>  '*'  <EXP_AUX>
#          | <EXP_AUX>  '/'  <EXP_AUX>
#          | <EXP_AUX>  '%'  <EXP_AUX>
#          | <EXP_AUX>  '^'  <EXP_AUX>
def p_exp_aux_unarias(p):
    ''' exp_aux : MENOS exp_aux %prec UMENOS 
                | MAS exp_aux %prec UMAS
                | NOT exp_aux'''
    if p[1] == '+':
        p[0] = ExpresionPositiva(p[2], p.slice[1].lineno)
        bnf.addProduccion('\<exp_aux> ::= "-" \<exp_aux>')
    elif p[1] == '-':
        p[0] = ExpresionNegativa(p[2], p.slice[1].lineno)
        bnf.addProduccion('\<exp_aux> ::= "+" \<exp_aux>')
    else:
        p[0] = ExpresionNegada(p[2])
        bnf.addProduccion('\<exp_aux> ::= "NOT" \<exp_aux>')


        
def p_exp_auxp(p):
    '''exp_aux : exp_aux MAS exp_aux 
                 | exp_aux MENOS exp_aux
                 | exp_aux ASTERISCO exp_aux
                 | exp_aux DIVISION exp_aux 
                 | exp_aux EXPONENT exp_aux
                 | exp_aux MODULO exp_aux
    '''
    bnf.addProduccion(f'\<expresion> ::= \<expresion> "{p.slice[2].value}" \<expresion>')
    if p[2] == '+':
        p[0] = ExpresionAritmetica(p[1], p[3], OPERACION_ARITMETICA.MAS, p.slice[2].lineno)
    elif p[2] == '-':
        p[0] = ExpresionAritmetica(p[1], p[3], OPERACION_ARITMETICA.MENOS, p.slice[2].lineno)
    elif p[2] == '*':
        p[0] = ExpresionAritmetica(p[1], p[3], OPERACION_ARITMETICA.POR, p.slice[2].lineno)
    elif p[2] == '/':
        p[0] = ExpresionAritmetica(p[1], p[3], OPERACION_ARITMETICA.DIVIDO, p.slice[2].lineno)
    elif p[2] == '%':
        p[0] = ExpresionAritmetica(p[1], p[3], OPERACION_ARITMETICA.MODULO, p.slice[2].lineno)
    elif p[2] == '^':
        p[0] = ExpresionAritmetica(p[1], p[3], OPERACION_ARITMETICA.EXPONENTE, p.slice[2].lineno)
#          | '(' <EXP_AUX> ')'
def p_exp_aux_entre_parentesis(p):
    'exp_aux : PABRE exp_aux  PCIERRA'
    bnf.addProduccion('\<exp_aux> ::= "(" \<exp_aux> ")"')
    p[0] = p[2]
#          | 'cadena'
def p_exp_aux_cadena(p):
    'exp_aux :  CADENA'
    p[0] = ExpresionCadena(p[1], TIPO_DE_DATO.CADENA, p.slice[1].lineno)
    bnf.addProduccion(f'\<exp_aux> ::= "CADENA"')
#          | 'numero'          
def p_exp_aux_numero(p):
    'exp_aux :  NUMERO'
    p[0] = ExpresionNumero(p[1], TIPO_DE_DATO.ENTERO, p.slice[1].lineno)
    bnf.addProduccion(f'\<exp_aux> ::= "NUMERO"')
#          | 'decimal'
def p_exp_aux_decimal(p):
    'exp_aux :  DECIMAL_LITERAL'
    p[0] = ExpresionNumero(p[1], TIPO_DE_DATO.DECIMAL, p.slice[1].lineno)
    bnf.addProduccion(f'\<exp_aux> ::= "DECIMAL_LITERAL"')
#          | 'id' '.' 'id'
def p_exp_aux_tabla(p):
    'exp_aux :  ID PUNTO ID'
    p[0] = ExpresionID(p[3], p.slice[1].lineno , tabla = p[1])
    bnf.addProduccion('\<exp_aux> ::= "ID" "." "ID"')
#          | 'id'
def p_exp_aux_id(p):
    'exp_aux :  ID'
    p[0] = ExpresionID(p[1], p.slice[1].lineno)
    bnf.addProduccion('\<exp_aux> ::= "ID"')
#          | <FUNCIONES>
def p_exp_aux_funciones(p):
    'exp_aux :  funciones'
    bnf.addProduccion('\<exp_aux> ::= \<funciones>')
    p[0] = p[1]

#<SUBQUERY> ::= '('<SELECT>')'
def p_subquery(p):
        'subquery :  PABRE select PCIERRA'
        bnf.addProduccion('\<subquery> ::= "(" \<select> ")"')

#<WHERE> ::= 'where' <EXPRESION>
def p_where(p):
        'where : WHERE expresion'
        bnf.addProduccion('\<where> ::= "WHERE" \<expresion>')

#<GROUP_BY> ::= <LISTA_IDS>
def p_groupby(p):
        'group_by : GROUP BY lista_ids'
        bnf.addProduccion('\<group_by> ::= "GROUP" "BY" \<lista_ids>')

#<HAVING> ::= 'having' <EXPRESION>
def p_having(p):
        'having : HAVING expresion'
        bnf.addProduccion('\<having> ::= "HAVING" \<expresion>')

#    <ORDERS> ::= <ORDERBY>
def p_orders(p):
        'orders : orderby'
        bnf.addProduccion('\<orders> ::= \<orderby>')
        p[0] = [p[1]]
#                |<ORDERS> ',' <ORDERBY>
def p_orders1(p):
        'orders : orders COMA orderby'
        bnf.addProduccion('\<orders> ::= \<orders> "," <orderby>')
        p[1].append(p[3])
        p[0] = p[1]  

#    <ORDERBY> ::= 'order' 'by' <EXPRESION> <ASC_DEC> <NULLS>
def p_orderby(p):
        'orderby : ORDER BY expresion asc_dec nulls'
        bnf.addProduccion('\<orderby> ::= "ORDER" "BY" \<expresion> \<asc_dec> \<nulls>')
#               | 'order' 'by' <EXPRESION> <ASC_DEC>
def p_orderby1(p):
        'orderby : ORDER BY expresion asc_dec'
        bnf.addProduccion('\<orderby> ::= "ORDER" "BY" \<expresion> \<asc_dec>')
#                | 'order' 'by' <EXPRESION> <NULLS>
def p_orderby2(p):
        'orderby : ORDER BY expresion nulls'
        bnf.addProduccion('\<orderby> ::= "ORDER" "BY" \<expresion> \<nulls>')
#                | 'order' 'by' <EXPRESION>        
def p_orderby3(p):
        'orderby : ORDER BY expresion'
        bnf.addProduccion('\<orderby> ::= "ORDER" "BY" \<expresion>')

#    <ASC_DEC> ::= 'asc'
def p_asc_dec(p):
        'asc_dec : ASC'
        bnf.addProduccion('\<asc_dec> ::= "ASC"')
        p[0] =p[1]
#               | 'desc'
def p_asc_dec1(p):
        'asc_dec : DESC'
        bnf.addProduccion('\<asc_dec> ::= "DESC"')
        p[0] =p[1]

#<NULLS> ::= 'nulls' <FIRST_LAST>
def p_nulls(p):
        'nulls : NULLS first_last'
        bnf.addProduccion('\<nulls> ::= "NULLS" \<first_last>')

#   <FIRST_LAST> ::= 'first'
def p_first_last(p):
        'first_last : FIRST'
        bnf.addProduccion('\<first_last> ::= "FIRST"')
        p[0] =p[1]
#                |    'last'
def p_first_last1(p):
        'first_last : LAST'
        bnf.addProduccion('\<first_last> ::= "LAST"')
        p[0] =p[1]
def p_select_item1(p):
    'select_item : exp_aux'
# ESTAS 3 POSIBILIDADES YA ESTAN CONSIDERADAS EN EXP_AUX
#    <SELECT_ITEM>::=  'id'
#                  | 'id' '.' 'id'
#                  | select_item : funciones'

def p_select_item2(p):
        'select_item : count'
        bnf.addProduccion('\<select_item> ::= \<count>')
        p[0] = p[1]
#                  | <AGGREGATE_F>
def p_select_item3(p):
        'select_item : aggregate_f'
        bnf.addProduccion('\<select_item> ::= \<aggregate_f>')
        p[0] = p[1]
#                  | <SUBQUERY>
def p_select_item4(p):
        'select_item : subquery'
        bnf.addProduccion('\<select_item> ::= \<subquery>')
        p[0] = p[1]
#                  | <CASE>
def p_select_item5(p):
        'select_item : case'
        bnf.addProduccion('\<select_item> ::= \<case>')
        p[0] = p[1]
#                  | <GREATEST>
def p_select_item6(p):
        'select_item : greatest'
        bnf.addProduccion('\<select_item> ::= \<greatest>')
        p[0] = p[1]
#                  | <LEAST>
def p_select_item7(p):
        'select_item : least'
        bnf.addProduccion('\<select_item> ::= \<least>')
        p[0] = p[1]

        
def p_select_item9(p):
        'select_item : ASTERISCO'
        bnf.addProduccion('\<select_item> ::= "ASTERISCO"')
        p[0] = p[1]
        
def p_select_item10(p):
        'select_item : ID PUNTO ASTERISCO'
        bnf.addProduccion('\<select_item> ::= "ID" "." "*"')

#    <COUNT> ::= 'count' '(' '*' ')'  
def p_count(p):
        'count : COUNT PABRE ASTERISCO PCIERRA'
        bnf.addProduccion('\<count> ::= "COUNT" "(" "*" ")"')
#             |  'count' '(' 'id' ')'
def p_count1(p):
        'count : COUNT PABRE ID PCIERRA'
        bnf.addProduccion('\<count> ::= "COUNT" "(" "ID" ")"')
#             |  'count' '(' 'distinct' 'id' ')' 
def p_count2(p):
        'count : COUNT PABRE DISTINCT ID PCIERRA'
        bnf.addProduccion('\<count> ::= "COUNT" "(" "DISTINCT" "ID" ")"')

#    <AGGREGATE_F> ::= 'sum' '(' 'id' ')'
def p_aggregate_f(p):
        'aggregate_f : SUM PABRE ID PCIERRA'
        bnf.addProduccion('\<aggregate_f> ::= "SUM" "(" "ID" ")"')
#                |     'avg' '(' 'id' ')'
def p_aggregate_f1(p):
        'aggregate_f : AVG PABRE ID PCIERRA'
        bnf.addProduccion('\<aggregate_f> ::= "AVG" "(" "ID" ")"')
#                |     'max' '(' 'id' ')'
def p_aggregate_f2(p):
        'aggregate_f : MAX PABRE ID PCIERRA'
        bnf.addProduccion('\<aggregate_f> ::= "MAX" "(" "ID" ")"')
#                |     'min' '(' 'id' ')'
def p_aggregate_f3(p):
        'aggregate_f : MIN PABRE ID PCIERRA'
        bnf.addProduccion('\<aggregate_f> ::= "MIN" "(" "ID" ")"')

#    <CASE> ::= 'case' <SUBCASE> <ELSE_CASE> 'end'
def p_case(p):
        'case : CASE subcase else_case END'
        bnf.addProduccion('\<case> ::= "CASE" \<subcase> \<else_case> "END"')
#             | 'case' <SUBCASE> 'end'   
def p_case1(p):
        'case : CASE subcase END'
        bnf.addProduccion('\<case> ::= "CASE" \<subcase>  "END"')   
#    <SUBCASE> ::= <WHEN_CASE>
def p_subcase(p):
        'subcase : when_case'
        bnf.addProduccion('\<subcase> ::= \<when_case>')
        p[0] = [p[1]]
#                | <SUBCASE> <WHEN_CASE>
def p_subcase1(p):
        'subcase : subcase when_case'
        bnf.addProduccion('\<subcase> ::= \<subcase> \<when_case>')
        p[1].append(p[2])
        p[0] = p[1]  

#<ELSE_CASE> ::= 'else' <EXPRESION>
def p_else_case(p):
        'else_case : ELSE expresion'
        bnf.addProduccion('\<else_case> ::= "ELSE" \<expresion>')

#<GREATEST> ::= 'greatest' '(' <LISTA_EXP>')'
def p_greatiest(p):
        'greatest : GREATEST PABRE lista_exp PCIERRA'
        bnf.addProduccion('\<greatest> ::= "GREATEST" "(" \<lista_exp> ")"')

#<LEAST> ::= 'least' '(' <LISTA_EXP> ')'
def p_least(p):
        'least : LEAST PABRE lista_exp PCIERRA'
        bnf.addProduccion('\<least> ::= "LEAST" "(" \<lista_exp> ")"')

# <LISTA_EXP> ::= <EXPRESION>
#            | <LISTA_EXP> ',' <EXPRESION>

def p_lista_exp_1(p):
    'lista_exp : expresion'
    bnf.addProduccion('\<lista_exp> ::= \<expresion>')
    p[0] = [p[1]]

def p_lista_exp_2(p):
    'lista_exp : lista_exp COMA expresion'  
    p[1].append(p[3])
    p[0] = p[1]
    bnf.addProduccion('\<lista_exp> ::=  \<lista_exp> "," \<expresion>')  

#<WHEN_CASE> ::= 'when' <EXPRESION> 'then' <EXPRESION>
def p_when_case(p):
    'when_case : WHEN expresion THEN expresion'
    bnf.addProduccion('\<when_case> ::=  "WHEN" \<expresion> "THEN" \<expresion>') 
        
def p_alias(p):
    '''alias : CADENA ''' # VALIDACION SEMANTICA QUE ESTA CADENA VENGA ENTRR COMILLAS DOBLES
    p[0] = p[1]
    bnf.addProduccion('\<alias> ::= "CADENA"')
    
def p_alias2(p):
    '''alias : ID '''
    p[0] = p[1]
    bnf.addProduccion('\<alias> ::= "ID"')
    

def p_error(p):
    print(p)
    print("Error sintáctico en '%s'" % p.value)




parser = yacc.yacc()


def analizarEntrada(entrada):
    return parser.parse(entrada)

arbolParser = analizarEntrada(''' 
select *
from tbcolaborador 
where substring(nombre,1,4) = 'suje' ;
''')
# print(arbolParser)
# arbolParser.dibujar()#viendo el resultado: 

