# Design a simple RESTful API endpoint in FastAPI (or your preferred framework) that accepts a JSON payload, 
# query database table and get the result it,  -> query
# and convert result as JSON,  -> table -> json | sqlachemy
# post the database result to another API endpoint,  -> post 
# convert the json response to a flat strcutre and write into a database table. -> to_json 
 
# uv add dev

from pydantic import(BaseMode)

from psycpg import conneciton

from dotenv import dot_env

from fastapi import FastAPI

app = FastAPI(title="demo")

import logging
logging.config()

# 参数
dot_env()


# seperate file  -> config.py
class connection:
    def __init__():
        pass # 数据库连接


# model.py
class smaple_data(BaseMode):
    user: str
    age:  int

class stucut_date(BaseMode):
    pass

def cover_date() -> stucut_date:
    pass

@app.get("/")
async def root():
    return {"status": "Health"}

# query
@app.get("/data/get")
async def get_data(query) -> None:
    conn = connection()
    with conn as c:
        result = c.query
    format_result= cover_date(result)
    return format_result
    

# post the database result to another API endpoint,  -> post 
# convert the json response to a flat strcutre and write into a database table. -> to_json 
@app.post("/data/trans")
async def post_data(in_data: stucut_date):
    await call_api()

@app.post("/data/save")
async def save_data(in_data: stucut_date):
    conn = connection()
    with conn as c:
        save_data(in_data)
    
@app.post("/query/data")
async def query_data(query : str):
    await get_data(query)
    await post_data()
    await save_data()


async def call_api():
    print("call another API endpoint ")



import httpx
import logging
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from schemas import SampleData, FlatData

# 初始化配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Data Transformer Demo")

# 数据库配置 (异步引擎)
DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/db"
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# 获取数据库连接的依赖
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/health")
async def root():
    return {"status": "Health"}

# 核心业务逻辑接口
@app.post("/query-and-sync")
async def query_and_sync(query_user: str, db: AsyncSession = Depends(get_db)):
    """
    1. 查询数据库 -> 2. Post 到外部 API -> 3. 数据打平 -> 4. 存回数据库
    """
    
    # --- Step 1: Query Database ---
    try:
        # 使用 SQLAlchemy 异步查询
        sql = text("SELECT username, age FROM users WHERE username = :u")
        result = await db.execute(sql, {"u": query_user})
        row = result.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        
        db_data = {"user": row[0], "age": row[1]}
        logger.info(f"Step 1: Get DB Result -> {db_data}")

        # --- Step 2: Post to External API ---
        async with httpx.AsyncClient() as client:
            # 模拟 Post 数据库结果到另一个端点
            response = await client.post(
                "https://api.example.com/process", 
                json=db_data,
                timeout=5.0
            )
            response.raise_for_status()
            api_result = response.json() # 假设返回 {"status": "ok", "meta": {"code": 200}}
        
        # --- Step 3: Convert to Flat Structure (数据打平) ---
        # 手动提取嵌套字段并组合
        flat_record = FlatData(
            user_name=db_data["user"],
            user_age=db_data["age"],
            api_status=api_result.get("status", "unknown")
        )

        # --- Step 4: Write back to Database ---
        insert_sql = text("""
            INSERT INTO processed_logs (user_name, user_age, api_status) 
            VALUES (:name, :age, :status)
        """)
        await db.execute(insert_sql, {
            "name": flat_record.user_name,
            "age": flat_record.user_age,
            "status": flat_record.api_status
        })
        await db.commit() # 异步提交事务

        return {"message": "Sync successful", "data": flat_record}

    except Exception as e:
        await db.rollback()
        logger.error(f"Error during sync: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))






