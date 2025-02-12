import time
import pytest
import allure

from Libraries.Framework.FactoryDrivers import get_chrome_driver
from Libraries.Framework.Utils import PageBase
from Libraries.Config import Default
from PageObjects.Web.Obj_Common import ObjCommon
from PageObjects.Web.Obj_VuViec import Obj_VuViec
from WebApplications.PageCommon import PageCommon, FillData
from WebApplications.PageHome import LoginPage
from WebApplications.PageVuViec import CaseManagement
from conftest import capture_screenshot_and_attach_allure, attach_table_to_allure
import parametrize_from_file as pff
from Libraries.Plugins.DataHandler import JsonDataHandler


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
    page_base = PageBase(driver)
    driver.get(url)
    page_login.do_login(username, password)
    page_login.click_obj(Obj_VuViec.iconVuViec)
    page_base.click_obj(Obj_VuViec.tabVuViec)
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


pageBase = PageBase(browser)
pathDataTestCase = pageBase.load_path_data_file_from_path("Datas_Case",
                                                     "Test_VuViec.json")


@pytest.fixture(scope='function')
def create_data(browser, Data):
    driver = browser
    page_base = PageBase(driver)
    page_guong_mat = CaseManagement(driver)

    page_base.click_obj(Obj_VuViec.btnTaoVuViec)
    page_guong_mat.do_dien_thong_tin_vu_viec(Data)
    page_base.click_obj(Obj_VuViec.btnSubmitVuViec)
    time.sleep(2)
    yield


@pytest.fixture(scope='function')
def clean_data(browser, save_current_url, Data):
    yield
    driver = browser
    page_base = PageBase(driver)
    json_data_handler = JsonDataHandler(Data)

    driver.get(save_current_url)
    time.sleep(3)
    # Kiểm tra danh sách đã load xong
    page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
    ten_vu_viec = json_data_handler.get_value_by_label("Tên vụ việc")
    page_base.send_key_input(Obj_VuViec.txtSearchVuViec, ten_vu_viec)
    page_base.click_obj(Obj_VuViec.btnTimKiem)

    time.sleep(5)
    checkbox_vu_viec = ObjCommon.item_checkbox(ten_vu_viec)
    page_base.click_obj(checkbox_vu_viec)
    time.sleep(2)
    page_base.click_obj(Obj_VuViec.btnDelete)
    time.sleep(2)
    page_base.click_obj(Obj_VuViec.btnXacNhan)
    time.sleep(2)


@allure.epic("Quản lý Vụ việc")
@allure.feature("Thư viện Vụ việc")
@pytest.mark.Case
@pytest.mark.CaseCreate
@pytest.mark.Add_DataList
class Test_Add_VuViec:

    @pytest.mark.DC
    @pytest.mark.UAT_DC
    @allure.testcase("c4i2-238", "c4i2-238")
    @allure.story("Thêm mới Vụ việc thành công")
    @allure.title("c4i2-238: Thêm mới vụ việc với thông tin ở trường dữ liệu bắt buộc")
    @pff.parametrize(pathDataTestCase)
    def test_CreateVuViec(self, browser, clean_data, Data):
        """Trường hợp kiểm thử tạo Vụ Việc thành công"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_vu_viec = CaseManagement(driver)

        page_base.click_obj(Obj_VuViec.btnTaoVuViec)
        time.sleep(1)
        page_base.show_overlay_text("Trường hợp kiểm thử tạo vụ việc thành công")
        with allure.step("Điền thông tin vụ việc"):
            attach_table_to_allure(Data, "Data Test")
            page_vu_viec.do_dien_thong_tin_vu_viec(Data)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, "FillInfo")

        with allure.step("Kiểm tra thông báo sau khi tạo thành công"):
            page_base.click_obj(Obj_VuViec.btnSubmitVuViec)
            time.sleep(2)
            check_popup = page_common.verify_notify_popup('Tạo vụ việc thành công')
            capture_screenshot_and_attach_allure(driver, "NotifySuccess")
            assert check_popup, "Không nhận được thông báo tạo vụ việc mới thành công"

    @pytest.mark.DC
    @pytest.mark.UAT_DC
    @allure.testcase("c4i2-244", "c4i2-244")
    @allure.story("Thêm mới Vụ việc thành công")
    @allure.title("c4i2-244: Xác minh có thể xóa vụ việc nếu sử dụng tài khoản có quyền")
    @pff.parametrize(pathDataTestCase)
    def test_DeleteVuViec(self, browser, Data):
        """Trường hợp kiểm thử xóa Vụ Việc thành công"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_vu_viec = CaseManagement(driver)
        json_data_handler = JsonDataHandler(Data)

        page_base.click_obj(Obj_VuViec.btnTaoVuViec)
        time.sleep(1)
        page_base.show_overlay_text("Trường hợp kiểm thử xóa vụ việc thành công")
        with allure.step("Điền thông tin vụ việc"):
            attach_table_to_allure(Data, "Data Test")
            page_vu_viec.do_dien_thong_tin_vu_viec(Data)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, "FillInfo")

        with allure.step("Kiểm tra thông báo sau khi tạo thành công"):
            page_base.click_obj(Obj_VuViec.btnSubmitVuViec)
            time.sleep(2)
            check_popup = page_common.verify_notify_popup('Tạo vụ việc thành công')
            capture_screenshot_and_attach_allure(driver, "NotifySuccess")
            assert check_popup, "Không nhận được thông báo tạo vụ việc mới thành công"

        with allure.step("Tìm kiếm Vụ việc"):
            ten_vu_viec = json_data_handler.get_value_by_label("Tên vụ việc")
            page_base.send_key_input(Obj_VuViec.txtSearchVuViec, ten_vu_viec)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, "SearchVV")
        with allure.step("Pre Test: Kiểm tra danh sách đã load xong"):
            # Kiểm tra danh sách đã load xong
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
            time.sleep(1)
        with allure.step("Xóa vụ việc"):
            checkbox_vu_viec = ObjCommon.item_checkbox(ten_vu_viec)
            page_base.click_obj(checkbox_vu_viec)
            time.sleep(2)
            page_base.click_obj(Obj_VuViec.btnDelete)
            time.sleep(2)
            page_base.click_obj(Obj_VuViec.btnXacNhan)
            time.sleep(2)
            check_popup = page_common.verify_notify_popup('Xóa vụ việc thành công')
            capture_screenshot_and_attach_allure(driver, "UpdateObj")
            assert check_popup, "Xóa vụ việc không thành công"

    @allure.testcase("c4i2-1554", "c4i2-1554")
    @allure.story("Chỉnh sửa Vụ việc thành công")
    @allure.title("Bổ sung đối tượng vào vụ việc")
    @pff.parametrize(pathDataTestCase)
    def test_UpdateDoiTuongVuViec(self, browser, Data, Data_UpdateObj, create_data, clean_data):
        """Trường hợp kiểm thử Thêm đối tượng vào Vụ việc thành công"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_vu_viec = CaseManagement(driver)
        json_data_handler = JsonDataHandler(Data)
        page_base.show_overlay_text("Trường hợp kiểm thử Thêm đối tượng vào vụ việc thành công")

        attach_table_to_allure(Data, "Data Test")
        attach_table_to_allure(Data_UpdateObj, "Data Update Obj")
        with allure.step("Pre Test: Kiểm tra danh sách đã load xong"):
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
        with allure.step("Tìm kiếm Vụ việc"):
            time.sleep(2)
            ten_vu_viec = json_data_handler.get_value_by_label("Tên vụ việc")
            page_base.send_key_input(Obj_VuViec.txtSearchVuViec, ten_vu_viec)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, "SearchVV")

        with allure.step("Nhấn chỉnh sửa kết quả tìm thấy trên danh sách lưới"):
            time.sleep(2)
            page_base.click_obj(Obj_VuViec.btnEditVuviecGrid)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, "ViewResultsVV")

        with allure.step("Thêm hình ảnh đối tượng vào vụ việc"):
            time.sleep(3)
            page_base.click_obj(Obj_VuViec.btnDanhSachDoiTuong)
            page_vu_viec.do_dien_thong_tin_doi_tuong(Data_UpdateObj)

            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, "UpdateObj")
            page_base.click_obj(Obj_VuViec.btnLuuDoiTuong)

        with allure.step("Cập nhật Vụ việc"):
            time.sleep(2)
            page_base.click_obj(Obj_VuViec.btnCapNhatVuViec)
            time.sleep(2)
            check_popup = page_common.verify_notify_popup('Cập nhật vụ việc thành công')
            capture_screenshot_and_attach_allure(driver, "UpdateObj")
            assert check_popup, "Cập nhật thông tin đối tượng trong vụ việc không thành công"

    @allure.testcase("c4i2-238", "c4i2-238")
    @allure.story("Chỉnh sửa Vụ việc thành công")
    @allure.title("Bổ sung nạn nhân vào vụ việc")
    @pff.parametrize(pathDataTestCase)
    def test_UpdateNanNhanVuViec(self, browser, Data, Data_UpdateVictim, create_data, clean_data):
        """Trường hợp kiểm thử Thêm nạn nhân vào Vụ việc thành công"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_vu_viec = CaseManagement(driver)
        json_data_handler = JsonDataHandler(Data)
        page_base.show_overlay_text("Trường hợp kiểm thử Thêm nạn nhân vào vụ việc thành công")

        attach_table_to_allure(Data, "Data Test")
        attach_table_to_allure(Data_UpdateVictim, "Data UpdateVictim")
        with allure.step("Pre Test: Kiểm tra danh sách đã load xong"):
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)

        with allure.step("Tìm kiếm Vụ việc"):
            time.sleep(2)
            ten_vu_viec = json_data_handler.get_value_by_label("Tên vụ việc")
            page_base.send_key_input(Obj_VuViec.txtSearchVuViec, ten_vu_viec)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, "SearchVV")

        with allure.step("Nhấn chỉnh sửa kết quả tìm thấy trên danh sách lưới"):
            time.sleep(2)
            page_base.click_obj(Obj_VuViec.btnEditVuviecGrid)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, "ViewResultsVV")

        with allure.step("Điều hướng đến popup Thêm nạn nhân"):
            page_base.do_scroll_mouse_to_element(Obj_VuViec.btnDanhSachNanNan)
            page_base.click_obj(Obj_VuViec.btnDanhSachNanNan)
            time.sleep(2)
            page_base.click_obj(Obj_VuViec.btnThemInPopup)

        with allure.step("Thêm thông tin nạn nhân vào vụ việc"):
            page_vu_viec.do_dien_thong_tin_vu_viec(Data_UpdateVictim)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, "UpdateVictim")
            time.sleep(2)
            page_base.click_obj(Obj_VuViec.btnLuuNanNhan)

        with allure.step("Cập nhật Vụ việc"):
            time.sleep(2)
            page_base.click_obj(Obj_VuViec.btnCapNhatVuViec)
            time.sleep(2)
            check_popup = page_common.verify_notify_popup('Cập nhật vụ việc thành công')
            capture_screenshot_and_attach_allure(driver, "UpdateObj")
            assert check_popup, "Cập nhật thông tin nạn nhân trong vụ việc không thành công"

    @allure.testcase("c4i2-1556", "c4i2-1556")
    @allure.story("Chỉnh sửa Vụ việc thành công")
    @allure.title("Bổ sung phương tiện vào vụ việc")
    @pff.parametrize(pathDataTestCase)
    def test_UpdatePhuongTienVuViec(self, browser, Data, Data_UpdateVehicle, create_data, clean_data):
        """Trường hợp kiểm thử Thêm phương tiện vào Vụ việc thành công"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_vu_viec = CaseManagement(driver)
        json_data_handler = JsonDataHandler(Data)
        page_base.show_overlay_text("Trường hợp kiểm thử Thêm phương tiện vào vụ việc thành công")

        attach_table_to_allure(Data, "Data Test")
        attach_table_to_allure(Data_UpdateVehicle, "Data Update Vehicle")
        with allure.step("Pre Test: Kiểm tra danh sách đã load xong"):
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
        with allure.step("Tìm kiếm Vụ việc"):
            time.sleep(2)
            ten_vu_viec = json_data_handler.get_value_by_label("Tên vụ việc")
            page_base.send_key_input(Obj_VuViec.txtSearchVuViec, ten_vu_viec)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, "SearchVV")

        with allure.step("Nhấn chỉnh sửa kết quả tìm thấy trên danh sách lưới"):
            time.sleep(2)
            page_base.click_obj(Obj_VuViec.btnEditVuviecGrid)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, "ViewResultsVV")
        with allure.step("Điều hướng đến popup Thêm phương tiện"):
            page_base.do_scroll_mouse_to_element(Obj_VuViec.btnDanhSachPhuongTien)
            page_base.click_obj(Obj_VuViec.btnDanhSachPhuongTien)
            time.sleep(2)
            page_base.click_obj(Obj_VuViec.btnThemInPopup)

        with allure.step("Thêm thông tin phương tiện vào vụ việc"):
            page_vu_viec.do_dien_thong_tin_vu_viec(Data_UpdateVehicle)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, "UpdateVictim")
            page_base.click_obj(Obj_VuViec.btnSearchPhuongTien)
            time.sleep(1)
            page_base.click_obj(Obj_VuViec.resultSearchPhuongTien)
            time.sleep(2)
            page_base.click_obj(Obj_VuViec.btnLuuPhuongTien)

        with allure.step("Cập nhật Vụ việc"):
            time.sleep(2)
            page_base.click_obj(Obj_VuViec.btnCapNhatVuViec)
            time.sleep(2)
            check_popup = page_common.verify_notify_popup('Cập nhật vụ việc thành công')
            capture_screenshot_and_attach_allure(driver, "UpdateObj")
            assert check_popup, "Cập nhật thông tin phương tiện  trong vụ việc không thành công"

    @allure.testcase("c4i2-238", "c4i2-238")
    @allure.story("Chỉnh sửa Vụ việc thành công")
    @allure.title("Bổ sung thông tin chi tiết vào vụ việc")
    @pff.parametrize(pathDataTestCase)
    def test_UpdateFileDinhKem(self, browser, Data, Data_UpdateAttachFile, create_data, clean_data):
        """Trường hợp kiểm thử Thêm chi tiếc vào Vụ việc thành công"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_vu_viec = CaseManagement(driver)
        json_data_handler = JsonDataHandler(Data)
        page_base.show_overlay_text("Trường hợp kiểm thử Thêm chi tiết vào vụ việc thành công")

        attach_table_to_allure(Data, "Data Test")
        attach_table_to_allure(Data_UpdateAttachFile, "Data Update Attach File")
        with allure.step("Pre Test: Kiểm tra danh sách đã load xong"):
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
        with allure.step("Tìm kiếm Vụ việc"):
            time.sleep(2)
            ten_vu_viec = json_data_handler.get_value_by_label("Tên vụ việc")
            page_base.send_key_input(Obj_VuViec.txtSearchVuViec, ten_vu_viec)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, "SearchVV")

        with allure.step("Nhấn chỉnh sửa kết quả tìm thấy trên danh sách lưới"):
            time.sleep(2)
            page_base.click_obj(Obj_VuViec.btnEditVuviecGrid)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, "ViewResultsVV")

        with allure.step("Thêm thông tin chi tiết (hình ảnh, video) vào vụ việc"):
            page_base.do_scroll_mouse_to_element(Obj_VuViec.txtvideo)
            time.sleep(2)
            page_vu_viec.do_them_thong_tin_file_dinh_kem(Data_UpdateAttachFile)
            time.sleep(2)

        with allure.step("Cập nhật Vụ việc"):
            time.sleep(2)
            page_base.click_obj(Obj_VuViec.btnCapNhatVuViec)
            time.sleep(2)
            check_popup = page_common.verify_notify_popup('Cập nhật vụ việc thành công')
            capture_screenshot_and_attach_allure(driver, "UpdateAttachFile")
            assert check_popup, "Cập nhật thông tin phương tiện  trong vụ việc không thành công"

    @allure.testcase("c4i2-239", "c4i2-239")
    @allure.story("Thêm mới Vụ việc không thành công")
    @allure.title("Xác minh thêm Vụ việc không thành công - Không điền thông tin bắt buộc")
    @pff.parametrize(pathDataTestCase)
    def test_CreateCaseUnSuccessfulNotFillRequiredField(self, browser, Data, Field_RequiredMissing):
        """Trường hợp kiểm thử tạo Vụ Việc không thành công - không điền thông tin ở trường dữ liệu bắt buộc"""
        # 6 case: Lần lượt bỏ trống các trường (All, Lĩnh vực, Tên vụ việc, Tỉnh/thành, Quận/huyện, Xã/phường)
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_vu_viec = CaseManagement(driver)
        fill_data = FillData(driver)

        page_base.click_obj(Obj_VuViec.btnTaoVuViec)
        time.sleep(1)
        page_base.show_overlay_text("Trường hợp kiểm thử Tạo vụ việc không thành công")
        with allure.step("Điền thông tin vụ việc"):
            attach_table_to_allure(Data, "Data Test")
            page_base.wait_for_page_load()
            page_vu_viec.do_dien_thong_tin_vu_viec(Data)
            capture_screenshot_and_attach_allure(driver, "FillInfo")
            time.sleep(2)
        with allure.step("Nhấn vào button 'Tạo vụ việc'"):
            page_base.click_obj(Obj_VuViec.btnSubmitVuViec)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, "NotifySuccess")
        with allure.step("Kiểm tra có cảnh báo khi bỏ trống trường bắt buộc"):
            for field in Field_RequiredMissing:
                check_field_required = fill_data._check_invalid_error(field)
                check_alert = page_common.verify_notify_field_required('Trường này không được để trống')
                assert check_field_required and check_alert, "Không có cảnh báo khi bỏ trống trường thông tin bắt buộc"
