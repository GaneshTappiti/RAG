"""
Create Lovable.dev Vector Database with Google Gemini
Description: Creates a Chroma vector database with Lovable.dev documentation using Google Gemini embeddings
"""

import os
import shutil
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_lovable_database_gemini():
    """Create a vector database from Lovable.dev documentation using Gemini embeddings"""
    
    print("🧠 Creating Lovable.dev Vector Database with Google Gemini")
    print("=" * 60)
    
    # Configuration
    docs_path = "data/lovable_docs"
    chroma_path = "chroma_lovable_gemini"
    
    # Remove existing database
    if os.path.exists(chroma_path):
        print(f"Removing existing database at {chroma_path}")
        shutil.rmtree(chroma_path)
    
    # Check if documentation exists
    if not os.path.exists(docs_path):
        print(f"❌ Error: Documentation folder '{docs_path}' not found!")
        print("Please ensure Lovable.dev documentation is available in the data folder.")
        return False
    
    try:
        # Initialize Gemini embeddings
        print("🔧 Initializing Google Gemini embeddings...")
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        # Load documents
        print(f"📚 Loading documents from {docs_path}...")
        loader = DirectoryLoader(docs_path, glob="*.md")
        documents = loader.load()
        
        if not documents:
            print("❌ No documents found! Make sure .md files exist in the docs folder.")
            return False
        
        print(f"Found {len(documents)} documents")
        
        # Split documents into chunks
        print("✂️ Splitting documents into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
        
        chunks = text_splitter.split_documents(documents)
        print(f"Created {len(chunks)} text chunks")
        
        # Add metadata for better retrieval
        print("🏷️ Adding metadata to chunks...")
        for chunk in chunks:
            # Extract category from filename or content
            filename = os.path.basename(chunk.metadata.get('source', ''))
            
            # Categorize based on filename patterns
            if 'prompting' in filename.lower():
                chunk.metadata['category'] = 'prompting'
            elif 'ui_design' in filename.lower() or 'ui' in filename.lower():
                chunk.metadata['category'] = 'ui_design'
            elif 'api' in filename.lower() or 'integration' in filename.lower():
                chunk.metadata['category'] = 'integration'
            elif 'debug' in filename.lower():
                chunk.metadata['category'] = 'debugging'
            elif 'performance' in filename.lower():
                chunk.metadata['category'] = 'performance'
            elif 'accessibility' in filename.lower():
                chunk.metadata['category'] = 'accessibility'
            else:
                chunk.metadata['category'] = 'general'
            
            # Add source info
            chunk.metadata['doc_title'] = filename.replace('.md', '').replace('_', ' ').title()
        
        # Create vector store with Gemini embeddings
        print("🔮 Creating vector store with Gemini embeddings...")
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=chroma_path,
            collection_metadata={"hnsw:space": "cosine"}
        )
        
        print("💾 Persisting vector store...")
        vector_store.persist()
        
        print("✅ Successfully created Lovable.dev vector database!")
        print(f"   📁 Location: {chroma_path}")
        print(f"   📄 Documents: {len(documents)}")
        print(f"   🧩 Chunks: {len(chunks)}")
        print(f"   🔮 Embeddings: Google Gemini (models/embedding-001)")
        
        # Test the database
        print("\n🔍 Testing vector database...")
        test_query = "responsive design best practices"
        results = vector_store.similarity_search(test_query, k=3)
        
        print(f"Test query: '{test_query}'")
        print(f"Retrieved {len(results)} relevant chunks:")
        
        for i, result in enumerate(results, 1):
            category = result.metadata.get('category', 'unknown')
            source = result.metadata.get('doc_title', 'unknown')
            content_preview = result.page_content[:100].replace('\n', ' ')
            print(f"  {i}. [{category}] {source}: {content_preview}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating vector database: {e}")
        print("Make sure you have set your GOOGLE_API_KEY in the .env file")
        return False

def main():
    """Main function to create the database"""
    success = create_lovable_database_gemini()
    if success:
        print("\n🎉 Database creation completed successfully!")
        print("You can now use the Gemini-powered prompt generator.")
    else:
        print("\n💥 Database creation failed!")
        print("Please check the error messages above.")

if __name__ == "__main__":
    main()
