import binary_file
import copy
import crud_tabla

class Tabla():
    def __init__(self,name,numberColumns):
        self.name = name
        self.numberColumns = numberColumns
        self.Tuplas  = None
        self.PK=[]
class Nodo():
    def __init__(self, name):
        self.name = name
        self.tables = []
        self.left = None
        self.right = None
        self.height = 0

class CRUD_DataBase:

    # The root is instantiated, to be used 
    # in the CRUD of the database
    def __init__(self):
        self.root = None        

    # Return Values
    # 0 Success Operation
    # 1 Operation Error
    # 2 Existing Database
    # @ Hay que recordar de cambiar el casteo del name y tmp.name
    def createDatabase(self, database):
        r_value = 0
        try:
            self.root = binary_file.rollback("databases")
            verificar_bdexistente = self.searchDatabase(database)
            if verificar_bdexistente is None:
                r_value = self._createDatabase(database, self.root)
            else:
                r_value = 2
        except FileNotFoundError:
            r_value = self._createDatabase(database, self.root)
        finally:
            if r_value not in [1, 2]:
                binary_file.commit(r_value, "databases")
                r_value = 0    
        return r_value
    
    def _createDatabase(self, name, tmp):
        
        try:
            if tmp is None:
                return Nodo(name)
            elif name > tmp.name:
                
                tmp.right = self._createDatabase(name, tmp.right)

                # Se verifica que no haya error en el nodo
                if tmp.right == 1:
                    tmp = 1
                else:
                    if (self.height(tmp.right) - self.height(tmp.left)) == 2:
                        if name > tmp.right.name:                    
                            tmp = self.srr(tmp)
                        else:
                            tmp = self.drr(tmp)
            else:
                tmp.left = self._createDatabase(name, tmp.left)

                # Se verifica que no haya error en el nodo
                if tmp.left == 1:
                    tmp = 1
                else:
                    if (self.height(tmp.left) - self.height(tmp.right)) == 2:
                        if name < tmp.left.name:
                            tmp = self.srl(tmp)
                        else:
                            tmp = self.drl(tmp)

            # Se verifica que no haya error en el nodo
            if tmp != 1:
                tmp.height = self.max_index(self.height(tmp.right), self.height(tmp.left)) + 1
            return tmp
        except:
            return 1

    def searchDatabase(self, name):
        self.root = binary_file.rollback("databases")
        return self._searchDatabase(name, self.root)

    def _searchDatabase(self, name, tmp):
        if tmp is None or name == tmp.name:
            return tmp
        elif name > tmp.name:
            tmp = self._searchDatabase(name, tmp.right)
        else:
            tmp = self._searchDatabase(name, tmp.left)            
        return tmp
        
    def height(self, tmp):
        if tmp != None:
            return tmp.height
        return -1

    def max_index(self, r, l):
        # st1 if condition else st2
        return (r if r>l else l)  

    # Left Left Case
    def srl(self, tmp):
        aux = tmp.left
        tmp.left = aux.right
        aux.right = tmp
        tmp.height = self.max_index(self.height(tmp.left), self.height(tmp.right)) + 1
        aux.height = self.max_index(self.height(aux.left), tmp.height) + 1
        return aux
    
    # Left Right Case
    def drl(self, tmp):
        tmp.left = self.srr(tmp.left)
        return self.srl(tmp)
    
    # Right Left Case
    def drr(self, tmp):
        tmp.right = self.srl(tmp.right)
        return self.srr(tmp)

    # Right Right Case
    def srr(self, tmp):
        aux = tmp.right
        tmp.right = aux.left
        aux.left = tmp
        tmp.height = self.max_index(self.height(tmp.left), self.height(tmp.right)) + 1
        aux.height = self.max_index(self.height(aux.left), tmp.height) + 1
        return aux
    
    # The ordering is in postorder
    def showDatabases(self):
        r_list = []
        try:
            tmp = binary_file.rollback("databases")
            self._showDatabases(tmp, r_list)
        except FileNotFoundError:
            pass
        return r_list

    def _showDatabases(self, tmp, r_list):
        if tmp:
            self._showDatabases(tmp.left, r_list)
            self._showDatabases(tmp.right, r_list)
            r_list.append(tmp.name)
    
    def r_Root(self):
        return binary_file.rollback("databases")

    # Left more Right
    def lmr (self, tmp):
        if tmp.left != None:
            valor = tmp.left
            while valor.right != None:
                valor = valor.right
            return valor
        else: 
            valor = tmp.right
            while valor.left != None:
                valor = valor.left
            return valor

    def giro(self, tmp):
        if (self.height(tmp.right) - self.height(tmp.left)) == 2:
            if tmp.right.right is not None:
                var_aux = copy.deepcopy(tmp)
                var_aux = self.srr(var_aux)
                if abs(self.height(var_aux.right) - self.height(var_aux.left)) == 2:
                    tmp = self.drr(tmp) 
                else:
                    del var_aux 
                    tmp = self.srr(tmp)
            else:
                tmp = self.drr(tmp)
        elif (self.height(tmp.right) - self.height(tmp.left)) == -2:
            if tmp.left.left is not None:
                var_aux = copy.deepcopy(tmp)
                var_aux = self.srl(var_aux)
                if abs(self.height(var_aux.right) - self.height(var_aux.left)) == 2:
                    tmp = self.drl(tmp)
                else:
                    del var_aux
                    tmp = self.srl(tmp)
            else:
                tmp = self.drl(tmp)
        tmp.height = self.max_index(self.height(tmp.right), self.height(tmp.left)) + 1
        return tmp

    def assignTables(self, database, nodo_Nuevo):
        
        r_value = 0
        try:
            self.root = binary_file.rollback("databases")
            verificar_bdexistente = self.searchDatabase(database)
            if verificar_bdexistente is None:
                r_value = self._assignTables(database, self.root, nodo_Nuevo)
            else:
                r_value = 2
        except FileNotFoundError:
            r_value = self._assignTables(database, self.root, nodo_Nuevo)
        finally:
            if r_value not in [1, 2]:
                binary_file.commit(r_value, "databases")
                r_value = 0    
        return r_value
    
    def _assignTables(self, name, tmp, nodo_Nuevo):
        
        try:
            if tmp is None:
                return nodo_Nuevo
            elif name > tmp.name:
                
                tmp.right = self._assignTables(name, tmp.right, nodo_Nuevo)

                # Se verifica que no haya error en el nodo
                if tmp.right == 1:
                    tmp = 1
                else:
                    if (self.height(tmp.right) - self.height(tmp.left)) == 2:
                        if name > tmp.right.name:                    
                            tmp = self.srr(tmp)
                        else:
                            tmp = self.drr(tmp)
            else:
                tmp.left = self._assignTables(name, tmp.left, nodo_Nuevo)

                # Se verifica que no haya error en el nodo
                if tmp.left == 1:
                    tmp = 1
                else:
                    if (self.height(tmp.left) - self.height(tmp.right)) == 2:
                        if name < tmp.left.name:
                            tmp = self.srl(tmp)
                        else:
                            tmp = self.drl(tmp)

            # Se verifica que no haya error en el nodo
            if tmp != 1:
                tmp.height = self.max_index(self.height(tmp.right), self.height(tmp.left)) + 1
            return tmp
        except:
            return 1

    def alterDatabase(self, databaseOld, databaseNew):
        
        tmp = copy.deepcopy(self.searchDatabase(databaseOld))
        if tmp is None:
            return 2
        else:
            nombre_existente = self.searchDatabase(databaseNew)
            if nombre_existente is not None:
                return 3
            else:
                nodo_Nuevo = copy.deepcopy(tmp)
                nodo_Nuevo.right = None
                nodo_Nuevo.left = None
                nodo_Nuevo.height = 0
                nodo_Nuevo.name = databaseNew

                # Eliminamos el Nodo Anterior
                val_drop = self.dropDatabase(databaseOld)

                if val_drop == 0:
                    val_assign = self.assignTables(nodo_Nuevo.name, nodo_Nuevo)
                    return val_assign
                elif val_drop == 2:
                    return 2
                else:
                    return 1
                    # Creamos un Nuevo Nodo
                    
    def dropDatabase(self, database):
        r_value = 0
        try:
            self.root = binary_file.rollback("databases")
            verificar_bdexistente = self.searchDatabase(database)
            if verificar_bdexistente is None:
                r_value = 2
            else:
                r_value = self._dropDatabase(database, self.root)

        except FileNotFoundError:
            r_value = self._dropDatabase(database, self.root)

        finally:
            if r_value not in [1, 2]:
                binary_file.commit(r_value, "databases")
                r_value = 0

        return r_value
    
    def _dropDatabase(self, name, tmp):

        try:
            if tmp is not None:
                if name == tmp.name:
                    if tmp.left != None:
                        tmp.name = self.lmr(tmp).name
                        tmp.left = self._dropDatabase(tmp.name, tmp.left)
                        tmp = self.giro(tmp)
                    # Este right solo esta sirviendo como pass, no hay
                    # ningun comportamiento que este realice en la BD
                    elif tmp.right != None:
                        pass
                    else:
                        return None
                #-----------------------------------#
                elif name > tmp.name:
                    tmp.right = self._dropDatabase(name, tmp.right)
                    tmp = self.giro(tmp)
                    # Se verifica que no haya error en el nodo
                    if tmp.right == 1: tmp = 1
                else:
                    tmp.left = self._dropDatabase(name, tmp.left)
                    tmp = self.giro(tmp)
                    # Se verifica que no haya error en el nodo
                    if tmp.left == 1: tmp = 1
                return tmp
        except:
            return 1

    def Buscar2(self, Clave, Actual):
        if Actual != None:
            Aux = Actual.Valores
            if Clave < Aux[0][0]:
                return self.Buscar2(Clave, Actual.Hijos[0])
            elif Clave == Aux[0][0]:
                return Aux[0]
            elif Aux[1][0] != -1 and Clave > Aux[1][0]:
                return self.Buscar2(Clave, Actual.Hijos[2])
            elif Aux[1][0] != -1 and Clave == Aux[1][0]:
                return Aux[1]
            else:
                return self.Buscar2(Clave, Actual.Hijos[1])
        else:
            return None

    def Buscar(self, Clave):
        if self.Raiz == None:
            return None
        else:
            return self.Buscar2(Clave, self.Raiz)

    def alterAddPK(self,database,table,keys):
        Pk = keys
        Datos = []
        ## busqueda tabla
        temp = self.extractTable(database,table)
        ## asignacion de valores para uso posterior del ordenamiento
        Datos =  temp.Tomar_Datos()


        print(Pk)
    def extractTable(self,database,table):
        temp = self.searchDatabase(database)
        temp_2 = ""
        try:
            for n in temp.tables:
                if n.name == table:
                    temp_2 = n
                    print(n)
                    return n.numberColumns
        except:
            return 1
        return ""
      ##  for n in temp :

    def createTable(self,database,table, numberColums):
        self.root = binary_file.rollback("databases")
        table_temp = Tabla(table,numberColums)
        self._createTable(database,self.root,table_temp)
        binary_file.commit(self.root,"databases")

    def _createTable(self,name,tmp,table_temp):

        if tmp is None:
            pass
        elif name == tmp.name :

            tmp.tables.append(table_temp)

        elif name > tmp.name:
            tmp = self._createTable(name,tmp.right,table_temp)
        else:
            tmp = self._createTable(name,tmp.left,table_temp)
        return tmp
    def shownTables(self,database):
        try:
            temp = self.searchDatabase(database)
            for n in temp.tables:
                print(n.name)
            return temp.tables
        except:
            return None
    def dropTable(self,database, table):
        try:
            try:
                temp = self.searchDatabase(database)
                try:
                    self.root = binary_file.rollback("databases")
                    self._dropTable(database,self.root,table)
                    print("asd")
                    binary_file.commit(self.root,"databases")

                except:
                    return 3
            except:
                return 2

        except:
            return 1
    def _dropTable(self,name,tmp,table_temp):
        if tmp is None:
            pass
        elif name == tmp.name:
            for n in tmp.tables:
                if n.name == table_temp:
                    id =tmp.tables.index(n)
                    tmp.tables.pop(id)
                    print("encontrado")

        elif name > tmp.name:
            tmp = self._dropTable(name, tmp.right, table_temp)
        else:
            tmp = self._dropTable(name, tmp.left, table_temp)
        return tmp
    def eliminarTabla(self,tmp,table_temp,a):
        if tmp.tables[a].name ==table_temp:
            tmp.tables.pop(a)
            return a
        else:
            b = a+1
            das = self.eliminarTabla(tmp,table_temp,b)
        return b
    def extractRangeTable(self,database,table,columnNumber,lower,upper):
        Valores = []
        i = lower
        temp = self.extractTable(database,table)
        while i <= upper:
            i += 1
            Valores.append(temp[i])
        return Valores
    def insert(self,database,table,tupla):
        self.root = binary_file.rollback("databases")
        self._insert(database,table,tupla)
        binary_file.commit(self.root,"databases")
    def _insert(self,database,tmp,table,tupla):
        if tmp is None:
            pass
        elif tmp.name == database:
            self.subinsert(tmp,table,tupla)
        elif name > tmp.name:
            tmp = self._insert(name, tmp.right, table,tupla)
        else:
            tmp = self._insert(name, tmp.left, table, tupla )
        return tmp

    def subinsert(self,tmp,table,tupla):
        for n in tmp.tables:
            if n.name == table:
                id = tmp.tables.index(n)
                if tmp.tables[id].Tuplas == None:
                    tmp.tables[id].Tuplas = crud_tabla.Arbol()
                    tmp.tables[id].Tuplas.insertar_(tupla)
                else:
                    tmp.tables[id].Tuplas.insertar_(tupla)
                return tmp
