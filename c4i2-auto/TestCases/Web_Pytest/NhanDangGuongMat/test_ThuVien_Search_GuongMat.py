import time
import pytest
import allure

from Libraries.Framework.FactoryDrivers import get_chrome_driver
from Libraries.Framework.Utils import PageBase
from Libraries.Config import Default
from PageObjects.Web.Obj_Common import ObjCommon
from PageObjects.Web.Obj_GuongMat import Obj_GuongMat, ObjGuongmatFuntion
from WebApplications.PageCommon import PageCommon
from WebApplications.PageHome import LoginPage
from WebApplications.PageGuongMat import PageGuongMat, PageGuongMatTabThuVien, PageGuongMatTabPhatHien
from conftest import capture_screenshot_and_attach_allure
import parametrize_from_file as pff
from Libraries.Plugins.DataHandler import JsonDataHandler


def generate_xpath_search(search_group: str, label: str) -> str:
    xpath_template = ('//div[contains(@class, "section-panel ") and .//*[text()="{search_group}"]]'
                      '//div[contains(@class, "form-control-row") and .//div[text()="{label}"]]//input')
    return xpath_template.format(search_group=search_group, label=label)


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
    page_login.click_obj(Obj_GuongMat.iconNhanDangGuongMat)
    page_base.click_obj(Obj_GuongMat.tabThuVien)
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
pathDataTestSearchFs = pageBase.load_path_data_file_from_path("Datas_FS",
                                                              "Test_ThuVien_Search_GuongMat.json")


@pff.parametrize(path=pathDataTestSearchFs, key="create_data_search")
def setup_data_search(Data):
    value_data = Data
    return value_data


@pytest.fixture(scope='class', autouse=True)
def create_data(browser, data=setup_data_search):
    driver = browser
    page_base = PageBase(driver)
    page_guong_mat = PageGuongMat(driver)
    Data = data.pytestmark[0].args[1][0].values[0]

    page_base.click_obj(Obj_GuongMat.btnThemMoiGuongMat)
    page_guong_mat.do_dien_thong_tin_cong_dan(Data)
    page_guong_mat.do_bo_sung_them_tt_cong_dan(Data)
    page_base.click_obj(Obj_GuongMat.btnLuuThemMoi)
    time.sleep(2)
    yield


@pytest.fixture(scope='class', autouse=True)
def clean_data(browser, save_current_url, data=setup_data_search):
    yield
    driver = browser
    page_base = PageBase(driver)
    Data = data.pytestmark[0].args[1][0].values[0]

    driver.get(save_current_url)
    time.sleep(1)
    ten_guong_mat = Data[0]["Value"]
    page_base.send_key_input(Obj_GuongMat.txtSearchGuongMat, ten_guong_mat)
    page_base.click_obj(Obj_GuongMat.btnTimKiem)

    time.sleep(3)
    page_base.click_obj(Obj_GuongMat.checkboxFace)
    time.sleep(2)
    page_base.click_obj(Obj_GuongMat.btnDelete)
    time.sleep(2)
    page_base.click_obj(Obj_GuongMat.btnXacNhan)
    time.sleep(2)


@allure.epic("Nhận dạng gương mặt")
@allure.feature("Thư viện Gương mặt")
@pytest.mark.FS
@pytest.mark.SearchLibraryFace
@pytest.mark.Add_DataList
class Test_FaceLibrarySearch:
    pageBase = PageBase(browser)
    pathDataTestSearchFs = pageBase.load_path_data_file_from_path("Datas_FS",
                                                                  "Test_ThuVien_Search_GuongMat.json")

    @allure.testcase("c4i2-345", "c4i2-345")
    @allure.story("Tìm kiếm Gương mặt trong thư viện thành công")
    @allure.title("Search Họ và tên")
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_search_by_name_success(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm gương mặt thành công - Search Họ và tên"""
        driver = browser
        page_base = PageBase(driver)
        page_guong_mat_tab_thu_vien = PageGuongMatTabThuVien(driver)
        page_base.show_overlay_text("Search Họ và tên")

        label_search = "Họ và tên"
        json_data_handler = JsonDataHandler(Data_Search)
        type_of, label, value = json_data_handler.get_info_by_label(label_search)
        name_search = value

        with allure.step("Nhập thông tin Họ và tên vào tab Tìm kiếm"):
            time.sleep(2)
            page_base.send_key_input(Obj_GuongMat.txtSearchGuongMat, name_search)
            capture_screenshot_and_attach_allure(driver, name="EnterName")
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
            check_exit_in_pop_up = page_base.check_element_visibility(Obj_GuongMat.iconEdit)
            assert check_exit_in_pop_up, "Không trả về kết quả tìm kiếm trên danh sách lưới !"
        with allure.step("Kiểm tra kết quả xuất hiện đầu tiên trên danh sách lưới"):
            time.sleep(3)
            page_base.click_obj(Obj_GuongMat.iconEdit)
            time.sleep(2)
            check_result = page_guong_mat_tab_thu_vien.do_verify_result_search_in_popup(type_of, label, value)
            allure.attach(driver.get_screenshot_as_png(), name="CheckResultEdited",
                          attachment_type=allure.attachment_type.PNG)
            assert check_result, "Kết quả tìm kiếm không hiển thị chính xác dữ liệu"

    @pytest.mark.UAT_DC
    @allure.testcase("c4i2-346", "c4i2-346")
    @allure.story("Tìm kiếm Gương mặt trong thư viện thành công")
    @allure.title("c4i2-346: Search CMND")
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_search_id_card_success(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm gương mặt thành công - Search CMND"""
        driver = browser
        page_base = PageBase(driver)
        page_guong_mat_tab_thu_vien = PageGuongMatTabThuVien(driver)
        page_base.show_overlay_text("Search CMND")

        label_search = "CMND/ CCCD/ Hộ chiếu"
        json_data_handler = JsonDataHandler(Data_Search)
        type_of, label, value = json_data_handler.get_info_by_label(label_search)

        id_search = value
        with allure.step("Nhập thông tin CMND vào tab Tìm kiếm"):
            time.sleep(2)
            page_base.send_key_input(Obj_GuongMat.txtSearchID, id_search)
            capture_screenshot_and_attach_allure(driver, name="EnterName")
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
            check_exit_in_pop_up = page_base.check_element_visibility(Obj_GuongMat.iconEdit)
            assert check_exit_in_pop_up, "Không trả về kết quả tìm kiếm trên danh sách lưới !"
        with allure.step("Kiểm tra kết quả xuất hiện đầu tiên trên danh sách lưới"):
            time.sleep(3)
            page_base.click_obj(Obj_GuongMat.iconEdit)
            time.sleep(2)
            check_result = page_guong_mat_tab_thu_vien.do_verify_result_search_in_popup(type_of, label, value)
            allure.attach(driver.get_screenshot_as_png(), name="CheckResultEdited",
                          attachment_type=allure.attachment_type.PNG)
            assert check_result, "Kết quả tìm kiếm không hiển thị chính xác dữ liệu"

    @allure.testcase("c4i2-347", "c4i2-347")
    @allure.story("Tìm kiếm Gương mặt trong thư viện thành công")
    @allure.title("Lọc theo Giới tính")
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_search_filter_by_gender(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm gương mặt thành công - Lọc theo Giới tính"""
        driver = browser
        page_base = PageBase(driver)
        page_guong_mat_tab_thu_vien = PageGuongMatTabThuVien(driver)
        page_base.show_overlay_text("Lọc theo Giới tính")

        label_search = "Giới tính"
        json_data_handler = JsonDataHandler(Data_Search)
        type_of, label, value = json_data_handler.get_info_by_label(label_search)

        gender_search = value
        with allure.step("Chọn option Giới tính cần lọc tại tab Tìm kiếm"):
            time.sleep(2)
            txt_search_bsx = ObjCommon.label_dropdown_list("Giới tính")
            page_base.select_key_dropdown(txt_search_bsx, gender_search)
            capture_screenshot_and_attach_allure(driver, name="EnterName")
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
            check_exit_in_pop_up = page_base.check_element_visibility(Obj_GuongMat.iconEdit)
            assert check_exit_in_pop_up, "Không trả về kết quả tìm kiếm trên danh sách lưới !"
        with allure.step("Kiểm tra kết quả xuất hiện đầu tiên trên danh sách lưới"):
            time.sleep(3)
            page_base.click_obj(Obj_GuongMat.iconEdit)
            time.sleep(2)
            check_result = page_guong_mat_tab_thu_vien.do_verify_result_search_in_popup(type_of, label, value)
            allure.attach(driver.get_screenshot_as_png(), name="CheckResultEdited",
                          attachment_type=allure.attachment_type.PNG)
            assert check_result, "Kết quả tìm kiếm không hiển thị chính xác dữ liệu"

    @allure.testcase("c4i2-350", "c4i2-350")
    @allure.story("Tìm kiếm Gương mặt trong thư viện thành công")
    @allure.title("Lọc theo Độ tuổi")
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_search_filter_by_age(self, browser, FromAge, ToAge):
        """Trường hợp kiểm thử Tìm kiếm gương mặt thành công - Lọc theo Độ tuổi"""
        driver = browser
        page_base = PageBase(driver)
        page_guong_mat_tab_thu_vien = PageGuongMatTabThuVien(driver)
        page_base.show_overlay_text("Lọc theo Độ tuổi")

        label_search = "Tuổi"

        with allure.step("Thiết lập độ tuổi bắt đầu"):
            time.sleep(2)
            input_search_age = ObjCommon.input_search_number("Từ")
            page_base.send_key_input(input_search_age, FromAge)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, "SetFromAge")
        with allure.step("Thiết lập độ tuổi kết thúc"):
            time.sleep(2)
            input_search_age = ObjCommon.input_search_number("Đến")
            page_base.send_key_input(input_search_age, ToAge)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, "SetToAge")
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            time.sleep(5)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
            check_exit_in_pop_up = page_base.check_element_visibility(Obj_GuongMat.iconEdit)
            assert check_exit_in_pop_up, "Không trả về kết quả tìm kiếm trên danh sách lưới !"
        with allure.step("Kiểm tra kết quả xuất hiện đầu tiên trên danh sách lưới"):
            time.sleep(3)
            page_base.click_obj(Obj_GuongMat.iconEdit)
            time.sleep(3)
            check_result = page_guong_mat_tab_thu_vien.do_verify_age_search_in_popup(label_search, FromAge, ToAge)
            allure.attach(driver.get_screenshot_as_png(), name="CheckResultEdited",
                          attachment_type=allure.attachment_type.PNG)
            assert check_result, "Kết quả tìm kiếm không hiển thị hoăc hiển thị không chính xác dữ liệu tuổi đã lọc"

    @allure.testcase("c4i2-351", "c4i2-351")
    @allure.story("Tìm kiếm Gương mặt trong thư viện thành công")
    @allure.title("Lọc theo Ngày sinh")
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_search_filter_by_date_of_birth(self, browser, FromDate, ToDate):
        """Trường hợp kiểm thử Tìm kiếm gương mặt thành công - Lọc theo Ngày sinh"""
        driver = browser
        page_base = PageBase(driver)
        page_guong_mat_tab_thu_vien = PageGuongMatTabThuVien(driver)
        page_base.show_overlay_text("Lọc theo Ngày sinh")

        label_search = "Ngày sinh"

        with allure.step("Thiết lập độ tuổi bắt đầu"):
            txt_search_time = ObjCommon.txt_search_time("Từ")
            input_search_time = ObjCommon.input_search_time("Từ")
            page_base.click_obj(txt_search_time)
            page_base.send_key_input(input_search_time, FromDate)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, "SetFromDate")
        with allure.step("Thiết lập độ tuổi kết thúc"):
            txt_search_time = ObjCommon.txt_search_time("Đến")
            input_search_time = ObjCommon.input_search_time("Đến")
            page_base.click_obj(txt_search_time)
            page_base.send_key_input(input_search_time, ToDate)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, "SetToDate")
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
            check_exit_in_pop_up = page_base.check_element_visibility(Obj_GuongMat.iconEdit)
            assert check_exit_in_pop_up, "Không trả về kết quả tìm kiếm trên danh sách lưới !"
        with allure.step("Kiểm tra kết quả xuất hiện đầu tiên trên danh sách lưới"):
            time.sleep(3)
            page_base.click_obj(Obj_GuongMat.iconEdit)
            time.sleep(3)
            check_result = page_guong_mat_tab_thu_vien.do_verify_birth_day_in_pop_up(label_search, FromDate, ToDate)
            allure.attach(driver.get_screenshot_as_png(), name="CheckResultEdited",
                          attachment_type=allure.attachment_type.PNG)
            assert check_result, "Kết quả tìm kiếm không hiển thị hoặc hiển thị không chính xác dữ liệu"

    @pytest.mark.UAT_DC
    @allure.testcase("c4i2-344", "c4i2-344")
    @allure.story("Tìm kiếm Gương mặt trong thư viện thành công")
    @allure.title("c4i2-344: Search hình ảnh Gương mặt")
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_search_single_face_in_image_success(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm gương mặt thành công - Search hình ảnh Gương mặt"""
        driver = browser
        page_base = PageBase(driver)
        page_guong_mat = PageGuongMat(driver)
        page_guong_mat_tab_thu_vien = PageGuongMatTabThuVien(driver)
        page_base.show_overlay_text("Search hình ảnh gương mặt")

        label_search = "Ảnh chính"
        json_data_handler = JsonDataHandler(Data_Search)
        type_of, label, value = json_data_handler.get_info_by_label(label_search)

        value_image = value
        with allure.step("Tải hình ảnh gương mặt lên tab Tìm kiếm"):
            page_guong_mat.do_fill_image_face_search(value_image)
            capture_screenshot_and_attach_allure(driver, name="FillImage")
            time.sleep(2)
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
            check_exit_in_pop_up = page_base.check_element_visibility(Obj_GuongMat.iconEdit)
            assert check_exit_in_pop_up, "Không trả về kết quả tìm kiếm trên danh sách lưới !"
        with allure.step("Kiểm tra kết quả xuất hiện đầu tiên trên danh sách lưới"):
            time.sleep(3)
            page_base.click_obj(Obj_GuongMat.iconEdit)
            time.sleep(2)
            label_search = "Họ và tên"
            type_of, label, value = json_data_handler.get_info_by_label(label_search)

            check_result = page_guong_mat_tab_thu_vien.do_verify_result_search_in_popup(type_of, label, value)
            allure.attach(driver.get_screenshot_as_png(), name="CheckResultEdited",
                          attachment_type=allure.attachment_type.PNG)
            assert check_result, "Kết quả tìm kiếm không hiển thị chính xác dữ liệu"

    @allure.testcase("c4i2-344", "c4i2-344")
    @allure.story("Tìm kiếm Gương mặt trong thư viện không thành công")
    @allure.title("Search hình ảnh bị mờ, không rõ Gương mặt")
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_search_unclear_image_failure(self, browser, Data_Search):
        """Trường hợp kiểm thử Tìm kiếm gương mặt không thành công - Search hình ảnh bị mờ, không rõ Gương mặt"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_guong_mat = PageGuongMat(driver)
        page_base.show_overlay_text("Search hình ảnh bị mờ, không rõ Gương mặt")

        label_search = "Gương mặt"
        json_data_handler = JsonDataHandler(Data_Search)
        type_of, label, value = json_data_handler.get_info_by_label(label_search)

        value_image = value
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

    @allure.testcase("c4i2-", "c4i2-")
    @allure.story("Tìm kiếm Gương mặt trong thư viện thành công")
    @allure.title("Nhấn Đặt lại (danh sách load về mặc định, các giá trị lọc bị remove)")
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_reset_button_behavior(self, browser, Data_Search):
        """Trường hợp kiểm thử nhấn Đặt lại (danh sách load về mặc định, các giá trị lọc bị remove)"""
        driver = browser
        page_base = PageBase(driver)
        page_guong_mat_tab_phat_hien = PageGuongMatTabPhatHien(driver)
        page_base.show_overlay_text("Kiểm thử nhấn Đặt lại")

        label_search = "Họ và tên"
        json_data_handler = JsonDataHandler(Data_Search)
        type_of, label, value = json_data_handler.get_info_by_label(label_search)

        name_search = value
        with allure.step("Nhập thông tin Họ và tên vào tab Tìm kiếm"):
            time.sleep(2)
            page_base.send_key_input(Obj_GuongMat.txtSearchNameLib, name_search)
            capture_screenshot_and_attach_allure(driver, name="EnterName")

        label_search = "CMND/CCCD/Hộ chiếu"
        json_data_handler = JsonDataHandler(Data_Search)
        type_of, label, value = json_data_handler.get_info_by_label(label_search)

        id_search = value
        with allure.step("Nhập thông tin CMND vào tab Tìm kiếm"):
            time.sleep(2)
            page_base.send_key_input(Obj_GuongMat.txtSearchID, id_search)
            capture_screenshot_and_attach_allure(driver, name="EnterName")

        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")

        with allure.step("Nhấn vào button Đặt lại"):
            page_base.click_obj(Obj_GuongMat.btnResetLibrary)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="Reset")

        with allure.step("Kiểm tra giá trị đã nhập/chọn"):
            capture_screenshot_and_attach_allure(driver, name="Reset")
            verify_name = page_guong_mat_tab_phat_hien.do_verify_data_cleaned(Obj_GuongMat.txtSearchGuongMat)
            verify_id = page_guong_mat_tab_phat_hien.do_verify_data_cleaned(Obj_GuongMat.txtSearchID)
            assert verify_name and verify_id, "Resert giá trị nhập không thành công"

    @pytest.mark.UAT_DC
    @allure.testcase("c4i2-308", "c4i2-308")
    @allure.story("Tìm kiếm Gương mặt trong thư viện thành công")
    @allure.title("c4i2-308: Xác minh có thể tìm kiếm công dân trong danh sách theo dõi")
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_search_in_tracking_list(self, browser, Data_Search, data_watchlist):
        """Trường hợp kiểm thử Tìm kiếm Gương mặt thành công - Search tìm kiếm công dân trong danh sách theo dõi"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        time.sleep(1)
        page_base.show_overlay_text("Search công dân trong danh sách theo dõi")

        label_search = "Họ và tên"
        json_data_handler = JsonDataHandler(Data_Search)
        type_of, label, value = json_data_handler.get_info_by_label(label_search)

        name_search = value

        with allure.step("Nhập thông tin Họ và tên vào tab Tìm kiếm"):
            time.sleep(2)
            page_base.send_key_input(Obj_GuongMat.txtSearchGuongMat, name_search)
            capture_screenshot_and_attach_allure(driver, name="EnterName")
        with allure.step("Chọn option Loại theo dõi cần lọc tại tab Tìm kiếm"):
            time.sleep(2)
            txt_search_bsx = ObjCommon.label_dropdown_list("Danh sách theo dõi")
            page_base.select_key_dropdown(txt_search_bsx, data_watchlist)
            capture_screenshot_and_attach_allure(driver, name="EnterName")
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
        with allure.step("Kiểm tra kết quả trả về có tên công dân đã gắn theo dõi hay không"):
            cellid = "name"
            index = 0
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, value,
                                                                            index)
            capture_screenshot_and_attach_allure(driver, name="VerifyInGrid")
            assert result, f"Trên danh sách lưới có tên gương mặt '{different_value}' khác với giá trị gương mặt mong muốn '{value}"

    @pytest.mark.UAT_DC
    @allure.testcase("c4i2-309 ", "c4i2-309")
    @allure.story("Tìm kiếm Gương mặt trong thư viện thành công")
    @allure.title("c4i2-309: Xác minh có thể tìm kiếm công dân thuộc danh sách miễn trừ")
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_search_search_in_exemption_list(self, browser, Data_Search, data_listType):
        """Trường hợp kiểm thử Tìm kiếm Gương mặt thành công - Search tìm kiếm công dân trong danh sách miễn trừ"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        time.sleep(1)
        page_base.show_overlay_text("Search công dân trong danh sách miễn trừ")

        label_search = "Họ và tên"
        json_data_handler = JsonDataHandler(Data_Search)
        type_of, label, value = json_data_handler.get_info_by_label(label_search)

        name_search = value
        with allure.step("Nhập thông tin Họ và tên vào tab Tìm kiếm"):
            time.sleep(2)
            page_base.send_key_input(Obj_GuongMat.txtSearchGuongMat, name_search)
            capture_screenshot_and_attach_allure(driver, name="EnterName")
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
            check_exit_in_pop_up = page_base.check_element_visibility(Obj_GuongMat.iconEdit)
            assert check_exit_in_pop_up, "Không trả về kết quả tìm kiếm trên danh sách lưới !"
        with allure.step("Thêm công dân vào danh sách miễn trừ"):
            time.sleep(2)
            page_base.click_obj(Obj_GuongMat.iconEdit)
            page_base.do_scroll_mouse_to_element(Obj_GuongMat.elementScrollDown)
            capture_screenshot_and_attach_allure(driver, "BeforeAddExcept")

            page_base.click_obj(Obj_GuongMat.btnCapNhatDanhSachMienTru)
            page_base.click_obj(ObjCommon.toggle_checkbox("Kích hoạt"))

            page_base.click_obj(Obj_GuongMat.inputDateInPopUp)
            page_base.click_obj(Obj_GuongMat.btnDateNow)

            page_base.click_obj(ObjCommon.toggle_checkbox("Không thời hạn"))
            page_base.click_obj(Obj_GuongMat.btnCapNhatFace)
            capture_screenshot_and_attach_allure(driver, "AfterAddExcept")
            page_base.click_obj(Obj_GuongMat.btnCapNhatFace)
        with allure.step("Chọn option Danh sách miễn trừ cần lọc tại tab Tìm kiếm"):
            time.sleep(2)
            txt_search_bsx = ObjCommon.label_dropdown_list("Danh sách")
            page_base.select_key_dropdown(txt_search_bsx, data_listType)
            capture_screenshot_and_attach_allure(driver, name="EnterName")
        with allure.step("Kiểm tra kết quả trả về có tên công dân đã thêm vào danh sách miễn trừ hay không"):
            cellid = "name"
            index = 0
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, value,
                                                                            index)
            capture_screenshot_and_attach_allure(driver, name="VerifyInGrid")
            assert result, f"Trên danh sách lưới có tên gương mặt '{different_value}' khác với giá trị gương mặt mong muốn '{value}"

    @pytest.mark.UAT_DC
    @allure.testcase("c4i2-337", "c4i2-337")
    @allure.story("Tìm kiếm Gương mặt trong thư viện thành công")
    @allure.title("c4i2-337: Xác minh có thể thêm thông tin theo dõi cho công dân")
    @pytest.mark.LPR
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_add_face_into_tracking_list(self, browser, Data_Search, data_listTracking):
        """Trường hợp kiểm thử xác minh có thể thêm thông tin theo dõi cho công dân trong thư viện"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        time.sleep(1)
        page_base.show_overlay_text("Thêm theo dõi cho công dân")
        label_search = "Họ và tên"
        json_data_handler = JsonDataHandler(Data_Search)
        type_of, label, value = json_data_handler.get_info_by_label(label_search)

        name_search = value
        with allure.step("Nhập thông tin Họ và tên vào tab Tìm kiếm"):
            time.sleep(2)
            page_base.send_key_input(Obj_GuongMat.txtSearchGuongMat, name_search)
            capture_screenshot_and_attach_allure(driver, name="EnterName")
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
            check_exit_in_pop_up = page_base.check_element_visibility(Obj_GuongMat.iconEdit)
            assert check_exit_in_pop_up, "Không trả về kết quả tìm kiếm trên danh sách lưới !"
        with allure.step("Nhấn vào icon Chỉnh sửa"):
            time.sleep(2)
            page_base.click_obj(Obj_GuongMat.iconEdit)
            capture_screenshot_and_attach_allure(driver, name="PopupDetail")
        with allure.step("Nhấn vào button Thêm theo dõi"):
            page_base.do_scroll_mouse_to_element(Obj_GuongMat.elementScrollDown)
            page_base.click_obj(Obj_GuongMat.btnThemTheoDoi)
            capture_screenshot_and_attach_allure(driver, "BeforeAddTracking")
        with allure.step("Thêm thông tin theo dõi"):
            dropdown_tracking = ObjCommon.label_dropdown_list("Theo dõi")
            page_base.select_key_dropdown(dropdown_tracking, data_listTracking)
            page_base.click_obj(ObjCommon.toggle_switch("Kích hoạt"))
            page_base.click_obj(ObjCommon.toggle_checkbox("Thời hạn"))
            capture_screenshot_and_attach_allure(driver, "PopupAddTracking")
        with allure.step("Nhấn vào button 'Xác nhận'"):
            page_base.click_obj(Obj_GuongMat.btnXacNhan)
            capture_screenshot_and_attach_allure(driver, "AfterpAddTracking")
        with allure.step("Nhấn vào button 'Cập nhật'"):
            page_base.click_obj(Obj_GuongMat.btnCapNhatFace)
            time.sleep(2)
            check_popup = page_common.verify_notify_popup('Cập nhật thành công')
            assert check_popup, "Chỉnh sửa Công dân không thành công"

    # @pytest.mark.depends(on=['test_add_face_into_tracking_list'])
    @pytest.mark.run(after='test_add_face_into_tracking_list')
    @pytest.mark.UAT_DC
    @allure.testcase("c4i2-1490", "c4i2-1490")
    @allure.story("Tìm kiếm Gương mặt trong thư viện thành công")
    @allure.title("c4i2-1490: Xác minh có thể xóa thông tin theo dõi công dân")
    @pff.parametrize(path=pathDataTestSearchFs, key="test_add_face_into_tracking_list")
    @pytest.mark.LPR
    def test_delete_tracking_information(self, browser, Data_Search, data_listTracking):
        """Trường hợp kiểm thử xác minh có thể xóa thông tin theo dõi cho công dân trong thư viện"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        time.sleep(1)
        page_base.show_overlay_text("Xóa theo dõi công dân")
        label_search = "Họ và tên"
        json_data_handler = JsonDataHandler(Data_Search)
        type_of, label, value = json_data_handler.get_info_by_label(label_search)

        name_search = value
        with allure.step("Nhập thông tin Họ và tên vào tab Tìm kiếm"):
            time.sleep(2)
            page_base.send_key_input(Obj_GuongMat.txtSearchGuongMat, name_search)
            capture_screenshot_and_attach_allure(driver, name="EnterName")
        with allure.step("Nhấn vào button 'Tìm kiếm'"):
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="ClickSearch")
            check_exit_in_pop_up = page_base.check_element_visibility(Obj_GuongMat.iconEdit)
            assert check_exit_in_pop_up, "Không trả về kết quả tìm kiếm trên danh sách lưới !"
        with allure.step("Nhấn vào icon Chỉnh sửa"):
            time.sleep(2)
            page_base.click_obj(Obj_GuongMat.iconEdit)
            capture_screenshot_and_attach_allure(driver, name="PopupDetail")
        with allure.step("Xóa thông tin theo dõi công dân"):
            page_base.do_scroll_mouse_to_element(Obj_GuongMat.elementScrollDown)
            capture_screenshot_and_attach_allure(driver, "BeforeDeleteTracking")
            page_base.click_obj(ObjGuongmatFuntion.icon_delete_tracking(data_listTracking))
            capture_screenshot_and_attach_allure(driver, "AfterDeleteTracking")
        with allure.step("Nhấn vào button 'Xác nhận'"):
            page_base.click_obj(Obj_GuongMat.btnXacNhan)
            capture_screenshot_and_attach_allure(driver, "PopupAddTracking")
        with allure.step("Nhấn vào button 'Cập nhât'"):
            page_base.click_obj(Obj_GuongMat.btnCapNhatFace)
            time.sleep(2)
            check_popup = page_common.verify_notify_popup('Cập nhật thành công')
            assert check_popup, "Chỉnh sửa Công dân không thành công"
