from surprise import accuracy
from surprise.model_selection import train_test_split
from surprise import Dataset, Reader

def evaluate_model(df, model):
    reader = Reader(rating_scale=(0.5, 5.0))
    data = Dataset.load_from_df(df[['user_id', 'movie_id', 'rating']], reader)
    trainset, testset = train_test_split(data, test_size=0.2)

    model.fit(trainset)
    predictions = model.test(testset)

    rmse = accuracy.rmse(predictions)
    mae = accuracy.mae(predictions)

    return rmse, mae