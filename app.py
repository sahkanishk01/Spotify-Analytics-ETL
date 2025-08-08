import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
from mysql.connector import connect
import matplotlib.pyplot as plt
import seaborn as sns


@st.cache_data  
def load_data():
    connection = connect(
        host='localhost',
        user='root',
        password='12345678',
        database='spotify_db'
    )
    df = pd.read_sql('SELECT * FROM spotify_tracks', connection)
    connection.close()
    return df

def load_audio_features():
    connection = connect(
        host='localhost',
        user='root',
        password='12345678',
        database='spotify_db'
    )
    query = """
    SELECT 
        t.track_name, t.artist, t.album, t.popularity, t.duration_minutes,
        a.danceability, a.energy, a.valence, a.acousticness
    FROM spotify_tracks t
    JOIN audio_features a ON t.id = a.track_id
    """
    df = pd.read_sql(query, connection)
    connection.close()
    return df

def run_dashboard():
    st.title('Spotify Music Analysis Dashboard')
    
    try:
       
        df = load_data()
        
        
        st.sidebar.header('Filters')
        artist_filter = st.sidebar.multiselect('Select Artists', df['artist'].unique())
        popularity_filter = st.sidebar.slider('Minimum Popularity', 0, 100, 30)

        
        filtered_df = df
        if artist_filter:
            filtered_df = filtered_df[filtered_df['artist'].isin(artist_filter)]
        filtered_df = filtered_df[filtered_df['popularity'] >= popularity_filter]

        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Tracks", len(filtered_df))
        with col2:
            st.metric("Average Popularity", round(filtered_df['popularity'].mean(), 2))
        with col3:
            st.metric("Average Duration (mins)", round(filtered_df['duration_minutes'].mean(), 2))

       
        st.subheader('Popularity Distribution')
        fig_pop = px.histogram(filtered_df, x='popularity', nbins=20)
        st.plotly_chart(fig_pop)

       
        st.subheader('Top Artists by Track Count')
        top_artists = filtered_df['artist'].value_counts().head(10)
        fig_artists = px.bar(x=top_artists.index, y=top_artists.values)
        st.plotly_chart(fig_artists)

       
        st.subheader('Duration vs Popularity')
        fig_scatter = px.scatter(filtered_df, x='duration_minutes', y='popularity')
        st.plotly_chart(fig_scatter)
        
        
        st.subheader('Audio Features Analysis')
        try:
            features_df = load_audio_features()
            
            
            feature_columns = ['danceability', 'energy', 'valence', 'acousticness']
            fig = px.line_polar(
                features_df.head(10), 
                r=[features_df[col].mean() for col in feature_columns],
                theta=feature_columns, 
                line_close=True
            )
            st.plotly_chart(fig)

            
            st.subheader('Audio Feature Distributions')
            feature_select = st.selectbox(
                'Select audio feature', 
                ['danceability', 'energy', 'valence', 'acousticness']
            )
            fig_feature = px.histogram(features_df, x=feature_select)
            st.plotly_chart(fig_feature)
        except Exception as e:
            st.warning(f"Audio features not available: {str(e)}")

        
        st.subheader('Track Details')
        st.dataframe(filtered_df[['track_name', 'artist', 'album', 'popularity', 'duration_minutes']])

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")

if __name__ == "__main__":
    run_dashboard()