import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity  # Load dataset
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "shl_full_catalogue.csv")

df = pd.read_csv(DATA_PATH)

df["combined_text"] = (
    df["name"].fillna("") + " " +
    df["description"].fillna("") + " " +
    df["test_type"].fillna("")
)

# ---------- TF-IDF ----------
tfidf_vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf_vectorizer.fit_transform(df["combined_text"])

# ---------- Embeddings ----------
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = embedding_model.encode(df["combined_text"].tolist(), show_progress_bar=False)

dimension = embeddings.shape[1]
faiss_index = faiss.IndexFlatL2(dimension)
faiss_index.add(np.array(embeddings))


def recommend(query, top_k=5, alpha=0.5):
    """
    alpha controls balance:
    alpha = 1 → pure embeddings
    alpha = 0 → pure TF-IDF
    """

    # ---- TF-IDF score ----
    query_tfidf = tfidf_vectorizer.transform([query])
    tfidf_scores = cosine_similarity(query_tfidf, tfidf_matrix).flatten()

    # ---- Embedding score ----
    query_embedding = embedding_model.encode([query])
    distances, indices = faiss_index.search(np.array(query_embedding), len(df))

    # Convert L2 distance to similarity
    embedding_scores = 1 / (1 + distances.flatten())

    # Normalize both scores
    tfidf_scores = (tfidf_scores - tfidf_scores.min()) / (tfidf_scores.max() - tfidf_scores.min() + 1e-9)
    embedding_scores = (embedding_scores - embedding_scores.min()) / (embedding_scores.max() - embedding_scores.min() + 1e-9)

    # Combine scores
    hybrid_scores = alpha * embedding_scores + (1 - alpha) * tfidf_scores

    top_indices = np.argsort(hybrid_scores)[-top_k:][::-1]

    results = df.iloc[top_indices].copy()

# Replace NaN with empty string
    results = results.fillna("")


    records = results.to_dict("records")

# Remove internal field
    for r in records:
        r.pop("combined_text", None)

    return records
