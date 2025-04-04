import pandas as pd

REQUIRED_COLUMNS = {
    'user_id': int,
    'movie_id': int,
    'rating': int,
    'timestamp': int,
}

def validate_schema(df: pd.DataFrame) -> bool:
    for column, expected_type in REQUIRED_COLUMNS.items():
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")
        if not pd.api.types.is_dtype_equal(df[column].dtype, expected_type):
            print(f"⚠️ Column '{column}' expected {expected_type}, got {df[column].dtype}")
    return True
