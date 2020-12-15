from subprocess import check_call
from Compi2RepoAux.team21.Analisis_Ascendente.Instrucciones.expresion import *
from Compi2RepoAux.team21.Analisis_Ascendente.Instrucciones.instruccion import *
from Compi2RepoAux.team21.Analisis_Ascendente.Instrucciones.Create.createTable import CreateTable
from Compi2RepoAux.team21.Analisis_Ascendente.Instrucciones.Create.createDatabase import CreateReplace,ComplementoCR


class AST:
    def __init__(self, sentencias):
        self.contador = 0
        self.c = ""
        self.sentencias = sentencias
        self.pe = 0

    def ReportarAST(self):
        print('en clase ast')
        #print(self.sentencias)
        f = open('AST.dot', 'w')
        self.c = 'digraph G{\n' 
        self.c += 'edge [color=blue]; rankdir = TB;\n'
        self.c += 'Nodo'+ str(self.contador)+ '[label="S"]\n'
        self.contador = self.contador + 1
        self.c += 'Nodo'+ str(self.contador)+ '[label="Instrucciones"]\n' 
        self.c += 'Nodo' + '0' +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
        self.TiposInstruccion(self.sentencias, str(self.contador))
        self.c += "}\n"
        #print(arbol)
        f.write(self.c)
        f.close()
        check_call(['dot', '-Tpng', 'AST.dot', '-o', 'AST.png'])

    def TiposInstruccion(self, inst, padre):
        if inst != None:
            for i in inst:
                if isinstance(i, CreateTable):
                    self.CreateTable(i, padre)
                if isinstance(i, InsertInto):
                    self.InsertInto(i, padre)
                if isinstance(i, CreateReplace):
                    self.CreateReplace(i, padre)
                if isinstance(i, Show):
                    self.Show(padre)
                if isinstance(i, AlterDatabase):
                    self.AlterDatabase(i, padre)
                if isinstance(i, AlterTable):
                    self.AlterTable(i, padre)
                if isinstance(i, Update):
                    self.Update(i, padre)


    
    def CreateTable(self, inst, padre):
        self.contador = self.contador + 1
        self.c += 'Nodo'+ str(self.contador)+ '[label="Instruccion: CREATE TABLE"]\n' 
        self.c += 'Nodo' + padre +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
        np = str(self.contador)
        self.contador = self.contador + 1
        self.c += 'Nodo'+ str(self.contador)+ '[label="Id: ' + inst.id + '"]\n' 
        self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
        #recorrer campos
        for campo in inst.campos:
            if isinstance(campo, Campo): 
                self.contador = self.contador + 1
                self.c += 'Nodo'+ str(self.contador)+ '[label="Campo"]\n' 
                self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
                ncp = str(self.contador) 
                if campo.caso == 1:
                    self.contador = self.contador + 1
                    self.c += 'Nodo'+ str(self.contador)+ '[label="Id: ' + campo.id + '"]\n' 
                    self.c += 'Nodo' + ncp +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
                    self.contador = self.contador + 1
                    if campo.tipo.longitud != None:
                        self.c += 'Nodo'+ str(self.contador)+ '[label="Tipo: ' + campo.tipo.tipo + '(' + str(campo.tipo.longitud.valor) + ')' + '"]\n' 
                    else:
                        self.c += 'Nodo'+ str(self.contador)+ '[label="Tipo: ' + campo.tipo.tipo + '"]\n' 
                    self.c += 'Nodo' + ncp +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
                    if campo.acompaniamiento != None:
                        for acom in campo.acompaniamiento:
                            self.contador = self.contador + 1
                            a = str(self.contador)
                            if acom.tipo == 'DEFAULT':
                                self.c += 'Nodo'+ str(self.contador)+ '[label="' + acom.tipo + ': '+ str(acom.valorDefault.valor) + '"]\n' 
                            elif acom.tipo == 'UNIQUE':
                                if acom.valorDefault != None:
                                    if isinstance(acom.valorDefault, Id):
                                        self.c += 'Nodo'+ str(self.contador)+ '[label="' + acom.tipo + ': ' + acom.valorDefault.id +'"]\n' 
                                    else:    
                                        self.c += 'Nodo'+ str(self.contador)+ '[label="' + acom.tipo + '"]\n'
                                        #listaId padre self.contador 
                                        self.listaID(acom.valorDefault, str(self.contador))
                                else:    
                                    self.c += 'Nodo'+ str(self.contador)+ '[label="' + acom.tipo + '"]\n' 
                            else:    
                                self.c += 'Nodo'+ str(self.contador)+ '[label="' + acom.tipo + '"]\n' 
                            self.c += 'Nodo' + ncp +' -> ' + 'Nodo'+ a + ';\n'
                if campo.caso == 2 or campo.caso == 3:
                    if campo.caso == 2:
                        self.contador = self.contador + 1
                        self.c += 'Nodo'+ str(self.contador)+ '[label="CONSTRAINT: ' + campo.id + '"]\n' 
                        self.c += 'Nodo' + ncp +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
                    self.contador = self.contador + 1
                    a = str(self.contador)
                    if len(campo.idFk) == 1:
                        self.c += 'Nodo'+ str(self.contador)+ '[label="FOREIGN KEY: ' + campo.idFk[0].id + '"]\n' 
                    else:
                        self.c += 'Nodo'+ str(self.contador)+ '[label="FOREIGN KEY"]\n' 
                        self.listaID(campo.idFk, str(self.contador))
                    self.c += 'Nodo' + ncp +' -> ' + 'Nodo'+ a + ';\n'
                    self.contador = self.contador + 1
                    self.c += 'Nodo'+ str(self.contador)+ '[label="REFERENCES: ' + campo.tablaR + '"]\n' 
                    self.c += 'Nodo' + ncp +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
                    self.contador = self.contador + 1
                    a = str(self.contador)
                    if len(campo.idR) == 1:
                        self.c += 'Nodo'+ str(self.contador)+ '[label="Columna: ' + campo.idR[0].id + '"]\n' 
                    else:
                        self.c += 'Nodo'+ str(self.contador)+ '[label="Columnas"]\n' 
                        self.listaID(campo.idR, str(self.contador))    
                    self.c += 'Nodo' + ncp +' -> ' + 'Nodo'+ a + ';\n'                     
                if campo.caso == 4:
                    self.contador = self.contador + 1
                    a = str(self.contador)
                    #if len(campo.id) == 1:
                     #   self.c += 'Nodo'+ str(self.contador)+ '[label="PRIMARY KEY: '+ campo.id +'"]\n' 
                    #else:
                    self.c += 'Nodo'+ str(self.contador)+ '[label="PRIMARY KEY"]\n' #
                    self.listaID(campo.id, str(self.contador))#
                    self.c += 'Nodo' + ncp +' -> ' + 'Nodo'+ a + ';\n'
        if inst.idInherits != None:
            self.contador = self.contador + 1
            self.c += 'Nodo'+ str(self.contador)+ '[label="INHERITS: '+ inst.idInherits +'"]\n' 
            self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'

    def InsertInto(self, inst, padre):
        self.contador = self.contador + 1
        self.c += 'Nodo'+ str(self.contador)+ '[label="Instruccion: INSERT INTO"]\n' 
        self.c += 'Nodo' + padre +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
        np = str(self.contador)
        self.contador = self.contador + 1
        self.c += 'Nodo'+ str(self.contador)+ '[label="Id: ' + inst.id + '"]\n' 
        self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
        if inst.listaId != None:
            self.contador = self.contador + 1
            self.c += 'Nodo'+ str(self.contador)+ '[label="Columnas"]\n' 
            self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
            self.listaID(inst.listaId, str(self.contador))  
            self.contador = self.contador + 1
            self.c += 'Nodo'+ str(self.contador)+ '[label="Values"]\n' 
            self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
            a = str(self.contador)
        if len(inst.values) == 1:
            self.listaID(inst.values[0], str(self.contador))
        else:
            for val in inst.values:
                self.contador = self.contador + 1
                self.c += 'Nodo'+ str(self.contador)+ '[label="Value"]\n' 
                self.c += 'Nodo' + a +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
                self.listaID(val, str(self.contador))          

    def CreateReplace(self, inst, padre):
        label = ""
        if inst.caso == 1: 
            label = 'CREATE'
        elif inst.caso == 2:
            label = 'CREATE OR REPLACE'
        self.contador = self.contador + 1
        self.c += 'Nodo'+ str(self.contador)+ '[label="Instruccion: '+label+'"]\n' 
        self.c += 'Nodo' + padre +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
        np = str(self.contador)
        if inst.exists:
            self.contador = self.contador + 1
            self.c += 'Nodo'+ str(self.contador)+ '[label="IF NOT EXISTS"]\n' 
            self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
        self.contador = self.contador + 1
        self.c += 'Nodo'+ str(self.contador)+ '[label="' + inst.id + '"]\n' 
        self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
        if inst.complemento != None:
            if isinstance(inst.complemento, ComplementoCR):
                self.contador = self.contador + 1
                self.c += 'Nodo'+ str(self.contador)+ '[label="OWNER: ' + inst.complemento.idOwner + '"]\n' 
                self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
                if inst.complemento.mode != None:
                    self.contador = self.contador + 1
                    self.c += 'Nodo'+ str(self.contador)+ '[label="MODE: ' + str(inst.complemento.mode) + '"]\n' 
                    self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'

    def Show(self, padre):
        self.contador = self.contador + 1
        self.c += 'Nodo'+ str(self.contador)+ '[label="Instruccion: SHOW DATABASES"]\n' 
        self.c += 'Nodo' + padre +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
        
    def AlterDatabase(self, inst, padre):
        self.contador = self.contador + 1
        self.c += 'Nodo'+ str(self.contador)+ '[label="Instruccion: ALTER DATABASE"]\n' 
        self.c += 'Nodo' + padre +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
        np = str(self.contador)
        self.contador = self.contador + 1
        self.c += 'Nodo'+ str(self.contador)+ '[label="' + inst.name + '"]\n' 
        self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
        self.contador = self.contador + 1
        label = ""
        if inst.caso == 1: 
            label = 'RENAME'
        elif inst.caso == 2:
            label = 'OWNER'
        self.c += 'Nodo'+ str(self.contador)+ '[label="' + label + '"]\n' 
        self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
        self.contador = self.contador + 1
        self.c += 'Nodo'+ str(self.contador)+ '[label="' + inst.newName + '"]\n' 
        self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'

    def AlterTable(self, inst, padre):
        self.contador = self.contador + 1
        self.c += 'Nodo'+ str(self.contador)+ '[label="Instruccion: ALTER TABLE"]\n' 
        self.c += 'Nodo' + padre +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
        np = str(self.contador)
        self.contador = self.contador + 1
        self.c += 'Nodo'+ str(self.contador)+ '[label="Tabla: ' + inst.id + '"]\n' 
        self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
        #ADD
        if inst.caso == 1:
            self.contador = self.contador + 1
            self.c += 'Nodo'+ str(self.contador)+ '[label="ADD"]\n' 
            self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
            #ADD COLUMN
            if inst.idAdd != None:
                self.contador = self.contador + 1
                self.c += 'Nodo'+ str(self.contador)+ '[label="COLUMN"]\n' 
                self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
                self.contador = self.contador + 1
                self.c += 'Nodo'+ str(self.contador)+ '[label="' + inst.idAdd + '"]\n' 
                self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
                self.contador = self.contador + 1
                if inst.tipoAdd != None:
                    self.c += 'Nodo'+ str(self.contador)+ '[label="Tipo: ' + inst.tipoAdd.tipo + '(' + str(inst.tipoAdd.longitud.valor) + ')' + '"]\n' 
                else:
                    self.c += 'Nodo'+ str(self.contador)+ '[label="Tipo: ' + inst.tipoAdd.tipo + '"]\n' 
                self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
            #ADD CONSTRAINT
            if inst.constraintId != None:
                self.contador = self.contador + 1
                self.c += 'Nodo'+ str(self.contador)+ '[label="CONSTRAINT"]\n' 
                self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
                self.contador = self.contador + 1
                self.c += 'Nodo'+ str(self.contador)+ '[label="' + inst.constraintId + '"]\n' 
                self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
                self.contador = self.contador + 1
                self.c += 'Nodo'+ str(self.contador)+ '[label="UNIQUE"]\n' 
                self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
                if inst.columnId != None:
                    self.contador = self.contador + 1
                    self.c += 'Nodo'+ str(self.contador)+ '[label="' + inst.columnId + '"]\n' 
                    self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
            #ADD FOREIGN
            if inst.listaFK != None:
                self.contador = self.contador + 1
                a = str(self.contador)
                if len(inst.listaFK) == 1:
                        self.c += 'Nodo'+ str(self.contador)+ '[label="FOREIGN KEY: ' + inst.listaFK[0].id + '"]\n' 
                else:
                    self.c += 'Nodo'+ str(self.contador)+ '[label="FOREIGN KEY"]\n' 
                    self.listaID(inst.listaFK, str(self.contador))
                self.c += 'Nodo' + np +' -> ' + 'Nodo'+ a + ';\n'
                if inst.listaReferences != None:
                    self.contador = self.contador + 1
                    a = str(self.contador)
                    if len(inst.listaReferences) == 1:
                        self.c += 'Nodo'+ str(self.contador)+ '[label="REFERENCES: ' + inst.listaReferences[0].id + '"]\n' 
                    else:
                        self.c += 'Nodo'+ str(self.contador)+ '[label="REFERENCES"]\n' 
                        self.listaID(inst.listaReferences, str(self.contador))    
                    self.c += 'Nodo' + np +' -> ' + 'Nodo'+ a + ';\n'
            #ADD CHECK

        #DROP
        if inst.caso == 2:
            self.contador = self.contador + 1
            self.c += 'Nodo'+ str(self.contador)+ '[label="DROP"]\n' 
            self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
            if inst.columnConstraint != None:
                self.contador = self.contador + 1
                self.c += 'Nodo'+ str(self.contador)+ '[label="' + inst.columnConstraint + '"]\n' 
                self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
            if inst.idDrop != None:
                self.contador = self.contador + 1
                self.c += 'Nodo'+ str(self.contador)+ '[label="' + inst.idDrop + '"]\n' 
                self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
        #ALTER
        if inst.caso == 3:
            self.contador = self.contador + 1
            self.c += 'Nodo'+ str(self.contador)+ '[label="ALTER COLUMN"]\n' 
            self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
            if inst.columnAlter != None:
                self.contador = self.contador + 1
                self.c += 'Nodo'+ str(self.contador)+ '[label="' + inst.columnAlter + '"]\n' 
                self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
            self.contador = self.contador + 1
            self.c += 'Nodo'+ str(self.contador)+ '[label="SET NOT NULL"]\n' 
            self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'

    
    def Update(self, inst, padre):
        self.contador = self.contador + 1
        self.c += 'Nodo'+ str(self.contador)+ '[label="Instruccion: UPDATE"]\n' 
        self.c += 'Nodo' + padre +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
        np = str(self.contador)
        self.contador = self.contador + 1
        self.c += 'Nodo'+ str(self.contador)+ '[label="Id: ' + inst.id + '"]\n' 
        self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
        for asign in inst.asignaciones:
            print('asignar')
            if isinstance(asign, Asignacion):
                self.Asignacion(asign, np)



#---------------------LISTAS----------------------------------------
#es una lista de entero, decimal, cadena, id
    def listaID(self, inst, padre):
        for var in inst:
            if isinstance(var, Id):
                self.contador += self.contador
                self.c += 'Nodo'+ str(self.contador)+ '[label="' + var.id + '"]\n' 
                self.c += 'Nodo' + padre +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
            if isinstance(var, Primitivo):
                self.contador += self.contador
                self.c += 'Nodo'+ str(self.contador)+ '[label="' + str(var.valor) + '"]\n' 
                self.c += 'Nodo' + padre +' -> ' + 'Nodo'+ str(self.contador) + ';\n'

#EXPRESION
    def E(self, inst, padre):
        self.contador += self.contador
        self.c += 'Nodo'+ str(self.contador)+ '[label="E"]\n' 
        self.c += 'Nodo' + padre +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
        np = str(self.contador)
        eiz = False
        edr = False
        prim = False
        prim2 = False
        if isinstance(inst, Unario):
            print('unario')
            print(inst)
            print(inst.op)
            print(inst.operador)
            self.contador = self.contador + 1
            self.c += 'Nodo'+ str(self.contador) + '[label="Operador\nUnario: '+str(inst.operador)+' "]\n'
            self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
            npu = str(self.contador)
            if isinstance(inst.op, Primitivo):
                self.Primitivo(inst.op, npu)
            if isinstance(inst.op, Id):
                self.Id(inst.op.id, npu)
            if isinstance(inst.op, IdId):
                pass
            if isinstance(inst.op, Expresion):
                self.E(inst.op, npu)
        else :
            if isinstance(inst.iz, Unario):
                self.contador = self.contador + 1
                self.c += 'Nodo'+ str(self.contador) + '[label="Operador\nUnario: '+inst.iz.operador+' "]\n'
                self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
                npu = str(self.contador)
                if isinstance(inst.iz.op, Primitivo):
                    self.Primitivo(inst.iz.op, npu)
                if isinstance(inst.iz.op, Id):
                    self.Id(inst.iz.op, npu)
                if isinstance(inst.iz.op, IdId):
                    pass
                if isinstance(inst.iz.op, Expresion):
                    self.E(inst.iz.op, npu)
                self.contador += self.contador
                self.c += 'Nodo'+ str(self.contador) + '[label="Operador: ' + inst.iz.operador+'"]\n'
                self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n' 
            if isinstance(inst.dr, Unario):
                self.contador = self.contador + 1
                self.c += 'Nodo'+ str(self.contador) + '[label="Operador\nUnario: '+inst.dr.operador+' "]\n'
                self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
                npu = str(self.contador)
                if isinstance(inst.dr.op, Primitivo):
                    self.Primitivo(inst.dr.op, npu)
                if isinstance(inst.dr.op, Id):
                    self.Id(inst.dr.op, npu)
                if isinstance(inst.dr.op, IdId):
                    pass
                if isinstance(inst.dr.op, Expresion):
                    self.E(inst.dr.op, npu)
            if isinstance(inst.iz, Primitivo):
                self.contador += self.contador
                self.c += 'Nodo'+ str(self.contador) + '[label="Primitivo: ' + str(inst.iz.valor) + '"]\n'
                self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'       
                self.contador = self.contador + 1
                self.c += 'Nodo'+ str(self.contador) + '[label="Operador: ' + inst.operador+'"]\n'
                self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n' 
                prim = True 
            if isinstance(inst.dr, Primitivo):
                self.contador += self.contador
                self.c += 'Nodo'+ str(self.contador) + '[label="Primitivo: ' + str(inst.dr.valor) + '"]\n'
                self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'        
                prim2 = True
            if isinstance(inst.iz, Id):
                self.Id(inst.iz.id, np)
                self.contador = self.contador + 1
                self.c += 'Nodo'+ str(self.contador) + '[label=" Operador: ' + inst.operador+'"]\n'
                self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
                prim = True
            if isinstance(inst.dr, Id):
                self.Id(inst.dr.id, np)
                prim2 = True
            if isinstance(inst.iz, IdId):
                pass
            if isinstance(inst.dr, IdId):
                pass
            if isinstance(inst.iz, Expresion):
                print('expresion iz')
                self.E(inst.iz, np)
                self.contador += self.contador
                self.c += 'Nodo'+ str(self.contador) + '[label="Operador: ' + inst.operador+'"]\n'
                self.c += 'Nodo' + np +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
                eiz = True
            if isinstance(inst.dr, Expresion):
                self.E(inst.dr, np)
                diz = True

    def Id(self, id, padre):
        self.contador += self.contador
        self.c += 'Nodo'+ str(self.contador)+ '[label="Id: ' + id + '"]\n' 
        self.c += 'Nodo' + padre +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
            
    def Primitivo(self, prim, padre):
        self.contador += self.contador
        self.c += 'Nodo'+ str(self.contador)+ '[label="' + str(prim.valor) + '"]\n' 
        self.c += 'Nodo' + padre +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
            
    def Unario(self, unario, padre):
        self.contador += self.contador
        self.c += 'Nodo'+ str(self.contador)+ '[label="' + unario.operador + '"]\n' 
        self.c += 'Nodo' + padre +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
        a = str(self.contador)
        self.contador += self.contador
        print('UNARIO')
        #if isinstance(unario.op, Id):
         #   print(unario.op)
          #  self.c += 'Nodo'+ str(self.contador)+ '[label="' + unario.op.id + '"]\n' 
        #elif isinstance(unario.op, Primitivo):
         #   print(unario.op)
          #  self.c += 'Nodo'+ str(self.contador)+ '[label="' + str(unario.op.val) + '"]\n' 
        #elif isinstance(unario.op, IdId):
         #   pass
        # self.c += 'Nodo' + a +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
        
        #es una expresion
        self.E(unario.op, a)    
        
#ASIGNACION
    def Asignacion(self, inst, padre):
        self.contador += self.contador
        self.c += 'Nodo'+ str(self.contador)+ '[label="Asignacion"]\n' 
        self.c += 'Nodo' + padre +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
        padre = str(self.contador)
        self.contador += self.contador
        if isinstance(inst.id, Id):
            self.c += 'Nodo'+ str(self.contador)+ '[label="' + inst.id.id + '"]\n' 
        if isinstance(inst.id, IdId):
            self.c += 'Nodo'+ str(self.contador)+ '[label="' + str(inst.id.id1.id) + '.' + str(inst.id.id2.id) + '"]\n' 
        self.c += 'Nodo' + padre +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
        self.contador += self.contador
        self.c += 'Nodo'+ str(self.contador)+ '[label="="]\n' 
        self.c += 'Nodo' + padre +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
        #self.contador += self.contador
        #self.c += 'Nodo'+ str(self.contador)+ '[label="E"]\n' 
        #self.c += 'Nodo' + padre +' -> ' + 'Nodo'+ str(self.contador) + ';\n'
        self.E(inst.expresion, padre)
        