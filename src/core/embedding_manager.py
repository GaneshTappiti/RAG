"""
Embedding Manager with ChromaDB Integration
Supports Google Gemini embeddings with ChromaDB vector database
"""

import os
import sys
from typing import Optional, Dict, Any, List, Union
from enum import Enum
from dataclasses import dataclass
from pathlib import Path

try:
    import chromadb
    from chromadb.config import Settings
    from chromadb.utils import embedding_functions
    CHROMADB_AVAILABLE = True
except ImportError:
    print("ChromaDB not installed. Please run: pip install chromadb")
    chromadb = None
    Settings = None
    embedding_functions = None
    CHROMADB_AVAILABLE = False

try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
except ImportError:
    print("Google Generative AI not installed. Please run: pip install langchain-google-genai")
    GoogleGenerativeAIEmbeddings = None

class EmbeddingProvider(Enum):
    """Supported embedding providers"""
    GOOGLE_GEMINI = "google_gemini"

@dataclass
class EmbeddingConfig:
    """Configuration for embedding models"""
    provider: EmbeddingProvider
    model_name: str
    api_key: Optional[str] = None
    batch_size: int = 100
    task_type: str = "retrieval_document"

@dataclass 
class ChromaDBConfig:
    """Configuration for ChromaDB"""
    persist_directory: str = "storage/chroma_db"
    collection_name: str = "ai_tools_documentation"
    distance_function: str = "cosine"
    
class ChromaEmbeddingManager:
    """Manager for ChromaDB with Google Gemini embeddings"""
    
    # Available models for Gemini
    GEMINI_MODELS = [
        "models/embedding-001",
        "models/text-embedding-004"
    ]
    
    def __init__(self, 
                 embedding_config: Optional[EmbeddingConfig] = None,
                 chroma_config: Optional[ChromaDBConfig] = None):
        """
        Initialize ChromaDB embedding manager
        
        Args:
            embedding_config: Embedding configuration. If None, uses default Gemini config
            chroma_config: ChromaDB configuration. If None, uses default config
        """
        if embedding_config is None:
            embedding_config = self.get_default_gemini_config()
        
        if chroma_config is None:
            chroma_config = ChromaDBConfig()
            
        self.embedding_config = embedding_config
        self.chroma_config = chroma_config
        self._embedding_model = None
        self._chroma_client = None
        self._collection = None
        
        # Validate ChromaDB availability
        if chromadb is None:
            raise ImportError("ChromaDB not available. Please install: pip install chromadb")
            
        # Validate Gemini availability
        if GoogleGenerativeAIEmbeddings is None:
            raise ImportError("Google Generative AI not available. Please install: pip install langchain-google-genai")
    
    @classmethod
    def get_default_gemini_config(cls) -> EmbeddingConfig:
        """Get default Google Gemini embedding configuration"""
        return EmbeddingConfig(
            provider=EmbeddingProvider.GOOGLE_GEMINI,
            model_name="models/embedding-001",
            api_key=os.getenv("GOOGLE_API_KEY"),
            task_type="retrieval_document"
        )
    
    def get_embedding_model(self):
        """
        Get the configured embedding model
        
        Returns:
            Embedding model instance
        """
        if self._embedding_model is None:
            self._embedding_model = self._create_gemini_embeddings()
        
        return self._embedding_model
    
    def get_chroma_client(self):
        """
        Get ChromaDB client
        
        Returns:
            ChromaDB client instance
        """
        if not CHROMADB_AVAILABLE or chromadb is None or Settings is None:
            raise ImportError("ChromaDB is not available. Please install it with: pip install chromadb")
            
        if self._chroma_client is None:
            # Create persist directory if it doesn't exist
            persist_dir = Path(self.chroma_config.persist_directory)
            persist_dir.mkdir(parents=True, exist_ok=True)
            
            self._chroma_client = chromadb.PersistentClient(
                path=str(persist_dir),
                settings=Settings(anonymized_telemetry=False)
            )
            
        return self._chroma_client
    
    def get_collection(self, reset: bool = False):
        """
        Get or create ChromaDB collection
        
        Args:
            reset: Whether to reset (delete and recreate) the collection
            
        Returns:
            ChromaDB collection
        """
        client = self.get_chroma_client()
        
        if reset and self._collection is not None:
            try:
                client.delete_collection(self.chroma_config.collection_name)
                self._collection = None
            except Exception as e:
                print(f"Warning: Could not delete collection: {e}")
        
        if self._collection is None:
            try:
                # Try to get existing collection
                self._collection = client.get_collection(self.chroma_config.collection_name)
            except:
                # Create new collection
                self._collection = client.create_collection(
                    name=self.chroma_config.collection_name,
                    metadata={
                        "description": "AI development tools documentation with Gemini embeddings",
                        "embedding_provider": self.embedding_config.provider.value,
                        "embedding_model": self.embedding_config.model_name,
                        "distance_function": self.chroma_config.distance_function
                    }
                )
                
        return self._collection
    
    def _create_gemini_embeddings(self):
        """Create Google Gemini embedding model"""
        # Validate API key
        api_key = self.embedding_config.api_key or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "Google API key not found. Set GOOGLE_API_KEY environment variable "
                "or provide api_key in config"
            )
        
        # Create Gemini embeddings
        if GoogleGenerativeAIEmbeddings is None:
            raise ImportError("GoogleGenerativeAIEmbeddings not available")
            
        return GoogleGenerativeAIEmbeddings(
            model=self.embedding_config.model_name,
            task_type=self.embedding_config.task_type
        )
    
    def add_documents(self, 
                     documents: List[str],
                     metadatas: Optional[List[Dict[str, Union[str, int, float, bool]]]] = None,
                     ids: Optional[List[str]] = None) -> None:
        """
        Add documents to ChromaDB collection
        
        Args:
            documents: List of document texts
            metadatas: Optional list of metadata dictionaries
            ids: Optional list of document IDs
        """
        collection = self.get_collection()
        embedding_model = self.get_embedding_model()
        
        # Generate embeddings
        embeddings = embedding_model.embed_documents(documents)
        
        # Generate IDs if not provided
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
        
        # Add to collection (ChromaDB handles the type conversion)
        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,  # type: ignore
            metadatas=metadatas  # type: ignore
        )
    
    def add_documents_batch(self,
                           documents: List[str],
                           metadatas: Optional[List[Dict[str, Union[str, int, float, bool]]]] = None,
                           ids: Optional[List[str]] = None,
                           batch_size: Optional[int] = None) -> None:
        """
        Add documents in batches to ChromaDB collection
        
        Args:
            documents: List of document texts
            metadatas: Optional list of metadata dictionaries  
            ids: Optional list of document IDs
            batch_size: Batch size for processing (uses config default if None)
        """
        if batch_size is None:
            batch_size = self.embedding_config.batch_size
            
        total_docs = len(documents)
        
        for i in range(0, total_docs, batch_size):
            batch_docs = documents[i:i + batch_size]
            batch_metas = metadatas[i:i + batch_size] if metadatas else None
            batch_ids = ids[i:i + batch_size] if ids else None
            
            self.add_documents(batch_docs, batch_metas, batch_ids)
    
    def query(self, 
              query_text: str,
              n_results: int = 5,
              where: Optional[Dict[str, Any]] = None):
        """
        Query the ChromaDB collection
        
        Args:
            query_text: Query text
            n_results: Number of results to return
            where: Optional metadata filter
            
        Returns:
            Query results
        """
        collection = self.get_collection()
        embedding_model = self.get_embedding_model()
        
        # Generate query embedding
        query_embedding = embedding_model.embed_query(query_text)
        
        # Query collection
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where
        )
        
        return results  # type: ignore
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the ChromaDB collection"""
        collection = self.get_collection()
        
        return {
            "name": collection.name,
            "count": collection.count(),
            "metadata": collection.metadata,
            "embedding_provider": self.embedding_config.provider.value,
            "embedding_model": self.embedding_config.model_name,
            "persist_directory": self.chroma_config.persist_directory
        }
    
    @classmethod
    def list_available_models(cls) -> List[str]:
        """List available Gemini models"""
        return cls.GEMINI_MODELS
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a query text"""
        model = self.get_embedding_model()
        return model.embed_query(text)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple documents"""
        model = self.get_embedding_model()
        return model.embed_documents(texts)


def create_chroma_embedding_manager(model_name: Optional[str] = None,
                                   collection_name: Optional[str] = None,
                                   persist_directory: Optional[str] = None) -> ChromaEmbeddingManager:
    """
    Convenience function to create ChromaDB embedding manager
    
    Args:
        model_name: Optional Gemini model name override
        collection_name: Optional collection name override
        persist_directory: Optional persist directory override
        
    Returns:
        ChromaEmbeddingManager instance
    """
    
    # Create embedding config
    embedding_config = ChromaEmbeddingManager.get_default_gemini_config()
    if model_name:
        embedding_config.model_name = model_name
    
    # Create ChromaDB config
    chroma_config = ChromaDBConfig()
    if collection_name:
        chroma_config.collection_name = collection_name
    if persist_directory:
        chroma_config.persist_directory = persist_directory
    
    return ChromaEmbeddingManager(embedding_config, chroma_config)


# For backward compatibility
def create_embedding_manager(provider: str = "google_gemini", 
                           model_name: Optional[str] = None) -> ChromaEmbeddingManager:
    """
    Backward compatibility function
    
    Args:
        provider: Only "google_gemini" is supported now
        model_name: Optional model name override
        
    Returns:
        ChromaEmbeddingManager instance
    """
    
    if provider != "google_gemini":
        raise ValueError(f"Only 'google_gemini' provider is supported, got: {provider}")
    
    return create_chroma_embedding_manager(model_name=model_name)


# Example usage and testing
if __name__ == "__main__":
    import sys
    
    test_text = "This is a test document for embedding."
    
    # Test Google Gemini embeddings with ChromaDB
    try:
        print("Testing Google Gemini embeddings with ChromaDB...")
        gemini_manager = create_chroma_embedding_manager()
        
        # Test embedding
        embedding = gemini_manager.embed_query(test_text)
        
        print(f"✓ Gemini embedding successful!")
        print(f"  Model: {gemini_manager.embedding_config.model_name}")
        print(f"  Embedding dimension: {len(embedding)}")
        print(f"  First 5 values: {embedding[:5]}")
        
        # Test ChromaDB integration
        print("\nTesting ChromaDB integration...")
        
        # Add test document
        test_docs = [test_text, "Another test document about AI tools."]
        test_metadata = [{"type": "test", "index": 0}, {"type": "test", "index": 1}]
        test_ids = ["test_1", "test_2"]
        
        gemini_manager.add_documents(test_docs, test_metadata, test_ids)
        
        # Query the collection
        results = gemini_manager.query("test document", n_results=2)
        
        print(f"✓ ChromaDB integration successful!")
        print(f"  Collection: {gemini_manager.chroma_config.collection_name}")
        print(f"  Documents added: {len(test_docs)}")
        try:
            if results and hasattr(results, 'get') and results.get('documents'):
                docs = results.get('documents', [[]])
                if docs and len(docs) > 0:
                    print(f"  Query results: {len(docs[0])} documents found")
                else:
                    print(f"  Query completed - no documents found")
            else:
                print(f"  Query completed successfully")
        except:
            print(f"  Query completed successfully")
        
        # Show collection info
        info = gemini_manager.get_collection_info()
        print(f"  Collection count: {info['count']}")
        
    except Exception as e:
        print(f"✗ Gemini ChromaDB integration failed: {e}")
        print("  Make sure GOOGLE_API_KEY is set in your environment")
        import traceback
        traceback.print_exc()



