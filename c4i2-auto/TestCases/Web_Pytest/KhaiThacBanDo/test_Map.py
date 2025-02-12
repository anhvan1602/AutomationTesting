import time
import pytest
import allure

from Libraries.Framework.FactoryDrivers import get_chrome_driver
from Libraries.Framework.Utils import PageBase
from Libraries.Config import Default
from PageObjects.Web.Obj_Common import ObjCommon
from PageObjects.Web.Obj_Map import Obj_Map
from WebApplications.PageHome import LoginPage
from allure_commons.types import AttachmentType
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


@pytest.mark.DC
@pytest.mark.Map
class Test_SearchLocation:
    pageBase = PageBase(browser)
    pathDataTestMap = pageBase.load_path_data_file_from_path("Datas_Map",
                                                             "Test_Map.json")

    @pytest.mark.Quick_Scan
    @allure.testcase("c4i2-225", "c4i2-225")
    @allure.epic("Khai thác bản đồ")
    @allure.feature("Tìm vị trí")
    @allure.story("Xác minh dịch vụ hoạt động, có thể tìm vị trí")
    @allure.title("Tìm vị trí trên map")
    @pff.parametrize(path=pathDataTestMap)
    def test_search_location_success(self, browser, location):
        """Trường hợp kiểm thử Tìm kiếm 1 vị trí trên map"""
        driver = browser
        page_base = PageBase(driver)
        time.sleep(1)
        page_base.show_overlay_text("Tìm vị trí")
        with allure.step("Nhấn vào icon Tìm Vị trí"):
            page_base.click_obj(Obj_Map.iconTimViTri)
            capture_screenshot_and_attach_allure(driver, "IconSearchLocation")
            time.sleep(1)
        with allure.step("Nhập và tìm vị trí"):
            page_base.send_key_input(Obj_Map.inputSearchLocation, location)
            capture_screenshot_and_attach_allure(driver, "SetLocation")
            time.sleep(1)
            page_base.click_obj(Obj_Map.suggestOne)
        with allure.step("Kiểm tra có popup xuất hiện vị trí trên map"):
            verify = page_base.check_element_visibility(Obj_Map.popupViTriHienTai)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="VerifyPopUp")
            assert verify, "Không hiển thị dữ liệu trên bản đồ"

    @allure.testcase("c4i2-1337", "c4i2-1337")
    @allure.epic("Khai thác bản đồ")
    @allure.feature("Tìm vị trí")
    @allure.title("Xác minh hiển thị ảnh địa điểm trong pop-up thông tin vị trí")
    @pff.parametrize(path=pathDataTestMap)
    def test_verify_display_location_image_in_info_popup(self, browser, location):
        """Trường hợp kiểm thử có hiển thị hình ảnh trong popup thông tin vị trí"""
        driver = browser
        page_base = PageBase(driver)
        time.sleep(1)
        page_base.show_overlay_text("Hiển thị hình ảnh tại vị trí")
        with allure.step("Nhấn vào icon Tìm Vị trí"):
            page_base.click_obj(Obj_Map.iconTimViTri)
            capture_screenshot_and_attach_allure(driver, "IconSearchLocation")
            time.sleep(1)
        with allure.step("Nhập và tìm vị trí"):
            page_base.send_key_input(Obj_Map.inputSearchLocation, location)
            capture_screenshot_and_attach_allure(driver, "SetLocation")
            time.sleep(1)
            page_base.click_obj(Obj_Map.suggestOne)
        with allure.step("Kiểm tra có popup xuất hiện vị trí trên map"):
            verify = page_base.check_element_visibility(Obj_Map.popupViTriHienTai)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="VerifyPopUp")
            assert verify, "Không hiển thị dữ liệu trên bản đồ"
        with allure.step("Kiểm tra hình ảnh trong popup vị trí"):
            verify_image = page_base.check_element_visibility(Obj_Map.imageInPopup)
            assert verify_image, "Hình ảnh xuất hiện trong popup không trùng khớp với kỳ vọng"

    @pytest.mark.Quick_Scan
    @allure.testcase("c4i2-227", "c4i2-227")
    @allure.epic("Khai thác bản đồ")
    @allure.feature("Tìm đường")
    @allure.story("Xác minh dịch vụ hoạt động, có thể tìm route")
    @allure.title("Tìm route giữa 2 địa điểm")
    @pff.parametrize(path=pathDataTestMap)
    def test_find_route_between_points(self, browser, start_point, destination):
        """Trường hợp kiểm thử Xác minh có thể tìm được route giữa 2 điểm đã nhập"""
        driver = browser
        page_base = PageBase(driver)
        time.sleep(1)
        page_base.show_overlay_text("Tìm route")
        with allure.step("Nhấn vào icon Tìm đường"):
            page_base.click_obj(Obj_Map.iconTimDuong)
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
        with allure.step("Kiểm tra có hướng dẫn route hay không"):
            verify = page_base.check_element_visibility(Obj_Map.xpath_route)
            capture_screenshot_and_attach_allure(driver, "Route")
            assert verify, "Không có route giữa 2 điểm"
        with allure.step("Thông tin chi tiết route giữa 2 điểm"):
            try:
                xpath_routes = page_base.get_text_element(Obj_Map.xpath_route, multiple=True)
                allure.attach(f"{xpath_routes}",
                              attachment_type=AttachmentType.TEXT)
            except Exception as e:
                allure.attach(f"Không thể tìm thấy hướng dẫn bước đi: {e}", name="Error",
                              attachment_type=AttachmentType.TEXT)


@pytest.mark.DC
class Test_BanDoTacChien:
    pageBase = PageBase(browser)
    pathDataTestMap = pageBase.load_path_data_file_from_path("Datas_Map",
                                                             "Test_Map.json")

    @allure.testcase("c4i2-176", "c4i2-176")
    @allure.testcase("c4i2-173", "c4i2-173")
    @allure.epic("Khai thác bản đồ")
    @allure.feature("Bản đồ tác chiến")
    @allure.story("Nhãn")
    @allure.title("Xác minh có thể tạo và xóa nhãn thành công")
    @pff.parametrize(path=pathDataTestMap)
    def test_create_and_delete_label_successfully(self, browser, title_label):
        """Trường hợp kiểm thử kiểm tra có thể tạo Nhãn & xóa Nhãn trên bản đồ"""
        driver = browser
        page_base = PageBase(driver)
        time.sleep(1)
        page_base.show_overlay_text("Tạo & Xóa Nhãn")
        try:
            with allure.step("Nhấn vào tính năng Bản đồ tác chiến"):
                page_base.click_obj(Obj_Map.iconBanDoTacChien)
                capture_screenshot_and_attach_allure(driver, "ClickBDTC")
                time.sleep(1)
            with allure.step("Nhấn vào button Nhãn"):
                page_base.click_obj(Obj_Map.iconNhan)
                capture_screenshot_and_attach_allure(driver, "ClickIcon")
                verify_icon_nhan = page_base.check_element_visibility(Obj_Map.verifyIconNhan)
                time.sleep(1)
                assert verify_icon_nhan, "Không có Highlight màu xanh khi chọn Nhãn"
            with allure.step("Nhấn vào Map - đặt Nhãn"):
                page_base.click_multiple_positions([(800, 400)])
                capture_screenshot_and_attach_allure(driver, "Set")
            with allure.step("Đổi tên Nhãn"):
                page_base.click_obj(ObjCommon.ellipsis_icon("Nhãn"))
                page_base.click_obj(ObjCommon.option_menu("Đổi tên"))
                page_base.set_val_input(Obj_Map.itemRename, title_label)
                capture_screenshot_and_attach_allure(driver, "Rename")
            with allure.step("Nhấn Áp dụng"):
                page_base.click_obj(Obj_Map.btnApDung)
                txt_xpath = ObjCommon.item_last_in_list(title_label)
                verify_rename_marker = page_base.check_element_visibility(txt_xpath)
                assert verify_rename_marker, "Đổi tên Nhãn không thành công"
            with allure.step("Load lại web - kiểm tra nhãn đã tạo"):
                driver.refresh()
                page_base.click_obj(Obj_Map.iconBanDoTacChien)
                txt_xpath = f'//div[contains(@class, "mapboxgl-marker")]//child::*[text()="{title_label}"]'
                verify_marker = page_base.check_element_visibility(txt_xpath)
                assert verify_marker, "Không tìm thấy Nhãn đã tạo trên map"
                capture_screenshot_and_attach_allure(driver, "Verify")
        finally:
            with allure.step("Xóa nhãn đã tạo"):
                page_base.click_obj(ObjCommon.ellipsis_icon(title_label))
                page_base.click_obj(ObjCommon.option_menu("Xóa"))
                page_base.click_obj(Obj_Map.btnApDung)
                capture_screenshot_and_attach_allure(driver, "Delete")
            with allure.step("Load lại web - kiểm tra nhãn đã xóa"):
                driver.refresh()
                page_base.click_obj(Obj_Map.iconBanDoTacChien)
                txt_xpath = f'//div[contains(@class, "mapboxgl-marker")]//child::*[text()="{title_label}"]'
                verify_marker = page_base.check_element_visibility(txt_xpath, wait_time=1)
                assert not verify_marker, "Xóa nhãn không thành công"

    @allure.testcase("c4i2-177", "c4i2-177")
    @allure.testcase("c4i2-252", "c4i2-252")
    @allure.epic("Khai thác bản đồ")
    @allure.feature("Bản đồ tác chiến")
    @allure.story("Điểm")
    @allure.title("Xác minh có thể tạo và xóa điểm thành công")
    @pff.parametrize(path=pathDataTestMap)
    def test_create_and_delete_point_successfully(self, browser, title_point):
        """Trường hợp kiểm thử kiểm tra có thể tạo Điểm & xóa Điểm trên bản đồ"""
        driver = browser
        page_base = PageBase(driver)
        time.sleep(1)
        page_base.show_overlay_text("Tạo & Xóa Điểm")
        try:
            with allure.step("Nhấn vào tính năng Bản đồ tác chiến"):
                page_base.click_obj(Obj_Map.iconBanDoTacChien)
                capture_screenshot_and_attach_allure(driver, "ClickBDTC")
                time.sleep(1)
            with allure.step("Nhấn vào button Điểm"):
                page_base.click_obj(Obj_Map.iconDiem)
                capture_screenshot_and_attach_allure(driver, "ClickIcon")
                verify_icon_nhan = page_base.check_element_visibility(Obj_Map.verifyIconDiem)
                time.sleep(1)
                assert verify_icon_nhan, "Không có Highlight màu xanh khi chọn Điểm"
            with allure.step("Nhấn vào Map - đặt Điểm"):
                page_base.click_multiple_positions([(800, 500)])
                capture_screenshot_and_attach_allure(driver, "Set")
            with allure.step("Đổi tên Nhãn"):
                page_base.click_obj(ObjCommon.ellipsis_icon("Điểm"))
                page_base.click_obj(ObjCommon.option_menu("Đổi tên"))
                page_base.set_val_input(Obj_Map.itemRename, title_point)
                capture_screenshot_and_attach_allure(driver, "Rename")
            with allure.step("Nhấn Áp dụng"):
                page_base.click_obj(Obj_Map.btnApDung)
                txt_xpath = ObjCommon.item_last_in_list(title_point)
                verify_rename_marker = page_base.check_element_visibility(txt_xpath)
                assert verify_rename_marker, "Đổi tên Nhãn không thành công"
            with allure.step("Load lại web - kiểm tra điểm đã tạo"):
                driver.refresh()
                page_base.click_obj(Obj_Map.iconBanDoTacChien)
                txt_xpath = ObjCommon.item_last_in_list(title_point)
                verify_marker = page_base.check_element_visibility(txt_xpath)
                assert verify_marker, "Không lưu Điểm đã tạo"
                capture_screenshot_and_attach_allure(driver, "Verify")
        finally:
            with allure.step("Xóa điểm đã tạo"):
                page_base.click_obj(ObjCommon.ellipsis_icon(title_point))
                page_base.click_obj(ObjCommon.option_menu("Xóa"))
                page_base.click_obj(Obj_Map.btnApDung)
                capture_screenshot_and_attach_allure(driver, "Delete")
            with allure.step("Load lại web - kiểm tra điểm đã xóa"):
                driver.refresh()
                page_base.click_obj(Obj_Map.iconBanDoTacChien)
                txt_xpath = ObjCommon.item_last_in_list(title_point)
                verify_marker = page_base.check_element_visibility(txt_xpath, wait_time=1)
                assert not verify_marker, "Xóa điểm không thành công"
                capture_screenshot_and_attach_allure(driver, "Verify")

    @allure.testcase("c4i2-186", "c4i2-186")
    @allure.epic("Khai thác bản đồ")
    @allure.feature("Bản đồ tác chiến")
    @allure.story("Điểm")
    @allure.title("Xác minh có thể bật/tắt tìm kiếm nâng cao")
    @pff.parametrize(path=pathDataTestMap)
    def test_toggle_advanced_search_with_point(self, browser, title_point, radius, data_layer):
        """Trường hợp kiểm thử kiểm tra có thể bật và tắt tìm kiếm nâng cao với Điểm trên bản đồ"""
        driver = browser
        page_base = PageBase(driver)
        time.sleep(1)
        page_base.show_overlay_text("Bật & Tắt Tìm kiếm nâng cao")

        try:
            with allure.step("Nhấn vào tính năng Bản đồ tác chiến"):
                page_base.click_obj(Obj_Map.iconBanDoTacChien)
                capture_screenshot_and_attach_allure(driver, "ClickBDTC")
                time.sleep(1)
            with allure.step("Nhấn vào button Điểm"):
                page_base.click_obj(Obj_Map.iconDiem)
                capture_screenshot_and_attach_allure(driver, "ClickIcon")
                verify_icon_nhan = page_base.check_element_visibility(Obj_Map.verifyIconDiem)
                time.sleep(1)
                assert verify_icon_nhan, "Không có Highlight màu xanh khi chọn Điểm"
            with allure.step("Nhấn vào Map - đặt Điểm"):
                page_base.click_multiple_positions([(800, 600)])
                capture_screenshot_and_attach_allure(driver, "Set")
            with allure.step("Đổi tên Nhãn"):
                page_base.click_obj(ObjCommon.ellipsis_icon("Điểm"))
                page_base.click_obj(ObjCommon.option_menu("Đổi tên"))
                page_base.set_val_input(Obj_Map.itemRename, title_point)
                capture_screenshot_and_attach_allure(driver, "Rename")
            with allure.step("Nhấn Áp dụng"):
                page_base.click_obj(Obj_Map.btnApDung)
                txt_xpath = ObjCommon.item_last_in_list(title_point)
                verify_rename_marker = page_base.check_element_visibility(txt_xpath)
                assert verify_rename_marker, "Đổi tên Nhãn không thành công"
            with allure.step("Bật Tìm kiếm nâng cao"):
                page_base.click_obj(ObjCommon.ellipsis_icon(title_point))
                page_base.click_obj(ObjCommon.option_menu("Tìm kiếm nâng cao"))
            with allure.step("Thiết lập tìm kiếm nâng cao"):
                page_base.send_key_input(ObjCommon.search_textbox("Bán kính"), radius)
                page_base.click_obj(ObjCommon.search_textbox("Lớp dữ liệu"))
                page_base.send_key_input(Obj_Map.inputLopDuLieu, data_layer)
                time.sleep(2)
                page_base.click_obj(ObjCommon.checkbox_filter(data_layer))
                page_base.click_obj(Obj_Map.btnApDung)
            with allure.step("Kiểm tra kết quả trả về"):
                verify_results = page_base.check_element_visibility(Obj_Map.verifyResultsSearch)
                assert verify_results, f"Không có kết quả trả về từ tìm kiếm nâng cao, {data_layer}"
                value_results = page_base.get_text_element(Obj_Map.verifyResultsSearch)
                print(value_results)
            with allure.step("Tắt tìm kiếm nâng cao"):
                page_base.click_obj(Obj_Map.iconDelete)
                verify_search_advance = page_base.check_element_visibility(Obj_Map.verifyResultsSearch, wait_time=2)
                assert not verify_search_advance, "Không thể tắt tìm kiếm nâng cao"
        finally:
            with allure.step("Xóa điểm đã tạo"):
                page_base.click_obj(ObjCommon.ellipsis_icon(title_point))
                page_base.click_obj(ObjCommon.option_menu("Xóa"))
                page_base.click_obj(Obj_Map.btnApDung)
                capture_screenshot_and_attach_allure(driver, "Delete")
            with allure.step("Load lại web - kiểm tra điểm đã xóa"):
                driver.refresh()
                page_base.click_obj(Obj_Map.iconBanDoTacChien)
                txt_xpath = ObjCommon.item_last_in_list(title_point)
                verify_marker = page_base.check_element_visibility(txt_xpath, wait_time=1)
                assert not verify_marker, "Xóa điểm không thành công"
                capture_screenshot_and_attach_allure(driver, "Verify")

    @allure.testcase("c4i2-254", "c4i2-254")
    @allure.testcase("c4i2-259", "c4i2-259")
    @allure.epic("Khai thác bản đồ")
    @allure.feature("Bản đồ tác chiến")
    @allure.story("Đường")
    @allure.title("Xác minh có thể tạo và xóa đường thành công")
    @pff.parametrize(path=pathDataTestMap)
    def test_create_and_delete_line_successfully(self, browser, title_line):
        """Trường hợp kiểm thử kiểm tra có thể tạo Điểm & xóa Đường trên bản đồ"""
        driver = browser
        page_base = PageBase(driver)
        time.sleep(1)
        page_base.show_overlay_text("Tạo & Xóa Đường")
        try:
            with allure.step("Nhấn vào tính năng Bản đồ tác chiến"):
                page_base.click_obj(Obj_Map.iconBanDoTacChien)
                capture_screenshot_and_attach_allure(driver, "ClickBDTC")
                time.sleep(1)
            with allure.step("Nhấn vào button Đường"):
                page_base.click_obj(Obj_Map.iconDuong)
                capture_screenshot_and_attach_allure(driver, "ClickIcon")
                verify_icon = page_base.check_element_visibility(Obj_Map.verifyIconDuong)
                time.sleep(1)
                assert verify_icon, "Không có Highlight màu xanh khi chọn Đường"
            with allure.step("Nhấn vào Map - vẽ Đường"):
                page_base.click_multiple_positions([(800, 600), (800, 700), (800, 700)])
                capture_screenshot_and_attach_allure(driver, "Set")
            with allure.step("Đổi tên Đường"):
                page_base.click_obj(ObjCommon.ellipsis_icon("Đường"))
                page_base.click_obj(ObjCommon.option_menu("Đổi tên"))
                page_base.set_val_input(Obj_Map.itemRename, title_line)
                capture_screenshot_and_attach_allure(driver, "Rename")
            with allure.step("Nhấn Áp dụng"):
                page_base.click_obj(Obj_Map.btnApDung)
                txt_xpath = ObjCommon.item_last_in_list(title_line)
                verify_rename_marker = page_base.check_element_visibility(txt_xpath)
                assert verify_rename_marker, "Đổi tên Đường không thành công"
            with allure.step("Load lại web - kiểm tra đường đã tạo"):
                driver.refresh()
                page_base.click_obj(Obj_Map.iconBanDoTacChien)
                txt_xpath = ObjCommon.item_last_in_list(title_line)
                verify_marker = page_base.check_element_visibility(txt_xpath)
                assert verify_marker, "Không lưu Đường đã vẽ"
                capture_screenshot_and_attach_allure(driver, "Verify")
        finally:
            with allure.step("Xóa đường đã tạo"):
                page_base.click_obj(ObjCommon.ellipsis_icon(title_line))
                page_base.click_obj(ObjCommon.option_menu("Xóa"))
                page_base.click_obj(Obj_Map.btnApDung)
                capture_screenshot_and_attach_allure(driver, "Delete")
            with allure.step("Load lại web - kiểm tra đường đã xóa"):
                driver.refresh()
                page_base.click_obj(Obj_Map.iconBanDoTacChien)
                txt_xpath = ObjCommon.item_last_in_list(title_line)
                verify_marker = page_base.check_element_visibility(txt_xpath, wait_time=1)
                assert not verify_marker, "Xóa đường không thành công"
                capture_screenshot_and_attach_allure(driver, "Verify")

    @allure.testcase("c4i2-1384", "c4i2-1384")
    @allure.epic("Khai thác bản đồ")
    @allure.feature("Bản đồ tác chiến")
    @allure.story("Đường")
    @allure.title("Xác minh có thể bật/tắt tìm kiếm nâng cao")
    @pff.parametrize(path=pathDataTestMap)
    def test_toggle_advanced_search_with_line(self, browser, title_line, radius, data_layer):
        """Trường hợp kiểm thử kiểm tra có thể bật và tắt tìm kiếm nâng cao với Đường trên bản đồ"""
        driver = browser
        page_base = PageBase(driver)
        time.sleep(1)
        page_base.show_overlay_text("Bật & Tắt Tìm kiếm nâng cao")

        try:
            with allure.step("Nhấn vào tính năng Bản đồ tác chiến"):
                page_base.click_obj(Obj_Map.iconBanDoTacChien)
                capture_screenshot_and_attach_allure(driver, "ClickBDTC")
                time.sleep(1)
            with allure.step("Nhấn vào button Đường"):
                page_base.click_obj(Obj_Map.iconDuong)
                capture_screenshot_and_attach_allure(driver, "ClickIcon")
                verify_icon = page_base.check_element_visibility(Obj_Map.verifyIconDuong)
                time.sleep(1)
                assert verify_icon, "Không có Highlight màu xanh khi chọn Đường"
            with allure.step("Nhấn vào Map - vẽ Đường"):
                page_base.click_multiple_positions([(800, 600), (800, 700), (800, 700)])
                capture_screenshot_and_attach_allure(driver, "Set")
            with allure.step("Đổi tên Đường"):
                page_base.click_obj(ObjCommon.ellipsis_icon("Đường"))
                page_base.click_obj(ObjCommon.option_menu("Đổi tên"))
                page_base.set_val_input(Obj_Map.itemRename, title_line)
                capture_screenshot_and_attach_allure(driver, "Rename")
            with allure.step("Nhấn Áp dụng"):
                page_base.click_obj(Obj_Map.btnApDung)
                txt_xpath = ObjCommon.item_last_in_list(title_line)
                verify_rename_marker = page_base.check_element_visibility(txt_xpath)
                assert verify_rename_marker, "Đổi tên Đường không thành công"
            with allure.step("Bật Tìm kiếm nâng cao"):
                page_base.click_obj(ObjCommon.ellipsis_icon(title_line))
                page_base.click_obj(ObjCommon.option_menu("Tìm kiếm nâng cao"))
            with allure.step("Thiết lập tìm kiếm nâng cao"):
                page_base.send_key_input(ObjCommon.search_textbox("Bán kính"), radius)
                page_base.click_obj(ObjCommon.search_textbox("Lớp dữ liệu"))
                page_base.send_key_input(Obj_Map.inputLopDuLieu, data_layer)
                time.sleep(2)
                page_base.click_obj(ObjCommon.checkbox_filter(data_layer))
                page_base.click_obj(Obj_Map.btnApDung)
            with allure.step("Kiểm tra kết quả trả về"):
                verify_results = page_base.check_element_visibility(Obj_Map.verifyResultsSearch)
                assert verify_results, f"Không có kết quả trả về từ tìm kiếm nâng cao, {data_layer}"
                value_results = page_base.get_text_element(Obj_Map.verifyResultsSearch)
                print(value_results)
                capture_screenshot_and_attach_allure(driver, "VerifyMarker")
            with allure.step("Tắt tìm kiếm nâng cao"):
                page_base.click_obj(Obj_Map.iconDelete)
                verify_search_advance = page_base.check_element_visibility(Obj_Map.verifyResultsSearch, wait_time=2)
                assert not verify_search_advance, "Không thể tắt tìm kiếm nâng cao"
        finally:
            with allure.step("Xóa đường đã tạo"):
                page_base.click_obj(ObjCommon.ellipsis_icon(title_line))
                page_base.click_obj(ObjCommon.option_menu("Xóa"))
                page_base.click_obj(Obj_Map.btnApDung)
                capture_screenshot_and_attach_allure(driver, "Delete")
            with allure.step("Load lại web - kiểm tra đường đã xóa"):
                driver.refresh()
                page_base.click_obj(Obj_Map.iconBanDoTacChien)
                txt_xpath = ObjCommon.item_last_in_list(title_line)
                verify_marker = page_base.check_element_visibility(txt_xpath, wait_time=1)
                assert not verify_marker, "Xóa đường không thành công"
                capture_screenshot_and_attach_allure(driver, "Verify")

    @allure.testcase("c4i2-270", "c4i2-270")
    @allure.testcase("c4i2-274", "c4i2-274")
    @allure.epic("Khai thác bản đồ")
    @allure.feature("Bản đồ tác chiến")
    @allure.story("Vùng")
    @allure.title("Xác minh có thể tạo và xóa vùng thành công")
    @pff.parametrize(path=pathDataTestMap)
    def test_create_and_delete_area_successfully(self, browser, title_area):
        """Trường hợp kiểm thử kiểm tra có thể tạo Điểm & xóa Vùng trên bản đồ"""
        driver = browser
        page_base = PageBase(driver)
        time.sleep(1)
        page_base.show_overlay_text("Tạo & Xóa Vùng")
        try:
            with allure.step("Nhấn vào tính năng Bản đồ tác chiến"):
                page_base.click_obj(Obj_Map.iconBanDoTacChien)
                capture_screenshot_and_attach_allure(driver, "ClickBDTC")
                time.sleep(1)
            with allure.step("Nhấn vào button Vùng"):
                page_base.click_obj(Obj_Map.iconVung)
                capture_screenshot_and_attach_allure(driver, "ClickIcon")
                verify_icon = page_base.check_element_visibility(Obj_Map.verifyIconVung)
                time.sleep(1)
                assert verify_icon, "Không có Highlight màu xanh khi chọn Đường"
            with allure.step("Nhấn vào Map - vẽ Vùng"):
                page_base.click_multiple_positions([(700, 300), (700, 500), (800, 400), (800, 400)])
                capture_screenshot_and_attach_allure(driver, "Set")
            with allure.step("Đổi tên Vùng"):
                page_base.click_obj(ObjCommon.ellipsis_icon("Vùng"))
                page_base.click_obj(ObjCommon.option_menu("Đổi tên"))
                page_base.set_val_input(Obj_Map.itemRename, title_area)
                capture_screenshot_and_attach_allure(driver, "Rename")
            with allure.step("Nhấn Áp dụng"):
                page_base.click_obj(Obj_Map.btnApDung)
                txt_xpath = ObjCommon.item_last_in_list(title_area)
                verify_rename_marker = page_base.check_element_visibility(txt_xpath)
                assert verify_rename_marker, "Đổi tên Vùng không thành công"
            with allure.step("Load lại web - kiểm tra vùng đã tạo"):
                driver.refresh()
                page_base.click_obj(Obj_Map.iconBanDoTacChien)
                txt_xpath = ObjCommon.item_last_in_list(title_area)
                verify_marker = page_base.check_element_visibility(txt_xpath)
                assert verify_marker, "Không lưu Vùng đã vẽ"
                capture_screenshot_and_attach_allure(driver, "Verify")
        finally:
            with allure.step("Xóa vùng đã tạo"):
                page_base.click_obj(ObjCommon.ellipsis_icon(title_area))
                page_base.click_obj(ObjCommon.option_menu("Xóa"))
                page_base.click_obj(Obj_Map.btnApDung)
                capture_screenshot_and_attach_allure(driver, "Delete")
            with allure.step("Load lại web - kiểm tra vùng đã xóa"):
                driver.refresh()
                page_base.click_obj(Obj_Map.iconBanDoTacChien)
                txt_xpath = ObjCommon.item_last_in_list(title_area)
                verify_marker = page_base.check_element_visibility(txt_xpath, wait_time=1)
                assert not verify_marker, "Xóa vùng không thành công"
                capture_screenshot_and_attach_allure(driver, "Verify")

    @allure.testcase("c4i2-1389", "c4i2-1389")
    @allure.epic("Khai thác bản đồ")
    @allure.feature("Bản đồ tác chiến")
    @allure.story("Vùng")
    @allure.title("Xác minh có thể bật/tắt tìm kiếm nâng cao")
    @pff.parametrize(path=pathDataTestMap)
    def test_toggle_advanced_search_with_area(self, browser, title_area, data_layer):
        """Trường hợp kiểm thử kiểm tra có thể bật và tắt tìm kiếm nâng cao với Vùng trên bản đồ"""
        driver = browser
        page_base = PageBase(driver)
        time.sleep(1)
        page_base.show_overlay_text("Tạo & Xóa Vùng")

        # di chuyển map đến vị trí marker
        time.sleep(2)
        start_position = (900, 400)
        end_position = (500, 400)
        for _ in range(5):
            page_base.drag_map(start_position[0], start_position[1], end_position[0], end_position[1])

        try:
            with allure.step("Nhấn vào tính năng Bản đồ tác chiến"):
                page_base.click_obj(Obj_Map.iconBanDoTacChien)
                capture_screenshot_and_attach_allure(driver, "ClickBDTC")
                time.sleep(1)
            with allure.step("Nhấn vào button Vùng"):
                page_base.click_obj(Obj_Map.iconVung)
                capture_screenshot_and_attach_allure(driver, "ClickIcon")
                verify_icon = page_base.check_element_visibility(Obj_Map.verifyIconVung)
                time.sleep(1)
                assert verify_icon, "Không có Highlight màu xanh khi chọn Đường"
            with allure.step("Nhấn vào Map - vẽ Vùng"):
                page_base.click_multiple_positions([(500, 300), (500, 600), (1000, 300), (1000, 300)])
                capture_screenshot_and_attach_allure(driver, "Set")
            with allure.step("Đổi tên Vùng"):
                page_base.click_obj(ObjCommon.ellipsis_icon("Vùng"))
                page_base.click_obj(ObjCommon.option_menu("Đổi tên"))
                page_base.set_val_input(Obj_Map.itemRename, title_area)
                capture_screenshot_and_attach_allure(driver, "Rename")
            with allure.step("Nhấn Áp dụng"):
                page_base.click_obj(Obj_Map.btnApDung)
                txt_xpath = ObjCommon.item_last_in_list(title_area)
                verify_rename_marker = page_base.check_element_visibility(txt_xpath)
                assert verify_rename_marker, "Đổi tên Vùng không thành công"
            with allure.step("Bật Tìm kiếm nâng cao"):
                page_base.click_obj(ObjCommon.ellipsis_icon(title_area))
                page_base.click_obj(ObjCommon.option_menu("Tìm kiếm nâng cao"))
            with allure.step("Thiết lập tìm kiếm nâng cao"):
                page_base.click_obj(ObjCommon.search_textbox("Lớp dữ liệu"))
                page_base.send_key_input(Obj_Map.inputLopDuLieu, data_layer)
                time.sleep(2)
                page_base.click_obj(ObjCommon.checkbox_filter(data_layer))
                page_base.click_obj(Obj_Map.btnApDung)
            with allure.step("Kiểm tra kết quả trả về"):
                verify_results = page_base.check_element_visibility(Obj_Map.verifyResultsSearch)
                assert verify_results, f"Không có kết quả trả về từ tìm kiếm nâng cao, {data_layer}"
                value_results = page_base.get_text_element(Obj_Map.verifyResultsSearch)
                print(value_results)
            with allure.step("Tắt tìm kiếm nâng cao"):
                page_base.click_obj(Obj_Map.iconDelete)
                verify_search_advance = page_base.check_element_visibility(Obj_Map.verifyResultsSearch, wait_time=2)
                assert not verify_search_advance, "Không thể tắt tìm kiếm nâng cao"
        finally:
            with allure.step("Xóa vùng đã tạo"):
                page_base.click_obj(ObjCommon.ellipsis_icon(title_area))
                page_base.click_obj(ObjCommon.option_menu("Xóa"))
                page_base.click_obj(Obj_Map.btnApDung)
                capture_screenshot_and_attach_allure(driver, "Delete")
            with allure.step("Load lại web - kiểm tra vùng đã xóa"):
                driver.refresh()
                page_base.click_obj(Obj_Map.iconBanDoTacChien)
                txt_xpath = ObjCommon.item_last_in_list(title_area)
                verify_marker = page_base.check_element_visibility(txt_xpath, wait_time=1)
                assert not verify_marker, "Xóa vùng không thành công"
                capture_screenshot_and_attach_allure(driver, "Verify")


@pytest.mark.DC
class Test_TaiNguyenVaTinhNang:
    pageBase = PageBase(browser)
    pathDataTestMap = pageBase.load_path_data_file_from_path("Datas_Map",
                                                             "Test_Map.json")

    @allure.testcase("c4i2-214", "c4i2-214")
    @allure.epic("Khai thác bản đồ")
    @allure.feature("Tài nguyên và tính năng")
    @allure.title("Xác minh có thể bật/tắt layer BẢN ĐỒ ĐIỆN TỬ")
    @pff.parametrize(path=pathDataTestMap)
    def test_verify_toggle_electronic_map_layer(self, browser, layer_name, location):
        """Trường hợp kiểm thử kiểm tra có thể bật/tắt layer BẢN ĐỒ ĐIỆN TỬ"""
        driver = browser
        page_base = PageBase(driver)
        time.sleep(1)
        page_base.show_overlay_text("bật/tắt layer BẢN ĐỒ ĐIỆN TỬ")
        try:
            with allure.step("Nhấn vào tính năng Tài nguyên và tính năng"):
                page_base.click_obj(Obj_Map.iconTaiNguyenVaTinhNanng)
                capture_screenshot_and_attach_allure(driver, "ClickTN&TN")
                time.sleep(1)
            with allure.step("Tick vào checkbox layer"):
                page_base.click_obj(ObjCommon.checkbox_button(layer_name))
                capture_screenshot_and_attach_allure(driver, "ClickIcon")
                verify_icon_nhan = page_base.verify_checkbox_checked(ObjCommon.checkbox_button(layer_name))
                time.sleep(1)
                assert verify_icon_nhan, f"Không thể checkbox của layer {layer_name}"
            with allure.step("Điều hướng đến vị trí có marker"):
                with allure.step("Nhấn vào icon Tìm Vị trí"):
                    page_base.click_obj(Obj_Map.iconTimViTri)
                    capture_screenshot_and_attach_allure(driver, "IconSearchLocation")
                    time.sleep(1)
                with allure.step("Nhập và tìm vị trí"):
                    page_base.send_key_input(Obj_Map.inputSearchLocation, location)
                    capture_screenshot_and_attach_allure(driver, "SetLocation")
                    time.sleep(1)
                    page_base.click_obj(Obj_Map.suggestOne)
                    page_base.click_obj(Obj_Map.iconTimViTri)
            with allure.step("Kiểm tra marker trên map"):
                verify_icon_video = page_base.check_element_visibility(Obj_Map.markerVideo)
                assert verify_icon_video, f"Không hiển thị marker trên map với layer {layer_name}"
                count_number = page_base.count_elements_by_xpath(Obj_Map.markerVideo)
                print(f"Layer {layer_name} có: {count_number} marker")
                capture_screenshot_and_attach_allure(driver, "ViewMarker")
        finally:
            with allure.step("Bỏ chọn layer"):
                page_base.click_obj(ObjCommon.checkbox_button(layer_name))
                capture_screenshot_and_attach_allure(driver, "ClickIcon")
                verify_icon_nhan = page_base.verify_checkbox_checked(ObjCommon.checkbox_button(layer_name))
                time.sleep(1)
                assert not verify_icon_nhan, f"Không thể bỏ chọn layer {layer_name}"

    @allure.testcase("c4i2-217", "c4i2-217")
    @allure.testcase("c4i2-216", "c4i2-216")
    @allure.testcase("c4i2-215", "c4i2-215")
    @allure.epic("Khai thác bản đồ")
    @allure.feature("Tài nguyên và tính năng")
    @allure.title("Xác minh có thể bật/tắt layer")
    @pff.parametrize(path=pathDataTestMap)
    def test_verify_toggle_data_layer(self, browser, layer_name, location, image_name):
        """Trường hợp kiểm thử kiểm tra có thể bật/tắt layer DỮ LIỆU TÍCH HỢP, DỮ LIỆU CHUYÊN NGÀNH, VỊ TRÍ CAMERA"""
        driver = browser
        page_base = PageBase(driver)
        time.sleep(1)
        page_base.show_overlay_text("bật/tắt layer")
        try:
            with allure.step("Nhấn vào tính năng Tài nguyên và tính năng"):
                page_base.click_obj(Obj_Map.iconTaiNguyenVaTinhNanng)
                capture_screenshot_and_attach_allure(driver, "ClickTN&TN")
                time.sleep(1)
            with allure.step("Tick vào checkbox layer"):
                page_base.do_scroll_mouse_to_element(ObjCommon.checkbox_button(layer_name))
                page_base.click_obj(ObjCommon.checkbox_button(layer_name))
                capture_screenshot_and_attach_allure(driver, "ClickIcon")
                verify_icon_nhan = page_base.verify_checkbox_checked(ObjCommon.checkbox_button(layer_name))
                time.sleep(1)
                assert verify_icon_nhan, f"Không thể checkbox của layer {layer_name}"
            with allure.step("Điều hướng đến vị trí có marker"):
                with allure.step("Nhấn vào icon Tìm Vị trí"):
                    page_base.click_obj(Obj_Map.iconTimViTri)
                    time.sleep(1)
                with allure.step("Nhập và tìm vị trí"):
                    page_base.send_key_input(Obj_Map.inputSearchLocation, location)
                    time.sleep(1)
                    page_base.click_obj(Obj_Map.suggestOne)
                    page_base.click_obj(Obj_Map.iconTimViTri)
                with allure.step("Kiểm tra có popup xuất hiện vị trí trên map"):
                    verify = page_base.check_element_visibility(Obj_Map.popupViTriHienTai)
                    time.sleep(1)
                    assert verify, "Không hiển thị dữ liệu trên bản đồ"
            with allure.step("Kiểm tra marker trên map"):
                verify_icon = page_base.check_image_visibility(image_name)
                assert verify_icon, f"Không hiển thị marker trên map với layer {layer_name}"
                capture_screenshot_and_attach_allure(driver, "ViewMarker")
        finally:
            with allure.step("Bỏ chọn layer"):
                page_base.click_obj(ObjCommon.checkbox_button(layer_name))
                capture_screenshot_and_attach_allure(driver, "ClickIcon")
                verify_icon_nhan = page_base.verify_checkbox_checked(ObjCommon.checkbox_button(layer_name))
                time.sleep(1)
                assert not verify_icon_nhan, f"Không thể bỏ chọn layer {layer_name}"

    @allure.testcase("c4i2-218", "c4i2-218")
    @allure.epic("Khai thác bản đồ")
    @allure.feature("Tài nguyên và tính năng")
    @allure.title("Xác minh hiển thị chi tiết khi click vào marker hiển thị trên map")
    @pff.parametrize(path=pathDataTestMap)
    def test_verify_details_displayed_on_marker_click(self, browser, layer_name, location, image_name):
        """Trường hợp kiểm thử kiểm tra hiển thị thông tin chi tiết nhấn vào marker"""
        driver = browser
        page_base = PageBase(driver)
        time.sleep(1)
        page_base.show_overlay_text("bật/tắt layer")
        try:
            with allure.step("Nhấn vào tính năng Tài nguyên và tính năng"):
                page_base.click_obj(Obj_Map.iconTaiNguyenVaTinhNanng)
                capture_screenshot_and_attach_allure(driver, "ClickTN&TN")
                time.sleep(1)
            with allure.step("Tick vào checkbox layer"):
                page_base.do_scroll_mouse_to_element(ObjCommon.checkbox_button(layer_name))
                page_base.click_obj(ObjCommon.checkbox_button(layer_name))
                capture_screenshot_and_attach_allure(driver, "ClickIcon")
                verify_icon_nhan = page_base.verify_checkbox_checked(ObjCommon.checkbox_button(layer_name))
                time.sleep(1)
                assert verify_icon_nhan, f"Không thể checkbox của layer {layer_name}"
            with allure.step("Điều hướng đến vị trí có marker"):
                with allure.step("Nhấn vào icon Tìm Vị trí"):
                    page_base.click_obj(Obj_Map.iconTimViTri)
                    time.sleep(1)
                with allure.step("Nhập và tìm vị trí"):
                    page_base.send_key_input(Obj_Map.inputSearchLocation, location)
                    time.sleep(1)
                    page_base.click_obj(Obj_Map.suggestOne)
                    page_base.click_obj(Obj_Map.iconTimViTri)
                with allure.step("Kiểm tra có popup xuất hiện vị trí trên map"):
                    verify = page_base.check_element_visibility(Obj_Map.popupViTriHienTai)
                    time.sleep(1)
                    assert verify, "Không hiển thị dữ liệu trên bản đồ"
                    page_base.click_obj(Obj_Map.iconClosePopupViTriHienTai)
            with allure.step("Kiểm tra marker trên map"):
                verify_icon = page_base.check_image_visibility(image_name)
                assert verify_icon, f"Không hiển thị marker trên map với layer {layer_name}"
                capture_screenshot_and_attach_allure(driver, "ViewMarker")
            with allure.step("Nhấn vào marker"):
                page_base.click_center_image(image_name)
                time.sleep(2)
                verify = page_base.check_element_visibility(Obj_Map.popupViTriHienTai)
                assert verify, "Không hiển thị popup thông tin marker"
        finally:
            with allure.step("Bỏ chọn layer"):
                page_base.click_obj(ObjCommon.checkbox_button(layer_name))
                capture_screenshot_and_attach_allure(driver, "ClickIcon")
                verify_icon_nhan = page_base.verify_checkbox_checked(ObjCommon.checkbox_button(layer_name))
                time.sleep(1)
                assert not verify_icon_nhan, f"Không thể bỏ chọn layer {layer_name}"


@pytest.mark.DC
class Test_LoaiBanDo:
    pageBase = PageBase(browser)
    pathDataTestMap = pageBase.load_path_data_file_from_path("Datas_Map",
                                                             "Test_Map.json")

    @allure.testcase("c4i2-172", "c4i2-172")
    @allure.epic("Khai thác bản đồ")
    @allure.feature("Loại bản đồ")
    @allure.title("Xác minh có thể thay đổi base map")
    @pff.parametrize(path=pathDataTestMap)
    def test_verify_base_map_can_be_changed(self, browser, overlay_name, location, image_name):
        """Trường hợp kiểm thử kiểm tra có thể thay đổi base map trên bản đồ"""
        driver = browser
        page_base = PageBase(driver)
        time.sleep(1)
        page_base.show_overlay_text("Kiểm tra lớp bản đồ")
        with allure.step("Nhấn vào tính năng Loại bản đồ"):
            page_base.click_obj(Obj_Map.iconLoaiBanDo)
            capture_screenshot_and_attach_allure(driver, "ClickLBD")
            time.sleep(1)
        with allure.step("Chọn lớp bản đồ mong muốn"):
            page_base.click_obj(ObjCommon.switcher_button(overlay_name))
            capture_screenshot_and_attach_allure(driver, "ClickIcon")
            verify_icon_nhan = page_base.verify_checkbox_checked(ObjCommon.switcher_button(overlay_name))
            time.sleep(1)
            assert verify_icon_nhan, f"Không thể lựa chọn lớp bản đồ: {overlay_name}"
            page_base.click_obj(Obj_Map.iconLoaiBanDo)
        with allure.step("Điều hướng đến vị trí có có thể kiểm tra"):
            with allure.step("Nhấn vào icon Tìm Vị trí"):
                page_base.click_obj(Obj_Map.iconTimViTri)
                time.sleep(1)
            with allure.step("Nhập và tìm vị trí"):
                page_base.send_key_input(Obj_Map.inputSearchLocation, location)
                time.sleep(1)
                page_base.click_obj(Obj_Map.suggestOne)
            with allure.step("Kiểm tra có popup xuất hiện vị trí trên map"):
                verify = page_base.check_element_visibility(Obj_Map.popupViTriHienTai)
                time.sleep(1)
                assert verify, "Không hiển thị dữ liệu trên bản đồ"
        with allure.step("Kiểm tra lớp trên map"):
            verify_overlay = page_base.check_image_visibility(image_name)
            assert verify_overlay, f"Lớp bản đồ chưa thay đổi: {overlay_name}"
