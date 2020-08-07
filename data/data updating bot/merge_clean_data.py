import time
import pandas as pd
import numpy as np
import sklearn as skl
from sklearn import preprocessing
import matplotlib.pyplot as plt


#time.sleep(5)

pd.set_option('display.max_columns', None)

cols_1=[0,1,2,3,4,23,27,31,36,55,59,63,65,69,71,77,82,84,104,109,113,127,134,142,146,152,154,165,169,174,177,180,
       199,201,203,216,236]
c1_data=pd.read_excel('../2020_CHRD.xlsx', sheet_name='Ranked Measure Data', header=1, usecols=cols_1)
c1_data=c1_data.drop(columns='% Uninsured')


# ### Read in the data
# Select specific columns of interest

cols_2=[0,3,22,41,60,787,81,84,88,90,92,94,113,131,135,139,143,144,147,152,157,175,176,177,178,197,217,238,241,
       245,248,249,250,252,254,256,258,260,262,264,267,269]
c2_data=pd.read_excel('../2020_CHRD.xlsx', sheet_name='Additional Measure Data', header=1, usecols=cols_2)
c2_data=c2_data.rename(columns={'% Uninsured.1':'% Children Uninsured', 'Segregation index':
                                'Black/White Segregation Index', 'Segregation Index':
                                'non-White/White Segregation Index','Average Grade Performance':
                               'Average Reading Performance','Average Grade Performance.1':'Average Math Performance',
                               })
c_data=pd.merge(c1_data, c2_data, on='FIPS')


internet_data=pd.read_excel('../internet_data.xlsx', sheet_name='County Connections Dec 2017', usecols=[0,3,4,5,6,7])
# some counties with low numbers have -9999 to 'preserve confidentiality' so we need to interpolate
# note: some counties have a ratio above one, presumably because some houses have multiple connections
internet_data=internet_data.replace(-9999,np.nan)
i_mean=internet_data['ratio'].mean()
internet_data=internet_data.fillna(0.698)

se_data=pd.merge(c_data, internet_data, left_on='FIPS', right_on='countycode')

covid_data=pd.read_csv('../us-counties.csv')

covid_data.date.unique()

last_day=covid_data['date'].iloc[-1]
covid_data=covid_data.loc[covid_data.date==last_day]
#covid_data=covid_data.last('1D')
covid_data['fips']=covid_data['fips'].fillna(0).astype(int)

covid_data['fips']=covid_data['fips'].astype(int)
#covid_data.head()

# look for NYC
#covid_ny=covid_data.loc[covid_data['state']=='New York']
#print (covid_ny)
# great, they put it all under new york city...

# so we need to pull NYC data from a different source
nyc_data=pd.read_csv('../by-boro.csv')

fips=[36005,36047,36061,36081,36085,0]
state=['New York', 'New York',' New York', 'New York', 'New York', 'New York']
nyc_data['fips']=fips
nyc_data['state']=state

nyc_data=nyc_data.rename(columns={'CASE_COUNT':'cases','DEATH_COUNT':'deaths'})
covid_data=covid_data.merge(nyc_data, how='outer')

covid_ny=covid_data.loc[covid_data['state']=='New York']
covid_ny=covid_ny.drop(['BOROUGH_GROUP','CASE_RATE','HOSPITALIZED_RATE','DEATH_RATE','HOSPITALIZED_COUNT'],axis=1)
#print(covid_ny)

covid_data=covid_data.drop(['BOROUGH_GROUP','CASE_RATE','HOSPITALIZED_RATE','DEATH_RATE','HOSPITALIZED_COUNT'],axis=1)


data=pd.merge(se_data, covid_data, left_on='FIPS', right_on='fips')
#data.drop(columns=['countycode'])
#data.head()

data_clean=data.rename(columns={'consumer':'internet_consumer','non_consumer':'internet_nonconsumer','all':'internet_all',
                    'hhs':'internet_hhs','ratio':'internet_ratio','cases':'covid_cases','deaths':'covid_deaths'})
data_clean=data_clean.drop(columns=['date','county','state','fips'])
#data_clean.head()


#change NaNs to 0
data_clean=data_clean.fillna(0)

data_clean['internet_percent']=100*data_clean.internet_ratio
data_clean['FIPS']=data_clean['FIPS'].astype(str)


#add the 0s back in to the fips code for first 9 states alphabetically
data_clean.loc[(data_clean.State=='Arizona'),'FIPS']='0'+data_clean.loc[(data_clean.State=='Arizona'),'FIPS']
data_clean.loc[(data_clean.State=='Alabama'),'FIPS']='0'+data_clean.loc[(data_clean.State=='Alabama'),'FIPS']
data_clean.loc[(data_clean.State=='Alaska'),'FIPS']='0'+data_clean.loc[(data_clean.State=='Alaska'),'FIPS']
data_clean.loc[(data_clean.State=='Arkansas'),'FIPS']='0'+data_clean.loc[(data_clean.State=='Arkansas'),'FIPS']
data_clean.loc[(data_clean.State=='California'),'FIPS']='0'+data_clean.loc[(data_clean.State=='California'),'FIPS']
data_clean.loc[(data_clean.State=='Colorado'),'FIPS']='0'+data_clean.loc[(data_clean.State=='Colorado'),'FIPS']
data_clean.loc[(data_clean.State=='Connecticut'),'FIPS']='0'+data_clean.loc[(data_clean.State=='Connecticut'),'FIPS']
print(data_clean.loc[data_clean.State=='New York'])

#data_clean.head()
list(data_clean.columns)
list(data_clean.columns)

#save full data set
data_clean.to_csv('../merged_data.csv')
