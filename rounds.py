import pandas as pd
import random

def tourney_round(df: pd.DataFrame) -> pd.DataFrame:
    winners = []
    for i in range(0, len(df), 2):
        elo_diff = df["Elo"].iloc[i] - df["Elo"].iloc[i + 1]
        win_prob = 1 / (1 + 10 ** (elo_diff / 400))
        rand = random.uniform(0, 1)

        if elo_diff > 0:
            if rand > win_prob:
                winners.append(df.loc[[i], :])
            else:
                winners.append(df.loc[[i + 1], :])
        else:
            if rand < win_prob:
                winners.append(df.loc[[i], :])
            else:
                winners.append(df.loc[[i + 1], :])
    return pd.concat(winners).reset_index(drop=True)