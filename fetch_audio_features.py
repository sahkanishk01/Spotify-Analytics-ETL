import re
import spotipy
import mysql.connector
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

load_dotenv()


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
))


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345678',
    'database': 'spotify_db'
}


def create_audio_features_table():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS audio_features (
        track_id VARCHAR(255) PRIMARY KEY,
        danceability FLOAT,
        energy FLOAT, 
        key_value INT,
        loudness FLOAT,
        tempo FLOAT,
        valence FLOAT,
        acousticness FLOAT,
        instrumentalness FLOAT,
        liveness FLOAT,
        speechiness FLOAT,
        FOREIGN KEY (track_id) REFERENCES spotify_tracks(id)
    )
    """
    cursor.execute(create_table_query)
    connection.commit()
    connection.close()


def fetch_and_store_audio_features():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
  
    cursor.execute("SELECT id, track_name FROM spotify_tracks")
    tracks = cursor.fetchall()
    
    for track_id, track_name in tracks:
        try:
            
            spotify_id = re.search(r'([a-zA-Z0-9]{22})', track_id).group(1)
            
            
            features = sp.audio_features(spotify_id)[0]
            
            if features:
                
                insert_query = """
                INSERT IGNORE INTO audio_features 
                (track_id, danceability, energy, key_value, loudness, tempo, 
                valence, acousticness, instrumentalness, liveness, speechiness)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    track_id,
                    features['danceability'],
                    features['energy'],
                    features['key'],
                    features['loudness'],
                    features['tempo'],
                    features['valence'],
                    features['acousticness'],
                    features['instrumentalness'],
                    features['liveness'],
                    features['speechiness']
                ))
                connection.commit()
                print(f"Added audio features for: {track_name}")
        except Exception as e:
            print(f"Error processing {track_name}: {e}")
    
    connection.close()

if __name__ == "__main__":
    create_audio_features_table()
    fetch_and_store_audio_features()
    print("Audio features extraction complete!")