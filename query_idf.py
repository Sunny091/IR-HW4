#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IDF 值查詢工具

本模組提供命令行界面，用於查詢已建立索引中任意詞彙的 IDF 值。
支持自動中文分詞，並顯示每個分詞的詳細統計信息。

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
import jieba
import pickle
from collections import defaultdict


class InvertedIndex:
    """反向索引類"""
    
    def __init__(self):
        self.index = defaultdict(set)
        self.doc_count = 0
        
    def get_document_frequency(self, term):
        """獲取詞彙的文檔頻率"""
        return len(self.index.get(term, set()))
    
    def get_idf(self, term):
        """計算詞彙的 IDF 值"""
        df = self.get_document_frequency(term)
        if df == 0:
            return 0
        return math.log10(self.doc_count / df)
    
    def load(self, filepath):
        """從文件加載索引"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.index = defaultdict(set, {k: set(v) for k, v in data['index'].items()})
            self.doc_count = data['doc_count']


def query_idf(term, index_path='indexes/inverted_index.pkl'):
    """查詢指定詞彙的 IDF 值"""
    print(f"正在查詢「{term}」的 IDF 值...")
    
    # 讀取索引
    try:
        inverted_index = InvertedIndex()
        inverted_index.load(index_path)
    except Exception as e:
        print(f"錯誤：無法讀取索引，請確保索引已建立")
        print(f"錯誤訊息：{e}")
        return
    
    # 先對查詢詞進行分詞
    terms = list(jieba.cut(term))
    print(f"分詞結果: {' '.join(terms)}")
    
    print(f"索引中共有 {inverted_index.doc_count} 篇文檔")
    
    # 計算每個分詞的 IDF
    for t in terms:
        df = inverted_index.get_document_frequency(t)
        if df > 0:
            idf = inverted_index.get_idf(t)
            print(f"\n詞彙: {t}")
            print(f"文檔頻率 (DF): {df}")
            print(f"IDF 值: {idf:.6f}")
        else:
            print(f"\n詞彙「{t}」在索引中未找到")
    
    # 如果原詞沒有被分詞，也嘗試查找完整詞彙
    if term not in terms and len(terms) > 1:
        df = inverted_index.get_document_frequency(term)
        if df > 0:
            idf = inverted_index.get_idf(term)
            print(f"\n完整詞彙: {term}")
            print(f"文檔頻率 (DF): {df}")
            print(f"IDF 值: {idf:.6f}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("使用方法: python query_idf.py <詞彙>")
        print("例如: python query_idf.py 蝙蝠俠")
        sys.exit(1)
    
    term = sys.argv[1]
    query_idf(term)
