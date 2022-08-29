
#import library
import requests
import pandas as pd
import numpy as np
#import pandas.util.testing as tm

# Extract Summary info about specified dataframe in argument.
def data_exploration(dataframe):
    print('\n There are {0} rows and {1} columns'.format(*dataframe.shape))
    
    print('\n{0:#^20}'.format('The columns in the dataset are'))
    
    print(dataframe.columns)

    print('\n{0:#^20}'.format('The columns with null values in the dataset are'))

    print(dataframe.columns[dataframe.isnull().any()].tolist())
    
    print('\n{0:#^20}'.format('The data types and null values count in the dataset are'))
    
    print(dataframe.info())
         
    return

def calc_out_weights(players):
    players['out_weight'] = 100
    players['out_weight'] -= players['diff']/3
    players['out_weight'] -= players['form'].astype("float")*10
    players['out_weight']+= (100 -players['chance_of_playing_this_round'].astype("float"))*0.2
    players.loc[players['element_type'] ==1, 'out_weight'] -=10
    players.loc[players['out_weight'] <0, 'out_weight'] =0
    return players.sample(1, weights=players.out_weight)

def calc_in_players_weights(players):
    players['in_weight'] = 1
    players['in_weight'] += players['diff']/3
    players['in_weight'] += players['form'].astype("float")*10
    players['in_weight'] -= (100 - players['chance_of_playing_this_round'].astype("float"))*0.2
    players.loc[players['in_weight'] <0, 'in_weight'] =0
    return players

def calc_starters_weights(players):
    players['start_weight'] = 1
    players['start_weight'] += players['diff']/2
    players['start_weight'] += players['form'].astype("float")*5
    players['start_weight'] -= (100 - players['chance_of_playing_this_round'].astype("float"))*0.2
    players.loc[players['start_weight'] <0, 'start_weight'] =0
    return players