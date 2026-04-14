# call tmdb api to extract trending movies - titles, director, actors, release year, genres, source?
# call tmdb every day? get top 20 movies to start maybe go up to 100
# call tmdb once to get genre id mappings
# could also get top rated movies to see how this changes over time?
import requests
import psycopg2
import os

API_KEY= os.getenv("TMDB_API_KEY")

def get_trending(n:int):
    #fetch top n movies from tmdb
    # get id, title, director, release date, country, genre, popularity,
    
    url=f""
    
    return
