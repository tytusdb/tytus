# Manual Técnico

## Funciones y clases

### Expresiones
![IMAGE](./img/1.png "Optional Title")

### Instrucciones
![IMAGE](./img/2.png "Optional Title")
![IMAGE](./img/3.png "Optional Title")
![IMAGE](./img/4.png "Optional Title")
![IMAGE](./img/5.png "Optional Title")

## Gramatica a usar

    <INICIO> ::= <INSTRUCCIONES>
    <INSTRUCCIONES> ::= <INSTRUCCIONES> <INSTRUCCION> 
            | <INSTRUCCION>

    <INSTRUCCION> ::= <COMBINE_QUERYS> ';'
                  | <INSERT> ';'
                  | <UPDATE> ';'
                  | <DELETE> ';'
                  | <DEFINICION> ';'
                  | <ALTER_TABLE> ';'
                  | <use> ';'
    
    <use> ::=  "USE" "ID" 

    <DEFINICION> ::= 'create' 'type' 'as' 'enum' '(' <LISTA_ENUM> ')'
                  | <CREATE_OR_REPLACE> 'database' <COMBINACIONES1>
                  | 'show' 'databases' 'like' 'regex'
                  | 'show' 'databases'
                  | 'alter' 'database' 'id' <ALTER>
                  | 'drop' 'database' 'if' 'exists' 'id'
                  | 'drop' 'database' 'id'
                  | 'drop' 'table' 'id'
                  | 'create' 'table' 'id' '('<COLUMNAS>')' <INHERITS>
                  | 'create' 'table' 'id' '('<COLUMNAS>')'

    <COLUMNAS> ::= <COLUMNA> 
                | <COLUMNAS> ',' <COLUMNA> 

    <COLUMNA> ::= 
            | 'id' <TIPO>
            | 'id' <TIPO> <LISTAOPCIONES> 
            | 'constraint' 'id' 'check' '('<LISTA_CONDICIONES>')' 
            | 'id' 'check' '('<LISTA_CONDICIONES>')'
            | 'unique' '('<LISTA_IDS>')'
            | 'primary' 'key' '('<LISTA_IDS>')'
            | 'foreign' 'key' '('<LISTA_IDS>')' 'references' 'id' '('<LISTA_IDS>')'

    <LISTAOPCIONES> ::= <LISTAOPCIONES> <OPCOL> 
                 | <OPCOL> 

    <OPCOL>   ::=  <DEFAULT> 
            |  <CONSTRAINTS>
            |  <CHECKS> 
            |  <NULLABLE>
            |  'primary' 'key'
            |  'references' 'id'


    <DEFAULT> ::= 'default' <VALOR>

    <NULLABLE> ::= 'not' 'null'
                | 'null'

    <CONSTRAINTS> ::= 'constraint' 'id' 'unique'
                    | 'unique'

    <CHECKS> ::= 'constraint' 'id' 'check' '('<EXPRESION>')'
                |'check' '('<EXPRESION>')' 
         

    <LISTA_CONDICIONES> ::= <EXPRESION>
                        |   <LISTA_CONDICIONES> ',' <EXPRESION>            

    <TIPO> ::= 'smallint'
            |  'integer'
            |  'bigint'
            |  'decimal'
            |  'numeric'
            |  'real'
            |  'double' 'precision'
            |  'money'
            |  'character' 'varying' '(''numero'')'
            |  'varchar' '(''numero'')'
            |  'character' '(''numero'')'
            |  'char' '(''numero'')'
            |  'text'
            |  'decimal' '(' 'numero' ',' 'numero' ')' 
            |  'date'
            |  <TIME>
            |  <INTERVAL>
            |  'boolean'


    <TIME> ::= 'time' '(''numero'')' 'tmstamp'
            |  'time' 'tmstamp'
            |  'time' '(''numero'')' 
            |  'time' 

    <INTERVAL> ::= 'interval' <FIELDS> '(''numero'')'
                |  'interval' <FIELDS>
                |  'interval' '(''numero'')'
                |  'interval'
                
    <FIELDS> ::= 'year'
              |  'month'
              |  'day'
              |  'hour'
              |  'minute'
              |  'second'

    <ALTER> ::= 'rename' 'to' 'id'
             | 'owner to' <NEW_OWNER>

    <NEW_OWNER> ::= 'id'
                 | 'current_user'
                 | 'session_user'

    <COMBINACIONES1> ::= 'if' 'not' 'exists' 'id' <COMBINACIONES2>
                      | 'id' <COMBINACIONES2>
                      | 'id'

    <COMBINACIONES2> ::= <OWNER>
                      |<MODE>
                      |<OWNER><MODE>

    <OWNER> ::= 'owner' 'id'
             | 'owner' '=' 'id'

    <MODE> ::= 'mode' 'entero'
            | 'mode' '=' 'entero'

    <CREATE_OR_REPLACE> ::= 'create'
                         | 'create' 'or' 'replace'
                  

    <LISTA_ENUM> ::= 'cadena'
                  | <LISTA_ENUM> ',' 'cadena'


    <ALTER_TABLE> ::=  'alter' 'table' 'id' <ALTER_OPTIONS>
                   |   'alter' 'table' 'id' <ALTER_VARCHAR_LISTA>

    
    <ALTER_OPTIONS> ::= 'add' 'column' 'id' <TIPO>
                    | 'drop' 'column' 'id'
                    | 'add' 'check' '(' 'id' '<''>' 'CADENA' ')'
                    | 'add' 'constraint' 'id' 'unique' '(' 'id' ')'
                    | 'add' 'foreign' 'key' '('<LISTA_IDS>')' 'references' <LISTA_IDS>
                    | 'alter' 'column' 'id' 'set' 'not' 'null' 
                    | 'drop' 'constraint' 'id'
                    | 'ADD' 'CONSTRAINT' 'ID' 'FOREIGN' 'KEY' '(' 'ID' ')' 'REFERENCES' 'ID' '(' 'ID' ')'
                    | 'ADD' 'FOREIGN' 'KEY' '(' <lista_ids> ')' 'REFERENCES' 'ID' '(' <lista_ids> ')'
                    | 'ALTER' 'COLUMN' 'ID' 'SET' 'NOT'  'NULL'
                    | 'DROP' 'CONSTRAINT' 'ID'
                    
    <ALTER_VARCHAR_LISTA>::= <ALTER_VARCHAR>
                           | <ALTER_VARCHAR_LISTA> ',' <ALTER_VARCHAR>
    
    <ALTER_VARCHAR> ::= 'alter' 'column' 'id' 'type' 'varchar(''entero'')'

    <INHERITS> ::= 'INHERITS' '(' 'ID' ')'
    
    <COMBINE_QUERYS> ::= <COMBINE_QUERYS> 'union' 'all'<SELECT>
                   | <COMBINE_QUERYS> 'union'<SELECT>
                   | <COMBINE_QUERYS> 'intersect' 'all'<SELECT>
                   | <COMBINE_QUERYS> 'intersect'<SELECT>
                   | <COMBINE_QUERYS> 'except' 'all'<SELECT>
                   | <COMBINE_QUERYS> 'except'<SELECT>
                   | <SELECT>

    <SELECT> ::= 'select' <SELECT_LIST> 'from' <LISTA_TABLAS> <FILTRO> 
              | 'select' <SELECT_LIST> 'from' <LISTA_TABLAS> <ORDERS> <LIMITS> <OFFSET>
              | 'select' <SELECT_LIST> 'from' <LISTA_TABLAS> <ORDERS> <LIMITS> 
              | 'select' <SELECT_LIST> 'from' <LISTA_TABLAS> <ORDERS> <OFFSET>
              | 'select' <SELECT_LIST> 'from' <LISTA_TABLAS> <ORDERS> 
              | 'select' <SELECT_LIST> 'from' <LISTA_TABLAS> <LIMITS> <OFFSET>
              | 'select' <SELECT_LIST> 'from' <LISTA_TABLAS> <LIMITS> 
              | 'select' <SELECT_LIST> 'from' <LISTA_TABLAS> <OFFSET>
              | 'select' 'distinct' <SELECT_LIST> 'from'  <LISTA_TABLAS> <FILTRO>      
              | 'select' 'distinct' <SELECT_LIST> 'from' <LISTA_TABLAS>  
              | 'select' <SELECT_LIST> 'from' <LISTA_TABLAS>
              | 'select' <SELECT_LIST> 
              | 'select' 'distinct'  <SELECT_LIST> 
              | select' <SELECT_LIST> 'from' <LISTA_TABLAS> <FILTRO>  <LIMITS>
              | select' 'distinct' <SELECT_LIST> 'from' <LISTA_TABLAS> <FILTRO>  <LIMITS>



    <LISTA_TABLAS> ::=  <LISTA_TABLAS> ',' <TABLA>
                     |  <TABLA>

    <ALIAS> ::= 'id'
              | 'cadena'

    <TABLA> ::=  'id' 
             |   'id' <alias>
             |   'id' 'as' <alias>
             |   <SUBQUERY>
             |   <SUBQUERY> <alias>
             |   <SUBQUERY> 'as' '<alias>
            


    <FILTRO>::= <WHERE><GROUP_BY><HAVING>
              |<WHERE><GROUP_BY>
              |<WHERE>

    <HAVING> ::= 'having' <EXPRESION>

    <WHERE> ::= 'where' <EXPRESION>

    <GROUP_BY> ::= <LISTA_IDS>

    <ORDERS> ::= <ORDERBY>
                |<ORDERS> ',' <ORDERBY>

    <ORDERBY> ::= 'order' 'by' <EXPRESION> <ASC_DEC> <NULLS>
                | 'order' 'by' <EXPRESION> <ASC_DEC>
                | 'order' 'by' <EXPRESION> <NULLS>
                | 'order' 'by' <EXPRESION> 

    <ASC_DEC> ::= 'asc'
                | 'desc'

    <NULLS> ::= 'nulls' <FIRST_LAST>

    <FIRST_LAST> ::= 'first'
                |    'last'

    <LIMITS> ::= 'limit' <LIMITC>

    <LIMITC> ::= 'numero'
                |'all'

    <OFFSET> ::= 'offset' 'numero'

    <SELECT_LIST> ::= <SELECT_ITEM>
                    | <SELECT_ITEM> <ALIAS>
                    | <SELECT_ITEM> 'AS' <ALIAS>
                    | <SELECT_LIST> ',' <SELECT_ITEM>
                    | <SELECT_LIST> ',' <SELECT_ITEM> <ALIAS>
                    | <SELECT_LIST> ',' <SELECT_ITEM> 'AS' <ALIAS>
  

    <SELECT_ITEM> ::=  <exp_aux>
                     | <COUNT>
                     | <SUBQUERY>
                     | <CASE>
                     | <GREATEST>
                     | <LEAST>
                     | '*'
                     | 'id' '.' '*'


    <COUNT> ::= 'count' '(' '*' ')'
             |  'count' '(' 'id' ')'
             |  'count' '(' 'distinct' 'id' ')'
    
    <AGGREGATE_F> ::= 'sum' '(' 'id' ')'
                |     'avg' '(' 'id' ')'
                |     'max' '(' 'id' ')'
                |     'min' '(' 'id' ')'

    <CASE> ::= 'case' <SUBCASE> <ELSE_CASE> 'end'
             | 'case' <SUBCASE> 'end'

    <GREATEST> ::= 'greatest' '(' <LISTA_EXP>')'

    <LEAST> ::= 'least' '(' <LISTA_EXP> ')'

    <SUBCASE> ::= <WHEN_CASE>
                | <SUBCASE> <WHEN_CASE>

    <WHEN_CASE> ::= 'when' <EXPRESION> 'then' <EXPRESION>

    <ELSE_CASE> ::= 'else' <EXPRESION>

    <SUBQUERY> ::= '('<SELECT>')'

    <INSERT> ::=  'insert' 'into'  'id' 'values' '('<LISTA_EXP>')'
                | 'insert' 'into' 'id' <parametros> 'values'  '('<LISTA_EXP>')'

    <LISTA_EXP> ::= <EXPRESION>
               | <LISTA_EXP> ',' <EXPRESION>


    <PARAMETROS> ::= '(' <LISTA_IDS> ')'

    <LISTA_IDS> ::= <LISTA_IDS> ',' 'ID'  
             | 'ID'

    <EXPRESION> ::=  '-'  <EXPRESION>
                |    '+'  <EXPRESION>
                | <EXPRESION> '<>'  <EXPRESION>
                | <EXPRESION> 'and'  <EXPRESION>
                | <EXPRESION> 'or'   <EXPRESION>
                | <EXPRESION> '='  <EXPRESION>
                | <EXPRESION> '!='  <EXPRESION>
                | <EXPRESION> '>='  <EXPRESION>
                | <EXPRESION> '<='  <EXPRESION> 
                | <EXPRESION>  '>'  <EXPRESION>
                | <EXPRESION>  '<'  <EXPRESION>
                | <EXPRESION>  '+'  <EXPRESION>
                | <EXPRESION>  '-'  <EXPRESION>
                | <EXPRESION>  '*'  <EXPRESION>
                | <EXPRESION>  '/'  <EXPRESION>
                | <EXPRESION>  '%'  <EXPRESION>
                | <EXPRESION>  '^'  <EXPRESION>
                | <EXPRESION> 'between' <EXP_AUX> 'and' <EXP_AUX>
                | <EXPRESION> 'not' 'between' <EXP_AUX> 'and' <EXP_AUX>
                | <EXPRESION> 'between' 'symmetric' <EXP_AUX> 'and' <EXP_AUX>
                | <EXPRESION> 'not' 'between' 'symmetric' <EXP_AUX> 'and' <EXP_AUX>
                | <EXPRESION> 'is' 'distinct' 'from' <EXPRESION>
                | <EXPRESION> 'is' 'not' 'distinct' 'from' <EXPRESION>
                | <EXPRESION> 'is' 'null'
                | <EXPRESION> 'is' 'not' 'null'
                | <EXPRESION> 'isnull'
                | <EXPRESION> 'notnull'
                | <EXPRESION> 'is' 'true'
                | <EXPRESION> 'is' 'not' 'true'
                | <EXPRESION> 'is' 'false'
                | <EXPRESION> 'is' 'not' 'false'
                | <EXPRESION> 'is' 'unknown'
                | <EXPRESION> 'is' 'not' 'unknown'
                | 'cadena'
                | 'numero'
                | 'decimal_literal'
                | 'cadena_date'
                | 'id' '.' 'id'
                | 'id'
                | '(' <EXPRESION> ')'
                | 'id' in  <subquery>
                | 'id' 'not in'  <subquery>
                |  exist  <subquery>
                | <FUNCIONES>


        <EXP_AUX> ::= '-'  <EXP_AUX>
                |    '+'  <EXP_AUX>
                | <EXP_AUX>  '+'  <EXP_AUX>
                | <EXP_AUX>  '-'  <EXP_AUX>
                | <EXP_AUX>  '*'  <EXP_AUX>
                | <EXP_AUX>  '/'  <EXP_AUX>
                | <EXP_AUX>  '%'  <EXP_AUX>
                | <EXP_AUX>  '^'  <EXP_AUX>
                | <EXPRESION> '<>'  <EXPRESION>
                | <EXPRESION> 'or'   <EXPRESION>
                | <EXPRESION> '='  <EXPRESION>
                | <EXPRESION> '!='  <EXPRESION>
                | <EXPRESION> '>='  <EXPRESION>
                | <EXPRESION> '<='  <EXPRESION> 
                | <EXPRESION>  '>'  <EXPRESION>
                | <EXPRESION>  '<'  <EXPRESION>
                | 'cadena'
                | 'numero'
                | 'decimal'
                | 'cadena_date'
                | 'id' '.' 'id'
                | 'id'
                | '(' <EXP_AUX> ')'
                | <FUNCIONES>


    <FUNCIONES> ::= 'length' '(' 'id' ')'
                    |   'substring' '(' 'id' ',' 'entero' ',' 'entero' ')'
                    |   'trim' '(' 'id' ')'
                    |   'md5' '(' 'cadena' ')'
                    |   'sha256' '(' 'cadena' ')'
                    |   'substr''(' 'id' ',' 'entero' ',' 'entero' ')'
                    |   'get_byte' '(' 'cadena' ':' ':' 'bytea' ',' 'numero' ')'
                    |   'set_byte' '(' 'cadena' ':' ':' 'bytea' ',' 'numero' ',' 'numero' ')'
                    |   'convert' '(' 'cadena' 'as' 'date' ')'
                    |   'convert' '(' 'cadena' 'as' 'integer' ')'
                    |   'encode' '(' 'cadena' ':' ':' 'bytea' ',' 'cadena' ')'
                    |   'decode' '(' 'cadena' ',' 'cadena' ')'
                    |   'as' '('<EXPRESION>')'
                    |   'acos' '('<EXPRESION>')'
                    |   'acosd' '('<EXPRESION>')'
                    |   'asin' '('<EXPRESION>')'
                    |   'asind' '('<EXPRESION>')'
                    |   'atan' '('<EXPRESION>')'
                    |   'atand' '('<EXPRESION>')'
                    |   'atan2' '('<EXPRESION>','<EXPRESION>')'
                    |   'atan2d' '('<EXPRESION>','<EXPRESION>')'
                    |   'cos' '('<EXPRESION>')'
                    |   'cosd' '('<EXPRESION>')'
                    |   'cot' '('<EXPRESION>')'
                    |   'cotd' '('<EXPRESION>')'
                    |   'sin' '('<EXPRESION>')'
                    |   'sind' '('<EXPRESION>')'
                    |   'tan' '('<EXPRESION>')'
                    |   'tand' '('<EXPRESION>')'
                    |   'cosh' '('<EXPRESION>')'
                    |   'sinh' '('<EXPRESION>')'
                    |   'tanh' '('<EXPRESION>')'
                    |   'acosh' '('<EXPRESION>')'
                    |   'asinh' '('<EXPRESION>')'
                    |   'atanh' '('<EXPRESION>')'
                    |   'abs' '('<EXPRESION>')'
                    |   'cbrt' '('<EXPRESION>')'
                    |   'ceil' '('<EXPRESION>')'
                    |   'ceiling' '('<EXPRESION>')'
                    |   'degrees' '('<EXPRESION>')'
                    |   'div' '('<EXPRESION>','<EXPRESION>')'
                    |   'exp' '('<EXPRESION>')'
                    |   'factorial' '('<EXPRESION>')'
                    |   'floor' '('<EXPRESION>')'
                    |   'gcd' '('<EXPRESION>')'
                    |   'ln' '('<EXPRESION>')'
                    |   'log' '('<EXPRESION>')'
                    |   'mod' '('<EXPRESION>',' <EXPRESION>')'
                    |   'pi' '('')'
                    |   'power' '('<EXPRESION>',' <EXPRESION>')'
                    |   'radians' '('<EXPRESION>')'
                    |   'round' '('<EXPRESION>')'
                    |   'sign' '(' <TIPO_NUMERO> ')'
                    |   'sqrt' '(' <TIPO_NUMERO> ')'
                    |   'width_bucket' '(' <LISTA_NUMEROS> ')'
                    |   'trunc' '(' <TIPO_NUMERO> ',' 'numero' ')'
                    |   'trunc' '(' <TIPO_NUMERO> ')'
                    |   'random' '(' ')'
                    |   'sum' '(' 'id' ')'
                    |   'square_root' <TIPO_NUMERO> /* VALOR DEL TOKEN square_root: | */
                    |   'cube_root' <TIPO_NUMERO> /* VALOR DEL TOKEN cube_root: || */
                    |   <TIPO_NUMERO> 'bitwise_and' <TIPO_NUMERO> /* VALOR DEL TOKEN bitwise_and: & */
                    |   <TIPO_NUMERO> 'bitwise_or' <TIPO_NUMERO> /* VALOR DEL TOKEN bitwise_or: | */
                    |   <TIPO_NUMERO> 'bitwise_xor' <TIPO_NUMERO> /* VALOR DEL TOKEN bitwise_xor: # */
                    |   'bitwise_not' <TIPO_NUMERO> /* VALOR DEL TOKEN bitwise_not: ~ */
                    |   <TIPO_NUMERO> 'bitwise_shift_left' <TIPO_NUMERO> /* VALOR DEL TOKEN bitwise_shift_left: << */
                    |   <TIPO_NUMERO> 'bitwise_shift_right' <TIPO_NUMERO> /* VALOR DEL TOKEN bitwise_shift_right: >> */
                    |   <AGGREGATE_F>
     


    <DELETE> ::= 'delete' 'from' 'id' 'where' <EXPRESION>
         
    <UPDATE> ::= 'update' 'id' 'set' <LISTA_ASIGNACIONES> 'where' <EXPRESION>
 
    <LISTA_ASIGNACIONES> ::=  <LISTA_ASIGNACIONES> ',' 'id' '=' <EXPRESION>
                          |  'id' '=' <EXPRESION>