import os
import shutil
from pathlib import Path
from fastapi import UploadFile, HTTPException
from app.schemas.file import FileResponse


class FileService:
    """文件上传服务"""
    
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = Path(upload_dir)
        self._ensure_upload_dir()
    
    def _ensure_upload_dir(self):
        """确保上传目录存在"""
        self.upload_dir.mkdir(parents=True, exist_ok=True)
    
    async def upload_file(self, file: UploadFile) -> FileResponse:
        """
        上传文件
        
        Args:
            file: FastAPI UploadFile 对象
            
        Returns:
            FileResponse: 包含文件信息的响应对象
            
        Raises:
            HTTPException: 当文件为空或保存失败时抛出异常
        """
        try:
            # 验证文件
            content = await file.read()
            if not content:
                raise HTTPException(
                    status_code=400,
                    detail="上传的文件为空"
                )
            
            # 生成安全的文件名
            safe_filename = self._sanitize_filename(file.filename or "unnamed")
            filepath = self.upload_dir / safe_filename
            
            # 保存文件
            with open(filepath, "wb") as buffer:
                buffer.write(content)
            
            return FileResponse(
                filename=safe_filename,
                filepath=str(filepath),
                size=len(content),
                message="文件上传成功"
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"文件上传失败：{str(e)}"
            )
    
    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        """
        清理文件名，移除危险字符
        
        Args:
            filename: 原始文件名
            
        Returns:
            str: 清理后的文件名
        """
        # 简单的文件名清理，实际项目中可以使用更严格的验证
        safe_name = "".join(c for c in filename if c.isalnum() or c in "._- ")
        return safe_name.strip() or "uploaded_file"
    
    async def upload_multiple_files(self, files: list[UploadFile]) -> list[FileResponse]:
        """
        批量上传文件
        
        Args:
            files: UploadFile 对象列表
            
        Returns:
            list[FileResponse]: 文件响应列表
        """
        responses = []
        for file in files:
            response = await self.upload_file(file)
            responses.append(response)
        return responses
