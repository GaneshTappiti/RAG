"""
Create Vector Database for Lovable.dev Documentation
Author: Enhanced RAG System
Description: Creates a ChromaDB vector database from Lovable.dev documentation
"""

import os
import shutil
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CHROMA_PATH = "chroma_lovable"
DATA_PATH = "data/lovable_docs"

def main():
    print("🚀 Creating Lovable.dev Vector Database")
    generate_data_store()

def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)

def load_documents():
    print(f"📂 Loading documents from {DATA_PATH}")
    
    if not os.path.exists(DATA_PATH):
        print(f"❌ Error: {DATA_PATH} does not exist")
        return []
    
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    
    print(f"✅ Loaded {len(documents)} documents")
    return documents

def split_text(documents: list[Document]):
    print("✂️ Splitting documents into chunks")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    
    # Add enhanced metadata for better retrieval
    for chunk in chunks:
        source_file = os.path.basename(chunk.metadata.get('source', ''))
        
        # Categorize based on filename
        if 'prompting' in source_file.lower():
            chunk.metadata['category'] = 'prompting'
            chunk.metadata['tags'] = ['best-practices', 'guidelines', 'structure']
        elif 'ui_design' in source_file.lower():
            chunk.metadata['category'] = 'ui_design'
            chunk.metadata['tags'] = ['ui', 'ux', 'design', 'components', 'responsive']
        elif 'api_integration' in source_file.lower():
            chunk.metadata['category'] = 'integration'
            chunk.metadata['tags'] = ['api', 'integration', 'authentication', 'http']
        elif 'debugging' in source_file.lower():
            chunk.metadata['category'] = 'debugging'
            chunk.metadata['tags'] = ['debugging', 'troubleshooting', 'performance', 'testing']
        else:
            chunk.metadata['category'] = 'general'
            chunk.metadata['tags'] = ['general']
        
        # Add content type metadata
        content = chunk.page_content.lower()
        if 'react' in content:
            chunk.metadata['framework'] = 'react'
        if 'next.js' in content or 'nextjs' in content:
            chunk.metadata['framework'] = 'nextjs'
        if 'tailwind' in content:
            chunk.metadata['styling'] = 'tailwind'
        if 'api' in content:
            chunk.metadata['type'] = 'api'
        if 'component' in content:
            chunk.metadata['type'] = 'component'
    
    print(f"✅ Split into {len(chunks)} chunks")
    return chunks

def save_to_chroma(chunks: list[Document]):
    print("💾 Saving chunks to ChromaDB")
    
    # Clear out the existing database
    if os.path.exists(CHROMA_PATH):
        print(f"🗑️ Clearing existing database at {CHROMA_PATH}")
        shutil.rmtree(CHROMA_PATH)
    
    # Create the new DB from the documents
    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=CHROMA_PATH
    )
    
    print(f"✅ Saved {len(chunks)} chunks to {CHROMA_PATH}")
    
    # Test the database
    print("\n🧪 Testing the database")
    test_queries = [
        "How to create a responsive dashboard?",
        "API authentication best practices",
        "React component debugging",
        "UI design patterns"
    ]
    
    for query in test_queries:
        results = db.similarity_search(query, k=2)
        print(f"Query: '{query}' -> Found {len(results)} results")
        if results:
            print(f"  Top result category: {results[0].metadata.get('category', 'unknown')}")

def test_categories():
    """Test retrieval by category"""
    print("\n🔍 Testing category-based retrieval")
    
    if not os.path.exists(CHROMA_PATH):
        print("❌ Database not found. Run main() first.")
        return
    
    embeddings = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    
    categories = ['prompting', 'ui_design', 'integration', 'debugging']
    
    for category in categories:
        results = db.similarity_search(
            "best practices",
            k=3,
            filter={"category": category}
        )
        print(f"Category '{category}': {len(results)} results")

if __name__ == "__main__":
    main()
    test_categories()
