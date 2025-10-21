# 中文維基百科索引建立與 IDF 計算

基於自定義反向索引實現的中文維基百科倒排索引系統，支持 IDF 值計算與詞彙檢索。

## 特色功能

- ✅ 純 Python 實現，無需 Java 環境
- ✅ 流式讀取大型 JSON 文件，內存高效
- ✅ 支持中文分詞與反向索引建立
- ✅ 快速 IDF 值查詢
- ✅ 索引持久化，一次建立重複使用

## 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 準備數據

如果尚未下載維基百科數據，請執行：

```bash
python scripts/download_wiki.py
```

或手動將數據文件放置在 `data/` 目錄下，命名為 `wiki_article_list_2023_tra.json`。

### 3. 建立索引

首次使用需要建立索引（根據數據量大小，可能需要數分鐘到數小時）：

```bash
python build_index.py
```

程序將自動完成：
- 讀取維基百科數據
- 中文分詞處理
- 建立反向索引
- 計算「蝙蝠俠」的 IDF 值示例

### 4. 查詢 IDF 值

索引建立完成後，可以查詢任意詞彙的 IDF 值：

```bash
python query_idf.py 蝙蝠俠
python query_idf.py 台灣
python query_idf.py 人工智慧
python query_idf.py 量子力學
```

## 項目結構

```
.
├── README.md                    # 專案說明文件
├── LICENSE                       # 授權文件
├── requirements.txt              # Python 依賴包
├── .gitignore                    # Git 忽略文件
├── setup.sh                      # 環境設定腳本
├── build_index.py                # 索引建立主程式
├── query_idf.py                  # IDF 查詢工具
├── scripts/                      # 輔助腳本
│   └── download_wiki.py          # 維基百科數據下載工具
├── data/                         # 數據目錄
│   └── wiki_article_list_2023_tra.json  # 維基百科數據文件
├── processed_data/               # 處理後的數據（自動生成）
│   └── wiki_segmented.jsonl      # 分詞後的維基百科數據
└── indexes/                      # 索引文件（自動生成）
    ├── inverted_index.pkl        # 序列化的反向索引
    └── pyserini_index/           # Pyserini 索引目錄
```

## 技術架構

### 反向索引 (Inverted Index)

反向索引是信息檢索的核心數據結構，建立從詞彙到文檔的映射：

```python
{
    "詞彙": {doc_id1, doc_id2, doc_id3, ...}
}
```

**優勢：**
- O(1) 查詢時間複雜度
- 使用 set 自動去重
- pickle 序列化支持快速持久化

### 中文分詞

採用 **jieba** 中文分詞工具：

```python
import jieba
text = "蝙蝠俠是一個超級英雄"
words = jieba.cut(text)  # ['蝙蝠俠', '是', '一個', '超級', '英雄']
```

### IDF 計算公式

```
IDF(t) = log₁₀(N / DF(t))
```

**參數說明：**
- `N`：語料庫總文檔數
- `DF(t)`：包含詞彙 t 的文檔數量

**意義：**
- IDF 值越高 → 詞彙越罕見 → 檢索權重越大
- 常用詞（如「的」、「是」）IDF 值低
- 專有名詞（如「蝙蝠俠」）IDF 值高

## 使用示例

### 建立索引並查詢

```bash
# 建立索引
$ python build_index.py
正在讀取中文維基百科數據...
使用 ijson 進行流式讀取...
已讀取 0 篇文章...
已讀取 1000 篇文章...
...
成功讀取 1208139 篇文章
正在構建反向索引並進行中文分詞...
已處理 0/1208139 篇文章...
...
反向索引構建完成！
索引已保存到 indexes/inverted_index.pkl

正在計算「蝙蝠俠」的 IDF 值...
分詞結果: 蝙蝠俠
索引中共有 1208139 篇文檔

詞彙: 蝙蝠俠
文檔頻率 (DF): 580
IDF 值: 3.35815
```

## 性能說明

### 索引建立時間

| 文檔數量 | 預計時間 | 索引大小 |
|---------|---------|---------|
| 50,000 篇 | 5-10 分鐘 | ~100-200 MB |
| 500,000 篇 | 30-60 分鐘 | ~400-600 MB |
| 1,200,000 篇 | 2-4 小時 | ~800 MB-1 GB |

*註：實際時間取決於 CPU 性能和內存大小*

### 優化特性

1. **流式讀取**：使用 ijson 避免內存溢出
2. **批量處理**：每 1000 篇顯示進度
3. **持久化**：索引建立一次，重複使用
4. **內存效率**：使用 set 存儲文檔 ID

## 進階使用

### 自定義詞典

提高分詞準確度：

```python
import jieba
jieba.load_userdict('custom_dict.txt')
```

### 批量查詢

```python
from query_idf import query_idf

terms = ['蝙蝠俠', '台灣', '人工智慧']
for term in terms:
    query_idf(term)
```

## 常見問題

### Q: 記憶體不足怎麼辦？

A: 使用流式讀取（ijson）可以大幅降低記憶體使用。若仍不足，可考慮：
- 分批處理文檔
- 增加系統 swap 空間
- 使用性能更好的機器

### Q: 分詞結果不準確？

A: 可以：
- 使用自定義詞典：`jieba.load_userdict()`
- 嘗試其他分詞工具（CKIP、pkuseg）
- 調整 jieba 分詞模式

### Q: 索引文件太大？

A: 可以：
- 使用壓縮（gzip）存儲
- 只索引關鍵詞彙
- 定期清理低頻詞

## 依賴項目

- [jieba](https://github.com/fxsjy/jieba) - 中文分詞
- [ijson](https://github.com/ICRAR/ijson) - 流式 JSON 解析
- [requests](https://requests.readthedocs.io/) - HTTP 請求
- [tqdm](https://github.com/tqdm/tqdm) - 進度條

## 授權

本項目僅供學習研究使用。

## 貢獻

歡迎提交 Issue 和 Pull Request！
