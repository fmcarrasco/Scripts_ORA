import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as c
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def parse_config(file_path):
    import re
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Use regex to match the variable name and value
            match = re.match(r'(\w+)\s*=\s*"(.*)"', line.strip())
            if match:
                config[match.group(1)] = match.group(2)
    return config


def agrega_falsos(df, archivo_falsos):
    
    
    falsos = pd.read_csv(archivo_falsos, header=None)
    ####################
    quiaca_f = df.loc[df['Estacion'].str.contains('quiaca', case=False),:]
    rio_grande_f = df.loc[df['Estacion'].str.contains('o_grande', case=False),:]
    iguazu_f = df.loc[df['Estacion'].str.contains('iguaz', case=False), :]
    calafate_f = df.loc[df['Estacion'].str.contains('calafate', case=False), :]
    #
    quiaca_f.loc[:,'Estacion'] = falsos.iloc[0,0]
    quiaca_f.loc[:, 'Lat'] = falsos.iloc[0,1]
    quiaca_f.loc[:, 'Long'] = falsos.iloc[0,2]

    #
    rio_grande_f.loc[:,'Estacion'] = falsos.iloc[1,0]
    rio_grande_f.loc[:, 'Lat'] = falsos.iloc[1,1]
    rio_grande_f.loc[:, 'Long'] = falsos.iloc[1,2]
    #
    iguazu_f.loc[:,'Estacion'] = falsos.iloc[2,0]
    iguazu_f.loc[:, 'Lat'] = falsos.iloc[2,1]
    iguazu_f.loc[:, 'Long'] = falsos.iloc[2,2]
    #
    calafate_f.loc[:,'Estacion'] = falsos.iloc[3,0]
    calafate_f.loc[:, 'Lat'] = falsos.iloc[3,1]
    calafate_f.loc[:, 'Long'] = falsos.iloc[3,2]
    #
    df = pd.concat([df, quiaca_f], ignore_index=True)
    df = pd.concat([df, rio_grande_f], ignore_index=True)
    df = pd.concat([df, iguazu_f], ignore_index=True)
    df = pd.concat([df, calafate_f], ignore_index=True)
    #
    return df


def mapa_revision(pais, provincia, funcion_color, df, columna, raster):
    c_pp, cMap, bounds, norm = funcion_color
    provincias = gpd.read_file(provincia)
    pais = gpd.read_file(pais)
    fig = plt.figure(figsize=(15, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())  # Use Lat/Lon projection
    ax.add_geometries(provincias.geometry.values, crs=ccrs.PlateCarree(), facecolor='none', edgecolor='black', linewidth=1.5, zorder=9)
    scatter = ax.scatter(df['Long'], df['Lat'], c=df[columna], cmap=cMap, norm=norm, s=30, edgecolors='black', linewidth=0.5, transform=ccrs.PlateCarree(), zorder=10)
    #ax.contourf(xgrd, ygrd, grid, levels=bounds, cmap=cMap, norm=norm, transform=ccrs.PlateCarree(), zorder=8 )
    raster.rio.clip(pais.geometry.values, pais.crs).plot.contourf(ax=ax, levels=bounds, cmap=cMap, norm=norm, add_colorbar=False)
    # Add colorbar with custom ticks
    cbar = plt.colorbar(scatter, ax=ax, shrink=0.8, pad=0.05, label=columna)
    cbar.set_ticks(bounds)  # Set ticks at interval boundaries
    # longitude min, longitude max, latitude min, latitude max)
    ax.set_extent([-75, -50, -56, -21], crs=ccrs.PlateCarree())
    #ax.set_xlabel('Longitude')
    #ax.set_ylabel('Latitude')
    ax.set_title("")
    #ax.set_title(titulo, loc='left')

    return fig, ax