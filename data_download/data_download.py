
import pandas as pd
import requests

def data_ingestion():
    ''''
    Component to download data from a github repo.
    '''
    df_allseasons = pd.read_csv('https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/cleaned_merged_seasons.csv', index_col = 'Unnamed: 0')

    # Get yearly historic data from endpoint for available seasons and identify the keys in each disctionary using 2016 as an example.

    Y2016= requests.get('https://www.fantasynutmeg.com/api/history/season/2016-17').json()
    Y2017= requests.get('https://www.fantasynutmeg.com/api/history/season/2017-18').json()
    Y2018= requests.get('https://www.fantasynutmeg.com/api/history/season/2018-19').json()
    Y2019= requests.get('https://www.fantasynutmeg.com/api/history/season/2019-20').json()  
    Y2020= requests.get('https://www.fantasynutmeg.com/api/history/season/2020-21').json()
    Y2021= requests.get('https://www.fantasynutmeg.com/api/history/season/2021-22').json()
    Y2022= requests.get('https://www.fantasynutmeg.com/api/history/season/2022-23').json()

    # Convert history data dictionary to a pandas dataframe.

    hist16_df = pd.DataFrame(Y2016['history'])
    hist17_df = pd.DataFrame(Y2017['history'])
    hist18_df = pd.DataFrame(Y2018['history'])
    hist19_df = pd.DataFrame(Y2019['history'])
    hist20_df = pd.DataFrame(Y2020['history'])
    hist21_df = pd.DataFrame(Y2021['history'])

    # Engineer feature to highlight each season year.

    hist16_df['year'] = hist16_df.apply(lambda x: "2016-17", axis=1)
    hist17_df['year'] = hist17_df.apply(lambda x: "2017-18", axis=1)
    hist18_df['year'] = hist18_df.apply(lambda x: "2018-19", axis=1)
    hist19_df['year'] = hist19_df.apply(lambda x: "2019-20", axis=1)
    hist20_df['year'] = hist20_df.apply(lambda x: "2020-21", axis=1)
    hist21_df['year'] = hist21_df.apply(lambda x: "2021-22", axis=1)

    # Concatenate all history data across years.

    hist_df = [hist16_df, hist17_df, hist18_df, hist19_df, hist20_df, hist21_df]
    hist = pd.concat(hist_df, axis = 0, ignore_index=True)


    #get current season data from FPL API endpoints and identify the keys
    fpl_base_url = 'https://fantasy.premierleague.com/api/'
    current_season = requests.get(fpl_base_url+'bootstrap-static/').json()

    #create dataframes for the current season dictionary keys for data exploration
    #- Contains summary of Gameweek data
    events_df = pd.DataFrame(current_season['events']) #
    phases_df = pd.DataFrame(current_season['phases']) #Shows calendar months for game weeks
    teams_df = pd.DataFrame(current_season['teams'])
    players_df = pd.DataFrame(current_season['elements'])
    element_stats_df = pd.DataFrame(current_season['element_stats'])
    element_types_df = pd.DataFrame(current_season['element_types'])

    for x in players_df.index :
        player_id = players_df.id[x]
        url = f'https://fantasy.premierleague.com/api/element-summary/{player_id}/'
        r = requests.get(url)
        json = r.json()
        json_history_df = pd.DataFrame(json['history'])

       
        if x == 0 :
            df_currentseason = json_history_df
        else : 
            df_currentseason = df_currentseason.append(json_history_df)


    #get current season fixtures from FPL API endpoint and create Dataframe
    current_season_fixtures = requests.get(fpl_base_url+'fixtures/').json()
    fixtures_df = pd.DataFrame(current_season_fixtures)

    #Map the team names and the player positions into the players_df_clean dataframe
    teams_now=dict(zip(teams_df.id, teams_df.short_name))
    positions=dict(zip(element_types_df.id, element_types_df.singular_name_short))
    players_df['club_name'] = players_df['team'].map(teams_now)
    players_df['position'] = players_df['element_type'].map(positions)



    
    df_allseasons.to_csv('all_seasons_hist.csv')
    hist.to_csv('hist_data.csv')
    players_df.to_csv('players_df.csv')
    df_currentseason.to_csv('currentseason.csv')
    fixtures_df.to_csv('fixtures.csv')

if __name__ == "__main__":
    data_ingestion()
    