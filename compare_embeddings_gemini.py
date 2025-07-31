"""
RAG System Embedding Comparison with Gemini
Author: Ganesh Tappiti
Description: Compares different embedding approaches using Google Gemini embeddings
"""

from langchain_google_genai import GoogleGenerativeAIEmbeddings
import numpy as np
from dotenv import load_dotenv
import os

# Load environment variables. Assumes that project contains .env file with API keys
load_dotenv()

# Set Google API key in environment for langchain-google-genai to use
os.environ['GOOGLE_API_KEY'] = os.environ.get('GOOGLE_API_KEY', '')

def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def main():
    # Get embedding for words using Google Gemini.
    embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # Test words
    word1 = "apple"
    word2 = "iphone"
    
    print(f"Getting embeddings for '{word1}' and '{word2}'...")
    
    vector1 = embedding_function.embed_query(word1)
    vector2 = embedding_function.embed_query(word2)
    
    print(f"Vector for '{word1}': First 10 dimensions: {vector1[:10]}")
    print(f"Vector length: {len(vector1)}")
    print(f"Vector for '{word2}': First 10 dimensions: {vector2[:10]}")
    print(f"Vector length: {len(vector2)}")

    # Calculate cosine similarity
    similarity = cosine_similarity(np.array(vector1), np.array(vector2))
    print(f"\nCosine similarity between '{word1}' and '{word2}': {similarity:.4f}")
    
    # Test with more similar words
    word3 = "fruit"
    vector3 = embedding_function.embed_query(word3)
    similarity2 = cosine_similarity(np.array(vector1), np.array(vector3))
    print(f"Cosine similarity between '{word1}' and '{word3}': {similarity2:.4f}")
    
    print(f"\nAs expected, '{word1}' is more similar to '{word3}' ({similarity2:.4f}) than to '{word2}' ({similarity:.4f})")


if __name__ == "__main__":
    main()
