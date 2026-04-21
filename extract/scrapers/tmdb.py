# call tmdb api to extract trending movies - titles, director, actors, release year, genres, source?
# call tmdb every day? get top 20 movies to start maybe go up to 100
# call tmdb once to get genre id mappings
# could also get top rated movies to see how this changes over time?
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY= os.getenv("TMDB_API_KEY")
BEARER_TOKEN= os.getenv("TMDB_BEARER_TOKEN")

def get_trending(n:int):
    #fetch top n movies from tmdb
    # get id, title, director, release date, country, genre, popularity,
    
    url="https://api.themoviedb.org/3/trending/movie/day?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    print(response.status_code)
    print(response.json())
    return


def main():
    get_trending(5)


if __name__ == "__main__":
    main()
