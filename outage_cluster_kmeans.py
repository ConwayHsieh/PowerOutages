import numpy as np
import pandas as pd
from sklearn import cluster

def cluster_kmeans(x, n=3):
	km = cluster.KMeans(n_clusters=n)	
	return km.fit_predict(x)

if __name__ == "__main__":
	outages = pd.read_csv('outages_zip.csv')
	x = outages[['pop_dens', 'med_house_inc', 'duration_hours']]
	labels = cluster_spectral(x.values, 2)
	print(labels)