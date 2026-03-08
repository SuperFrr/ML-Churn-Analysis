import pandas as pd
from datetime import datetime

def main():
    print("Calender generator ready..")
    start_date = "2024-10-01"
    end_date = "2026-09-30"
    dates = pd.date_range(start = start_date , end = end_date, freq="D")
    print(dates[0])
    print(dates[-1])
    print(len(dates)) 
    calendar_df = pd.DataFrame({"date": dates})
    print(calendar_df.head())
    print(calendar_df.tail())

    s1_start = pd.Timestamp("2024-10-1")
    s1_playoff_start = pd.Timestamp("2025-04-16")
    s1_playoff_end = pd.Timestamp("2025-06-15")
    s1_end = pd.Timestamp("2025-09-30")

    s2_start = pd.Timestamp("2025-10-01")
    s2_playoff_start = pd.Timestamp("2026-04-16")
    s2_playoff_end = pd.Timestamp("2026-06-15")
    s2_end = pd.Timestamp("2026-09-30")

    calendar_df["season_number"] = 1
    calendar_df.loc[calendar_df["date"] >= s2_start, "season_number"] = 2

    calendar_df["season_phase"] = "regular"

    calendar_df.loc[
    (calendar_df["date"] >= s1_playoff_start) &
    (calendar_df["date"] <= s1_playoff_end),
    "season_phase"
    ] = "playoff"

    calendar_df.loc[
        (calendar_df["date"] > s1_playoff_end) &
        (calendar_df["date"] <= s1_end),
        "season_phase"
    ] = "offseason"

    calendar_df.loc[
        (calendar_df["date"] > s1_playoff_end) &
         (calendar_df["date"] <= s1_end),
         "season_phase"
    ] = "offseason"

    calendar_df.loc[
    (calendar_df["date"] >= s2_playoff_start) &
    (calendar_df["date"] <= s2_playoff_end),
    "season_phase"
    ] = "playoff"
    
    calendar_df.loc[
        (calendar_df["date"] > s2_playoff_end) &
        (calendar_df["date"] <= s2_end),
        "season_phase"
    ] = "offseason"
    print(calendar_df.groupby(["season_number", "season_phase"]).size())
    print(calendar_df["season_phase"].unique())
    calendar_df["is_season2"] = calendar_df["season_number"] == 2
    print(calendar_df["is_season2"].value_counts())
    calendar_df.to_csv("data/calendar.csv", index=False)
    print("Calendar saved successfuily")

if __name__ == "__main__":
    main() 
    