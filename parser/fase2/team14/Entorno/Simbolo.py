from Entorno.TipoSimbolo import TipoSimbolo

class Simbolo:
    def __init__(self, tipo = "", nombre = "", valor = None, linea = 0):
        self.tipo = tipo
        self.nombre = nombre
        self.valor = valor
        self.linea = linea
        self.atributos = {}
        self.baseDatos = ""
        self.tabla = ""
    
    def toString(self):
        cadena:str = ""
        #nombre,tipoSym,baseDatos,tabla,valor
        if self.nombre != None:
            if self.tipo == TipoSimbolo.TABLA:
                columnas:Simbolo = [] 
                columnas = self.valor
                cadena += "<TR><TD rowspan='" + str(len(columnas)) + "'>" + self.nombre.split('_')[0] + "</TD><TD rowspan='" + str(len(columnas)) + "'>TABLA</TD><TD rowspan='" + str(len(columnas)) + "'>" + self.baseDatos + "</TD><TD rowspan='" + str(len(columnas)) + "'>"
                cadena += self.tabla + "</TD><TD>" + columnas[0].nombre + ":" + columnas[0].tipo.tipo + "</TD></TR>\n"
                for col in range(1,len(columnas),1):
                    cadena += "<TR><TD>" + columnas[col].nombre + ":" + columnas[col].tipo.tipo + "</TD></TR>\n"
            
            elif self.tipo == TipoSimbolo.CONSTRAINT_UNIQUE:
                cadena += "<TR><TD>" + self.nombre + "</TD><TD>UNIQUE</TD><TD>" + self.baseDatos + "</TD><TD>"
                cadena += self.tabla + "</TD><TD>" + self.valor + "</TD></TR>\n\n"
            
            elif self.tipo == TipoSimbolo.CONSTRAINT_CHECK:
                cond:str = self.valor.simbolo
                if cond in ">":
                    cond = cond.replace(">","&#62;")
                if cond in "<":
                    cond = cond.replace("<","&#60;")
                if cond in "<=":
                    cond = cond.replace("<=","&#60;&#61;")
                if cond in ">=":
                    cond = cond.replace(">=","&#62;&#61;")
                if cond in "<>":
                    cond = cond.replace(">=","&#60;&#62;")

                cadena += "<TR><TD>" + self.nombre + "</TD><TD>CONSTRAINT CHECK</TD><TD>" + self.baseDatos + "</TD><TD>"
                cadena += self.tabla + "</TD><TD>" + str(self.valor.exp1.valor) + " " + cond + " " + str(self.valor.exp2.valor) + "</TD></TR>\\n"
            elif self.tipo == TipoSimbolo.CONSTRAINT_FOREIGN:
                cadena += "<TR><TD>" + self.nombre + "</TD><TD>CONSTRAINT FORANEA</TD><TD>" + self.baseDatos + "</TD><TD>"
                cadena += self.tabla + "</TD><TD></TD></TR>"
            elif self.tipo == TipoSimbolo.CONSTRAINT_PRIMARY:
                cadena += "<TR><TD>" + self.nombre + "</TD><TD>CONSTRAINT PRIMARIA</TD><TD>" + self.baseDatos + "</TD><TD>"
                cadena += self.tabla + "</TD><TD>" + str(self.valor) + "</TD></TR>"
            elif self.tipo == TipoSimbolo.TYPE_ENUM:
                columnas:Simbolo = [] 
                columnas = self.valor
                cadena += "<TR><TD rowspan='" + str(len(columnas)) + "'>" + self.nombre.split('_')[2] + "</TD><TD rowspan='" + str(len(columnas)) + "'>ENUM</TD><TD rowspan='" + str(len(columnas)) + "'>" + self.baseDatos + "</TD><TD rowspan='" + str(len(columnas)) + "'>"
                cadena += self.tabla + "</TD><TD>" + columnas[0].valor + "</TD></TR>\n"
                for col in range(1,len(columnas),1):
                    cadena += "<TR><TD>" + columnas[col].valor + "</TD></TR>\n"


        return cadena
        