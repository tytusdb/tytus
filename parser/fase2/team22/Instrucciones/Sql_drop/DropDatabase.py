from Instrucciones.TablaSimbolos.Instruccion import Instruccion
from storageManager.jsonMode import *
from Optimizador.C3D import *
from Instrucciones.TablaSimbolos import Instruccion3D as c3d

class DropDatabase(Instruccion):
    def __init__(self, id, tipo, existe, opcion, strGram, linea, columna):
        Instruccion.__init__(self,tipo,linea,columna, strGram)
        self.id = id
        self.opcion = opcion
        self.existe = existe

        
    def ejecutar(self, tabla, arbol):
        super().ejecutar(tabla,arbol)
        bandera = False
        listaBD = showDatabases()
        for bd in listaBD:
            if bd == self.id:
                bandera = True
                break

        #LA BD se encontro
        if self.existe and bandera:
            print(f"La Base de Datos: {self.id} ha sido eliminada")
            arbol.consola.append(f"Se encontro la base de datos: {self.id} ha sido eliminada")
            dropDatabase(self.id)
            arbol.eliminarBD(self.id)
        elif self.existe and not bandera:
            arbol.consola.append(f"La Base de datos: {self.id} no existe")
        elif not self.existe and bandera:
            arbol.consola.append(f"La Base de Datos: {self.id} ha sido eliminada")
            dropDatabase(self.id)
            arbol.eliminarBD(self.id)
        elif not self.existe and not bandera:
            error = Exception("XX000", "Semantico", "Error Base de Datos no existe", self.linea, self.columna)
            arbol.excepciones.append(error)
            arbol.consola.append(error.toString())
            

    def generar3D(self, tabla, arbol):
        super().generar3D(tabla,arbol)
        code = []
        t0 = c3d.getTemporal()
        if self.existe:
            code.append(c3d.asignacionString(t0, "DROP DATABASE IF EXISTS " + self.id + ";"))
        else:
            code.append(c3d.asignacionString(t0, "DROP DATABASE " + self.id + ";"))
        code.append(c3d.asignacionTemporalStack(t0))
        code.append(c3d.aumentarP())

        return code
        
'''
instruccion = Use("hola mundo",None, 1,2)

instruccion.ejecutar(None,None)
'''