import polars as pl
from tourney_round import play_round

# Read the bracket data from a CSV file
r64 = pl.read_csv("bracket.csv")

# Store all simulations
simulations = []

# Run the tournament simulation 50,000 times
for i in range(100_000):  # Adjust the loop count as needed
    r32 = play_round(r64)
    r16 = play_round(r32)
    r8 = play_round(r16)
    r4 = play_round(r8)
    r2 = play_round(r4)
    champ = play_round(r2)

    res_store = pl.concat(
        [
            r64[["Teams"]].rename({"Teams": "r64"}),
            r32[["Teams"]].rename({"Teams": "r32"}),
            r16[["Teams"]].rename({"Teams": "sweet16"}),
            r8[["Teams"]].rename({"Teams": "elite8"}),
            r4[["Teams"]].rename({"Teams": "final5"}),
            r2[["Teams"]].rename({"Teams": "championship"}),
            champ[["Teams"]].rename({"Teams": "national champion"}),
        ],
        how="horizontal",
    )
    # Save to CSV
    res_store.write_csv(f"brackets/tournament_results{i}.csv")
