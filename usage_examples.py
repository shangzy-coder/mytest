#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件记录器使用示例
展示如何使用 FileRecorder 类进行文件记录和管理
"""

from file_recorder import FileRecorder
import datetime


def example_basic_usage():
    """基础使用示例"""
    print("=== 基础使用示例 ===")
    
    # 创建文件记录器实例
    recorder = FileRecorder()
    
    # 创建一个简单的文本文件
    content = """这是一个示例文件
包含多行内容
用于演示文件记录功能"""
    
    recorder.create_file(
        file_path="examples/sample.txt",
        content=content,
        description="示例文本文件",
        file_type="text",
        tags=["示例", "测试"]
    )
    
    # 创建一个配置文件
    config_content = """{
    "app_name": "文件记录器",
    "version": "1.0.0",
    "debug": true,
    "log_level": "INFO"
}"""
    
    recorder.create_file(
        file_path="config/app_config.json",
        content=config_content,
        description="应用程序配置文件",
        file_type="json",
        tags=["配置", "JSON"]
    )


def example_markdown_documentation():
    """创建 Markdown 文档示例"""
    print("\n=== Markdown 文档示例 ===")
    
    recorder = FileRecorder()
    
    # 创建项目文档
    doc_content = """# 项目文档

## 概述
这是一个文件记录管理系统的项目文档。

## 功能特性
- ✅ 文件创建和记录
- ✅ 文件信息管理
- ✅ 标签系统
- ✅ 报告生成

## 使用方法

### 基础用法
```python
from file_recorder import FileRecorder

recorder = FileRecorder()
recorder.create_file("test.txt", "Hello World!", "测试文件")
```

### 命令行用法
```bash
python file_recorder.py create --file "test.txt" --content "Hello World!" --description "测试文件"
```

## 文件结构
```
workspace/
├── file_recorder.py      # 主程序
├── usage_examples.py     # 使用示例
├── file_records.json     # 记录文件
└── examples/             # 示例文件目录
```

## 更新日志
- 2024-12-19: 初始版本发布
"""
    
    recorder.create_file(
        file_path="docs/README.md",
        content=doc_content,
        description="项目主要文档",
        file_type="markdown",
        tags=["文档", "README", "项目介绍"]
    )


def example_code_files():
    """创建代码文件示例"""
    print("\n=== 代码文件示例 ===")
    
    recorder = FileRecorder()
    
    # 创建一个简单的工具函数文件
    utils_content = """# -*- coding: utf-8 -*-
\"\"\"
实用工具函数集合
\"\"\"

import os
import datetime
from typing import List, Dict, Any


def get_current_timestamp() -> str:
    \"\"\"获取当前时间戳\"\"\"
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_directory(dir_path: str) -> bool:
    \"\"\"确保目录存在\"\"\"
    try:
        os.makedirs(dir_path, exist_ok=True)
        return True
    except Exception as e:
        print(f"创建目录失败: {e}")
        return False


def format_file_size(size_bytes: int) -> str:
    \"\"\"格式化文件大小显示\"\"\"
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def validate_file_path(file_path: str) -> bool:
    \"\"\"验证文件路径是否有效\"\"\"
    forbidden_chars = ['<', '>', ':', '"', '|', '?', '*']
    return not any(char in file_path for char in forbidden_chars)
"""
    
    recorder.create_file(
        file_path="utils/file_utils.py",
        content=utils_content,
        description="文件操作相关的实用工具函数",
        file_type="python",
        tags=["工具", "Python", "文件操作"]
    )


def example_data_files():
    """创建数据文件示例"""
    print("\n=== 数据文件示例 ===")
    
    recorder = FileRecorder()
    
    # 创建 CSV 数据文件
    csv_content = """文件名,类型,大小,创建时间,描述
sample.txt,text,45,2024-12-19 10:00:00,示例文本文件
config.json,json,256,2024-12-19 10:05:00,配置文件
utils.py,python,1024,2024-12-19 10:10:00,工具函数
README.md,markdown,2048,2024-12-19 10:15:00,项目文档"""
    
    recorder.create_file(
        file_path="data/file_summary.csv",
        content=csv_content,
        description="文件摘要数据表",
        file_type="csv",
        tags=["数据", "CSV", "摘要"]
    )
    
    # 创建 YAML 配置文件
    yaml_content = """# 文件记录器配置
app:
  name: "文件记录器"
  version: "1.0.0"
  author: "AI助手"

settings:
  encoding: "utf-8"
  backup_enabled: true
  max_file_size: 10485760  # 10MB
  
file_types:
  - text
  - markdown
  - python
  - json
  - yaml
  - csv
  
default_tags:
  - "自动创建"
  
logging:
  level: "INFO"
  format: "%(asctime)s - %(levelname)s - %(message)s"
"""
    
    recorder.create_file(
        file_path="config/settings.yaml",
        content=yaml_content,
        description="系统配置文件（YAML格式）",
        file_type="yaml",
        tags=["配置", "YAML", "设置"]
    )


def example_list_and_report():
    """列表查看和报告生成示例"""
    print("\n=== 文件列表和报告示例 ===")
    
    recorder = FileRecorder()
    
    # 列出所有文件
    print("\n📁 所有记录的文件:")
    all_files = recorder.list_files()
    for file_info in all_files:
        print(f"  {file_info['id']}. {file_info['file_path']}")
        print(f"     类型: {file_info['file_type']}, 描述: {file_info['description']}")
    
    # 按类型过滤
    print("\n🐍 Python 文件:")
    python_files = recorder.list_files(file_type="python")
    for file_info in python_files:
        print(f"  - {file_info['file_path']}")
    
    # 按标签过滤
    print("\n🏷️ 配置相关文件:")
    config_files = recorder.list_files(tag="配置")
    for file_info in config_files:
        print(f"  - {file_info['file_path']}")
    
    # 生成报告
    print("\n📊 生成详细报告...")
    report = recorder.generate_report()
    
    # 保存报告到文件
    with open("/workspace/file_records_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("✅ 报告已保存到: file_records_report.md")


if __name__ == "__main__":
    print("🚀 文件记录器使用示例")
    print("=" * 50)
    
    # 运行所有示例
    example_basic_usage()
    example_markdown_documentation()
    example_code_files()
    example_data_files()
    example_list_and_report()
    
    print("\n✨ 所有示例执行完成！")
    print("您可以查看生成的文件和记录。")