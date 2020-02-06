import numpy as np
import pandas as pd
from sklearn import cluster

def cluster_dbscan(x, n=3):
	dbs = cluster.DBSCAN(eps=3, min_samples=2)
	return dbs.fit_predict(x)

if __name__ == "__main__":
	outages = pd.read_csv('outages_zip.csv')
	x = outages[['pop_dens', 'med_house_inc', 'duration_hours']]
	labels = cluster_dbscan(x.values, 2)
	print(labels)