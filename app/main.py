# """
# app/main.py
# FastAPI service: predictions + live listing feed + agent Q&A.

# Run with: uvicorn app.main:app --reload
# """
# import sys
# import os
# import joblib
# import numpy as np
# import pandas as pd
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware

# sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
# sys.path.append(os.path.join(os.path.dirname(__file__), "..", "db"))
# sys.path.append(os.path.join(os.path.dirname(__file__), "..", "agent"))

# from feature_engineering import build_feature_matrix  # noqa: E402
# from init_db import get_connection  # noqa: E402
# from schemas import CarFeatures, PredictionResponse, ListingOut  # noqa: E402

# app = FastAPI(title="Used Car Price Prediction API", version="1.0")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# MODEL_PATH = "models/linear_regression_model.pkl"
# _bundle = None


# def get_bundle():
#     global _bundle
#     if _bundle is None:
#         _bundle = joblib.load(MODEL_PATH)
#     return _bundle


# @app.get("/health")
# def health():
#     return {"status": "ok"}


# @app.post("/predict", response_model=PredictionResponse)
# def predict(car: CarFeatures):
#     bundle = get_bundle()
#     row = pd.DataFrame([car.dict()])
#     # selling_price isn't present here; feature builder only needs it for y
#     X, _, _ = build_feature_matrix(row, encoder=bundle["encoder"])
#     X = X.reindex(columns=bundle["feature_columns"], fill_value=0)

#     pred_log = bundle["model"].predict(X)[0]
#     predicted_price = float(np.expm1(pred_log))
#     return PredictionResponse(predicted_price=round(predicted_price, 2))


# @app.get("/listings/recent", response_model=list[ListingOut])
# def recent_listings(limit: int = 20):
#     conn = get_connection()
#     try:
#         with conn.cursor() as cur:
#             cur.execute(
#                 """
#                 SELECT id, brand, model, year, km_driven, fuel_type,
#                        price_actual, price_predicted, ingested_at
#                 FROM listings
#                 ORDER BY ingested_at DESC
#                 LIMIT %s
#                 """,
#                 (limit,),
#             )
#             rows = cur.fetchall()
#             cols = [desc[0] for desc in cur.description]
#         return [dict(zip(cols, [str(v) if i == len(cols) - 1 else v
#                                  for i, v in enumerate(r)])) for r in rows]
#     finally:
#         conn.close()


# @app.get("/stats")
# def stats():
#     conn = get_connection()
#     try:
#         with conn.cursor() as cur:
#             cur.execute("""
#                 SELECT brand,
#                        COUNT(*) AS n,
#                        AVG(price_actual) AS avg_price,
#                        AVG(ABS(price_actual - price_predicted)) AS avg_abs_error
#                 FROM listings
#                 GROUP BY brand
#                 ORDER BY n DESC
#                 LIMIT 10
#             """)
#             rows = cur.fetchall()
#             cols = [desc[0] for desc in cur.description]
#         return [dict(zip(cols, r)) for r in rows]
#     finally:
#         conn.close()


# @app.post("/ask")
# def ask(question: str):
#     """Natural-language Q&A over the listings DB, powered by the agent."""
#     try:
#         from car_agent import answer_question
#     except ImportError:
#         raise HTTPException(status_code=501, detail="Agent module not configured.")
#     return {"answer": answer_question(question)}


"""
app/main.py
FastAPI service: predictions + live listing feed + agent Q&A.

Run with: uvicorn app.main:app --reload
"""
import sys
import os
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "db"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "agent"))

from feature_engineering import build_feature_matrix  # noqa: E402
from init_db import get_connection  # noqa: E402
from .schemas import CarFeatures, PredictionResponse, ListingOut  # noqa: E402

app = FastAPI(title="Used Car Price Prediction API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "models/linear_regression_model.pkl"
_bundle = None


def get_bundle():
    global _bundle
    if _bundle is None:
        _bundle = joblib.load(MODEL_PATH)
    return _bundle


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(car: CarFeatures):
    bundle = get_bundle()
    row = pd.DataFrame([car.dict()])
    # selling_price isn't present here; feature builder only needs it for y
    X, _, _ = build_feature_matrix(row, encoder=bundle["encoder"])
    X = X.reindex(columns=bundle["feature_columns"], fill_value=0)

    pred_log = bundle["model"].predict(X)[0]
    predicted_price = float(np.expm1(pred_log))
    return PredictionResponse(predicted_price=round(predicted_price, 2))


@app.get("/listings/recent", response_model=list[ListingOut])
def recent_listings(limit: int = 20):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, brand, model, year, km_driven, fuel_type,
                       price_actual, price_predicted, ingested_at
                FROM listings
                ORDER BY ingested_at DESC
                LIMIT %s
                """,
                (limit,),
            )
            rows = cur.fetchall()
            cols = [desc[0] for desc in cur.description]
        return [dict(zip(cols, [str(v) if i == len(cols) - 1 else v
                                 for i, v in enumerate(r)])) for r in rows]
    finally:
        conn.close()


@app.get("/stats")
def stats():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT brand,
                       COUNT(*) AS n,
                       AVG(price_actual) AS avg_price,
                       AVG(ABS(price_actual - price_predicted)) AS avg_abs_error
                FROM listings
                GROUP BY brand
                ORDER BY n DESC
                LIMIT 10
            """)
            rows = cur.fetchall()
            cols = [desc[0] for desc in cur.description]
        return [dict(zip(cols, r)) for r in rows]
    finally:
        conn.close()


@app.post("/ask")
def ask(question: str):
    """Natural-language Q&A over the listings DB, powered by the agent."""
    try:
        from car_agent import answer_question
    except ImportError:
        raise HTTPException(status_code=501, detail="Agent module not configured.")
    return {"answer": answer_question(question)}