import os
import tempfile
import requests
import time

import pytest
import allure

from Libraries.Config import Default
from Libraries.Framework.FactoryDrivers import get_chrome_driver
from Libraries.Framework.Paths import Paths
from Libraries.Framework.Utils import PageBase
from Libraries.Plugins.PandasExcel import PandasExcel
from PageObjects.Web.Obj_BienSo import Obj_BienSo
from PageObjects.Web.Obj_Common import ObjCommon
from PageObjects.Web.Obj_Import import Obj_Import, ObjImportFunction
from WebApplications.PageCommon import PageCommon
from WebApplications.PageHome import LoginPage
from WebApplications.PageImport import PageImport
from conftest import capture_screenshot_and_attach_allure, attach_table_to_allure
import parametrize_from_file as pff
from Libraries.Plugins.DataHandler import JsonDataHandler

isDataDeletion = True


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

    page_base.click_obj(Obj_BienSo.iconNhanDangBienSo)
    page_base.click_obj(Obj_BienSo.tabNhapLieu)
    time.sleep(2)

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

    if not is_first_test and save_current_url is not None:
        driver = browser
        driver.get(save_current_url)

    is_first_test = False
    yield


@allure.epic("Nhận dạng BSX")
@allure.feature("Nhập liệu BSX")
@pytest.mark.Import
@pytest.mark.ImportLPR
class Test_Import_BSX:
    pageBase = PageBase(browser)
    pathDataTestImport = pageBase.load_path_data_file_from_path("Datas_Import",
                                                                "Test_ImportBSX.json")

    @allure.testcase("c4i2-791", "c4i2-791")
    @allure.story("Import dữ liệu BSX thành công")
    @allure.title("Xác minh có thể upload file có định dạng excel")
    @pff.parametrize(path=pathDataTestImport)
    def test_ImportBSXSuccess(self, browser, Data, statusImport):
        "Trường hợp kiểm thử Import BSX thành công: Biển số xe thêm mới (chưa có dữ liệu trong hệ thống)"
        driver = browser
        page_base = PageBase(driver)
        json_data_handler = JsonDataHandler(Data)
        page_import = PageImport(driver)
        page_base.show_overlay_text("Trường hợp kiểm thử Import BSX thành công")
        attach_table_to_allure(Data, name="Data Test")
        with allure.step("Nhập liệu file"):
            with allure.step("Chọn loại theo dõi và tải file lên hệ thống"):
                page_base.click_obj(Obj_Import.btnChonTapTin)
                type_of_dropdown, label_dropdown, value_dropdown = json_data_handler.get_info_by_type_of(
                    "dropdown-btn-text")
                page_import.private_fill_file_import(type_of_dropdown, label_dropdown, value_dropdown)

                type_of_file, label_file, value_file = json_data_handler.get_info_by_type_of("file")
                page_import.private_fill_file_import(type_of_file, label_file, value_file)
            with allure.step("Chọn trang tính"):
                page_base.select_key_dropdown(ObjCommon.dropdown_list("Trang tính"), value_file)
            with allure.step("Nhấn xác nhận tải file"):
                page_base.click_obj(ObjCommon.button_with_text("Xác nhận"))
                page_base.click_obj(ObjCommon.element_text(label_file))
                capture_screenshot_and_attach_allure(driver, name="UploadFile")
            with allure.step("Nhấn bắt đầu import file"):
                page_base.click_obj(ObjCommon.button_with_text("Tạo mới"))
                page_base.click_obj(ObjCommon.button_with_text("Xác nhận"))
            with allure.step("Xác minh trạng thái nhập liệu của file"):
                check_status = page_import.do_verify_import_status(label_file, statusImport)
                assert check_status, "Trạng thái import không chính xác"
                capture_screenshot_and_attach_allure(driver, "VerifyStatus")
        with allure.step("Xác minh dữ liệu được nhập liệu"):
            with allure.step("Điều hướng đến thư viện"):
                page_base.click_obj(Obj_BienSo.tabThuVien)
            with allure.step("Tìm kiếm dữ liệu đã nhập liệu"):
                page_base.select_key_dropdown(ObjCommon.dropdown_list(label_dropdown), value_dropdown)
                page_base.click_obj(ObjCommon.button_with_text("Tìm kiếm"))
                time.sleep(1)
            with allure.step("Kiểm tra kết quả tìm kiếm trên danh sách lưới"):
                txt_input = '//div[@cellid]'
                check_exit_in_grid = page_base.check_element_visibility(txt_input)
                assert check_exit_in_grid, "Không tìm thấy kết quả đã tạo trên danh sách lưới"
                capture_screenshot_and_attach_allure(driver, "VerifyData")
        with allure.step("Xóa dữ liệu đã nhập liệu"):
            if isDataDeletion:
                with allure.step("Xóa file import"):
                    page_base.click_obj(Obj_BienSo.tabNhapLieu)
                    page_base.click_obj(ObjImportFunction.icon_in_file(label_file, "fa-trash-alt"))
                    page_base.click_obj(ObjCommon.button_with_text("Xác nhận"))
                    page_base.click_obj(ObjCommon.button_with_text("Xác nhận"))
                    page_base.wait_for_page_load()
                    check_exits_file = page_base.check_element_visibility(ObjCommon.element_text(label_file))
                    assert not check_exits_file, "File Import sau khi xóa vẫn tồn tại (Loading)"
                with allure.step("Kiểm tra dữ liệu ở thư viện"):
                    page_base.click_obj(Obj_BienSo.tabThuVien)
                    page_base.click_obj(ObjCommon.button_with_text("Đặt lại"))
                    page_base.select_key_dropdown(ObjCommon.dropdown_list(label_dropdown), value_dropdown)
                    page_base.click_obj(ObjCommon.button_with_text("Tìm kiếm"))
                with allure.step("Kiểm tra kết quả tìm kiếm trên danh sách lưới"):
                    txt_input = '//div[@cellid]'
                    check_exit_in_grid = page_base.check_element_visibility(txt_input, wait_time=5)
                    assert not check_exit_in_grid, "Vẫn tồn tại dữ liệu sau khi clean data"
            else:
                with allure.step("Dữ liệu sau khi thực hiện kiểm thử vẫn tồn tại"):
                    pass
