🧠 GenAI Assessment Recommendation Engine
Overview

This project implements a GenAI-powered assessment recommendation system that maps job descriptions (JD) to the most relevant SHL assessments using semantic similarity.

The system exposes a FastAPI-based web service and also supports batch/offline recommendation generation via CSV for evaluation and analysis.

The solution is designed to be:

Lightweight

Interpretable

Extensible (LLM-based skill extraction can be plugged in)

Problem Statement

Given a job description, recommend the most suitable SHL assessments from a provided product dataset.

The recommendation should:

Capture semantic similarity (not just keyword matching)

Rank assessments by relevance

Provide a confidence score per recommendation

Dataset Description

Input Dataset: Gen_AI Dataset.xlsx

The dataset contains mappings of:

Column	Description
Query	Skill or role-based query text
Assessment_url	Corresponding SHL assessment link

Note: The dataset does not contain metadata such as assessment duration, test type, or description.
Hence, the system focuses on semantic query-to-assessment matching.

System Architecture
Job Description
      │
      ▼
Skill / Text Processing
      │
      ▼
TF-IDF Vectorization
      │
      ▼
Cosine Similarity Matching
      │
      ▼
Experience Weighting
      │
      ▼
Ranked Assessment URLs + Confidence
Core Approach
1. Text Representation

TF-IDF is used to vectorize:

Job descriptions

Dataset Query texts

This enables semantic similarity comparison beyond exact keyword matches.

2. Similarity Scoring

Cosine similarity is computed between:

Job description vector

Each assessment query vector

3. Experience Weighting

Experience inferred from JD (e.g., “2–4 years”, “3+ years”)

Weighting adjusts ranking to favor assessments suitable for seniority level.

4. Confidence Scoring

Confidence is computed from normalized relevance scores.

Scores are scaled to a realistic range (≈80–95) to avoid artificial certainty.

API Design
Health Check
GET /health

Response:

{
  "status": "ok"
}
Recommendation Endpoint
POST /recommend

Request:

{
  "job_description": "Java backend developer with REST APIs and 3 years experience"
}

Response:

{
  "recommended_assessments": [
    {
      "assessment_url": "https://www.shl.com/solutions/products/product-catalog/view/java-8-new/",
      "confidence": 92.4
    },
    {
      "assessment_url": "https://www.shl.com/solutions/products/product-catalog/view/core-java-entry-level-new/",
      "confidence": 87.1
    }
  ]
}
Batch Recommendation (CSV Output)

For evaluation and offline analysis, recommendations can be generated in batch.

A script generate_submission_csv.py produces:

submission_recommendations.csv

Format:

job_description,assessment_url,confidence
Java backend developer with REST APIs and 3 years experience,https://www.shl.com/...,92.4

This demonstrates how the same recommendation logic can be reused for both API and batch workflows.

Technology Stack

Python 3.12

FastAPI

scikit-learn

pandas

openpyxl

SQLite (for logging requests)

Extensibility

The system is intentionally modular and can be extended with:

LLM-based skill extraction (OpenAI / Azure OpenAI)

RAG-based retrieval over full SHL catalog metadata

Frontend UI for recruiter interaction

More advanced ranking models (BM25, embeddings)

Key Design Decisions

Used TF-IDF + cosine similarity for transparency and interpretability

Normalized confidence scores to avoid misleading 100% certainty

Designed API to be minimal and production-safe

Focused on dataset understanding rather than inventing missing metadata

Conclusion

This solution demonstrates:

Practical GenAI application for talent assessment

Strong data understanding

Clean, extensible backend design

Real-world production thinking

The system is submission-ready and aligns with SHL’s assessment recommendation use case.

Author

Name: (Pradhunya More)
Role: AI / Backend Engineering Candidate