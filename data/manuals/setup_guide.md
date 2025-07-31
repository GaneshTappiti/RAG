# Technical Manual: RAG System Setup

## Overview

This manual covers the setup and configuration of a Retrieval-Augmented Generation (RAG) system using Google Gemini API.

## Prerequisites

- Python 3.13 or higher
- Google AI Studio API key
- Virtual environment (recommended)

## Installation Steps

### Step 1: Environment Setup

Create a virtual environment:

```bash
python -m venv venv
```

### Step 2: Install Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

### Step 3: Configuration

Set up your API keys in the .env file:

```env
GOOGLE_API_KEY=your_api_key_here
```

## Usage

### Creating Database

Run the database creation script:

```bash
python create_database_gemini.py
```

### Querying Data

Query your documents:

```bash
python query_data_gemini.py "Your question here"
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **API Key Errors**: Verify your Google API key is correct
3. **File Not Found**: Check file paths and permissions

### Performance Tips

- Use smaller chunk sizes for better precision
- Adjust similarity thresholds based on your needs
- Monitor API usage to stay within limits
