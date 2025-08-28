#!/bin/bash
# 快速文件记录脚本

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📝 文件记录器 - 快速记录工具${NC}"
echo "=================================="

# 检查 Python 是否可用
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 未找到，请先安装 Python3${NC}"
    exit 1
fi

# 显示菜单
show_menu() {
    echo ""
    echo -e "${YELLOW}请选择操作:${NC}"
    echo "1. 创建新文件并记录"
    echo "2. 列出所有记录的文件"
    echo "3. 查看文件信息"
    echo "4. 生成报告"
    echo "5. 运行示例"
    echo "6. 退出"
    echo ""
}

# 创建文件函数
create_file() {
    echo -e "${BLUE}创建新文件${NC}"
    echo -n "请输入文件路径: "
    read file_path
    
    echo -n "请输入文件描述: "
    read description
    
    echo -n "请输入文件类型 (text/python/json/markdown/yaml/csv): "
    read file_type
    
    echo -n "请输入标签 (逗号分隔): "
    read tags
    
    echo "请输入文件内容 (输入 'EOF' 结束):"
    content=""
    while IFS= read -r line; do
        if [ "$line" = "EOF" ]; then
            break
        fi
        content="$content$line\n"
    done
    
    # 使用 Python 创建文件
    python3 file_recorder.py create \
        --file "$file_path" \
        --content "$content" \
        --description "$description" \
        --type "$file_type" \
        --tags "$tags"
}

# 主循环
while true; do
    show_menu
    echo -n "请输入选择 (1-6): "
    read choice
    
    case $choice in
        1)
            create_file
            ;;
        2)
            echo -e "${BLUE}📁 文件列表:${NC}"
            python3 file_recorder.py list
            ;;
        3)
            echo -n "请输入文件路径: "
            read file_path
            python3 file_recorder.py info --file "$file_path"
            ;;
        4)
            echo -e "${BLUE}📊 生成报告...${NC}"
            python3 file_recorder.py report
            ;;
        5)
            echo -e "${BLUE}🚀 运行示例...${NC}"
            python3 usage_examples.py
            ;;
        6)
            echo -e "${GREEN}👋 再见！${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ 无效选择，请输入 1-6${NC}"
            ;;
    esac
    
    echo ""
    echo -n "按 Enter 键继续..."
    read
done