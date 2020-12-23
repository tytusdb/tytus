from execution.symbol.environment import *
from TypeChecker.checker import *
from TypeChecker.Database_Types import *
from execution.symbol.column import * 

class Avg(object):
    def __init__(self, id):
        self.id = id
    
    def execute(self, tabla, metadata):
        if self.id != None:
            datos = []
            for data in tabla:
                #declarar cada campo en la tabla de simbolos
                env = Environment(None)
                for index  in range(len(data)):
                    meta = metadata.columns[index]            
                    env.guardarVariable(meta.name, getPrimitivo(meta.tipo), data[index])
                datos.append(self.id.execute(env)['value'])

            promedio = sum(datos)/len(datos)            

            #AGREGANDO A LAS TUPLAS
            for data in self.tabla:
                data.append(promedio)

            #AGREGANDO A LA METADATA
            columna = Column( 'AVG('+self.id.id+')', DBType.numeric, 0, -1)
            if not any(columna.name == x.name for x in metadata.columns):
                metadata.columns.append(columna)
            return {'tabla': metadata, 'data': tabla}