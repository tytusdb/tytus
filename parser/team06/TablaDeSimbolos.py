from enum import Enum
import pandas as pd

class TIPO_DE_DATO(Enum) :
    NUMERO = 1
    FLOTANTE=2
    CARACTER=3
    #ir agregando los tipos faltantes para la comprobacion de tipos en las operacioens

class Simbolo() :
    'Esta clase representa un simbolo dentro de nuestra tabla de simbolos'

    def __init__(self, id, nombre, tipo, tamanoCadena, BD, tabla, obligatorio, pk, FK, referenciaTablaFK, referenciaCampoFK, unique, idUnique, check, condicionCheck, idCheck,valor,default, idConstraintFK, idConstraintPK) :
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.tamanoCadena = tamanoCadena
        self.BD = BD
        self.tabla = tabla
        self.obligatorio = obligatorio
        self.pk = pk
        self.FK = FK
        self.referenciaTablaFK = referenciaTablaFK
        self.referenciaCampoFK = referenciaCampoFK
        self.unique = unique
        self.idUnique = idUnique
        self.check = check
        self.condicionCheck = condicionCheck
        self.idCheck = idCheck
        self.valor = valor
        self.default = default
        self.idConstraintFK = idConstraintFK
        self.idConstraintPK = idConstraintPK
        


class TablaDeSimbolos() :
    'Esta clase representa la tabla de simbolos'

    def __init__(self, simbolos = {}) :
        self.simbolos = simbolos

    def agregar(self, simbolo) :
        self.simbolos[simbolo.nombre] = simbolo
    
    def obtener(self, id) :
        print("a este entra")
        if not id in self.simbolos :
            print('Error1: variable ', id, ' no definida.')
            return("no definida")
        return self.simbolos[id]
    
    def obtener2(self, nombre) :
        print("a este entra")
        if not nombre in self.simbolos :
            print('Error1: variable ', nombre, ' no definida.')
            return 0
        return self.simbolos[nombre]

    def actualizar(self, simbolo) :
        if not simbolo.nombre in self.simbolos :
            print('Error2: variable ', simbolo.nombre, ' no definida.')
        else :
            self.simbolos[simbolo.nombre] = simbolo

    def mostrar(self,var):
        print(str(var))
        for x in self.simbolos:
            print(x)


    def destruir(self,simbolo):
        print("########################### simbolos>",str(simbolo.id))
        if not simbolo.id in self.simbolos :
            print('Error3: variable ', simbolo.id, ' no definida.')
        else :
            self.simbolos[simbolo.id] = simbolo
            del self.simbolos[simbolo.id]
            print("si lo elimina")

    def destruirColumna(self,nombre,BD,tabla):
        clave = str(nombre)+str(BD)+str(tabla)
        print(clave)
        for simb in self.simbolos:
            print (simb)
            if simb == clave:
                if self.simbolos[simb].nombre == nombre and self.simbolos[simb].BD == BD and self.simbolos[simb].tabla == tabla:
                    del self.simbolos[simb]
                    return    
            #print(self.simbolos[simb].id," ",self.simbolos[simb].nombre," ",self.simbolos[simb].BD," ",self.simbolos[simb].tabla)
        print("la columna no existe")
        return 0



    def obtenerColumnas(self,tabla,BD):
        #print("EMPIEZO A BORRAR LA TABLA: ",tabla)
        print("DE MOMENTO IMPRIMIRÉ ACÁ ABAJO CUALES SON LAS COLUMNAS QUE PERTENECEN A LA TABLA")
        listaColumnas = []
        for simb in self.simbolos:
            if self.simbolos[simb].tabla == tabla and self.simbolos[simb].BD == BD:
                listaColumnas.append(self.simbolos[simb].nombre)
                #print(self.simbolos[simb].nombre)
        return listaColumnas

    def destruirTabla(self,nombre,BD):
        for simb in self.simbolos:
            if self.simbolos[simb].nombre == nombre and self.simbolos[simb].BD == BD:
                del self.simbolos[simb]
                return

        '''claveTabla = str(tabla)+str(BD)
        for simb in self.simbolos:
            if simb == claveTabla:
                del self.simbolos[simb]
                print("SE ACABARON LAS COLUMNAS DE LA TABLA: ",tabla)
                return 0 '''
    

    def destruirConstraint(self,nombre,BD,tabla):
        print("aca estoy meeeeen!")
        print(nombre)
        print(BD)
        print(tabla)
        for simb in self.simbolos:
            print("xdddx")
            if self.simbolos[simb].tabla == tabla and self.simbolos[simb].BD == BD:
                print("encontre una entrada posible")
                print(self.simbolos[simb].idConstraintFK)
                print(self.simbolos[simb].idConstraintPK)
                if self.simbolos[simb].idConstraintFK == nombre:
                    print("ENCONTRE EL CONSTRAINTFK, KEMOSION")
                    self.simbolos[simb].idConstraintFK=None
                    self.simbolos[simb].FK = 0
                    self.simbolos[simb].referenciaTablaFK=None
                    self.simbolos[simb].referenciaCampoFK=None
                elif self.simbolos[simb].idConstraintPK == nombre:
                    print("ENCONTRE EL CONSTRAINTPK, KEMOSION")
                    self.simbolos[simb].idConstraintPK=None
                    self.simbolos[simb].pk = 0
        #-------------------------------------------------------------------
        '''print("########################### simbolos>",str(simbolo.id))
        if not simbolo.id in self.simbolos :
            print('Error3: variable ', simbolo.id, ' no definida.')
        else :
            self.simbolos[simbolo.id] = simbolo
            del self.simbolos[simbolo.id]
            print("si lo elimina")'''

    #-----------------------------------------------------------------------------------------------------------------------
    def obtenerDato(self, nombre):
        print("a este entra")
        if not nombre in self.simbolos :
            print('Error1: variable ', nombre, ' no definida.')
            return("no definida")
        return self.simbolos[nombre]

    #-----------------------------------------------------------------------------------------------------------------------
    def agregarnuevTablaBD(self,simbolo):
        clave = str(simbolo.nombre)+str(simbolo.BD)
        self.simbolos[clave] = simbolo

    def validarTabla(self,nombre,BD):
        clave = str(nombre)+str(BD)
        if not clave in self.simbolos:
            return 0
        return 1

    def obtenerTablaBD(self, nombre):
        print("a este entra")
        if not nombre in self.simbolos :
            print('Error: La tabla: ', nombre, ' no definida.')
            return 0
        return self.simbolos[nombre]

    #-----------------------------------------------------------------------------------------------------------------------
    #Inicia creacion de tabla
    def agregarnuevaColumna(self,simbolo):
        clave = str(simbolo.nombre) + str(simbolo.BD) + str(simbolo.tabla)
        self.simbolos[clave] = simbolo

    def verificarcolumnaBD(self,nombre,BD,tabla):
        clave = str(nombre) + str(BD) + str(tabla)
        if not clave in self.simbolos :
            print('Error: La columna: ', nombre, ' no definida.')
            return 0
        return 1

    def verificarcolumnaBDAT(self,nombre,BD,tabla):
        clave = str(nombre) + str(BD) + str(tabla)
        if not clave in self.simbolos :
            print('Error: La tabla: ', nombre, ' no definida.')
            return 0
        return self.simbolos[clave]

    def actualizauniqueColumna(self,nombre,BD,tabla):
        clave = str(nombre) + str(BD) + str(tabla)
        for simb in self.simbolos:
            if simb == clave:
                if self.simbolos[simb].nombre == nombre and self.simbolos[simb].BD == BD and self.simbolos[simb].tabla == tabla:
                    self.simbolos[simb].unique = 1
                    print("se actualizao restriccion unique en columna")
                    return    
            #print(self.simbolos[simb].id," ",self.simbolos[simb].nombre," ",self.simbolos[simb].BD," ",self.simbolos[simb].tabla)
        print("la columna no existe")
        return 0

    def actualizauniqueColumnaAT(self,nombre,BD,tabla,idConstraint):
        clave = str(nombre) + str(BD) + str(tabla)
        print(clave)
        for simb in self.simbolos:
            if simb == clave:
                if self.simbolos[simb].nombre == nombre and self.simbolos[simb].BD == BD and self.simbolos[simb].tabla == tabla:
                    self.simbolos[simb].unique = 1
                    self.simbolos[simb].idConstraintFK = idConstraint
                    print("**********************************")
                    print(self.simbolos[simb].idConstraintFK)
                    print("**********************************")
                    print("se actualizao restriccion unique en columna")
                    return    
            #print(self.simbolos[simb].id," ",self.simbolos[simb].nombre," ",self.simbolos[simb].BD," ",self.simbolos[simb].tabla)
        print("la columna no existe")
        return 0

    def actualizarcheckColumna(self,nombre,BD,tabla,idchk,condchk):
        clave = str(nombre) + str(BD) + str(tabla)
        print(clave)
        for simb in self.simbolos:
            if simb == clave:
                if self.simbolos[simb].nombre == nombre and self.simbolos[simb].BD == BD and self.simbolos[simb].tabla == tabla:
                    self.simbolos[simb].check = 1
                    self.simbolos[simb].condCheck = condchk
                    self.simbolos[simb].idCheck = idchk
                    print("se actualizo restricion check en columna")
                    return
            #print(self.simbolos[simb].id," ",self.simbolos[simb].nombre," ",self.simbolos[simb].BD," ",self.simbolos[simb].tabla)
        print("la columna no existe")
        return 0

    def actualizapkcolumna(self,nombre,BD,tabla):
        clave = str(nombre) + str(BD) + str(tabla)
        print(clave)
        for simb in self.simbolos:
            if simb == clave:
                if self.simbolos[simb].nombre == nombre and self.simbolos[simb].BD == BD and self.simbolos[simb].tabla == tabla:
                    self.simbolos[simb].pk = 1
                    print("se actualizo restricion llave primaria en columna")
                    return
            #print(self.simbolos[simb].id," ",self.simbolos[simb].nombre," ",self.simbolos[simb].BD," ",self.simbolos[simb].tabla)
        print("la columna no existe")
        return 0


    def actualizapkcolumnaAT(self,nombre,BD,tabla,idConstraint):
        clave = str(nombre) + str(BD) + str(tabla)
        print(clave)
        for simb in self.simbolos:
            if simb == clave:
                if self.simbolos[simb].nombre == nombre and self.simbolos[simb].BD == BD and self.simbolos[simb].tabla == tabla:
                    self.simbolos[simb].pk = 1
                    self.simbolos[simb].unique = 1
                    self.simbolos[simb].obligatorio = 0
                    self.simbolos[simb].idConstraintPK = idConstraint
                    print("se actualizo restricion llave primaria en columna")
                    return
            #print(self.simbolos[simb].id," ",self.simbolos[simb].nombre," ",self.simbolos[simb].BD," ",self.simbolos[simb].tabla)
        print("la columna no existe")
        return 0


    def actualizafkcolumna(self,nombre,BD,tabla,idrefcolumna,idreftabla):
        clave = str(nombre) + str(BD) + str(tabla)
        print(clave)
        for simb in self.simbolos:
            if simb == clave:
                if self.simbolos[simb].nombre == nombre and self.simbolos[simb].BD == BD and self.simbolos[simb].tabla == tabla:
                    self.simbolos[simb].FK = 1
                    self.simbolos[simb].referenciaCampoFK = idrefcolumna
                    self.simbolos[simb].referenciaTablaFK = idreftabla
                    print("se actualizo columna como llave foranea")
                    return
            #print(self.simbolos[simb].id," ",self.simbolos[simb].nombre," ",self.simbolos[simb].BD," ",self.simbolos[simb].tabla)
        print("la columna no existe")
        return 0


    def actualizafkcolumnaAT(self,nombre,BD,tabla,idrefcolumna,idreftabla,idConstraint):
        clave = str(nombre) + str(BD) + str(tabla)
        print(clave)
        for simb in self.simbolos:
            if simb == clave:
                if self.simbolos[simb].nombre == nombre and self.simbolos[simb].BD == BD and self.simbolos[simb].tabla == tabla:
                    self.simbolos[simb].FK = 1
                    self.simbolos[simb].referenciaCampoFK = idrefcolumna
                    self.simbolos[simb].referenciaTablaFK = idreftabla
                    self.simbolos[simb].idConstraintFK = idConstraint
                    print("se actualizo columna como llave foranea")
                    return
            #print(self.simbolos[simb].id," ",self.simbolos[simb].nombre," ",self.simbolos[simb].BD," ",self.simbolos[simb].tabla)
        print("la columna no existe")
        return 0
    def numerodeColumnas(self,BD,tabla):
        cont = 0
        for simb in self.simbolos:
            if self.simbolos[simb].tabla == tabla and self.simbolos[simb].BD == BD:
                cont=cont+1
        return cont

    def numerodeDatosenColumna(self,nombre,BD,tabla):
        clave = str(nombre)+str(BD)+str(tabla)
        if self.simbolos[clave].valor == None:
            return 0
        return len(self.simbolos[clave].valor)


    def actualizandoDefaultColumna(self,nombre,BD,tabla):
        clave = str(nombre)+str(BD)+str(tabla)
        if self.simbolos[clave].valor == None:
            if self.simbolos[clave].default != None:
                self.simbolos[clave].valor = [self.simbolos[clave].default]
            else:
                self.simbolos[clave].valor = ["NULL"]
        else:
            if self.simbolos[clave].default != None:
                self.simbolos[clave].valor.append(self.simbolos[clave].defualt)
            else:
                self.simbolos[clave].valor.append("NULL")

    

    #-----------------------------------------------------------------------------------------------------------------------
    #Inicia Insert en Tabla

    #se llama cuando en el insert solo colocan los registros a ingresar a la columna
    def obtenersinNombreColumna(self,nombre,BD,id):
        for simb in self.simbolos:
            if self.simbolos[simb].tabla == nombre and self.simbolos[simb].BD == BD and self.simbolos[simb].id == id:
                return self.simbolos[simb]
        return 0
    
    #se llama cuando en insert se especifica el id de la columna
    def obtenerconNombreColumna(self,nombre,BD,tabla):
        clave = str(nombre) + str(BD) + str(tabla)
        for simb in self.simbolos:
            if simb == clave:
                if self.simbolos[simb].nombre == nombre and self.simbolos[simb].BD == BD and self.simbolos[simb].tabla == tabla:
                    return self.simbolos[simb]
        return 0

    #se utiliza para actualizar los datos en la tabla de simbolos
    def actualizarValorColumna(self,nombre,BD,tabla,dato):
        clave = str(nombre) + str(BD) + str(tabla)
        for simb in self.simbolos:
            if simb == clave:
                if self.simbolos[simb].nombre == nombre and self.simbolos[simb].BD == BD and self.simbolos[simb].tabla == tabla:
                    if self.simbolos[simb].valor == None:
                        self.simbolos[simb].valor = [dato]
                    else:
                        self.simbolos[simb].valor.append(dato)
                    print("se agrego un dato a la columna: ",nombre," en tabla: ",tabla)
                    return
            #print(self.simbolos[simb].id," ",self.simbolos[simb].nombre," ",self.simbolos[simb].BD," ",self.simbolos[simb].tabla)
        print("la columna no existe")
        return 0
    
    def columnasPrimaria(self,BD,tabla):
        listpk = []
        for simb in self.simbolos:
            if self.simbolos[simb].tabla == tabla and self.simbolos[simb].BD == BD and self.simbolos[simb].pk == 1:
                listpk.append(self.simbolos[simb].id)
        return listpk

#--------------Delete de registro
    def eliminarRegistroTabla(self,BD,tabla,posvalor):
        for simb in self.simbolos:
            if self.simbolos[simb].tabla == tabla and self.simbolos[simb].BD == BD:
                self.simbolos[simb].valor.pop(posvalor)
        return 0

    def printcontsimbolos(self):
        tm = 0
        for simb in self.simbolos:
            print("----------Columna ",tm,"----------")
            print(self.simbolos[simb].id)
            print(self.simbolos[simb].nombre)
            print(self.simbolos[simb].tipo)
            print(self.simbolos[simb].tamanoCadena)
            print(self.simbolos[simb].BD)
            print(self.simbolos[simb].tabla)
            print(self.simbolos[simb].obligatorio)
            print(self.simbolos[simb].pk)
            print(self.simbolos[simb].FK)
            print(self.simbolos[simb].referenciaTablaFK)
            print(self.simbolos[simb].referenciaCampoFK)
            print(self.simbolos[simb].unique)
            print(self.simbolos[simb].idUnique)
            print(self.simbolos[simb].check)
            print(self.simbolos[simb].condicionCheck)
            print(self.simbolos[simb].idCheck)
            print(self.simbolos[simb].valor)
            print(self.simbolos[simb].default)
            print(self.simbolos[simb].idConstraintFK)
            print(self.simbolos[simb].idConstraintPK)
            tm=tm+1
        return 0
# --------------------CREAR, ALTER USE Y DROP BD---------------------------------------------------------------------
    def agregarCrearBD(self, simbolo) :
        self.simbolos[simbolo.nombre] = simbolo
    
    def verificacionCrearBD(self, nombre) :
        for simb in self.simbolos:            
            if self.simbolos[simb].nombre == nombre and self.simbolos[simb].BD == None and self.simbolos[simb].tabla == None:
                print('Error1: base de datos ', nombre, ' ya definida.')
                return 1
        return 0 

    def verificacionUseBD(self, nombre) :
        for simb in self.simbolos:            
            if self.simbolos[simb].nombre == nombre and self.simbolos[simb].BD == None and self.simbolos[simb].tabla == None:
                print('BD ', nombre, ' existente.')
                return 1
        return 0  

    def verificacionAlterBD(self, nombre) :
        for simb in self.simbolos:            
            if self.simbolos[simb].nombre == nombre and self.simbolos[simb].BD == None and self.simbolos[simb].tabla == None:
                return 1
        return 0

    def verificacionAlterBD_2(self, nombre) :
        for simb in self.simbolos:            
            if self.simbolos[simb].nombre == nombre and self.simbolos[simb].BD == None and self.simbolos[simb].tabla == None:
                return 1
        return 0

    def actualizarAlterBD(self, old, alter) :
        for simb in self.simbolos:            
            if self.simbolos[simb].nombre == old and self.simbolos[simb].BD == None and self.simbolos[simb].tabla == None:
                print("SIMB",self.simbolos[simb])
                self.simbolos[alter] = self.simbolos.pop(simb)
                self.simbolos[alter].nombre = alter
                return 2
        return 1

    def destruirBD(self,nombre):
        for simb in self.simbolos:
            if self.simbolos[simb].nombre == nombre and self.simbolos[simb].BD == None and self.simbolos[simb].tabla == None:
                print('Se elimino ', nombre)
                self.simbolos.pop(simb)
                return 1
        return 0

    def verificacionShowBD(self) :
        bd = []
        for simb in self.simbolos:            
            if self.simbolos[simb].nombre != None and self.simbolos[simb].BD == None and self.simbolos[simb].tabla == None:                
                for simb in self.simbolos:
                    bd.append(self.simbolos[simb].nombre)      
                return bd
        return 0 



#obtiene los datos cuando se manda una tabla y todas las columnas
    def obtenerSelect1A(self, tabla, bd) :
        print("a este entra metodo")
        print("la bd: ",bd)
        if tabla=="" or bd=="": return 0
        a=""
        columnas=[]
        datos={}
        for simb in self.simbolos:   
            print(simb)         
            if self.simbolos[simb].tabla == tabla and self.simbolos[simb].BD == bd:                
                print("res: ",self.simbolos[simb].valor)
                print( simb,"  = ",self.simbolos[simb].valor)
                a+=str(simb)+"  = "+str(self.simbolos[simb].valor)+"\n"
                datos[simb]=self.simbolos[simb].valor
                #columnas.append(simb)   
        if a=="": 
            print("A va vacio")
            return 0
        else:
            print("vera si genera el dataframe")
            df=pd.DataFrame(datos)
            print(df)
            print("si termino")
            print("A es: ",a)
            return df


    #obtiene un dato cuando se mandan varias columnas de 1  tabla
    def obtenerSelect2B(self, tabla, bd, campos) :
        print("a este entra metodo")
        print("la bd: ",bd)
        print("la tabla: ",tabla)
        print("campos: ",campos)
        if tabla=="" or bd=="" or len(campos)==0: return 0
        a=""
        columnas=[]
        datos={}
        for x in range(0,len(campos)):
            for simb in self.simbolos:   
                print(simb)         
                key=str(self.simbolos[simb].nombre)+str(self.simbolos[simb].BD)+str(self.simbolos[simb].tabla)
                print("el nombre sera ====",key)
                if self.simbolos[simb].tabla == tabla and self.simbolos[simb].BD == bd and (self.simbolos[simb].nombre+self.simbolos[simb].BD+self.simbolos[simb].tabla)==campos[x]:                
                    print("res: ",self.simbolos[simb].valor)
                    print( simb,"  = ",self.simbolos[simb].valor)
                    a+=str(simb)+"  = "+str(self.simbolos[simb].valor)+"\n"
                    datos[simb]=self.simbolos[simb].valor
                    #columnas.append(simb)
        if a=="": 
            print("A va vacio")
            return 0
        else:
            print("vera si genera el dataframe")
            df=pd.DataFrame(datos)
            print(df)
            print("si termino")
            print("A es: ",a)
            return df
    
    def obtenerSelect2E(self, identificador):
        if len(identificador)==0: return "no se encontro la variable"
        a=""
        
        for x in range(0,len(identificador)):
            for simb in self.simbolos:   
                if self.simbolos[simb].nombre == identificador[x]:  
                    a+= str(self.simbolos[simb].nombre)+" = "+ str(self.simbolos[simb].valor)+"\n"

              

        if a=="": 
            print("A va vacio")
            return 0
        else:
            return a


#obtiene un dato cuando se mandan varias columnas de 1  tabla
    def obtenerSelect4(self, tabla, bd, campos) :
        print("a este entra metodo----------------------")
        print("la bd: ",bd)
        print("la tabla: ",tabla)
        print("campos: ",campos)
        if tabla=="" or bd=="" or len(campos)==0: return 0
        a=""
        columnas=[]
        datos={}
        for x in range(0,len(tabla)):
            for y in range(0,len(campos)):
                for simb in self.simbolos:   
                    print(simb)         
                    key=str(self.simbolos[simb].nombre)+str(self.simbolos[simb].BD)+str(self.simbolos[simb].tabla)
                    print("el nombre sera ====",key)
                    if self.simbolos[simb].tabla == tabla[x] and self.simbolos[simb].BD == bd and (self.simbolos[simb].nombre+self.simbolos[simb].BD+self.simbolos[simb].tabla)==campos[y]:                
                        print("res: ",self.simbolos[simb].valor)
                        print( simb,"  = ",self.simbolos[simb].valor)
                        a+=str(simb)+"  = "+str(self.simbolos[simb].valor)+"\n"
                        datos[simb]=self.simbolos[simb].valor
                        #columnas.append(simb)
        if a=="": 
            print("A va vacio")
            return 0
        else:
            print("vera si genera el dataframe")
            df=pd.DataFrame(datos)
            print(df)
            print("si termino")
            print("A es: ",a)
            return df
