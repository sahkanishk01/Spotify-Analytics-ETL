from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import pandas as pd
from mysql.connector import connect
from dotenv import load_dotenv
import os

def build_recommender():
    connection = connect(
        host='localhost',
        user='root',
        password='12345678',
        database='spotify_db'
    )
    
    
    df = pd.read_sql('SELECT * FROM spotify_tracks', connection)
    
    
    features = ['popularity', 'duration_minutes']
    X = df[features]
    
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
   
    kmeans = KMeans(n_clusters=5, random_state=42)
    df['cluster'] = kmeans.fit_predict(X_scaled)
    
    
    def get_recommendations(track_name):
        if track_name not in df['track_name'].values:
            return "Track not found in database"
        
        cluster = df[df['track_name'] == track_name]['cluster'].values[0]
        similar_songs = df[df['cluster'] == cluster].sample(5)
        return similar_songs[['track_name', 'artist', 'popularity']]
    
    return get_recommendations

if __name__ == "__main__":
    recommender = build_recommender()
    track_name = "Blinding Lights"  
    recommendations = recommender(track_name)
    print(f"\nRecommendations for {track_name}:")
    print(recommendations)