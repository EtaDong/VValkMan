import asyncio
from typing import Optional, AsyncGenerator, List
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import select

from mcp.server.fastmcp import FastMCP

# --- 数据库配置 ---
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# 创建异步引擎和会话工厂
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# 定义数据库模型
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    role: Mapped[str]

class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float]

# --- Pydantic Models ---
class ItemCreate(BaseModel):
    name: str
    price: float

class ItemResponse(ItemCreate):
    id: int

    class Config:
        from_attributes = True

# --- FastAPI & MCP 配置 ---
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Shutdown
    await engine.dispose()

# --- FastAPI & MCP 配置 ---
app = FastAPI(title="User Data MCP Server", lifespan=lifespan)
mcp_server = FastMCP("user-manager")

# --- 修改后的 MCP Tool ---
@mcp_server.tool()
async def get_user_info(user_id: int) -> str:
    """
    根据用户 ID 获取用户的详细信息，包括姓名和权限。
    """
    # 使用异步会话查询数据库
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            return f"User with ID {user_id} not found."
        
        user_info = {"name": user.name, "role": user.role}
        return str(user_info)

# 挂载 MCP 路由
app.mount("/mcp", mcp_server.streamable_http_app())

# --- Items Endpoints ---
@app.post("/items/", response_model=ItemResponse)
async def create_item(item: ItemCreate):
    async with AsyncSessionLocal() as session:
        db_item = Item(name=item.name, price=item.price)
        session.add(db_item)
        await session.commit()
        await session.refresh(db_item)
        return db_item

@app.get("/items/", response_model=List[ItemResponse])
async def read_items(skip: int = 0, limit: int = 100):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Item).offset(skip).limit(limit))
        items = result.scalars().all()
        return items

@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Item).where(Item.id == item_id))
        item = result.scalar_one_or_none()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

# 可选：在启动时创建表（仅用于演示）
# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         # await conn.run_sync(Base.metadata.create_all)
#         pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)