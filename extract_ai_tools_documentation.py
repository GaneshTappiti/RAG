#!/usr/bin/env python3
"""
Extract and organize AI tool documentation from the external repository
into the organized data structure for the RAG system.

This script processes the system prompts and documentation from:
https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools

Author: Ganesh Tappiti
"""

import os
import shutil
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AIToolsDocumentationExtractor:
    def __init__(self, source_dir: str, target_dir: str):
        """
        Initialize the extractor with source and target directories.
        
        Args:
            source_dir: Path to external_ai_tools_data directory
            target_dir: Path to data directory where organized docs will be stored
        """
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        
        # Mapping of source folders to target folder names
        self.folder_mapping = {
            "Lovable": "lovable_docs",
            "Cursor Prompts": "cursor_docs", 
            "v0 Prompts and Tools": "v0_docs",
            "Devin AI": "devin_docs",
            "Replit": "replit_docs",
            "Windsurf": "windsurf_docs",
            "VSCode Agent": "vscode_docs",
            "Same.dev": "same_docs",
            "Manus Agent Tools & Prompt": "manus_docs",
            "Trae": "trae_docs",
            "Cluely": "cluely_docs",
            "Perplexity": "perplexity_docs",
            "Xcode": "xcode_docs",
            "-Spawn": "spawn_docs",
            "Orchids.app": "orchids_docs",
            "Warp.dev": "warp_docs",
            "dia": "dia_docs",
            "Junie": "junie_docs",
            "Kiro": "kiro_docs",
            "Z.ai Code": "zai_docs",
            "Open Source prompts": "opensource_docs"
        }
        
        # File types to extract
        self.supported_extensions = {'.txt', '.md', '.yaml', '.yml', '.json', '.py', '.js', '.ts'}
        
    def create_target_directories(self):
        """Create target directories if they don't exist."""
        for target_folder in self.folder_mapping.values():
            target_path = self.target_dir / target_folder
            target_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {target_path}")
    
    def extract_tool_documentation(self) -> Dict[str, List[str]]:
        """
        Extract documentation from each AI tool folder.
        
        Returns:
            Dictionary mapping tool names to lists of extracted files
        """
        extracted_files = {}
        
        for source_folder, target_folder in self.folder_mapping.items():
            source_path = self.source_dir / source_folder
            target_path = self.target_dir / target_folder
            
            if not source_path.exists():
                logger.warning(f"Source folder not found: {source_path}")
                continue
            
            logger.info(f"Processing {source_folder} -> {target_folder}")
            extracted_files[target_folder] = []
            
            # Extract files from the source folder
            for file_path in source_path.rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in self.supported_extensions:
                    # Create relative path structure in target
                    rel_path = file_path.relative_to(source_path)
                    target_file_path = target_path / rel_path
                    
                    # Create parent directories if needed
                    target_file_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    try:
                        # Copy the file
                        shutil.copy2(file_path, target_file_path)
                        extracted_files[target_folder].append(str(rel_path))
                        logger.info(f"  Extracted: {rel_path}")
                    except Exception as e:
                        logger.error(f"  Failed to copy {file_path}: {e}")
        
        return extracted_files
    
    def create_extraction_summary(self, extracted_files: Dict[str, List[str]]):
        """Create a summary report of extracted files."""
        summary_path = self.target_dir / "extraction_summary.md"
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("# AI Tools Documentation Extraction Summary\n\n")
            f.write(f"Extracted from: {self.source_dir}\n")
            f.write(f"Target directory: {self.target_dir}\n\n")
            
            total_files = sum(len(files) for files in extracted_files.values())
            f.write(f"**Total files extracted:** {total_files}\n\n")
            
            for tool_folder, files in extracted_files.items():
                f.write(f"## {tool_folder.replace('_docs', '').title()}\n")
                f.write(f"**Files extracted:** {len(files)}\n\n")
                
                if files:
                    for file_name in sorted(files):
                        f.write(f"- `{file_name}`\n")
                    f.write("\n")
                else:
                    f.write("No files found.\n\n")
        
        logger.info(f"Created extraction summary: {summary_path}")
    
    def create_tool_index(self, extracted_files: Dict[str, List[str]]):
        """Create an index of all AI tools and their documentation."""
        index_path = self.target_dir / "ai_tools_index.json"
        
        tool_index = {
            "extraction_date": datetime.now().isoformat(),
            "source_repository": "https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools",
            "tools": {}
        }
        
        for tool_folder, files in extracted_files.items():
            tool_name = tool_folder.replace('_docs', '')
            tool_index["tools"][tool_name] = {
                "folder": tool_folder,
                "file_count": len(files),
                "files": files,
                "primary_files": self._identify_primary_files(files)
            }
        
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(tool_index, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Created tool index: {index_path}")
    
    def _identify_primary_files(self, files: List[str]) -> List[str]:
        """Identify primary documentation files for a tool."""
        primary_files = []
        
        # Look for common primary file patterns
        priority_patterns = [
            'prompt.txt', 'prompt.md', 'system.txt', 'system.md',
            'readme.md', 'readme.txt', 'agent.txt', 'agent.md',
            'instructions.txt', 'instructions.md'
        ]
        
        for pattern in priority_patterns:
            for file_name in files:
                if file_name.lower().endswith(pattern.lower()):
                    primary_files.append(file_name)
        
        return primary_files
    
    def run_extraction(self):
        """Run the complete extraction process."""
        logger.info("Starting AI tools documentation extraction...")
        
        # Verify source directory exists
        if not self.source_dir.exists():
            raise FileNotFoundError(f"Source directory not found: {self.source_dir}")
        
        # Create target directories
        self.create_target_directories()
        
        # Extract documentation
        extracted_files = self.extract_tool_documentation()
        
        # Create summary and index
        self.create_extraction_summary(extracted_files)
        self.create_tool_index(extracted_files)
        
        total_files = sum(len(files) for files in extracted_files.values())
        logger.info(f"Extraction completed! {total_files} files extracted across {len(extracted_files)} tools.")
        
        return extracted_files


def main():
    """Main execution function."""
    
    # Set up paths
    base_dir = Path(__file__).parent
    source_dir = base_dir / "external_ai_tools_data"
    target_dir = base_dir / "data"
    
    # Initialize and run extractor
    extractor = AIToolsDocumentationExtractor(str(source_dir), str(target_dir))
    
    try:
        extracted_files = extractor.run_extraction()
        
        print("\n" + "="*60)
        print("EXTRACTION COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"Source: {source_dir}")
        print(f"Target: {target_dir}")
        print(f"Total tools processed: {len(extracted_files)}")
        print(f"Total files extracted: {sum(len(files) for files in extracted_files.values())}")
        print("\nCheck 'extraction_summary.md' for detailed results.")
        
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise


if __name__ == "__main__":
    main()
