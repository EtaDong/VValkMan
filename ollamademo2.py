from langchain_postgres import PGVector
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

# 1. Connection String
CONNECTION_STRING = "postgresql+psycopg://myuser:mypassword@localhost:5432/vector_db"

# 2. init embeding model
embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")

# 3. create vector store collection is like a table
vector_store = PGVector(
    embeddings=embeddings,
    collection_name="my_knowledge_base",
    connection=CONNECTION_STRING,
    use_jsonb=True,
)

# 4. add doc
docs = [
    Document(
        page_content="Postgres 配合 pgvector 是企业级 RAG 的首选。",
        metadata={"category": "database"},
    ),
]
vector_store.add_documents(docs)

# 5. Filter Retrieval
results = vector_store.similarity_search(
    "哪个数据库适合企业 RAG？", k=1, filter={"category": "database"}
)

print(results[0].page_content)
