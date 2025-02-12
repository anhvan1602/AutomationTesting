import time
import pytest
import allure
import datetime

from Libraries.Framework.FactoryDrivers import get_chrome_driver
from Libraries.Framework.Utils import PageBase
from Libraries.Config import Default
from PageObjects.Web.Obj_Common import ObjCommon
from PageObjects.Web.Obj_GuongMat import Obj_GuongMat
from WebApplications.PageCommon import PageCommon
from WebApplications.PageHome import LoginPage
from WebApplications.PageGuongMat import PageGuongMatTabPhatHien, PageGuongMat
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
    page_base = PageBase(driver)
    driver.get(url)
    page_login.do_login(username, password)
    page_login.click_obj(Obj_GuongMat.iconNhanDangGuongMat)
    page_base.click_obj(Obj_GuongMat.tabPhatHien)
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


@allure.epic("Nhận dạng gương mặt")
@allure.feature("Phát hiện Gương mặt")
@pytest.mark.FS
@pytest.mark.SearchDetectFace
class Test_FacePhatHienSearch:
    pageBase = PageBase(browser)
    pathDataTestSearchFs = pageBase.load_path_data_file_from_path("Datas_FS",
                                                                  "Test_PhatHien_Search_GuongMat.json")

    @pytest.mark.skipif(
        datetime.datetime.now().weekday() in [5,
                                              6] or datetime.datetime.now().hour >= 17 or datetime.datetime.now().hour < 8,
        reason="Testcase is skipped on Saturday, Sunday, or from 5 PM to 8 AM"
    )
    @pytest.mark.DC
    @pytest.mark.UAT_DC
    @pytest.mark.Quick_Scan
    @allure.testcase("c4i2-708", "c4i2-708")
    @allure.story("Tìm kiếm Gương mặt được phát hiện thành công")
    @allure.title("c4i2-708: Xác minh hệ thống vẫn đang hoạt động và cập nhật liên tục")
    # unit type ['seconds, 'minutes', 'hours', 'days']
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_verify_system_operation_and_continuous_update(self, browser, value, unit):
        """Trường hợp kiểm thử xác minh hệ thống vẫn hoạt động và cập nhật liên tục dữ liệu Gương mặt"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        time.sleep(1)
        page_base.show_overlay_text("Kiểm tra hệ thống")
        with allure.step("Lấy giá trị thời gian Gương mặt được phát hiện trên danh sách lưới"):
            txtTabPhatHien = f'//div[contains(@class,"tab-header")]//span[text()="Phát hiện"]'
            page_base.click_obj(txtTabPhatHien)
            time.sleep(1)
            cellid = "details"
            datatest = page_common.do_get_data_test_in_grid(cellid)
            value_time = [item[-1] for item in datatest]
            first_license = value_time[0]
            allure.attach("\n".join(map(str, first_license)), "Giá trị Test", allure.attachment_type.TEXT)
            capture_screenshot_and_attach_allure(driver, name="valuefirst")
        with allure.step("Lấy khoảng thời gian cần verify"):
            current_time, past_time = page_common.get_current_and_past_time(value, unit)
            current_time = page_common.format_datetime(current_time)
            past_time = page_common.format_datetime(past_time)
            allure.attach(f"{past_time}: {current_time}", "Khoảng thời gian kỳ vọng:", allure.attachment_type.TEXT)
        with allure.step("Verify thời gian thực tế có nằm trong khoảng thời gian mong muốn hay không"):
            result = page_common.is_valid_tim_range(first_license, past_time, current_time)
            assert result, f"Kết quả phát hiện mới nhất không nằm trong khoảng thời gian kỳ vọng"

    @pytest.mark.UAT_DC
    @pytest.mark.Add_DataList
    @allure.testcase("c4i2-308", "c4i2-308")
    @allure.story("Tìm kiếm Gương mặt được phát hiện thành công")
    @allure.title("c4i2-308: Search Họ và tên")
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_search_name_success(self, browser, Label, Value):
        """Trường hợp kiểm thử Tìm kiếm Gương mặt thành công - Search Họ và tên"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        time.sleep(1)
        page_base.show_overlay_text("Search Họ và tên")
        with allure.step("Nhập Họ và tên công dân cần tìm vào tab Tìm kiếm"):
            value_guong_mat = Value
            label_guong_mat = Label
            page_base.send_key_input(ObjCommon.input_search(label_guong_mat), value_guong_mat)
            capture_screenshot_and_attach_allure(driver, name="EnterInfo")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="SearchName")
        with allure.step("Kiểm tra Họ và tên của tất cả kết quả trả về trên grid"):
            cellid = "details"
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, value_guong_mat)
            capture_screenshot_and_attach_allure(driver, name="VerifyInGrid")
            assert result, f"Trên danh sách lưới có tên gương mặt '{different_value}' khác với giá trị gương mặt mong muốn '{value_guong_mat}"

    @pytest.mark.UAT_DC
    @pytest.mark.Add_DataList
    @allure.testcase("c4i2-309", "c4i2-309")
    @allure.story("Tìm kiếm Gương mặt được phát hiện thành công")
    @allure.title("c4i2-309: Search CMND/CCCD/Hộ chiếu")
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_search_id_card_success(self, browser, Label, Value):
        """Trường hợp kiểm thử Tìm kiếm Gương mặt thành công - Search CMND/CCCD/Hộ chiếu"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        time.sleep(1)
        page_base.show_overlay_text("Search CMND/CCCD/Hộ chiếu")
        with allure.step("Nhập CMND/CCCD/Hộ chiếu cần tìm vào tab Tìm kiếm"):
            value_cmnd = Value
            label_cmnd = Label
            page_base.send_key_input(ObjCommon.input_search(label_cmnd), value_cmnd)
            capture_screenshot_and_attach_allure(driver, name="EnterInfo")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="SearchID")
        with allure.step("Kiểm tra CMND/CCCD/Hộ chiếu của tất cả kết quả trả về trên grid"):
            cellid = "details"
            index = 0
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, value_cmnd,
                                                                            index)
            capture_screenshot_and_attach_allure(driver, name="VerifyInGrid")
            assert result, f"Trên danh sách lưới có CMND/CCCD/Hộ chiếu '{different_value}' khác với giá trị CMND/CCCD/Hộ chiếu mong muốn '{value_cmnd}"

    @pytest.mark.DC
    @pytest.mark.UAT_DC
    @pytest.mark.Add_DataList
    @allure.testcase("c4i2-307", "c4i2-307")
    @allure.story("Tìm kiếm Gương mặt được phát hiện thành công")
    @allure.title("c4i2-307: Search 1 Gương mặt (search image)")
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_search_single_face_image_success(self, browser, Label, Value):
        """Trường hợp kiểm thử Tìm kiếm Gương mặt thành công - Search 1 Gương mặt (search image)"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_guong_mat = PageGuongMat(driver)
        time.sleep(1)
        page_base.show_overlay_text("Search 1 gương mặt (search image)")
        with allure.step("Tải hình ảnh Gương mặt lên tab Tìm kiếm"):
            value_image = Value
            label_image = Label
            page_guong_mat.do_fill_image_face_search(value_image)
            capture_screenshot_and_attach_allure(driver, name="FillImage")
            time.sleep(2)
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="SearchImage")
        with allure.step("Kiểm tra kết quả trả về trên danh sách lưới"):
            cellid = "details"
            index = 0
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, label_image,
                                                                            index)
            capture_screenshot_and_attach_allure(driver, name="VerifyInGrid")
            assert result, f"Trên danh sách lưới có hình ảnh gương mặt '{different_value}' khác với giá trị hình ảnh gương mặt mong muốn '{label_image}"

    @pytest.mark.DC
    @pytest.mark.Add_DataList
    @allure.testcase("c4i2-755", "c4i2-755")
    @allure.story("Tìm kiếm Gương mặt được phát hiện thành công")
    @allure.title("Search by image (with multiple faces)")
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_search_multi_face_image_success(self, browser, TypeOf, Label, Value):
        """Trường hợp kiểm thử Tìm kiếm Gương mặt thành công - Tìm kiếm bằng 1 hình ảnh có nhiều gương mặt"""
        driver = browser
        page_base = PageBase(driver)
        page_guong_mat = PageGuongMat(driver)
        page_common = PageCommon(driver)

        time.sleep(1)
        page_base.show_overlay_text("Search 1 image (multiple Face)")
        with allure.step("Tải hình ảnh gương mặt lên tab Tìm kiếm"):
            value_image = Value
            page_guong_mat.do_fill_image_face_search(value_image)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="FillImage")
        with allure.step("Mở rộng thông tin danh sách lưới"):
            time.sleep(2)
            page_base.click_obj(Obj_GuongMat.btnMoRongGrid)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="ExtendGrid")

        with allure.step("Chọn tuỳ chọn thời gian trong 30 ngày"):
            time.sleep(2)
            txt_option_time = f'//div[@class="checkbox-form" and .//*[contains(text(),"Khoảng thời gian")]]//span[@class="radio-input checkbox--icon-md"]'
            page_base.do_scroll_mouse_to_element(txt_option_time)
            time.sleep(1)
            page_base.click_obj(txt_option_time)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="Chọn tuỳ chọn thời gian trong 30 ngày")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="SearchImage")
        list_label = Label
        face_names = TypeOf
        for face_name, value_name in zip(face_names, list_label):
            with allure.step(f"Kiểm tra kết quả '{face_name}' trả về trên danh sách lưới"):
                txt_search_face = ObjCommon.label_dropdown_list("Chọn khuôn mặt")
                page_base.select_key_dropdown(txt_search_face, face_name)
                time.sleep(1)
                cellid = "details"
                index = 0
                list_actual = page_common.do_get_data_test_in_grid(cellid)
                result, different_value = page_common.do_verify_results_in_grid(list_actual, value_name,
                                                                                index)
                capture_screenshot_and_attach_allure(driver, name=f"VerifyInGrid_{face_name}")
                assert result, f"Trên danh sách lưới có hình ảnh gương mặt '{different_value}' khác với giá trị hình ảnh gương mặt mong muốn '{value_name}"

    @pytest.mark.Add_DataList
    @allure.testcase("c4i2-", "c4i2-")
    @allure.story("Tìm kiếm Gương mặt được phát hiện không thành công")
    @allure.title("Search image không rõ Gương mặt")
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_search_unclear_image_failure(self, browser, Value, expected):
        """Trường hợp kiểm thử Tìm kiếm Gương mặt không thành công - Search image không rõ Gương mặt"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_guong_mat = PageGuongMat(driver)
        time.sleep(1)
        page_base.show_overlay_text("Search image không rõ Gương mặt")
        with allure.step("Tải hình ảnh gương mặt lên tab Tìm kiếm"):
            value_image = Value
            page_guong_mat.do_fill_image_face_search(value_image)
            capture_screenshot_and_attach_allure(driver, name="FillImage")
            time.sleep(2)
        with allure.step("Kiểm tra thông báo lỗi"):
            check_popup = page_common.verify_notify_error(expected)
            capture_screenshot_and_attach_allure(driver, name="NotifyUnSuccess")
            assert check_popup, "Không có thông báo hoặc thông báo không hợp lệ khi tải ảnh không rõ gương mặt"

    @pytest.mark.Add_DataList
    @allure.testcase("c4i2-312", "c4i2-312")
    @allure.story("Tìm kiếm Gương mặt được phát hiện thành công")
    @allure.title("Lọc theo độ chính xác")
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_filter_by_accuracy_success(self, browser, From, To):
        """Trường hợp kiểm thử Tìm kiếm Gương mặt thành công - Lọc theo độ chính xác"""
        driver = browser
        page_base = PageBase(driver)
        page_guong_mat_tab_phat_hien = PageGuongMatTabPhatHien(driver)
        time.sleep(1)
        cellid = "candidateRT"
        page_base.show_overlay_text("Lọc theo độ chính xác")

        with allure.step("Thiết lập độ chính xác cần tìm kiếm"):
            page_guong_mat_tab_phat_hien.do_move_slider(From, To)
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="SearchFace")
        with allure.step("Kiểm tra độ chính xác các kết quả trả về trên danh sách lưới"):
            capture_screenshot_and_attach_allure(driver, name="ResultInGrid")
            result = page_guong_mat_tab_phat_hien.do_verify_accuracy_face(cellid, From, To)
            assert result, f"Hiển thị danh sách kết quả lọc theo độ chính xác không hợp lệ"

    @pytest.mark.UAT_DC
    @pytest.mark.Add_DataList
    @allure.testcase("c4i2-313", "c4i2-313")
    @allure.story("Tìm kiếm Gương mặt được phát hiện thành công")
    @allure.title("c4i2-313: Lọc theo khoảng thời gian")
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_filter_by_time_range_success(self, browser, startTime, endTime):
        """Trường hợp kiểm thử Tìm kiếm Gương mặt thành công - Lọc theo khoảng thời gian"""
        driver = browser
        page_base = PageBase(driver)
        page_guong_mat_tab_phat_hien = PageGuongMatTabPhatHien(driver)
        time.sleep(1)
        page_base.show_overlay_text("Lọc theo khoảng thời gian")
        with allure.step("Check vào checkbox lọc theo Khoảng thời gian"):
            xpathchecksearch = ObjCommon.radio_button("Khoảng thời gian")
            scrolltoelement = ObjCommon.radio_button("Cách đây")
            page_base.do_scroll_mouse_to_element(xpathchecksearch)
            time.sleep(1)
            page_base.click_obj(xpathchecksearch)
            capture_screenshot_and_attach_allure(driver, "CheckBox")
        with allure.step("Thiết lập khoảng thời gian bắt đầu"):
            txt_search_time = ObjCommon.txt_search_time("Từ")
            input_search_time = ObjCommon.input_search_time("Từ")
            page_base.do_scroll_mouse_to_element(scrolltoelement)
            page_base.click_obj(txt_search_time)
            page_base.send_key_input(input_search_time, startTime)
            time.sleep(1)
            page_base.click_obj(xpathchecksearch)
            capture_screenshot_and_attach_allure(driver, "SetTime")
        with allure.step("Thiết lập khoảng thời gian kết thúc"):
            txt_search_time = ObjCommon.txt_search_time("Đến")
            input_search_time = ObjCommon.input_search_time("Đến")
            page_base.do_scroll_mouse_to_element(scrolltoelement)
            page_base.click_obj(txt_search_time)
            page_base.send_key_input(input_search_time, endTime)
            time.sleep(1)
            page_base.click_obj(xpathchecksearch)
            capture_screenshot_and_attach_allure(driver, "SetTime")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="SearchFace")
        with allure.step("Kiểm tra thời gian phát hiện các kết quả trả về trên danh sách lưới"):
            capture_screenshot_and_attach_allure(driver, name="ResultInGrid")
            cellid = "details"
            result = page_guong_mat_tab_phat_hien.do_verify_time_range_face(cellid, startTime, endTime)
            assert result, f"Hiển thị danh sách kết quả lọc theo khoảng thời gian không hợp lệ"

    @pytest.mark.UAT_DC
    @pytest.mark.Add_DataList
    @allure.testcase("c4i2-1401", "c4i2-1401")
    @allure.story("Tìm kiếm Gương mặt được phát hiện thành công")
    @allure.title("c4i2-1401: Lọc theo Mốc thời gian")
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_filter_by_timestamp_success(self, browser, ToTime):
        """Trường hợp kiểm thử Tìm kiếm Gương mặt thành công - Lọc theo Mốc thời gian"""
        driver = browser
        page_base = PageBase(driver)
        page_guong_mat_tab_phat_hien = PageGuongMatTabPhatHien(driver)
        time.sleep(1)
        cellid = "details"
        page_base.show_overlay_text("Lọc theo Mốc thời gian")

        with allure.step("Check vào checkbox lọc theo Mốc thời gian - Cách đây"):
            xpathchecksearch = ObjCommon.radio_button("Cách đây")
            page_base.do_scroll_mouse_to_element(xpathchecksearch)
            page_base.click_obj(xpathchecksearch)
            capture_screenshot_and_attach_allure(driver, "CheckBox")
        with allure.step("Lựa chọn mốc thời gian cần lọc"):
            page_base.click_obj(Obj_GuongMat.txtCachDay)
            page_base.click_obj(ObjCommon.option_time_stamp(ToTime))
            capture_screenshot_and_attach_allure(driver, "SetTime")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="SearchFace")
        with allure.step("Kiểm tra thời gian phát hiện các kết quả trả về trên danh sách lưới"):
            capture_screenshot_and_attach_allure(driver, name="ResultInGrid")
            result = page_guong_mat_tab_phat_hien.do_verify_time_stamp_face(cellid, ToTime)
        assert result, f"Hiển thị danh sách kết quả lọc theo khoảng thời gian không hợp lệ"

    @pytest.mark.UAT_DC
    @pytest.mark.Add_DataList
    @allure.testcase("c4i2-310", "c4i2-310")
    @allure.story("Tìm kiếm Gương mặt được phát hiện thành công")
    @allure.title("c4i2-310: Lọc theo Camera")
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_filter_by_camera_success(self, browser, Camera):
        """Trường hợp kiểm thử Tìm kiếm Gương mặt thành công - Lọc theo Camera"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        time.sleep(1)
        page_base.show_overlay_text("Lọc theo Camera")
        with allure.step("Lựa chọn Camera cần lọc"):
            txt_search_bsx = ObjCommon.label_dropdown_list("Camera")
            page_base.select_key_dropdown(txt_search_bsx, Camera)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, "SelectCamera")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="SearchFace")
        with allure.step("Kiểm tra camera các kết quả trả về trên danh sách lưới"):
            cellid = "details"
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, Camera)
            capture_screenshot_and_attach_allure(driver, name="VerifyInGrid")
            assert result, f"Trên danh sách lưới có camera '{different_value}' khác với giá trị camera mong muốn '{Camera}"

    @pytest.mark.Add_DataList
    @allure.testcase("c4i2-1403", "c4i2-1403")
    @allure.story("Tìm kiếm Gương mặt được phát hiện thành công")
    @allure.title("Search kết hợp (Họ và tên & CMND)")
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_filter_combined_name_and_id_card_success(self, browser, LabelID, ValueID, LabelName, ValueName):
        """Trường hợp kiểm thử Tìm kiếm Gương mặt thành công - Search kết hợp (Họ và tên & CMND)"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        time.sleep(1)
        page_base.show_overlay_text("Search kết hợp (Họ và tên & CMND)")

        with allure.step("Nhập Họ và tên công dân cần tìm vào tab Tìm kiếm"):
            value_guong_mat = ValueName
            label_guong_mat = LabelName
            page_base.send_key_input(ObjCommon.input_search(label_guong_mat), value_guong_mat)
            capture_screenshot_and_attach_allure(driver, name="EnterInfo")
        with allure.step("Nhập CMND/CCCD/Hộ chiếu cần tìm vào tab Tìm kiếm"):
            value_cmnd = ValueID
            label_cmnd = LabelID
            page_base.send_key_input(ObjCommon.input_search(label_cmnd), value_cmnd)
            capture_screenshot_and_attach_allure(driver, name="EnterInfo")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="SearchFace")
        with allure.step("Kiểm tra Họ và tên của tất cả kết quả trả về trên grid"):
            cellid = "details"
            index = 1
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, value_guong_mat,
                                                                            index)
            capture_screenshot_and_attach_allure(driver, name="VerifyInGrid")
            assert result, f"Trên danh sách lưới có Họ và tên '{different_value}' khác với giá trị Họ và tên mong muốn '{value_guong_mat}"
        with allure.step("Kiểm tra CMND/CCCD/Hộ chiếu của tất cả kết quả trả về trên grid"):
            cellid = "details"
            index = 0
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, value_cmnd,
                                                                            index)
            capture_screenshot_and_attach_allure(driver, name="VerifyInGrid")
            assert result, f"Trên danh sách lưới có CMND/CCCD/Hộ chiếu '{different_value}' khác với giá trị CMND/CCCD/Hộ chiếu mong muốn '{value_cmnd}"

    @pytest.mark.Add_DataList
    @allure.testcase("c4i2-", "c4i2-")
    @allure.story("Tìm kiếm Gương mặt được phát hiện thành công")
    @allure.title("Nhấn Đặt lại (danh sách load về mặc định, các giá trị lọc bị remove)")
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_reset_button_behavior(self, browser, Label, Value):
        """Trường hợp kiểm thử nhấn Đặt lại (danh sách load về mặc định, các giá trị lọc bị remove)"""
        driver = browser
        page_base = PageBase(driver)
        page_guong_mat_tab_phat_hien = PageGuongMatTabPhatHien(driver)
        time.sleep(1)
        page_base.show_overlay_text("kiểm thử nhấn Đặt lại")

        with allure.step("Nhập Họ và tên công dân cần tìm vào tab Tìm kiếm"):
            value_guong_mat = Value
            label_guong_mat = Label
            page_base.send_key_input(ObjCommon.input_search(label_guong_mat), value_guong_mat)
            capture_screenshot_and_attach_allure(driver, name="EnterInfo")
        with allure.step("Nhấn vào button Đặt lại"):
            page_base.click_obj(Obj_GuongMat.btnReset)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="Reset")
        with allure.step("Kiểm tra giá trị đã nhập/chọn"):
            capture_screenshot_and_attach_allure(driver, name="Reset")
            result = page_guong_mat_tab_phat_hien.do_verify_data_cleaned(ObjCommon.input_search(label_guong_mat))
            assert result, "Resert giá trị nhập không thành công"

    @pytest.mark.DC
    @pytest.mark.UAT_DC
    @pytest.mark.Add_DataList
    @allure.testcase("c4i2-1406", "c4i2-1406")
    @allure.story("Tìm kiếm Gương mặt được phát hiện thành công")
    @allure.title("c4i2-1406: Xác minh có thể xem lịch sử nhận dạng đối tượng trong pop-up chi tiết")
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_face_detection_history_verification(self, browser, Label, Value):
        """Trường hợp kiểm thử xác minh có thể xem lịch sử nhận phát hiện gương mặt"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        time.sleep(1)
        page_base.show_overlay_text("Xem lịch sử phát hiện")
        cellid = "details"

        with allure.step("Nhập Họ và tên công dân cần tìm vào tab Tìm kiếm"):
            value_guong_mat = Value
            label_guong_mat = Label
            page_base.send_key_input(ObjCommon.input_search(label_guong_mat), value_guong_mat)
            capture_screenshot_and_attach_allure(driver, name="EnterInfo")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="SearchName")
        with allure.step("Kiểm tra có giá trị phát hiện trên grid hay không"):
            datatest = page_common.do_get_data_test_in_grid(cellid)
            capture_screenshot_and_attach_allure(driver, name="ViewResults")
        with allure.step("Nhấn vào button 'Xem chi tiết'"):
            page_base.click_obj(Obj_GuongMat.iconDetail)
            capture_screenshot_and_attach_allure(driver, "PageDetail")
        with allure.step("Nhấn vào button 'Lịch sử'"):
            page_base.click_obj(Obj_GuongMat.btnLichSu)
            capture_screenshot_and_attach_allure(driver, "PageDetail")
        with allure.step("Kiểm tra Lịch sử phát hiện sự kiện"):
            list_actual = page_common.do_get_data_test_on_grid_in_pop_up(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, Value)
            byte_object = bytes(str(list_actual), 'utf-8')
            allure.attach(byte_object, "Lịch sử phát hiện:", allure.attachment_type.TEXT)
            assert result, f"Lịch sử phát hiện có giá trị '{different_value}' khác với giá trị kỳ vọng '{Value}"
            capture_screenshot_and_attach_allure(driver, name="Check")

    @pytest.mark.DC
    @pytest.mark.UAT_DC
    @pytest.mark.Add_DataList
    @allure.testcase("c4i2-1407", "c4i2-1407")
    @allure.story("Tìm kiếm Gương mặt được phát hiện thành công")
    @allure.title("c4i2-1407: Xác minh có thể thêm theo dõi cho đối tượng")
    @pff.parametrize(path=pathDataTestSearchFs)
    def test_add_tracking_to_detected_face(self, browser, Label, Value, data_watchlist):
        """Trường hợp kiểm thử xác minh có thể thêm theo dõi cho gương mặt được phát hiện"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        time.sleep(1)
        page_base.show_overlay_text("Thêm theo dõi")
        cellid = "details"
        with allure.step("Nhập Họ và tên công dân cần tìm vào tab Tìm kiếm"):
            value_guong_mat = Value
            label_guong_mat = Label
            page_base.send_key_input(ObjCommon.input_search(label_guong_mat), value_guong_mat)
            capture_screenshot_and_attach_allure(driver, name="EnterInfo")
        with allure.step("Nhấn vào button Tìm kiếm"):
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="SearchName")
        with allure.step("Kiểm tra Gương mặt của tất cả kết quả trả về trên grid"):
            index = 1
            list_actual = page_common.do_get_data_test_in_grid(cellid)
            result, different_value = page_common.do_verify_results_in_grid(list_actual, value_guong_mat, index)
            assert result, f"Trên danh sách lưới có gương mặt '{different_value}' khác với giá trị Gương mặt mong muốn '{value_guong_mat}"
        with allure.step("Nhấn vào button 'Xem chi tiết'"):
            page_base.click_obj(Obj_GuongMat.iconDetail)
            capture_screenshot_and_attach_allure(driver, "PageDetail")
        with allure.step("Nhấn vào button 'Thêm theo dõi'"):
            page_base.do_scroll_mouse_to_element(Obj_GuongMat.btnThemTheoDoi)
            time.sleep(1)
            page_base.click_obj(Obj_GuongMat.btnThemTheoDoi)
            capture_screenshot_and_attach_allure(driver, "PopupAddTracking")
        with allure.step("Chọn loại theo dõi tại popup theo dõi"):
            dropdown_tracking = ObjCommon.label_dropdown_list("Theo dõi")
            page_base.select_key_dropdown(dropdown_tracking, data_watchlist)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, "SelectTracking")
        with allure.step("Nhấn vào button 'Cập nhật'"):
            page_base.click_obj(Obj_GuongMat.btnCapNhatFace)
            capture_screenshot_and_attach_allure(driver, "UpdateTracking")
        with allure.step("Xóa thông tin tracking đã cập nhật"):
            page_base.do_scroll_mouse_to_element(Obj_GuongMat.iconDeleteTracking)
            time.sleep(1)
            page_base.click_obj(Obj_GuongMat.iconDeleteTracking)
            time.sleep(1)
            page_base.click_obj(Obj_GuongMat.btnXacNhan)
            capture_screenshot_and_attach_allure(driver, "DeleteTracking")
