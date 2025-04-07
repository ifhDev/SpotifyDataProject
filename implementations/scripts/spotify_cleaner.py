import pandas as pd

def clean_data(df):
    '''
    Takes pandas DataFrame.
    
    Cleans Spotify data for song analysis by:
    * removing rows where target variables popularity and danceability are missing
    * filtering out tracks that are under 30s or over 20min
    * removes tracks with speechiness over 0.7 (likely audiobooks or other narration)

    Returns cleaned DataFrame
    '''
    print('Initial dataset shape: {}'.format(df.shape))

    df = df.dropna(subset=['popularity', 'danceability'])
    df = df[(df['duration_ms'] >= 30000) & (df['duration_ms'] <= 1200000)]
    df = df[df['speechiness'] <= 0.7]

    print('Data cleaned! Final shape: {}'.format(df.shape))
    return df

def remove_duplicates(df):
    '''
    Removes duplicate tracks (keeping only the first occurrence)
    Duplicates: tracks with the same 'track_id'

    Returns: DataFrame with duplicates removed.
    '''
    print('Initial dataset shape: {}'.format(df.shape))

    df = df.drop_duplicates(subset=['track_id'], keep='first')

    print('Duplicates removed! Final shape: {}'.format(df.shape))
    return df