import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row
from sentence_transformers import SentenceTransformer


load_dotenv()


from sentence_transformers import SentenceTransformer, util


load_dotenv()


class QASearcher:
    """
    Industrial-grade semantic search over the 90 Q&A pairs using PostgreSQL's pgvector.

    - Uses a multilingual sentence-transformers model to embed queries.
    - Uses the <=> (cosine distance) operator in SQL for database-level search.
    """

    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        dsn = os.getenv("DATABASE_URL")
        if not dsn:
            raise RuntimeError("DATABASE_URL is not set for QASearcher")

        self._dsn = dsn
        self._model = SentenceTransformer(model_name)

    def best_match(self, utterance: str, qa_category: Optional[str] = None) -> Dict[str, Any]:
        """
        Returns the best matching QA row using pgvector semantic search.
        """
        if not utterance.strip():
            raise ValueError("Utterance is empty.")

        query_embedding = self._model.encode(utterance).tolist()

        sql = """
            SELECT id, category, question, answer, language, tags,
                   (1 - (embedding <=> %s::vector)) as similarity_score
            FROM "QAPair"
        """
        params = [query_embedding]

        if qa_category:
            sql += " WHERE category = %s "
            params.append(qa_category)

        sql += " ORDER BY embedding <=> %s::vector ASC LIMIT 1 "
        params.append(query_embedding)

        with psycopg.connect(self._dsn, row_factory=dict_row) as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            row = cur.fetchone()

        if not row:
            # Fallback if category filter yields no results
            if qa_category:
                return self.best_match(utterance, qa_category=None)
            raise RuntimeError("QAPair table is empty or search failed.")

        return {
            "qa_id": row["id"],
            "category": row["category"],
            "question": row["question"],
            "answer": row["answer"],
            "language": row["language"],
            "tags": row.get("tags"),
            "similarity_score": float(row["similarity_score"]),
        }

