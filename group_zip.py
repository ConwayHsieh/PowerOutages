import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)

df = pd.read_csv('outages_grouped.csv', engine='c')
#print(df.head(10))
df_zip = df.groupby(['zip', 'pop', 'pop_dens', 'med_house_inc'], \
    as_index=False)

zip_cause_dict = {}
for name, group in df_zip:
    zip_cause_dict[name[0]] = \
        group.cause.value_counts()

df_zip_agg = df_zip.agg({'latitude': np.mean,
    'longitude': np.mean,
    'estCustAffected': np.sum,
    #'cause': pd.Series.nunique,#pd.Series.value_counts,
    'duration_hours': np.mean})
#print(df_zip_agg.head(10))

for i in range(9):
    j = i + 1
    df_zip_agg['cause_' + str(j)] = 0
#print(df_zip_agg.head(10))

for i, row in df_zip_agg.iterrows():
    curr_series = zip_cause_dict[row['zip']]
    #print(curr_series)
    #print(curr_series.index)
    for index in curr_series.index:
        if len(index) > 1:
            continue
        else:
            df_zip_agg.at[i, 'cause_' + index] = curr_series[index]
    #for i in range(len(curr_series)):
    #    print(curr_series[i])
    #print(row)
    #df_zip_agg.at[index] = row
print(df_zip_agg.head(10))
df_zip_agg.to_csv('outages_zip.csv', index=False)
