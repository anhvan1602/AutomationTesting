import os
import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Libraries.Framework.FactoryDrivers import get_chrome_driver
from Libraries.Framework.Paths import Paths
from Libraries.Framework.Utils import PageBase
from Libraries.Config import Default
from Libraries.Plugins.DataHandler import XMLFileHandler, read_section_from_md
from WebApplications.PageHome import LoginPage
from conftest import capture_screenshot_and_attach_allure


@pytest.fixture(scope='class')
def browser():
    driver = get_chrome_driver()
    driver.implicitly_wait(Default.timeOut)

    default_tenant = Default()
    driver.get(default_tenant.url)

    page_login = LoginPage(driver)
    page_login.do_login(default_tenant.username, default_tenant.password)

    # Lưu URL hiện tại sau khi đăng nhập
    current_url = driver.current_url

    yield driver, current_url
    driver.quit()


@pytest.fixture(scope='function', autouse=True)
def setup_url(browser):
    driver, current_url = browser
    global is_first_test
    # Điều hướng về URL đã lưu nếu không phải test đầu tiên
    if not is_first_test:
        driver.get(current_url)
    is_first_test = False
    yield


is_first_test = True


@pytest.mark.version
class Test_Version:
    @allure.title("Cập nhật web-version vào file environment")
    def test_get_current_version(self, browser):
        driver, _ = browser
        page_base = PageBase(driver)

        # Sử dụng WebDriverWait để chờ các phần tử cần thiết
        version_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"Phiên bản")]'))
        )
        txt_version = version_element.text

        time_release_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"Ngày cập nhật")]'))
        )
        txt_time_release = time_release_element.text

        page_base.show_overlay_text("Điều hướng đến trang chủ")

        # Đường dẫn tới file XML và CHANGELOG.md
        path_file_xml = os.path.join(Paths().get_path_project(), "configAllure", "environment.xml")
        path_file_changelog = os.path.join(Paths().get_path_project(), "CHANGELOG.md")

        # Cập nhật file environment.xml
        handler = XMLFileHandler(path_file_xml)
        try:
            self.update_environment_file(handler, txt_version, txt_time_release, path_file_changelog)
        except AssertionError as e:
            allure.attach(f"Key không lấy được: {str(e)}", name="Lỗi cập nhật version", attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"Không thể cập nhật environment.xml: {str(e)}")

        capture_screenshot_and_attach_allure(driver, "Get Version")

    @allure.step("Cập nhật file environment.xml")
    def update_environment_file(self, handler, version, time_release, path_file_changelog):
        """
        Cập nhật các thông tin version vào file XML environment. Nếu có lỗi thì assert False.
        """
        try:
            handler.edit_element("Tenant", Default().url)
        except Exception:
            raise AssertionError("Tenant")

        try:
            handler.edit_element("Tenant Version", f'{version} - {time_release}')
        except Exception:
            raise AssertionError("Tenant Version")

        try:
            source_code_version = read_section_from_md(path_file_changelog, 2)
            handler.edit_element("Source Code Version", source_code_version)
        except Exception:
            raise AssertionError("Source Code Version")
