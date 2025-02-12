import time
import pytest
import allure
import parametrize_from_file as pff

from Libraries.Framework.FactoryDrivers import get_chrome_driver
from Libraries.Framework.Utils import PageBase
from Libraries.Config import Default
from PageObjects.Web.Obj_BienSo import Obj_BienSo
from PageObjects.Web.Obj_Common import ObjCommon
from WebApplications.PageCommon import PageCommon
from WebApplications.PageHome import LoginPage
from WebApplications.PageBienSoXe import PageBienSoXeTabPhatHien
from conftest import capture_screenshot_and_attach_allure


@pytest.fixture(scope='class')
def browser():
    default_tenant = Default()
    driver = get_chrome_driver()
    driver.implicitly_wait(default_tenant.timeOut)

    url = default_tenant.url
    username = default_tenant.username
    password = default_tenant.password

    page_login = LoginPage(driver)
    page_base = PageBase(driver)

    driver.get(url)

    page_login.do_login(username, password)
    page_login.click_obj(Obj_BienSo.iconNhanDangBienSo)
    page_base.click_obj(Obj_BienSo.tabPhatHien)

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


@allure.epic("Nhận dạng biển số xe")
@allure.feature("Phát hiện BSX")
@pytest.mark.LPR
@pytest.mark.SearchDetectLPR
class Test_LPRPhatHienSearch:
    pageBase = PageBase(browser)
    pathDataTestSearchLpr = pageBase.load_path_data_file_from_path("Datas_LPR",
                                                                   "Test_PhatHien_Search_BSX.json")

    @pytest.mark.DC
    @pytest.mark.UAT
    @pytest.mark.UAT_DC
    @pytest.mark.Quick_Scan
    @allure.testcase("c4i2-709", "c4i2-709")
    @allure.story("Tìm kiếm BSX được phát hiện thành công")
    @allure.title("c4i2-709: Xác minh hệ thống vẫn đang hoạt động và cập nhật liên tục")
    # unit type ['seconds, 'minutes', 'hours', 'days']
    @pff.parametrize(path=pathDataTestSearchLpr)
    def test_verify_system_operation_and_continuous_update(self, browser, value, unit):
        """Trường hợp kiểm thử xác minh hệ thống vẫn hoạt động và cập nhật liên tục"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)

        time.sleep(1)
        page_base.show_overlay_text("Kiểm tra hệ thông")
        with allure.step("Lấy giá trị thời gian BSX đầu tiên được phát hiện trên danh sách lưới"):
            cellid = "details"
            datatest = page_common.do_get_data_test_in_grid(cellid)
            first_license = datatest[0][3]
            first_license = page_common.format_datetime(first_license)
            allure.attach(first_license, "Giá trị Test", allure.attachment_type.TEXT)
            capture_screenshot_and_attach_allure(driver, name="valuefirst")
        with allure.step("Lấy khoảng thời gian cần verify"):
            current_time, past_time = page_common.get_current_and_past_time(value, unit)
            current_time = page_common.format_datetime(current_time)
            past_time = page_common.format_datetime(past_time)
            allure.attach(f"{past_time}: {current_time}", "Khoảng thời gian kỳ vọng:", allure.attachment_type.TEXT)
        with allure.step("Verify thời gian thực tế có nằm trong khoảng thời gian mong muốn hay không"):
            result = page_common.is_valid_tim_range(first_license, past_time, current_time)
            assert result, f"Kết quả phát hiện mới nhất không nằm trong khoảng thời gian kỳ vọng"

    @pytest.mark.UAT_DC
    @allure.testcase("c4i2-353", "c4i2-353")
    @allure.story("Tìm kiếm BSX được phát hiện thành công")
    @allure.title("c4i2-353: Xác minh có thể tìm kiếm biển số xe bằng text (1 text)")
    @pytest.mark.Add_DataList
    @pff.parametrize(path=pathDataTestSearchLpr)
    def test_search_single_license_plate_success(self, browser, licensePlates, expected):
        """Trường hợp kiểm thử Tìm kiếm BSX thành công - Search 1 BSX (search text)"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        expected_lpr = expected['value']
        expected_status = expected['status']

        time.sleep(1)
        page_base.show_overlay_text("Search 1 BSX (search text)")
        cellid = "details"
        with allure.step("Nhập thông tin BSX vào tab Tìm kiếm"):
            txt_search_bsx = Obj_BienSo.txtSearchBSX
            page_base.send_key_input(txt_search_bsx, licensePlates)
            capture_screenshot_and_attach_allure(driver, name="EnterInfo")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_BienSo.btnTimKiem)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="TimBSX")
        if expected_status:
            with allure.step("Kiểm tra BSX của tất cả kết quả trả về trên grid"):
                index = 0
                list_actual = page_common.do_get_data_test_in_grid(cellid)
                result, different_value = page_common.do_verify_results_in_grid(list_actual, expected_lpr,
                                                                                index)
                capture_screenshot_and_attach_allure(driver, name="Verify")
                assert result, f"Trên danh sách lưới có biển số xe '{different_value}' khác với giá trị BSX mong muốn '{expected_lpr}"
        else:
            with allure.step("Kiểm tra kết quả trả về trên grid"):
                xpath = '//div[@class="dg-body"]'
                verify = page_base.verify_element_contains_content(xpath)
                capture_screenshot_and_attach_allure(driver, name="Verify")
                assert verify == expected_status, "Danh sách lưới vẫn trả về kết quả dù key search không hợp lệ"

    @allure.testcase("c4i2-823", "c4i2-823")
    @allure.story("Tìm kiếm BSX được phát hiện thành công")
    @allure.title("Tìm cùng lúc nhiều biển số (nhập text cách nhau bởi dấu phẩy)")
    def test_search_multiple_license_plates_success(self, browser):
        """Trường hợp kiểm thử Tìm kiếm BSX thành công - Search 2 BSX (search text)"""
        _timeout = 3
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)

        time.sleep(1)
        page_base.show_overlay_text("Search 2 BSX (search text)")
        with allure.step("Lấy 2 giá trị BSX trên danh lưới làm data test"):
            cellid = "details"
            datatest = page_common.do_get_data_test_in_grid(cellid)
            unique_license_plates_list = [item[0] for item in datatest]
            # Lấy 2 giá trị khác nhau của License_Plates
            if len(unique_license_plates_list) >= 2:
                license_plates1 = unique_license_plates_list[0]
                license_plates2 = unique_license_plates_list[1]
                license_plates = (license_plates1 + "," + license_plates2)
            allure.attach(license_plates1, "Giá trị BSX search 1", allure.attachment_type.TEXT)
            allure.attach(license_plates2, "Giá trị BSX search 2", allure.attachment_type.TEXT)
        with allure.step("Nhập thông tin BSX vào tab Tìm kiếm"):
            txt_search_bsx = Obj_BienSo.txtSearchBSX
            page_base.send_key_input(txt_search_bsx, license_plates)
            capture_screenshot_and_attach_allure(driver, name="EnterInfo")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_BienSo.btnTimKiem)
            time.sleep(_timeout)
            capture_screenshot_and_attach_allure(driver, name="TimBSX")
        with allure.step("Kiểm tra kết quả BSX thứ nhất trả về trên grid"):
            txt_search_bsx = ObjCommon.dropdown_list("Chọn biển số")
            page_base.select_key_dropdown(txt_search_bsx, license_plates1)
            time.sleep(_timeout)
            capture_screenshot_and_attach_allure(driver, "checkBSX1")
            index = 0
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, license_plates1,
                                                                            index)
            assert result, f"Trên danh sách lưới có biển số xe '{different_value}' khác với giá trị BSX mong muốn '{license_plates1}"
        with allure.step("Kiểm tra kết quả BSX thứ hai trả về trên grid"):
            time.sleep(_timeout)
            txt_search_bsx = ObjCommon.dropdown_list("Chọn biển số")
            page_base.select_key_dropdown(txt_search_bsx, license_plates2)
            time.sleep(_timeout)
            capture_screenshot_and_attach_allure(driver, "checkBSX2")
            index = 0
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, license_plates2,
                                                                            index)
            assert result, f"Trên danh sách lưới có biển số xe '{different_value}' khác với giá trị BSX mong muốn '{license_plates2}"

    @pytest.mark.DC
    @pytest.mark.UAT
    @pytest.mark.UAT_DC
    @allure.testcase("c4i2-820", "c4i2-820")
    @allure.story("Tìm kiếm BSX được phát hiện thành công")
    @allure.title("c4i2-820: Xác minh có thể tìm kiếm biển số xe bằng ảnh (1 ảnh)")
    @pytest.mark.Add_DataList
    @pff.parametrize(path=pathDataTestSearchLpr)
    def test_search_single_license_plate_image_success(self, browser, imageLicensePlates, expected):
        """Trường hợp kiểm thử Tìm kiếm BSX thành công - Search 1 BSX (search image) -
        [hình ảnh rõ biển số, hình ảnh không rõ biển số]"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_bien_so_xe_tab_phat_hien = PageBienSoXeTabPhatHien(driver)
        expected_lpr = expected['value']
        expected_status = expected['status']
        time.sleep(1)
        page_base.show_overlay_text("Search 1 BSX (search image)")
        with allure.step("Tải hình ảnh BSX lên tab Tìm kiếm"):
            page_bien_so_xe_tab_phat_hien.do_fill_image_bsx(imageLicensePlates)
            capture_screenshot_and_attach_allure(driver, name="UploadImage")
            time.sleep(2)
        if expected_status:
            with allure.step("Kiểm tra biển số từ ảnh được fill vào trường tìm kiếm"):
                capture_screenshot_and_attach_allure(driver, name="fillbsxfromimage")
                verify = page_bien_so_xe_tab_phat_hien.do_check_fill_bsx_from_image(expected_lpr)
                time.sleep(3)
                assert verify, "Biển số xe từ ảnh không được fill vào trường tìm kiếm"
            with allure.step("Set thời gian phát hiện BSX trong 1 tháng"):
                checkbox_range_time = f'//label[.//*[text()="Khoảng thời gian"]]//span[contains(@class,"radio-input checkbox")]'
                page_base.click_obj(checkbox_range_time)
                time.sleep(1)
                assert True
            with allure.step("Nhấn vào button Tìm kiếm"):
                page_base.click_obj(Obj_BienSo.btnTimKiem)
                time.sleep(1)
                capture_screenshot_and_attach_allure(driver, name="TimBSX")
            with allure.step("Kiểm tra kết quả BSX trả về trên grid"):
                cellid = "details"
                index = 0
                list_actual = page_common.do_get_data_test_in_grid(cellid)
                result, different_value = page_common.do_verify_results_in_grid(list_actual, expected_lpr,
                                                                                index)
                assert result, f"Trên danh sách lưới có biển số xe '{different_value}' khác với giá trị BSX mong muốn '{expected_lpr}"
        else:
            with allure.step("Kiểm tra thông báo lỗi"):
                check_popup = page_common.verify_notify_error(expected_lpr)
                allure.attach(driver.get_screenshot_as_png(), name="NotifyUnSuccess",
                              attachment_type=allure.attachment_type.PNG)
                assert check_popup, "Không có thông báo hoặc thông báo không hợp lệ khi tải ảnh không rõ biển số"

    @pytest.mark.DC
    @pytest.mark.UAT
    @allure.testcase("c4i2-822", "c4i2-822")
    @allure.story("Tìm kiếm BSX được phát hiện thành công")
    @allure.title("Tìm với ảnh nhiều biển số")
    @pytest.mark.Add_DataList
    @pff.parametrize(path=pathDataTestSearchLpr)
    def test_search_single_image_with_two_license_plates_success(self, browser, imageLicensePlates, expected):
        """Trường hợp kiểm thử Tìm kiếm BSX thành công - Search nhiều BSX với 1 hình ảnh(search image)"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_bien_so_xe_tab_phat_hien = PageBienSoXeTabPhatHien(driver)
        time.sleep(1)
        expected_lpr = expected['value']
        page_base.show_overlay_text("Search nhiều BSX (search image)")
        cellid = "details"
        with allure.step("Tải hình ảnh BSX lên tab Tìm kiếm"):
            page_bien_so_xe_tab_phat_hien.do_fill_image_bsx(imageLicensePlates)
            capture_screenshot_and_attach_allure(driver, name="UploadImage")
            time.sleep(2)
        with allure.step("Kiểm tra biển số từ ảnh được fill vào trường tìm kiếm"):
            for license_plates in expected_lpr:
                time.sleep(5)
                capture_screenshot_and_attach_allure(driver, name="fillbsxfromimage")
                verify = page_bien_so_xe_tab_phat_hien.do_check_fill_bsx_from_image(license_plates)
                time.sleep(3)
                assert verify, "Biển số xe từ ảnh không được fill vào trường tìm kiếm"
        with allure.step("Set thời gian phát hiện BSX trong 1 tháng"):
            checkbox_range_time = f'//label[.//*[text()="Khoảng thời gian"]]//span[contains(@class,"radio-input checkbox")]'
            page_base.click_obj(checkbox_range_time)
            time.sleep(1)
            assert True
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_BienSo.btnTimKiem)
            time.sleep(5)
            capture_screenshot_and_attach_allure(driver, name="TimBSX")
        for license_plates in expected_lpr:
            with allure.step(f"Kiểm tra kết quả BSX {license_plates} trả về trên grid"):
                txt_search_bsx = ObjCommon.dropdown_list("Chọn biển số")
                page_base.select_key_dropdown(txt_search_bsx, license_plates)
                time.sleep(3)
                capture_screenshot_and_attach_allure(driver, "checkBSX")
                index = 0
                list_actual = page_common.do_get_data_test_in_grid(cellid)
                result, different_value = page_common.do_verify_results_in_grid(list_actual, license_plates,
                                                                                index)
                assert result, f"Trên danh sách lưới có biển số xe '{different_value}' khác với giá trị BSX mong muốn '{license_plates}"

    @pytest.mark.UAT_DC
    @allure.testcase("c4i2-358", "c4i2-358")
    @allure.story("Tìm kiếm BSX được phát hiện thành công")
    @allure.title("c4i2-358: Xác minh có thể tìm kiếm biển số xe bằng độ chính xác đã chọn")
    @pytest.mark.Add_DataList
    @pff.parametrize(path=pathDataTestSearchLpr)
    def test_filter_by_accuracy_success(self, browser, From, To):
        """Trường hợp kiểm thử Tìm kiếm BSX thành công - Lọc theo độ chính xác"""
        driver = browser
        page_base = PageBase(driver)
        page_bien_so_xe_tab_phat_hien = PageBienSoXeTabPhatHien(driver)
        time.sleep(1)
        cellid = "accuracy"
        page_base.show_overlay_text("Lọc theo độ chính xác")
        with allure.step("Thiết lập độ chính xác cần tìm kiếm"):
            page_bien_so_xe_tab_phat_hien.do_move_slider(From, To)
            capture_screenshot_and_attach_allure(driver, name="SetAccuracy")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_BienSo.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="TimBSX")
        with allure.step("Kiểm tra độ chính xác các kết quả trả về trên danh sách lưới"):
            capture_screenshot_and_attach_allure(driver, name="ResultInGrid")
            result = page_bien_so_xe_tab_phat_hien.do_verify_accuracy_bsx(cellid, From, To)
        assert result, f"Hiển thị danh sách kết quả lọc theo độ chính xác không hợp lệ"

    @pytest.mark.UAT_DC
    @allure.testcase("c4i2-359", "c4i2-359")
    @allure.story("Tìm kiếm BSX được phát hiện thành công")
    @allure.title("c4i2-359: Xác minh có thể tìm kiếm với khoảng thời gian phát hiện cụ thể")
    @pytest.mark.Add_DataList
    @pff.parametrize(path=pathDataTestSearchLpr)
    def test_filter_by_time_range_success(self, browser, startTime, endTime):
        """Trường hợp kiểm thử Tìm kiếm BSX thành công - Lọc theo khoảng thời gian"""
        driver = browser
        page_base = PageBase(driver)
        page_bien_so_xe_tab_phat_hien = PageBienSoXeTabPhatHien(driver)
        time.sleep(1)
        cellid = "details"
        page_base.show_overlay_text("Lọc theo khoảng thời gian")

        with allure.step("Check vào checkbox lọc theo Mốc thời gian - Cách đây"):
            xpathchecksearch = ObjCommon.radio_button("Khoảng thời gian")
            page_base.click_obj(xpathchecksearch)
            capture_screenshot_and_attach_allure(driver, "CheckBox")
        with allure.step("Thiết lập thời gian bắt đầu"):
            txt_search_time = ObjCommon.txt_search_time("Từ")
            input_search_time = ObjCommon.input_search_time("Từ")
            page_base.click_obj(txt_search_time)
            page_base.send_key_input(input_search_time, startTime)
            time.sleep(1)
            page_base.click_obj(xpathchecksearch)
        with allure.step("Thiết lập thời gian kết thúc"):
            txt_search_time = ObjCommon.txt_search_time("Đến")
            input_search_time = ObjCommon.input_search_time("Đến")
            page_base.click_obj(txt_search_time)
            page_base.send_key_input(input_search_time, endTime)
            time.sleep(1)
            page_base.click_obj(xpathchecksearch)
        capture_screenshot_and_attach_allure(driver, "SetTime")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_BienSo.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="TimBSX")
        with allure.step("Kiểm tra thời gian phát hiện các kết quả trả về trên danh sách lưới"):
            index = 3
            result = page_bien_so_xe_tab_phat_hien.do_verify_time_range_bsx(cellid, startTime, endTime, index)
            time.sleep(3)
            capture_screenshot_and_attach_allure(driver, name="ResultInGrid")
            assert result, f"Hiển thị danh sách kết quả lọc theo khoảng thời gian không hợp lệ"

    @allure.testcase("c4i2-1398", "c4i2-1398")
    @allure.story("Tìm kiếm BSX được phát hiện thành công")
    @allure.title("Lọc theo Mốc thời gian")
    @pytest.mark.Add_DataList
    @pff.parametrize(path=pathDataTestSearchLpr)
    def test_filter_by_timestamp_success(self, browser, ToTime):
        """Trường hợp kiểm thử Tìm kiếm BSX thành công - Lọc theo Mốc thời gian"""
        driver = browser
        page_base = PageBase(driver)
        page_bien_so_xe_tab_phat_hien = PageBienSoXeTabPhatHien(driver)
        time.sleep(1)
        cellid = "details"
        page_base.show_overlay_text("Lọc theo Mốc thời gian")

        with allure.step("Check vào checkbox lọc theo Mốc thời gian - Cách đây"):
            xpathchecksearch = ObjCommon.radio_button("Cách đây")
            page_base.click_obj(xpathchecksearch)
            capture_screenshot_and_attach_allure(driver, "CheckBox")
        with allure.step("Lựa chọn mốc thời gian cần lọc"):
            page_base.click_obj(Obj_BienSo.txtCachDay)
            page_base.click_obj(ObjCommon.option_time_stamp(ToTime))
            capture_screenshot_and_attach_allure(driver, "SetTime")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_BienSo.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="TimBSX")
        with allure.step("Kiểm tra thời gian phát hiện các kết quả trả về trên danh sách lưới"):
            capture_screenshot_and_attach_allure(driver, name="ResultInGrid")
            index = 3
            result = page_bien_so_xe_tab_phat_hien.do_verify_time_stamp_bsx(cellid, ToTime, index)
        assert result, f"Hiển thị danh sách kết quả lọc theo khoảng thời gian không hợp lệ"

    @allure.testcase("c4i2-356", "c4i2-356")
    @allure.story("Tìm kiếm BSX được phát hiện thành công")
    @allure.title("Lọc theo Camera")
    @pytest.mark.Add_DataList
    @pff.parametrize(path=pathDataTestSearchLpr)
    def test_filter_by_camera_success(self, browser, Camera):
        """Trường hợp kiểm thử Tìm kiếm BSX thành công - Lọc theo Camera"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        time.sleep(1)
        cellid = "details"
        page_base.show_overlay_text("Lọc theo Camera")

        with allure.step("Lựa chọn Camera cần lọc"):
            txt_search_bsx = ObjCommon.dropdown_list("Camera")
            page_base.select_key_dropdown(txt_search_bsx, Camera)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, "SelectCamera")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_BienSo.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="TimBSX")
        with allure.step("Kiểm tra camera các kết quả trả về trên danh sách lưới"):
            index = 2
            time.sleep(3)
            capture_screenshot_and_attach_allure(driver, name="ResultInGrid")
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result = page_common.do_verify_results_in_grid(list_actual, Camera, index)
        assert result, f"Hiển thị danh sách kết quả lọc theo camera không hợp lệ"

    @allure.testcase("c4i2-353", "c4i2-353")
    @allure.story("Tìm kiếm BSX được phát hiện thành công")
    @allure.title("Search kết hợp (Biển số xe & Camera)")
    @pytest.mark.Add_DataList
    @pff.parametrize(path=pathDataTestSearchLpr)
    def test_filter_combined_license_plate_and_camera_success(self, browser, licensePlates, Camera):
        """Trường hợp kiểm thử Tìm kiếm BSX thành công - Search kết hợp (Biển số xe & Camera)"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)

        time.sleep(1)
        page_base.show_overlay_text("Lọc kết hợp (Biển số xe & Camera)")
        cellid = "details"

        with allure.step("Nhập thông tin BSX vào tab Tìm kiếm"):
            txt_search_bsx = Obj_BienSo.txtSearchBSX
            page_base.send_key_input(txt_search_bsx, licensePlates)
            capture_screenshot_and_attach_allure(driver, name="EnterInfo")
        with allure.step("Lựa chọn Camera cần lọc"):
            txt_search_camera = ObjCommon.dropdown_list("Camera")
            page_base.select_key_dropdown(txt_search_camera, Camera)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, "SelectCamera")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_BienSo.btnTimKiem)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="TimBSX")
        with allure.step("Kiểm tra BSX của tất cả kết quả trả về trên grid"):
            index = 0
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, licensePlates,
                                                                            index)
            assert result, f"Trên danh sách lưới có biển số xe '{different_value}' khác với giá trị BSX mong muốn '{licensePlates}"
        with allure.step("Kiểm tra camera các kết quả trả về trên danh sách lưới"):
            index = 2
            time.sleep(3)
            capture_screenshot_and_attach_allure(driver, name="ResultInGrid")
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result = page_common.do_verify_results_in_grid(list_actual, Camera, index)
        assert result, f"Hiển thị danh sách kết quả lọc theo camera không hợp lệ"

    @pytest.mark.UAT_DC
    @pytest.mark.Add_DataList
    @allure.testcase("c4i2-438", "c4i2-438")
    @allure.story("Tìm kiếm BSX được phát hiện thành công")
    @allure.title("c4i2-438: Nhấn Đặt lại (danh sách load về mặc định, các giá trị lọc bị remove)")
    @pytest.mark.Add_DataList
    @pff.parametrize(path=pathDataTestSearchLpr)
    def test_reset_button_behavior(self, browser, licensePlates):
        """Trường hợp kiểm thử nhấn Đặt lại (danh sách load về mặc định, các giá trị lọc bị remove)"""
        driver = browser
        page_base = PageBase(driver)
        page_bien_so_xe_tab_phat_hien = PageBienSoXeTabPhatHien(driver)
        time.sleep(1)
        page_base.show_overlay_text("kiểm thử nhấn Đặt lại")

        with allure.step("Nhập thông tin BSX vào tab Tìm kiếm"):
            txt_search_bsx = Obj_BienSo.txtSearchBSX
            page_base.send_key_input(txt_search_bsx, licensePlates)
            capture_screenshot_and_attach_allure(driver, name="EnterInfo")
        with allure.step("Nhấn vào button Đặt lại"):
            page_base.click_obj(Obj_BienSo.btnReset)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="Reset")
        with allure.step("Kiểm tra giá trị đã nhập/chọn"):
            result = page_bien_so_xe_tab_phat_hien.do_verify_data_cleaned(txt_search_bsx)
            assert result, "Resert giá trị nhập không thành công"

    @pytest.mark.DC
    @pytest.mark.UAT_DC
    @allure.testcase("c4i2-444", "c4i2-444")
    @allure.story("Tìm kiếm BSX được phát hiện thành công")
    @allure.title("c4i2-444: Xác minh có thể xem lịch sử phát hiện của biển số")
    def test_license_plate_detection_history_verification(self, browser):
        """Trường hợp kiểm thử xác minh có thể xem lịch sử nhận phát hiện biển số"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        time.sleep(1)
        page_base.show_overlay_text("Xem lịch sử phát hiện")

        with allure.step("Lấy giá trị BSX đầu tiên trên danh lưới làm data test"):
            cellid = "details"
            datatest = page_common.do_get_data_test_in_grid(cellid)
            first_license = datatest[0][0]
            allure.attach(first_license, "Giá trị Test", allure.attachment_type.TEXT)
        with allure.step("Nhấn vào button 'Xem chi tiết'"):
            page_base.click_obj(Obj_BienSo.iconDetail)
            capture_screenshot_and_attach_allure(driver, "PageDetail")
        with allure.step("Nhấn vào button 'Lịch sử'"):
            page_base.click_obj(Obj_BienSo.btnLichSu)
            capture_screenshot_and_attach_allure(driver, "PageDetail")
        with allure.step("Kiểm tra Lịch sử phát hiện sự kiện"):
            list_actual = page_common.do_get_data_test_on_grid_in_pop_up("details")
            result, different_value = page_common.do_verify_results_in_grid(list_actual, first_license, 0)
            byte_object = bytes(str(list_actual), 'utf-8')
            allure.attach(byte_object, "Lịch sử phát hiện:", allure.attachment_type.TEXT)
            assert result, f"Lịch sử phát hiện có biển số xe '{different_value}' khác với giá trị BSX kỳ vọng '{first_license}"
            capture_screenshot_and_attach_allure(driver, name="Check")

    @pytest.mark.DC
    @pytest.mark.UAT_DC
    @allure.testcase("c4i2-442", "c4i2-442")
    @allure.story("Tìm kiếm BSX được phát hiện thành công")
    @allure.title("c4i2-442: Xác minh có thể thêm theo dõi cho biển số")
    @pytest.mark.Add_DataList
    @pff.parametrize(path=pathDataTestSearchLpr)
    def test_add_tracking_to_detected_license_plates(self, browser, data_bsx, data_watchlist):
        """Trường hợp kiểm thử xác minh có thể xem thêm theo dõi cho biển số"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        time.sleep(1)
        page_base.show_overlay_text("Thêm theo dõi")
        cellid = "details"

        with allure.step("Nhập thông tin BSX vào tab Tìm kiếm"):
            txt_search_bsx = Obj_BienSo.txtSearchBSX
            page_base.send_key_input(txt_search_bsx, data_bsx)
            capture_screenshot_and_attach_allure(driver, name="EnterInfo")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_BienSo.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="TimBSX")
        with allure.step("Kiểm tra BSX của tất cả kết quả trả về trên grid"):
            index = 0
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, data_bsx,
                                                                            index)
            assert result, f"Trên danh sách lưới có biển số xe '{different_value}' khác với giá trị BSX mong muốn '{data_bsx}"
        with allure.step("Nhấn vào button 'Xem chi tiết'"):
            page_base.click_obj(Obj_BienSo.iconDetail)
            capture_screenshot_and_attach_allure(driver, "PageDetail")
        with allure.step("Nhấn vào button 'Thêm theo dõi'"):
            page_base.click_obj(Obj_BienSo.btnThemTheoDoi)
            capture_screenshot_and_attach_allure(driver, "PopupAddTracking")
        with allure.step("Chọn loại theo dõi tại popup theo dõi"):
            dropdown_tracking = ObjCommon.dropdown_list("Theo dõi")
            page_base.select_key_dropdown(dropdown_tracking, data_watchlist)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, "SelectCamera")
        with allure.step("Nhấn vào button 'Cập nhật'"):
            page_base.click_obj(Obj_BienSo.btnCapNhatBSX)
            capture_screenshot_and_attach_allure(driver, "UpdateTracking")
            time.sleep(2)
