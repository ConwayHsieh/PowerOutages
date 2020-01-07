import csv
import numpy as np
import pandas as pd
from uszipcode import SearchEngine

'''
col_names = ['id', 'outage', 'outage_label', 'snapshot', 'snapshot_label', 
  'lastUpdateTime', 'currentEtor', 'estCustAffected', 'hazardFlag',
  'latitude', 'longitude', 'regionName', 'regionName_label', 'cause', 
  'cause_label', 'crewCurrentStatus', 'crewCurrentStatus_label']
'''
col_names = ['outage', 'snapshot_label', 'estCustAffected', \
    'latitude', 'longitude', 'cause']
df = pd.read_csv('outage_snapshots_new.csv', engine='python', #names=col_names,
    #delimiter=",", quoting=csv.QUOTE_NONE, encoding='utf-8', 
    error_bad_lines=False)#, nrows=5000)
#df = df[['outage', 'snapshot', 'snapshot_label', 'estCustAffected', \
#    'latitude', 'longitude', 'cause']]
df['snapshot_label'] = pd.to_datetime(df['snapshot_label'])
df_outage = df.groupby('outage', as_index=False).agg({'snapshot_label': [np.max, np.min],
                                      'estCustAffected': np.max,
                                      'latitude': np.mean,
                                      'longitude': np.mean,
                                      'cause': pd.Series.mode  })
#print(df_outage.head(10))
df_outage['duration_hours'] = (df_outage[('snapshot_label', 'amax')] - \
    df_outage[('snapshot_label', 'amin')]) / np.timedelta64(1,'h')

df_outage = df_outage.drop([('snapshot_label', 'amax'), ('snapshot_label', 'amin')], \
    axis=1)
df_outage.columns = [pair[0] for pair in df_outage.columns]
#print(df_outage.head(10))

# uszipcode
search = SearchEngine(simple_zipcode=False)
df_zip = df_outage.copy()
def find_zip(row):
    results = search.by_coordinates(row.latitude, row.longitude, returns=1)[0]
    return [results.zipcode, results.population, results.population_density, \
        results.median_household_income]
df_zip[['zip', 'pop', 'pop_dens', 'med_house_inc']] = df_zip.apply(\
    lambda row: pd.Series(find_zip(row)), axis=1)
print(df_zip.head(10))

df_zip.to_csv('outages_grouped.csv', index=False)
