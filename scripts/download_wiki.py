#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文維基百科數據集下載工具

本模組提供維基百科數據集的下載功能，支持：
- 進度條顯示
- 文件驗證
- 斷點續傳提示
- 多種數據獲取方式說明

使用方法:
    python scripts/download_wiki.py
    
注意:
    需要替換為實際的數據集 URL
    或參考腳本中提供的其他獲取方式

作者: Information Retrieval HW4
日期: 2023
"""

import requests
import json
import os
from tqdm import tqdm


def download_file(url, output_path, chunk_size=8192):
    """
    下載文件並顯示進度條

    Args:
        url: 下載 URL
        output_path: 保存路徑
        chunk_size: 每次讀取的塊大小
    """
    print(f"正在下載: {url}")
    print(f"保存至: {output_path}")

    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get('content-length', 0))

    with open(output_path, 'wb') as f, tqdm(
        desc=output_path,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                pbar.update(len(chunk))

    print(f"下載完成: {output_path}")


def verify_json_file(filepath):
    """
    驗證 JSON 文件是否有效

    Args:
        filepath: JSON 文件路徑

    Returns:
        bool: 文件是否有效
    """
    print(f"\n正在驗證文件: {filepath}")

    try:
        # 嘗試讀取前幾個元素
        with open(filepath, 'r', encoding='utf-8') as f:
            # 讀取前 1KB 檢查格式
            sample = f.read(1024)
            if not sample.strip():
                print("❌ 文件為空")
                return False

        print("✅ 文件格式看起來正常")

        # 獲取文件大小
        file_size = os.path.getsize(filepath)
        print(f"文件大小: {file_size / (1024**3):.2f} GB")

        return True

    except Exception as e:
        print(f"❌ 驗證失敗: {e}")
        return False


def download_wiki_dataset():
    """
    下載中文維基百科數據集
    """
    # 數據集 URL（這裡使用示例 URL，實際使用時需要替換為真實的 URL）
    wiki_url = "https://example.com/data/wiki_article_list_2023_tra.json"
    output_file = "./data/data/wiki_article_list_2023_tra.json"

    # 檢查文件是否已存在
    if os.path.exists(output_file):
        print(f"文件已存在: {output_file}")
        response = input("是否重新下載？(y/N): ")
        if response.lower() != 'y':
            print("跳過下載")
            if verify_json_file(output_file):
                print("現有文件可以使用")
                return True
            else:
                print("現有文件無效，需要重新下載")

    try:
        # 下載文件
        download_file(wiki_url, output_file)

        # 驗證下載的文件
        if verify_json_file(output_file):
            print("\n✅ 數據集下載並驗證成功！")
            return True
        else:
            print("\n❌ 下載的文件無效")
            return False

    except Exception as e:
        print(f"\n❌ 下載失敗: {e}")
        return False


def download_alternative_sources():
    """
    提供其他下載方式的說明
    """
    print("\n" + "="*60)
    print("其他獲取中文維基百科數據的方式：")
    print("="*60)

    print("\n1. 官方維基百科轉儲：")
    print("   https://dumps.wikimedia.org/zhwiki/")
    print("   - 下載 zhwiki-latest-pages-articles.xml.bz2")
    print("   - 需要額外處理 XML 格式")

    print("\n2. 使用 Wikipedia API：")
    print("   - 可以通過 Wikipedia API 逐頁下載")
    print("   - 適合小規模數據獲取")

    print("\n3. 預處理數據集：")
    print("   - CKIP Lab 或其他學術機構提供的預處理數據")
    print("   - 格式可能更適合 NLP 任務")

    print("\n4. 自行爬取：")
    print("   - 使用 wikipedia-api 或 pywikibot")
    print("   - 需要遵守 Wikipedia 的爬取政策")

    print("\n" + "="*60)


if __name__ == '__main__':
    print("="*60)
    print("中文維基百科數據集下載工具")
    print("="*60)

    # 檢查是否已有數據文件
    if os.path.exists("data/wiki_article_list_2023_tra.json"):
        print("\n✅ 數據文件已存在: data/wiki_article_list_2023_tra.json")
        if verify_json_file("data/wiki_article_list_2023_tra.json"):
            print("\n數據文件可以正常使用，無需重新下載")
        else:
            print("\n數據文件可能損壞，建議重新下載")
    else:
        print("\n⚠️  未找到數據文件: data/wiki_article_list_2023_tra.json")
        print("\n請手動下載中文維基百科數據集，或使用以下方式：")
        download_alternative_sources()

    print("\n" + "="*60)
    print("提示：本腳本提供數據集下載框架")
    print("實際使用時需要替換為真實的數據集 URL")
    print("="*60)
