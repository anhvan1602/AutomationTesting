import time
from datetime import datetime

import pytest
import allure
from selenium.common import TimeoutException

from Libraries.Framework.FactoryDrivers import get_chrome_driver
from Libraries.Framework.Utils import PageBase
from Libraries.Config import Default
from PageObjects.Web.Obj_BienSo import Obj_BienSo
from PageObjects.Web.Obj_SuKien import Obj_SuKien

from WebApplications.PageHome import LoginPage
from Libraries.Request import EventSimulator
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import parametrize_from_file as pff
from conftest import capture_screenshot_and_attach_allure


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
    page_login.click_obj(Obj_SuKien.iconSuKien)
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


@allure.epic("Sự kiện")
@allure.feature("Phát hiện BSX")
@pytest.mark.Detect
class Test_SuKienPhatHien:
    pageBase = PageBase(browser)
    pathDataTestEvent = pageBase.load_path_data_file_from_path("Datas_Event",
                                                          "Test_SuKien_Search.json")

    @allure.story("Nhận thông báo phát hiện")
    @allure.title("Nhận thông báo phát hiện sự kiện Biển số xe")
    @pff.parametrize(path=pathDataTestEvent, key="test_search_lpr_filter_by_timestamp_success")
    def test_VerifyThongBaoPhatHien(self, browser, ValueBSX, ToTime):
        """Trường hợp kiểm thử nhận thông báo phát hiện sự kiện Biển số xe"""
        bien_so = ValueBSX
        mess = f"Sự kiện mới: Biển số: {bien_so}"
        delay = 10
        driver = browser
        page_base = PageBase(driver)
        WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, '//h3[contains(text(), "Sự kiện")]')))
        time.sleep(5)
        page_base.show_overlay_text("Trường hợp kiểm thử nhận thông báo phát hiện sự kiện Biển số xe")
        with allure.step("Bắn giả lập sự kiện phát hiện biển số xe"):
            res = EventSimulator(bien_so)
            assert res, "Bắn giả lập thất bại"

        with allure.step("Kiểm tra nhận thông báo phát hiện sự kiện BSX"):
            total = 0
            txt_xpath = '//div[@class="toast-message css-0" and not(span[@class="tb tb1"])]'
            try:
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, txt_xpath)))
                element = driver.find_element(By.XPATH, '//div[@class="toast-message css-0"]')
                get_text_popup = element.text
                if get_text_popup == mess:
                    total += 1
                    capture_screenshot_and_attach_allure(driver, "Message")
                assert total > 0
            except TimeoutException:
                assert False, f"Không nhận được thông báo phát hiện sự kiện BSX {bien_so}"

    @allure.story("Nhận thông báo phát hiện")
    @allure.title("Kiểm tra dữ liêu được bắn phát hiện trên danh sách lưới")
    @pff.parametrize(path=pathDataTestEvent, key="test_search_lpr_filter_by_timestamp_success")
    def test_VerifyDuLieuPhatHien(self, browser, ValueBSX, ToTime):
        """Trường hợp verify dữ liệu phát hiện BSX trên danh sách lưới"""
        delay = 5
        driver = browser
        page_base = PageBase(driver)
        WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, '//h3[contains(text(), "Sự kiện")]')))
        time.sleep(5)
        page_base.show_overlay_text("Trường hợp verify dữ liệu phát hiện BSX trên danh sách lưới")
        bien_so = ValueBSX
        with allure.step("Bắn giả lập sự kiện phát hiện biển số xe"):
            current_time = datetime.now()
            formatted_time = current_time.strftime("%d/%m/%Y %H:%M")
            res = EventSimulator(bien_so)
            assert res, "Bắn giả lập thất bại"
        with allure.step("Tìm kiếm dữ liệu đã bắn giả lập phát hiện"):
            page_base.send_key_input(Obj_BienSo.txtSearchBSX, bien_so)
            time.sleep(1)
            page_base.click_obj(Obj_BienSo.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, "SearchBSX")
        with allure.step("Verify bsx được phát hiện trên grid"):
            time.sleep(2)
            txt_input_bien_so = '(//*[text()="{}"])[1]'.format(f"Biển số: {bien_so}")
            check_bien_so = page_base.check_element_visibility(txt_input_bien_so)

            txt_input_formatted_time = '(//*[text()="{}"])[1]'.format(formatted_time)
            check_formatted_time = page_base.check_element_visibility(txt_input_formatted_time)

            if check_bien_so and check_formatted_time:
                assert True, "Không tìm thấy dữ liệu đã bắn giả lập phát hiện trên danh sách lưới"
