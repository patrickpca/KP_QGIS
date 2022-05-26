import pandas as pd
import numpy as np
import gsw
import matplotlib.pyplot as plt 

from mpl_toolkits.basemap import Basemap
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

###############################################################################
###############################################################################

def kp(lon,lat,dist_segmento,n):
    '''
    

    Parameters
    ----------
    lon : DataFrame
        Longitude dos segmentos originais.
        
    lat : DataFrame
        Latitude dos segmentos originais.
    
    dist_segmento : float
        Valor em metros da distância de corte requerida
        
    n : float
        Número de subseções entre os segmentos que serão somados para encontrar a distância requerida aproximada\
            .

    Returns
    -------
    lox : DataFrame
        Longitude dos segmentos reamostrados.
        
    lax : DataFrame
        Latitude dos segmentos reamostrados.

    '''

    lonx=pd.DataFrame()
    latx=pd.DataFrame()
    for count in range(len(df)-1):
        lonx = lonx.append(pd.DataFrame(np.linspace(lon[count],lon[count+1],n)))
        latx = latx.append(pd.DataFrame(np.linspace(lat[count],lat[count+1],n)))
                
    lox=pd.DataFrame();lox=lox.append([lon[0]])
    lax=pd.DataFrame();lax =lax.append([lat[0]])
    aux=0;ind=0;
    
    count=0;
    while count < len(lonx)-1 :
        k = gsw.distance(lonx.iloc[count:count+2,0],latx.iloc[count:count+2,0])
        aux = aux+ k
        if (aux > dist_segmento):
            lox=lox.append(pd.DataFrame([lonx.iloc[count-1,0]]))
            lax=lax.append(pd.DataFrame([latx.iloc[count-1,0]]))
            aux=0
        count+=1
    
    k = gsw.distance(lox.iloc[:,0],lax.iloc[:,0])
    print (f'Distância entre os segmentos é de:\n\
           max: {np.max(k)}, \n\
           min: {np.min(k)}\n\
           média: {np.mean(k)}\n\
           Para maior precisão aumente o valor de n!!')
    
    
    return lox,lax

###############################################################################
###############################################################################

##


df = pd.read_csv(r'dado.xyz')
lon=df['lon']
lat=df['lat']

n=1000 # mil divisões
dist_segmento = 1000 #1km
                        
###
lox,lax = kp(lon,lat,dist_segmento,n)
###


            

## Visualizaçao dos pontos        
fig, ax = plt.subplots(1, 1, figsize=(35,20),
                        subplot_kw={'projection': ccrs.PlateCarree()})
ax = plt.axes(projection=ccrs.PlateCarree())
# ax.coastlines()
ax.add_feature(cfeature.COASTLINE, linewidth=1)
ax.plot(lox, lax ,'o',transform=ccrs.PlateCarree(),lw=5)
ax.plot(lon, lat, 'o',transform=ccrs.PlateCarree(),lw=5,alpha=0.4)

gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,\
                    linewidth=2, color='gray', alpha=0.2, linestyle='--')
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.xlabel_style = {'size': 30 ,'color': 'black','weight': 'bold'}
gl.ylabel_style = {'size': 30, 'color': 'black', 'weight': 'bold'}
gl.xlabels_top = False
gl.ylabels_left = True
gl.ylabels_right = False
plt.legend(['dado reamostradas', 'dado original'])
# plt.show()
