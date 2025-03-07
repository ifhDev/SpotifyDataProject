from collections import OrderedDict
import numpy as np

def create_binary_classification(df, new_col_name, base_col, percentile_cutoff):
    '''
    Converts a numerical column into a binary classification based on a percentile cutoff.

    Parameters:
    df (pd.DataFrame): The dataset
    new_col_name (str): Name of the new binary column
    base_col (str): The column to base classification on
    percentile_cutoff (float): The percentile threshold (e.g., 67 for top 33%)

    Returns:
    pd.DataFrame: Updated DataFrame with new binary column
    '''
    df[new_col_name] = (df[base_col] >= percentile_cutoff).astype(int)
    return df

GENRE_PRIORITY = OrderedDict({
    'soundtracks': ['disney', 'show-tunes', 'romance', 'anime', 'kids', 'children', 'comedy'],
    'electronic': ['edm', 'electro', 'electronic', 'house', 'deep-house', 'progressive-house', 
                   'minimal-techno', 'techno', 'trance', 'dubstep', 'drum-and-bass', 'chicago-house', 'detroit-techno', 'breakbeat', 'club', 'hardstyle'],
    'hip-hop/rap': ['hip-hop', 'rap', 'r-n-b', 'afrobeat', 'reggaeton', 'dancehall'],
    'pop': ['pop', 'indie-pop', 'synth-pop', 'k-pop', 'j-pop', 'power-pop', 'pop-film', 'j-idol', 'j-dance', 'disco'],
    'rock': ['rock', 'alt-rock', 'psych-rock', 'hard-rock', 'punk-rock', 'punk', 'grunge', 'rock-n-roll', 
             'rockabilly', 'metal', 'metalcore', 'heavy-metal', 'death-metal', 'black-metal', 'emo', 'j-rock', 'garage', 'grindcore', 'hardcore', 'guitar', 'alternative'],
    'jazz/blues': ['jazz', 'blues', 'bluegrass', 'soul', 'funk'],
    'latin': ['latin', 'latino', 'brazil', 'samba', 'salsa', 'pagode', 'forro', 'mpb', 'sertanejo', 'tango'],
    'world': ['afrobeat', 'indian', 'iranian', 'british', 'malay', 'mandopop', 'cantopop', 'swedish', 'french', 
              'german', 'spanish', 'turkish', 'world-music', 'gospel'],
    'folk/country': ['folk', 'singer-songwriter', 'songwriter', 'honky-tonk', 'country', 'acoustic'],
    'experimental': ['ambient', 'industrial', 'goth', 'idm', 'trip-hop', 'minimal-techno', 'avant-garde', 'chill', 'indie'],
    'classical': ['classical', 'piano', 'opera', 'new-age'],
    'reggae-like': ['reggae', 'ska', 'dub', 'groove'],
    'miscellaneous': ['sleep', 'study', 'happy', 'sad', 'party', 'dance']
})

def assign_meta_genres(df, ORDERED_DICT):
    '''
    Assigns a meta-genre to each row in the DataFrame based on the track_genre column, sorted according to an ORDERED_DICT. 
    Returns: DataFrame with new 'meta_genre' column.
    '''
    def map_genre(genre):
        if genre in ORDERED_DICT:  # Check if genre is a meta-genre key itself
            return genre
        for meta_genre, subgenres in ORDERED_DICT.items():
            if genre in subgenres:
                return meta_genre
        return 'other'

    # formatting
    df = df.copy()
    df['track_genre'] = df['track_genre'].astype(str).str.strip().str.lower()

    # mapping
    df['meta_genre'] = df['track_genre'].apply(map_genre)
    df['meta_genre'] = df['meta_genre'].astype('category')

    return df


def remove_meta_duplicates(df, ORDERED_DICT):
    '''
    Removes duplicate tracks while keeping the highest-priority genre entry.
    Priority is determined by the ORDERED_DICT dictionary.
    Returns: DataFrame with duplicates removed.
    '''
    print('Initial dataset shape: {}'.format(df.shape))
    df['genre_rank'] = df['meta_genre'].apply(lambda g: list(ORDERED_DICT.keys()).index(g) 
                                              if g in ORDERED_DICT else len(ORDERED_DICT))
    df = df.sort_values(by='genre_rank')
    df = df.drop_duplicates(subset=['track_id'], keep='first')
    df = df.drop(columns=['genre_rank'])
    df = df.sort_index()
    print('Duplicates removed! Final shape: {}'.format(df.shape))
    return df

def engineer_features(df):
    """
    Enhances the dataset with new features to improve Danceability predictions.
    """

    # Tempo Categories: Bins tempo into slow, mid, and fast using an if-elif-else loop
    def categorize_tempo(tempo):
        if tempo >= 120:
            return 'fast'
        elif tempo >= 90:
            return 'mid'
        else:
            return 'slow'
    
    df['tempo_category'] = df['tempo'].apply(categorize_tempo)

    # Beat Density: Tempo relative to time signature
    df['beat_density'] = np.where(df['time_signature'] == 0, 0, df['tempo'] / df['time_signature'])

    # Energy-Tempo Interaction: Do energetic AND fast-paced songs correlate with danceability?
    df['energy_tempo_interaction'] = df['energy'] * df['tempo']

    # Groove Score: Danceability weighted by instrumentalness (lower means more vocals)
    df['groove_score'] = df['danceability'] * (1 - df['instrumentalness'])

    # Party Factor: Combination of Valence & Energy
    df['party_factor'] = df['valence'] * df['energy']
    
    # Mood Score: Weighted combination of valence, energy, and tempo
    df['mood_score'] = 0.4 * df['valence'] + 0.4 * df['energy'] + 0.2 * (df['tempo'] / 200)

    return df