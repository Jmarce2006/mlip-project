from flask import Flask
from surprise import SVD
import pandas as pd
import pickle
from datetime import datetime
from kafka import KafkaProducer
import json
import time
import socket
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Kafka producer as None
producer = None
KAFKA_TOPIC = 'recommender_api_logs'

# Try to setup Kafka producer
try:
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    logger.info("Successfully connected to Kafka")
except Exception as e:
    logger.warning(f"Failed to connect to Kafka: {str(e)}. Logging to Kafka will be disabled.")

# Load the model
model = pickle.load(open("models/svd_model.pkl", "rb"))

# Load user ratings
ratings = pd.read_csv("data/processed/ratings_with_features.csv")

# Get list of all movie IDs
all_movie_ids = ratings['movie_id'].unique()

@app.route('/recommend/<int:user_id>', methods=['GET'])
def recommend(user_id):
    start_time = time.time()
    try:
        # Movies the user has already rated
        seen = ratings[ratings['user_id'] == user_id]['movie_id'].values
        unseen = [m for m in all_movie_ids if m not in seen]

        # Predict ratings for unseen movies
        predictions = [model.predict(user_id, m) for m in unseen]

        # Sort predictions by estimated rating
        top_20 = sorted(predictions, key=lambda x: x.est, reverse=True)[:20]

        # Return comma-separated movie IDs
        top_ids = [str(pred.iid) for pred in top_20]
        
        # Create Kafka log message
        log_message = {
            "time": datetime.utcnow().isoformat(),
            "userid": user_id,
            "server": socket.gethostname(),
            "status": 200,
            "result": top_ids,
            "responsetime": round((time.time() - start_time) * 1000, 2)  # in ms
        }

        # Send to Kafka only if producer is available
        if producer is not None:
            try:
                producer.send(KAFKA_TOPIC, log_message)
            except Exception as e:
                logger.error(f"Failed to send message to Kafka: {str(e)}")
        
        return ",".join(top_ids), 200

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
