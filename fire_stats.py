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
outages = outages[['outage', 'estCustAffected', 'snapshot_label', 'regionName_label']]
outages = outages.rename({'regionName_label': 'Place'}, axis='columns')
outages = outages[outages.groupby('outage')['snapshot_label'].transform(max) == \
outages['snapshot_label']]
outages = outages.drop(['outage', 'snapshot_label'], 1) 
outages = outages.groupby(['Place']).sum()
outages = pd.merge(outages, geo, on='Place', how='left')
pop_income = pd.read_csv('california_pop_income.csv')
pop_income = pop_income.replace('[7]', '$0,')
pop_income['Per capita income'] = pop_income['Per capita income'].str.replace('$', '')
pop_income['Per capita income'] = pop_income['Per capita income'].str.replace(',', '')
pop_income['Median household income'] = pop_income['Median household income'].str.replace(',', '')
pop_income['Median household income'] = pop_income['Median household income'].str.replace('$', '')
pop_income['Median family income'] = pop_income['Median family income'].str.replace(',', '')
pop_income['Median family income'] = pop_income['Median family income'].str.replace('$', '')
pop_income = pop_income.drop('County', 1)
combo = pd.merge(outages, pop_income, on='Place', how='inner')
#print(combo.head())

'''
lon = combo['longitude'].values
lat = combo['latitude'].values
dens = combo['Population Density'].astype(int).values
pop = combo['Population']
aff = combo['estCustAffected'].astype(int).values
inc = combo['Per capita income'].astype(int).values
'''

combo['avg_inc'] = (combo['estCustAffected'].astype(int) * \
	combo['Per capita income'].astype(int))
print(combo['avg_inc'])
print(combo['avg_inc'].sum()/(combo['estCustAffected'].sum()))