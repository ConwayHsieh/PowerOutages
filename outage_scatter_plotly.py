import numpy as np
import pandas as pd
import plotly.tools as tls
import plotly.express as px
from sklearn import preprocessing
from outage_cluster_GMM import cluster_GMM
from outage_cluster_kmeans import cluster_kmeans
import plotly

outages = pd.read_csv('outages_zip.csv')

features = outages[['pop_dens', 'med_house_inc', 'duration_hours']]
scaler = preprocessing.RobustScaler()
x_scaled = scaler.fit_transform(features.values)

labels = cluster_GMM(x_scaled, 2) + 1
label_list = labels.tolist()
label_str = ['Cluster ' + str(i) for i in label_list]

features['label'] = label_str

fig = px.scatter_3d(features, x='pop_dens', y='med_house_inc', \
	z='duration_hours', color='label', opacity=0.9, \
	color_continuous_scale='bluered')

#fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
fig.update_layout(title='Gaussian Mixture Clustering')
#fig.show(renderer="browser")

plotly.offline.plot(fig, filename='./docs/cluster.html')

