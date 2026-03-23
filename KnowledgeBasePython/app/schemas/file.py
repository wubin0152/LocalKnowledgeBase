from pydantic import BaseModel


class FileResponse(BaseModel):
    """文件上传响应模型"""
    filename: str
    filepath: str
    size: int
    message: str = "File uploaded successfully"


class UploadFileSchema(BaseModel):
    """上传文件信息 schema"""
    filename: str
    content_type: str | None = None
    size: int
