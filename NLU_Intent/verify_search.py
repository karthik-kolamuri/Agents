import sys
import os
from dotenv import load_dotenv

# Add the current directory to sys.path to allow importing from .nlu_service
sys.path.append(os.getcwd())

from nlu_service.qa_search import QASearcher

def test_search():
    searcher = QASearcher()
    
    queries = [
        "what is the price of 2bhk?",
        "is there a swimming pool?",
        "how to book a flat?"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        result = searcher.best_match(query)
        print(f"Match: {result['question']}")
        print(f"Answer: {result['answer']}")
        print(f"Similarity Score: {result['similarity_score']:.4f}")

if __name__ == "__main__":
    test_search()
