# test_api.py
# Basic unit tests for the FastAPI API
from fastapi.testclient import TestClient
from main import app

def test_root():
    client = TestClient(app)
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "Anysoft SQL Demo API"}
    print("Root endpoint test passed.")

def test_query():
    client = TestClient(app)
    resp = client.post("/query", json={"prompt": "Show me all customers"})
    assert resp.status_code == 200
    data = resp.json()
    assert "table" in data
    assert isinstance(data["table"], list)
    print("Query endpoint test passed.")

if __name__ == "__main__":
    test_root()
    test_query() 