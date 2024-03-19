import numpy as np
import pandas as pd
import random
import rounds as rd
import first_four as ff 

# Read the bracket data from a CSV file
bracket_df = pd.read_csv('bracket.csv', index_col=False)

# Define the teams and Elo ratings for the first four games
first_four = {'Teams': ['Grambling State', 'Montana State', 'Virginia',
                         'Colorado State', 'Boise State', 'Colorado', 'Howard', 'Wagner'], 
            'Elo': [1353.96, 1341.79, 1582.20, 1554.52, 1594.00, 1629.95, 1306.70, 1212.28]}
first_four_df = pd.DataFrame(first_four)

# Simulate the first four games and insert the winners into the bracket
r64 =  ff.first_four_games(first_four_df, bracket_df, 46.5, 57.5, 43.5, 16.5)

# Run the tournament simulation 50,000 time
for i in range(50_000):
    res_store = pd.DataFrame() # Store the results of each simulation

    # Simulate the tournament rounds
    r32 = rd.tourney_round(df=r64)
    res_store['r32'] = r32['Teams']
    r16 = rd.tourney_round(r32)
    res_store['sweet16'] = r16['Teams']
    r8 = rd.tourney_round(r16)
    res_store['elite8'] = r8['Teams']
    r4 = rd.tourney_round(r8)
    res_store['final4'] = r4['Teams']
    r2 = rd.tourney_round(r4)
    res_store['championship'] = r2['Teams']
    champ = rd.tourney_round(r2)
    res_store['national champion'] = champ['Teams']

    # Save the results of each simulation to a CSV file
    res_store.to_csv(f'bracket_attempts/bracket_{i}.csv')