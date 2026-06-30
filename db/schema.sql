-- Used Car Price Prediction: Database Schema

CREATE TABLE IF NOT EXISTS listings (
    id SERIAL PRIMARY KEY,
    source VARCHAR(50) NOT NULL DEFAULT 'simulated_feed',
    brand VARCHAR(50),
    model VARCHAR(100),
    year INT,
    km_driven INT,
    fuel_type VARCHAR(30),
    transmission VARCHAR(20),
    owner VARCHAR(30),
    engine_cc INT,
    mileage_kmpl FLOAT,
    seats INT,
    price_actual NUMERIC(12, 2),       -- actual listed price (from dataset)
    price_predicted NUMERIC(12, 2),    -- model's predicted price
    ingested_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_listings_ingested_at ON listings (ingested_at DESC);
CREATE INDEX IF NOT EXISTS idx_listings_brand ON listings (brand);

CREATE TABLE IF NOT EXISTS prediction_log (
    id SERIAL PRIMARY KEY,
    listing_id INT REFERENCES listings(id),
    model_version VARCHAR(50),
    predicted_price NUMERIC(12, 2),
    residual NUMERIC(12, 2),           -- actual - predicted (NULL if no actual)
    is_anomaly BOOLEAN DEFAULT FALSE,  -- flagged by agent if residual is extreme
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
