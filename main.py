"""
What Format - 纯后端 API 入口
前后端分离：仅暴露数据接口，不提供页面渲染
"""
from backend.main import app


if __name__ == "__main__":
    import uvicorn
    from backend.config import settings

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
