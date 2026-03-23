"""
测试文件列表 API 的脚本
"""
import requests
import json

def test_get_file_list():
    """测试获取文件列表"""
    url = "http://localhost:8000/api/files/list"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        files = response.json()
        
        print("=" * 60)
        print(f"✅ 获取文件列表成功！共 {len(files)} 个文件")
        print("=" * 60)
        
        if not files:
            print("\n📂 uploads 目录为空")
            print("\n提示：请先上传一些文件进行测试")
            return
        
        print(f"\n{'文件名':<30} {'大小':<12} {'类型':<25} {'上传时间'}")
        print("-" * 90)
        
        for file in files:
            size = format_size(file['size'])
            file_type = file['type'][:20] + '...' if len(file['type']) > 20 else file['type']
            print(f"{file['name']:<30} {size:<12} {file_type:<25} {file['uploadTime']}")
        
        print("\n完整 JSON 数据:")
        print(json.dumps(files, indent=2, ensure_ascii=False))
        
    except requests.exceptions.ConnectionError:
        print("❌ 错误：无法连接到后端服务")
        print("\n请确保后端服务已启动:")
        print("  cd KnowledgeBasePython")
        print("  python main.py")
    except Exception as e:
        print(f"❌ 测试失败：{e}")


def format_size(bytes):
    """格式化文件大小"""
    if bytes == 0:
        return '0 B'
    k = 1024
    sizes = ['B', 'KB', 'MB', 'GB']
    i = int(__import__('math').floor(__import__('math').log(bytes) / __import__('math').log(k)))
    return f"{round(bytes / pow(k, i) * 100) / 100} {sizes[i]}"


if __name__ == "__main__":
    print("\n🔍 测试文件列表 API\n")
    test_get_file_list()
    print("\n")
