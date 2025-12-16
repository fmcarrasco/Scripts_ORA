# Scripts ORA
Codigos para realizar y facilitar algunas de las tareas que se realizan en la ORA: Cambio de tamaño de imagenes, Semanales, Reserva, Agua Util Decadial.

A continuación se detalla la función que tienen los scripts en cada carpeta:

## AguaUtilDecadial

Esta carpeta contiene los scripts para calcular y generar los mapas de agua util decadial y sus anomalías (todo para departamentos) y también los scripts para calcular el agua util decadial por cuartel utilizado para un índice.

Si es **primera vez que se utiliza, revisar las carpetas**.
Revisar los siguientes archivos y modificar las carpetas de acuerdo a como este organizado en cada computadora

1. `namelist_agua_util.txt`: Revisar todas las carpetas y ubicarlas de acuerdo a su maquina. Cualquier duda, revisar el [instructivo](https://docs.google.com/document/d/1xEYE-H-Ul1XOV13QOQEJh78HA3IRZgH1/edit?rtpof=true#heading=h.gjdgxs)
2. `1resumen_AguaUtil_depto.py`: revisar las lineas 33 a 38.
3. `2proc_final_depto.py`: revisar lineas 21 a 28 y ajustar las carpetas según corresponda a su máquina.
4. `3resumen_AguaUtil_cuartel.py`: revisar lineas 32 a 41.
5. `4proc_final_cuartel.py`: Revisar y modificar la ruta de las carpetas en las lineas 49 a 56.



## MapasControl

Esta carpeta contiene un script en python que permite hacer los mapas control cada lunes y revisar los datos que ingresan y también como quedo la interpolación. Los detalles se pueden ver en el [instructivo](https://docs.google.com/document/d/1u7-_dUJcydFzMHCWmDmdbWidSVH3g6g2/edit#bookmark=id.wrd0ork2lmhj)

El script *run_mapas_control.py* solo necesita modificar la ruta de las carpetas de acuerdo a SU computadora en las lineas 18 a 21.

Luego de eso genera una carpeta output con las imagenes que se utilizan para evaluar los datos de carga e interpolación.

## MapasReserva

Esta carpeta contiene un script para actualizar el archivo excel de reservas y también actualizar los shapefiles que permiten hacer los mapas que se publican.

Se debe modificar el archivo config.txt dentro de la carpeta. esto depende de las rutas y datos de SU computadora. 

Las dudas se pueden revisar en el [instructivo](https://docs.google.com/document/d/1N3-AjRKuhjyW0VXT1TVjIRkK35qXSDTk/edit)

El script genera una carpeta de salida con:

1. Archivo excel Reservas_al_YYYYMMDD.xlxx que contiene para cada centroide el valor de agua util para cada cultivo. 
2. Shapefiles de mapeo, actualizados con los datos a la fecha. A priori al reemplazar donde se encuentra el proyecto en ArcGIS o QGis, debiera levantar actualizado.
3. Una carpeta con la fecha que contiene los shapefiles ya con el nombre como se debe subir a la página de descargas de la web ORA.


## Resize_Imagenes

Esta carpeta contiene un script que actualmente recibe una carpeta de entrada, busca las imagenes dentro y devuelve una copia con tamaño distinto en una carpeta que cada uno utilice. Actualmente esta hecho para cambiar el tamaño de las imagenes de balance hídrico por estación.

Cambiar las rutas en las líneas 45 y 46 del script

## Seguimiento_PP_T

Esta carpeta contiene el script para generar las figuras que se encuentran en la web ORA de seguimiento de temperatura y precipitación [link](http://www.ora.gob.ar/pp_t.php).

Antes de correr el script, modificar el archivo `config_database.txt` que contiene las rutas para la base de datos ORA en formato access.

Una vez modificado, correr el script:

`python run_seguimiento_pp_t.py dd-mm-yyyy`

reemplazando la fecha por la cual se desea correr el script.

# FIN