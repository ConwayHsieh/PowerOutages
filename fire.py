
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib import cm
import folium
from folium.map import FeatureGroup
import branca
import branca.colormap as cm
import os
#from uszipcode import SearchEngine
pd.set_option('display.max_columns', None)

outages = pd.read_csv('outages_zip.csv')
#print(outages.head())

lon = outages['longitude'].values
lat = outages['latitude'].values
dens = outages['pop_dens'].astype(int).values
pop = outages['pop']
aff = outages['estCustAffected'].astype(int).values
inc = outages['med_house_inc'].astype(int).values

thousand = 1000
mininc = inc.min()/thousand
maxinc = inc.max()/thousand

start_lat = 39
start_lon = -121.5

income_steps = [0, 30000, 50000, 80000, 100000, 200000]
feature_group1 = FeatureGroup(name='Less than $30,000 Per Capita Income')
feature_group2 = FeatureGroup(name='$30,000-$50,000 Per Capita Income')
feature_group3 = FeatureGroup(name='$50,000-$80,000 Per Capita Income')
feature_group4 = FeatureGroup(name='$80,000-$100,000 Per Capita Income')
feature_group5 = FeatureGroup(name='More than $100,000 Per Capita Income')

feat_list = [feature_group1, feature_group2, feature_group3, \
	feature_group4, feature_group5]

folium_map = folium.Map(location=[start_lat, start_lon], 
						zoom_start = 8)
cmap = cm.LinearColormap(colors=['red', 'yellow'], index=[mininc, maxinc],
    vmin=mininc, vmax=maxinc)
cmap = cmap.to_step(n=12, method='log', round_method='log10')
cmap.caption = 'Median Household Income in Thousands of Dollars ($1,000)'

for index, row in outages.iterrows():
    popup_text = """Zip Code: {}<br> 
                    Estimated Customers Affected: {}<br>
                    Population Density: {}<br>
                    Total Population: {}<br>
                    Median Household Income: ${}"""
    popup_text = popup_text.format(int(row['zip']),
                                   int(row['estCustAffected']),
                                   int(row['pop_dens']),
                                   int(row['pop']),
                                   int(row['med_house_inc']))

    income = int(row['med_house_inc'])
    for i in range(len(feat_list)):
        if income in range(income_steps[i], income_steps[i+1]):
            f = feat_list[i]

    folium.Circle(location=(row['latitude'], row['longitude']),
        radius=(row['estCustAffected'])/5,#/row['pop'])*500,
        #radius = (row['duration_hours'])*500,
        color=cmap(income/thousand),
        popup=popup_text,
        fill=True).add_to(f)

for feat_group in feat_list:
    folium_map.add_child(feat_group)
folium_map.add_child(cmap)
folium.LayerControl().add_to(folium_map)

'''
'''
#title_html = '''
'''
	<html>
	<head>
		<title>Power Outages Map</title>
	</head>
	<body>
		<p>This map shows <strong>number of customers affected by power outages
		</strong><em>(shown in size or radius of each circle)</em> vs the 
		<strong>per capita income</strong> of the places these customers reside 
		<em>(colormap)</em> </p>
		<p>You can <em>click each bubble</em> to find more detailed information
		such as the exact income or number of customers affected</p>
		<p><strong>Filtering by income</strong> is available by checking or 
		unchecking income categories after hovering over the layers button in 
		the right hand corner, under the color bar</p>
	</body>
	</html>
	'''
#folium_map.get_root().html.add_child(folium.Element(title_html))
folium_map.save('./docs/poweroutages_income_raw.html')
