import pandas as pd
import pickle
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


from evaluator import evaluate_model

def test_model_evaluation():
    df = pd.read_csv("data/processed/ratings_with_features.csv")
    with open("models/svd_model.pkl", "rb") as f:
        model = pickle.load(f)
    rmse, mae = evaluate_model(df, model)
    assert rmse > 0
    assert mae > 0