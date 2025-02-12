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
from WebApplications.PageGuongMat import PageGuongMat, PageGuongMatTabThuVien
from conftest import capture_screenshot_and_attach_allure
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


pageBase = PageBase(browser)
pathDataTestObjSearch = pageBase.load_path_data_file_from_path("Datas_Case",
                                                               "Test_DoiTuong_Search.json")


@pff.parametrize(path=pathDataTestObjSearch, key="create_data_search")
def setup_data_search(Data):
    value_data = Data
    return value_data


@pytest.fixture(scope='class', autouse=True)
def create_data(browser, data=setup_data_search):
    driver = browser
    page_base = PageBase(driver)
    page_guong_mat = PageGuongMat(driver)
    Data = data.pytestmark[0].args[1][0].values[0]

    page_base.click_obj(Obj_VuViec.btnTaoDoiTuong)
    page_base.do_scroll_mouse_to_element(Obj_VuViec.elementLastPopup)
    page_guong_mat.do_dien_thong_tin_cong_dan(Data)
    page_guong_mat.do_bo_sung_them_tt_cong_dan(Data)
    page_base.click_obj(Obj_VuViec.btnSubmitDoiTuong)
    time.sleep(2)
    yield


@pytest.fixture(scope='class', autouse=True)
def clean_data(browser, save_current_url, data=setup_data_search):
    yield
    driver = browser
    page_base = PageBase(driver)
    Data = data.pytestmark[0].args[1][0].values[0]
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


@allure.epic("Quản lý Vụ việc")
@allure.feature("Thư viện Đối tượng")
@pytest.mark.Obj
@pytest.mark.ObjSearch
@pytest.mark.Add_DataList
class Test_CaseObjSearch:
    @allure.testcase("c4i2-289", "c4i2-289")
    @allure.story("Tìm kiếm Đối tượng thành công")
    @allure.title("Search hình ảnh Đối tượng")
    @pff.parametrize(path=pathDataTestObjSearch)
    def test_search_single_face_in_image_success(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm đối tượng thành công - Search hình ảnh Đối tượng"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_guong_mat_tab_thu_vien = PageGuongMatTabThuVien(driver)
        page_guong_mat = PageGuongMat(driver)
        json_data_handler = JsonDataHandler(Data_Search)
        page_base.show_overlay_text("Search hình ảnh gương mặt")

        label_search = "Ảnh chính"
        type_of, label, value = json_data_handler.get_info_by_label(label_search)

        value_image = value
        with allure.step("Kiểm tra danh sách đã load xong trước khi bắt đầu tìm kiếm"):
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
        with allure.step("Tải hình ảnh gương mặt lên tab Tìm kiếm"):
            page_guong_mat.do_fill_image_face_search(value_image)
            capture_screenshot_and_attach_allure(driver, name="FillImage")
            time.sleep(2)
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
        with allure.step("Kiểm tra kết quả xuất hiện đầu tiên trên danh sách lưới"):
            cellid = "HOVATEN"
            results_in_grid = page_common.do_get_data_test_in_grid(cellid)
            print(f"Kết quả trên grid hiển thị: {results_in_grid}")

            time.sleep(3)
            page_base.click_obj(Obj_VuViec.iconEditDoiTuong)
            time.sleep(2)
            label_search = "Họ và tên"
            type_of, label, value = json_data_handler.get_info_by_label(label_search)
            check_result = page_guong_mat_tab_thu_vien.do_verify_result_search_in_popup(type_of, label, value)
            capture_screenshot_and_attach_allure(driver, "CheckResultEdited")
            assert check_result, "Kết quả tìm kiếm không hiển thị chính xác dữ liệu"

    @allure.testcase("c4i2-289", "c4i2-289")
    @allure.story("Tìm kiếm Đối tượng không thành công")
    @allure.title("Search hình ảnh bị mờ, không rõ Gương mặt")
    @pff.parametrize(path=pathDataTestObjSearch)
    def test_search_unclear_image_failure(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm gương mặt không thành công - Search hình ảnh bị mờ, không rõ Gương mặt"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_guong_mat = PageGuongMat(driver)
        json_data_handler = JsonDataHandler(Data_Search)
        page_base.show_overlay_text("Search hình ảnh bị mờ, không rõ Gương mặt")

        label_search = "Ảnh chính"
        type_of, label, value = json_data_handler.get_info_by_label(label_search)

        value_image = value
        with allure.step("Kiểm tra danh sách đã load xong trước khi bắt đầu tìm kiếm"):
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
        with allure.step("Tải hình ảnh gương mặt lên tab Tìm kiếm"):
            page_guong_mat.do_fill_image_face_search(value_image)
            capture_screenshot_and_attach_allure(driver, name="FillImage")
            time.sleep(2)
        with allure.step("Kiểm tra cảnh báo khi upload hình ảnh không hợp lệ"):
            text_notify = "Không nhận dạng được mặt"
            allure.attach(driver.get_screenshot_as_png(), name="NotifySuccess",
                          attachment_type=allure.attachment_type.PNG)
            check_notify = page_common.verify_notify_field_required(text_notify)
            assert check_notify, "Không có cảnh báo (hoặc cảnh báo không chính xác) khi upload hình ảnh không hợp lệ"

    @allure.testcase("c4i2-294", "c4i2-294")
    @allure.story("Tìm kiếm Đối tượng thành công")
    @allure.title("Search theo Nhóm tội danh")
    @pff.parametrize(path=pathDataTestObjSearch)
    def test_filter_by_offense_group_success(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm Gương mặt thành công - Search theo Nhóm tội danh"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        json_data_handler = JsonDataHandler(Data_Search)
        page_guong_mat_tab_thu_vien = PageGuongMatTabThuVien(driver)
        page_base.show_overlay_text("Search theo Nhóm tội danh")

        label_search = "Nhóm tội danh"
        type_of, label, value = json_data_handler.get_info_by_label(label_search)

        with allure.step("Kiểm tra danh sách đã load xong trước khi bắt đầu tìm kiếm"):
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
        with allure.step("Nhập thông tin Nhóm tội danh vào tab Tìm kiếm"):
            time.sleep(2)
            txt_search_obj = ObjCommon.label_dropdown_list(label)
            page_base.select_key_dropdown(txt_search_obj, value)
            capture_screenshot_and_attach_allure(driver, name="EnterObj")
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            time.sleep(1)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
        with allure.step("Kiểm tra Nhóm tội danh trong popup chi tiết của kết quả đầu tiên trả về trên grid"):
            cellid = "HOVATEN"
            results_in_grid = page_common.do_get_data_test_in_grid(cellid)
            print(f"Kết quả trên grid hiển thị: {results_in_grid}")

            time.sleep(3)
            page_base.click_obj(Obj_VuViec.btnEditVuviecGrid)
            time.sleep(2)
            check_result = page_guong_mat_tab_thu_vien.do_verify_result_search_in_popup(type_of, label, value)
            allure.attach(driver.get_screenshot_as_png(), name="CheckResultEdited",
                          attachment_type=allure.attachment_type.PNG)
            assert check_result, "Kết quả tìm kiếm không hiển thị chính xác dữ liệu"

    @allure.testcase("c4i2-1565", "c4i2-1565")
    @allure.story("Tìm kiếm Đối tượng thành công")
    @allure.title("Search theo Tội danh")
    @pff.parametrize(path=pathDataTestObjSearch)
    def test_filter_by_offense_success(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm Gương mặt thành công - Search theo Tội danh"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        json_data_handler = JsonDataHandler(Data_Search)
        page_guong_mat_tab_thu_vien = PageGuongMatTabThuVien(driver)
        page_base.show_overlay_text("Search Tội danh")

        label_search = "Tội danh"
        type_of, label, value = json_data_handler.get_info_by_label(label_search)

        label_group_search = "Nhóm tội danh"
        type_of_group, label_group, value_group = json_data_handler.get_info_by_label(label_group_search)

        with allure.step("Kiểm tra danh sách đã load xong trước khi bắt đầu tìm kiếm"):
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
        with allure.step("Nhập thông tin Nhóm tội danh, Tội danh vào tab Tìm kiếm"):
            time.sleep(2)
            txt_search_bsx = ObjCommon.label_dropdown_list(label_group)
            page_base.select_key_dropdown(txt_search_bsx, value_group)
            time.sleep(2)
            txt_search_bsx = ObjCommon.label_dropdown_list(label)
            page_base.select_key_dropdown(txt_search_bsx, value)
            capture_screenshot_and_attach_allure(driver, name="EnterGroup")
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            time.sleep(1)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
        with allure.step("Kiểm tra Tội danh trong popup chi tiết của kết quả đầu tiên trả về trên grid"):
            cellid = "HOVATEN"
            results_in_grid = page_common.do_get_data_test_in_grid(cellid)
            print(f"Kết quả trên grid hiển thị: {results_in_grid}")

            time.sleep(3)
            page_base.click_obj(Obj_VuViec.btnEditVuviecGrid)
            time.sleep(2)
            check_result = page_guong_mat_tab_thu_vien.do_verify_result_search_in_popup(type_of, label, value)
            capture_screenshot_and_attach_allure(driver, "CheckResultEdited")
            assert check_result, "Kết quả tìm kiếm không hiển thị chính xác dữ liệu"

    @allure.testcase("c4i2-291", "c4i2-291")
    @allure.story("Tìm kiếm Đối tượng thành công")
    @allure.title("Tìm với Họ và tên Đối tượng")
    @pff.parametrize(path=pathDataTestObjSearch)
    def test_search_with_full_name(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm Gương mặt thành công - Tìm kiếm theo Họ và tên đối tượng"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        json_data_handler = JsonDataHandler(Data_Search)
        page_guong_mat_tab_thu_vien = PageGuongMatTabThuVien(driver)
        page_base.show_overlay_text("Search Họ và tên")

        label_search = "Họ và tên"
        type_of, label, value = json_data_handler.get_info_by_label(label_search)

        with allure.step("Kiểm tra danh sách đã load xong trước khi bắt đầu tìm kiếm"):
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
        with allure.step("Nhập thông tin Tên Đối tượng vào textbox Họ và tên"):
            time.sleep(2)
            txt_search_obj = ObjCommon.search_textbox(label_search)
            page_base.send_key_input(txt_search_obj, value)
            capture_screenshot_and_attach_allure(driver, name="EnterObj")
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            time.sleep(1)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
        with allure.step("Kiểm tra Tên đối tượng trong popup chi tiết của kết quả đầu tiên trả về trên grid"):
            cellid = "HOVATEN"
            results_in_grid = page_common.do_get_data_test_in_grid(cellid)
            print(f"Kết quả trên grid hiển thị: {results_in_grid}")

            time.sleep(3)
            page_base.click_obj(Obj_VuViec.btnEditVuviecGrid)
            time.sleep(2)
            check_result = page_guong_mat_tab_thu_vien.do_verify_result_search_in_popup(type_of, label, value)
            capture_screenshot_and_attach_allure(driver, "CheckResultEdited")
            assert check_result, "Kết quả tìm kiếm không hiển thị chính xác dữ liệu"

    @allure.testcase("c4i2-292", "c4i2-292")
    @allure.story("Tìm kiếm Đối tượng thành công")
    @allure.title("Tìm với CMND/CCCD/Hộ chiếu")
    @pff.parametrize(path=pathDataTestObjSearch)
    def test_search_with_identity_card(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm Gương mặt thành công - Tìm với CMND/CCCD/Hộ chiếu"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        json_data_handler = JsonDataHandler(Data_Search)
        page_guong_mat_tab_thu_vien = PageGuongMatTabThuVien(driver)
        page_base.show_overlay_text("Search CMND")

        label_search = "CMND/ CCCD/ Hộ chiếu"
        type_of, label, value = json_data_handler.get_info_by_label(label_search)

        with allure.step("Kiểm tra danh sách đã load xong trước khi bắt đầu tìm kiếm"):
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
        with allure.step("Nhập thông tin CMND vào textbox CMND/CCCD/Hộ chiếu"):
            time.sleep(2)
            txt_search_obj = ObjCommon.search_textbox(label_search)
            page_base.send_key_input(txt_search_obj, value)
            capture_screenshot_and_attach_allure(driver, name="EnterObj")
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            time.sleep(1)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
        with allure.step("Kiểm tra CMND trong popup chi tiết của kết quả đầu tiên trả về trên grid"):
            cellid = "HOVATEN"
            results_in_grid = page_common.do_get_data_test_in_grid(cellid)
            print(f"Kết quả trên grid hiển thị: {results_in_grid}")

            time.sleep(3)
            page_base.click_obj(Obj_VuViec.btnEditVuviecGrid)
            time.sleep(2)
            check_result = page_guong_mat_tab_thu_vien.do_verify_result_search_in_popup(type_of, label, value)
            capture_screenshot_and_attach_allure(driver, "CheckResultEdited")
            assert check_result, "Kết quả tìm kiếm không hiển thị chính xác dữ liệu"

    @allure.testcase("c4i2-293", "c4i2-293")
    @allure.story("Tìm kiếm Đối tượng thành công")
    @allure.title("Lọc theo Giới tính")
    @pff.parametrize(path=pathDataTestObjSearch)
    def test_filter_by_gender(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm Gương mặt thành công - Lọc theo Giới tính"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        json_data_handler = JsonDataHandler(Data_Search)
        page_guong_mat_tab_thu_vien = PageGuongMatTabThuVien(driver)
        page_base.show_overlay_text("Search theo Giới tính")

        label_search = "Giới tính"
        type_of, label, value = json_data_handler.get_info_by_label(label_search)

        with allure.step("Kiểm tra danh sách đã load xong trước khi bắt đầu tìm kiếm"):
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
        with allure.step("Lựa chọn option search tại combobox Giới tính"):
            time.sleep(2)
            txt_search_obj = ObjCommon.label_dropdown_list(label_search)
            page_base.select_key_dropdown(txt_search_obj, value)
            capture_screenshot_and_attach_allure(driver, name="EnterObj")
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            time.sleep(1)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
        with allure.step("Kiểm tra Giới tính trong popup chi tiết của kết quả đầu tiên trả về trên grid"):
            cellid = "HOVATEN"
            results_in_grid = page_common.do_get_data_test_in_grid(cellid)
            print(f"Kết quả trên grid hiển thị: {results_in_grid}")

            time.sleep(3)
            page_base.click_obj(Obj_VuViec.btnEditVuviecGrid)
            time.sleep(2)
            check_result = page_guong_mat_tab_thu_vien.do_verify_result_search_in_popup(type_of, label, value)
            capture_screenshot_and_attach_allure(driver, "CheckResultEdited")
            assert check_result, "Kết quả tìm kiếm không hiển thị chính xác dữ liệu"

    @allure.testcase("c4i2-1433", "c4i2-1433")
    @allure.story("Tìm kiếm Đối tượng thành công")
    @allure.title("Lọc theo Quận/ huyện")
    @pff.parametrize(path=pathDataTestObjSearch)
    def test_filter_by_district(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm Gương mặt thành công - Lọc theo Quận/ huyện"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        json_data_handler = JsonDataHandler(Data_Search)
        page_guong_mat_tab_thu_vien = PageGuongMatTabThuVien(driver)
        page_base.show_overlay_text("Search theo Quận/ huyện")

        label_search = "Quận/ huyện"
        type_of, label, value = json_data_handler.get_info_by_label(label_search)

        with allure.step("Kiểm tra danh sách đã load xong trước khi bắt đầu tìm kiếm"):
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
        with allure.step("Lựa chọn option search tại combobox Quận/ huyện"):
            time.sleep(2)
            txt_search_obj = ObjCommon.label_dropdown_list(label_search)
            page_base.select_key_dropdown(txt_search_obj, value)
            capture_screenshot_and_attach_allure(driver, name="EnterObj")
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            time.sleep(1)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
        with allure.step("Kiểm tra Quận/ huyện trong popup chi tiết của kết quả đầu tiên trả về trên grid"):
            cellid = "HOVATEN"
            results_in_grid = page_common.do_get_data_test_in_grid(cellid)
            print(f"Kết quả trên grid hiển thị: {results_in_grid}")

            time.sleep(3)
            page_base.click_obj(Obj_VuViec.btnEditVuviecGrid)
            time.sleep(2)
            check_result = page_guong_mat_tab_thu_vien.do_verify_result_search_in_popup(type_of, label, value)
            capture_screenshot_and_attach_allure(driver, "CheckResultEdited")
            assert check_result, "Kết quả tìm kiếm không hiển thị chính xác dữ liệu"

    @allure.testcase("c4i2-1566", "c4i2-1566")
    @allure.story("Tìm kiếm Đối tượng thành công")
    @allure.title("Lọc theo Xã/ phường")
    @pff.parametrize(path=pathDataTestObjSearch)
    def test_filter_by_wards(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm Gương mặt thành công
        - Tìm kiếm kết hợp (Quận/ huyện + Xã/ phường"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        json_data_handler = JsonDataHandler(Data_Search)
        page_guong_mat_tab_thu_vien = PageGuongMatTabThuVien(driver)
        page_base.show_overlay_text("Tìm kiếm kết hợp")

        label_search_qh = "Quận/ huyện"
        type_of_qh, label_qh, value_qh = json_data_handler.get_info_by_label(label_search_qh)
        label_search_xp = "Xã/ phường"
        type_of_xp, label_xp, value_xp = json_data_handler.get_info_by_label(label_search_xp)

        with allure.step("Kiểm tra danh sách đã load xong trước khi bắt đầu tìm kiếm"):
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
        with allure.step("Lựa chọn option search tại combobox Quận/ huyện"):
            time.sleep(2)
            txt_search_obj = ObjCommon.label_dropdown_list(label_search_qh)
            page_base.select_key_dropdown(txt_search_obj, value_qh)
            capture_screenshot_and_attach_allure(driver, name="EnterObj")
        with allure.step("Lựa chọn option search tại combobox Xã/ phường"):
            time.sleep(2)
            txt_search_obj = ObjCommon.label_dropdown_list(label_search_xp)
            page_base.select_key_dropdown(txt_search_obj, value_xp)
            capture_screenshot_and_attach_allure(driver, name="EnterObj")

        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            time.sleep(1)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
        with allure.step("Nhấn vào icon chi tiết -> Mở popup thông tin"):
            cellid = "HOVATEN"
            results_in_grid = page_common.do_get_data_test_in_grid(cellid)
            print(f"Kết quả trên grid hiển thị: {results_in_grid}")

            time.sleep(3)
            page_base.click_obj(Obj_VuViec.btnEditVuviecGrid)
        with allure.step(
                "Kiểm tra Quận/ huyện trong popup chi tiết của kết quả đầu tiên trả về trên grid"):
            time.sleep(2)
            check_result = page_guong_mat_tab_thu_vien.do_verify_result_search_in_popup(type_of_qh, label_qh, value_qh)
            allure.attach(driver.get_screenshot_as_png(), name="CheckResultEdited",
                          attachment_type=allure.attachment_type.PNG)
            assert check_result, "Kết quả tìm kiếm không hiển thị chính xác dữ liệu"
        with allure.step("Kiểm tra Xã/ phường trong popup chi tiết của kết quả đầu tiên trả về trên grid"):
            time.sleep(2)
            check_result = page_guong_mat_tab_thu_vien.do_verify_result_search_in_popup(type_of_xp, label_xp, value_xp)
            allure.attach(driver.get_screenshot_as_png(), name="CheckResultEdited",
                          attachment_type=allure.attachment_type.PNG)
            assert check_result, "Kết quả tìm kiếm không hiển thị chính xác dữ liệu"
