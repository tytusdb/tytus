from .storageManager import jsonMode
from .storageManager.TypeChecker import TCcreateDatabase,TCSearchDatabase,TCdropDatabase,TCgetDatabase
from .AST.error import * 

def executeDropDatabase(self,database):
    if(database.ifExistsFlag):
        res=TCSearchDatabase(database.name)
        if res==1:
            return jsonMode.dropDatabase(database.name)
        elif res==2:
            return jsonMode.dropDatabase(database.name)
        elif res==3:
            return jsonMode.dropDatabase(database.name)
        elif res==4:
            return jsonMode.dropDatabase(database.name)
        elif res==8:
            return jsonMode.dropDatabase(database.name)
        else:
            print_error("SEMANTIC ERROR","Mode between 1-5")
    else:
        res=TCSearchDatabase(database.name)
        if res==1:
            return jsonMode.dropDatabase(database.name)
        elif res==2:
            return jsonMode.dropDatabase(database.name)
        elif res==3:
            return jsonMode.dropDatabase(database.name)
        elif res==4:
            return jsonMode.dropDatabase(database.name)
        elif res==8:
            return jsonMode.dropDatabase(database.name)
        else:
            print_error("SEMANTIC ERROR","Mode between 1-5")

def executeDropTable(self,table):
    database=TCgetDatabase()
    res=TCSearchDatabase(database)
    if res==1:
        return jsonMode.dropTable(database,table.name)
    elif res==2:
        return jsonMode.dropTable(database,table.name)
    elif res==3:
        return jsonMode.dropTable(database,table.name)
    elif res==4:
        return jsonMode.dropTable(database,table.name)
    elif res==8:
        return jsonMode.dropTable(database,table.name)
    else:
        print_error("SEMANTIC ERROR","Mode between 1-5")
