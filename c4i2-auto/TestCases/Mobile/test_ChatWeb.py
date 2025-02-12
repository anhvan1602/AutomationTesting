import time
import pytest
import allure
from selenium.webdriver import ActionChains, Keys

from Libraries.Framework.FactoryDrivers import get_chrome_driver
from Libraries.Framework.Utils import PageBase
from Libraries.Config import Default
from PageObjects.Web.Obj_Chat import Obj_Chat
from WebApplications.PageHome import LoginPage
from conftest import capture_screenshot_and_attach_allure
from TestCases.Mobile.test_DataChat import test_chat_data



@pytest.fixture(scope='class')
def browser():
    # Khởi tạo ChromeDriver 1 đặt kích thước và vị trí cửa sổ
    driverChrome_1 = get_chrome_driver()
    driverChrome_1.implicitly_wait(Default.timeOut)
    # driverChrome_1.maximize_window()

    default = Default()
    urlChat = default.url
    usernameFrom, passwordFrom = default.username_from, default.password_from

    driverChrome_1.get(urlChat)

    pageLogin = LoginPage(driverChrome_1)
    pageLogin.do_login(usernameFrom, passwordFrom)
    pageLogin.click_obj(Obj_Chat.iconKenhLienLac)
    time.sleep(1)

    yield driverChrome_1
    driverChrome_1.quit()


@pytest.fixture(scope='class', autouse=True)
def save_current_url(browser):
    driver_1 = browser
    current_url_1 = driver_1.current_url
    yield current_url_1


is_first_test = True


@pytest.fixture(scope='function', autouse=True)
def setup_url(browser, save_current_url):
    global is_first_test
    current_url_1 = save_current_url
    driver_1 = browser
    if not is_first_test and current_url_1 is not None:
        driver_1.get(current_url_1)
    is_first_test = False
    yield



@allure.epic("Kênh liên lạc")
@allure.feature("Tin nhắn trực tiếp")
class Test_TinNhanTrucTiep:

    @pytest.mark.run(order=1)
    @pytest.mark.MobileChat
    @allure.testcase("c4i2-459", "c4i2-487")
    @allure.title("Pre_Test: TestCase id c4i2-494 ")
    @pytest.mark.parametrize("SourceUser, DestinationUser", [("vannta_1", "vannta_2")])
    def test_send_message(self, browser, SourceUser, DestinationUser, test_chat_data):
        """Trường hợp kiểm thử kiểm tra có thể GỬI tin nhắn giữa 2 tài khoản"""
        driver_Chrome_1 = browser
        pageBase_Chrome_1 = PageBase(driver_Chrome_1)
        actions_Chrome_1 = ActionChains(driver_Chrome_1)
        time.sleep(1)
        pageBase_Chrome_1.show_overlay_text("Kiểm tra chat trực tiếp")

        allure.attach(test_chat_data, "Giá trị Test", allure.attachment_type.TEXT)
        with allure.step(f"Từ {SourceUser} nhấn đến đoạn chat {DestinationUser}"):
            pageBase_Chrome_1.click_obj(Obj_Chat.txtTimKenh)
            time.sleep(1)
            pageBase_Chrome_1.send_key_input(Obj_Chat.txtTimKiemKenh, DestinationUser)
            time.sleep(1)
            pageBase_Chrome_1.click_obj(Obj_Chat.optionFirst)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver_Chrome_1, "ToChat")
        with allure.step("Nhập tin nhắn"):
            pageBase_Chrome_1.send_key_input(Obj_Chat.textareaChat, test_chat_data)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver_Chrome_1, "EnterChat")
        with allure.step("Gửi tin nhắn"):
            actions_Chrome_1.send_keys(Keys.ENTER)
            actions_Chrome_1.perform()
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver_Chrome_1, "SendChat")
