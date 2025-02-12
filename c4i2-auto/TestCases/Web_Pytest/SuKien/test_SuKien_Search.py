import time
import pytest
import allure
import datetime

from Libraries.Framework.FactoryDrivers import get_chrome_driver
from Libraries.Framework.Utils import PageBase
from Libraries.Config import Default
from PageObjects.Web.Obj_Common import ObjCommon
from PageObjects.Web.Obj_SuKien import Obj_SuKien

from WebApplications.PageHome import LoginPage
from WebApplications.PageSuKien import PageSuKien
from WebApplications.PageCommon import PageCommon
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



@pytest.mark.skipif(
        datetime.datetime.now().weekday() in [5, 6],
        reason="Testcase is skipped on Saturday and Sunday"
    )
@allure.link(
        "https://vietbando-my.sharepoint.com/:x:/g/personal/vannta_vietbando_vn/EQzmLNznQjpAn5iez9o0Qr8BkeWsfilGCGagIUZ1teg3qQ?e=ZY5q9o",
        name="File TestCase")
@allure.epic("Sự kiện")
@allure.feature("Phát hiện")
@pytest.mark.Event
class Test_SuKienPhatHien:
    pageBase = PageBase(browser)
    pathDataTestEvent = pageBase.load_path_data_file_from_path("Datas_Event",
                                                               "Test_SuKien_Search.json")

    @allure.testcase("c4i2-1354", "c4i2-1354")
    @allure.story("Xác minh hệ thống update liên tục dữ liệu phát hiện")
    @allure.title("Lọc theo Mốc thời gian")
    @pytest.mark.UAT
    @pytest.mark.Quick_Scan
    @pff.parametrize(path=pathDataTestEvent)
    def test_filter_by_timestamp_success(self, browser, ToTime):
        """ Trường hợp kiểm thử Tìm kiếm Sự kiện thành công (Gương Mặt & BSX)
        - Lọc theo Mốc thời gian - Danh sách lưới trả về kết quả trong khoảng thời gian lọc"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_check_server = PageSuKien(driver)
        time.sleep(1)
        cellid = "receiveTime"
        page_base.show_overlay_text("Lọc theo Mốc thời gian")

        with allure.step("Check vào checkbox lọc theo Mốc thời gian - Cách đây"):
            xpathchecksearch = ObjCommon.radio_button("Cách đây")
            page_base.click_obj(xpathchecksearch)
            capture_screenshot_and_attach_allure(driver, "CheckBox")
        with allure.step("Lựa chọn mốc thời gian cần lọc"):
            allure.attach(ToTime, name="Data Test", attachment_type=allure.attachment_type.TEXT)
            page_base.select_key_dropdown(Obj_SuKien.txtCachDay, ToTime)
            capture_screenshot_and_attach_allure(driver, "SetTime")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_SuKien.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="TimBSX")
        with allure.step("Kiểm tra thời gian phát hiện các kết quả trả về trên danh sách lưới"):
            list_value_actual = page_common.do_get_data_test_in_grid(cellid)
            result = page_check_server.do_verify_time_stamp_bsx(list_value_actual, ToTime, index=0)
            capture_screenshot_and_attach_allure(driver, name="ResultInGrid")
            assert result, f"Hiển thị danh sách kết quả lọc theo khoảng thời gian không hợp lệ"

    @allure.testcase("c4i2-362", "c4i2-362")
    @allure.story("Xác minh hệ thống update liên tục dữ liệu phát hiện")
    @allure.title("Xác minh có thể lọc theo tên đối tượng")
    @pff.parametrize(path=pathDataTestEvent)
    def test_search_fs_filter_by_timestamp_success(self, browser, NameObj, ToTime):
        """ Trường hợp kiểm thử Tìm kiếm Sự kiện thành công (Gương Mặt)
        - Lọc theo Mốc thời gian - Danh sách lưới trả về kết quả trong khoảng thời gian lọc"""
        driver = browser
        page_base = PageBase(driver)
        page_check_server = PageSuKien(driver)
        page_common = PageCommon(driver)
        time.sleep(1)
        page_base.show_overlay_text("Lọc theo Tên đối tượng & Mốc thời gian")
        with allure.step("Nhập tên đối tượng cần tìm vào tab Tìm kiếm"):
            xpath_obj = ObjCommon.input_search("Nhập tên đối tượng")
            page_base.send_key_input(xpath_obj, NameObj)
            capture_screenshot_and_attach_allure(driver, name="EnterInfo")
        with allure.step("Check vào checkbox lọc theo Mốc thời gian - Cách đây"):
            xpathchecksearch = ObjCommon.radio_button("Cách đây")
            page_base.click_obj(xpathchecksearch)
            capture_screenshot_and_attach_allure(driver, "CheckBox")
        with allure.step("Lựa chọn mốc thời gian cần lọc"):
            allure.attach(ToTime, name="Data Test", attachment_type=allure.attachment_type.TEXT)
            page_base.select_key_dropdown(Obj_SuKien.txtCachDay, ToTime)
            capture_screenshot_and_attach_allure(driver, "SetTime")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_SuKien.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="TimBSX")
        with allure.step("Kiểm tra tên đối tượng của tất cả kết quả trả về trên grid"):
            value = f"Gương mặt: {NameObj}"
            cellid = "Title"
            index = 0
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, value,
                                                                           index)
            capture_screenshot_and_attach_allure(driver, name="VerifyInGrid")
            assert result, f"Trên danh sách lưới có đối tượng '{different_value}' khác với giá trị đối tượng mong muốn '{value}"
        with allure.step("Kiểm tra thời gian phát hiện các kết quả trả về trên danh sách lưới"):
            cellid = "receiveTime"
            list_value_actual = page_common.do_get_data_test_in_grid(cellid)
            result = page_check_server.do_verify_time_stamp_bsx(list_value_actual, ToTime, index=0)
            capture_screenshot_and_attach_allure(driver, name="ResultInGrid")
            assert result, f"Hiển thị danh sách kết quả lọc theo khoảng thời gian không hợp lệ"

    @allure.testcase("c4i2-363", "c4i2-363")
    @allure.story("Xác minh hệ thống update liên tục dữ liệu phát hiện")
    @allure.title("Xác minh có thể lọc theo biển số xe")
    @pff.parametrize(path=pathDataTestEvent)
    def test_search_lpr_filter_by_timestamp_success(self, browser, ValueBSX, ToTime):
        """ Trường hợp kiểm thử Tìm kiếm Sự kiện thành công (Biển số xe)
        - Lọc theo Mốc thời gian - Danh sách lưới trả về kết quả trong khoảng thời gian lọc"""
        driver = browser
        page_base = PageBase(driver)
        page_check_server = PageSuKien(driver)
        page_common = PageCommon(driver)
        time.sleep(1)
        page_base.show_overlay_text("Lọc theo Biển số xe & Mốc thời gian")
        with allure.step("Nhập Biển số xe cần tìm vào tab Tìm kiếm"):
            xpath_bsx = ObjCommon.input_search("Nhập biển số xe")
            page_base.send_key_input(xpath_bsx, ValueBSX)
            capture_screenshot_and_attach_allure(driver, name="EnterInfo")
        with allure.step("Check vào checkbox lọc theo Mốc thời gian - Cách đây"):
            xpathchecksearch = ObjCommon.radio_button("Cách đây")
            page_base.click_obj(xpathchecksearch)
            capture_screenshot_and_attach_allure(driver, "CheckBox")
        with allure.step("Lựa chọn mốc thời gian cần lọc"):
            allure.attach(ToTime, name="Data Test", attachment_type=allure.attachment_type.TEXT)
            page_base.select_key_dropdown(Obj_SuKien.txtCachDay, ToTime)
            capture_screenshot_and_attach_allure(driver, "SetTime")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_SuKien.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="TimBSX")
        with allure.step("Kiểm tra biển số xe của tất cả kết quả trả về trên grid"):
            value = f"Biển số: {ValueBSX}"
            cellid = "Title"
            index = 0
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, value,
                                                                           index)
            capture_screenshot_and_attach_allure(driver, name="VerifyInGrid")
            assert result, f"Trên danh sách lưới hiển thị bsx '{different_value}' khác với giá trị bsx mong muốn '{value}"
        with allure.step("Kiểm tra thời gian phát hiện các kết quả trả về trên danh sách lưới"):
            cellid = "receiveTime"
            list_value_actual = page_common.do_get_data_test_in_grid(cellid)
            result = page_check_server.do_verify_time_stamp_bsx(list_value_actual, ToTime, index=0)
            capture_screenshot_and_attach_allure(driver, name="ResultInGrid")
            assert result, f"Hiển thị danh sách kết quả lọc theo khoảng thời gian không hợp lệ"

    @allure.testcase("c4i2-364", "c4i2-364")
    @allure.story("Xác minh hệ thống update liên tục dữ liệu phát hiện")
    @allure.title("Xác minh có thể lọc theo loại theo dõi")
    @pff.parametrize(path=pathDataTestEvent)
    def test_filter_by_monitoring_type(self, browser, LoaiTheoDoi, ToTime):
        """ Trường hợp kiểm thử Tìm kiếm Sự kiện thành công (theo Loại theo dõi)
        - Lọc theo Mốc thời gian - Danh sách lưới trả về kết quả trong khoảng thời gian lọc"""
        driver = browser
        page_base = PageBase(driver)
        page_check_server = PageSuKien(driver)
        page_common = PageCommon(driver)
        time.sleep(1)
        page_base.show_overlay_text("Lọc theo Loại theo dõi")
        with allure.step("Lựa chọn Camera cần lọc"):
            txt_search_bsx = ObjCommon.label_dropdown_list("Loại theo dõi")
            page_base.select_key_dropdown(txt_search_bsx, LoaiTheoDoi)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, "SelectCamera")
        with allure.step("Mở rộng thông tin danh sách lưới"):
            time.sleep(2)
            page_base.click_obj(Obj_SuKien.btnMoRongGrid)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="ExtendGrid")
        with allure.step("Check vào checkbox lọc theo Mốc thời gian - Cách đây"):
            xpathchecksearch = ObjCommon.radio_button("Cách đây")
            page_base.click_obj(xpathchecksearch)
            capture_screenshot_and_attach_allure(driver, "CheckBox")
        with allure.step("Lựa chọn mốc thời gian cần lọc"):
            allure.attach(ToTime, name="Data Test", attachment_type=allure.attachment_type.TEXT)
            page_base.select_key_dropdown(Obj_SuKien.txtCachDay, ToTime)
            capture_screenshot_and_attach_allure(driver, "SetTime")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_SuKien.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="TimBSX")
        with allure.step("Kiểm tra loại theo dõi của tất cả kết quả trả về trên grid"):
            cellid = "text_Danh_sách_theo_dõi"
            index = 0
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, LoaiTheoDoi,
                                                                           index)
            capture_screenshot_and_attach_allure(driver, name="VerifyInGrid")
            assert result, f"Trên danh sách lưới hiển thị loại theo dõi '{different_value}' khác với giá trị loại theo dõi mong muốn '{LoaiTheoDoi}"
        with allure.step("Kiểm tra thời gian phát hiện các kết quả trả về trên danh sách lưới"):
            cellid = "receiveTime"
            list_value_actual = page_common.do_get_data_test_in_grid(cellid)
            result = page_check_server.do_verify_time_stamp_bsx(list_value_actual, ToTime, index=0)
            capture_screenshot_and_attach_allure(driver, name="ResultInGrid")
            assert result, f"Hiển thị danh sách kết quả lọc theo khoảng thời gian không hợp lệ"

    @allure.testcase("c4i2-366", "c4i2-366")
    @allure.story("Tìm kiếm")
    @allure.title("Xác minh có thể tìm kiếm sự kiện với thời gian cụ thể")
    @pff.parametrize(path=pathDataTestEvent)
    def test_filter_by_time_range_success(self, browser, startTime, endTime):
        """ Trường hợp kiểm thử Tìm kiếm Sự kiện thành công (Gương Mặt & BSX)
        - Lọc theo Khoảng thời gian - Danh sách lưới trả về kết quả trong khoảng thời gian lọc"""
        driver = browser
        page_base = PageBase(driver)
        page_check_server = PageSuKien(driver)
        time.sleep(1)
        cellid = "receiveTime"
        page_base.show_overlay_text("Lọc theo Khoảng thời gian")

        with allure.step("Check vào checkbox - Tìm theo thời gian"):
            xpathchecksearch = ObjCommon.radio_button("Tìm theo thời gian")
            page_base.click_obj(xpathchecksearch)
            capture_screenshot_and_attach_allure(driver, "CheckBox")
        with allure.step("Thiết lập khoảng thời gian bắt đầu"):
            txt_search_time = ObjCommon.txt_search_time("Từ")
            input_search_time = ObjCommon.input_search_time("Từ")
            page_base.click_obj(txt_search_time)
            page_base.send_key_input(input_search_time, startTime)
            time.sleep(1)
            page_base.click_obj(xpathchecksearch)
            capture_screenshot_and_attach_allure(driver, "SetTime")
        with allure.step("Thiết lập khoảng thời gian kết thúc"):
            txt_search_time = ObjCommon.txt_search_time("Đến")
            input_search_time = ObjCommon.input_search_time("Đến")
            page_base.click_obj(txt_search_time)
            page_base.send_key_input(input_search_time, endTime)
            time.sleep(1)
            page_base.click_obj(xpathchecksearch)
            capture_screenshot_and_attach_allure(driver, "SetTime")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_SuKien.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="TimBSX")
        with allure.step("Kiểm tra thời gian phát hiện các kết quả trả về trên danh sách lưới"):
            result = page_check_server.do_verify_time_range_event(cellid, startTime, endTime)
            capture_screenshot_and_attach_allure(driver, name="ResultInGrid")
            assert result, f"Hiển thị danh sách kết quả lọc theo khoảng thời gian không hợp lệ"

    @allure.testcase("c4i2-361", "c4i2-361")
    @allure.story("Tìm kiếm")
    @allure.title("Xác minh có thể tìm kiếm với loại sự kiện")
    @pff.parametrize(path=pathDataTestEvent)
    def test_search_by_event_type(self, browser, eventType):
        """ Trường hợp kiểm thử Tìm kiếm Sự kiện thành công
        - Lọc theo Loại sự kiện - Danh sách lưới trả về kết quả đúng với điều kiện lọc"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        time.sleep(1)
        cellid = "Title"
        page_base.show_overlay_text("Lọc theo Loại sự kiện")

        with allure.step("Lựa chọn Loại sự kiện cần lọc"):
            xpath_event = ObjCommon.label_dropdown_list("Loại sự kiện")
            page_base.select_key_dropdown(xpath_event, eventType)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, "SelectCamera")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_SuKien.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="TimBSX")
        with allure.step("Kiểm tra loại sự kiện của tất cả kết quả trả về trên grid"):
            list_value_actual = page_common.do_get_data_test_in_grid(cellid)
            for item in list_value_actual:
                assert eventType in item[0], f"Trên danh sách lưới có sự kiện'{item}' khác với giá trị mong muốn '{eventType}"
            capture_screenshot_and_attach_allure(driver, name="VerifyInGrid")