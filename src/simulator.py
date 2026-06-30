"""
src/simulator.py

Mimics a real-time data feed by inserting rows from the static, legally-
sourced dataset into Postgres at random intervals — the same pattern used
to test real Kafka/streaming pipelines in development.

Run this as a background process:
    python src/simulator.py
"""
import os
import sys
import time
import random
import joblib
import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "db"))

from feature_engineering import build_feature_matrix  # noqa: E402
from init_db import get_connection  # noqa: E402

DATA_PATH = "data/processed/cleaned_listings.csv"
MODEL_PATH = "models/linear_regression_model.pkl"
MIN_DELAY_SEC = 3
MAX_DELAY_SEC = 10
SOURCE_TAG = "simulated_feed"


def insert_listing(conn, row: pd.Series, predicted_price: float):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO listings
                (source, brand, model, year, km_driven, fuel_type,
                 transmission, owner, engine_cc, mileage_kmpl, seats,
                 price_actual, price_predicted)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                SOURCE_TAG,
                row.get("brand"),
                row.get("model"),
                int(row.get("year")) if pd.notna(row.get("year")) else None,
                int(row.get("km_driven")) if pd.notna(row.get("km_driven")) else None,
                row.get("fuel"),
                row.get("transmission"),
                row.get("owner"),
                int(row.get("engine_cc")) if pd.notna(row.get("engine_cc")) else None,
                float(row.get("mileage_kmpl")) if pd.notna(row.get("mileage_kmpl")) else None,
                int(row.get("seats")) if pd.notna(row.get("seats")) else None,
                float(row.get("selling_price")),
                float(predicted_price),
            ),
        )
        listing_id = cur.fetchone()[0]
    conn.commit()
    return listing_id


def run():
    df = pd.read_csv(DATA_PATH)
    bundle = joblib.load(MODEL_PATH)
    model, encoder = bundle["model"], bundle["encoder"]

    conn = get_connection()
    print(f"Simulator started. Streaming from {len(df)} rows. Ctrl+C to stop.")

    try:
        while True:
            row = df.sample(1).iloc[0]
            X, _, _ = build_feature_matrix(pd.DataFrame([row]), encoder=encoder)
            X = X.reindex(columns=bundle["feature_columns"], fill_value=0)
            pred_log = model.predict(X)[0]
            predicted_price = float(np.expm1(pred_log))

            listing_id = insert_listing(conn, row, predicted_price)
            print(f"[+] Inserted listing #{listing_id}: "
                  f"{row.get('brand')} {row.get('model')} -> "
                  f"actual ₹{row.get('selling_price'):,.0f}, "
                  f"predicted ₹{predicted_price:,.0f}")

            time.sleep(random.uniform(MIN_DELAY_SEC, MAX_DELAY_SEC))
    except KeyboardInterrupt:
        print("\nSimulator stopped.")
    finally:
        conn.close()


if __name__ == "__main__":
    run()
