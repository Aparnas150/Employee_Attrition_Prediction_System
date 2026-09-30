async function predictRisk(event) {

    if (event) {
        event.preventDefault();
    }

    const data = {
        Age: Number(document.getElementById("age").value),
        DailyRate: Number(document.getElementById("dailyRate").value),
        DistanceFromHome: Number(document.getElementById("distance").value),
        Education: Number(document.getElementById("education").value),
        EnvironmentSatisfaction: Number(document.getElementById("environment").value),
        HourlyRate: Number(document.getElementById("hourlyRate").value),
        JobInvolvement: Number(document.getElementById("jobInvolvement").value),
        JobLevel: Number(document.getElementById("jobLevel").value),
        JobSatisfaction: Number(document.getElementById("satisfaction").value),
        MonthlyIncome: Number(document.getElementById("income").value),
        MonthlyRate: Number(document.getElementById("monthlyRate").value),
        NumCompaniesWorked: Number(document.getElementById("companiesWorked").value),
        PercentSalaryHike: Number(document.getElementById("salaryHike").value),
        PerformanceRating: Number(document.getElementById("performance").value),
        RelationshipSatisfaction: Number(document.getElementById("relationship").value),
        StockOptionLevel: Number(document.getElementById("stockOption").value),
        TotalWorkingYears: Number(document.getElementById("workingYears").value),
        TrainingTimesLastYear: Number(document.getElementById("training").value),
        WorkLifeBalance: Number(document.getElementById("workLife").value),
        YearsAtCompany: Number(document.getElementById("companyYears").value),
        YearsInCurrentRole: Number(document.getElementById("currentRoleYears").value),
        YearsSinceLastPromotion: Number(document.getElementById("promotionYears").value),
        YearsWithCurrManager: Number(document.getElementById("managerYears").value),

        "BusinessTravel_Travel_Frequently": document.getElementById("travel").value === "Travel_Frequently" ? 1 : 0,
        "BusinessTravel_Travel_Rarely": document.getElementById("travel").value === "Travel_Rarely" ? 1 : 0,

        "Department_Research & Development": document.getElementById("department").value === "Research & Development" ? 1 : 0,
        "Department_Sales": document.getElementById("department").value === "Sales" ? 1 : 0,

        "EducationField_Life Sciences": document.getElementById("educationField").value === "Life Sciences" ? 1 : 0,
        "EducationField_Marketing": document.getElementById("educationField").value === "Marketing" ? 1 : 0,
        "EducationField_Medical": document.getElementById("educationField").value === "Medical" ? 1 : 0,
        "EducationField_Other": document.getElementById("educationField").value === "Other" ? 1 : 0,
        "EducationField_Technical Degree": document.getElementById("educationField").value === "Technical Degree" ? 1 : 0,

        "Gender_Male": document.getElementById("gender").value === "Male" ? 1 : 0,

        "JobRole_Human Resources": document.getElementById("jobRole").value === "Human Resources" ? 1 : 0,
        "JobRole_Laboratory Technician": document.getElementById("jobRole").value === "Laboratory Technician" ? 1 : 0,
        "JobRole_Manager": document.getElementById("jobRole").value === "Manager" ? 1 : 0,
        "JobRole_Manufacturing Director": document.getElementById("jobRole").value === "Manufacturing Director" ? 1 : 0,
        "JobRole_Research Director": document.getElementById("jobRole").value === "Research Director" ? 1 : 0,
        "JobRole_Research Scientist": document.getElementById("jobRole").value === "Research Scientist" ? 1 : 0,
        "JobRole_Sales Executive": document.getElementById("jobRole").value === "Sales Executive" ? 1 : 0,
        "JobRole_Sales Representative": document.getElementById("jobRole").value === "Sales Representative" ? 1 : 0,

        "MaritalStatus_Married": document.getElementById("maritalStatus").value === "Married" ? 1 : 0,
        "MaritalStatus_Single": document.getElementById("maritalStatus").value === "Single" ? 1 : 0,

        "OverTime_Yes": document.getElementById("overtime").value === "Yes" ? 1 : 0
    };

    try {

        const response = await fetch(
"https://employee-attrition-prediction-system-ydid.onrender.com/predict",            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            }
        );

        const result = await response.json();

        if (!response.ok) {
            alert("Prediction error: " + result.error);
            return;
        }

        document.getElementById("riskLevel").textContent = result.risk_level;
        document.getElementById("riskProbability").textContent = result.attrition_probability + "%";
        document.getElementById("riskMessage").textContent = result.message;

        document.getElementById("resultCard").style.display = "block";

       
    } catch (error) {

        alert("Unable to connect to backend: " + error.message);

    }
}