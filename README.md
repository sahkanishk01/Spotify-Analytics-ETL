# Spotify ETL Pipeline

A complete **Extract, Transform, Load (ETL)** pipeline to fetch and store Spotify track data using Python and MySQL. Built to enable structured analysis of music trends and metadata using Spotify's API.

---

## Overview

This project extracts track information (artists, albums, genres, etc.) from the Spotify API using `Spotipy`, transforms it using Python, and loads it into a **MySQL database** for analysis or visualization.

---

## Tech Stack

- Python 3.x  
- MySQL  
- [Spotipy](https://spotipy.readthedocs.io/en/2.22.1/) – Spotify Web API wrapper  
- `python-dotenv` – for managing credentials  
- `mysql-connector-python` – for DB connectivity

---

## Setup

### Prerequisites

- Python 3.x installed  
- MySQL installed and running  
- Spotify Developer Account (for API keys)  
 [Create one here](https://developer.spotify.com/dashboard/)

---
### 📥 Installation

#### 1. **Clone the repository**
```bash
git clone https://github.com/your-username/spotify-etl-pipeline.git
cd spotify-etl-pipeline
```

### 2. (Optional) Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

###3. 3. Install Dependencies
```
pip install -r requirements.txt
```

4. Set up .env file
Create a .env file in the root directory and add your Spotify credentials:
```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
```

5. Create MySQL Database
Run the provided SQL schema (you can also use a tool like MySQL Workbench):
```
source spotify.sql
```

 Run the Project
 ```
python3 spotify_urls.py
```

## This script will:

Authenticate via Spotify API

Extract track/artist/album data

Transform and load it into the MySQL database




