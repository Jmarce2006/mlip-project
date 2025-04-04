## 🚀 MLIP Project – Recommender System API

This repository contains the implementation of a movie recommender system developed for the **MLIP (Machine Learning in Practice)** course. The project includes data processing, model training, evaluation, and deployment of a REST API using **Flask**.

---

### 📈 Overview

#### Requirements & Setup
- Defined the scope of the project and functional goals.
- Set up the repository structure (`src/`, `tests/`, `data/`, etc.).
- Created the API using **Flask** to serve recommendations.
- Created `requirements.txt` and `pytest.ini` files.
- Wrote and tested unit tests for key modules: data loading, model training, and evaluation.

#### Model Training & Evaluation
- Implemented collaborative filtering using **Scikit-Surprise**.
- Trained a **KNNBasic** model with user-item rating data.
- Generated the top 20 recommendations for each user.
- Evaluated the model by calculating the **average rating of the 20 recommendations per user**.
- Automated testing and linting using **GitHub Actions** CI workflow.

### 📊 Recommendation Model

For this milestone, a recommendation system was implemented using **SVD (Singular Value Decomposition)** with the `scikit-surprise` library. The model was trained on the processed dataset and evaluated using a custom metric.

### 🔍 Evaluation Metric

The evaluation metric used was the **average predicted rating** for the top 20 recommendations generated for each user. This approach provides a general idea of the quality of the predictions, instead of using Hit@10.

### 🛠️ Implementation

- Library: `scikit-surprise`
- Algorithm: `SVD`
- Metric: Average of predicted `rating` values in the top-20 recommendations per user



#### Deployment
- Deployed the API to a public platform using **Render.com**.
- Integrated continuous deployment (CD) via GitHub.
- API is now publicly accessible for test queries and recommendations.
- Created a working endpoint: `/recommend/<user_id>`

---

### 🧪 Testing

Run the tests using:

```bash
pytest
