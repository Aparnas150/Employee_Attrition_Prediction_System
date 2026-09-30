import pandas as pd
import os

file_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "dataset",
    "WA_Fn-UseC_-HR-Employee-Attrition.csv"
)

df = pd.read_csv(file_path)

print("Original Dataset Shape:", df.shape)

# Remove columns that are not useful for prediction
columns_to_drop = [
    "EmployeeCount",
    "EmployeeNumber",
    "Over18",
    "StandardHours"
]

df = df.drop(columns=columns_to_drop)

print("After Removing Unnecessary Columns:", df.shape)

# Convert target column
df["Attrition"] = df["Attrition"].map({
    "Yes": 1,
    "No": 0
})

# Convert categorical columns into numerical columns
categorical_columns = df.select_dtypes(include=["object"]).columns

df = pd.get_dummies(
    df,
    columns=categorical_columns,
    drop_first=True
)

print("After Encoding:", df.shape)

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum().sum())

# Save processed dataset
output_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "dataset",
    "processed_attrition.csv"
)

df.to_csv(output_path, index=False)

print("\nPreprocessing completed successfully!")
print("Processed dataset saved at:")
print(output_path)