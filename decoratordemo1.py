import functools
import time

# 第一层：工厂层，接收配置参数
def observe(name: str = None, as_type: str = "span"):
    # 第二层：真正的装饰器，接收被装饰的函数
    def decorator(func):
        # 使用 @functools.wraps 保证被装饰后的函数名、文档等属性不丢失
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # --- 前置动作：开始追踪 ---
            span_name = name or func.__name__
            print(f"[TRACE START] 正在监控: {span_name} | 类型: {as_type}")
            print(f"[INPUT] 位置参数: {args} | 关键字参数: {kwargs}")
            
            start_time = time.time()
            try:
                # --- 核心动作：执行原函数 ---
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                print(f"[ERROR] 函数执行崩溃: {e}")
                raise
            finally:
                # --- 后置动作：计算耗时并上传数据 ---
                duration = time.time() - start_time
                print(f"[TRACE END] {span_name} 完成，耗时: {duration:.4f}s")
                print("-" * 30)
                
        return wrapper
    return decorator

# --- 实战使用 ---

@observe(name="OpenAI_Chat_Completion", as_type="generation")
def call_llm(prompt, model="gpt-4o"):
    time.sleep(0.5) # 模拟网络延迟
    return f"Response for: {prompt}"

# 运行一下
call_llm("你好，解释一下装饰器", model="deepseek-v3")