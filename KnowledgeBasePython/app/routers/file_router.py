from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from app.services.file_service import FileService
from app.schemas.file import FileResponse
import os
from pathlib import Path

router = APIRouter(prefix="/api/files", tags=["文件管理"])

# 初始化文件服务
file_service = FileService()


@router.post("/upload", response_model=FileResponse, summary="上传单个文件")
async def upload_file(file: UploadFile = File(..., description="要上传的文件")):
    """
    上传单个文件
    
    - **file**: 要上传的文件 (multipart/form-data)
    
    返回:
    - filename: 保存的文件名
    - filepath: 文件完整路径
    - size: 文件大小（字节）
    - message: 成功消息
    """
    return await file_service.upload_file(file)


@router.post("/upload/batch", response_model=List[FileResponse], summary="批量上传文件")
async def upload_multiple_files(
    files: List[UploadFile] = File(..., description="要上传的文件列表")
):
    """
    批量上传多个文件
    
    - **files**: 要上传的文件列表 (multipart/form-data)
    
    返回:
    - 文件响应列表，包含每个文件的信息
    """
    if not files:
        raise HTTPException(status_code=400, detail="未选择任何文件")
    
    return await file_service.upload_multiple_files(files)


@router.get("/list", response_model=List[dict], summary="获取文件列表")
async def get_file_list():
    """
    获取 uploads 目录中的所有文件列表
    
    返回:
    - 文件信息列表，包含文件名、大小、路径等
    """
    try:
        upload_dir = Path("uploads")
        
        # 如果目录不存在，创建它
        if not upload_dir.exists():
            upload_dir.mkdir(parents=True, exist_ok=True)
            return []
        
        files = []
        for file_path in upload_dir.iterdir():
            if file_path.is_file() and not file_path.name.startswith('.'):
                stat = file_path.stat()
                files.append({
                    "id": hash(str(file_path)),
                    "name": file_path.name,
                    "size": stat.st_size,
                    "type": get_file_type(file_path.suffix),
                    "filepath": str(file_path),
                    "uploadTime": format_timestamp(stat.st_mtime),
                    "status": "success"
                })
        
        # 按修改时间倒序排列
        files.sort(key=lambda x: x["uploadTime"], reverse=True)
        return files
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取文件列表失败：{str(e)}"
        )


def get_file_type(suffix: str) -> str:
    """根据文件后缀判断文件类型"""
    suffix = suffix.lower()
    type_map = {
        '.pdf': 'application/pdf',
        '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.xls': 'application/vnd.ms-excel',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.ppt': 'application/vnd.ms-powerpoint',
        '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        '.txt': 'text/plain',
        '.md': 'text/markdown',
        '.json': 'application/json',
        '.xml': 'application/xml',
        '.csv': 'text/csv',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.bmp': 'image/bmp',
        '.svg': 'image/svg+xml',
        '.webp': 'image/webp',
        '.mp4': 'video/mp4',
        '.avi': 'video/x-msvideo',
        '.mov': 'video/quicktime',
        '.wmv': 'video/x-ms-wmv',
        '.flv': 'video/x-flv',
        '.mp3': 'audio/mpeg',
        '.wav': 'audio/x-wav',
        '.aac': 'audio/aac',
        '.wma': 'audio/x-ms-wma',
        '.zip': 'application/zip',
        '.rar': 'application/x-rar-compressed',
        '.7z': 'application/x-7z-compressed',
        '.tar': 'application/x-tar',
        '.gz': 'application/gzip',
        '.py': 'text/x-python',
        '.java': 'text/x-java-source',
        '.cpp': 'text/x-c++src',
        '.c': 'text/x-c',
        '.js': 'application/javascript',
        '.ts': 'application/typescript',
        '.vue': 'text/x-vue',
        '.css': 'text/css',
        '.scss': 'text/x-scss',
        '.less': 'text/x-less',
        '.html': 'text/html',
        '.htm': 'text/html',
        '.sql': 'application/sql',
        '.sh': 'application/x-sh',
        '.bat': 'application/x-bat',
        '.exe': 'application/x-msdownload',
        '.dll': 'application/x-msdownload',
        '.so': 'application/x-sharedlib',
    }
    return type_map.get(suffix, 'application/octet-stream')


def format_timestamp(timestamp: float) -> str:
    """格式化时间戳"""
    from datetime import datetime
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%Y/%m/%d %H:%M')
