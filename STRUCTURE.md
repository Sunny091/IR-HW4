# 專案結構說明

## 目錄組織

本專案採用清晰的模組化結構，每個目錄都有明確的用途：

```
中文維基百科索引系統/
│
├── 📄 核心文件（項目根目錄）
│   ├── build_index.py          # 索引建立主程式
│   ├── query_idf.py            # IDF 查詢工具
│   ├── README.md               # 主要說明文件
│   ├── LICENSE                 # MIT 開源授權
│   ├── CHANGELOG.md            # 版本更新記錄
│   ├── COMPLETION_REPORT.md    # 專案完成報告
│   ├── PROJECT_OVERVIEW.txt    # 可視化總覽
│   ├── STRUCTURE.md            # 本文件 - 結構說明
│   ├── requirements.txt        # Python 依賴
│   ├── setup.sh                # 安裝腳本
│   └── .gitignore              # Git 配置
│
├── 📁 scripts/                 # 輔助腳本目錄
│   └── download_wiki.py        # 維基百科數據下載工具
│
├── 📁 docs/                    # 文檔目錄
│   ├── TECHNICAL.md            # 技術架構文檔
│   └── PROJECT_SUMMARY.md      # 專案總結
│
├── 📁 data/                    # 數據目錄
│   └── wiki_article_list_2023_tra.json  # 維基百科數據（2.88 GB）
│
└── 📁 indexes/                 # 索引文件目錄（自動生成）
    └── inverted_index.pkl      # 序列化的反向索引（780 MB）
```

## 文件說明

### 核心程式文件

#### build_index.py
- **功能**: 建立反向索引的主程式
- **輸入**: `data/wiki_article_list_2023_tra.json`
- **輸出**: `indexes/inverted_index.pkl`
- **用法**: `python build_index.py`

#### query_idf.py
- **功能**: 查詢指定詞彙的 IDF 值
- **依賴**: `indexes/inverted_index.pkl`（需先運行 build_index.py）
- **用法**: `python query_idf.py <詞彙>`
- **範例**: `python query_idf.py 蝙蝠俠`

### 輔助腳本

#### scripts/download_wiki.py
- **功能**: 維基百科數據下載與驗證工具
- **輸出**: `data/wiki_article_list_2023_tra.json`
- **用法**: `python scripts/download_wiki.py`

### 文檔文件

#### README.md
- 主要說明文件
- 包含快速開始、技術架構、使用示例
- **推薦首先閱讀**

#### docs/TECHNICAL.md
- 技術架構詳細說明
- 包含算法原理、數據結構設計
- 適合深入理解系統實現

#### docs/PROJECT_SUMMARY.md
- 專案完整總結
- 包含功能特點、性能數據
- 適合了解專案全貌

#### COMPLETION_REPORT.md
- 專案完成報告
- 詳細的任務清單與完成情況
- 適合審查專案進度

#### PROJECT_OVERVIEW.txt
- 可視化專案總覽
- 快速了解專案結構和特點
- 使用 ASCII 藝術美化顯示

### 配置文件

#### requirements.txt
Python 依賴包清單：
- jieba ≥ 0.42.1 - 中文分詞
- ijson ≥ 3.2.0 - 流式 JSON 處理
- requests ≥ 2.28.0 - HTTP 請求
- tqdm ≥ 4.65.0 - 進度條顯示

#### setup.sh
一鍵安裝腳本，自動完成：
- Python 版本檢查
- 虛擬環境創建（可選）
- 依賴包安裝

#### .gitignore
Git 版本控制配置，忽略：
- Python 緩存文件（__pycache__/）
- 虛擬環境（venv/）
- 數據文件（*.json, 除配置文件外）
- 索引文件（indexes/, *.pkl）
- 日誌文件（*.log）

## 目錄說明

### data/
- **用途**: 存放原始數據文件
- **內容**: 維基百科數據集
- **大小**: 約 2.88 GB
- **說明**: 此目錄不納入版本控制（在 .gitignore 中）

### indexes/
- **用途**: 存放生成的索引文件
- **內容**: 序列化的反向索引
- **大小**: 約 780 MB
- **說明**: 自動生成，不納入版本控制

### scripts/
- **用途**: 存放輔助腳本
- **內容**: 數據下載、處理等工具腳本
- **說明**: 與核心功能分離，保持主目錄簡潔

### docs/
- **用途**: 存放詳細文檔
- **內容**: 技術文檔、專案總結等
- **說明**: 與主 README 分離，便於組織

## 工作流程

### 初次使用

```bash
# 1. 安裝依賴
./setup.sh

# 2. 準備數據（如果還沒有數據文件）
python scripts/download_wiki.py
# 或手動將數據文件放到 data/ 目錄

# 3. 建立索引
python build_index.py

# 4. 查詢使用
python query_idf.py 蝙蝠俠
```

### 日常使用

索引建立完成後，可以直接查詢：

```bash
python query_idf.py 台灣
python query_idf.py 人工智慧
python query_idf.py 量子力學
```

## 文件大小統計

| 類型 | 文件數 | 總大小 |
|-----|--------|--------|
| 核心代碼 | 2 個 | ~10 KB |
| 輔助腳本 | 1 個 | ~4 KB |
| 文檔文件 | 7 個 | ~30 KB |
| 配置文件 | 3 個 | ~3 KB |
| 數據文件 | 1 個 | ~2.88 GB |
| 索引文件 | 1 個 | ~780 MB |
| **總計** | **15 個** | **~3.66 GB** |

## 設計原則

1. **模組化**: 功能分離，各司其職
2. **清晰性**: 目錄結構一目了然
3. **專業性**: 符合業界標準
4. **可維護**: 易於擴展和修改
5. **文檔化**: 完整的說明文檔

## 注意事項

1. **數據文件**: 大型文件，不要提交到 Git
2. **索引文件**: 可重新生成，不要提交到 Git
3. **虛擬環境**: 建議使用，避免依賴衝突
4. **路徑引用**: 所有路徑都使用相對路徑，確保可移植性

---

*本文件最後更新: 2023*
*專案: Information Retrieval HW4*
