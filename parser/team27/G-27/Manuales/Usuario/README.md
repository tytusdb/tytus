# Manual de Usuario :closed_book:

### Integrantes
201800634	ANTHONY FERNANDO SON MUX

201801181	CÉSAR EMANUEL GARCIA PÉREZ

201801195	JOSE CARLOS JIMENEZ

201801237	JOSÉ RAFAEL MORENTE GONZÁLEZ

## Contenido
1. [Query Tool](#id1)
2. [Ejecución Programa](#id2)
3. [Reportes](#id3)

## Query Tool<a name="id1"></a>
Sub componente que consiste en una ventana gráfica similar al Query Tool de pgadmin de PostgreSQL, para ingresar consultas y mostrar los resultados, incluyendo el resultado de dicho análisis.

![Query Tool](https://res.cloudinary.com/dtpqmjmhk/image/upload/v1608784300/OLC2/Captura_de_Pantalla_2020-12-23_a_la_s_16.17.46_yp1q8f.png)

## Ejecución Programa<a name="id2"></a>
Para poder ejecutar perfectamente el programa se debe de seguir los siguientes pasos.
1. Ingresar a la consola y ejecutar el programa

```sh
$ cd G-27
$ python inicio.py
```
2. Se abre una ventana 
3. Ingresar las instrucciones en la entrada.
4. La salida se muestra en el TextArea inferior
5. Al presionar el botón (Escoba) se limpia TextArea de Entrada para ingresar nuevo texto.
6. Al presionar el boton (Esferas) se genera el reporte AST
7. Al presionar el botón (Documento) genera el reporte dinámico BNF

![Instrucciones](https://res.cloudinary.com/dtpqmjmhk/image/upload/v1608789352/OLC2/Captura_de_Pantalla_2020-12-23_a_la_s_23.55.25_xzkf3u.png)


## Reportes <a name="id3"></a>
Para la generación de reportes en la interfaz gráfica lleva 2 botones para generar el reporte AST y otro para el reporte BNF, los demás reportes se generan ejecutando el análisis.

### Reportes AST
El reporte AST se realiza recorriendo la gramática ascendente y vamos uniendo cada nodo producido, para la generación del reporte se utilizó Grapvhiz, este nos genera un grafico en formato pdf. Graphviz es un programa de visualización gráfica de fuente abierta.

![Instrucciones](https://res.cloudinary.com/dtpqmjmhk/image/upload/v1608789283/OLC2/Captura_de_Pantalla_2020-12-23_a_la_s_23.52.32_gd8hq0.png)

### Reportes BNF
El reporte BNF dinámico se realizó recorriendo la gramática ascendente. Este reporte nos da una panorámica acerca de las producciónes que fueron utilizadas para correr ciertas instrucciones.

![Instrucciones](https://res.cloudinary.com/dtpqmjmhk/image/upload/v1608789283/OLC2/Captura_de_Pantalla_2020-12-23_a_la_s_23.51.14_hziuo4.png)

### Reporte Errores
El reporte de errores se presentara en la salida de la interfaz gráfica entre estos incluye errores lexicos, sintacticos, semanticos y la tabla de simbolos.
