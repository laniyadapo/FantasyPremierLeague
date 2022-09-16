
import pandas as pd
import numpy as np
import argparse

def feat_eng(args):
    df_allseasons = pd.read_csv(args.allseasons)
    hist = pd.read_csv(args.hist)
    players_df = pd.read_csv(args.players_df)
    df_currentseason = pd.read_csv(args.currentseason)
    fixtures_df = pd.read_csv(args.fixtures_df)

    # FOR THE TRAIN AND VALIDATION SET
    # Engineer feature to highlight the form of the players.
    hist['form'] = hist['total_points']/38 

    # Engineer feature to highlight the players name and the season they played in.
    hist['name_season'] = hist['first_name'] + ' ' + hist['second_name'] + '_' + hist['year']

    # Engineer feature to highlight the players name and the season they played in.
    df_allseasons['name_season'] = df_allseasons['name'] + '_' + df_allseasons['season_x']

    # Engineer a feature to highlight the club of the player.
    teams=dict(zip(hist.name_season, hist.team_name))

    df_allseasons['club_name'] = df_allseasons['name_season'].map(teams)

    # Engineer a feature to highlight the form of the player.
    teams=dict(zip(hist.name_season, hist.form))

    df_allseasons['form'] = df_allseasons['name_season'].map(teams)

    # Engineer feature to highlight the game dates from kickoff_time.
    df_allseasons['game_date'] = df_allseasons['kickoff_time'].str.replace('T', ' ')
    df_allseasons['game_date'] = df_allseasons['game_date'].str.replace(':00Z', '')

    # Convert game_date feature to appropriate dtype.
    df_allseasons['game_date'] = pd.to_datetime(df_allseasons['game_date'])

    # Engineer game season weather feature.
    seasons = [1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 1]
    month_to_season = dict(zip(range(1,13), seasons))
    df_allseasons['game_weather'] = df_allseasons.game_date.dt.month.map(month_to_season)

    # Engineer feature to highlights games that started before 13:00 (early starts) and those that started after 13:00 (late starts)
    df_allseasons['start_label'] = np.where((df_allseasons['game_date'].dt.hour) < 13, 0, 1)
    # Engineer feature to highlight the game year only.
    df_allseasons['year'] = df_allseasons.game_date.dt.year

    # Drop feature.
    df_allseasons.drop('team_x', axis = 1, inplace=True)
    # Drop all missing observations.
    df_allseasons.dropna(inplace=True)

    # Change dypes.
    df_allseasons['team_h_score'] = df_allseasons['team_h_score'].astype(int)
    df_allseasons['team_a_score'] = df_allseasons['team_a_score'].astype(int)

    # Drop features.
    df_allseasons.drop(['opponent_team', 'kickoff_time'], axis = 1, inplace=True)

    # Drop features.
    df_allseasons.drop(['season_x', 'name', 'name_season', 'fixture', 'game_date', 'round', 'element'], axis=1, inplace=True)
    # Drop all players with zero playtime.
    zero_minutes = df_allseasons[df_allseasons.minutes == 0].index
    df_allseasons.drop(zero_minutes, axis = 0, inplace=True)
    df_allseasons.set_index('year', inplace=True)

    # FEATURING ENGINEERING FOR THE TEST SET
    #create the player name feature
    players_df['name'] = players_df['first_name'] + ' ' + players_df['second_name']
    #Create season_x feature to align with the train data
    df_currentseason['season_x'] = df_currentseason.apply(lambda x: "2022-23", axis=1)
    #Map the team names, player names and form into the all current season data player dataframe
    teams_map=dict(zip(players_df.id, players_df.name))
    club_map=dict(zip(players_df.id, players_df.club_name))
    opp_teams_map=dict(zip(players_df.team, players_df.club_name))
    form_map=dict(zip(players_df.id, players_df.form))
    position_map=dict(zip(players_df.id, players_df.position))
    df_currentseason['name'] = df_currentseason['element'].map(teams_map)
    df_currentseason['club_name'] = df_currentseason['element'].map(club_map)
    df_currentseason['opp_team_name'] = df_currentseason['opponent_team'].map(opp_teams_map)
    df_currentseason['form'] = df_currentseason['element'].map(form_map)
    df_currentseason['position'] = df_currentseason['element'].map(form_map)

    df_currentseason.drop(['Unnamed: 0'], axis=1, inplace=True)
    play_zero_minutes = df_currentseason[df_currentseason.minutes == 0].index
    df_currentseason.drop(play_zero_minutes, axis = 0, inplace=True)
    df_currentseason.rename(columns= { 'round': 'GW' }, inplace=True)
    df_currentseason['game_date'] = df_currentseason['kickoff_time'].str.replace('T', ' ')
    df_currentseason['game_date'] = df_currentseason['game_date'].str.replace(':00Z', '')
    df_currentseason['game_date'] = pd.to_datetime(df_currentseason['game_date'])
    df_currentseason['game_weather'] = df_currentseason.game_date.dt.month.map(month_to_season) 
    df_currentseason['start_label'] = np.where((df_currentseason['game_date'].dt.hour) < 13, 0, 1)
    # Engineer feature tp highlight the game year only.
    df_currentseason['year'] = df_currentseason.game_date.dt.year
    df_currentseason.drop(['game_date', 'season_x'], axis=1, inplace=True)
    df_currentseason.drop(['opponent_team', 'fixture', 'kickoff_time'], axis=1, inplace=True)
    df_currentseason.form = df_currentseason.form.astype(float)
    df_currentseason.set_index('year', inplace=True)
    df_currentseason.drop(['element', 'name'], axis = 1, inplace=True)



    df_allseasons.to_csv('all_seasons_clean_hist.csv')
    df_currentseason.to_csv('df_test.csv')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--allseasons')
    parser.add_argument('--hist')
    parser.add_argument('--currentseason')
    parser.add_argument('--players_df')
    parser.add_argument('--fixtures_df')
    args = parser.parse_args()
    feat_eng(args)
