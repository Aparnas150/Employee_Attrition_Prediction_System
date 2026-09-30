import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file_path = os.path.join(
    base_path,
    "dataset",
    "processed_attrition.csv"
)

df = pd.read_csv(file_path)

print("Processed dataset loaded!")
print("Shape:", df.shape)

X = df.drop("Attrition", axis=1)
y = df["Attrition"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining data:", X_train.shape)
print("Testing data:", X_test.shape)

# Logistic Regression
logistic_model = LogisticRegression(
    max_iter=2000,
    random_state=42
)

logistic_model.fit(X_train, y_train)

logistic_predictions = logistic_model.predict(X_test)

logistic_accuracy = accuracy_score(
    y_test,
    logistic_predictions
)

print("\n===== Logistic Regression =====")
print("Accuracy:", logistic_accuracy)
print(classification_report(y_test, logistic_predictions))

# Random Forest
random_forest_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

random_forest_model.fit(X_train, y_train)

random_forest_predictions = random_forest_model.predict(X_test)

random_forest_accuracy = accuracy_score(
    y_test,
    random_forest_predictions
)

print("\n===== Random Forest =====")
print("Accuracy:", random_forest_accuracy)
print(classification_report(y_test, random_forest_predictions))

# Create models folder
models_path = os.path.join(base_path, "models")
os.makedirs(models_path, exist_ok=True)

# Save models
joblib.dump(
    logistic_model,
    os.path.join(models_path, "logistic_model.pkl")
)

joblib.dump(
    random_forest_model,
    os.path.join(models_path, "random_forest_model.pkl")
)

# Save feature names
joblib.dump(
    list(X.columns),
    os.path.join(models_path, "feature_names.pkl")
)

print("\nModels saved successfully!")
print("Models folder:", models_path)