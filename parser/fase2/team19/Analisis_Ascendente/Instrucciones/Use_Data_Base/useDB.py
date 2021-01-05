from Analisis_Ascendente.Instrucciones.instruccion import Instruccion
import Analisis_Ascendente.Tabla_simbolos.TablaSimbolos as TS
from Analisis_Ascendente.storageManager.jsonMode import *

#from Instrucciones.instruccion import Instruccion
#import Tabla_simbolos.TablaSimbolos as TS
#from storageManager.jsonMode import *

#USE
class Use(Instruccion):
    def __init__(self, id):
        self.id = id

    def ejecutar(use,ts,consola,exceptions):

            if ts.validar_sim("usedatabase1234") == -1:

                lb = showDatabases()
                for bd in lb:

                    if bd == str(use.id):
                        simbolo_use = TS.Simbolo(TS.TIPO_DATO.USE, "usedatabase1234", None, use.id, None)
                        ts.agregar_sim(simbolo_use)
                        consola.append(f"Seleccionando {simbolo_use.valor} base de datos\n")
                        return

                consola.append(f"La Base de Datos {use.id} no existe\n")
            else:

                lb = showDatabases()
                for bd in lb:
                    if bd == use.id:
                        use_anterior = ts.buscar_sim("usedatabase1234")
                        simbolo_use = TS.Simbolo(TS.TIPO_DATO.USE, "usedatabase1234", None, use.id, None)
                        ts.actualizar_sim(simbolo_use)
                        consola.append(f"Cambiando use de {use_anterior.valor} ahora el actual es: {simbolo_use.valor}\n")
                        return

                consola.append(f"La Base de Datos {use.id} no existe\n")
