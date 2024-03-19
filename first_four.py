import pandas as pd
import random
from rounds import tourney_round


def first_four_games(
    ff_bracket: pd.DataFrame,
    insert_bracket: pd.DataFrame,
    insert1: float,
    insert2: float,
    insert3: float,
    insert4: float,
) -> pd.DataFrame:
    r64 = tourney_round(ff_bracket)
    insert_bracket.loc[insert1] = r64.loc[0]
    insert_bracket.loc[insert2] = r64.loc[1]
    insert_bracket.loc[insert3] = r64.loc[2]
    insert_bracket.loc[insert4] = r64.loc[3]
    insert_bracket.sort_index(inplace=True)
    insert_bracket.reset_index(drop=True, inplace=True)
    return insert_bracket
