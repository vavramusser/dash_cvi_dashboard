import pandas as pd
pd.set_option('display.max_columns', None)


counties_name = "us-counties.csv"
nyc_name = "by-boro.csv"

counties_df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
counties_df.to_csv("../" + counties_name)

nyc_df = pd.read_csv('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/by-boro.csv')
nyc_df.to_csv("../" + nyc_name)