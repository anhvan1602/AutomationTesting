import time
import pytest
import allure

from Libraries.Framework.FactoryDrivers import get_chrome_driver
from Libraries.Framework.Utils import PageBase
from Libraries.Config import Default
from PageObjects.Web.Obj_Common import ObjCommon
from PageObjects.Web.Obj_Map import Obj_Map
from WebApplications.PageHome import LoginPage
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
    page_login.click_obj(Obj_Map.iconKhaiThacBanDo)
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




@pytest.mark.Compare_Image
class Test_SearchLocation:

    @allure.title("Tìm route giữa 2 địa điểm - demo compare image pass")
    @pytest.mark.parametrize("start_point, destination", [("VietBanDo", "Công viên Gia Định")])
    def test_compare_image_pass(self, browser, start_point, destination):
        """Trường hợp kiểm thử Xác minh có thể tìm được route giữa 2 điểm đã nhập"""
        driver = browser
        page_base = PageBase(driver)
        time.sleep(1)
        page_base.show_overlay_text("Tìm route")
        with allure.step("Nhấn vào icon Tìm đường"):
            xpath_check_search = Obj_Map.iconTimDuong
            page_base.click_obj(xpath_check_search)
            capture_screenshot_and_attach_allure(driver, "IconRouter")
            time.sleep(1)
        with allure.step("Nhấn vào tab Lộ trình"):
            xpath_tab_lo_trinh = Obj_Map.tabLoTrinh
            page_base.click_obj(xpath_tab_lo_trinh)
            time.sleep(1)
        with allure.step("Nhập điểm bắt đầu"):
            page_base.send_key_input(ObjCommon.input_search("Chọn điểm xuất phát"), start_point)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, "SetStartPoint")
            page_base.click_obj(Obj_Map.suggestOne)
        with allure.step("Nhập điểm đến"):
            page_base.send_key_input(ObjCommon.input_search("Chọn điểm đến"), destination)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, "SetDestination")
            page_base.click_obj(Obj_Map.suggestOne)
            time.sleep(2)
        with allure.step("Kiểm tra bằng so sánh ảnh"):
            verify = page_base.compare_imgage("searchroute", position=(196, 0), size=(1200, 700))
            assert verify, "So sánh hình ảnh thất bại: Đã phát hiện sự khác biệt lớn hơn ngưỡng cho phép."

    @allure.title("Tìm route giữa 2 địa điểm - demo compare image failed")
    @pytest.mark.parametrize("start_point, destination", [("VietBanDo", "Bộ tư lệnh quân khu 7")])
    def test_compare_image_failed(self, browser, start_point, destination):
        """Trường hợp kiểm thử Xác minh có thể tìm được route giữa 2 điểm đã nhập"""
        driver = browser
        page_base = PageBase(driver)
        time.sleep(1)
        page_base.show_overlay_text("Tìm route")
        with allure.step("Nhấn vào icon Tìm đường"):
            xpath_check_search = Obj_Map.iconTimDuong
            page_base.click_obj(xpath_check_search)
            capture_screenshot_and_attach_allure(driver, "IconRouter")
            time.sleep(1)
        with allure.step("Nhấn vào tab Lộ trình"):
            xpath_tab_lo_trinh = Obj_Map.tabLoTrinh
            page_base.click_obj(xpath_tab_lo_trinh)
            time.sleep(1)
        with allure.step("Nhập điểm bắt đầu"):
            page_base.send_key_input(ObjCommon.input_search("Chọn điểm xuất phát"), start_point)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, "SetStartPoint")
            page_base.click_obj(Obj_Map.suggestOne)
        with allure.step("Nhập điểm đến"):
            page_base.send_key_input(ObjCommon.input_search("Chọn điểm đến"), destination)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, "SetDestination")
            page_base.click_obj(Obj_Map.suggestOne)
            time.sleep(2)
        with allure.step("Kiểm tra bằng so sánh ảnh"):
            verify = page_base.compare_imgage("searchroute", position=(196, 0), size=(1200, 700))
            assert verify, "So sánh hình ảnh thất bại: Đã phát hiện sự khác biệt lớn hơn ngưỡng cho phép."