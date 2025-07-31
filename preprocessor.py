import pandas as pd

def preprocessor(df,region_df):

    # filtering summer olympics data
    df = df[df['Season'] == 'Summer']
    # merge with region_df
    df = df.merge(region_df, on='NOC', how='left')
    # dropping duplicates
    df.drop_duplicates(inplace=True)
    # one hot encoding medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)


    bool_cols = ['Gold', 'Silver', 'Bronze']
    df[bool_cols] = df[bool_cols].astype(int)

    return df