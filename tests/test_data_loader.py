import pytest
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_loader import load_ratings

def test_load_valid_data():
    df = load_ratings("data/processed/ratings_with_features.csv")
    assert not df.empty
    assert {'user_id', 'movie_id', 'rating'}.issubset(df.columns)

def test_missing_columns():
    df = pd.DataFrame({'user_id': [1], 'rating': [5.0]})
    df.to_csv("temp.csv", index=False)
    with pytest.raises(ValueError):
        load_ratings("temp.csv")