import pandas as pd
import matplotlib.pyplot as plt
from mysql.connector import connect
import os
import re

def analyze_collaborations():
    """Analyze artist collaborations from track names"""
    
    connection = connect(
        host='localhost',
        user='root',
        password='12345678',
        database='spotify_db',
        
    )
    
    # Create visualization directory
    os.makedirs('visualisations/collaborations', exist_ok=True)
    
    # Get all tracks
    query = """
    SELECT track_name, artist, album, popularity
    FROM spotify_tracks
    """
    
    df = pd.read_sql(query, connection)
    connection.close()
    
    # Find collaborations (tracks with "feat.", "ft.", "&", "with", etc.)
    collab_patterns = [
        r'feat\.?\s+([^()\[\]]+)',
        r'ft\.?\s+([^()\[\]]+)',
        r'\s+&\s+([^()\[\]]+)',
        r'\s+and\s+([^()\[\]]+)',
        r'\s+with\s+([^()\[\]]+)',
        r'\(with\s+([^()\[\]]+)\)',
        r'\(feat\.?\s+([^()\[\]]+)\)',
        r'\(ft\.?\s+([^()\[\]]+)\)'
    ]
    
    # Find collaborations
    collaborations = []
    
    for _, row in df.iterrows():
        track = row['track_name']
        main_artist = row['artist']
        
        # Check each pattern for collaborations
        for pattern in collab_patterns:
            match = re.search(pattern, track, re.IGNORECASE)
            if match:
                # Extract collaborator
                collab_artist = match.group(1).strip()
                
                # Add to collaborations list
                collaborations.append({
                    'track_name': track,
                    'main_artist': main_artist,
                    'collaborator': collab_artist,
                    'popularity': row['popularity']
                })
                break
    
    # Create DataFrame for collaborations
    collab_df = pd.DataFrame(collaborations)
    
    # Save collaborations to CSV
    if len(collab_df) > 0:
        collab_df.to_csv('visualisations/collaborations/collaborations.csv', index=False)
        
        # Get top collaborators
        top_collaborators = collab_df['collaborator'].value_counts().head(15)
        
        # Create bar chart of top collaborators
        plt.figure(figsize=(12, 8))
        top_collaborators.plot(kind='barh')
        plt.title('Top Featured Artists')
        plt.xlabel('Number of Collaborations')
        plt.tight_layout()
        plt.savefig('visualisations/collaborations/top_collaborators.png')
        plt.close()
        
        # Find most successful collaborations by popularity
        top_collabs = collab_df.nlargest(10, 'popularity')
        
        # Generate report
        with open('visualisations/collaborations/collaboration_report.txt', 'w') as f:
            f.write("=== Artist Collaboration Analysis ===\n\n")
            f.write(f"Total Collaborations Found: {len(collab_df)}\n\n")
            
            f.write("Most Frequent Collaborators:\n")
            for artist, count in top_collaborators.head(5).items():
                f.write(f"• {artist}: {count} collaborations\n")
            
            f.write("\nMost Popular Collaborations:\n")
            for _, row in top_collabs.iterrows():
                f.write(f"• {row['track_name']} - {row['main_artist']} feat. {row['collaborator']} (Popularity: {row['popularity']})\n")
    else:
        with open('visualisations/collaborations/collaboration_report.txt', 'w') as f:
            f.write("No collaborations found in the dataset.\n")
    
    print("Artist collaboration analysis complete!")

if __name__ == "__main__":
    analyze_collaborations()