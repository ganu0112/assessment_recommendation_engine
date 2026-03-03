import numpy as np
import json
from model.recommendation_engine import recommend  # <-- your real recommender


def precision_at_k(recommended, relevant, k=5):
    recommended = recommended[:k]
    relevant_set = set(relevant)
    hits = sum([1 for item in recommended if item in relevant_set])
    return hits / k


def recall_at_k(recommended, relevant, k=5):
    recommended = recommended[:k]
    relevant_set = set(relevant)
    hits = sum([1 for item in recommended if item in relevant_set])
    return hits / len(relevant_set) if relevant_set else 0


def mean_reciprocal_rank(recommended, relevant):
    for i, item in enumerate(recommended):
        if item in relevant:
            return 1 / (i + 1)
    return 0


def evaluate_system():
    with open("data/test/evaluation_queries.json") as f:
        test_queries = json.load(f)

    precision_scores = []
    recall_scores = []
    mrr_scores = []

    for q in test_queries:
        query = q["query"]
        relevant = q["relevant"]

        # 🔥 Get real recommendations from your model
        recommended_results = recommend(query, top_k=5, alpha=0.8)

        # Extract only names
        recommended_names = [r["name"] for r in recommended_results]

        precision_scores.append(precision_at_k(recommended_names, relevant))
        recall_scores.append(recall_at_k(recommended_names, relevant))
        mrr_scores.append(mean_reciprocal_rank(recommended_names, relevant))

    print("Evaluation Results:")
    print("Precision@5:", np.mean(precision_scores))
    print("Recall@5:", np.mean(recall_scores))
    print("MRR:", np.mean(mrr_scores))