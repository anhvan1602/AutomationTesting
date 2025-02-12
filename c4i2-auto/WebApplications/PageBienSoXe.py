import os

from selenium.webdriver.common.by import By

from WebApplications.PageCommon import FillData

from Libraries.Framework.Paths import Paths
from Libraries.Framework.Utils import PageBase
from WebApplications.PageCommon import PageCommon


class PageBienSoXe(PageBase):
    def __init__(self, driver):
        super().__init__(driver)
        self.pathDatas = Paths().get_path_datas()

    def do_dien_thong_tin_bsx(self, test_data):
        fill_data = FillData(self.driver)
        fill_data.fill_in_each_attribute(test_data)


class PageBienSoXeTabPhatHien(PageBase):
    def __init__(self, driver):
        super().__init__(driver)
        self.pathDatas = Paths().get_path_datas()

    def do_fill_image_bsx(self, path_file_upload):
        try:
            path_image = os.path.join(self.pathDatas, "c4i2_images", path_file_upload)
            input_file = (
                '//div[text()="{0}"]//ancestor::div[contains(@class, "form-control")]//child::input[@type="file"]').format(
                "Biển số")
            return self.driver.find_element(By.XPATH, input_file).send_keys(path_image)
        except Exception as e:
            print("Đã xảy ra lỗi trong quá trình upload ảnh:", str(e))

    def do_check_fill_bsx_from_image(self, value_exp):
        xpath_expression = '//span[contains(@class, "tag-container")]'
        element_list = self.driver.find_elements(By.XPATH, xpath_expression)
        # Trích xuất văn bản từ danh sách các phần tử và đưa vào mảng
        text_list = [element.text for element in element_list]
        if value_exp in text_list:
            return True
        else:
            return False

    def do_move_slider(self, from_value, to_value):
        from selenium.webdriver.common.action_chains import ActionChains
        action = ActionChains(self.driver)
        # Định vị các phần tử bằng XPath
        xpath_from = '//div[@class="slider__range-thumb"][1]'
        xpath_to = '//div[@class="slider__range-thumb"][2]'
        start_taget = '//div[@class="slider-mark"][1]'
        end_taget = '//div[@class="slider-mark"][4]'

        # Định vị các phần tử bằng find_element
        from_handle = self.driver.find_element(By.XPATH, xpath_from)
        to_handle = self.driver.find_element(By.XPATH, xpath_to)
        start_handle = self.driver.find_element(By.XPATH, start_taget)
        end_handle = self.driver.find_element(By.XPATH, end_taget)

        action.click_and_hold(from_handle).move_to_element(start_handle).perform()
        action.reset_actions()

        action.click_and_hold(to_handle).move_to_element(end_handle).perform()
        action.reset_actions()
        # Sử dụng ActionChains để kéo thanh trượt từ 0% đến 100%
        set_fromvalue = from_value * 2.38
        action.click_and_hold(from_handle).move_by_offset(set_fromvalue, 0).perform()
        action.reset_actions()
        set_tovalue = (100 - to_value) * 2.38
        action.click_and_hold(to_handle).move_by_offset(-int(set_tovalue), 0).perform()
        action.reset_actions()

    def do_verify_accuracy_bsx(self, attribute, from_value, to_value):
        page_common = PageCommon(self.driver)
        result = page_common.do_get_data_test_in_grid(attribute)
        results_accuracy_in_grid = [item[0] for item in result]
        # results_accuracy_in_grid = [item['Value'] for item in result if 'Value' in item]
        array_accuracy = range(from_value, to_value)

        invalid_results = []

        for item in results_accuracy_in_grid:
            value = int(item.rstrip('%'))
            if from_value <= value <= to_value:
                # Giá trị nằm trong khoảng lọc
                continue
            else:
                invalid_results.append(item)

        if invalid_results:
            print("Invalid results:", invalid_results, " Accuracy:", array_accuracy)
            return False
        else:
            print("Valid results:", results_accuracy_in_grid, " Accuracy:", array_accuracy)
            return True

    def do_verify_time_range_bsx(self, attribute, from_time, to_time, value_actual):
        page_common = PageCommon(self.driver)
        result = page_common.do_get_data_test_in_grid(attribute)
        result_compare = [item[value_actual] for item in result if len(item) > value_actual]
        page_common = PageCommon(self.driver)
        from_time = page_common.format_datetime(from_time)
        to_time = page_common.format_datetime(to_time)
        result_compare = page_common.format_datetime(result_compare)
        verify = page_common.is_valid_tim_range(result_compare, from_time, to_time)

        return verify

    def do_verify_time_stamp_bsx(self, attribute, to_time, value_actual):
        from datetime import datetime, timedelta
        page_common = PageCommon(self.driver)
        result = page_common.do_get_data_test_in_grid(attribute)
        result_compare = [item[value_actual] for item in result if len(item) > value_actual]

        current_time = datetime.now()
        totime = current_time.strftime('%d/%m/%Y %H:%M:%S')

        # Xác định khoảng thời gian bạn muốn trừ khỏi thời gian hiện tại
        if to_time == '6 giờ':
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
        fromtime = (current_time - delta).strftime('%d/%m/%Y %H:%M:%S')

        page_common = PageCommon(self.driver)
        from_time = page_common.format_datetime(fromtime)
        to_time = page_common.format_datetime(totime)
        result_compare = page_common.format_datetime(result_compare)
        verify = page_common.is_valid_tim_range(result_compare, from_time, to_time)

        return verify

    def do_verify_data_cleaned(self, xpath):
        element = self.driver.find_element(By.XPATH, xpath)
        reset_data = element.get_attribute('value')
        if reset_data == '':
            print("Test Passed: Dữ liệu đã nhập bị xóa thành công")
            return True
        else:
            print("Test Failed: Dữ liệu đã nhập không bị xóa")
            return False
