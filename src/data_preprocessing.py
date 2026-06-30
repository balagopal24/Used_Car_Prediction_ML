# """
# src/data_preprocessing.py
# Cleans the raw used-car dataset (Kaggle CarDekho-derived CSV).
# Expected raw columns: name, year, selling_price, km_driven, fuel,
# seller_type, transmission, owner, mileage, engine, max_power, seats
# """
# import re
# import pandas as pd

# NUMERIC_PATTERN = re.compile(r"[-+]?\d*\.?\d+")


# def _extract_number(value):
#     if pd.isna(value):
#         return None
#     match = NUMERIC_PATTERN.search(str(value))
#     return float(match.group()) if match else None


# def load_raw(path: str) -> pd.DataFrame:
#     return pd.read_csv(path)


# def clean(df: pd.DataFrame) -> pd.DataFrame:
#     df = df.copy()

#     # Split "name" -> brand, model
#     df["brand"] = df["name"].str.split().str[0]
#     df["model"] = df["name"].str.split(n=1).str[1]

#     # Strip units, coerce to numeric
#     for col in ["mileage", "engine", "max_power"]:
#         if col in df.columns:
#             df[col] = df[col].apply(_extract_number)

#     df["engine_cc"] = df.get("engine")
#     df["mileage_kmpl"] = df.get("mileage")

#     # Drop rows missing the target or core features
#     required = ["selling_price", "year", "km_driven", "fuel", "transmission"]
#     df = df.dropna(subset=[c for c in required if c in df.columns])

#     # Remove obvious outliers
#     df = df[(df["km_driven"] > 0) & (df["km_driven"] < 500_000)]
#     df = df[(df["selling_price"] > 10_000) & (df["selling_price"] < 1.5e7)]
#     df = df[(df["year"] >= 1990) & (df["year"] <= 2026)]

#     df = df.drop_duplicates()
#     return df.reset_index(drop=True)


# if __name__ == "__main__":
#     raw = load_raw("data/raw/cardekho_dataset.csv")
#     cleaned = clean(raw)
#     cleaned.to_csv("data/processed/cleaned_listings.csv", index=False)
#     print(f"Cleaned dataset shape: {cleaned.shape}")


"""
src/data_preprocessing.py
Cleans the raw used-car dataset.

Expected raw columns (actual CarDekho Kaggle export):
car_name, brand, model, vehicle_age, km_driven, seller_type, fuel_type,
transmission_type, mileage, engine, max_power, seats, selling_price
"""
import pandas as pd

CURRENT_YEAR = 2026


def load_raw(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Drop the unnamed index column some Kaggle exports include
    if df.columns[0].startswith("Unnamed"):
        df = df.drop(columns=[df.columns[0]])
    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Derive a "year" column from vehicle_age (rest of the pipeline expects "year")
    df["year"] = CURRENT_YEAR - df["vehicle_age"]

    # Normalize naming to match the rest of the codebase
    df = df.rename(columns={
        "fuel_type": "fuel",
        "transmission_type": "transmission",
        "engine": "engine_cc",
        "mileage": "mileage_kmpl",
    })

    # Coerce numerics defensively (in case of stray text/units)
    numeric_cols = ["km_driven", "selling_price", "year", "engine_cc",
                     "mileage_kmpl", "max_power", "seats"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    required = ["selling_price", "year", "km_driven", "fuel", "transmission"]
    df = df.dropna(subset=[c for c in required if c in df.columns])

    # Remove obvious outliers
    df = df[(df["km_driven"] > 0) & (df["km_driven"] < 500_000)]
    df = df[(df["selling_price"] > 10_000) & (df["selling_price"] < 1.5e7)]
    df = df[(df["year"] >= 1990) & (df["year"] <= CURRENT_YEAR)]

    df = df.drop_duplicates()
    return df.reset_index(drop=True)


if __name__ == "__main__":
    raw = load_raw("data/raw/cardekho_dataset.csv")
    cleaned = clean(raw)
    cleaned.to_csv("data/processed/cleaned_listings.csv", index=False)
    print(f"Cleaned dataset shape: {cleaned.shape}")
    print(cleaned.head())