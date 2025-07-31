# RAG System with LangChain

A Retrieval Augmented Generation (RAG) system using LangChain, ChromaDB, and OpenAI embeddings. This project demonstrates how to create a question-answering system over documents.

Created by **Ganesh Tappiti**

## Features

- Document loading and processing with Unstructured
- Text chunking with LangChain's RecursiveCharacterTextSplitter
- Vector embeddings using OpenAI's text-embedding-ada-002
- Vector storage with ChromaDB
- Question answering with RAG pipeline
- Embedding comparison utilities

## Prerequisites

- Python 3.13.5
- OpenAI API key
- Microsoft Visual C++ Build Tools (Windows only)

## Installation

### For Windows Users

1. **Install Microsoft Visual C++ Build Tools** (if not already installed)
   - Follow the [Windows Compilers guide](https://wiki.python.org/moin/WindowsCompilers)
   - Set the environment variable path as instructed

2. **Clone this repository**

   ```bash
   git clone https://github.com/GaneshTappiti/RAG.git
   cd RAG
   ```

3. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

4. **Install onnxruntime first** (Windows requirement)

   ```bash
   pip install onnxruntime
   ```

5. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   pip install "unstructured[md]"
   ```

### For macOS Users

1. **Clone this repository**

   ```bash
   git clone https://github.com/GaneshTappiti/RAG.git
   cd RAG
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install onnxruntime via conda** (recommended)

   ```bash
   conda install onnxruntime -c conda-forge
   ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   pip install "unstructured[md]"
   ```

## Configuration

1. **Set up OpenAI API Key**

   Create a `.env` file in the project root:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   Get your API key from: <https://platform.openai.com/api-keys>

## Usage

1. **Create the database**

   ```bash
   python create_database.py
   ```

   This will:
   - Load documents from the `data/books/` directory
   - Split text into chunks
   - Generate embeddings using OpenAI
   - Store vectors in ChromaDB

2. **Query the database**

   ```bash
   python query_data.py "How does Alice meet the Mad Hatter?"
   ```

3. **Compare embeddings**

   ```bash
   python compare_embeddings.py
   ```

## Project Structure

```text
RAG/
├── venv/                    # Virtual environment
├── .env                     # Environment variables (create this)
├── requirements.txt         # Python dependencies
├── create_database.py       # Creates the ChromaDB vector database
├── query_data.py           # Queries the database with RAG
├── compare_embeddings.py   # Compares different embedding approaches
├── README.md               # This file
├── chroma/                 # ChromaDB storage (created after running create_database.py)
└── data/
    └── books/
        └── alice_in_wonderland.md  # Sample document
```

## Dependencies

- **langchain**: Framework for developing LLM applications
- **langchain-community**: Community integrations for LangChain
- **langchain-openai**: OpenAI integrations for LangChain
- **chromadb**: Vector database for embeddings
- **openai**: OpenAI Python client
- **unstructured**: Document loading and processing
- **tiktoken**: Token counting for OpenAI models
- **python-dotenv**: Environment variable management

## Troubleshooting

### Python 3.13 Compatibility

This project has been updated to work with Python 3.13. The requirements.txt uses flexible version constraints (>=) instead of exact versions to ensure compatibility.

### Windows Installation Issues

- Ensure Microsoft Visual C++ Build Tools are installed
- Install onnxruntime before other dependencies
- Use PowerShell with execution policy that allows script execution

### macOS Installation Issues

- Use conda to install onnxruntime: `conda install onnxruntime -c conda-forge`
- Ensure Xcode command line tools are installed: `xcode-select --install`

## About This Project

This RAG (Retrieval Augmented Generation) system was developed by **Ganesh Tappiti** to demonstrate practical implementation of question-answering over documents using modern AI technologies.

## License

This project is developed and maintained by **Ganesh Tappiti**. Feel free to use it for educational and personal purposes.
