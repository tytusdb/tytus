from controllers.error_controller import ErrorController
from controllers.procedures import Procedures
from controllers.three_address_code import ThreeAddressCode
from models.instructions.shared import Instruction


class DeleteFunction(Instruction):

    def __init__(self, id, ifExists, line, column):
        self.id = id
        self.ifExists = ifExists
        self.line = line
        self.column = column
        self._tac = ''

    def __repr__(self):
        return str(vars(self))

    def process(self, environment):
        for name in self.id:
            name = name['value']
            drop = Procedures().dropProcedure(name, self.line, self.column)
            if not drop and not self.ifExists:
                desc = f": Function {name} does not exist"
                ErrorController().add(39, 'Execution', desc, self.line, self.column)

    def compile(self, environment):
        temp = ThreeAddressCode().newTemp()
        ThreeAddressCode().addCode(f"{temp} = '{self._tac}'")
        temp1 = ThreeAddressCode().newTemp()
        ThreeAddressCode().addCode(f"{temp1} = parse({temp})")
        return
