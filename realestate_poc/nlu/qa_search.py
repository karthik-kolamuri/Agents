import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row
from sentence_transformers import SentenceTransformer, util


load_dotenv()


class QASearcher:
    """
    Similarity search over Q&A pairs using Python-side cosine similarity.

    - Loads Q&A rows + pre-computed embeddings from PostgreSQL.
    - Encodes the user query with the same multilingual model.
    - Computes cosine similarity in Python for full control over scoring.
    """

    SIMILARITY_THRESHOLD = 0.45  # Minimum score to consider a match

    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        dsn = os.getenv("DATABASE_URL")
        if not dsn:
            raise RuntimeError("DATABASE_URL is not set for QASearcher")

        self._dsn = dsn
        self._model = SentenceTransformer(model_name)
        self._cache = None  # Cache loaded rows to avoid repeated DB calls

    def _load_qa_pairs(self):
        """Load all Q&A pairs with their embeddings from the database (cached)."""
        if self._cache is not None:
            return self._cache

        try:
            with psycopg.connect(self._dsn, row_factory=dict_row) as conn:
                cur = conn.cursor()
                cur.execute('SELECT id, category, question, answer, language, tags, embedding FROM "QAPair"')
                self._cache = cur.fetchall()
        except Exception as e:
            print(f"[WARN] Failed to load Q&A pairs from database (falling back to empty): {e}")
            return []

        return self._cache


    def best_match(self, utterance: str, qa_category: Optional[str] = None) -> Dict[str, Any]:
        """
        Returns the best matching QA row using cosine similarity.
        """
        if not utterance.strip():
            raise ValueError("Utterance is empty.")

        rows = self._load_qa_pairs()

        # Filter by category if provided
        if qa_category:
            filtered = [r for r in rows if r["category"] == qa_category]
            if not filtered:
                filtered = rows  # Fallback to all if category has no matches
        else:
            filtered = rows

        if not filtered:
            print("[WARN] No Q&A pairs available to search against.")
            return None

        # Encode the user query
        query_embedding = self._model.encode(utterance, convert_to_tensor=True)

        # Get stored embeddings (pgvector returns them as strings, so parse if needed)
        doc_embeddings = []
        for r in filtered:
            emb = r["embedding"]
            if isinstance(emb, str):
                emb = [float(x) for x in emb.strip("[]").split(",")]
            doc_embeddings.append(emb)

        # Compute cosine similarity scores
        scores = util.cos_sim(query_embedding, doc_embeddings)[0]
        best_idx = int(scores.argmax())
        best_score = float(scores[best_idx])

        # If score is below threshold, return None (no confident match)
        if best_score < self.SIMILARITY_THRESHOLD:
            return None

        row = filtered[best_idx]

        return {
            "qa_id": row["id"],
            "category": row["category"],
            "question": row["question"],
            "answer": row["answer"],
            "language": row["language"],
            "tags": row.get("tags"),
            "similarity_score": best_score,
        }
