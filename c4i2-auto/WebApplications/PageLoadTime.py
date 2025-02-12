import allure
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Libraries.Framework.Utils import PageBase
from PageObjects.Web.Obj_Common import ObjCommon
from conftest import capture_screenshot_and_attach_allure


class PageLoadTime(PageBase):
    def __init__(self, driver):
        super().__init__(driver)

    def report_remaining_loading_elements(self, loading_locator):
        """
        Kiểm tra và báo cáo các phần tử còn trong trạng thái 'loading' khi hết thời gian chờ.

        :param loading_locator: Định vị của phần tử "loading" (By.CSS_SELECTOR, ".loading" hoặc tương tự)
        """
        remaining_loading_elements = self.driver.find_elements(*loading_locator)

        loading_info = ""
        for idx, element in enumerate(remaining_loading_elements):
            loading_info += f"Element {idx + 1}: Location - {element.location}, Size - {element.size}, HTML - {element.get_attribute('outerHTML')}\n"

        allure.attach(
            loading_info,
            name="Remaining Loading Elements",
            attachment_type=allure.attachment_type.TEXT
        )

        capture_screenshot_and_attach_allure(self.driver, "Timeout Screenshot")

    def measure_page_load_time(self, time_out):
        """
        Đo thời gian tải trang và báo cáo thời gian tải hoặc lỗi.

        :param time_out: Thời gian chờ tối đa
        :return: Thời gian tải trang
        """
        loading_locator = (By.XPATH, "//*[contains(@class, 'loading')]")
        self.driver.implicitly_wait(0)
        try:
            WebDriverWait(self.driver, time_out).until(
                EC.invisibility_of_element_located(loading_locator)
            )
            return True
        except TimeoutException:
            self.report_remaining_loading_elements(loading_locator)
            return False
        finally:
            self.driver.implicitly_wait(time_out)

    def verify_signals_visibility(self, expected_signals, default_time_out):
        """
        Kiểm tra tính khả dụng của các phần tử quan trọng dựa trên các tín hiệu.

        :param expected_signals: Danh sách các tín hiệu cần kiểm tra
        :param default_time_out: Thời gian chờ tối đa
        """
        types_mapping = {
            'button_text': ObjCommon.button_with_text,
            'button_icon': ObjCommon.button_with_icon,
            'text': ObjCommon.element_text
        }

        for signal in expected_signals:
            signal_type = signal['type']
            signal_value = signal['value']

            if signal_type in types_mapping:
                xpath = types_mapping[signal_type](signal_value)
                verify = self.check_element_visibility(xpath, wait_time=default_time_out)
                return verify

    def setup_steps_before_check(self, steps):
        """
            Prepares and executes a series of steps before performing location checks.

            Parameters:
            - steps (list): A list of dictionaries, each representing an action step with keys:
                - 'action' (str): Type of action to perform, e.g., 'send_key' or 'click'.
                - 'type' (str): Element type identifier, such as 'button_text', 'button_icon', 'text', or 'text_box'.
                - 'label' (str): Label or identifier for the target element.
                - 'value' (str, optional): Input value for actions like 'send_key'.
            """

        types_mapping = {
            'button_text': ObjCommon.button_with_text,
            'button_icon': ObjCommon.button_with_icon,
            'text': ObjCommon.element_text,
            'text_box': ObjCommon.input_search,
            'dropdown_list': ObjCommon.dropdown_list
        }

        for step in steps:
            step_action = step['action']
            step_type = step['type']
            step_label = step['label']
            step_value = step.get('value', "")

            if step_type not in types_mapping:
                raise ValueError(f"Step type '{step_type}' is not supported.")

            xpath_element = types_mapping[step_type](step_label)

            if step_action == "send_key":
                self.send_key_input(xpath_element, step_value)
            elif step_action == "click":
                self.click_obj(xpath_element)
            elif step_action == "select":
                self.select_key_dropdown(xpath_element, step_value)
            else:
                raise ValueError(f"Step action '{step_action}' is not supported.")
