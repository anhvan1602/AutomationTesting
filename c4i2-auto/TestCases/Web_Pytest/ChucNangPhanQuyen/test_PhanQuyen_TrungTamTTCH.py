import time
import pytest
import allure

from Libraries.Framework.FactoryDrivers import get_chrome_driver
from Libraries.Framework.Utils import PageBase
from WebApplications.PagePermission import PagePermission
from Libraries.Config import Default
from PageObjects.Web.Obj_Common import ObjCommon
from WebApplications.PageHome import LoginPage
from conftest import capture_screenshot_and_attach_allure
from faker import Faker
import parametrize_from_file as pff
from urllib.parse import urljoin
import pyautogui

fake = Faker()


class ChromeDriverManager:
    """
    A class to manage the initialization of ChromeDriver instances.
    """

    def __init__(self):
        self.window_size = Default.windowSize
        self.screen_width, self.screen_height = map(int, self.window_size.split(","))

    def initialize_split_screen_chrome_drivers(self):
        """
        Initializes two ChromeDriver instances, splitting the screen in half.

        Returns:
            tuple: (driver_chrome_1, driver_chrome_2) - two ChromeDriver instances.
        """
        half_screen_width = self.screen_width // 2
        left_screen_position = (0, 0)
        right_screen_position = (half_screen_width, 0)

        # Initialize ChromeDriver 1 for the left half
        driver_chrome_1 = get_chrome_driver()
        driver_chrome_1.implicitly_wait(Default.timeOut)
        driver_chrome_1.set_window_size(half_screen_width, self.screen_height)
        driver_chrome_1.set_window_position(left_screen_position[0], left_screen_position[1])

        # Initialize ChromeDriver 2 for the right half
        driver_chrome_2 = get_chrome_driver()
        driver_chrome_2.implicitly_wait(Default.timeOut)
        driver_chrome_2.set_window_size(half_screen_width, self.screen_height)
        driver_chrome_2.set_window_position(right_screen_position[0], right_screen_position[1])

        return driver_chrome_1, driver_chrome_2

    @staticmethod
    def initialize_two_chrome_drivers():
        """
        Initializes two ChromeDriver instances with the same implicit wait time.

        Returns:
            tuple: (driver_chrome_1, driver_chrome_2) - two initialized ChromeDriver instances.
        """
        # Initialize ChromeDriver 1
        driver_chrome_1 = get_chrome_driver()
        driver_chrome_1.implicitly_wait(Default.timeOut)

        # Initialize ChromeDriver 2
        driver_chrome_2 = get_chrome_driver()
        driver_chrome_2.implicitly_wait(Default.timeOut)

        return driver_chrome_1, driver_chrome_2

    @staticmethod
    def switch_window():
        if not Default.headlessBrowser:
            pyautogui.hotkey('alt', 'tab')
        else:
            pass


def wait_for_worker():
    """
    The `wait_for_worker` function is designed to support parallel execution in testing environments.
    """
    import os
    worker_id = os.environ.get('PYTEST_XDIST_WORKER', 'gw0')
    if worker_id.startswith('gw'):
        worker_num = int(worker_id[2:])

        if worker_num > 0:
            delay_time = worker_num * 10
            print(f"Worker {worker_id} đang chờ {delay_time} giây...")
            time.sleep(delay_time)


@pytest.fixture(scope='class')
def browser():
    default = Default()
    manager = ChromeDriverManager()

    # Initialize ChromeDrivers based on the split-screen setting
    use_split_screen = getattr(Default, 'useSplitScreen', False)
    if use_split_screen:
        driver_chrome_1, driver_chrome_2 = manager.initialize_split_screen_chrome_drivers()
    else:
        driver_chrome_1, driver_chrome_2 = manager.initialize_two_chrome_drivers()

    # Retrieve login credentials and URL
    url = default.url
    username_per, password_per = default.username_permission, default.password_permission

    username_check_per, password_check_per = default.username_check_permission, default.password_check_permission

    driver_chrome_1.get(url)
    driver_chrome_2.get(url)

    wait_for_worker()

    manager.switch_window()
    time.sleep(1)
    page_login = LoginPage(driver_chrome_1)
    page_login.do_login(username_per, password_per)
    time.sleep(1)

    manager.switch_window()
    time.sleep(1)
    page_login = LoginPage(driver_chrome_2)
    page_login.do_login(username_check_per, password_check_per)
    time.sleep(1)

    yield driver_chrome_1, driver_chrome_2
    driver_chrome_1.quit()
    driver_chrome_2.quit()


@pytest.fixture(scope='class', autouse=True)
def save_current_url(browser):
    driver_1, driver_2 = browser
    current_url_1 = driver_1.current_url
    current_url_2 = driver_2.current_url
    yield current_url_1, current_url_2


is_first_test = True


@pytest.fixture(scope='function', autouse=True)
def setup_url(browser, save_current_url):
    """Sets up url for test cases and transfers it between them."""
    global is_first_test
    current_url_1, current_url_2 = save_current_url
    driver_1, driver_2 = browser
    if not is_first_test and current_url_1 is not None:
        driver_1.get(current_url_1)
    if not is_first_test and current_url_2 is not None:
        driver_2.get(current_url_2)
    is_first_test = False
    yield


pageBase = PageBase(browser)
data_files = pageBase.load_path_data_file_from_path("Datas_Permission", "Test_Permission_TrungTamTTCH.json")

data_files_for_parallel = [
    pageBase.load_path_data_file_from_path("Datas_Permission", "Test_Permission_TrungTamTTCH_1.json"),
    pageBase.load_path_data_file_from_path("Datas_Permission", "Test_Permission_TrungTamTTCH_2.json")
]


@pytest.mark.Permission
class Test_PhanQuyen_TTCH:

    @staticmethod
    def auto_assign_allure_features(feature_string):
        import allure
        parts = feature_string.split('/')

        if len(parts) > 0:
            allure.dynamic.epic(f'{parts[0]}')
        if len(parts) > 1:
            allure.dynamic.feature(f'{parts[1]}')
        if len(parts) > 2:
            remaining_story = '/'.join(parts[2:])
            allure.dynamic.story(f'{remaining_story}')

    @staticmethod
    def validate_and_set_defaults(params):
        """Validates the input parameters and sets default values for missing fields."""
        defaults = {
            'id_tsc': 'default_id',
            'unit': 'QC',
            'role': 'van_member'
        }
        for key, value in defaults.items():
            if key not in params:
                params[key] = value

        required_fields = {
            'id_tsc': str,
            'unit': str,
            'role': str,
            'pre_condition': list,
            'feature': str,
            'status': bool,
            'path_permission': str,
            'steps_to_permission_page': list,
            'path_check_permission': str,
            'expected_signals': list,
        }

        for field, field_type in required_fields.items():
            if field not in params or params[field] is None:
                raise ValueError(f"Tham chiếu {field} của tsc {params['id_tsc']} bị trống.")
            if not isinstance(params[field], field_type):
                raise ValueError(f"Tham chiếu {field} của tsc {params['id_tsc']} phải là kiểu {field_type.__name__}.")

        return params

    @allure.title("Kiểm tra phân quyền")
    @pff.parametrize(path=data_files_for_parallel, schema=validate_and_set_defaults)
    def test_permission_assignment(self, browser, id_tsc, unit, role, feature, status, path_permission,
                                   path_check_permission, steps_to_permission_page, expected_signals, pre_condition):
        self.auto_assign_allure_features(f'{feature}')
        status_text = "ON" if status else "OFF"
        allure.dynamic.title(f"{id_tsc}: {feature} - Trạng thái: {status_text}")
        allure.dynamic.description(
            f"Trường hợp kiểm thử kiểm tra có thể phân quyền: {feature} - trạng thái: {status_text}")
        allure.dynamic.testcase(f"{id_tsc}", f"{id_tsc}")

        driver_chrome_1, driver_chrome_2 = browser

        default = Default()
        manager = ChromeDriverManager()
        url = default.url
        page_base_chrome_1 = PageBase(driver_chrome_1)
        page_base_chrome_2 = PageBase(driver_chrome_2)

        page_permission_chrome_1 = PagePermission(driver_chrome_1)
        page_permission_chrome_2 = PagePermission(driver_chrome_2)

        manager.switch_window()
        time.sleep(1)

        with allure.step("Điều hướng đến trang phân quyền"):
            with allure.step("Get URL permission"):
                url_per = urljoin(url, path_permission)
                driver_chrome_1.get(url_per)
                time.sleep(1)
            with allure.step("Nhấn vào Đơn vị"):
                page_base_chrome_1.show_overlay_text(f"{feature} - {status_text}")
                page_permission_chrome_1.navigate_to_unit(unit)
            with allure.step("Nhấn vào tab Vai trò"):
                page_base_chrome_1.click_obj(ObjCommon.text_span("Vai trò"))
            with allure.step("Nhấn vào button Phân quyền ở cột thao tác"):
                page_base_chrome_1.do_scroll_mouse_to_element(ObjCommon.action_button(role, "fal fa-user"))
                page_base_chrome_1.click_obj(ObjCommon.action_button(role, "fal fa-user"))
        with allure.step("Pre_Condition"):
            if pre_condition:
                for pc in pre_condition:
                    page_permission_chrome_1.action_permission(pc["feature"], pc["status"])
                    capture_screenshot_and_attach_allure(driver_chrome_1, name="win1_perm")
            else:
                allure.attach("Không có điều kiện tiên quyết cho trường hợp này", name="No Pre-condition",
                              attachment_type=allure.attachment_type.TEXT)
        with allure.step("Phân quyền"):
            page_permission_chrome_1.action_permission(feature, status)
            capture_screenshot_and_attach_allure(driver_chrome_1, name="win1_perm")

        types_mapping = {
            'button_text': ObjCommon.button_with_text,
            'button_icon': ObjCommon.button_with_icon,
            'text': ObjCommon.element_text
        }

        manager.switch_window()
        time.sleep(1)

        with allure.step("Điều hướng đến trang kiểm tra phân quyền"):
            with allure.step("Get URL check permission"):
                url_check_per = urljoin(url, path_check_permission)
                driver_chrome_2.get(url_check_per)
            with allure.step("Thao tác đến vị trí phần quyền (optional)"):
                page_base_chrome_2.show_overlay_text(f"Verify - {feature} - {status_text}")
                for step in steps_to_permission_page:
                    step_type = step['type']
                    step_value = step['value']

                    if step_type in types_mapping:
                        element = types_mapping[step_type](step_value)
                        page_permission_chrome_2.click_obj(element)
                        time.sleep(2)
                    else:
                        raise ValueError(f"Step type {step_type} không được hỗ trợ.")
        with allure.step("Kiểm tra phân quyền"):
            for signal in expected_signals:
                signal_action = signal['action']
                signal_type = signal['type']
                signal_value = signal['value']

                if signal_type in types_mapping:
                    xpath = types_mapping[signal_type](signal_value)
                    if signal_action == 'hide':
                        page_permission_chrome_2.verify_permission_with_xpath(status, xpath)
                    elif signal_action == 'disable':
                        page_permission_chrome_2.verify_permission_element_hidden(status, xpath)
                    else:
                        raise ValueError(f"Signal action {signal_action} không được hỗ trợ.")
                else:
                    raise ValueError(f"Signal type {signal_type} không được hỗ trợ.")
            capture_screenshot_and_attach_allure(driver_chrome_1, name="win1_perm")
            capture_screenshot_and_attach_allure(driver_chrome_2, name="win2_perm")
