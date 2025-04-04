import pandas as pd

def detect_rating_drift(new_df: pd.DataFrame, reference_df: pd.DataFrame, threshold: float = 0.1) -> bool:
    """Detect if mean rating changed too much."""
    old_mean = reference_df['rating'].mean()
    new_mean = new_df['rating'].mean()
    drift = abs(old_mean - new_mean)

    print(f"Reference rating mean: {old_mean:.2f}")
    print(f"New rating mean: {new_mean:.2f}")
    print(f"Drift: {drift:.4f} (threshold={threshold})")

    return drift > threshold
