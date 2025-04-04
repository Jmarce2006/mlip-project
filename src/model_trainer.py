import pickle
from surprise import Dataset, Reader, SVD

def train_model(df, model_path):
    reader = Reader(rating_scale=(0.5, 5.0))
    data = Dataset.load_from_df(df[['user_id', 'movie_id', 'rating']], reader)
    trainset = data.build_full_trainset()

    model = SVD()
    model.fit(trainset)

    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    return model
