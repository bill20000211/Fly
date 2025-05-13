from Utils.RawToJson import CrawlertoRawData_kkday, CrawlertoRawData_lion
from Utils.ProductCrawler import crawler_kkday, crawler_lion
from model.rawdata_dao import RawData_dao
from model.member_dao import Member_dao


class crawler_service():
    def process_data(p_from, p_to, p_type, p_module):
        # 執行爬蟲
        if p_module == 'crawler' or p_module == 'all':
            try:
                if p_type == 'kkday' or p_type == 'all':
                    kkday_data, kkday_file = crawler_kkday(
                        "計劃機票", p_from)  # 爬取 KKday 資料並輸出到指定目錄
                if p_type == 'lion' or p_type == 'all':
                    lion_data, lion_file = crawler_lion(
                        "超值特惠機票", p_from)  # 爬取 KKday 資料並輸出到指定目錄

            except Exception as e:
                print(f"An error occurred while crawling data: {e}")
                return None
        # 爬蟲資料 --> DB資料
        if p_module == 'rawdata' or p_module == 'all':
            try:
                if p_type == 'kkday' or p_type == 'all':
                    datas, file = CrawlertoRawData_kkday(
                        p_from, p_to)  # 處理KKDay資料並輸出到指定目錄
                if p_type == 'lion' or p_type == 'all':
                    datas, file = CrawlertoRawData_lion(
                        p_from, p_to)  # 處理KKDay資料並輸出到指定目錄

            except Exception as e:
                print(f"An error occurred while processing data: {e}")
                return None

            # 資料的檢查
            if datas:
                count = 0
                for data in datas:
                    data_exsit = RawData_dao.check_data_exsit(data)
                    if data_exsit[0] > 0:  # 有大於一筆相同的data --> 不搬進來
                        continue

                    else:  # 沒有的話 --> 要看條件搬進來
                        key_data_exsit = RawData_dao.check_key_data_exsit(data)

                        if key_data_exsit[0] > 0:  # 該鍵值在DB有資料 --> 可能是同筆資料有異動 or 真的新資料
                            # 全進全出，這筆進來之後，會先by key值刪掉之前的
                            RawData_dao.delete_data_by_key(data)

                            # TODO # 產品Table的資料也要delete掉

                        if p_type == 'kkday':  # 搬資料進來
                            RawData_dao.create_rawdata_kkday(data)
                        elif p_type == 'lion':
                            RawData_dao.create_rawdata_lion(data)

                        count = count + 1
                '''
                搬進DB之後的data，會先壓上import
                因為再檢查DB是否有重複資料的時候，會限制他只檢查被壓上ready的資料
                不然他會在這次的執行中，一直刪掉相同prod_oid, pkg_oid的資料
                '''
                if p_type == 'kkday':
                    v_input_data = {'supplier': 'KKDAY'}
                    RawData_dao.raw_import_to_ready(
                        v_input_data)  # 把DB的資料壓成ready
                elif p_type == 'lion':
                    v_input_data = {'supplier': 'LionTravel'}
                    RawData_dao.raw_import_to_ready(
                        v_input_data)  # 把DB的資料壓成ready

                print(f'{type} : 輸入 {count} 資料')
            else:
                print(f'{type} 無資料')
        return datas

    # def process_kkday_data(kkday_from, kkday_to):
    #     try:
    #         key_word = '計劃機票'
    #         # 爬取 KKday 資料並輸出到指定目錄 by Walt
    #         kkday_data, kkday_file = crawler_kkday(key_word, kkday_from)
    #     except Exception as e:
    #         print(f"An error occurred while crawling KKday data: {e}")
    #         return None

    #     try:
    #         # 處理KKDay資料並輸出到指定目錄 by Walt
    #         kkday_datas, kkday_file = CrawlertoRawData_kkday(kkday_from, kkday_to)
    #     except Exception as e:
    #         print(f"An error occurred while processing KKday data: {e}")
    #         return None

    #     if kkday_datas:
    #         count = 0
    #         for kkday_data in kkday_datas:
    #             data_exsit = RawData_dao.check_data_exsit(kkday_data)
    #             # 有大於一筆相同的data --> 不搬進來
    #             if data_exsit[0] > 0:
    #                 continue
    #             # 沒有的話 --> 要看條件搬進來
    #             else:
    #                 key_data_exsit = RawData_dao.check_key_data_exsit(kkday_data)
    #                 # 該鍵值在DB有資料 --> 可能是同筆資料有異動 or 真的新資料
    #                 if key_data_exsit[0] > 0:
    #                     # 全進全出，這筆進來之後，會先by key值刪掉之前的
    #                     RawData_dao.delete_data_by_key(kkday_data)
    #                     # 產品Table的資料也要delete掉
    #                     # TODO
    #                 # 然後搬一份進來
    #                 RawData_dao.create_rawdata_kkday(kkday_data)
    #                 count = count + 1
    #         input_data = {
    #             'supplier': 'KKDAY'
    #         }
    #         RawData_dao.raw_import_to_ready(input_data)

    #         print(f'KKday : 輸入 {count} 資料')
    #     else:
    #         print(f'KKday 無資料')
    #     return kkday_datas

    # def process_lion_data(lion_from, lion_to):
    #     try:
    #         key_word = '超值特惠機票'
    #         # 爬取 KKday 資料並輸出到指定目錄
    #        # kkday_data, kkday_file = crawler_lion(key_word, lion_from)
    #     except Exception as e:
    #         print(f"An error occurred while crawling Lion data: {e}")
    #         return None

    #     try:
    #         # 處理KKDay資料並輸出到指定目錄
    #         lion_datas, lion_file = CrawlertoRawData_lion(lion_from, lion_to)
    #     except Exception as e:
    #         print(f"An error occurred while processing Lion data: {e}")
    #         return None

    #     if lion_datas:
    #         count = 0
    #         for lion_data in lion_datas:
    #             data_exsit = RawData_dao.check_data_exsit(lion_data)
    #             # 有大於一筆相同的data --> 不搬進來
    #             if data_exsit[0] > 0:
    #                 continue
    #             # 沒有的話 --> 要看條件搬進來
    #             else:
    #                 key_data_exsit = RawData_dao.check_key_data_exsit(lion_data)
    #                 # 該鍵值在DB有資料 --> 可能是同筆資料有異動 or 真的新資料
    #                 if key_data_exsit[0] > 0:
    #                     # 全進全出，這筆進來之後，會先by key值刪掉之前的
    #                     RawData_dao.delete_data_by_key(lion_data)
    #                     # 產品Table的資料也要delete掉
    #                     # TODO
    #                 # 然後搬一份進來
    #                 RawData_dao.create_rawdata_lion(lion_data)
    #                 count = count + 1
    #         input_data = {
    #             'supplier': 'LionTravel'
    #         }
    #         RawData_dao.raw_import_to_ready(input_data)

    #         print(f'Lion : 輸入 {count} 資料')
    #     else:
    #         print(f'Lion 無資料')
    #     return lion_datas
