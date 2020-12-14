from enum import Enum

#aqui se van agregar los tipos de datos que tengamos que usar
class TIPO_DATO(Enum):
    INTEGER = 1
    SMALLINT = 2
    BIGINT = 3
    DECIMAL = 4
    NUMERIC = 5
    REAL = 6
    DOUBLEPRECISION = 7
    MONEY = 8
    CHARACTERVARIYING = 9
    CHARACTER = 10
    VARCHAR = 11
    CHAR = 12
    TEXT = 13
    DATE = 14
    TIME = 15
    TIMESTAMP = 16
    INTERVAL = 17
    TABLA = 18
    CAMPO = 19
    FUNCIONDEAGREGACION = 20






#La clase simbolo sera todo aquello que se desee guardar para el manejo de los datos
class Simbolo():



    def __init__(self, categoria,id, tipo, valor):
        self.categoria = categoria
        self.id = id
        self.tipo = tipo
        self.valor = valor


#Aqui se define la tabla de simbolos , cada tabla define un nuevo entorno
# es decir tablasimbolos = entorno de cada definiacion
class TablaDeSimbolos():


    def __init__(self, simbolos={}):
        self.simbolos = simbolos



    def agregar_sim(self, simbolo):
        self.simbolos[simbolo.id] = simbolo

    def buscar_sim(self, id):
        if not id in self.simbolos:
            print('Error: el identificador ', id, ' no esta definido.')

        return self.simbolos[id]

    def actualizar_sim(self, simbolo):
        if not simbolo.id in self.simbolos:
            print('Error: el identificador ', id, ' no esta definido.')
        else:
            self.simbolos[simbolo.id] = simbolo