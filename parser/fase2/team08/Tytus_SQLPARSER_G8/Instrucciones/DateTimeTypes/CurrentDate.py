from Instrucciones.TablaSimbolos.Instruccion import Instruccion
from Instrucciones.TablaSimbolos.Simbolo import Simbolo 
from datetime import datetime 

class CurrentDate(Instruccion):
    def __init__(self, strGram, linea, columna):
        Instruccion.__init__(self,None,linea,columna,strGram)
        
    def ejecutar(self, ts, arbol):
        super().ejecutar(ts,arbol)
        #año-mes-dia
        todays_date = datetime.today()
        date = todays_date.strftime("%Y-%m-%d")
        return date

    def analizar(self, ts, arbol):
        pass
    def traducir(self, tabla, arbol):
        return "CURRENT_DATE"

'''
instruccion = Declare("hola mundo",None, 1,2)

instruccion.ejecutar(None,None)
'''