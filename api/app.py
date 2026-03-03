# from db.database import log_to_db
# from fastapi import FastAPI
# from utils.preprocess import load_and_prepare_data
# from model.recommender import recommend
# from utils.skill_extractor import extract_skills_from_jd
# from fastapi.middleware.cors import CORSMiddleware

# import re

# def infer_experience_from_jd(jd_text: str) -> str:
#     """
#     Extract experience like '2-4 years', '3+ years' from JD text
#     """
#     match = re.search(r"(\d+)\s*[-+to]+\s*(\d+)?\s*years?", jd_text.lower())
#     if match:
#         if match.group(2):
#             return f"{match.group(1)}-{match.group(2)} years"
#         return f"{match.group(1)}+ years"
#     return ""


# app = FastAPI()

# # Load SHL catalog once
# df = load_and_prepare_data("data/Gen_AI Dataset.xlsx")

# from db.database import log_to_db
# from fastapi import FastAPI
# from utils.preprocess import load_and_prepare_data
# from model.recommender import recommend
# from utils.skill_extractor import extract_skills_from_jd


# import re

# def infer_experience_from_jd(jd_text: str) -> str:
#     """
#     Extract experience like '2-4 years', '3+ years' from JD text
#     """
#     match = re.search(r"(\d+)\s*[-+to]+\s*(\d+)?\s*years?", jd_text.lower())
#     if match:
#         if match.group(2):
#             return f"{match.group(1)}-{match.group(2)} years"
#         return f"{match.group(1)}+ years"
#     return ""


# app = FastAPI()

# # Load SHL catalog once
# df = load_and_prepare_data("data/Gen_AI Dataset.xlsx")

# @app.post("/recommend")
# def recommend_from_jd(payload: dict):
#     try:
#         jd_text = payload.get("job_description", "")
#         if not jd_text:
#             return {"error": "Job description is required"}

#         extracted = extract_skills_from_jd(jd_text)

#         skills = extracted.get("skills", [])
#         experience = extracted.get("experience", "")

#         # fallback experience inference if needed
#         if not experience:
#             experience = infer_experience_from_jd(jd_text)

#         job_text = " ".join(skills) + " " + experience

#         recommendations = recommend(job_text, experience, df)

#         # 🔥 STORE EVERYTHING IN DB
#         log_to_db(
#             job_description=jd_text,
#             skills=skills,
#             experience=experience,
#             recommendations=recommendations
#         )

#         return {

#             "recommended_assessments": recommendations
#         }

#     except Exception as e:
#         return {
#             "error": "Internal processing error",
#             "details": str(e)
#         }

# @app.get("/health")
# def health():
#     return {"status": "ok"}


from fastapi import FastAPI
from pydantic import BaseModel
from model.recommendation_engine import recommend

app = FastAPI(title="SHL Assessment Recommendation API")


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


@app.post("/recommend")
def recommend_assessments(request: QueryRequest):
    results = recommend(request.query, top_k=request.top_k)

    return {
        "query": request.query,
        "results": results
    }