import time
import pytest
import allure

from Libraries.Framework.FactoryDrivers import get_chrome_driver
from Libraries.Framework.Utils import PageBase
from Libraries.Config import Default
from PageObjects.Web.Obj_GuongMat import Obj_GuongMat
from WebApplications.PageCommon import PageCommon
from WebApplications.PageHome import LoginPage
from WebApplications.PageGuongMat import PageGuongMat
import parametrize_from_file as pff
from Libraries.Plugins.DataHandler import JsonDataHandler
from conftest import capture_screenshot_and_attach_allure, attach_table_to_allure


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


@pytest.fixture(scope='function')
def create_data(browser, Data):
    driver = browser
    page_base = PageBase(driver)
    page_guong_mat = PageGuongMat(driver)

    page_base.click_obj(Obj_GuongMat.btnThemMoiGuongMat)
    page_guong_mat.do_dien_thong_tin_cong_dan(Data)
    page_guong_mat.do_bo_sung_them_tt_cong_dan(Data)
    page_base.click_obj(Obj_GuongMat.btnLuuThemMoi)
    time.sleep(2)
    yield


@pytest.fixture(scope='function')
def clean_data(browser, save_current_url, Data):
    yield
    driver = browser
    page_base = PageBase(driver)

    driver.get(save_current_url)
    time.sleep(1)
    label_search = "CMND/ CCCD/ Hộ chiếu"
    json_data_handler = JsonDataHandler(Data)
    id_guong_mat = json_data_handler.get_value_by_label(label_search)

    page_base.send_key_input(Obj_GuongMat.txtSearchID, id_guong_mat)
    page_base.click_obj(Obj_GuongMat.btnTimKiem)

    time.sleep(3)
    page_base.click_obj(Obj_GuongMat.checkboxFace)
    time.sleep(2)
    page_base.click_obj(Obj_GuongMat.btnDelete)
    time.sleep(2)
    page_base.click_obj(Obj_GuongMat.btnXacNhan)
    time.sleep(2)


pageBase = PageBase(browser)
pathDataTestFS = pageBase.load_path_data_file_from_path("Datas_FS",
                                                   "Test_ThuVien_GuongMat.json")


@allure.epic("Nhận dạng gương mặt")
@allure.feature("Thư viện Gương mặt")
@pytest.mark.FS
@pytest.mark.Add_DataList
class Test_Add_Face:

    @pytest.mark.DC
    @allure.testcase("c4i2-334", "c4i2-334")
    @allure.story("Thêm mới Gương mặt trong thư viện thành công")
    @allure.title("Thêm mới công dân với thông tin đầy đủ")
    @pff.parametrize(pathDataTestFS)
    def test_AddFaceSuccess(self, browser, clean_data, Data):
        """Trường hợp kiểm thử thêm thông tin Công dân thành công"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_guong_mat = PageGuongMat(driver)

        page_base.click_obj(Obj_GuongMat.btnThemMoiGuongMat)
        time.sleep(1)
        page_base.show_overlay_text("Trường hợp kiểm thử thêm công dân thành công")
        attach_table_to_allure(Data)
        with allure.step("Điền thông tin công dân"):
            page_guong_mat.do_dien_thong_tin_cong_dan(Data)
            page_guong_mat.do_bo_sung_them_tt_cong_dan(Data)
            capture_screenshot_and_attach_allure(driver, name="FillInfo")
            time.sleep(2)

        with allure.step("Kiểm tra thông báo sau khi tạo thành công"):
            page_base.click_obj(Obj_GuongMat.btnLuuThemMoi)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="NotifySucess")
            check_popup = page_common.verify_notify_popup('Thêm thành công')
            assert check_popup, "Không nhận được thông báo tạo công dân mới không thành công"

        with allure.step("Tìm kiếm thông tin công dân mới đã thêm"):
            label_search = "CMND/ CCCD/ Hộ chiếu"
            json_data_handler = JsonDataHandler(Data)
            id_guong_mat = json_data_handler.get_value_by_label(label_search)

            page_base.send_key_input(Obj_GuongMat.txtSearchID, id_guong_mat)
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="FindBSX")
            check_exit_in_pop_up = page_base.check_element_visibility(Obj_GuongMat.iconEdit)
            assert check_exit_in_pop_up, "Không tìm thấy kết quả đã tạo trên danh sách lưới !"

        with allure.step("Nhấn chỉnh sửa kết quả đầu tiên"):
            time.sleep(3)
            page_base.click_obj(Obj_GuongMat.iconEdit)
            time.sleep(2)

        with allure.step("Kiểm tra kết quả đã tạo"):
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="CheckResultCreated")
            check_result = page_common.verify_result_created(Data)
            assert check_result, "Dữ liệu đã thêm không hiển thị đầy đủ"

    @allure.testcase("c4i2-335", "c4i2-335")
    @allure.story("Thêm mới Gương mặt trong thư viện không thành công")
    @allure.title("Thêm mới công dân thiếu thông tin ở trường dữ liệu bắt buộc")
    @pff.parametrize(pathDataTestFS)
    def test_AddFaceNotFillRequired(self, browser, Data, desc):
        # Thêm mô tả vào allure
        description = f"Trường hợp kiểm thử tạo công dân không thành công - {desc}"
        allure.dynamic.description(description)

        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_guong_mat = PageGuongMat(driver)

        page_base.click_obj(Obj_GuongMat.btnThemMoiGuongMat)
        time.sleep(1)
        page_base.show_overlay_text(f"Trường hợp kiểm thử tạo công dân không thành công- {desc}")
        attach_table_to_allure(Data)
        with allure.step("Điền thông tin công dân"):
            page_guong_mat.do_dien_thong_tin_cong_dan(Data)
            page_guong_mat.do_bo_sung_them_tt_cong_dan(Data)
            capture_screenshot_and_attach_allure(driver, name="FillInfo")
            time.sleep(2)

        with allure.step("Kiểm tra button Thêm mới"):
            allure.attach(driver.get_screenshot_as_png(), name="NotifyUnSuccess",
                          attachment_type=allure.attachment_type.PNG)
            check_button = page_base.check_button_clickable(Obj_GuongMat.btnLuuThemMoi)
            if check_button:
                page_base.click_obj(Obj_GuongMat.btnLuuThemMoi)
                check_popup = page_common.verify_notify_popup('CMND/ CCCD/ Hộ chiếu không được bỏ trống')
                assert check_popup, "Không có thông báo hoặc thông báo không hợp lệ khi bỏ trông trường dữ liệu bắt buộc"
            else:
                assert not check_button, f"Cho phép tạo công dân khi {desc}"

    @allure.testcase("c4i2-736", "c4i2-736")
    @allure.story("Thêm mới Gương mặt trong thư viện không thành công")
    @allure.title("Thêm mới công dân với dữ liệu CMND/CCCD/Hộ chiếu đã tồn tại trong hệ thống")
    @pff.parametrize(pathDataTestFS)
    def test_AddFaceCMNDExist(self, browser, Data, desc):
        f"""Trường hợp kiểm thử tạo thông tin Công dân không thành công - {desc}"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_guong_mat = PageGuongMat(driver)

        page_base.click_obj(Obj_GuongMat.btnThemMoiGuongMat)
        time.sleep(1)
        page_base.show_overlay_text(
            "Trường hợp kiểm thử tạo công dân không thành công - điền CMND/CCCD/Hộ chiếu đã tồn tại trong hệ thống")
        attach_table_to_allure(Data)
        with allure.step("Điền thông tin công dân"):
            page_guong_mat.do_dien_thong_tin_cong_dan(Data)
            page_guong_mat.do_bo_sung_them_tt_cong_dan(Data)
            capture_screenshot_and_attach_allure(driver, name="FillInfo")
            time.sleep(2)
        with allure.step("Kiểm tra thông báo khi điền thông tin CMND/CCCD/Hộ chiếu đã tồn tại"):
            page_base.click_obj(Obj_GuongMat.btnLuuThemMoi)
            time.sleep(0.5)
            text_notify = "CMND/ CCCD/ Hộ chiếu này đã tồn tại"
            check_notify = page_common.verify_notify_error(text_notify)
            capture_screenshot_and_attach_allure(driver, name="NotifySuccess")
            assert check_notify, "Không có thông báo khi nhập CMND / CCCD / Hộ chiếu đã tồn tại"

    @allure.testcase("c4i2-335", "c4i2-335")
    @allure.story("Thêm mới Gương mặt trong thư viện không thành công")
    @allure.title("Thêm mới công dân với hình ảnh không hợp lệ")
    @pff.parametrize(pathDataTestFS)
    def test_AddFaceImageInValid(self, browser, Data, text_notify, desc):
        """Trường hợp kiểm thử tạo thông tin Công dân không thành công - upload hình ảnh không hợp lệ"""
        description = f"Trường hợp kiểm thử tạo công dân không thành công - {desc}"
        allure.dynamic.description(description)
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_guong_mat = PageGuongMat(driver)

        page_base.click_obj(Obj_GuongMat.btnThemMoiGuongMat)
        time.sleep(1)
        page_base.show_overlay_text(f"Trường hợp kiểm thử tạo công dân không thành công - {desc}")
        attach_table_to_allure(Data)
        with allure.step("Điền thông tin công dân"):
            page_guong_mat.do_dien_thong_tin_cong_dan(Data)
            page_guong_mat.do_bo_sung_them_tt_cong_dan(Data)
            capture_screenshot_and_attach_allure(driver, name="FillInfo")
            time.sleep(2)
        with allure.step("Kiểm tra cảnh báo khi upload hình ảnh không hợp lệ"):
            capture_screenshot_and_attach_allure(driver, name="NotifySuccess")
            check_notify = page_common.verify_notify_field_required(text_notify)
            assert check_notify, "Không có cảnh báo (hoặc cảnh báo không chính xác) khi upload hình ảnh không hợp lệ"


@allure.epic("Nhận dạng gương mặt")
@allure.feature("Thư viện Gương mặt")
@pytest.mark.FS
@pytest.mark.Add_DataList
class Test_Edit_Face:

    @pytest.mark.DC
    @allure.testcase("c4i2-737", "c4i2-737")
    @allure.story("Chỉnh sửa Gương mặt trong thư viện thành công")
    @allure.title("Chỉnh sửa công dân với thông tin hợp lệ")
    @pff.parametrize(pathDataTestFS)
    def test_EditFaceSuccess(self, browser, create_data, clean_data, Data, Data_Update):
        """Trường hợp kiểm thử Chỉnh sửa Công dân thành công"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_guong_mat = PageGuongMat(driver)
        page_base.show_overlay_text("Trường hợp kiểm thử Chỉnh sửa thông tin Công dân thành công")
        attach_table_to_allure(Data, name="Initial Data")
        attach_table_to_allure(Data_Update, name="Data for Editing")
        with allure.step("Tìm kiếm Công dân"):
            time.sleep(2)
            label_search = "CMND/ CCCD/ Hộ chiếu"
            json_data_handler = JsonDataHandler(Data)
            id_guong_mat = json_data_handler.get_value_by_label(label_search)

            page_base.send_key_input(Obj_GuongMat.txtSearchID, id_guong_mat)
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="FillInfo")
            check_exit_in_pop_up = page_base.check_element_visibility(Obj_GuongMat.iconEdit)
            assert check_exit_in_pop_up, "Không tìm thấy kết quả đã tạo trên danh sách lưới !"

        with allure.step("Nhấn chỉnh sửa kết quả tìm thấy trên danh sách lưới"):
            time.sleep(2)
            page_base.click_obj(Obj_GuongMat.iconEdit)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="VewResultsFace")

        with allure.step("Chỉnh sửa thông tin Công dân"):
            page_guong_mat.do_dien_thong_tin_cong_dan(Data_Update)
            page_guong_mat.do_bo_sung_them_tt_cong_dan(Data_Update)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="EditBSX")
            page_base.click_obj(Obj_GuongMat.btnCapNhatFace)
            time.sleep(2)
            check_popup = page_common.verify_notify_popup('Cập nhật thành công')
            assert check_popup, "Chỉnh sửa Công dân không thành công"

        with allure.step("Tìm kiếm Công dân đã chỉnh sửa"):
            time.sleep(2)
            label_search = "CMND/ CCCD/ Hộ chiếu"
            json_data_handler = JsonDataHandler(Data)
            id_guong_mat = json_data_handler.get_value_by_label(label_search)

            page_base.send_key_input(Obj_GuongMat.txtSearchID, id_guong_mat)
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="FindBSX")
            check_exit_in_pop_up = page_base.check_element_visibility(Obj_GuongMat.iconEdit)
            assert check_exit_in_pop_up, "Không tìm thấy kết quả đã chỉnh sửa trên danh sách lưới"

        with allure.step("Kiểm tra kết quả đã chỉnh sửa"):
            time.sleep(3)
            page_base.click_obj(Obj_GuongMat.iconEdit)
            time.sleep(2)
            check_result = page_common.verify_result_created(Data_Update)
            allure.attach(driver.get_screenshot_as_png(), name="CheckResultEdited",
                          attachment_type=allure.attachment_type.PNG)
            assert check_result, "Dữ liệu đã thêm không hiển thị đầy đủ"

    @allure.testcase("c4i2-738", "c4i2-738")
    @allure.story("Chỉnh sửa Gương mặt trong thư viện không thành công")
    @allure.title("Chỉnh sửa công dân với hình ảnh không hợp lệ")
    @pff.parametrize(pathDataTestFS)
    def test_EditFaceImageInValid(self, browser, create_data, clean_data, Data, Data_Edit, text_notify,
                                  desc):
        """Trường hợp kiểm thử Chỉnh sửa Công dân không thành công"""
        description = f"Trường hợp kiểm thử chỉnh sửa công dân không thành công - {desc}"
        allure.dynamic.description(description)
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_guong_mat = PageGuongMat(driver)
        page_base.show_overlay_text(f"Trường hợp kiểm thử chỉnh sửa công dân không thành công - {desc}")
        attach_table_to_allure(Data, name="Initial Data")
        attach_table_to_allure(Data_Edit, name="Data for Editing")
        with allure.step("Tìm kiếm Công dân"):
            time.sleep(2)
            label_search = "CMND/ CCCD/ Hộ chiếu"
            json_data_handler = JsonDataHandler(Data)
            id_guong_mat = json_data_handler.get_value_by_label(label_search)

            page_base.send_key_input(Obj_GuongMat.txtSearchID, id_guong_mat)
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="FillInfo")
            check_exit_in_pop_up = page_base.check_element_visibility(Obj_GuongMat.iconEdit)
            assert check_exit_in_pop_up, "Không tìm thấy kết quả đã tạo trên danh sách lưới !"

        with allure.step("Nhấn chỉnh sửa kết quả tìm thấy trên danh sách lưới"):
            time.sleep(2)
            page_base.click_obj(Obj_GuongMat.iconEdit)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="ViewResultsFace")

        with allure.step("Chỉnh sửa thông tin Công dân"):
            page_guong_mat.do_dien_thong_tin_cong_dan(Data_Edit)
            page_guong_mat.do_bo_sung_them_tt_cong_dan(Data_Edit)
            time.sleep(4)
            capture_screenshot_and_attach_allure(driver, name="EditBSX")

        with allure.step("Kiểm tra cảnh báo khi upload hình ảnh không hợp lệ"):
            allure.attach(driver.get_screenshot_as_png(), name="NotifySuccess",
                          attachment_type=allure.attachment_type.PNG)
            check_notify = page_common.verify_notify_field_required(text_notify)
            assert check_notify, "Không có cảnh báo (hoặc cảnh báo không chính xác) khi upload hình ảnh không hợp lệ"

    @allure.testcase("c4i2-739", "c4i2-739")
    @allure.story("Chỉnh sửa Gương mặt trong thư viện không thành công")
    @allure.title("Chỉnh sửa công dân với dữ liệu CMND/CCCD/Hộ chiếu đã tồn tại trong hệ thống")
    @pff.parametrize(pathDataTestFS)
    def test_EditFaceCMNDExist(self, browser, create_data, clean_data, Data, Data_Edit, desc):
        f"""Trường hợp kiểm thử Chỉnh sửa Công dân không thành công - {desc}"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_guong_mat = PageGuongMat(driver)
        page_base.show_overlay_text(
            "Trường hợp kiểm thử Chỉnh sửa thông tin Công dân không thành công - chỉnh sửa CMND/CCCD/Hộ chiếu đã tồn tại trong hệ thống")
        attach_table_to_allure(Data, name="Initial Data")
        attach_table_to_allure(Data_Edit, name="Data for Editing")
        with allure.step("Tìm kiếm Công dân"):
            time.sleep(2)
            label_search = "CMND/ CCCD/ Hộ chiếu"
            json_data_handler = JsonDataHandler(Data)
            id_guong_mat = json_data_handler.get_value_by_label(label_search)

            page_base.send_key_input(Obj_GuongMat.txtSearchID, id_guong_mat)
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="FindFace")
            check_exit_in_pop_up = page_base.check_element_visibility(Obj_GuongMat.iconEdit)
            assert check_exit_in_pop_up, "Không trả về kết quả tìm kiếm trên danh sách lưới !"

        with allure.step("Nhấn chỉnh sửa kết quả tìm thấy trên danh sách lưới"):
            time.sleep(2)
            page_base.click_obj(Obj_GuongMat.iconEdit)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="ViewResultsFace")

        with allure.step("Chỉnh sửa thông tin Công dân"):
            page_guong_mat.do_dien_thong_tin_cong_dan(Data_Edit)
            page_guong_mat.do_bo_sung_them_tt_cong_dan(Data_Edit)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="EditBSX")

        with allure.step("Kiểm tra thông báo khi chỉnh sửa thông tin CMND/CCCD/Hộ chiếu đã tồn tại"):
            page_base.click_obj(Obj_GuongMat.btnCapNhatFace)
            time.sleep(1)
            text_notify = "CMND/ CCCD/ Hộ chiếu này đã tồn tại"
            check_notify = page_common.verify_notify_error(text_notify)
            allure.attach(driver.get_screenshot_as_png(), name="NotifySuccess",
                          attachment_type=allure.attachment_type.PNG)
            assert check_notify, "Không có thông báo khi chỉnh sửa CMND / CCCD / Hộ chiếu đã tồn tại"


@allure.epic("Nhận dạng gương mặt")
@allure.feature("Thư viện Gương mặt")
@pytest.mark.FS
@pytest.mark.Add_DataList
class Test_Delete_Face:

    @pytest.mark.DC
    @pytest.mark.UAT_DC
    @allure.testcase("c4i2-342", "c4i2-342")
    @allure.story("Xóa Gương mặt trong thư viện thành công")
    @allure.title("c4i2-342: Nhấn xác nhận xóa công dân")
    @pff.parametrize(pathDataTestFS)
    def test_DeleteFaceSuccess(self, browser, create_data, Data):
        """Trường hợp kiểm thử xóa Công dân đã tạo thành công"""
        driver = browser
        page_base = PageBase(driver)
        page_common = PageCommon(driver)
        page_base.show_overlay_text("Trường hợp kiểm thử xóa Công dân đã tạo thành công")
        attach_table_to_allure(Data)
        with allure.step("Tìm kiếm Face muốn xóa"):
            time.sleep(2)
            label_search = "CMND/ CCCD/ Hộ chiếu"
            json_data_handler = JsonDataHandler(Data)
            id_guong_mat = json_data_handler.get_value_by_label(label_search)

            page_base.send_key_input(Obj_GuongMat.txtSearchID, id_guong_mat)
            page_base.click_obj(Obj_GuongMat.btnTimKiem)
            capture_screenshot_and_attach_allure(driver, name="FindFace")

        with allure.step("Tick kết quả đầu tiên"):
            time.sleep(3)
            page_base.click_obj(Obj_GuongMat.checkboxFace)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="CheckResultFace")

        with allure.step("Nhấn xóa"):
            page_base.click_obj(Obj_GuongMat.btnDelete)
            time.sleep(2)
            capture_screenshot_and_attach_allure(driver, name="DeleteFace")

        with allure.step("Xác nhận xóa"):
            page_base.click_obj(Obj_GuongMat.btnXacNhan)
            time.sleep(1)
            capture_screenshot_and_attach_allure(driver, name="ConfirmDeleteBSX")
            check_popup = page_common.verify_notify_popup('Xóa thành công')
            assert check_popup, "Không nhận được thông báo xóa thông tin công dân thành công"
