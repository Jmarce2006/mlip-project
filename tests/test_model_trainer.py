import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from model_trainer import train_model

def test_model_training():
    df = pd.read_csv("data/processed/ratings_with_features.csv")
    model = train_model(df, "models/temp_model.pkl")
    assert model is not None