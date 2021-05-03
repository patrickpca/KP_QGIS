# -*- coding: utf-8 -*-
"""
Spyder Editor

Autor: Patrick Coser 

Convert RPL para KP


KP - Ponto por kilometro (1)
"""


# path = r'D:\EGS\Python\Convert_KP\RPL_CRS01_MCP-BEL_SEG1_13Octob2020.txt'

# names = ['X', 'Y', 'Depth']

# dado_rpl = pd.read_csv(path, header=None, names=names)

##############################################################################
##############################################################################
##############################################################################


import pandas as pd
import numpy as np
import csv

path2 = r'D:\Git\arquivos\malbec_praia_grande.xls'

cols = [2,3,4,5,6,7]

dado_xls = pd.read_excel(path2, sheet_name='RPL', header = 2, usecols = cols, names=[0,1,2,3,4,5]).dropna()

dado_xls.reset_index(drop=True, inplace = True)


long = dado_xls[3].astype(int).astype(str) + '° ' + dado_xls[4].map('{:,.5f}'.format) + '\' ' + dado_xls[5] 

lat = dado_xls[0].astype(int).astype(str) + '° ' + dado_xls[1].map('{:,.5f}'.format) + '\' ' + dado_xls[2]
aux =(dado_xls[0]*0-999999).astype(int).astype(str)

rpl = pd.DataFrame()
rpl[0] = long 
rpl[1] = lat
rpl[2]= aux

rpl.to_csv(r'D:\Git\arquivos\rpl.xyz',index=False, header=None)#, sep=',')





import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt
# import gsw
# from mpl_toolkits.basemap import Basemap
import cartopy.crs as ccrs
import cartopy.feature as cfeature
# import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
# import netCDF4 as nc

# from mpl_toolkits.mplot3d import Axes3D
# import cmocean as cm
# from matplotlib.collections import PolyCollection
# from mpl_toolkits.mplot3d.art3d import Poly3DCollection


lat2 = -(dado_xls[0] + dado_xls[1]/60)
lon2 = -(dado_xls[3] + dado_xls[4]/60)

r_lat2_max = max(lat2.astype(int))+2
r_lat2_min = min(lat2.astype(int))-2

r_lon2_max = max(lon2.astype(int))+2
r_lon2_min = min(lon2.astype(int))-2

fig, ax = plt.subplots(1, 1, figsize=(35,20),
                        subplot_kw={'projection': ccrs.PlateCarree()}) #platecarree é mercator 
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
ax.add_feature(cfeature.COASTLINE, linewidth=1)

im=ax.plot(lon2,lat2, transform=ccrs.PlateCarree())
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                    linewidth=2, color='gray', alpha=0.2, linestyle='--')
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
ax.stock_img()
ax.set_extent([r_lon2_max, r_lon2_min, r_lat2_max, r_lat2_min], crs=ccrs.PlateCarree())
# ax.set_extent([-43, -48, -22, -27], crs=ccrs.PlateCarree())
gl.xlabel_style = {'size': 20 ,'color': 'black','weight': 'bold'}
gl.ylabel_style = {'size': 20, 'color': 'black', 'weight': 'bold'}
gl.xlabels_top = False
gl.ylabels_left = True
gl.ylabels_right = False
plt.title('', fontsize=40, fontweight='bold')

# plt.savefig('Fig_thetao_mean.png')
# plt.show()

