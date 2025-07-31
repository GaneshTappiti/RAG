"""
RAG System Multi-Folder Database Creation
Author: Ganesh Tappiti
Description: Creates a ChromaDB vector database from multiple document folders using Gemini embeddings
"""

from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
import google.generativeai as genai
from dotenv import load_dotenv
import os
import shutil

# Load environment variables
load_dotenv()
# Configure Google AI API key
os.environ['GOOGLE_API_KEY'] = os.environ.get('GOOGLE_API_KEY', '')

CHROMA_PATH = "chroma_gemini"
DATA_PATHS = [
    "data/books",      # Original books folder
    "data/documents",  # New documents folder
    "data/research",   # Research papers
    "data/manuals"     # Manuals/guides
]

# Supported file extensions
FILE_EXTENSIONS = ["*.md", "*.txt", "*.pdf", "*.docx"]

def main():
    print("🚀 Starting multi-folder database generation...")
    generate_data_store()

def generate_data_store():
    all_documents = load_all_documents()
    if not all_documents:
        print("❌ No documents found! Please add files to one of these folders:")
        for path in DATA_PATHS:
            print(f"   - {path}")
        return
    
    chunks = split_text(all_documents)
    save_to_chroma(chunks)

def load_all_documents():
    """Load documents from all data folders."""
    all_documents = []
    
    for data_path in DATA_PATHS:
        if os.path.exists(data_path):
            print(f"📂 Scanning folder: {data_path}")
            folder_docs = load_documents_from_folder(data_path)
            all_documents.extend(folder_docs)
            print(f"   Found {len(folder_docs)} documents")
        else:
            print(f"⚠️  Folder not found: {data_path} (skipping)")
    
    print(f"📚 Total documents loaded: {len(all_documents)}")
    return all_documents

def load_documents_from_folder(folder_path):
    """Load documents from a specific folder."""
    documents = []
    
    for extension in FILE_EXTENSIONS:
        try:
            loader = DirectoryLoader(folder_path, glob=extension)
            folder_docs = loader.load()
            documents.extend(folder_docs)
            if folder_docs:
                print(f"   - Loaded {len(folder_docs)} {extension} files")
        except Exception as e:
            print(f"   - Error loading {extension} files: {e}")
    
    return documents

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✂️  Split {len(documents)} documents into {len(chunks)} chunks.")

    if chunks:
        # Show a sample chunk
        sample_chunk = chunks[min(10, len(chunks) - 1)]
        print(f"\n📄 Sample chunk:")
        print(f"Content: {sample_chunk.page_content[:150]}...")
        print(f"Source: {sample_chunk.metadata.get('source', 'Unknown')}")

    return chunks

def save_to_chroma(chunks: list[Document]):
    # Clear out the database first
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print(f"🗑️  Cleared existing database at {CHROMA_PATH}")

    # Create a new DB from the documents using Google Gemini embeddings
    print("🧠 Creating embeddings with Google Gemini...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = Chroma.from_documents(
        chunks, embeddings, persist_directory=CHROMA_PATH
    )
    print(f"💾 Saved {len(chunks)} chunks to {CHROMA_PATH}")
    print("✅ Database creation complete!")

if __name__ == "__main__":
    main()
