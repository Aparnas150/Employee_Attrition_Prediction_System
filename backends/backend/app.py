from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import joblib
import pandas as pd
import sqlite3

app = Flask(__name__)
CORS(app)

base_path = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

models_path = os.path.join(base_path, "models")
database_path = os.path.join(base_path, "database", "attrition.db")

model = joblib.load(
    os.path.join(models_path, "logistic_model.pkl")
)

feature_names = joblib.load(
    os.path.join(models_path, "feature_names.pkl")
)


@app.route("/")
def home():
    return jsonify({
        "message": "Employee Attrition Prediction API is running!"
    })


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        input_data = {}

        for feature in feature_names:
            input_data[feature] = data.get(feature, 0)

        input_df = pd.DataFrame(
            [input_data],
            columns=feature_names
        )

        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]

        probability_percent = round(
            probability * 100,
            2
        )

        if probability_percent < 40:
            risk = "Low"
        elif probability_percent < 70:
            risk = "Medium"
        else:
            risk = "High"

        if data.get("Gender_Male", 0) == 1:
            gender = "Male"
        else:
            gender = "Female"

        if data.get(
            "Department_Research & Development",
            0
        ) == 1:
            department = "Research & Development"

        elif data.get(
            "Department_Sales",
            0
        ) == 1:
            department = "Sales"

        else:
            department = "Human Resources"

        if data.get("OverTime_Yes", 0) == 1:
            overtime = "Yes"
        else:
            overtime = "No"

        if data.get(
            "MaritalStatus_Married",
            0
        ) == 1:
            marital_status = "Married"

        elif data.get(
            "MaritalStatus_Single",
            0
        ) == 1:
            marital_status = "Single"

        else:
            marital_status = "Divorced"

        job_roles = {
            "JobRole_Human Resources":
                "Human Resources",

            "JobRole_Laboratory Technician":
                "Laboratory Technician",

            "JobRole_Manager":
                "Manager",

            "JobRole_Manufacturing Director":
                "Manufacturing Director",

            "JobRole_Research Director":
                "Research Director",

            "JobRole_Research Scientist":
                "Research Scientist",

            "JobRole_Sales Executive":
                "Sales Executive",

            "JobRole_Sales Representative":
                "Sales Representative"
        }

        job_role = "Other"

        for feature, role in job_roles.items():
            if data.get(feature, 0) == 1:
                job_role = role
                break

        connection = sqlite3.connect(
            database_path
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO predictions (
                age,
                gender,
                marital_status,
                department,
                job_role,
                overtime,
                monthly_income,
                job_satisfaction,
                total_working_years,
                years_at_company,
                risk_level,
                attrition_probability
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data.get("Age", 0),
                gender,
                marital_status,
                department,
                job_role,
                overtime,
                data.get("MonthlyIncome", 0),
                data.get("JobSatisfaction", 0),
                data.get("TotalWorkingYears", 0),
                data.get("YearsAtCompany", 0),
                risk,
                probability_percent
            )
        )

        connection.commit()
        connection.close()

        return jsonify({
            "prediction": int(prediction),
            "attrition_probability":
                probability_percent,
            "risk_level": risk,
            "message":
                "Prediction saved successfully!"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


@app.route("/history", methods=["GET"])
def history():
    try:
        connection = sqlite3.connect(
            database_path
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                age,
                gender,
                marital_status,
                department,
                job_role,
                overtime,
                monthly_income,
                job_satisfaction,
                total_working_years,
                years_at_company,
                risk_level,
                attrition_probability,
                created_at
            FROM predictions
            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        connection.close()

        history_data = []

        for row in rows:
            history_data.append({
                "id": row[0],
                "age": row[1],
                "gender": row[2],
                "marital_status": row[3],
                "department": row[4],
                "job_role": row[5],
                "overtime": row[6],
                "monthly_income": row[7],
                "job_satisfaction": row[8],
                "total_working_years": row[9],
                "years_at_company": row[10],
                "risk_level": row[11],
                "attrition_probability": row[12],
                "created_at": row[13]
            })

        return jsonify(history_data)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )