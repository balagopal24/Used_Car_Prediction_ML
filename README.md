# 🚗 Used Car Price Prediction — Real-Time Pipeline (Linear Regression + Agent + API)

An end-to-end ML system that predicts used car resale prices using linear
regression (with Ridge/Lasso/ElasticNet comparison), served through a
FastAPI backend, with a simulated real-time ingestion pipeline, a
Gemini-powered natural-language query agent, and a live Streamlit dashboard.

## Why "simulated" real-time, and why that's okay

Scraping live data from used-car marketplaces (CarDekho, Cars24, OLX) was
considered for this project, but their Terms of Use explicitly prohibit
automated scraping — common for listing/classifieds sites since the data
itself is their core business asset. Building this project on scraped data
in violation of ToS isn't something this repo does.

Instead, this project uses a legally-distributed, open dataset and simulates
a live feed by dripping rows into PostgreSQL at randomized intervals —
**the same pattern used to test real Kafka/streaming pipelines in
development.** The API, agent, and dashboard all read from the database
with no knowledge of how it was populated, so the architecture is
identical to a true real-time system; only the producer is swapped for a
production data source (e.g. a licensed API) in a real deployment.

## Architecture

```
 [simulator.py] --inserts--> [PostgreSQL] <--reads-- [FastAPI] <--queries-- [Streamlit UI]
                                   ^                     |
                                   |                     v
                          [car_agent.py] <---- /ask endpoint (Gemini NL->SQL)
```

## Project Structure

```
used-car-price-prediction/
├── db/                  # schema.sql, connection helper
├── data/                # raw + processed dataset
├── src/                 # preprocessing, feature engineering, training, evaluation, simulator
├── agent/               # Gemini-powered NL→SQL agent + anomaly flagging
├── app/                 # FastAPI service
├── frontend/            # Streamlit live dashboard
├── models/               # saved model + diagnostics
├── tests/                # pytest suite
├── docker-compose.yml
└── Dockerfile
```

## What this project demonstrates

1. **EDA & data cleaning** — outlier handling, unit parsing from messy text fields
2. **Feature engineering** — car age, log-transforms, one-hot encoding
3. **Linear regression assumption checks** — VIF for multicollinearity,
   residual/Q-Q plots, Breusch-Pagan test for homoscedasticity
4. **Model comparison** — OLS vs Ridge vs Lasso vs ElasticNet with 5-fold CV
5. **Production-style serving** — FastAPI with Pydantic validation
6. **Simulated streaming ingestion** — a standard dev/test pattern for
   pipelines that will later connect to a true real-time source
7. **LLM agent integration** — natural-language questions translated to
   SQL and summarized (read-only, injection-guarded)
8. **Live dashboard** — Streamlit UI showing the feed, predictions, and
   agent Q&A

## Setup

### 1. Get the dataset
Download the CarDekho used-car dataset from Kaggle (openly licensed for ML use)
and place it at `data/raw/cardekho_dataset.csv`.

### 2. Install dependencies
```bash
python -m venv venv && source venv/bin/activate   # or `.\venv\Scripts\activate` on Windows
pip install -r requirements.txt
cp .env.example .env   # then fill in your GEMINI_API_KEY
```

### 3. Start Postgres
```bash
docker compose up -d postgres
python db/init_db.py
```

### 4. Run the ML pipeline
```bash
python src/data_preprocessing.py
python src/train.py
python src/evaluate.py     # generates models/residual_plot.png
```

### 5. Start the simulator, API, and dashboard (3 terminals)
```bash
python src/simulator.py
uvicorn app.main:app --reload
streamlit run frontend/streamlit_app.py
```

Visit `http://localhost:8501` for the dashboard and `http://localhost:8000/docs`
for the interactive API docs.

### 6. Run tests
```bash
pytest tests/
```

## Results

| Model       | R² (log price) | RMSE (₹) | MAE (₹) |
|-------------|-----------------|----------|---------|
| Linear      | _fill in_       | _fill in_| _fill in_|
| Ridge       | _fill in_       | _fill in_| _fill in_|
| Lasso       | _fill in_       | _fill in_| _fill in_|
| ElasticNet  | _fill in_       | _fill in_| _fill in_|

(Run `src/train.py` to populate this table with your actual results.)

## Future improvements
- Swap the simulator for a licensed real-time automotive data API
- Add a tree-based model (XGBoost/LightGBM) for comparison
- Add SHAP-based feature importance to the dashboard
- Deploy via Railway/Fly.io with a managed Postgres instance

## License
MIT — see LICENSE file. Dataset license follows its original Kaggle source.
