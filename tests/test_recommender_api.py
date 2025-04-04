import requests
def test_recommendation_api_response():
    user_id = 42  
    response = requests.get(f"https://mlip-project.onrender.com/recommend/{user_id}")
     
    assert response.status_code == 200
    result = response.text.split(",")
     
    assert len(result) == 20 
    assert all(r.isdigit() for r in result)