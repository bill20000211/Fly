import requests
import json
import time
import os
import random
from datetime import datetime, timedelta
from fake_useragent import UserAgent

class LionFlightScraper:
    def __init__(self, keyword="超值特惠機票", travel_type=0, max_retries=5):
        """初始化雄獅旅遊爬蟲"""
        self.keyword = keyword
        self.travel_type = travel_type
        self.max_retries = max_retries
        self.ua = UserAgent()
        
        # 設定時間範圍為三個月
        self.today = datetime.now()
        self.go_date_start = self.today.strftime("%Y-%m-%d")
        self.go_date_end = (self.today + timedelta(days=90)).strftime("%Y-%m-%d")
        
        # 存儲所有抓取到的數據
        self.all_product_data = []
        
        # API 網址
        self.search_api_url = "https://travel.liontravel.com/search/grouplistinfojson"
        self.detail_api_url = "https://travel.liontravel.com/detail/travelinfojson"
    
    def get_json_response(self, url, payload, method="POST"):
        """通用方法：獲取 JSON 回應"""
        retries = 0
        while retries < self.max_retries:
            try:
                headers = {
                    "User-Agent": self.ua.random,
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Referer": "https://travel.liontravel.com/",
                }
                
                if method.upper() == "POST":
                    response = requests.post(url, json=payload, headers=headers)
                else:
                    response = requests.get(url, params=payload, headers=headers)
                
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"HTTP 錯誤: {response.status_code}")
                    retries += 1
                    if retries < self.max_retries:
                        wait_time = random.uniform(2, 5)
                        print(f"第 {retries} 次重試，等待 {wait_time:.2f} 秒...")
                        time.sleep(wait_time)
                    else:
                        print(f"已達最大重試次數 {self.max_retries}，放棄此請求")
                        return None
                        
            except requests.RequestException as e:
                print(f"請求錯誤: {e}")
                retries += 1
                if retries < self.max_retries:
                    wait_time = random.uniform(2, 5)
                    print(f"第 {retries} 次重試，等待 {wait_time:.2f} 秒...")
                    time.sleep(wait_time)
                else:
                    print(f"已達最大重試次數 {self.max_retries}，放棄此請求")
                    return None
            except json.JSONDecodeError as e:
                print(f"JSON 解析錯誤: {e}")
                return None
            except Exception as e:
                print(f"其他錯誤: {e}")
                retries += 1
                if retries < self.max_retries:
                    wait_time = random.uniform(2, 5)
                    print(f"第 {retries} 次重試，等待 {wait_time:.2f} 秒...")
                    time.sleep(wait_time)
                else:
                    print(f"已達最大重試次數 {self.max_retries}，放棄此請求")
                    return None
        return None
    
    def get_search_payload(self, page=1, page_size=10):
        """建立搜尋 API 的 payload"""
        return {
            "ArriveID": "",
            "GoDatestart": self.go_date_start,
            "GroupID": None,
            "Keywords": self.keyword,
            "IsEnsureGroup": None,
            "IsSold": True,
            "ThemeID": None,
            "TravelPavilionGroupID": None,
            "KeywordsCity": None,
            "TravelType": self.travel_type,
            "BuIDs": "",
            "PreferAirlines": None,
            "GoDateEnd": self.go_date_end,
            "DepartureID": "",
            "WeekDay": "",
            "PriceList": None,
            "AirlineIDs": "",
            "TripTypes": "",
            "Tags": "",
            "SortType": None,
            "Days": "",
            "Page": page,
            "PageSize": page_size
        }
    
    def get_all_groups(self):
        """
        object: 獲取所有 NormGroupID 和 GroupID 列表
        return: NormGroupIDs 列表、GroupIDs 列表
        """
        print("正在獲取 NormGroupID 和 GroupID 列表...")
        
        # 第一次請求，獲取總數量
        initial_payload = self.get_search_payload()
        initial_data = self.get_json_response(self.search_api_url, initial_payload)
        
        if not initial_data:
            print("無法獲取初始數據")
            return [], []
        
        total_count = initial_data.get("TotalCount", 0)
        print(f"找到共 {total_count} 筆旅遊資料")
        
        if total_count <= 0:
            print("未找到任何旅遊資料")
            return [], []
        
        # 第二次請求，取得所有資料
        final_payload = self.get_search_payload(page_size=total_count)
        all_data = self.get_json_response(self.search_api_url, final_payload)
        
        if not all_data:
            print("無法獲取完整數據列表")
            return [], []
        
        # 提取所有 NormGroupID
        norm_group_ids = []
        for item in all_data.get("NormGroupList", []):
            norm_group_id = item.get("NormGroupID")
            tour_name = item.get("TourName")
            
            if norm_group_id:
                norm_group_ids.append((norm_group_id, tour_name))
        
        # 提取所有 GroupID
        all_group_ids = []
        for item in all_data.get("NormGroupList", []):
            for group in item.get("GroupList", []):
                group_id = group.get("GroupID")
                if group_id and group_id not in all_group_ids:
                    all_group_ids.append(group_id)
        
        # 輸出所有 NormGroupID
        if norm_group_ids:
            print(f"\n找到 {len(norm_group_ids)} 個 NormGroupID:")
            for i, (norm_id, tour_name) in enumerate(norm_group_ids):
                print(f"{i+1}. NormGroupID: {norm_id} | 行程名稱: {tour_name}")
        
        print(f"\n總共找到 {len(all_group_ids)} 個 GroupID")
        
        return norm_group_ids, all_group_ids
    
    def get_group_detail(self, group_id):
        """獲取指定 GroupID 的詳細資訊"""
        print(f"正在獲取 GroupID: {group_id} 的詳細資訊...")
        
        payload = {"GroupID": group_id, "TourBu": "T"}
        detail_data = self.get_json_response(self.detail_api_url, payload)
        
        if detail_data:
            print(f"✅ 成功獲取 GroupID: {group_id} 的詳細資訊")
            return detail_data
        else:
            print(f"❌ 無法獲取 GroupID: {group_id} 的詳細資訊")
            return None
    
    def save_to_json(self, data, output_file):
        """
        將資料儲存為JSON檔案
        
        Args:
            data (list): 要儲存的資料
            output_file (str): 輸出檔案路徑
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"數據已保存至 {output_file}")
    
    def run(self):
        """執行爬蟲流程"""
        
        # 獲取所有 NormGroupID 和 GroupID
        _, all_group_ids = self.get_all_groups()
        
        if not all_group_ids:
            print("無法獲取 GroupID 資料")
            return False
        
        # 獲取每個 GroupID 的詳細資訊
        print(f"\n開始獲取各 GroupID 的詳細資訊...")
        successful_count = 0
        
        for i, group_id in enumerate(all_group_ids):
            print(f"\n處理 GroupID [{i+1}/{len(all_group_ids)}]: {group_id}")
            group_data = self.get_group_detail(group_id)
            
            if group_data:
                self.all_product_data.append({
                    "group_id": group_id,
                    "detail_data": group_data
                })
                successful_count += 1
            
            # 隨機暫停以避免請求過於頻繁
            wait_time = random.uniform(0.5, 2)
            time.sleep(wait_time)

        return self.all_product_data
