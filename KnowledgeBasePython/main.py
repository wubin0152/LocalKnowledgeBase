import uvicorn
from app.main import app


def main():
    """启动 FastAPI 应用"""
    print("🚀 启动 Knowledge Base 后端服务...")
    print("📖 API 文档：http://localhost:8000/docs")
    print("📝 ReDoc 文档：http://localhost:8000/redoc")
    
    # 使用 uvicorn 运行应用
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
