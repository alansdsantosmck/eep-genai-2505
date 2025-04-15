from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_match_endpoint():
    response = client.post("/match", json={
        "job": {
            "cst_name": "Acme Inc",
            "client_problem_statement": "Need a backend engineer to optimize data pipeline performance.",
            "title": "Senior Backend Engineer",
            "location": "New York",
            "industry": "Tech",
            "required_skills": "Python, FastAPI, PostgreSQL, Data Pipelines",
            "years_experience": 5
        }
    })
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert "full_name" in response.json()[0]