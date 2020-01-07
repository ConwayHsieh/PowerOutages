import numpy as np
import pandas as pd

df = pd.read_csv('outages_grouped.csv', engine='c')
print(df.head(10))
df_zip = df.groupby(['zip', 'pop', 'pop_dens', 'med_house_inc'], \
    as_index=False).agg({'latitude': np.mean,
        'longitude': np.mean,
        'estCustAffected': np.sum,
        'cause': pd.Series.value_counts,
        'duration_hours': np.mean})
print(df_zip.head(10))

#df_zip.to_csv('outages_zip.csv', index=False)
