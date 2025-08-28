#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件记录器 - 用于记录和写入新文件的工具
作者: AI助手
创建时间: 2024年12月19日
"""

import os
import json
import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path


class FileRecorder:
    """文件记录器类 - 用于管理文件的创建和记录"""
    
    def __init__(self, base_dir: str = "/workspace"):
        """
        初始化文件记录器
        
        Args:
            base_dir: 基础工作目录
        """
        self.base_dir = Path(base_dir)
        self.records_file = self.base_dir / "file_records.json"
        self.ensure_records_file()
    
    def ensure_records_file(self):
        """确保记录文件存在"""
        if not self.records_file.exists():
            initial_data = {
                "created_at": datetime.datetime.now().isoformat(),
                "files": [],
                "metadata": {
                    "total_files": 0,
                    "last_updated": datetime.datetime.now().isoformat()
                }
            }
            self.save_records(initial_data)
    
    def load_records(self) -> Dict:
        """加载记录数据"""
        try:
            with open(self.records_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "created_at": datetime.datetime.now().isoformat(),
                "files": [],
                "metadata": {"total_files": 0, "last_updated": datetime.datetime.now().isoformat()}
            }
    
    def save_records(self, data: Dict):
        """保存记录数据"""
        data["metadata"]["last_updated"] = datetime.datetime.now().isoformat()
        with open(self.records_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def create_file(self, 
                   file_path: str, 
                   content: str, 
                   description: str = "", 
                   file_type: str = "text",
                   tags: List[str] = None) -> bool:
        """
        创建新文件并记录
        
        Args:
            file_path: 文件路径（相对于base_dir）
            content: 文件内容
            description: 文件描述
            file_type: 文件类型
            tags: 标签列表
            
        Returns:
            bool: 创建是否成功
        """
        try:
            # 确保目录存在
            full_path = self.base_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 写入文件
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 记录文件信息
            self.record_file(file_path, description, file_type, tags or [])
            
            print(f"✅ 成功创建文件: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ 创建文件失败: {e}")
            return False
    
    def record_file(self, 
                   file_path: str, 
                   description: str = "", 
                   file_type: str = "text",
                   tags: List[str] = None):
        """记录文件信息到记录文件中"""
        records = self.load_records()
        
        file_info = {
            "id": len(records["files"]) + 1,
            "file_path": file_path,
            "description": description,
            "file_type": file_type,
            "tags": tags or [],
            "created_at": datetime.datetime.now().isoformat(),
            "size_bytes": os.path.getsize(self.base_dir / file_path) if os.path.exists(self.base_dir / file_path) else 0
        }
        
        records["files"].append(file_info)
        records["metadata"]["total_files"] = len(records["files"])
        
        self.save_records(records)
    
    def list_files(self, file_type: str = None, tag: str = None) -> List[Dict]:
        """
        列出记录的文件
        
        Args:
            file_type: 按文件类型过滤
            tag: 按标签过滤
            
        Returns:
            过滤后的文件列表
        """
        records = self.load_records()
        files = records["files"]
        
        if file_type:
            files = [f for f in files if f["file_type"] == file_type]
        
        if tag:
            files = [f for f in files if tag in f["tags"]]
        
        return files
    
    def get_file_info(self, file_path: str) -> Optional[Dict]:
        """获取特定文件的信息"""
        records = self.load_records()
        for file_info in records["files"]:
            if file_info["file_path"] == file_path:
                return file_info
        return None
    
    def update_file_description(self, file_path: str, new_description: str):
        """更新文件描述"""
        records = self.load_records()
        for file_info in records["files"]:
            if file_info["file_path"] == file_path:
                file_info["description"] = new_description
                file_info["updated_at"] = datetime.datetime.now().isoformat()
                break
        
        self.save_records(records)
        print(f"✅ 已更新文件描述: {file_path}")
    
    def delete_file_record(self, file_path: str):
        """删除文件记录（不删除实际文件）"""
        records = self.load_records()
        records["files"] = [f for f in records["files"] if f["file_path"] != file_path]
        records["metadata"]["total_files"] = len(records["files"])
        
        self.save_records(records)
        print(f"✅ 已删除文件记录: {file_path}")
    
    def generate_report(self) -> str:
        """生成文件记录报告"""
        records = self.load_records()
        
        report = f"""# 文件记录报告
        
## 统计信息
- 总文件数: {records['metadata']['total_files']}
- 记录创建时间: {records['created_at']}
- 最后更新时间: {records['metadata']['last_updated']}

## 文件列表
"""
        
        for file_info in records["files"]:
            report += f"""
### {file_info['id']}. {file_info['file_path']}
- **描述**: {file_info['description'] or '无描述'}
- **类型**: {file_info['file_type']}
- **标签**: {', '.join(file_info['tags']) if file_info['tags'] else '无标签'}
- **创建时间**: {file_info['created_at']}
- **文件大小**: {file_info['size_bytes']} 字节
"""
        
        return report


def main():
    """主函数 - 命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="文件记录器工具")
    parser.add_argument("action", choices=["create", "list", "info", "update", "delete", "report"], 
                       help="要执行的操作")
    parser.add_argument("--file", "-f", help="文件路径")
    parser.add_argument("--content", "-c", help="文件内容")
    parser.add_argument("--description", "-d", help="文件描述")
    parser.add_argument("--type", "-t", default="text", help="文件类型")
    parser.add_argument("--tags", help="标签（逗号分隔）")
    parser.add_argument("--filter-type", help="按类型过滤")
    parser.add_argument("--filter-tag", help="按标签过滤")
    
    args = parser.parse_args()
    
    recorder = FileRecorder()
    
    if args.action == "create":
        if not args.file or not args.content:
            print("❌ 创建文件需要指定 --file 和 --content 参数")
            return
        
        tags = args.tags.split(',') if args.tags else []
        recorder.create_file(args.file, args.content, args.description or "", args.type, tags)
    
    elif args.action == "list":
        files = recorder.list_files(args.filter_type, args.filter_tag)
        if files:
            print("📁 文件列表:")
            for file_info in files:
                print(f"  {file_info['id']}. {file_info['file_path']} ({file_info['file_type']})")
                if file_info['description']:
                    print(f"     描述: {file_info['description']}")
        else:
            print("📭 没有找到匹配的文件")
    
    elif args.action == "info":
        if not args.file:
            print("❌ 查看文件信息需要指定 --file 参数")
            return
        
        info = recorder.get_file_info(args.file)
        if info:
            print(f"📄 文件信息:")
            print(f"  路径: {info['file_path']}")
            print(f"  描述: {info['description'] or '无描述'}")
            print(f"  类型: {info['file_type']}")
            print(f"  标签: {', '.join(info['tags']) if info['tags'] else '无标签'}")
            print(f"  创建时间: {info['created_at']}")
            print(f"  文件大小: {info['size_bytes']} 字节")
        else:
            print(f"❌ 未找到文件记录: {args.file}")
    
    elif args.action == "update":
        if not args.file or not args.description:
            print("❌ 更新描述需要指定 --file 和 --description 参数")
            return
        
        recorder.update_file_description(args.file, args.description)
    
    elif args.action == "delete":
        if not args.file:
            print("❌ 删除记录需要指定 --file 参数")
            return
        
        recorder.delete_file_record(args.file)
    
    elif args.action == "report":
        report = recorder.generate_report()
        report_file = "file_records_report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✅ 报告已生成: {report_file}")


if __name__ == "__main__":
    main()