import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file_path = os.path.join(
    base_path,
    "dataset",
    "processed_attrition.csv"
)

df = pd.read_csv(file_path)

print("Processed Dataset Loaded!")
print("Shape:", df.shape)

print("\nAttrition Distribution:")
print(df["Attrition"].value_counts())

# Create graphs folder
graphs_path = os.path.join(base_path, "reports", "graphs")
os.makedirs(graphs_path, exist_ok=True)

# 1. Attrition Distribution
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x="Attrition")
plt.title("Employee Attrition Distribution")
plt.xlabel("Attrition")
plt.ylabel("Number of Employees")
plt.savefig(os.path.join(graphs_path, "attrition_distribution.png"))
plt.show()

# 2. Age Distribution
plt.figure(figsize=(8, 5))
sns.histplot(data=df, x="Age", bins=20, kde=True)
plt.title("Employee Age Distribution")
plt.xlabel("Age")
plt.ylabel("Number of Employees")
plt.savefig(os.path.join(graphs_path, "age_distribution.png"))
plt.show()

# 3. Monthly Income vs Attrition
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="Attrition", y="MonthlyIncome")
plt.title("Monthly Income vs Attrition")
plt.xlabel("Attrition")
plt.ylabel("Monthly Income")
plt.savefig(os.path.join(graphs_path, "income_vs_attrition.png"))
plt.show()

# 4. Job Satisfaction vs Attrition
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="JobSatisfaction", hue="Attrition")
plt.title("Job Satisfaction vs Attrition")
plt.xlabel("Job Satisfaction")
plt.ylabel("Number of Employees")
plt.savefig(os.path.join(graphs_path, "job_satisfaction_vs_attrition.png"))
plt.show()

# 5. Overtime vs Attrition
overtime_file = os.path.join(
    graphs_path,
    "overtime_vs_attrition.png"
)

if "OverTime_Yes" in df.columns:
    plt.figure(figsize=(7, 5))
    sns.countplot(data=df, x="OverTime_Yes", hue="Attrition")
    plt.title("Overtime vs Attrition")
    plt.xlabel("Overtime")
    plt.ylabel("Number of Employees")
    plt.savefig(overtime_file)
    plt.show()

print("\nEDA completed successfully!")
print("Graphs saved in:")
print(graphs_path)