
import os
import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

def main():
    print("--- Starting RAG Demo ---")

    # 1. Setup Embeddings (Local, no API key needed)
    print("Initializing Embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 2. Setup Vector Store (Chroma)
    # Using a local persistent directory or ephemeral
    # For demo, ephemeral client passed to LangChain wrapper is easiest, 
    # or just let LangChain manage it. We'll use a local ./chroma_db dir for persistence.
    print("Initializing Chroma Vector Store...")
    vector_store = Chroma(
        collection_name="rag_demo_collection",
        embedding_function=embeddings,
        persist_directory="./chroma_db"  # Saves to disk
    )

    # 3. Create Sample Documents
    docs = [
        Document(page_content="The capital of France is Paris.", metadata={"source": "geography"}),
        Document(page_content="The capital of Germany is Berlin.", metadata={"source": "geography"}),
        Document(page_content="Chroma is an open-source vector database.", metadata={"source": "tech"}),
        Document(page_content="LangChain is a framework for developing applications powered by language models.", metadata={"source": "tech"}),
    ]

    # 4. Ingest Documents
    print(f"Adding {len(docs)} documents to the store...")
    vector_store.add_documents(documents=docs)
    print("Documents added.")

    # 5. Retrieval Loop
    queries = [
        "What is Chroma?",
        "Tell me about European capitals.",
        "What is LangChain?"
    ]

    print("\n--- Testing Retrieval ---")
    for query in queries:
        print(f"\nQuery: {query}")
        results = vector_store.similarity_search(query, k=2)
        for i, res in enumerate(results):
            print(f"  Result {i+1}: {res.page_content} (Source: {res.metadata.get('source')})")

    # Clean up (optional, to keep demo repeatable without duplicates if run multiple times)
    # vector_store.delete_collection() 
    # print("\nCollection cleaned up.")

if __name__ == "__main__":
    main()
