import pandas as pd
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

data_path = os.path.join(
    base_path,
    "dataset",
    "processed_attrition.csv"
)

models_path = os.path.join(
    base_path,
    "models"
)

df = pd.read_csv(data_path)

X = df.drop("Attrition", axis=1)
y = df["Attrition"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

logistic_model = joblib.load(
    os.path.join(models_path, "logistic_model.pkl")
)

random_forest_model = joblib.load(
    os.path.join(models_path, "random_forest_model.pkl")
)

logistic_predictions = logistic_model.predict(X_test)
random_forest_predictions = random_forest_model.predict(X_test)

# Calculate metrics
results = {
    "Model": [
        "Logistic Regression",
        "Random Forest"
    ],
    "Accuracy": [
        accuracy_score(y_test, logistic_predictions),
        accuracy_score(y_test, random_forest_predictions)
    ],
    "Precision": [
        precision_score(y_test, logistic_predictions),
        precision_score(y_test, random_forest_predictions)
    ],
    "Recall": [
        recall_score(y_test, logistic_predictions),
        recall_score(y_test, random_forest_predictions)
    ],
    "F1 Score": [
        f1_score(y_test, logistic_predictions),
        f1_score(y_test, random_forest_predictions)
    ]
}

results_df = pd.DataFrame(results)

print("===== MODEL COMPARISON =====")
print(results_df.to_string(index=False))

# Create evaluation graph folder
graphs_path = os.path.join(
    base_path,
    "reports",
    "graphs"
)

os.makedirs(graphs_path, exist_ok=True)

# Confusion Matrix - Logistic Regression
cm_logistic = confusion_matrix(
    y_test,
    logistic_predictions
)

plt.figure(figsize=(6, 5))
sns.heatmap(
    cm_logistic,
    annot=True,
    fmt="d",
    cmap="Blues"
)

plt.title("Logistic Regression - Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.savefig(
    os.path.join(
        graphs_path,
        "logistic_confusion_matrix.png"
    )
)

plt.show()

# Confusion Matrix - Random Forest
cm_rf = confusion_matrix(
    y_test,
    random_forest_predictions
)

plt.figure(figsize=(6, 5))
sns.heatmap(
    cm_rf,
    annot=True,
    fmt="d",
    cmap="Greens"
)

plt.title("Random Forest - Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.savefig(
    os.path.join(
        graphs_path,
        "random_forest_confusion_matrix.png"
    )
)

plt.show()

# Save comparison results
results_path = os.path.join(
    base_path,
    "reports",
    "model_comparison.csv"
)

results_df.to_csv(
    results_path,
    index=False
)

print("\nEvaluation completed successfully!")
print("Comparison saved at:")
print(results_path)