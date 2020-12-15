#Importacion de metodos de ejecucion
#Se utilizan archivos separados para minimizar los conflictos
from .executeSentence import executeSentence
class Execute():
    nodes = []
    errors = []
    types = {
        1: 'Entero',
        2: 'Decimal',
        3: 'Cadena',
        4: 'Variable',
        5: 'Regex'
    }
    def __init__(self, nodes):
        self.nodes = nodes
    # def __init__(self, nodes, errors):
    #     self.nodes = nodes
    #     self.errors = errors
    #Aqui va metodo principal ejecutar, al que se le enviara la raiz del AST 
    #y se encargaran de llamar el resto de metodos
    def execute(self):
        if(self.nodes is not None):
           for node in self.nodes:
               executeSentence(self,node)


#Como guardar un error
# self.errors.append(
#                         Error('Semántico', 'Ya existe una tabla con el nombre ' + nodo.id, nodo.fila, nodo.columna))
    
    
    