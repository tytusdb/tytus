from Instrucciones.Declaracion import Declaracion
from Instrucciones.Sql_create.Tipo_Constraint import Tipo_Constraint, Tipo_Dato_Constraint
from Instrucciones.TablaSimbolos.Tipo import Tipo
from Instrucciones.TablaSimbolos.Instruccion import Instruccion
from Instrucciones.TablaSimbolos.Tabla import Tabla
from Instrucciones.Excepcion import Excepcion
from storageManager.jsonMode import *
from Instrucciones.Tablas.Tablas import Tablas

class CreateTable(Instruccion):
    def __init__(self, tabla, tipo, campos, herencia, linea, columna):
        Instruccion.__init__(self,tipo,linea,columna)
        self.tabla = tabla
        self.campos = campos
        self.herencia = herencia
    

    def ejecutar(self, tabla, arbol):
        super().ejecutar(tabla,arbol)
        # Ambito para la tabla
        tablaLocal = Tabla(tabla)

        #SE VALIDA QUE SE HAYA SELECCIONADO UN BD
        if arbol.bdUsar != None:
            for camp in self.campos:
                if isinstance(camp, Tipo_Constraint):
                    tc=self.campos.pop(int(self.campos.index(camp)))
                    if tc.tipo == Tipo_Dato_Constraint.UNIQUE or tc.tipo == Tipo_Dato_Constraint.PRIMARY_KEY or tc.tipo == Tipo_Dato_Constraint.FOREIGN_KEY:
                        for id in tc.expresion:
                            bid=False
                            for ct in self.campos:
                                if ct.nombre== id:
                                    if  self.campos[self.campos.index(ct)].constraint == None:
                                        self.campos[self.campos.index(ct)].constraint=[]
                                        if tc.tipo == Tipo_Dato_Constraint.UNIQUE:
                                            self.campos[self.campos.index(ct)].constraint.append(Tipo_Constraint(None, Tipo_Dato_Constraint.UNIQUE, None))
                                        if tc.tipo == Tipo_Dato_Constraint.PRIMARY_KEY:
                                            
                                            self.campos[self.campos.index(ct)].constraint.append(Tipo_Constraint(None, Tipo_Dato_Constraint.PRIMARY_KEY, None))
                                        #if tc.tipo == Tipo_Dato_Constraint.FOREIGN_KEY:
                                            #self.campos[self.campos.index(ct)].constraint.append(Tipo_Constraint(None, Tipo_Dato_Constraint.UNIQUE, None))
                                    bid=True

                            if not bid:
                                error = Excepcion("42P10","Semantico",f"La columna <<{id}>> no existe, Error en el Constraint",self.linea,self.columna)
                                arbol.excepciones.append(error)
                                arbol.consola.append(error.toString())
                                return
                    
                                
                        
            #SE VALIDA SI LA TABLA VA HEREDAR
            if self.herencia!=None:
                #SE BUSCA LA SI LA TABLA HEREDADA EXISTE
                htabla = arbol.devolverBaseDeDatos().getTabla(self.herencia)
                if htabla != None:
                    tabla_temp=[]
                    #SE RECORRE TODOS LAS COLUMNAS DE LA TABLA PARA UNIR CAMPOS REPETIDOS
                    for campo_her in htabla.lista_de_campos:
                        indice=0 
                        bandera_campo=True
                        for campo_nuevo in self.campos:
                            if campo_her.nombre==campo_nuevo.nombre:
                                tabla_temp.append(campo_nuevo)
                                arbol.consola.append(f"NOTICE: mezclando la columna <<{campo_nuevo.nombre}>> con la definición heredada.")
                                self.campos.pop(indice)
                                indice+=1
                                bandera_campo=False
                                break
                        if bandera_campo:
                            tabla_temp.append(campo_her)
                    tabla_temp = tabla_temp + self.campos
                    self.campos= tabla_temp
                else:
                    error = Excepcion(f"42P01","Semantico","No existe la relación <<{self.herencia}>>.",self.linea,self.columna)
                    arbol.excepciones.append(error)
                    arbol.consola.append(error.toString())
                    return
            # VERIFICACIÓN LLAVES PRIMARIAS
            listaPrimarias = []
            for camp in self.campos:
                if isinstance(camp.tipo,Tipo):
                    if camp.constraint != None:
                        for s in camp.constraint:
                            if s.tipo == Tipo_Dato_Constraint.PRIMARY_KEY:
                                listaPrimarias.append(camp)
            if len(listaPrimarias) > 1:
                error = Excepcion("42P16","Semantico","No se permiten múltiples llaves primarias para la tabla «"+self.tabla+"»",self.linea,self.columna)
                arbol.excepciones.append(error)
                arbol.consola.append(error.toString())
                return error
            
            #SE CREA UN AMBITO PARA LA TABLA
            tablaNueva = Tablas(self.tabla,None)
            #SE LLENA LA TABLA EN MEMORIA
            for camp in self.campos:
                if isinstance(camp.tipo,Tipo):
                    if camp.constraint != None:
                        for s in camp.constraint:
                            if s.tipo == Tipo_Dato_Constraint.CHECK:
                                objeto = Declaracion(camp.nombre, camp.tipo, s.expresion)
                                checkBueno = objeto.ejecutar(tablaLocal, arbol)
                                if not isinstance(checkBueno,Excepcion):
                                    #tablaNueva.agregarColumna(camp.nombre,camp.tipo.toString(),None, camp.constraint)
                                    #continue
                                    pass
                                else:
                                    #arbol.consola.append(checkBueno.toString())
                                    return
                    tablaNueva.agregarColumna(camp.nombre,camp.tipo,None, camp.constraint)
                else:
                    tablaNueva.agregarColumna(camp.nombre,camp.tipo,None, camp.constraint) 
            #SE CREA LA TABLA EN DISCO
            ctable = createTable(arbol.bdUsar,self.tabla,len(self.campos))

            if ctable==0: #CUANDO LA TABLA SE CREA CORRECTAMENTE
                arbol.consola.append(f"La Tabla: <<{self.tabla}>> se creo correctamente.")
                arbol.agregarTablaABd(tablaNueva)                  
            elif ctable==3: #CUANDO LA TABLA YA EXISTE
                error = Excepcion("100","Semantico","La Tabla ya Existe.",self.linea,self.columna)
                arbol.excepciones.append(error)
                arbol.consola.append(error.toString())
            elif ctable==2: #CUANDO POR ALGUN ERROR  NO SE CREA LA TABLA.
                error = Excepcion("100","Semantico","Error Interno.",self.linea,self.columna)
                arbol.excepciones.append(error)
                arbol.consola.append(error.toString())
            
            # SE AGREGAN LAS LLAVES PRIMARIAS A LA TABLA
            listaIndices = []
            resultado=0
            for i in listaPrimarias:
                listaIndices.append(tablaNueva.devolverColumna(i.nombre))
            if len(listaIndices) >0:
                print("SE AGREGO UN INDICE")
                resultado = alterAddPK(arbol.getBaseDatos(), self.tabla, listaIndices)
            if resultado == 1:
                error = Excepcion('XX000',"Semántico","Error interno",self.linea,self.columna)
                arbol.excepciones.append(error)
                arbol.consola.append(error.toString())
                return error
            elif resultado == 2:
                error = Excepcion('42P00',"Semántico","La base de datos "+str(arbol.getBaseDatos())+" no existe",self.linea,self.columna)
                arbol.excepciones.append(error)
                arbol.consola.append(error.toString())
                return error
            elif resultado == 3:
                error = Excepcion('42P01',"Semántico","No existe la relación "+self.tabla,self.linea,self.columna)
                arbol.excepciones.append(error)
                arbol.consola.append(error.toString())
                return error
            elif resultado == 4:
                error = Excepcion('42P16',"Semántico","No se permiten múltiples llaves primarias para la tabla «"+self.tabla+"»",self.linea,self.columna)
                arbol.excepciones.append(error)
                arbol.consola.append(error.toString())
                return error
            elif resultado == 5:
                error = Excepcion('XX002',"Semántico","Columna fuera de limites."+self.tabla,self.linea,self.columna)
                arbol.excepciones.append(error)
                arbol.consola.append(error.toString())
                return error
        else:
            error = Excepcion("100","Semantico","No ha seleccionado ninguna Base de Datos.",self.linea,self.columna)
            arbol.excepciones.append(error)
            arbol.consola.append(error.toString())


'''
instruccion = CreateTable("hola mundo",None, 1,2)

instruccion.ejecutar(None,None)
'''