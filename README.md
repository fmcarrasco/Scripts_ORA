# Scripts ORA
Codigos para realizar y facilitar algunas de las tareas que se realizan en la ORA: Cambio de tamaño de imagenes, Semanales, Reserva, Agua Util Decadial.

Las pruebas se hicieron a partir de un *environment* creado con CONDA, cuyos paquetes necesarios para correr estos scripts se encuentran en el archivo
`ora_environment.yml` que se encuentra en la carpeta **z-requerimientos**. Más información sobre CONDA se puede ver [aquí](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

A continuación se detalla las funciones que resuelve los scripts y vamos por cada carpeta de este proyecto revisando:

## AguaUtilDecadial

Esta carpeta contiene los scripts para calcular y generar los mapas de agua util decadial y sus anomalías (todo para departamentos) y también los scripts para calcular el agua util decadial por cuartel utilizado para un índice.

Si es **primera vez que se utiliza, revisar las carpetas**.
Revisar los siguientes archivos y modificar las carpetas de acuerdo a como este organizado en cada computadora

1. `namelist_agua_util.txt`: Revisar todas las carpetas y ubicarlas de acuerdo a su maquina. Cualquier duda, revisar el [instructivo](https://docs.google.com/document/d/1xEYE-H-Ul1XOV13QOQEJh78HA3IRZgH1/edit?rtpof=true#heading=h.gjdgxs)

Se da aca una descripción de las variables/carpetas/opciones que van en dicho archivo:

* **deca:** Fecha de inicio de la década en formato "YYYY-mm-dd".
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

Esta carpeta contiene un script en python que permite hacer los mapas de control cada lunes y revisar los datos que ingresan y como quedaron los datos interpolados. Los detalles se pueden ver en el [instructivo](https://docs.google.com/document/d/1u7-_dUJcydFzMHCWmDmdbWidSVH3g6g2/edit#bookmark=id.wrd0ork2lmhj)

El script **run_mapas_control.py** solo necesita que se modifiquen los parametros en el archivo `config_mapas_control.txt` para el cual damos una descripción:

* **archivo_in:** Ruta y nombre del archivo con datos de entrada.
* **archivo_out:** Ruta y nombre del archivo con datos de salida.
* **shape_provincias:** Ruta y nombre donde se encuentra el archivo: *provincias_geo.shp*.
* **shape_deptos:** Ruta y nombre donde se encuentra el archivo: *dptos_geo.shp*.

Luego de eso genera una carpeta *output* con las imagenes que se utilizan para evaluar los datos de carga e interpolación para PP, TMIN y TMAX.


## MapasMensuales

Esta carpeta contiene scripts para hacer interpolar utilizando Krigging los mapas mensuales: AAPP y Palmer. Al finalizar el script genera una carpeta con el nombre {YearMes} corresponde y que contiene los archivos geotiff para mapear en QGIS o ArcGIS. Además dentro de esa carpeta se arman figuras que contienen una versión simple con los mapas y el valor de la variable en las estaciones para corroborar si las interpolaciones dieron bien.

No hay que modificar el código, pero si es primera vez que usan el script deben abrir con un editor de texto el archivo `datos_in.txt` y modificar los parametros:

* **fecha_i:** Fecha de inicio del mapa mensual en formato YYYY-MM-DD.
* **fecha_f:** Fecha de fin del mapa mensual en formato YYYY-MM-DD.
* **f_palmer:** Ruta del archivo generado con programa_ora.exe para PALMER.
* **f_aapp:** Ruta del archivo generado con programa_ora.exe para Anomalía PP (AAPP).
* **provincias_shp:** Ruta del archivo SHAPEFILE de provincias argentinas del IGN.
* **argentina_shp:** Ruta del archivo SHAPEFILE del límite de Argentina del IGN.
* **carpeta_salida:** Ruta para donde se van a guardar las salidas del script (ruta de carpeta).


## MapasReserva

Esta carpeta contiene un script para actualizar el archivo excel de reservas y también actualizar los shapefiles que permiten hacer los mapas que se publican.

Se debe modificar el archivo `config.txt` dentro de la carpeta. esto depende de las rutas y datos de SU computadora y se da acá una descripción de ellas:

* **archivo_balance:** Ruta y nombre al archivo balances.txt
* **data_folder:** Ruta de la carpeta donde se encuentran los shapefile IN (previo a actualización) para los mapas de reserva (Reservas, Reservas500, CBA, etc.).
* **output:** Ruta de la carpeta donde se van a guardar las salidas de este script.
* **fecha:** Fecha en formato YYYYMMDD que corresponde al balance hídrico.
* **prioridad_m11:** "True": Si tiene prioridad la primera fecha del maiz de primera. "False": Si tiene prioridad la segunda fecha del maíz de primera.
* **prioridad_m21:** "True": Si tiene prioridad la primera fecha del maiz de segunda. "False": Si tiene prioridad la segunda fecha del maíz de segunda.


Las dudas se pueden revisar en el [instructivo](https://docs.google.com/document/d/1N3-AjRKuhjyW0VXT1TVjIRkK35qXSDTk/edit)

El script genera una **carpeta de salida** con:

1. Archivo excel Reservas_al_YYYYMMDD.xlsx que contiene para cada centroide el valor de agua util para cada cultivo. 
2. Shapefiles de mapeo, actualizados con los datos a la fecha. A priori al reemplazar donde se encuentra el proyecto en ArcGIS o QGis, debiera levantar actualizado y listo para mapear.
3. Una carpeta dentro de **output** cuyo nombre es la **fecha** que contiene los shapefiles tal como se deben subir a la página de descargas de la web ORA.


## MapasSemanales

Esta carpeta contiene scripts para hacer los mapas semanales (Tmin/Tmax/PP/AA etc.). Al finalizar el script genera una carpeta con el nombre de {fecha_ini}_{fecha_fin} que contiene los archivos geotiff para mapear en QGIS o ArcGIS. Además dentro de esa carpeta se arman figuras que continen una versión simple con los mapas y el valor de
la variable en las estaciones.

No hay que modificar el código, pero si es primera vez que usan el script deben abrir con un editor de texto el archivo `datos_in.txt` y modificar los parametros:

* **fecha_i:** Fecha de inicio del mapa semanal en formato YYYY-MM-DD.
* **fecha_f:** Fecha de fin del mapa semanal en formato YYYY-MM-DD.
* **file_5:** Ruta del archivo generado con el listado 5 de estaciones (PPMAXMIN_5-0).
* **file_51:** Ruta del archivo generado con el listado 5.1 de estaciones (PPMAXMIN_5-1).
* **file_sin_interp:** Ruta del archivo generado con el listado 5 de estaciones (PPMAXMIN_SIN INTERPOLADOS) y SIN INTERPOLADOS.
* **provincias_shp:** Ruta del archivo SHAPEFILE de provincias argentinas del IGN.
* **argentina_shp:** Ruta del archivo SHAPEFILE del límite de Argentina del IGN.
* **carpeta_salida:** Ruta para donde se van a guardar las salidas del script (ruta de carpeta).


## Resize_Imagenes

Esta carpeta contiene un script que actualmente recibe una carpeta de entrada, busca las imagenes dentro y devuelve una copia con tamaño distinto en una carpeta que cada uno utilice. 

Hay que pasar los parámetros al archivo `config_file.txt` que contiene estas variables:

* **input_folder:** Carpeta con las imagenes originales.
* **output_folder:** Carpeta para guardar las imagenes con el nuevo tamaño.
* **tipo:** Para elegir que tamaño se hace el resize. Actualmente hay 2 opciones que pueden ir (incluir las comillas): 
    * *"BalanceHidrico"*: Modifica el tamaño para el seguimiento de BH por estación.
    * *"MapasSemanales"*: Modifica el tamaño para los mapas semanales y subirlos a la web.
    * *"MapasReserva"*: Modifica el tamaño para los mapas de reserva y subirlos a la web.

Una vez que se modifican los parametros en el archivo de configuración, correr el script utilizando:

`python resizer_images.py`

## Seguimiento_PP_T

Esta carpeta contiene el script para generar las figuras que se encuentran en la web ORA de seguimiento de temperatura y precipitación [link](http://www.ora.gob.ar/pp_t.php).

Antes de correr el script, modificar el archivo `config_database.txt` que contiene las rutas para la base de datos ORA en formato access.

Una vez modificado, correr el script:

`python run_seguimiento_pp_t.py dd-mm-yyyy`

reemplazando la fecha por la cual se desea correr el script.

# FIN