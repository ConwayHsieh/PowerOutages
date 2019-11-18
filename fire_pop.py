
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib import cm
import folium
from folium.map import FeatureGroup
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

mindens = dens.min()
maxdens = dens.max()

start_lat = 39
start_lon = -121.5


dens_steps = [0, 2000, 4000, 6000, 7000, 9000, 10000]
feature_group1 = FeatureGroup(name='Less than 2000 Population Density')
feature_group2 = FeatureGroup(name='2000 - 4000 Population Density')
feature_group3 = FeatureGroup(name='4000 - 6000 Population Density')
feature_group4 = FeatureGroup(name='6000 - 7000 Population Density')
feature_group5 = FeatureGroup(name='7000 - 9000 Population Density')
feature_group6 = FeatureGroup(name='More than 10000 Population Density')

feat_list = [feature_group1, feature_group2, feature_group3, feature_group4, \
    feature_group5, feature_group6]

folium_map = folium.Map(location=[start_lat, start_lon], 
                        zoom_start = 8)
cmap = cm.LinearColormap(colors=['red', 'yellow'], index=[mindens, maxdens],
    vmin=mindens, vmax=maxdens)
cmap = cmap.to_step(n=12, method='log', round_method='log10')
cmap.caption = 'Population Density'

for index, row in combo.iterrows():
    popup_text = """Place: {}<br> 
                    Estimate Customers Affected: {}<br>
                    Population Density of Place: {}"""
    popup_text = popup_text.format(row['Place'],
                                   int(row['estCustAffected']),
                                   int(row['Population Density']))

    density = int(row['Population Density'])
    for i in range(len(feat_list)):
        if density in range(dens_steps[i], dens_steps[i+1]):
            f = feat_list[i]

    folium.CircleMarker(location=(row['latitude'], row['longitude']),
        radius=row['estCustAffected']/700,
        color=cmap(density),
        popup=popup_text,
        fill=True).add_to(f)

for feat_group in feat_list:
    folium_map.add_child(feat_group)
folium_map.add_child(cmap)
folium.LayerControl().add_to(folium_map)

title_html = '''
    <html>
    <head>
        <title>Power Outages Map: Population Density</title>
    </head>
    <body>
        <p>This map shows <strong>number of customers affected by power outages
        </strong><em>(shown in size or radius of each circle)</em> vs the 
        <strong>population density</strong> of the places these customers reside 
        <em>(colormap)</em> </p>
        <p>You can <em>click each bubble</em> to find more detailed information
        such as the population densityor number of customers affected</p>
        <p><strong>Filtering by population density</strong> is available by checking or 
        unchecking population density categories after hovering over the layers button in 
        the right hand corner, under the color bar</p>
    </body>
    </html>
    '''
folium_map.get_root().html.add_child(folium.Element(title_html))
folium_map.save('./docs/poweroutages_population.html')
