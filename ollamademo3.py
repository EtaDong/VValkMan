from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document

# 1. 准备数据 (Prepare Raw Data)
raw_documents = [
    Document(
        page_content="DeepSeek R1 擅长逻辑推理，其训练采用了强化学习技术。",
        metadata={"source": "tech_blog"},
    ),
    Document(
        page_content="Nomic-embed-text 支持 8192 token 的上下文长度。",
        metadata={"source": "model_spec"},
    ),
]

# 2. 文档切分 (Chunking)
# chunk_size: 每一块的大小；chunk_overlap: 块与块之间的重叠，防止语义断层
text_splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)
splits = text_splitter.split_documents(raw_documents)

# 3. 初始化 Embedding (Using Nomic via Ollama)
embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")

# 4. 创建并持久化向量库 (Vector Store Creation)
# 这一步会调用 Embedding 模型将 splits 转化为向量并存入 Chroma
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="./chroma_db",  # 将数据保存在本地硬盘
)

# 5. 检索测试 (Similarity Search)
query = "Nomic 模型的上下文长度是多少？"
docs = vectorstore.similarity_search(query, k=1)  # k=1 表示找最像的那一个

print(f"检索到的内容: {docs[0].page_content}")
print(f"来源元数据: {docs[0].metadata}")
