# 启动指南和诊断脚本
import subprocess
import time
import sys
import os

def print_banner(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def check_backend():
    """检查后端服务"""
    print_banner("步骤 1: 检查后端服务")
    
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=3)
        if response.status_code == 200:
            print("✅ 后端服务已启动")
            print(f"   响应：{response.json()}")
            return True
        else:
            print("❌ 后端服务响应异常")
            return False
    except Exception as e:
        print("❌ 后端服务未启动")
        print(f"   错误：{e}")
        return False

def start_backend():
    """启动后端服务"""
    print_banner("启动后端服务")
    
    # 切换到后端目录
    backend_dir = os.path.join(os.path.dirname(__file__), "KnowledgeBasePython")
    
    if not os.path.exists(backend_dir):
        print(f"❌ 后端目录不存在：{backend_dir}")
        return
    
    print(f"📂 后端目录：{backend_dir}")
    print("🚀 正在启动 FastAPI 服务...")
    print("\n提示：新窗口中将显示服务器日志")
    print("按 Ctrl+C 可停止服务器\n")
    
    # 在新窗口启动后端
    subprocess.Popen([sys.executable, "main.py"], cwd=backend_dir)
    
    # 等待 5 秒让服务启动
    print("⏳ 等待服务启动...")
    for i in range(5, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    # 再次检查
    if check_backend():
        print("\n✅ 后端服务启动成功！")
        print("\n📖 访问以下地址查看 API 文档:")
        print("   http://localhost:8000/docs")
        print("   http://localhost:8000/redoc")
    else:
        print("\n❌ 后端服务启动失败，请手动运行:")
        print(f"   cd {backend_dir}")
        print("   python main.py")

def test_upload_api():
    """测试文件上传 API"""
    print_banner("步骤 2: 测试文件上传 API")
    
    try:
        import requests
        
        # 创建测试文件
        test_content = "这是一个测试文件\n" * 10
        test_file_path = os.path.join(os.path.dirname(__file__), "test_temp.txt")
        
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        # 上传测试
        with open(test_file_path, "rb") as f:
            files = {"file": ("test_temp.txt", f, "text/plain")}
            response = requests.post("http://localhost:8000/api/files/upload", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 文件上传成功!")
            print(f"   文件名：{result['filename']}")
            print(f"   路径：{result['filepath']}")
            print(f"   大小：{result['size']} bytes")
            print(f"   消息：{result['message']}")
        else:
            print(f"❌ 上传失败：HTTP {response.status_code}")
            print(f"   响应：{response.text}")
        
        # 清理测试文件
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
            
    except Exception as e:
        print(f"❌ 测试失败：{e}")

def show_frontend_guide():
    """前端启动指南"""
    print_banner("步骤 3: 启动前端服务")
    
    frontend_dir = os.path.join(os.path.dirname(__file__), "KnowledgeBaseVue")
    
    print(f"📂 前端目录：{frontend_dir}")
    print("\n请在新的终端窗口中执行以下命令:\n")
    print(f"   cd {frontend_dir}")
    print("   npm run dev")
    print("\n然后访问显示的地址（通常是 http://localhost:5173）")

def main():
    """主函数"""
    print_banner("知识库系统 - 启动与测试指南")
    
    # 检查并启动后端
    if not check_backend():
        start_backend()
    
    # 测试 API
    test_upload_api()
    
    # 显示前端启动指南
    show_frontend_guide()
    
    print_banner("完成")
    print("现在可以:")
    print("1. 在浏览器中打开前端地址")
    print("2. 拖拽或选择文件上传")
    print("3. 查看左侧文件列表")
    print("4. 在右侧与文件对话")
    print("\n按 Ctrl+C 退出")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 程序已中断")
    except Exception as e:
        print(f"\n❌ 发生错误：{e}")
