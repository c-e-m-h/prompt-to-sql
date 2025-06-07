# agent.py
# Logic for converting natural language prompts to SQL using OpenAI

import os
import openai
import logging
import re

openai.api_key = os.getenv("OPENAI_API_KEY")
logging.basicConfig(level=logging.DEBUG)

def extract_sql_from_response(response_content: str) -> str:
    code_block = re.search(r"```(?:sql)?\s*([\s\S]*?)```", response_content, re.IGNORECASE)
    if code_block:
        return code_block.group(1).strip()
    return response_content.strip()

def prompt_to_sql(prompt: str, max_tokens: int = 256, temperature: float = 0.0) -> str:
    """
    Converts a natural language prompt to a SQL query using OpenAI's GPT-4.1-mini model.
    Returns a default message if the prompt is unsupported or empty.
    """
    if not prompt.strip():
        logging.warning("Prompt is empty or whitespace.")
        return "SELECT 'Please clarify your question.' AS message;"

    system_message = (
        "You are an expert SQL analyst with up-to-date knowledge of PostgreSQL. "
        "Given a user's question and the following database schema, generate a syntactically correct SQL query for PostgreSQL. "
        "Return only the SQL query, no explanation.\n"
        "\n"
        "Schema:\n"
        "Table customers: id (int), name (text), state (text)\n"
        "Table products: id (int), name (text), category (text), launch_date (date)\n"
        "Table orders: id (int), customer_id (int), product_id (int), order_date (date), amount (numeric), status (text)\n"
        "\n"
        "The database is PostgreSQL. Use PostgreSQL SQL syntax."
    )

    try:
        logging.debug(f"Prompt sent to OpenAI: {prompt}")
        response = openai.chat.completions.create(
            model="gpt-4.1-mini",  # or your correct model name
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        logging.debug(f"OpenAI API raw response: {response}")
        sql = extract_sql_from_response(response.choices[0].message.content)
        logging.debug(f"Generated SQL: {sql}")
        # TEMP: Do not enforce SELECT-only for debugging
        return sql
    except Exception as e:
        logging.error(f"Error generating SQL: {e}")
        return "SELECT 'Please clarify your question.' AS message;"
