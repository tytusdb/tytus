from os import environ
from sentencias import *
from storageManager import jsonMode as jBase
import TablaSimbolos as TS
import Error as Error
import re
import math
from random import random
from datetime import datetime
from datetime import date
from datetime import time
import hashlib
from prettytable import PrettyTable
from hashlib import sha256
import itertools

consola = ""
useActual = ""
listaSemanticos = []
listaConstraint = []
listaFK = []
types = {}
d1 = ""
d2 = ""

def interpretar_sentencias(arbol, tablaSimbolos):
    # jBase.dropAll()
    global consola
    for nodo in arbol:
        if isinstance(nodo, SCrearBase):
            crearBase(nodo, tablaSimbolos)
        elif isinstance(nodo, SShowBase):
            if nodo.like == False:
                bases = jBase.showDatabases()
                for base in bases:
                    consola += base + "\n"
            else:
                bases = jBase.showDatabases()
                basn = []
                for base in bases:
                    basn.append(base)
                basn2 = []
                r = re.compile(".*" + nodo.cadena + ".*")
                basn2 = list(filter(r.match, basn))

                for bas in basn2:
                    consola += bas + "\n"
        elif isinstance(nodo, SUse):
            global useActual
            useActual = nodo.id
            consola += "La base de datos '" + nodo.id + "' es ahora la seleccionada como activa\n"
        elif isinstance(nodo, SAlterBase):
            AlterDatabase(nodo, tablaSimbolos)
        elif isinstance(nodo, SDropBase):
            if nodo.exists == False:
                db = jBase.dropDatabase(nodo.id.valor)
                if db == 2:
                    listaSemanticos.append(
                        Error.ErrorS("Error Semantico", "Error la base de datos " + nodo.id.valor + " no existe"))
                elif db == 1:
                    listaSemanticos.append(Error.ErrorS(
                        "Error Semantico", "Error en la operacion."))
                else:
                    b = tablaSimbolos.eliminar(nodo.id.valor)
                    if b == True:
                        consola += "La base de datos " + nodo.id.valor + " se elimino con exito. \n"

            else:
                db = jBase.dropDatabase(nodo.id.valor)
                if db == 1:
                    listaSemanticos.append(Error.ErrorS(
                        "Error Semantico", "Error en la operacion."))
                elif db == 0:
                    b = tablaSimbolos.eliminar(nodo.id.valor)
                    if b == True:
                        consola += "La base de datos " + nodo.id.valor + " se elimino con exito. \n"
                    else:
                        consola += "Error no se pudo elminar la base " + \
                                   nodo.id.valor + " de la tabla de simbolos \n"
        elif isinstance(nodo, STypeEnum):
            my_dict = {}
            for val in nodo.lista:
                my_dict[val.valor] = val.valor
            types[nodo.id] = my_dict
        elif isinstance(nodo, SUpdateBase):
            registros = jBase.extractTable(useActual, nodo.id)
            actualizar = []

            if registros != None:

                tabla = tablaSimbolos.get(useActual).getTabla(nodo.id)
                columnas = tabla.columnas
                tupla = {"nombreC": [], "tipo": [], "valor": []}
                nombres = []
                valores = []
                tipos = []
                diccionario = {}
                primary = []
                llaves = []

                for k in columnas:
                    tupla["nombreC"].append(columnas[k].nombre)
                    tupla["tipo"].append(columnas[k].tipo)
                    nombres.append(columnas[k].nombre)
                    tipos.append(columnas[k].tipo)
                    
                i = 1
                for r in registros:

                    for c in r:
                        tupla["valor"].append(c)

                    b = Interpreta_Expresion(nodo.listaWhere,tablaSimbolos,tupla)
                    tupla["valor"].clear()

                    if b.valor:
                        actualizar.append(r)
                        llaves.append([str(i) + "|"])
                    i += 1
                bandera1 = False
                primary = tabla.get_pk_index()

                for x in range(len(actualizar)):
                                
                    for z in range(len(nombres)):

                        bandera = False
                        for y in range(len(nodo.listaSet)):

                            if nombres[z] == nodo.listaSet[y].columna:
                                diccionario[tabla.getIndex(nombres[z])] = nodo.listaSet[y].valor.valor

                                valores.append(nodo.listaSet[y].valor)
                                bandera = True
                                break

                        if not bandera:
                            if hasattr(tipos[z],'dato'):
                                valores.append(SExpresion(actualizar[x][z],retornarTipo(tipos[z].dato)))
                            else:
                                valores.append(SExpresion(actualizar[x][z],tipos[z].tipo))
                            

                    validarUpdate(valores,nombres,tablaSimbolos,tabla,diccionario,llaves[x])
                    valores.clear()
                    diccionario = {}
                                 
            else:

                listaSemanticos.append(Error.ErrorS("Error Semantico",
                                                    "Error en UPDATE, no se encontró la base de datos [%s] o la tabla [%s] especificada" % (
                                                    useActual, nodo.id)))

        elif isinstance(nodo, SDeleteBase):
            deleteBase(nodo, tablaSimbolos)
        elif isinstance(nodo, STruncateBase):
            truncatebase(nodo, tablaSimbolos)
        elif isinstance(nodo, SInsertBase):
            InsertTable(nodo, tablaSimbolos)
        elif isinstance(nodo, SShowTable):
            tablas = jBase.showTables(useActual)
            for tabla in tablas:
                consola += tabla + "\n"
        elif isinstance(nodo, SDropTable):
            bandera = True
            for fk in listaFK:
                if fk.idtlocal == nodo.id:
                    bandera = False
            if bandera:
                b = jBase.dropTable(useActual, nodo.id)
                if b == 0:
                    base = tablaSimbolos.get(useActual)
                    if base.deleteTable(nodo.id) == True:
                        consola += "La tabla " + nodo.id + " de la base " + \
                                   useActual + " se eliminó con éxito. \n"
                    else:
                        consola += "Error no se pudo eliminar la tabla " + \
                                   nodo.id + " de la tabla de simbolos \n"
                elif b == 2:
                    listaSemanticos.append(Error.ErrorS("Error Semantico",
                                                        "Error la base de datos " + useActual + " no existe, No se puede eliminar la tabla " + nodo.id))
                elif b == 3:
                    listaSemanticos.append(Error.ErrorS("Error Semantico",
                                                        "Error la tabla " + nodo.id + " no existe en la base de datos " + useActual))
                elif b == 1:
                    listaSemanticos.append(Error.ErrorS(
                        "Error Semantico", "Error en la operacion."))
            else:
                consola += "No se puede eliminar la tabla debido a que esta siendo referenciada por una llave foranea \n"
        elif isinstance(nodo, SAlterTableRenameColumn):
            AlterRenameColumn(nodo, tablaSimbolos)
        elif isinstance(nodo, SAlterRenameTable):
            AlterRenameTable(nodo, tablaSimbolos)
        elif isinstance(nodo, SAlterTableAddColumn):
            AlterAddColumn(nodo, tablaSimbolos)
        elif isinstance(nodo, SAlterTableCheck):
            AlterTableCheck(nodo, tablaSimbolos)
        elif isinstance(nodo, SAlterTableAddUnique):
            AlterTableUnique(nodo, tablaSimbolos)
        elif isinstance(nodo, SAlterTableAddFK):
            AlterTableFK(nodo, tablaSimbolos)
        elif isinstance(nodo, SAlterTable_AlterColumn):
            for col in nodo.columnas:
                if col.tipo == TipoAlterColumn.NOTNULL:
                    AlterColumnNotNull(nodo, tablaSimbolos)
                    break
                else:
                    AlterColumnCTipo(nodo, tablaSimbolos)
                    break
        elif isinstance(nodo, SAlterTableDrop):
            if nodo.tipo == TipoAlterDrop.COLUMN:
                AlterTableDropColumn(nodo, tablaSimbolos)
            else:
                AlterTableDropConstraint(nodo, tablaSimbolos)
        elif isinstance(nodo, SCrearTabla):
            crearTabla(nodo, tablaSimbolos)

        # FRANCISCO
        elif isinstance(nodo, Squeries):
            if nodo.ope == False:
                # print("Query Simple")
                if isinstance(nodo.query1, SQuery):
                    Qselect = nodo.query1.select
                    Qffrom = nodo.query1.ffrom
                    Qwhere = nodo.query1.where
                    Qgroupby = nodo.query1.groupby
                    Qhaving = nodo.query1.having
                    Qorderby = nodo.query1.orderby
                    Qlimit = nodo.query1.limit
                    base = tablaSimbolos.get(useActual)
                    pT = PrettyTable()
                    hacerConsulta(Qselect, Qffrom, Qwhere, Qgroupby, Qhaving, Qorderby, Qlimit, base, pT, False,tablaSimbolos)
                    consola += str(pT) + "\n"


            else:
                print("Query no 1")
                consulta1=[]
                consulta2=[]
                
                Qselect = nodo.query1.select
                Qffrom = nodo.query1.ffrom
                Qwhere = nodo.query1.where
                Qgroupby = nodo.query1.groupby
                Qhaving = nodo.query1.having
                Qorderby = nodo.query1.orderby
                Qlimit = nodo.query1.limit
                base = tablaSimbolos.get(useActual)
                pT = PrettyTable()
                consulta1=hacerConsulta(Qselect, Qffrom, Qwhere, Qgroupby, Qhaving, Qorderby, Qlimit, base, pT, False,tablaSimbolos)
                
                Qselect2 = nodo.query2.select
                Qffrom2 = nodo.query2.ffrom
                Qwhere2 = nodo.query2.where
                Qgroupby2 = nodo.query2.groupby
                Qhaving2 = nodo.query2.having
                Qorderby2 = nodo.query2.orderby
                Qlimit2 = nodo.query2.limit
                base2 = tablaSimbolos.get(useActual)
                pT = PrettyTable()
                consulta2=hacerConsulta(Qselect2, Qffrom2, Qwhere2, Qgroupby2, Qhaving2, Qorderby2, Qlimit2, base2, pT, False,tablaSimbolos)
                
                arrColNames = []
                arrFinal = []
                arrAux = []
                arrAux2 = []
                if nodo.ope.lower() == "union":
                    print("union")
                    n=0
                    for e in consulta1:
                        if n == 0:
                            arrColNames .append(e)
                        n+=1
                   
                    m=0
                    for e in consulta1:
                        if m != 0 :
                            for x in e :
                                if x not in arrFinal:
                                    arrFinal.append(x)
                        m+=1
                   
                    x=0
                    for e in consulta2:
                        if x != 0 :
                            for z in e :
                                if z not in arrFinal:
                                    arrFinal.append(z)
                        x+=1
                    
                    x = PrettyTable()
                    x.field_names = arrColNames[0]
                    for e in arrFinal:
                        print(e)
                        x.add_row(e)
                    consola += str(x) + "\n"

                elif nodo.ope.lower() == "intersect":
                    print("intersect")
                    n=0
                    for e in consulta1:
                        if n == 0:
                            arrColNames .append(e)
                        n+=1
                   
                    m=0
                    for e in consulta1:
                        if m != 0 :
                            for x in e :
                                if x not in arrFinal:
                                    arrFinal.append(x)
                                else :
                                    arrAux.append(x)
                        m+=1
                   
                    x=0
                    for e in consulta2:
                        if x != 0 :
                            for z in e :
                                if z not in arrFinal:
                                    arrFinal.append(z)
                                else :
                                    arrAux.append(z)
                        x+=1

                    x = PrettyTable()
                    x.field_names = arrColNames[0]
                    for e in arrAux:
                        print(e)
                        x.add_row(e)
                    consola += str(x) + "\n"
                    
                elif nodo.ope.lower() == "except":
                    print("intersect")
                    n=0
                    for e in consulta1:
                        if n == 0:
                            arrColNames .append(e)
                        n+=1
                   
                    m=0
                    for e in consulta1:
                        if m != 0 :
                            for x in e :
                                if x not in arrFinal:
                                    arrFinal.append(x)
                                else :
                                    arrAux.append(x)
                        m+=1
                   
                    x=0
                    for e in consulta2:
                        if x != 0 :
                            for z in e :
                                if z not in arrFinal:
                                    arrFinal.append(z)
                                else :
                                    arrAux.append(z)
                        x+=1

                    #no Repetidos
                    g=0
                    for e in consulta1:
                        if g != 0 :
                            for x in e :
                                if x not in arrAux:
                                    arrAux2.append(x)
                        g+=1
                   

                    x = PrettyTable()
                    x.field_names = arrColNames[0]
                    for e in arrAux2:
                        print(e)
                        x.add_row(e)
                    consola += str(x) + "\n"



    for i in listaSemanticos:
        print(i)
        consola += i.descripcion + "\n"
    return consola


def deleteBase(nodo, tablaSimbolos):
    global consola
    if nodo.listaWhere == False:
        b = jBase.truncate(useActual, nodo.id)
        if b == 0:
            consola += "Los registros de la tabla " + nodo.id + " se eliminaron exitosamente \n"
        elif b == 1:
            listaSemanticos.append(Error.ErrorS("Error semantico", "error de operacion"))
        elif b == 2:
            listaSemanticos.append(Error.ErrorS("Error semantico", "la base " + useActual + " no existe"))
        elif b == 3:
            listaSemanticos.append(Error.ErrorS("Error semantico", "la tabla " + nodo.id + " no existe"))

    else:

        registros = jBase.extractTable(useActual, nodo.id)
        actualizar = []

        if registros != None:
            tabla = tablaSimbolos.get(useActual).getTabla(nodo.id)
            columnas = tabla.columnas
            tupla = {"nombreC": [], "tipo": [], "valor": []}
            nombres = []
            valores = []
            tipos = []
            primary = []
            llaves = []

            for k in columnas:
                tupla["nombreC"].append(columnas[k].nombre)
                tupla["tipo"].append(columnas[k].tipo)
                nombres.append(columnas[k].nombre)
                tipos.append(columnas[k].tipo)

            i = 1
            for r in registros:

                for c in r:
                    tupla["valor"].append(c)

                b = Interpreta_Expresion(nodo.listaWhere, tablaSimbolos, tupla)
                tupla["valor"].clear()

                if b.valor:
                    actualizar.append(r)
                    llaves.append([str(i) + "|"])
                
                i += 1

            bandera1 = False
            primary = tabla.get_pk_index()

            for x in range(len(actualizar)):

                rs = jBase.delete(useActual, tabla.nombre, llaves[x])
                llaves.clear()

                if rs == 0:
                    consola += "La columna con PK '%s' ha sido eliminada con éxito" % str(llaves) + "\n"

                elif rs == 1:

                    listaSemanticos.append(Error.ErrorS("Error Semantico",
                                                        "Error al intentar eliminar la columna con PK '%s', Error en la operación" % (
                                                            str(llaves))))
                elif rs == 2:

                    listaSemanticos.append(Error.ErrorS("Error Semantico",
                                                        "Error al intentar eliminar la columna con PK '%s', La base de datos '%s' no ha sido hallada" % (
                                                        str(llaves), useActual)))

                elif rs == 3:

                    listaSemanticos.append(Error.ErrorS("Error Semantico",
                                                        "Error al intentar eliminar la columna con PK '%s', La tabla '%s' no ha sido hallada" % (
                                                        str(llaves), tabla.nombre)))
                elif rs == 4:

                    listaSemanticos.append(Error.ErrorS("Error Semantico",
                                                        "Error al intentar eliminar la columna con PK '%s', Llave primaria no encontrada" % (
                                                            str(llaves))))

                


def crearBase(nodo, tablaSimbolos):
    val = nodo.id.valor
    global consola
    if nodo.replace == False and nodo.exists == False:
        if nodo.owner == False and nodo.mode == False:
            if jBase.createDatabase(val) == 0:
                bd = TS.SimboloBase(val, None, None)
                tablaSimbolos.put(val, bd)
                consola += "Base de datos " + val + " creada. \n"
            else:
                consola += "Error al crear la base de datos \n"
        elif nodo.owner == False and nodo.mode != False:
            if jBase.createDatabase(val) == 0:
                bd = TS.SimboloBase(val, None, nodo.mode)
                tablaSimbolos.put(val, bd)
                consola += "Base de datos " + val + " creada. \n"
            else:
                consola += "Error al crear la base de datos \n"
        elif nodo.owner != False and nodo.mode == False:
            if jBase.createDatabase(val) == 0:
                bd = TS.SimboloBase(val, nodo.owner.valor, None)
                tablaSimbolos.put(val, bd)
                consola += "Base de datos " + val + " creada. \n"
            else:
                consola += "Error al crear la base de datos \n"
        elif nodo.owner != False and nodo.mode != False:
            if jBase.createDatabase(val) == 0:
                bd = TS.SimboloBase(val, nodo.owner.valor, nodo.mode)
                tablaSimbolos.put(val, bd)
                consola += "Base de datos " + val + " creada. \n"
            else:
                consola += "Error al crear la base de datos \n"
    elif nodo.replace != False and nodo.exists == False:
        jBase.dropDatabase(val)
        if nodo.owner == False and nodo.mode == False:
            if jBase.createDatabase(val) == 0:
                bd = TS.SimboloBase(val, None, None)
                tablaSimbolos.put(val, bd)
                consola += "Base de datos " + val + " creada. \n"
            else:
                consola += "Error al crear la base de datos \n"
        elif nodo.owner == False and nodo.mode != False:
            if jBase.createDatabase(val) == 0:
                bd = TS.SimboloBase(val, None, nodo.mode)
                tablaSimbolos.put(val, bd)
                consola += "Base de datos " + val + " creada. \n"
            else:
                consola += "Error al crear la base de datos \n"
        elif nodo.owner != False and nodo.mode == False:
            if jBase.createDatabase(val) == 0:
                bd = TS.SimboloBase(val, nodo.owner, None)
                tablaSimbolos.put(val, bd)
                consola += "Base de datos " + val + " creada. \n"
            else:
                consola += "Error al crear la base de datos \n"
        elif nodo.owner != False and nodo.mode != False:
            if jBase.createDatabase(val) == 0:
                bd = TS.SimboloBase(val, nodo.owner, nodo.mode)
                tablaSimbolos.put(val, bd)
                consola += "Base de datos " + val + " creada. \n"
            else:
                consola += "Error al crear la base de datos \n"
    elif nodo.replace == False and nodo.exists != False:
        if nodo.owner == False and nodo.mode == False:
            if jBase.createDatabase(val) == 0:
                bd = TS.SimboloBase(val, None, None)
                tablaSimbolos.put(val, bd)
                consola += "Base de datos " + val + " creada. \n"
            elif jBase.createDatabase(val) == 2:
                consola += "La base de datos " + val + " ya existe. \n"
            else:
                consola += "Error al crear la base de datos \n"
        elif nodo.owner == False and nodo.mode != False:
            if jBase.createDatabase(val) == 0:
                bd = TS.SimboloBase(val, None, nodo.mode)
                tablaSimbolos.put(val, bd)
                consola += "Base de datos " + val + " creada. \n"
            elif jBase.createDatabase(val) == 2:
                consola += "La base de datos " + val + " ya existe. \n"
            else:
                consola += "Error al crear la base de datos \n"
        elif nodo.owner != False and nodo.mode == False:
            if jBase.createDatabase(val) == 0:
                bd = TS.SimboloBase(val, nodo.owner, None)
                tablaSimbolos.put(val, bd)
                consola += "Base de datos " + val + " creada. \n"
            elif jBase.createDatabase(val) == 2:
                consola += "La base de datos " + val + " ya existe. \n"
            else:
                consola += "Error al crear la base de datos \n"
        elif nodo.owner != False and nodo.mode != False:
            if jBase.createDatabase(val) == 0:
                bd = TS.SimboloBase(val, nodo.owner, nodo.mode)
                tablaSimbolos.put(val, bd)
                consola += "Base de datos " + val + " creada. \n"
            elif jBase.createDatabase(val) == 2:
                consola += "La base de datos " + val + " ya existe. \n"
            else:
                consola += "Error al crear la base de datos \n"


def crearTabla(nodo, tablaSimbolos):
    val = nodo.id
    global useActual
    global consola
    primarykeys = []

    contador = 0
    nueva = TS.SimboloTabla(val, None)

    for col in nodo.columnas:
        pk = False
        default_ = None
        check = None
        null = True
        unique = False

        if isinstance(col, SColumna):
            if col.opcionales != None:
                for opc in col.opcionales:
                    if isinstance(opc, SOpcionales):
                        if opc.tipo == TipoOpcionales.PRIMARYKEY:
                            pk = True
                        elif opc.tipo == TipoOpcionales.DEFAULT:
                            default_ = opc.valor
                        elif opc.tipo == TipoOpcionales.CHECK:
                            if opc.id == None:
                                check = {"id": col.id + "_check",
                                    "condicion": opc.valor}
                                listaConstraint.append(
                                    TS.Constraints(useActual, val, col.id + "_check", col.id, "check"))
                            else:
                                check = {"id": opc.id,
                                    "condicion": opc.valor}
                                listaConstraint.append(
                                    TS.Constraints(useActual, val, opc.id, col.id, "check"))
                        elif opc.tipo == TipoOpcionales.NULL:
                            null = True
                        elif opc.tipo == TipoOpcionales.NOTNULL:
                            null = False
                        elif opc.tipo == TipoOpcionales.UNIQUE:
                            if opc.id == None:
                                unique = col.id + "_unique"
                                listaConstraint.append(
                                    TS.Constraints(useActual, val, col.id + "_unique", col.id, "unique"))
                            else:
                                unique = opc.id
                                listaConstraint.append(
                                    TS.Constraints(useActual, val, opc.id, col.id, "unique"))
                colnueva = TS.SimboloColumna(col.id, col.tipo, pk, None, unique, default_, null, check,
                                                len(nueva.columnas))
                if pk:
                    primarykeys.append(colnueva.index)
                nueva.crearColumna(col.id, colnueva)
                if colnueva == None:
                    listaSemanticos.append(
                        Error.ErrorS("Error Semantico", "Ya existe una columna con el nombre " + col.id))
            else:
                auxc = TS.SimboloColumna(col.id, col.tipo,pk,None,unique,default_,null,check,len(nueva.columnas))
                nueva.crearColumna(col.id, auxc)

            contador += 1

        elif isinstance(col, SColumnaUnique):
            for id in col.id:
                if nueva.modificarUnique(id.valor, True, id.valor + "_unique") == None:
                    listaSemanticos.append(
                        Error.ErrorS("Error Semantico", "No se encontró la columna con id " + id.valor))
                else:
                    listaConstraint.append(TS.Constraints(
                        useActual, val, id.valor + "_unique", id.valor, "unique"))
        elif isinstance(col, SColumnaCheck):
            print("Entró al constraint")
            condicion = col.condicion
            opIzq = condicion.opIzq
            idcol = opIzq.valor
            result = False
            if col.id == None:
                result = nueva.modificarCheck(
                    idcol, col.condicion, idcol + "_check")
                listaConstraint.append(TS.Constraints(
                    useActual, val, idcol + "_check", idcol, "check"))
            else:
                result = nueva.modificarCheck(idcol, condicion, col.id)
                listaConstraint.append(TS.Constraints(
                    useActual, val, col.id, idcol, "check"))
            if result != True:
                listaSemanticos.append(Error.ErrorS(
                    "Error Semantico", "No se encontró la columna con id " + idcol))
        elif isinstance(col, SColumnaFk):
            for i in range(len(col.idlocal)):
                idlocal = col.idlocal[i].valor
                idfk = col.idfk[i].valor
                columnafk = tablaSimbolos.getColumna(
                    useActual, col.id, idfk)
                columnalocal = nueva.getColumna(idlocal)

                if columnafk != None and columnalocal != None:
                    if columnafk.tipo.tipo == columnalocal.tipo.tipo:
                        nueva.modificarFk(idlocal, col.id, idfk)
                        if col.idconstraint != None:
                            listaConstraint.append(
                                TS.Constraints(useActual, val, col.idconstraint, columnalocal, "FK"))
                        listaFK.append(TS.llaveForanea(
                            useActual, val, col.id, idlocal, idfk))
                    else:
                        listaSemanticos.append(Error.ErrorS("Error Semantico",
                                                            "La columna %s y la columna %s no tienen el mismo tipo" % (
                                                                idlocal, idfk)))
                else:
                    listaSemanticos.append(
                        Error.ErrorS("Error Semantico", "No se encontró la columna"))

        elif isinstance(col, SColumnaPk):
            for id in col.id:
                if nueva.modificarPk(id.valor) == None:
                    listaSemanticos.append(
                        Error.ErrorS("Error Semantico", "No se encontró la columna " + id.valor))
                else:
                    primarykeys.append(nueva.getColumna(id.valor).index)

    if nodo.herencia:
        tabla_p = tablaSimbolos.get(useActual).getTabla(nodo.nodopadre)

        if tabla_p is not None:

            for llave_h in tabla_p.columnas:
                col_tmp = TS.SimboloColumna(tabla_p.columnas[llave_h].nombre,tabla_p.columnas[llave_h].tipo,tabla_p.columnas[llave_h].primary_key,tabla_p.columnas[llave_h].foreign_key,tabla_p.columnas[llave_h].unique,tabla_p.columnas[llave_h].default,tabla_p.columnas[llave_h].null,tabla_p.columnas[llave_h].check,len(nueva.columnas))
                nueva.crearColumna(llave_h, col_tmp)
                contador += 1
            nueva.padre = nodo.nodopadre

        else:
            listaSemanticos.append(
                        Error.ErrorS("Error Semantico", "La tabla [%s] especificada para la herencia no ha sido hallada." % nodo.padre))

        

    base = tablaSimbolos.get(useActual)
    base.crearTabla(val, nueva)
    tt = jBase.createTable(useActual, nodo.id, contador)
    if len(primarykeys) > 0:
        jBase.alterAddPK(useActual, val, primarykeys)
    if tt == 0:
        consola += "La tabla " + nodo.id + " se creó con éxito. \n"
    elif tt == 1:
        consola += "Error en la operación al crear la tabla " + nodo.id + "\n"
    elif tt == 2:
        consola += "La base de datos " + useActual + " no existe. \n"
    else:
        consola += "La tabla " + nodo.id + " ya existe. \n"


def AlterDatabase(nodo, tablaSimbolos):
    global consola
    if nodo.rename:
        b = jBase.alterDatabase(nodo.id.valor, nodo.idnuevo)
        if b == 0:
            base = tablaSimbolos.renameBase(nodo.id.valor, nodo.idnuevo)
            if base:
                for fk in listaFK:
                    if fk.idbase == nodo.id.valor:
                        fk.idbase = nodo.idnuevo
                for cons in listaConstraint:
                    if cons.idbase == nodo.id.valor:
                        cons.idbase = nodo.idnuevo
                consola += "La base se renombró con éxito " + nodo.idnuevo + " \n"

            else:
                consola += "Error no se pudo renombrar la base " + \
                           nodo.id.valor + " en la tabla de simbolos \n"
        elif b == 2:
            listaSemanticos.append(Error.ErrorS(
                "Error Semantico", "La base de datos " + nodo.id.valor + " no existe"))
        elif b == 3:
            listaSemanticos.append(Error.ErrorS(
                "Error Semantico", "La base de datos ya existe " + nodo.idnuevo))
        elif b == 1:
            listaSemanticos.append(Error.ErrorS(
                "Error Semantico", "Error en la operacion."))


def AlterAddColumn(nodo, tablaSimbolos):
    global consola
    global useActual
    base = tablaSimbolos.get(useActual)
    tabla = base.getTabla(nodo.idtabla)
    for col in nodo.listaColumnas:
        auxcol = TS.SimboloColumna(
            col.idcolumna, col.tipo, False, None, None, None, True, None, len(tabla.columnas))
        if tabla.crearColumna(col.idcolumna, auxcol):
            b = jBase.alterAddColumn(useActual, nodo.idtabla, col.idcolumna)
            if b == 0:
                consola += "La columna " + col.idcolumna + \
                           " se agregó a la tabla " + nodo.idtabla + " \n"
            elif b == 1:
                listaSemanticos.append(Error.ErrorS(
                    "Error Semantico", "Error en la operacion."))
            elif b == 2:
                listaSemanticos.append(Error.ErrorS(
                    "Error Semantico", "Error la base " + useActual + "no existe"))
            elif b == 3:
                listaSemanticos.append(Error.ErrorS(
                    "Error Semantico", "Error la tabla " + nodo.idtabla + "no existe"))
        else:
            consola += "Error al crear la columna " + col.idcolumna + " \n"


def AlterRenameColumn(nodo, tablaSimbolos):
    base = tablaSimbolos.get(useActual)
    tabla = base.getTabla(nodo.idtabla)
    global consola
    op = tabla.renameColumna(nodo.idcolumna, nodo.idnuevo)
    if op == 0:
        for fk in listaFK:
            if fk.idcfk == nodo.idcolumna:
                fk.idcfk = nodo.idnuevo
                tablaRF = base.getTabla(fk.idtlocal)
                columnaRF = tablaRF.getColumna(fk.idclocal)
                columnaRF.foreign_key["columna"] = nodo.idnuevo
            elif fk.idclocal == nodo.idcolumna:
                fk.idclocal = nodo.idnuevo

        for cons in listaConstraint:
            if cons.idcol == nodo.idcolumna:
                cons.idcol = nodo.idnuevo
        consola += "Se cambio el nombre de la columna " + \
                   nodo.idcolumna + " a " + nodo.idnuevo + " con exito \n"
    elif op == 1:
        listaSemanticos.append(Error.ErrorS(
            "Error Semantico", "La columna con nombre " + nodo.idnuevo + " ya existe"))
    elif op == 2:
        listaSemanticos.append(Error.ErrorS(
            "Error Semantico", "La columna con nombre " + nodo.idactual + " no existe"))


def AlterRenameTable(nodo, tablaSimbolos):
    global useActual
    global consola
    base = tablaSimbolos.get(useActual)
    op = base.renameTable(nodo.idactual, nodo.idnuevo)
    if op == 0:
        lib = jBase.alterTable(useActual, nodo.idactual, nodo.idnuevo)
        if lib == 0:
            for fk in listaFK:
                if fk.idtfk == nodo.idactual:
                    fk.idtfk = nodo.idnuevo
                    tablaRF = base.getTabla(fk.idtlocal)
                    columnaRF = tablaRF.getColumna(fk.idclocal)
                    columnaRF.foreign_key["tabla"] = nodo.idnuevo
                elif fk.idtlocal == nodo.idactual:
                    fk.idtlocal = nodo.idnuevo
            for cons in listaConstraint:
                if cons.idtabla == nodo.idactual:
                    cons.idtabla = nodo.idnuevo
            consola += "La tabla " + nodo.idactual + \
                       " se cambio a " + nodo.idnuevo + " exitosamente \n"
        elif lib == 1:
            listaSemanticos.append(Error.ErrorS(
                "Error Semantico", "Error en la operacion."))
        elif lib == 2:
            listaSemanticos.append(Error.ErrorS(
                "Error Semantico", "La base de datos " + useActual + " no existe"))
        elif lib == 3:
            listaSemanticos.append(Error.ErrorS(
                "Error Semantico", "La tabla " + nodo.idactual + " no existe"))
        elif lib == 4:
            listaSemanticos.append(Error.ErrorS(
                "Error Semantico", "La tabla " + nodo.idnuevo + " ya existe"))
    elif op == 1:
        listaSemanticos.append(Error.ErrorS(
            "Error Semantico", "La tabla con nombre " + nodo.idnuevo + " ya existe"))
    elif op == 2:
        listaSemanticos.append(Error.ErrorS(
            "Error Semantico", "La tabla con nombre " + nodo.idactual + " no existe"))


def AlterTableCheck(nodo, tablaSimbolos):
    global useActual
    base = tablaSimbolos.get(useActual)
    tabla = base.getTabla(nodo.idtabla)
    condicion = nodo.expresion
    opIzq = condicion.opIzq
    idcol = opIzq.valor
    result = False
    global consola
    if nodo.idcons == None:
        result = tabla.modificarCheck(idcol, condicion, idcol + "_check")
        listaConstraint.append(TS.Constraints(
            useActual, nodo.idtabla, idcol + "_check", idcol, "check"))
        consola += "Se agrego el check a la columna " + idcol + " exitosamente \n"
    else:
        result = tabla.modificarCheck(idcol, condicion, nodo.idcons)
        listaConstraint.append(TS.Constraints(
            useActual, nodo.idtabla, nodo.idcons, idcol, "check"))
        consola += "Se agrego el check a la columna " + idcol + " exitosamente \n"
    if result != True:
        listaSemanticos.append(Error.ErrorS(
            "Error Semantico", "No se encontró la columna con id " + idcol))


def AlterTableUnique(nodo, tablaSimbolos):
    global consola
    global useActual
    base = tablaSimbolos.get(useActual)
    tabla = base.getTabla(nodo.idtabla)
    if tabla.modificarUnique(nodo.idcolumna, True, nodo.idconstraint):
        listaConstraint.append(TS.Constraints(
            useActual, nodo.idtabla, nodo.idconstraint, nodo.idcolumna, "unique"))
        consola += "Se agrego el unique a la columna " + \
                   nodo.idcolumna + " exitosamente \n"
    else:
        listaSemanticos.append(
            Error.ErrorS("Error Semantico", "No se encontró la columna con id " + nodo.idcolumna))


def AlterTableFK(nodo, tablaSimbolos):
    global useActual
    global consola
    base = tablaSimbolos.get(useActual)
    tabla = base.getTabla(nodo.idtabla)
    for i in range(len(nodo.idlocal)):
        idlocal = nodo.idlocal[i].valor
        idfk = nodo.idfk[i].valor
        columnafk = tablaSimbolos.getColumna(useActual, nodo.idtablafk, idfk)
        columnalocal = tabla.getColumna(idlocal)
        if columnafk != None and columnalocal != None:
            if columnafk.tipo.tipo == columnalocal.tipo.tipo:
                tabla.modificarFk(idlocal, nodo.idtablafk, idfk)
                if nodo.idconstraint != None:
                    listaConstraint.append(
                        TS.Constraints(useActual, nodo.idtabla, nodo.idconstraint, columnalocal, "FK"))
                listaFK.append(TS.llaveForanea(
                    useActual, nodo.idtabla, nodo.idtablafk, idlocal, idfk))
                consola += "Se agrego la llave foranea a " + idlocal + " exitosamente \n"
            else:
                listaSemanticos.append(Error.ErrorS("Error Semantico",
                                                    "La columna %s y la columna %s no tienen el mismo tipo" % (
                                                        idlocal, idfk)))
        else:
            listaSemanticos.append(
                Error.ErrorS("Error Semantico", "No se encontró la columna"))


def AlterTableDropColumn(nodo, tablaSimbolos):
    global useActual
    global consola
    base = tablaSimbolos.get(useActual)
    tabla = base.getTabla(nodo.idtabla)
    for col in nodo.listaColumnas:
        if jBase.alterDropColumn(useActual, nodo.idtabla, tabla.getIndex(col.idcolumna)) == 0:
            if tabla.deleteColumn(col.idcolumna):
                consola += "Se eliminó con exito la columna " + col.idcolumna + "\n"
            else:
                listaSemanticos.append(Error.ErrorS(
                    "Error Semantico", "La columna " + col.idcolumna + " no existe"))


def AlterTableDropConstraint(nodo, tablaSimbolos):
    global useActual
    global consola
    base = tablaSimbolos.get(useActual)
    tabla = base.getTabla(nodo.idtabla)
    bandera = False
    for cons in listaConstraint:
        if cons.idconstraint == nodo.listaColumnas:
            bandera = True
            if cons.tipo == "unique":
                if tabla.deleteUnique(cons.idcol):
                    consola += "Se eliminó con éxito el constraint " + nodo.listaColumnas + "\n"
                else:
                    consola += "Error no se pudo eliminar el constraint " + nodo.listaColumnas + "\n"
            elif cons.tipo == "check":
                if tabla.deleteCheck(cons.idcol):
                    consola += "Se eliminó con éxito el constraint " + nodo.listaColumnas + "\n"
                else:
                    consola += "Error no se pudo eliminar el constraint " + nodo.listaColumnas + "\n"
            elif cons.tipo == "FK":
                if tabla.deleteFk(cons.idcol):
                    consola += "Se eliminó con éxito el constraint " + nodo.listaColumnas + "\n"
                else:
                    consola += "Error no se pudo eliminar el constraint " + nodo.listaColumnas + "\n"

    if bandera == False:
        listaSemanticos.append(Error.ErrorS(
            "Error Semantico", "No se encontro el constraint " + nodo.listaColumnas))


def AlterColumnNotNull(nodo, tablaSimbolos):
    global useActual
    global consola

    base = tablaSimbolos.get(useActual)
    tabla = base.getTabla(nodo.idtabla)

    for col in nodo.columnas:
        if tabla.modificarNull(col.idcolumna):
            consola += "Se cambió a not null con exito la columna " + col.idcolumna + " \n"
        else:
            listaSemanticos.append(Error.ErrorS(
                "Error Semantico", "No se encontro la columna" + col.idcolumna))


def AlterColumnCTipo(nodo, tablaSimbolos):
    global useActual
    global consola

    base = tablaSimbolos.get(useActual)
    tabla = base.getTabla(nodo.idtabla)

    for col in nodo.columnas:
        b = tabla.modificarTipo(
            col.idcolumna, col.valcambio.tipo, col.valcambio.cantidad)
        if b == 0:
            consola += "Se modificó el tipo exitosamente a la columna " + col.idcolumna + " \n"
        elif b == 1:
            listaSemanticos.append(Error.ErrorS(
                "Error Semantico", "El valor es menor al actual"))
        elif b == 2:
            listaSemanticos.append(Error.ErrorS(
                "Error Semantico", "Los tipos no coinciden"))
        elif b == 3:
            listaSemanticos.append(Error.ErrorS(
                "Error Semantico", "la columna no existe " + col.idcolumna))


def InsertTable(nodo, tablaSimbolos):
    global consola
    flag = False
    base = tablaSimbolos.get(useActual)
    if base != None:
        tabla = base.getTabla(nodo.id)
        if tabla != None:
            if nodo.listaColumnas != None:
                if len(nodo.listaColumnas) == len(nodo.listValores):

                    result = False
                    # se comprueba la cantidad de columnas y las que tienen valor null
                    b = tabla.comprobarNulas(nodo.listaColumnas)
                    if b["cod"] == 0:
                        # se validan tipos
                        for i in range(len(nodo.listaColumnas)):
                            col = tabla.getColumna(nodo.listaColumnas[i].valor)
                            val = Interpreta_Expresion(nodo.listValores[i], tablaSimbolos, tabla)
                            if hasattr(col.tipo,"valor"):
                                
                                el_tipo = types[col.tipo.valor]

                                if el_tipo is not None:
                                    
                                    if nodo.listValores[i].valor in el_tipo.keys():
                                        result = True
                                    else:
                                        result = False
                                        listaSemanticos.append(Error.ErrorS(
                                            "Error Semantico",
                                            "El valor: '%s' no ha sido definido en la colección: '%s'." % (nodo.listValores[i].valor,col.tipo.valor) ))
                                        return

                                else:
                                    listaSemanticos.append(Error.ErrorS(
                                            "Error Semantico",
                                            "Error en ENUM TYPE: la colección " + col.tipo.valor + " no ha sido definida. "))

                            else:

                                if col.tipo.tipo == TipoDato.NUMERICO:
                                    result = validarTiposNumericos(
                                        col.tipo.dato.lower(), val)
                                elif col.tipo.tipo == TipoDato.CHAR:
                                    if val.tipo == Expresion.CADENA:
                                        result = validarTiposChar(col.tipo, val)
                                    else:
                                        result = False
                                        listaSemanticos.append(Error.ErrorS(
                                            "Error Semantico",
                                            "Error de tipos: tipo " + col.tipo.dato + " columna " + col.nombre + " valor a insertar " + str(
                                                val.tipo)))
                                elif col.tipo.tipo == TipoDato.FECHA:
                                    result = validarTiposFecha(
                                        col.tipo.dato.lower(), val)
                                elif col.tipo.tipo == TipoDato.BOOLEAN:
                                    if val.tipo == Expresion.BOOLEAN or val.tipo == Expresion.NULL:
                                        result = True
                            
                            if not result:
                                listaSemanticos.append(Error.ErrorS("Error Semantico",
                                                                    "Error de tipos: tipo " + col.tipo.dato + " columna " + col.nombre + " valor a insertar " + str(
                                                                        val.tipo)))
                                flag = False
                                break
                            else:
                                bas1 = validaCheck(
                                    col, val, nodo.listaColumnas, nodo.listValores)

                                if (bas1 == 0):

                                    if validarUnique(col, val.valor, tabla):

                                        if validarPK(col, val.valor, tabla):

                                            if validarFK(col, val.valor, tabla, tablaSimbolos):

                                                flag = True

                                            else:

                                                listaSemanticos.append(Error.ErrorS(
                                                    "Error Semantico", "El valor " + str(
                                                        val.valor) + " no corresponde a ningún valor de llave foránea"))

                                        else:

                                            listaSemanticos.append(Error.ErrorS(
                                                "Error Semantico", "El valor " + str(
                                                    val.valor) + " infringe la condición de llave primaria"))

                                    else:

                                        listaSemanticos.append(Error.ErrorS(
                                            "Error Semantico",
                                            "El valor " + val.valor + " infringe la condición de columna única"))

                                elif bas1 == 1:

                                    listaSemanticos.append(Error.ErrorS(
                                        "Error Semantico",
                                        "La columna " + col.nombre + " no superó la condición CHECK"))
                                    return


                                elif bas1 == 2:
                                    flag = False
                                    listaSemanticos.append(Error.ErrorS("Error Semantico", "La columna " + col.nombre +
                                                                        " en su condición CHECK contienen un operario inexistente dentro de la tabla actual "))
                                    return

                        if flag:
                            flag = False
                            tupla = validarDefault(nodo.listaColumnas, nodo.listValores, tabla, tablaSimbolos)
                            rs = jBase.insert(useActual, tabla.nombre, tupla)

                            if rs == 0:
                                consola += "Se insertó con éxito la tupla" + str(tupla) + "\n"
                                
                                if tabla.padre is not None:

                                    tabla_padre = tablaSimbolos.get(useActual).getTabla(tabla.padre)

                                    if tabla_padre is not None:

                                        lista_de_columnas = []
                                        lista_de_valores = []

                                        for l in range(len(nodo.listaColumnas)):

                                            if nodo.listaColumnas[l].valor in tabla_padre.columnas:
                                                
                                                lista_de_columnas.append(nodo.listaColumnas[l])
                                                lista_de_valores.append(nodo.listValores[l])
                                        
                                            l += 1

                                        nuevo_insert = SInsertBase(tabla.padre,lista_de_columnas,lista_de_valores)
                                        InsertTable(nuevo_insert, tablaSimbolos)

                                    else:

                                        listaSemanticos.append(Error.ErrorS("Error Semantico", "Fallo al insertar la tupla: " + str(tupla) + ". Tabla padre no encontrada. " + str(tabla.padre) ))
                                        

                            elif rs == 1:

                                listaSemanticos.append(
                                    Error.ErrorS("Error Semantico", "Fallo al insertar la tupla: " + str(tupla)))

                            elif rs == 2:

                                listaSemanticos.append(Error.ErrorS("Error Semantico",
                                                                    "Fallo al insertar, la base de datos '%s' no existe " % useActual))

                            elif rs == 3:

                                listaSemanticos.append(Error.ErrorS("Error Semantico",
                                                                    "Fallo al insertar, la tabla '%s' no existe" % tabla.nombre))

                            elif rs == 4:

                                listaSemanticos.append(
                                    Error.ErrorS("Error Semantico", "Fallo al insertar, Llaves duplicadas"))

                            elif rs == 5:

                                listaSemanticos.append(Error.ErrorS("Error Semantico",
                                                                    "Fallo al insertar, La tupla excede el número de columnas"))


                    elif b["cod"] == 1:
                        listaSemanticos.append(Error.ErrorS(
                            "Error Semantico", "La columna "+b["col"]+" no existe en la tabla"))
                    elif b["cod"] == 2:
                        listaSemanticos.append(Error.ErrorS(
                            "Error Semantico", "La columna " + b["col"] + " no puede ser nula"))

                else:
                    listaSemanticos.append(
                        Error.ErrorS("Error Semantico", "El numero de columnas a insertar no coincide"))
            else:
                if (len(nodo.listValores) == len(tabla.columnas)):

                    result = False
                    # se comprueba la cantidad de columnas y las que tienen valor null
                    columnas = list(tabla.columnas.keys())
                    b = tabla.comprobarNulas2(columnas)
                    
                    if b["cod"]== 0:
                        # se validan tipos
                        for i in range(len(columnas)):
                            col = tabla.getColumna(columnas[i])
                            val = Interpreta_Expresion(nodo.listValores[i], tablaSimbolos, tabla)

                            if hasattr(col.tipo,"valor"):
                                
                                el_tipo = types[col.tipo.valor]

                                if el_tipo is not None:
                                    
                                    if nodo.listValores[i].valor in el_tipo.keys():
                                        result = True
                                    else:
                                        result = False
                                        listaSemanticos.append(Error.ErrorS(
                                            "Error Semantico",
                                            "El valor: '%s' no ha sido definido en la colección: '%s'." % (nodo.listValores[i].valor,col.tipo.valor) ))
                                        return

                                else:
                                    listaSemanticos.append(Error.ErrorS(
                                            "Error Semantico",
                                            "Error en ENUM TYPE: la colección " + col.tipo.valor + " no ha sido definida. "))
                            else:

                                if col.tipo.tipo == TipoDato.NUMERICO:
                                    result = validarTiposNumericos(
                                        col.tipo.dato.lower(), val)
                                elif col.tipo.tipo == TipoDato.CHAR:
                                    if val.tipo == Expresion.CADENA:
                                        result = validarTiposChar(col.tipo, val)
                                    else:
                                        result = False
                                        listaSemanticos.append(Error.ErrorS(
                                            "Error Semantico",
                                            "Error de tipos: tipo " + col.tipo.dato + " columna " + col.nombre + " valor a insertar " + str(
                                                val.tipo)))
                                elif col.tipo.tipo == TipoDato.FECHA:
                                    result = validarTiposFecha(
                                        col.tipo.dato.lower(), val)
                                elif col.tipo.tipo == TipoDato.BOOLEAN:
                                    if val.tipo == Expresion.BOOLEAN:
                                        result = True
                            if not result:
                                listaSemanticos.append(Error.ErrorS("Error Semantico",
                                                                    "Error de tipos: tipo " + str(col.tipo.tipo) + " columna " + str(col.nombre) + " valor a insertar " + str(
                                                                        val.tipo)))
                                flag = False
                                break
                            else:
                                bas1 = validaCheck(
                                    col, val, columnas, nodo.listValores)

                                if (bas1 == 0):

                                    if validarUnique(col, val.valor, tabla):

                                        if validarPK(col, val.valor, tabla):

                                            if validarFK(col, val.valor, tabla, tablaSimbolos):

                                                flag = True

                                            else:

                                                listaSemanticos.append(Error.ErrorS(
                                                    "Error Semantico", "El valor " + str(
                                                        val.valor) + " no corresponde a ningún valor de llave foránea"))

                                        else:

                                            listaSemanticos.append(Error.ErrorS(
                                                "Error Semantico", "El valor " + str(
                                                    val.valor) + " infringe la condición de llave primaria"))

                                    else:

                                        listaSemanticos.append(Error.ErrorS(
                                            "Error Semantico",
                                            "El valor " + val.valor + " infringe la condición de columna única"))

                                elif bas1 == 1:

                                    listaSemanticos.append(Error.ErrorS(
                                        "Error Semantico",
                                        "La columna " + col.nombre + " no superó la condición CHECK"))
                                    return


                                elif bas1 == 2:
                                    flag = False
                                    listaSemanticos.append(Error.ErrorS("Error Semantico", "La columna " + col.nombre +
                                                                        " en su condición CHECK contienen un operario inexistente dentro de la tabla actual "))
                                    return

                        if flag:
                            flag = False
                            tupla = validarDefault2(columnas, nodo.listValores, tabla, tablaSimbolos)
                            rs = jBase.insert(useActual, tabla.nombre, tupla)

                            if rs == 0:
                                consola += "Se insertó con éxito la tupla" + str(tupla) + "\n"

                            elif rs == 1:

                                listaSemanticos.append(
                                    Error.ErrorS("Error Semantico", "Fallo al insertar la tupla: " + str(tupla)))

                            elif rs == 2:

                                listaSemanticos.append(Error.ErrorS("Error Semantico",
                                                                    "Fallo al insertar, la base de datos '%s' no existe " % useActual))

                            elif rs == 3:

                                listaSemanticos.append(Error.ErrorS("Error Semantico",
                                                                    "Fallo al insertar, la tabla '%s' no existe" % tabla.nombre))

                            elif rs == 4:

                                listaSemanticos.append(
                                    Error.ErrorS("Error Semantico", "Fallo al insertar, Llaves duplicadas"))

                            elif rs == 5:

                                listaSemanticos.append(Error.ErrorS("Error Semantico",
                                                                    "Fallo al insertar, La tupla excede el número de columnas"))


                    elif b["cod"] == 1:
                        listaSemanticos.append(Error.ErrorS(
                            "Error Semantico", "La columna " + b["col"] + "no existe en la tabla"))
                    elif b["cod"] == 2:
                        listaSemanticos.append(Error.ErrorS(
                            "Error Semantico", "La columna " + b["col"] + " no puede ser nula"))

                else:
                    listaSemanticos.append(
                        Error.ErrorS("Error Semantico", "El numero de columnas a insertar no coincide"))

        else:
            listaSemanticos.append(
                Error.ErrorS("Error Semantico", "la base de datos " + useActual + " no ha sido encontrada"))
    else:
        listaSemanticos.append(
            Error.ErrorS("Error Semantico", "la base de datos " + useActual + " no ha sido encontrada"))


def validarUpdate(tupla, nombres, tablaSimbolos, tabla, diccionario, pk):
    result = False
    flag = False
    global consola
    # se comprueba la cantidad de columnas y las que tienen valor null
    columnas = nombres
    b = tabla.comprobarNulas2(nombres)

    if b["cod"] == 0:
        # se validan tipos
        for i in range(len(columnas)):
            col = tabla.getColumna(columnas[i])
            print("============== DENTRO DEL UPDATE ==============")
            print("============== tupla ==============")
            print(tupla[i])
            print("============== tabla ==============")
            print(tabla)
            
            val = Interpreta_Expresion(tupla[i],tablaSimbolos,tabla)
            if col.tipo.tipo == TipoDato.NUMERICO:
                result = validarTiposNumericos(
                    col.tipo.dato.lower(), val)
            elif col.tipo.tipo == TipoDato.CHAR:
                if val.tipo == Expresion.CADENA:
                    result = validarTiposChar(col.tipo, val)
                else:
                    result = False
                    listaSemanticos.append(Error.ErrorS(
                        "Error Semantico",
                        "Error de tipos: tipo " + col.tipo.dato + " columna " + col.nombre + " valor a insertar " + str(
                            val.tipo)))
            elif col.tipo.tipo == TipoDato.FECHA:
                result = validarTiposFecha(
                    col.tipo.dato.lower(), val)
            elif col.tipo.tipo == TipoDato.BOOLEAN:
                if val.tipo == Expresion.BOOLEAN:
                    result = True
            if not result:
                listaSemanticos.append(Error.ErrorS("Error Semantico",
                                                    "Error de tipos: tipo " + col.tipo.dato + " columna " + col.nombre + " valor a insertar " + str(
                                                        val.tipo)))
                break
            else:
                bas1 = validaCheck(
                    col, val, columnas, tupla)

                if (bas1 == 0):

                    if True:

                        if True:

                            if validarFK(col, val.valor, tabla, tablaSimbolos):

                                flag = True

                            else:

                                listaSemanticos.append(Error.ErrorS(
                                    "Error Semantico",
                                    "El valor " + str(val.valor) + " no corresponde a ningún valor de llave foránea"))

                        else:

                            listaSemanticos.append(Error.ErrorS(
                                "Error Semantico",
                                "El valor " + str(val.valor) + " infringe la condición de llave primaria"))

                    else:

                        listaSemanticos.append(Error.ErrorS(
                            "Error Semantico", "El valor " + val.valor + " infringe la condición de columna única"))

                elif bas1 == 1:

                    listaSemanticos.append(Error.ErrorS(
                        "Error Semantico", "La columna " + col.nombre + " no superó la condición CHECK"))
                    return False


                elif bas1 == 2:
                    flag = False
                    listaSemanticos.append(Error.ErrorS("Error Semantico", "La columna " + col.nombre +
                                                        " en su condición CHECK contienen un operario inexistente dentro de la tabla actual "))
                    return False

        if flag:
            flag = False
            tuplas = validarDefault2(columnas,tupla,tabla,tablaSimbolos)
            #print(tuplas)
            rs = jBase.update(useActual,tabla.nombre,diccionario,pk)
            #rs = jBase.insert(useActual,tabla.nombre,tuplas)

            if tabla.padre is not None:
                print(diccionario)
                tabla_padre = tablaSimbolos.get(useActual).getTabla(tabla.padre)

                if tabla_padre is not None:
                    print("Tiene Padre :)")
                


            if rs == 0:
                consola += "Se actualizó con éxito la tupla" + str(tupla) + "\n"

            elif rs == 1:

                listaSemanticos.append(Error.ErrorS("Error Semantico", "Fallo al insertar la tupla: " + str(tupla)))

            elif rs == 2:

                listaSemanticos.append(
                    Error.ErrorS("Error Semantico", "Fallo al insertar, la base de datos '%s' no existe " % useActual))

            elif rs == 3:

                listaSemanticos.append(
                    Error.ErrorS("Error Semantico", "Fallo al insertar, la tabla '%s' no existe" % tabla.nombre))

            elif rs == 4:

                listaSemanticos.append(
                    Error.ErrorS("Error Semantico", "Fallo al insertar, La llave primaria '%s' no existe" % str(pk)))


    elif b["cod"] == 1:
        listaSemanticos.append(Error.ErrorS(
            "Error Semantico", "La columna " + b["col"] + "no existe en la tabla"))
    elif b["cod"] == 2:
        listaSemanticos.append(Error.ErrorS(
            "Error Semantico", "La columna " + b["col"] + " no puede ser nula"))


# MÉTODO PARA RETORNAR LA TUPLA COMPLETA
def validarDefault(listaC, listaV, tabla, tablaSimbolos):
    tupla = []
    indice = 0
    

    for i in tabla.columnas:
        encontrado = False
        print(tabla.columnas[i].index,indice)

        if tabla.columnas[i].index == indice:
            
            for j in range(len(listaC)):

                if tabla.columnas[i].nombre == listaC[j].valor:
                    tupla.append(listaV[j].valor)
                    indice += 1
                    i = 0
                    encontrado = True
                    break

            if not encontrado:

                if tabla.columnas[i].default != None:

                    tupla.append(Interpreta_Expresion(tabla.columnas[i].default, tablaSimbolos, tabla).valor)

                else:

                    tupla.append(None)

                indice += 1

            if (len(tabla.columnas) == len(tupla) ):
                
                return tupla
        


# MÉTODO PARA RETORNAR LA TUPLA COMPLETA
def validarDefault2(listaC, listaV, tabla, tablaSimbolos):
    tupla = []
    indice = 0
    encontrado = False

    for i in tabla.columnas:

        if tabla.columnas[i].index == indice:

            for j in range(len(listaC)):

                if tabla.columnas[i].nombre == listaC[j]:
                    tupla.append(Interpreta_Expresion(listaV[j], tablaSimbolos, tabla).valor)
                    indice += 1
                    i = 0
                    encontrado = True
                    break

            if not encontrado:

                if tabla.columnas[i].default != None:

                    tupla.append(Interpreta_Expresion(tabla.columnas[i].default, tablaSimbolos, tabla).valor)

                else:

                    tupla.append(None)

            if (len(tabla.columnas) == len(tupla)):
                return tupla


# MÉTODO PARA VALIDAR LAS LLAVES FORÁNEAS
def validarFK(col, val, tabla, tablaSimbolos):
    if col.foreign_key != None:

        registro = jBase.extractTable(useActual, col.foreign_key["tabla"])
        indice = tablaSimbolos.getColumna(
            useActual, col.foreign_key["tabla"], col.foreign_key["columna"]).index

        if registro != None and len(registro) > 0:

            for i in range(len(registro)):

                if val == registro[i][indice]:
                    return True

            return False

        else:
            return False

    return True


# MÉTODO PARA VALIDAR LOS CHECKS
def validaCheck(col, val, columnas, valores):
    if col.check != None:

        tipo = col.check["condicion"].opDer.tipo
        if tipo == Expresion.ID:
            for i in range(len(columnas)):
                if columnas[i].valor == col.check["condicion"].opDer.valor:

                    nuevo = SOperacion(val, valores[i], col.check["condicion"].operador)

                    if Interpreta_Expresion(nuevo, None, None).valor:
                        return 0
                    else:
                        return 1
            return 2
        else:
            
            nuevo = SOperacion(val, col.check["condicion"].opDer, col.check["condicion"].operador)

            r = Interpreta_Expresion(nuevo, None, None)

            if r.valor:
                return 0
            else:
                return 1
    return 0


# MÉTODO PARA VALIDAR LOS UNIQUE
def validarUnique(col, val, tabla):
    global useActual
    registros = jBase.extractTable(useActual, tabla.nombre)
    indice = col.index

    if (col.unique == True):

        for i in range(len(registros)):

            if registros[i][indice] == val:
                return False

    return True


# MÉTODO PARA VALIDAR LAS PRIMARY KEY
def validarPK(col, val, tabla):
    global useActual
    registros = jBase.extractTable(useActual, tabla.nombre)
    indice = col.index

    if (col.primary_key == True):

        if registros != None:

            for i in range(len(registros)):

                if registros[i][indice] == val:
                    return False

    return True


def validarTiposNumericos(dato, expresion):
    if dato == "smallint":
        if expresion.tipo == Expresion.ENTERO or expresion.tipo == Expresion.NEGATIVO:
            if expresion.valor >= -32768 and expresion.valor <= 32767:
                return True
    elif dato == "integer":
        if expresion.tipo == Expresion.ENTERO or expresion.tipo == Expresion.NEGATIVO:
            if expresion.valor >= -2147483648 and expresion.valor <= 2147483647:
                return True
    elif dato == "bigint":
        if expresion.tipo == Expresion.ENTERO or expresion.tipo == Expresion.NEGATIVO:
            if expresion.valor >= -9223372036854775808 and expresion.valor <= 9223372036854775807:
                return True
    elif dato == "decimal":
        if expresion.tipo == Expresion.DECIMAL or expresion.tipo == Expresion.NEGATIVO:
            return True
    elif dato == "numeric":
        if expresion.tipo == Expresion.DECIMAL or expresion.tipo == Expresion.NEGATIVO:
            return True
    elif dato == "real":
        if expresion.tipo == Expresion.DECIMAL or expresion.tipo == Expresion.NEGATIVO:
            return True
    elif dato == "double":
        if expresion.tipo == Expresion.DECIMAL or expresion.tipo == Expresion.NEGATIVO:
            return True
    elif dato == "money":
        if expresion.tipo == Expresion.DECIMAL or expresion.tipo == Expresion.ENTERO:
            return True

    if expresion.tipo==Expresion.NULL:
        return True
    
    return False


def validarTiposChar(dato, expresion):
    if dato.dato.lower() == "varying" or dato.dato.lower() == "varchar":
        if len(expresion.valor) <= dato.cantidad:
            return True
    elif dato.dato.lower() == "character" or dato.dato.lower() == "char":
        if len(expresion.valor) <= dato.cantidad:
            return True
    elif dato.dato.lower() == "text":
        return  True

    if expresion.tipo == Expresion.NULL:
        return True 

    return False


def validarTiposFecha(dato, expresion):
    if dato == "date":
        if expresion.tipo == Expresion.FECHA:
            return True
    elif dato == "timestamp":
        if expresion.tipo == Expresion.FECHA or expresion.tipo == Expresion.FECHA_HORA:
            return True
    elif dato == "time":
        if expresion.tipo == Expresion.HORA:
            return True
    elif dato == "interval":
        if expresion.tipo == Expresion.INTERVALO:
            return True

    if expresion.tipo == Expresion.NULL:
        return True
    
    return False


def Interpreta_Expresion(expresion, tablaSimbolos, tabla):
    global consola
    if isinstance(expresion, SOperacion):
        # Logicas
        if (expresion.operador == Logicas.AND):
            opIzq = Interpreta_Expresion(expresion.opIzq, tablaSimbolos, tabla).valor
            opDer = Interpreta_Expresion(expresion.opDer, tablaSimbolos, tabla).valor
            result = (opIzq and opDer)
            return SExpresion(result, Expresion.BOOLEAN)
        if (expresion.operador == Logicas.OR):
            opIzq = Interpreta_Expresion(expresion.opIzq, tablaSimbolos, tabla).valor
            opDer = Interpreta_Expresion(expresion.opDer, tablaSimbolos, tabla).valor
            result = (opIzq or opDer)
            return SExpresion(result, Expresion.BOOLEAN)

        # Relacionales
        if (expresion.operador == Relacionales.IGUAL):
            opIzq = Interpreta_Expresion(expresion.opIzq, tablaSimbolos, tabla).valor
            opDer = Interpreta_Expresion(expresion.opDer, tablaSimbolos, tabla).valor
            result = (opIzq == opDer)
            return SExpresion(result, Expresion.BOOLEAN)
        if (expresion.operador == Relacionales.DIFERENTE):
            opIzq = Interpreta_Expresion(expresion.opIzq, tablaSimbolos, tabla).valor
            opDer = Interpreta_Expresion(expresion.opDer, tablaSimbolos, tabla).valor
            result = (opIzq != opDer)
            return SExpresion(result, Expresion.BOOLEAN)
        if (expresion.operador == Relacionales.MENORIGUAL_QUE):
            opIzq = Interpreta_Expresion(expresion.opIzq, tablaSimbolos, tabla)
            opDer = Interpreta_Expresion(expresion.opDer, tablaSimbolos, tabla)

            result = opIzq.valor <= opDer.valor
            return SExpresion(result, opIzq.tipo)

        if (expresion.operador == Relacionales.MAYORIGUAL_QUE):
            opIzq = Interpreta_Expresion(expresion.opIzq, tablaSimbolos, tabla)
            opDer = Interpreta_Expresion(expresion.opDer, tablaSimbolos, tabla)

            result = opIzq.valor >= opDer.valor
            return SExpresion(result, opIzq.tipo)

        if (expresion.operador == Relacionales.MENOR_QUE):
            opIzq = Interpreta_Expresion(expresion.opIzq, tablaSimbolos, tabla)
            opDer = Interpreta_Expresion(expresion.opDer, tablaSimbolos, tabla)

            result = opIzq.valor < opDer.valor
            return SExpresion(result, opIzq.tipo)

        if (expresion.operador == Relacionales.MAYOR_QUE):
            opIzq = Interpreta_Expresion(expresion.opIzq, tablaSimbolos, tabla)
            opDer = Interpreta_Expresion(expresion.opDer, tablaSimbolos, tabla)
            
            result = opIzq.valor > opDer.valor
            return SExpresion(result, opIzq.tipo)

        # Aritmetica
        if (expresion.operador == Aritmetica.MAS):
            opIzq = Interpreta_Expresion(expresion.opIzq, tablaSimbolos, tabla)
            opDer = Interpreta_Expresion(expresion.opDer, tablaSimbolos, tabla)
            if (opIzq.tipo == Expresion.ENTERO or opIzq.tipo == Expresion.DECIMAL) and (
                    opDer.tipo == Expresion.ENTERO or opDer.tipo == Expresion.DECIMAL):
                result = opIzq.valor + opDer.valor
                return SExpresion(result, opIzq.tipo)
        if (expresion.operador == Aritmetica.MENOS):
            opIzq = Interpreta_Expresion(expresion.opIzq, tablaSimbolos, tabla)
            opDer = Interpreta_Expresion(expresion.opDer, tablaSimbolos, tabla)
            if (opIzq.tipo == Expresion.ENTERO or opIzq.tipo == Expresion.DECIMAL) and (
                    opDer.tipo == Expresion.ENTERO or opDer.tipo == Expresion.DECIMAL):
                result = opIzq.valor - opDer.valor
                return SExpresion(result, opIzq.tipo)
        if (expresion.operador == Aritmetica.POR):
            opIzq = Interpreta_Expresion(expresion.opIzq, tablaSimbolos, tabla)
            opDer = Interpreta_Expresion(expresion.opDer, tablaSimbolos, tabla)
            if (opIzq.tipo == Expresion.ENTERO or opIzq.tipo == Expresion.DECIMAL) and (
                    opDer.tipo == Expresion.ENTERO or opDer.tipo == Expresion.DECIMAL):
                result = opIzq.valor * opDer.valor
                return SExpresion(result, opIzq.tipo)
        if (expresion.operador == Aritmetica.DIVIDIDO):
            opIzq = Interpreta_Expresion(expresion.opIzq, tablaSimbolos, tabla)
            opDer = Interpreta_Expresion(expresion.opDer, tablaSimbolos, tabla)
            if (opIzq.tipo == Expresion.ENTERO or opIzq.tipo == Expresion.DECIMAL) and (
                    opDer.tipo == Expresion.ENTERO or opDer.tipo == Expresion.DECIMAL):
                result = opIzq.valor / opDer.valor
                return SExpresion(result, opIzq.tipo)
        if (expresion.operador == Aritmetica.MODULO):
            opIzq = Interpreta_Expresion(expresion.opIzq, tablaSimbolos, tabla)
            opDer = Interpreta_Expresion(expresion.opDer, tablaSimbolos, tabla)
            if (opIzq.tipo == Expresion.ENTERO or opIzq.tipo == Expresion.DECIMAL) and (
                    opDer.tipo == Expresion.ENTERO or opDer.tipo == Expresion.DECIMAL):
                result = opIzq.valor % opDer.valor
                return SExpresion(result, opIzq.tipo)
        if (expresion.operador == Aritmetica.POTENCIA):
            opIzq = Interpreta_Expresion(expresion.opIzq, tablaSimbolos, tabla)
            opDer = Interpreta_Expresion(expresion.opDer, tablaSimbolos, tabla)
            if (opIzq.tipo == Expresion.ENTERO or opIzq.tipo == Expresion.DECIMAL) and (
                    opDer.tipo == Expresion.ENTERO or opDer.tipo == Expresion.DECIMAL):
                result = opIzq.valor ** opDer.valor
                return SExpresion(result, opIzq.tipo)
    # f
    elif isinstance(expresion, SFuncMath):
        if expresion.funcion.lower() == "abs":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = abs(param.valor)
            return SExpresion(val, param.tipo)
        elif expresion.funcion.lower() == "cbrt":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = (param.valor) ** (1 / 3)
            return SExpresion(val, param.tipo)
        elif expresion.funcion.lower() == "ceil":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = math.ceil(param.valor)
            return SExpresion(val, param.tipo)
        elif expresion.funcion.lower() == "ceiling":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = math.ceil(param.valor)
            return SExpresion(val, param.tipo)
        elif expresion.funcion.lower() == "degrees":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = math.degrees(param.valor)
            return SExpresion(val, param.tipo)
        elif expresion.funcion.lower() == "exp":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = math.exp(param.valor)
            return SExpresion(val, param.tipo)
        elif expresion.funcion.lower() == "factorial":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = math.factorial(param.valor)
            return SExpresion(val, param.tipo)
        elif expresion.funcion.lower() == "floor":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = math.floor(param.valor)
            return SExpresion(val, param.tipo)
        elif expresion.funcion.lower() == "ln":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = math.log(param.valor)
            return SExpresion(val, param.tipo)
        elif expresion.funcion.lower() == "log":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = math.log10(param.valor)
            return SExpresion(val, param.tipo)
        elif expresion.funcion.lower() == "radians":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = math.radians(param.valor)
            return SExpresion(val, param.tipo)
        elif expresion.funcion.lower() == "round":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = round(param.valor)
            return SExpresion(val, param.tipo)
        elif expresion.funcion.lower() == "sign":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            if param.valor >= 0:
                val = 1
            else:
                val = -1
            return SExpresion(val, param.tipo)
        elif expresion.funcion.lower() == "sqrt":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = math.sqrt(param.valor)
            return SExpresion(val, param.tipo)
        elif expresion.funcion.lower() == "trunc":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = math.trunc(param.valor)
            return SExpresion(val, param.tipo)

    elif isinstance(expresion, SFuncMathSimple):
        if expresion.funcion.lower() == "pi":
            val = math.pi
            return SExpresion(val, Expresion.DECIMAL)
        elif expresion.funcion.lower() == "random":
            val = random()
            return SExpresion(val, Expresion.DECIMAL)

    elif isinstance(expresion, SFuncMath2):
        if expresion.funcion.lower() == "div":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            param2 = Interpreta_Expresion(expresion.param2, tablaSimbolos, tabla)
            val = param2.valor // param.valor
            return SExpresion(val, param.tipo)
        elif expresion.funcion.lower() == "gcd":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            param2 = Interpreta_Expresion(expresion.param2, tablaSimbolos, tabla)
            val = math.gcd(param.valor, param2.valor)
            return SExpresion(val, param.tipo)
        elif expresion.funcion.lower() == "mod":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            param2 = Interpreta_Expresion(expresion.param2, tablaSimbolos, tabla)
            val = param.valor % param2.valor
            return SExpresion(val, param.tipo)
        elif expresion.funcion.lower() == "power":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            param2 = Interpreta_Expresion(expresion.param2, tablaSimbolos, tabla)
            val = math.pow(param.valor, param2.valor)
            return SExpresion(val, param.tipo)
        elif expresion.funcion.lower() == "round":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            param2 = Interpreta_Expresion(expresion.param2, tablaSimbolos, tabla)
            val = round(param.valor, param2.valor)
            return SExpresion(val, param.tipo)

    elif isinstance(expresion, SFuncMathLista):
        if expresion.funcion.lower() == "width_bucket":
            val = 1
            return SExpresion(val, Expresion.ENTERO)

    elif isinstance(expresion, SFuncTrig):
        if expresion.funcion.lower() == "acos":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = math.acos(param.valor)
            return SExpresion(val, Expresion.DECIMAL)
        elif expresion.funcion.lower() == "acosd":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val1 = math.acos(param.valor)
            val = math.degrees(val1)
            return SExpresion(val, Expresion.DECIMAL)
        elif expresion.funcion.lower() == "asin":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = math.asin(param.valor)
            return SExpresion(val, Expresion.DECIMAL)
        elif expresion.funcion.lower() == "asind":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val1 = math.asin(param.valor)
            val = math.degrees(val1)
            return SExpresion(val, Expresion.DECIMAL)
        elif expresion.funcion.lower() == "atan":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = math.atan(param.valor)
            return SExpresion(val, Expresion.DECIMAL)
        elif expresion.funcion.lower() == "atand":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val1 = math.atan(param.valor)
            val = math.degrees(val1)
            return SExpresion(val, Expresion.DECIMAL)
        elif expresion.funcion.lower() == "cos":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = math.cos(param.valor)
            return SExpresion(val, Expresion.DECIMAL)
        elif expresion.funcion.lower() == "cosd":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val1 = math.cos(param.valor)
            val = math.degrees(val1)
            return SExpresion(val, Expresion.DECIMAL)
        elif expresion.funcion.lower() == "cot":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = 1 / math.tan(param.valor)
            return SExpresion(val, Expresion.DECIMAL)
        elif expresion.funcion.lower() == "cotd":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val1 = 1 / math.tan(param.valor)
            val = math.degrees(val1)
            return SExpresion(val, Expresion.DECIMAL)
        elif expresion.funcion.lower() == "sin":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = math.sin(param.valor)
            return SExpresion(val, Expresion.DECIMAL)
        elif expresion.funcion.lower() == "sind":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val1 = math.sin(param.valor)
            val = math.degrees(val1)
            return SExpresion(val, Expresion.DECIMAL)
        elif expresion.funcion.lower() == "tan":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = math.tan(param.valor)
            return SExpresion(val, Expresion.DECIMAL)
        elif expresion.funcion.lower() == "tand":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val1 = math.tan(param.valor)
            val = math.degrees(val1)
            return SExpresion(val, Expresion.DECIMAL)
        elif expresion.funcion.lower() == "sinh":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = math.sinh(param.valor)
            return SExpresion(val, Expresion.DECIMAL)
        elif expresion.funcion.lower() == "cosh":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = math.cosh(param.valor)
            return SExpresion(val, Expresion.DECIMAL)
        elif expresion.funcion.lower() == "tanh":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = math.tanh(param.valor)
            return SExpresion(val, Expresion.DECIMAL)
        elif expresion.funcion.lower() == "asinh":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = math.asinh(param.valor)
            return SExpresion(val, Expresion.DECIMAL)
        elif expresion.funcion.lower() == "acosh":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = math.acosh(param.valor)
            return SExpresion(val, Expresion.DECIMAL)
        elif expresion.funcion.lower() == "atanh":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = math.atanh(param.valor)
            return SExpresion(val, Expresion.DECIMAL)

    elif isinstance(expresion, SFuncTrig2):
        if expresion.funcion.lower() == "atan2":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            param2 = Interpreta_Expresion(expresion.param2, tablaSimbolos, tabla)
            val = math.atan2(param.valor,param2.valor)
            return SExpresion(val, Expresion.DECIMAL)
        elif expresion.funcion.lower() == "atan2d":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            param2 = Interpreta_Expresion(expresion.param2, tablaSimbolos, tabla)
            val1 = math.atan2(param.valor,param2.valor)
            val = math.degrees(val1)
            return SExpresion(val, Expresion.DECIMAL)

    elif isinstance(expresion, SFuncBinary):
        if expresion.funcion.lower() == "length":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = len(param.valor)
            return SExpresion(val, Expresion.ENTERO)
        elif expresion.funcion.lower() == "trim":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = len(param)
            return SExpresion(val, Expresion.ENTERO)
        elif expresion.funcion.lower() == "md5":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = hashlib.md5(str(param.valor).encode("utf-8")).hexdigest()
            return SExpresion(val, Expresion.CADENA)
        elif expresion.funcion.lower() == "sha256":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = hashlib.sha256(str(param.valor).encode("utf-8")).hexdigest()
            return SExpresion(val, Expresion.CADENA)
        elif expresion.funcion == "|":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = math.sqrt(param.valor)
            return SExpresion(val, Expresion.ENTERO)
        elif expresion.funcion == "||":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = (param.valor ** (1 / 3))
            return SExpresion(val, Expresion.ENTERO)
        elif expresion.funcion == "~":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = (~int(param.valor))
            return SExpresion(val, Expresion.ENTERO)

    elif isinstance(expresion, SFuncBinary2):
        if expresion.funcion == "&":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            param2 = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = param.valor & param2.valor
            return SExpresion(val, Expresion.ENTERO)
        elif expresion.funcion == "|":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            param2 = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = param.valor | param2.valor
            return SExpresion(val, Expresion.ENTERO)
        elif expresion.funcion == "?":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            param2 = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = param.valor ^ param2.valor
            return SExpresion(val, Expresion.ENTERO)
        elif expresion.funcion == "<<":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            param2 = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = param.valor << param2.valor
            return SExpresion(val, Expresion.ENTERO)
        elif expresion.funcion == ">>":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            param2 = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = param.valor >> param2.valor
            return SExpresion(val, Expresion.ENTERO)
        elif expresion.funcion.lower() == "encode":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            param2 = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = len(param)
            return SExpresion(val, Expresion.ENTERO)
        elif expresion.funcion.lower() == "get_byte":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            param2 = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = len(param)
            return SExpresion(val, Expresion.ENTERO)

    elif isinstance(expresion, SFuncBinary3):
        if expresion.funcion.lower() == "decode":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            param2 = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = len(param)
            return SExpresion(val, Expresion.ENTERO)
        elif expresion.funcion.lower() == "convert":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            param2 = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = len(param)
            return SExpresion(val, Expresion.ENTERO)

    elif isinstance(expresion, SFuncBinary4):
        if expresion.funcion.lower() == "set_byte":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            param2 = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            val = len(param)
            return SExpresion(val, Expresion.ENTERO)

    elif isinstance(expresion, SSelectFunc):
        if expresion.id.lower() == "current_date":
            today = date.today()
            val = today.strftime("%d/%m/%Y")
            return SExpresion(val, Expresion.FECHA)
        elif expresion.id.lower() == "current_time":
            now = datetime.now()
            val = now.strftime("%H:%M:%S")
            return SExpresion(val, Expresion.HORA)
        elif expresion.id.lower() == "now":
            now = datetime.now()
            val = now.strftime("%d/%m/%Y %H:%M:%S")
            return SExpresion(val, Expresion.FECHA)

    elif isinstance(expresion, SFechaFunc2):
        if expresion.id.lower() == "date_part":
            param = Interpreta_Expresion(expresion.param, tablaSimbolos, tabla)
            param2 = Interpreta_Expresion(expresion.param2, tablaSimbolos, tabla)


    elif isinstance(expresion, SExpresion):
        if expresion.tipo == Logicas.NOT:
            result = not expresion.valor
            return result
        elif expresion.tipo == Expresion.NEGATIVO:
            result = expresion.valor.valor * -1
            return SExpresion(result, Expresion.NEGATIVO)

        elif expresion.tipo == Expresion.ID:

            # print("")
            # print("==============================================")
            # print("|            Estamos en el ID                |")
            # print("==============================================")
            # print("|              El ID es: '%s'                |" % expresion.valor)
            # print("==============================================")

            for i in range(len(tabla["nombreC"])):

                if tabla["nombreC"][i] == expresion.valor:
                    tipo = retornarTipo(tabla["tipo"][i].dato)
                    valor = tabla["valor"][i]

                    return SExpresion(valor, tipo)

        elif expresion.tipo == Expresion.FECHA:

            valor = datetime.strptime(str(expresion.valor),'%Y-%m-%d').date()
            return SExpresion(valor, expresion.tipo)


        elif expresion.tipo == Expresion.FECHA_HORA:

            valor = datetime.strptime(expresion.valor,'%Y-%m-%d %H:%M:%S')
            return SExpresion(valor, expresion.tipo)

        elif expresion.tipo == Expresion.HORA:

            valor = datetime.strptime(expresion.valor,'%H:%M:%S').time()
            return SExpresion(valor, expresion.tipo)

    elif isinstance(expresion,SAny):

        print("================== ENTRÓ AL ANY ==================")
        columna = Interpreta_Expresion(expresion.columna,tablaSimbolos,tabla)
        qr = expresion.consulta
        pT = PrettyTable()
        for tb in tabla["tablas"]:
            qr.ffrom.clist.append(tb)
        resultado_sub = hacerConsulta(qr.select,qr.ffrom,qr.where,qr.groupby,qr.having,qr.orderby,qr.limit,base,pT,False,tablaSimbolos)
        
        print(expresion.operador)
        if expresion.operador == '=':
            for rs in resultado_sub:
                if str(rs[0]) == str(columna.valor):
                    return SExpresion(True,Expresion.BOOLEAN)
            return SExpresion(False,Expresion.BOOLEAN)

        elif expresion.operador == '<':
            for rs in resultado_sub:
                if float(rs[0]) < float(columna.valor):
                    return SExpresion(True,Expresion.BOOLEAN)
            return SExpresion(False,Expresion.BOOLEAN)


        elif expresion.operador == '>':
            for rs in resultado_sub:
                if float(rs[0]) > float(columna.valor):
                    return SExpresion(True,Expresion.BOOLEAN)
            return SExpresion(False,Expresion.BOOLEAN)


        elif expresion.operador == '<=':
            for rs in resultado_sub:
                if float(rs[0]) <= float(columna.valor):
                    return SExpresion(True,Expresion.BOOLEAN)
            return SExpresion(False,Expresion.BOOLEAN)


        elif expresion.operador == '>=':
            for rs in resultado_sub:
                if float(rs[0]) >= float(columna.valor):
                    return SExpresion(True,Expresion.BOOLEAN)
            return SExpresion(False,Expresion.BOOLEAN)


        elif expresion.operador == '<>':
            for rs in resultado_sub:
                if float(rs[0]) != float(columna.valor):
                    return SExpresion(True,Expresion.BOOLEAN)
            return SExpresion(False,Expresion.BOOLEAN)
        
        print("=================== FIN AL ANY ===================")
        return SExpresion(False,Expresion.BOOLEAN)

    elif isinstance(expresion,SAll):

        print("================== ENTRÓ AL ALL ==================")
        columna = Interpreta_Expresion(expresion.columna,tablaSimbolos,tabla)
        qr = expresion.consulta
        pT = PrettyTable()
        for tb in tabla["tablas"]:
            qr.ffrom.clist.append(tb)
        resultado_sub = hacerConsulta(qr.select,qr.ffrom,qr.where,qr.groupby,qr.having,qr.orderby,qr.limit,base,pT,False,tablaSimbolos)
        
        print(expresion.operador)
        if expresion.operador == '=':
            for rs in resultado_sub:
                if str(rs[0]) != str(columna.valor):
                    return SExpresion(False,Expresion.BOOLEAN)
            return SExpresion(True,Expresion.BOOLEAN)

        elif expresion.operador == '<':
            for rs in resultado_sub:
                if float(rs[0]) >= float(columna.valor):
                    return SExpresion(False,Expresion.BOOLEAN)
            return SExpresion(True,Expresion.BOOLEAN)


        elif expresion.operador == '>':
            for rs in resultado_sub:
                if float(rs[0]) <= float(columna.valor):
                    return SExpresion(False,Expresion.BOOLEAN)
            return SExpresion(True,Expresion.BOOLEAN)


        elif expresion.operador == '<=':
            for rs in resultado_sub:
                if float(rs[0]) > float(columna.valor):
                    return SExpresion(False,Expresion.BOOLEAN)
            return SExpresion(True,Expresion.BOOLEAN)


        elif expresion.operador == '>=':
            for rs in resultado_sub:
                if float(rs[0]) < float(columna.valor):
                    return SExpresion(False,Expresion.BOOLEAN)
            return SExpresion(True,Expresion.BOOLEAN)


        elif expresion.operador == '<>':
            for rs in resultado_sub:
                if float(rs[0]) == float(columna.valor):
                    return SExpresion(False,Expresion.BOOLEAN)
            return SExpresion(True,Expresion.BOOLEAN)

        
        print("=================== FIN AL ALL ===================")
        return SExpresion(False,Expresion.BOOLEAN)
    
    elif isinstance(expresion,SNotExist):

        qr = expresion.consulta
        base = tablaSimbolos.get(useActual)
        pT = PrettyTable()
        for tb in tabla["tablas"]:
            qr.ffrom.clist.append(tb)
        resultado_sub = hacerConsulta(qr.select,qr.ffrom,qr.where,qr.groupby,qr.having,qr.orderby,qr.limit,base,pT,False,tablaSimbolos)

        if len(resultado_sub) > 0:
            return SExpresion(False,Expresion.BOOLEAN)
        return SExpresion(True,Expresion.BOOLEAN)

    elif isinstance(expresion,SExist):

        qr = expresion.consulta
        base = tablaSimbolos.get(useActual)
        pT = PrettyTable()
        for tb in tabla["tablas"]:
            qr.ffrom.clist.append(tb)
        resultado_sub = hacerConsulta(qr.select,qr.ffrom,qr.where,qr.groupby,qr.having,qr.orderby,qr.limit,base,pT,False,tablaSimbolos)

        if len(resultado_sub) > 0:
            return SExpresion(True,Expresion.BOOLEAN)
        return SExpresion(False,Expresion.BOOLEAN)
               
        
    
    elif isinstance(expresion,SIn):

        qr = expresion.consulta
        base = tablaSimbolos.get(useActual)
        pT = PrettyTable()
        for tb in tabla["tablas"]:
            qr.ffrom.clist.append(tb)
        resultado_sub = hacerConsulta(qr.select,qr.ffrom,qr.where,qr.groupby,qr.having,qr.orderby,qr.limit,base,pT,False,tablaSimbolos)
        columna = Interpreta_Expresion(expresion.columna,tablaSimbolos,tabla)

        for r in resultado_sub:
            if str(r[0]) == str(columna.valor):
                return SExpresion(True,Expresion.BOOLEAN)
        return SExpresion(False,Expresion.BOOLEAN)

    elif isinstance(expresion,SNotIn):
       
        qr = expresion.consulta
        base = tablaSimbolos.get(useActual)
        pT = PrettyTable()
        for tb in tabla["tablas"]:
            qr.ffrom.clist.append(tb)
        resultado_sub = hacerConsulta(qr.select,qr.ffrom,qr.where,qr.groupby,qr.having,qr.orderby,qr.limit,base,pT,False,tablaSimbolos)
        columna = Interpreta_Expresion(expresion.columna,tablaSimbolos,tabla)

        for r in resultado_sub:

            if str(r[0]) == str(columna.valor):

                return SExpresion(False,Expresion.BOOLEAN)
        return SExpresion(True,Expresion.BOOLEAN)

    elif isinstance(expresion,SBetween):

        # print("")
        # print("============= ENTRÓ A BETWEEN =============")

        op1 = Interpreta_Expresion(expresion.opIzq,tablaSimbolos, tabla)
        # print("OP1: " + str(op1))
        col = Interpreta_Expresion(expresion.columna,tablaSimbolos, tabla)
        #print("COL: " + str(col))
        op2 = Interpreta_Expresion(expresion.opDer,tablaSimbolos, tabla)
        #print("OP2: " + str(op2))

        res = col.valor >= op1.valor and col.valor <= op2.valor
        #print("res: " + str(res))
        #print("===========================================")
        #print("")
        return SExpresion(res,Expresion.BOOLEAN)


    elif isinstance(expresion,SNotBetween):

        #print("")
        #print("============= ENTRÓ A NOT BETWEEN =============")

        op1 = Interpreta_Expresion(expresion.opIzq,tablaSimbolos, tabla)
        #print("OP1: " + str(op1))
        col = Interpreta_Expresion(expresion.columna,tablaSimbolos, tabla)
        #print("COL: " + str(col))
        op2 = Interpreta_Expresion(expresion.opDer,tablaSimbolos, tabla)
        #print("OP2: " + str(op2))

        res = col.valor < op1.valor or col.valor > op2.valor
        #print("res: " + str(res))
        #print("===============================================")
        #print("")
        return SExpresion(res,Expresion.BOOLEAN)


    elif isinstance(expresion,SLike):

        col =  Interpreta_Expresion(expresion.columna,tablaSimbolos, tabla)
        cadena = expresion.cadena

        r = re.compile(".*" + cadena + ".*")
        res = r.search(col.valor)

        return SExpresion(res,Expresion.BOOLEAN)


    elif isinstance(expresion,SLike):

        col =  Interpreta_Expresion(expresion.columna,tablaSimbolos, tabla)
        cadena = expresion.cadena

        r = re.compile(".*" + cadena + ".*")
        res = not r.search(col.valor)

        return SExpresion(res,Expresion.BOOLEAN)


    elif isinstance(expresion,SSimilar):

        col =  Interpreta_Expresion(expresion.columna,tablaSimbolos, tabla)
        patron = expresion.patron

        r = re.compile(patron)
        res = not r.search(col.valor)

        return SExpresion(res,Expresion.BOOLEAN)


    elif isinstance(expresion,SSubstring):

        cadena = Interpreta_Expresion(expresion.cadena,tablaSimbolos,tabla)
        inicio = Interpreta_Expresion(expresion.inicio,tablaSimbolos,tabla)
        tamanio = Interpreta_Expresion(expresion.tamanio,tablaSimbolos,tabla)
        comparar = Interpreta_Expresion(expresion.comparar,tablaSimbolos,tabla)

        res = cadena.valor[inicio.valor:inicio.valor+tamanio.valor]==comparar.valor

        return SExpresion(res,Expresion.BOOLEAN)

    return expresion


def retornarTipo(tipo):
    if tipo == "smallint" or tipo == "integer" or tipo == "bigint":
        return Expresion.ENTERO

    elif tipo == "decimal" or tipo == "numeric" or tipo == "real" or tipo == "double" or tipo == "money":
        return Expresion.DECIMAL

    elif tipo == "varying" or tipo == "varchar" or tipo == "character" or tipo == "char" or tipo == "text":
        return Expresion.CADENA

    elif tipo == "date":
        return Expresion.FECHA

    elif tipo == "timestamp":
        return Expresion.FECHA_HORA

    elif tipo == "time":
        return Expresion.HORA

    elif tipo == "interval":
        return Expresion.INTERVALO


def getFechaFunc(funcion):
    if funcion.lower() == "current_date":
        today = date.today()
        val = today.strftime("%d/%m/%Y")
        return val
    elif funcion.lower() == "current_time":
        now = datetime.now()
        val = now.strftime("%H:%M:%S")
        return val
    elif funcion.lower() == "now":
        now = datetime.now()
        val = now.strftime("%d/%m/%Y %H:%M:%S")
        return val


def getFechaFunc2(funcion, param):
    if funcion.lower() == "timestamp":
        if param.lower() == "now":
            now = datetime.now()
            val = now.strftime("%d/%m/%Y %H:%M:%S")
            return val
        else:
            today = date.today()
            val = today.strftime("%d/%m/%Y %H:%M:%S")
            return val
    elif funcion.lower() == "date":
        today = date.today()
        val = today.strftime("%d/%m/%Y")
        return val
    elif funcion.lower() == "time":
        now = datetime.now()
        val = now.strftime("%H:%M:%S")
        return val

def truncatebase(nodo, tablaSimbolos):
    global useActual
    global consola
    for tabs in nodo.listaIds:
        b= jBase.truncate(useActual,tabs)
        if b==0:
            consola+="Los registros de la tabla "+tabs+" se eliminaron exitosamente \n"
        elif b==1:
            listaSemanticos.append(Error.ErrorS("Error semantico","error de operacion"))
        elif b==2:
            listaSemanticos.append(Error.ErrorS("Error semantico", "la base "+useActual+" no existe"))
        elif b==3:
            listaSemanticos.append(Error.ErrorS("Error semantico", "la tabla "+tabs+" no existe"))


# METODOS QUERIES

def hacerConsulta(Qselect, Qffrom, Qwhere, Qgroupby, Qhaving, Qorderby, Qlimit, base, pT, subConsulta,tablaSimbolos):
    global consola
    global useActual
    x = PrettyTable()
    encabezados = []
    indices = []
    oficial = []
    
    print("------------------ EMPIEZA CONSULTA ---------------------")
    if Qwhere == False:

        # VARIABLES
        tablaConsulta = ""
        distinct = False
        todasCols = False
        arrCols = []
        arrcast = []
        tablasColumna = []
        tipoAgregacion = False
        groupBy = []
        tipoAsterisco = False

        # SELECT
        if Qselect.distinct != False:
            distinct = True

        # Cantidad de columnas
        if Qselect.cols == "*":
            todasCols = True

        # Columnas específicas
        else:
            contador=0
            for col in Qselect.cols:
                vNombre = ""
                vAlias = ""
                vTipo = ""
                vParam = ""
                vTabla = ""
                vIndice= ""
                vNodo=""
                vcTipo=""
                if isinstance(col, SColumnasSubstr):
                    print("Funcion Substr:")
                    tipoSubstr = True
                    vNombre = "substr"
                    vTipo = 9
                    vIndice = contador
                    d1= col.cols2.valor
                    d2 =col.cols3.valor
                    if isinstance(col.cols, SExpresion):
                        vParam = col.cols
                        vTabla = False
                    else:
                        vNombre = col.cols.opDer.valor
                        vTabla = col.cols.opIzq.valor

                elif isinstance(col.cols, SExpresion):
                    vNombre = col.cols.valor
                    vTipo = 0
                    vIndice=contador
                    # arrCols.append(col.cols.valor)
                    vTabla = False

                elif isinstance(col.cols, SOperacion):
                    vNombre = col.cols.opDer.valor
                    vTipo = 0
                    vTabla = col.cols.opIzq.valor
                    vIndice=contador

                # FUNCIONES DE AGREGACION
                elif isinstance(col.cols, SFuncAgregacion):
                    tipoAgregacion = True
                    vNombre = col.cols.funcion
                    vTipo = 1
                    vIndice=contador
                    if isinstance(col.cols.param, SExpresion):
                        vParam = col.cols.param.valor
                        vTabla = False
                    elif isinstance(col.cols.param, SOperacion):
                        vNombre = col.cols.param.opDer.valor
                        vTabla = col.cols.param.opIzq.valor
                    else:
                        print("err")


                # FUNCIONES DE FECHA
                elif isinstance(col.cols, SSelectFunc):
                    vNombre = col.cols.id
                    vTabla = False
                    vParam = False
                    vTipo = 4
                    vIndice=contador


                elif isinstance(col.cols, SFechaFunc):
                    if isinstance(col.cols.param, STipoDato):
                        tipoMathS = True
                        vNombre = col.cols.param.dato
                        vTabla = False
                        vParam = col.cols.param2.valor
                        vTipo = 4
                        vIndice = contador
                        # Ssalida = getFechaFunc2(col.cols.param.dato, col.cols.param2.valor)
                    else:
                        print("else")
                        # print(col.cols.param)
                        # print(col.cols.param2)

                # FUNCIONES MATH
                elif isinstance(col.cols, SFuncMath):
                    vNombre = col.cols.funcion
                    vTipo = 2
                    vIndice = contador
                    vNodo = col.cols
                    if isinstance(col.cols.param, SExpresion):
                        vParam = col.cols.param.valor
                        vcTipo = col.cols.param.tipo
                        vTabla = False
                    else:
                        vNombre = col.cols.param.opDer.valor
                        vTabla = col.cols.param.opIzq.valor

                elif isinstance(col.cols, SFuncMath2):
                    vNombre = col.cols.funcion
                    vTipo = 5
                    vIndice = contador
                    vNodo = col.cols
                    if isinstance(col.cols.param, SExpresion):
                        arr1 = []
                        arrt = []
                        arr1.append(col.cols.param.valor)
                        arr1.append(col.cols.param2.valor)
                        arrt.append(col.cols.param.tipo)
                        arrt.append(col.cols.param2.tipo)
                        vParam = arr1
                        vcTipo = arrt
                        vTabla = False
                    else:
                        arr1 = []
                        arr2 = []
                        arr1.append(col.cols.param.opDer.valor)
                        arr1.append(col.cols.param2.opDer.valor)
                        arr2.append(col.cols.param.opIzq.valor)
                        arr2.append(col.cols.param2.opIzq.valor)
                        vParam = arr1
                        vTabla = arr2
                elif isinstance(col.cols, SFuncTrig2):
                    vNombre = col.cols.funcion
                    vTipo = 6
                    vIndice = contador
                    vNodo = col.cols
                    if isinstance(col.cols.param, SExpresion):
                        arr1 = []
                        arrt = []
                        print("params")
                        arr1.append(col.cols.param.valor)
                        arr1.append(col.cols.param2.valor)
                        arrt.append(col.cols.param.tipo)
                        arrt.append(col.cols.param2.tipo)
                        vcTipo = arrt
                        vParam = arr1
                        vTabla = False
                    else:
                        print("params")
                        arr1 = []
                        arr2 = []
                        print(col.cols.param)
                        print(col.cols.param2)
                        arr1.append(col.cols.param.opDer.valor)
                        arr1.append(col.cols.param2.opDer.valor)
                        arr2.append(col.cols.param.opIzq.valor)
                        arr2.append(col.cols.param2.opIzq.valor)
                        vParam = arr1
                        vTabla = arr2


                ###
                elif isinstance(col.cols, SFuncBinary):
                    vNombre = col.cols.funcion
                    vTipo = 8
                    vIndice = contador
                    vNodo = col.cols
                    if isinstance(col.cols.param, SExpresion):
                        vParam = col.cols.param.valor
                        vcTipo = col.cols.param.tipo
                        vTabla = False
                    else:
                        vNombre = col.cols.param.opDer.valor
                        vTabla = col.cols.param.opIzq.valor


                elif isinstance(col, SColumnasMulti):
                    tipoAsterisco = True
                    vTabla = col.id.valor
                    vTipo = 10


                elif isinstance(col.cols, SFuncBinary2):
                    print("Funcion Binary2:")
                    print(col.cols.funcion)
                    vNombre = col.cols.funcion
                    vTipo = 7
                    vIndice = contador
                    vNodo = col.cols
                    if isinstance(col.cols.param, SExpresion):
                        arr1 = []
                        arrt = []
                        print("params")
                        arr1.append(col.cols.param.valor)
                        arr1.append(col.cols.param2.valor)
                        arrt.append(col.cols.param.tipo)
                        arrt.append(col.cols.param2.tipo)
                        vcTipo = arrt
                        vParam = arr1
                        vTabla = False
                    else:
                        print("params")
                        arr1 = []
                        arr2 = []
                        print(col.cols.param.valor)
                        print(col.cols.param2)
                        arr1.append(col.cols.param.valor)
                        arr1.append(col.cols.param2.valor)
                        vParam = arr1
                        vTabla = arr2


                elif isinstance(col.cols, SFuncMathSimple):
                    print("Funcion MathSimple:")
                    tipoMathS = True
                    vNombre = col.cols.funcion
                    vTipo = 4
                    vTabla = False
                    vParam = False
                    vIndice = contador



                elif isinstance(col.cols, SFuncTrig):
                    tipoTrig = True
                    vNombre = col.cols.funcion
                    vTipo = 3
                    vIndice = contador
                    vNodo = col.cols
                    if isinstance(col.cols.param, SExpresion):
                        vParam = col.cols.param.valor
                        vcTipo = col.cols.tipo
                        vTabla = False
                    else:
                        vNombre = col.cols.param.opDer.valor
                        vTabla = col.cols.param.opIzq.valor

                # ALIAS
                if col.id != False:
                    vAlias = col.id.valor
                else:
                    if isinstance(col, SColumnasSubstr):
                        vAlias = "substr"
                    elif isinstance(col.cols, SExpresion):
                        vAlias = col.cols.valor
                    elif isinstance(col.cols, SOperacion):
                        vAlias = col.cols.opDer.valor
                    elif isinstance(col.cols, SFuncAgregacion):
                        vAlias = col.cols.funcion
                    elif isinstance(col.cols, SFuncMath):
                        vAlias = col.cols.funcion
                    elif isinstance(col.cols, SFuncMath2):
                        vAlias = col.cols.funcion
                    elif isinstance(col.cols, SFuncMathSimple):
                        vAlias = col.cols.funcion
                    elif isinstance(col.cols, SSelectFunc):
                        vAlias = col.cols.id
                    elif isinstance(col.cols, SFechaFunc):
                        vAlias = col.cols.param.dato
                    elif isinstance(col.cols, SFechaFunc2):
                        vAlias = col.cols.funcion
                    elif isinstance(col.cols, SFuncTrig):
                        vAlias = col.cols.funcion
                    elif isinstance(col.cols, SFuncTrig2):
                        vAlias = col.cols.funcion
                    elif isinstance(col.cols, SFuncBinary):
                        vAlias = col.cols.funcion
                    elif isinstance(col.cols, SFuncBinary2):
                        vAlias = col.cols.funcion
                    elif isinstance(col, SColumnasMulti):
                        vAlias = col.id.valor
                contador=contador+1
                auxCols = TS.colsConsulta(vNombre, vAlias, vTipo, vParam, vTabla,vIndice,vcTipo,vNodo)
                if vTipo == 10:
                    arrcast.append(auxCols)
                else:
                    arrCols.append(auxCols)

        # FROM
        if isinstance(Qffrom, SFrom):
            print(Qffrom.clist)
            for col in Qffrom.clist:
                if col.alias == False:
                    tablaConsulta = col.id
                    aliasTablaConsulta = col.id
                    tablasC = TS.colsTabla(tablaConsulta, aliasTablaConsulta)
                    if tablasC not in tablasColumna:
                        tablasColumna.append(tablasC)
                else:
                    tablaConsulta = col.id
                    aliasTablaConsulta = col.alias
                    tablasC = TS.colsTabla(tablaConsulta, aliasTablaConsulta)
                    if tablasC not in tablasColumna:
                        tablasColumna.append(tablasC)

        print(Qwhere)

        # GROUP BY
        if isinstance(Qgroupby, SGroupBy):
            print("entro al Group By")
            for col in Qgroupby.slist:
                if isinstance(col, SExpresion):
                    print("Agrupado por")
                    print(col.valor)
                    groupBy.append(col.valor)
                else:
                    print("Agrupado por")
                    print(col)




        elif isinstance(Qffrom, SFrom2):
            print("entro al From2")

        if tablaConsulta != "":
            bConsulta = jBase.extractTable(useActual, tablaConsulta)
            tabla = base.getTabla(tablaConsulta)
            if distinct:
                # DISTINCT SIN WHERE
                bConsulta = jBase.extractTable(useActual, tablaConsulta)
                tabla = base.getTabla(tablaConsulta)
                print("DISTINCT")
                arrIndices = []
                arrGlobal = []
                for e in arrCols:
                    indice = tabla.getColumna(e.nombre).index
                    arrIndices.append(indice)

                for i in range(len(bConsulta)):
                    arr1 = []
                    for index in arrIndices:
                        dato = bConsulta[i][index]
                        arr1.append(dato)
                    arrGlobal.append(arr1)

                arrFinal = []
                for g in arrGlobal:
                    if g not in arrFinal:
                        arrFinal.append(g)
                x = PrettyTable()
                nombreCols = []
                for e in arrCols:
                    nombreCols.append(e.alias)
                x.field_names = nombreCols
                for e in arrFinal:
                    x.add_row(e)
                consola += str(x) + "\n"

            else:
                # TODAS LAS COLS SIN WHERE 
                if todasCols:
                    x = PrettyTable()
                    t2 = base.getTabla(tablaConsulta)
                    nombreCols = []
                    for e in t2.columnas.keys():
                        nombreCols.append(e)
                    x.field_names = nombreCols
                    print(nombreCols)
                    for e in bConsulta:
                        x.add_row(e)
                    print(bConsulta)
                    consola += str(x) + "\n"
                    oficial.append(nombreCols)
                    oficial.append(bConsulta)
                else:
                    # COLUMNAS ESPECIFICAS SIN WHERE
                    print("ESPECIFICAS")

                    if tipoAgregacion:
                        agregacionSinWhere(arrCols, base, tablasColumna, pT, subConsulta,groupBy)
                    elif tipoAsterisco:
                        puntoAsterisco(arrcast, base, tablasColumna, pT, groupBy, tablaSimbolos)
                        multcolumns(arrCols, base, tablasColumna, pT, subConsulta, groupBy)
                    else:
                        un_temporal = multcolumns(arrCols, base, tablasColumna, pT, subConsulta, groupBy)


                        for r in un_temporal:
                            for r2 in r:
                                for r3 in r2:
                                    oficial.append([r3])
                        
                '''    elif tipoTrig:
                        trigSinWhere(tabla, arrCols, base, tablasColumna, pT, subConsulta)
                    elif tipoMathS:
                        consultaSimple(arrCols, pT, subConsulta)
                    elif tipoMath:
                        MathUnoSinWhere(arrCols, base, tablasColumna, pT, subConsulta)
                    elif tipoMath2:
                        MathDosSinWhere(arrCols, base, tablasColumna, pT, subConsulta)
                    else:
                        columnaEspecificaSinWhere(arrCols, base, tablasColumna, pT, subConsulta, )'''
        # Consulta simple

        else:
            if isinstance(col.cols, SExtract2):
                #print("Funcion Extract:") #len 17
                if isinstance(col.cols.field, STipoDato):
                    extraer = str(col.cols.field.dato)
                    dtstr = str(col.cols.timestampstr.valor)
                    year=dtstr[0:4]
                    month=dtstr[5:7]
                    day=dtstr[8:10]
                    hour=dtstr[11:13]
                    minute=dtstr[13:15]
                    second=dtstr[15:18]
                    if extraer.lower() == "year":
                        val = year
                    elif extraer.lower() == "month":
                        val = month
                    elif extraer.lower() == "day":
                        val = day
                    elif extraer.lower() == "hour":
                        val = hour
                    elif extraer.lower() == "minute":
                        val = minute
                    elif extraer.lower() == "second":
                        val = second
                    #print(val)
                    pT.add_column(str(extraer), val)
            elif isinstance(col.cols, SDatePart):
                #print("Funcion DatePart:")
                if isinstance(col.cols.param, SExpresion):
                    extraer = str(col.cols.param.valor)
                    cad = str(col.cols.param2.valor)
                    hours=""
                    mins=""
                    secs=""
                    x = cad.split("hours")
                    if len(x) == 2:
                        hours=str(x[0])
                        cad1 = str(x[1])
                        y= cad1.split("minutes")
                    else:
                        y = cad.split("minutes")              
                    if len(y) == 2:
                        mins=str(y[0])
                        w = y[1].split("seconds")
                        secs = w[0]
                    else:
                        w = y[0].split("seconds")
                        secs = w[0]
                    if extraer == "hour":
                        pT.add_column(str(extraer), hours)
                    elif extraer == "minutes":
                        pT.add_column(str(extraer), mins)
                    elif extraer == "seconds":
                        pT.add_column(str(extraer), secs)
            else:
                consultaSimple(arrCols,pT,groupBy)
    

    else:
        tupla = {"nombreC": [], "tipo": [], "valor": [], "tablas": []}
        registros = []
        columnas = []
        
        for tabs in Qffrom.clist:
            tupla["tablas"].append(tabs)
            registros.append(jBase.extractTable(useActual,tabs.id))

            str_alias = ""
            if tabs.alias != False:
                str_alias = tabs.alias + "_"

            for nm in tablaSimbolos.get(useActual).getTabla(tabs.id).get_name_list():

                columnas.append(str_alias + nm )
                tupla["nombreC"].append(str_alias + nm)
                tupla["tipo"].append(tablaSimbolos.get(useActual).getTabla(tabs.id).getColumna(nm).tipo)            
        
        resultado = []
        temporal = []

        resultado = registros[0]

        for t in range(len(registros)-1) :
            temporal = registros[t+1]

            resultado = [( rs,tmp ) for rs in resultado for tmp in temporal]
            arreglo_tmp = []
            for m in resultado:
                lista_tmp = []
                for m_2 in m:
                    lista_tmp += m_2
                arreglo_tmp.append(lista_tmp)
            resultado = arreglo_tmp

        resultado_2 = []
        for t in resultado:
            
            for c in t:

                tupla["valor"].append(c)


            b = Interpreta_Expresion(Qwhere.clist,tablaSimbolos,tupla)
            tupla["valor"].clear()

            if b.valor:
                resultado_2.append(t)

        #AGREGAR LAS VALIDACIONES NECESARIAS PARA CUANDO HAY QUE FILTRAR COLUMNAS
        if Qselect.cols != '*':
            tab_temporal = []
            for ind in range(len(columnas)) :

                for q_cols in Qselect.cols:

                    if q_cols.cols.valor == columnas[ind]:
                        indices.append(ind)
                        
                        if q_cols.id == False:

                            encabezados.append(columnas[ind])
                        
                        else:

                            encabezados.append(q_cols.id.valor)
                        break
            
            i_t = 0
            for in2 in indices:

                columnas_2 = []

                for r2 in resultado_2:
                    columnas_2.append(r2[in2])

                x.add_column(encabezados[i_t],columnas_2)
                i_t +=1
            

            for row in x:
                tab_temporal.append(row._rows[0])

            oficial = tab_temporal
            consola += str(x) + "\n"

        else:
            tab_temporal = []

            for in2 in range(len(columnas)):

                columnas_2 = []
                

                for r3 in resultado_2:
                    columnas_2.append(r3[in2])

                x.add_column(columnas[in2],columnas_2)
            

            for row in x:
                tab_temporal.append(row._rows[0])
            
            oficial = tab_temporal
            consola += str(x) + "\n"      

        #AGREGAR LAS VALIDACIONES NECESARIAS PARA HACER UN DISTINCT
        if Qselect.distinct != False:
            print("Tiene Distinct") 

    print("------------------ TERMINA CONSULTA ---------------------")
    return oficial


def multcolumns(arrCols, base, tablasColumna, pT, subConsulta,groupBy):
    global consola
    retorno = []
    if not subConsulta:
        for e in arrCols:
            tabla = ""
            bandd = False
            indice = None
            auxCons = ""
            if e.tipo == 0:
                retorno.append(columnaEspecificaSinWhere([e], base, tablasColumna, pT, False))
            elif e.tipo == 2:
                retorno.append(MathUnoSinWhere([e], base, tablasColumna, pT, False))
            elif e.tipo == 3:
                retorno.append(trigSinWhere([e], base, tablasColumna, pT, False))
            elif e.tipo == 4:
                retorno.append(consultaSimple([e], pT, False))
            elif e.tipo == 5:
                retorno.append(MathDosSinWhere([e], base, tablasColumna, pT, False))
            elif e.tipo==6:
                retorno.append(TrigDosSinWhere(arrCols,base,tablasColumna,pT,False))
            elif e.tipo==8:
                retorno.append(BinStringSinWhere(arrCols,base,tablasColumna,pT,False))
            elif e.tipo==7:
                retorno.append(BinDosStringSinWhere(arrCols,base,tablasColumna,pT,False))
            elif e.tipo==9:
                retorno.append(SubstrSinWhere(arrCols,base,tablasColumna,pT,False))

    return retorno



def columnaEspecificaSinWhere(arrCols, base, tablasColumna, pT,groupby):
    global consola
    arrGlobal = []
    aReturn=[]
    arrIndices = []
    tabla=""
    indice=None
    for e in arrCols:
        tabla = ""
        bandd = False
        indice = None
        if e.tabla == False:
            for c in tablasColumna:
                tabla = base.getTabla(c.nombre)
                indice = tabla.getColumna(e.nombre)
                auxCons = jBase.extractTable(useActual, tabla.nombre)
                if indice != None:
                    arr1 = []
                    for i in range(len(auxCons)):
                        dato = auxCons[i][indice.index]
                        arr1.append(str(dato))
                        sim=TS.Grupo(i,indice.index,tabla.nombre,dato)
                        aReturn.append(sim)
                    arrGlobal.append(arr1)
                    bandd = True
                    break
        else:
            for a in tablasColumna:
                if a.alias == e.tabla:
                    tabla = base.getTabla(a.nombre)
                    indice = tabla.getColumna(e.nombre)
                    auxCons = jBase.extractTable(useActual, tabla.nombre)
                    if indice != None:
                        arr1 = []
                        for i in range(len(auxCons)):
                            dato = auxCons[i][indice.index]
                            arr1.append(str(dato))
                            sim = TS.Grupo(i, indice.index, tabla.nombre, dato)
                            aReturn.append(sim)
                        arrGlobal.append(arr1)
                        bandd = True
                        break
        if indice == None:
            listaSemanticos.append(Error.ErrorS("Error Semántico", "No se encontró la columna" + e.nombre))
    if not groupby:
        n = 0
        for xd in arrGlobal:
            pT.add_column(arrCols[n].alias, xd)
            n += 1
        return arrGlobal
    else:
        return aReturn

    # consola += str(pT)+"\n"


def consultaSimple(arrCols, pT,groupby):
    global consola
    arrGlobal = []
    for e in arrCols:
        if e.param == False:
            if e.nombre.lower() == "pi":
                arr1 = []
                val = math.pi
                arr1.append(val)
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "random":
                arr1 = []
                val = random()
                arr1.append(val)
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "current_date":
                arr1 = []
                today = date.today()
                val = today.strftime("%d/%m/%Y")
                arr1.append(val)
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "current_time":
                arr1 = []
                now = datetime.now()
                val = now.strftime("%H:%M:%S")
                arr1.append(val)
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "now":
                arr1 = []
                now = datetime.now()
                val = now.strftime("%d/%m/%Y %H:%M:%S")
                arr1.append(val)
                arrGlobal.append(arr1)
        else:
            if e.nombre.lower() == "timestamp":
                if e.param.lower() == "now":
                    arr1 = []
                    now = datetime.now()
                    val = now.strftime("%d/%m/%Y %H:%M:%S")
                    arr1.append(val)
                    arrGlobal.append(arr1)
                else:
                    arr1 = []
                    today = date.today()
                    val = today.strftime("%d/%m/%Y %H:%M:%S")
                    arr1.append(val)
                    arrGlobal.append(arr1)
            elif e.nombre.lower() == "date":
                arr1 = []
                today = date.today()
                val = today.strftime("%d/%m/%Y")
                arr1.append(val)
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "time":
                arr1 = []
                now = datetime.now()
                val = now.strftime("%H:%M:%S")
                arr1.append(val)
                arrGlobal.append(arr1)
            else:
                val = Interpreta_Expresion(e.nodo, None, None)
                arrGlobal.append([str(val.valor)])

    # x = PrettyTable()
    if not groupby:
        n = 0
        for xd in arrGlobal:
            pT.add_column(arrCols[n].alias, xd)
            n += 1
    else:
        return arrGlobal
    # x.field_names = nombreCols
    # x.add_rows([arrGlobal])
    # consola += str(pT) + "\n"

    return arrGlobal

def puntoAsterisco(arrCols, base, tablasColumna, pT,groupBy,tablaSimbolos):
    global useActual
    tupla = {"nombreC": [], "tipo": [], "valor": []}
    registros = []
    columnas = []
    for e in arrCols:
        ntabla=""
        for a in tablasColumna:
            if a.alias == e.tabla:
                ntabla=a.nombre
        registros.append(jBase.extractTable(useActual, ntabla))

        str_alias = ""
        if e.alias != False:
            str_alias = e.alias + "_"

        for nm in tablaSimbolos.get(useActual).getTabla(ntabla).get_name_list():
            columnas.append(str_alias + nm)
            tupla["nombreC"].append(str_alias + nm)
            tupla["tipo"].append(tablaSimbolos.get(useActual).getTabla(ntabla).getColumna(nm).tipo)

    resultado = []
    temporal = []

    resultado = registros[0]

    for t in range(len(registros) - 1):
        temporal = registros[t + 1]

        resultado = [(rs, tmp) for rs in resultado for tmp in temporal]
        arreglo_tmp = []
        for m in resultado:
            lista_tmp = []
            for m_2 in m:
                lista_tmp += m_2
            arreglo_tmp.append(lista_tmp)
        resultado = arreglo_tmp
    pT.field_names=columnas
    for r in resultado:
        pT.add_row(r)

def MathUnoSinWhere(arrCols, base, tablasColumna, pT,groupby):
    global consola
    arrIndices = []
    bande=False
    arrGlobal = []
    for e in arrCols:
        print("ADENTRO DEL MATH UNO")
        print(e.nombre)
        print(e.tipo)
        print(e.alias)
        print(e.param)
        print(e.tabla)
        tabla = ""
        bandd = False
        indice = None
        auxCons = ""
        if e.tabla == False and e.vtipo==Expresion.ID:
            for c in tablasColumna:
                tabla = base.getTabla(c.nombre)
                indice = tabla.getColumna(e.param)
                auxCons = jBase.extractTable(useActual, tabla.nombre)
                if indice != None:
                    bandd = True
                    break
        elif e.vtipo==Expresion.ID and e.tabla!=False:
            for a in tablasColumna:
                if a.alias == e.tabla:
                    tabla = base.getTabla(a.nombre)
                    indice = tabla.getColumna(e.param)
                    auxCons = jBase.extractTable(useActual, tabla.nombre)
                    if indice != None:
                        bandd = True
                        break
        else:
            val = Interpreta_Expresion(e.nodo, None, None)
            arrGlobal.append([str(val.valor)])
            bande = True

        if indice == None and not bande:
            listaSemanticos.append(Error.ErrorS("Error Semántico", "No se encontró la columna" + str(e.param)))
        elif not bande:
            if e.nombre.lower() == "abs":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arrIndices.append(i)
                    arr1.append(abs(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "cbrt":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arrIndices.append(i)
                    arr1.append((dato) ** (1 / 3))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "ceil":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(math.ceil(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "ceiling":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(math.ceil(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "degrees":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(math.degrees(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "exp":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(math.exp(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "factorial":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(math.factorial(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "floor":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(math.floor(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "ln":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(math.log(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "log":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(math.log10(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "radians":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(math.radians(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "round":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(round(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "sign":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    if dato >= 0:
                        arr1.append(1)
                    else:
                        arr1.append(-1)
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "sqrt":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(math.sqrt(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "trunc":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(math.trunc(dato))
                arrGlobal.append(arr1)
        bande=False

    if not groupby:
        n=0
        for xd in arrGlobal:
            pT.add_column(arrCols[n].alias + "(" + str(arrCols[n].param)+ ")", xd)
            n += 1
    else:
        pass
    return arrGlobal


def MathDosSinWhere(arrCols, base, tablasColumna, pT,groupby):
    global consola
    arrIndices = []
    arrGlobal = []
    bande = False
    for e in arrCols:
        tabla = ""
        tabla2 = ""
        bandd = False
        indice = None
        indice2 = None
        auxCons = ""
        auxCons2 = ""

        # indice 1
        if e.tabla == False and e.vtipo[0]==Expresion.ID:
            for c in tablasColumna:
                tabla = base.getTabla(c.nombre)
                indice = tabla.getColumna(e.param[0])
                auxCons = jBase.extractTable(useActual, tabla.nombre)
                if indice != None:
                    bandd = True
                    break
        elif e.vtipo[0]==Expresion.ID and e.tabla!=False:
            for a in tablasColumna:
                if a.alias == e.tabla[0]:
                    tabla = base.getTabla(a.nombre)
                    indice = tabla.getColumna(e.param[0])
                    auxCons = jBase.extractTable(useActual, tabla.nombre)
                    if indice != None:
                        bandd = True
                        break
        else:
            bande = True
        if indice == None and not bande:
            listaSemanticos.append(Error.ErrorS("Error Semántico", "No se encontró la columna" + e.param[0]))

        # indice 2
        if  e.tabla == False and e.vtipo[0]==Expresion.ID:
            for c in tablasColumna:
                tabla2 = base.getTabla(c.nombre)
                indice2 = tabla2.getColumna(e.param[1])
                auxCons2 = jBase.extractTable(useActual, tabla2.nombre)
                if indice2 != None:
                    bandd = True
                    break
        elif e.vtipo[0]==Expresion.ID and e.tabla!=False:
            for a in tablasColumna:
                if a.alias == e.tabla[1]:
                    tabla2 = base.getTabla(a.nombre)
                    indice2 = tabla2.getColumna(e.param[1])
                    auxCons2 = jBase.extractTable(useActual, tabla2.nombre)
                    if indice2 != None:
                        bandd = True
                        break
        else:
            val = Interpreta_Expresion(e.nodo, None, None)
            arrGlobal.append([str(val.valor)])
            bande = True

        if indice2 == None and not bande:
            listaSemanticos.append(Error.ErrorS("Error Semántico", "No se encontró la columna" + e.param[1]))
        elif not bande:
            indice = indice.index
            indice2 = indice2.index
            if e.nombre.lower() == "div":
                arrcc = []
                for i in range(len(auxCons)):
                    param = auxCons[i][indice]
                    param2 = auxCons2[i][indice2]
                    val = param2 // param
                    arrcc.append(val)
                arrGlobal.append(arrcc)
            elif e.nombre.lower() == "gcd":
                arrcc = []
                for i in range(len(auxCons)):
                    param = auxCons[i][indice]
                    param2 = auxCons2[i][indice2]
                    val = math.gcd(param, param2)
                    arrcc.append(val)
                arrGlobal.append(arrcc)
            elif e.nombre.lower() == "mod":
                arrcc = []
                for i in range(len(auxCons)):
                    param = auxCons[i][indice]
                    param2 = auxCons2[i][indice2]
                    val = param % param2
                    arrcc.append(val)
                arrGlobal.append(arrcc)
            elif e.nombre.lower() == "power":
                arrcc = []
                for i in range(len(auxCons)):
                    param = auxCons[i][indice]
                    param2 = auxCons2[i][indice2]
                    val = math.pow(param, param2)
                    arrcc.append(val)
                arrGlobal.append(arrcc)
            elif e.nombre.lower() == "round":
                arrcc = []
                for i in range(len(auxCons)):
                    param = auxCons[i][indice]
                    param2 = auxCons2[i][indice2]
                    val = round(param, param2)
                    arrcc.append(val)
                arrGlobal.append(arrcc)
        bande=False
    # x = PrettyTable()
    if not groupby:
        n = 0
        for xd in arrGlobal:
            print(arrCols[n].alias)
            pT.add_column(arrCols[n].alias + "(" +str(arrCols[n].param[0]) + "," + str(arrCols[n].param[1]) + ")", xd)
            n += 1
    # x.field_names = nombreCols
    # x.add_rows([arrGlobal])
    # consola += str(x) + "\n"
    return arrGlobal


def FechaSimple(arrCols, base, tablasColumna, pT,groupby):
    global consola
    arrGlobal = []
    for e in arrCols:

        if e.nombre.lower() == "pi":
            arr1 = []
            val = math.pi
            arr1.append(val)
            arrGlobal.append(arr1)
        elif e.nombre.lower() == "random":
            arr1 = []
            val = random()
            arr1.append(val)
            arrGlobal.append(arr1)
    if not groupby:
        n = 0
        for xd in arrGlobal:
            pT.add_column(arrCols[n].alias, xd)
            n += 1
    # x.field_names = nombreCols
    # x.add_rows([arrGlobal])
    #consola += str(x) + "\n"


def trigSinWhere(arrCols, base, tablasColumna, pT,groupby):
    global consola
    arrIndices = []
    arrGlobal = []
    bande = False
    for e in arrCols:
        tabla = ""
        bandd = False
        indice = None
        auxCons = ""
        if e.tabla == False and e.vtipo==Expresion.ID:
            for c in tablasColumna:
                tabla = base.getTabla(c.nombre)
                indice = tabla.getColumna(e.param)
                auxCons = jBase.extractTable(useActual, tabla.nombre)
                if indice != None:
                    bandd = True
                    break
        elif e.vtipo==Expresion.ID and e.tabla!=False:
            for a in tablasColumna:
                if a.alias == e.tabla:
                    tabla = base.getTabla(a.nombre)
                    indice = tabla.getColumna(e.param)
                    auxCons = jBase.extractTable(useActual, tabla.nombre)
                    if indice != None:
                        bandd = True
                        break
        else:
            val = Interpreta_Expresion(e.nodo, None, None)
            arrGlobal.append([str(val.valor)])
            bande = True

        if indice == None and not bande:
            listaSemanticos.append(Error.ErrorS("Error Semántico", "No se encontró la columna" + e.param))
        elif not bande:
            if e.nombre.lower() == "acos":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(math.acos(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "acosd":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    val = math.acos(dato)
                    arr1.append(math.degrees(val))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "asin":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(math.asin(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "asind":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    val = math.asin(dato)
                    arr1.append(math.degrees(val))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "atan":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(math.atan(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "atand":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    val = math.atan(dato)
                    arr1.append(math.degrees(val))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "cos":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(math.cos(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "cosd":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    val = math.cos(dato)
                    arr1.append(math.degrees(val))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "cot":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(1 / math.tan(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "cotd":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    val = 1 / math.tan(dato)
                    arr1.append(math.degrees(val))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "sin":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(math.sin(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "sind":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    val = math.sin(dato)
                    arr1.append(math.degrees(val))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "tan":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(math.tan(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "tand":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    val = math.tan(dato)
                    arr1.append(math.degrees(val))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "sinh":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(math.sinh(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "cosh":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(math.cosh(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "tan":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(math.tan(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "atanh":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(math.atanh(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "asinh":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(math.asinh(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "acosh":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(math.acosh(dato))
                arrGlobal.append(arr1)
        bande=False
    if not groupby:
        n=0
        for xd in arrGlobal:
            pT.add_column(arrCols[n].alias + "(" + str(arrCols[n].param) + ")", xd)
            n += 1
        # x.field_names = nombreCols
        # x.add_rows([arrGlobal])
        # consola += str(x)+"\n"

    return arrGlobal


def TrigDosSinWhere(arrCols, base, tablasColumna, pT, groupby):
    global consola
    arrIndices = []
    arrGlobal = []
    bande = False
    for e in arrCols:
        tabla = ""
        tabla2 = ""
        bandd = False
        indice = None
        indice2 = None
        auxCons = ""
        auxCons2 = ""

        # indice 1
        if e.tabla == False and e.vtipo[0]==Expresion.ID:
            for c in tablasColumna:
                tabla = base.getTabla(c.nombre)
                indice = tabla.getColumna(e.param[0])
                auxCons = jBase.extractTable(useActual, tabla.nombre)
                if indice != None:
                    bandd = True
                    break
        elif e.vtipo[0]==Expresion.ID and e.tabla!=False:
            for a in tablasColumna:
                if a.alias == e.tabla[0]:
                    tabla = base.getTabla(a.nombre)
                    indice = tabla.getColumna(e.param[0])
                    auxCons = jBase.extractTable(useActual, tabla.nombre)
                    if indice != None:
                        bandd = True
                        break
        else:
            bande = True

        if indice == None and not bande:
            listaSemanticos.append(Error.ErrorS("Error Semántico", "No se encontró la columna" + e.param[0]))

        # indice 2
        if e.tabla == False and e.vtipo[0]==Expresion.ID:
            for c in tablasColumna:
                tabla2 = base.getTabla(c.nombre)
                indice2 = tabla2.getColumna(e.param[1])
                auxCons2 = jBase.extractTable(useActual, tabla2.nombre)
                if indice2 != None:
                    bandd = True
                    break
        elif e.vtipo[0]==Expresion.ID and e.tabla!=False:
            for a in tablasColumna:
                if a.alias == e.tabla[1]:
                    tabla2 = base.getTabla(a.nombre)
                    indice2 = tabla2.getColumna(e.param[1])
                    auxCons2 = jBase.extractTable(useActual, tabla2.nombre)
                    if indice2 != None:
                        bandd = True
                        break
        else:
            val = Interpreta_Expresion(e.nodo, None, None)
            arrGlobal.append([str(val.valor)])
            bande = True

        if indice2 == None and not bande:
            listaSemanticos.append(Error.ErrorS("Error Semántico", "No se encontró la columna" + e.param[1]))

        elif not bande:
            indice = indice.index
            indice2 = indice2.index
            if e.nombre.lower() == "atan2":
                arrcc = []
                for i in range(len(auxCons)):
                    param = auxCons[i][indice]
                    param2 = auxCons2[i][indice2]
                    val = math.atan2(param, param2)
                    arrcc.append(val)
                arrGlobal.append(arrcc)
            elif e.nombre.lower() == "atan2d":
                arrcc = []
                for i in range(len(auxCons)):
                    param = auxCons[i][indice]
                    param2 = auxCons2[i][indice2]
                    val1 = math.atan2(param, param2)
                    val = math.degrees(val1)
                    arrcc.append(val)
                arrGlobal.append(arrcc)
        bande=False

    # x = PrettyTable()
    if not groupby:
        n = 0
        for xd in arrGlobal:
            pT.add_column(arrCols[n].alias + "(" + str(arrCols[n].param[0]) + "," + str(arrCols[n].param[1]) + ")", xd)
            n += 1
    # x.field_names = nombreCols
    # x.add_rows([arrGlobal])
    # consola += str(x) + "\n"
    return arrGlobal

def BinStringSinWhere(arrCols, base, tablasColumna, pT, groupby):
    global consola
    arrIndices = []
    arrGlobal = []
    bande = False
    for e in arrCols:
        tabla = ""
        bandd = False
        indice = None
        auxCons = ""
        if e.tabla == False and e.vtipo==Expresion.ID:
            for c in tablasColumna:
                tabla = base.getTabla(c.nombre)
                indice = tabla.getColumna(e.param)
                auxCons = jBase.extractTable(useActual, tabla.nombre)
                if indice != None:
                    bandd = True
                    break
        elif e.vtipo==Expresion.ID and e.tabla!=False:
            for a in tablasColumna:
                if a.alias == e.tabla:
                    tabla = base.getTabla(a.nombre)
                    indice = tabla.getColumna(e.param)
                    auxCons = jBase.extractTable(useActual, tabla.nombre)
                    if indice != None:
                        bandd = True
                        break
        else:
            val = Interpreta_Expresion(e.nodo, None, None)
            print(val.valor)
            arrGlobal.append([str(val.valor)])
            bande = True

        if indice == None and not bande:
            listaSemanticos.append(Error.ErrorS("Error Semántico", "No se encontró la columna" + str(e.param)))

        elif not bande:
            if e.nombre.lower() == "length":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arrIndices.append(i)
                    arr1.append(len(dato))
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "trim":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arrIndices.append(i)
                    v = str(dato)
                    d=v.replace(" ", "")
                    print(d)
                    arr1.append(d)
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "md5":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    val = hashlib.md5(str(dato).encode("utf-8")).hexdigest()
                    arr1.append(val)
                arrGlobal.append(arr1)
            elif e.nombre.lower() == "sha256":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    hs = hashlib.sha256(str(dato().encode('utf-8')).hexdigest())
                    arr1.append(val)
                arrGlobal.append(arr1)
            elif e.nombre == "|":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    print(dato)
                    arr1.append(math.sqrt(dato))
                arrGlobal.append(arr1)
            elif e.nombre == "||":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append((dato) ** (1 / 3))
                arrGlobal.append(arr1)
            elif e.nombre == "~":
                arr1 = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arr1.append(~int(dato))
                arrGlobal.append(arr1)
        bande=False

    if not groupby:
        n = 0
        for xd in arrGlobal:
            pT.add_column(arrCols[n].alias + "(" + str(arrCols[n].param) + ")", xd)
            n += 1
    else:
        return {"indices": arrIndices, "valore": arrGlobal}
            # x.field_names = nombreCols
            # x.add_rows([arrGlobal])
            # consola += str(x)+"\n"
    return arrGlobal

def BinDosStringSinWhere(arrCols, base, tablasColumna, pT, groupby):
    global consola
    arrIndices = []
    arrGlobal = []
    bande=False
    for e in arrCols:
        tabla = ""
        tabla2 = ""
        bandd = False
        indice = None
        indice2 = None
        auxCons = ""
        auxCons2 = ""

        # indice 1
        if e.tabla == False and e.vtipo[0]==Expresion.ID:
            for c in tablasColumna:
                tabla = base.getTabla(c.nombre)
                indice = tabla.getColumna(e.param[0])
                auxCons = jBase.extractTable(useActual, tabla.nombre)
                if indice != None:
                    bandd = True
                    break
        elif e.vtipo[0]==Expresion.ID and e.tabla!=False:
            for a in tablasColumna:
                if a.alias == e.tabla[0]:
                    tabla = base.getTabla(a.nombre)
                    indice = tabla.getColumna(e.param[0])
                    auxCons = jBase.extractTable(useActual, tabla.nombre)
                    if indice != None:
                        bandd = True
                        break
        else:
            bande = True
        if indice == None and not bande:
            listaSemanticos.append(Error.ErrorS("Error Semántico", "No se encontró la columna" + e.param[0]))

        # indice 2
        if e.tabla == False and e.vtipo[0]==Expresion.ID:
            for c in tablasColumna:
                tabla2 = base.getTabla(c.nombre)
                indice2 = tabla2.getColumna(e.param[1])
                auxCons2 = jBase.extractTable(useActual, tabla2.nombre)
                if indice2 != None:
                    bandd = True
                    break
        elif e.vtipo[0]==Expresion.ID and e.tabla!=False:
            for a in tablasColumna:
                if a.alias == e.tabla[1]:
                    tabla2 = base.getTabla(a.nombre)
                    indice2 = tabla2.getColumna(e.param[1])
                    auxCons2 = jBase.extractTable(useActual, tabla2.nombre)
                    if indice2 != None:
                        bandd = True
                        break
        else:
            val = Interpreta_Expresion(e.nodo, None, None)
            arrGlobal.append([str(val.valor)])
            bande = True
        if indice2 == None and not bande:
            listaSemanticos.append(Error.ErrorS("Error Semántico", "No se encontró la columna" + e.param[1]))

        elif not bande:
            indice = indice.index
            indice2 = indice2.index
            if e.nombre == "&":
                arrcc = []
                for i in range(len(auxCons)):
                    param = auxCons[i][indice]
                    param2 = auxCons2[i][indice2]
                    val = param & param2
                    arrcc.append(val)
                arrGlobal.append(arrcc)
            elif e.nombre == "|":
                arrcc = []
                for i in range(len(auxCons)):
                    param = auxCons[i][indice]
                    param2 = auxCons2[i][indice2]
                    val = param | param2
                    arrcc.append(val)
                arrGlobal.append(arrcc)
            elif e.nombre == "?":
                arrcc = []
                for i in range(len(auxCons)):
                    param = auxCons[i][indice]
                    param2 = auxCons2[i][indice2]
                    val = param ^ param2
                    arrcc.append(val)
                arrGlobal.append(arrcc)
            elif e.nombre == "<<":
                arrcc = []
                for i in range(len(auxCons)):
                    param = auxCons[i][indice]
                    param2 = auxCons2[i][indice2]
                    val = param << param2
                    arrcc.append(val)
                arrGlobal.append(arrcc)
            elif e.nombre == ">>":
                arrcc = []
                for i in range(len(auxCons)):
                    param = auxCons[i][indice]
                    param2 = auxCons2[i][indice2]
                    val = param >> param2
                    arrcc.append(val)
                arrGlobal.append(arrcc)
            elif e.nombre.lower() == "convert":
                arrcc = []
                for i in range(len(auxCons)):
                    param = auxCons[i][indice]
                    param2 = auxCons2[i][indice2]
                    val = param >> param2
                    arrcc.append(val)
                arrGlobal.append(arrcc)
            elif e.nombre.lower() == "decode":
                arrcc = []
                for i in range(len(auxCons)):
                    param = auxCons[i][indice]
                    param2 = auxCons2[i][indice2]
                    val = param >> param2
                    arrcc.append(val)
                arrGlobal.append(arrcc)
        bande=False

    # x = PrettyTable()
    if not groupby:
        n = 0
        for xd in arrGlobal:
            pT.add_column(arrCols[n].alias + "(" + str(arrCols[n].param[0]) + "," + str(arrCols[n].param[1]) + ")", xd)
            n += 1
    # x.field_names = nombreCols
    # x.add_rows([arrGlobal])
    # consola += str(x) + "\n"
    return arrGlobal

def agregacionSinWhere(arrCols, base, tablasColumna, pT,subconsulta,groupBy):
    global consola
    band = False
    for e in arrCols:
        if e.tipo != 1:
            band = True
            break

    arrGlobal = []

    if not band:
        for e in arrCols:
            tabla = ""
            bandd = False
            indice = None
            auxCons = ""
            if e.tabla == False:
                for c in tablasColumna:
                    tabla = base.getTabla(c.nombre)
                    indice = tabla.getColumna(e.param)
                    auxCons = jBase.extractTable(useActual, tabla.nombre)
                    if indice != None:
                        bandd = True
                        break
            else:
                for a in tablasColumna:
                    if a.alias == e.tabla:
                        tabla = base.getTabla(a.nombre)
                        indice = tabla.getColumna(e.param)
                        auxCons = jBase.extractTable(useActual, tabla.nombre)
                        if indice != None:
                            bandd = True
                            break
            if indice == None:
                listaSemanticos.append(Error.ErrorS("Error Semántico", "No se encontró la columna" + e.nombre))

            if e.nombre.lower() == "sum":
                suma = 0
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    suma += int(dato)
                arrGlobal.append([str(suma)])
            elif e.nombre.lower() == "count":
                cont = 0
                for e in auxCons:
                    cont += 1
                arrGlobal.append([str(cont)])
            elif e.nombre.lower() == "avg":
                suma = 0
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    suma += int(dato)
                arrGlobal.append([str(suma / len(auxCons))])
            elif e.nombre.lower() == "min":
                arrMin = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arrMin.append(int(dato))
                arrGlobal.append([str(min(arrMin))])

            elif e.nombre.lower() == "max":
                arrMax = []
                for i in range(len(auxCons)):
                    dato = auxCons[i][indice.index]
                    arrMax.append(int(dato))
                arrGlobal.append([str(max(arrMax))])

        # x = PrettyTable()
        n = 0
        for xd in arrGlobal:
            pT.add_column(arrCols[n].alias + "(" + arrCols[n].param + ")", xd)
            n += 1
        # consola += str(x)+"\n"

    else:
        if groupBy !=None:
            n = 0
            arrgroup=[]
            for e in arrCols:
                tabla = ""
                bandd = False
                indice = None
                auxCons = ""
                if e.tipo == 0:
                    arrgroup.append(columnaEspecificaSinWhere([e], base, tablasColumna, pT,True))
                elif e.tipo == 2:
                    MathUnoSinWhere([e], base, tablasColumna, pT,True)
                elif e.tipo == 3:
                    trigSinWhere([e], base, tablasColumna, pT,True)
                elif e.tipo == 4:
                    consultaSimple([e], pT,True)
                elif e.tipo == 5:
                    MathDosSinWhere([e], base, tablasColumna, pT,True)
        else:
            listaSemanticos.append(Error.ErrorS("Error semantico","Falta el group by en la consulta"))


def SubstrSinWhere(arrCols, base, tablasColumna, pT,groupby):
    global consola
    global d1,d2
    arrIndices = []
    arrGlobal = []
    indice = None
    for e in arrCols:
        tabla = ""
        bandd = False
        auxCons = ""
        if e.tabla == False:
            for c in tablasColumna:
                tabla = base.getTabla(c.nombre)
                if isinstance(e.param,SExpresion):
                    indice = tabla.getColumna(e.param.valor)
                else: 
                    indice = tabla.getColumna(e.param.index)
                auxCons = jBase.extractTable(useActual, tabla.nombre)
                if indice != None:
                    bandd = True
                    break
        else:
            for a in tablasColumna:
                if a.alias == e.tabla:
                    tabla = base.getTabla(a.nombre)
                    if isinstance(e.param,SExpresion):
                        indice = tabla.getColumna(e.param.valor)
                    else: 
                        indice = tabla.getColumna(e.param)
                    auxCons = jBase.extractTable(useActual, tabla.nombre)
                    if indice != None:
                        bandd = True
                        break
        if indice == None:
            listaSemanticos.append(Error.ErrorS("Error Semántico", "No se encontró la columna" + str(e.param.valor)))

        if e.nombre.lower() == "substr":
            arr1 = []
            for i in range(len(auxCons)):
                dato = auxCons[i][indice.index]
                arrIndices.append(i)
                val1 = str(dato)
                inicio = int(d1)
                fin = int(d2)
                val = val1[inicio:fin]
                arr1.append(val)
            arrGlobal.append(arr1)
        
        if not groupby:
            n=0
            for xd in arrGlobal:
                if isinstance(arrCols[n].param,SExpresion):
                    pT.add_column(arrCols[n].alias + "(" + arrCols[n].param.valor + ")", xd)
                else:
                    pT.add_column(arrCols[n].alias + "(" + arrCols[n].param + ")", xd)
                n += 1
        else:
            return {"indices": arrIndices, "valore": arrGlobal}
        
        return arrGlobal
        # x.field_names = nombreCols
        # x.add_rows([arrGlobal])
        # consola += str(x)+"\n"
   