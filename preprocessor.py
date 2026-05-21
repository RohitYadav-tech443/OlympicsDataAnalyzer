import pandas as pd


def preprocess(df, region_df):

    # Keep only Summer Olympics
    df = df[df['Season'] == "Summer"]

    # Keep only required columns
    df = df[['Name', 'Sex', 'Age', 'Team', 'NOC', 'Games',
             'Year', 'Season', 'City', 'Sport', 'Event', 'Medal']]

    # Optional but highly effective:
    # Keep Olympics from year 2000 onwards
    df = df[df['Year'] >= 2000]

    # Merge with region dataframe
    df = df.merge(region_df, how='left', on='NOC')

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # One hot encoding for medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    return df