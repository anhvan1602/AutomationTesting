import os
import time
from urllib.parse import urljoin

import pytest
import allure
from datetime import datetime

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By

from Libraries.Framework.FactoryDrivers import get_chrome_driver
from Libraries.Framework.Utils import PageBase
from Libraries.Config import Default
from PageObjects.Web.Obj_Common import ObjCommon
from WebApplications.PageHome import LoginPage
from PageObjects.Web.Obj_Chat import Obj_Chat
from conftest import capture_screenshot_and_attach_allure
import parametrize_from_file as pff


@pytest.fixture(scope='class')
def browser():
    default_tenant = Default()
    driver = get_chrome_driver()
    driver.implicitly_wait(default_tenant.timeOut)

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


@pytest.mark.SendAttachment
@allure.epic("Kênh liên lạc")
@allure.feature("Kênh công khai")
class Test_SendChat:
    pageBase = PageBase(browser)
    pathDataTestChat = pageBase.load_path_data_file_from_path("Datas_Chat", "Test_SendFileAttachment_Chat.json")

    @allure.title("Gửi file đính kèm trong kênh liên lạc")
    @pff.parametrize(path=pathDataTestChat)
    def test_send_file_attachment_in_chat(self, browser, channel_name, path_prepare, path_chat):
        """Trường hợp kiểm thử kiểm tra có thể gửi file đính kèm trong kênh liên lạc"""
        driver = browser
        page_base = PageBase(driver)
        actions_chrome = ActionChains(driver)
        default = Default()
        url = default.url
        time.sleep(1)
        page_base.show_overlay_text("Kiểm tra hệ thống")
        screenshot_dir = "screenshots"
        with allure.step("Chuẩn bị file đính kèm"):
            with allure.step("Điều hướng đến vị trí cần capture image"):
                url_prepare = urljoin(url, path_prepare)
                driver.get(url_prepare)
                time.sleep(2)
            with allure.step("Capture hình ảnh và lưu hình ảnh vào hệ thống"):
                if not os.path.exists(screenshot_dir):
                    os.makedirs(screenshot_dir)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_file = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")
                driver.save_screenshot(screenshot_file)
        with allure.step("Gửi file đính kèm vào kênh liên lạc"):
            with allure.step("Điều hướng đến Kênh liên lạc"):
                url_chat = urljoin(url, path_chat)
                driver.get(url_chat)
            with allure.step("Nhập thông tin kênh vào textbox Tìm kênh"):
                page_base.click_obj(Obj_Chat.txtTimKenh)
                time.sleep(1)
                page_base.send_key_input(Obj_Chat.txtTimKiemKenh, channel_name)
                capture_screenshot_and_attach_allure(driver, "EnterNameChannel")
                time.sleep(1)
            with allure.step("Nhấn vào kênh"):
                xpath_results = ObjCommon.result_item(channel_name)
                page_base.click_obj(xpath_results)
                capture_screenshot_and_attach_allure(driver, "ClickToChannel")
            with allure.step("Thêm file đính kèm"):
                absolute_screenshot_path = os.path.abspath(screenshot_file)
                upload_input = driver.find_element(By.XPATH, '//input[@type="file"][1]')
                upload_input.send_keys(absolute_screenshot_path)
                capture_screenshot_and_attach_allure(driver, "AttachFile")
            with allure.step("Gửi tin nhắn"):
                actions_chrome.send_keys(Keys.ENTER)
                actions_chrome.perform()
                time.sleep(1)
                capture_screenshot_and_attach_allure(driver, "SendChat")
