# sample_queries.py
# Add sample queries and unit tests for the backend
from db import SessionLocal
from sqlalchemy import text

def test_db_connection():
    try:
        with SessionLocal() as db:
            result = db.execute(text("SELECT 1")).scalar()
            assert result == 1
        print("DB connection test passed.")
    except Exception as e:
        print(f"DB connection test failed: {e}")

def test_sample_query():
    try:
        with SessionLocal() as db:
            result = db.execute(text("SELECT COUNT(*) FROM customers")).scalar()
            print(f"Customer count: {result}")
    except Exception as e:
        print(f"Sample query failed: {e}")

if __name__ == "__main__":
    test_db_connection()
    test_sample_query()

# TODO: Implement sample queries and tests 