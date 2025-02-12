from Libraries.Framework.Paths import Paths
from Libraries.Framework.Utils import PageBase
from WebApplications.PageCommon import PageCommon


class PageSuKien(PageBase):
    def __init__(self, driver):
        super().__init__(driver)
        self.pathDatas = Paths().get_path_datas()

    def do_verify_time_stamp_bsx(self, list_value_actual, to_time, index=None):
        from datetime import datetime, timedelta
        page_common = PageCommon(self.driver)

        result = list_value_actual
        if index is not None:
            result_compare = [item[index] for item in list_value_actual if len(item) > index]
        else:
            result_compare = result
        if not result:
            print("Không có dữ liệu để kiểm tra.")
            return False

        current_time = datetime.now()
        totime = current_time.strftime('%d/%m/%Y %H:%M')

        # Xác định khoảng thời gian bạn muốn trừ khỏi thời gian hiện tại
        if to_time == '1 giờ':
            delta = timedelta(hours=1)
        elif to_time == '6 giờ':
            delta = timedelta(hours=6)
        elif to_time == '12 giờ':
            delta = timedelta(hours=12)
        elif to_time == '1 ngày':
            delta = timedelta(days=1)
        elif to_time == '7 ngày':
            delta = timedelta(days=7)
        elif to_time == '30 ngày':
            delta = timedelta(days=30)
        else:
            print("Khoảng thời gian không hợp lệ")
            return False
        fromtime = (current_time - delta).strftime('%d/%m/%Y %H:%M')

        results = page_common.is_valid_tim_range(result_compare, fromtime, totime)
        return bool(results)

    def do_verify_time_range_event(self, attribute, from_time, to_time, value_actual=None):
        page_common = PageCommon(self.driver)
        result_compare = page_common.do_get_data_test_in_grid(attribute)
        if value_actual is None:
            value_actual = 0
        result_compare = [item[value_actual] for item in result_compare if len(item) > value_actual]
        page_common = PageCommon(self.driver)
        from_time = page_common.format_datetime(from_time)
        to_time = page_common.format_datetime(to_time)
        result_compare = page_common.format_datetime(result_compare)
        verify = page_common.is_valid_tim_range(result_compare, from_time, to_time)

        return verify
