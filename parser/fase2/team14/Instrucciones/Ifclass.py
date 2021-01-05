
from Instrucciones.Instruccion import Instruccion


from Expresion.FuncionesNativas import *

class Ifclass(Instruccion):
    def __init__(self,exp,cif,elsif=None,celse=None):
        self.exp=exp
        self.cif=cif
        self.elsif=elsif
        self.celse=celse


    def ejecutar(self, ent:Entorno):
            'sdfsadf'

    def traducir(self,entorno):
        if self.elsif==None and self.celse==None:
            lv = entorno.newlabel()
            lf = entorno.newlabel()
            # pongo en codigo el temporal  de la expresion
            exp=self.exp.traducir(entorno)
            cad = exp.codigo3d
            cond=exp.temp
            instrif=self.cif
            # condicional del if que hace que se salto al codigo verdadero
            cad += 'if ' + cond + ': \n \t goto ' + lv + '\ngoto ' + lf + '\n'
            # salto hacia el final si no fue verdadera la expresion
            cad += 'label ' + lv + '\n'
            # instrucciones dentro del if
            for instr in instrif:
                cad += str(instr.traducir(entorno).codigo3d)
            # codigo que sigue despues del if
            cad += 'label ' + lf + '\n'
            self.codigo3d=cad
        elif self.elsif!=None and self.celse!=None:
            tmp = None
            for i in range(len(self.elsif)-1,-1,-1):
                inst=self.elsif[i]
                if i==len(self.elsif)-1:
                    inst=Ifclass(inst.exp,inst.cif,inst.elsif,self.celse)
                else:
                    inst = Ifclass(inst.exp,inst.cif,inst.elsif, [tmp])
                tmp=inst

            cif=Ifclass(self.exp,self.cif,None,[tmp])
            cad=cif.traducir(entorno).codigo3d
            self.codigo3d=cad

        elif self.elsif!=None:
            lv = entorno.newlabel()
            lf = entorno.newlabel()
            lend = entorno.newlabel()
            # pongo en codigo el temporal  de la expresion
            exp = self.exp.traducir(entorno)
            cad = exp.codigo3d
            cond = exp.temp
            # condicional del if que hace que se salte al codigo verdadero
            cad += 'if ' + cond + ': \n \t goto ' + lv + '\ngoto ' + lf + '\n'
            # salto hacia el final si no fue verdadera la expresion
            cad += 'label ' + lv + '\n'
            # instrucciones dentro del if
            instrif = self.cif
            for instr in instrif:
                cad += str(instr.traducir(entorno).codigo3d)
            # salto hacia el final porque ya entro al if
            cad += 'goto' + lend + '\n'
            # codigo que sigue despues del if
            cad += 'label ' + lf + '\n'
            # codigo del siguiente if (elsif)
            for ins in self.elsif:
                cad += ins.traducir(entorno).codigo3d
            #etiqueta del final
            cad += 'label ' + lend + '\n'
            self.codigo3d = cad
        elif self.celse!=None:
            lv = entorno.newlabel()
            lf = entorno.newlabel()
            lend = entorno.newlabel()
            # pongo en codigo el temporal  de la expresion
            exp = self.exp.traducir(entorno)
            cad = exp.codigo3d
            cond = exp.temp
            # condicional del if que hace que se salte al codigo verdadero
            cad += 'if ' + cond+ ': \n \t goto ' + lv + '\ngoto ' + lf + '\n'
            # salto hacia el final si no fue verdadera la expresion
            cad += 'label ' + lv + '\n'
            # instrucciones dentro del if
            instrif = self.cif
            for instr in instrif:
                cad += str(instr.traducir(entorno).codigo3d)
            # salto para que no haga el codigo del else
            cad += 'goto ' + lend + '\n'
            # aqui van las instrucciones del else
            cad += 'label ' + lf + '\n'
            # codigo del else
            for ins in self.celse:
                cad += ins.traducir(entorno).codigo3d
            # codigo al final del if
            cad += 'label ' + lend + '\n'
            self.codigo3d = cad
        return self


