import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mysql.connector import connect
from dotenv import load_dotenv
import os

def analyze_spotify_data():
    connection = connect(
        host="localhost",
        database="spotify_db",
        user="root",
        password="12345678"
    )
    
    os.makedirs('visualisations', exist_ok=True)
    
    
    df = pd.read_sql("SELECT * FROM spotify_tracks", connection)
    
    #pop dist
    plt.figure(figsize=(12, 6))
    sns.histplot(data=df, x='popularity', bins=20)
    plt.title('Track Popularity Distribution')
    plt.savefig('visualisations/popularity_dist.png')
    plt.close()
    
    #top artists
    plt.figure(figsize=(12, 6))
    df['artist'].value_counts().head(10).plot(kind='bar')
    plt.title('Top 10 Artists by Number of Tracks')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('visualisations/top_artists.png')
    plt.close()
    
    #duation-popularity
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='duration_minutes', y='popularity')
    plt.title('Track Duration vs Popularity')
    plt.savefig('visualisations/duration_vs_popularity.png')
    plt.close()
    
    #stats
    stats = {
        'total_tracks': len(df),
        'unique_artists': df['artist'].nunique(),
        'avg_popularity': df['popularity'].mean(),
        'avg_duration': df['duration_minutes'].mean(),
        'most_popular_track': df.loc[df['popularity'].idxmax(), 'track_name']
    }
    
    #add to folder file
    with open('visualisations/stats_summary.txt', 'w') as f:
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")
    
    return stats

if __name__ == "__main__":
    stats = analyze_spotify_data()
    print("Analysis complete! Check visualisations folder.")