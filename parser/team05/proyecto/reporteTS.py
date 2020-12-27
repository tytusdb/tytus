import os
import webbrowser

def generarReporte(reporte) :
    f = open('reports/errorSeman.html', 'w')

    file1 = open("reports/inicio_error_semantico.txt", "r")
    file3 = open("reports/fin_error.txt", "r")
    html = file1.read()
    fin = file3.read()

    for key, v in reporte.simbolos.items():
        html += '''  <tr>
                    <td>''' + str(v.id) + '''</td>
                    <td>''' + str(v.tipo) + '''</td>
                </tr>'''
    html += fin
    f.write(html)
    f.close()
    webbrowser.open('file://' + os.path.realpath("reports/errorSeman.html"))


def generarTablaSimbolos(tabladeSimbolos) :
    f = open('reports/TablaSimbolos.html', 'w')

    file1 = open("reports/inicio_tabla_simbolos.txt", "r")
    file3 = open("reports/fin_error.txt", "r")
    html = file1.read()
    fin = file3.read()

    for key, v in tabladeSimbolos.symbols.items():
        html += '''  <tr>
                    <td>''' + str(v.type) + '''</td>
                    <td>''' + str(v.id) + '''</td>
                    <td>''' + str(v.value) + '''</td>
                </tr>'''
    html += fin
    f.write(html)
    f.close()
    webbrowser.open('file://' + os.path.realpath("reports/TablaSimbolos.html"))


def reporteErrores() :
    try :
        os.startfile('ReporteErrores.html')
    except :
        return 0