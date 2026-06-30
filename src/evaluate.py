"""
src/evaluate.py
Linear regression assumption checks: multicollinearity (VIF),
residual plots, homoscedasticity (Breusch-Pagan).
"""
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan
import statsmodels.api as sm

from feature_engineering import build_feature_matrix


def compute_vif(X: pd.DataFrame) -> pd.DataFrame:
    vif_data = pd.DataFrame()
    vif_data["feature"] = X.columns
    vif_data["VIF"] = [
        variance_inflation_factor(X.values, i) for i in range(X.shape[1])
    ]
    return vif_data.sort_values("VIF", ascending=False)


def residual_diagnostics(model, X_test, y_test, out_path="models/residual_plot.png"):
    preds = model.predict(X_test)
    residuals = y_test - preds

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].scatter(preds, residuals, alpha=0.4)
    axes[0].axhline(0, color="red", linestyle="--")
    axes[0].set_xlabel("Predicted (log price)")
    axes[0].set_ylabel("Residual")
    axes[0].set_title("Residuals vs Predicted")

    sm.qqplot(residuals, line="45", ax=axes[1])
    axes[1].set_title("Q-Q Plot of Residuals")

    plt.tight_layout()
    plt.savefig(out_path)
    print(f"Saved residual diagnostics to {out_path}")

    X_test_const = sm.add_constant(X_test)
    bp_test = het_breuschpagan(residuals, X_test_const)
    print(f"Breusch-Pagan p-value (homoscedasticity test): {bp_test[1]:.4f}")
    if bp_test[1] < 0.05:
        print("  -> Evidence of heteroscedasticity (residual variance not constant)")
    else:
        print("  -> No strong evidence against homoscedasticity")


if __name__ == "__main__":
    bundle = joblib.load("models/linear_regression_model.pkl")
    df = pd.read_csv("data/processed/cleaned_listings.csv")
    X, y, _ = build_feature_matrix(df, encoder=bundle["encoder"])

    print("Variance Inflation Factors (VIF > 10 suggests multicollinearity):")
    print(compute_vif(X[bundle["feature_columns"]]).head(10))

    residual_diagnostics(bundle["model"], X, y)
