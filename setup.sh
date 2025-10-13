#!/bin/bash
# 安裝腳本

echo "================================"
echo "中文維基百科索引系統 - 安裝程式"
echo "================================"
echo ""

# 檢查 Python 版本
echo "檢查 Python 版本..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ 錯誤: 未找到 Python 3"
    echo "請先安裝 Python 3.7 或更高版本"
    exit 1
fi

echo "✅ Python 版本正常"
echo ""

# 創建虛擬環境（可選）
read -p "是否創建 Python 虛擬環境？(推薦) [Y/n]: " create_venv
create_venv=${create_venv:-Y}

if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "正在創建虛擬環境..."
    python3 -m venv venv
    
    if [ $? -eq 0 ]; then
        echo "✅ 虛擬環境創建成功"
        echo ""
        echo "請執行以下命令啟動虛擬環境："
        echo "  source venv/bin/activate  # Linux/Mac"
        echo "  venv\\Scripts\\activate     # Windows"
        echo ""
        
        # 啟動虛擬環境
        source venv/bin/activate 2>/dev/null || . venv/bin/activate 2>/dev/null
    else
        echo "⚠️  虛擬環境創建失敗，將使用系統 Python"
    fi
fi

# 安裝依賴
echo "正在安裝依賴套件..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ 依賴套件安裝完成"
else
    echo "❌ 依賴套件安裝失敗"
    exit 1
fi

echo ""
echo "================================"
echo "安裝完成！"
echo "================================"
echo ""
echo "下一步："
echo "  1. 準備數據文件: python scripts/download_wiki.py"
echo "  2. 建立索引: python build_index.py"
echo "  3. 查詢 IDF: python query_idf.py 蝙蝠俠"
echo ""
echo "詳細說明請參考 README.md"
