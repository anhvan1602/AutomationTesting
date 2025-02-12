import os
import time
from datetime import datetime

from selenium.webdriver.common.by import By

from Libraries.Framework.Paths import Paths
from Libraries.Framework.Utils import PageBase
from WebApplications.PageCommon import PageCommon, FillData


class PageGuongMat(PageBase):
    def __init__(self, driver):
        super().__init__(driver)
        self.pathDatas = Paths().get_path_datas()

    def do_dien_thong_tin_cong_dan(self, test_data):
        fill_data = FillData(self.driver)
        fill_data.fill_in_each_attribute(test_data)

    def do_bo_sung_them_tt_cong_dan(self, test_data):
        for data in test_data:
            typeof = data.get("TypeOf")
            label = data.get("Label")
            value = data.get("Value")
            if typeof == "Image":
                path_image = os.path.join(self.pathDatas, "c4i2_images", value)
                input_file = f'//div[text()="{label}"]/..//input[@type="file"]'
                self.driver.find_element(By.XPATH, input_file).send_keys(path_image)
            elif typeof == "date-list":
                self.private_fill_birthday(label, value)
            elif typeof == "filladdress":
                self.private_fill_address(label, value)

    def private_fill_birthday(self, label, val):
        val_list = eval(val)  # Chuyển đổi chuỗi thành danh sách
        txt_xpath = (
            f'//div[contains(@class,"form-control-label") and .//div[text()="{label}"]]//div[@class="dropdown-btn-text"]')
        element_xpaths = ['(' + txt_xpath + ')' + f'[{i}]' for i in range(1, 4)]
        for i, xpath in enumerate(element_xpaths):
            element_val = val_list[i]
            self.set_val_input(xpath, element_val)
            frst_item = '(//div[@class="as-dropdown-item-button"])[1]'
            self.click_obj(frst_item)

    def private_fill_address(self, label, val):
        data = val
        for json_str in data:
            data_type_of = json_str['TypeOf']
            data_label = json_str['Label']
            data_value = json_str['Value']
            if data_type_of == "not-fill":
                btncheck = (
                    '//div[contains(@class, "checkbox-form") and .//span[text()="{0}"]]//span[contains(@class, "checkbox-input")]').format(
                    data_value)
                self.click_obj(btncheck)
            elif data_type_of == "input-search":
                btn_popup_search = (
                    '((//div[text()="{0}"])//ancestor::div[contains(@class, "flex-basis-0 items-center")])//button').format(
                    label)
                self.click_obj(btn_popup_search)
                time.sleep(2)

                txt_xpath = '//div[contains(@class,"form-control-label") and .//div[text()="{}"]]//div[@class="dropdown-btn-text"]'.format(
                    data_label)
                if self.get_text_element(txt_xpath) != "":
                    self.set_val_input(txt_xpath, data_value)
                time.sleep(2)
                frst_item = '(//div[@class="as-dropdown-item-button"])[1]'
                self.click_obj(frst_item)
                time.sleep(6)
                bnt_luu_search_addr = '//span[text()="Lưu"]'
                self.click_obj(bnt_luu_search_addr)

    def do_fill_image_face_search(self, value):
        path_image = os.path.join(self.pathDatas, "c4i2_images", value)
        input_file = '//div[contains(@class, "form-group")]//child::input[@type="file"]'
        self.driver.find_element(By.XPATH, input_file).send_keys(path_image)


class PageGuongMatTabPhatHien(PageBase):
    def __init__(self, driver):
        super().__init__(driver)
        self.pathDatas = Paths().get_path_datas()

    def do_verify_accuracy_face(self, attribute, from_value, to_value):
        page_common = PageCommon(self.driver)
        result = page_common.do_get_data_test_in_grid(attribute)
        array_accuracy = range(from_value, to_value)

        invalid_results = []

        for sublist in result:
            for item in sublist:
                value = int(item.rstrip(' %'))
                if from_value <= value <= to_value:
                    # Giá trị nằm trong khoảng lọc
                    continue
                else:
                    invalid_results.append(item)

        if invalid_results:
            print("Invalid results:", invalid_results, " Accuracy:", array_accuracy)
            return False
        else:
            print("Valid results:", result, " Accuracy:", array_accuracy)
            return True

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

    def do_get_data_time_in_grid(self, attribute):
        from datetime import datetime
        page_common = PageCommon(self.driver)
        result_compare = page_common.do_get_data_test_in_grid(attribute)
        date_format = '%d/%m/%Y %H:%M:%S'
        datetime_list = []

        for item in result_compare:
            for value in item:
                try:
                    date_obj = datetime.strptime(value, date_format)
                    datetime_list.append(date_obj)
                except ValueError:
                    pass
        return datetime_list

    def do_verify_time_range_face(self, attribute, from_time, to_time):
        from datetime import datetime
        datetime_list = self.do_get_data_time_in_grid(attribute)
        from_time = datetime.strptime(from_time, '%d/%m/%Y %H:%M')
        to_time = datetime.strptime(to_time, '%d/%m/%Y %H:%M')
        is_valid = True
        for item in datetime_list:
            # # Kiểm tra xem phần tử có nằm trong khoảng thời gian không
            if not (from_time <= item <= to_time):
                is_valid = False
                break
        if is_valid:
            print("Valid results:", datetime_list, " TimeRange:", from_time, "-", to_time)
            return True
        else:
            print("Invalid results:", datetime_list, " TimeRange:", from_time, "-", to_time)
            return False

    def do_verify_time_stamp_face(self, attribute, to_time):
        from datetime import datetime, timedelta
        datetime_list = self.do_get_data_time_in_grid(attribute)

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

        # chuyển chuỗi sang thời gian
        from_time = datetime.strptime(fromtime, '%d/%m/%Y %H:%M:%S')
        to_time = datetime.strptime(totime, '%d/%m/%Y %H:%M:%S')

        # Biến để theo dõi kết quả kiểm tra
        is_valid = True
        for item in datetime_list:
            if not (from_time <= item <= to_time):
                is_valid = False
                break
        if is_valid:
            print("Valid results:", datetime_list, " TimeRange:", from_time, "-", to_time)
            return True
        else:
            print("Invalid results:", datetime_list, " TimeRange:", from_time, "-", to_time)
            return False

    def do_verify_data_cleaned(self, xpath):
        element = self.driver.find_element(By.XPATH, xpath)
        reset_data = element.get_attribute('value')
        if reset_data == '':
            print("Test Passed: Dữ liệu đã nhập bị xóa thành công")
            return True
        else:
            print("Test Failed: Dữ liệu đã nhập không bị xóa")
            return False


class PageGuongMatTabThuVien(PageBase):
    def __init__(self, driver):
        super().__init__(driver)
        self.pathDatas = Paths().get_path_datas()

    def do_verify_result_search_in_popup(self, type_of, label, value):
        if type_of in ["input"]:
            txt_input = f'(//div[.//text()="{label}" and .//input[@value="{value}"]])[last()]'
        elif type_of in ["dropdown-btn-text", "textarea"]:
            txt_input = f'(//div[.//text()="{label}" and .//text()="{value}"])[last()]'
        else:
            txt_input = None
        if txt_input is not None:
            if self.check_element_visibility(txt_input):
                print(f"Tìm thấy '{label}' là '{value}'")
                return True
            else:
                print(f"Không tìm thấy '{label}' là '{value}'")
                return False

    def do_verify_age_search_in_popup(self, label_actual, from_exp, to_exp):
        txt_input = f'//div[contains(text(),"{label_actual}")]//ancestor::div[contains(@class, "form-control")]//child::input'
        find_txt_input = self.driver.find_element(By.XPATH, txt_input)
        value_txt_input = find_txt_input.get_attribute("value")
        if not value_txt_input:
            return False
        else:
            value_txt_input = int(value_txt_input)
            return from_exp <= value_txt_input <= to_exp

    def do_verify_birth_day_in_pop_up(self, label_actual, from_exp, to_exp):
        txt_xpath = f'//div[contains(@class,"form-control-label") and .//div[text()="{label_actual}"]]//div[@class="dropdown-btn-text"]'
        try:
            elements = self.driver.find_elements(By.XPATH, txt_xpath)
            array_birthday = [element.text for element in elements]
            birthday = self.convert_to_date_params(array_birthday)
            start_date = self.convert_number_to_date_param(from_exp)
            end_date = self.convert_number_to_date_param(to_exp)
            check = self.is_birthdate_in_range(birthday, start_date, end_date)
            return check
        except Exception as e:
            print(f"Không tìm thấy element {txt_xpath}", str(e))

    @staticmethod
    def convert_to_date_params(date_array):
        """
        Chuyển đổi mảng ngày sinh thành dạng có thể đưa làm tham số đầu vào.

        Parameters:
        - date_array: Mảng chứa ngày sinh ['Ngày', 'Tháng', 'Năm']

        Returns:
        - Ngày trong định dạng có thể đưa làm tham số đầu vào (dd-mm-yyyy).
        """
        try:
            # Chuyển đổi tháng từ tên sang số
            month_mapping = {'Tháng 1': '01',
                             'Tháng 2': '02',
                             'Tháng 3': '03',
                             'Tháng 4': '04',
                             'Tháng 5': '05',
                             'Tháng 6': '06',
                             'Tháng 7': '07',
                             'Tháng 8': '08',
                             'Tháng 9': '09',
                             'Tháng 10': '10',
                             'Tháng 11': '11',
                             'Tháng 12': '12'}

            day = date_array[0]
            month = month_mapping.get(date_array[1])
            year = date_array[2]

            # Tạo đối tượng datetime và chuyển đổi về định dạng mong muốn
            date_obj = datetime.strptime(f"{day}-{month}-{year}", "%d-%m-%Y")
            formatted_date = date_obj.strftime("%d-%m-%Y")

            return formatted_date
        except (ValueError, TypeError, KeyError) as e:
            print(f"Lỗi chuyển đổi: {e}")
            return None

    @staticmethod
    def convert_number_to_date_param(number):
        """
        Chuyển đổi số thành chuỗi ngày-tháng-năm có thể đưa làm tham số đầu vào.

        Parameters:
        - number: Số cần chuyển đổi (ví dụ: 11012003).

        Returns:
        - Ngày trong định dạng có thể đưa làm tham số đầu vào (dd-mm-yyyy).
        """
        try:
            # Chuyển đổi số thành chuỗi và cắt thành các phần ngày, tháng, năm
            date_str = str(number)
            day = date_str[:2]
            month = date_str[2:4]
            year = date_str[4:]

            # Tạo đối tượng datetime và chuyển đổi về định dạng mong muốn
            date_obj = datetime.strptime(f"{day}-{month}-{year}", "%d-%m-%Y")
            formatted_date = date_obj.strftime("%d-%m-%Y")

            return formatted_date
        except (ValueError, TypeError) as e:
            print(f"Lỗi chuyển đổi: {e}")
            return None

    @staticmethod
    def is_birthdate_in_range(birthdate_str, start_date_str, end_date_str):
        """
        Kiểm tra xem ngày sinh có nằm trong khoảng thời gian không.

        Parameters:
        - birthdate_str: Chuỗi biểu diễn ngày sinh (dd-mm-yyyy)
        - start_date_str: Chuỗi biểu diễn ngày bắt đầu của khoảng thời gian (dd-mm-yyyy)
        - end_date_str: Chuỗi biểu diễn ngày kết thúc của khoảng thời gian (dd-mm-yyyy)

        Returns:
        - True nếu ngày sinh nằm trong khoảng thời gian, False nếu ngược lại.
        """
        try:
            if birthdate_str is not None and start_date_str is not None and end_date_str is not None:
                start_date_dt = datetime.strptime(start_date_str, '%d-%m-%Y')
                end_day_dt = datetime.strptime(end_date_str, '%d-%m-%Y')
                birthday_dt = datetime.strptime(birthdate_str, '%d-%m-%Y')
                return start_date_dt <= birthday_dt <= end_day_dt
            else:
                print("Một hoặc nhiều tham số đầu vào là None.")
                return False
        except ValueError:
            # Xử lý lỗi định dạng nếu ngày sinh, ngày bắt đầu hoặc ngày kết thúc không đúng định dạng
            print("Lỗi định dạng ngày. Hãy sử dụng định dạng dd-mm-yyyy.")
            return False
