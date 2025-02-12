import time
import pytest
import allure

from Libraries.Framework.FactoryDrivers import get_chrome_driver
from Libraries.Framework.Utils import PageBase
from Libraries.Config import Default
from PageObjects.Web.Obj_BienSo import Obj_BienSo
from PageObjects.Web.Obj_Common import ObjCommon
from WebApplications.PageCommon import PageCommon
from WebApplications.PageHome import LoginPage
from WebApplications.PageBienSoXe import PageBienSoXe
from conftest import capture_screenshot_and_attach_allure, attach_table_to_allure
import parametrize_from_file as pff
from Libraries.Plugins.DataHandler import JsonDataHandler


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
    page_base.click_obj(Obj_BienSo.tabThuVien)
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


@pytest.fixture(scope='function')
def create_data(browser, Data):
    driver = browser
    page_base = PageBase(driver)
    page_bien_so_xe = PageBienSoXe(driver)

    page_base.click_obj(Obj_BienSo.btnThemMoiBSX)
    page_bien_so_xe.do_dien_thong_tin_bsx(Data)
    page_base.click_obj(Obj_BienSo.btnLuuThemMoi)
    time.sleep(2)
    yield


@pytest.fixture(scope='function')
def clean_data(browser, save_current_url, Data):
    yield
    driver = browser
    page_base = PageBase(driver)

    driver.get(save_current_url)
    time.sleep(1)
    bien_so_xe = Data[0]["Value"]
    page_base.send_key_input(Obj_BienSo.txtSearchBSX, bien_so_xe)
    page_base.click_obj(Obj_BienSo.btnTimKiem)

    time.sleep(3)
    page_base.click_obj(Obj_BienSo.checkboxBSX)
    time.sleep(2)
    page_base.click_obj(Obj_BienSo.btnDelete)
    time.sleep(2)
    page_base.click_obj(Obj_BienSo.btnXacNhan)
    time.sleep(2)


@allure.epic("Nhận dạng biển số xe")
@allure.feature("Thư viện BSX")
@pytest.mark.LPR
@pytest.mark.Add_DataList
@pytest.mark.LPRLib
class Test_Add_BSX:
    pageBase = PageBase(browser)
    pathDataTestLibraryLpr = pageBase.load_path_data_file_from_path("Datas_LPR",
                                                                    "Test_ThuVien_BSX.json")

    @pytest.mark.DC
    @pytest.mark.UAT_DC
    @allure.testcase("c4i2-503", "c4i2-503")
    @allure.story("Thêm mới BSX trong thư viện thành công")
    @allure.title("c4i2-503: Tạo với thông tin bắt buộc")
    @pff.parametrize(path=pathDataTestLibraryLpr)
    def test_AddBSXSuccess(self, browser, clean_data, Data):
        """Trường hợp kiểm thử tạo Biển số xe thành công"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_bien_so_xe = PageBienSoXe(driver)

        page_base.click_obj(Obj_BienSo.btnThemMoiBSX)
        time.sleep(1)
        page_base.show_overlay_text("Trường hợp kiểm thử tạo Biển số xe thành công")
        attach_table_to_allure(Data, "Data Test")

        json_data_handler = JsonDataHandler(Data)
        label_search = "Biển số xe"
        bien_so_xe = json_data_handler.get_value_by_label(label_search)
        with allure.step("Điền thông tin biển số xe"):
            page_bien_so_xe.do_dien_thong_tin_bsx(Data)
            capture_screenshot_and_attach_allure(driver, "FillInfo")
            time.sleep(2)
        with allure.step("Kiểm tra thông báo sau khi tạo thành công"):
            page_base.click_obj(Obj_BienSo.btnLuuThemMoi)
            time.sleep(2)
            allure.attach(driver.get_screenshot_as_png(), name="NotifySuccess",
                          attachment_type=allure.attachment_type.PNG)
            check_popup = page_common.verify_notify_popup('Thêm thành công')
            assert check_popup, "Tạo BSX không thành công"
        with allure.step("Tìm kiếm biển số xe đã thêm"):
            time.sleep(2)
            # bien_so_xe = Data[0]["Value"]
            page_base.send_key_input(Obj_BienSo.txtSearchBSX, bien_so_xe)
            page_base.click_obj(Obj_BienSo.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, "FindBSX")
            check_exit_in_pop_up = page_base.check_element_visibility(Obj_BienSo.iconEdit)
            assert check_exit_in_pop_up, "Không tìm thấy kết quả đã tạo trên danh sách lưới"

        with allure.step("Nhấn chỉnh sửa kết quả đầu tiên"):
            time.sleep(3)
            page_base.click_obj(Obj_BienSo.iconEdit)
            time.sleep(2)

        with allure.step("Kiểm tra kết quả đã tạo"):
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, "CheckResultCreated")
            check_result = page_common.verify_result_created(Data)
            assert check_result, "Dữ liệu đã thêm không hiển thị đầy đủ"

    @allure.testcase("c4i2-504", "c4i2-504")
    @allure.story("Thêm mới BSX trong thư viện không thành công")
    @allure.title(f"Tạo với biển số trùng")
    @pff.parametrize(path=pathDataTestLibraryLpr)
    def test_AddBSXUnSuccess_AddExitData(self, browser, create_data, clean_data, Data, desc):
        # Thêm mô tả vào allure
        description = f"Trường hợp kiểm thử tạo Biển số xe không thành công - dữ liệu đã tồn tại - {desc}"
        allure.dynamic.description(description)

        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_bien_so_xe = PageBienSoXe(driver)

        page_base.click_obj(Obj_BienSo.btnThemMoiBSX)
        time.sleep(1)
        page_base.show_overlay_text("Trường hợp kiểm thử tạo Biển số xe không thành công - dữ liệu đã tồn tại")
        attach_table_to_allure(Data, "Data Test")
        json_data_handler = JsonDataHandler(Data)
        label_search = "Biển số xe"
        bien_so_xe = json_data_handler.get_value_by_label(label_search)
        with allure.step("Điền thông tin biển số xe"):
            page_bien_so_xe.do_dien_thong_tin_bsx(Data)
            capture_screenshot_and_attach_allure(driver, "FillInfoToForm")
            time.sleep(2)

        with allure.step("Kiểm tra thông báo khi thêm BSX trùng"):
            page_base.click_obj(Obj_BienSo.btnLuuThemMoi)
            time.sleep(2)
            allure.attach(driver.get_screenshot_as_png(), name="NotifyUnSuccess",
                          attachment_type=allure.attachment_type.PNG)
            check_popup = page_common.verify_notify_popup('Biển số xe đã tồn tại trong hệ thống')
            assert check_popup, "Thông báo không hợp lệ"

        with allure.step("Tìm kiếm biển số xe đã thêm"):
            page_base.click_obj(Obj_BienSo.iconClosePopup)
            time.sleep(2)
            # bien_so_xe = Data[0]["Value"]
            page_base.send_key_input(Obj_BienSo.txtSearchBSX, bien_so_xe)
            page_base.click_obj(Obj_BienSo.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, "FindBSX")
            count_element = page_base.count_elements_by_xpath(Obj_BienSo.iconEdit)
            if count_element == 1:
                assert True
            else:
                assert False, "Kết quả trên danh sách lưới không đạt yêu cầu"

    @allure.testcase("c4i2-504", "c4i2-504")
    @allure.story("Thêm mới BSX trong thư viện không thành công")
    @allure.title("Tạo bỏ trống trường dữ liệu bắt buộc")
    @pff.parametrize(path=pathDataTestLibraryLpr)
    def test_AddBSXUnSuccess(self, browser, Data, desc):
        # Thêm mô tả vào allure
        description = f"Trường hợp kiểm thử tạo Biển số xe không thành công - {desc}"
        allure.dynamic.description(description)

        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_bien_so_xe = PageBienSoXe(driver)

        time.sleep(2)
        page_base.click_obj(Obj_BienSo.btnThemMoiBSX)
        time.sleep(1)
        page_base.show_overlay_text(
            "Trường hợp kiểm thử tạo Biển số xe không thành công - bỏ trống trường bắt buộc")
        attach_table_to_allure(Data, "Data Test")
        with allure.step("Điền thông tin biển số xe"):
            page_bien_so_xe.do_dien_thong_tin_bsx(Data)
            capture_screenshot_and_attach_allure(driver, "FillInfo")
            time.sleep(2)
        with allure.step("Kiểm tra có thể tạo mới dữ liệu hay không"):
            check_button = page_base.check_button_clickable(Obj_BienSo.btnLuuThemMoi)
            if check_button:
                page_base.click_obj(Obj_BienSo.btnLuuThemMoi)
                time.sleep(2)
                capture_screenshot_and_attach_allure(driver, "NotifyUnSuccess")
                check_popup = page_common.verify_notify_popup("Biển số không được để trống hoặc chỉ chứa khoảng trắng")
                assert check_popup, "Thông báo không chính xác"
            else:
                capture_screenshot_and_attach_allure(driver, "HideButton")
                assert True


@allure.epic("Nhận dạng biển số xe")
@allure.feature("Thư viện BSX")
@pytest.mark.LPR
@pytest.mark.Add_DataList
@pytest.mark.LPRLib
class Test_Edit_BSX:
    pageBase = PageBase(browser)
    pathDataTestLibraryLpr = pageBase.load_path_data_file_from_path("Datas_LPR",
                                                                    "Test_ThuVien_BSX.json")

    @pytest.mark.DC
    @pytest.mark.UAT_DC
    @allure.testcase("c4i2-510", "c4i2-510")
    @allure.story("Chỉnh sửa BSX trong thư viện thành công")
    @allure.title("c4i2-510: Chỉnh sửa thông tin biển số xe hợp lệ")
    @pff.parametrize(path=pathDataTestLibraryLpr)
    def test_EditBSXSuccess(self, browser, create_data, clean_data, Data, Data_Edit, desc):
        # Thêm mô tả vào allure
        description = f"Trường hợp kiểm thử chỉnh sửa Biển số xe thành công - {desc}"
        allure.dynamic.description(description)

        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_bien_so_xe = PageBienSoXe(driver)
        page_base.show_overlay_text("Trường hợp kiểm thử Chỉnh sửa BSX thành công")
        attach_table_to_allure(Data, "Pre-editing test data")
        attach_table_to_allure(Data_Edit, "Post-editing test data")
        json_data_handler = JsonDataHandler(Data)
        label_search = "Biển số xe"
        bien_so_xe = json_data_handler.get_value_by_label(label_search)
        with allure.step("Tìm kiếm BSX"):
            time.sleep(2)
            # bienSoXe = Data[0]["Value"]
            page_base.send_key_input(Obj_BienSo.txtSearchBSX, bien_so_xe)
            page_base.click_obj(Obj_BienSo.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, "SeachBSX")

        with allure.step("Nhấn chỉnh sửa kết quả tìm thấy trên danh sách lưới"):
            time.sleep(2)
            page_base.click_obj(Obj_BienSo.iconEdit)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, "ViewResultsBSX")

        with allure.step("Chỉnh sửa thông tin BSX"):
            page_bien_so_xe.do_dien_thong_tin_bsx(Data_Edit)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, "editBSX")
            page_base.click_obj(Obj_BienSo.btnCapNhatBSX)
            time.sleep(2)
            check_popup = page_common.verify_notify_popup('Cập nhật thành công')
            assert check_popup, "Chỉnh sửa BSX không thành công"

        with allure.step("Tìm kiếm BSX đã chỉnh sửa"):
            time.sleep(2)
            # bienSoXe = Data[0]["Value"]
            page_base.send_key_input(Obj_BienSo.txtSearchBSX, bien_so_xe)
            page_base.click_obj(Obj_BienSo.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, "FindBSX")
            check_exit_in_pop_up = page_base.check_element_visibility(Obj_BienSo.iconEdit)
            assert check_exit_in_pop_up, "Không tìm thấy kết quả đã chỉnh sửa trên danh sách lưới"

        with allure.step("Kiểm tra kết quả đã chỉnh sửa"):
            time.sleep(3)
            page_base.click_obj(Obj_BienSo.iconEdit)
            time.sleep(2)
            check_result = page_common.verify_result_created(Data_Edit)
            capture_screenshot_and_attach_allure(driver, "CheckResultEdited")
            assert check_result, "Dữ liệu đã thêm không hiển thị đầy đủ"

    @pytest.mark.UAT_DC
    @allure.testcase("c4i2-507", "c4i2-507")
    @allure.story("Chỉnh sửa BSX trong thư viện thành công")
    @allure.title("c4i2-507: Xác minh có thể thêm theo dõi cho biển số")
    @pff.parametrize(path=pathDataTestLibraryLpr)
    def test_AddTrackingIntoBSX(self, browser, create_data, Data, data_watchlist):
        """Trường hợp kiểm thử xác minh có thể thêm theo dõi cho biển số xe trong thư viện"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)

        time.sleep(1)
        page_base.show_overlay_text("Thêm theo dõi cho biển số")
        attach_table_to_allure(Data, "Data Test")
        json_data_handler = JsonDataHandler(Data)
        label_search = "Biển số xe"
        bien_so_xe = json_data_handler.get_value_by_label(label_search)
        with allure.step("Tìm kiếm biển số xe đã thêm"):
            time.sleep(1)
            # bien_so_xe = Data[0]["Value"]
            page_base.send_key_input(Obj_BienSo.txtSearchBSX, bien_so_xe)
            page_base.click_obj(Obj_BienSo.btnTimKiem)
            time.sleep(1)
            allure.attach(driver.get_screenshot_as_png(), name="FindBSX",
                          attachment_type=allure.attachment_type.PNG)
            check_exit_in_pop_up = page_base.check_element_visibility(Obj_BienSo.iconEdit)
            assert check_exit_in_pop_up, "Không tìm thấy kết quả đã tạo trên danh sách lưới"
        with allure.step("Nhấn chỉnh sửa kết quả đầu tiên"):
            time.sleep(1)
            page_base.click_obj(Obj_BienSo.iconEdit)
        with allure.step("Nhấn vào button 'Thêm theo dõi'"):
            time.sleep(1)
            page_base.do_scroll_mouse_to_element(Obj_BienSo.btnThemTheoDoi)
            time.sleep(1)
            page_base.click_obj(Obj_BienSo.btnThemTheoDoi)
            capture_screenshot_and_attach_allure(driver, "PopupAddTracking")
        with allure.step("Chọn loại theo dõi tại popup theo dõi"):
            time.sleep(1)
            dropdown_tracking = ObjCommon.dropdown_list("Theo dõi")
            page_base.select_key_dropdown(dropdown_tracking, data_watchlist)
            page_base.click_obj(ObjCommon.toggle_switch("Kích hoạt"))
            page_base.click_obj(ObjCommon.toggle_checkbox("Thời hạn"))
            capture_screenshot_and_attach_allure(driver, "SelectCamera")
        with allure.step("Nhấn vào button 'Xác nhận'"):
            time.sleep(1)
            page_base.click_obj(Obj_BienSo.btnXacNhan)
            capture_screenshot_and_attach_allure(driver, "UpdateTracking")
        with allure.step("Kiểm tra thông báo sau khi cập nhật theo dõi"):
            time.sleep(1)
            page_base.click_obj(Obj_BienSo.btnCapNhatBSX)
            time.sleep(1)
            allure.attach(driver.get_screenshot_as_png(), name="NotifyUnSuccess",
                          attachment_type=allure.attachment_type.PNG)
            check_popup = page_common.verify_notify_popup('Cập nhật thành công')
            assert check_popup, "Thông báo không hợp lệ"

    @pytest.mark.depends(on=['test_AddTrackingIntoBSX'])
    @pytest.mark.UAT_DC
    @allure.testcase("c4i2-511", "c4i2-511")
    @allure.story("Chỉnh sửa BSX trong thư viện thành công")
    @allure.title("c4i2-511: Xác minh có thể xóa theo dõi cho biển số")
    @pff.parametrize(path=pathDataTestLibraryLpr, key="test_AddTrackingIntoBSX")
    def test_DeleteTrackingIntoBSX(self, browser, clean_data, Data, data_watchlist):
        # Thêm mô tả vào allure
        description = f"Trường hợp kiểm thử có thể xóa Thông tin theo dõi đã thêm vào Biển số xe - {data_watchlist}"
        allure.dynamic.description(description)

        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)

        time.sleep(1)
        page_base.show_overlay_text("Xóa theo dõi biển số xe")
        attach_table_to_allure(Data, "Data Test")
        json_data_handler = JsonDataHandler(Data)
        label_search = "Biển số xe"
        bien_so_xe = json_data_handler.get_value_by_label(label_search)
        with allure.step("Tìm kiếm biển số xe đã thêm"):
            time.sleep(1)
            # bien_so_xe = Data[0]["Value"]
            page_base.send_key_input(Obj_BienSo.txtSearchBSX, bien_so_xe)
            page_base.click_obj(Obj_BienSo.btnTimKiem)
            time.sleep(1)
            allure.attach(driver.get_screenshot_as_png(), name="FindBSX",
                          attachment_type=allure.attachment_type.PNG)
            check_exit_in_pop_up = page_base.check_element_visibility(Obj_BienSo.iconEdit)
            assert check_exit_in_pop_up, "Không tìm thấy kết quả đã tạo trên danh sách lưới"
        with allure.step("Nhấn chỉnh sửa kết quả đầu tiên"):
            time.sleep(1)
            page_base.click_obj(Obj_BienSo.iconEdit)
        with allure.step("Nhấn vào icon 'Xóa' thông tin theo dõi"):
            page_base.click_obj(Obj_BienSo.iconDeleteTracking)
            time.sleep(1)
            page_base.click_obj(Obj_BienSo.btnXacNhan)
            capture_screenshot_and_attach_allure(driver, "DeleteTracking")
        with allure.step("Kiểm tra thông báo sau khi cập nhật xóa theo dõi"):
            time.sleep(1)
            page_base.click_obj(Obj_BienSo.btnCapNhatBSX)
            time.sleep(1)
            allure.attach(driver.get_screenshot_as_png(), name="NotifyUnSuccess",
                          attachment_type=allure.attachment_type.PNG)
            check_popup = page_common.verify_notify_popup('Cập nhật thành công')
            assert check_popup, "Thông báo không hợp lệ"


@allure.epic("Nhận dạng biển số xe")
@allure.feature("Thư viện BSX")
@pytest.mark.LPR
@pytest.mark.Add_DataList
@pytest.mark.LPRLib
class Test_Delete_BSX:
    pageBase = PageBase(browser)
    pathDataTestLibraryLpr = pageBase.load_path_data_file_from_path("Datas_LPR",
                                                                    "Test_ThuVien_BSX.json")

    @pytest.mark.DC
    @pytest.mark.UAT_DC
    @allure.testcase("c4i2-509", "c4i2-509")
    @allure.story("Xóa BSX trong thư viện thành công")
    @allure.title("c4i2-509: Nhấn Xác nhận xóa BSX")
    @pff.parametrize(path=pathDataTestLibraryLpr, key="test_DeleteBSX")
    def test_DeleteBSXSuccess(self, browser, create_data, Data):
        """Trường hợp kiểm thử xóa Biển số xe đã tạo thành công"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_base.show_overlay_text("Trường hợp kiểm thử xóa Biển số xe đã tạo thành công")
        attach_table_to_allure(Data, "Data Test")
        json_data_handler = JsonDataHandler(Data)
        label_search = "Biển số xe"
        bien_so_xe = json_data_handler.get_value_by_label(label_search)
        with allure.step("Tim kiếm BSX muốn xóa"):
            time.sleep(2)
            # bien_so_xe = Data[0]["Value"]
            page_base.send_key_input(Obj_BienSo.txtSearchBSX, bien_so_xe)
            page_base.click_obj(Obj_BienSo.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, "SearchBSX")

        with allure.step("Tick kết quả đầu tiên"):
            time.sleep(3)
            page_base.click_obj(Obj_BienSo.checkboxBSX)
            time.sleep(2)
            allure.attach(driver.get_screenshot_as_png(), name="CheckResultBSX",
                          attachment_type=allure.attachment_type.PNG)

        with allure.step("Nhấn xóa"):
            page_base.click_obj(Obj_BienSo.btnDelete)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, "DeleteBSX")

        with allure.step("Xác nhận xóa"):
            page_base.click_obj(Obj_BienSo.btnXacNhan)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, "ConfirmDeleteBSX")
            check_popup = page_common.verify_notify_popup('Xóa thành công')
            assert check_popup, "Xóa BSX không thành công"

    @allure.testcase("c4i2-509", "c4i2-509")
    @allure.story("Xóa BSX trong thư viện không thành công")
    @allure.title("Nhấn Hủy xóa BSX")
    @pff.parametrize(path=pathDataTestLibraryLpr, key="test_DeleteBSX")
    def test_DeleteBSXUnSuccess(self, browser, create_data, clean_data, Data):
        """Trường hợp kiểm thử xóa Biển số xe không thành công khi nhấn Cancel Delete"""
        driver = browser
        page_base = PageBase(driver)
        page_base.show_overlay_text("Trường hợp kiểm thử xóa Biển số xe không thành công - nhấn Cancel Delete")
        attach_table_to_allure(Data, "Data Test")
        json_data_handler = JsonDataHandler(Data)
        label_search = "Biển số xe"
        bien_so_xe = json_data_handler.get_value_by_label(label_search)
        with allure.step("Tim kiếm BSX muốn xóa"):
            time.sleep(2)
            # bien_so_xe = Data[0]["Value"]
            page_base.send_key_input(Obj_BienSo.txtSearchBSX, bien_so_xe)
            page_base.click_obj(Obj_BienSo.btnTimKiem)
            allure.attach(driver.get_screenshot_as_png(), name="TimBSX", attachment_type=allure.attachment_type.PNG)

        with allure.step("Tick kết quả đầu tiên"):
            time.sleep(3)
            page_base.click_obj(Obj_BienSo.checkboxBSX)
            time.sleep(2)
            allure.attach(driver.get_screenshot_as_png(), name="CheckResultBSX",
                          attachment_type=allure.attachment_type.PNG)

        with allure.step("Nhấn xóa"):
            page_base.click_obj(Obj_BienSo.btnDelete)
            time.sleep(2)
            allure.attach(driver.get_screenshot_as_png(), name="DeleteBSX", attachment_type=allure.attachment_type.PNG)

        with allure.step("Nhấn Hủy"):
            page_base.click_obj(Obj_BienSo.btnHuy)
            time.sleep(2)
            allure.attach(driver.get_screenshot_as_png(), name="CancelDelete",
                          attachment_type=allure.attachment_type.PNG)
        with allure.step("Tìm kiếm biển số xe đã thêm"):
            time.sleep(2)
            # bien_so_xe = Data[0]["Value"]
            page_base.send_key_input(Obj_BienSo.txtSearchBSX, bien_so_xe)
            page_base.click_obj(Obj_BienSo.btnTimKiem)
            time.sleep(2)
            allure.attach(driver.get_screenshot_as_png(), name="FindBSX", attachment_type=allure.attachment_type.PNG)
            check_exit_in_pop_up = page_base.check_element_visibility(Obj_BienSo.iconEdit)
            assert check_exit_in_pop_up, "Không tìm thấy kết quả đã tạo trên danh sách lưới"


@allure.epic("Nhận dạng biển số xe")
@allure.feature("Thư viện BSX")
@pytest.mark.LPR
@pytest.mark.Add_DataList
@pytest.mark.LPRLib
class Test_Search_BSX:
    pageBase = PageBase(browser)
    pathDataTestLibraryLpr = pageBase.load_path_data_file_from_path("Datas_LPR",
                                                                    "Test_ThuVien_BSX.json")

    @allure.testcase("c4i2-496", "c4i2-496")
    @allure.testcase("c4i2-497", "c4i2-497")
    @allure.testcase("c4i2-498", "c4i2-498")
    @allure.testcase("c4i2-499", "c4i2-499")
    @allure.story("Tìm kiếm BSX trong thư viện thành công")
    @allure.title("Tìm kiếm BSX theo 1 thuộc tính")
    @pff.parametrize(path=pathDataTestLibraryLpr)
    def test_SearchSingleBSX(self, browser, create_data, clean_data, Data, Data_Search, desc):
        # Thêm mô tả vào allure
        description = f"Trường hợp kiểm thử tìm BSX thành công - tab Thư viện - Search {desc}"
        allure.dynamic.description(description)

        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_base.show_overlay_text("Trường hợp kiểm thử tìm BSX thành công - tab Thư viện")
        attach_table_to_allure(Data, "Data Test")
        attach_table_to_allure(Data_Search, "Search Data")
        with allure.step("Nhập thông tin BSX vào tab Tìm kiếm"):
            time.sleep(2)
            value_bsx = Data_Search[0]["Value"]
            label_bsx = Data_Search[0]["Label"]
            txt_search_bsx = ObjCommon.search_textbox(label_bsx)
            page_base.send_key_input(txt_search_bsx, value_bsx)
            capture_screenshot_and_attach_allure(driver, "SearchBSX")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_BienSo.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, "PressButtonSearch")
        with allure.step("Kiểm tra kết quả tìm kiếm có xuất hiện trên grid hay không"):
            txt_input = '//div[@cellid]'
            check_exit_in_grid = page_common.check_element_visibility(txt_input)
            assert check_exit_in_grid, "Không tìm thấy kết quả đã tạo trên danh sách lưới"
        with allure.step("Kiểm tra kết quả tìm kiếm có chính xác là kết quả đã search hay không"):
            time.sleep(3)
            json_data_handler = JsonDataHandler(Data)
            label_search = "Biển số xe"
            bien_so_xe = json_data_handler.get_value_by_label(label_search)
            # bien_so_xe = Data[0]["Value"]
            icon_edit = ObjCommon.edit_icon(bien_so_xe)
            page_base.click_obj(icon_edit)
            time.sleep(2)
            check_result = page_common.verify_result_created(Data_Search)
            capture_screenshot_and_attach_allure(driver, "CheckResultSearch")
            assert check_result, "Dữ liệu xuất hiện không phải là dữ liệu đang tìm kiếm"

    @allure.testcase("c4i2-502", "c4i2-502")
    @allure.story("Tìm kiếm BSX trong thư viện thành công")
    @allure.title("Tìm kiếm BSX kết hợp nhiều thuộc tính")
    @pff.parametrize(path=pathDataTestLibraryLpr)
    def test_SearchCombinedBSX(self, browser, create_data, clean_data, Data, Data_Search, desc):
        # Search kết hợp ngẫu nhiên 2 giá trị
        import random
        random_indexes = random.sample([0, 1, 2, 3], 2)
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_base.show_overlay_text("Trường hợp kiểm thử tìm BSX thành công - tab Thư viện")
        attach_table_to_allure(Data, "Data Test")
        attach_table_to_allure(Data_Search, "Search Data")
        with allure.step("Nhập thông tin BSX vào tab Tìm kiếm"):
            # Khởi tạo danh sách để lưu trữ giá trị value_bsx và label_bsx
            value_bsx_list = []
            label_bsx_list = []
            for random_index in random_indexes:
                time.sleep(2)
                value_bsx = Data_Search[random_index]["Value"]
                label_bsx = Data_Search[random_index]["Label"]
                txt_search_bsx = ObjCommon.search_textbox(label_bsx)
                page_base.send_key_input(txt_search_bsx, value_bsx)

                # Thêm giá trị value_bsx và label_bsx vào danh sách
                value_bsx_list.append(value_bsx)
                label_bsx_list.append(label_bsx)

            capture_screenshot_and_attach_allure(driver, "SearchBSX")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_BienSo.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, "PressButtonSearch")
        with allure.step("Kiểm tra kết quả tìm kiếm có xuất hiện trên grid hay không"):
            txt_input = '//div[@cellid]'
            check_exit_in_grid = page_common.check_element_visibility(txt_input)
            assert check_exit_in_grid, "Không tìm thấy kết quả đã tạo trên danh sách lưới"
        with allure.step("Kiểm tra kết quả tìm kiếm có chính xác là kết quả đã search hay không"):
            time.sleep(3)
            json_data_handler = JsonDataHandler(Data)
            label_search = "Biển số xe"
            bien_so_xe = json_data_handler.get_value_by_label(label_search)
            # bien_so_xe = Data_Search[0]["Value"]
            icon_edit = ObjCommon.edit_icon(bien_so_xe)
            page_base.click_obj(icon_edit)
            time.sleep(2)
            check_result = page_common.verify_result_created(Data)
            capture_screenshot_and_attach_allure(driver, "CheckResultSearch")
            assert check_result, "Dữ liệu tìm thấy không phải là dữ liệu đang tìm kiếm"
            # Thêm mô tả vào allure
            description = f"Trường hợp kiểm thử tìm BSX thành công - tab Thư viện - Search {desc} - {', '.join(label_bsx_list)}"
            allure.dynamic.description(description)
