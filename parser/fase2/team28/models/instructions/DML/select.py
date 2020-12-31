from numpy.core.records import array
from numpy.lib.arraysetops import isin
from views.data_window import DataWindow
from models.instructions.shared import *
from models.instructions.Expression.expression import *
from models.instructions.DML.special_functions import *
import pandas as pd 
class Union(Instruction):
    def __init__(self,  array_instr, type_union,line, column) :
        self.array_instr = array_instr
        self.type_union = type_union
        self.line = line
        self.column = column
    def __repr__(self):
        return str(vars(self))
    
    def process(self, instrucction):
        pass
class Select(Instruction):
    '''
        SELECT recibe un array con todas los parametros
    '''
    def __init__(self,  instrs, order_option, limit_option) :
        self.instrs = instrs
        self.order_option = order_option
        self.limit_option = limit_option
        self.alias = f'{self.instrs.alias}'
    def __repr__(self):
        return str(vars(self))
    
    def process(self, instrucction):
        instr = None
        order = None
        limit = None
        try:
            if self.instrs != None and self.order_option != None and self.limit_option != None:
                instr = self.instrs.process(instrucction)
                order = self.order_option.process(instrucction, instr)
                limit = self.limit_option.process(instrucction, order)
                return limit
            elif self.instrs != None and self.order_option != None and self.limit_option == None:
                instr = self.instrs.process(instrucction)
                order = self.order_option.process(instrucction,instr)
                return order
            elif self.instrs != None  and self.order_option == None and self.limit_option != None:
                instr = self.instrs.process(instrucction)
                limit = self.limit_option.process(instrucction, instr)
                return limit
            elif self.instrs != None and self.order_option == None and self.limit_option == None:
                instr = self.instrs.process(instrucction)
                return instr
        except:
            desc = "FATAL ERROR, murio en Select, F"
            ErrorController().add(34, 'Execution', desc, self.line, self.column)
    
class TypeQuerySelect(Instruction):
    '''
    TypeQuerySelect recibe si va a ser 
    UNION 
    INTERSECT
    EXCEPT
    Y si va a ir con la opcion ALL 
    '''
    def __init__(self, arr_select, line, column):
        self.arr_select = arr_select
        self.line = line
        self.column = column
        self.alias = f'{arr_select[0].alias}'
    def __repr__(self):
        return str(vars(self))
    
    def process(self, instrucction):
        select1 = None
        select2 = None
        table_result = None
        ## ALL OPTION
        try:
            if len(self.arr_select) == 4:
                type_query = self.arr_select[1]
                select1 = self.arr_select[0]
                select2 = self.arr_select[3]
                if isinstance(select1, Select):
                        select1 = select1.process(instrucction)
                if isinstance(select2, Select):
                        select2 = select2.process(instrucction)
                if type_query.lower() == "union":
                    table_result = pd.concat([select1, select2])
                elif type_query.lower() == 'intersect':
                    table_result = pd.merge(select1, select2, how='inner')
                elif type_query.lower() == 'except':
                    table_result = select1.merge(select2, how='outer', indicator = True).query("_merge == 'left_only'").drop('_merge', 1)
        ## SIN ALL OPTION 
            else:
                type_query = self.arr_select[1]
                select1 = self.arr_select[0]
                select2 = self.arr_select[2]
                if isinstance(select1, Select):
                    select1 = select1.process(instrucction)
                if isinstance(select2, Select):
                    select2 = select2.process(instrucction)
                    
                if type_query.lower() == "union":
                    table_result = pd.concat([select1, select2]).drop_duplicates()
                elif type_query.lower() == 'intersect':
                    table_result = pd.merge(select1, select2, how='inner')
                elif type_query.lower() == 'except':
                    table_result = select1.merge(select2, how='outer', indicator = True).query("_merge == 'left_only'").drop('_merge', 1)
            return table_result
        except:
            desc = "FATAL ERROR, murio en TypeQuerySelect, F"
            ErrorController().add(34, 'Execution', desc, self.line, self.column)
            
class Table:
    def __init__(self, headers, values):
        self.headers = headers
        self.values = values
    def __repr__(self):
        return str(vars(self))

class SelectQ(Instruction):
    '''va a recibir la lista de parametros a seleccion y de que traba se esta seleccionando'''
    def __init__(self, type_select, select_list, from_clause, where_or_grouphaving,line, column):
        self.type_select = type_select
        self.select_list = select_list
        self.from_clause = from_clause
        self.where_or_grouphaving = where_or_grouphaving
        if self.from_clause == None:
            self.alias = None
        else:
            self.alias = f'{from_clause.alias}'
        self.line = line
        self.column = column

    def __repr__(self):
        return str(vars(self))
    
    def process(self, instrucction):
        list_select = None
        # print(self.alias)
        try:
           #########################################################################################################################################
            if self.type_select == None and self.from_clause == None and self.where_or_grouphaving == None and self.select_list != None:
                print( self.select_list )
                list_select = list_expressions(self.select_list, instrucction)
                return list_select
            
            ################################################################################################################################
            elif self.type_select != None and self.from_clause != None and self.where_or_grouphaving == None and self.select_list != None:
                list_from = self.from_clause.process(instrucction)
                type_select = self.type_select
                ## Esto es para selects simples 
                if len(list_from) > 1:
                    if isinstance(self.select_list[0], PrimitiveData) and len(self.select_list) == 1:
                        list_select = loop_list(self.select_list, instrucction)
                        if type_select.lower() == 'distinct' or  type_select.lower() == 'unique':
                            list_from[0] = list_from[0].drop_duplicates()
                            return list_from[0]
                        else:
                            return list_from[0]   
                    # elif isinstance(self.select_list[0], ObjectReference) and len(self.select_list) == 1:
                    #     if type_select.lower() == 'distinct' or  type_select.lower() == 'unique':
                    #         list_from[0] = list_from[0].drop_duplicates()
                    #         return list_from[0]
                    #     else:
                    #         return list_from[0]  
                    else:
                        list_select = loop_list_with_columns(self.select_list, list_from[1], instrucction)
                        if type_select.lower() == 'distinct' or  type_select.lower() == 'unique':
                            list_select = list_select.drop_duplicates()
                            return list_select
                        else:
                            return list_select
                else:
                    if isinstance(self.select_list[0], PrimitiveData) and len(self.select_list) == 1:
                        list_select = loop_list(self.select_list, instrucction)
                        if type_select.lower() == 'distinct' or  type_select.lower() == 'unique':
                            list_from[0] = list_from[0].drop_duplicates()
                            return list_from[0]
                        else:
                            return list_from[0]       
                    # elif isinstance(self.select_list[0], ObjectReference) and len(self.select_list) == 1:
                    #     if type_select.lower() == 'distinct' or  type_select.lower() == 'unique':
                    #         list_from[0] = list_from[0].drop_duplicates()
                    #         return list_from[0]
                    #     else:
                    #         return list_from[0]                            
                    else:
                        list_select = loop_list_with_columns(self.select_list, self.alias, instrucction)
                        if type_select.lower() == 'distinct' or  type_select.lower() == 'unique':
                            list_select = list_select.drop_duplicates()
                            return list_select
                        else:
                            return list_select
            ####################################################################################################################################        
            elif self.type_select != None and self.from_clause != None and self.where_or_grouphaving != None and self.select_list != None:
                list_from = self.from_clause.process(instrucction)
                type_select = self.type_select
                where_table = None
                group_by = None
                if len(list_from) > 1:
                    if isinstance(self.select_list[0], PrimitiveData) and len(self.select_list) == 1:
                        list_select = loop_list(self.select_list, instrucction)
                        # print(type(self.where_or_grouphaving))
                        if isinstance(self.where_or_grouphaving, GroupBy):
                            list_select = list_expressions_groupby(self.select_list, instrucction)
                            group_by = self.where_or_grouphaving.process(instrucction,list_select)
                            if type_select.lower() == 'distinct' or  type_select.lower() == 'unique':
                                group_by = group_by.drop_duplicates()
                                return group_by
                            else:
                                return group_by
                        elif isinstance(self.where_or_grouphaving, Where):
                            where_table = self.where_or_grouphaving.process(instrucction, list_from[0], list_from[1])
                            if type_select.lower() == 'distinct' or  type_select.lower() == 'unique':
                                where_table = where_table.drop_duplicates()
                                return where_table
                            else:
                                return where_table
                        elif isinstance(self.where_or_grouphaving, list):
                            where_table = self.where_or_grouphaving[0]
                            where_table = where_table.process(instrucction, list_from[0], list_from[1])
                            list_select = list_expressions_groupby(self.select_list, instrucction)
                            group_by = self.where_or_grouphaving[1]
                            group_by = group_by.process(instrucction,list_select)
                            if type_select.lower() == 'distinct' or  type_select.lower() == 'unique':
                                group_by = group_by.drop_duplicates()
                                return group_by
                            else:
                                return group_by
                    else:
                        if isinstance(self.where_or_grouphaving, GroupBy):
                            list_select = list_expressions_groupby(self.select_list, instrucction)
                            group_by = self.where_or_grouphaving.process(instrucction,list_select)
                            if type_select.lower() == 'distinct' or  type_select.lower() == 'unique':
                                group_by = group_by.drop_duplicates()
                                return group_by
                            else:
                                return group_by
                        elif isinstance(self.where_or_grouphaving, Where):
                            where_table = self.where_or_grouphaving.process(instrucction, list_from[0], list_from[1])
                            list_select = loop_list_with_columns(self.select_list, list_from[1], instrucction)
                            if type_select.lower() == 'distinct' or  type_select.lower() == 'unique':
                                list_select = list_select.drop_duplicates()
                                return list_select
                            else:
                                return list_select
                        elif isinstance(self.where_or_grouphaving, list):
                            where_table = self.where_or_grouphaving[0]
                            where_table = where_table.process(instrucction, list_from[0], list_from[1])
                            list_select = list_expressions_groupby(self.select_list, instrucction)
                            group_by = self.where_or_grouphaving[1]
                            group_by = group_by.process(instrucction,list_select)
                            if type_select.lower() == 'distinct' or  type_select.lower() == 'unique':
                                group_by = group_by.drop_duplicates()
                                return group_by
                            else:
                                return group_by
                else:
                    if isinstance(self.select_list[0], PrimitiveData) and len(self.select_list) == 1:
                        list_select = loop_list(self.select_list, instrucction)
                        where_table = self.where_or_grouphaving.process(instrucction, list_from[0], list_from[1])
                        if type_select.lower() == 'distinct' or  type_select.lower() == 'unique':
                                where_table = where_table.drop_duplicates()
                                return where_table
                        else:
                            return where_table
                    # elif isinstance(self.select_list[0], ObjectReference) and len(self.select_list) == 1:
                    #     # list_select = loop_list(self.select_list, instrucction)
                    #     where_table = self.where_or_grouphaving.process(instrucction, list_from[0], list_from[1])
                    #     if type_select.lower() == 'distinct' or  type_select.lower() == 'unique':
                    #             where_table = where_table.drop_duplicates()
                    #             return where_table
                    #     else:
                    #         return where_table
                    else:
                        where_table = self.where_or_grouphaving.process(instrucction, list_from[0], self.alias)
                        list_select = loop_list_with_columns(self.select_list, self.alias, instrucction)
                        if type_select.lower() == 'distinct' or  type_select.lower() == 'unique':
                                list_select = list_select.drop_duplicates()
                                return list_select
                        else:
                            return list_select
            
            
            #######################################################################################################################################
            elif self.type_select == None and self.from_clause != None and self.where_or_grouphaving != None and self.select_list != None:
                list_from = self.from_clause.process(instrucction)
                where_table = None
                group_by = None
                if len(list_from) > 1:
                    if isinstance(self.select_list[0], PrimitiveData) and len(self.select_list) == 1:
                        list_select = loop_list(self.select_list, instrucction)
                        # print(type(self.where_or_grouphaving))
                        if isinstance(self.where_or_grouphaving, GroupBy):
                            list_select = list_expressions_groupby(self.select_list, instrucction)
                            group_by = self.where_or_grouphaving.process(instrucction,list_select)
                            return group_by
                        elif isinstance(self.where_or_grouphaving, Where):
                            where_table = self.where_or_grouphaving.process(instrucction, list_from[0], list_from[1])
                            return where_table
                        elif isinstance(self.where_or_grouphaving, list):
                            where_table = self.where_or_grouphaving[0]
                            where_table = where_table.process(instrucction, list_from[0], list_from[1])
                            list_select = list_expressions_groupby(self.select_list, instrucction)
                            group_by = self.where_or_grouphaving[1]
                            group_by = group_by.process(instrucction,list_select)
                            return group_by
                    else:
                        if isinstance(self.where_or_grouphaving, GroupBy):
                            list_select = list_expressions_groupby(self.select_list, instrucction)
                            group_by = self.where_or_grouphaving.process(instrucction,list_select)
                            return group_by
                        elif isinstance(self.where_or_grouphaving, Where):
                            where_table = self.where_or_grouphaving.process(instrucction, list_from[0], list_from[1])
                            list_select = loop_list_with_columns(self.select_list, list_from[1], instrucction)
                            return list_select
                        elif isinstance(self.where_or_grouphaving, list):
                            where_table = self.where_or_grouphaving[0]
                            where_table = where_table.process(instrucction, list_from[0], list_from[1])
                            list_select = list_expressions_groupby(self.select_list, instrucction)
                            group_by = self.where_or_grouphaving[1]
                            group_by = group_by.process(instrucction,list_select)
                            return group_by
                else:
                    if isinstance(self.select_list[0], PrimitiveData) and len(self.select_list) == 1:
                        list_select = loop_list(self.select_list, instrucction)
                        where_table = self.where_or_grouphaving.process(instrucction, list_from[0], list_from[1])
                        return where_table
                    # elif isinstance(self.select_list[0], ObjectReference) and len(self.select_list) == 1:
                    #     # list_select = loop_list(self.select_list, instrucction)
                    #     where_table = self.where_or_grouphaving.process(instrucction, list_from[0], list_from[1])
                    #     return where_table
                    else:
                        where_table = self.where_or_grouphaving.process(instrucction, list_from[0], self.alias)
                        list_select = loop_list_with_columns(self.select_list, self.alias, instrucction)
                        return list_select
            
        ###################################### SELECTS SIMPLES #######################################################################
            elif self.type_select == None and self.from_clause != None and self.where_or_grouphaving == None and self.select_list != None:
                list_from = self.from_clause.process(instrucction)
                ## Esto es para selects simples 
                if len(list_from) > 1:
                    if isinstance(self.select_list[0], PrimitiveData) and len(self.select_list) == 1:
                        list_select = loop_list(self.select_list, instrucction)
                        return list_from[0]
                    # elif isinstance(self.select_list[0], ObjectReference) and len(self.select_list) == 1:
                    #     # list_select = loop_list(self.select_list, instrucction)
                    #     return list_from[0]
                    else:
                        list_select = loop_list_with_columns(self.select_list, list_from[1], instrucction)
                        return list_select
                else:
                    if isinstance(self.select_list[0], PrimitiveData) and len(self.select_list) == 1:
                        list_select = loop_list(self.select_list, instrucction)
                        return list_from[0]
                    # elif isinstance(self.select_list[0], ObjectReference) and len(self.select_list) == 1:
                    #     # list_select = loop_list(self.select_list, instrucction) 
                    #     return list_from[0]
                    else:
                        list_select = loop_list_with_columns(self.select_list, self.alias, instrucction)
                        return list_select
        ######################################################################################################################################
        except:
            desc = "FATAL ERROR, murio en SELECTQ, F"
            ErrorController().add(34, 'Execution', desc, self.line, self.column)
            

class OrderClause(Instruction):
    '''
    Recibe Los parametros para order clause los cuales
    son la lista de parametros a ordenar y que tipo de
    order si ASC o DESC
    '''
    def __init__(self, arrvaluesorder, type_order,line, column):
        self.arrvaluesorder = arrvaluesorder
        self.type_order = type_order
        self.line = line
        self.column = column

    def __repr__(self):
        return str(vars(self))
    
    def process(self, instrucction, select_clasue: DataFrame):
        arrvaluesorder = None
        try:
            arrvaluesorder = loop_list_of_order_by(self.arrvaluesorder, instrucction)
            order_aux = []
            for x in arrvaluesorder:
                if self.type_order != None:
                    if self.type_order.lower() == 'desc':
                        order_aux.append(False)
                    elif self.type_order.lower() == 'asc':
                        order_aux.append(True)
                else:
                    order_aux.append(True)
            select_clasue.sort_values(by=arrvaluesorder,inplace=True,ascending=order_aux)
            return select_clasue
        except:
            desc = "FATAL ERROR, murio en OrderClause, F"
            ErrorController().add(34, 'Execution', desc, self.line, self.column)
        

class LimitClause(Instruction):
    '''
    Recibe los parametros para limit Clause los cuales
    son un rango establecido o bien solo un parametro y 
    la opcion OFFSET 
    '''
    def __init__(self, limitarr, offset,line, column):
        self.limitarr = limitarr
        self.offset = offset
        self.line = line
        self.column = column
        
    def __repr__(self):
        return str(vars(self))
    
    def process(self, instrucction, table: DataFrame):
        try:
            if self.limitarr != None and self.offset != None:
                limit = self.limitarr 
                offset = self.offset
                table = table.iloc[offset:offset+limit-1]
            elif self.limitarr != None and self.offset == None:
                if not isinstance(self.limitarr, int):
                    table.head()
                else:
                    table = table.head(int(self.limitarr))
            return table
        except:
            desc = "FATAL ERROR, murio en LimitClause, F"
            ErrorController().add(34, 'Execution', desc, self.line, self.column)

class JoinClause(Instruction):
    '''
    JoinClause recibe los parametros de 
    Tipo de Join, Tabla y Expression
    '''
    def __init__(self, type_join, table, arr_expression,line, column):
        self.type_join = type_join
        self.table = table
        self.arr_expression = arr_expression
        self.line = line
        self.column = column
        
    def __repr__(self):
        return str(vars(self))
    
    def process(self, instrucction):
        pass
    

    
class AgreggateFunctions(Instruction):
    '''
        AgreggateFunctions
    '''
    def __init__(self, type_agg, cont_agg, opt_alias,line, column):
        self.type_agg = type_agg
        self.cont_agg = cont_agg
        self.opt_alias = opt_alias
        self.alias = f'{self.type_agg}({cont_agg.alias})'
        self.line = line
        self.column = column
    def __repr__(self):
        return str(vars(self))
    
    def process(self, instrucction):
        data = None
        try:
            result = self.cont_agg.process(instrucction)
            if isinstance(result, list):
                if self.type_agg.lower() == "avg":
                    data = {str(self.alias): 'mean'}
                elif self.type_agg.lower() == 'sum':
                    data = {str(self.alias): 'sum'}
                elif self.type_agg.lower() == 'count':
                    data = {str(self.alias): 'size'}
                elif self.type_agg.lower() == 'max':
                    data = {str(self.alias): 'max'}
                elif self.type_agg.lower() == 'min':
                    data = {str(self.alias): 'min'}
                    #dict  # column  # encambezado
                return [result[0], result[1], data]
            else:
                if self.type_agg.lower() == "avg":
                    data = {str(self.alias.lower()): 'mean'}
                elif self.type_agg.lower() == 'sum':
                    data = {str(self.alias.lower()): 'sum'}
                elif self.type_agg.lower() == 'count':
                    data = {str(result.value): 'size'}
                elif self.type_agg.lower() == 'max':
                    data = {str(self.alias.lower()): 'max'}
                elif self.type_agg.lower() == 'min':
                    data = {str(self.alias.lower()): 'min'}
                return [data, result.value, self.type_agg]
        except:
            desc = "FATAL ERROR, murio en AgreggateFunctions, F"
            ErrorController().add(34, 'Execution', desc, self.line, self.column)

class Case(Instruction):
    '''
        CASE recibe un array con todas las opciones y un else
    '''
    def __init__(self, arr_op, c_else,line, column): 
        self.arr_op = arr_op
        self.c_else = c_else
        self.line = line
        self.column = column
        
    def __repr__(self):
        return str(vars(self))
    
    def process(self, instrucction):
        pass

class CaseOption(Instruction):
    '''
        CASE OPTION
    '''
    def __init__(self, when_exp, then_exp,line, column):
        self.when_exp = when_exp
        self.then_exp = then_exp
        self.line = line
        self.column = column
    def __repr__(self):
        return str(vars(self)) 

    def process(self, instrucction):
        pass  