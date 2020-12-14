import BaseDatos as DB
import os

main_path = os.getcwd()+"\\data\\hash"


class ListaBaseDatos:

    def __init__(self):

        self.lista_bases_datos = []
        

    def Buscar(self, database):

        for base_datos in self.lista_bases_datos:

            if base_datos.Name == database:
                return base_datos

        else:
            return False


    def createDatabase(self, database):

        for base_datos in self.lista_bases_datos:

            if base_datos.Name == database:
                return 2

        else:

            try:
                temp_path = main_path+"\\"+database

                if not os.path.isdir(temp_path):
                    os.mkdir(temp_path)

                temp = DB.BaseDatos(database, temp_path)          
                self.lista_bases_datos.append(temp)
                    
                return 0

            except:
                return 1


    def showDatabases(self):
        
        temp_list = []

        for base_datos in self.lista_bases_datos:
            temp_list.append(base_datos.Name)

        return temp_list
        


    def alterDatabase(self, databaseOld, databaseNew):

        temp_old = self.Buscar(databaseOld)
        temp_new = self.Buscar(databaseNew)

        if temp_old:

            if not temp_new:

                try:
                    temp_old.Name = databaseNew

                    temp_path_old = main_path+"\\"+databaseOld
                    temp_path_new = main_path+"\\"+databaseNew

                    os.rename(temp_path_old, temp_path_new)

                    return 0

                except:
                    return 1

            else:
                return 3

        else:
            return 2


    def dropDatabase(self, database):

        temp = self.Buscar(database)

        if temp:

            try:
                self.lista_bases_datos.remove(temp)

                temp_path = main_path+"\\"+database

                if os.path.isdir(temp_path):
                    os.rmdir(temp_path)

                return 0
            
            except:
                return 1

        else:
            return 2

    def graficar(self):
        file = open('dbs.dot', "w")
        file.write("digraph grafica{" + os.linesep)
        file.write("rankdir=LR;" + os.linesep)
        info = "{"
        
        j = 0
        for i in self.list_table:
            if j == 0:
                info += i+ os.linesep
            else:
                info += "|"+i+ os.linesep
            j = j+1
            
        file.write('dbs[shape=record label="'+info+'}"];')
        file.write(' }' + os.linesep)
        file.close()
        os.system('dot -Tpng dbs.dot -o dbs.png')
        os.system('dbs.png')
