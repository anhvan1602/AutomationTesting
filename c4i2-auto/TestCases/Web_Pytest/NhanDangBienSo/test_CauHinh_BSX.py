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
from conftest import capture_screenshot_and_attach_allure
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
    page_base.click_obj(Obj_BienSo.tabCauHinh)
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
@allure.feature("Cấu hình BSX")
@pytest.mark.LPR
@pytest.mark.Add_DataList
class Test_LPRCauHinh:
    pageBase = PageBase(browser)
    pathDataTestLibraryLpr = pageBase.load_path_data_file_from_path("Datas_LPR",
                                                                    "Test_CauHinh_BSX.json")

    @pytest.mark.UAT_DC
    @allure.testcase("c4i2-775", "c4i2-775")
    @allure.title("c4i2-775: Xác minh có thể tạo loại theo dõi mới")
    @pff.parametrize(path=pathDataTestLibraryLpr)
    def test_creation_of_new_tracking_type(self, browser, Data, expected):
        """Trường hợp kiểm thử xác minh có thể tạo loại theo dõi mới cho biển số xe"""
        driver = browser
        page_base = PageBase(driver)
        page_bien_so_xe = PageBienSoXe(driver)
        page_common = PageCommon(driver)
        time.sleep(1)
        expected_config = expected['value']
        expected_status = expected['status']
        page_base.show_overlay_text("Tạo loại theo dõi mới")
        with allure.step("Nhấn vào button 'Thêm'"):
            page_base.click_obj(Obj_BienSo.btnThemMoiBSX)
            capture_screenshot_and_attach_allure(driver, "ClickButtonCreate")
        with allure.step("Điền thông tin theo dõi"):
            page_bien_so_xe.do_dien_thong_tin_bsx(Data)
            capture_screenshot_and_attach_allure(driver, name="EnterInfo")
        if expected_status:
            with allure.step("Kiểm tra thông báo sau khi tạo"):
                page_base.click_obj(Obj_BienSo.btnLuuThemMoi)
                time.sleep(2)
                check_popup = page_common.verify_notify_popup(expected_config)
                assert check_popup, "Tạo mới theo dõi không thành công"
                capture_screenshot_and_attach_allure(driver, name="NotifySuccess")
        else:
            with allure.step("Kiểm tra thông báo lỗi"):
                page_base.click_obj(Obj_BienSo.btnLuuThemMoi)
                time.sleep(2)
                check_popup = page_common.verify_notify_popup(expected_config)
                assert check_popup, "Không có thông báo lỗi khi nhập trường dữ liệu không hợp lệ"
                capture_screenshot_and_attach_allure(driver, name="MessageErro")

    @pytest.mark.depends(on=['test_creation_of_new_tracking_type'])
    @pytest.mark.UAT_DC
    @allure.testcase("c4i2-778", "c4i2-778")
    @allure.title("c4i2-778: Xác minh có thể xóa loại theo dõi")
    @pff.parametrize(path=pathDataTestLibraryLpr, key="test_creation_of_new_tracking_type")
    def test_delete_tracking_type(self, browser, Data, expected):
        """Trường hợp kiểm thử xác minh có thể xóa loại theo dõi đã tạo"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        time.sleep(1)
        page_base.show_overlay_text("Xóa loại theo dõi")

        label_search = "Tên"
        json_data_handler = JsonDataHandler(Data)
        name_config = json_data_handler.get_value_by_label(label_search)
        expected_status = expected['status']
        if expected_status:
            with allure.step("Check vào checkbox bên trái của loại theo dõi"):
                page_base.do_scroll_mouse_to_element(ObjCommon.item_checkbox(name_config))
                time.sleep(1)
                page_base.click_obj(ObjCommon.item_checkbox(name_config))
                time.sleep(1)
                capture_screenshot_and_attach_allure(driver, "check")
            with allure.step("Nhấn xóa"):
                page_base.click_obj(Obj_BienSo.btnDelete)
                time.sleep(1)
                page_base.click_obj(Obj_BienSo.btnXacNhanXoa)
                time.sleep(1)
                capture_screenshot_and_attach_allure(driver, "DeleteBSX")
            with allure.step("Kiểm tra thông báo sau khi tạo"):
                check_popup = page_common.verify_notify_popup('Xóa thành công')
                assert check_popup, "Tạo mới theo dõi không thành công"
                capture_screenshot_and_attach_allure(driver, name="TimBSX")
        else:
            with allure.step("Không thực hiện hành động xóa vì loại theo dõi không được tạo"):
                capture_screenshot_and_attach_allure(driver, "check")
