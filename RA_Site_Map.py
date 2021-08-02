import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
#from geopandas import GeoDataFrame

from mpl_toolkits.axes_grid1 import make_axes_locatable

df_state= pd.read_csv('Data-Table 1.csv')

def StateMap():
    
    df= df_state.copy()
    
    temp1= df.groupby('State')['Address'].count()
    temp1= temp1.to_frame()

    map_df= gpd.read_file('/Users/richa/Downloads/Igismap/Indian_States.shp')
    map_df['st_nm']= map_df['st_nm'].replace({'Odisha': 'Orissa', 'Puducherry': 'Pondicherry', 'Meghalaya': 'Megalaya',
                           'Dadara & Nagar Havelli': 'Dadra und Nagar Hav.', 'Daman & Diu': 'Daman und Diu',
                                             'Arunanchal Pradesh': 'Arunachal Pradesh'})
    # Merging dataframe and geodataframe
    merged= temp1.join(map_df.set_index('st_nm'), on= 'State')
    merged = gpd.GeoDataFrame(merged)

    # Range for the choropleth values
    vmin, vmax= temp1['Address'].min(), temp1['Address'].max()

    fig, ax= plt.subplots()
    ax.axis('off')
    ax.set_title('Site count State wise')

    # Creating colorbar
    sm= plt.cm.ScalarMappable(cmap= 'Spectral', norm= plt.Normalize(vmin= vmin, vmax= vmax))
    sm.set_array([])
    fig.colorbar(sm)

    # Plotting the map
    merged.plot(column= 'Address', cmap= 'Spectral', ax= ax)

    fig.savefig('State-wise.png')
    fig.show()
    return fig

def DistrictMap():
    
    df1= df_state.copy()
    
    temp_ra_dist= df1.groupby('District')['Address'].count()
    temp_ra_dist= temp_ra_dist.to_frame()

    dist_map_df= gpd.read_file('/Users/richa/Downloads/GIS_file_of_India_State,_District_and_Tehsil_Boundaries/commondata/ind_adm_shp/IND_adm3.shp')
    dist_map_df= dist_map_df.loc[:, ['NAME_2', 'geometry']]
    dist_map_df= dist_map_df.rename(columns= {'NAME_2': 'District'})
    dist_map_df['District']= dist_map_df['District'].str.upper()

    dist_map_df= dist_map_df.groupby('District').first()

    merged1= temp_ra_dist.join(dist_map_df, on= 'District')

    merged1 = gpd.GeoDataFrame(merged1)

    # Range for the choropleth values
    vmin1, vmax1= temp_ra_dist['Address'].min(), temp_ra_dist['Address'].max()

    fig1, ax1= plt.subplots()
    ax1.axis('off')
    ax1.set_title('Site count District wise')

    # Creating colorbar
    sm1= plt.cm.ScalarMappable(cmap= 'Spectral', norm= plt.Normalize(vmin= vmin1, vmax= vmax1))
    sm1.set_array([])
    fig1.colorbar(sm1)

    # Plotting the map
    merged1.plot(column= 'Address', cmap= 'Spectral', ax= ax1)

    fig1.savefig('District-wise.png')
    fig1.show()
    return fig1

StateMap()
DistrictMap()


