"""
src/train.py
Trains and compares OLS, Ridge, Lasso, ElasticNet.
Saves the best model + encoder to models/.
"""
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

from feature_engineering import build_feature_matrix

MODELS = {
    "linear": LinearRegression(),
    "ridge": Ridge(alpha=1.0),
    "lasso": Lasso(alpha=0.01),
    "elasticnet": ElasticNet(alpha=0.01, l1_ratio=0.5),
}


def evaluate(model, X_test, y_test_log):
    preds_log = model.predict(X_test)
    preds = np.expm1(preds_log)
    actual = np.expm1(y_test_log)

    return {
        "r2": r2_score(y_test_log, preds_log),
        "rmse": mean_squared_error(actual, preds, squared=False),
        "mae": mean_absolute_error(actual, preds),
    }


def main():
    df = pd.read_csv("data/processed/cleaned_listings.csv")
    X, y, encoder = build_feature_matrix(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    results = {}
    fitted_models = {}
    for name, model in MODELS.items():
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="r2")
        model.fit(X_train, y_train)
        metrics = evaluate(model, X_test, y_test)
        metrics["cv_r2_mean"] = cv_scores.mean()
        results[name] = metrics
        fitted_models[name] = model
        print(f"{name:12s} -> {metrics}")

    best_name = max(results, key=lambda k: results[k]["r2"])
    best_model = fitted_models[best_name]
    print(f"\nBest model: {best_name} ({results[best_name]})")

    joblib.dump(
        {"model": best_model, "encoder": encoder, "feature_columns": list(X.columns)},
        "models/linear_regression_model.pkl",
    )
    print("Saved best model to models/linear_regression_model.pkl")


if __name__ == "__main__":
    main()
