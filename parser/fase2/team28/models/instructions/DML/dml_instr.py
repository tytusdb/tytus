import pandas as pd

from models.instructions.shared import Instruction
from models.instructions.DDL.table_inst import CreateTB
from models.instructions.DML.special_functions import loop_list
from controllers.type_checker import TypeChecker
from controllers.symbol_table import SymbolTable
from controllers.error_controller import ErrorController
from controllers.data_controller import DataController
from models.instructions.shared import Where, putVarValues
from models.instructions.DML.special_functions import storage_columns, storage_table
from controllers.three_address_code import ThreeAddressCode

from models.Other.funcion import Funcion
from storageManager import jsonMode as j
'''
    Lenguaje de Manipulación de Datos (DML) =======================================================================================================================
'''


class Insert(Instruction):
    '''
        INSERT recibe tres parametros: 
            1. tabla a insertar
            2. columnas donde insertar (puede estar vacio (se inserta en todas))
            3. valores a insertar
    '''

    def __init__(self,  table, arr_columns, arr_values, tac, line, column):
        self.table = table
        self.arr_columns = arr_columns
        self.arr_values = arr_values
        self._tac = tac

        self.line = line
        self.column = column

    def __repr__(self):
        return str(vars(self))

    def compile(self, environment):
        database_id = SymbolTable().useDatabase
        #ejecutando si hay llamada a alguna funcion
        temps_array = []
        for value in self.arr_values:
            if isinstance(value, Funcion):
                temps_array.append(value.compile(environment))
        new_val = putVarValues(self._tac, temps_array, environment)

        temp = ''

        if new_val == self._tac: #Es un temporal --- quitar comillas

            temp = ThreeAddressCode().newTemp()

            if database_id is not None:
                ThreeAddressCode().addCode(f"{temp} = \"USE {database_id}; {new_val}\"")
            else:
                ThreeAddressCode().addCode(f"{temp} = \"{new_val}\"")
        else:
            temp = new_val

                    #LLAMANDO A FUNCION PARA ANALIZAR ESTA COCHINADA
        temp1 = ThreeAddressCode().newTemp()
        ThreeAddressCode().addCode(f"{temp1} = parse({temp})")
        return temp1

    def process(self, instruction):
        if self.arr_columns == None:
            # Solo nos dieron los valores, tienen que venir todos ---> Espino ya valida longitud? ---> CREO QUE SI -- TEST --
            vals_insert = []
            for column in self.arr_values:
                val = column.process(instruction)
                vals_insert.append(val.value)
            # print(vals_insert)
            if self.validateValues(vals_insert):
                pass
            else:
                return
            DataController().insert(self.table.alias, vals_insert, self.line, self.column)
        else:
            if len(self.arr_columns) == len(self.arr_values):
                dic = {}
                for i in range(len(self.arr_columns)):
                    id_col = self.arr_columns[i].alias
                    if id_col in dic:
                        desc = f'Columna {id_col} ya definida'
                        ErrorController().add(29, 'Execution', desc, self.line, self.column)
                        return None
                    else:
                        dic[id_col] = self.arr_values[i].process(
                            instruction).value

                # Pidiendo tabla
                database_id = SymbolTable().useDatabase
                table_tp = TypeChecker().searchTable(database_id, self.table.alias)
                headers = TypeChecker().searchColumnHeadings(table_tp)
                checker = CreateTB(None, None, None, None)
                # validando nombres de columnas ingresados
                for key in dic:
                    if not key in headers:
                        desc = f'Nombre de columna invalido, {key}'
                        ErrorController().add(26, 'Execution', desc, self.line, self.column)
                        return None
                for name_col in headers:
                    column = TypeChecker().searchColumn(table_tp, name_col).__dict__
                    if not name_col in dic:  # Valor Nulo --> ver si se puede
                        if column['_default'] is not None:
                            if isinstance(column['_default'], str):
                                dic[name_col] = column['_default'].replace(
                                    "\'", "")
                            else:
                                dic[name_col] = column['_default']
                        else:
                            dic[name_col] = None
                            if column['_notNull'] == True:
                                desc = f'Columna {name_col} no puede ser null'
                                ErrorController().add(28, 'Execution', desc, self.line, self.column)
                                return None
                            else:
                                dic[name_col] = None

                    else:  # validar valor
                        is_correct = checker.validateType(
                            column['_dataType'], dic.get(name_col), False)
                        if not is_correct:
                            desc = f'Valor no valido para la columna {name_col}'
                            ErrorController().add(9, 'Execution', desc, self.line, self.column)
                            return None
                        # VALIDAR CHECK
                        if not realizeCheck(column, dic, self.line, self.column):
                            return None

                # TODO: METER EL WHERE, VALIDAR UNIQUE Y VALIDAR CHECK
                ordered_vals = []
                for name_col in headers:
                    ordered_vals.append(dic.get(name_col))
                print(ordered_vals)
                DataController().insert(self.table.alias, ordered_vals,
                                        0, 1)  # Enviar numero de fila y columna
            else:
                desc = "Error Datos incompletos"
                ErrorController().add(28, 'Execution', desc, self.line, self.column)
        return None

    def validateValues(self, array_values: list):
        database_id = SymbolTable().useDatabase
        table_tp = TypeChecker().searchTable(database_id, self.table.alias)
        headers = TypeChecker().searchColumnHeadings(table_tp)
        if len(headers) != len(array_values):
            desc = "Error Datos incompletos"
            ErrorController().add(28, 'Execution', desc, self.line, self.column)
            return False

        checker = CreateTB(None, None, None, None)
        dic = dict(zip(headers, array_values))
        for index, name_col in enumerate(headers):
            column = TypeChecker().searchColumn(table_tp, name_col).__dict__
            is_correct = checker.validateType(
                column['_dataType'], array_values[index], False)
            if not is_correct:
                desc = f'Valor no valido para la columna {name_col}'
                ErrorController().add(9, 'Execution', desc, self.line, self.column)
                return False
            if not realizeCheck(column, dic, self.line, self.column):
                return False
        return True


class Update(Instruction):
    '''
        UPDATE recibe tres parametros: 
            1. tabla a insertar
            2. array de columnas con el valor a insertar (ColumnVal[])
            3. recibe un array con todas los parametros OPCIONALES
    '''

    def __init__(self,  table, arr_columns_vals, params, tac, line, column):
        self.table = table
        self.arr_columns_vals = arr_columns_vals
        self.params = params
        self._tac = tac

        self.line = line
        self.column = column

    def __repr__(self):
        return str(vars(self))

    def compile(self, instrucction):
       #CREANDO C3D
        temp = ThreeAddressCode().newTemp()
        database_id = SymbolTable().useDatabase
        if database_id is not None:
            ThreeAddressCode().addCode(f"{temp} = \"USE {database_id}; {self._tac}\"")
        else:
            ThreeAddressCode().addCode(f"{temp} = \"{self._tac}\"")
        #LLAMANDO A FUNCION PARA ANALIZAR ESTA COCHINADA
        temp1 = ThreeAddressCode().newTemp()
        ThreeAddressCode().addCode(f"{temp1} = parse({temp})")
        return temp1

    def process(self, instruction):
        # Obteniendo tabla de la cual voy a hacer el update
        database_id = SymbolTable().useDatabase
        table_tp = TypeChecker().searchTable(database_id, self.table)
        table_cont = DataController().extractTable(self.table, self.line, self.column)
        headers = TypeChecker().searchColumnHeadings(table_tp)
        table_update = pd.DataFrame(table_cont)

        tuplas = []  # t[0] = nombre columna, t[1] = valor a cambiar

        for column in self.arr_columns_vals:
            tuplas.append(column.process(instruction))
        d = {}
        d_col_names = {}
        # validando nombres de columnas ingresados
        for t in tuplas:
            if not t[0] in headers:
                desc = f'Nombre de columna invalido, {t[0]}'
                ErrorController().add(26, 'Execution', desc, self.line, self.column)
                return None
            else:
                d[headers.index(t[0])] = t[1].value
                d_col_names[t[0]] = t[1].value

        # validando tipo de valores para las columnas
        print(d_col_names)
        checker = CreateTB(None, None, None, None)
        for key in list(d_col_names.keys()):
            column = TypeChecker().searchColumn(table_tp, key).__dict__
            is_correct = checker.validateType(
                column['_dataType'], d_col_names.get(key), False)
            if not is_correct:
                desc = f'Valor no valido para la columna {key}'
                ErrorController().add(9, 'Execution', desc, self.line, self.column)
                return None
            if not realizeCheck(column, d_col_names, self.line, self.column):
                return None
        # CAMBIAR TODOS LOS REGISTROS DE LA TABLA
        if self.params == None:

            pk_col_name = TypeChecker().searchColPrimaryKey(table_tp)
            if pk_col_name == []:  # NO HAY LLAVE PRIMARIA

                pk_list = range(len(table_update.index))
                print(pk_list)
                for pk in pk_list:
                    DataController().update(self.table, d, [
                        pk], self.line, self.column)
            else:
                list_pks = []
                for col in pk_col_name:
                    list_pks.append(col.name)

                table_update.columns = headers
                pk_list = table_update[list_pks].values.tolist()
                print(pk_list)
                for pk in pk_list:
                    DataController().update(self.table, d, [
                        pk], self.line, self.column)

        else:
            if self.params is not list:
                self.params = [self.params]
            for option in self.params:
                if isinstance(option, Where):
                    table_update.columns = headers
                    storage_columns(table_cont, headers,
                                    self.line, self.column)
                    storage_table(table_cont, headers, self.table,
                                  self.line, self.column)
                    table_result = option.process(
                        instruction, table_update, self.table)

                    pk_col_name = TypeChecker().searchColPrimaryKey(table_tp)
                    if pk_col_name == []:  # NO HAY LLAVE PRIMARIA
                        pk_list = table_result.index.to_list()
                        print(pk_list)
                        lista_aux = pk_list
                        pk_list = []
                        for _, value in enumerate(lista_aux):
                            pk_list.append([f'{str(value[0])}|'])
                        for pk in pk_list:
                            if type(pk) is list:
                                DataController().update(self.table, d, pk, self.line, self.column)
                            else:
                                DataController().update(self.table, d, [pk], self.line, self.column)
                    else:
                        table_result.columns = headers
                        list_pks = []
                        for col in pk_col_name:
                            list_pks.append(col.name)

                        pk_list = table_result[list_pks].values.tolist()
                        print(pk_list)
                        lista_aux = pk_list
                        pk_list = []
                        for _, value in enumerate(lista_aux):
                            pk_list.append([f'{str(value[0])}|'])
                        for pk in pk_list:
                            if type(pk) is list:
                                DataController().update(self.table, d, pk, self.line, self.column)
                            else:
                                DataController().update(self.table, d, [pk], self.line, self.column)
        return None


class ColumnVal(Instruction):
    '''
        ColumnVal recibe dos parametros: 
            1. nombre del campo a insertar
            2. valor a poner
    '''

    def __init__(self,  column, value):
        self.column = column
        self.value = value
        self._tac = ''

    def __repr__(self):
        return str(vars(self))

    def process(self, instruction):

        id_col = self.column.alias
        val = self.value.process(instruction)

        return [id_col, val]


class Opt1(Instruction):
    '''
        Recibe si se ha introducido un ALIAS y un asterisco (true || false)
    '''

    def __init__(self, isAsterisco, alias):
        self.isAsterisco = isAsterisco
        self.alias = alias
        self._tac = ''

    def __repr__(self):
        return str(vars(self))

    def process(self, instrucction):
        pass


class Delete(Instruction):
    '''
        DELETE recibe la tabla donde tiene que borrar y recibe un array con todas los parametros OPCIONALES
        Las opciones disponibles en un array del DELETE
        opt1 = ASTERISK SQLALIAS || ASTERISK || SQLALIAS
        opt2 = USING
        opt3 = WHERE
        opt4 = RETURNING
    '''

    def __init__(self,  table, params, tac, line, column):
        self.table = table
        self.params = params
        self._tac = tac

        self.line = line
        self.column = column

    def __repr__(self):
        return str(vars(self))

    def compile(self, environment):
        database_id = SymbolTable().useDatabase
        #ejecutando si hay llamada a alguna funcion
        temps_array = []
        if self.params is not None:
            for value in self.params:
                if isinstance(value, Funcion):
                    temps_array.append(value.compile(environment))
        new_val = None
        if temps_array is not None:
            new_val = putVarValues(self._tac, temps_array, environment)
        else:
            new_val = self._tac
            
        temp = ''

        if new_val == self._tac: #Es un temporal --- quitar comillas

            temp = ThreeAddressCode().newTemp()

            if database_id is not None:
                ThreeAddressCode().addCode(f"{temp} = \"USE {database_id}; {new_val}\"")
            else:
                ThreeAddressCode().addCode(f"{temp} = \"{new_val}\"")
        else:
            temp = new_val

        #LLAMANDO A FUNCION PARA ANALIZAR ESTA COCHINADA
        temp1 = ThreeAddressCode().newTemp()
        ThreeAddressCode().addCode(f"{temp1} = parse({temp})")

        return temp1

    def process(self, instrucction):
        # Obteniendo tabla de la cual voy a borrar
        database_id = SymbolTable().useDatabase
        table_tp = TypeChecker().searchTable(database_id, self.table)
        table_cont = DataController().extractTable(self.table, self.line, self.column)
        headers = TypeChecker().searchColumnHeadings(table_tp)
        table_delete = pd.DataFrame(table_cont)

        if self.params == None:

            pk_col_name = TypeChecker().searchColPrimaryKey(table_tp)
            if pk_col_name == []:  # NO HAY LLAVE PRIMARIA
                pk_list = table_delete.index.tolist()
                print(pk_list)
                for pk in pk_list:
                    DataController().delete(self.table, pk, self.line, self.column)

            else:
                table_delete.columns = headers
                list_pks = []
                for col in pk_col_name:
                    list_pks.append(col.name)

                pk_list = table_delete[list_pks].values.tolist()
                print(pk_list)
                for pk in pk_list:
                    DataController().delete(self.table, pk, self.line, self.column)

        else:
            for option in self.params:
                if isinstance(option, Where):
                    table_delete.columns = headers
                    storage_columns(table_cont, headers,
                                    self.line, self.column)
                    storage_table(table_cont, headers, self.table,
                                  self.line, self.column)
                    table_result = option.process(
                        instrucction, table_delete, self.table)

                    pk_col_name = TypeChecker().searchColPrimaryKey(table_tp)
                    if pk_col_name == []:  # NO HAY LLAVE PRIMARIA
                        pk_list = table_result.index.to_list()
                        print(pk_list)
                        lista_aux = pk_list
                        pk_list = []
                        for _, value in enumerate(lista_aux):
                            pk_list.append([f'{str(value[0])}|'])
                        for pk in pk_list:
                            DataController().delete(self.table, pk, self.line, self.column)
                    else:
                        table_result.columns = headers
                        list_pks = []
                        for col in pk_col_name:
                            list_pks.append(col.name)

                        pk_list = table_result[list_pks].values.tolist()
                        print(pk_list)
                        lista_aux = pk_list
                        pk_list = []
                        for _, value in enumerate(lista_aux):
                            pk_list.append([f'{str(value[0])}|'])
                        for pk in pk_list:
                            DataController().delete(self.table, pk, self.line, self.column)

                    break
        return None


def realizeCheck(column: dict, dic: dict, line, pos_column):
    # VALIDAR CHECK
    if column['_check'] == []:
        print("NO tiene check")
        # no tiene check
    else:
        print("tiene check")
        condition = column['_check']['_condition_check']
        print(condition)
        val = eval(condition, dic)
        print(val)
        if not val:
            desc = f'Valor no cumple la condicion {condition} del check'
            ErrorController().add(9, 'Execution', desc, line, pos_column)
            return False
    return True
