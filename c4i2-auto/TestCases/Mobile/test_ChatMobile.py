import time
import allure
import pytest
from appium import webdriver
from appium.options.common import AppiumOptions
from conftest import capture_screenshot_and_attach_allure
from Libraries.Framework.Utils import PagebaseMobile
from PageObjects.Mobile.Obj_Mobile import Obj_Function
from PageObjects.Mobile.Obj_PageLogin import Obj_PageLogin
from TestCases.Mobile.test_DataChat import test_chat_data

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    appPackage='com.vbd.c4i2.react',
    appActivity='com.dcmsapp.MainActivity'
)

appium_server_url = 'http://localhost:4723'
@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Remote(appium_server_url, options=AppiumOptions().load_capabilities(capabilities))
    yield driver
    if driver:
        driver.quit()
class Test_TinNhanTrucTiep:
    @pytest.mark.MobileChat
    @allure.epic("Kênh liên lạc")
    @allure.feature("Kênh riêng tư")
    @allure.title("c4i2-494: Kiểm tra có tin nhắn trực tiếp gửi từ web")
    @pytest.mark.parametrize("SourceUser, DestinationUser", [("vannta_2", "vannta_1")])
    def test_chat(self, driver, SourceUser, DestinationUser, test_chat_data):
        pageBase_Mobile = PagebaseMobile(driver)
        allure.attach(test_chat_data, "Giá trị Test", allure.attachment_type.TEXT)
        with allure.step("Cấp quyền cho ứng dụng"):
            # pageBase_Mobile.clickObj(Obj_PageLogin.btnAllow)
            pageBase_Mobile.click_obj(Obj_Function.TextView("Yêu cầu cấp quyền vị trí"))
            pageBase_Mobile.click_obj(Obj_Function.Button("WHILE USING THE APP"))
            pageBase_Mobile.click_obj(Obj_PageLogin.iconBack)
            capture_screenshot_and_attach_allure(driver, "Permisson")
            pageBase_Mobile.click_obj(Obj_Function.TextView("Đi tiếp"))
        with allure.step("Thay đổi kết nối ứng dụng -> staging"):
            pageBase_Mobile.click_obj(Obj_Function.TextView("Thay đổi kết nối ứng dụng"))
            time.sleep(2)
            pageBase_Mobile.send_key_input(Obj_PageLogin.changeAuthority, "c4i2-staging")
            pageBase_Mobile.send_key_input(Obj_PageLogin.changeDomain, ".vbd.vn")
            capture_screenshot_and_attach_allure(driver, "ChangeConnect")
            pageBase_Mobile.click_obj(Obj_Function.TextView("Tiếp tục"))
        with allure.step("Đăng nhập ứng dụng"):
            time.sleep(2)
            pageBase_Mobile.send_key_input(Obj_Function.EditText("Tên đăng nhập"), SourceUser)
            pageBase_Mobile.send_key_input(Obj_Function.EditText("Mật khẩu"), "123123123")
            capture_screenshot_and_attach_allure(driver, "InfoLogin")
            pageBase_Mobile.click_obj(Obj_PageLogin.btnLogin)
            pageBase_Mobile.click_obj(Obj_Function.Button("OK"))
            time.sleep(2)
        with allure.step("Điều hướng đến chức năng Kênh liên lạc"):
            pageBase_Mobile.click_obj(Obj_PageLogin.iconBack)
            pageBase_Mobile.click_obj(Obj_Function.Button("OK"))
            time.sleep(2)
            pageBase_Mobile.click_obj(Obj_Function.TextView("Nhắn tin"))
            capture_screenshot_and_attach_allure(driver, "PageChat")
        with allure.step("Tìm kiếm tài khoản chat"):
            time.sleep(2)
            pageBase_Mobile.send_key_input(Obj_Function.EditText("Tìm kiếm"), DestinationUser)
            capture_screenshot_and_attach_allure(driver, "SearchUser")
        with allure.step("Điều hướng đến hộp thoại chat"):
            time.sleep(2)
            pageBase_Mobile.click_obj(Obj_Function.TextView(DestinationUser))
            capture_screenshot_and_attach_allure(driver, "ChatBox")
        with allure.step("Kiểm tra có tin nhắn từ web gửi đến hay không"):
            verify = pageBase_Mobile.check_element_exist(Obj_Function.ContainsTextView(test_chat_data))
            assert verify, "Không hiển thị tin nhắn được gửi từ web"



