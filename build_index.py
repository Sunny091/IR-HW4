#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文維基百科反向索引建立與 IDF 計算（使用 Pyserini）

- 大規模文檔的流式讀取
- 中文分詞處理（使用 jieba）
- 使用 Pyserini/Lucene 建立反向索引
- IDF 值計算

作者: Information Retrieval HW4
日期: 2023
"""

import json
import os
import jieba
from pyserini.index.lucene import IndexReader


def build_inverted_index():
    """構建反向索引（使用 Pyserini）"""

    # 確保"蝙蝠俠"不會被 jieba 切分
    jieba.add_word("蝙蝠俠")

    print("正在讀取中文維基百科數據...")

    articles = []

    # 數據文件路徑
    data_file = 'data/wiki_article_list_2023_tra.json'

    # 使用 ijson 進行流式讀取
    try:
        import ijson
        print("使用 ijson 進行流式讀取...")

        with open(data_file, 'rb') as f:
            parser = ijson.items(f, 'item')
            for idx, article in enumerate(parser):
                if idx % 1000 == 0:
                    print(f"已讀取 {idx} 篇文章...")
                articles.append(article)

    except ImportError:
        print("ijson 未安裝，使用標準方法...")
        # 回退到標準讀取
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                articles = json.load(f)
        except Exception as e:
            print(f"讀取失敗: {e}")
            print("嘗試讀取部分有效數據...")

            # 逐行手動解析
            with open(data_file, 'r', encoding='utf-8', errors='replace') as f:
                current_article = ""
                in_string = False
                escape_next = False

                for line in f:
                    for char in line:
                        if escape_next:
                            if in_string:
                                current_article += char
                            escape_next = False
                            continue

                        if char == '\\':
                            escape_next = True
                            if in_string:
                                current_article += char
                            continue

                        if char == '"':
                            in_string = not in_string
                            if not in_string and current_article.strip():
                                # 完成一篇文章
                                articles.append(current_article)
                                current_article = ""
                                if len(articles) % 1000 == 0:
                                    print(f"已讀取 {len(articles)} 篇文章...")
                        elif in_string:
                            current_article += char
    except Exception as e:
        print(f"讀取過程出錯: {e}")

    if not articles:
        print("錯誤：無法讀取任何文章數據")
        return False

    print(f"成功讀取 {len(articles)} 篇文章")

    # 準備 Pyserini 所需的 JSONL 格式文檔
    # 每篇文章進行分詞處理
    print("正在準備分詞後的文檔...")
    os.makedirs('processed_data', exist_ok=True)
    jsonl_file = 'processed_data/wiki_segmented.jsonl'

    with open(jsonl_file, 'w', encoding='utf-8') as f:
        for idx, article in enumerate(articles):
            if idx % 1000 == 0:
                print(f"已處理 {idx}/{len(articles)} 篇文章...")

            # 使用 jieba 進行中文分詞
            segmented_text = ' '.join(jieba.cut(article))

            # 準備 Pyserini 格式的文檔
            doc = {
                'id': str(idx),
                'contents': segmented_text
            }
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')

    print(f"分詞完成，已保存到 {jsonl_file}")

    # 使用 Pyserini 建立索引
    print("\n正在使用 Pyserini 建立反向索引...")
    print("請執行以下命令來建立索引：")
    print(f"\npython -m pyserini.index.lucene \\")
    print(f"  --collection JsonCollection \\")
    print(f"  --input processed_data \\")
    print(f"  --index indexes/pyserini_index \\")
    print(f"  --generator DefaultLuceneDocumentGenerator \\")
    print(f"  --threads 1 \\")
    print(f"  --storePositions --storeDocvectors --storeRaw\n")

    return True


def get_idf_value(term, index_path='indexes/pyserini_index'):
    """使用 Pyserini 獲取指定詞彙的 IDF 值（不分詞，直接查找完整詞彙）"""

    try:
        # 讀取 Pyserini 索引
        index_reader = IndexReader(index_path)
    except Exception as e:
        print(f"錯誤：無法讀取索引")
        print(f"錯誤訊息：{e}")
        print("請確保已使用 Pyserini 建立索引")
        return

    print(f"\n正在計算「{term}」的 IDF 值...")

    # 獲取索引統計資訊
    total_docs = index_reader.stats()['documents']
    print(f"索引中共有 {total_docs} 篇文檔")

    # 直接查找完整詞彙，不進行分詞
    # 獲取該詞彙的文檔頻率（DF）
    # get_term_counts() 返回 (df, cf) tuple，我們只需要 df（第一個元素）
    result = index_reader.get_term_counts(term, analyzer=None)
    df = result[0] if result[0] is not None else 0

    if df > 0:
        # 計算 IDF 值
        import math
        idf = math.log10(total_docs / df)

        print(f"\n詞彙: {term}")
        print(f"文檔頻率 (DF): {df}")
        print(f"IDF 值: {idf:.6f}")
    else:
        print(f"\n詞彙「{term}」在索引中未找到")
        print(f"這可能是因為：")
        print(f"  1. 該詞彙在維基百科語料中不存在")
        print(f"  2. jieba 將該詞彙切分成了其他形式")


if __name__ == '__main__':
    # 步驟 1: 準備分詞後的文檔並提示建立索引
    success = build_inverted_index()

    if success:
        print("\n" + "=" * 60)
        print("文檔準備完成！")
        print("請先執行上述 Pyserini 建立索引命令")
        print("索引建立完成後，請執行以下命令查詢 IDF 值：")
        print("  python query_idf.py 蝙蝠俠")
        print("=" * 60)
    else:
        print("文檔準備失敗")
