"""
数据模型定义
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime


class DocType(str, Enum):
    """文档类型"""
    RESUME = "resume"
    COVER_LETTER = "cl"


class FileFormat(str, Enum):
    """文件格式"""
    PDF = "pdf"
    DOCX = "docx"
    PNG = "png"
    JPG = "jpg"
    JPEG = "jpeg"


class ProcessingStatus(str, Enum):
    """处理状态"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


# ========== 简历内容数据模型 ==========

class ContactInfo(BaseModel):
    """联系信息"""
    name: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""
    linkedin: str = ""
    github: str = ""
    website: str = ""
    other: List[str] = Field(default_factory=list)


class EducationItem(BaseModel):
    """教育经历条目"""
    institution: str = ""
    location: str = ""
    degree: str = ""
    major: str = ""
    gpa: str = ""
    start_date: str = ""
    end_date: str = ""
    coursework: List[str] = Field(default_factory=list)
    honors: List[str] = Field(default_factory=list)


class ExperienceItem(BaseModel):
    """工作/项目经历条目"""
    organization: str = ""
    location: str = ""
    title: str = ""
    start_date: str = ""
    end_date: str = ""
    descriptions: List[str] = Field(default_factory=list)


class SkillCategory(BaseModel):
    """技能类别"""
    category: str = ""
    skills: List[str] = Field(default_factory=list)


class ResumeContent(BaseModel):
    """简历结构化内容"""
    contact: ContactInfo = Field(default_factory=ContactInfo)
    education: List[EducationItem] = Field(default_factory=list)
    skills: List[SkillCategory] = Field(default_factory=list)
    experience: List[ExperienceItem] = Field(default_factory=list)
    projects: List[ExperienceItem] = Field(default_factory=list)
    leadership: List[ExperienceItem] = Field(default_factory=list)
    other_sections: Dict[str, List[str]] = Field(default_factory=dict)
    raw_text: str = ""


# ========== 模板样式数据模型 ==========

class FontStyle(BaseModel):
    """字体样式"""
    name: str = "Times New Roman"
    size: float = 11
    bold: bool = False
    italic: bool = False
    underline: bool = False
    color: str = "#000000"


class ParagraphStyle(BaseModel):
    """段落样式"""
    alignment: str = "left"  # left, center, right, justify
    line_spacing: float = 1.0
    space_before: float = 0
    space_after: float = 0
    first_line_indent: float = 0
    left_indent: float = 0
    right_indent: float = 0


class SectionStyle(BaseModel):
    """章节样式"""
    title_font: FontStyle = Field(default_factory=FontStyle)
    title_paragraph: ParagraphStyle = Field(default_factory=ParagraphStyle)
    content_font: FontStyle = Field(default_factory=FontStyle)
    content_paragraph: ParagraphStyle = Field(default_factory=ParagraphStyle)
    bullet_style: str = "•"
    has_separator: bool = False
    separator_style: str = "line"  # line, none


class TemplateStyle(BaseModel):
    """模板整体样式"""
    page_margins: Dict[str, float] = Field(
        default_factory=lambda: {"top": 1, "bottom": 1, "left": 1, "right": 1}
    )
    header_style: SectionStyle = Field(default_factory=SectionStyle)
    contact_style: SectionStyle = Field(default_factory=SectionStyle)
    section_styles: Dict[str, SectionStyle] = Field(default_factory=dict)
    default_font: FontStyle = Field(default_factory=FontStyle)
    column_layout: int = 1  # 1 或 2 列布局


# ========== API请求/响应模型 ==========

class ProcessRequest(BaseModel):
    """处理请求"""
    doc_type: DocType = DocType.RESUME


class ProcessResponse(BaseModel):
    """处理响应"""
    status: ProcessingStatus
    message: str
    task_id: Optional[str] = None
    download_url: Optional[str] = None
    processing_time: Optional[float] = None


class ErrorResponse(BaseModel):
    """错误响应"""
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str = "healthy"
    version: str
    timestamp: str = ""


class SupportedFormatsResponse(BaseModel):
    """支持的格式响应"""
    input_formats: List[str]
    output_formats: List[str]
    max_file_size: int
    templates: Dict[str, str]


class TemplateInfoResponse(BaseModel):
    """模板信息响应"""
    resume: Dict[str, Any]
    cover_letter: Dict[str, Any]


class PreviewResponse(BaseModel):
    """预览响应"""
    success: bool
    sections: Dict[str, List[Dict[str, Any]]]
    total_paragraphs: int
    classified_items: int


# ========== 内部处理模型 ==========

class FileInfo(BaseModel):
    """文件信息"""
    filename: str
    filepath: str
    file_format: FileFormat
    file_size: int
    mime_type: str


class ProcessingTask(BaseModel):
    """处理任务"""
    task_id: str
    template_file: FileInfo
    content_file: FileInfo
    doc_type: DocType
    status: ProcessingStatus = ProcessingStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    output_path: Optional[str] = None
    error_message: Optional[str] = None
    retry_count: int = 0
