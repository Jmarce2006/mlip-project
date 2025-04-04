import pandas as pd
import requests
import time
import json
import os
from datetime import datetime

# === Load Data ===
ratings = pd.read_csv("data/raw/ml-100k/u.data", sep="\t", header=None, 
                     names=["user_id", "movie_id", "rating", "timestamp"])

movies = pd.read_csv("data/raw/ml-100k/u.item", sep="|", header=None, encoding='latin-1',
                    names=["movie_id", "title", "release_date", "video_release_date",
                           "IMDb_URL", "unknown", "Action", "Adventure", "Animation",
                           "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
                           "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi",
                           "Thriller", "War", "Western"])

# Calculate average rating for each movie
movie_avg_ratings = ratings.groupby('movie_id')['rating'].mean().to_dict()

# Get list of genre columns (excluding non-genre columns)
genre_columns = movies.columns[6:]  # All columns after "unknown" are genres

# Convert to user → {movie_id: rating} dict
user_ratings = ratings.groupby('user_id').apply(
    lambda df: dict(zip(df['movie_id'], df['rating']))
).to_dict()

# === Evaluate Recommendations ===
logs = []

for user_id in list(user_ratings.keys())[:100]:  # Adjust number of users if needed
    try:
        start = time.time()

        # Call the actual API
        response = requests.get(f"http://localhost:8082/recommend/{user_id}", timeout=1.0)
        latency = round((time.time() - start) * 1000, 2)  # in ms

        if response.status_code == 200:
            recs = list(map(int, response.text.strip().split(",")))
            print(f"Recommendations for user {user_id}: {recs}")
            
            # Get movie information for recommended movies
            recommended_movies = movies[movies['movie_id'].isin(recs)]
            
            # Calculate average rating for recommendations
            rec_ratings = [movie_avg_ratings.get(movie_id, 0) for movie_id in recs]
            avg_rating = sum(rec_ratings) / len(rec_ratings) if rec_ratings else 0
            
            print(f"\nAverage Rating for Recommendations: {avg_rating:.2f}")
            
            # Calculate genre distribution
            genre_distribution = {}
            for genre in genre_columns:
                genre_count = recommended_movies[genre].sum()
                genre_distribution[genre] = {
                    'count': int(genre_count),
                    'percentage': round((genre_count / len(recs)) * 100, 2) if len(recs) > 0 else 0
                }
            
            print("\nGenre Distribution in Recommendations:")
            for genre, stats in genre_distribution.items():
                if stats['count'] > 0:  # Only show genres that appear in recommendations
                    print(f"{genre}: {stats['count']} movies ({stats['percentage']}%)")
            
            logs.append({
                "timestamp": datetime.utcnow().isoformat(),
                "user_id": user_id,
                "recommendations": recs,
                "recommended_movies": recommended_movies[['movie_id', 'title']].to_dict('records'),
                "genre_distribution": genre_distribution,
                "avg_rating": round(avg_rating, 4),
                "latency_ms": latency
            })

    except Exception as e:
        print(f"Error for user {user_id}: {e}")

# === Save Logs ===
os.makedirs("data/logs", exist_ok=True)
with open("data/logs/online_eval_logs.json", "w") as f:
    json.dump(logs, f, indent=2)

# === Print Summary ===
# Calculate overall genre distribution across all recommendations
overall_genre_distribution = {}
for genre in genre_columns:
    total_count = sum(log["genre_distribution"][genre]['count'] for log in logs)
    total_movies = sum(len(log["recommendations"]) for log in logs)
    overall_genre_distribution[genre] = {
        'count': total_count,
        'percentage': round((total_count / total_movies) * 100, 2) if total_movies > 0 else 0
    }

print("\nOverall Genre Distribution:")
for genre, stats in overall_genre_distribution.items():
    if stats['count'] > 0:  # Only show genres that appear in recommendations
        print(f"{genre}: {stats['count']} movies ({stats['percentage']}%)")

# Calculate overall average rating
overall_avg_rating = sum(log["avg_rating"] for log in logs) / len(logs)
print(f"\nOverall Average Rating for Recommendations: {overall_avg_rating:.2f}")

avg_latency = sum(log["latency_ms"] for log in logs) / len(logs)
print(f"Average Latency: {avg_latency:.2f} ms")
