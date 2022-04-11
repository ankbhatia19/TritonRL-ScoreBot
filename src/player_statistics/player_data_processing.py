import pandas as pd
import numpy as np 
import json 
import os
import pandas as pd
# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
from sklearn.preprocessing import MinMaxScaler

def get_totals(df):
    # Select only the columns that contain the total counts for each statistic over the course of the season.
    total = df[[
    'team name', 'player name', 'games', 'wins', 'score', 'goals', 'assists', 'saves', 'shots', 'shots conceded', 'goals conceded',
    'goals conceded while last defender', 'amount collected', 'amount collected big pads', 'amount collected small pads',  
    'count collected big pads', 'count collected small pads','amount stolen', 'amount stolen big pads', 'amount stolen small pads',
    'count stolen big pads', 'count stolen small pads', '0 boost time', '100 boost time', 'amount used while supersonic',
    'amount overfill total','amount overfill stolen', 'total distance', 'time slow speed', 'time boost speed', 'time supersonic speed',
    'time on ground', 'time low in air', 'time high in air', 'time powerslide','count powerslide','time most back', 'time most forward',
    'time in front of ball','time behind ball', 'time defensive half', 'time offensive half', 'time defensive third', 'time neutral third',
    'time offensive third','demos inflicted', 'demos taken'
    ]]
    # Lowercase all playernames for consistency.
    total['player name'] = total["player name"].str.lower() 
    # Since we only have a dataframe of total statistics, we can group by player to account for BallChasing.com accidently
    # mismanaging 
    # team and player relationships. This is acting as a merge between rows where playernames match but the teams names didnt. 
    cleaned_data = total.groupby(['player name']).sum().reset_index()
    return cleaned_data

def average_player_statistics(cleaned_data):
    # In order to round the data to the nearest thousandth, we need to remove all columns without int datatypes. I divide the total
    # statistics for every player by the total number of (recorded) games that they have played and uploaded replays. 
    per_game_stats = cleaned_data.iloc[:,2:].div(cleaned_data.games, axis=0).round(4)
    # This is theseries that contains all columns without int datatypes, in other words all of the players. 
    players = cleaned_data.iloc[:,:2]
    # Then we merge these back together for the final dataframe.
    final_df = pd.concat([players, per_game_stats], axis=1)
    # return df so we can 
    return final_df

def remove_player_statistics(df, lst):
    # Provide as input a list of player names to be drop from this dataframe. 
    return df[~df['player name'].isin(lst)]

def patch_duplicates(df, dictionary):
    all_players = [list(dictionary.keys()), list(dictionary.values())]
    flattened = [item for sublist in all_players for item in sublist]
    # data = df.set_index('player name', drop = True, verify_integrity = True)
    data = df.set_index('player name', drop = True)
    # Remove players 
    patched_data = data.loc[flattened]
    patched_data = patched_data.rename(index=dictionary)
    patched_data = patched_data.reset_index(drop = False)\
        .groupby(['player name']).sum()\
            .reset_index(drop=False)
    # Removed players that we combined so we can recombine them
    removed_duplicates = remove_player_statistics(df, flattened).reset_index(drop = True)
    # Combine the two
    patched_dataframe = pd.concat([removed_duplicates, patched_data])
    return patched_dataframe.reset_index(drop=True)

def offensive_stats(df):
    # Select all columns with relevant data 
    Offensive = df[[
        'player name', 'score', 'shots', 'assists',
        'time most forward','time offensive half',
        'time neutral third','time offensive third'
        ]]
    # Create a new column with the calculated offensive rating value based on original column data calculations
    Offensive['Offensive Rating'] = .05*Offensive['score'] + .2*Offensive['shots'] \
                                + .05*Offensive['assists'] + .05*Offensive['time most forward'] + .05*Offensive['time neutral third'] \
                                + .1*Offensive['time offensive third'] 
    # The we use the MinMaxScaler from SKLearn to normalize all of the values and to generate ranks. 
    scaler = MinMaxScaler()
    Offensive['Offensive Rating']  = scaler.fit_transform(Offensive[['Offensive Rating']])
    # Return the DataFrame containing [player name, offensive rating] 
    # Columns in sorted order with respect to Offensive rating  
    return Offensive.sort_values('Offensive Rating',ascending=False)[['player name', 'Offensive Rating']]

def defensive_stats(df):
    # Select all columns with relevant data 
    Defensive = df[[
        'player name', 'score', 'saves','goals conceded','goals conceded while last defender',
        'time most back','time defensive half','time neutral third','time defensive third'
        ]]
    # Create a new column with the calculated defensive rating value based on original column data calculations
    Defensive['Defensive Rating'] = .05* Defensive['score']  + .2*Defensive['saves'] + .05*Defensive['goals conceded'] +\
                                    .1*Defensive['goals conceded while last defender']+ .1*Defensive['time most back'] +\
                                    .15*Defensive['time defensive half'] + .1 * Defensive['time neutral third'] +\
                                    .05 * Defensive['time defensive third']
    # The we use the MinMaxScaler from SKLearn to normalize all of the values and to generate ranks. 
    scaler = MinMaxScaler()
    Defensive['Defensive Rating']  = scaler.fit_transform(Defensive[['Defensive Rating']])
    # Return the DataFrame containing [player name, defensive rating] 
    # Columns in sorted order with respect to Offensive rating  
    return Defensive.sort_values('Defensive Rating',ascending=False)[['player name', 'Defensive Rating']]

def aggression_stats(df):
    # Select all columns with relevant data 
    Aggression = df[[
        'player name', 'shots', 'amount stolen', 'amount stolen big pads', 'amount stolen small pads',
        'time offensive half','demos inflicted','demos taken','time powerslide','count powerslide'
        ]]
    # Create a new column with the calculated defensive rating value based on original column data calculations
    Aggression['Aggression Rating'] = .2*Aggression['shots'] +.025*Aggression['amount stolen']+ .05*Aggression['amount stolen big pads']+\
                                        .025*Aggression['amount stolen small pads'] + .075*Aggression['time offensive half'] +\
                                        .2*Aggression['demos inflicted'] + .025*Aggression['demos taken'] +\
                                        .05*Aggression['time powerslide'] + .15*Aggression['count powerslide']
    # The we use the MinMaxScaler from SKLearn to normalize all of the values and to generate ranks.
    scaler = MinMaxScaler()
    Aggression['Aggression Rating']  = scaler.fit_transform(Aggression[['Aggression Rating']])
    # Return the DataFrame containing [player name, aggression rating] 
    # Columns in sorted order with respect to aggression rating  
    return Aggression.sort_values('Aggression Rating',ascending=False)[['player name', 'Aggression Rating']]

def speed_stats(df):
    # Select all columns with relevant data 
    Speed = df[[
        'player name','total distance','amount collected','amount collected big pads','amount collected small pads',
        '0 boost time','100 boost time','amount used while supersonic','time slow speed','time boost speed','time supersonic speed'
        ]]
    # Create a new column with the calculated defensive rating value based on original column data calculations
    Speed['Speed Rating'] = + 4*Speed['total distance']\
                        + (-3*Speed['amount used while supersonic']) + 1*Speed['amount collected']\
                        + 1*Speed['amount collected big pads'] + 2*Speed['amount collected small pads'] + (-3*Speed['0 boost time'])\
                        + 3*Speed['100 boost time'] + -1*Speed['time slow speed'] + 1*Speed['time boost speed']\
                        + 3*Speed['time supersonic speed']
    # The we use the MinMaxScaler from SKLearn to normalize all of the values and to generate ranks.
    scaler = MinMaxScaler()
    # Return the DataFrame containing [player name, speed rating] 
    # Columns in sorted order with respect to speed rating  
    Speed['Speed Rating'] = scaler.fit_transform(Speed[['Speed Rating']])
    return Speed.sort_values('Speed Rating',ascending=False)[['player name', 'Speed Rating']]

def translate(value, leftMin, leftMax, rightMin, rightMax):
        """ Mapping a range of values to another """ 

        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin
        
        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)
        
        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)    

def generate_overall_standings(df, offensive_stats, defensive_stats, aggression_stats, speed_stats):
    # Take name and win rate from cleaned dataframe
    final_df = df[['player name', 'wins']]
    # Add the offensive player ratings to final df by merging on playername.
    final_df = final_df.merge(offensive_stats, how='left')
    # Add the defensive player ratings to final df by merging on playername.
    final_df = final_df.merge(defensive_stats, how='left')
    # Add the aggression player ratings to final df by merging on playername.
    final_df = final_df.merge(aggression_stats, how='left')
    # Add the speed player ratings to final df by merging on playername.
    final_df = final_df.merge(speed_stats, how='left')


    feature_weights = {
        'off': .25, 
        'def': .25, 
        'agro': .25, 
        'spdy': .25
    }
    # Formatting by reordering columns in a readable format. 
    overalls = final_df[['player name','wins','Offensive Rating', 'Defensive Rating', 'Aggression Rating', 'Speed Rating']]

    # Generate overall standings based on all generated stats
    overalls['Total Overall'] = feature_weights['off']*overalls['Offensive Rating'] +\
                                feature_weights['def']*overalls['Defensive Rating'] +\
                                feature_weights['agro']*overalls['Aggression Rating'] +\
                                feature_weights['spdy']*overalls['Speed Rating']
    
    # Scaler for normalization                             
    scaler = MinMaxScaler()
    # Normalize
    overalls['Total Overall'] = scaler.fit_transform(overalls[['Total Overall']])
    # Sort values by total overall score
    total_overalls = overalls.sort_values('Total Overall',ascending=False)

    # Formatting for easier human readability
    total_overalls.reset_index(drop=True).round(3)
    total_overalls['Offensive Rating'] = total_overalls['Offensive Rating'] *100 
    total_overalls['Defensive Rating'] = total_overalls['Defensive Rating'] *100 
    total_overalls['Aggression Rating'] = total_overalls['Aggression Rating'] *100 
    total_overalls['Speed Rating'] = total_overalls['Speed Rating'] *100 
    total_overalls['Total Overall'] = total_overalls['Total Overall'] *100 

    # Display the final dataframe for people to inspect
    results = total_overalls[[
        'player name', 'wins', 'Total Overall',
        'Offensive Rating', 'Defensive Rating', 'Aggression Rating', 'Speed Rating']]\
            .round(2).reset_index(drop=True)\
                .rename(columns={
                    "player name": "participant",
                    'wins': 'win rate',
                    "Total Overall": "Overall",
                    'Offensive Rating': 'Offense',
                    'Defensive Rating': 'Defense',
                    'Aggression Rating':'Aggression',
                    'Speed Rating': 'Speed'})

    return results

def add_relevant_metadata(standings, names_fp, playercard_imgs, rank_fp):
    df = standings.set_index('participant')

    # Merge the player specified names
    player_names_fp = r'.\output\playercard_names.csv'
    player_names_df = pd.read_csv(player_names_fp, index_col=0)
    player_names_df = player_names_df.drop_duplicates(subset=['message_author', 'leaderboard_name'], keep='last')
    cols = {'message_author': 'discord_username', 'leaderboard_name': 'ballchasing_username'}
    names_df = player_names_df.rename(columns = cols)
    names_df.ballchasing_username = names_df.ballchasing_username.str.lower()
    names_df= names_df.set_index('ballchasing_username', drop = True)
    merged_names = df.merge(names_df, left_index = True, right_index = True, how = 'left')
    merged_names = merged_names.reset_index(drop = False) # Reset the index here to preserve original playercard rank data
    old_index = {'index': 'name_index'}
    merged_names = merged_names.rename(columns = old_index)

    # Merge the playercard image paths 
    x = os.listdir("./assets/playercard_imgs")
    start_directory = 'C:\\Users\\Q\'s\\Python Stuff\\Triton-Replay-Bot\\TritonRL-ScoreBot\\assets'
    abs_path = start_directory + '\\playercard_imgs\\'
    file_paths = [abs_path + i for i in x]
    names = [name.strip('.png') for name in x]
    fp_df = {'avatar_username': names, 'img_filepath': file_paths}
    fp_df = pd.DataFrame(data = fp_df)
    merged_names_paths = merged_names.merge(fp_df,  left_on = 'discord_username', right_on='avatar_username', how = 'left')

    # Merge the players associated rank 
    player_ranks_fp = r'.\output\playercard_ranks.csv'
    player_ranks_df = pd.read_csv(player_ranks_fp, index_col=0)
    player_ranks_df = player_ranks_df.drop_duplicates(subset=['message_author'], keep='last')
    merged_names_paths_ranks = merged_names_paths.merge(player_ranks_df, left_on = 'discord_username', right_on='message_author', how = 'left')

    # Clean Final DataFrame
    cleaned_df = merged_names_paths_ranks.sort_values('Overall', ascending = False)
    cleaned_df = cleaned_df.reset_index(drop=True) # Remove old index 
    cleaned_df = cleaned_df.reset_index(drop=False) # make a new index 
    cleaned_df = cleaned_df.set_index('index', drop = True)
    cleaned_df = cleaned_df.fillna('N/A')
    cleaned_df['img_filepath'] = cleaned_df['img_filepath'].str.replace('\\', '/')
    cleaned_df = cleaned_df.fillna('N/A')
    cleaned_df = cleaned_df.drop(columns = ['avatar_username', 'message_author'])

    return cleaned_df

    