import time
import pytest
import allure

from Libraries.Framework.FactoryDrivers import get_chrome_driver
from Libraries.Framework.Utils import PageBase
from Libraries.Config import Default
from PageObjects.Web.Obj_VuViec import Obj_VuViec
from PageObjects.Web.Obj_GuongMat import Obj_GuongMat
from PageObjects.Web.Obj_Common import ObjCommon
from WebApplications.PageCommon import PageCommon
from WebApplications.PageHome import LoginPage
from WebApplications.PageGuongMat import PageGuongMat
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
    page_base.click_obj(Obj_VuViec.tabThuVien)
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
    page_guong_mat = PageGuongMat(driver)

    page_base.click_obj(Obj_VuViec.btnTaoDoiTuong)
    page_guong_mat.do_bo_sung_them_tt_cong_dan(Data)
    page_base.do_scroll_mouse_to_element(Obj_VuViec.elementLastPopup)
    page_guong_mat.do_dien_thong_tin_cong_dan(Data)
    page_base.click_obj(Obj_VuViec.btnSubmitDoiTuong)
    time.sleep(2)
    yield


@pytest.fixture(scope='function')
def clean_data(browser, save_current_url, Data):
    yield
    driver = browser
    page_base = PageBase(driver)
    json_data_handler = JsonDataHandler(Data)

    driver.get(save_current_url)
    time.sleep(1)
    labelsearch = "Họ và tên"
    ten_doi_tuong = json_data_handler.get_value_by_label(labelsearch)
    page_base.send_key_input(ObjCommon.search_textbox(labelsearch), ten_doi_tuong)
    page_base.click_obj(Obj_VuViec.btnTimKiem)

    time.sleep(3)
    page_base.click_obj(ObjCommon.item_checkbox(ten_doi_tuong))
    time.sleep(2)
    page_base.click_obj(Obj_VuViec.btnDeleteDoiTuong)
    time.sleep(2)
    page_base.click_obj(Obj_VuViec.btnXacNhan)
    time.sleep(2)

    # xóa dữ liệu đối tượng tại thư viện gương mặt
    page_base.click_obj(Obj_GuongMat.iconNhanDangGuongMat_navigation)
    time.sleep(1)
    page_base.click_obj(Obj_GuongMat.tabThuVien)
    time.sleep(1)
    page_base.send_key_input(Obj_GuongMat.txtSearchGuongMat, ten_doi_tuong)
    page_base.click_obj(Obj_GuongMat.btnTimKiem)
    time.sleep(3)
    page_base.click_obj(ObjCommon.item_checkbox(ten_doi_tuong))
    time.sleep(2)
    page_base.click_obj(Obj_GuongMat.btnDelete)
    time.sleep(2)
    page_base.click_obj(Obj_GuongMat.btnXacNhan)
    time.sleep(2)


pageBase = PageBase(browser)
pathDataTestObj = pageBase.load_path_data_file_from_path("Datas_Case",
                                                    "Test_DoiTuong.json")


@allure.epic("Quản lý Vụ việc")
@allure.feature("Thư viện Đối tượng")
@pytest.mark.Obj
@pytest.mark.Add_DataList
class Test_Add_CaseObj:

    @allure.testcase("c4i2-1436", "c4i2-1436")
    @allure.story("Thêm mới Đối tượng thành công")
    @allure.title("Thêm đối tượng không xác định")
    @pff.parametrize(pathDataTestObj)
    def test_AddUndefinedObject(self, browser, Data, clean_data):
        """Trường hợp kiểm thử Thêm mới đối tượng thành công - Thêm mới đối tượng không xác định thành công"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_guong_mat = PageGuongMat(driver)

        page_base.click_obj(Obj_VuViec.btnTaoDoiTuong)
        time.sleep(1)
        page_base.show_overlay_text("Trường hợp kiểm thử thêm công dân thành công")
        attach_table_to_allure(Data)
        with allure.step("Điền thông tin công dân"):
            page_guong_mat.do_dien_thong_tin_cong_dan(Data)
            page_guong_mat.do_bo_sung_them_tt_cong_dan(Data)
            capture_screenshot_and_attach_allure(driver, "FillInfo")
            time.sleep(2)

        with allure.step("Kiểm tra thông báo sau khi tạo thành công"):
            page_base.click_obj(Obj_VuViec.btnSubmitDoiTuong)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, "NotifySuccess")
            check_popup = page_common.verify_notify_popup('Thêm thành công')
            assert check_popup, "Không nhận được thông báo tạo công dân mới không thành công"

    @allure.testcase("c4i2-1436", "c4i2-1436")
    @allure.story("Thêm mới Đối tượng thành công")
    @allure.title("Thêm mới đối tượng với đầy đủ toàn bộ thuộc tính")
    @pff.parametrize(pathDataTestObj)
    def test_CreateObjectWithAllAttributes(self, browser, Data, clean_data):
        """Trường hợp kiểm thử Thêm mới đối tượng thành công - Thêm mới đối tượng với đầy đủ toàn bộ thuộc tính"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_guong_mat = PageGuongMat(driver)
        json_data_handler = JsonDataHandler(Data)

        page_base.click_obj(Obj_VuViec.btnTaoDoiTuong)
        time.sleep(1)
        page_base.show_overlay_text("Thêm mới với đầy đủ thuộc tính")
        attach_table_to_allure(Data)
        with allure.step("Điền thông tin công dân"):
            page_base.do_scroll_mouse_to_element(Obj_VuViec.elementLastPopup)
            page_guong_mat.do_dien_thong_tin_cong_dan(Data)
            page_guong_mat.do_bo_sung_them_tt_cong_dan(Data)
            capture_screenshot_and_attach_allure(driver, "FillInfo")
            time.sleep(2)

        with allure.step("Kiểm tra thông báo sau khi tạo thành công"):
            page_base.click_obj(Obj_VuViec.btnSubmitDoiTuong)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, "NotifySuccess")
            check_popup = page_common.verify_notify_popup('Thêm thành công')
            assert check_popup, "Không nhận được thông báo tạo công dân mới không thành công"

        with allure.step("Tìm kiếm thông tin công dân mới đã thêm"):
            time.sleep(2)
            labelsearch = "Họ và tên"
            ten_doi_tuong = json_data_handler.get_value_by_label(labelsearch)
            page_base.send_key_input(ObjCommon.search_textbox(labelsearch), ten_doi_tuong)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, "SearchValue")
            check_exit_in_pop_up = page_base.check_element_visibility(Obj_VuViec.iconEditDoiTuong)
            assert check_exit_in_pop_up, "Không tìm thấy kết quả đã tạo trên danh sách lưới"

        with allure.step("Nhấn chỉnh sửa kết quả đầu tiên"):
            time.sleep(3)
            page_base.click_obj(Obj_VuViec.iconEditDoiTuong)
            time.sleep(2)

        with allure.step("Kiểm tra kết quả đã tạo"):
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, "CheckResultCreated")
            page_base.do_scroll_mouse_to_element(Obj_VuViec.elementLastPopup)
            check_result = page_common.verify_result_created(Data)
            assert check_result, "Dữ liệu đã thêm không hiển thị đầy đủ"

    @allure.testcase("c4i2-1562", "c4i2-1562")
    @allure.story("Thêm mới Đối tượng thành công")
    @allure.title("Xác minh có thể tra cứu nhận dạng ảnh được upload")
    @pff.parametrize(pathDataTestObj)
    def test_VerifyImageUploadCanBeSearched(self, browser, Data, Name):
        """Trường hợp kiểm thử Thêm mới đối tượng thành công
        - Xác minh có thể tra cứu nhận dạng ảnh được upload (form thêm mới đối tượng)"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_guong_mat = PageGuongMat(driver)

        page_base.click_obj(Obj_VuViec.btnTaoDoiTuong)
        time.sleep(1)
        page_base.show_overlay_text("Tra cứu nhận dạng ảnh")
        with allure.step("Nhập thông tin Đối tượng - upload hình ảnh"):
            page_guong_mat.do_bo_sung_them_tt_cong_dan(Data)
            capture_screenshot_and_attach_allure(driver, "FillImage")
            time.sleep(2)
        with allure.step("Nhấn vào button 'Tra cứu nhận dạng'"):
            page_base.click_obj(Obj_VuViec.btnTraCuuNhanDangDoiTuong)
        with allure.step("Kiểm tra kết quả tra cứu nhận dạng"):
            cellid = "details"
            index = 1
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, Name,
                                                                           index)
            capture_screenshot_and_attach_allure(driver, "VerifyInGrid")
            assert result, f"Trên danh sách lưới có Họ và tên '{different_value}' khác với giá trị Họ và tên mong muốn '{Name}' "

    @allure.testcase("c4i2-1539", "c4i2-1539")
    @allure.story("Thêm mới Đối tượng thành công")
    @allure.title("Xác minh có thể xem lịch sử nhận dạng đối tượng")
    @pff.parametrize(pathDataTestObj)
    def test_VerifyCanViewRecognitionHistory(self, browser, Data, Name):
        """Trường hợp kiểm thử Thêm mới đối tượng thành công
        - Xác minh có thể xem lịch sử nhận dạng đối tượng(form thêm mới đối tượng)"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_guong_mat = PageGuongMat(driver)

        page_base.click_obj(Obj_VuViec.btnTaoDoiTuong)
        time.sleep(1)
        page_base.show_overlay_text("Xem lịch sử nhận dạng")
        with allure.step("Nhập thông tin Đối tượng - upload hình ảnh"):
            page_guong_mat.do_bo_sung_them_tt_cong_dan(Data)
            capture_screenshot_and_attach_allure(driver, "FillImage")
            time.sleep(2)
        with allure.step("Nhấn vào button 'Lịch sử nhận dạng'"):
            page_base.click_obj(Obj_VuViec.btnTraCuuLichSuNhanDang)
        with allure.step("Kiểm tra kết quả tra cứu lịch sử nhận dạng"):
            cellid = "details"
            index = 1
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, Name,
                                                                           index)
            capture_screenshot_and_attach_allure(driver, "VerifyInGrid")
            assert result, f"Trên danh sách lưới có Họ và tên '{different_value}' khác với giá trị Họ và tên mong muốn '{Name}"

    @allure.testcase("c4i2-1443", "c4i2-1443")
    @allure.story("Thêm mới Đối tượng không thành công")
    @allure.title("Thêm đối tượng với hình ảnh không hợp lệ")
    @pff.parametrize(pathDataTestObj)
    def test_AddUndefinedObjectWithImageUnValid(self, browser, Data, text_notify, desc):
        """Trường hợp kiểm thử tạo thông tin Đối tượng không thành công - upload hình ảnh không hợp lệ"""
        description = f"Trường hợp kiểm thử tạo đối tượng không thành công - {desc}"
        allure.dynamic.description(description)
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_guong_mat = PageGuongMat(driver)

        page_base.click_obj(Obj_VuViec.btnTaoDoiTuong)
        time.sleep(1)
        page_base.show_overlay_text(f"Trường hợp kiểm thử tạo đối tượng không thành công - {desc}")
        attach_table_to_allure(Data)
        with allure.step("Điền thông tin công dân"):
            page_guong_mat.do_dien_thong_tin_cong_dan(Data)
            page_guong_mat.do_bo_sung_them_tt_cong_dan(Data)
            capture_screenshot_and_attach_allure(driver, "FillInfo")
            time.sleep(2)
        with allure.step("Kiểm tra cảnh báo khi upload hình ảnh không hợp lệ"):
            capture_screenshot_and_attach_allure(driver, name="NotifySuccess")
            check_notify = page_common.verify_notify_field_required(text_notify)
            assert check_notify, "Không có cảnh báo (hoặc cảnh báo không chính xác) khi upload hình ảnh không hợp lệ"


@allure.epic("Quản lý Vụ việc")
@allure.feature("Thư viện Đối tượng")
@allure.story("Chỉnh sửa đối tượng thành công")
@pytest.mark.Obj
@pytest.mark.Add_DataList
class Test_Edit_CaseObj:

    @allure.testcase("c4i2-1444", "c4i2-1444")
    @allure.title("Chỉnh sửa đối tượng với đầy đủ toàn bộ thuộc tính")
    @pff.parametrize(pathDataTestObj)
    def test_EditObjectWithAllAttributes(self, browser, create_data, clean_data, Data, Data_Edit):
        """Trường hợp kiểm thử Chỉnh sửa đối tượng thành công - Thêm mới chỉnh sửa với đầy đủ toàn bộ thuộc tính"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_guong_mat = PageGuongMat(driver)
        json_data_handler = JsonDataHandler(Data_Edit)

        time.sleep(1)
        page_base.show_overlay_text("Chỉnh sửa với đầy đủ thuộc tính")
        attach_table_to_allure(Data)
        attach_table_to_allure(Data_Edit, name="Data Edit")
        with allure.step("Tìm kiếm Đối tượng"):
            time.sleep(2)
            labelsearch = "Họ và tên"
            ten_doi_tuong = json_data_handler.get_value_by_label(labelsearch)
            page_base.send_key_input(ObjCommon.search_textbox(labelsearch), ten_doi_tuong)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, "SearchValue")
            check_exit_in_pop_up = page_base.check_element_visibility(Obj_VuViec.iconEditDoiTuong)
            assert check_exit_in_pop_up, "Không tìm thấy kết quả đã tạo trên danh sách lưới"

        with allure.step("Nhấn chỉnh sửa kết quả tìm thấy trên danh sách lưới"):
            time.sleep(2)
            page_base.click_obj(Obj_GuongMat.iconEdit)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="VewResultsFace")
        with allure.step("Sửa thông tin công dân"):
            page_base.do_scroll_mouse_to_element(Obj_VuViec.elementLastPopup)
            page_guong_mat.do_dien_thong_tin_cong_dan(Data_Edit)
            page_guong_mat.do_bo_sung_them_tt_cong_dan(Data_Edit)
            capture_screenshot_and_attach_allure(driver, "FillInfo")
            time.sleep(2)

        with allure.step("Kiểm tra thông báo sau khi tạo thành công"):
            page_base.click_obj(Obj_VuViec.btnUpdateDoiTuong)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, "NotifySuccess")
            check_popup = page_common.verify_notify_popup('Cập nhật đối tượng thành công')
            assert check_popup, "Không nhận được thông báo cập nhật đối tượng thành công"

        with allure.step("Tìm kiếm thông tin công dân mới đã thêm"):
            time.sleep(2)
            labelsearch = "Họ và tên"
            ten_doi_tuong = json_data_handler.get_value_by_label(labelsearch)
            page_base.send_key_input(ObjCommon.search_textbox(labelsearch), ten_doi_tuong)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, "SearchValue")
            check_exit_in_pop_up = page_base.check_element_visibility(Obj_VuViec.iconEditDoiTuong)
            assert check_exit_in_pop_up, "Không tìm thấy kết quả đã tạo trên danh sách lưới"

        with allure.step("Nhấn chỉnh sửa kết quả đầu tiên"):
            time.sleep(3)
            page_base.click_obj(Obj_VuViec.iconEditDoiTuong)
            time.sleep(2)

        with allure.step("Kiểm tra kết quả đã tạo"):
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, "CheckResultCreated")
            page_base.do_scroll_mouse_to_element(Obj_VuViec.elementLastPopup)
            check_result = page_common.verify_result_created(Data_Edit)
            assert check_result, "Dữ liệu đã thêm không hiển thị đầy đủ"


@allure.epic("Quản lý Vụ việc")
@allure.feature("Thư viện Đối tượng")
@allure.story("Xóa đối tượng thành công")
@pytest.mark.Obj
@pytest.mark.Add_DataList
class Test_Delete_CaseObj:

    @allure.testcase("c4i2-1445", "c4i2-1445")
    @allure.title("Xóa 1 đối tượng")
    @pff.parametrize(pathDataTestObj)
    def test_DeleteObject(self, browser, create_data, Data):
        """Trường hợp kiểm thử Xóa đối tượng thành công - Xóa ở Thư viện đối tượng và Thư viện gương mặt"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        json_data_handler = JsonDataHandler(Data)

        time.sleep(1)
        page_base.show_overlay_text("Xóa đối tượng thành công")
        attach_table_to_allure(Data)
        with allure.step("Tìm kiếm Đối tượng"):
            time.sleep(2)
            labelsearch = "Họ và tên"
            ten_doi_tuong = json_data_handler.get_value_by_label(labelsearch)
            page_base.send_key_input(ObjCommon.search_textbox(labelsearch), ten_doi_tuong)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, "SearchValue")
            check_exit_in_pop_up = page_base.check_element_visibility(Obj_VuViec.iconEditDoiTuong)
            assert check_exit_in_pop_up, "Không tìm thấy kết quả đã tạo trên danh sách lưới"

        with allure.step("Xóa đối tượng tại tab Thư viện đối tượng"):
            time.sleep(1)
            page_base.click_obj(ObjCommon.item_checkbox(ten_doi_tuong))
            capture_screenshot_and_attach_allure(driver, "CheckObj")
            time.sleep(1)
            page_base.click_obj(Obj_VuViec.btnDeleteDoiTuong)
            time.sleep(1)
            page_base.click_obj(Obj_VuViec.btnXacNhan)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, "NotifySuccess")

        with allure.step("Xóa đối tượng tại tab Thư viện gương mặt"):
            page_base.click_obj(Obj_GuongMat.iconNhanDangGuongMat_navigation)
            time.sleep(1)
            page_base.click_obj(Obj_GuongMat.tabThuVien)
            time.sleep(1)
            page_base.send_key_input(Obj_GuongMat.txtSearchGuongMat, ten_doi_tuong)
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            time.sleep(3)
            page_base.click_obj(ObjCommon.item_checkbox(ten_doi_tuong))
            time.sleep(2)
            page_base.click_obj(Obj_GuongMat.btnDelete)
            time.sleep(2)
            page_base.click_obj(Obj_GuongMat.btnXacNhan)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, "NotifySuccess")
            check_popup = page_common.verify_notify_popup('Xóa thành công')
            assert check_popup, "Không nhận được thông báo xóa đối tượng thành công thành công"
