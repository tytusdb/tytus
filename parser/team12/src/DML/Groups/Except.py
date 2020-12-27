import sys, os.path

storage = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')) + '\\DML\\Groups')
sys.path.append(storage)

from RespuestaSelect import RespuestaSelect

class Except():
    def __init__(self, Resp1 = None, Resp2 = None):
        self.Resp1 = Resp1
        self.Resp2 = Resp2
        self.Respuesta = RespuestaSelect()


    def execute(self, parent):
        if len(parent.hijos) ==2 :
            self.Resp1 = parent.hijos[0].execute(None)
            self.Resp2 = parent.hijos[1].execute(None)
        if self.Resp1 != None and self.Resp2 != None:
            if len(self.Resp1.encabezados) == len(self.Resp2.encabezados):
                for i in range(0, len(self.Resp1.tipos)):
                    if self.Resp1.tipos[i] != self.Resp2.tipos[i]:
                        self.Respuesta.data = None
                        return self.Respuesta
                respuesta = RespuestaSelect()
                respuesta.tipos = self.Resp1.tipos
                respuesta.encabezados = self.Resp1.encabezados
                
                listaResp = []

                for data in self.Resp1.data:
                    if not(data in self.Resp2.data):
                        listaResp.append(data)
                
                respuesta.data= listaResp

                return respuesta
            else:
                print("Se debe de tener la misma cantidad de columnas en el select")

        self.Respuesta.data = None
        return self.Respuesta
            
