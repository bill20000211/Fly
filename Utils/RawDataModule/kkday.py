import json
from datetime import datetime

def process_json_data(data):
    """
    處理KKDay格式的JSON資料
    
    Args:
        data: 已載入的JSON資料
        
    Returns:
        list: 處理後的資料列表
    """
    result_list = []
    id_counter = 1
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for product in data:
        prod_oid = product['prod_oid']
        
        for package in product['packages']:
            pkg_oid = package['pkg_oid']
            pkg_name = package['name']
            
            # 處理description
            description = []
            if 'description_content' in package and 'list' in package['description_content']:
                for desc_item in package['description_content']['list']:
                    if 'desc' in desc_item:
                        description.append(desc_item['desc'])
            description = ' '.join(description)
            
            # 遍歷available_dates
            for departure_date, items in package['available_dates'].items():
                for item in items:
                    # 處理spec_names，分離產品類型和年齡類型
                    spec_names = item.get('spec_names', [])
                    pax_type = ''
                    prod_type = []
                    
                    # 處理spec_names
                    if spec_names:
                        for spec in spec_names:
                            if spec in ['成人', '嬰兒']:
                                pax_type = spec
                            else:
                                prod_type.append(spec)
                    
                    result_dict = {
                        'supplier': 'KKDAY',
                        'prod_oid': prod_oid,
                        'pkg_oid': pkg_oid,
                        'pkg_name': pkg_name,
                        'description': description,
                        'departure_date': departure_date,
                        'prod_type': ' '.join(prod_type),  # 只包含非年齡類型的資訊
                        'price': item.get('price', 0),
                        'pax_type': pax_type,  # 只存放年齡類型
                        'src': "https://www.kkday.com/zh-tw/product/" + str(prod_oid),
                        'last_updated': current_time
                    }
                    
                    result_list.append(result_dict)
                    id_counter += 1

    return result_list

def kkday_process_json_file(file_path):
    """
    處理KKDay格式的JSON檔案
    
    Args:
        file_path (str): JSON檔案的路徑
        
    Returns:
        list: 處理後的資料列表
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return process_json_data(data)

def kkday_save_to_json(data, output_file):
    """
    將資料儲存為JSON檔案
    
    Args:
        data (list): 要儲存的資料
        output_file (str): 輸出檔案路徑
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)