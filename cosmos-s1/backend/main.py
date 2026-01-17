import json
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

app = FastAPI(
    title="cosmos-s1",
    description="cosmos-s1",
    version="0.0.1",
    openapi_url="/openapi.json",
    docs_url="/docs",
)

# 配置允许跨域的源
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/stream")
async def stream_fix():
    async def event_generator():
        # 模拟 LangChain chain.astream 的输出过程
        tokens = ["SELECT", " * ", "FROM", " users ", "WHERE", " id", " = ", "1;"]
        for token in tokens:
            await asyncio.sleep(0.2)  # 模拟网络/推理延迟
            # 格式：data: {json}\n\n (这是标准 SSE 协议)
            yield f"data: {json.dumps({'token': token})}\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")