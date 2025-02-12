import os
import time
import calendar
from datetime import datetime, timedelta

import pytest
from selenium.common import NoSuchElementException
from Libraries.Config import Default
from Libraries.Framework.Paths import Paths
from Libraries.Framework.Utils import PageBase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class FillData(PageBase):
    def __init__(self, driver):
        super().__init__(driver)
        self.pathDatas = Paths().get_path_datas()
        self.pageCommon = PageCommon(driver)
        self.attributeColumns = ['TypeOf', 'Label', 'Value', 'ExpectVerify']

    def fill_in_each_attribute(self, test_data):
        _actions = {
            "input": self._fill_input,
            "input-popup": self._fill_input_popup,
            "dropdown-btn-text": self._select_dropdown_option,
            "textarea": self._fill_textarea,
            "input-search": self._fill_input_search,
            "switchToggle": self._toggle_switch,
            "checkbox": self._toggle_checkbox,
            "datetime": self._select_date_time,
            "input-datetime": self._fill_date_time
        }

        for data in test_data:
            type_of = data.get("TypeOf")
            label = data.get("Label")
            val = data.get("Value")

            if type_of in _actions:
                _actions[type_of](label, val)

    # fillInEachAttribute_Actions
    def _fill_input(self, label, val):
        txt_input = '//div[contains(@class,"popup")]//div[contains(@class,"form-control-label") and .//div[text()="{0}"]]//input'.format(
            label)
        self.send_key_input(txt_input, val)

    def _fill_input_popup(self, label, val):
        txt_input = (
            '(//div[contains(@class,"popup-container")]//div[contains(@class,"form-control-label") and .//div[text()="{0}"]]//input)[1]').format(
            label)

        self.send_key_input(txt_input, val)

    def _select_dropdown_option(self, label, val):
        txt_xpath = f'(//div[contains(@class,"form-control-label") and .//div[text()="{label}"]]//div[@class="dropdown-btn-text"])[last()]'
        self.select_key_dropdown(txt_xpath, val)

    def _fill_textarea(self, label, val):
        txt_input = '//div[contains(@class,"form-control-label") and .//div[text()="{}"]]//textarea'.format(label)
        self.send_key_input(txt_input, val)

    def _fill_input_search(self, label, val):
        txt_xpath = '(//div[contains(@class,"form-control-label") and .//div[text()="{}"]]//div[@class="dropdown-btn-text"])[last()]'.format(
            label)
        self.set_val_input(txt_xpath, val)
        time.sleep(1)
        txt_val_select = f'//div[@class="as-dropdown-item-button" and text()="{val}"]'
        self.click_obj(txt_val_select)
        time.sleep(1)

    def _toggle_switch(self, label, val):
        btn_switch_toggle = '//div[contains(@class,"form-control-label") and .//div[text()="{}"]]//div[contains(@class,"switch-toogle")]'.format(
            label)
        class_value = self.driver.find_element(By.XPATH, btn_switch_toggle).get_attribute("class")
        flag_toggle = False
        time.sleep(1)
        if "active" in class_value:
            flag_toggle = True
        if (val == "True" and not flag_toggle) or (val == "False" and flag_toggle):
            self.click_obj(btn_switch_toggle)

    def _toggle_checkbox(self, label, val):
        btn_checkbox = '//div[contains(@class,"form-control-label") and .//div[text()="{}"]]//span[contains(@class,"checkbox-input")]'.format(
            label)
        class_value = self.driver.find_element(By.XPATH, btn_checkbox).get_attribute("class")
        flag_toggle = False
        time.sleep(1)
        if "checked" in class_value:
            flag_toggle = True
        if (val == "True" and not flag_toggle) or (val == "False" and flag_toggle):
            self.click_obj(btn_checkbox)

    def _select_date_time(self, label, val):
        btn_calendar = '//div[contains(@class,"form-control-label") and .//div[text()="{0}"]]//*[@class="fal fa-calendar-alt  "]'.format(
            label)
        self.click_obj(btn_calendar)
        self.pageCommon.choose_date(val)

    def _fill_date_time(self, label, val):
        btn_calendar = '//div[contains(@class,"form-control-label") and .//div[text()="{0}"]]//*[@class="fal fa-calendar-alt  "]'.format(
            label)
        self.click_obj(btn_calendar)
        actions = ActionChains(self.driver)
        input_date_time = '//div[contains(@class,"form-control-label") and .//div[text()="{0}"]]//child::input'.format(
            label)
        self.send_key_input(input_date_time, val)
        actions.send_keys(Keys.ENTER)
        actions.perform()

    # END-fillInEachAttribute_Actions

    # verifyAttributesOnForm_Actions
    def _verify_input(self, label, val, xpath_submit):
        txt_input = '//div[contains(@class,"popup")]//div[contains(@class,"form-control-label") and .//div[text()="{0}"]]//input'.format(
            label)
        self.send_key_input(txt_input, val)
        self.click_obj(xpath_submit)

        return self._check_invalid_error(label)

    def _verify_dropdown_option(self, label, val, xpath_submit):
        # 1. clean trị nếu có
        xpath_clear = f'//div[contains(@id, "case-form-popup")]//div[text()="{label}"]/../..//div[contains(@class,"clear")]'
        elements = self.driver.find_elements(By.XPATH, xpath_clear)
        if elements:
            elements[0].click()

        # 2. Nếu val có thì chọn
        if val != "":
            self._select_dropdown_option(label, val)

        # 3. Bấm Submit để xem hợp lệ không
        self.click_obj(xpath_submit)

        return self._check_invalid_error(label)

    # END-verifyAttributesOnForm_Actions
    def _check_invalid_error(self, label):
        time.sleep(0.5)
        div_error = f'//div[contains(@id, "case-form-popup")]//div[text()="{label}"]/../..//div[contains(@class,"invalid-error")]'
        elements = self.driver.find_elements(By.XPATH, div_error)
        res = False
        if elements:
            res = True
        return res


class PageCommon(PageBase):
    def __init__(self, driver):
        super().__init__(driver)
        self.pathDatas = Paths().get_path_datas()

    #######################################
    @staticmethod
    def get_current_and_past_time(interval, unit='seconds'):
        """
        :param interval: The amount of time to go back from the current time.
        :param unit: The unit of the interval (default is 'seconds')
        :return: A tuple containing the current time and the pastime
        """
        units = {
            'seconds': 1,
            'minutes': 60,
            'hours': 3600,
            'days': 86400
        }
        if unit not in units:
            raise ValueError("Invalid unit. Please choose one of 'seconds', 'minutes', 'hours', 'days'.")

        seconds_in_interval = interval * units[unit]
        current_time = datetime.now()
        past_time = current_time - timedelta(seconds=seconds_in_interval)
        return current_time, past_time

    def get_data_from_grid(self, xpath_expression):
        """
        :param xpath_expression: The XPath expression to locate the grid or table elements.
        :return: A list containing the text content of the located elements.
        """
        element_list = self.driver.find_elements(By.XPATH, xpath_expression)
        # Trích xuất văn bản từ danh sách các phần tử và đưa vào mảng
        text_list = [element.text for element in element_list]
        # Lọc ra các phần tử không trống
        filtered_data = [item for item in text_list if item]
        result = []
        for item in filtered_data:
            parts = item.split('\n')
            result.append(parts)
        assert len(result) != 0, "Không tìm thấy dữ liệu !"
        # Loại bỏ phần tử cuối cùng
        if len(result) > 3:
            result = result[:-1]
        return result

    def do_get_data_test_on_grid_in_pop_up(self, attribute):
        """
        :param attribute: The attribute or identifier used to locate the element.
        :return: A list containing the retrieved data from the grid
        """
        xpath = f'//div[contains(@class, "popup")]//child::div[contains(@class, "dg-row") and @cellid="{attribute}"]'
        result = self.get_data_from_grid(xpath)
        return result

    def do_get_data_test_in_grid(self, attribute):
        """
        :param attribute: The attribute or identifier used to locate the element.
        :return: A list containing the retrieved data from the grid
        """
        xpath = f'//div[contains(@class, "dg-row") and @cellid="{attribute}"]'
        result = self.get_data_from_grid(xpath)
        return result

    @staticmethod
    def do_verify_results_in_grid(list_value_actual, value_exp, index=None):
        """
        :param list_value_actual:A list containing actual values from the grid or list to verify
        :param value_exp: The expected value to verify against the actual values.
        :param index: Optional index to specify a specific position in the list (default: None).
        :return: True if `value_exp` matches any actual value in `list_value_actual`, otherwise False.
        """
        if index is not None:
            result_compare = [item[index] for item in list_value_actual if len(item) > index]
            for item in result_compare:
                if item != value_exp:
                    return False, item
            print(f"All results in the grid list are valid - {result_compare}")
            return True, None
        else:
            for item in list_value_actual:
                if value_exp not in item:
                    return False, item
            print(f"All results in the grid list are valid - {list_value_actual}")
            return True, None

    def is_valid_tim_range(self, result_compare, from_time, to_time):
        """
        :param result_compare: Time value to be compared against the time range.
        :param from_time: The start time of the time range
        :param to_time: The end time of the time range
        :return: True if `result_compare` falls within the time range [from_time, to_time], False otherwise.
        """
        if not isinstance(result_compare, list):
            result_compare = [result_compare]  # Chuyển đổi thành danh sách nếu chỉ là một giá trị đơn
        invalid_results = []
        result_compare_last = []

        # Kiểm tra và lọc lại danh sách các giá trị hợp lệ
        for item in result_compare:
            try:
                date_object = self.format_datetime(item)
                result_compare_last.append(date_object)
            except ValueError:
                continue
        if not result_compare_last:
            assert False, "Giá trị đầu vào không hợp lệ hoặc rỗng"

        from_time = datetime.strptime(from_time, '%d/%m/%Y %H:%M')
        to_time = datetime.strptime(to_time, '%d/%m/%Y %H:%M')
        for item in result_compare_last:
            item = datetime.strptime(item, '%d/%m/%Y %H:%M')
            if from_time <= item <= to_time:
                # Giá trị nằm trong khoảng lọc
                continue
            else:
                invalid_results.append(item)

        if invalid_results:
            print("Invalid results:", invalid_results, " TimeRange:", from_time, "-", to_time)
            return False
        else:
            print("Valid results:", result_compare_last, " TimeRange:", from_time, "-", to_time)
            return True

    def format_datetime(self, dt, fmt=None):
        """
        :param dt: The datetime object or string representation to format.
        :param fmt: Optional format string, if fmt=None then fmt = "%d/%m/%Y %H:%M"
        :return: Formatted datetime string according to the specified format.
        """
        # Xử lý trường hợp tham số truyền vào là một danh sách
        if isinstance(dt, list):
            return [self.format_datetime(item, fmt) for item in dt]

            # Xử lý trường hợp tham số truyền vào là giá trị đơn
        if isinstance(dt, str):
            # Chuyển đổi từ định dạng có giây sang định dạng không có giây
            if dt.count(':') == 2:
                dt = datetime.strptime(dt, "%d/%m/%Y %H:%M:%S")
                dt = dt.replace(second=0)
            else:
                dt = datetime.strptime(dt, "%d/%m/%Y %H:%M")

        if fmt is None:
            fmt = "%d/%m/%Y %H:%M"

        return dt.strftime(fmt)

    def get_path_file_in_datas(self, file):
        """
        :param file: The name of the file
        :return: Path of the file
        """
        return os.path.join(self.pathDatas, file)

        ###############################

    def choose_date(self, data_value):
        """
        :param data_value: value datetime
        :return: action choose datetime
        """
        page_base = PageBase(self.driver)

        value_day = data_value.day
        value_month = data_value.month
        value_year = data_value.year

        value_month_english = f"tháng{str(value_month)}"
        if Default.defaultLanguage == 'English':
            value_month_english = calendar.month_name[value_month]

        # Chọn năm/ Hiện tại chỉ được chọn năm trong khoảng 2016 - 2030
        page_base.click_obj(f"//*[@class='current-date']//button[2]")
        page_base.click_obj(f"//div[contains(text(),'{value_year}')]")
        # Chọn tháng
        page_base.click_obj(f"//*[@class='current-date']//button[1]")
        page_base.click_obj(f"//div[contains(text(),'{value_month_english}')]")
        # Chọn ngày
        page_base.click_obj(
            f"//td[not(contains(@class, 'next-month')) and not(contains(@class, 'prev-month'))]/div[text()='{value_day}']")
        time.sleep(2)

    def verify_notify_popup(self, txt_message_check_exit):
        """
        :param txt_message_check_exit: The text message expected to appear in the notification popup.
        :return: True if the notification popup with the specified message is found, False otherwise.
        """
        try:
            get_text_popup = ''  # Khởi tạo giá trị mặc định
            for _ in range(10):
                time.sleep(0.5)
                elements = self.driver.find_elements(By.XPATH, '//div[@class="toast-message css-0"]')
                if elements:
                    last_element = elements[-1]
                    get_text_popup = last_element.text
                    if get_text_popup != '':
                        break

            if txt_message_check_exit not in get_text_popup:
                return f"Thông báo: {get_text_popup} != {txt_message_check_exit}"

            return txt_message_check_exit in get_text_popup

        except NoSuchElementException:
            return False

    def verify_notify_error(self, txt_message_check_exit):
        """
        :param txt_message_check_exit: The text message expected to appear in the notification popup.
        :return:  True if the notification error with the specified message is found, False otherwise.
        """
        from selenium.webdriver.support.wait import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common import TimeoutException
        mess = txt_message_check_exit
        delay = 10
        txt_xpath = '//div[@class="toast-message css-0" and not(span[@class="tb tb1"])]'
        get_text_popup = ""
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, txt_xpath)))
            elements = self.driver.find_elements(By.XPATH, '//div[@class="toast-message css-0"]')
            for element in elements:
                get_text_popup = element.text
            if mess in get_text_popup:
                return True
        except TimeoutException:
            return False

    def verify_notify_field_required(self, txt_message_check_exit):
        """
        :param txt_message_check_exit: The text message expected to appear for the required field notification.
        :return: True if the required field notification with the specified message is found, False otherwise.
        """
        time.sleep(0.5)
        div_error = f'//span[contains(text(), "{txt_message_check_exit}")]'
        elements = self.driver.find_elements(By.XPATH, div_error)
        res = False
        if elements:
            res = True
        return res

    def verify_result_created(self, test_data):
        """
        :param test_data: The test data used to verify the creation of the result.
        :return: True if the result creation is verified successfully, False otherwise.
        """
        t = 0
        for data in test_data:
            type_of = data.get("TypeOf")
            label = data.get("Label")
            value = data.get("Value")
            if type_of in ["input"]:
                txt_input = f'(//div[.//text()="{label}" and .//input[@value="{value}"]])[last()]'
            elif type_of in ["dropdown-btn-text", "textarea", "input-datetime"]:
                txt_input = f'(//div[.//text()="{label}" and .//text()="{value}"])[last()]'
            else:
                txt_input = None
            if txt_input is not None:
                self.do_scroll_mouse_to_element(txt_input)
                time.sleep(1)
                if self.check_element_visibility(txt_input):
                    print(f"Tìm thấy '{label}' là '{value}'")
                else:
                    print(f"Không tìm thấy '{label}' là '{value}'")
                    t += 1
        if t == 0:
            return True
        else:
            return False
