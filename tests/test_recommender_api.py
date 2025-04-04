import requests

def test_recommendation_api_response():
    user_id = 42  
    response = requests.get(f"http://localhost:8082/recommend/{user_id}")
    
    assert response.status_code == 200
    result = response.text.split(",")
    
    assert len(result) == 20 
    assert all(r.isdigit() for r in result)
