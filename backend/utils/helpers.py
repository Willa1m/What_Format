"""
辅助工具函数
"""
import os
import uuid
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional
import aiofiles
try:
    import magic
except Exception:  # pragma: no cover - optional dependency
    magic = None


def generate_unique_id() -> str:
    """生成唯一ID"""
    return str(uuid.uuid4())[:8]


def generate_timestamp() -> str:
    """生成时间戳字符串"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def get_file_extension(filename: str) -> str:
    """获取文件扩展名（小写）"""
    return Path(filename).suffix.lower()


def get_file_hash(file_path: Path) -> str:
    """计算文件MD5哈希"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def detect_file_type(file_path: Path) -> str:
    """检测文件MIME类型"""
    try:
        if magic is not None:
            mime = magic.Magic(mime=True)
            return mime.from_file(str(file_path))
    except Exception:
        # 备用方案：根据扩展名判断
        ext = get_file_extension(file_path.name)
        mime_map = {
            ".pdf": "application/pdf",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
        }
        return mime_map.get(ext, "application/octet-stream")


def validate_file_type(filename, allowed_types: list) -> bool:
    """验证文件类型是否允许"""
    if isinstance(filename, Path):
        filename = filename.name
    ext = get_file_extension(filename)
    return ext in allowed_types


def sanitize_filename(filename: str) -> str:
    """清理文件名，移除非法字符"""
    illegal_chars = '<>:"/\\|?*'
    for char in illegal_chars:
        filename = filename.replace(char, "_")
    return filename


def ensure_directory(path: Path) -> Path:
    """确保目录存在"""
    path.mkdir(parents=True, exist_ok=True)
    return path


async def save_upload_file(upload_file, dest_dir: Path) -> Path:
    """
    异步保存上传的文件
    
    Args:
        upload_file: FastAPI UploadFile 对象
        dest_dir: 目标目录
        
    Returns:
        保存的文件路径
    """
    ensure_directory(dest_dir)
    
    # 生成唯一文件名
    unique_id = generate_unique_id()
    ext = get_file_extension(upload_file.filename)
    safe_name = sanitize_filename(Path(upload_file.filename).stem)
    dest_path = dest_dir / f"{safe_name}_{unique_id}{ext}"
    
    # 读取并保存文件
    content = await upload_file.read()
    async with aiofiles.open(dest_path, "wb") as f:
        await f.write(content)
    
    # 重置文件指针
    await upload_file.seek(0)
    
    return dest_path


def cleanup_temp_files(files_or_directory, max_age_hours: int = 24):
    """
    清理临时文件
    
    Args:
        files_or_directory: 文件列表或目录路径
        max_age_hours: 最大保留时间（小时），仅对目录清理有效
    """
    # 如果是文件列表
    if isinstance(files_or_directory, list):
        for file_path in files_or_directory:
            try:
                if isinstance(file_path, Path) and file_path.exists():
                    file_path.unlink()
            except Exception:
                pass
        return
    
    # 如果是目录
    directory = files_or_directory
    if not isinstance(directory, Path):
        directory = Path(directory)
    
    if not directory.exists():
        return
    
    now = datetime.now()
    for file in directory.iterdir():
        if file.is_file():
            file_age = now - datetime.fromtimestamp(file.stat().st_mtime)
            if file_age.total_seconds() > max_age_hours * 3600:
                try:
                    file.unlink()
                except Exception:
                    pass


def format_file_size(size_bytes: int) -> str:
    """格式化文件大小显示"""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"
