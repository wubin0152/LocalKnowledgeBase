from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import file_router
from app.schemas import HealthResponse
from app.utils.logger import logger

app = FastAPI(
    title="Knowledge Base API",
    description="知识库后端服务，提供文件上传和管理功能",
    version="1.0.0"
)

# 配置 CORS（允许前端访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse, tags=["健康检查"])
async def root():
    """根路径健康检查"""
    logger.info("Root endpoint accessed")
    return HealthResponse()


@app.get("/health", response_model=HealthResponse, tags=["健康检查"])
async def health_check():
    """健康检查端点"""
    logger.info("Health check performed")
    return HealthResponse()


# 注册路由
app.include_router(file_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
