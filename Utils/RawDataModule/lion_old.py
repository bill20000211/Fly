import json
from datetime import datetime
import re

def convert_price_to_int(price_str):
    """將價格字串轉換為整數"""
    if price_str is None:
        return None
    
    try:
        # 移除所有逗號
        cleaned_price = price_str.replace(',', '')
        # 轉換為整數
        return int(cleaned_price)
    except (ValueError, AttributeError):
        # 如果轉換失敗，則返回原字串
        return price_str

def extract_ids_from_status_url(status_url):
    """從 StatusUrl 提取 GroupID 和 NormGroupID"""
    norm_group_id = re.search(r'NormGroupID=([^&]+)', status_url)
    group_id = re.search(r'GroupID=([^&]+)', status_url)
    
    return {
        'norm_group_id': norm_group_id.group(1) if norm_group_id else '',
        'group_id': group_id.group(1) if group_id else ''
    }

# 假設 group_info.get('GoDate') 和 group_info.get('BackDate') 是 '2025/03/05' 格式的字串
def format_date(date_str):
    # 先將日期字串轉換成 datetime 物件，再將其格式化為 'YYYY-MM-DD' 格式
    return datetime.strptime(date_str, '%Y/%m/%d').strftime('%Y-%m-%d')

def process_json_data(data):
    """
    處理雄獅格式的JSON資料
    
    Args:
        data: 已載入的JSON資料
        
    Returns:
        list: 處理後的資料列表
    """
    result_list = []
    id_counter = 1
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 處理航班資訊
    go_flight = data.get('GoFlight', {})
    back_flight = data.get('BackFlight', {})
    
    # 組合航班描述
    description = []
    if go_flight:
        go_desc = (f"去程：{go_flight.get('Airline')} "
                  f"{go_flight.get('DepartureAirport')}({go_flight.get('DepartureTime')}) → "
                  f"{go_flight.get('ArriveAirport')}({go_flight.get('ArriveTime')})")
        description.append(go_desc)
    
    if back_flight:
        back_desc = (f"回程：{back_flight.get('Airline')} "
                    f"{back_flight.get('DepartureAirport')}({back_flight.get('DepartureTime')}) → "
                    f"{back_flight.get('ArriveAirport')}({back_flight.get('ArriveTime')})")
        description.append(back_desc)
    
    # 取得團體資訊
    group_info = data.get('GroupInfo', {})
    
    # 從 StatusUrl 提取資訊並組合 src URL
    status_url = group_info.get('StatusUrl', '')
    ids = extract_ids_from_status_url(status_url)
    src_url = f"https://travel.liontravel.com/detail?GroupID={ids['group_id']}&Platform=APP&NormGroupID={ids['norm_group_id']}"
    
    # 處理座位資訊
    seats_info = group_info.get('Seats', {})

    # 處理價格資訊
    pricing_info = group_info.get('Pricing', {})

    result_dict = {
        'supplier': 'LionTravel',
        'prod_oid': group_info.get('TourID'),
        'pkg_oid': group_info.get('NormGroupID'),
        'prod_name': group_info.get('TourName'),
        'pkg_name': group_info.get('NormGroup'),
        'description': ' | '.join(description),
        # 將日期格式轉換為 'YYYY-MM-DD'
        'departure_date': format_date(group_info.get('GoDate')),
        'return_date': format_date(group_info.get('BackDate')),
        
        'seats_total': seats_info.get('Total'),
        'seats_quota': seats_info.get('Quota'),
        'seats_spare': seats_info.get('Spare'),
        'seats_actual': seats_info.get('Actual'),
        'seats_wait': seats_info.get('Wait'),
        'seats_kk': seats_info.get('KK'),
        'seats_keep': seats_info.get('Keep'),
        'seats_ob': seats_info.get('OB'),
        
        'straight_lowest_price': pricing_info.get('StraightLowestPrice'),
        'industry_lowest_price': pricing_info.get('IndustryLowestPrice'),
        'price': convert_price_to_int(pricing_info.get('Price')),
        
        'src': src_url,
        'last_updated': current_time
    }
    
    result_list.append(result_dict)

    return result_list

def lion_process_json_file(file_path):
    """
    處理雄獅格式的JSON檔案
    
    Args:
        file_path (str): JSON檔案的路徑
        
    Returns:
        list: 處理後的資料列表
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return process_json_data(data)

def lion_save_to_json(data, output_file):
    """
    將資料儲存為JSON檔案
    
    Args:
        data (list): 要儲存的資料
        output_file (str): 輸出檔案路徑
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)