from surprise import SVD, Dataset, Reader, accuracy
from surprise.model_selection import train_test_split
import pandas as pd

# Load your DataFrame (from MovieLens)
ratings = pd.read_csv("data/processed/ratings_with_features.csv")

# Surprise requires a specific format: user_id, item_id, rating
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings[['user_id', 'movie_id', 'rating']], reader)

# Train-test split (80/20)
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

# Train the model
model = SVD()
model.fit(trainset)

# Predict on test set
predictions = model.test(testset)

# Evaluate
rmse = accuracy.rmse(predictions)
mae = accuracy.mae(predictions)

from collections import defaultdict

def precision_at_k(predictions, k=10, threshold=4.0):
    """
    Compute Precision@K for each user.
    A hit is a movie with predicted rating >= threshold and true rating >= threshold.
    """
    # Organize predictions by user
    user_est_true = defaultdict(list)
    for pred in predictions:
        user_est_true[pred.uid].append((pred.est, pred.r_ui))

    precisions = []

    for uid, user_ratings in user_est_true.items():
        # Sort by estimated rating
        user_ratings.sort(key=lambda x: x[0], reverse=True)
        top_k = user_ratings[:k]

        # Count how many in top K are relevant (true rating >= threshold)
        relevant = sum((true >= threshold) for (_, true) in top_k)
        precisions.append(relevant / k)

    # Return average Precision@K
    return sum(precisions) / len(precisions)

def split_users_by_activity(ratings_df, threshold=50): # 50 is the threshold for active users 
    user_counts = ratings_df.groupby("user_id").size()
    active_users = set(user_counts[user_counts >= threshold].index)
    inactive_users = set(user_counts[user_counts < threshold].index)
    return active_users, inactive_users


p_at_10 = precision_at_k(predictions, k=10)
print(f"Precision@10: {p_at_10:.4f}")

# Get subpopulations
active_users, inactive_users = split_users_by_activity(ratings)

# Filter predictions
active_preds = [p for p in predictions if int(p.uid) in active_users]
inactive_preds = [p for p in predictions if int(p.uid) in inactive_users]

# Evaluate separately
print("Active users:")
print("  RMSE:", accuracy.rmse(active_preds, verbose=False))
print("  MAE :", accuracy.mae(active_preds, verbose=False))
print("  Precision@10:", precision_at_k(active_preds, k=10))

print("\nInactive users:")
print("  RMSE:", accuracy.rmse(inactive_preds, verbose=False))
print("  MAE :", accuracy.mae(inactive_preds, verbose=False))
print("  Precision@10:", precision_at_k(inactive_preds, k=10))


