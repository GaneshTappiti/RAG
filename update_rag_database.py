#!/usr/bin/env python3
"""
Update RAG database with extracted AI tools documentation.

This script creates embeddings for the new AI tools documentation
and integrates them into the existing RAG system.

Author: Ganesh Tappiti
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
import sys

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    print("ChromaDB not installed. Installing...")
    os.system("pip install chromadb")
    import chromadb
    from chromadb.config import Settings

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AIToolsDBUpdater:
    def __init__(self, data_dir: str, db_name: str = "chroma_ai_tools"):
        """
        Initialize the database updater.
        
        Args:
            data_dir: Path to data directory with extracted documentation
            db_name: Name of the ChromaDB database
        """
        self.data_dir = Path(data_dir)
        self.db_name = db_name
        self.db_path = self.data_dir.parent / "storage" / db_name
        
        # Create storage directory if it doesn't exist
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(self.db_path),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Load tools index
        self.tools_index = self._load_tools_index()
        
        # Create collection for AI tools documentation
        self.collection = self._get_or_create_collection()
        
    def _load_tools_index(self) -> Dict:
        """Load the AI tools index."""
        index_file = self.data_dir / "ai_tools_index.json"
        if not index_file.exists():
            raise FileNotFoundError(f"Tools index not found: {index_file}")
        
        with open(index_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _get_or_create_collection(self):
        """Get or create the AI tools collection."""
        collection_name = "ai_tools_documentation"
        
        try:
            # Try to get existing collection
            collection = self.client.get_collection(collection_name)
            logger.info(f"Using existing collection: {collection_name}")
        except:
            # Create new collection
            collection = self.client.create_collection(
                name=collection_name,
                metadata={"description": "AI development tools documentation and prompts"}
            )
            logger.info(f"Created new collection: {collection_name}")
        
        return collection
    
    def process_tool_documentation(self, tool_name: str, tool_info: Dict) -> List[Dict]:
        """
        Process documentation for a single tool.
        
        Args:
            tool_name: Name of the tool
            tool_info: Tool information from index
            
        Returns:
            List of document dictionaries
        """
        documents = []
        tool_folder = self.data_dir / tool_info["folder"]
        
        for file_name in tool_info["files"]:
            file_path = tool_folder / file_name
            
            if not file_path.exists():
                logger.warning(f"File not found: {file_path}")
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Skip empty files
                if not content.strip():
                    continue
                
                # Create document
                doc = {
                    "id": f"{tool_name}_{file_name}",
                    "content": content,
                    "metadata": {
                        "tool_name": tool_name,
                        "file_name": file_name,
                        "file_path": str(file_path),
                        "tool_type": self._classify_tool_type(tool_name),
                        "file_type": self._classify_file_type(file_name, content),
                        "is_primary": file_name in tool_info.get("primary_files", []),
                        "char_count": len(content),
                        "line_count": len(content.splitlines()),
                        "source": "github_x1xhlol_system_prompts"
                    }
                }
                
                documents.append(doc)
                logger.info(f"Processed: {tool_name}/{file_name} ({len(content)} chars)")
                
            except Exception as e:
                logger.error(f"Failed to process {file_path}: {e}")
        
        return documents
    
    def _classify_tool_type(self, tool_name: str) -> str:
        """Classify the type of AI tool."""
        ide_tools = ["cursor", "vscode"]
        generators = ["lovable", "bolt", "v0", "spawn"]
        agents = ["devin", "manus", "trae", "cluely"]
        platforms = ["replit", "windsurf", "same", "orchids"]
        
        if tool_name in ide_tools:
            return "ide"
        elif tool_name in generators:
            return "code_generator"
        elif tool_name in agents:
            return "ai_agent"
        elif tool_name in platforms:
            return "development_platform"
        else:
            return "general"
    
    def _classify_file_type(self, file_name: str, content: str) -> str:
        """Classify the type of documentation file."""
        file_name_lower = file_name.lower()
        
        if "prompt" in file_name_lower:
            return "system_prompt"
        elif "tools" in file_name_lower and file_name.endswith('.json'):
            return "tool_definitions"
        elif "agent" in file_name_lower:
            return "agent_configuration"
        elif "memory" in file_name_lower:
            return "memory_system"
        elif file_name.endswith('.json'):
            return "json_configuration"
        else:
            return "documentation"
    
    def chunk_large_documents(self, documents: List[Dict], max_chunk_size: int = 8000) -> List[Dict]:
        """
        Split large documents into smaller chunks for better embedding.
        
        Args:
            documents: List of document dictionaries
            max_chunk_size: Maximum size for each chunk
            
        Returns:
            List of chunked documents
        """
        chunked_docs = []
        
        for doc in documents:
            content = doc["content"]
            
            if len(content) <= max_chunk_size:
                chunked_docs.append(doc)
                continue
            
            # Split into chunks
            lines = content.splitlines()
            current_chunk = []
            current_size = 0
            chunk_index = 0
            
            for line in lines:
                line_size = len(line) + 1  # +1 for newline
                
                if current_size + line_size > max_chunk_size and current_chunk:
                    # Save current chunk
                    chunk_content = "\\n".join(current_chunk)
                    chunk_doc = {
                        "id": f"{doc['id']}_chunk_{chunk_index}",
                        "content": chunk_content,
                        "metadata": {
                            **doc["metadata"],
                            "is_chunk": True,
                            "chunk_index": chunk_index,
                            "total_chunks": -1,  # Will be updated later
                            "char_count": len(chunk_content),
                            "line_count": len(current_chunk)
                        }
                    }
                    chunked_docs.append(chunk_doc)
                    
                    # Reset for next chunk
                    current_chunk = [line]
                    current_size = line_size
                    chunk_index += 1
                else:
                    current_chunk.append(line)
                    current_size += line_size
            
            # Save final chunk
            if current_chunk:
                chunk_content = "\\n".join(current_chunk)
                chunk_doc = {
                    "id": f"{doc['id']}_chunk_{chunk_index}",
                    "content": chunk_content,
                    "metadata": {
                        **doc["metadata"],
                        "is_chunk": True,
                        "chunk_index": chunk_index,
                        "total_chunks": chunk_index + 1,
                        "char_count": len(chunk_content),
                        "line_count": len(current_chunk)
                    }
                }
                chunked_docs.append(chunk_doc)
            
            # Update total_chunks for all chunks
            total_chunks = chunk_index + 1
            for chunk_doc in chunked_docs:
                if chunk_doc["id"].startswith(doc["id"]) and "chunk_index" in chunk_doc["metadata"]:
                    chunk_doc["metadata"]["total_chunks"] = total_chunks
            
            logger.info(f"Split {doc['id']} into {total_chunks} chunks")
        
        return chunked_docs
    
    def add_documents_to_db(self, documents: List[Dict]):
        """Add documents to the ChromaDB collection."""
        if not documents:
            logger.warning("No documents to add")
            return
        
        # Prepare data for ChromaDB
        ids = [doc["id"] for doc in documents]
        texts = [doc["content"] for doc in documents]
        metadatas = [doc["metadata"] for doc in documents]
        
        try:
            # Add documents to collection
            self.collection.add(
                ids=ids,
                documents=texts,
                metadatas=metadatas
            )
            
            logger.info(f"Added {len(documents)} documents to database")
            
        except Exception as e:
            logger.error(f"Failed to add documents to database: {e}")
            raise
    
    def update_database(self):
        """Update the database with all AI tools documentation."""
        logger.info("Starting database update...")
        
        all_documents = []
        
        # Process each tool
        for tool_name, tool_info in self.tools_index["tools"].items():
            logger.info(f"Processing {tool_name}...")
            
            # Process tool documentation
            tool_docs = self.process_tool_documentation(tool_name, tool_info)
            
            if tool_docs:
                all_documents.extend(tool_docs)
                logger.info(f"Processed {len(tool_docs)} documents for {tool_name}")
            else:
                logger.warning(f"No documents found for {tool_name}")
        
        if not all_documents:
            logger.warning("No documents to add to database")
            return
        
        # Chunk large documents
        logger.info("Chunking large documents...")
        chunked_docs = self.chunk_large_documents(all_documents)
        
        # Add to database
        logger.info(f"Adding {len(chunked_docs)} documents to database...")
        self.add_documents_to_db(chunked_docs)
        
        # Create summary
        self._create_db_summary(chunked_docs)
        
        logger.info("Database update completed successfully!")
        
        return len(chunked_docs)
    
    def _create_db_summary(self, documents: List[Dict]):
        """Create a summary of the database update."""
        summary_path = self.data_dir / "database_update_summary.md"
        
        # Analyze documents
        tool_counts = {}
        file_type_counts = {}
        total_chars = 0
        
        for doc in documents:
            tool_name = doc["metadata"]["tool_name"]
            file_type = doc["metadata"]["file_type"]
            
            tool_counts[tool_name] = tool_counts.get(tool_name, 0) + 1
            file_type_counts[file_type] = file_type_counts.get(file_type, 0) + 1
            total_chars += doc["metadata"]["char_count"]
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("# Database Update Summary\\n\\n")
            f.write(f"**Total documents added:** {len(documents)}\\n")
            f.write(f"**Total characters:** {total_chars:,}\\n")
            f.write(f"**Database path:** `{self.db_path}`\\n\\n")
            
            f.write("## Documents by Tool\\n\\n")
            for tool_name, count in sorted(tool_counts.items()):
                f.write(f"- **{tool_name.title()}:** {count} documents\\n")
            f.write("\\n")
            
            f.write("## Documents by Type\\n\\n")
            for file_type, count in sorted(file_type_counts.items()):
                f.write(f"- **{file_type.replace('_', ' ').title()}:** {count} documents\\n")
            f.write("\\n")
            
            f.write("## Usage\\n\\n")
            f.write("The database is now ready for use with your RAG system. You can:\\n\\n")
            f.write("1. Query specific tool documentation\\n")
            f.write("2. Generate prompts using AI tool best practices\\n")
            f.write("3. Search for specific features or capabilities\\n")
            f.write("4. Compare different tools and their approaches\\n\\n")
        
        logger.info(f"Created database summary: {summary_path}")
    
    def test_database(self):
        """Test the database with a sample query."""
        logger.info("Testing database with sample queries...")
        
        test_queries = [
            "How to generate React components",
            "System prompts for code generation",
            "AI agent capabilities",
            "Web development tools"
        ]
        
        for query in test_queries:
            try:
                results = self.collection.query(
                    query_texts=[query],
                    n_results=3
                )
                
                if results and 'documents' in results and results['documents']:
                    docs = results['documents']
                    if docs and len(docs) > 0 and docs[0]:
                        logger.info(f"Query: '{query}' - Found {len(docs[0])} results")
                    else:
                        logger.info(f"Query: '{query}' - No results found")
                else:
                    logger.info(f"Query: '{query}' - No results found")
                
            except Exception as e:
                logger.error(f"Query failed for '{query}': {e}")


def main():
    """Main execution function."""
    
    # Set up paths
    base_dir = Path(__file__).parent
    data_dir = base_dir / "data"
    
    # Initialize and run updater
    updater = AIToolsDBUpdater(str(data_dir))
    
    try:
        # Update database
        doc_count = updater.update_database()
        
        # Test database
        updater.test_database()
        
        print("\\n" + "="*60)
        print("DATABASE UPDATE COMPLETED!")
        print("="*60)
        print(f"Documents added: {doc_count}")
        print(f"Database path: {updater.db_path}")
        print("\\nThe RAG system is now ready to use with AI tools documentation!")
        
    except Exception as e:
        logger.error(f"Database update failed: {e}")
        raise


if __name__ == "__main__":
    main()
