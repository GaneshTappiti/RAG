# Google Gemini Integration Guide

This guide explains how to use Google Gemini API instead of OpenAI for your RAG system.

## 🔧 Setup Instructions

### 1. Get Google AI Studio API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click on "Get API Key"
4. Create a new API key or use an existing one
5. Copy your API key

### 2. Update Environment Variables

Create or update your `.env` file:

```env
# Google Gemini API Configuration
GOOGLE_API_KEY=your_google_api_key_here

# OpenAI API Configuration (optional, for comparison)
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Install Required Packages

The required packages have been added to `requirements.txt`. Install them:

```bash
pip install google-generativeai langchain-google-genai
```

## 🚀 Using Google Gemini

### Creating the Vector Database with Gemini Embeddings

Use the new `create_database_gemini.py` script:

```bash
python create_database_gemini.py
```

This creates a vector database using Google's `models/embedding-001` embedding model.

### Querying with Gemini Chat

Use the new `query_data_gemini.py` script:

```bash
python query_data_gemini.py "How does Alice meet the Mad Hatter?"
```

This uses:

- Google Gemini embeddings for similarity search
- Gemini Pro model for generating responses

### Comparing Embeddings

Use the new `compare_embeddings_gemini.py` script:

```bash
python compare_embeddings_gemini.py
```

## 📊 Key Differences: OpenAI vs Google Gemini

| Feature | OpenAI | Google Gemini |
|---------|--------|---------------|
| **Embedding Model** | text-embedding-ada-002 | models/embedding-001 |
| **Chat Model** | gpt-3.5-turbo/gpt-4 | gemini-pro |
| **Vector Dimensions** | 1536 | 768 |
| **Cost** | Pay per token | Free tier + pay per token |
| **Speed** | Fast | Fast |
| **Context Length** | Varies by model | 30,720 tokens (Gemini Pro) |

## 🔄 File Mapping

| Original (OpenAI) | New (Gemini) | Purpose |
|-------------------|--------------|---------|
| `create_database.py` | `create_database_gemini.py` | Create vector database |
| `query_data.py` | `query_data_gemini.py` | Query the RAG system |
| `compare_embeddings.py` | `compare_embeddings_gemini.py` | Compare embeddings |

## 💡 Usage Tips

### 1. Database Storage

- OpenAI version stores in `chroma/` directory
- Gemini version stores in `chroma_gemini/` directory
- This allows you to compare both approaches side by side

### 2. Model Selection

You can use different Gemini models:

```python
# For embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# For chat (choose one)
model = ChatGoogleGenerativeAI(model="gemini-pro")          # Standard
model = ChatGoogleGenerativeAI(model="gemini-pro-vision")   # With vision
```

### 3. Temperature Control

Control response creativity:

```python
model = ChatGoogleGenerativeAI(
    model="gemini-pro", 
    temperature=0.1  # Lower = more focused, Higher = more creative
)
```

## 🔍 Example Usage

**Create the Gemini database:**

```bash
python create_database_gemini.py
```

**Ask questions:**

```bash
python query_data_gemini.py "What is the relationship between Alice and the Cheshire Cat?"
```

**Compare with OpenAI (if you have both API keys):**

```bash
python query_data.py "What is the relationship between Alice and the Cheshire Cat?"
```

## 🚨 Troubleshooting

### API Key Issues

- Ensure your `GOOGLE_API_KEY` is correctly set in the `.env` file
- Check that your Google AI Studio API key is active
- Verify you have quota remaining

### Import Errors

- Make sure you've installed the required packages
- Activate your virtual environment before running scripts

### Rate Limiting

- Google Gemini has rate limits in the free tier
- Consider adding delays between requests if needed

## 📈 Performance Considerations

### Vector Dimensions

- Gemini embeddings are 768-dimensional vs OpenAI's 1536
- This means Gemini uses about half the storage space
- Performance differences depend on your specific use case

### Speed Comparison

Both APIs are generally fast, but you can test with your specific data:

```bash
# Time the database creation
time python create_database.py        # OpenAI
time python create_database_gemini.py # Gemini

# Time queries
time python query_data.py "test question"
time python query_data_gemini.py "test question"
```

This integration gives you the flexibility to use Google's powerful Gemini models for your RAG system while maintaining compatibility with your existing OpenAI setup!
