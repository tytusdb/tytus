from abstract.instruccion import *
from tools.console_text import *
from tools.tabla_tipos import *
from storage import jsonMode as funciones
from error.errores import *


class create_db(instruccion):
    def __init__(self, id_db, replace_, if_exists, owner, mode, line, column, num_nodo):
        super().__init__(line, column)
        self.id_db = id_db
        self.replace_ = replace_
        self.if_exists = if_exists
        self.owner = owner
        self.mode = mode

        #Nodo AST Create DB
        self.nodo = nodo_AST('CREATE DATABASE', num_nodo)
        self.nodo.hijos.append(nodo_AST('CREATE DATABASE', num_nodo+1))        
        if replace_ != None:
            self.nodo.hijos.append(nodo_AST('OR REPLACE', num_nodo+3))
        if if_exists != None:
            self.nodo.hijos.append(nodo_AST('IF NOT EXISTS', num_nodo+4))
        self.nodo.hijos.append(nodo_AST(id_db, num_nodo+2))
        if owner != None:
            self.nodo.hijos.append(owner.nodo)
        if mode != None:
            self.nodo.hijos.append(mode.nodo)

        #Gramatica
        self.grammar_ = '<TR><TD>INSTRUCCION ::= CREATE'
        if replace_ != None:
            self.grammar_ += ' OR REPLACE'
        self.grammar_ += ' DATABASE '
        if if_exists != None:
            self.grammar_ += ' IF NOT EXISTS ' 
        self.grammar_ += id_db
        if owner != None:
            self.grammar_ += ' OWNER '
        if mode != None:
            self.grammar_ += ' MODE '
        self.grammar_ += '</TD><TD>INSTRUCCION = new create_db(ID,  REPLACE, IF_EXISTS, OWNER, MODE);</TD></TR>'

        if owner != None:
            self.grammar_ += owner.grammar_
        if mode != None:
            self.grammar_ += mode.grammar_

    def ejecutar(self):
        try:       
            crear = funciones.createDatabase(self.id_db)

            if(crear == 0):
                add_text("Base de datos creada con exito con nombre - " + self.id_db + " -")
            if(crear == 2):
                add_text("Base de datos ya existe - " + self.id_db + " -")
            else:
                add_text("Base de datos no pudo ser creada.")

        except:
            errores.append(nodo_error(self.line, self.column, 'Error en create database', 'Semántico'))