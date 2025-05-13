import os
from datetime import datetime

# 修正導入方式
# 如果 kkday.py 和 lion.py 是模組，則直接導入
from Utils.RawDataModule.kkday import *
from Utils.RawDataModule.lion import *

# 如果這些是包含處理函數的模組，則直接導入函數
# from RawDataModule.kkday import process_json_file as kkday_process
# from RawDataModule.lion import process_json_file as lion_process


def CrawlertoRawData_kkday(directory_path, output_dir=None):
    """處理指定目錄下的所有KKDay JSON檔案，可作為功能性函式被呼叫
    
    Args:
        directory_path: 包含爬蟲原始資料的目錄路徑
        output_dir: 輸出目錄的路徑，若為None則輸出到當前目錄
        
    Returns:
        tuple: (處理後的資料列表, 輸出檔案的完整路徑)
    """
    all_results = []
    id_counter = 1
    
    # 確認目錄存在
    if not os.path.isdir(directory_path):
        print(f"目錄不存在: {directory_path}")
        return all_results, None
    
    # 遍歷目錄中的所有JSON檔案
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            
            try:
                # 根據您的模組結構調整調用方式
                results = kkday_process_json_file(file_path)
                
                # 更新ID計數器
                for i, item in enumerate(results):
                    item['id'] = id_counter + i
                
                all_results.extend(results)
                id_counter += len(results)
            
            except Exception as e:
                print(f"處理 {filename} 時發生錯誤: {str(e)}")
    
    # 設定輸出檔案名稱（使用對檔案系統友好的格式）
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")  # 將冒號替換為連字符
    output_filename = f"kkday_RawData_{timestamp}.json"
    
    if output_dir:
        # 確保輸出目錄存在
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_path = os.path.join(output_dir, output_filename)
    else:
        output_path = output_filename
    
    # 儲存結果
    if all_results:
        # 根據您的模組結構調整調用方式
        kkday_save_to_json(all_results, output_path)
    else:
        print("沒有處理任何資料。")
        return all_results, None
    
    return all_results, output_path

def CrawlertoRawData_lion(directory_path, output_dir=None):
    """處理指定目錄下的所有Lion JSON檔案，可作為功能性函式被呼叫
    
    Args:
        directory_path: 包含爬蟲原始資料的目錄路徑
        output_dir: 輸出目錄的路徑，若為None則輸出到當前目錄
        
    Returns:
        tuple: (處理後的資料列表, 輸出檔案的完整路徑)
    """
    all_results = []
    id_counter = 1
    
    # 確認目錄存在
    if not os.path.isdir(directory_path):
        print(f"目錄不存在: {directory_path}")
        return all_results, None
    
    # 遍歷目錄中的所有JSON檔案
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            
            try:
                # 根據您的模組結構調整調用方式
                results = lion_process_json_file(file_path)
                
                # 更新ID計數器
                for i, item in enumerate(results):
                    item['id'] = id_counter + i
                
                all_results.extend(results)
                id_counter += len(results)
            
            except Exception as e:
                print(f"處理 {filename} 時發生錯誤: {str(e)}")
    
    # 設定輸出檔案名稱（使用對檔案系統友好的格式）
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")  # 將冒號替換為連字符
    output_filename = f"lion_RawData_{timestamp}.json"
    
    if output_dir:
        # 確保輸出目錄存在
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_path = os.path.join(output_dir, output_filename)
    else:
        output_path = output_filename
    
    # 儲存結果
    if all_results:
        # 根據您的模組結構調整調用方式
        lion_save_to_json(all_results, output_path)
    else:
        print("沒有處理任何資料。")
        return all_results, None
    
    return all_results, output_path