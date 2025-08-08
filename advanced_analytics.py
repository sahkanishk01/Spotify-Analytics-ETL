import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mysql.connector import connect
from dotenv import load_dotenv
import os

load_dotenv()

try:
    
    connection = connect(
        host='localhost',
        user='root',
        password='12345678',  
        database='spotify_db'
    )

    
    df = pd.read_sql('SELECT * FROM spotify_tracks', connection)  

    def analyze_advanced_metrics():
        os.makedirs('visualizations', exist_ok=True)
        
        
        plt.figure(figsize=(12, 6))
        df['artist'].value_counts().head(10).plot(kind='pie')  
        plt.title('Top Artists Distribution')
        plt.savefig('visualizations/artist_dist.png')
        plt.close()

        
        artist_features = pd.pivot_table(df, 
                                    values='popularity',
                                    index='artist',
                                    aggfunc='mean')
        plt.figure(figsize=(10, 6))
        sns.heatmap(artist_features.head(10).corr())
        plt.title('Artist Popularity Correlation')
        plt.savefig('visualizations/artist_correlation.png')
        plt.close()

    if __name__ == "__main__":
        analyze_advanced_metrics()
        print("Advanced analytics complete! Check visualizations folder.")

except Exception as e:
    print(f"Error: {e}")
finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()