#from Instrucciones.instruccion import Instruccion
from Analisis_Ascendente.Instrucciones.instruccion import *
#from storageManager.jsonMode import *
from Analisis_Ascendente.storageManager.jsonMode import *
#import Tabla_simbolos.TablaSimbolos as ts
import Analisis_Ascendente.Tabla_simbolos.TablaSimbolos as TS
from Analisis_Ascendente.Instrucciones.Select.select import *
import Analisis_Ascendente.Instrucciones.Select as Select
from Analisis_Ascendente.Instrucciones.expresion import *
from Analisis_Ascendente.Instrucciones.Expresiones.IdAsId import IdAsId
from Analisis_Ascendente.Instrucciones.Time import  Time
from Analisis_Ascendente.Instrucciones.Expresiones.Math import Math_
from prettytable import PrettyTable

class Select_Dist(Instruccion):

    def __init__(self):
        vairable = 4


    def ejecutar(y,Select,ts,consola,exceptions):


        insert('prueba1', 'tabla1', [1, 'Fredy', 'Ramirez'])
        insert('prueba1', 'tabla1', [2, 'Mauro', 'Martinez'])
        insert('prueba1', 'tabla1', [3, 'Javier', 'Lima'])
        insert('prueba1', 'tabla1', [4, 'Yisus', 'Yisusx2'])
        insert('prueba1', 'tabla1', [5, 'Jacks', 'Wade'])
        insert('prueba1', 'tabla1', [6, 'Jacks', 'Wade'])
        insert('prueba1', 'tabla1', [3, 'Javier', 'Lima'])
        insert('prueba1', 'tabla1', [1, 'Fredy', 'Ramirez'])

        insert('prueba1', 'tabla2', [1, 'Mario', 'Guatemala', 'Contabilidad'])
        insert('prueba1', 'tabla2', [2, 'Jorge', 'Dubai', 'Programador'])
        insert('prueba1', 'tabla2', [3, 'Pepe', 'Brasil', 'Contabilidad'])
        insert('prueba1', 'tabla2', [4, 'Fredy', 'Noruega', 'Jefe'])
        insert('prueba1', 'tabla2', [5, 'Juan', 'Italia', 'Desarollador'])

        insert('prueba1', 'tabla3', [1, 'Sic', 'USA', '4av. km 19.3'])
        insert('prueba1', 'tabla3', [2, 'Pepe', 'Irak', 'en amatitlan ese'])
        insert('prueba1', 'tabla3', [3, 'Etesech', 'China', 'perdido'])
        insert('prueba1', 'tabla3', [4, 'ufuefue', 'Japon', 'Selva'])
        insert('prueba1', 'tabla3', [5, 'osas', 'Venezuela', 'Jungla'])
        print("entro en selectinst2")
        #x = PrettyTable()




        ejemplo = opcion(Select,ts,consola,exceptions)
        #print('Antes del final')
        #print(ejemplo)
        #print('LLEGUE AL FINAL ')
        return ejemplo



def opcion(Select,ts,consola,exceptions):
    listaSubquery = []
    listaCampoOficial = []

    listCampos2 = []
    listaCamposIndice = []
    x = PrettyTable()
    consolaAux=[]
    if ts.validar_sim("usedatabase1234") == 1:
        listaCamposIndice.clear()
        bdactual = ts.buscar_sim("usedatabase1234")
        BD = ts.buscar_sim(bdactual.valor)
        entornoBD = BD.Entorno
        listaTablas = entornoBD.simbolos
        contador = -1
        contador2 = -1
        auxExisteT = False
        if Select.columnas == '*': #COMPARO SI SOLO VIENE UN ASTERISCO EN COLUMNAS
            # LLEVARLO A UN METODO
            if isinstance(Select.inner, GroupBy):
                listaAuxiliarC = []
                '''for tmp  in Select.inner.listaC:
                    if isinstance(tmp,Id):
                        print(tmp.id)
                    elif isinstance(tmp,IdId):
                        pass
                    elif isinstance(tmp,IdAsId):
                        pass

                if isinstance(Select.inner.compGroup, Having):
                    for tmp in Select.inner.compGroup.lista:
                        if isinstance(tmp,Id):
                            print(tmp.id)'''
                datos_columnas = []
                listaTmp = []
                index_2 = 0
                if isinstance(Select.inner.compGroup, Having):
                    nuevoCampo = obtenerCamposGroup(listaTablas, Select, bdactual)
                    index_2 = -1
                    for tmp in Select.inner.compGroup.lista:
                        if isinstance(tmp, Id):  # OBTENGO EL VALOR QUE A LA PAR DEL GROUP BY
                            index_2 = existeCampo(tmp.id, nuevoCampo[0], listaTmp)[1]  ##-------> OBTENGO LA POSICION DEL CAMPO

                registro = []
                for tmp in Select.inner.listaC:
                    if isinstance(tmp, Id):
                        for elemento in listaTablas:
                            if str(tmp.id) == listaTablas.get(elemento).id:
                                registro = extractTable(bdactual.valor,str(tmp.id))  # ------>> OBTENGO LOS VALORES DE LA TABLA


                for tupla in registro:

                    contador_aux = 0

                    for aux in tupla:

                        if index_2 == contador_aux:
                            if groupby(tupla, datos_columnas, index_2):
                                datos_columnas.append(tupla)

                        contador_aux += 1
                #print(datos_columnas)  #----> lista que contiene tuplas del group by
                for tabl in Select.inner.listaC:  # VEO LA OPCIONES QUE PUEDEN VENIR EN LA DECLARACION DE TABLAS
                    existeTablas = False
                    if isinstance(tabl, Id):
                        auxExisteT = IDGr(x, tabl, bdactual, listaTablas, listCampos2, contador2, consolaAux,existeTablas,datos_columnas,listaSubquery,listaAuxiliarC)
                        # print(auxExisteT)
                        if auxExisteT:
                            pass
                        else:
                            break

                listaCampoOficial.extend(listaDeListas(listaAuxiliarC))
                if Select.orderby != None:
                    pass
                else:
                    consola.append('\n' + x.get_string() + '\n')
                    x.clear()
                #consola.append('\n' + x.get_string() + '\n')
                #listaCampoOficial.extend(listaDeListas(listaAuxiliarC))
                #print(listaCampoOficial)
                #x.clear()
            else:
                listaAuxiliarC = []
                listaNumeros = []
                duplicado = 0
                contadorTmp = 0

                #for campo in Select.inner:
                while contadorTmp != 100:
                    listaNumeros.append(0)
                    contadorTmp += 1

                repetido = []
                for tabl in Select.inner:
                    if isinstance(tabl, Id):
                        listaAux = existeCampo(tabl.id, listaTablas,repetido)
                        print(listaAux[0])
                        print(listaAux[1])
                        if (listaAux[0]):
                            listaNumeros[listaAux[1]] += 1

                for aux in listaNumeros:  # busca si hay campos duplicados
                    # print(aux)
                    if aux > 1:
                        duplicado += 1

                if duplicado == 0:
                    listTExiste = []
                    listTNoExiste = []
                    for tabl in Select.inner:
                        listTNoExiste.append(tabl.id)
                    for tabl in Select.inner: #VEO LA OPCIONES QUE PUEDEN VENIR EN LA DECLARACION DE TABLAS
                        existeTablas = False
                        if isinstance(tabl, Id):
                            auxExisteT =  ID(x,tabl,bdactual,listaTablas,listCampos2,contador2,consolaAux,existeTablas,listTExiste,listaSubquery,listaAuxiliarC)
                            #print(auxExisteT)
                            if auxExisteT:
                                pass
                            else:
                                break

                        elif isinstance(tabl, IdId):
                            print(tabl.id1.id)
                        elif isinstance(tabl, IdAsId):
                            pass
                            # Agregar Metodo
                    if auxExisteT:  # mostrar tablas si es true

                        listaCampoOficial.extend(listaDeListas(listaAuxiliarC))
                        if Select.orderby != None:
                            pass
                        else:
                            #consolaAux.clear()
                            x.clear()
                            mostrar = []
                            aux1 = listaCampoOficial
                            for n in listaCampoOficial:
                                if validar_distinct(n, aux1) == 1:
                                    mostrar.append(n)
                                    print(n)
                                else:
                                    cont = 0
                                    for reco in mostrar:

                                        if n == reco:
                                            cont = 2
                                            break
                                        else:
                                            cont = 1

                                    if cont == 1:
                                        mostrar.append(n)
                            registro = mostrar
                            imprimir_Tabla(Select, registro, listaSubquery, x)
                            consola.append('\n' + x.get_string())
                            #consola.extend(consolaAux)

                    else:
                        errores = Diff(listTExiste,listTNoExiste)
                        for err in errores:
                            consola.append(f"42P01 	undefined_table, Tabla no existe -> '{err}'") #NO EXISTE TABLAS
                            exceptions.append(f"Error semantico-42P01 	undefined_table, Tabla no existe '{err}'")
                        consolaAux.clear()
                else:
                    repetido2 = Repeat(repetido)
                    for dup in repetido2:
                        consola.append(f"42P07 	duplicate_table ,Tabla duplicada -> '{dup}'")
                        exceptions.append(f"Error semantico-42P07 	duplicate_table, Tabla duplicada '{dup}'")


                # consola.append('\n'+x.get_string())
        else: # BUSCAR TODAS LAS OPCIONES QUE PUEDE VENIR EN COLUMNAS
            if isinstance(Select.inner,GroupBy): #----------------------------------------> GROUP BY
                listaAuxiliarC = []
                datos_columnas = []
                listaTmp = []
                if isinstance(Select.inner.compGroup, Having):
                    nuevoCampo = obtenerCamposGroup(listaTablas, Select, bdactual)
                    index_2 = -1
                    for tmp in Select.inner.compGroup.lista:
                        if isinstance(tmp, Id): # OBTENGO EL VALOR QUE A LA PAR DEL GROUP BY
                            index_2 = existeCampo(tmp.id,nuevoCampo[0],listaTmp)[1]  ##-------> OBTENGO LA POSICION DEL CAMPO



                    registro = []
                    for tmp in Select.inner.listaC:
                        if isinstance(tmp, Id):
                            for elemento in listaTablas:
                                if str(tmp.id) == listaTablas.get(elemento).id:
                                    registro = extractTable(bdactual.valor,str(tmp.id)) #------>> OBTENGO LOS VALORES DE LA TABLA

                    for tupla in registro:

                        contador_aux = 0

                        for aux in tupla:

                            if index_2 == contador_aux:
                                if groupby(tupla, datos_columnas, index_2):
                                    datos_columnas.append(tupla)

                            contador_aux += 1
                    #print(datos_columnas)  ----> lista que contiene tuplas del group by

                for col in Select.columnas:

                    if isinstance(col, Id):
                        for tmp in Select.inner.compGroup.lista:
                            if isinstance(tmp, Id):
                                validar = IdSimpleG(Select, listaTablas, bdactual,datos_columnas, x, listCampos2, col, tmp,listaSubquery,listaAuxiliarC)
                                if validar:
                                    consola.append('42725 	ambiguous_function, Existe una ambiguedad')
                                    exceptions.append('Error semantico-42725 	ambiguous_function, Existe una ambiguedad')
                                    break
                                else:
                                    pass
                listaCampoOficial.extend(listaDeListas(listaAuxiliarC))
                if Select.orderby != None:
                    pass
                else:

                    # print(listaCampoOficial)
                    # listaCamposIndice.append(listaDeListas(listaAuxiliarC))
                    consola.append('\n' + x.get_string() + '\n')
                    x.clear()
                #consola.append('\n' + x.get_string() + '\n')
                #listaCampoOficial.extend(listaDeListas(listaAuxiliarC))
                #print(listaCampoOficial)
                #x.clear()
            else:
                nuevoCampo = obtenerCampos(listaTablas,Select,bdactual)
                siExiste = 0
                aux=[]
                listaCampos2 = []

                for colAux in Select.columnas:
                    if isinstance(colAux, Id): # LLENAR LA TABLA DE COLUMNAS CUANDO SOLO VIENE ID
                        listaCampos2.append(colAux.id)

                for col2 in Select.columnas: #busca si el campo existe
                    if isinstance(col2,Id):
                        if nuevoCampo != None:
                            noExiste = existeCampo(col2.id, nuevoCampo[0],aux)
                            if noExiste[0]:
                                pass
                            else:
                                siExiste += 1
                listaNumeros = []
                duplicado = 0
                listaAux2 = []
                if nuevoCampo != None:
                    for campo in nuevoCampo[0]:
                        listaNumeros.append(0)
                        # contador += 1

                    for col in Select.columnas:
                        if isinstance(col, Id):
                            listaAux = existeCampo(col.id, nuevoCampo[0],listaAux2)
                            if (listaAux[0]):
                                listaNumeros[listaAux[1]] += 1

                    for aux in listaNumeros: #busca si hay campos duplicados
                        #print(aux)
                        if aux > 1:
                            duplicado += 1

                idSimpleCont = 0
                listaIdsAux = []
                #for tablAux in Select.inner:

                listaTmp = (BuscarTBIdId(Select, listaTablas))
                listaTmp2 = (BuscarTBIdId2(Select, listaTablas))
                listaAuxiliarC = []
                if siExiste == 0:
                    if duplicado == 0:
                        for col in Select.columnas:
                            if isinstance(col, Id):
                                validar = IdSimple(Select, listaTablas, bdactual, contador2, x, listCampos2, col,listaAuxiliarC,listaSubquery)
                                if validar:
                                    consola.append('42725 	ambiguous_function, Existe una ambiguedad')
                                    exceptions.append('Error semantico-42725 	ambiguous_function, Existe una ambiguedad')
                                    break
                                else:
                                    pass

                            elif isinstance(col, IdId):
                                tmpLista =[]
                                for nombreTabla in listaTmp2[0]:
                                    auxTmp = BuscarColumnasLQVP(nombreTabla['Tabla'].id, col, listaTablas,nombreTabla['Tabla'].id)
                                    tmpLista.append(auxTmp)

                                for nombreTabla in listaTmp2[0]:
                                    auxTmp = BuscarColumnasLQVP4(nombreTabla['Tabla'].id, col, listaTablas,nombreTabla['Tabla'].id)
                                    tmpLista.append(auxTmp)

                                for nombreTabla in listaTmp[0]:
                                    auxTmp = BuscarColumnasLQVP(nombreTabla['Tabla'].id, col, listaTablas,nombreTabla['Alias'])
                                    tmpLista.append(auxTmp)

                                for nombreTabla in listaTmp[0]:
                                    auxTmp = BuscarColumnasLQVP3(nombreTabla['Tabla'].id, col, listaTablas,nombreTabla['Alias'])
                                    tmpLista.append(auxTmp)


                                for lp in tmpLista:

                                    for alias in listaTmp[0]:
                                        if lp != None:
                                            if(lp['LQBP']==alias['Alias'] and lp['Columna']=='*'):
                                                TablaCompleta(x, bdactual, alias['Tabla'].id, listaTablas,listaSubquery,listaAuxiliarC)
                                            elif(lp['LQBP']==alias['Alias']):
                                                IdIdp(x, col, listCampos2, listaTablas, bdactual, alias['Tabla'].id,listaSubquery,listaAuxiliarC)


                                    for alias in listaTmp2[0]:
                                        if lp != None:
                                            if(lp['LQBP'] == alias['Tabla'].id and lp['Columna']=='*'):
                                                TablaCompleta(x, bdactual, alias['Tabla'].id, listaTablas,listaSubquery,listaAuxiliarC)
                                            elif lp['LQBP'] == alias['Tabla'].id:
                                                IdIdp(x, col, listCampos2, listaTablas, bdactual, alias['Tabla'].id,listaSubquery,listaAuxiliarC)



                            elif isinstance(col, IdAsId):

                                if isinstance(col.id1,Id):
                                    IdSimple2(Select, listaTablas, bdactual, x, listCampos2, col.id1, col.id2.id,listaSubquery,listaAuxiliarC)
                                elif isinstance(col.id1,IdId):
                                    # print(col.id1.id1.id)
                                    # print(col.id1.id2.id)
                                    tmpLista = []
                                    for nombreTabla in listaTmp2[0]:
                                        auxTmp = BuscarColumnasLQVP5(nombreTabla['Tabla'].id, col, listaTablas,
                                                                    nombreTabla['Tabla'].id)
                                        tmpLista.append(auxTmp)


                                    for nombreTabla in listaTmp[0]:
                                        auxTmp = BuscarColumnasLQVP5(nombreTabla['Tabla'].id, col, listaTablas,
                                                                    nombreTabla['Alias'])
                                        tmpLista.append(auxTmp)

                                    for lp in tmpLista:

                                        for alias in listaTmp[0]:
                                            if lp != None:
                                                if (lp['LQBP'] == alias['Alias']):
                                                    print('ENTRO EN LA OPCION DEL ALIAS ')
                                                    IdIdp2(x, col, listCampos2, listaTablas, bdactual, alias['Tabla'].id,col.id2.id,listaSubquery,listaAuxiliarC)

                                        for alias in listaTmp2[0]:
                                            if lp != None:
                                                if lp['LQBP'] == alias['Tabla'].id:
                                                    print('ENTRO EN LA OPCION LA TABLA ')
                                                    IdIdp2(x, col, listCampos2, listaTablas, bdactual, alias['Tabla'].id,col.id2.id,listaSubquery,listaAuxiliarC)


                                #print(col.id2.id)

                            elif isinstance(col,Math_):
                                pass
                        #print(listaDeListas(listaAuxiliarC))
                        listaCampoOficial.extend(listaDeListas(listaAuxiliarC))
                        if Select.orderby != None:
                            pass
                        else:
                            x.clear()
                            mostrar = []
                            aux1 = listaCampoOficial
                            for n in listaCampoOficial:
                                if validar_distinct(n, aux1) == 1:
                                    mostrar.append(n)
                                    print(n)
                                else:
                                    cont = 0
                                    for reco in mostrar:

                                        if n == reco:
                                            cont = 2
                                            break
                                        else:
                                            cont = 1

                                    if cont == 1:
                                        mostrar.append(n)
                            registro = mostrar
                            imprimir_Tabla(Select,registro,listaSubquery,x)
                            consola.append('\n' + x.get_string() + '\n')

                    else:
                        #print("aqui")
                        repetido2 = Repeat(listaAux2)
                        for dup in repetido2:
                            consola.append(f"42701 	duplicate_column,Campos duplicados '{dup}' ")
                            exceptions.append("Error semantico-42701 	duplicate_column-Campos duplicados DB-fila-columna")
                        return
                else:
                    prueba = Diff(listaCampos2,listaAux2)
                    for pr in prueba:
                        consola.append(f"42703 	undefined_column, Campo no existe '{pr}'")
                        exceptions.append("Error semantico-42703 	undefined_column-Campo no existe DB-fila-columna")
                    return
        #print(listaSubquery)

        if Select.orderby != None: ##-------------------------------------->>> ORDER BY
            pass
            for nm in Select.orderby:
                if isinstance(nm, Id):
                    indexG = buscar_infice(nm.id, listaSubquery)
                    registro = sorted(listaCampoOficial, key=lambda i: str(i[indexG]).lower())
                    imprimir_Tabla(Select,registro,listaSubquery,x)
            consola.append('\n' + x.get_string() + '\n')
            x.clear()

            #if isinstance(Select.orderby,Id):
             #   print('-----------------')
              #  print(Select.orderby.id)
               # print('-----------------')
            #elif isinstance(Select.orderby,)


            #indexG = buscar_infice(auxOrder_by.valor[0], listaSubquery)


            #if Select.orderby == 'ASC':
            #registro = sorted(listaCampoOficial, key=lambda i: str(i[indexG]).lower())
            #elif Select.orderby == 'DESC':
             #   registro = sorted(listaCampoOficial, key=lambda i: str(i[indexG]).lower(), reverse=True)
            #print('POR AQUI')
            #print(listaSubquery)
            #print(listaCampoOficial)
            #print('AQUI TAMBIEN ')
    else:
        consola.append("22005	error_in_assignment, No se ha seleccionado una BD\n")
        exceptions.append("Error semantico-22005	error_in_assignment-No se ha seleccionado DB-fila-columna")
    return listaCampoOficial


    # for col in Select.columnas:
    #   for


def IdSimple(Select,listaTablas,bdactual,contador2,x,listCampos2,col,listaAuxiliarC,sub):
    lista = obtenerCampos(listaTablas,Select,bdactual)

    if lista != None:

        listaCamposJson = extractTable(bdactual.valor,str(lista[1].id))  # OBTENGO LOS DATOS DENTRO DE LA TABLA
        #contador = 0
        auxCont = 0
        for tmp in Select.inner:
            auxCont += 1
        if auxCont == 1:
            contador = -1
            for campo in lista[0]:  # RECORRO LOS NOMBRES DE LOS CAMPOS DE LA TS
                listCampos2.clear()  # LIMPIO LA LISTA DONDE ALMACENARE LOS DATOS DE CADA COLUMNA
                contador +=1  # INDICA LA POSICION DE LA COLUMNA DONDE OBTENGO LOS VALORES
                if (col.id == lista[0].get(campo).id):
                    auxiliarColumna = []
                    for col2 in listaCamposJson:  # RECORRO LOS DATOS DE LA TABLA DE SIMBOLOS
                        auxiliarColumna.append(col2[contador])
                        listCampos2.append(str(col2[contador]))
                    x.add_column(lista[0].get(campo).id, listCampos2)  # AGREGO UNA COLUMNA
                    listaAuxiliarC.append(auxiliarColumna)
                    sub.append(lista[0].get(campo).id)

            #listaCamposJson = metodo_sis(listaAuxiliarC)
            return False
        else:
            #consola.append('ERROR SEMANTICO DOS TABLAS DECLARADAS')
            return True
    else:
        x.clear()
        return True

        #consola.append("ERROR SEMANTICO AQUI EN IDSIMPLE")





def IdSimpleG(Select,listaTablas,bdactual,listaAux,x,listCampos2,col,groups,sub,listaAuxiliarC):
    lista = obtenerCampos(listaTablas,Select,bdactual)
    lista2 = listaAux
    validar = True
    if lista != None:
        listaCamposJson = extractTable(bdactual.valor,str(lista[1].id))  # OBTENGO LOS DATOS DENTRO DE LA TABLA
        #contador = 0
        auxCont = 0
        for tmp in Select.inner.listaC:
            auxCont += 1
        if auxCont == 1:
            contador = -1
            for campo in lista[0]:  # RECORRO LOS NOMBRES DE LOS CAMPOS DE LA TS
                listCampos2.clear()  # LIMPIO LA LISTA DONDE ALMACENARE LOS DATOS DE CADA COLUMNA
                contador +=1  # INDICA LA POSICION DE LA COLUMNA DONDE OBTENGO LOS VALORES
                auxiliarColumna = []
                if (col.id == groups.id):
                    for tr in lista2:
                        print(tr[contador])
                        listCampos2.append(tr[contador])
                        auxiliarColumna.append(tr[contador])
                        validar = False
                #if verficarRepetidos(listCampos2):#VERIFICA SI SE REPITE ELEMENTO
                 #   listaAux = Repeat(listCampos2)
                  #  x.add_column(lista[0].get(campo).id, listaAux)
                #else:
                x.add_column(lista[0].get(campo).id, listCampos2)  # AGREGO UNA COLUMNA
                listaAuxiliarC.append(auxiliarColumna)
                sub.append(lista[0].get(campo).id)
            return validar
        else:
            #consola.append('ERROR SEMANTICO DOS TABLAS DECLARADAS')
            sub.clear()
            return validar
    else:
        x.clear()
        return validar

        #consola.append("ERROR SEMANTICO AQUI EN IDSIMPLE")


def IdSimple2(Select,listaTablas,bdactual,x,listCampos2,col,alias,sub,listaAuxiliarC):
    lista = obtenerCampos(listaTablas,Select,bdactual)

    listaCamposJson = extractTable(bdactual.valor,str(lista[1].id))  # OBTENGO LOS DATOS DENTRO DE LA TABLA
    #contador = 0

    contador = -1
    for campo in lista[0]:  # RECORRO LOS NOMBRES DE LOS CAMPOS DE LA TS
        listCampos2.clear()  # LIMPIO LA LISTA DONDE ALMACENARE LOS DATOS DE CADA COLUMNA
        contador +=1  # INDICA LA POSICION DE LA COLUMNA DONDE OBTENGO LOS VALORES
        if (col.id == lista[0].get(campo).id):
            auxiliarColumna = []
            for col2 in listaCamposJson:  # RECORRO LOS DATOS DE LA TABLA DE SIMBOLOS
                listCampos2.append(col2[contador])
                auxiliarColumna.append(col2[contador])
            #if verficarRepetidos(listCampos2):#VERIFICA SI SE REPITE ELEMENTO
             #   listaAux = Repeat(listCampos2)
              #  x.add_column(lista[0].get(campo).id, listaAux)
            #else:
            x.add_column(alias, listCampos2)  # AGREGO UNA COLUMNA
            listaAuxiliarC.append(auxiliarColumna)
            sub.append(lista[0].get(campo).id)
def existeCampo(cadena,lista,repetido):
    contador = 0
    for campo in lista:
        if cadena == lista.get(campo).id:
            repetido.append(cadena)
            return [True,contador]
        contador += 1
    return [False,contador]



def obtenerCampos(listaTablas,Select,bdactual):
    if isinstance(Select.inner,GroupBy):
        for tabl in Select.inner.listaC:
            contador = 0
            for elemento in listaTablas:  # RECORRO LAS TABLAS DE LA TS
                # contador2 = contador2 + 1
                if isinstance(tabl, Id):
                    if tabl.id == listaTablas.get(
                            elemento).id:  # COMPARO SI EL NOMBRE ESCRITO DE LA TABLA ES IGUAL EN LAS TABLAS DEL TS
                        listaCamposJson = extractTable(bdactual.valor,str(tabl.id))  # OBTENGO LOS DATOS DENTRO DE LA TABLA
                        entornoTabla = listaTablas.get(elemento).Entorno
                        campos = entornoTabla.simbolos  # obtengo los campos de la tabla de simbolos
                        return [campos, tabl, contador]
                    contador += 1
                '''elif isinstance(tabl,IdAsId):
                    if tabl.id1.id == listaTablas.get(elemento).id:
                        entornoTabla = listaTablas.get(elemento).Entorno
                        campos = entornoTabla.simbolos
                        return [campos, tabl, contador]
                    contador += 1'''

        return None
    else:
        for tabl in Select.inner:
            contador = 0
            for elemento in listaTablas:  # RECORRO LAS TABLAS DE LA TS
                # contador2 = contador2 + 1
                if isinstance(tabl, Id):
                    if tabl.id == listaTablas.get(
                            elemento).id:  # COMPARO SI EL NOMBRE ESCRITO DE LA TABLA ES IGUAL EN LAS TABLAS DEL TS
                        listaCamposJson = extractTable(bdactual.valor,
                                                       str(tabl.id))  # OBTENGO LOS DATOS DENTRO DE LA TABLA
                        entornoTabla = listaTablas.get(elemento).Entorno
                        campos = entornoTabla.simbolos  # obtengo los campos de la tabla de simbolos
                        return [campos, tabl, contador]
                    contador += 1
                '''elif isinstance(tabl,IdAsId):
                    if tabl.id1.id == listaTablas.get(elemento).id:
                        entornoTabla = listaTablas.get(elemento).Entorno
                        campos = entornoTabla.simbolos
                        return [campos, tabl, contador]
                    contador += 1'''

        return None
def obtenerCamposG(listaTablas,Select,bdactual):
    for tabl in Select.inner.listaC:
        contador = 0
        for elemento in listaTablas:  # RECORRO LAS TABLAS DE LA TS
            # contador2 = contador2 + 1
            if isinstance(tabl, Id):
                if tabl.id == listaTablas.get(elemento).id:  # COMPARO SI EL NOMBRE ESCRITO DE LA TABLA ES IGUAL EN LAS TABLAS DEL TS
                    listaCamposJson = extractTable(bdactual.valor, str(tabl.id))  # OBTENGO LOS DATOS DENTRO DE LA TABLA
                    entornoTabla = listaTablas.get(elemento).Entorno
                    campos = entornoTabla.simbolos  # obtengo los campos de la tabla de simbolos
                    return [campos,tabl,contador]
                contador += 1
            '''elif isinstance(tabl,IdAsId):
                if tabl.id1.id == listaTablas.get(elemento).id:
                    entornoTabla = listaTablas.get(elemento).Entorno
                    campos = entornoTabla.simbolos
                    return [campos, tabl, contador]
                contador += 1'''

    return None

def obtenerCamposGroup(listaTablas,Select,bdactual):
    for tabl in Select.inner.listaC:
        contador = 0
        for elemento in listaTablas:  # RECORRO LAS TABLAS DE LA TS
            # contador2 = contador2 + 1
            if isinstance(tabl, Id):
                if tabl.id == listaTablas.get(elemento).id:  # COMPARO SI EL NOMBRE ESCRITO DE LA TABLA ES IGUAL EN LAS TABLAS DEL TS
                    listaCamposJson = extractTable(bdactual.valor, str(tabl.id))  # OBTENGO LOS DATOS DENTRO DE LA TABLA
                    entornoTabla = listaTablas.get(elemento).Entorno
                    campos = entornoTabla.simbolos  # obtengo los campos de la tabla de simbolos
                    return [campos,tabl,contador]
                contador += 1
            '''elif isinstance(tabl,IdAsId):
                if tabl.id1.id == listaTablas.get(elemento).id:
                    entornoTabla = listaTablas.get(elemento).Entorno
                    campos = entornoTabla.simbolos
                    return [campos, tabl, contador]
                contador += 1'''

    return None

def ID(x,tabl,bdactual,listaTablas,listCampos2,contador2,consolaAux,existeTablas,listTExiste,sub,listaAuxiliarC):
    # print(tabl.id)
    auxExisteT2 = True
    contTablaE = 0
    for elemento in listaTablas:  # RECORRO LAS TABLAS DE LA TS
        # contador2 = contador2 + 1
        if tabl.id == listaTablas.get(elemento).id:  # COMPARO SI EL NOMBRE ESCRITO DE LA TABLA ES IGUAL EN LAS TABLAS DEL TS
            listTExiste.append(listaTablas.get(elemento).id)
            existeTablas = True
            #tablasJson = showTables(bdactual.valor) #OBTENGO LAS TABLAS DEL JSON
            # print(tablasJson)
            #for tablJson in tablasJson:  # BUSCO LA TABLAS DEL JSON
            #if (tabl.id == tablJson): # COMPARO SI LA TABLA ESCRITA ESTA EN LAS TABLAS JSON
            listaCamposJson = extractTable(bdactual.valor, tabl.id)  # OBTENGO LOS DATOS DENTRO DE LA TABLA
            # print(listaCamposJson)
            entornoTabla = listaTablas.get(elemento).Entorno
            campos = entornoTabla.simbolos  # obtengo los campos de la tabla de simbolos
            contador = contador2
            x.clear()
            for campo in campos: #RECORRO LOS NOMBRES DE LOS CAMPOS DE LA TS
                listCampos2.clear() # LIMPIO LA LISTA DONDE ALMACENARE LOS DATOS DE CADA COLUMNA
                contador +=1 # INDICA LA POSICION DE LA COLUMNA DONDE OBTENGO LOS VALORES
                auxiliarColumna = []
                if (contador != -1):

                    for col in listaCamposJson: # RECORRO LOS DATOS DE LA TABLA DE SIMBOLOS
                        listCampos2.append(col[contador])
                        auxiliarColumna.append(col[contador])
                #if verficarRepetidos(listCampos2):  # VERIFICA SI SE REPITE ELEMENTO
                 #   listaAux = Repeat(listCampos2)
                  #  x.add_column(campos.get(campo).id, listaAux)
                #else:
                x.add_column(campos.get(campo).id, listCampos2) #AGREGO UNA COLUMNA
                sub.append(campos.get(campo).id)
                listaAuxiliarC.append(auxiliarColumna)

    if existeTablas:
        consolaAux.append('\n' + x.get_string() + '\n') # LO INGRESO A LA CONSOLA
    else:
        consolaAux.clear()
    return existeTablas





def IDGr(x,tabl,bdactual,listaTablas,listCampos2,contador2,consolaAux,existeTablas,listaG,sub,listaAuxiliarC):
    # print(tabl.id)
    auxExisteT2 = True
    contTablaE = 0
    for elemento in listaTablas:  # RECORRO LAS TABLAS DE LA TS
        # contador2 = contador2 + 1
        if tabl.id == listaTablas.get(elemento).id:  # COMPARO SI EL NOMBRE ESCRITO DE LA TABLA ES IGUAL EN LAS TABLAS DEL TS
            #listTExiste.append(listaTablas.get(elemento).id)
            existeTablas = True
            listaCamposJson = extractTable(bdactual.valor, tabl.id)  # OBTENGO LOS DATOS DENTRO DE LA TABLA
            entornoTabla = listaTablas.get(elemento).Entorno
            campos = entornoTabla.simbolos  # obtengo los campos de la tabla de simbolos
            contador = contador2
            x.clear()
            auxiliarColumna = []
            for campo in campos: #RECORRO LOS NOMBRES DE LOS CAMPOS DE LA TS
                listCampos2.clear() # LIMPIO LA LISTA DONDE ALMACENARE LOS DATOS DE CADA COLUMNA
                contador +=1 # INDICA LA POSICION DE LA COLUMNA DONDE OBTENGO LOS VALORES
                if (contador != -1):
                    for col in listaG: # RECORRO LOS DATOS DE LA TABLA DE SIMBOLOS
                        listCampos2.append(col[contador])
                        auxiliarColumna.append(col[contador])
                x.add_column(campos.get(campo).id, listCampos2) #AGREGO UNA COLUMNA
                listaAuxiliarC.append(auxiliarColumna)
                sub.append(campos.get(campo).id)

    if existeTablas:
        consolaAux.append('\n' + x.get_string() + '\n') # LO INGRESO A LA CONSOLA
    else:
        consolaAux.clear()
    return existeTablas

def Diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif


def Repeat(x):
    _size = len(x)
    repeated = []
    for i in range(_size):
        k = i + 1
        for j in range(k, _size):
            if x[i] == x[j] and x[i] not in repeated:
                repeated.append(x[i])
    return repeated


def existeId(id,listaIds):
    for aux in listaIds:
        if id == aux[1]:
            return aux
    return None

def BuscarTBIdId(Select, listaTablas):
    listaTmp = []
    listaNomT = []
    for tabl in Select.inner:
        if isinstance(tabl, IdAsId):
            for elemento in listaTablas:
                if elemento == tabl.id1.id:
                    x = {'Tabla': tabl.id1,'Alias': tabl.id2.id}
                    listaNomT.append(tabl.id1.id)
                    listaTmp.append(x)
                    #print(x['Tabla'].id)
                    #return {'Tabla': tabl.id1,'Alias': tabl.id2.id}
    return [listaTmp,listaNomT]


def BuscarTBIdId2(Select, listaTablas):
    listaTmp = []
    listaNomT = []
    for tabl in Select.inner:
        if isinstance(tabl, Id):
            for elemento in listaTablas:
                if elemento == tabl.id:
                    x = {'Tabla': tabl}
                    listaNomT.append(tabl.id)
                    listaTmp.append(x)
                    # print(x['Tabla'].id)
                    # return {'Tabla': tabl.id1,'Alias': tabl.id2.id}
    return [listaTmp, listaNomT]
'''
def existe_id(id,listaIds):
    for aux in listaIds:
        if aux[1] == id:
            return aux
    return None'''
def BuscarColumnasLQVP(nombreTabla,col,listaTablas,Alias):
    listaTmp = []
    lista = obtenerCampos2(nombreTabla,listaTablas)
    for campo in lista[0]:  # RECORRO LOS NOMBRES DE LOS CAMPOS DE LA TS 2
        #print(lista[0].get(campo).id)
        if col.id2.id == lista[0].get(campo).id:
            if col.id1.id == Alias:
                #x = {'LQBP':col.id1.id,'Columna':col.id2.id}
                #listaTmp.append(x)
                return {'LQBP':col.id1.id,'Columna':col.id2.id}
    return None
    #return listaTmp


def BuscarColumnasLQVP5(nombreTabla,col,listaTablas,Alias):
    listaTmp = []
    lista = obtenerCampos2(nombreTabla,listaTablas)
    for campo in lista[0]:  # RECORRO LOS NOMBRES DE LOS CAMPOS DE LA TS 2
        #print(lista[0].get(campo).id)
        if col.id1.id2.id == lista[0].get(campo).id:
            if col.id1.id1.id == Alias:
                #x = {'LQBP':col.id1.id,'Columna':col.id2.id}
                #listaTmp.append(x)
                return {'LQBP':col.id1.id1.id,'Columna':col.id1.id2.id}
    return None

def BuscarColumnasLQVP3(nombreTabla,col,listaTablas,Alias):
    if col.id1.id == Alias:
        if col.id2.id == '*':
            return {'LQBP':col.id1.id,'Columna':col.id2.id}
    return None

def BuscarColumnasLQVP4(nombreTabla,col,listaTablas,Alias):
    if col.id1.id == nombreTabla:
        if col.id2.id == '*':
            return {'LQBP':col.id1.id,'Columna':col.id2.id}
    return None

def obtenerCampos2(nombreTabla,listaTablas):
    contador = 0
    for elemento in listaTablas:  # RECORRO LAS TABLAS DE LA TS
        if nombreTabla == listaTablas.get(elemento).id:
            entornoTabla = listaTablas.get(elemento).Entorno
            campos = entornoTabla.simbolos  # obtengo los campos de la tabla de simbolos
            return [campos, contador]
        contador += 1

def existe_id(tuplaCol):
    for tmp in tuplaCol:
        pass

def IdIdp(x,col,listCampos2,listaTablas,bdactual,nombreTabla,sub,listaAuxiliarC):
    lista = obtenerCampos2(nombreTabla,listaTablas)

    listaCamposJson = extractTable(bdactual.valor, nombreTabla)  # OBTENGO LOS DATOS DENTRO DE LA TABLA
    # contador = 0

    contador = -1
    for campo in lista[0]:  # RECORRO LOS NOMBRES DE LOS CAMPOS DE LA TS
        listCampos2.clear()  # LIMPIO LA LISTA DONDE ALMACENARE LOS DATOS DE CADA COLUMNA
        contador += 1  # INDICA LA POSICION DE LA COLUMNA DONDE OBTENGO LOS VALORES
        if (col.id2.id == lista[0].get(campo).id):
            auxiliarColumna =[]
            for col2 in listaCamposJson:  # RECORRO LOS DATOS DE LA TABLA DE SIMBOLOS
                listCampos2.append(col2[contador])
                auxiliarColumna.append(col2[contador])
            #if verficarRepetidos(listCampos2):  # VERIFICA SI SE REPITE ELEMENTO
             #   listaAux = Repeat(listCampos2)
              #  x.add_column(lista[0].get(campo).id, listaAux)
            #else:
            x.add_column(lista[0].get(campo).id, listCampos2)  # AGREGO UNA COLUMNA
            listaAuxiliarC.append(auxiliarColumna)
            sub.append(lista[0].get(campo).id)

def IdIdp2(x,col,listCampos2,listaTablas,bdactual,nombreTabla,Alias,sub,listaAuxiliarC):
    lista = obtenerCampos2(nombreTabla,listaTablas)

    listaCamposJson = extractTable(bdactual.valor, nombreTabla)  # OBTENGO LOS DATOS DENTRO DE LA TABLA
    # contador = 0

    contador = -1
    for campo in lista[0]:  # RECORRO LOS NOMBRES DE LOS CAMPOS DE LA TS
        listCampos2.clear()  # LIMPIO LA LISTA DONDE ALMACENARE LOS DATOS DE CADA COLUMNA
        contador += 1  # INDICA LA POSICION DE LA COLUMNA DONDE OBTENGO LOS VALORES
        if (col.id1.id2.id == lista[0].get(campo).id):
            auxiliarColumna= []
            for col2 in listaCamposJson:  # RECORRO LOS DATOS DE LA TABLA DE SIMBOLOS
                listCampos2.append(col2[contador])
                auxiliarColumna.append(col2[contador])
            #if verficarRepetidos(listCampos2):  # VERIFICA SI SE REPITE ELEMENTO
             #   listaAux = Repeat(listCampos2)
              #  x.add_column(lista[0].get(campo).id, listaAux)
            #else:
            x.add_column(Alias, listCampos2)  # AGREGO UNA COLUMNA
            listaAuxiliarC.append(auxiliarColumna)
            sub.append(lista[0].get(campo).id)
def verficarRepetidos(listOfElems):
    if len(listOfElems) == len(set(listOfElems)):
        return False
    else:
        return True

def TablaCompleta(x,bdactual,nombreTabla,listaTablas,sub,listaAuxiliarC):
    listaCamposJson = extractTable(bdactual.valor, nombreTabla)  # OBTENGO LOS DATOS DENTRO DE LA TABLA
    # print(listaCamposJson)
    lista = obtenerCampos2(nombreTabla, listaTablas)
    #entornoTabla = listaTablas.get(elemento).Entorno
    #campos = entornoTabla.simbolos  # obtengo los campos de la tabla de simbolos
    contador = -1
    listCampos2 = []
    x.clear()
    for campo in lista[0]:  # RECORRO LOS NOMBRES DE LOS CAMPOS DE LA TS
        listCampos2.clear()  # LIMPIO LA LISTA DONDE ALMACENARE LOS DATOS DE CADA COLUMNA
        contador += 1  # INDICA LA POSICION DE LA COLUMNA DONDE OBTENGO LOS VALORES
        auxiliarColumna = []
        if (contador != -1):
            for col in listaCamposJson:  # RECORRO LOS DATOS DE LA TABLA DE SIMBOLOS
                listCampos2.append(col[contador])
                auxiliarColumna.append(col[contador])
        # if verficarRepetidos(listCampos2):  # VERIFICA SI SE REPITE ELEMENTO
        #   listaAux = Repeat(listCampos2)
        #  x.add_column(campos.get(campo).id, listaAux)
        # else:
        x.add_column(lista[0].get(campo).id, listCampos2)  # AGREGO UNA COLUMNA
        listaAuxiliarC.append(auxiliarColumna)
        sub.append(lista[0].get(campo).id)

def groupby(valor, lista, index):

    for elem in lista:
        contadorG = 0
        for columna in elem:
            if contadorG == index:
                if str(columna) == str(valor[index]):
                    return False
            contadorG += 1

    return True

def listaDeListas(lista):
    lista_original = []
    contador = 0

    for recorido in lista[0]:
        lista_aux = []
        for columna in lista:
            lista_aux.append(columna[contador])
        contador += 1
        lista_original.append(lista_aux)

    return lista_original

def buscar_infice(id, lista_campo):
    contador = -1
    for campo in lista_campo:  # RECORRO LOS NOMBRES DE LOS CAMPOS DE LA TS
        contador += 1  # INDICA LA POSICION DE LA COLUMNA DONDE OBTENGO LOS VALORES
        if (id == campo):
            return contador

    return -1

def imprimir_Tabla(Select,listaCampos,listaEncabezado,x):
    x.clear()
    contador = -1
    listCampos2 = []
    for campo in listaEncabezado:  # RECORRO LOS NOMBRES DE LOS CAMPOS DE LA TS
        listCampos2.clear()  # LIMPIO LA LISTA DONDE ALMACENARE LOS DATOS DE CADA COLUMNA
        contador += 1  # INDICA LA POSICION DE LA COLUMNA DONDE OBTENGO LOS VALORES
        auxiliarColumna = []
        if (contador != -1):

            for col in listaCampos:  # RECORRO LOS DATOS DE LA TABLA DE SIMBOLOS
                listCampos2.append(col[contador])
                auxiliarColumna.append(col[contador])
        # if verficarRepetidos(listCampos2):  # VERIFICA SI SE REPITE ELEMENTO
        #   listaAux = Repeat(listCampos2)
        #  x.add_column(campos.get(campo).id, listaAux)
        # else:
        x.add_column(campo, listCampos2)  # AGREGO UNA COLUMNA

def validar_distinct(dato, lista):
    aux = lista
    contador = 0
    for recorrido in aux:
        if (recorrido == dato):
            contador += 1
        else:
            pass
    return contador