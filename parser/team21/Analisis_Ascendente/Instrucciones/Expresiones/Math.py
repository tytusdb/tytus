import  math
import random
from tytus.parser.team21.Analisis_Ascendente.Instrucciones.instruccion import *
from tytus.parser.team21.Analisis_Ascendente.Instrucciones.expresion import *
import  tytus.parser.team21.Analisis_Ascendente.Instrucciones.Expresiones.Trigonometrica as  Trigonometrica
import tytus.parser.team21.Analisis_Ascendente.Instrucciones.Expresiones.Expresion as Expresion
import hashlib
class Math_(Instruccion):
    def __init__(self, nombre, E1, E2,fila,columna):
        self.nombre = nombre
        self.E1 = E1
        self.E2 = E2
        self.fila = fila
        self.columna = columna


    def Resolver(mathe,ts, Consola,exceptions):

        #Consola.append('E1 -- ' + mathe.nombre + '\n')
        #Consola.append('E2 -- ' + type(mathe.E2).__name__ + '\n')


        if isinstance(mathe,Math_):
            if mathe.E1 == None and mathe.E2 == None:
                if mathe.nombre == 'PI':
                    return math.pi
                elif mathe.nombre == 'RANDOM':
                    return random.random()
            else:


                if mathe.E2 == None: # operaciones de un valor
                    num1 = Math_.Resolver(mathe.E1,ts,Consola,exceptions)
                    if mathe.nombre == 'LN' or mathe.nombre == 'LOG':
                        return math.log(float(num1))
                    elif mathe.nombre == 'ABS':
                        return  abs(num1)
                    elif mathe.nombre == 'CBRT':
                        return num1 ** (1/3)
                    elif mathe.nombre == 'CEIL' or mathe.nombre == 'CEILING':
                        return math.ceil(num1)
                    elif mathe.nombre == 'DEGREES':
                        return  math.degrees(num1)
                    elif mathe.nombre == 'EXP':
                        return math.exp(num1)
                    elif mathe.nombre == 'FACTORIAL':
                        return math.factorial(int(num1))
                    elif mathe.nombre == 'FLOOR':
                        return  math.floor(num1)
                    elif mathe.nombre == 'LOG10':
                        return  math.log10(num1)
                    elif mathe.nombre == 'RADIANS':
                        return  math.radians(num1)
                    elif mathe.nombre == 'ROUND':
                        return  round(num1)
                    elif mathe.nombre == 'SIGN':
                        if num1 >= 0:
                            return 1
                        else:
                            return  -1
                    elif mathe.nombre == 'SQRT':
                        return  math.sqrt(num1)
                    elif mathe.nombre == 'TRUNC':
                        return  math.trunc(num1)
                    elif mathe.nombre == 'SUM':
                         return math.fsum(num1)
                    elif mathe.nombre == 'MD5':
                        return hashlib.md5(str(num1).encode("utf-8")).hexdigest()
                    elif mathe.nombre == 'WIDTH_BUCKET':
                        print("whidth bucket")
                        print(mathe.E1)
                        elementos = mathe.E1

                        valor = elementos[0].valor
                        min = elementos[1].valor
                        max = elementos[2].valor
                        count = elementos[3].valor


                        temp = (max - min) / count
                        contador = float(min)
                        cubo = 0
                        if float(valor) == contador:
                            return 1
                        while contador < float(max):
                            if float(valor) < contador:
                                return cubo

                            contador += temp
                            cubo += 1

                        return cubo + 1


                else:
                    num1 = Math_.Resolver(mathe.E1,ts,Consola,exceptions)
                    num2 = Math_.Resolver(mathe.E2,ts,Consola,exceptions)
                    if mathe.nombre == 'DIV':
                        return num1/num2
                    elif mathe.nombre == 'GCD':
                        return math.gcd(num1,num2)
                    elif mathe.nombre == 'MOD':
                        return num1 % num2
                    elif mathe.nombre == 'POWER':
                        return  num1 ** num2
        elif isinstance(mathe, Trigonometrica.Trigonometrica):
            return Trigonometrica.Trigonometrica.Resolver(mathe,ts,Consola,exceptions)
        elif isinstance(mathe,Math_):
            return Math_.Resolver(mathe,ts,Consola,exceptions)
        elif isinstance(mathe, Primitivo):
            return  mathe.valor
        elif isinstance(mathe, Expresion.Expresion):
            return Expresion.Expresion.Resolver(mathe,ts,Consola,exceptions)

