"""
测试文件上传 API 的脚本
"""
import requests

# 测试文件上传
def test_upload_file():
    """测试单个文件上传"""
    url = "http://localhost:8000/api/files/upload"
    
    # 创建一个测试文件
    test_content = "这是一个测试文件内容\n" * 10
    with open("test_upload.txt", "w", encoding="utf-8") as f:
        f.write(test_content)
    
    # 上传文件
    with open("test_upload.txt", "rb") as f:
        files = {"file": ("test_upload.txt", f, "text/plain")}
        response = requests.post(url, files=files)
    
    print(f"状态码：{response.status_code}")
    print(f"响应内容：{response.json()}")
    
    # 清理测试文件
    import os
    if os.path.exists("test_upload.txt"):
        os.remove("test_upload.txt")


# 测试批量上传
def test_batch_upload():
    """测试批量文件上传"""
    url = "http://localhost:8000/api/files/upload/batch"
    
    # 创建多个测试文件
    test_files = []
    for i in range(3):
        filename = f"test_batch_{i}.txt"
        content = f"批量测试文件 {i}\n" * 5
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        test_files.append(filename)
    
    # 上传文件
    files = []
    for filename in test_files:
        files.append(("files", (filename, open(filename, "rb"), "text/plain")))
    
    response = requests.post(url, files=files)
    
    print(f"\n批量上传状态码：{response.status_code}")
    print(f"批量上传响应：{response.json()}")
    
    # 清理测试文件
    import os
    for filename in test_files:
        if os.path.exists(filename):
            os.remove(filename)


if __name__ == "__main__":
    print("=" * 50)
    print("测试文件上传 API")
    print("=" * 50)
    
    try:
        test_upload_file()
        test_batch_upload()
        print("\n✅ 所有测试通过!")
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        print("请确保后端服务已启动：python main.py")
