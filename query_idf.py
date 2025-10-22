#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IDF 值查詢工具（使用 Pyserini）

本模組提供命令行界面，用於查詢已建立的 Pyserini 索引中任意詞彙的 IDF 值。
直接查詢完整詞彙，不進行分詞處理。

使用方法:
    python query_idf.py <詞彙>

範例:
    python query_idf.py 蝙蝠俠
    python query_idf.py 人工智慧

作者: Information Retrieval HW4
日期: 2023
"""

import sys
import math
from pyserini.index.lucene import IndexReader


def query_idf(term, index_path='indexes/pyserini_index'):
    """使用 Pyserini 查詢指定詞彙的 IDF 值（不分詞）"""

    print(f"正在查詢「{term}」的 IDF 值...")

    # 讀取 Pyserini 索引
    try:
        index_reader = IndexReader(index_path)
    except Exception as e:
        print(f"錯誤：無法讀取索引，請確保索引已建立")
        print(f"錯誤訊息：{e}")
        print(f"\n請先執行以下步驟：")
        print(f"1. 運行 build_index.py 準備分詞後的文檔")
        print(f"2. 使用 Pyserini 建立索引")
        print(f"3. 再次執行此查詢腳本")
        return

    # 獲取索引統計資訊
    total_docs = index_reader.stats()['documents']
    print(f"索引中共有 {total_docs} 篇文檔")

    # 直接查找完整詞彙，不進行分詞
    # analyzer=None 表示不使用分析器，直接查找原始詞彙
    print(f"\n查詢詞彙: {term} (不進行分詞)")

    # 獲取該詞彙的文檔頻率（DF）
    # get_term_counts() 返回 (df, cf) tuple，我們只需要 df（第一個元素）
    result = index_reader.get_term_counts(term, analyzer=None)
    df = result[0] if result[0] is not None else 0

    if df > 0:
        # 計算 IDF 值
        print(f'"詞彙「{term}」的 DF : {df}"')
        print(f'"總文檔數 : {total_docs}"')
        idf = math.log(total_docs / df)

        print(f"\n===== 查詢結果 =====")
        print(f"詞彙: {term}")
        print(f"文檔頻率 (DF): {df}")
        print(f"IDF 值: {idf:.6f}")
        print(f"===================")
    else:
        print(f"\n詞彙「{term}」在索引中未找到")
        print(f"\n可能的原因：")
        print(f"  1. 該詞彙在中文維基百科語料中不存在")
        print(f"  2. jieba 將該詞彙切分成了其他形式")
        print(f"  3. 索引建立時該詞彙被過濾")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("使用方法: python query_idf.py <詞彙>")
        print("例如: python query_idf.py 蝙蝠俠")
        sys.exit(1)

    # 使用命令行參數而非硬編碼
    term = sys.argv[1]
    query_idf(term)
