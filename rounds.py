import pandas as pd
import random


def tourney_round(df: pd.DataFrame) -> pd.DataFrame:
    """
    Simulates a tournament round with the given DataFrame of players and their Elo ratings.

    Args:
        df (pd.DataFrame): A DataFrame containing players and their Elo ratings.
                           It should have a column named "Elo".

    Returns:
        pd.DataFrame: A DataFrame containing the winners of the tournament round.
    """
    winners = []  # List to store the winners of each match
    for i in range(0, len(df), 2):
        # Calculate the Elo difference between the two teams
        elo_diff = df["Elo"].iloc[i] - df["Elo"].iloc[i + 1]
        # Calculate the probability of the higher-rated player winning
        win_prob = 1 / (1 + 10 ** (elo_diff / 400))
        # Generate a random number between 0 and 1
        rand = random.uniform(0, 1)
        # Determine the winner based on the Elo difference and the random number
        if elo_diff > 0:
            # The first team has a higher Elo rating
            if rand > win_prob:
                winners.append(df.loc[[i], :])  # The first team wins
            else:
                winners.append(df.loc[[i + 1], :])  # The second team wins
        else:
            # The second player has a higher Elo rating
            if rand < win_prob:
                winners.append(df.loc[[i], :])  # The first team wins
            else:
                winners.append(df.loc[[i + 1], :])  # The second team wins

    # Concatenate the winners and reset the index
    return pd.concat(winners).reset_index(drop=True)
