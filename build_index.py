#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文維基百科反向索引建立與 IDF 計算

本模組實現了基於反向索引的中文維基百科索引系統，支持：
- 大規模文檔的流式讀取
- 中文分詞處理
- 反向索引建立
- IDF 值計算

作者: Information Retrieval HW4
日期: 2023
"""

import json
import os
import math
import jieba
import pickle
from collections import defaultdict


class InvertedIndex:
    """反向索引類"""
    
    def __init__(self):
        self.index = defaultdict(set)  # term -> set of doc_ids
        self.doc_count = 0
        
    def add_document(self, doc_id, terms):
        """添加文檔到索引"""
        for term in terms:
            self.index[term].add(doc_id)
    
    def get_document_frequency(self, term):
        """獲取詞彙的文檔頻率"""
        return len(self.index.get(term, set()))
    
    def get_idf(self, term):
        """計算詞彙的 IDF 值"""
        df = self.get_document_frequency(term)
        if df == 0:
            return 0
        return math.log10(self.doc_count / df)
    
    def save(self, filepath):
        """保存索引到文件"""
        with open(filepath, 'wb') as f:
            pickle.dump({'index': dict(self.index), 'doc_count': self.doc_count}, f)
    
    def load(self, filepath):
        """從文件加載索引"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.index = defaultdict(set, {k: set(v) for k, v in data['index'].items()})
            self.doc_count = data['doc_count']


def build_inverted_index():
    """構建反向索引"""
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
        return None
    
    print(f"成功讀取 {len(articles)} 篇文章")
    
    # 創建反向索引
    inverted_index = InvertedIndex()
    inverted_index.doc_count = len(articles)
    
    print("正在構建反向索引並進行中文分詞...")
    for idx, article in enumerate(articles):
        if idx % 1000 == 0:
            print(f"已處理 {idx}/{len(articles)} 篇文章...")
        
        # 使用 jieba 進行中文分詞
        terms = list(jieba.cut(article))
        
        # 添加到反向索引
        inverted_index.add_document(idx, terms)
    
    print("反向索引構建完成！")
    
    # 保存索引
    os.makedirs('indexes', exist_ok=True)
    inverted_index.save('indexes/inverted_index.pkl')
    print("索引已保存到 indexes/inverted_index.pkl")
    
    return inverted_index


def get_idf_value(inverted_index, term):
    """獲取指定詞彙的 IDF 值"""
    print(f"\n正在計算「{term}」的 IDF 值...")
    
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
    # 步驟 1: 構建反向索引
    inverted_index = build_inverted_index()
    
    if inverted_index:
        # 步驟 2: 計算「蝙蝠俠」的 IDF 值
        get_idf_value(inverted_index, '蝙蝠俠')
    else:
        print("索引構建失敗")
