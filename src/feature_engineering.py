# # # """
# # # src/feature_engineering.py
# # # Builds model-ready features from cleaned listings.
# # # """
# # # import numpy as np
# # # import pandas as pd
# # # from sklearn.preprocessing import OneHotEncoder


# # # CURRENT_YEAR = 2026
# # # CATEGORICAL_COLS = ["brand", "fuel", "transmission", "owner", "seller_type"]
# # # NUMERIC_COLS = ["car_age", "km_driven", "engine_cc", "mileage_kmpl", "seats"]


# # # def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
# # #     df = df.copy()
# # #     df["car_age"] = CURRENT_YEAR - df["year"]
# # #     df["log_price"] = np.log1p(df["selling_price"])
# # #     df["log_km_driven"] = np.log1p(df["km_driven"])
# # #     return df


# # # def build_feature_matrix(df: pd.DataFrame, encoder: OneHotEncoder = None):
# # #     """Returns (X, y, fitted_encoder). Pass a fitted encoder at inference time."""
# # #     df = add_derived_features(df)

# # #     cat_cols = [c for c in CATEGORICAL_COLS if c in df.columns]
# # #     num_cols = [c for c in NUMERIC_COLS if c in df.columns]

# # #     if encoder is None:
# # #         encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
# # #         cat_encoded = encoder.fit_transform(df[cat_cols])
# # #     else:
# # #         cat_encoded = encoder.transform(df[cat_cols])

# # #     cat_df = pd.DataFrame(
# # #         cat_encoded, columns=encoder.get_feature_names_out(cat_cols), index=df.index
# # #     )
# # #     X = pd.concat([df[num_cols].fillna(0), cat_df], axis=1)
# # #     y = df["log_price"] if "selling_price" in df.columns else None

# # #     return X, y, encoder

# # """
# # src/feature_engineering.py
# # Builds model-ready features from cleaned listings.
# # """
# # import numpy as np
# # import pandas as pd
# # from sklearn.preprocessing import OneHotEncoder


# # CURRENT_YEAR = 2026
# # CATEGORICAL_COLS = ["brand", "fuel", "transmission", "owner", "seller_type"]
# # NUMERIC_COLS = ["car_age", "km_driven", "engine_cc", "mileage_kmpl", "seats"]


# # def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
# #     df = df.copy()
# #     df["car_age"] = CURRENT_YEAR - df["year"]
# #     df["log_price"] = np.log1p(df["selling_price"])
# #     df["log_km_driven"] = np.log1p(df["km_driven"])
# #     return df


# # def build_feature_matrix(df: pd.DataFrame, encoder: OneHotEncoder = None):
# #     """Returns (X, y, fitted_encoder). Pass a fitted encoder at inference time."""
# #     df = add_derived_features(df)

# #     cat_cols = [c for c in CATEGORICAL_COLS if c in df.columns]
# #     num_cols = [c for c in NUMERIC_COLS if c in df.columns]

# #     if encoder is None:
# #         encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False, drop = "first")
# #         cat_encoded = encoder.fit_transform(df[cat_cols])
# #     else:
# #         cat_encoded = encoder.transform(df[cat_cols])

# #     cat_df = pd.DataFrame(
# #         cat_encoded, columns=encoder.get_feature_names_out(cat_cols), index=df.index
# #     )
# #     X = pd.concat([df[num_cols].fillna(0), cat_df], axis=1)
# #     y = df["log_price"] if "selling_price" in df.columns else None

# #     return X, y, encoder


# """
# src/feature_engineering.py
# Builds model-ready features from cleaned listings.
# """
# import numpy as np
# import pandas as pd
# from sklearn.preprocessing import OneHotEncoder


# CURRENT_YEAR = 2026
# CATEGORICAL_COLS = ["brand", "fuel", "transmission", "owner", "seller_type"]
# NUMERIC_COLS = ["car_age", "km_driven", "engine_cc", "mileage_kmpl", "seats"]


# def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
#     df = df.copy()
#     df["car_age"] = CURRENT_YEAR - df["year"]
#     df["log_price"] = np.log1p(df["selling_price"])
#     df["log_km_driven"] = np.log1p(df["km_driven"])
#     return df


# def build_feature_matrix(df: pd.DataFrame, encoder: OneHotEncoder = None):
#     """Returns (X, y, fitted_encoder). Pass a fitted encoder at inference time."""
#     df = add_derived_features(df)

#     cat_cols = [c for c in CATEGORICAL_COLS if c in df.columns]
#     num_cols = [c for c in NUMERIC_COLS if c in df.columns]

#     if encoder is None:
#         encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False, drop="first")
#         cat_encoded = encoder.fit_transform(df[cat_cols])
#     else:
#         cat_encoded = encoder.transform(df[cat_cols])

#     cat_df = pd.DataFrame(
#         cat_encoded, columns=encoder.get_feature_names_out(cat_cols), index=df.index
#     )
#     X = pd.concat([df[num_cols].fillna(0), cat_df], axis=1)
#     y = df["log_price"] if "selling_price" in df.columns else None

#     return X, y, encoder


"""
src/feature_engineering.py
Builds model-ready features from cleaned listings.
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder


CURRENT_YEAR = 2026
CATEGORICAL_COLS = ["brand", "fuel", "transmission", "seller_type"]
NUMERIC_COLS = ["car_age", "km_driven", "engine_cc", "mileage_kmpl", "seats"]


def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["car_age"] = CURRENT_YEAR - df["year"]
    if "selling_price" in df.columns:
        df["log_price"] = np.log1p(df["selling_price"])
    if "km_driven" in df.columns:
        df["log_km_driven"] = np.log1p(df["km_driven"])
    return df


def build_feature_matrix(df: pd.DataFrame, encoder: OneHotEncoder = None):
    """Returns (X, y, fitted_encoder). Pass a fitted encoder at inference time."""
    df = add_derived_features(df)

    cat_cols = [c for c in CATEGORICAL_COLS if c in df.columns]
    num_cols = [c for c in NUMERIC_COLS if c in df.columns]

    if encoder is None:
        encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False, drop="first")
        cat_encoded = encoder.fit_transform(df[cat_cols])
    else:
        cat_encoded = encoder.transform(df[cat_cols])

    cat_df = pd.DataFrame(
        cat_encoded, columns=encoder.get_feature_names_out(cat_cols), index=df.index
    )
    X = pd.concat([df[num_cols].fillna(0), cat_df], axis=1)
    y = df["log_price"] if "selling_price" in df.columns else None

    return X, y, encoder