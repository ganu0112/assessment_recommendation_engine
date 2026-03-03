import pandas as pd
from utils.preprocess import load_and_prepare_data
from model.recommender import recommend

# -----------------------------
# Load dataset
# -----------------------------
df = load_and_prepare_data("data/Gen_AI Dataset.xlsx")

# -----------------------------
# Sample Job Descriptions
# (You can add more)
# -----------------------------
job_descriptions = [
    "Java backend developer with REST APIs and 3 years experience",
    "Python developer with data analysis and machine learning skills",
    "Frontend developer with JavaScript, React and UI design"
]

rows = []

# -----------------------------
# Generate recommendations
# -----------------------------
for jd in job_descriptions:
    results = recommend(jd, "", df)

    for r in results:
        rows.append({
            "job_description": jd,
            "assessment_url": r["assessment_url"],
            "confidence": r["confidence"]
        })

# -----------------------------
# Save CSV
# -----------------------------
output_df = pd.DataFrame(rows)
output_df.to_csv("submission_recommendations.csv", index=False)

print("✅ submission_recommendations.csv generated successfully")