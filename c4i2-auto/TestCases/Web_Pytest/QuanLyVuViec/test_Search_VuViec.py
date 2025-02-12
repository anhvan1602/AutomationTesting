import time
import pytest
import allure

from allure_commons.types import AttachmentType
from Libraries.Framework.FactoryDrivers import get_chrome_driver
from Libraries.Framework.Utils import PageBase
from Libraries.Config import Default
from PageObjects.Web.Obj_VuViec import Obj_VuViec
from PageObjects.Web.Obj_Common import ObjCommon
from WebApplications.PageCommon import PageCommon
from WebApplications.PageHome import LoginPage
from WebApplications.PageVuViec import CaseManagement, CaseManagementTabVuViec
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
pathDataTestSearchCase = pageBase.load_path_data_file_from_path("Datas_Case",
                                                           "Test_Search_VuViec.json")


@pff.parametrize(path=pathDataTestSearchCase, key="create_data_search")
def setup_data_search(Data, Data_UpdateObj):
    value_data = Data
    value_data_updateobj = Data_UpdateObj
    return value_data, value_data_updateobj


@pytest.fixture(scope='class', autouse=True)
def create_data(browser, data=setup_data_search):
    driver = browser
    page_base = PageBase(driver)
    page_guong_mat = CaseManagement(driver)
    page_vu_viec = CaseManagement(driver)

    Data = data.pytestmark[0].args[1][0].values[0]
    data_update_obj = data.pytestmark[0].args[1][0].values[1]

    page_base.click_obj(Obj_VuViec.btnTaoVuViec)
    page_guong_mat.do_dien_thong_tin_vu_viec(Data)

    # Thêm đối tượng vào vụ việc

    page_base.click_obj(Obj_VuViec.btnDanhSachDoiTuong)
    page_vu_viec.do_dien_thong_tin_doi_tuong(data_update_obj)

    time.sleep(2)
    page_base.click_obj(Obj_VuViec.btnLuuDoiTuong)

    page_base.click_obj(Obj_VuViec.btnSubmitVuViec)
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
@pytest.mark.CaseSearch
@pytest.mark.Add_DataList
class Test_CaseLibrarySearch:

    @allure.testcase("c4i2-", "c4i2-")
    @allure.story("Xác minh có hiển thị dữ liệu tại danh sách vụ việc")
    @allure.title("Kiểm tra dữ liệu vụ việc tại danh sách lưới")
    def test_displayed_data_in_case_list(self, browser):
        """Trường hợp kiểm thử kiểm tra có dữ liệu vụ việc hiển thị tại danh sách lưới"""
        driver = browser
        page_base = PageBase(driver)
        page_base.show_overlay_text("Verify data in Grid")
        with allure.step("Kiểm tra có data trên grid hay không"):
            verify = page_base.check_element_visibility(Obj_VuViec.xpathIDCase)
            capture_screenshot_and_attach_allure(driver, "DataInGrid")
            assert verify, "Không có dữ liệu trên grid"
        with allure.step("In ra ID các Vụ việc đang hiển th trên danh sách lưới"):
            try:
                xpath_routes = page_base.get_text_element(Obj_VuViec.xpathIDCase, multiple=True)
                allure.attach(f"{xpath_routes}",
                              attachment_type=AttachmentType.TEXT)
            except Exception as e:
                allure.attach(f"Không thể tìm thấy data: {e}", name="Error",
                              attachment_type=AttachmentType.TEXT)

    @allure.testcase("c4i2-284", "c4i2-284")
    @allure.story("Tìm kiếm Vụ việc thành công")
    @allure.title("Tìm với Đơn vị tạo")
    @pff.parametrize(path=pathDataTestSearchCase)
    def test_search_by_agency_success(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm Vụ việc thành công - Search Đơn vị tạo"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_base.show_overlay_text("Search Cơ quan tạo")

        label_search = "Đơn vị tạo"
        json_data_handler = JsonDataHandler(Data_Search)
        type_of_search, label_search, value_search = json_data_handler.get_info_by_label(label_search)

        with allure.step("Kiểm tra danh sách đã load xong trước khi bắt đầu tìm kiếm"):
            page_base.wait_for_page_load()
        with allure.step("Mở rộng thông tin danh sách lưới"):
            time.sleep(2)
            page_base.click_obj(Obj_VuViec.btnMoRongGrid)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="ExtendGrid")
        with allure.step("Nhập thông tin Cơ quan tạo vào tab Tìm kiếm"):
            time.sleep(2)
            page_base.send_key_input(ObjCommon.search_textbox(label_search), value_search)
            capture_screenshot_and_attach_allure(driver, name="EnterAgency")
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
        with allure.step("Kiểm tra Đơn vị tạo của tất cả kết quả trả về trên grid"):
            time.sleep(2)
            page_base.wait_for_page_load()
            cellid = "ID_CANBO"
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, value_search)
            capture_screenshot_and_attach_allure(driver, name="VerifyInGrid")
            assert result, f"Trên danh sách lưới có giá trị: '{different_value}' khác với giá trị mong muốn: '{value_search}'"

    @allure.testcase("c4i2-287", "c4i2-287")
    @allure.story("Tìm kiếm Vụ việc thành công")
    @allure.title("Tìm với Trạng thái vụ việc")
    @pff.parametrize(path=pathDataTestSearchCase)
    def test_search_by_status_success(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm Vụ việc thành công - Search Trạng thái vụ việc"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        case_management_tab_vu_viec = CaseManagementTabVuViec(driver)
        page_base.show_overlay_text("Search Trạng thái")

        label_search = "Trạng thái"
        json_data_handler = JsonDataHandler(Data_Search)
        type_of_search, label_search, value_search = json_data_handler.get_info_by_label(label_search)

        with allure.step("Kiểm tra danh sách đã load xong trước khi bắt đầu tìm kiếm"):
            page_base.wait_for_page_load()
        with allure.step("Nhập thông tin Trạng thái vào tab Tìm kiếm"):
            time.sleep(2)
            txt_search_bsx = ObjCommon.label_dropdown_list(label_search)
            page_base.select_key_dropdown(txt_search_bsx, value_search)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="EnterStatus")
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            time.sleep(1)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
        with allure.step("Kiểm tra Trạng thái của tất cả kết quả trả về trên grid"):
            time.sleep(2)
            cellid = "TRANGTHAI"
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, value_search)
            capture_screenshot_and_attach_allure(driver, name="VerifyInGrid")
            assert result, f"Trên danh sách lưới có giá trị: '{different_value}' khác với giá trị mong muốn: '{value_search}"
        with allure.step("Kiểm tra Trạng thái trong popup chi tiết của kết quả đầu tiên trả về trên grid"):
            time.sleep(3)
            page_base.click_obj(Obj_VuViec.btnEditVuviecGrid)
            time.sleep(2)
            check_result = case_management_tab_vu_viec.do_verify_result_search_in_popup(type_of_search, label_search, value_search)
            capture_screenshot_and_attach_allure(driver, "CheckResultEdited")
            assert check_result, "Kết quả tìm kiếm không hiển thị chính xác dữ liệu"

    @allure.testcase("c4i2-286", "c4i2-286")
    @allure.story("Tìm kiếm Vụ việc thành công")
    @allure.title("Tìm với Quận/huyện")
    @pff.parametrize(path=pathDataTestSearchCase)
    def test_search_by_district_success(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm Vụ việc thành công - Search Quận/huyện"""
        driver = browser
        page_base = PageBase(driver)
        case_management_tab_vu_viec = CaseManagementTabVuViec(driver)
        page_base.show_overlay_text("Search Quận/huyện")

        label_search = "Quận/ huyện"
        json_data_handler = JsonDataHandler(Data_Search)
        type_of_search, label_search, value_search = json_data_handler.get_info_by_label(label_search)

        with allure.step("Kiểm tra danh sách đã load xong trước khi bắt đầu tìm kiếm"):
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
        with allure.step("Nhập thông tin Quận/huyện vào tab Tìm kiếm"):
            time.sleep(2)
            txt_search_bsx = ObjCommon.label_dropdown_list(label_search)
            page_base.select_key_dropdown(txt_search_bsx, value_search)
            capture_screenshot_and_attach_allure(driver, name="EnterDistrict")
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            time.sleep(1)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
        with allure.step("Kiểm tra Quận/ huyện trong popup chi tiết của kết quả đầu tiên trả về trên grid"):
            time.sleep(3)
            page_base.click_obj(Obj_VuViec.btnEditVuviecGrid)
            time.sleep(2)
            check_result = case_management_tab_vu_viec.do_verify_result_search_in_popup(type_of_search, label_search, value_search)
            capture_screenshot_and_attach_allure(driver, "CheckResultEdited")
            assert check_result, "Kết quả tìm kiếm không hiển thị chính xác dữ liệu"

    @allure.testcase("c4i2-286", "c4i2-286")
    @allure.story("Tìm kiếm Vụ việc thành công")
    @allure.title("Tìm với Xã/phường")
    @pff.parametrize(path=pathDataTestSearchCase)
    def test_search_by_commune_success(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm Vụ việc thành công - Search Xã/phường"""
        driver = browser
        page_base = PageBase(driver)
        case_management_tab_vu_viec = CaseManagementTabVuViec(driver)
        page_base.show_overlay_text("Search Xã/phường")

        json_data_handler = JsonDataHandler(Data_Search)
        label_search_qh = "Quận/ huyện"
        type_of_search_qh, label_search_qh, value_search_qh = json_data_handler.get_info_by_label(label_search_qh)
        label_search_xp = "Xã/ phường"
        type_of_search_xp, label_search_xp, value_search_xp = json_data_handler.get_info_by_label(label_search_xp)

        with allure.step("Kiểm tra danh sách đã load xong trước khi bắt đầu tìm kiếm"):
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
        with allure.step("Nhập thông tin Quận/huyện, Xã/phường vào tab Tìm kiếm"):
            time.sleep(2)
            txt_search_bsx = ObjCommon.label_dropdown_list(label_search_qh)
            page_base.select_key_dropdown(txt_search_bsx, value_search_qh)
            time.sleep(2)
            txt_search_bsx = ObjCommon.label_dropdown_list(label_search_xp)
            page_base.select_key_dropdown(txt_search_bsx, value_search_xp)
            capture_screenshot_and_attach_allure(driver, name="EnterCommune")
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            time.sleep(1)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
        with allure.step("Kiểm tra Xã phường trong popup chi tiết của kết quả đầu tiên trả về trên grid"):
            time.sleep(3)
            page_base.click_obj(Obj_VuViec.btnEditVuviecGrid)
            time.sleep(2)
            check_result = case_management_tab_vu_viec.do_verify_result_search_in_popup(type_of_search_xp, label_search_xp,
                                                                                    value_search_xp)
            capture_screenshot_and_attach_allure(driver, "CheckResultEdited")
            assert check_result, "Kết quả tìm kiếm không hiển thị chính xác dữ liệu"

    @pytest.mark.DC
    @allure.testcase("c4i2-282", "c4i2-282")
    @allure.story("Tìm kiếm Vụ việc thành công")
    @allure.title("Tìm với Tên đối tượng")
    @pff.parametrize(path=pathDataTestSearchCase)
    def test_search_by_subject_name_success(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm Vụ việc thành công - Search Tên đối tượng"""
        driver = browser
        page_base = PageBase(driver)
        case_management_tab_vu_viec = CaseManagementTabVuViec(driver)
        page_base.show_overlay_text("Search Tên đối tượng")

        label_search = "Đối tượng"
        json_data_handler = JsonDataHandler(Data_Search)
        type_of_search, label_search, value_search = json_data_handler.get_info_by_label(label_search)

        with allure.step("Kiểm tra danh sách đã load xong trước khi bắt đầu tìm kiếm"):
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
        with allure.step("Nhập thông tin Tên đối tượng vào tab Tìm kiếm"):
            time.sleep(2)
            page_base.send_key_input(ObjCommon.search_textbox("Tên đối tượng"), value_search)
            capture_screenshot_and_attach_allure(driver, name="EnterNameObj")
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            time.sleep(1)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
        with allure.step("Kiểm tra Tên đối tượng trong popup chi tiết của kết quả đầu tiên trả về trên grid"):
            time.sleep(3)
            page_base.click_obj(Obj_VuViec.btnEditVuviecGrid)
            time.sleep(2)
            check_result = case_management_tab_vu_viec.do_verify_result_search_in_popup(type_of_search, label_search, value_search)
            capture_screenshot_and_attach_allure(driver, "CheckResultEdited")
            assert check_result, "Kết quả tìm kiếm không hiển thị chính xác dữ liệu"

    @allure.testcase("c4i2-283", "c4i2-283")
    @allure.story("Tìm kiếm Vụ việc thành công")
    @allure.title("Tìm với CNMD/CCCD/Hộ chiếu đối tượng")
    @pff.parametrize(path=pathDataTestSearchCase)
    def test_search_by_subject_id_card_success(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm Vụ việc thành công - Search CNMD/CCCD/Hộ chiếu đối tượng"""
        driver = browser
        page_base = PageBase(driver)
        case_management_tab_vu_viec = CaseManagementTabVuViec(driver)
        page_base.show_overlay_text("Search CNMD/CCCD/Hộ chiếu đối tượng")

        label_search = "CMND / CCCD / Hộ chiếu đối tượng"
        json_data_handler = JsonDataHandler(Data_Search)
        type_of_search, label_search, value_search = json_data_handler.get_info_by_label(label_search)

        with allure.step("Kiểm tra danh sách đã load xong trước khi bắt đầu tìm kiếm"):
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
        with allure.step("Nhập thông tin CMND vào tab Tìm kiếm"):
            time.sleep(2)
            page_base.send_key_input(ObjCommon.search_textbox(label_search), value_search)
            capture_screenshot_and_attach_allure(driver, name="EnterID")
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            time.sleep(1)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
        with allure.step(
                "Kiểm tra Tên đối tượng có CMND đã search trong popup chi tiết của kết quả đầu tiên trả về trên grid"):
            time.sleep(3)
            page_base.click_obj(Obj_VuViec.btnEditVuviecGrid)
            page_base.wait_for_page_load()
            label_search = "Đối tượng"
            type_of, label, value = json_data_handler.get_info_by_label(label_search)
            check_result = case_management_tab_vu_viec.do_verify_result_search_in_popup(type_of, label, value)
            capture_screenshot_and_attach_allure(driver, "CheckResultEdited")
            assert check_result, "Kết quả tìm kiếm không hiển thị chính xác dữ liệu"

    @allure.testcase("c4i2-", "c4i2-")
    @allure.story("Tìm kiếm Vụ việc thành công")
    @allure.title("Nhấn Đặt lại (danh sách load về mặc định, các giá trị lọc bị remove)")
    @pff.parametrize(path=pathDataTestSearchCase)
    def test_reset_button_behavior(self, browser, Data_Search):
        """Trường hợp kiểm thử nhấn Đặt lại (danh sách load về mặc định, các giá trị lọc bị remove)"""
        driver = browser
        page_base = PageBase(driver)
        case_management_tab_vu_viec = CaseManagementTabVuViec(driver)
        page_base.show_overlay_text("Kiểm thử nhấn đặt lại")

        label_search = "Đối tượng"
        json_data_handler = JsonDataHandler(Data_Search)
        type_of_search, label_search, value_search = json_data_handler.get_info_by_label(label_search)

        with allure.step("Kiểm tra danh sách đã load xong trước khi bắt đầu tìm kiếm"):
            page_base.wait_for_page_load()
        with allure.step("Nhập thông tin Tên đối tượng vào tab Tìm kiếm"):
            time.sleep(2)
            page_base.send_key_input(ObjCommon.search_textbox("Tên đối tượng"), value_search)
            capture_screenshot_and_attach_allure(driver, name="EnterDistrict")
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            time.sleep(1)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
        with allure.step("Nhấn vào button Đặt lại"):
            page_base.click_obj(Obj_VuViec.btnReset)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="Reset")
        with allure.step("Kiểm tra giá trị đã nhập/chọn"):
            result = case_management_tab_vu_viec.do_verify_data_cleaned(ObjCommon.search_textbox("Tên đối tượng"))
            capture_screenshot_and_attach_allure(driver, name="CheckReset")
            assert result, "Resert giá trị nhập không thành công"

    @pytest.mark.DC
    @allure.testcase("c4i2-280", "c4i2-280")
    @allure.story("Tìm kiếm Vụ việc thành công")
    @allure.title("Tìm với Tên vụ việc")
    @pff.parametrize(path=pathDataTestSearchCase)
    def test_search_by_case_name(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm Vụ việc thành công - Search Tên Vụ việc"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_base.show_overlay_text("Search Tên vụ việc")

        label_search = "Tên vụ việc"
        json_data_handler = JsonDataHandler(Data_Search)
        type_of_search, label_search, value_search = json_data_handler.get_info_by_label(label_search)

        with allure.step("Kiểm tra danh sách đã load xong trước khi bắt đầu tìm kiếm"):
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
        with allure.step("Nhập thông tin tên Vụ việc tại textbox Tên Vụ việc tại tab Tìm kiếm"):
            time.sleep(2)
            page_base.send_key_input(ObjCommon.search_textbox(label_search), value_search)
            capture_screenshot_and_attach_allure(driver, name="EnterCaseName")
            allure.attach(f"{label_search} : {value_search}", name="Data Test",
                          attachment_type=allure.attachment_type.TEXT)
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
        with allure.step("Kiểm tra Tên vụ việc của tất cả kết quả trả về trên grid"):
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
            time.sleep(2)
            cellid = "TENVUVIEC"
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, value_search)
            capture_screenshot_and_attach_allure(driver, name="VerifyInGrid")
            assert result, f"Trên danh sách lưới có giá trị: '{different_value}' khác với giá trị mong muốn: '{value_search}"

    @allure.testcase("c4i2-", "c4i2-")
    @allure.story("Tìm kiếm Vụ việc thành công")
    @allure.title("Tìm với free search")
    @pff.parametrize(path=pathDataTestSearchCase, key="test_search_by_case_name")
    def test_search_with_free_search(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm Vụ việc thành công - Free Search (search với tên vụ việc)"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_base.show_overlay_text("Free Search")

        label_search = "Tên vụ việc"
        json_data_handler = JsonDataHandler(Data_Search)
        type_of_search, label_search, value_search = json_data_handler.get_info_by_label(label_search)

        with allure.step("Kiểm tra danh sách đã load xong trước khi bắt đầu tìm kiếm"):
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
        with allure.step("Nhập thông tin tên Vụ việc vào trường free search tại tab Tìm kiếm"):
            time.sleep(2)
            page_base.send_key_input(Obj_VuViec.txtSearchVuViec, value_search)
            capture_screenshot_and_attach_allure(driver, name="EnterCaseName")
            allure.attach(f"{label_search} : {value_search}", name="Data Test",
                          attachment_type=allure.attachment_type.TEXT)
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
        with allure.step("Kiểm tra Tên vụ việc của tất cả kết quả trả về trên grid"):
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
            time.sleep(2)
            cellid = "TENVUVIEC"
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, value_search)
            capture_screenshot_and_attach_allure(driver, name="VerifyInGrid")
            assert result, f"Trên danh sách lưới có giá trị: '{different_value}' khác với giá trị mong muốn: '{value_search}"

    @allure.testcase("c4i2-281", "c4i2-281")
    @allure.story("Tìm kiếm Vụ việc thành công")
    @allure.title("Tìm bằng ID Đối tượng")
    @pff.parametrize(path=pathDataTestSearchCase)
    def test_search_by_object_id(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm Vụ việc thành công - Tìm bằng ID Đối tượng"""
        driver = browser
        page_base = PageBase(driver)
        case_management_tab_vu_viec = CaseManagementTabVuViec(driver)
        page_base.show_overlay_text("Search ID đối tượng")
        json_data_handler = JsonDataHandler(Data_Search)
        label_search = "Id đối tượng"
        type_of_search, label_search, value_search = json_data_handler.get_info_by_label(label_search)

        with allure.step("Kiểm tra danh sách đã load xong trước khi bắt đầu tìm kiếm"):
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
        with allure.step("Nhập thông tin ID Đối tượng vào textbox ID Đối tượng"):
            time.sleep(2)
            page_base.send_key_input(ObjCommon.search_textbox(label_search), value_search)
            allure.attach(f"{label_search} : {value_search}", name="Data Test",
                          attachment_type=allure.attachment_type.TEXT)
            capture_screenshot_and_attach_allure(driver, name="EnterID")

        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            time.sleep(1)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
        with allure.step(
                "Kiểm tra Tên đối tượng có CMND đã search trong popup chi tiết của kết quả đầu tiên trả về trên grid"):
            time.sleep(3)
            page_base.click_obj(Obj_VuViec.btnEditVuviecGrid)
            time.sleep(2)
            label_search = "Đối tượng"
            type_of_search, label_search, value_search = json_data_handler.get_info_by_label(label_search)
            check_result = case_management_tab_vu_viec.do_verify_result_search_in_popup(type_of_search, label_search, value_search)
            capture_screenshot_and_attach_allure(driver, "CheckResultEdited")
            assert check_result, "Kết quả tìm kiếm không hiển thị chính xác dữ liệu"

    @allure.testcase("c4i2-285", "c4i2-285")
    @allure.story("Tìm kiếm Vụ việc thành công")
    @allure.title("Tìm với Lĩnh vực")
    @pff.parametrize(path=pathDataTestSearchCase)
    def test_search_with_field(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm Vụ việc thành công - Tìm với Lĩnh vực"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        case_management_tab_vu_viec = CaseManagementTabVuViec(driver)
        page_base.show_overlay_text("Search Lĩnh Vực")

        label_search = "Lĩnh vực"
        json_data_handler = JsonDataHandler(Data_Search)
        type_of_search, label_search, value_search = json_data_handler.get_info_by_label(label_search)

        with allure.step("Kiểm tra danh sách đã load xong trước khi bắt đầu tìm kiếm"):
            page_base.wait_for_page_load()
        with allure.step("Mở rộng thông tin danh sách lưới"):
            time.sleep(2)
            page_base.click_obj(Obj_VuViec.btnMoRongGrid)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="ExtendGrid")
        with allure.step("Lựa chọn option search tại combobox Lĩnh vực"):
            time.sleep(2)
            txt_search_bsx = ObjCommon.label_dropdown_list(label_search)
            page_base.select_key_dropdown(txt_search_bsx, value_search)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="EnterStatus")
            allure.attach(f"{label_search} : {value_search}", name="Data Test",
                          attachment_type=allure.attachment_type.TEXT)
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            time.sleep(1)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
        with allure.step("Kiểm tra Lĩnh vực của tất cả kết quả trả về trên grid"):
            time.sleep(2)
            cellid = "PHANLOAI"
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, value_search)
            capture_screenshot_and_attach_allure(driver, name="VerifyInGrid")
            assert result, f"Trên danh sách lưới có giá trị: '{different_value}' khác với giá trị mong muốn: '{value_search}"
        with allure.step("Kiểm tra Lĩnh vực trong popup chi tiết của kết quả đầu tiên trả về trên grid"):
            time.sleep(3)
            page_base.click_obj(Obj_VuViec.btnEditVuviecGrid)
            time.sleep(2)
            check_result = case_management_tab_vu_viec.do_verify_result_search_in_popup(type_of_search, label_search, value_search)
            capture_screenshot_and_attach_allure(driver, "CheckResultEdited")
            assert check_result, "Kết quả tìm kiếm không hiển thị chính xác theo lĩnh vực mong muốn"

    @allure.testcase("c4i2-285", "c4i2-285")
    @allure.story("Tìm kiếm Vụ việc thành công")
    @allure.title("Tìm với Loại vụ việc")
    @pff.parametrize(path=pathDataTestSearchCase)
    def test_search_by_category(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm Vụ việc thành công - Tìm với Loại vụ việc"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        case_management_tab_vu_viec = CaseManagementTabVuViec(driver)
        page_base.show_overlay_text("Search Loại vụ việc")

        json_data_handler = JsonDataHandler(Data_Search)
        label_search = "Lĩnh vực"
        type_of_search_lv, label_search_lv, value_search_lv = json_data_handler.get_info_by_label(label_search)
        label_search = "Loại vụ việc"
        type_of_search_lvv, label_search_lvv, value_search_lvv = json_data_handler.get_info_by_label(label_search)

        with allure.step("Kiểm tra danh sách đã load xong trước khi bắt đầu tìm kiếm"):
            page_base.wait_for_page_load()
        with allure.step("Mở rộng thông tin danh sách lưới"):
            time.sleep(2)
            page_base.click_obj(Obj_VuViec.btnMoRongGrid)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="ExtendGrid")
        with allure.step("Lựa chọn option search tại combobox Lĩnh vực"):
            time.sleep(2)
            txt_search_bsx = ObjCommon.label_dropdown_list(label_search_lv)
            page_base.select_key_dropdown(txt_search_bsx, value_search_lv)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="EnterStatus")
            allure.attach(f"{label_search_lvv} : {value_search_lvv}", name="Data Test",
                          attachment_type=allure.attachment_type.TEXT)
        with allure.step("Lựa chọn option search tại combobox Loại vụ việc"):
            time.sleep(2)
            txt_search_bsx = ObjCommon.label_dropdown_list(label_search_lvv)
            page_base.select_key_dropdown(txt_search_bsx, value_search_lvv)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="EnterStatus")
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            time.sleep(1)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
        with allure.step("Kiểm tra Lĩnh vực của tất cả kết quả trả về trên grid"):
            time.sleep(2)
            cellid = "PHANLOAI"
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, value_search_lv)
            capture_screenshot_and_attach_allure(driver, name="VerifyInGrid")
            assert result, f"Trên danh sách lưới có giá trị: '{different_value}' khác với giá trị mong muốn: '{value_search_lv}"
        with allure.step("Kiểm tra Loại vụ việc trong popup chi tiết của kết quả đầu tiên trả về trên grid"):
            time.sleep(3)
            page_base.click_obj(Obj_VuViec.btnEditVuviecGrid)
            time.sleep(2)
            check_result = case_management_tab_vu_viec.do_verify_result_search_in_popup(type_of_search_lvv, label_search_lvv,
                                                                                    value_search_lvv)
            capture_screenshot_and_attach_allure(driver, "CheckResultEdited")
            assert check_result, "Kết quả tìm kiếm không hiển thị chính xác theo lĩnh vực mong muốn"

    @allure.testcase("c4i2-287", "c4i2-287")
    @allure.story("Tìm kiếm Vụ việc thành công")
    @allure.title("Tìm với Tính chất vụ việc")
    @pff.parametrize(path=pathDataTestSearchCase)
    def test_search_with_case_behavior(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm Vụ việc thành công - Tìm với Tính chất vụ việc"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        case_management_tab_vu_viec = CaseManagementTabVuViec(driver)
        page_base.show_overlay_text("Search Tính chất vụ việc")

        json_data_handler = JsonDataHandler(Data_Search)
        label_search = "Tính chất vụ việc"
        type_of_search, label_search, value_search = json_data_handler.get_info_by_label(label_search)

        with allure.step("Kiểm tra danh sách đã load xong trước khi bắt đầu tìm kiếm"):
            page_base.wait_for_page_load()
        with allure.step("Mở rộng thông tin danh sách lưới"):
            time.sleep(2)
            page_base.click_obj(Obj_VuViec.btnMoRongGrid)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="ExtendGrid")
        with allure.step("Lựa chọn option search tại combobox Tính chất vụ việc"):
            time.sleep(2)
            txt_search_bsx = ObjCommon.label_dropdown_list(label_search)
            page_base.select_key_dropdown(txt_search_bsx, value_search)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="EnterStatus")
            allure.attach(f"{label_search} : {value_search}", name="Data Test",
                          attachment_type=allure.attachment_type.TEXT)
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            time.sleep(1)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
        with allure.step("Kiểm tra Tính chất vụ việc của tất cả kết quả trả về trên grid"):
            time.sleep(2)
            cellid = "TINHCHATVUVIEC"
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, value_search)
            capture_screenshot_and_attach_allure(driver, name="VerifyInGrid")
            assert result, f"Trên danh sách lưới có giá trị: '{different_value}' khác với giá trị mong muốn: '{value_search}"
        with allure.step("Kiểm tra Tính chất vụ việc trong popup chi tiết của kết quả đầu tiên trả về trên grid"):
            time.sleep(3)
            page_base.click_obj(Obj_VuViec.btnEditVuviecGrid)
            time.sleep(2)
            check_result = case_management_tab_vu_viec.do_verify_result_search_in_popup(type_of_search, label_search, value_search)
            capture_screenshot_and_attach_allure(driver, "CheckResultEdited")
            assert check_result, "Kết quả tìm kiếm không hiển thị chính xác theo tính chất vụ việc mong muốn"

    @allure.testcase("c4i2-1416", "c4i2-1416")
    @allure.story("Tìm kiếm Vụ việc thành công")
    @allure.title("Tìm với khoảng thời gian tạo vụ việc")
    @pff.parametrize(path=pathDataTestSearchCase)
    def test_filter_by_time_range_success(self, browser, startTime, endTime):
        """Trường hợp kiểm thử Tìm kiếm Vụ việc thành công - Lọc theo khoảng thời gian"""
        driver = browser
        page_base = PageBase(driver)
        case_management_tab_vu_viec = CaseManagementTabVuViec(driver)
        page_base.show_overlay_text("Search theo Khoảng thời gian")

        from_time = startTime
        to_time = endTime

        with allure.step("Kiểm tra danh sách đã load xong trước khi bắt đầu tìm kiếm"):
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
        with allure.step("Mở rộng thông tin danh sách lưới"):
            time.sleep(2)
            page_base.click_obj(Obj_VuViec.btnMoRongGrid)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="ExtendGrid")
        with allure.step("Check vào checkbox lọc theo Khoảng thời gian - Tìm theo thời gian"):
            xpathchecksearch = ObjCommon.checkbox_button("Tìm theo thời gian tạo vụ việc")
            page_base.click_obj(xpathchecksearch)
            capture_screenshot_and_attach_allure(driver, "CheckBox")
        with allure.step("Thiết lập khoảng thời gian bắt đầu"):
            txt_search_time = ObjCommon.txt_search_time("Từ")
            txt_search_time = f"({txt_search_time})[1]"
            input_search_time = ObjCommon.input_search_time("Từ")
            page_base.click_obj(txt_search_time)
            page_base.send_key_input(input_search_time, startTime)
            time.sleep(1)
            page_base.click_obj(Obj_VuViec.btnMoRongGrid)
            capture_screenshot_and_attach_allure(driver, "SetTime")
        with allure.step("Thiết lập khoảng thời gian kết thúc"):
            txt_search_time = ObjCommon.txt_search_time("Đến")
            txt_search_time = f"({txt_search_time})[1]"
            input_search_time = ObjCommon.input_search_time("Đến")
            page_base.click_obj(txt_search_time)
            page_base.send_key_input(input_search_time, endTime)
            time.sleep(1)
            page_base.click_obj(Obj_VuViec.btnMoRongGrid)
            capture_screenshot_and_attach_allure(driver, "SetTime")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.wait_for_page_load()
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="TimBSX")
        with allure.step("Kiểm tra thời gian phát hiện các kết quả trả về trên danh sách lưới"):
            capture_screenshot_and_attach_allure(driver, name="ResultInGrid")
            cellid = 'NGAYTAO'
            result = case_management_tab_vu_viec.do_verify_time_range_case(cellid, from_time, to_time)
            assert result, f"Hiển thị danh sách kết quả lọc theo khoảng thời gian không hợp lệ"

    @allure.testcase("c4i2-1415", "c4i2-1415")
    @allure.story("Tìm kiếm Vụ việc thành công")
    @allure.title("Tìm kiếm kết hợp")
    @pff.parametrize(path=pathDataTestSearchCase)
    def test_search_combined(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm Vụ việc thành công - Search kết hợp (Tên đối tượng, ID đối tượng)"""
        driver = browser
        page_base = PageBase(driver)
        case_management_tab_vu_viec = CaseManagementTabVuViec(driver)
        page_base.show_overlay_text("Search kết hợp")

        json_data_handler = JsonDataHandler(Data_Search)

        with allure.step("Kiểm tra danh sách đã load xong trước khi bắt đầu tìm kiếm"):
            page_base.check_element_visibility(Obj_VuViec.xpathElementInGrid)
        with allure.step("Nhập thông tin Tên đối tượng vào tab Tìm kiếm"):
            time.sleep(2)
            label_search = "Đối tượng"
            type_of_search, label_search, value_search = json_data_handler.get_info_by_label(label_search)
            page_base.send_key_input(ObjCommon.search_textbox("Tên đối tượng"), value_search)
            capture_screenshot_and_attach_allure(driver, name="EnterNameObj")

        with allure.step("Nhập thông tin ID Đối tượng vào textbox ID Đối tượng"):
            time.sleep(2)
            label_search = "Id đối tượng"
            type_of, label, value = json_data_handler.get_info_by_label(label_search)
            page_base.send_key_input(ObjCommon.search_textbox(label), value)
            allure.attach(f"{label} : {value}", name="Data Test",
                          attachment_type=allure.attachment_type.TEXT)
            capture_screenshot_and_attach_allure(driver, name="EnterID")
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            time.sleep(1)
            page_base.click_obj(Obj_VuViec.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
        with allure.step("Kiểm tra Tên đối tượng trong popup chi tiết của kết quả đầu tiên trả về trên grid"):
            time.sleep(3)
            page_base.click_obj(Obj_VuViec.btnEditVuviecGrid)
            time.sleep(2)
            check_result = case_management_tab_vu_viec.do_verify_result_search_in_popup(type_of_search, label_search, value_search)
            allure.attach(driver.get_screenshot_as_png(), name="CheckResultEdited",
                          attachment_type=allure.attachment_type.PNG)
            assert check_result, "Kết quả tìm kiếm không hiển thị chính xác dữ liệu"
