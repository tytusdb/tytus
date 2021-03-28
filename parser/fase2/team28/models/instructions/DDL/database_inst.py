import re

from models.instructions.shared import Instruction
from models.database import Database
from controllers.type_checker import TypeChecker
from controllers.data_controller import DataController
from controllers.symbol_table import SymbolTable
from controllers.error_controller import ErrorController
from controllers.three_address_code import ThreeAddressCode
from views.data_window import DataWindow


class CreateDB(Instruction):

    def __init__(self, properties, replace, tac, noLine, noColumn):
        # if_not_exists:bool, id:str, listpermits: []
        self._properties = properties
        self._replace = replace
        self._noLine = noLine
        self._noColumn = noColumn
        self._tac = tac

    def __repr__(self):
        return str(vars(self))

    def process(self, instrucction):
        typeChecker = TypeChecker()
        database = typeChecker.searchDatabase(self._properties['id'])

        if database:
            if self._properties['if_not_exists']:
                return

            if self._replace:
                typeChecker.deleteDatabase(database.name, self._noLine,
                                           self._noColumn)

        # TODO Verificar permisos y modo
        database = Database(self._properties['id'])

        for permits in self._properties['listpermits']:
            if 'MODE' in permits:
                database.mode = permits['MODE']

        typeChecker.createDatabase(database, self._noLine,
                                   self._noColumn)

    def compile(self, instrucction):
        temp = ThreeAddressCode().newTemp()
        ThreeAddressCode().addCode(f"{temp} = '{self._tac}'")
        #LLAMANDO A FUNCION PARA ANALIZAR
        temp1 = ThreeAddressCode().newTemp()
        ThreeAddressCode().addCode(f"{temp1} = parse({temp})")
        return temp1


class DropDB(Instruction):

    def __init__(self, if_exists, database_name, tac, noLine, noColumn):
        self._if_exists = if_exists
        self._database_name = database_name
        self._noLine = noLine
        self._noColumn = noColumn
        self._tac = ''

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

    def process(self, instrucction):
        typeChecker = TypeChecker()
        database = typeChecker.searchDatabase(self._database_name)

        if self._if_exists and not database:
            return

        typeChecker.deleteDatabase(self._database_name, self._noLine,
                                   self._noColumn)


class ShowDatabase(Instruction):

    def __init__(self, patherMatch, tac):
        self._patherMatch = patherMatch
        self._tac = ''

    def compile(self, instrucction):
        temp = ThreeAddressCode().newTemp()
        ThreeAddressCode().addCode(f"{temp} = '{self._tac};'")

    def process(self, instrucction):
        databases = DataController().showDatabases()
        if self._patherMatch != None:
            if self._patherMatch.value[0] == '%' and self._patherMatch.value[-1] == '%':
                # Busca en cualquier parte
                pattern = rf"{self._patherMatch.value[1:-1].lower()}"
                databases = list(filter(lambda x: re.findall(pattern, x.lower()),
                                        databases))

            elif self._patherMatch.value[0] == '%':
                # Busca al final
                pattern = rf".{{0,}}{self._patherMatch.value[1:].lower()}$"
                databases = list(filter(lambda x: re.match(pattern, x.lower()),
                                        databases))

            elif self._patherMatch.value[-1] == '%':
                # Busca al inicio
                pattern = rf"{self._patherMatch.value[:-1].lower()}"
                databases = list(filter(lambda x: re.findall(pattern, x.lower()),
                                        databases))

            else:
                # Busca especificamente
                pattern = rf"{self._patherMatch.value.lower()}$"
                databases = list(filter(lambda x: re.match(pattern, x.lower()),
                                        databases))

        columnsData = []
        for db in databases:
            columnsData.append([db])
        DataWindow().consoleTable(['Databases'], columnsData)

    def __repr__(self):
        return str(vars(self))


class AlterDatabase(Instruction):
    '''
        ALTER DATABASE recibe ya sea el nombre o el duenio antiguo y lo sustituye por un nuevo nombre o duenio
        si recibe un 1 es porque es la base de datos
        si recibe un 2 es porque es el duenio
    '''

    def __init__(self, alterType, oldValue, newValue, tac, noLine, noColumn):
        self._alterType = alterType
        self._oldValue = oldValue
        self._newValue = newValue
        self._noLine = noLine
        self._noColumn = noColumn
        self._tac = ''

    def compile(self, instrucction):
        temp = ThreeAddressCode().newTemp()
        ThreeAddressCode().addCode(f"{temp} = '{self._tac};'")

    def process(self, instrucction):
        if self._alterType == 1:
            TypeChecker().updateDatabase(self._oldValue, self._newValue,
                                         self._noLine, self._noColumn)
        elif self._alterType == 2:
            pass

    def __repr__(self):
        return str(vars(self))


class UseDatabase(Instruction):
    '''
        Use database recibe el nombre de la base de datos que sera utilizada
    '''

    def __init__(self, dbActual, tac, noLine, noColumn):
        self._dbActual = dbActual
        self._noLine = noLine
        self._noColumn = noColumn
        self._tac = tac

    def compile(self, instrucction):
        temp = ThreeAddressCode().newTemp()
        ThreeAddressCode().addCode(f"{temp} = '{self._tac};'")
        SymbolTable().useDatabase = self._dbActual
        temp1 = ThreeAddressCode().newTemp()
        ThreeAddressCode().addCode(f"{temp1} = parse({temp})")
    

    def process(self, instrucction):
        typeChecker = TypeChecker()
        database = typeChecker.searchDatabase(self._dbActual)

        if not database:
            desc = f": Database {self._dbActual} does not exist"
            ErrorController().add(35, 'Execution', desc,
                                  self._noLine, self._noColumn)
            return

        SymbolTable().useDatabase = database
        DataWindow().consoleText('Query returned successfully: USE DATABASE')

    def __repr__(self):
        return str(vars(self))
