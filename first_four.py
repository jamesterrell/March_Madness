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
    """
    Simulates the first four games of a tournament and inserts the winners into the provided bracket.

    Args:
        ff_bracket (pd.DataFrame): A DataFrame containing players for the first four games.
        insert_bracket (pd.DataFrame): A DataFrame representing the tournament bracket.
        insert1 (float): The index in the insert_bracket where the winner of the first game should be inserted.
        insert2 (float): The index in the insert_bracket where the winner of the second game should be inserted.
        insert3 (float): The index in the insert_bracket where the winner of the third game should be inserted.
        insert4 (float): The index in the insert_bracket where the winner of the fourth game should be inserted.

    Returns:
        pd.DataFrame: The updated tournament bracket with the winners of the first four games inserted.
    """
    r64 = tourney_round(ff_bracket)
    # Insert the winners of the first four games into the bracket
    insert_bracket.loc[insert1] = r64.loc[0]
    insert_bracket.loc[insert2] = r64.loc[1]
    insert_bracket.loc[insert3] = r64.loc[2]
    insert_bracket.loc[insert4] = r64.loc[3]

    # Sort the bracket by index and reset the index
    insert_bracket.sort_index(inplace=True)
    insert_bracket.reset_index(drop=True, inplace=True)
    return insert_bracket
