# Scripts ORA
Codigos para realizar y facilitar algunas de las tareas que se realizan en la ORA: Cambio de tamaño de imagenes, Semanales, Reserva, Agua Util Decadial.

A continuación se detalla la función que tienen los scripts en cada carpeta:

## AguaUtilDecadial

Esta carpeta contiene los scripts para calcular y generar los mapas de agua util decadial y sus anomalías (todo para departamentos) y también los scripts para calcular el agua util decadial por cuartel utilizado para un índice.

Si es **primera vez que se utiliza, revisar las carpetas**.
Revisar los siguientes archivos y modificar las carpetas de acuerdo a como este organizado en cada computadora

1. `namelist_agua_util.txt`: Revisar todas las carpetas y ubicarlas de acuerdo a su maquina. Cualquier duda, revisar el [instructivo](https://docs.google.com/document/d/1xEYE-H-Ul1XOV13QOQEJh78HA3IRZgH1/edit?rtpof=true#heading=h.gjdgxs)

Se da aca una descripción de las variables/carpetas/opciones que van en dicho archivo:

* **deca:** Fecha de inicio de la década.
* **todos_cult:** "SI": calcula sin discriminar cultivos; "NO": Calcula si el cultivo esta activo en la decada; "UNO": Calcula para un unico cultivo.
* **espec_cult:** Si la opcion todos_cult="UNO", esta variable permite especificar que cultivo se trabaja.
* **calcula_deca:** Si se calcula los archivos decadales historicos (opciones: "SI" o "NO").
* **calculo_por:** Si se trabaja por "departamento" o "cuartel".
* **opcion_fecha:** "0": calcula ultima fecha decadial del archivo; "1": Calcula para fecha dada en fecha_opcion.
* **fecha_opcion:** fecha en formato "YYYY-mm-dd" para la cual se calcula el decadial.
* **file_ind:** nombre del archivo que indica que cultivo se hace en la decada que se esta trabajando.
* **carpeta_ppal:** Carpeta donde estan los codigos.
* **carpeta_bal:** Carpeta donde están los balances diarios.
* **carpeta_deca:** Carpeta donde se guardan los balances decádiales.
* **carpeta_out:** Carpeta de salida general (estan los datos/logs del procesamiento)
* **carpeta_out_final:** Carpeta de salida final de los datos (donde va a estar lo que se usa para mapear).
* **carpeta_out_cuartel:** Carpeta de salida final para el calculo por cuartel.
* **carpeta_ret:** Carpeta donde se guardan los archivos de retículas.
* **archivo_ret_50:** Archivo reticula 1:50000.
* **archivo_ret_500:** Archivo reticula 1:500000.
* **guide_file:** Archivo guia de salida final para calculo por departamento.
* **guide_file_cuartel:** Archivo guia de salida final para calculo por cuartel.
* **std_folder:** Carpeta donde esta guardada la desviación estándar entre 2000-2020 para cada decadial.
* **avg_folder:** Carpeta donde esta guardada la media entre 2000-2020 para cada decadial.
* **shapefile_loc:** Archivo shapefile deptos_geo.shp. Permite generar el shapefile a plotear (debe tener la columna LINK).


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