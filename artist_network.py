import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from mysql.connector import connect
import os
from itertools import combinations
from dotenv import load_dotenv

load_dotenv()

def create_artist_network():
    """Create network analysis of artist relationships"""
    # Connect to database
    connection = connect(
        host='localhost',
        user='root',
        password='12345678',
        database='spotify_db'
    )
    
    # Create folders for visualizations
    os.makedirs('visualisations/network', exist_ok=True)
    
    # Get artist data
    df = pd.read_sql("SELECT artist, album, popularity FROM spotify_tracks", connection)
    
    # Create network graph
    G = nx.Graph()
    
    # Count artist occurrences
    artist_counts = df['artist'].value_counts()
    
    # Add top artists as nodes (limit to top 30 for visibility)
    top_artists = artist_counts.head(30).index
    
    # Add nodes with size based on number of tracks
    for artist in top_artists:
        G.add_node(artist, size=artist_counts[artist])
    
    # Create edges between artists based on appearing in the same albums
    artist_albums = {}
    for _, row in df.iterrows():
        if row['artist'] in top_artists:
            if row['artist'] not in artist_albums:
                artist_albums[row['artist']] = set()
            artist_albums[row['artist']].add(row['album'])
    
    # Create edges between artists who share albums or have similar popularity
    for artist1, artist2 in combinations(top_artists, 2):
        # Artists with similar popularity (within 15 points)
        a1_pop = df[df['artist'] == artist1]['popularity'].mean()
        a2_pop = df[df['artist'] == artist2]['popularity'].mean()
        
        if abs(a1_pop - a2_pop) <= 15:
            # Add edge with weight based on popularity similarity
            weight = 1 + (15 - abs(a1_pop - a2_pop)) / 15
            G.add_edge(artist1, artist2, weight=weight)
    
    # Create visualization
    plt.figure(figsize=(20, 20))
    
    # Calculate node size based on number of tracks
    node_sizes = [G.nodes[artist]['size'] * 10 for artist in G.nodes]
    
    # Get edge weights for width
    edge_weights = [G[u][v]['weight'] * 0.5 for u, v in G.edges]
    
    # Set positions - spring layout groups related nodes together
    pos = nx.spring_layout(G, k=0.6, seed=42)
    
    # Draw the graph elements
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                          node_color='lightblue', alpha=0.8)
    nx.draw_networkx_edges(G, pos, width=edge_weights, alpha=0.5, 
                          edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    plt.title("Artist Relationship Network", size=20)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('visualisations/network/artist_network.png', dpi=300)
    plt.close()
    
    # Generate summary statistics
    with open('visualisations/network/network_stats.txt', 'w') as f:
        f.write("=== Artist Network Analysis ===\n\n")
        f.write(f"Number of artists: {len(G.nodes)}\n")
        f.write(f"Number of connections: {len(G.edges)}\n")
        
        # Find most connected artists
        degree_centrality = nx.degree_centrality(G)
        top_central = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        
        f.write("\nMost connected artists:\n")
        for artist, score in top_central:
            f.write(f"- {artist}: {score:.3f}\n")
        
        # Find distinct communities
        communities = list(nx.community.greedy_modularity_communities(G))
        f.write(f"\nNumber of artist communities: {len(communities)}\n")
        
        f.write("\nLargest communities:\n")
        for i, community in enumerate(communities[:3]):
            f.write(f"Community {i+1}: {', '.join(list(community)[:5])}")
            if len(community) > 5:
                f.write(f" and {len(community)-5} more")
            f.write("\n")
    
    connection.close()
    print("Artist network analysis complete! Check visualisations/network folder.")

if __name__ == "__main__":
    try:
        # Install networkx if not already installed
        import networkx
    except ImportError:
        print("Installing required packages...")
        import subprocess
        subprocess.check_call(["pip", "install", "networkx"])
        
    create_artist_network()