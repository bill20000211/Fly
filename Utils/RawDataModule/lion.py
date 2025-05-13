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

def process_json_data(data):
    """
    處理雄獅格式的多筆JSON資料
    
    Args:
        data_array: 已載入的JSON資料陣列
        
    Returns:
        list: 處理後的資料列表
    """
    result_list = []
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for item in data:
        # 從新的資料結構取得 detail_data
        group_id = item.get('group_id')
        detail_data = item.get('detail_data', {})
        
        # 處理航班資訊 - 從新的資料結構中取得
        go_flight = {
            'Airline': detail_data.get('GoAirline'),
            'DepartureTime': detail_data.get('GoDepartureTime'),
            'ArriveTime': detail_data.get('GoArriveTime'),
            'DepartureAirport': detail_data.get('GoDepartureAirport'),
            'ArriveAirport': detail_data.get('GoArriveAirport')
        }
        
        back_flight = {
            'Airline': detail_data.get('BackAirline'),
            'DepartureTime': detail_data.get('BackDepartureTime'),
            'ArriveTime': detail_data.get('BackArriveTime'),
            'DepartureAirport': detail_data.get('BackDepartureAirport'),
            'ArriveAirport': detail_data.get('BackArriveAirport')
        }
        
        # 組合航班描述
        description = []
        if go_flight['Airline']:
            go_desc = (f"去程：{go_flight['Airline']} "
                      f"{go_flight['DepartureAirport']}({go_flight['DepartureTime']}) → "
                      f"{go_flight['ArriveAirport']}({go_flight['ArriveTime']})")
            description.append(go_desc)
        
        if back_flight['Airline']:
            back_desc = (f"回程：{back_flight['Airline']} "
                        f"{back_flight['DepartureAirport']}({back_flight['DepartureTime']}) → "
                        f"{back_flight['ArriveAirport']}({back_flight['ArriveTime']})")
            description.append(back_desc)
        
        # 取得團體資訊
        group_info = detail_data.get('GroupInfo', {})
        
        # 從 StatusUrl 提取資訊並組合 src URL
        status_url = group_info.get('StatusUrl', '')
        src_url = f"https://travel.liontravel.com/detail?GroupID={group_id}&Platform=APP&NormGroupID={group_info.get('NormGroupID')}"
        
        # 處理座位資訊 - 在新的資料結構中直接取得
        seats_info = {
            'Total': group_info.get('TotalSeats'),
            'Quota': group_info.get('QuotaSeats'),
            'Spare': group_info.get('SpareSeats'),
            'Actual': group_info.get('ActualSeats'),
            'Wait': group_info.get('WaitSeats'),
            'KK': group_info.get('KKSeats'),
            'Keep': group_info.get('KeepSeats'),
            'OB': group_info.get('OBSeats')
        }

        # 處理價格資訊 - 在新的資料結構中直接取得
        pricing_info = {
            'StraightLowestPrice': group_info.get('StraightLowestPrice'),
            'IndustryLowestPrice': group_info.get('IndustryLowestPrice'),
            'Price': group_info.get('Price')
        }

        result_dict = {
            'supplier': 'LionTravel',
            'prod_oid': group_id,
            'pkg_oid': group_info.get('NormGroupID'),
            'prod_name': group_info.get('TourName'),
            'pkg_name': group_info.get('NormGroup'),
            'description': ' | '.join(description),
            'departure_date': group_info.get('GoDate'),
            'return_date': group_info.get('BackDate'),
            
            'seats_total': seats_info['Total'],
            'seats_quota': seats_info['Quota'],
            'seats_spare': seats_info['Spare'],
            'seats_actual': seats_info['Actual'],
            'seats_wait': seats_info['Wait'],
            'seats_kk': seats_info['KK'],
            'seats_keep': seats_info['Keep'],
            'seats_ob': seats_info['OB'],
            
            'straight_lowest_price': pricing_info['StraightLowestPrice'],
            'industry_lowest_price': pricing_info['IndustryLowestPrice'],
            'price': convert_price_to_int(pricing_info['Price']),
            
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