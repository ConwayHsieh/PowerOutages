import numpy as np
import pandas as pd
from sklearn import preprocessing
import plotly
import plotly.graph_objects as go
from outage_cluster_GMM import cluster_GMM
from outage_cluster_kmeans import cluster_kmeans

outages = pd.read_csv('outages_zip.csv')

features = outages[['pop_dens', 'med_house_inc', 'duration_hours']]
scaler = preprocessing.RobustScaler()
x_scaled = scaler.fit_transform(features.values)

labels = cluster_GMM(x_scaled, 2) + 1
#label_list = labels.tolist()
#label_str = ['Cluster ' + str(i) for i in label_list]

features['labels'] = labels

f1 = features[features['labels'] == 1]
f2 = features[features['labels'] == 2]

# Create figure
fig = go.Figure()

dot_size = 6
op = 0.9

fig.add_trace(
	go.Scatter3d(x=f1['pop_dens'], \
	y=f1['med_house_inc'], \
	z=f1['duration_hours'], 
	mode='markers', 
	name='Cluster 1',
	visible=True,
	marker=dict(
        size=dot_size,
        color='crimson', # set color to an array/list of desired values
        opacity=op),
	hovertemplate = 
	'Population Density: %{x}'+
    '<br>Median Household Income: %{y}<br>'+
    'Average Duration of Power Outage: %{z}')
	)

fig.add_trace(
    go.Scatter3d(x=f2['pop_dens'], \
	y=f2['med_house_inc'], \
	z=f2['duration_hours'], 
	mode='markers', 
	name='Cluster 2',
	visible=True,
	marker=dict(
        size=dot_size,
        color='darkcyan', # set color to an array/list of desired values
        opacity=op),
    	hovertemplate = 
	'Population Density: %{x}'+
    '<br>Median Household Income: %{y}<br>'+
    'Average Duration of Power Outage: %{z}')
	)

fig.update_layout(
    updatemenus=[
        go.layout.Updatemenu(
            active=0,
            buttons=list([
                dict(label="Both",
                     method="update",
                     args=[{"visible": [True, True]}]),
                dict(label="Cluster 1",
                     method="update",
                     args=[{"visible": [True, False]}]),
                dict(label="Cluster 2",
                     method="update",
                     args=[{"visible": [False, True]}])
            ]),
        )
    ])

# Update remaining layout properties
fig.update_layout(
    title_text="Average Duration of Power Outages per Zip Code",
    showlegend=True,
)

fig.update_layout(scene = dict(
    xaxis_title="Population Density (People/Mile<sup>2</sup>)",
    yaxis_title="Median Household Income ($)",
    zaxis_title="Average Duration (Hours)")
)

plotly.offline.plot(fig, filename='./docs/cluster.html')