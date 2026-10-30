import pandas as pd
import joblib

from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix
)

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "orders_sample.csv"
MODEL_PATH = BASE_DIR / "models" / "cod_risk_model_time_based.pkl"

# Load dataset
df = pd.read_csv(DATA_PATH)

# Clean status
df["final_status"] = df["final_status"].astype(str).str.strip().str.upper()

df = df[df["final_status"].isin(["DELIVERED", "RTO"])].copy()

# Remove duplicate orders
df = df.drop_duplicates(subset="order_id", keep="first")

# Convert dates
df["order_datetime"] = pd.to_datetime(
    df["order_datetime"], errors="coerce"
)

df = df.dropna(subset=["order_datetime"])

# Feature engineering
df["address"] = df["address"].fillna("").astype(str).str.strip()

df["address_length"] = df["address"].str.len()

df["address_incomplete"] = df["address"].isin(
    ["", ".", "None", "nan"]
).astype(int)

df["pincode"] = df["pincode"].apply(
    lambda value: "UNKNOWN"
    if pd.isna(value)
    else str(value).replace(".0", "")
)

# Define features
numeric_features = [
    "order_value",
    "num_items",
    "customer_prior_orders",
    "customer_prior_rto",
    "address_length",
    "address_incomplete"
]

categorical_features = [
    "city",
    "state",
    "pincode",
    "utm_source",
    "courier"
]

feature_columns = numeric_features + categorical_features

# Prepare numeric columns
for column in numeric_features:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Prepare categorical columns
for column in categorical_features:
    df[column] = df[column].apply(
        lambda value: "UNKNOWN"
        if pd.isna(value)
        else str(value)
    )

# Target: RTO = 1, Delivered = 0
df["target"] = (df["final_status"] == "RTO").astype(int)

# Time-based split
train_df = df[df["order_datetime"] < "2026-09-01"].copy()

test_df = df[
    (df["order_datetime"] >= "2026-09-01") &
    (df["order_datetime"] < "2026-10-01")
].copy()

X_train = train_df[feature_columns]
y_train = train_df["target"]

X_test = test_df[feature_columns]
y_test = test_df["target"]

print("\n========== TIME-BASED MODEL TRAINING ==========")
print("Training orders:", len(train_df))
print("Testing orders:", len(test_df))

# Preprocessing
numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median"))
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(transformers=[
    ("num", numeric_transformer, numeric_features),
    ("cat", categorical_transformer, categorical_features)
])

# Random Forest model
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=300,
        max_depth=10,
        min_samples_split=10,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ))
])

# Train model only on April-August data
model.fit(X_train, y_train)

# Predict September outcomes
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

# Evaluation
print("\n========== SEPTEMBER MODEL PERFORMANCE ==========")

print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision: {precision_score(y_test, y_pred, zero_division=0):.4f}")
print(f"Recall:    {recall_score(y_test, y_pred, zero_division=0):.4f}")
print(f"F1 Score:  {f1_score(y_test, y_pred, zero_division=0):.4f}")

if y_test.nunique() == 2:
    print(f"ROC AUC:   {roc_auc_score(y_test, y_prob):.4f}")

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=["DELIVERED", "RTO"],
    zero_division=0
))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Save separately to protect the existing dashboard model
joblib.dump(model, MODEL_PATH)

print("\nTime-based model saved successfully:")
print(MODEL_PATH)