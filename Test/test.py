import pandas as pd
import requests

df_allseasons = pd.read_csv('https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/cleaned_merged_seasons.csv', index_col = 'Unnamed: 0')
df_allseasons.to_csv('all_seasons_hist.csv') 