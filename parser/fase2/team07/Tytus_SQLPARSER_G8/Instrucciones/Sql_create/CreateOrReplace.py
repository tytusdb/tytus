from Instrucciones.Excepcion import Excepcion
from lexico import columas
from tkinter.constants import FALSE
from Instrucciones.Sql_create.ShowDatabases import ShowDatabases
from Instrucciones.TablaSimbolos.Instruccion import *
from Instrucciones.Tablas.BaseDeDatos import BaseDeDatos
from storageManager.jsonMode import *

class CreateOrReplace(Instruccion):
    def __init__(self, base, tipo, existe, owner, mode, strGram ,linea, columna):
        Instruccion.__init__(self,tipo,linea,columna, strGram)
        self.base=base
        self.tipo=tipo
        self.existe = existe
        self.owner=owner
        self.mode=mode

    def ejecutar(self, tabla, arbol):
        super().ejecutar(tabla,arbol)
        bandera = False
        arbol.lRepDin.append(self.strGram)
        #SE OBTIENE LA LISTA DE BD
        lb=showDatabases()
        #SE RECORRE LA BD PARA VERIFICAR QUE NO EXISTA
        if self.base in lb:
            dropDatabase(self.base)
            result=createDatabase(self.base)
            if result==0:
                #CUANDO LA TABLA SE CREA CORRECTAMENTE
                arbol.consola.append(f"La Base de Datos: {self.base} fue reemplazada.")
                arbol.eliminarBD(self.base)
                nueva = BaseDeDatos(str(self.base))
                arbol.setListaBd(nueva)
            elif result==2:
                error = Excepcion("100","Semantico","Error Interno.",self.linea,self.columna)
                arbol.excepciones.append(error)
                arbol.consola.append(error.toString())
        else:
            result=createDatabase(self.base)
            if result==0:
                #CUANDO LA TABLA SE CREA CORRECTAMENTE
                arbol.consola.append(f"La Base de Datos: {self.base} se creo correctamente.")
                nueva = BaseDeDatos(str(self.base))
                arbol.setListaBd(nueva)
            elif result==2:
                error = Excepcion("100","Semantico","Error Interno.",self.linea,self.columna)
                arbol.excepciones.append(error)
                arbol.consola.append(error.toString())

        '''for bd in lb:
            if bd== self.base:
                #SI SE ENCUENTRA LA BD SE TERMINA EL RECORRIDO
                bandera = True
                break
            
        if self.existe=="IF NOT EXISTS" and bandera==True:
            arbol.consola.append(f"La Base de Datos ya existe: {self.base}.")
        elif self.existe=="IF NOT EXISTS" and bandera==False:
            arbol.consola.append(f"Se Creo la base de datos: {self.base} correctamente.")
            createDatabase(str(self.base))
            nueva = BaseDeDatos(str(self.base))
            arbol.setListaBd(nueva)
        elif self.existe=="NULL" and bandera==True:
            error = Excepcion("100","Semantico","La Base de Datos ya Existe.",self.linea,self.columna)
            arbol.excepciones.append(error)
            arbol.consola.append(error.toString())
        elif self.existe=="NULL" and bandera==False:
            #AVISOS
            arbol.consola.append(f"Se Creo la base de datos: {self.base} correctamente.")
            createDatabase(str(self.base))
            nueva = BaseDeDatos(str(self.base))
            arbol.setListaBd(nueva)
        '''

'''
instruccion = CreateOrReplace("hola mundo",None, 1,2)

instruccion.ejecutar(None,None)
'''