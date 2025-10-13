# 技術文檔

## 系統架構

### 反向索引 (Inverted Index)

反向索引是信息檢索系統的核心數據結構，它建立從詞彙到文檔的映射關係。

#### 數據結構

```python
{
    "詞彙1": {doc_id1, doc_id2, doc_id3, ...},
    "詞彙2": {doc_id5, doc_id6, ...},
    ...
}
```

#### 特點

- **快速檢索**：O(1) 時間複雜度查找詞彙
- **空間效率**：使用 set 存儲文檔 ID，自動去重
- **持久化**：使用 pickle 序列化，支持快速載入

### IDF 計算

#### 公式

```
IDF(t) = log₁₀(N / DF(t))
```

其中：
- `N`：語料庫中的總文檔數
- `DF(t)`：包含詞彙 t 的文檔數量

#### 意義

- IDF 值越高，詞彙越稀有，在檢索中越重要
- 常見詞（如「的」、「是」）IDF 值低
- 專有名詞（如「蝙蝠俠」）IDF 值高

### 中文分詞

使用 jieba 分詞庫：

```python
import jieba
text = "蝙蝠俠是一個超級英雄"
words = jieba.cut(text)
# 結果: ['蝙蝠俠', '是', '一個', '超級', '英雄']
```

## 性能優化

### 1. 流式讀取

使用 ijson 進行流式讀取，避免內存溢出：

```python
import ijson
with open('large_file.json', 'rb') as f:
    for item in ijson.items(f, 'item'):
        process(item)
```

### 2. 批量處理

每處理 1000 個文檔輸出一次進度，平衡性能和用戶體驗。

### 3. 索引持久化

建立一次索引，多次使用，避免重複計算。

## 常見問題

### Q1: 索引建立需要多長時間？

取決於文檔數量和機器性能：
- 50,000 篇：約 5-10 分鐘
- 1,200,000 篇：約 2-4 小時

### Q2: 索引文件有多大？

大約為原始數據的 30-40%：
- 50,000 篇：約 100-200 MB
- 1,200,000 篇：約 800 MB - 1 GB

### Q3: 如何處理記憶體不足？

- 使用 ijson 流式讀取
- 分批處理文檔
- 增加系統交換空間

### Q4: 分詞結果不準確怎麼辦？

- 使用自定義詞典：`jieba.load_userdict('dict.txt')`
- 使用其他分詞工具（如 CKIP、pkuseg）

## 擴展功能

### 1. TF-IDF 計算

在 IDF 基礎上，可以計算 TF-IDF：

```python
TF-IDF(t, d) = TF(t, d) × IDF(t)
```

### 2. 相似度計算

使用餘弦相似度比較文檔：

```python
similarity = cosine_similarity(vec1, vec2)
```

### 3. 文檔檢索

根據查詢詞返回相關文檔：

```python
def search(query):
    terms = jieba.cut(query)
    doc_scores = calculate_scores(terms)
    return sorted_documents(doc_scores)
```

## 參考資料

1. Manning, C. D., Raghavan, P., & Schütze, H. (2008). Introduction to Information Retrieval.
2. Jieba 中文分詞：https://github.com/fxsjy/jieba
3. 維基百科數據轉儲：https://dumps.wikimedia.org/
