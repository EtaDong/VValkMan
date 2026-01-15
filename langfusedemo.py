import os
from langfuse.decorators import observe, langfuse_context
from mlx_lm import load, generate
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(".env")

# --- 模块化函数 1: 检索环节 ---
@observe(name="retrieval")
def retrieve_context(question):
    # 模拟检索逻辑
    docs = [{"page_content": "MLX utilizes Unified Memory to eliminate data copy between CPU and GPU."}] 
    context = "\n".join([d["page_content"] for d in docs])
    
    # v2 标准写法：更新当前 Span 的元数据
    langfuse_context.update_current_observation(
        metadata={"num_docs": len(docs), "retrieval_type": "vector_search"}
    )
    return context

# --- 模块化函数 2: 生成环节 ---
@observe(name="generation") # 移除不支持的 as_generation=True
def generate_response(prompt, model, tokenizer):
    # 执行 MLX 推理
    response = generate(model, tokenizer, prompt=prompt, max_tokens=512)
    
    # 核心修正：手动指定这是一个 Generation，并传入 Input/Output
    langfuse_context.update_current_observation(
        input=prompt,
        output=response,
        model="DeepSeek-R1-7B-MLX",
        metadata={"usage_type": "mlx_inference"}
    )
    return response

# --- 主流程 ---
@observe() 
def local_rag_with_tracing(question, model, tokenizer):
    # 设置主 Trace 的元数据
    langfuse_context.update_current_trace(
        name="Local_RAG_Query_V2", 
        user_id="user_123"
    )
    
    # 调用子函数
    context = retrieve_context(question)
    prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer:"
    response = generate_response(prompt, model, tokenizer)
    
    return response

if __name__ == "__main__":
    print("⏳ Loading MLX Model...")
    model_path = "mlx-community/DeepSeek-R1-Distill-Qwen-7B-4bit"
    model, tokenizer = load(model_path)

    print("🚀 Running RAG with Tracing...")
    try:
        ans = local_rag_with_tracing("MLX 的内存管理有什么优势？", model, tokenizer)
        print(f"\n🤖 AI 回答: {ans}")
    finally:
        print("\n📤 Syncing traces to Langfuse v2...")
        langfuse_context.flush()