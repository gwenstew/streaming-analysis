# call tmdb api to extract trending movies - titles, director, actors, release year, genres, source?
#  get top 20 movies to start maybe go up to 100
# call tmdb once to get genre id mappings
# could also get top rated movies to see how this changes over time?
import requests
from dotenv import load_dotenv
import psycopg2
import json
import os
from datetime import datetime

load_dotenv()

API_KEY= os.getenv("TMDB_API_KEY")
TMDB_BEARER_TOKEN= os.getenv("TMDB_BEARER_TOKEN")
POSTGRES_USER= os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD= os.getenv("POSTGRES_PASSWORD")
DATABASE_URL=os.getenv("DATABASE_URL")

def get_movies(num_movies=5):
    url="https://api.themoviedb.org/3/movie/popular"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_BEARER_TOKEN}"
    }

    movies = []
    page = 1

    while len(movies) < num_movies:
        #fetch next page of movies
        params = {
            "language": "en-US",
            "page": page
        }

        response = requests.get(url, headers=headers, params=params)
        print(f"fetching page {page}...{response.status_code}")
        data = response.json()
        results = data.get("results", []) 

        movies.extend(results)
        page+=1

    return movies[:num_movies] 


def get_movie_credits(movie_id):
    url=f"https://api.themoviedb.org/3/movie/{movie_id}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_BEARER_TOKEN}"
    }

    params = {
        "language": "en-US",
        "append_to_response": "credits"
    }

    response = requests.get(url, headers=headers, params=params)
    
    return response.json()

def transform_movie(movie):
    credits = movie.get("credits")
    crew = credits.get("crew")
    cast = credits.get("cast")

    crew_by_job = {}
    for person in crew:
        crew_by_job.setdefault(person.get("job"),[]).append(person.get("name"))

    directors = crew_by_job["Director"]
    top_cast = [actor.get("name") for actor in cast[:5]]
    genres = [g["name"] for g in movie.get("genres", [])]
    
    return {
        "id": movie["id"],
        "title": movie["title"],
        "release_date": movie["release_date"],
        "language": movie["original_language"],
        "director": directors,
        "cast": top_cast,
        "genres": genres,
        "popularity": movie["popularity"],
        "vote_avg": movie["vote_average"],
        "vote_count": movie["vote_count"]
    }

def get_top_movies(num_movies=5):
    movies = get_movies(num_movies)

    transformed_movies = []

    for movie in movies:
        movie_data = get_movie_credits(movie.get("id"))
        transformed_movies.append(transform_movie(movie_data))

    return transformed_movies


def load_to_postgres(movies):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    for movie in movies:
        # Insert into movies table
        cur.execute("""
            INSERT INTO raw.movies (id, title, release_date, language, genres, director, cast, source)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            movie["id"],
            movie["title"],
            movie.get("release_date") or None,
            movie.get("language"),
            movie.get("genres", []),
            movie.get("director", []),
            movie.get("cast", []),
            "tmdb"
        ))

        # Insert into ratings table
        cur.execute("""
            INSERT INTO raw.ratings (movie_id, score, vote_avg, vote_count, rating source)
            VALUES (%s, %s, %s, %s, %s);
        """, (
            movie["id"],
            movie.get("popularity"),
            movie.get("vote_average"),
            movie.get("vote_count"),
            "tmdb"
        ))


    conn.commit()
    cur.close()
    conn.close()
    return


def main():
    movies = get_top_movies(5)
    load_to_postgres(movies)


if __name__ == "__main__":
    main()
