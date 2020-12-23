from execution.abstract.function import *
from execution.symbol.typ import *
from libraries.math_functions import trunc

class Trunc(Function):
    def __init__(self, input, row, column):
        Function.__init__(self,row,column)
        self.input = input
    
    def execute(self, environment):
        #input es una lista        
        if isinstance(self.input,list):
            respuesta = []
            for val in self.input:
                value = val.execute(environment)
                if value['typ'] != Type.INT and value['typ'] != Type.DECIMAL:
                    respuesta.append({'Error':"El valor " + value['value'] + " no es decimal o entero", 'linea':self.row,'columna':self.column })
                    continue
                result = trunc(value['value'])
                respuesta.append({'value':result, 'typ': Type.DECIMAL})
            return respuesta
        #input valor puntual
        else:
            value = self.input.execute(environment)
            if value['typ'] != Type.INT and value['typ'] != Type.DECIMAL:
                return {'Error':"El valor " + value['value'] + " no es decimal o entero", 'linea':self.row,'columna':self.column }
            return [{'value':trunc(value['value']), 'typ': Type.DECIMAL}]