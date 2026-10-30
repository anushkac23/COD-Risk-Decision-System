import pandas as pd
import numpy as np
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
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


# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "orders_sample.csv"

MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "cod_risk_model.pkl"

MODEL_DIR.mkdir(exist_ok=True)


# ==========================================
# 2. LOAD DATASET
# ==========================================

print("\nLoading COD order dataset...")

df = pd.read_csv(DATA_PATH)

print("Original records:", len(df))


# ==========================================
# 3. DATA CLEANING
# ==========================================

df["final_status"] = (
    df["final_status"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# Keep only completed orders
df = df[
    df["final_status"].isin(["DELIVERED", "RTO"])
].copy()

# Remove duplicate order IDs to avoid counting
# the same order multiple times.
df = df.drop_duplicates(
    subset=["order_id"],
    keep="first"
)

print("Records after cleaning:", len(df))


# ==========================================
# 4. FEATURE ENGINEERING
# ==========================================

# Address quality indicators

df["address"] = (
    df["address"]
    .fillna("")
    .astype(str)
    .str.strip()
)

df["address_length"] = df["address"].str.len()

df["address_incomplete"] = (
    df["address"].isin(["", "."])
).astype(int)


# Pincode as categorical data

# Pincode as categorical data

df["pincode"] = df["pincode"].map(
    lambda value: "UNKNOWN" if pd.isna(value) else str(value).replace(".0", "")
)

# Fill missing categorical values

categorical_features = [
    "city",
    "state",
    "pincode",
    "utm_source",
    "courier"
]

for column in categorical_features:
    df[column] = df[column].apply(
        lambda value: "UNKNOWN" if pd.isna(value) else str(value)
    )

# Numeric features

numeric_features = [
    "order_value",
    "num_items",
    "customer_prior_orders",
    "customer_prior_rto",
    "address_length",
    "address_incomplete"
]


# ==========================================
# 5. SELECT FEATURES AND TARGET
# ==========================================

features = numeric_features + categorical_features

X = df[features]

# RTO = 1
# DELIVERED = 0

y = (
    df["final_status"] == "RTO"
).astype(int)


print("\nFeature columns:")
print(features)

print("\nTarget distribution:")
print(y.value_counts())


# ==========================================
# 6. TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))


# ==========================================
# 7. PREPROCESSING
# ==========================================

numeric_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median"))
    ]
)

categorical_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "encoder",
            OneHotEncoder(handle_unknown="ignore")
        )
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("numeric", numeric_transformer, numeric_features),
        (
            "categorical",
            categorical_transformer,
            categorical_features
        )
    ]
)


# ==========================================
# 8. RANDOM FOREST MODEL
# ==========================================

random_forest = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    min_samples_split=10,
    min_samples_leaf=5,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)


# Complete machine learning pipeline

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", random_forest)
    ]
)


# ==========================================
# 9. TRAIN MODEL
# ==========================================

print("\nTraining machine learning model...")

model.fit(X_train, y_train)

print("Training completed!")


# ==========================================
# 10. MODEL EVALUATION
# ==========================================

predictions = model.predict(X_test)

probabilities = model.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, predictions)

precision = precision_score(
    y_test,
    predictions,
    zero_division=0
)

recall = recall_score(
    y_test,
    predictions,
    zero_division=0
)

f1 = f1_score(
    y_test,
    predictions,
    zero_division=0
)

auc = roc_auc_score(y_test, probabilities)


print("\n========== MODEL PERFORMANCE ==========")

print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")
print(f"ROC AUC:   {auc:.4f}")

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions,
        target_names=["DELIVERED", "RTO"],
        zero_division=0
    )
)

print("\nConfusion Matrix:")

print(confusion_matrix(y_test, predictions))


# ==========================================
# 11. SAVE TRAINED MODEL
# ==========================================

joblib.dump(model, MODEL_PATH)

print("\nModel saved successfully!")

print("Model location:", MODEL_PATH)

print("\n========== TRAINING COMPLETED ==========")