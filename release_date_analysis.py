import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

load_dotenv()

db_config={
    'host': 'localhost',
    'user': 'root',
    'password': '12345678',
    'database': 'spotify_db'
}

def update_schema():
    """Add release_date column to spotify_tracks table"""
    connection= mysql.connector.connect(**db_config)
    cursor=connection.cursor()
    cursor.execute("SHOW COLUMNS FROM spotify_tracks LIKE 'release_date'")
    column_exists=cursor.fetchone()
    if not column_exists:
        cursor.execute("ALTER TABLE spotify_tracks ADD COLUMN release_date DATE")
        print("column add done")
    cursor.close()
    connection.close()


def fetch_release_dates():


    """Fetch release dates for tracks and update the database"""
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
    ))
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT id, track_name, artist FROM spotify_tracks WHERE release_date IS NULL")
    tracks = cursor.fetchall()
    updated_count = 0
    for track_id, track_name, artist in tracks:
        try:
            search_query = f"track:{track_name} artist:{artist}"
            results = sp.search(search_query, type='track', limit=1)
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                album = track['album']
                release_date = album['release_date']
                #normalise
                if len(release_date) == 4: 
                    release_date = f"{release_date}-01-01"
                elif len(release_date) == 7:
                    release_date = f"{release_date}-01"
                cursor.execute(
                    "UPDATE spotify_tracks SET release_date = %s WHERE id = %s",
                    (release_date, track_id)
                )
                connection.commit()
                updated_count += 1
                if updated_count % 20 == 0:
                    print(f"Updated {updated_count} tracks with release dates DONE")
                
        except Exception as e:
            print(f"Error updating {track_name}: {e}")
    
    print(f" {updated_count} tracks with release dates DONE")
    cursor.close()
    connection.close()   


def analyze_by_year():
    """Analyze tracks by year released"""
    connection=mysql.connector.connect(**db_config)
    query="""SELECT track_name,artist,album,popularity,duration_minutes,YEAR(release_date) as release_year
            FROM spotify_tracks WHERE release_date IS NOT NULL"""
    df=pd.read_sql(query, connection)
    os.makedirs('visualisations', exist_ok=True)
    #tracks_yoy
    plt.figure(figsize=(15, 6))
    year_counts=df['release_year'].value_counts().sort_index()
    year_counts.plot(kind='bar')
    plt.title('Number of Tracks Released by Year')
    plt.xlabel('Year')  
    plt.ylabel('Number of Tracks')
    plt.xticks(rotation=90)
    plt.tight_layout() #auto adjust pading
    plt.savefig('visualisations/tracks_by_year.png')
    plt.close()

    #popularity yoy
    plt.figure(figsize=(15, 6))
    year_popularity = df.groupby('release_year')['popularity'].mean()
    year_popularity.plot(kind='line', marker='o')
    plt.title('Average Track Popularity by Release Year')
    plt.xlabel('Year')
    plt.ylabel('Average Popularity')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('visualisations/popularity_by_year.png')
    plt.close()

    #duration yoy
    plt.figure(figsize=(14, 6))
    year_duration = df.groupby('release_year')['duration_minutes'].mean()
    year_duration.plot(kind='line', marker='o')
    plt.title('Average Track Duration by Release Year')
    plt.xlabel('Year')
    plt.ylabel('Average Duration (minutes)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('visualisations/duration_by_year.png')
    plt.close()

    #stats
    with open('visualisations/year_analysis_summary.txt', 'w') as f:
        f.write("=== Release Year Analysis ===\n\n")
        f.write(f"Earliest Track Year: {df['release_year'].min()}\n")
        f.write(f"Latest Track Year: {df['release_year'].max()}\n")
        f.write(f"Most Common Year: {df['release_year'].mode()[0]}\n")
        f.write(f"Year with Highest Average Popularity: {year_popularity.idxmax()} ({year_popularity.max():.2f})\n")
        f.write(f"Year with Longest Average Duration: {year_duration.idxmax()} ({year_duration.max():.2f} minutes)\n")
    
    connection.close()
    print("DONE")

if __name__ == "__main__":
    update_schema()
    fetch_release_dates()
    analyze_by_year()
    
