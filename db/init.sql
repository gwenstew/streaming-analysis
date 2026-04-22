CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.movies (
    id INT PRIMARY KEY,
    title TEXT,
    release_date DATE,
    language TEXT,
    genres TEXT[],
    director TEXT[],
    "cast" TEXT[],
    source TEXT,
    scraped_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS raw.ratings (
    id SERIAL PRIMARY KEY,
    movie_id INT REFERENCES raw.movies(id),
    title TEXT,
    score NUMERIC,
    vote_avg NUMERIC,
    vote_count NUMERIC,
    rating_source TEXT,
    scraped_at TIMESTAMP DEFAULT NOW()
);
