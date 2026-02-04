"""
配置管理模块
"""
import os
from pathlib import Path
from typing import List, Optional


# 基础路径
_BASE_DIR = Path(__file__).parent.parent


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _env_path(name: str, default: Path) -> Path:
    value = os.getenv(name)
    if value:
        return Path(value)
    return default


class Settings:
    """应用配置（轻量环境版，避免额外依赖）"""

    def __init__(self):
        # 应用基本配置
        self.APP_NAME = os.getenv("APP_NAME", "What Format")
        self.APP_VERSION = os.getenv("APP_VERSION", "2.0.0")
        self.DEBUG = _env_bool("DEBUG", False)

        # 服务器配置
        self.HOST = os.getenv("HOST", "0.0.0.0")
        self.PORT = _env_int("PORT", 8000)

        # 路径配置
        self.BASE_DIR = _BASE_DIR
        self.UPLOAD_DIR = _env_path("UPLOAD_DIR", _BASE_DIR / "uploads")
        self.OUTPUT_DIR = _env_path("OUTPUT_DIR", _BASE_DIR / "outputs")
        self.SAMPLES_DIR = _env_path("SAMPLES_DIR", _BASE_DIR / "Samples")
        self.FRONTEND_DIR = _env_path("FRONTEND_DIR", _BASE_DIR / "frontend")
        self.LOG_DIR = _env_path("LOG_DIR", _BASE_DIR / "logs")

        # 固定模板路径
        self.RESUME_TEMPLATE = _BASE_DIR / "Samples" / "PDF_sample.pdf"
        self.COVER_LETTER_TEMPLATE = _BASE_DIR / "Samples" / "Sample_Career-Cover-Letter.pdf"

        # 文件配置
        self.MAX_FILE_SIZE = 15 * 1024 * 1024  # 15MB
        self.ALLOWED_TEMPLATE_EXTENSIONS = [".pdf", ".docx", ".png", ".jpg", ".jpeg"]
        self.ALLOWED_CONTENT_EXTENSIONS = [".pdf", ".docx"]
        self.ALLOWED_OUTPUT_FORMATS = [".docx", ".pdf"]

        # 处理配置
        self.MAX_CONCURRENT_TASKS = 5
        self.PROCESSING_TIMEOUT = 60
        self.MAX_RETRY_ATTEMPTS = 3

        # OCR配置
        self.TESSERACT_CMD = os.getenv("TESSERACT_CMD", "tesseract")
        self.OCR_LANGUAGE = os.getenv("OCR_LANGUAGE", "chi_sim+eng")

        self.ensure_directories()

    def ensure_directories(self):
        """确保目录存在"""
        self.UPLOAD_DIR.mkdir(exist_ok=True)
        self.OUTPUT_DIR.mkdir(exist_ok=True)
        self.LOG_DIR.mkdir(exist_ok=True)


# 全局配置实例
settings = Settings()


# 简历各部分的标识关键词
RESUME_SECTION_KEYWORDS = {
    "education": [
        "education", "学历", "教育背景", "教育经历", "学业",
        "academic", "university", "college", "degree"
    ],
    "skills": [
        "skills", "技能", "技术", "专业技能", "技能证书",
        "programming", "tools", "languages", "proficient"
    ],
    "experience": [
        "experience", "工作经历", "工作经验", "实习经历", "相关经历",
        "relevant experience", "work experience", "employment"
    ],
    "projects": [
        "projects", "项目经历", "项目经验", "项目", "产品设计",
        "project experience", "portfolio"
    ],
    "leadership": [
        "leadership", "领导经历", "社团活动", "课外活动",
        "activities", "volunteer", "extracurricular"
    ],
    "interests": [
        "interests", "爱好", "特长", "兴趣爱好", "特长爱好",
        "hobbies"
    ],
    "contact": [
        "contact", "联系方式", "email", "phone", "address",
        "linkedin", "github"
    ]
}


# 模板样式映射
TEMPLATE_STYLE_MAP = {
    "header": {
        "font_name": "Times New Roman",
        "font_size": 24,
        "bold": True,
        "alignment": "center"
    },
    "contact": {
        "font_name": "Times New Roman",
        "font_size": 10,
        "alignment": "center"
    },
    "section_title": {
        "font_name": "Times New Roman",
        "font_size": 12,
        "bold": True,
        "underline": True
    },
    "subsection_title": {
        "font_name": "Times New Roman",
        "font_size": 11,
        "bold": True
    },
    "body": {
        "font_name": "Times New Roman",
        "font_size": 10,
    },
    "bullet": {
        "font_name": "Times New Roman",
        "font_size": 10,
        "indent": 0.25
    }
}
