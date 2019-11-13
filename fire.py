
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import folium
#from mpl_toolkits.basemap import Basemap
import os
#os.environ['PROJ_LIB'] = 'D:\\Anaconda3\\Lib\\site-packages\\mpl_toolkits\\basemap'
pd.set_option('display.max_columns', None)

outages = pd.read_csv('outage_snapshots.csv')
geo = outages[['regionName_label', 'latitude', 'longitude']]
geo = geo.rename({'regionName_label': 'Place'}, axis='columns')
geo = geo.groupby(['Place']).mean()
#print(geo)
outages = outages[['outage', 'estCustAffected', 'snapshot_label', 'regionName_label']]
	#'latitude', 'longitude']]
outages = outages.rename({'regionName_label': 'Place'}, axis='columns')
#print(outages.shape)
outages = outages[outages.groupby('outage')['snapshot_label'].transform(max) == \
	outages['snapshot_label']]
outages = outages.drop(['outage', 'snapshot_label'], 1) 
outages = outages.groupby(['Place']).sum()
outages = pd.merge(outages, geo, on='Place', how='left')

#print(outages.head())
#print(outages.shape)

#outages.sort_values('outage', ascending=False).drop_duplicates(['outage', 'snapshot_label'], inplace=True)
pop_income = pd.read_csv('california_pop_income.csv')
pop_income = pop_income.replace('[7]', '$0,')
#print(pop_income.head())
pop_income['Per capita income'] = pop_income['Per capita income'].str.replace('$', '')
pop_income['Per capita income'] = pop_income['Per capita income'].str.replace(',', '')
pop_income['Median household income'] = pop_income['Median household income'].str.replace(',', '')
pop_income['Median household income'] = pop_income['Median household income'].str.replace('$', '')
pop_income['Median family income'] = pop_income['Median family income'].str.replace(',', '')
pop_income['Median family income'] = pop_income['Median family income'].str.replace('$', '')
pop_income = pop_income.drop('County', 1)
#print(len(outages['outage'].unique().tolist()))
#print('meow')
#print(pop_income.head())
#print(pop_income.shape)
combo = pd.merge(outages, pop_income, on='Place', how='inner')
#combo = combo[['outage', 'estCustAffected,']]
#print(combo.head())
#print(combo.shape)
#print(combo)

lon = combo['longitude'].values
lat = combo['latitude'].values
dens = combo['Population Density'].astype(int).values
pop = combo['Population']
aff = combo['estCustAffected'].astype(int).values
#print(aff)
inc = combo['Per capita income'].astype(int).values
#print(inc)

start_lat = 39
start_lon = -122

folium_map = folium.Map(location=[start_lat, start_lon], 
						zoom_start = 8)#,
						#tiles="CartoDB dark_matter")

cmap = cm.get_cmap('viridis', 12)
for index, row in combo.iterrows():
	#print(row['estCustAffected'])
	folium.CircleMarker(location=(row['latitude'], row['longitude']),
						radius=int(row['Per capita income'])/5000,
						color=cmap(int(row['estCustAffected'])),
						fill=True).add_to(folium_map)

folium_map.save('./docs/my_map.html')

'''
# 1. Draw the map background
fig = plt.figure(figsize=(8, 8))
m = Basemap(projection='lcc', resolution='h', 
            lat_0=37.5, lon_0=-119,
            width=1E6, height=1.2E6)
m.shadedrelief()
m.drawcoastlines(color='gray')
m.drawcountries(color='gray')
m.drawstates(color='gray')

# 2. scatter city data, with color reflecting population
# and size reflecting area
m.scatter(lon, lat, latlon=True,
          c=inc, s=aff/10,
          cmap='hot', alpha=0.5)

# 3. create colorbar and legend
#plt.colorbar(label=r'$\log_{10}({\rm population})$')
#plt.colorbar(label='Population Density')
plt.colorbar(label='Per Capita Income')
#plt.clim(3, 7)

# make legend with dummy points
for a in [100, 500, 1000]:
    plt.scatter([], [], c='k', alpha=0.5, s=a/10,
                label=str(a) + ' Persons affected by Power Outage')
plt.legend(scatterpoints=1, frameon=False,
           labelspacing=2, loc='lower left');

plt.title('Income and Customers Affected by Electric Outage due to Fires')
plt.show()
'''
