import numpy as np
import pandas as pd
from sklearn import mixture

def cluster_GMM(x, n=3):
	gmm = mixture.GaussianMixture(n_components=n,
                                        covariance_type='full').fit(x)	
	return gmm.predict(x)

if __name__ == "__main__":
	outages = pd.read_csv('outages_zip.csv')
	x = outages[['pop_dens', 'med_house_inc', 'duration_hours']]
	labels = cluster_GMM(x.values, 2)
	print(labels)