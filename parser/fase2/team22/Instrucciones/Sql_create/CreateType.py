from Instrucciones.TablaSimbolos.Instruccion import Instruccion
from Instrucciones.Expresiones.Primitivo import Primitivo
from Instrucciones.Expresiones.Enum import Enum
from storageManager.jsonMode import *
from Optimizador.C3D import *
from Instrucciones.TablaSimbolos import Instruccion3D as c3d

class CreateType(Instruccion):
    def __init__(self, id, tipo, listaExpre, strGram,linea, columna):
        Instruccion.__init__(self,tipo,linea,columna, strGram)
        self.valor = id
        self.listaExpre = listaExpre

    def ejecutar(self, tabla, arbol):
        super().ejecutar(tabla,arbol)
        enum1 = Enum(self.valor, None, self.linea, self.columna)
        lista = []
        if(self.listaExpre):
            #print("------VALORES------")
            for x in range(0,len(self.listaExpre)):
                #volver tipo primitivo
                if(type(self.listaExpre[x]) is Primitivo):
                    valor = self.listaExpre[x].ejecutar(tabla,arbol)
                    lista.append(valor)
                    #print(valor)
        
        #print(lista)
        enum1.listaValores = lista
        arbol.lEnum.append(enum1)
        #print(self.valor + " linea: " + str(self.linea) + " columna: " + str(self.columna))
        arbol.consola.append("Consulta devuelta correctamente.")


    def generar3D(self, tabla, arbol):
        super().generar3D(tabla,arbol)
        '''code = []
        t0 = c3d.getTemporal()
        code.append(c3d.asignacionString(t0, "CREATE TYPE " + self.valor + "AS ENUM ("))
        t1 = c3d.getTemporal()

        sizeCol = len(self.listaExpre)
        contador = 1
        for enum in self.listaExpre:
            code.append(c3d.operacion(t1, Identificador(t0), Valor("\\'" + enum + "\\'", "STRING"), OP_ARITMETICO.SUMA))
            t0 = t1
            t1 = t1 = c3d.getTemporal()
            if contador != sizeCol:
                code.append(c3d.operacion(t1, Identificador(t0), Valor("\\', \\'", "STRING"), OP_ARITMETICO.SUMA))
                t0 = t1
                t1 = t1 = c3d.getTemporal()
        code.append(c3d.operacion(t1, Identificador(t0), Valor('");"', "STRING"), OP_ARITMETICO.SUMA))
        code.append(c3d.asignacionTemporalStack(t1))
        code.append(c3d.aumentarP())'''
        
        return []
