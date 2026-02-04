"""
What Format - 简历/求职信格式转换服务
FastAPI 主入口
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from backend.config import settings
from backend.api.routes import router as api_router
from backend.utils.logger import logger, log_user_operation, log_error
from backend.utils.helpers import cleanup_temp_files


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    logger.info("=" * 50)
    logger.info(f"启动 {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"服务地址: http://{settings.HOST}:{settings.PORT}")
    logger.info("=" * 50)
    
    # 确保必要目录存在
    settings.UPLOAD_DIR.mkdir(exist_ok=True)
    settings.OUTPUT_DIR.mkdir(exist_ok=True)
    settings.LOG_DIR.mkdir(exist_ok=True)
    
    yield
    
    # 关闭时
    logger.info("正在关闭服务...")
    
    # 清理临时文件
    cleanup_temp_files(settings.UPLOAD_DIR, max_age_hours=1)
    
    logger.info("服务已关闭")


# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    description="简历/求职信模板统一格式转换服务",
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)


# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    log_error(exc, f"未处理的异常 [{request.method} {request.url.path}]")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "服务器内部错误",
            "error": str(exc) if settings.DEBUG else "请联系管理员"
        }
    )


# 请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """记录请求日志"""
    import time
    start_time = time.time()
    
    # 记录请求
    logger.debug(f"请求: {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    # 计算处理时间
    process_time = time.time() - start_time
    
    # 记录响应
    logger.debug(f"响应: {request.method} {request.url.path} - {response.status_code} ({process_time:.3f}s)")
    
    return response


# 注册API路由
app.include_router(api_router, prefix="/api", tags=["API"])


@app.get("/")
async def root():
    """API根路由（保持后端纯 API）"""
    return {"message": f"{settings.APP_NAME} API", "version": settings.APP_VERSION}


def main():
    """主函数"""
    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )


if __name__ == "__main__":
    main()
