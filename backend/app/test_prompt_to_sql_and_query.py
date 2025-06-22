import os
import sys
import pytest

pytest.importorskip("httpx")

sys.path.append(os.path.dirname(__file__))
from agent import prompt_to_sql
from db import SessionLocal
from sqlalchemy import text
import pandas as pd

def test_prompt_to_sql_and_query():
    # Test: Agent returns a SELECT for a supported prompt
    prompt = "Show me all customers"
    sql = prompt_to_sql(prompt)
    assert sql.strip().lower().startswith("select"), f"Agent did not return a SELECT: {sql}"
    with SessionLocal() as db:
        result = db.execute(text(sql))
        rows = result.fetchall()
        assert isinstance(rows, list)
    print("Prompt-to-SQL and data retrieval test passed.")

    # Test: Agent returns fallback for empty prompt
    sql2 = prompt_to_sql("")
    assert "Please clarify your question" in sql2, f"Agent did not return fallback for empty prompt: {sql2}"
    print("Agent fallback test passed.")

def test_table_output_with_pandas():
    sql = "SELECT * FROM customers LIMIT 5;"
    with SessionLocal() as db:
        df = pd.read_sql(sql, db.bind)
        assert df.shape[0] == 5
        assert "id" in df.columns
    print("Pandas table output test passed.")

if __name__ == "__main__":
    test_prompt_to_sql_and_query()
    test_table_output_with_pandas() 