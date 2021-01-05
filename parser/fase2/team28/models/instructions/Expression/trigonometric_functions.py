from models.instructions.Expression.type_enum import DATA_TYPE
from controllers.error_controller import ErrorController
from models.instructions.Expression.expression import Expression, Identifiers, PrimitiveData
from models.instructions.shared import ObjectReference
from math import *
class ExpressionsTrigonometric(Expression):
    '''
        ExpressionsTrigonometric
    '''
    def __init__(self, type_trigonometric, expression1, optional_expression2,line, column):
        self.type_trigonometric = type_trigonometric
        self.expression1 = expression1
        self.optional_expression2 = optional_expression2
        self.line = line
        self.column = column
        self.alias = f'{self.type_trigonometric}({self.expression1.alias})'
        
    def __repr__(self):
        return str(vars(self))
    def process(self, expression):
        type_trigo = self.type_trigonometric
        exp1 = None
        exp2 = None
        result = 0
        lista1 = []
        try:
            if isinstance(self.expression1, Identifiers):
                if isinstance(self.optional_expression2, PrimitiveData):
                    exp2 = self.optional_expression2.process(expression)
                    exp1 = self.expression1.process(expression)
                if type_trigo.lower() == "acos":
                    result = [acos(columns) for columns in exp1[0]]
                    lista1.append(result)
                    lista1.append(self.alias)
                    return lista1
                elif type_trigo.lower() == 'acosd':
                    result = [degrees(acos(columns)) for columns in exp1[0]]
                    lista1.append(result)
                    lista1.append(self.alias)
                    return lista1
                elif type_trigo.lower() == 'asin':
                    result = [asin(columns) for columns in exp1[0]]
                    lista1.append(result)
                    lista1.append(self.alias)
                    return lista1
                elif type_trigo.lower() == 'asind':
                    result = [degrees(asin(columns)) for columns in exp1[0]]
                    lista1.append(result)
                    lista1.append(self.alias)
                    return lista1
                elif type_trigo.lower() == 'atan':
                    result = [atan(columns) for columns in exp1[0]]
                    lista1.append(result)
                    lista1.append(self.alias)
                    return lista1
                elif type_trigo.lower() == 'atand':
                    result = [degrees(atan(columns)) for columns in exp1[0]]
                    lista1.append(result)
                    lista1.append(self.alias)
                    return lista1
                elif type_trigo.lower() == 'atan2':
                    result = [atan2(columns,exp2.value) for columns in exp1[0]]
                    lista1.append(result)
                    lista1.append(self.alias)
                    return lista1
                elif type_trigo.lower() == 'atan2d':
                    result = [degrees(atan2(columns,exp2.value)) for columns in exp1[0]]
                    lista1.append(result)
                    lista1.append(self.alias)
                    return lista1
                elif type_trigo.lower() == 'cos':
                    result = [cos(columns) for columns in exp1[0]]
                    lista1.append(result)
                    lista1.append(self.alias)
                    return lista1
                elif type_trigo.lower() == 'cosd':
                    result = [degrees(cos(columns)) for columns in exp1[0]]
                    lista1.append(result)
                    lista1.append(self.alias)
                    return lista1
                elif type_trigo.lower() == 'cot':
                    result = [(1)/(tan(columns)) for columns in exp1[0]]
                    lista1.append(result)
                    lista1.append(self.alias)
                    return lista1
                elif type_trigo.lower() == 'cotd':
                    result = [degrees((1)/(tan(columns))) for columns in exp1[0]]
                    lista1.append(result)
                    lista1.append(self.alias)
                    return lista1
                elif type_trigo.lower() == 'sin':
                    result = [sin(columns) for columns in exp1[0]]
                    lista1.append(result)
                    lista1.append(self.alias)
                    return lista1
                elif type_trigo.lower() == 'sind':
                    result = [degrees(sin(columns)) for columns in exp1[0]]
                    lista1.append(result)
                    lista1.append(self.alias)
                    return lista1
                elif type_trigo.lower() == 'tan':
                    result = [tan(columns) for columns in exp1[0]]
                    lista1.append(result)
                    lista1.append(self.alias)
                    return lista1
                elif type_trigo.lower() == 'tand':
                    result = [degrees(tan(columns)) for columns in exp1[0]]
                    lista1.append(result)
                    lista1.append(self.alias)
                    return lista1
                elif type_trigo.lower() == 'cosh':
                    result = [cosh(columns) for columns in exp1[0]]
                    lista1.append(result)
                    lista1.append(self.alias)
                    return lista1
                elif type_trigo.lower() == 'sinh':
                    result = [sinh(columns) for columns in exp1[0]]
                    lista1.append(result)
                    lista1.append(self.alias)
                    return lista1
                elif type_trigo.lower() == 'tanh':
                    result = [tanh(columns) for columns in exp1[0]]
                    lista1.append(result)
                    lista1.append(self.alias)
                    return lista1
                elif type_trigo.lower() == 'acosh':
                    result = [acosh(columns) for columns in exp1[0]]
                    lista1.append(result)
                    lista1.append(self.alias)
                    return lista1
                elif type_trigo.lower() == 'asinh':
                    result = [asinh(columns) for columns in exp1[0]]
                    lista1.append(result)
                    lista1.append(self.alias)
                    return lista1
                elif type_trigo.lower() == 'atanh':
                    result = [atanh(columns) for columns in exp1[0]]
                    lista1.append(result)
                    lista1.append(self.alias)
                    return lista1
            else:
                if isinstance(self.expression1, PrimitiveData):
                    exp1 = self.expression1.process(expression)
                if isinstance(self.optional_expression2, PrimitiveData):
                    exp2 = self.optional_expression2.process(expression)
                if type_trigo.lower() == "acos":
                    result = round(acos(float(exp1.value)), 4)
                elif type_trigo.lower() == 'acosd':
                    result = round(degrees(acos(float(exp1.value))), 4)
                elif type_trigo.lower() == 'asin':
                    result = round(asin(float(exp1.value)), 4)
                elif type_trigo.lower() == 'asind':
                    result = round(degrees(asin(float(exp1.value))), 4)
                elif type_trigo.lower() == 'atan':
                    result = round(atan(float(exp1.value)), 4)
                elif type_trigo.lower() == 'atand':
                    result = round(degrees(atan(float(exp1.value))), 4)
                elif type_trigo.lower() == 'atan2':
                    result = round(atan2(float(exp1.value), float(exp2.value)), 4)
                elif type_trigo.lower() == 'atan2d':
                    result = round(degrees(atan2(float(exp1.value), float(exp2.value))), 4)
                elif type_trigo.lower() == 'cos':
                    result = round(cos(float(exp1.value)), 4)
                elif type_trigo.lower() == 'cosd':
                    result = round(degrees(cos(float(exp1.value))), 4)
                elif type_trigo.lower() == 'cot':
                    result = round(1/(tan(float(exp1.value))), 4)
                elif type_trigo.lower() == 'cotd':
                    result = round(degrees(1/(tan(float(exp1.value)))), 4)
                elif type_trigo.lower() == 'sin':
                    result = round(sin(float(exp1.value)), 4)
                elif type_trigo.lower() == 'sind':
                    result = round(degrees(sin(float(exp1.value))), 4)
                elif type_trigo.lower() == 'tan':
                    result = round(tan(float(exp1.value)), 4)
                elif type_trigo.lower() == 'tand':
                    result = round(degrees(tan(float(exp1.value))), 4)
                elif type_trigo.lower() == 'cosh':
                    result = round(cosh(float(exp1.value)), 4)
                elif type_trigo.lower() == 'sinh':
                    result = round(sinh(float(exp1.value)), 4)
                elif type_trigo.lower() == 'tanh':
                    result = round(tanh(float(exp1.value)), 4)
                elif type_trigo.lower() == 'acosh':
                    result = round(acosh(float(exp1.value)),4)
                elif type_trigo.lower() == 'asinh':
                    result = round(asinh(float(exp1.value)),4)
                elif type_trigo.lower() == 'atanh':
                    result = round(atanh(float(exp1.value)),4)
                return PrimitiveData(DATA_TYPE.NUMBER, result, self.line, self.column)
        except:
            desc = "FATAL ERROR --- ExpressionsTrigonometric"
            ErrorController().add(34, 'Execution', desc, self.line, self.column)