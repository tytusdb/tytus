from models.instructions.shared import Instruction
from models.Other.ambito import Ambito
from controllers.three_address_code import ThreeAddressCode
from controllers.procedures import Procedures
from models.instructions.Expression.expression import DATA_TYPE, PrimitiveData


class Parametro(Instruction):
    def __init__(self, id, data_type, line, column):
        self.id = id
        self.data_type = data_type
        self.line = line
        self.column = column
        self._tac = ''

    def compile(self):
        pass

    def process(self, environment):
        pass

    def __repr__(self):
        return str(vars(self))


class Funcion(Instruction):

    def __init__(self, id, params, body, val_return, isNew, isCall, line, column):
        self.id = id
        self.params = params
        self.body = body
        self.val_return = val_return
        self.isNew = isNew
        self.isCall = isCall
        self.environment = None
        self.line = line
        self.column = column
        self._tac = ''

    def __repr__(self):
        return str(vars(self))

    def process(self, environment):
        pass

    def compile(self, environment):
        params = len(self.params)
        temporal = None
        if self.isNew:
            self.environment = environment  # TODO verificar
            if Procedures().saveProcedure(self.id, self, self.val_return, self.line, self.column):
                var_array = self.print(environment)
                temporal = self.setVariables(var_array, environment)
        else:
            var_array = Procedures().getProcedure(self.id, params, self.line, self.column)
            if var_array:
                temporal = self.setVariables(var_array, environment)
            else:
                fun = ThreeAddressCode().searchFunction(self.id)
                if fun:
                    temporal = self.setVariables(fun['variables'], environment)
        
        return temporal
                #temp = ThreeAddressCode().newTemp()


    def print(self, environment):
        if ThreeAddressCode().searchFunction(self.id):
            return None

        ThreeAddressCode().newFunction(self.id)
        newAmbito = Ambito(environment)
        pos = 0
        var_array = []
        for var in self.params:
            pos = ThreeAddressCode().stackCounter
            var_array.append(newAmbito.addVar(var.id, var.data_type, None,
                                              pos, var.line, var.column))
            ThreeAddressCode().incStackCounter()

        pos = ThreeAddressCode().stackCounter
        #Generando etiqueta de salida para la funcion
        lbl_exit = ThreeAddressCode().newLabel()
        newAmbito.lbl_return = lbl_exit

        #Agregando cuerpo de la funcion
        self.body.compile(newAmbito)
        # Agregando etiqueta de salida
        ThreeAddressCode().addCode(f"label .{lbl_exit}")  
        # Imprime primera variable declarada, NO parametro
        # ThreeAddressCode().addCode(f"print(Stack[{pos}])")

        ThreeAddressCode().createFunction(self.id, self.params, var_array)
        return var_array

    def setVariables(self, var_array, environment):
        if self.isCall:
            value = 0
            for index, var in enumerate(var_array):
                value = self.params[index].compile(environment)

                if isinstance(value, PrimitiveData):
                    if value.data_type == DATA_TYPE.STRING:
                        if value.value[0]  == "'" or value.value[0]  == "\"":
                            value.value = f"\"{value.value}\""
                        else:
                            value.value = f"\'{value.value}\'"
                            
                ThreeAddressCode().addCode(f"Stack[{var.position}] = {value.value}")

            temp = ThreeAddressCode().newTemp()
            
            #Llamando a la funcion
            ThreeAddressCode().addCode(f"{self.id}()")
            #Obteniendo el valor de retorno de la funcion
            ThreeAddressCode().addCode("#Obteniendo valor de retorno--------")
            ThreeAddressCode().addCode(f"{temp} = Stack[P]")
            return temp
        return None


class DropFuncion(Instruction):
    def __init__(self, id, params, line, column):
        self.id = id
        self.params = params
        self.line = line
        self.column = column

class ProcedimientoAlmacenado(Instruction):

    def __init__(self, id, params, body, isNew, isCall, line, column):
        self.id = id
        self.params = params
        self.body = body
        self.isNew = isNew
        self.isCall = isCall
        self.environment = None
        self.line = line
        self.column = column

    def __repr__(self):
        return str(vars(self))

    def process(self, environment):
        pass

    def compile(self, environment):
        params = len(self.params)
        if self.isNew:
            self.environment = environment  # TODO verificar
            if Procedures().saveProcedure(self.id, self, None, self.line, self.column):
                var_array = self.print(environment)
                self.setVariables(var_array, environment)
        else:
            var_array = Procedures().getProcedure(self.id, params, self.line, self.column)
            if var_array:
                self.setVariables(var_array, environment)

            fun = ThreeAddressCode().searchFunction(self.id)
            if fun:
                
                self.setVariables(fun['variables'], environment)
                #temp = ThreeAddressCode().newTemp()


    def print(self, environment):
        if ThreeAddressCode().searchFunction(self.id):
            return None

        ThreeAddressCode().newFunction(self.id)
        newAmbito = Ambito(environment)
        pos = 0
        var_array = []
        for var in self.params:
            pos = ThreeAddressCode().stackCounter
            var_array.append(newAmbito.addVar(var.id, var.data_type, None,
                                              pos, var.line, var.column))
            ThreeAddressCode().incStackCounter()

        pos = ThreeAddressCode().stackCounter
        #Generando etiqueta de salida para la funcion
        lbl_exit = ThreeAddressCode().newLabel()
        newAmbito.lbl_return = lbl_exit

        #Agregando cuerpo de la funcion
        self.body.compile(newAmbito)
        # Agregando etiqueta de salida
        ThreeAddressCode().addCode(f"label .{lbl_exit}")  
        # Imprime primera variable declarada, NO parametro
        # ThreeAddressCode().addCode(f"print(Stack[{pos}])")

        ThreeAddressCode().createFunction(self.id, self.params, var_array)
        return var_array

    def setVariables(self, var_array, environment):
        if self.isCall:
            value = 0
            for index, var in enumerate(var_array):
                value = self.params[index].compile(environment)

                if isinstance(value, PrimitiveData):
                    if value.data_type == DATA_TYPE.STRING:
                        value.value = f"\'{value.value}\'"

                ThreeAddressCode().addCode(f"Stack[{var.position}] = {value.value}")
            
            #Llamando a la funcion
            ThreeAddressCode().addCode(f"{self.id}()")
            #Una procedimiento almacenado NO devuelve nada