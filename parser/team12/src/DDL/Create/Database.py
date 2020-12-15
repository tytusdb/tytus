import json
import sys, os.path
import os

storage = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')) + '\\storageManager')
sys.path.append(storage)

from jsonMode import *



class Database():
    def __init__(self):
        self.name = None
        self.owner = None
        self.mode = None
        self.replaced = False
        self.ifNotExists = False
        self.responseCode = "0000"
        self.responseMessage = ""

    def execute(self, parent):
        for hijo in parent.hijos:
            if hijo.nombreNodo == "ORREPLACE":
                self.replaced = True
            elif hijo.nombreNodo == "IF_NOT_EXISTS":
                self.ifNotExists = True
            elif hijo.nombreNodo == "IDENTIFICADOR":
                self.name = hijo.valor.upper()
            elif hijo.nombreNodo == "OPCIONALES_CREAR_DATABASE":
                self.procesarOpcionales(hijo)
        
        if self.responseCode == "0000":
            self.addDatabase()

        return {"Code":self.responseCode,"Message":self.responseMessage}


    def procesarOpcionales(self,parent):
        for i in range(0,len(parent.hijos),2):
            if parent.hijos[i].nombreNodo == "OWNER":
                if self.owner == None:
                    self.owner = parent.hijos[i+1].nombreNodo.upper()
                else:
                    self.responseCode = "42601"
                    self.responseMessage = "Ya se declaró el OWNER anteriormente"
                    return False
            elif parent.hijos[i].nombreNodo == "MODE":
                if self.mode == None:
                    self.mode = parent.hijos[i+1].nombreNodo
                else:
                    self.responseCode = "42601"
                    self.responseMessage = "Ya se declaró el MODE anteriormente"
                    return False
        return True
    
    def addDatabase(self):
        if self.mode == None:
            self.mode = 1
        jsonDatabase = {
            'nombre': self.name,
            'owner': self.owner,
            'mode' : self.mode,
            'tablas' : [{
                'columna' : 'COL1'
            }]
        }



        if not (self.name in showDatabases()) : # No existe la base de datos, se crea
            if createDatabase(self.name) == 0:
                self.responseCode="0000"
                self.responseMessage="Se creo la base de datos."
                databases.append(jsonDatabase)
        else:
            index = showDatabases().index(self.name) 
            if not (self.ifNotExists) and self.replaced :
                if createDatabase(self.name) == 2:
                    self.responseCode="0000"
                    self.responseMessage = "La base de datos fue reemplazada exitosamente"
            else:
                self.responseCode="42P04"
                self.responseMessage = "La base de datos "+self.name+" ya existe"