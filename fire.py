
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib import cm
import folium
import branca
import branca.colormap as cm
import os
pd.set_option('display.max_columns', None)

outages = pd.read_csv('outage_snapshots.csv')
geo = outages[['regionName_label', 'latitude', 'longitude']]
geo = geo.rename({'regionName_label': 'Place'}, axis='columns')
geo = geo.groupby(['Place']).mean()
#print(geo)
outages = outages[['outage', 'estCustAffected', 'snapshot_label', 'regionName_label']]
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
#print(combo.head())
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

mininc = inc.min()
maxinc = inc.max()

start_lat = 39
start_lon = -122

folium_map = folium.Map(location=[start_lat, start_lon], 
						zoom_start = 8)
cmap = cm.LinearColormap(colors=['red', 'yellow'], index=[mininc, maxinc],
    vmin=mininc, vmax=maxinc)
cmap = cmap.to_step(n=12, method='log', round_method='log10')
cmap.caption = 'Per Capita Income in Dollars ($)'

for index, row in combo.iterrows():
    popup_text = """Place: {}<br> 
                    Estimate Customers Affected: {}<br>
                    Per Capita Income of Place: ${}"""
    popup_text = popup_text.format(row['Place'],
                                   int(row['estCustAffected']),
                                   row['Per capita income'])

    folium.CircleMarker(location=(row['latitude'], row['longitude']),
        radius=row['estCustAffected']/700,
        color=cmap(int(row['Per capita income'])),
        popup=popup_text,
        fill=True).add_to(folium_map)

folium_map.add_child(cmap)
folium_map.save('./docs/my_map.html')
