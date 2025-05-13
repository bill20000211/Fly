import os
import sys
import json
from datetime import datetime
import urllib.parse

from Utils.CrawlerModule.kkday import KKdayFlightScraper
from Utils.CrawlerModule.lion import LionFlightScraper

"""
爬蟲時間區間皆為 90天
"""

def crawler_kkday(keyword, output_path="./crawler_output"):
    """
    使用KKdayFlightScraper爬取KKday網站上的產品資訊
    
    Parameters:
    ----------
    keyword : str
        搜尋關鍵字，例如: "計畫機票"、"日本行程" 等
    output_path : str, optional
        輸出JSON檔案的儲存路徑，預設為 "./crawler_output"
        
    Returns:
    -------
    tuple
        (all_product_data, output_file_path)
        all_product_data: 爬蟲獲取的原始資料
        output_file_path: JSON檔案的完整路徑，失敗時為None
    """
    # 確保輸出目錄存在
    os.makedirs(output_path, exist_ok=True)
    
    # 構建搜尋URL
    encoded_keyword = urllib.parse.quote(keyword.strip())
    url = f'https://www.kkday.com/zh-tw/product/ajax_get_product_list?keyword={encoded_keyword}&currency=TWD&sort=prec&count=50'
    
    # 創建爬蟲實例
    kkday_scraper = KKdayFlightScraper(url, max_retries=5)
    
    # 更改輸出路徑 - 使用符合Windows文件名規範的格式 (不含冒號和空格)
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_keywords = keyword.replace(' ', '_').replace('/', '_')
    output_file = os.path.join(output_path, f"kkday_{safe_keywords}_{current_time}_data.json")
    
    # 執行爬蟲
    print(f"開始爬取kkday關鍵字: '{keyword}' 的資料")
    kkday_crawler_data = kkday_scraper.run()
    
    # 判斷是否成功爬取資料
    if kkday_crawler_data:
        # 儲存資料為JSON
        kkday_scraper.save_to_json(kkday_crawler_data, output_file)
        return kkday_crawler_data, output_path
    else:
        return [], None


def crawler_lion(keyword, output_path="./crawler_output"):
    """
    使用LionFlightScraper爬取雄獅旅遊網站上的產品資訊，並將所有資料儲存到單一JSON檔案
    
    Parameters:
    ----------
    keywords : str, optional
        搜尋關鍵字，例如: "超值特惠機票"、"東京自由行" 等，預設為 "超值特惠機票"
    output_path : str, optional
        輸出JSON檔案的儲存路徑，預設為 "./crawler_output"
        
    Returns:
    -------
    tuple
        (all_product_data, output_file_path)
        all_product_data: 爬蟲獲取的原始資料
        output_file_path: JSON檔案的完整路徑，失敗時為None
    """
    # 確保輸出目錄存在
    os.makedirs(output_path, exist_ok=True)
    
    # 創建爬蟲實例
    encoded_keyword = urllib.parse.quote(keyword.strip())
    lion_scraper = LionFlightScraper(encoded_keyword)
    
    # 更改輸出設定
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_keywords = keyword.replace(' ', '_').replace('/', '_')
    output_file = os.path.join(output_path, f"lion_{safe_keywords}_{current_time}_data.json")
    
    # 執行爬蟲
    print(f"開始爬取雄獅旅遊關鍵字: '{keyword}' 的資料")
    lion_crawler_data = lion_scraper.run()
    
    # 檢查爬蟲結果並儲存
    if lion_crawler_data:
        # 將所有資料儲存為單一JSON檔案
        lion_scraper.save_to_json(lion_crawler_data,output_file)
        return lion_crawler_data, output_path
    else:
        print("未獲取到任何產品資料")
        return [], None