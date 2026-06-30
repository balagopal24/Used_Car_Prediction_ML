"""
agent/car_agent.py

A lightweight Gemini-powered agent that:
  1. Answers natural-language questions about the listings DB
     by translating them into SQL and summarizing results.
  2. Flags anomalous listings (large gap between actual and predicted price).

Requires: GEMINI_API_KEY in environment.
Get a free key at: https://aistudio.google.com/apikey
"""
import os
import sys
import json
from google import genai
from google.genai import types

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "db"))
from init_db import get_connection  # noqa: E402

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-2.5-flash"

SCHEMA_DESCRIPTION = """
Table: listings
Columns: id, source, brand, model, year, km_driven, fuel_type, transmission,
         owner, engine_cc, mileage_kmpl, seats, price_actual, price_predicted,
         ingested_at
"""

SQL_SYSTEM_PROMPT = f"""You translate natural-language questions about a used-car
listings database into a single read-only PostgreSQL SELECT query.

{SCHEMA_DESCRIPTION}

Rules:
- Output ONLY the SQL query, no explanation, no markdown fences.
- Never write INSERT/UPDATE/DELETE/DROP statements.
- Always include a LIMIT clause (max 50) unless the question asks for an aggregate.
"""


def _generate_sql(question: str) -> str:
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=question,
        config=types.GenerateContentConfig(
            system_instruction=SQL_SYSTEM_PROMPT,
            temperature=0,
            max_output_tokens=300,
        ),
    )
    sql = response.text.strip().strip("`").strip()
    if sql.lower().startswith("sql"):
        sql = sql[3:].strip()
    if not sql.lower().startswith("select"):
        raise ValueError(f"Refused unsafe or invalid query: {sql}")
    return sql


def _run_query(sql: str):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            cols = [desc[0] for desc in cur.description]
        return [dict(zip(cols, r)) for r in rows]
    finally:
        conn.close()


def answer_question(question: str) -> str:
    sql = _generate_sql(question)
    results = _run_query(sql)

    summary_prompt = (
        f"Question: {question}\n"
        f"SQL used: {sql}\n"
        f"Query results (JSON): {json.dumps(results, default=str)[:4000]}\n\n"
        "Summarize the answer in 2-3 plain-English sentences."
    )
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=summary_prompt,
        config=types.GenerateContentConfig(max_output_tokens=300),
    )
    return response.text.strip()


def flag_anomalies(threshold_pct: float = 25.0):
    """Flags listings where |actual - predicted| / actual exceeds threshold_pct."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, price_actual, price_predicted
                FROM listings
                WHERE price_actual IS NOT NULL AND price_predicted IS NOT NULL
                  AND ABS(price_actual - price_predicted) / price_actual * 100 > %s
            """, (threshold_pct,))
            anomalies = cur.fetchall()
        for listing_id, actual, predicted in anomalies:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO prediction_log
                        (listing_id, model_version, predicted_price, residual, is_anomaly)
                    VALUES (%s, %s, %s, %s, TRUE)
                    """,
                    (listing_id, "v1-linear-regression-gemini", predicted, actual - predicted),
                )
        conn.commit()
        return len(anomalies)
    finally:
        conn.close()


if __name__ == "__main__":
    print(answer_question("What is the average price of diesel SUVs?"))
