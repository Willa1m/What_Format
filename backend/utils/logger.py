"""
日志系统配置模块
提供应用运行日志、错误日志、用户操作日志、处理日志
"""
import sys
import logging
from pathlib import Path
from datetime import datetime

# 日志目录
LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

try:
    from loguru import logger as _loguru_logger
    _HAS_LOGURU = True
except Exception:
    _HAS_LOGURU = False


if _HAS_LOGURU:
    logger = _loguru_logger
    # 移除默认处理器
    logger.remove()

    # 日志格式
    LOG_FORMAT = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    FILE_FORMAT = (
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
        "{level: <8} | "
        "{name}:{function}:{line} | "
        "{message}"
    )

    def setup_logger():
        """配置日志系统 (loguru)"""
        # 控制台输出 - 彩色格式
        logger.add(
            sys.stdout,
            format=LOG_FORMAT,
            level="INFO",
            colorize=True,
            filter=lambda record: record["level"].no < 40  # INFO及以下
        )

        # 控制台错误输出
        logger.add(
            sys.stderr,
            format=LOG_FORMAT,
            level="ERROR",
            colorize=True
        )

        # 应用运行日志 - 记录所有信息
        logger.add(
            LOG_DIR / "app_{time:YYYY-MM-DD}.log",
            format=FILE_FORMAT,
            level="DEBUG",
            rotation="00:00",
            retention="30 days",
            compression="zip",
            encoding="utf-8",
            enqueue=False  # Windows兼容
        )

        # 错误日志 - 只记录错误
        logger.add(
            LOG_DIR / "error_{time:YYYY-MM-DD}.log",
            format=FILE_FORMAT,
            level="ERROR",
            rotation="00:00",
            retention="90 days",
            compression="zip",
            encoding="utf-8",
            enqueue=False,
            backtrace=True,  # 包含异常追踪
            diagnose=True    # 包含诊断信息
        )

        # 用户操作日志
        logger.add(
            LOG_DIR / "user_operations_{time:YYYY-MM-DD}.log",
            format=FILE_FORMAT,
            level="INFO",
            rotation="00:00",
            retention="60 days",
            compression="zip",
            encoding="utf-8",
            enqueue=False,
            filter=lambda record: record["extra"].get("log_type") == "user_operation"
        )

        # 处理日志 - 文件处理详情
        logger.add(
            LOG_DIR / "processing_{time:YYYY-MM-DD}.log",
            format=FILE_FORMAT,
            level="DEBUG",
            rotation="00:00",
            retention="30 days",
            compression="zip",
            encoding="utf-8",
            enqueue=False,
            filter=lambda record: record["extra"].get("log_type") == "processing"
        )

        logger.info("日志系统初始化完成")
        return logger
else:
    class _SimpleLogger:
        def __init__(self):
            self._logger = logging.getLogger("whatformat")
            self._logger.setLevel(logging.INFO)
            formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

            console = logging.StreamHandler(sys.stdout)
            console.setFormatter(formatter)
            self._logger.addHandler(console)

            file_handler = logging.FileHandler(LOG_DIR / "app.log", encoding="utf-8")
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)

        def remove(self):
            return None

        def add(self, *args, **kwargs):
            return None

        def bind(self, **kwargs):
            return self

        def opt(self, **kwargs):
            return self

        def info(self, message):
            self._logger.info(message)

        def debug(self, message):
            self._logger.debug(message)

        def error(self, message):
            self._logger.error(message)

    logger = _SimpleLogger()

    def setup_logger():
        """配置日志系统 (fallback)"""
        logger.info("日志系统初始化完成 (fallback)")
        return logger


# 便捷日志函数
def log_user_operation(action: str, message: str = "", details: dict = None):
    """记录用户操作"""
    logger.bind(log_type="user_operation").info(
        f"用户操作: {action} | {message} | 详情: {details or {}}"
    )


def log_processing(stage: str, message: str, details: dict = None):
    """记录处理过程"""
    logger.bind(log_type="processing").info(
        f"[{stage}] {message} | 详情: {details or {}}"
    )


def log_error(error: Exception, context: str = ""):
    """记录错误"""
    logger.opt(exception=True).error(f"错误发生 [{context}]: {str(error)}")


# 模块加载时初始化日志
setup_logger()
