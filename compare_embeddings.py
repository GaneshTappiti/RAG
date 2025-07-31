"""
RAG System Embedding Comparison
Author: Ganesh Tappiti
Description: Compares different embedding approaches for the RAG system
"""

from langchain_openai import OpenAIEmbeddings
import numpy as np
from dotenv import load_dotenv
import openai
import os

# Load environment variables. Assumes that project contains .env file with API keys
load_dotenv()
#---- Set OpenAI API key 
# Change environment variable name from "OPENAI_API_KEY" to the name given in 
# your .env file.
openai.api_key = os.environ['OPENAI_API_KEY']

def main():
    # Get embedding for a word.
    embedding_function = OpenAIEmbeddings()
    vector1 = embedding_function.embed_query("apple")
    vector2 = embedding_function.embed_query("iphone")
    
    print(f"Vector for 'apple': {vector1[:5]}...")  # Show first 5 elements
    print(f"Vector length: {len(vector1)}")

    # Calculate cosine similarity between the two vectors
    import numpy as np
    
    def cosine_similarity(v1, v2):
        dot_product = np.dot(v1, v2)
        magnitude1 = np.linalg.norm(v1)
        magnitude2 = np.linalg.norm(v2)
        return dot_product / (magnitude1 * magnitude2)
    
    similarity = cosine_similarity(vector1, vector2)
    print(f"Comparing ('apple', 'iphone') - Cosine similarity: {similarity:.4f}")


if __name__ == "__main__":
    main()
