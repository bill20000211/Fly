import urllib.request as req
import json
import urllib.error
import gzip
import time
import random
import os
import urllib.parse
from datetime import datetime, timedelta
from fake_useragent import UserAgent

class KKdayFlightScraper:
    def __init__(self, url, max_retries=3):
        self.url = url
        self.all_product_data = []
        self.max_retries = max_retries
        self.ua = UserAgent()
            
    def get_json_response(self, url):
        """通用方法：獲取 JSON 回應"""
        retries = 0
        while retries < self.max_retries:
            try:
                headers = {
                    "User-Agent": self.ua.random,
                    "Accept": "application/json, text/plain, */*",  
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Referer": "https://www.kkday.com/zh-tw/",
                }
                request = req.Request(url, headers=headers)
                
                with req.urlopen(request) as response:
                    if response.info().get('Content-Encoding') == 'gzip':
                        return json.loads(gzip.decompress(response.read()).decode('utf-8'))
                    else:
                        return json.loads(response.read().decode('utf-8'))
                
            except urllib.error.HTTPError as e:
                print(f"HTTP Error: {e.code} - {e.reason}")
                if e.code == 403:
                    print("可能是反爬機制觸發，等待後重試...")
                elif e.code == 407:
                    print("代理認證失敗，請檢查代理設置")
                retries += 1
                if retries < self.max_retries:
                    wait_time = random.uniform(2, 5) 
                    print(f"第 {retries} 次重試，等待 {wait_time:.2f} 秒...")
                    time.sleep(wait_time)
                else:
                    print(f"已達最大重試次數 {self.max_retries}，放棄此請求")
                    return None
            except json.JSONDecodeError as e:
                print(f"JSON 解析錯誤：{e}")
                return None
            except Exception as e:
                print(f"其他錯誤：{e}")
                retries += 1
                if retries < self.max_retries:
                    wait_time = random.uniform(2, 5)
                    print(f"第 {retries} 次重試，等待 {wait_time:.2f} 秒...")
                    time.sleep(wait_time)
                else:
                    print(f"已達最大重試次數 {self.max_retries}，放棄此請求")
                    return None
        return None
    
    def get_all_product(self):
        """
        object: 取得計畫機票所有搜尋結果產品
        return: 產品總數、所有產品id
        """
        all_product_json = self.get_json_response(self.url)
        
        if all_product_json:
            all_product_data = all_product_json.get("data",{}).get("data",[])
            total_product = all_product_json.get("data",{}).get("total")
            prod_oids = [product.get("prod_oid") for product in all_product_data if product.get("prod_oid") is not None]
            return total_product, prod_oids
        return 0,[]
    
    def get_product_package(self, prod_oid):
        """取得該產品所有方案"""
        product_url = f'https://www.kkday.com/zh-tw/product/ajax_get_packages_data?prodMid={prod_oid}'
        print(f"正在獲取 product 資訊: {product_url}")
        packages_json = self.get_json_response(product_url)
        
        if not packages_json:
            print(f"無法獲取 {prod_oid} 的產品資訊")
            return []
        
        packages = packages_json.get("data", {}).get("PACKAGE", {})
        if not packages:
            print("未找到方案資訊")
            return []
        
        product_packages = []
        for pkg_oid, pkg in packages.items():
            if pkg.get("is_all_sold_out", False):
                continue

            name = pkg.get("name", "未知標題")
            description_content = pkg.get("description_module", {}).get("PMDL_PACKAGE_DESC", {}).get("content", {})
            items = pkg.get("items", [])

            earliest_sale_time = pkg.get("sale_time", {}).get("earliest_sale_time", {}).get("date")
            latest_sale_time = pkg.get("sale_time", {}).get("latest_sale_time", {}).get("date")
            
            print(f"\n方案ID {pkg_oid}: {name}")
            print(f"原始最早日期: {earliest_sale_time}, 原始最晚日期: {latest_sale_time}")

            begin_date, end_date = self._calculate_date_range(earliest_sale_time, latest_sale_time)
            print(f"調整後日期參數 - beginDate: {begin_date}, endDate: {end_date}")

            if items:
                item_oid = items[0]
                detail_url = f"https://www.kkday.com/zh-tw/product/ajax_get_items_data?pkgOid={pkg_oid}&itemOidList[]={item_oid}&beginDate={begin_date}&endDate={end_date}"
                print(f"正在獲取方案資訊: {detail_url}")
                
                detail_data = self.get_json_response(detail_url)
                if detail_data:
                    packages_data = self._process_detail_data(pkg_oid, name, description_content, detail_data)
                    product_packages.extend(packages_data)
                else:
                    print(f"無法獲取 {pkg_oid} 的方案資訊，跳過此方案")
                
                time.sleep(random.uniform(1, 3))
        
        return product_packages
    
    def _calculate_date_range(self, earliest_sale_time, latest_sale_time):
        """計算並返回有效的日期範圍"""
        today = datetime.now().date()
        default_begin_date = today.strftime("%Y-%m-%d")
        default_end_date = (today + timedelta(days=90)).strftime("%Y-%m-%d")
        
        # 設定開始日期
        begin_date = earliest_sale_time or default_begin_date
        
        # 設定結束日期
        if not latest_sale_time:
            end_date = default_end_date
        else:
            # 確保日期範圍不超過90天
            begin_datetime = datetime.strptime(begin_date, "%Y-%m-%d").date()
            end_datetime = datetime.strptime(latest_sale_time, "%Y-%m-%d").date()
            
            date_diff = (end_datetime - begin_datetime).days
            
            if date_diff > 90:
                end_date = (begin_datetime + timedelta(days=90)).strftime("%Y-%m-%d")
            else:
                end_date = latest_sale_time
        
        return begin_date, end_date
                    
    def _find_infant_sku(self, skus):
        """找出嬰兒、小孩以及學生票的 SKU ID"""
        for sku in skus:
            spec = sku.get("spec", {})
            if spec.get("spec-ticket") == "infant" or spec.get("spec-ticket") == "child" or spec.get("spec-ticket") == "student":
                return sku.get("sku_oid")
        return None
    
    def _process_detail_data(self, pkg_oid, name, description_content, detail_data):
        """處理方案詳細資訊並排除 infant 日期價格"""
        detail_info = detail_data.get("data", {})
        if not detail_info:
            print("detail_info 錯誤: 無法獲取 data")
            return []

        package_data = []
        for item_id, item_data in detail_info.items():
            # 尋找 infant 的 sku_oid
            item_info = item_data.get("item", {})
            skus = item_info.get("skus", {})
            infant_sku = self._find_infant_sku(skus)

            # 處理價格日期並排除 infant
            price_calendar = item_data.get("skusPriceCalendar", {})
            is_sold_out = item_data.get("calendar", {})
            close_list = item_data.get("closeList", {})
            available_dates = {}
            
            # 確保 close_list 是字典，如果不是則設為空字典
            if not isinstance(close_list, dict):
                close_list = {}
            
            # 處理sku的spec名稱
            specs = item_info.get("specs", {})
            
            spec_map = {}
            for spec in specs:
                spec_oid = spec["spec_oid"]
                spec_map[spec_oid] = {item["spec_item_oid"]: item["name"] for item in spec["spec_items"]}
            
            # 遍歷所有 SKU 
            for sku_oid, dates in price_calendar.items():
                if sku_oid == infant_sku:  # 跳過 infant 的資訊
                    continue
                
                # 從 skus 中找到該 sku_oid 的 spec
                sku_spec = next((sku["spec"] for sku in skus if sku["sku_oid"] == sku_oid), None)
                if not sku_spec:
                    continue

                # 提取該 SKU 的 spec 名稱
                spec_names = []
                for spec_oid, spec_item_oid in sku_spec.items():
                    if spec_oid in spec_map and spec_item_oid in spec_map[spec_oid]:
                        spec_names.append(spec_map[spec_oid][spec_item_oid])
                
                # 獲取該 SKU 在 closeList 中的關閉日期 
                closed_dates = close_list.get(sku_oid, {})
                
                # 遍歷該 SKU 的所有日期價格
                for date, price_info in dates.items():
                    # 檢查此日期價格是否已經售出
                    if price_info and price_info.get("price") and price_info["price"].get("fullday"):
                        # 檢查是否在 closeList 中
                        if date in closed_dates:  # 如果日期在 closeList 中，跳過
                            continue

                        # 檢查是否售完
                        sold_out_status = is_sold_out.get(date, {}).get("is_sold_out", True)
                        if not sold_out_status:
                            price = price_info["price"]["fullday"]
                            if date not in available_dates:
                                available_dates[date] = []
                            available_dates[date].append({
                                "price": price,
                                "spec_names": spec_names
                            })

            # 儲存處理後的數據
            product_info = {
                "pkg_oid": pkg_oid,
                "name": name,
                "description_content": description_content,
                "item_id": item_id,
                "available_dates": available_dates
            }
            package_data.append(product_info)
            
        return package_data
    
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
        # request with ajax url, starting crawler
        print("開始獲取計畫機票所有產品")
        total_product, prod_oids = self.get_all_product()
        if not prod_oids:
            print("無法獲取產品資料")
            return []
        
        print(f"總共有 {total_product} 個產品")
        time.sleep(random.uniform(1, 3))
        
        print("開始獲取各產品 json 數據...")
        
        for prod_oid in prod_oids:
            print(f"\n處理產品 {prod_oid}...")
            packages = self.get_product_package(prod_oid)
            if packages:
                self.all_product_data.append({
                    "prod_oid": prod_oid,
                    "packages": packages
                })
        
        return self.all_product_data