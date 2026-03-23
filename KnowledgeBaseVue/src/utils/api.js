/**
 * API 配置
 */
export const API_CONFIG = {
  BASE_URL: 'http://localhost:8000',
  TIMEOUT: 30000, // 30 秒超时
}

/**
 * 文件上传 API
 */
export const FILE_API = {
  UPLOAD: `${API_CONFIG.BASE_URL}/api/files/upload`,
  UPLOAD_BATCH: `${API_CONFIG.BASE_URL}/api/files/upload/batch`,
  LIST: `${API_CONFIG.BASE_URL}/api/files/list`,
}

/**
 * 健康检查 API
 */
export const HEALTH_API = {
  ROOT: `${API_CONFIG.BASE_URL}/`,
  HEALTH: `${API_CONFIG.BASE_URL}/health`,
}
