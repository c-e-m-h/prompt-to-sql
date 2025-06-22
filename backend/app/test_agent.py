# test_agent.py
# Basic unit tests for the agent logic
import os
import sys
import pytest

pytest.importorskip("httpx")

sys.path.append(os.path.dirname(__file__))
from agent import prompt_to_sql

def test_prompt_to_sql():
    sql = prompt_to_sql("Show me all customers")
    assert sql.strip().lower().startswith("select"), f"Agent did not return a SELECT: {sql}"
    print("Agent SELECT test passed.")

    sql2 = prompt_to_sql("")
    assert "Please clarify your question" in sql2, f"Agent did not return fallback for empty prompt: {sql2}"
    print("Agent fallback test passed.")

if __name__ == "__main__":
    test_prompt_to_sql()
