import pandas as pd
from validators import validate_schema
from drift_detector import detect_rating_drift

def load_ratings(file_path):
    df = pd.read_csv(file_path)
    
    # Validate schema
    validate_schema(df)

    # Load reference data (previous clean baseline)
    reference_df = pd.read_csv("data/reference/ratings_reference.csv")

    # Detect data drift
    detect_rating_drift(df, reference_df)

    return df