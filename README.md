# Spotify ETL Pipeline

Extract, Transform, and Load pipeline for Spotify track data using Python and MySQL.

## Overview
This project fetches track information from Spotify's API and stores it in a MySQL database for analysis.

## Tech Stack
- Python 3.x
- MySQL
- Spotipy (Spotify API wrapper)
- Python-dotenv
- MySQL Connector

## Setup

### Prerequisites
- Python 3.x
- MySQL
- Spotify Developer Account

### Installation
1. Clone the repository:
```bash
git clone https://github.com/SharmaKabir/spotify-analytics-ETL
cd spotify-de-project
```

2. Create Virtual Environment (Optional):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install Dependencies:
```bash
pip install -r requirements.txt
```

4. Set up .ENV file:
```bash
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
```

5. Create MySQL DB (Use this command / run commands one-by-one in the .sql file):
```bash
source spotify.sql
```

### Run the project
1. Run:
```bash
python3 spotify_urls.py
```


