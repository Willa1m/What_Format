"""
API路由定义
- /resume: 简历格式转换（固定模板）
- /cover-letter: 求职信格式转换（固定模板）
"""
import os
import tempfile
import asyncio
import time
from pathlib import Path
from typing import Optional
from datetime import datetime

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse

from backend.utils.logger import logger, log_processing, log_user_operation
from backend.utils.helpers import (
    generate_unique_id, validate_file_type, save_upload_file,
    cleanup_temp_files, sanitize_filename
)
from backend.config import settings
from backend.models.schemas import (
    ProcessResponse, HealthResponse, SupportedFormatsResponse, ProcessingStatus
)
from backend.services.template_processor import (
    resume_processor, cover_letter_processor
)


router = APIRouter()


# ==================== 健康检查 ====================

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查接口"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version=settings.APP_VERSION
    )


# ==================== 支持格式 ====================

@router.get("/supported-formats", response_model=SupportedFormatsResponse)
async def get_supported_formats():
    """获取支持的文件格式"""
    return SupportedFormatsResponse(
        input_formats=["pdf", "docx", "png", "jpg", "jpeg"],
        output_formats=["docx"],
        max_file_size=settings.MAX_FILE_SIZE,
        templates={
            "resume": "PDF_sample.pdf (固定模板)",
            "cover_letter": "Sample_Career-Cover-Letter.pdf (固定模板)"
        }
    )


# ==================== 简历处理 ====================

@router.post("/resume/convert", response_model=ProcessResponse)
async def convert_resume(
    background_tasks: BackgroundTasks,
    content_file: UploadFile = File(..., description="简历内容文件（PDF/DOCX/PNG）"),
):
    """
    简历格式转换
    
    上传个人简历内容文件，自动应用固定模板（PDF_sample.pdf）生成标准格式简历
    
    支持输入格式：PDF, DOCX, PNG, JPG
    输出格式：DOCX
    """
    request_id = generate_unique_id()
    start_time = time.perf_counter()
    log_user_operation("resume_convert", f"请求ID: {request_id}", {
        "filename": content_file.filename
    })
    
    try:
        # 验证文件类型
        allowed_ext = [".pdf", ".docx", ".png", ".jpg", ".jpeg"]
        if not validate_file_type(content_file.filename, allowed_ext):
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件格式。支持: {', '.join(allowed_ext)}"
            )
        
        # 验证文件大小
        content = await content_file.read()
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"文件太大。最大支持: {settings.MAX_FILE_SIZE // (1024*1024)}MB"
            )
        await content_file.seek(0)
        
        # 保存上传文件
        upload_path = await save_upload_file(content_file, settings.UPLOAD_DIR)
        
        # 生成输出文件名
        original_name = Path(content_file.filename).stem
        safe_name = sanitize_filename(original_name)
        output_filename = f"{safe_name}_Formatted_{request_id[:8]}.docx"
        output_path = settings.OUTPUT_DIR / output_filename
        
        # 处理简历
        result_path = resume_processor.process(upload_path, output_path)
        
        # 清理临时文件
        background_tasks.add_task(cleanup_temp_files, [upload_path])
        
        log_user_operation("resume_convert", f"转换成功: {request_id}", {
            "output": output_filename
        })
        
        processing_time = round(time.perf_counter() - start_time, 3)
        return ProcessResponse(
            status=ProcessingStatus.COMPLETED,
            message="简历转换完成",
            task_id=request_id,
            download_url=f"/api/files/{output_filename}",
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"简历转换失败: {e}")
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


@router.post("/resume/preview")
async def preview_resume(
    content_file: UploadFile = File(..., description="简历内容文件"),
):
    """
    预览简历解析结果
    
    返回智能识别的章节和内容，用于前端预览
    """
    from backend.services.file_parser import FileParser
    from backend.services.smart_classifier import smart_classifier
    
    try:
        # 保存并解析
        upload_path = await save_upload_file(content_file, settings.UPLOAD_DIR)
        
        parser = FileParser()
        content, _ = parser.parse(upload_path)
        
        # 智能分类
        classified = smart_classifier.classify_resume_content(content.paragraphs)
        
        # 整理结果
        sections = {}
        for item in classified:
            if item.section not in sections:
                sections[item.section] = []
            sections[item.section].append({
                "content": item.content,
                "confidence": item.confidence,
                "keywords": item.keywords_matched
            })
        
        # 清理
        upload_path.unlink(missing_ok=True)
        
        return JSONResponse({
            "success": True,
            "sections": sections,
            "total_paragraphs": len(content.paragraphs),
            "classified_items": len(classified)
        })
        
    except Exception as e:
        logger.error(f"预览失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 求职信处理 ====================

@router.post("/cover-letter/convert", response_model=ProcessResponse)
async def convert_cover_letter(
    background_tasks: BackgroundTasks,
    content_file: UploadFile = File(..., description="求职信内容文件"),
    recipient_name: Optional[str] = Form(None, description="收件人姓名"),
    recipient_title: Optional[str] = Form(None, description="收件人职位"),
    recipient_company: Optional[str] = Form(None, description="收件人公司"),
    recipient_location: Optional[str] = Form(None, description="收件人地址"),
):
    """
    求职信格式转换
    
    上传求职信内容，自动应用固定模板生成标准格式求职信
    """
    request_id = generate_unique_id()
    start_time = time.perf_counter()
    log_user_operation("cover_letter_convert", f"请求ID: {request_id}", {
        "filename": content_file.filename
    })
    
    try:
        # 验证文件
        allowed_ext = [".pdf", ".docx", ".png", ".jpg", ".jpeg", ".txt"]
        if not validate_file_type(content_file.filename, allowed_ext):
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件格式。支持: {', '.join(allowed_ext)}"
            )
        
        # 验证文件大小
        content = await content_file.read()
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"文件太大。最大支持: {settings.MAX_FILE_SIZE // (1024*1024)}MB"
            )
        await content_file.seek(0)

        # 保存上传文件
        upload_path = await save_upload_file(content_file, settings.UPLOAD_DIR)
        
        # 生成输出文件名
        original_name = Path(content_file.filename).stem
        safe_name = sanitize_filename(original_name)
        output_filename = f"{safe_name}_CoverLetter_{request_id[:8]}.docx"
        output_path = settings.OUTPUT_DIR / output_filename
        
        # 处理求职信
        result_path = cover_letter_processor.process(
            upload_path, output_path,
            recipient_name or "",
            recipient_title or "",
            recipient_company or "",
            recipient_location or ""
        )
        
        # 清理
        background_tasks.add_task(cleanup_temp_files, [upload_path])
        
        processing_time = round(time.perf_counter() - start_time, 3)
        return ProcessResponse(
            status=ProcessingStatus.COMPLETED,
            message="求职信转换完成",
            task_id=request_id,
            download_url=f"/api/files/{output_filename}",
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"求职信转换失败: {e}")
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


@router.post("/cover-letter/preview")
async def preview_cover_letter(
    content_file: UploadFile = File(..., description="求职信内容文件"),
):
    """
    预览求职信解析结果
    """
    from backend.services.file_parser import FileParser
    from backend.services.smart_classifier import smart_classifier
    
    try:
        upload_path = await save_upload_file(content_file, settings.UPLOAD_DIR)
        
        parser = FileParser()
        content, _ = parser.parse(upload_path)
        
        classified = smart_classifier.classify_cover_letter_content(content.paragraphs)
        merged = smart_classifier.merge_similar_sections(classified)
        
        upload_path.unlink(missing_ok=True)
        
        return JSONResponse({
            "success": True,
            "sections": merged,
            "total_paragraphs": len(content.paragraphs)
        })
        
    except Exception as e:
        logger.error(f"预览失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 模板信息 ====================

@router.get("/templates/info")
async def get_templates_info():
    """获取固定模板信息"""
    return JSONResponse({
        "resume": {
            "name": "PDF_sample.pdf",
            "description": "标准简历模板，包含教育背景、工作经历、项目经验、技能等章节",
            "sections": ["EDUCATION", "PROFESSIONAL EXPERIENCE", "ACADEMIC PROJECTS", "OTHER SKILLS"],
            "features": [
                "日期右对齐",
                "公司/学校名称加粗+下划线",
                "职位/学位斜体",
                "自动字体大小调整（确保单页）"
            ]
        },
        "cover_letter": {
            "name": "Sample_Career-Cover-Letter.pdf", 
            "description": "标准求职信模板，包含发件人信息、收件人信息、正文、签名",
            "sections": ["发件人信息", "收件人信息", "日期", "称呼", "正文", "结尾", "签名"],
            "features": [
                "专业商务格式",
                "自动日期填充",
                "智能段落识别"
            ]
        }
    })


# ==================== 结果文件下载 ====================

@router.get("/files/{filename}")
async def download_output_file(filename: str):
    """下载转换后的文件（仅输出目录）"""
    safe_name = Path(filename).name
    file_path = settings.OUTPUT_DIR / safe_name
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")
    return FileResponse(
        path=str(file_path),
        filename=safe_name,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


# ==================== 旧接口兼容 ====================

@router.post("/process", response_model=ProcessResponse)
async def process_legacy(
    background_tasks: BackgroundTasks,
    content_file: UploadFile = File(...),
    document_type: str = Form("resume", description="文档类型: resume 或 cover_letter")
):
    """
    旧版兼容接口
    
    根据document_type路由到对应处理器
    """
    if document_type == "cover_letter":
        return await convert_cover_letter(background_tasks, content_file)
    else:
        return await convert_resume(background_tasks, content_file)
