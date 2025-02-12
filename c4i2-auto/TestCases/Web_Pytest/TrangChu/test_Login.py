import time
import pytest
import allure

from Libraries.Framework.FactoryDrivers import get_chrome_driver
from Libraries.Framework.Utils import PageBase
from Libraries.Config import Default
from WebApplications.PageHome import LoginPage
from conftest import capture_screenshot_and_attach_allure
from WebApplications.PageCommon import PageCommon
from Libraries.Plugins.PandasExcel import PandasExcel
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


fileName = "c4i2_Datas_v1.0.xlsx"


@allure.link(
    "https://vietbando-my.sharepoint.com/:x:/g/personal/vannta_vietbando_vn/EQzmLNznQjpAn5iez9o0Qr8BkeWsfilGCGagIUZ1teg3qQ?e=ZY5q9o",
    name="File TestCase")
@allure.epic("Trang chủ")
@allure.feature("Home")
@allure.story("Xác minh Trang chủ")
class Test_Login:
    pageBase = PageBase(browser)
    pathDataTestHome = pageBase.load_path_data_file_from_path("Datas_TrangChu",
                                                         "Test_Login.json")

    @pytest.mark.Quick_Scan
    @allure.story("Xác minh Trang chủ")
    @allure.title("Kiểm tra hiển thị đầy đủ các tính năng")
    @pff.parametrize(path=pathDataTestHome)
    def test_successful_login_and_display_full_features_EX(self, browser, label_feature, icon_name, icon_url,
                                                           icon_label_feature):
        """Xác minh đăng nhập vào hệ thống thành công.
         Hiển thị đầy đủ các chức năng tại:
         + Trung tâm chỉ huy
         + Quản lý dữ liệu bản đồ
         Xác minh có thể điều hướng chính xác đến từng chức năng
         """

        driver = browser
        page_base = PageBase(driver)
        page_base.show_overlay_text("Kiểm tra hiển thị đầy đủ các tính năng")
        title = f"Kiểm tra hiển thị tính năng: {icon_name}"
        allure.dynamic.title(title)
        with allure.step(f" {label_feature} - {icon_name}"):
            xpath_label_feature = f"//span[contains(@class, 'feature-label') and contains(text(), '{label_feature}')]"
            page_base.click_obj(xpath_label_feature)
            current_url = browser.current_url
            allure.attach(f"URL hiện tại: {current_url}", name="URL hiện tại",
                          attachment_type=allure.attachment_type.TEXT)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, f"Home")

        xpath_icon = f"//img[@alt='{icon_name}']"
        xpath_home = "//i[contains(@class, 'fal fa-house')]"
        xpath_check_exit = f"//*[text()='{icon_label_feature}']"

        with allure.step(f"Kiểm tra có hiển thị icon {icon_name}"):
            check = page_base.check_element_visibility(xpath_icon)
            assert check, f"Không tìm thấy {icon_name}"
        with allure.step(f"Điều hướng đến {icon_name}"):
            page_base.click_obj(xpath_icon)
            time.sleep(5)
        with allure.step(f"Kiểm tra trang web được điều hướng đến"):
            current_url = browser.current_url
            attachment_text = f"Đường dẫn URL: {current_url}, tính năng: {icon_name}"
            assert icon_url in current_url, f"Không điều hướng đến đúng: {icon_name}"
            check_displays_page = page_base.check_element_visibility(xpath_check_exit)
            assert check_displays_page, "Trang chưa hiển thị dữ liệu"
            allure.attach(attachment_text, name="Thông tin Icon: ", attachment_type=allure.attachment_type.TEXT)
            capture_screenshot_and_attach_allure(driver, f"{icon_name}")
            page_base.click_obj(xpath_home)

    @allure.title("Kiểm tra Update Version")
    @pytest.mark.parametrize("sheet_name_check", ["UpdateVersion_Log"])
    @pytest.mark.CheckVersion
    def test_checkUpdateVersion(self, browser, sheet_name_check):
        """Cảnh báo khi có sự thay đổi Phiên bản hoặc Ngày cập nhật"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        path_file = page_common.get_path_file_in_datas(fileName)
        pe = PandasExcel(path_file, sheet_name_check)
        df = pe.get_data_excel()

        page_base.show_overlay_text("Kiểm tra version")
        allure.attach(df.to_string(), name="Data from Excel", attachment_type=allure.attachment_type.TEXT)
        with allure.step(f"Kiểm tra Version"):
            capture_screenshot_and_attach_allure(driver, "CheckVersion")
            label_date = "Ngày cập nhật"
            xpath = f"//div[contains(@class, 'portal-header')]//*[contains(text(), '{label_date}')]//b"
            value_actual_date = str(page_base.get_text_element(xpath))
            value_expected_date = str(df[label_date].iloc[0])

            label_version = "Phiên bản"
            xpath = f"//div[contains(@class, 'portal-header')]//*[contains(text(), '{label_version}')]//b"
            value_actual_version = str(page_base.get_text_element(xpath))
            value_expected_version = str(df[label_version].iloc[0])

            if value_actual_date != value_expected_date or value_actual_version != value_expected_version:
                pe.insert_new_value(label_date, value_actual_date)
                pe.insert_new_value(label_version, value_actual_version)

            assert value_actual_date == value_expected_date and value_actual_version == value_expected_version, \
                f"Update: Ngày cập nhật {value_expected_date} => {value_actual_date}, Phiên bản {value_expected_version} => {value_actual_version}"
