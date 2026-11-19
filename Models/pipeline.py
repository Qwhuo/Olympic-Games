from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "Data" / "preprocessed" / "model1_df.csv"
MODEL_PATH = ROOT / "Models" / "model1.joblib"

TARGET = "total_medals"
NUMERIC = [
    "year",
    "GPD",
    "Popul",
    "Disciplines",
    "Athletes",
    "total_countries",
    "Events",
    "is_host",
]
CATEGORICAL = [
    "type",
    "noc",
]
FEATURES = NUMERIC + CATEGORICAL

def main():
    df = pd.read_csv(DATA_PATH)
    required = FEATURES + [TARGET]
    missing = set(required) - set(df.columns)

    if missing:
        raise ValueError(f"Missing columns: {missing}")
    years = sorted(df["year"].unique())
    split_idx = int(len(years) * 0.8)
    train_years = years[:split_idx]
    test_years = years[split_idx:]
    train = df[df["year"].isin(train_years)]
    test = df[df["year"].isin(test_years)]
    X_train = train[FEATURES]
    y_train = train[TARGET]
    X_test = test[FEATURES]
    y_test = test[TARGET]
    print(f"Train: {len(train)} rows")
    print(f"Test:  {len(test)} rows")
    print(f"Test years: {test_years}")
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(
            n_estimators=200,
            random_state=42,
            n_jobs=-1,
        ),
        "Gradient Boosting": HistGradientBoostingRegressor(
            random_state=42,
        ),
    }
    results = []
    fitted_models = {}
    for name, estimator in models.items():
        preprocessor = ColumnTransformer([
            (
                "numeric",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                ]),
                NUMERIC,
            ),
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
                CATEGORICAL,
            ),
        ])
        pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("model", estimator),
        ])
        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        r2 = r2_score(y_test, predictions)
        results.append({
            "Model": name,
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2,
        })
        fitted_models[name] = pipeline
    results_df = pd.DataFrame(results).sort_values("MAE")
    print("\nModel comparison:")
    print(results_df.to_string(index=False))
    best_name = results_df.iloc[0]["Model"]
    best_model = fitted_models[best_name]
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_model, MODEL_PATH)
    print(f"\nBest model: {best_name}")
    print(f"Saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()