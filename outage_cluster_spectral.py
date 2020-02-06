import numpy as np
import pandas as pd
from sklearn import cluster

def cluster_spectral(x, n=3):
	sp = cluster.SpectralClustering(n_clusters=n,
                                        assign_labels="kmeans").fit(x)	
	return sp.labels_#sp.predict(x)

if __name__ == "__main__":
	outages = pd.read_csv('outages_zip.csv')
	x = outages[['pop_dens', 'med_house_inc', 'duration_hours']]
	labels = cluster_spectral(x.values, 2)
	print(labels)