from Tipo import Tipo
from Instrucciones.Instruccion import Instruccion
from storageManager import jsonMode as DBMS
from Entorno.Entorno import Entorno
from Entorno.Simbolo import Simbolo
from Entorno.TipoSimbolo import TipoSimbolo
from Expresion.Logica import *
from Expresion.Relacional import *
from Expresion.Expresion import *
from Expresion.Terminal import *


class Insert(Instruccion):
    def __init__(self, nombre,valores=[]):
        self.nombre=nombre
        self.valores=valores

    def ejecutar(self, ent:Entorno):
        completo=self.nombre+'_'+ent.getDataBase()
        tabla:Simbolo = ent.buscarSimbolo(completo)
        if tabla != None:
            columnas=tabla.valor
            if len(self.valores)== len(columnas):
                i=0
                correcto=True
                for columna in columnas:
                    nombre=columna.nombre
                    tipo=columna.tipo
                    util=Tipo(None,None,-1,-1)
                    if util.comparetipo(tipo,self.valores[i].tipo):
                        'todo correcto'
                    else:
                        correcto=False
                        return 'Error los tipos de los valores no coinciden con la definicion de la tabla'
                    i=i+1
                terminales = []
                for val in self.valores:
                    terminales.append(val.getval(ent))
                    print("T ",terminales)

                r=DBMS.insert(ent.getDataBase(),self.nombre,terminales)
                if(r==4):
                    return 'Error al Insertar Registro Violacion de Constraint Primary Key'

                return 'Registros insertados con exito'


class InsertWhitColum(Instruccion):
    def __init__(self, nombre,namecolums=[],valores=[]):
        self.nombre=nombre
        self.valores=valores
        self.namecolums=namecolums

    def ejecutar(self, ent:Entorno):
        completo=self.nombre+'_'+ent.getDataBase()
        tabla:Simbolo = ent.buscarSimbolo(completo)
        if tabla != None:
            columnas=tabla.valor
            i=0
            contador=0
            for columna in columnas:
              
                verificarnull=tabla.valor[i].atributos.get('not null')
                verificarprimary=tabla.valor[i].atributos.get('primary')
                verificarunique=tabla.valor[i].atributos.get('unique')
                verificarcheck=tabla.valor[i].atributos.get('check')
                
                condicion1:Expresion
                condicion2:Expresion
                if(verificarcheck!=None):
                    check=ent.buscarSimbolo(verificarcheck)
                    print("Condicion:",check.valor.exp1.getval(ent),check.valor.simbolo,check.valor.exp2.getval(ent))
                    condicion1=Terminal(columna.tipo,check.valor.exp1.getval(ent))
                    condicion2=Terminal(columna.tipo,check.valor.exp2.getval(ent))
                    operador=check.valor.simbolo
                    l=0
                    for columna in columnas:
                        tipo=columna.tipo
                        if(check.valor.exp1.getval(ent)==columna.nombre):
                            k=0
                            for actual in self.namecolums:
                                if(check.valor.exp1.getval(ent)==actual.getval(ent)):
                                    condicion1=Terminal(tipo,self.valores[k].getval(ent))
                                k=k+1
                        l=l+1
                    
                    n=0
                    for columna in columnas:
                        if(check.valor.exp2.getval(ent)==columna.nombre):
                            k=0
                            for actual in self.namecolums:
                                if(check.valor.exp2.getval(ent)==actual.getval(ent)):
                                    condicion2=Terminal(columna.tipo,self.valores[k].getval(ent))
                                k=k+1
                        n=n+1
                    
                    correcto=False
                    if operador in ('>','<','>=','<=','='):
                        print(condicion1.getval(ent),operador,condicion2.getval(ent))
                        nuevaop = Relacional(condicion1,condicion2,operador);
                        if nuevaop.getval(ent):
                            correcto=True
                        else:
                            return('Registro no cumple con condicion check')

                    elif operador in ('or','and','not'):
                        nuevaop = Logica(condicion1,condicion2,operador);
                        if nuevaop.getval(ent):
                            correcto=True
                        else:
                            return('Registro no cumple con condicion Check')
                                
                  



                if(verificarnull !=None or verificarprimary!=None or verificarunique!=None):
                    contador=contador+1
                i=i+1
                
                #print("contador",contador)
            if( (len(self.valores) >= contador) and (len(self.valores) == len(self.namecolums)) and (len(self.namecolums)<=len(columnas))):
                j=0
                t=0
                correcto=True
                terminales = []
                for columna in columnas:
                    nombre=columna.nombre
                    tipo=columna.tipo
                    util=Tipo(None,None,-1,-1)
                    if(nombre==self.namecolums[j].getval(ent)):
                        #print("iguales",nombre,":",self.namecolums[j].getval(ent),"J",j,"t",t)
                        if util.comparetipo(tipo,self.valores[j].tipo):
                            'todo correcto'
                        else:
                            correcto=False
                            return 'Error los tipos de los valores no coinciden con la definicion de la tabla'
                        terminales.append(self.valores[j].getval(ent))
                        j=j+1
                    else: 
                        #print("diferentes",nombre,":",self.namecolums[j].getval(ent),"J",j,"t",t)
                        terminales.append('')
                r=DBMS.insert(ent.getDataBase(),self.nombre,terminales)
                if(r==4):
                    return 'Error al Insertar Registro Violacion de Constraint Primary Key'

                print("Insert: ",terminales)
                return 'Registro insertado exitosamente'
                #print("insertando",r)
            else:
                return str('Error Numero Parametros en tabla '+self.nombre+' Incorrectos')

        else:
            return str('Error Tabla '+self.nombre+' No Existe en la BD actual')