import polars as pl
import numpy as np

def play_round(bracket_df: pl.DataFrame):
    bracket_df = bracket_df.with_columns(
        [
            # Create groups (0,0,1,1,2,2,...) to identify pairs
            (pl.arange(0, pl.len()) // 2).alias("pair")
        ]
    )
    bracket_df = bracket_df.with_columns(
        [
            (pl.col("Elo") - pl.col("Elo").shift(1))
            .fill_null((pl.col("Elo") - pl.col("Elo").shift(-1)))
            .over("pair")
            .alias("Elo_diff")
        ]
    )

    bracket_df = bracket_df.with_columns(
        [(1 - (1 / (1 + 10 ** (pl.col("Elo_diff") / 400)))).alias("winning_chances")]
    )

    bracket_df = bracket_df.with_columns(
        [
            pl.col("pair")
            .unique()
            .map_elements(lambda _: np.random.random(), return_dtype=pl.Float64)
            .gather(pl.col("pair"))
            .alias("random_value")
        ]
    )

    bracket_df = bracket_df.with_columns(
        [
            (pl.col("Elo") - pl.col("Elo").shift(1))
            .fill_null((pl.col("Elo") - pl.col("Elo").shift(-1)))
            .over("pair")
            .alias("Elo_diff")
        ]
    )

    bracket_df = bracket_df.with_columns(
        [pl.arange(0, pl.len()).over("pair").alias("position_in_pair")]
    )

    bracket_df = bracket_df.with_columns(
        [
            # when the favorite wins
            pl.when(
                pl.col("Elo_diff") > 0,
                pl.col("position_in_pair") == 0,
                pl.col("winning_chances") > pl.col("random_value"),
            )
            .then(1)
            .when(
                pl.col("Elo_diff") > 0,
                pl.col("position_in_pair") == 1,
                pl.col("winning_chances") > pl.col("random_value"),
            )
            .then(1)
            # when the favorite loses
            .when(
                pl.col("Elo_diff") > 0,
                pl.col("position_in_pair") == 0,
                pl.col("winning_chances") < pl.col("random_value"),
            )
            .then(0)
            .when(
                pl.col("Elo_diff") > 0,
                pl.col("position_in_pair") == 1,
                pl.col("winning_chances") < pl.col("random_value"),
            )
            .then(0)
            .otherwise(None)
            .alias("favorite result"),
            # when the underdog wins
            pl.when(
                pl.col("Elo_diff") < 0,
                pl.col("position_in_pair") == 1,
                pl.col("winning_chances").shift(1) < pl.col("random_value"),
            )
            .then(1)
            .when(
                pl.col("Elo_diff") < 0,
                pl.col("position_in_pair") == 0,
                pl.col("winning_chances").shift(-1) < pl.col("random_value"),
            )
            .then(1)
            # when the underdog loses
            .when(
                pl.col("Elo_diff") < 0,
                pl.col("position_in_pair") == 1,
                pl.col("winning_chances").shift(1) > pl.col("random_value"),
            )
            .then(0)
            .when(
                pl.col("Elo_diff") < 0,
                pl.col("position_in_pair") == 0,
                pl.col("winning_chances").shift(-1) > pl.col("random_value"),
            )
            .then(0)
            .otherwise(None)
            .alias("underdog result"),
        ]
    )
    # just keep the winners 
    bracket_df = bracket_df.filter(
        ((pl.col("favorite result") == 1) & pl.col("underdog result").is_null())
        | (pl.col("favorite result").is_null() & (pl.col("underdog result") == 1))
    )

    bracket_df = bracket_df.drop(
        [
            "pair",
            "Elo_diff",
            "winning_chances",
            "random_value",
            "position_in_pair",
            "favorite result",
            "underdog result",
        ]
    )
    return bracket_df
