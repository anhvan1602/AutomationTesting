import time
import pytest
import allure
from selenium.webdriver import ActionChains, Keys

from Libraries.Framework.FactoryDrivers import get_chrome_driver
from Libraries.Framework.Utils import PageBase
from WebApplications.PageCommon import PageCommon
from Libraries.Config import Default
from PageObjects.Web.Obj_Chat import Obj_Chat
from PageObjects.Web.Obj_Common import ObjCommon
from WebApplications.PageHome import LoginPage
from conftest import capture_screenshot_and_attach_allure
from faker import Faker
import parametrize_from_file as pff

fake = Faker()


@pytest.fixture(scope='class')
def browser():
    # Khởi tạo ChromeDriver 1 đặt kích thước và vị trí cửa sổ
    driver_chrome_1 = get_chrome_driver()
    driver_chrome_1.implicitly_wait(Default.timeOut)
    # driver_chrome_1.maximize_window()
    # driver_chrome_1.set_window_size(halfScreenWidth, screenHeight)
    # driver_chrome_1.set_window_position(leftScreen[0], leftScreen[1])

    # Khởi tạo ChromeDriver 2 đặt kích thước và vị trí cửa sổ
    driver_chrome_2 = get_chrome_driver()
    driver_chrome_2.implicitly_wait(Default.timeOut)
    # driver_chrome_2.maximize_window()
    # driver_chrome_2.set_window_size(halfScreenWidth, screenHeight)
    # driver_chrome_2.set_window_position(rightScreen[0], rightScreen[1])

    default = Default()
    url_chat = default.url
    username_from, password_from = default.username_from, default.password_from

    username_to, password_to = default.username_to, default.password_to

    driver_chrome_1.get(url_chat)
    driver_chrome_2.get(url_chat)

    page_login = LoginPage(driver_chrome_1)
    page_login.do_login(username_from, password_from)
    page_login.click_obj(Obj_Chat.iconKenhLienLac)
    time.sleep(1)

    page_login = LoginPage(driver_chrome_2)
    page_login.do_login(username_to, password_to)
    page_login.click_obj(Obj_Chat.iconKenhLienLac)
    time.sleep(1)

    yield driver_chrome_1, driver_chrome_2
    driver_chrome_1.quit()
    driver_chrome_2.quit()


@pytest.fixture(scope='class', autouse=True)
def save_current_url(browser):
    # Lấy trình duyệt từ fixture
    driver_1, driver_2 = browser
    # Lưu URL hiện tại của driver 1
    current_url_1 = driver_1.current_url
    # Lưu URL hiện tại của driver 2
    current_url_2 = driver_2.current_url
    # Trả về URL hiện tại của cả hai driver
    yield current_url_1, current_url_2


is_first_test = True


@pytest.fixture(scope='function', autouse=True)
def setup_url(browser, save_current_url):
    global is_first_test
    current_url_1, current_url_2 = save_current_url
    driver_1, driver_2 = browser
    # Nếu không phải là test đầu tiên, thực hiện setup_url
    if not is_first_test and current_url_1 is not None:
        driver_1.get(current_url_1)
    if not is_first_test and current_url_2 is not None:
        driver_2.get(current_url_2)
    # Đánh dấu biến cờ là False sau khi đã thực hiện setup_url lần đầu tiên
    is_first_test = False
    yield


pageBase = PageBase(browser)
pathDataTestChat = pageBase.load_path_data_file_from_path("Datas_Chat", "Test_Chat.json")


@pytest.mark.DC
@pytest.mark.Chat
@pytest.mark.UAT_DC
@allure.epic("Kênh liên lạc")
@allure.feature("Kênh công khai")
class Test_KenhCongKhai:

    @allure.testcase("c4i2-458", "c4i2-458")
    @allure.title("c4i2-458: Xác minh có thể tạo kênh công khai")
    @pff.parametrize(path=pathDataTestChat, key="test_publish_channel")
    def test_public_channel_creation(self, browser, SourceUser, DestinationUser, channel_name, random_text):
        """Trường hợp kiểm thử kiểm tra có thể TẠO kênh công khai"""
        driver_chrome_1, driver_chrome_2 = browser
        page_common_chrome_1 = PageCommon(driver_chrome_1)
        page_base_chrome_1 = PageBase(driver_chrome_1)
        time.sleep(1)
        page_base_chrome_1.show_overlay_text("Kiểm tra tạo kênh công khai")

        with allure.step("Nhấn vào icon (+)"):
            page_base_chrome_1.click_obj(Obj_Chat.iconAdd)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver_chrome_1, "ClickAdd")
        with allure.step("Chọn option 'Tạo kênh'"):
            page_base_chrome_1.click_obj(Obj_Chat.optionTaoKenh)
            time.sleep(1)
            page_base_chrome_1.click_obj(Obj_Chat.chanelTypePublic)
            capture_screenshot_and_attach_allure(driver_chrome_1, "EnterChat")
        with allure.step("Nhập thông tin kênh"):
            allure.attach(channel_name, name="Name Channel:", attachment_type=allure.attachment_type.TEXT)
            xpath_input_name = ObjCommon.search_textbox("Tên kênh:")
            page_base_chrome_1.send_key_input(xpath_input_name, channel_name)
            capture_screenshot_and_attach_allure(driver_chrome_1, "EnterNameChannel")
        with allure.step("Nhấn vào button 'Tạo kênh'"):
            page_base_chrome_1.click_obj(Obj_Chat.btnTaoKenh)
            check_popup = page_common_chrome_1.verify_notify_popup('Tạo kênh thành công')
            assert check_popup, "Tạo mới theo dõi không thành công"
            capture_screenshot_and_attach_allure(driver_chrome_1, name="AssertNotify")
        with allure.step("Tìm kiếm kênh đã tạo"):
            page_base_chrome_1.click_obj(Obj_Chat.txtTimKenh)
            time.sleep(1)
            page_base_chrome_1.send_key_input(Obj_Chat.txtTimKiemKenh, channel_name)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver_chrome_1, name="AssertNotify")
            xpath_results = ObjCommon.result_item(channel_name)
            check_exits = page_base_chrome_1.check_element_visibility(xpath_results)
            assert check_exits, "Kênh công khai đã tạo không hiển thị trong danh sách tìm kiếm"

    @pytest.mark.depends(on='test_public_channel_creation')
    @allure.testcase("c4i2-460", "c4i2-460")
    @allure.title("c4i2-460: Xác minh có thể thêm thành viên vào kênh")
    @pff.parametrize(path=pathDataTestChat, key="test_publish_channel")
    def test_public_channel_member_addition(self, browser, SourceUser, DestinationUser, channel_name, random_text):
        """Trường hợp kiểm thử kiểm tra có thể THÊM thành viên vào kênh công khai"""
        driver_chrome_1, driver_chrome_2 = browser
        page_common_chrome_1 = PageCommon(driver_chrome_1)
        page_base_chrome_1 = PageBase(driver_chrome_1)
        page_base_chrome_2 = PageBase(driver_chrome_2)
        time.sleep(1)
        page_base_chrome_1.show_overlay_text("Thêm thành viên vào kênh")
        page_base_chrome_2.show_overlay_text("Thêm thành viên vào kênh")
        with allure.step("Nhập thông tin kênh vào textbox Tìm kênh"):
            page_base_chrome_1.click_obj(Obj_Chat.txtTimKenh)
            time.sleep(1)
            page_base_chrome_1.send_key_input(Obj_Chat.txtTimKiemKenh, channel_name)
            capture_screenshot_and_attach_allure(driver_chrome_1, "EnterNameChannel")
            time.sleep(1)
        with allure.step("Nhấn vào kênh"):
            xpath_results = ObjCommon.result_item(channel_name)
            page_base_chrome_1.click_obj(xpath_results)
            capture_screenshot_and_attach_allure(driver_chrome_1, "ClickToChannel")
        with allure.step("Nhấn vào icon (i)"):
            page_base_chrome_1.click_obj(Obj_Chat.iconDetail)
            capture_screenshot_and_attach_allure(driver_chrome_1, "PageDetail")
        with allure.step("Nhấn vào button 'Thêm'"):
            page_base_chrome_1.click_obj(Obj_Chat.btnAddMember)
            capture_screenshot_and_attach_allure(driver_chrome_1, "AddMember")
        with allure.step("Nhập thông tin thành viên vào textbox Tìm thành viên"):
            page_base_chrome_1.send_key_input(Obj_Chat.inputSeachMember, DestinationUser)
            capture_screenshot_and_attach_allure(driver_chrome_1, "SearchMember")
        with allure.step("Nhấn chọn thành viên"):
            xpath_results = ObjCommon.result_item(DestinationUser)
            page_base_chrome_1.click_obj(xpath_results)
            capture_screenshot_and_attach_allure(driver_chrome_1, "SelectOptionMember")
        with allure.step("Nhấn vào button 'Xác nhận'"):
            page_base_chrome_1.click_obj(Obj_Chat.btnXacNhan)
            check_popup = page_common_chrome_1.verify_notify_popup('Thêm thành công')
            assert check_popup, "Không có thông báo thêm mới thành viên thành công"
            capture_screenshot_and_attach_allure(driver_chrome_1, name="NotifySuccessful")

    @pytest.mark.depends(on='test_public_channel_member_addition')
    @allure.testcase("c4i2-478", "c4i2-478")
    @allure.title("c4i2-478: Xác minh có thể chat trong kênh")
    @pff.parametrize(path=pathDataTestChat, key="test_publish_channel")
    def test_public_channel_chat(self, browser, SourceUser, DestinationUser, channel_name, random_text):
        """Trường hợp kiểm thử kiểm tra có thể CHAT trong kênh"""
        driver_chrome_1, driver_chrome_2 = browser
        page_base_chrome_1 = PageBase(driver_chrome_1)
        page_base_chrome_2 = PageBase(driver_chrome_2)
        actions_chrome_1 = ActionChains(driver_chrome_1)
        time.sleep(1)
        page_base_chrome_1.show_overlay_text("Kiểm tra chat trong kênh")
        page_base_chrome_2.show_overlay_text("Kiểm tra chat kênh")
        with allure.step("Nhập thông tin kênh vào textbox Tìm kênh"):
            page_base_chrome_1.click_obj(Obj_Chat.txtTimKenh)
            time.sleep(1)
            page_base_chrome_1.send_key_input(Obj_Chat.txtTimKiemKenh, channel_name)
            capture_screenshot_and_attach_allure(driver_chrome_1, "EnterNameChannel")
            time.sleep(1)
        with allure.step("Nhấn vào kênh"):
            xpath_results = ObjCommon.result_item(channel_name)
            page_base_chrome_1.click_obj(xpath_results)
            capture_screenshot_and_attach_allure(driver_chrome_1, "ClickToChannel")
        with allure.step(f"Nhập tin nhắn từ tài khoản {SourceUser}"):
            page_base_chrome_1.send_key_input(Obj_Chat.textareaChat, random_text)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver_chrome_1, "EnterChat")
        with allure.step("Gửi tin nhắn"):
            actions_chrome_1.send_keys(Keys.ENTER)
            actions_chrome_1.perform()
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver_chrome_1, "SendChat")
        with allure.step(f"Từ tài khoản {DestinationUser} điều hướng đến kênh chat"):
            page_base_chrome_2.click_obj(Obj_Chat.txtTimKenh)
            time.sleep(1)
            page_base_chrome_2.send_key_input(Obj_Chat.txtTimKiemKenh, channel_name)
            capture_screenshot_and_attach_allure(driver_chrome_2, "EnterNameChannel")
            time.sleep(1)
            xpath_results = ObjCommon.result_item(channel_name)
            page_base_chrome_2.click_obj(xpath_results)
            capture_screenshot_and_attach_allure(driver_chrome_2, "ClickToChannel")
        with allure.step(f"Từ tài khoản {DestinationUser} kiểm tra có tin nhắn trong kênh"):
            verify_chat = page_base_chrome_2.check_element_visibility(ObjCommon.text_span(random_text))
            assert verify_chat, "Không có tin nhắn được gửi đến"

    @pytest.mark.depends(on='test_public_channel_member_addition')
    @allure.testcase("c4i2-462", "c4i2-462")
    @allure.title("c4i2-462: Xác minh có thể xóa thành viên khỏi kênh")
    @pff.parametrize(path=pathDataTestChat, key="test_publish_channel")
    def test_public_channel_member_removal(self, browser, SourceUser, DestinationUser, channel_name, random_text):
        """Trường hợp kiểm thử kiểm tra có thể xóa thành viên ra khỏi kênh công khai"""
        driver_chrome_1, driver_chrome_2 = browser
        page_common_chrome_1 = PageCommon(driver_chrome_1)
        page_base_chrome_1 = PageBase(driver_chrome_1)
        page_base_chrome_2 = PageBase(driver_chrome_2)
        time.sleep(1)
        page_base_chrome_1.show_overlay_text("Xóa thành viên ra khỏi kênh công khai")
        page_base_chrome_2.show_overlay_text("Xóa thành viên ra khỏi kênh công khai")
        with allure.step("Nhập thông tin kênh vào textbox Tìm kênh"):
            page_base_chrome_1.click_obj(Obj_Chat.txtTimKenh)
            time.sleep(1)
            page_base_chrome_1.send_key_input(Obj_Chat.txtTimKiemKenh, channel_name)
            capture_screenshot_and_attach_allure(driver_chrome_1, "EnterNameChannel")
            time.sleep(1)
        with allure.step("Nhấn vào kênh"):
            xpath_results = ObjCommon.result_item(channel_name)
            page_base_chrome_1.click_obj(xpath_results)
            capture_screenshot_and_attach_allure(driver_chrome_1, "ClickToChannel")
        with allure.step("Nhấn vào icon (i)"):
            page_base_chrome_1.click_obj(Obj_Chat.iconDetail)
            capture_screenshot_and_attach_allure(driver_chrome_1, "PageDetail")
        with allure.step("verify danh sách user panel bên phải"):
            xpath_results = ObjCommon.result_item(DestinationUser)
            check_exits = page_base_chrome_1.check_element_visibility(xpath_results)
            assert check_exits, "Không hiển thị tên user đã thêm tại panel bên phải kênh"
        with allure.step("Nhấn vào button 'Quản lý'"):
            page_base_chrome_1.click_obj(Obj_Chat.btnQuanLy)
            capture_screenshot_and_attach_allure(driver_chrome_1, "ManagerMember")
        with allure.step("Nhấn vào icon (:) bên phải tên thành viên"):
            page_base_chrome_1.click_obj(ObjCommon.ellipsis_icon(DestinationUser))
            capture_screenshot_and_attach_allure(driver_chrome_1, "ControlMember")
        with allure.step("Nhấn chọn option 'Xóa thành viên'"):
            page_base_chrome_1.click_obj(ObjCommon.option_menu("Xóa thành viên"))
            capture_screenshot_and_attach_allure(driver_chrome_1, "DeleteMember")
            check_popup = page_common_chrome_1.verify_notify_popup('Xóa thành công')
            assert check_popup, "Không có thông báo xóa thành công thành viên khỏi kênh"
        with allure.step("verify danh sách user panel bên phải không hiển thị thành viên vừa xóa"):
            xpath_results = ObjCommon.result_item(DestinationUser)
            check_exits = page_base_chrome_1.check_element_visibility(xpath_results)
            assert not check_exits, "Tên user vẫn hiển thị tại panel bên phải kênh sau khi xóa"

    @allure.testcase("c4i2-466", "c4i2-466")
    @pytest.mark.depends(on='test_public_channel_chat')
    @allure.title("c4i2-466: Xác minh có thể xóa kênh")
    @pff.parametrize(path=pathDataTestChat, key="test_publish_channel")
    def test_public_channel_delete(self, browser, SourceUser, DestinationUser, channel_name, random_text):
        """Trường hợp kiểm thử kiểm tra có thể XÓA kênh công khai"""
        driver_chrome_1, driver_chrome_2 = browser
        page_common_chrome_1 = PageCommon(driver_chrome_1)
        page_base_chrome_1 = PageBase(driver_chrome_1)
        page_base_chrome_2 = PageBase(driver_chrome_2)
        time.sleep(1)
        page_base_chrome_1.show_overlay_text("Xóa kênh công khai")
        page_base_chrome_2.show_overlay_text("Xóa kênh công khai")
        with allure.step("Nhập thông tin kênh vào textbox Tìm kênh"):
            page_base_chrome_1.click_obj(Obj_Chat.txtTimKenh)
            time.sleep(1)
            page_base_chrome_1.send_key_input(Obj_Chat.txtTimKiemKenh, channel_name)
            capture_screenshot_and_attach_allure(driver_chrome_1, "EnterNameChannel")
            time.sleep(1)
        with allure.step("Nhấn vào kênh"):
            xpath_results = ObjCommon.result_item(channel_name)
            page_base_chrome_1.click_obj(xpath_results)
            capture_screenshot_and_attach_allure(driver_chrome_1, "ClickToChannel")
        with allure.step("Nhấn vào icon bên cạnh tên kênh"):
            page_base_chrome_1.click_obj(Obj_Chat.iconChevronDown)
            capture_screenshot_and_attach_allure(driver_chrome_1, "PageDetail")
        with allure.step("Nhấn vào option 'Xóa kênh'"):
            page_base_chrome_1.click_obj(ObjCommon.option_menu("Xóa kênh"))
        with allure.step("Nhấn vào button 'Xác nhận' xóa kênh"):
            page_base_chrome_1.click_obj(Obj_Chat.btnXacNhanXoaKenh)
            capture_screenshot_and_attach_allure(driver_chrome_1, "DeleteChannel")
            check_popup = page_common_chrome_1.verify_notify_popup('Xóa kênh thành công')
            assert check_popup, "Không có thông báo xóa kênh thành công"


@pytest.mark.DC
@pytest.mark.Chat
@pytest.mark.UAT_DC
@allure.epic("Kênh liên lạc")
@allure.feature("Kênh riêng tư")
class Test_KenhRiengTu:

    @allure.testcase("c4i2-459", "c4i2-459")
    @allure.title("c4i2-459: Xác minh có thể tạo kênh riêng tư")
    @pff.parametrize(path=pathDataTestChat, key="test_private_channel")
    def test_private_channel_creation(self, browser, SourceUser, DestinationUser, channel_name, random_text):
        """Trường hợp kiểm thử kiểm tra có thể TẠO kênh riêng tư"""
        driver_chrome_1, driver_chrome_2 = browser
        page_common_chrome_1 = PageCommon(driver_chrome_1)
        page_base_chrome_1 = PageBase(driver_chrome_1)
        time.sleep(1)
        page_base_chrome_1.show_overlay_text("Kiểm tra tạo kênh riêng tư")

        with allure.step("Nhấn vào icon (+)"):
            page_base_chrome_1.click_obj(Obj_Chat.iconAdd)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver_chrome_1, "ClickAdd")
        with allure.step("Chọn option 'Tạo kênh'"):
            page_base_chrome_1.click_obj(Obj_Chat.optionTaoKenh)
            time.sleep(1)
            page_base_chrome_1.click_obj(Obj_Chat.chanelTypePrivate)
            capture_screenshot_and_attach_allure(driver_chrome_1, "EnterChat")
        with allure.step("Nhập thông tin kênh"):
            allure.attach(channel_name, name="Name Channel:", attachment_type=allure.attachment_type.TEXT)
            xpath_input_name = ObjCommon.search_textbox("Tên kênh:")
            page_base_chrome_1.send_key_input(xpath_input_name, channel_name)
            capture_screenshot_and_attach_allure(driver_chrome_1, "EnterNameChannel")
        with allure.step("Nhấn vào button 'Tạo kênh'"):
            page_base_chrome_1.click_obj(Obj_Chat.btnTaoKenh)
            check_popup = page_common_chrome_1.verify_notify_popup('Tạo kênh thành công')
            assert check_popup, "Tạo mới theo dõi không thành công"
            capture_screenshot_and_attach_allure(driver_chrome_1, name="AssertNotify")
        with allure.step("Tìm kiếm kênh đã tạo"):
            xpath_results = ObjCommon.item_collapsible(channel_name)
            page_base_chrome_1.click_obj(xpath_results)
            capture_screenshot_and_attach_allure(driver_chrome_1, name="AssertViewChannel")

    @pytest.mark.depends(on='test_private_channel_creation')
    @allure.testcase("c4i2-461", "c4i2-461")
    @allure.title("c4i2-461: Xác minh có thể thêm thành viên vào kênh")
    @pff.parametrize(path=pathDataTestChat, key="test_private_channel")
    def test_private_channel_member_addition(self, browser, SourceUser, DestinationUser, channel_name, random_text):
        """Trường hợp kiểm thử kiểm tra có thể THÊM thành viên vào kênh riêng tư"""
        driver_chrome_1, driver_chrome_2 = browser
        page_common_chrome_1 = PageCommon(driver_chrome_1)
        page_base_chrome_1 = PageBase(driver_chrome_1)
        page_base_chrome_2 = PageBase(driver_chrome_2)
        time.sleep(1)
        page_base_chrome_1.show_overlay_text("Thêm thành viên vào kênh")
        page_base_chrome_2.show_overlay_text("Thêm thành viên vào kênh")

        with allure.step("Nhấn vào kênh"):
            xpath_results = ObjCommon.item_collapsible(channel_name)
            page_base_chrome_1.click_obj(xpath_results)
            capture_screenshot_and_attach_allure(driver_chrome_1, "ClickToChannel")
        with allure.step("Nhấn vào icon (i)"):
            page_base_chrome_1.click_obj(Obj_Chat.iconDetail)
            capture_screenshot_and_attach_allure(driver_chrome_1, "PageDetail")
        with allure.step("Nhấn vào button 'Thêm'"):
            page_base_chrome_1.click_obj(Obj_Chat.btnAddMember)
            capture_screenshot_and_attach_allure(driver_chrome_1, "AddMember")
        with allure.step("Nhập thông tin thành viên vào textbox Tìm thành viên"):
            page_base_chrome_1.send_key_input(Obj_Chat.inputSeachMember, DestinationUser)
            capture_screenshot_and_attach_allure(driver_chrome_1, "SearchMember")
        with allure.step("Nhấn chọn thành viên"):
            xpath_results = ObjCommon.result_item(DestinationUser)
            page_base_chrome_1.click_obj(xpath_results)
            capture_screenshot_and_attach_allure(driver_chrome_1, "SelectOptionMember")
        with allure.step("Nhấn vào button 'Xác nhận'"):
            page_base_chrome_1.click_obj(Obj_Chat.btnXacNhan)
            check_popup = page_common_chrome_1.verify_notify_popup('Thêm thành công')
            assert check_popup, "Không có thông báo thêm mới thành viên thành công"
            capture_screenshot_and_attach_allure(driver_chrome_1, name="NotifySuccessful")

    @pytest.mark.depends(on='test_private_channel_member_addition')
    @allure.testcase("c4i2-479", "c4i2-479")
    @allure.title("c4i2-479: Xác minh có thể chat trong kênh")
    @pff.parametrize(path=pathDataTestChat, key="test_private_channel")
    def test_private_channel_chat(self, browser, SourceUser, DestinationUser, channel_name, random_text):
        """Trường hợp kiểm thử kiểm tra có thể CHAT trong kênh"""
        driver_chrome_1, driver_chrome_2 = browser
        page_base_chrome_1 = PageBase(driver_chrome_1)
        page_base_chrome_2 = PageBase(driver_chrome_2)
        actions_chrome_1 = ActionChains(driver_chrome_1)
        time.sleep(1)
        page_base_chrome_1.show_overlay_text("Kiểm tra chat trong kênh")
        page_base_chrome_2.show_overlay_text("Kiểm tra chat kênh")
        with allure.step("Nhấn vào kênh"):
            xpath_results = ObjCommon.item_collapsible(channel_name)
            page_base_chrome_1.click_obj(xpath_results)
            capture_screenshot_and_attach_allure(driver_chrome_1, "ClickToChannel")
        with allure.step(f"Nhập tin nhắn từ tài khoản {SourceUser}"):
            page_base_chrome_1.send_key_input(Obj_Chat.textareaChat, random_text)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver_chrome_1, "EnterChat")
        with allure.step("Gửi tin nhắn"):
            actions_chrome_1.send_keys(Keys.ENTER)
            actions_chrome_1.perform()
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver_chrome_1, "SendChat")
        with allure.step(f"Từ tài khoản {DestinationUser} điều hướng đến kênh chat"):
            xpath_results = ObjCommon.item_collapsible(channel_name)
            page_base_chrome_2.click_obj(xpath_results)
            capture_screenshot_and_attach_allure(driver_chrome_2, "ClickToChannel")
        with allure.step(f"Từ tài khoản {DestinationUser} kiểm tra có tin nhắn trong kênh"):
            verify_chat = page_base_chrome_2.check_element_visibility(ObjCommon.text_span(random_text))
            assert verify_chat, "Không có tin nhắn được gửi đến"

    @pytest.mark.depends(on='test_private_channel_member_addition')
    @allure.testcase("c4i2-463", "c4i2-463")
    @allure.title("c4i2-463: Xác minh có thể xóa thành viên khỏi kênh")
    @pff.parametrize(path=pathDataTestChat, key="test_private_channel")
    def test_private_channel_member_removal(self, browser, SourceUser, DestinationUser, channel_name, random_text):
        """Trường hợp kiểm thử kiểm tra có thể xóa thành viên ra khỏi kênh công khai"""
        driver_chrome_1, driver_chrome_2 = browser
        page_common_chrome_1 = PageCommon(driver_chrome_1)
        page_base_chrome_1 = PageBase(driver_chrome_1)
        page_base_chrome_2 = PageBase(driver_chrome_2)
        time.sleep(1)
        page_base_chrome_1.show_overlay_text("Xóa thành viên ra khỏi kênh công khai")
        page_base_chrome_2.show_overlay_text("Xóa thành viên ra khỏi kênh công khai")
        with allure.step("Nhấn vào kênh"):
            xpath_results = ObjCommon.item_collapsible(channel_name)
            page_base_chrome_1.click_obj(xpath_results)
            capture_screenshot_and_attach_allure(driver_chrome_1, "ClickToChannel")
        with allure.step("Nhấn vào icon (i)"):
            page_base_chrome_1.click_obj(Obj_Chat.iconDetail)
            capture_screenshot_and_attach_allure(driver_chrome_1, "PageDetail")
        with allure.step("verify danh sách user panel bên phải"):
            xpath_results = ObjCommon.result_item(DestinationUser)
            check_exits = page_base_chrome_1.check_element_visibility(xpath_results)
            assert check_exits, "Không hiển thị tên user đã thêm tại panel bên phải kênh"
        with allure.step("Nhấn vào button 'Quản lý'"):
            page_base_chrome_1.click_obj(Obj_Chat.btnQuanLy)
            capture_screenshot_and_attach_allure(driver_chrome_1, "ManagerMember")
        with allure.step("Nhấn vào icon (:) bên phải tên thành viên"):
            page_base_chrome_1.click_obj(ObjCommon.ellipsis_icon(DestinationUser))
            capture_screenshot_and_attach_allure(driver_chrome_1, "ControlMember")
        with allure.step("Nhấn chọn option 'Xóa thành viên'"):
            page_base_chrome_1.click_obj(ObjCommon.option_menu("Xóa thành viên"))
            capture_screenshot_and_attach_allure(driver_chrome_1, "DeleteMember")
            check_popup = page_common_chrome_1.verify_notify_popup('Xóa thành công')
            assert check_popup, "Không có thông báo xóa thành công thành viên khỏi kênh"
        with allure.step("verify danh sách user panel bên phải không hiển thị thành viên vừa xóa"):
            xpath_results = ObjCommon.result_item(DestinationUser)
            check_exits = page_base_chrome_1.check_element_visibility(xpath_results)
            assert not check_exits, "Tên user vẫn hiển thị tại panel bên phải kênh sau khi xóa"

    @allure.testcase("c4i2-466", "c4i2-466")
    @pytest.mark.depends(on='test_private_channel_chat')
    @allure.title("c4i2-467: Xác minh có thể xóa kênh")
    @pff.parametrize(path=pathDataTestChat, key="test_private_channel")
    def test_private_channel_delete(self, browser, SourceUser, DestinationUser, channel_name, random_text):
        """Trường hợp kiểm thử kiểm tra có thể XÓA kênh riêng tư"""
        driver_chrome_1, driver_chrome_2 = browser
        page_common_chrome_1 = PageCommon(driver_chrome_1)
        page_base_chrome_1 = PageBase(driver_chrome_1)
        page_base_chrome_2 = PageBase(driver_chrome_2)
        time.sleep(1)
        page_base_chrome_1.show_overlay_text("Xóa kênh công khai")
        page_base_chrome_2.show_overlay_text("Xóa kênh công khai")
        with allure.step("Nhấn vào kênh"):
            xpath_results = ObjCommon.item_collapsible(channel_name)
            page_base_chrome_1.click_obj(xpath_results)
            capture_screenshot_and_attach_allure(driver_chrome_1, "ClickToChannel")
        with allure.step("Nhấn vào icon bên cạnh tên kênh"):
            page_base_chrome_1.click_obj(Obj_Chat.iconChevronDown)
            capture_screenshot_and_attach_allure(driver_chrome_1, "PageDetail")
        with allure.step("Nhấn vào option 'Xóa kênh'"):
            page_base_chrome_1.click_obj(ObjCommon.option_menu("Xóa kênh"))
        with allure.step("Nhấn vào button 'Xác nhận' xóa kênh"):
            page_base_chrome_1.click_obj(Obj_Chat.btnXacNhanXoaKenh)
            capture_screenshot_and_attach_allure(driver_chrome_1, "DeleteChannel")
            check_popup = page_common_chrome_1.verify_notify_popup('Xóa kênh thành công')
            assert check_popup, "Không có thông báo xóa kênh thành công"


@pytest.mark.DC
@pytest.mark.Chat
@pytest.mark.UAT_DC
@allure.epic("Kênh liên lạc")
@allure.feature("Tin nhắn trực tiếp")
class Test_TinNhanTrucTiep:

    @pytest.mark.Quick_Scan
    @allure.testcase("c4i2-459", "c4i2-487")
    @allure.title("c4i2-487: Xác minh có thể tạo tin nhắn trực tiếp")
    @pff.parametrize(path=pathDataTestChat, key="test_direct_message")
    def test_send_message(self, browser, SourceUser, DestinationUser, random_text):
        """Trường hợp kiểm thử kiểm tra có thể GỬI tin nhắn giữa 2 tài khoản"""
        driver_chrome_1, driver_chrome_2 = browser
        page_base_chrome_1 = PageBase(driver_chrome_1)
        page_base_chrome_2 = PageBase(driver_chrome_2)
        actions_chrome_1 = ActionChains(driver_chrome_1)
        time.sleep(1)
        page_base_chrome_1.show_overlay_text("Kiểm tra chat trực tiếp")
        page_base_chrome_2.show_overlay_text("Kiểm tra chat trực tiếp")

        with allure.step(f"Từ {SourceUser} nhấn đến đoạn chat {DestinationUser}"):
            page_base_chrome_1.click_obj(Obj_Chat.txtTimKenh)
            time.sleep(1)
            page_base_chrome_1.send_key_input(Obj_Chat.txtTimKiemKenh, DestinationUser)
            time.sleep(1)
            page_base_chrome_1.click_obj(ObjCommon.result_item(DestinationUser))
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver_chrome_1, "ToChat")
        with allure.step("Nhập tin nhắn"):
            page_base_chrome_1.send_key_input(Obj_Chat.textareaChat, random_text)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver_chrome_1, "EnterChat")
        with allure.step("Gửi tin nhắn"):
            actions_chrome_1.send_keys(Keys.ENTER)
            actions_chrome_1.perform()
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver_chrome_1, "SendChat")
        with allure.step(f"Từ {DestinationUser} nhấn đến đoạn chat {SourceUser}"):
            page_base_chrome_2.click_obj(Obj_Chat.txtTimKenh)
            time.sleep(1)
            page_base_chrome_2.send_key_input(Obj_Chat.txtTimKiemKenh, SourceUser)
            time.sleep(1)
            page_base_chrome_2.click_obj(ObjCommon.result_item(SourceUser))
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver_chrome_2, "Verify")
        with allure.step("Kiểm tra có tin nhắn hiển thị từ SourceUser"):
            verify_chat = page_base_chrome_2.check_element_visibility(ObjCommon.text_span(random_text))
            assert verify_chat, "Không có tin nhắn được gửi đến"
