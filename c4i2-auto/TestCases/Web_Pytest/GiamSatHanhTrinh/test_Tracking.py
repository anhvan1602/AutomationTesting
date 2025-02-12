import time
import pytest
import allure

from Libraries.Framework.FactoryDrivers import get_chrome_driver
from Libraries.Framework.Utils import PageBase
from Libraries.Config import Default
from PageObjects.Web.Obj_Tracking import Obj_Tracking, ObjTrackingFuntion
from WebApplications.PageHome import LoginPage
from allure_commons.types import AttachmentType
from conftest import capture_screenshot_and_attach_allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import parametrize_from_file as pff


@pytest.fixture(scope='class')
def browser():
    driver = get_chrome_driver()
    driver.implicitly_wait(Default.timeOut)
    # driver.maximize_window()

    default_tenant = Default()

    url = default_tenant.url
    username = default_tenant.username
    password = default_tenant.password

    page_login = LoginPage(driver)
    driver.get(url)
    page_login.do_login(username, password)
    page_login.click_obj(Obj_Tracking.iconGiamSatHanhTrinh)
    time.sleep(1)

    yield driver
    driver.quit()


@pytest.fixture(scope='class', autouse=True)
def save_current_url(browser):
    driver = browser
    current_url = driver.current_url
    yield current_url


is_first_test = True


@pytest.fixture(scope='function', autouse=True)
def setup_url(browser, save_current_url):
    global is_first_test
    # Nếu không phải là test đầu tiên, thực hiện setup_url
    if not is_first_test and save_current_url is not None:
        driver = browser
        driver.get(save_current_url)
    # Đánh dấu biến cờ là False sau khi đã thực hiện setup_url lần đầu tiên
    is_first_test = False
    yield


@pytest.mark.Tracking
class Test_Tracking:
    pageBase = PageBase(browser)
    pathDataTestTracking = pageBase.load_path_data_file_from_path("Datas_Tracking",
                                                             "Test_Tracking.json")

    statuses = ["Xe đang di chuyển", "Xe dừng", "Xe mất tín hiệu"]
    status_colors = {
        "Xe đang di chuyển": "rgb(124, 179, 66)",
        "Xe dừng": "rgb(253, 216, 53)",
        "Xe mất tín hiệu": "rgb(117, 117, 117)"
    }

    @pytest.mark.Quick_Scan
    @allure.testcase("c4i2-1765", "c4i2-1765")
    @allure.epic("Giám sát hành trình")
    @allure.feature("Giám sát hành trình")
    @allure.story("Xác minh có dữ liệu tracking")
    @allure.title("Xác minh hiển thị dữ liệu danh sách tài khoản tracking")
    @pff.parametrize(path=pathDataTestTracking)
    def test_display_tracking_accounts(self, browser, OU):
        """Trường hợp kiểm thử Xác minh có hiển thị dữ liệu danh sách tài khoản tracking theo trạng thái
        - [Xe đang di chuyển, Xe dừng, Xe mất tín hiệu]"""
        driver = browser
        page_base = PageBase(driver)
        time.sleep(1)
        page_base.show_overlay_text("Xác minh hiển thị data tracking")
        with allure.step("Nhấn chọn OU"):
            xpath_check_search = ObjTrackingFuntion.button_tracking(OU)
            page_base.click_obj(xpath_check_search)
            capture_screenshot_and_attach_allure(driver, "IconSearchLocation")
            time.sleep(1)
        with allure.step("Filter status (check all)"):
            page_base.click_obj(Obj_Tracking.iconFilterStatus)
            for status in self.statuses:
                xpath_checkbox = ObjTrackingFuntion.checkbox_filter(status)

                try:
                    checkbox_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, xpath_checkbox))
                    )
                    if "checked" not in checkbox_element.get_attribute("class"):
                        checkbox_element.click()
                except Exception as e:
                    print(f"An error occurred: {str(e)}")
            capture_screenshot_and_attach_allure(driver, "CheckAll")
            time.sleep(1)
        with allure.step("Kiểm tra danh sách tracking trả về hiển thị các trạng thái"):
            number_user = 0
            for status in self.statuses:
                status_color = self.status_colors.get(status, "DEFAULT_COLOR")
                number_user_tracking = page_base.count_elements_by_xpath(ObjTrackingFuntion.icon_signal(status_color))
                time.sleep(1)
                number_user += number_user_tracking
                allure.attach(f"Số lượng {status} hiển thị: {number_user_tracking - 1}",
                              attachment_type=AttachmentType.TEXT)
            assert number_user > 3, "Không trả về danh sách theo dõi tracking"
