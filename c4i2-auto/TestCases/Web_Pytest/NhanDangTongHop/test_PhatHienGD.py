import time
import pytest
import allure

from Libraries.Framework.FactoryDrivers import get_chrome_driver
from Libraries.Framework.Utils import PageBase
from Libraries.Config import Default
from PageObjects.Web.Obj_Common import ObjCommon
from WebApplications.PageCommon import PageCommon
from PageObjects.Web.Obj_TongHop import Obj_TongHop
from WebApplications.PageHome import LoginPage
from WebApplications.PageGuongMat import PageGuongMatTabPhatHien
from conftest import capture_screenshot_and_attach_allure
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
    page_login.click_obj(Obj_TongHop.iconNhanDangTongHop)
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


@pytest.mark.GD
@allure.epic("Nhận dạng tổng hợp")
@allure.feature("Phát hiện")
class Test_GDPhatHien:
    pageBase = PageBase(browser)
    pathDataTestGD = pageBase.load_path_data_file_from_path("Datas_GD",
                                                       "Test_PhatHienGD.json")

    @pytest.mark.Quick_Scan
    @allure.testcase("c4i2-715", "c4i2-715")
    @allure.story("Xác minh hệ thống update liên tục dữ liệu")
    @allure.title("Lọc theo Mốc thời gian")
    @pff.parametrize(path=pathDataTestGD)
    def test_filter_by_timestamp_success(self, browser, ToTime):
        """Trường hợp kiểm thử có dữ liệu tại danh sách lưới trong khoảng thời gian mong muốn"""
        driver = browser
        page_base = PageBase(driver)
        page_guong_mat_tab_phat_hien = PageGuongMatTabPhatHien(driver)
        time.sleep(1)
        cellid = "information"
        page_base.show_overlay_text("Lọc theo Mốc thời gian")
        with allure.step("Kiểm tra thời gian phát hiện các kết quả trả về trên danh sách lưới"):
            capture_screenshot_and_attach_allure(driver, name="ResultInGrid")
            result = page_guong_mat_tab_phat_hien.do_verify_time_stamp_face(cellid, ToTime)
        assert result, f"Hiển thị danh sách kết quả lọc theo khoảng thời gian không hợp lệ"

    @allure.testcase("c4i2-711", "c4i2-711")
    @allure.story("Tìm kiếm")
    @allure.title("Lọc theo Mốc thời gian")
    @pff.parametrize(path=pathDataTestGD)
    def test_verify_search_by_camera(self, browser, Camera):
        """Trường hợp kiểm thử có dữ liệu khi search theo camera"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        time.sleep(1)
        cellid = "information"
        page_base.show_overlay_text("Lọc theo Camera")
        with allure.step("Mở rộng danh sách lưới"):
            page_base.click_obj(ObjCommon.button_with_icon("fal fa-list"))
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="ExtendGrid")
        with allure.step("Lựa chọn Camera cần lọc"):
            txt_search_bsx = ObjCommon.dropdown_list("Camera")
            page_base.select_key_dropdown(txt_search_bsx, Camera)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, "SelectCamera")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(ObjCommon.text_span("Tìm kiếm"))
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="ClickButtonSearch")
        with allure.step("Kiểm tra camera các kết quả trả về trên danh sách lưới"):
            index = 0
            capture_screenshot_and_attach_allure(driver, name="ResultInGrid")
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result = page_common.do_verify_results_in_grid(list_actual, Camera, index)
        assert result, f"Hiển thị danh sách kết quả lọc theo camera không hợp lệ"

    @allure.testcase("c4i2-714", "c4i2-714")
    @allure.story("Tìm kiếm")
    @allure.title("Lọc theo Khoảng thời gian")
    @pff.parametrize(path=pathDataTestGD)
    def test_filter_by_time_range_success(self, browser, startTime, endTime):
        """Trường hợp kiểm thử có dữ liệu khi search theo Khoảng thời gian"""
        driver = browser
        page_base = PageBase(driver)
        page_guong_mat_tab_phat_hien = PageGuongMatTabPhatHien(driver)
        time.sleep(1)
        cellid = "information"
        page_base.show_overlay_text("Lọc theo Khoảng thời gian")
        with allure.step("Mở rộng danh sách lưới"):
            page_base.click_obj(ObjCommon.button_with_icon("fal fa-list"))
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="ExtendGrid")
        with allure.step("Check vào checkbox lọc theo Khoảng thời gian"):
            xpathchecksearch = ObjCommon.radio_button("Khoảng thời gian")
            scrolltoelement = ObjCommon.radio_button("Cách đây")
            page_base.click_obj(xpathchecksearch)
            capture_screenshot_and_attach_allure(driver, "CheckBox")
        with allure.step("Thiết lập khoảng thời gian bắt đầu"):
            txt_search_time = ObjCommon.txt_search_time("Từ")
            input_search_time = ObjCommon.input_search_time("Từ")
            page_base.do_scroll_mouse_to_element(scrolltoelement)
            page_base.click_obj(txt_search_time)
            page_base.send_key_input(input_search_time, startTime)
            time.sleep(1)
            page_base.click_obj(xpathchecksearch)
            capture_screenshot_and_attach_allure(driver, "SetTime")
        with allure.step("Thiết lập khoảng thời gian kết thúc"):
            txt_search_time = ObjCommon.txt_search_time("Đến")
            input_search_time = ObjCommon.input_search_time("Đến")
            page_base.do_scroll_mouse_to_element(scrolltoelement)
            page_base.click_obj(txt_search_time)
            page_base.send_key_input(input_search_time, endTime)
            time.sleep(1)
            page_base.click_obj(xpathchecksearch)
            capture_screenshot_and_attach_allure(driver, "SetTime")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(ObjCommon.text_span("Tìm kiếm"))
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="SearchFace")
        with allure.step("Kiểm tra thời gian phát hiện các kết quả trả về trên danh sách lưới"):
            capture_screenshot_and_attach_allure(driver, name="ResultInGrid")
            result = page_guong_mat_tab_phat_hien.do_verify_time_range_face(cellid, startTime, endTime)
            assert result, f"Hiển thị danh sách kết quả lọc theo khoảng thời gian không hợp lệ"

    @allure.testcase("c4i2-714", "c4i2-714")
    @allure.story("Tìm kiếm")
    @allure.title("Xác minh có thể tìm với biển số xe")
    @pff.parametrize(path=pathDataTestGD)
    def test_verify_search_by_license_plate(self, browser, licensePlates):
        """Trường hợp kiểm thử có dữ liệu khi search theo Biển số xe"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        time.sleep(1)
        cellid = "details"
        page_base.show_overlay_text("Lọc theo Biển số xe")
        with allure.step("Mở rộng danh sách lưới"):
            page_base.click_obj(ObjCommon.button_with_icon("fal fa-list"))
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="ExtendGrid")
        with allure.step("Nhấn (+)"):
            xpath_option = ObjCommon.button_with_icon("fal fa-plus")
            page_base.click_obj(xpath_option)
            capture_screenshot_and_attach_allure(driver, "ClickAdd")
        with allure.step("Lựa chọn lọc theo Biển số"):
            xpath_option_lpr = ObjCommon.option_menu("Biển số")
            page_base.click_obj(xpath_option_lpr)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, "SelectOption")
        with allure.step("Nhập thông tin BSX vào tab Tìm kiếm"):
            page_base.send_key_input(ObjCommon.search_textbox("Biển số"), licensePlates)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, "EnterValue")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(ObjCommon.text_span("Tìm kiếm"))
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="SearchFace")
        with allure.step("Kiểm tra kết quả trả về trên danh sách lưới"):
            capture_screenshot_and_attach_allure(driver, name="ResultInGrid")
            results = page_common.do_get_data_test_in_grid(cellid)
            print(results)
            for result in results:
                assert licensePlates in result[0], f"'{licensePlates}' not found in {result[0]}"
