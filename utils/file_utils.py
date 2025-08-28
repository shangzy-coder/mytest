# -*- coding: utf-8 -*-
"""
实用工具函数集合
"""

import os
import datetime
from typing import List, Dict, Any


def get_current_timestamp() -> str:
    """获取当前时间戳"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_directory(dir_path: str) -> bool:
    """确保目录存在"""
    try:
        os.makedirs(dir_path, exist_ok=True)
        return True
    except Exception as e:
        print(f"创建目录失败: {e}")
        return False


def format_file_size(size_bytes: int) -> str:
    """格式化文件大小显示"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def validate_file_path(file_path: str) -> bool:
    """验证文件路径是否有效"""
    forbidden_chars = ['<', '>', ':', '"', '|', '?', '*']
    return not any(char in file_path for char in forbidden_chars)
