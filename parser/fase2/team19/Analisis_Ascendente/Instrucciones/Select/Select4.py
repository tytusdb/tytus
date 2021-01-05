from Analisis_Ascendente.Instrucciones.instruccion import *
from Analisis_Ascendente.storageManager.jsonMode import *
import Analisis_Ascendente.Tabla_simbolos.TablaSimbolos as TS
import Analisis_Ascendente.Instrucciones.Select as Select
from Analisis_Ascendente.Instrucciones.Select.select import GroupBy,Having
from Analisis_Ascendente.Instrucciones.Time import  Time
from Analisis_Ascendente.Instrucciones.expresion import  *
from Analisis_Ascendente.Instrucciones.Expresiones.Trigonometrica import  Trigonometrica
from Analisis_Ascendente.Instrucciones.Expresiones.IdAsId import  IdAsId,Id,IdId
from Analisis_Ascendente.Instrucciones.Expresiones.Math import  Math_
from prettytable import PrettyTable
from Analisis_Ascendente.storageManager.jsonMode import *
import Analisis_Ascendente.Instrucciones.Expresiones.Where as Where
import Analisis_Ascendente.Instrucciones.Expresiones.Expresion as Expresion

class Selectp7(Instruccion):

    def ejecutar(Select,ts,Consola, Exceptions,mostrar):
        '''insert('prueba1', 'tabla1', [1, 'Fredy', 'Ramirez'])
        insert('prueba1', 'tabla1', [2, 'Mauro', 'Martinez'])
        insert('prueba1', 'tabla1', [3, 'Javier', 'Lima'])
        insert('prueba1', 'tabla1', [4, 'Yisus', 'Yisusx2'])
        insert('prueba1', 'tabla1', [5, 'Jacks', 'Wade'])

        insert('prueba1', 'tabla2', [1, 'Mario', 'Guatemala', 'Contabilidad'])
        insert('prueba1', 'tabla2', [2, 'Eli', 'Dubai', 'Progra'])
        insert('prueba1', 'tabla2', [3, 'Sis', 'Brasil', 'Master Chief'])
        insert('prueba1', 'tabla2', [4, 'Fredy', 'Noruega', 'God of War'])
        insert('prueba1', 'tabla2', [5, 'Luigi', 'Italia', 'Mario Kart'])

        insert('prueba1', 'tabla3', [1, 'Sic', 'USA', '4av. km 19.3'])
        insert('prueba1', 'tabla3', [2, 'Pepe', 'Irak', 'en amatitlan ese'])
        insert('prueba1', 'tabla3', [3, 'Etesech', 'China', 'perdido'])
        insert('prueba1', 'tabla3', [4, 'ufuefue', 'Japon', 'Selva'])
        insert('prueba1', 'tabla3', [5, 'osas', 'Venezuela', 'Jungla'])'''



        tablasRef = {}
        cont=0
        x = PrettyTable()
        x.clear()
        en=[]
        DataSelect=[]
        DataSelectInicial=[]
        columnasT = len(Select.columnas)
        Error = False;
        resultado = FROM(Select, tablasRef, Exceptions,DataSelectInicial) #leemos las tablas
        for i in tablasRef.items():
            print(i)
        for columna in Select.columnas:
            print('what -- ' + str(len(Select.columnas)))
            Permutar = False

            if (ts.validar_sim("usedatabase1234") and cont<=columnasT):
                cont=cont+1
                simboloBD = ts.buscar_sim(ts.buscar_sim("usedatabase1234").valor)
                print(simboloBD.id)
                entornoBD = simboloBD.Entorno
                listado_tablas = entornoBD.simbolos
                listadoCampo = {}




                if resultado[0]: #si vienen valores de ids de tablas validos


                    for k in tablasRef.keys():
                        if not existeTabla(listado_tablas, tablasRef.get(k)):
                            Exceptions.append(f'Error semantico - 42P01 - no existe la relación, error en  - {Select.fila} - {Select.columna}')
                            Error = True
                            break;

                    if not Error:

                        if isinstance(columna, str):  # todos los campitos es decir *
                            cont22 = 0
                            NombreAnterior=''
                            for k in tablasRef.keys():
                                if cont22 >0:
                                    Permutar= True
                                    DataAux=[]
                                    DataAux= DataSelect.copy()
                                    DataSelect=[]
                                    DataJson = extractTable(simboloBD.id, tablasRef.get(k))
                                    DataSelect = ActualizarTabla(x,DataJson,Contt[0],Contt[2],DataAux,None)
                                    print("sad-->"+str((DataSelect)))

                                en = []
                                Contt = []
                                Contt=encabezados(tablasRef.get(k),tablasRef,listado_tablas,en)
                                #listadoCampo[tablasRef.get(k)] = Cont
                                DataJson= extractTable(simboloBD.id,tablasRef.get(k))
                                NombreAnterior= tablasRef.get(k)
                                DataSelect = agregarData(x,DataJson,Contt[0],Contt[2], DataSelect,None,Permutar,tablasRef.get(k))
                                cont22=cont22 + 1
                                print('agregar---'+k)

                        elif isinstance(columna, Id):
                            nombreCampo = columna.id
                            print('campo'+nombreCampo)

                            Frecuencia = CamposRepetidos(tablasRef,Exceptions,listado_tablas,nombreCampo)
                            print('Frecuencia <<<->>>'+str(Frecuencia))
                            if (Frecuencia == 1):
                                referencia = BuscarCampoTablas(tablasRef, Exceptions, listado_tablas, nombreCampo)
                                DataSelectAux=[]
                                if(referencia[0]):#quiere decir que existe en una de las tablas del from
                                    DataJson= extractTable(simboloBD.id,referencia[1])
                                    columna=[]
                                    for column in DataJson:
                                        columna.append(column[referencia[2]])

                                    #DataSelectAux.append([nombreCampo,columna,referencia[1]])
                                    DataSelectAux.append(nombreCampo)
                                    DataSelectAux.append(columna)
                                    DataSelectAux.append((referencia[1]))
                                    DataSelect = PermutarData(DataSelect,DataSelectAux);
                                    #x.add_column(nombreCampo,columna)
                            elif Frecuencia == 0 :
                                Exceptions.append(
                                    'Error semantico - 42703 -no existe la columna, error en ' + ' - ' + str(Select.fila) + ' - ' + str(Select.columna) + '')
                                print('No existe campo en tablas de referencia')
                                Error = True
                                break;
                            else:
                                Exceptions.append(
                                    'Error semantico - 42702 -la referencia a la columna es ambigua, error en ' + ' - ' + str(Select.fila) + ' - ' + str(Select.columna) + '')
                                print('Existe ambigüedad en campos de tablas de referencia campo'+ nombreCampo)
                                Error = True
                                break;



                        elif isinstance(columna, IdId): #cuando viene con puntito id.id la columna
                            nombreCampo = columna.id2
                            print( 'campito bebé-->'+str(nombreCampo))

                            if isinstance(columna.id1,Id):
                                nombreTabla = columna.id1.id #alias de la tabla
                                if isinstance(columna.id2,Id) :
                                    nombreCampo = columna.id2.id


                                    Tabla = existeAliasTabla(tablasRef,nombreTabla) #nombre de tabla con ese alias

                                    if Tabla[0]: # existe un alias para una tabla en ese select

                                        if nombreCampo == '*':

                                            en = []
                                            ContT = []
                                            ContT = encabezados(str(Tabla[1]), tablasRef, listado_tablas, en)
                                            DataJson = extractTable(simboloBD.id, str(Tabla[1]))

                                            if len(DataSelect) > 0:
                                                Permutar = True
                                                DataAux = []
                                                DataAux = DataSelect.copy()
                                                DataSelect = []
                                                DataJson = extractTable(simboloBD.id, str(Tabla[1]))
                                                DataSelect = ActualizarTabla(x, DataJson, ContT[0], ContT[2], DataAux,
                                                                                 None)
                                                print("sad-->" + str((DataSelect)))


                                            DataSelect = agregarData(x, DataJson, ContT[0], ContT[2], DataSelect, nombreTabla,
                                                                         Permutar, str(Tabla[1]))

                                        else:
                                            referencia = existeCampo(nombreCampo,(listado_tablas.get(Tabla[1]).Entorno).simbolos)
                                            DataSelectAux = []
                                            if (referencia[0]):  # quiere decir que existe en una de las tablas del from
                                                DataJson = extractTable(simboloBD.id, Tabla[1])
                                                columna = []
                                                for column in DataJson:
                                                    columna.append(column[referencia[1]])
                                                #DataSelect.append([str(nombreTabla)+'.'+str(nombreCampo), columna])
                                                DataSelectAux.append(str(nombreTabla)+'.'+str(nombreCampo))
                                                DataSelectAux.append(columna)
                                                DataSelectAux.append((Tabla[1]))
                                                DataSelect = PermutarData(DataSelect, DataSelectAux);
                                                #x.add_column(str(nombreTabla)+'.'+str(nombreCampo), columna)
                                            else:
                                                Exceptions.append(
                                                    'Error semantico - 42703 -no existe la columna, error en ' + ' - ' + str(Select.fila) + ' - ' + str(Select.columna) + '')
                                                print('no existe campo  en tabla' + Tabla[1])
                                                Error = True
                                                break;

                                    else:
                                        Exceptions.append(
                                            'Error semantico - 42P01 -falta una entrada para la tabla en la cláusula FROM, error en ' + ' - ' + str(Select.fila) + ' - ' + str(Select.columna) + '')
                                        print('no existe tabla con ese alias' + nombreTabla)
                                        Error = True
                                        break;

                            else:
                                Exceptions.append(
                                    'Error semantico - 42P01 -tipo invalido de id campo , error en ' + ' - ' + str(Select.fila) + ' - ' + str(Select.columna) + '')

                                Error = True
                                break;
                        else:
                            print()
                    else:
                        Error = True
                        break

            else:
                print("no se seleciona una bd")

        if (not Error):

            #x.clear()
            DataSelect = EvaluarWhere(ts,Select,DataSelect,Exceptions,Consola)


            print('lo que llego')
            print(DataSelect)


            if isinstance(DataSelect,list):
                for i in range(len(DataSelect[0])):
                    columnas=[]
                    for fila  in DataSelect[1]:
                        columnas.append(fila[i])
                    x.add_column(str(DataSelect[0][i]),columnas)
                if mostrar:
                    Consola.append('\n' + x.get_string() + '\n')
                return DataSelect
            #cont=cont+1




def existeTabla(listadoTablas,tablaBuscar):

        for tablita in listadoTablas:
            if listadoTablas.get(tablita).id == tablaBuscar:
                return True
        return  False


def existeAliasTabla(tablasRef, Alias):

    for k in tablasRef.keys():
        if k == Alias:
            return [True, tablasRef.get(k)]
    return [False,False]

def encabezados(tablaR,tablasRef,listado_tablas,en):

        contadorCampos = 0
        campos = []

        for elemento in listado_tablas: #tablas en ts

            if listado_tablas.get(elemento).id == tablaR:
                entornoTabla = listado_tablas.get(elemento).Entorno
                lista_campos = entornoTabla.simbolos
                for campito in lista_campos:
                    nombreCampo = str(lista_campos.get(campito).id)
                    enc = ''
                    if nombreCampo in en:
                        for k in tablasRef.keys():
                            if tablasRef.get(k) == tablaR:
                                enc = k
                                break

                        en.append(enc + '.' + nombreCampo)
                        campos.append(nombreCampo)

                    else:
                        en.append(nombreCampo)
                        campos.append(nombreCampo)
                    contadorCampos = contadorCampos + 1

                return [contadorCampos,campos,en]
        return  [0,campos,en]

def ActualizarTabla(x,DataJson,rango,en,DataSelect3, alias):
    filas = len(DataJson)
    print('filas nueva tabla'+str(filas))
    DataSelectAux =[]
    row = []

    for columna in DataSelect3: #3
        row = []

        for fila in columna[1]: #2
            for i in range(filas):
                row.append(str(fila))
        DataSelectAux.append([str(columna[0]),row,columna[2]])

    return DataSelectAux




def agregarData(x,DataJson,rango,en,DataSelect3,alias,Permutar,tabla):

    if Permutar:
        for i in range(rango):
            columna = []
            print(len(DataSelect3[0][1]))
            if(len(DataJson)>0):
                for j in range(int(len(DataSelect3[0][1])/len(DataJson))):
                    for row in DataJson:
                        columna.append(row[i])
            if alias != None:
                DataSelect3.append([alias+'.'+en[i], columna,tabla])
            else:
                DataSelect3.append([en[i], columna, tabla])

        return DataSelect3

    else:
        for i in range(rango):
            columna = []
            for column in DataJson:
                columna.append(column[i])
            if alias != None:
                DataSelect3.append([alias + '.' + en[i], columna, tabla])
            else:
                DataSelect3.append([en[i], columna, tabla])
            #x.add_column(en[i], columna)

        return  DataSelect3

        #x.add_column(en[i], columna)


def FROM(Select,tablasRef,Exceptions,DataSelectInicial):
    if Select.subquery != None:  # resolver subquery primero que de aca saldrían los datos
        print('what -- ' + type(Select.subquery).__name__)
    else:  # las tablas vendrían en inner
        for tablas in Select.inner:  # nada mas obteniendo los id de las tablas solicitadas
           # print('tablas55555 -- ' + tablas.id1.id)
            if isinstance(tablas, Id):
                tablasRef[str(tablas.id)] = tablas.id
            elif isinstance(tablas, IdAsId):
                if isinstance(tablas.id1, Id) and isinstance(tablas.id2, Id):

                    if str(tablas.id2.id) in tablasRef.keys():
                        Exceptions.append(
                            'Error semantico - 42712 -  el nombre de tabla  fue especificado más de una vez, error en ' + ' - ' + str(Select.fila) + ' - ' + str(Select.columna) + '')

                        print('alias repetidos-->'+ tablas.id2.id)
                        return [False,tablasRef]
                    tablasRef[str(tablas.id2.id)] = str(tablas.id1.id)
                else:
                    Exceptions.append(
                        'Error semantico - 42712 -  alias de tipo invalidos, error en ' + ' - ' + str(Select.fila) + ' - ' + str(Select.columna) + '')
                    return [False,tablasRef]

    return [True,tablasRef,Exceptions]


def BuscarCampoTablas(tablasRef,Exceptions,listado_tablas,campobuscar):
    for ref in tablasRef.keys():
        entornoTabla = listado_tablas.get(tablasRef.get(ref)).Entorno
        lista_campos = entornoTabla.simbolos
        contadorPosicion= 0

        for campo in lista_campos:
            if campobuscar == lista_campos.get(campo).id:
                return [True,tablasRef.get(ref),contadorPosicion]
            contadorPosicion = contadorPosicion + 1
    return [False,False,False]

def CamposRepetidos(tablasRef,Exceptions,listado_tablas,campobuscar):
    contador = 0
    for ref in tablasRef.keys():
        entornoTabla = listado_tablas.get(tablasRef.get(ref)).Entorno
        lista_campos = entornoTabla.simbolos


        for campo in lista_campos:
            if campobuscar == lista_campos.get(campo).id:
                contador = contador + 1
    return contador

def existeCampo(nombreCampo,lista):
    contador = 0
    for campo in lista:
        if nombreCampo == lista.get(campo).id:
            return [True,contador]
        contador += 1
    return [False,contador]


def EvaluarWhere(ts,Select,DataSelect,Exceptions,Consola):
    print(type(Select.complementS).__name__)
    #print(DataSelect)
    l = []
    filas=[False,[]]
    if isinstance(Select.complementS,Where.Where) or isinstance(Select.complementS,Expresion.Expresion):
        filas = Where.Where.Resolver(Select.complementS,ts,Exceptions,Consola,DataSelect)

    elif isinstance(Select.complementS,GroupBy):
        filas = Where.Where.Resolver(Select.complementS.listaC, ts, Exceptions, Consola, DataSelect)
    '''for c in DataSelect:
        l.append(str(c[0]))
    x.field_names= l'''
    print(filas)
    DataSelectAux = []
    row = []
    if filas[0] and filas[1]!=None and len(filas[1])>0:
        registros=[]
        columnas=[]
        for i in filas[1]:

            registros=[]
            columnas=[]
            for column in DataSelect:

                registros.append(column[1][i])
                columnas.append(column[0])
            row.append(registros)
            #x.add_row(registros)

        print('rows')

        return [columnas,row]
    else:
        print(filas[1])
        columnas=[]
        for column in DataSelect:
            columnas.append(column[0])
        return [columnas,[]]



def PermutarData(DataSelect3, DataSelectAux):

    if len(DataSelect3)>0: # hay más entonces
        # buscar si hay una columna de la misma tabla
        veces =-1
        columnaAux = []
        contcolumna=0
        for columna in DataSelect3:
            if columna[2] == DataSelectAux[2]:
                if len(DataSelectAux[1])>0:
                    veces = int(len(columna[1])/len(DataSelectAux[1]))

                break;
            contcolumna = contcolumna + 1
        print('veces' + str(veces))
        if veces>0:

            if DataSelect3[contcolumna][1][0] == DataSelect3[contcolumna][1][1]:
                for row in DataSelectAux[1]:
                    for i in range(veces):
                        columnaAux.append(row)
                DataSelect3.append([DataSelectAux[0],columnaAux,DataSelectAux[2]])
            else:
                for i in range(veces):
                    for row in DataSelectAux[1]:
                        columnaAux.append(row)
                DataSelect3.append([DataSelectAux[0], columnaAux, DataSelectAux[2]])
            return DataSelect3

        else:
            DataSelect3 = ActualizarTabla(None,DataSelectAux[1],None,None,DataSelect3,None) # permutado la data existente hasta el momento

            columna = []
            print(len(DataSelect3[0][1]))
            if len(DataSelectAux[1])>0:
                for j in range(int(len(DataSelect3[0][1]) / len(DataSelectAux[1]))):
                    for row in DataSelectAux[1]:
                        columna.append(row)
            DataSelect3.append([DataSelectAux[0], columna, DataSelectAux[2]])
            return  DataSelect3


    else:
        print('lo que llega')
        print(DataSelectAux)
        DataSelect3.append([DataSelectAux[0],DataSelectAux[1],DataSelectAux[2]])
        return DataSelect3
