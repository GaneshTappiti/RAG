"""
RAG System Query Interface with Gemini
Author: Ganesh Tappiti
Description: Queries the ChromaDB vector database using RAG pipeline with Google Gemini
"""

"""
RAG System Query Interface with Gemini
Author: Ganesh Tappiti
Description: Queries the ChromaDB vector database using RAG pipeline with Google Gemini
"""

import argparse
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set Google API key in environment for langchain-google-genai to use
os.environ['GOOGLE_API_KEY'] = os.environ.get('GOOGLE_API_KEY', '')

CHROMA_PATH = "chroma_gemini"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    # Prepare the DB with Google Gemini embeddings.
    embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < 0.3:
        print(f"Unable to find matching results.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    # Use Google Gemini for chat completion
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1)
    response = model.invoke(prompt)
    response_text = response.content

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)


if __name__ == "__main__":
    main()
